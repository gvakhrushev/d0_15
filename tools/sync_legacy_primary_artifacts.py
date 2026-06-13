#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY_ROOT = ROOT / "05_CERTS" / "ported_legacy_primary"
OUT = ROOT / "05_CERTS" / "PORTED_LEGACY_PRIMARY_ARTIFACTS.csv"


def main() -> int:
    rows = []
    for path in sorted(LEGACY_ROOT.rglob("*.py")):
        claim_id = path.parent.name
        rows.append(
            {
                "Claim_ID": claim_id,
                "Artifact": path.name,
                "Status": "PORTED",
                "Path": path.relative_to(ROOT).as_posix(),
            }
        )

    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Claim_ID", "Artifact", "Status", "Path"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
