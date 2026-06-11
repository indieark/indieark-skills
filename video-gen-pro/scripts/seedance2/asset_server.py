"""Optional local reference_video serving for private media experiments."""

from __future__ import annotations

import argparse
import contextlib
import http.server
import os
import queue
import re
import shutil
import socket
import subprocess
import threading
import time
from pathlib import Path

from seedance2.artifacts import resolve_run_dir
from seedance2.constants import EXIT_USAGE
from seedance2.errors import SeedanceError
from seedance2.http import is_http_url
from seedance2.media_probe import local_media_metadata

TUNNEL_PATTERN = re.compile(r"https://[a-zA-Z0-9.-]+\.trycloudflare\.com")


@contextlib.contextmanager
def maybe_serve_local_assets(args: argparse.Namespace):
    mode = getattr(args, "serve_local_assets", "none")
    if mode in (None, "none"):
        yield None
        return
    if mode != "cloudflare":
        raise SeedanceError(f"unsupported asset server: {mode}", code=EXIT_USAGE)

    sources = _local_media_sources(args)
    if not sources:
        yield None
        return
    cloudflared_bin = os.environ.get("SEEDANCE_CLOUDFLARED_BIN", "cloudflared")
    if not shutil.which(cloudflared_bin):
        raise SeedanceError(
            "cloudflared is required for --serve-local-assets cloudflare; "
            "run `winget install Cloudflare.cloudflared`, provide an HTTPS/signed "
            "video URL, or use asset:// media",
            code=EXIT_USAGE,
            payload={
                "install": "winget install Cloudflare.cloudflared",
                "required_when": "local reference_video needs a temporary HTTPS URL",
                "alternatives": [
                    "provide an HTTPS/signed video URL",
                    "use asset:// media",
                ],
            },
        )

    run_dir = resolve_run_dir(args)
    assets_dir = run_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    mapping = _copy_assets(sources, assets_dir)

    httpd = _ThreadedHttpServer(assets_dir)
    httpd.start()
    tunnel = _CloudflareTunnel(httpd.url)
    try:
        public_base = tunnel.start()
        _rewrite_args(args, mapping, public_base)
        yield {
            "local_url": httpd.url,
            "public_url": public_base,
            "asset_dir": str(assets_dir),
            "files": [
                {
                    "source": source,
                    "served_name": served_name,
                    "url": f"{public_base}/{served_name}",
                    "metadata": local_media_metadata(source),
                }
                for source, served_name in mapping.items()
            ],
        }
    finally:
        tunnel.stop()
        httpd.stop()


def _local_media_sources(args: argparse.Namespace) -> list[str]:
    sources: list[str] = []
    for source in getattr(args, "reference_video", None) or []:
        if _is_local_file(source):
            sources.append(source)
    return sources


def _is_local_file(source: str) -> bool:
    return not (
        is_http_url(source)
        or source.startswith(("data:", "asset://"))
        or not Path(source).expanduser().is_file()
    )


def _copy_assets(sources: list[str], assets_dir: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    used: set[str] = set()
    for index, source in enumerate(sources, start=1):
        path = Path(source).expanduser()
        stem = _safe_name(path.stem) or "asset"
        suffix = path.suffix.lower()
        name = f"{index:02d}-{stem}{suffix}"
        while name in used:
            name = f"{index:02d}-{stem}-{len(used)}{suffix}"
        used.add(name)
        shutil.copy2(path, assets_dir / name)
        mapping[source] = name
    return mapping


def _rewrite_args(args: argparse.Namespace, mapping: dict[str, str], public_base: str) -> None:
    def rewrite(source: str | None) -> str | None:
        if source in mapping:
            return f"{public_base}/{mapping[source]}"
        return source

    values = getattr(args, "reference_video", None)
    if values:
        setattr(args, "reference_video", [rewrite(value) for value in values])


def _safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-")


class _ThreadedHttpServer:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.port = _free_port()
        self.url = f"http://127.0.0.1:{self.port}"
        self._server = None
        self._thread = None

    def start(self) -> None:
        class QuietHandler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, format, *args) -> None:
                return

        handler = lambda *a, **kw: QuietHandler(*a, directory=str(self.root), **kw)
        self._server = http.server.ThreadingHTTPServer(("127.0.0.1", self.port), handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if self._server:
            self._server.shutdown()
            self._server.server_close()
        if self._thread:
            self._thread.join(timeout=5)


class _CloudflareTunnel:
    def __init__(self, local_url: str) -> None:
        self.local_url = local_url
        self.process: subprocess.Popen | None = None
        self.reader: threading.Thread | None = None
        self.output_queue: queue.Queue[str] = queue.Queue()
        self.lines: list[str] = []

    def start(self) -> str:
        self.process = subprocess.Popen(
            [
                os.environ.get("SEEDANCE_CLOUDFLARED_BIN", "cloudflared"),
                "tunnel",
                "--url",
                self.local_url,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self.reader = threading.Thread(target=self._read_output, daemon=True)
        self.reader.start()
        timeout = float(os.environ.get("SEEDANCE_CLOUDFLARED_TIMEOUT", "45"))
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self.process.poll() is not None:
                break
            try:
                line = self.output_queue.get(timeout=0.2)
                self.lines.append(line.strip())
                match = TUNNEL_PATTERN.search(line)
                if match:
                    return match.group(0).rstrip("/")
            except queue.Empty:
                continue
        self.stop()
        raise SeedanceError(
            "cloudflared tunnel did not produce a trycloudflare URL",
            code=EXIT_USAGE,
            payload={"cloudflared_output": self.lines[-20:]},
        )

    def _read_output(self) -> None:
        if not self.process or not self.process.stdout:
            return
        for line in self.process.stdout:
            self.output_queue.put(line)

    def stop(self) -> None:
        if not self.process:
            return
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()
        if self.reader:
            self.reader.join(timeout=2)
        self.process = None
        self.reader = None


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])
