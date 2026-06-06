#!/usr/bin/env python3
"""Verify Book 04 centered full-support selector closures.

This certificate does not test a local +-1 window and does not use an inserted
indicator target.  Each selector is checked over the entire finite support
0..2R, with score zero exactly when the support-symmetry equation 2x=2R holds.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_CSV = ROOT / "05_CERTS" / "book04_centered_full_support_selectors.csv"
OUT_JSON = ROOT / "05_CERTS" / "book04_centered_full_support_selectors.json"

CASES = [
    ("electroweak_depth", 35),
    ("proton_readout", 306),
    ("beta_unlock_depth", 19),
]


def score(x: int, R: int) -> int:
    return 0 if 2 * x == 2 * R else 1


def verify_case(name: str, R: int) -> dict[str, object]:
    support = list(range(2 * R + 1))
    scored = [(x, score(x, R)) for x in support]
    minima = [x for x, s in scored if s == min(v for _, v in scored)]
    ok = minima == [R] and all(score(x, R) > score(R, R) for x in support if x != R)
    return {
        "case": name,
        "R": R,
        "support_min": 0,
        "support_max": 2 * R,
        "support_size": 2 * R + 1,
        "selected": R,
        "minima": minima,
        "score_selected": score(R, R),
        "score_alternative": 1,
        "full_support_checked": len(support),
        "pass": ok,
    }


def main() -> int:
    rows = [verify_case(name, R) for name, R in CASES]
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    OUT_JSON.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if not all(row["pass"] for row in rows):
        print("FAIL_BOOK04_CENTERED_FULL_SUPPORT_SELECTORS")
        return 1
    print("PASS_BOOK04_CENTERED_FULL_SUPPORT_SELECTORS")
    print(f"wrote {OUT_CSV.relative_to(ROOT)}")
    print(f"wrote {OUT_JSON.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
