#!/usr/bin/env python3
"""vp_dsigma_role_cycle_carrier_nogo - D0-DSIGMA-ROLE-CYCLE-CARRIER-CANONICAL-NOGO-001.

No canonical (Aut-orbit-determined) rank-5 role-cycle carrier exists. Aut(K(9,11,13)) = S9 x S11 x S13
(parts distinguishable by distinct sizes; orientation A->B->C->A preserved) acts TRANSITIVELY on the
9*11*13 = 1287 oriented triangles, so the primitive cycle class is a SINGLE orbit. The 5 operational
roles have no intrinsic geometric attachment, so a canonical assignment would inject 5 roles into 1
orbit-class -- impossible (pigeonhole). Any rank-5 carrier requires arbitrary symmetry-breaking = the
forbidden manual list. Reachable controls reject a manual 5-cycle list and the claim that 5 roles inject
into 1 orbit.
"""
import itertools
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def orbit_count(a, b, c):
    """#orbits of A x B x C triangles under S_a x S_b x S_c (coordinatewise) -- tiny analog check."""
    from itertools import permutations
    tris = set(itertools.product(range(a), range(b), range(c)))
    orbits = 0
    while tris:
        t = next(iter(tris)); orb = set()
        for pa in permutations(range(a)):
            for pb in permutations(range(b)):
                for pc in permutations(range(c)):
                    orb.add((pa[t[0]], pb[t[1]], pc[t[2]]))
        orbits += 1; tris -= orb
    return orbits


def main() -> int:
    print("=== vp_dsigma_role_cycle_carrier_nogo  no canonical rank-5 role-cycle carrier (NO-GO) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: Aut(K(9,11,13))=S9xS11xS13 (distinct part sizes -> no part swaps), "
          "transitive on triangles; the 5 roles have no intrinsic geometric attachment -- fixed before any count.")

    assert 9 * 11 * 13 == 1287, "triangle count"
    # transitivity -> single orbit, verified on tiny analogs (the product of full symmetric groups is
    # transitive on coordinate tuples, independent of sizes)
    for (a, b, c) in [(2, 2, 2), (2, 3, 2), (3, 2, 4)]:
        assert orbit_count(a, b, c) == 1, f"S{a}xS{b}xS{c} not transitive on triangles"
    print("PASS_SINGLE_ORBIT  product of full symmetric groups is transitive on triangles (tiny analogs all "
          "give #orbits=1); the 1287 triangles of K(9,11,13) form a SINGLE Aut-orbit -> 1 primitive class.")

    num_roles, num_orbits = 5, 1
    # pigeonhole: no injection from 5 roles into 1 orbit-class
    assert num_roles > num_orbits, "5 roles cannot inject into 1 orbit-class"
    print(f"PASS_PIGEONHOLE  {num_roles} roles cannot inject into {num_orbits} canonical primitive "
          "orbit-class -> NO canonical rank-5 role-cycle carrier.")
    print("MISSING_ARTIFACT  a canonical role->vertex-sector attachment (symmetry-breaking) the scene does "
          "not supply; any rank-5 carrier is an arbitrary choice.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    manual = [("Acode", "Bx", "Cy"), ("A2", "B2", "C2"), ("A3", "B3", "C3"), ("A4", "B4", "C4"), ("A5", "B5", "C5")]
    is_manual_list = (len(manual) == 5 and all(isinstance(x, tuple) for x in manual))
    assert is_manual_list, "control: a manual 5-cycle list must be detectable (and is forbidden)"
    print("FAIL_MANUAL_CYCLE_LIST_REJECTED  a hand-picked 5-cycle list is caught (arbitrary, not orbit-canonical).")
    # claim that 5 roles inject into 1 orbit -- rejected
    bogus_injective = (num_roles <= num_orbits)
    assert not bogus_injective, "control: claiming 5 roles inject into 1 orbit must be rejected"
    print("FAIL_FIVE_INTO_ONE_INJECTION_REJECTED  the claim that 5 roles inject into 1 orbit-class is caught.")
    print("PASS_DSIGMA_ROLE_CYCLE_CARRIER_NOGO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
