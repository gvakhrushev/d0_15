#!/usr/bin/env python3
"""Rank-8 witness: pure condition (28) is strictly weaker than full-rank (26).

J_r in the assignment are the memo's B_r, built here from the same CAR
formulas. They are not a new operator and not an import of the R01 package
or of the #334 checker. M = |chi><chi| - I/16 is an algebraic control.
It is not a native field velocity, and this file does not solve a field kernel
or build a nonlinear branch.
"""

from __future__ import annotations

import json

import sympy as s


PIN = "ec45c8cc4085e7bce888d97439251be9e578d4ff"
MEMO = "02_REGISTRY/research/A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md"

A, B = s.symbols("A B", real=True)
CHECKS: list[str] = []


def require(name: str, condition: bool) -> None:
    if not bool(condition):
        raise ArithmeticError(name)
    CHECKS.append(name)


def creators():
    """Exterior creators on masks 0..15. Annihilators are their transposes."""
    out = []
    for slot in range(4):
        matrix = s.zeros(16)
        for mask in range(16):
            if mask & (1 << slot):
                continue
            occupied = mask & ((1 << slot) - 1)
            sign = (-1) ** bin(occupied).count("1")
            matrix[mask | (1 << slot), mask] = sign
        out.append(matrix)
    return out


def gamma(ops, vector):
    return sum((vector[i] * (ops[i] + ops[i].T) for i in range(4)), s.zeros(16))


def kappa(ops, vector):
    return sum((vector[i] * (ops[i] - ops[i].T) for i in range(4)), s.zeros(16))


def source_operators(ops):
    """Memo B_1, B_2, B_3. Spatial legs only; the time leg is not a B_r."""
    frame = (A - B) * s.eye(4) + B * s.ones(4)
    legs = [frame.row(i).T for i in range(4)]
    probes = (
        s.Matrix([0, 0, -1, 1]),
        s.Matrix([0, 1, 0, -1]),
        s.Matrix([0, -1, 1, 0]),
    )
    return [gamma(ops, probes[i]) * kappa(ops, legs[i + 1]) for i in range(3)]


def pure_chi():
    """Memo seed chi = (e_mask1 - e_mask15) / sqrt(2)."""
    chi = s.zeros(16, 1)
    chi[1] = 1 / s.sqrt(2)
    chi[15] = -1 / s.sqrt(2)
    return chi


def vanished(value) -> bool:
    if isinstance(value, s.MatrixBase):
        return all(vanished(entry) for entry in value)
    return s.expand(value) == 0


def certify() -> dict:
    ops = creators()
    sources = source_operators(ops)
    chi = pure_chi()
    eye = s.eye(16)
    projector = chi * chi.T
    witness = projector - eye / 16
    neutral = witness

    require("chi_normalized", (chi.T * chi)[0] == 1)
    require("chi_real", vanished(chi - s.conjugate(chi)))
    require("witness_real_symmetric", vanished(witness - witness.T))
    require("witness_trace_zero", s.trace(witness) == 0)

    # (28) holds with real lambda and real beta. The orthogonal piece is zero.
    lam = s.Rational(15, 16)
    beta = (s.Integer(0), s.Integer(0), s.Integer(0))
    acted = witness * chi
    reconstructed = lam * chi + sum(
        (beta[i] * sources[i] * chi for i in range(3)), s.zeros(16, 1)
    )
    require("equation_28_on_chi", vanished(acted - reconstructed))
    require("equation_28_lambda_is_15_over_16", acted == lam * chi)
    require("equation_28_beta_real", all(coefficient.is_real for coefficient in beta))

    for index, operator in enumerate(sources):
        require(f"B_{index + 1}_real_symmetric", vanished(operator - operator.T))
        require(f"B_{index + 1}_trace_zero", vanished(s.trace(operator)))
        require(f"chi_source_moment_{index + 1}_zero", vanished((chi.T * operator * chi)[0]))
        require(f"neutral_pairs_B_{index + 1}_to_zero", vanished(s.trace(neutral * operator)))

    pairing = s.trace(neutral * witness)
    require("full_rank_pairing_is_15_over_16", pairing == s.Rational(15, 16))
    require("hs_square_equals_pairing", s.trace(witness * witness) == pairing)

    # If witness were alpha*I + sum beta_r B_r, the pairing would vanish.
    alpha = s.symbols("alpha", real=True)
    free_beta = s.symbols("beta1:4", real=True)
    combination = alpha * eye + sum(
        (free_beta[i] * sources[i] for i in range(3)), s.zeros(16)
    )
    moment = s.expand(
        alpha * s.trace(witness)
        + sum((free_beta[i] * s.trace(witness * sources[i]) for i in range(3)))
    )
    # A real span member pairs to 0 against this neutral witness.
    # The witness pairs to 15/16 against itself, so it is outside the span.
    require("span_member_pairs_to_zero_with_witness", moment == 0)
    require("pairing_obstructs_span_membership", pairing == s.Rational(15, 16) and moment == 0)

    # (26) implies (28) on every vector, by applying the real linear combination.
    probe = s.Matrix(s.symbols("v0:16", real=True))
    applied = combination * probe
    by_coefficients = alpha * probe + sum(
        (free_beta[i] * sources[i] * probe for i in range(3)), s.zeros(16, 1)
    )
    require("equation_26_implies_equation_28", vanished(applied - by_coefficients))

    # Positive control: an explicit real span member passes (28) and pairs to 0.
    inside = 3 * eye + sources[0] + 2 * sources[1] - sources[2]
    inside_action = 3 * chi + sources[0] * chi + 2 * sources[1] * chi - sources[2] * chi
    require("span_control_passes_equation_28", vanished(inside * chi - inside_action))
    require("span_control_pairs_to_zero", vanished(s.trace(neutral * inside)))

    # Negative control: (28) is not automatic. e_mask0 is orthogonal to
    # span{chi, B_r chi}, so the symmetric lift fails the pure test.
    tangent = eye[:, 0]
    require("pure_tangent_orthogonal_to_chi", (tangent.T * chi)[0] == 0)
    for index, operator in enumerate(sources):
        require(
            f"pure_tangent_orthogonal_to_B_{index + 1}_chi",
            vanished((tangent.T * operator * chi)[0]),
        )
    pure_lift = tangent * chi.T + chi * tangent.T
    require("pure_lift_sends_chi_to_tangent", vanished(pure_lift * chi - tangent))
    require("pure_lift_fails_equation_28", (tangent.T * pure_lift * chi)[0] == 1)

    return {
        "schema": "d0-rank-mv-rank8-witness/1",
        "status": "candidate",
        "pin": PIN,
        "memo": MEMO,
        "chi": "(e_mask1-e_mask15)/sqrt(2)",
        "J_r_means": "memo B_r",
        "operator": "|chi><chi|-I/16",
        "equation_28": {
            "holds": True,
            "lambda": "15/16",
            "beta": [0, 0, 0],
            "coefficients_real": True,
        },
        "equation_26": {
            "holds_for_operator": False,
            "neutral_pairing": "15/16",
            "neutral_S": "|chi><chi|-I/16",
        },
        "strictly_weaker": True,
        "equation_26_implies_equation_28": True,
        "native_field_velocity": False,
        "field_kernel_solved": False,
        "nonlinear_branch_constructed": False,
        "gr_derived": False,
        "r01_package_imported": False,
        "pull_request_334_merged": False,
        "exact_checks": len(CHECKS),
        "checks": CHECKS,
    }


def main() -> None:
    print(json.dumps(certify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
