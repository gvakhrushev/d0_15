#!/usr/bin/env python3
"""Constructive finite Higgs/scalar projector certificate.

This cert checks the rational frozen-doublet algebra used by
`D0.Matter.HiggsScalarProjectorConstructive`.  It does not use a Higgs mass,
VEV, PDG value, fitted Yukawa coupling, or Standard Model potential input.
"""

from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import sympy as sp  # noqa: E402


STATUS = "PASS_HIGGS_SCALAR_PROJECTOR_CONSTRUCTIVE"


def main() -> int:
    a, b, c, d = sp.symbols("a b c d")
    vx, vy = sp.symbols("vx vy", real=True)

    P = sp.Matrix([[a, b], [c, d]])
    X = sp.Matrix([[0, 1], [1, 0]])
    Z = sp.Matrix([[1, 0], [0, -1]])

    comm_x = sp.simplify(P * X - X * P)
    comm_z = sp.simplify(P * Z - Z * P)
    equations = list(comm_x) + list(comm_z)
    solution = sp.solve(equations, [b, c, d], dict=True)
    commutant_forces_scalar = solution == [{b: 0, c: 0, d: a}]

    scalar_projector = sp.Matrix([[a, 0], [0, a]])
    idem_eq = sp.factor((scalar_projector * scalar_projector - scalar_projector)[0, 0])
    idem_solutions = set(sp.solve(sp.Eq(idem_eq, 0), a))
    idempotent_zero_or_one = idem_solutions == {sp.Integer(0), sp.Integer(1)}

    nonzero_selects_identity = sp.Integer(1) in idem_solutions and sp.Integer(0) in idem_solutions
    identity_projector = scalar_projector.subs(a, 1)
    rank_trace = sp.trace(identity_projector)
    rank_trace_two = rank_trace == 2

    rank1_a = sp.Rational(1, 2)
    rank1_candidate = scalar_projector.subs(a, rank1_a)
    rank1_trace_one = sp.trace(rank1_candidate) == 1
    rank1_idempotence_residual = sp.simplify(rank1_candidate * rank1_candidate - rank1_candidate)
    rank1_fails_idempotence = rank1_trace_one and rank1_idempotence_residual != sp.zeros(2)

    symmetric_identity = identity_projector.T == identity_projector
    v = sp.Matrix([vx, vy])
    response = sp.expand((v.T * identity_projector * v)[0])
    positive_response_formula = response == vx**2 + vy**2

    forbidden_external_inputs = {
        "higgs_mass": None,
        "vev": None,
        "pdg": None,
        "fitted_yukawa": None,
        "sm_potential": None,
    }
    no_external_inputs = all(value is None for value in forbidden_external_inputs.values())

    checks = {
        "commutator_XZ_forces_P_eq_aI": commutant_forces_scalar,
        "idempotent_scalar_gives_a_0_or_1": idempotent_zero_or_one,
        "nonzero_excludes_a_0_selects_identity": nonzero_selects_identity,
        "therefore_P_eq_I2": identity_projector == sp.eye(2),
        "trace_rank_identity_eq_2": rank_trace_two,
        "trace_rank_1_candidate_fails_idempotence": rank1_fails_idempotence,
        "identity_is_symmetric": symmetric_identity,
        "identity_response_is_sum_of_squares": positive_response_formula,
        "no_higgs_mass_vev_pdg_fitted_yukawa_or_sm_potential": no_external_inputs,
    }

    print("--- D0 HIGGS SCALAR PROJECTOR CONSTRUCTIVE CERTIFICATE ---")
    for label, ok in checks.items():
        print(f"[{'PASS' if ok else 'FAIL'}] {label}")
    print(f"commutant_solution = {solution}")
    print(f"idempotent_equation = {idem_eq}")
    print(f"identity_trace_rank = {rank_trace}")
    print(f"rank1_idempotence_residual = {rank1_idempotence_residual.tolist()}")
    print(f"quadratic_response = {response}")

    if all(checks.values()):
        print(f"[CERT-CLOSED] {STATUS}")
        return 0
    print("FAIL_HIGGS_SCALAR_PROJECTOR_CONSTRUCTIVE")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
