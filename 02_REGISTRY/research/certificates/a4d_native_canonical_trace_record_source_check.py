#!/usr/bin/env python3
"""Narrow actual canonical-record source consumer; no old suite or receipt."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "02_REGISTRY/research/sources/d0_canonical_trace_record_source_2026-10-15"))

from canonical_source import run_checks


if __name__ == "__main__":
    print(json.dumps(run_checks(ROOT), sort_keys=True))
