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
    p = (sp.sqrt(5) - 1) / 2
    k = sp.diag(sp.sqrt(a), sp.sqrt(b))
    s = sp.diag(sp.sqrt(1 - a), sp.sqrt(1 - b))
    identity = sp.eye(2)
    golden_gate = sp.Matrix([[sp.sqrt(p), -p], [p, sp.sqrt(p)]])
    v_polar = k.col_join(identity * s)
    v_rotated = k.col_join(golden_gate * s)

    ck("both completions preserve the same good compression", v_polar[:2, :] == v_rotated[:2, :])
    ck("polar completion is an isometry", sp.simplify(v_polar.T * v_polar) == sp.eye(2))
    ck("golden-gate failure completion is an isometry",
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
    expected_rotated = [sp.Rational(9, 64), 27 * p ** 2 / 64,
                        27 * p / 64, 7 * p / 64,
                        7 * p ** 2 / 64, sp.Rational(21, 64)]
    ck("all six polar occupation outcomes retained exactly",
       all(sp.simplify(x - y) == 0 for x, y in zip(polar, expected_polar)))
    ck("all six golden-gate occupation outcomes retained exactly",
       all(sp.simplify(x - y) == 0 for x, y in zip(rotated, expected_rotated)))
    ck("both complete laws normalize",
       sp.simplify(sum(polar) - 1) == 0 and sp.simplify(sum(rotated) - 1) == 0)

    x, y = sp.symbols("x y", positive=True)

    def entropy(masses: list[sp.Expr]) -> sp.Expr:
        return -sum(q * sp.log(q) for q in masses if q != 0)

    polar_entropy = entropy([x * y, x * (1 - y), (1 - x) * y, (1 - x) * (1 - y)])
    u = sp.symbols("u", positive=True)
    rotated_entropy = entropy([
        x * y,
        x * (1 - y) * u,
        x * (1 - y) * (1 - u),
        (1 - x) * y * (1 - u),
        (1 - x) * y * u,
        (1 - x) * (1 - y),
    ])
    hgold = -p * sp.log(p) - p ** 2 * sp.log(p ** 2)
    hsplit = -u * sp.log(u) - (1 - u) * sp.log(1 - u)
    entropy_gap = sp.expand_log(rotated_entropy - polar_entropy, force=True)
    expected_gap = (x * (1 - y) + (1 - x) * y) * hsplit
    ck("general entropy shift has exact closed form",
       sp.simplify(entropy_gap - expected_gap) == 0)
    source_gap = sp.simplify(sp.diff(expected_gap, x).subs(y, b))
    ck("same K has a nonzero first-source shift",
       sp.simplify(source_gap - hsplit / 2) == 0)
    ck("golden gate split probabilities are p and p squared",
       sp.simplify(p + p ** 2 - 1) == 0)

    # The second golden block is above one half, so the source shift remains
    # nonzero for a Q-block variation at the actual golden base point.
    r = p ** 3 / 4
    w0 = 1 - p ** 6
    q0 = 1 - r * 4 * p ** 3
    r0 = 1 - r * (1 - p ** 12)
    a_q, a_r = sp.simplify((w0 * q0) ** 2), sp.simplify((w0 * r0) ** 2)
    golden_source_gap = sp.simplify((1 - 2 * a_r) * hgold)
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
            "golden_gate_failure_completion_probabilities": [str(q) for q in rotated],
            "entropy_gap_exact": "17/32 * [-p*log(p)-p^2*log(p^2)]",
            "entropy_gap_first_derivative_wrt_a_exact": "[-p*log(p)-p^2*log(p^2)]/2 at b=1/4",
        },
        "golden_control": {
            "a_Q": str(a_q),
            "a_R": str(a_r),
            "dH_gap_for_DaQ": "(1-2*a_R)*H(p)*Da_Q",
            "coefficient_value": str(sp.N(golden_source_gap, 16)),
        },
        "scope": "Two valid complete isometries with identical good compression have different full occupation laws and different Shannon first sources. The second completion uses the existing golden two-port G on the failure subspace. This is a kinematic allowed-gate control, not proof that a post-feedback failure rotation is admitted or has the same native Book cost; the compression alone does not select the polar readout basis or its mean entropy.",
    }


def main() -> None:
    result = run()
    result["checker_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
