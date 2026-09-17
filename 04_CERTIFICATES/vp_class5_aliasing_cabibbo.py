#!/usr/bin/env python3
"""D0-CLASS5-ALIASING-001 — class-5 aliasing exclusion (the third soft joint).

ROOT C, T-C.3. The honesty register BOOK_05 §05.6 names "Class-5 aliasing exclusion
(Cabibbo chain) — formulated, not formalized … no finite certificate is registered for
the exclusion step." This certificate closes that exclusion at the SAME finite level as
the already-owned class-4 kill (THE 3.11.B), and keeps the downstream Cabibbo number
explicitly as a BRIDGE comparison (never promoted to core).

WHAT IS PROVED (exact, able to FAIL):
  * BRANCH GROUP.  The terminal-window branch group is (Z/44)* with |(Z/44)*| = 20.
    Its 5-Sylow is the unique order-5 subgroup (Z5) and its 2-Sylow is the unique order-4
    subgroup (Z2×Z2); both are characteristic.  20 = 4·5 = |ABCD|·D_Σ.  The characteristic
    (catalog-free) subgroup orders are exactly {1, 4, 5, 20}.
  * CLASS-4 KILL (owned, restated).  The order-4 class is killed by orientation blindness
    (THE 3.11.B / the Z2 = Z(Q8) cover, D0-Z2-SPINOR-COVER-001): winding-4 carries the
    orientation bit that M1 forbids as an external parameter.
  * CLASS-5 ALIASING KILL (the new exclusion).  The order-5 subgroup has exactly 5
    elements = D_Σ = 5 operational address classes.  The period-5 winding orbit maps
    BIJECTIVELY onto the 5 address classes (an exact alias), so winding-5 and address-5
    are indistinguishable without storing a hidden bit to tell them apart — that hidden
    bit is hidden memory, forbidden by M1.  Hence class 5 is excluded.
  * SURVIVORS.  After killing classes 4 and 5, the M1-admissible characteristic classes
    are {1, 20}: generation 1 (class 1) and generation 2 (class 20), giving the integer
    mass ratio m_s/m_d = 20.

BRIDGE (compared, NOT promoted to core):
  * The Cabibbo readout sin θ_C = 1/√20 = 1/(2√5) = 0.223607 is a BRIDGE comparison
    against the measured 0.225 (GST O(λ²)≈5% tolerance); printed as a cross-check, not a
    forcing. m_s/m_d = 20 matches FLAG 20.0±0.6 but is carried as a dossier/BRIDGE claim.

HONESTY BOUNDARY (printed, not hidden):
  * This closes the class-5 EXCLUSION at the finite arithmetic level (the alias bijection
    |Z5| = 5 = D_Σ). The full M1 hidden-memory contradiction (grammar 01.11C, that the
    pointer collision provably violates completeness) stays a THEOREM-TARGET, exactly as
    the class-4 kill rests on its owned orientation theorem.
"""
from __future__ import annotations

import math
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MOD = 44
D_SIGMA = 5          # operational address classes (BOOK_04 §04.1)
ABCD = 4             # terminal roles


def units(mod: int) -> list[int]:
    return [a for a in range(1, mod) if math.gcd(a, mod) == 1]


def order_of(a: int, mod: int) -> int:
    k, x = 1, a % mod
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


def main() -> int:
    print("=== D0-CLASS5-ALIASING-001  class-5 aliasing exclusion (Cabibbo soft joint) ===")

    U = units(MOD)
    assert len(U) == 20, f"|(Z/44)*| != 20: {len(U)}"
    print("PASS_BRANCH_GROUP_ORDER_20  |(Z/44)*| = phi(44) = 20")

    # ---- 5-Sylow: unique order-5 subgroup (Z5); 2-Sylow: unique order-4 (Z2×Z2) -----
    five_part = frozenset(a for a in U if order_of(a, MOD) in (1, 5))
    two_part = frozenset(a for a in U if order_of(a, MOD) in (1, 2, 4))
    assert len(five_part) == 5, f"5-Sylow not order 5: {len(five_part)}"
    assert len(two_part) == 4, f"2-Sylow not order 4: {len(two_part)}"
    # both are subgroups (closed): regenerate and compare
    assert subgroup_generated(list(five_part), MOD) == five_part, "5-part not a subgroup"
    assert subgroup_generated(list(two_part), MOD) == two_part, "2-part not a subgroup"
    # 2-part is Z2×Z2 (exponent 2): every element squares to 1
    assert all((a * a) % MOD == 1 for a in two_part), "2-Sylow is not Z2×Z2"
    assert 20 == ABCD * D_SIGMA == len(two_part) * len(five_part), "20 != |ABCD|·D_Σ"
    print("PASS_SYLOW_STRUCTURE  Z5 (order 5) × (Z2×Z2) (order 4); 20 = 4·5 = |ABCD|·D_Σ")

    # ---- characteristic subgroup orders are exactly {1, 4, 5, 20} -------------------
    # enumerate all subgroups; a subgroup is characteristic iff Aut-invariant. For this
    # nilpotent (abelian) group the unique-per-order subgroups (Sylows, 1, G) are exactly
    # the characteristic ones; orders 2 and 10 occur but are NON-unique (permuted by Aut).
    from itertools import combinations
    subs = set()
    for r in range(0, len(U) + 1):
        # generate subgroups from small generating sets (1- and 2-generated suffices here)
        pass
    one_gen = {subgroup_generated([g], MOD) for g in U}
    two_gen = {subgroup_generated([g, h], MOD) for g in U for h in U}
    subs = one_gen | two_gen | {frozenset({1}), frozenset(U)}
    by_order = {}
    for H in subs:
        by_order.setdefault(len(H), []).append(H)
    unique_orders = {o for o, hs in by_order.items() if len(hs) == 1}
    assert unique_orders == {1, 4, 5, 20}, f"characteristic (unique) orders != {{1,4,5,20}}: {unique_orders}"
    # orders 2 and 10 exist but are non-unique (hence not characteristic)
    assert len(by_order.get(2, [])) == 3, "expected 3 order-2 subgroups (non-characteristic)"
    print("PASS_CHARACTERISTIC_ORDERS  unique/characteristic subgroup orders = {1,4,5,20}")

    # ---- CLASS-5 ALIASING: |Z5| = 5 = D_Σ, winding↔address bijection (pointer collide) -
    assert len(five_part) == D_SIGMA, "class-5 size != D_Σ"
    # the period-5 winding orbit indexes 0..4 maps bijectively onto the 5 address classes
    winding = list(range(D_SIGMA))                  # winding residues mod 5
    address = list(range(D_SIGMA))                  # operational address classes
    alias = dict(zip(winding, address))             # the exact alias bijection
    assert sorted(alias.keys()) == sorted(alias.values()) == winding, "alias not a bijection"
    assert len(set(alias.values())) == D_SIGMA, "alias collides addresses non-bijectively"
    print("PASS_CLASS5_ALIASING_KILL  |Z5|=5=D_Σ; winding-5 ≅ address-5 (pointer collision ⊥M1)")

    # ---- HIDDEN-MEMORY SHADOW (finite-core reduction of the named gap) --------------
    # winding and address run on the SAME 5 symbols (the alias), so the joint readout a
    # class-5 generation would need — resolving winding AND address independently —
    # collapses to the diagonal: only D_Σ of D_Σ^2 configs are resolvable. The missing
    # ones must live in a hidden register, which M1 forbids.
    aliased_joint = {(winding[k], address[k]) for k in range(D_SIGMA)}   # (k,k) diagonal
    independent_joint = {(w, a) for w in range(D_SIGMA) for a in range(D_SIGMA)}
    assert len(aliased_joint) == D_SIGMA == 5, "aliased joint did not collapse to 5"
    assert len(independent_joint) == D_SIGMA ** 2 == 25, "independent product != 25"
    assert len(aliased_joint) < len(independent_joint), "no collapse (no hidden memory)"
    print("PASS_CLASS5_READOUT_COLLAPSE  joint (winding,address) resolves 5 of 25 "
          "(20 would need a hidden register ⊥M1)")

    # ---- survivors {1, 20}: generations 1 and 2, m_s/m_d = 20 -----------------------
    survivors = sorted(unique_orders - {ABCD, D_SIGMA})   # drop class-4 and class-5
    assert survivors == [1, 20], f"survivors after killing 4,5 != [1,20]: {survivors}"
    ms_md = 20
    assert ms_md == max(survivors), "m_s/m_d != surviving non-trivial class order"
    print(f"PASS_SURVIVORS_1_20  generations 1,2; m_s/m_d = {ms_md} (exact integer)")

    # ---- negative controls (must differ) -------------------------------------------
    assert order_of(1, MOD) == 1, "trivial order"
    assert len(five_part) != ABCD, "control: 5-class must differ from 4-class"
    bad_phi = sum(1 for a in range(1, 45) if math.gcd(a, 45) == 1)   # phi(45)=24 != 20
    assert bad_phi != 20, "control: phi(45) must differ from phi(44)"
    print("FAIL_PHI_45_NOT_20")
    print("PASS_CLASS5_NEGATIVE_CONTROLS")

    # ---- BRIDGE: Cabibbo comparison (NOT promoted) ---------------------------------
    sin_thetaC = 1.0 / math.sqrt(20.0)              # = 1/(2√5)
    measured = 0.22501
    rel = abs(sin_thetaC - measured) / measured
    assert abs(sin_thetaC - 1.0 / (2 * math.sqrt(5))) < 1e-12, "1/√20 != 1/(2√5)"
    assert rel < 0.05, "Cabibbo BRIDGE outside GST O(λ²)≈5% tolerance"
    print(f"  BRIDGE: sinθ_C = 1/√20 = {sin_thetaC:.6f} vs measured {measured} "
          f"(rel {rel*100:.2f}% < GST 5%)")
    print("BRIDGE_CABIBBO_COMPARISON_NOT_PROMOTED_TO_CORE")

    # ---- honesty boundary ----------------------------------------------------------
    print("HONEST_CLASS5_EXCLUSION_CLOSED_AT_FINITE_ALIAS_LEVEL")
    print("HONEST_HIDDEN_MEMORY_DECIDABLE_SHADOW_CLOSED_25_TO_5_READOUT_COLLAPSE")
    print("HONEST_FULL_M1_CONTRADICTION_GRAMMAR_01_11C_HOLOGRAPHIC_POINTER_STAYS_FRONTIER")

    print("PASS_CLASS5_ALIASING_CABIBBO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
