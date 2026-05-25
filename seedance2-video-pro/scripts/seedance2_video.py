#!/usr/bin/env python3
"""Entry-point shim — keeps ``python scripts/seedance2_video.py`` working.

The implementation lives in the ``seedance2/`` package next to this file.
Run ``python -m seedance2`` for the same effect once this directory is on sys.path.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from seedance2.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
