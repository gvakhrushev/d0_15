#!/usr/bin/env python3
"""Exact algebraic bridge between the golden scale and owned memory source."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[3]
PINS = {
    "02_REGISTRY/research/A4D_NATIVE_CLOSED_RECORD_ENGINE.md":
        "36eaeb8617630acaeace297fa64e7b8c33b92fc4824133a2b8e3515c4c79520a",
    "02_REGISTRY/research/A4D_NATIVE_MEMORY_SOURCE_FIBRE.md":
        "37d31c0e3ab9ebfd4e60a105913f46b1c959f97e1be9b0c339a12dc8ce31b014",
    "02_REGISTRY/research/sources/d0_native_memory_source_2026-10-16/result.json":
        "51c2e602f6915df1726eb108b3b22f11745d097ed6e4b7dcf09294573d561e5d",
}
CHECK_COUNT = 0


def require(condition: bool, label: str) -> None:
    global CHECK_COUNT
    CHECK_COUNT += 1
    if not condition:
        raise ArithmeticError("golden_memory_source_alignment:" + label)


def main() -> None:
    for rel, expected in PINS.items():
        actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        require(actual == expected, "source_pin:" + rel)

    sqrt5 = sp.sqrt(5)
    phi = (1 + sqrt5) / 2
    p = phi - 1
    r = 2 * p - 1
    delta0 = r / 2
    a0 = phi - 1
    b0 = 2 - phi

    require(sp.simplify(p + p**2 - 1) == 0, "golden_recurrence")
    require(sp.simplify(1 / phi - p) == 0, "p_is_inverse_phi")
    require(sp.simplify(a0 - p) == 0 and sp.simplify(b0 - p**2) == 0,
            "user_split_is_p_and_p_squared")
    require(sp.simplify(delta0 - (a0 - b0) / 2) == 0,
            "distinguishability_quantum")
    require(sp.simplify(r - sqrt5 + 2) == 0, "native_return_coordinate")
    require(sp.simplify(r * phi**3 - 1) == 0, "r_is_phi_minus_three")
    require(sp.simplify(r - p**3) == 0, "return_is_golden_cubic")
    require(sp.simplify(2 - 3 * p - p**4) == 0, "reversed_path_source")
    require(sp.simplify((2 - 3 * p) / p - p**3) == 0,
            "same_endpoint_source_ratio")

    for dimension in range(1, 9):
        q = 2 * delta0 * phi ** (dimension - 1)
        require(sp.simplify(q - phi ** (dimension - 4)) == 0,
                "dimension_scale:" + str(dimension))

    for n in range(2, 18):
        require(sp.simplify(
            sp.chebyshevt(n + 1, r)
            - 2 * r * sp.chebyshevt(n, r)
            + sp.chebyshevt(n - 1, r)
        ) == 0, "chebyshev_recurrence:" + str(n))

    non_golden = sp.Rational(1, 2)
    require(sp.simplify(non_golden**3 - (2 * non_golden - 1)) != 0,
            "reject_non_golden_parameter_mutation")
    require(sp.simplify(non_golden + non_golden**2 - 1) != 0,
            "reject_mutated_golden_equation")

    print(json.dumps({
        "schema": "d0-golden-memory-source-alignment/1",
        "status": "PASS_EXACT_GOLDEN_MEMORY_ALIGNMENT",
        "exact_checks": CHECK_COUNT,
        "dimension_scales_checked": list(range(1, 9)),
        "chebyshev_orders_checked": list(range(3, 19)),
        "path_source_ratio": "p^3 = 2*p-1 = phi^-3 = Q(1)",
        "non_golden_mutation": "REJECTED",
        "input_sha256": PINS,
        "scope": "conditional v8 source/readout bridge only; no refinement, physical admission or GR claim",
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
