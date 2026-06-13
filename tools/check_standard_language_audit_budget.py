#!/usr/bin/env python3
"""Guard the standard-language rewrite budget."""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "06_AUDIT" / "standard_language_audit.csv"
MAX_FLAGGED = 125


def main() -> int:
    subprocess.run([sys.executable, str(ROOT / "tools" / "audit_standard_language_terms.py")], cwd=ROOT, check=True)
    with CSV.open(encoding="utf-8", newline="") as f:
        flagged = [row for row in csv.DictReader(f) if row["classification"] == "NEEDS_STANDARD_REWRITE"]
    count = len(flagged)
    if count > MAX_FLAGGED:
        print(f"FAIL_STANDARD_LANGUAGE_AUDIT_BUDGET flagged={count} max={MAX_FLAGGED}")
        return 1
    print(f"PASS_STANDARD_LANGUAGE_AUDIT_BUDGET flagged={count} max={MAX_FLAGGED}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
