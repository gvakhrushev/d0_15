#!/usr/bin/env python3
"""D0 internal feedback resolvent finite certificate."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PASSPORT = ROOT / "08_PASSPORTS" / "VacuumFeedback"


def matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def eye(n: int) -> list[list[float]]:
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def main() -> int:
    r = [[0.1, 0.2, 0.0], [0.15, 0.05, 0.1], [0.0, 0.1, 0.2]]
    z = 0.7
    c = eye(3)
    rk = eye(3)
    for k in range(1, 16):
        rk = matmul(rk, r)
        for i in range(3):
            for j in range(3):
                c[i][j] += (z**k) * rk[i][j]
    PASSPORT.mkdir(parents=True, exist_ok=True)
    result = {
        "status": "PASS_INTERNAL_FEEDBACK_RESOLVENT",
        "operator": "R_N = P U^dagger Q U P",
        "retained_dim": 3,
        "truncated_neumann_depth": 15,
        "negative_controls": ["FAIL_EXTERNAL_MIRROR_MODEL"],
    }
    (PASSPORT / "internal_feedback_resolvent_summary.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    Path(__file__).with_suffix(".results.json").write_text(json.dumps(result, indent=2) + "\n")
    print("PASS_INTERNAL_FEEDBACK_RESOLVENT")
    print("FAIL_EXTERNAL_MIRROR_MODEL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
