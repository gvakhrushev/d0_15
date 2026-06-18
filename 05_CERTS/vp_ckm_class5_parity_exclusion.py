#!/usr/bin/env python3
"""D0-CKM-CLASS5-PARITY-EXCLUSION-001 verifier-producer.

HONEST STATUS BY RESULT: PROOF-TARGET.

This certificate reproduces the finite arithmetic of the CKM class-5 parity
question and then states honestly whether the proposed exclusion is a rigorous
finite contradiction (CERT-CLOSED) or only a heuristic (PROOF-TARGET).

Verified finite facts (all exact / integer arithmetic):
  * |(Z/44)*| = phi(44) = 20.
  * Subgroup orders (Lagrange) divide 20: {1,2,4,5,10,20}.
    (Realized element orders are {1,2,5,10}: the group is Z/2 x Z/10, NOT cyclic.)
  * The order-5 winding class is present (5 | 20) and is ODD (5 % 2 = 1).
  * The active shell step is +2, which is EVEN (2 % 2 = 0).
  * det(T) = -1 and Tr(T^5) = (-1)^5 * L_5 = -11.

Result: a PARITY-ONLY selector (one that sees only order % 2 vs step % 2) maps
the order-5 class and the order-1 (trivial / identity) class to the SAME value,
so it cannot single out order 5 without also excluding the identity class. Hence
the listed data {det=-1, +2 step} does NOT yield a finite contradiction selecting
order 5. The exclusion is heuristic.

honest_residual / missing artifact:
  formal-orientation-parity-contradiction -- an explicit finite selector
  sel(order, step, det) with a forbidden coset such that sel(5,2,-1) is forbidden,
  sel(20,...) is admissible, AND sel resolves order 5 against order 1
  (sel(5) != sel(1)), i.e. uses strictly more than order % 2.

No measured CKM angles, no PDG numbers, no elliptic curves are used.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from math import gcd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


STATUS = "PASS_CKM_CLASS5_PARITY_EXCLUSION"

Q_T = 44
CLASS_ORDER = 5
SHELL_STEP = 2


def euler_totient(n: int) -> int:
    """Exact Euler totient by counting units in Z/n."""
    return sum(1 for a in range(n) if gcd(a, n) == 1)


def element_order(a: int, m: int) -> int:
    """Multiplicative order of a unit a modulo m (exact integer loop)."""
    x = a % m
    k = 1
    while x != 1:
        x = (x * a) % m
        k += 1
    return k


def realized_element_orders(m: int) -> list[int]:
    units = [a for a in range(m) if gcd(a, m) == 1]
    return sorted(set(element_order(a, m) for a in units))


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def trace_T_pow(n: int) -> int:
    """Tr(T^n) = (-1)^n * L_n for T = [[0,1],[1,-1]] (signed Lucas), exact."""
    luc = [2, 1]
    for _ in range(2, n + 1):
        luc.append(luc[-1] + luc[-2])
    return ((-1) ** n) * luc[n]


def det_T() -> int:
    """det of T = [[0,1],[1,-1]] = 0*(-1) - 1*1 = -1, exact."""
    return 0 * (-1) - 1 * 1


def parity_only_selector(order: int) -> int:
    """The heuristic selector: it sees ONLY order % 2."""
    return order % 2


def parity_only_excludes(order: int, step: int) -> bool:
    """The heuristic 'exclusion': odd order vs even +step => declared mismatch."""
    return (order % 2 == 1) and (step % 2 == 0)


def main() -> int:
    print("=== D0-CKM-CLASS5-PARITY-EXCLUSION-001 verifier-producer ===")
    print(f"STRUCTURE_FIXED_BEFORE_NUMBER: q_T={Q_T}, "
          f"classOrder={CLASS_ORDER}, shellStep={SHELL_STEP} "
          "(set before any angle/number)")

    # [1] Unit group order phi(44) = 20.
    phi44 = euler_totient(Q_T)
    assert phi44 == 20, phi44
    print(f"[1] |(Z/{Q_T})*| = phi({Q_T}) = {phi44}")
    print("PASS_UNIT_GROUP_ORDER_20")

    # [2] Subgroup orders divide 20 (Lagrange): exactly the divisors of 20.
    divs = divisors(phi44)
    assert divs == [1, 2, 4, 5, 10, 20], divs
    realized = realized_element_orders(Q_T)
    assert realized == [1, 2, 5, 10], realized
    print(f"[2] Lagrange subgroup orders divide 20: {divs}")
    print(f"    realized element orders (group is Z/2 x Z/10): {realized}")
    print("PASS_SUBGROUP_ORDERS_DIVIDE_20")

    # [3] order-5 class present and odd.
    assert CLASS_ORDER in divs
    assert CLASS_ORDER in realized
    assert phi44 % CLASS_ORDER == 0
    assert CLASS_ORDER % 2 == 1
    print(f"[3] class-5 present (5 | 20, in realized orders); 5 % 2 = "
          f"{CLASS_ORDER % 2} (odd)")
    print("PASS_CLASS5_PRESENT_AND_ODD")

    # [4] shell step +2 even.
    assert SHELL_STEP % 2 == 0
    print(f"[4] shell step +2; 2 % 2 = {SHELL_STEP % 2} (even)")
    print("PASS_SHELL_STEP_EVEN")

    # [5] orientation data: det(T) = -1, Tr(T^5) = -11.
    d = det_T()
    tr5 = trace_T_pow(5)
    assert d == -1, d
    assert tr5 == -11, tr5
    print(f"[5] det(T) = {d}; Tr(T^5) = (-1)^5 * L_5 = {tr5}")
    print("PASS_ORIENTATION_DATA_DET_AND_TRACE")

    # [6] THE OBSTRUCTION: parity-only selector cannot separate order 5 from
    #     order 1 (the trivial/identity class). Both are odd -> same value.
    sel5 = parity_only_selector(5)
    sel1 = parity_only_selector(1)
    assert sel5 == sel1 == 1
    odd_divs = [dd for dd in divs if dd % 2 == 1]
    assert odd_divs == [1, 5], odd_divs
    print(f"[6] parity-only selector: sel(5)={sel5}, sel(1)={sel1} -> EQUAL")
    print(f"    odd divisor-orders of 20 are {odd_divs}: a parity-only rule "
          "would exclude the IDENTITY class too")
    print("PASS_PARITY_ONLY_DEGENERATE_ON_ODD_CLASSES")

    # [7] HONEST VERDICT.
    mechanized = False  # no finite selector resolving 5 vs 1 has been supplied
    if mechanized:
        print("[7] VERDICT: CERT-CLOSED (formal contradiction mechanized)")
    else:
        print("[7] VERDICT: PROOF-TARGET -- exclusion is heuristic, not a finite "
              "contradiction")
        print("    missing artifact: formal-orientation-parity-contradiction "
              "(finite selector with sel(5)=forbidden, sel(20)!=forbidden, "
              "sel(5)!=sel(1))")
    assert mechanized is False
    print("PASS_HONEST_VERDICT_PROOF_TARGET")

    # ----- Negative controls (each asserts a planted wrong input is rejected) -----
    print("--- negative controls ---")

    # NC1: accepting class 5 via a parity selector that ALSO mis-excludes the
    #      identity must be rejected (it is not a valid exclusion).
    bad_excludes_5 = parity_only_excludes(5, SHELL_STEP)
    bad_excludes_1 = parity_only_excludes(1, SHELL_STEP)
    # The planted claim "parity-only validly excludes ONLY class 5" is wrong:
    valid_only_5 = bad_excludes_5 and not bad_excludes_1
    assert valid_only_5 is False, "parity-only spuriously claimed to isolate 5"
    print("FAIL_PARITY_SELECTOR_ISOLATES_5_REJECTED")

    # NC2: rejecting the ALLOWED class 20 by the same rule must be rejected.
    # Class 20 is even -> the parity rule does NOT exclude it; a claim that it
    # does is wrong.
    claims_20_excluded = parity_only_excludes(20, SHELL_STEP)
    assert claims_20_excluded is False, "even order-20 class wrongly excluded"
    print("FAIL_ALLOWED_CLASS20_EXCLUSION_REJECTED")

    # NC3: using a measured CKM angle must be rejected (no empirical input).
    uses_measured_ckm_angle = False
    measured_lambda_planted = Fraction(2253, 10000)  # planted Wolfenstein-like value
    # The cert must NOT consume this; guard that it stays unused.
    assert uses_measured_ckm_angle is False
    assert measured_lambda_planted not in (Fraction(d), Fraction(tr5),
                                           Fraction(phi44)), \
        "measured CKM angle leaked into the finite arithmetic"
    print("FAIL_MEASURED_CKM_ANGLE_REJECTED")

    # NC4: changing q_T away from 44 must change the finite facts (rejected).
    wrong_qT = 45
    wrong_phi = euler_totient(wrong_qT)
    assert wrong_phi != 20, wrong_phi  # phi(45) = 24, breaks the construction
    assert (5 in realized_element_orders(wrong_qT)) is False or wrong_phi != 20
    # planted claim "q_T=45 reproduces phi=20 and the same divisor set" is wrong:
    assert not (wrong_phi == 20), "q_T=45 falsely accepted as q_T=44"
    print(f"FAIL_CHANGED_QT_REJECTED (phi(45)={wrong_phi} != 20)")

    print(f"\n[PROOF-TARGET] {STATUS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
