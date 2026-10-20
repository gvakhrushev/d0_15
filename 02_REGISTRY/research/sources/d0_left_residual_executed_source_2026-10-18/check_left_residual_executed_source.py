"""LEFT recording word versus the address marginal.

The owned word samples address projectors.  The owned golden and pi0
residuals are phase-projection defects.  This module tests whether that
defect is an executed stress on the dressed metric.  It does not invent a
functional, a measure, or a gate, and it does not set a stress equal to an
Einstein tensor.
"""

from __future__ import annotations

import json

import sympy as sp

PIN = "f3fe3c80ae69f122edc8cbef19c71fb22a1d68e6"
MISSING_PRIMITIVE = "fiber_resolved_cochain_shift_effect"


class CheckFailure(RuntimeError):
    """An owned identity used by this comparison failed."""


class LeftResidualFraud(RuntimeError):
    """A conclusion was declared by copying or renaming, not by the comparison."""


def must_zero(expr: sp.Expr, name: str) -> None:
    if sp.simplify(expr) != 0:
        raise CheckFailure(name)


def same_tensor(left, right) -> bool:
    try:
        diff = sp.Matrix(left) - sp.Matrix(right)
    except (TypeError, ValueError, AttributeError):
        return sp.simplify(left - right) == 0
    return all(sp.simplify(entry) == 0 for entry in diff)


def cycle_laplacian(period: int) -> sp.Matrix:
    lap = sp.zeros(period)
    for i in range(period):
        lap[i, i] = 2
        lap[i, (i + 1) % period] = -1
        lap[i, (i - 1) % period] = -1
    return lap


def phase_projection(fine: int, coarse: int) -> list[int]:
    return [i % coarse for i in range(fine)]


def operator_residual(lap_fine: sp.Matrix, lap_coarse: sp.Matrix,
                      projection: list[int], probe: sp.Expr) -> sp.Matrix:
    residual = sp.zeros(lap_fine.rows)
    for i in range(lap_fine.rows):
        for j in range(lap_fine.rows):
            residual[i, j] = (
                lap_fine[i, j] - probe * lap_coarse[projection[i], projection[j]]
            )
    return sp.simplify(residual)


def push_marginal(law: tuple[sp.Expr, ...], projection: list[int],
                  coarse: int) -> tuple[sp.Expr, ...]:
    marginal = [sp.Integer(0)] * coarse
    for i, weight in enumerate(law):
        marginal[projection[i]] += weight
    return tuple(sp.simplify(item) for item in marginal)


def dressed_factors(marginal: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    reference = sp.simplify(sum(marginal) / len(marginal))
    must_zero(reference * len(marginal) - sum(marginal), "reference is the mean mass")
    if sp.simplify(reference) == 0:
        raise CheckFailure("reference mass vanished")
    return tuple(sp.simplify(weight / reference) for weight in marginal)


def cocycle_gap() -> sp.Expr:
    """Owned qρ(ω)=μ(ω)Tr(ρ M_ω) on one golden round, not the rename qρ=μ."""
    phi = (1 + sp.sqrt(5)) / 2
    mu_direct = sp.simplify(phi ** (-1))
    likelihood = phi
    return sp.simplify(mu_direct * likelihood - mu_direct)


def compare(force_identity: bool = False, renamed: bool = False,
            stress=None, einstein=None, claim_q_equals_mu: bool = False,
            close_equation_20: bool = False,
            close_equation_28: bool = False,
            identify_phase_with_dressed_site: bool = False) -> dict:
    phi = sp.simplify((1 + sp.sqrt(5)) / 2)
    pi0 = sp.simplify(sp.Rational(6, 5) * phi ** 2)
    must_zero(phi ** 2 - phi - 1, "phi is the golden unit")
    must_zero(pi0 - sp.Rational(6, 5) * phi ** 2, "pi0 is the owned closure probe")
    must_zero(pi0 - phi - (sp.sqrt(5) + 13) / 10, "pi0 is not the golden scale")

    coarse = 4
    fine = 5
    projection = phase_projection(fine, coarse)
    lap_fine = cycle_laplacian(fine)
    lap_coarse = cycle_laplacian(coarse)
    for lap in (lap_fine, lap_coarse):
        for i in range(lap.rows):
            must_zero(sum(lap[i, :]), "cycle Laplacian is conservative")

    residual_phi = operator_residual(lap_fine, lap_coarse, projection, phi)
    residual_pi0 = operator_residual(lap_fine, lap_coarse, projection, pi0)
    entry_phi_same_fiber = sp.simplify(residual_phi[0, 1])
    entry_phi_other_end = sp.simplify(residual_phi[4, 1])
    fiber_gap = sp.simplify(entry_phi_same_fiber - entry_phi_other_end)
    pi0_gap = sp.simplify(residual_pi0[0, 1] - residual_pi0[4, 1])
    must_zero(entry_phi_same_fiber - (phi - 1), "golden residual at (0,1)")
    must_zero(entry_phi_other_end - phi, "golden residual at (4,1)")
    must_zero(fiber_gap + 1, "fiber gap is -1")
    must_zero(pi0_gap + 1, "pi0 probe has the same fiber gap")
    must_zero(
        sp.simplify(residual_pi0[0, 1] - residual_phi[0, 1]) - (pi0 - phi),
        "the two probes are different residuals",
    )
    if projection[0] != projection[4]:
        raise CheckFailure("sites 0 and 4 are not one address fiber")

    uneven = (
        sp.Rational(1, 4), sp.Rational(1, 4), sp.Rational(1, 4),
        sp.Rational(1, 8), sp.Rational(1, 8),
    )
    swapped = (
        sp.Rational(1, 8), sp.Rational(1, 4), sp.Rational(1, 4),
        sp.Rational(1, 8), sp.Rational(1, 4),
    )
    uniform_fiber = (
        sp.Rational(1, 8), sp.Rational(1, 4), sp.Rational(1, 4),
        sp.Rational(1, 4), sp.Rational(1, 8),
    )
    for law in (uneven, swapped, uniform_fiber):
        must_zero(sum(law) - 1, "recording law is a probability")
    marginal_uneven = push_marginal(uneven, projection, coarse)
    marginal_swapped = push_marginal(swapped, projection, coarse)
    marginal_uniform = push_marginal(uniform_fiber, projection, coarse)
    if marginal_uneven != marginal_swapped:
        raise CheckFailure("fiber swap changed the address marginal")
    if marginal_uneven == marginal_uniform:
        raise CheckFailure("two address marginals accidentally agree")
    if uneven[0] == swapped[0]:
        raise CheckFailure("fiber swap was invisible to the recording")
    factors = dressed_factors(marginal_uneven)
    factors_uniform = dressed_factors(marginal_uniform)
    if factors == factors_uniform:
        raise CheckFailure("dressed metric did not see the marginal")
    if dressed_factors(marginal_swapped) != factors:
        raise CheckFailure("same marginal produced two dressed metrics")

    row_sum = [sp.simplify(sum(residual_phi[i, :])) for i in range(fine)]
    expected_row_sum = [-2 * phi, phi, 0, phi, -2 * phi]
    for got, want in zip(row_sum, expected_row_sum):
        must_zero(got - want, "residual row sum")
    if row_sum[0] != row_sum[4]:
        raise CheckFailure("row-sum contraction failed to be fiber-constant")

    q_minus_mu = cocycle_gap()
    must_zero(q_minus_mu - (sp.Rational(3, 2) - sp.sqrt(5) / 2), "cocycle gap")

    descends = fiber_gap == 0
    identity_holds = bool(descends)
    scoped_nogo = not identity_holds
    gr_derived = False
    if renamed and same_tensor(residual_phi, residual_phi):
        raise LeftResidualFraud(
            "defect declared executed because a symbol was renamed"
        )
    if claim_q_equals_mu or close_equation_20 or close_equation_28 or force_identity:
        raise LeftResidualFraud(
            "conclusion declared without a fiber-resolved recording effect"
        )
    if stress is not None and einstein is not None and same_tensor(stress, einstein):
        raise LeftResidualFraud("Einstein tensor copied into the stress")
    if identify_phase_with_dressed_site:
        raise LeftResidualFraud(
            "phase fiber i mod 4 identified with the coframe site of (9)"
        )
    if identity_holds == scoped_nogo or gr_derived:
        raise CheckFailure("verdict flags are inconsistent")

    return {
        "identity_holds": identity_holds,
        "scoped_nogo": scoped_nogo,
        "gr_derived": gr_derived,
        "equation_20_closed": False,
        "equation_28_closed": False,
        "missing_primitive": MISSING_PRIMITIVE,
        "pin": PIN,
        "fiber_gap": str(fiber_gap),
        "golden_entry_same_address": str(entry_phi_same_fiber),
        "golden_entry_other_fiber_end": str(entry_phi_other_end),
        "pi0_minus_phi": str(sp.simplify(pi0 - phi)),
        "q_minus_mu": str(q_minus_mu),
        "recording_distinguishes_fiber_shift": True,
        "address_marginal_distinguishes_fiber_shift": False,
        "residual_descends_to_address": False,
        "row_sum_depends_on_sampling_measure": False,
        "word_field_jet": "0",
        "phase_fiber_versus_dressed_address": True,
        "phase_index": "archive phase i mod 4",
        "dressed_index": "coframe site x of (9)",
    }


def main() -> None:
    print(json.dumps(compare(), ensure_ascii=True, sort_keys=True))


if __name__ == "__main__":
    main()
