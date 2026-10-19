#!/usr/bin/env python3
"""Exact control: the same good compression has basis-dependent full entropy."""
from __future__ import annotations

import hashlib
import json
from itertools import combinations
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[4]
PINS = {
    "02_REGISTRY/research/sources/d0_exterior_mean_entropy_2026-10-19/check_exterior_mean_source.py":
        "56bda572b4156bbafbb0b4b0985f8014497fbde47d9b3963b3d5b52930cbeef6",
    "02_REGISTRY/research/sources/d0_exterior_mean_entropy_2026-10-19/RESULT.json":
        "6076080dcb366af20ecbaa8825357e555226b16e482d2d47426244bfc82ef175",
}


def run() -> dict:
    checks: list[str] = []

    def ck(name: str, condition: bool) -> None:
        if not bool(condition):
            raise ArithmeticError(name)
        checks.append(name)

    input_hashes = {}
    for rel, expected in PINS.items():
        actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        ck("pinned " + Path(rel).name, actual == expected)
        input_hashes[rel] = actual

    # Two exact unitary completions of the same 2x2 good compression K.
    a, b = sp.Rational(9, 16), sp.Rational(1, 4)
    k = sp.diag(sp.sqrt(a), sp.sqrt(b))
    s = sp.diag(sp.sqrt(1 - a), sp.sqrt(1 - b))
    identity = sp.eye(2)
    hadamard = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
    v_polar = k.col_join(identity * s)
    v_rotated = k.col_join(hadamard * s)

    ck("both completions preserve the same good compression", v_polar[:2, :] == v_rotated[:2, :])
    ck("polar completion is an isometry", sp.simplify(v_polar.T * v_polar) == sp.eye(2))
    ck("Hadamard failure completion is an isometry",
       sp.simplify(v_rotated.T * v_rotated) == sp.eye(2))

    def occupation_law(v: sp.Matrix) -> list[sp.Expr]:
        masses = []
        for rows in combinations(range(4), 2):
            amplitude = sp.simplify(v.extract(rows, [0, 1]).det())
            masses.append(sp.simplify(amplitude * sp.conjugate(amplitude)))
        return masses

    polar = occupation_law(v_polar)
    rotated = occupation_law(v_rotated)
    expected_polar = [sp.Rational(9, 64), 0, sp.Rational(27, 64),
                      sp.Rational(7, 64), 0, sp.Rational(21, 64)]
    expected_rotated = [sp.Rational(9, 64), sp.Rational(27, 128),
                        sp.Rational(27, 128), sp.Rational(7, 128),
                        sp.Rational(7, 128), sp.Rational(21, 64)]
    ck("all six polar occupation outcomes retained exactly",
       all(sp.simplify(x - y) == 0 for x, y in zip(polar, expected_polar)))
    ck("all six rotated occupation outcomes retained exactly",
       all(sp.simplify(x - y) == 0 for x, y in zip(rotated, expected_rotated)))
    ck("both complete laws normalize",
       sp.simplify(sum(polar) - 1) == 0 and sp.simplify(sum(rotated) - 1) == 0)

    x, y = sp.symbols("x y", positive=True)

    def entropy(masses: list[sp.Expr]) -> sp.Expr:
        return -sum(q * sp.log(q) for q in masses if q != 0)

    polar_entropy = entropy([x * y, x * (1 - y), (1 - x) * y, (1 - x) * (1 - y)])
    rotated_entropy = entropy([
        x * y,
        x * (1 - y) / 2,
        x * (1 - y) / 2,
        (1 - x) * y / 2,
        (1 - x) * y / 2,
        (1 - x) * (1 - y),
    ])
    entropy_gap = sp.expand_log(rotated_entropy - polar_entropy, force=True)
    expected_gap = (x * (1 - y) + (1 - x) * y) * sp.log(2)
    ck("general entropy shift has exact closed form",
       sp.simplify(entropy_gap - expected_gap) == 0)
    source_gap = sp.simplify(sp.diff(expected_gap, x).subs(y, b))
    ck("same K has a nonzero first-source shift", source_gap == sp.log(2) / 2)

    # The second golden block is above one half, so the source shift remains
    # nonzero for a Q-block variation at the actual golden base point.
    p = (sp.sqrt(5) - 1) / 2
    r = p ** 3 / 4
    w0 = 1 - p ** 6
    q0 = 1 - r * 4 * p ** 3
    r0 = 1 - r * (1 - p ** 12)
    a_q, a_r = sp.simplify((w0 * q0) ** 2), sp.simplify((w0 * r0) ** 2)
    golden_source_gap = sp.simplify((1 - 2 * a_r) * sp.log(2))
    ck("golden failure-basis source gap is nonzero",
       sp.simplify(1 - 2 * a_r) != 0 and float(sp.N(a_r, 30)) > 0.5)

    return {
        "status": "PASS_SAME_COMPRESSION_BASIS_AMBIGUITY",
        "check_count": len(checks),
        "checks": checks,
        "input_sha256": input_hashes,
        "finite_control": {
            "good_compression": [["3/4", "0"], ["0", "1/2"]],
            "polar_occupation_probabilities": [str(q) for q in polar],
            "hadamard_failure_completion_probabilities": [str(q) for q in rotated],
            "entropy_gap_exact": "17*log(2)/32",
            "entropy_gap_first_derivative_wrt_a_exact": "log(2)/2 at b=1/4",
        },
        "golden_control": {
            "a_Q": str(a_q),
            "a_R": str(a_r),
            "dH_gap_for_DaQ": "(1-2*a_R)*log(2)*Da_Q",
            "coefficient_value": str(sp.N(golden_source_gap, 16)),
        },
        "scope": "Two valid complete isometries with identical good compression have different full occupation laws and different Shannon first sources. This does not show both completions are native-admissible; it shows the compression alone does not select the polar readout basis or its mean entropy.",
    }


def main() -> None:
    result = run()
    result["checker_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
