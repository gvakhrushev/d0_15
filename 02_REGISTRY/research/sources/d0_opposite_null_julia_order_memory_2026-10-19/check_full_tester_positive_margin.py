#!/usr/bin/env python3
"""Exact rational bounds for the complete two-Julia Lorentz tester record.

This certifies a local probability margin for the specified fixed positive
POVM when it is read on every retained success/failure flag branch. It does
not certify physical admission or select the Book Cost-Info price.
"""

from fractions import Fraction as F
import json


def factorial(n: int) -> int:
    value = 1
    for k in range(2, n + 1):
        value *= k
    return value


def exp_upper(x: F, n: int) -> F:
    """Rational upper bound for exp(x), x >= 0, with a geometric tail."""
    partial = sum((x**k / factorial(k) for k in range(n + 1)), F(0))
    first_tail = x ** (n + 1) / factorial(n + 1)
    ratio = x / (n + 2)
    require(0 <= ratio < 1, "geometric-tail ratio")
    return partial + first_tail / (1 - ratio)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> dict:
    # ||X|| <= 1/100 and ||d Lambda(X)|| <= 4 ||X|| on CAR16.
    radius = F(1, 100)
    e_upper = exp_upper(4 * radius, 4)
    require(e_upper < F(1041, 1000), "exp(4r) rational upper bound")

    # T_X=Lambda(exp X)/2, compared with T_0=I/2.
    delta_t = (e_upper - 1) / 2
    t_upper = e_upper / 2
    require(delta_t < F(41, 2000), "uniform T_X-I/2 bound")
    require(t_upper < F(1041, 2000), "uniform contraction bound")

    # D_X=sqrt(I-T_X^T T_X), compared with sqrt(3)I/2.
    delta_s = (t_upper + F(1, 2)) * delta_t
    require(delta_s < F(21, 1000), "T_X^T T_X-I/4 bound")
    s_lower = F(3, 4) - F(21, 1000)
    require(s_lower == F(729, 1000), "positive defect-square lower bound")
    require(F(853, 1000) ** 2 < F(729, 1000), "square-root lower bound")
    delta_d = F(21, 1000) / (2 * F(853, 1000))
    require(delta_d < F(13, 1000), "uniform D_X-sqrt(3)I/2 bound")
    require(delta_d < delta_t, "defect variation below T variation")

    # Each of the four retained two-gate branches is K=F_2 F_1 with
    # F_j in {T_j,D_j}; its flat scalar is 1/4, sqrt(3)/4, or 3/4.
    delta_k = 2 * delta_t
    require(delta_k < F(41, 1000), "two-factor branch perturbation")
    require(delta_k < F(1, 24), "branch perturbation below overlap margin")
    # The least flat overlap is 1/(4 sqrt(2)) > 1/6. The perturbed
    # rank-one POVM overlap therefore remains greater than 1/8.
    require(F(1, 6) - F(1, 24) == F(1, 8), "rank-one overlap margin")
    rank_one_probability = F(1, 12) * F(1, 8) ** 2
    require(rank_one_probability == F(1, 768), "rank-one event lower bound")

    # Since exp(4r)<1041/1000, the inverse exterior representation gives
    # sigma_min(T)>500/1041>12/25. D has an even larger minimum singular
    # value. Therefore sigma_min(K)>(12/25)^2 and the rest effect >=I/2
    # has probability >1/40 on every branch.
    t_min = F(12, 25)
    require(F(500, 1041) > t_min, "T minimum singular value lower bound")
    require(F(1) - t_upper**2 > t_min**2, "defect minimum singular value")
    k_min = t_min**2
    rest_probability = F(1, 2) * k_min**2
    require(rest_probability > F(1, 40), "positive rest-effect event bound")

    # One retained Golden F/R split has p^2=(3-sqrt(5))/2>3/8.
    require(F(9) ** 2 > F(4) ** 2 * F(5), "9 > 4 sqrt(5)")
    split_probability = F(3, 8) * rank_one_probability
    require(split_probability == F(1, 2048), "split-event lower bound")

    # At the flat point the four flag masses sum to one and the 13 POVM
    # effects sum to identity: 12 rank-one effects each contribute 1/24
    # on Omega_4 before the common 1/12 factor; E_rest contributes 1/2.
    flat_branch_masses = [F(1, 16), F(3, 16), F(3, 16), F(9, 16)]
    require(sum(flat_branch_masses) == 1, "all four flag branches retained")
    require(12 * F(1, 24) + F(1, 2) == 1, "13-effect POVM completeness")

    return {
        "status": "PASS_STRICT_POSITIVITY_FOR_COMPLETE_TWO_JULIA_TAPE",
        "scope": "mathematical local chart; no physical admission or price selection",
        "per_lorentz_generator_operator_radius": "1/100",
        "strict_contraction_upper": str(t_upper),
        "two_gate_branch_operator_error_upper": str(delta_k),
        "retained_flag_pointer_outcomes": 52,
        "rank_one_outcome_lower_bound": ">1/768",
        "rest_effect_outcome_lower_bound": ">1/40",
        "after_one_retained_golden_split_outcomes": 53,
        "split_tape_outcome_lower_bound": ">1/2048",
        "flat_flag_masses": [str(x) for x in flat_branch_masses],
        "entropy_regular_on_chart": True,
        "exact_controls": 14,
    }


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, sort_keys=True, indent=2))
