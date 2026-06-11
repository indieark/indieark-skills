#!/usr/bin/env python3
"""Legacy entry-point shim for existing ``seedance2`` callers.

The primary CLI shim is ``video_gen_pro.py`` and public wrappers should expose
it as ``videogen``. This file intentionally remains so old scripts that call
``python scripts/seedance2_video.py`` keep working during the compatibility
period.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from seedance2.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
