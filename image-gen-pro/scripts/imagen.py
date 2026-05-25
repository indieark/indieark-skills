from __future__ import annotations

import sys
from pathlib import Path


def _bootstrap() -> None:
    here = Path(__file__).resolve().parent
    if str(here) not in sys.path:
        sys.path.insert(0, str(here))


def main() -> int:
    _bootstrap()
    from imagegenpro.cli import main as cli_main

    return cli_main()


if __name__ == "__main__":
    raise SystemExit(main())
