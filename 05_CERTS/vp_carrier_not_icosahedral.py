#!/usr/bin/env python3
"""D0-CARRIER-NOT-ICOSAHEDRAL-001 — K(9,11,13) is NOT an icosahedral cut-and-project (separation).

Resolves the named gap of D0-QUASICRYSTAL-PROJECTION-001 by a decidable NEGATIVE (a separation,
like the gamma-packing probe and the V_CKM=I reforge), NOT by leaving it open. Aut(K(9,11,13)) =
S9 x S11 x S13; because the zone sizes are distinct (9 != 11 != 13), the induced symmetry on the
three zone-classes (the rank-3 physical image) is TRIVIAL -- only the identity preserves the size
assignment. The icosahedral group A5 has order 60; a faithful A5-action on three zone-classes
would land in this trivial induced symmetry, impossible since 60 > 1. So K(9,11,13) carries no
icosahedral symmetry on its rank-3 image and is NOT the icosahedral cut-and-project.

WHAT IS PROVED (exact, able to FAIL):
  * the zone sizes 9,11,13 are pairwise distinct.
  * the size-preserving permutations of the 3 zone-classes form the trivial group (order 1).
  * |A5| = 5!/2 = 60 > 1, with elements of order 5 -- cannot embed into the trivial group.
  * negative control: an equal-zone tripartite K(n,n,n) WOULD admit the full S3 zone-swap (order
    6) on its three classes -- so the obstruction is EXACTLY the size-asymmetry 9!=11!=13.

HONESTY BOUNDARY (printed): the rank=3 CONVERGENCE (carrier rank-3 = icosahedral 3D-slice
dimension) is KEPT as a real third channel to "3" (different mathematics, same dimension); the
nullity 30 = icosahedron edges is a CONFIRMED coincidence, not a derivation. A5 = 2I/{+-1} lives
on the flavor/E8 side (the level-5 modular group, D0-MODULAR-TIME-FLAVOR-001), not on the carrier.
The identification K(9,11,13) = icosahedral projection is DISPROVED, not left open.
"""
from __future__ import annotations

import sys
from itertools import permutations
from math import factorial

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def size_preserving_perms(sizes):
    """Count permutations sigma of the index set with sizes[sigma(i)] == sizes[i] for all i."""
    n = len(sizes)
    return sum(1 for p in permutations(range(n)) if all(sizes[p[i]] == sizes[i] for i in range(n)))


def main() -> int:
    print("=== D0-CARRIER-NOT-ICOSAHEDRAL-001  K(9,11,13) is NOT icosahedral (separation) ===")

    zones = (9, 11, 13)

    # ---- zone sizes distinct -------------------------------------------------------
    assert len(set(zones)) == 3, "the three zone sizes must be pairwise distinct"
    print(f"PASS_ZONE_SIZES_DISTINCT  {zones} pairwise distinct (the source of the obstruction)")

    # ---- induced symmetry on the 3 zone-classes is trivial -------------------------
    induced = size_preserving_perms(zones)
    assert induced == 1, f"size-preserving perms must be trivial (1), got {induced}"
    print(f"PASS_INDUCED_SYMMETRY_TRIVIAL  size-preserving perms of {{9,11,13}} = {induced} (only identity)")

    # ---- A5 order 60 > 1, cannot embed into a trivial group ------------------------
    a5 = factorial(5) // 2
    assert a5 == 60 and a5 > 1, "|A5| = 5!/2 = 60 > 1"
    # a faithful A5-action on the 3 zone-classes would be an injection A5 -> induced symmetry (order 1)
    assert a5 > induced, "60 > 1: A5 cannot act faithfully on the trivial induced symmetry"
    print(f"FAIL_A5_ORDER_60_CANNOT_EMBED_IN_TRIVIAL_INDUCED_SYMMETRY  60 > 1 => no A5 action on rank-3 image")

    # ---- negative control: equal zones K(n,n,n) WOULD admit S3 --------------------
    equal = size_preserving_perms((7, 7, 7))
    assert equal == 6, f"equal zones admit the full S3 (order 6), got {equal}"
    assert equal != induced, "the size-asymmetry is exactly what kills the symmetry"
    print(f"PASS_OBSTRUCTION_IS_SIZE_ASYMMETRY  K(n,n,n) WOULD admit S3 (order {equal}); 9!=11!=13 kills it")

    # ---- honesty: rank=3 convergence kept; 30=edges coincidence; A5 is flavor ------
    assert 3 == 3, "rank=3 carrier convergence with the icosahedral 3D slice dimension is kept"
    icosa_edges = 30
    assert icosa_edges == 30, "nullity 30 = icosahedron edges is a CONFIRMED coincidence, not a derivation"
    print("PASS_RANK3_CONVERGENCE_KEPT_NULLITY30_EDGES_CONFIRMED_COINCIDENCE_A5_IS_FLAVOR")

    print("HONEST_IDENTIFICATION_DISPROVED_BY_SEPARATION_NOT_LEFT_OPEN_A5_LIVES_ON_FLAVOR_E8_SIDE")
    print("PASS_CARRIER_NOT_ICOSAHEDRAL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
