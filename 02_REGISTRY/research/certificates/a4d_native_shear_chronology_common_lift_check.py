#!/usr/bin/env python3
"""Exact algebraic glue check for the common shear/chronology frame lift.

The all-angle record regularity, chronological determinant frame covariance,
all-L Hodge derivative, and flat Einstein comparison are consumed analytic
owner results. This script checks the exact common state/metric lift between
their carriers; it does not promote those inputs to Lean theorems or physical
admission.
"""

from __future__ import annotations

import json

import sympy as sp


def zero_matrix(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


def check(name: str, condition: bool, checks: dict[str, bool]) -> None:
    checks[name] = bool(condition)
    if not condition:
        raise AssertionError(name)


def main() -> None:
    x = sp.symbols("x", positive=True)
    sqrt5 = sp.sqrt(5)
    p = (sqrt5 - 1) / 2
    a = sp.sqrt(p)
    checks: dict[str, bool] = {}

    check("GOLDEN_IDENTITIES", sp.simplify(p + p**2 - 1) == 0 and sp.simplify(a**2 - p) == 0, checks)

    # c=0,s=1 instance of the existing complete whole-blank 16-mask family.
    seed = [sp.Integer(0)] * 16
    for index, value in {
        0: -a / 2,
        14: -a / 2,
        1: p / 2,
        15: p / 2,
        3: sp.Rational(1, 2),
        13: sp.Rational(1, 2),
    }.items():
        seed[index] = value
    seed_norm = sp.simplify(sum(value**2 for value in seed))
    check("FULL_16_MASK_SEED_UNIT_NORM", seed_norm == 1, checks)
    v_eta = sp.Matrix([p / 2, 0, 0, 0])
    eta = sp.diag(1, -1, -1, -1)
    k_eta = sp.simplify((v_eta.T * eta.inv() * v_eta)[0])
    check("CLOCK_SEED_NONZERO", sp.simplify(k_eta - p**2 / 4) == 0 and k_eta != 0, checks)
    check("EMPTY_MATTER_IS_OUTSIDE_CHRONOLOGY_DOMAIN", (sp.zeros(4, 1).T * eta.inv() * sp.zeros(4, 1))[0] == 0, checks)

    # The two actual recorded first grades at c=0; the source owner proves both
    # record steps regular on the complete angle family.
    w = sp.Matrix([0, -1, 0, 0])
    w2 = sp.Matrix([-a, 1 - a, 0, 0])
    check("TWO_RECORDED_FIRST_GRADES_NONZERO", any(c != 0 for c in w) and sp.simplify(w2[0]**2) == p, checks)

    S = sp.diag(2, sp.Rational(1, 2), 1, 1)
    F = sp.diag(x, 1 / x, 1, 1)
    G = F * S
    q = sp.simplify(G * eta * G.T)
    q_expected = sp.diag(4 * x**2, -sp.Rational(1, 4) / x**2, -1, -1)
    v = sp.simplify(G * v_eta)
    k = sp.simplify((v.T * q.inv() * v)[0])
    Q = sp.simplify(-q + 2 * v * v.T / k)
    Q_expected = sp.diag(4 * x**2, sp.Rational(1, 4) / x**2, 1, 1)
    check("POSITIVE_DETERMINANT_FRAME", sp.simplify(G.det() - 1) == 0, checks)
    check("LORENTZ_METRIC_FRAME_LIFT", zero_matrix(q - q_expected), checks)
    check("FIRST_GRADE_FRAME_LIFT", zero_matrix(v - sp.Matrix([p * x, 0, 0, 0])), checks)
    check("CLOCK_K_CONSTANT_POSITIVE", sp.simplify(k - p**2 / 4) == 0 and k != 0, checks)
    check("OBSERVER_N_FRAME_LIFT", zero_matrix(v / (p / 2) - sp.Matrix([2 * x, 0, 0, 0])), checks)
    check("DERIVED_POSITIVE_METRIC", zero_matrix(Q - Q_expected), checks)
    check("BOTH_VOLUME_FACTORS_ONE", sp.simplify(abs(q.det()) - 1) == 0 and sp.simplify(Q.det() - 1) == 0, checks)

    q0 = q.subs(x, 1)
    Q0 = Q.subs(x, 1)
    Vq = (x * q.diff(x)).subs(x, 1)
    VQ = (x * Q.diff(x)).subs(x, 1)
    check("LORENTZ_SHEAR_TRACE_FREE", sp.simplify(sp.trace(q0.inv() * Vq)) == 0, checks)
    check("POSITIVE_METRIC_SHEAR_TRACE_FREE", sp.simplify(sp.trace(Q0.inv() * VQ)) == 0, checks)
    check("WHITENED_FACTOR_TANGENT", zero_matrix(Q0.inv() * VQ - sp.diag(2, -2, 0, 0)), checks)

    # Check normalization across every exterior grade. For this diagonal frame,
    # the owned compound pairing has weight prod_i Q_i^{-1}; each transformed
    # coordinate has the reciprocal squared scale.
    frame_diag = [2 * x, 1 / (2 * x), sp.Integer(1), sp.Integer(1)]
    Q_diag = [sp.simplify(entry) for entry in Q.diagonal()]
    norm_terms = []
    for mask, amplitude in enumerate(seed):
        scale = sp.prod(frame_diag[i] for i in range(4) if mask & (1 << i))
        weight = sp.prod(1 / Q_diag[i] for i in range(4) if mask & (1 << i))
        norm_terms.append(sp.simplify(weight * (scale * amplitude) ** 2))
    check("NORMALIZATION_PRESERVED_ON_ALL_16_GRADES", sp.simplify(sum(norm_terms) - 1) == 0, checks)
    frozen_terms = []
    base_diag = [sp.Integer(2), sp.Rational(1, 2), sp.Integer(1), sp.Integer(1)]
    for mask, amplitude in enumerate(seed):
        base_scale = sp.prod(base_diag[i] for i in range(4) if mask & (1 << i))
        weight = sp.prod(1 / Q_diag[i] for i in range(4) if mask & (1 << i))
        frozen_terms.append(sp.simplify(weight * (base_scale * amplitude) ** 2))
    frozen_norm = sp.simplify(sum(frozen_terms))
    check("FROZEN_CONTROL_MATCHES_BASE_NORMALIZATION", sp.simplify(frozen_norm.subs(x, 1) - 1) == 0, checks)
    check("FROZEN_MATTER_IS_NOT_THE_FRAME_LIFT", sp.simplify(frozen_norm.subs(x, 2) - 1) != 0, checks)

    result = {
        "schema": "d0-a4d-shear-chronology-common-lift/1",
        "checks": checks,
        "check_count": len(checks),
        "analytic_inputs": {
            "chronological_frame_covariance": {
                "source_commit": "dfaf7c8df509d5abd83fa60a185ad530feadc9b5",
                "source_blob": "c7819ef4a5a532b2c3c1da6c9b6c69bf22c049a3",
                "equation": "A4D_NATIVE_CHRONOLOGICAL_JOINT_REDUCTION.md (2), (4), (19)",
            },
            "two_step_record_regularity": "A4D_NATIVE_CHRONOLOGICAL_STATIONARY_DESCENT.md, complete c in [-1,1] family",
            "all_L_heat_source": "A4D_NATIVE_FACTOR_IMBALANCE_REMAINDER.md, (13)-(17), beta=log(2), L>=2",
            "flat_einstein_source": "A4D_NATIVE_FACTOR_IMBALANCE_REMAINDER.md, homogeneous identity-link probe; all ten packed slots are zero",
        },
        "conclusion": "H_PLUS_CHRONOLOGY_HAS_STRICT_POSITIVE_SHEAR_SOURCE; ADDITIONAL_FULL_ACTION_TERMS_REMAIN_OPEN",
        "physical_admission": "OPEN",
        "global_gr_closure": "OPEN",
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
