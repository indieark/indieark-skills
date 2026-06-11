#!/usr/bin/env python3
"""Primary Video Gen Pro CLI entry point.

The implementation currently lives in the ``seedance2/`` provider adapter
package next to this file. Public wrappers should call this shim as
``videogen``; ``video-gen-pro`` and ``seedance2`` remain compatibility wrappers.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from seedance2.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
