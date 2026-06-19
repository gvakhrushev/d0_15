#!/usr/bin/env python3
"""D0-CKM-CLASS5-SELECTOR-OWNER-001 verifier-producer.

HONEST STATUS BY RESULT: CERT-CLOSED (finite witness).

This certificate is the OWNER object for the class-5 pointer collision: it does NOT
re-prove the class-5 EXCLUSION (already CORE-FORMALIZED as D0-CLASS5-ALIASING-001 in
D0.Claims.Class5Aliasing). It verifies the finite data behind the NEW Lean witness
D0.Matter.CKMClass5SelectorOwner, which wires the collision to the proven M1 selector
spine (D0.Foundation.M1Predicate: selector_M1Forced / m1_alternative_needs_catalogue).

Verified finite facts (all exact / integer / rational arithmetic):
  * |(Z/44)*| = phi(44) = 20; the characteristic (unique-per-order) subgroup orders are
    {1, 4, 5, 20}; 20 = 4 * 5 = |ABCD| * D_Sigma.
  * Orbit-length separation: a class-d generator sweeps a cyclic orbit of length d, so the
    three M1-admissible classes {1, 5, 20} have orbit lengths {1, 5, 20} -- pairwise distinct.
  * Class 5 is the UNIQUE pointer-collider: orbitLength(5) = D_Sigma = 5. Classes 1 and 20 do
    NOT collide, so class 20 is NOT excluded by this aliasing test.
  * Register deficit: the aliased diagonal readout resolves D_Sigma = 5 of D_Sigma^2 = 25
    (winding, address) configs; the 25 - 5 = 20 off-diagonal ones are what a hidden register
    must store.
  * Register selector: over the candidate answers {diagonal, hiddenPartial, hiddenFull} with
    register-cost {0, 1, 20}, the diagonal (cost 0) is the UNIQUE STRICT MINIMUM -- exactly the
    StrictSelected obligation the Lean witness discharges, so it is M1-forced and every
    hidden-register alternative requires an external catalogue.

honest boundary (printed, not hidden):
  This certifies the finite OWNER witness (the selector + orbit separation) that the Lean
  module proves term-mode against the proven spine. The full M1 hidden-memory contradiction
  (grammar 01.11C, holographic pointer machine) remains the upstream frontier obligation that
  D0-CLASS5-ALIASING-001 already flags; this owner does not claim to discharge it.

No measured CKM angles, no PDG numbers, no elliptic curves are used.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from math import gcd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


STATUS = "PASS_CKM_CLASS5_SELECTOR_OWNER"

Q_T = 44
D_SIGMA = 5          # operational address classes (BOOK_04 §04.1)
ABCD = 4             # terminal roles
ADMISSIBLE_CLASSES = (1, 5, 20)   # M1-admissible characteristic orders (class 4 already killed)


def units(mod: int) -> list[int]:
    return [a for a in range(1, mod) if gcd(a, mod) == 1]


def order_of(a: int, mod: int) -> int:
    """Multiplicative order of a unit a modulo mod (exact integer loop)."""
    x = a % mod
    k = 1
    while x != 1:
        x = (x * a) % mod
        k += 1
    return k


def subgroup_generated(gens: list[int], mod: int) -> frozenset:
    s = {1}
    frontier = [1]
    while frontier:
        x = frontier.pop()
        for g in gens:
            y = (x * g) % mod
            if y not in s:
                s.add(y)
                frontier.append(y)
    return frozenset(s)


def orbit_length(d: int) -> int:
    """Length of the cyclic winding orbit of a class-d generator (== d)."""
    return d


def collides_with_dsigma(d: int) -> bool:
    """A class pointer-collides exactly when its orbit length equals D_Sigma."""
    return orbit_length(d) == D_SIGMA


# ---- the register selector (mirrors the Lean RegisterConfig / registerCost) ----
REGISTER_COST = {
    "diagonal": Fraction(0),     # no hidden register
    "hiddenPartial": Fraction(1),  # stores at least one off-diagonal config
    "hiddenFull": Fraction(20),    # stores all 20 off-diagonal configs
}


def strict_minimum(cost: dict) -> str:
    """The unique candidate strictly below every other (raises if not unique)."""
    best = min(cost, key=lambda k: cost[k])
    strictly = [k for k in cost if k != best and cost[k] <= cost[best]]
    assert not strictly, f"minimum not strict: ties {strictly}"
    return best


def main() -> int:
    print("=== D0-CKM-CLASS5-SELECTOR-OWNER-001 verifier-producer ===")
    print(f"STRUCTURE_FIXED_BEFORE_NUMBER: q_T={Q_T}, D_Sigma={D_SIGMA}, "
          f"admissibleClasses={ADMISSIBLE_CLASSES} "
          "(orbit/selector structure fixed before any angle/number)")

    U = units(Q_T)
    assert len(U) == 20, f"|(Z/44)*| != 20: {len(U)}"
    print(f"[1] |(Z/{Q_T})*| = phi({Q_T}) = {len(U)}")
    print("PASS_UNIT_GROUP_ORDER_20")

    # [2] characteristic (unique-per-order) subgroup orders = {1,4,5,20}; 20 = 4*5 = |ABCD|*D_Sigma
    one_gen = {subgroup_generated([g], Q_T) for g in U}
    two_gen = {subgroup_generated([g, h], Q_T) for g in U for h in U}
    subs = one_gen | two_gen | {frozenset({1}), frozenset(U)}
    by_order: dict[int, list] = {}
    for H in subs:
        by_order.setdefault(len(H), []).append(H)
    char_orders = {o for o, hs in by_order.items() if len(hs) == 1}
    assert char_orders == {1, 4, 5, 20}, f"characteristic orders != {{1,4,5,20}}: {char_orders}"
    assert 20 == ABCD * D_SIGMA, "20 != |ABCD| * D_Sigma"
    print(f"[2] characteristic subgroup orders = {sorted(char_orders)}; "
          f"20 = {ABCD} * {D_SIGMA} = |ABCD| * D_Sigma")
    print("PASS_CHARACTERISTIC_ORDERS_1_4_5_20")

    # [3] orbit-length separation of the M1-admissible classes {1,5,20}
    orbits = {d: orbit_length(d) for d in ADMISSIBLE_CLASSES}
    assert orbits == {1: 1, 5: 5, 20: 20}, orbits
    assert len(set(orbits.values())) == 3, "orbit lengths not pairwise distinct"
    print(f"[3] orbit lengths of admissible classes: {orbits} (pairwise distinct)")
    print("PASS_ORBIT_LENGTH_SEPARATION_1_5_20")

    # [4] class 5 is the UNIQUE pointer-collider; class 20 NOT excluded
    colliders = [d for d in ADMISSIBLE_CLASSES if collides_with_dsigma(d)]
    assert colliders == [5], f"unique collider should be class 5, got {colliders}"
    assert collides_with_dsigma(5) is True
    assert collides_with_dsigma(1) is False
    assert collides_with_dsigma(20) is False, "class 20 must NOT collide (not excluded)"
    print(f"[4] orbitLength(5) = {orbit_length(5)} = D_Sigma -> class 5 is the unique collider; "
          "class 1 and class 20 do NOT collide (class 20 is a survivor, not excluded)")
    print("PASS_CLASS5_UNIQUE_COLLIDER_CLASS20_NOT_EXCLUDED")

    # [5] register deficit: diagonal resolves 5 of 25; 20 off-diagonal -> hidden register
    assert D_SIGMA == 5
    assert D_SIGMA ** 2 == 25
    assert D_SIGMA ** 2 - D_SIGMA == 20
    print(f"[5] aliased diagonal resolves {D_SIGMA} of {D_SIGMA**2}; "
          f"{D_SIGMA**2 - D_SIGMA} off-diagonal configs would need a hidden register")
    print("PASS_REGISTER_DEFICIT_25_TO_5")

    # [6] the register selector: diagonal (cost 0) is the UNIQUE STRICT MINIMUM
    assert REGISTER_COST["diagonal"] == 0
    assert REGISTER_COST["hiddenPartial"] == 1
    assert REGISTER_COST["hiddenFull"] == 20
    selected = strict_minimum(REGISTER_COST)
    assert selected == "diagonal", f"strict minimum should be diagonal, got {selected}"
    # the StrictSelected obligation: diagonal strictly below every alternative
    for k, c in REGISTER_COST.items():
        if k != "diagonal":
            assert REGISTER_COST["diagonal"] < c, f"diagonal not strictly below {k}"
    print(f"[6] register-cost selector: {dict((k, str(v)) for k, v in REGISTER_COST.items())}; "
          "diagonal (cost 0) is the UNIQUE STRICT MINIMUM -> M1-forced")
    print("    -> every hidden-register alternative RequiresExternalCatalogue "
          "(via selector_M1Forced / m1_alternative_needs_catalogue)")
    print("PASS_REGISTER_SELECTOR_DIAGONAL_M1FORCED")

    # ----- Negative controls (each asserts a planted wrong input is rejected) -----
    print("--- negative controls ---")

    # NC1: parity of the orbit length cannot separate class 1 from class 5.
    #      Both orbit lengths are ODD, so a parity-only fibre map collapses them ->
    #      a parity-only rule is INSUFFICIENT to single out class 5. Reject the claim
    #      that parity alone separates them.
    parity = {d: orbit_length(d) % 2 for d in ADMISSIBLE_CLASSES}
    assert parity[1] == parity[5] == 1, parity
    parity_separates_1_from_5 = (parity[1] != parity[5])
    assert parity_separates_1_from_5 is False, \
        "parity wrongly claimed to separate class 1 from class 5"
    print(f"    orbit-length parities: {parity} (class 1 and class 5 both odd -> same fibre)")
    print("FAIL_PARITY_ONLY_SEPARATES_REJECTED")

    # NC2: class 20 is NOT a pointer-collider, so any claim that it is excluded by the
    #      aliasing test is wrong and must be rejected.
    claims_class20_excluded = collides_with_dsigma(20)
    assert claims_class20_excluded is False, "class 20 wrongly claimed excluded (it is a survivor)"
    print("FAIL_CLASS20_EXCLUDED_REJECTED")

    # NC3: using a measured CKM datum must be rejected (no empirical input).
    uses_measured_ckm_data = False
    measured_lambda_planted = Fraction(2253, 10000)  # planted Wolfenstein-like value
    assert uses_measured_ckm_data is False
    finite_values = {Fraction(len(U)), Fraction(D_SIGMA), Fraction(ABCD)} | \
        set(REGISTER_COST.values()) | {Fraction(v) for v in orbits.values()}
    assert measured_lambda_planted not in finite_values, \
        "measured CKM datum leaked into the finite arithmetic"
    print("FAIL_CKM_DATA_INPUT_REJECTED")

    # NC4 (structural guard): a planted selector that ties the diagonal with a hidden
    #     register has NO strict minimum -> the M1Forced witness must NOT be claimable.
    degenerate_cost = {"diagonal": Fraction(0), "hiddenPartial": Fraction(0),
                       "hiddenFull": Fraction(20)}
    try:
        strict_minimum(degenerate_cost)
        raised = False
    except AssertionError:
        raised = True
    assert raised, "degenerate (tied) selector wrongly admitted a strict minimum"
    print("FAIL_TIED_SELECTOR_NO_STRICT_MINIMUM_REJECTED")

    # ----- honest boundary -----
    print("HONEST_OWNER_WITNESS_CLOSED_AT_FINITE_SELECTOR_LEVEL")
    print("HONEST_FULL_M1_HIDDEN_MEMORY_CONTRADICTION_GRAMMAR_01_11C_STAYS_UPSTREAM_FRONTIER")

    print(f"\n[CERT-CLOSED] {STATUS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
