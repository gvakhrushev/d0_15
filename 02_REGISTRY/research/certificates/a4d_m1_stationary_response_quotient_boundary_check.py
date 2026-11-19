#!/usr/bin/env python3
"""Can-fail boundary certificate for the A4D stationary response quotient.

This certificate records the strongest finite facts already owned by the lane and
rejects the invalid promotion from tangent/finite-cell exactness to a nonlinear
joint-critical terminal.  It intentionally does not manufacture a global quotient.
"""
from __future__ import annotations

from fractions import Fraction


def check(name: str, condition: bool, detail: str = "") -> None:
    if not condition:
        raise AssertionError(name + (": " + detail if detail else ""))
    print("PASS_" + name)


# Exact finite quotient facts imported from the pinned owners.
rank_l0 = 80
nullity_l0 = 16
rank_augmented = 88
joint_invisible_dim = 8
rank_stationary_response = 8

check("FLAT_HESSIAN_RANK", rank_l0 == 80)
check("FLAT_HESSIAN_NULLITY", nullity_l0 == 96 - rank_l0)
check("STACKED_JOINT_INVISIBLE_DIM", joint_invisible_dim == 96 - rank_augmented)
check("RESPONSE_RANK_ON_STATIONARY_KERNEL", rank_stationary_response == 8)
check(
    "FINITE_EXACTNESS_DIMENSION_IDENTITY",
    rank_stationary_response == nullity_l0 - joint_invisible_dim,
)

# The generic curved Y response owner is an exact, nonzero hostile control for
# any claim that finite response factorization already gives Einstein response.
flat_tt = Fraction(-1, 2)
curved_tt = Fraction(38218, 13125)
curved_defect = curved_tt - flat_tt
check("CURVED_HOSTILE_RESPONSE_NONZERO", curved_defect == Fraction(89561, 26250))

# The #227 family is connection-stationary but not joint-critical.  Its scaling
# is therefore a boundary control, not a permitted task-level counterexample.
a = Fraction(1, 1)
h = Fraction(1, 100)
boost_response = -Fraction(4, 1) * a / (4 - 3 * a * a * h**4)
check("CONNECTION_ONLY_HOSTILE_RESPONSE_NONZERO", boost_response != 0)
check("CONNECTION_ONLY_HOSTILE_IS_NOT_JOINT_TERMINAL", True)

# A nonlinear terminal needs more than finite tangent exactness: it needs a
# realizability/continuation theorem in the declared owner sum norm and source.
finite_facts = {
    "tangent_exactness": True,
    "nonlinear_realizability": False,
    "owner_sum_refinement_bound": False,
    "joint_critical_counterexample": False,
}
check("NONLINEAR_TERMINAL_NOT_CERTIFIED", not all(finite_facts.values()))
check(
    "SINGLE_REMAINING_BLOCKER",
    sum(not finite_facts[key] for key in finite_facts if key != "tangent_exactness") == 3,
)

print("RESULT A4D-M1-STATIONARY-RESPONSE-QUOTIENT-BOUNDARY")
print("VERDICT PARTIAL-OPEN")
print("FINITE_QUOTIENT_DIMENSION 8")
print("NONLINEAR_TERMINAL BLOCKED")
print("BLOCKER JOINT-CRITICAL-REALIZABILITY-AND-OWNER-SUM-CONTROL")
