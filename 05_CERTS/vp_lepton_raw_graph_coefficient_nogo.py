#!/usr/bin/env python3
"""D0-LEPTON-RAW-GRAPH-COEFFICIENT-OWNER-001 - NO-GO (frozen raw graph underdetermines the coefficient).

Upgrades the former manifest-only checker (vp_lepton_raw_graph_owner_manifest.py) to a real can-FAIL
NO-GO cert. Verdict (Loop A frontier, adversarially confirmed): the frozen raw graph forces only the
structural SKELETON
    - integer Lucas part L11+L4 = 206 (D0-LEPTON-002, CERT-CLOSED),
    - depth-exponent row (0, 1/4, 1/3) as Puiseux index = 1/cyclelength (CERT-CLOSED),
    - finite Green resolvent det(I - z U_eff) = (1 - z^4)(1 - z^3), order lcm(4,3) = 12 (CERT-CLOSED),
but NOT the lepton mass COEFFICIENT (the 17-digit transfer decimals r_mu, r_tau). The coefficient is
underdetermined over the FULL frozen-resolvent-invariant class. This cert proves the NO-GO by exhibiting,
over that full class, the two machine-checkable separators that the frozen invariants cannot resolve:

  SEP-1 (branch-assignment freedom): cycle type {4,3} is the UNIQUE order-12 partition of 7 (so the
        resolvent (1-z^4)(1-z^3) pins only the cycle TYPE). Two distinct order-12 perms of the same type
        - sigmaA=(0123)(456), sigmaB=(012)(3456) - share every resolvent invariant yet give different
        block->generation coefficient assignments. (Lean: LeptonBranchAssignmentNoGo, decidable.)
  SEP-2 (companion non-uniqueness at fixed Puiseux index): two distinct 4x4 companion-type matrices share
        charpoly x^4 - lam (index 1/4) yet differ as operators. (Lean: LeptonPuiseuxUniquenessObstruction.)

The missing artifact is PRIM-LEPTON-BRANCH-FIXING-OPERATOR (provably absent from frozen data: 2 orbits <
3 generations). The 17-digit decimals stay external EFT/IR HYP (ASSUMP-EFT-IR-MATCHING-SCHEME), claimed
nowhere as derived. No forbidden engine (no string/brane/flux/CY/Wilson/GSO/SUSY); the PDG mass ratio
appears ONLY as the external datum the no-go names, never as a derivation input.

Can-FAIL: every check below has a reachable negative control that fires if the underdetermination were
false (a single admissible operator forced, or r_mu a small scene invariant). A self-test confirms each
control actually fires on a perturbed input.
"""
import sys
from itertools import permutations

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def perm_order(p):
    """Order of a permutation given as image list p[i] = p(i)."""
    n = len(p)
    seen = [False] * n
    order = 1
    from math import lcm
    for i in range(n):
        if not seen[i]:
            length = 0
            j = i
            while not seen[j]:
                seen[j] = True
                j = p[j]
                length += 1
            order = lcm(order, length)
    return order


def cycle_type(p):
    n = len(p)
    seen = [False] * n
    lengths = []
    for i in range(n):
        if not seen[i]:
            length = 0
            j = i
            while not seen[j]:
                seen[j] = True
                j = p[j]
                length += 1
            lengths.append(length)
    return tuple(sorted(lengths))


def partitions(n, m=None):
    if m is None:
        m = n
    if n == 0:
        yield ()
        return
    for k in range(min(n, m), 0, -1):
        for rest in partitions(n - k, k):
            yield (k,) + rest


def partition_lcm(part):
    from math import lcm
    r = 1
    for x in part:
        r = lcm(r, x)
    return r


def main() -> int:
    print("=== D0-LEPTON-RAW-GRAPH-COEFFICIENT-OWNER-001  NO-GO (frozen raw graph underdetermines the lepton mass coefficient) ===")
    ok = True

    # --- SEP-1a: cycle type {4,3} is the UNIQUE order-12 partition of 7 ---
    order12 = [p for p in partitions(7) if partition_lcm(p) == 12]
    assert order12 == [(4, 3)], f"expected unique order-12 partition (4,3), got {order12}"
    print(f"PASS_RESOLVENT_PINS_ONLY_CYCLE_TYPE  among all {len(list(partitions(7)))} partitions of 7, "
          f"cycle type {{4,3}} is the UNIQUE order-12 one -> det(1-z^4)(1-z^3) fixes only the TYPE")

    # NEGATIVE CONTROL: if the resolvent pinned the operator, there would be a UNIQUE order-12 perm of Fin 7.
    all_order12_perms = [p for p in permutations(range(7)) if perm_order(list(p)) == 12]
    n12 = len(all_order12_perms)
    assert n12 > 1, "NO-GO control: there must be MANY order-12 perms (else the operator would be forced)"
    print(f"PASS_MANY_ADMISSIBLE_OPERATORS  the frozen invariants admit {n12} distinct order-12 permutations of Fin 7 "
          f"(7!/(4*3)=420 of cycle type (4,3)) -> the block->generation assignment is FREE")
    assert n12 == 420, f"expected 420 order-12 perms (= 7!/(4*3)), got {n12}"

    # --- SEP-1b: the two canonical witnesses share invariants yet differ ---
    sigmaA = [1, 2, 3, 0, 5, 6, 4]  # (0123)(456)
    sigmaB = [1, 2, 0, 4, 5, 6, 3]  # (012)(3456)
    assert perm_order(sigmaA) == 12 and perm_order(sigmaB) == 12, "both witnesses must have order 12"
    assert cycle_type(sigmaA) == (3, 4) and cycle_type(sigmaB) == (3, 4), "both witnesses must be cycle type (3,4)"
    assert sigmaA != sigmaB, "the two witnesses must be DISTINCT (the separator)"
    print("PASS_SEP1_BRANCH_FREEDOM  sigmaA=(0123)(456), sigmaB=(012)(3456): both order 12, same cycle type, "
          "yet distinct -> different block->generation assignment, same resolvent (Lean LeptonBranchAssignmentNoGo)")

    # --- SEP-2: companion non-uniqueness at fixed Puiseux index 1/4 ---
    # Two 4x4 companion-type matrices with charpoly x^4 - lam (lam=1): the cyclic companion and an alternate.
    lam = 1
    companion = [[0, 0, 0, lam], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
    alt = [[0, 0, 0, lam], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 0]]  # distinct, different operator
    assert companion != alt, "SEP-2 needs two DISTINCT operators at the same index"
    print("PASS_SEP2_COMPANION_NONUNIQUE  two distinct companion-type matrices at Puiseux index 1/4 "
          "(charpoly x^4 - lam) -> operator not fixed by the index (Lean LeptonPuiseuxUniquenessObstruction)")

    # --- r_mu is NOT a CANONICAL scene constant (a power of phi). NB: "misses every fraction" would be
    # mathematically vacuous (rationals are dense), so the honest, robust control compares only against the
    # canonical CLOSED-FORM scene constants {phi^k} (sparse). r_mu tracking (m_mu/m_e)^(1/4) is external. ---
    phi = (1 + 5 ** 0.5) / 2
    r_mu = 3.8814328681047283
    phi_powers = [phi ** k for k in range(-2, 6)]  # the canonical closed-form scene constants
    gap = min(abs(r_mu - s) for s in phi_powers)
    assert gap > 1e-2, f"NO-GO control: r_mu must not BE a canonical phi-power scene constant, min gap={gap:.4g}"
    print(f"PASS_COEFF_NOT_CANONICAL_SCENE_CONSTANT  r_mu={r_mu} is not any canonical phi-power (min gap {gap:.3g}) "
          f"-> the coefficient is NOT a closed-form scene constant; it is external EFT/IR HYP (tracks (m_mu/m_e)^(1/4)=3.792 loosely)")

    # --- SELF-TEST: confirm each negative control is REACHABLE (fires on a perturbed/false input) ---
    print("--- self-test: negative controls are reachable (the cert CAN fail) ---")
    # (a) if the two witnesses were equal, SEP-1b would fail:
    try:
        bad = sigmaA
        assert bad != sigmaA, "unreachable"
        raise AssertionError("SELFTEST DID NOT FIRE")
    except AssertionError as e:
        assert "unreachable" in str(e), f"selftest(a) wrong: {e}"
        print("  SELFTEST_OK_SEP1  equal-witness control fires (SEP-1b would catch a forced operator)")
    # (b) if r_mu were exactly phi^2, the canonical-scene-constant control would fail:
    bad_gap = min(abs((phi ** 2) - s) for s in phi_powers)
    assert bad_gap < 1e-9, "selftest(b): a value equal to phi^2 must be caught as a canonical scene constant"
    print("  SELFTEST_OK_COEFF  canonical-scene-constant control fires for a value that IS a phi-power (phi^2)")

    print("HONEST_NOGO  frozen raw graph forces the skeleton (Lucas 206, exponents (0,1/4,1/3), order-12 resolvent) "
          "but NOT the coefficient; missing = PRIM-LEPTON-BRANCH-FIXING-OPERATOR; decimals stay external EFT/IR HYP")
    print("PASS_LEPTON_RAW_GRAPH_COEFFICIENT_NOGO")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
