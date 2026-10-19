#!/usr/bin/env python3
"""Exact controls for the response-preserving C_Y capacity boundary.

This checks a scoped finite coupling/entropy statement. It does not establish
physical admission of C_Y or select a full D0 action.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[4]
INPUTS = {
    "01_BOOKS/BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md":
        "90d493492834c36900baddc57c987aa5e9910ee560993a793f6d178b4d827f03",
    "02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md":
        "748f723516dead3a713f31dd5a49dcbde7805ef0a15e7450f3026790abefa5e2",
}
CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(f"FAIL: {label}")


def main() -> None:
    pinned = {}
    for rel, expected in INPUTS.items():
        actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        require(actual == expected, f"source pin: {rel}")
        pinned[rel] = actual

    # Columns are input leaves; rows are output leaves. Full one-hot leaf
    # response preservation means R_out K = R_in with R_out = R_in = I.
    K = sp.Matrix([[sp.Rational(1, 2), sp.Rational(1, 2)],
                   [sp.Rational(1, 2), sp.Rational(1, 2)]])
    one = sp.Matrix([[1, 1]])
    require(one * K == one, "normalization-only response is preserved")
    require(K != sp.eye(2), "negative control actually mixes leaves")
    require(sp.eye(2) * K != sp.eye(2), "full leaf response rejects mixing")
    require(sp.eye(2) * sp.eye(2) == sp.eye(2),
            "full leaf response admits the identity kernel")

    pi = sp.Matrix([sp.Rational(1, 3), sp.Rational(2, 3)])
    uniform = sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 2)])
    Z = sp.Matrix([3, 3])
    r_star = Z / sum(Z)
    require(r_star == uniform, "equal vacuum Z_i gives uniform capacity profile")
    require(K * pi == uniform, "mixing kernel realizes the reweighted profile")
    require(r_star != pi, "reweighted profile changes a nonuniform old response")
    require(sp.eye(2) * K * pi != sp.eye(2) * pi,
            "the reweighting fails the full response vector")

    # A declared quotient that forgets the leaf label permits this same kernel;
    # this is why any response-loss map must be named explicitly.
    R_loss = one
    require(R_loss * K == R_loss,
            "declared total-only quotient permits within-quotient mixing")

    J, Hbeta = sp.symbols("J Hbeta", real=True)
    g = sp.exp(-2 * J)
    Hcond = -g * sp.log(g) - (1 - g) * sp.log(1 - g) + (1 - g) * Hbeta
    kappa = g * (Hbeta - sp.log((1 - g) / g))
    require(sp.simplify(sp.diff(Hcond, J) - 2 * kappa) == 0,
            "conditional Shannon derivative gives 2*kappa")
    require(sp.simplify(sp.diff(Hcond, Hbeta) - (1 - g)) == 0,
            "moving failure entropy has coefficient 1-g")

    pi0, J0, J1 = sp.symbols("pi0 J0 J1", positive=True, real=True)
    Hpi = -pi0 * sp.log(pi0) - (1 - pi0) * sp.log(1 - pi0)
    H0 = Hcond.subs(J, J0)
    H1 = Hcond.subs(J, J1)
    Hjoint = Hpi + pi0 * H0 + (1 - pi0) * H1
    dH_dpi = sp.diff(Hpi, pi0) + H0 - H1
    require(sp.simplify(sp.diff(Hjoint, pi0) - dH_dpi) == 0,
            "joint derivative retains the moving-leaf term")
    require(sp.simplify((sp.diff(Hjoint, pi0) - sp.diff(Hpi, pi0))
                         .subs(J1, J0)) == 0,
            "equal base conditional entropies cancel the cross term")
    require(sp.simplify(sp.diff(Hjoint, J0)
                         - pi0 * 2 * kappa.subs(J, J0)) == 0,
            "leaf-weighted local source is exact")
    require(sp.simplify(sp.diff(Hjoint, J1)
                         - (1 - pi0) * 2 * kappa.subs(J, J1)) == 0,
            "second leaf-weighted local source is exact")

    result = {
        "status": "PASS_SCOPED_RESPONSE_PRESERVING_CY_BOUNDARY",
        "checks": CHECKS,
        "source_sha256": pinned,
        "scope": {
            "full_leaf_response_forces_identity_kernel": True,
            "normalization_only_does_not_fix_leaf_masses": True,
            "fixed_leaf_shannon_source_derived": True,
            "physical_CY_admission_proved": False,
            "native_good_failure_law_proved": False,
            "GR_closed": False,
        },
        "sympy": sp.__version__,
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
