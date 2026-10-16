#!/usr/bin/env python3
"""Actual recorded AF state in the complete reference heat/source interface."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "02_REGISTRY/research/sources/d0_native_archive_occupation_2026-10-15"
sys.path.insert(0, str(SOURCE))

from archive_occupation import run_checks


if __name__ == "__main__":
    print(json.dumps(run_checks(ROOT), sort_keys=True))
