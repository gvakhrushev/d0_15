#!/usr/bin/env python3
"""Narrow exact amplitude-source budget; immutable owners are only imported."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "02_REGISTRY/research/sources/d0_amplitude_source_regularity_2026-10-15"
sys.path.insert(0, str(SOURCE))

from jet_budget import run_checks


if __name__ == "__main__":
    print(json.dumps(run_checks(ROOT), sort_keys=True))
