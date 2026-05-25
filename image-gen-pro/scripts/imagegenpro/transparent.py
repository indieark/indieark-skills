from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from .artifacts import sha256_file, write_json
from .errors import UsageError


DEFAULT_TOLERANCE = 36
DEFAULT_SOFT_RANGE = 18
EDGE_CLEANUP_CHOICES = {"rgb-unmix-despill", "none"}
OPAQUE_BACKGROUND_ALPHA_MIN = 250


def make_transparent(args) -> dict[str, Any]:
    source = Path(args.input)
    output = Path(args.output)
    metadata_file = Path(args.metadata_file) if args.metadata_file else _default_metadata_path(output)
    preview_file = Path(args.preview_file) if args.preview_file else None

    if not source.exists() or not source.is_file():
        raise UsageError(f"--input must be an existing image file: {source}")
    if output.resolve() == source.resolve():
        raise UsageError("--output must not overwrite --input")
    if output.suffix.lower() != ".png":
        raise UsageError("--output must end in .png for transparent output")
    if metadata_file.resolve() == source.resolve() or metadata_file.resolve() == output.resolve():
        raise UsageError("--metadata-file must not overwrite input or output image")
    if args.tolerance < 0:
        raise UsageError("--tolerance must be >= 0")
    if args.soft_range < 1:
        raise UsageError("--soft-range must be >= 1")
    if args.edge_cleanup not in EDGE_CLEANUP_CHOICES:
        raise UsageError("--edge-cleanup must be one of: rgb-unmix-despill, none")
    if args.min_island_area < 0:
        raise UsageError("--min-island-area must be >= 0")
    if args.edge_decontaminate_strength < 0 or args.edge_decontaminate_strength > 1:
        raise UsageError("--edge-decontaminate-strength must be between 0 and 1")

    try:
        from PIL import Image
    except Exception as exc:
        raise UsageError("Pillow is required for transparent output. Install it with: python -m pip install Pillow") from exc

    try:
        with Image.open(source) as image:
            image.load()
            rgba = image.convert("RGBA")
    except Exception as exc:
        raise UsageError(f"image file cannot be opened for transparent output: {source}") from exc

    background = _resolve_background(args.background, rgba)
    result = _apply_transparency(
        rgba,
        background["rgb"],
        tolerance=args.tolerance,
        soft_range=args.soft_range,
        edge_cleanup=args.edge_cleanup,
        min_island_area=args.min_island_area,
        edge_decontaminate_strength=args.edge_decontaminate_strength,
    )
    processed = result["image"]
    stats = result["stats"]
    output.parent.mkdir(parents=True, exist_ok=True)
    processed.save(output, format="PNG", optimize=True)

    preview = None
    if preview_file:
        preview_file.parent.mkdir(parents=True, exist_ok=True)
        _checkerboard_preview(processed).save(preview_file, format="PNG", optimize=True)
        preview = {
            "path": str(preview_file),
            "size_bytes": preview_file.stat().st_size,
            "sha256": sha256_file(preview_file),
        }

    alpha_bbox = processed.getchannel("A").getbbox()
    metadata = {
        "schema": "image-gen-pro.transparent-output.v1",
        "transparent_output": True,
        "transparency_source": "generated_chroma_background_plus_postprocess",
        "input": {
            "path": str(source),
            "size_bytes": source.stat().st_size,
            "sha256": sha256_file(source),
            "width": rgba.width,
            "height": rgba.height,
        },
        "output": {
            "path": str(output),
            "format": "png",
            "size_bytes": output.stat().st_size,
            "sha256": sha256_file(output),
            "width": processed.width,
            "height": processed.height,
        },
        "background": {
            "mode": args.background,
            "detected": _hex(background["rgb"]),
            "sample_count": background["sample_count"],
        },
        "alpha": {
            "tolerance": args.tolerance,
            "soft_range": args.soft_range,
            "alpha_changed": True,
            "bbox_before_cleanup": list(stats["alpha_bbox_before_cleanup"]) if stats["alpha_bbox_before_cleanup"] else None,
            "bbox": list(alpha_bbox) if alpha_bbox else None,
            "bbox_changed_by_cleanup": stats["alpha_bbox_before_cleanup"] != alpha_bbox,
            "background_like_cleanup_tolerance": stats["background_like_cleanup_tolerance"],
            "removed_background_like_pixels": stats["removed_background_like_pixels"],
            "min_island_area": args.min_island_area,
            "removed_island_pixels": stats["removed_island_pixels"],
        },
        "edge_cleanup": args.edge_cleanup,
        "edge_cleanup_details": {
            "mode": args.edge_cleanup,
            "rgb_only": True,
            "alpha_preserved_after_rgb_cleanup": True,
            "edge_decontaminate_strength": args.edge_decontaminate_strength,
            "rgb_unmixed_pixels": stats["rgb_unmixed_pixels"],
            "rgb_decontaminated_pixels": stats["rgb_decontaminated_pixels"],
        },
        "preview": preview,
        "warnings": [],
    }
    write_json(metadata_file, metadata)
    summary = {
        "schema": "image-gen-pro.transparent-summary.v1",
        "ok": True,
        "command": "transparent",
        "input": str(source),
        "output": str(output),
        "metadata_file": str(metadata_file),
        "preview_file": str(preview_file) if preview_file else None,
        "transparent_output": True,
        "transparency_source": metadata["transparency_source"],
        "background": metadata["background"],
        "alpha": metadata["alpha"],
        "edge_cleanup": args.edge_cleanup,
        "edge_cleanup_details": metadata["edge_cleanup_details"],
    }
    return summary


def _default_metadata_path(output: Path) -> Path:
    return output.with_suffix(".metadata.json")


def _resolve_background(raw: str, image) -> dict[str, Any]:
    if raw == "auto":
        samples = _background_samples(image)
        return {"rgb": _median_rgb(samples), "sample_count": len(samples)}
    return {"rgb": _parse_hex_color(raw), "sample_count": 0}


def _parse_hex_color(raw: str) -> tuple[int, int, int]:
    value = raw.strip()
    if value.startswith("#"):
        value = value[1:]
    if len(value) != 6:
        raise UsageError("--background must be auto or a #rrggbb color")
    try:
        return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)
    except ValueError as exc:
        raise UsageError("--background must be auto or a #rrggbb color") from exc


def _background_samples(image) -> list[tuple[int, int, int]]:
    width, height = image.size
    pixels = image.load()
    band = max(1, min(width, height, 24) // 12)
    samples: list[tuple[int, int, int]] = []
    for y in range(height):
        for x in range(width):
            in_corner = (x < band or x >= width - band) and (y < band or y >= height - band)
            in_edge = x == 0 or y == 0 or x == width - 1 or y == height - 1
            if in_corner or in_edge:
                r, g, b, _a = pixels[x, y]
                samples.append((r, g, b))
    if not samples:
        raise UsageError("cannot estimate background from an empty image")
    return samples


def _median_rgb(samples: list[tuple[int, int, int]]) -> tuple[int, int, int]:
    channels = []
    for index in range(3):
        values = sorted(sample[index] for sample in samples)
        channels.append(values[len(values) // 2])
    return channels[0], channels[1], channels[2]


def _apply_transparency(
    image,
    background: tuple[int, int, int],
    *,
    tolerance: int,
    soft_range: int,
    edge_cleanup: str,
    min_island_area: int,
    edge_decontaminate_strength: float,
) -> dict[str, Any]:
    processed = image.copy()
    pixels = processed.load()
    for y in range(processed.height):
        for x in range(processed.width):
            r, g, b, original_alpha = pixels[x, y]
            distance = _rgb_distance((r, g, b), background)
            alpha = _alpha_for_distance(distance, tolerance, soft_range)
            alpha = min(original_alpha, alpha)
            pixels[x, y] = (r, g, b, alpha)

    alpha_bbox_before_cleanup = processed.getchannel("A").getbbox()
    cleanup_tolerance = _background_like_cleanup_tolerance(tolerance, soft_range)
    removed_background_like_pixels = _remove_background_like_alpha_pixels(
        processed,
        background,
        cleanup_tolerance=cleanup_tolerance,
    )
    removed_island_pixels = 0
    if min_island_area > 0:
        removed_island_pixels = _remove_small_alpha_islands(processed, min_area=min_island_area)
    rgb_stats = {"rgb_unmixed_pixels": 0, "rgb_decontaminated_pixels": 0}
    if edge_cleanup == "rgb-unmix-despill":
        rgb_stats = _decontaminate_background_spill_rgb(
            processed,
            background,
            tolerance=tolerance,
            soft_range=soft_range,
            cleanup_tolerance=cleanup_tolerance,
            strength=edge_decontaminate_strength,
        )

    return {
        "image": processed,
        "stats": {
            "alpha_bbox_before_cleanup": alpha_bbox_before_cleanup,
            "background_like_cleanup_tolerance": cleanup_tolerance,
            "removed_background_like_pixels": removed_background_like_pixels,
            "removed_island_pixels": removed_island_pixels,
            **rgb_stats,
        },
    }


def _background_like_cleanup_tolerance(tolerance: int, soft_range: int) -> int:
    base = tolerance + soft_range
    return min(220, max(base + 45, int(base * 2.4)))


def _remove_background_like_alpha_pixels(image, background: tuple[int, int, int], *, cleanup_tolerance: int) -> int:
    pixels = image.load()
    removed = 0
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, alpha = pixels[x, y]
            if alpha < OPAQUE_BACKGROUND_ALPHA_MIN:
                continue
            if _rgb_distance((r, g, b), background) <= cleanup_tolerance:
                pixels[x, y] = (r, g, b, 0)
                removed += 1
    return removed


def _remove_small_alpha_islands(image, *, min_area: int) -> int:
    alpha = image.getchannel("A")
    width, height = alpha.size
    alpha_values = list(alpha.getdata())
    visited = bytearray(width * height)
    removed = 0

    for start in range(width * height):
        if visited[start] or alpha_values[start] == 0:
            continue
        stack = [start]
        visited[start] = 1
        component: list[int] = []
        while stack:
            index = stack.pop()
            component.append(index)
            x = index % width
            y = index // width
            for next_index in _neighbor_indices(x, y, width, height):
                if visited[next_index] or alpha_values[next_index] == 0:
                    continue
                visited[next_index] = 1
                stack.append(next_index)
        if len(component) < min_area:
            for index in component:
                if alpha_values[index] != 0:
                    alpha_values[index] = 0
                    removed += 1

    if removed:
        alpha.putdata(alpha_values)
        image.putalpha(alpha)
    return removed


def _neighbor_indices(x: int, y: int, width: int, height: int):
    if x > 0:
        yield y * width + (x - 1)
    if x + 1 < width:
        yield y * width + (x + 1)
    if y > 0:
        yield (y - 1) * width + x
    if y + 1 < height:
        yield (y + 1) * width + x


def _decontaminate_background_spill_rgb(
    image,
    background: tuple[int, int, int],
    *,
    tolerance: int,
    soft_range: int,
    cleanup_tolerance: int,
    strength: float,
) -> dict[str, int]:
    pixels = image.load()
    alpha_values = list(image.getchannel("A").getdata())
    edge_pixels = _edge_pixel_indices(alpha_values, image.width, image.height)
    rgb_unmixed = 0
    rgb_decontaminated: set[int] = set()
    bg_like_distance = max(150, cleanup_tolerance + 20, tolerance + soft_range + 55)

    for y in range(image.height):
        for x in range(image.width):
            index = y * image.width + x
            r, g, b, alpha = pixels[x, y]
            if alpha <= 0:
                continue
            if 0 < alpha < 255:
                r, g, b = _unmix_rgb((r, g, b), background, alpha)
                rgb_unmixed += 1
                rgb_decontaminated.add(index)

            edge = index in edge_pixels
            distance = _rgb_distance((r, g, b), background)
            bg_like = edge and distance <= bg_like_distance
            magenta_spill = edge and (r - g > 24) and (b - g > 24) and abs(r - b) < 96
            green_spill = edge and (g - r > 35) and (g - b > 25)
            if bg_like or magenta_spill or green_spill:
                spill_strength = max(strength, min(1.0, strength + 0.14)) if bg_like else strength
                r, g, b = _neutralize_rgb((r, g, b), spill_strength)
                rgb_decontaminated.add(index)
            pixels[x, y] = (r, g, b, alpha)

    return {
        "rgb_unmixed_pixels": rgb_unmixed,
        "rgb_decontaminated_pixels": len(rgb_decontaminated),
    }


def _edge_pixel_indices(alpha_values: list[int], width: int, height: int) -> set[int]:
    edge: set[int] = set()
    for index, alpha in enumerate(alpha_values):
        if alpha <= 0:
            continue
        if alpha < 255:
            edge.add(index)
            continue
        x = index % width
        y = index // width
        for next_index in _neighbor_indices_8(x, y, width, height):
            if alpha_values[next_index] == 0:
                edge.add(index)
                break
    return edge


def _neighbor_indices_8(x: int, y: int, width: int, height: int):
    for next_y in range(max(0, y - 1), min(height, y + 2)):
        for next_x in range(max(0, x - 1), min(width, x + 2)):
            if next_x == x and next_y == y:
                continue
            yield next_y * width + next_x


def _neutralize_rgb(pixel: tuple[int, int, int], strength: float) -> tuple[int, int, int]:
    r, g, b = pixel
    luma = (0.2126 * r) + (0.7152 * g) + (0.0722 * b)
    return (
        _clamp(round((r * (1 - strength)) + (luma * strength))),
        _clamp(round((g * (1 - strength)) + (luma * strength))),
        _clamp(round((b * (1 - strength)) + (luma * strength))),
    )


def _rgb_distance(pixel: tuple[int, int, int], background: tuple[int, int, int]) -> float:
    return math.sqrt(sum((pixel[index] - background[index]) ** 2 for index in range(3)))


def _alpha_for_distance(distance: float, tolerance: int, soft_range: int) -> int:
    if distance <= tolerance:
        return 0
    if distance >= tolerance + soft_range:
        return 255
    return round(((distance - tolerance) / soft_range) * 255)


def _unmix_rgb(pixel: tuple[int, int, int], background: tuple[int, int, int], alpha: int) -> tuple[int, int, int]:
    a = alpha / 255
    if a <= 0:
        return pixel
    values = []
    for index in range(3):
        value = (pixel[index] - ((1 - a) * background[index])) / a
        values.append(_clamp(round(value)))
    return values[0], values[1], values[2]


def _clamp(value: int) -> int:
    return max(0, min(255, value))


def _checkerboard_preview(image):
    try:
        from PIL import Image
    except Exception as exc:
        raise UsageError("Pillow is required for preview rendering") from exc
    tile = 16
    preview = Image.new("RGBA", image.size, (255, 255, 255, 255))
    pixels = preview.load()
    for y in range(preview.height):
        for x in range(preview.width):
            shade = 224 if ((x // tile) + (y // tile)) % 2 == 0 else 176
            pixels[x, y] = (shade, shade, shade, 255)
    preview.alpha_composite(image)
    return preview.convert("RGB")


def _hex(rgb: tuple[int, int, int]) -> str:
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
