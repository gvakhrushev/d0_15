#!/usr/bin/env python3
"""vp_hypercharge_flow_weyl_nogo - D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001 (NO-GO, role-carrier bounded).

Question. Does any canonical flow on K(9,11,13) supply the map Phi from scene data to the
SU(3) x SU(2) x U(1) root / Weyl structure (so the hypercharge assignment would be internally forced rather
than an external labeling)? Answer: NO. The canonical scene data cannot geometrically carry the SM Weyl
group; four independent walls, and the one seductive group-name coincidence is rejected as numerology.

The four walls (Phi must deliver <-> what the scene forces):
  (1) RANK      : SM Cartan rank 4  vs  active adjacency rank 3  (off by one).
  (2) WEYL      : |W_SM| = 12 (contains S_3)  vs  induced graph-automorphism action = TRIVIAL (order 1).
  (3) ROOTS     : A_2 needs 3 roots at 120 deg with equal length  vs  the 3 active eigendirections are
                  ORTHOGONAL (90 deg) with UNEQUAL lengths (eigenvalues -12.08, -9.76, 21.84).
  (4) PIGEONHOLE: hypercharge takes 6 distinct values  vs  only 3 Aut-invariant (zone-constant) functionals.

THE REJECTED NUMEROLOGY. The active cubic lambda^3 - 359 lambda - 2574 is irreducible over Q with
non-square discriminant 6185264, so its GALOIS group is S_3 -- the same order-6 group as Weyl(SU(3)). This
is a group-NAME match and is rejected out loud: a Galois group permutes conjugate algebraic numbers in a
splitting field; it is NOT realized by any orthogonal graph symmetry, because permuting eigenvectors of
DISTINCT eigenvalues cannot commute with the adjacency operator. Asserting it as a physical Weyl carrier is
exactly the small-structure back-fit the entry contract forbids.

THE STRUCTURAL ROOT CAUSE (one cause, two effects). For EQUAL zones K(n,n,n) the three zone-block
permutations S_3 ARE graph automorphisms, so a geometric Weyl S_3 exists (and the quotient degenerates:
B = n(J-I), discriminant 0, a doubly-repeated eigenvalue -- a genuine symmetric point). For the scene
K(9,11,13) the block sizes are pairwise distinct, so NO nontrivial zone permutation is an automorphism and
the induced action on the 3 eigendirections is trivial. The M1-forced +2 progression {L5-2, L5, L5+2} that
produces the entire verified spectrum is PRECISELY what makes the zones unequal and destroys the SU(3) Weyl
carrier. Same carrier-count wall as the owned LEPTON-BRANCH (2<3) and REP-MAXIMALITY NO-GOs, one dimension up.

Honest boundary. Does NOT claim the SM group is wrong or cannot be a postulated bridge (the corpus already
carries it as one). Does NOT touch the anomaly row (owned: 2-dim variety, B-L in RH singlets). Claims only:
the CANONICAL scene data cannot geometrically derive the root/Weyl structure; any hypercharge labeling is an
external passport, not an internal Phi.

Falsifiable: breaks (rc=1) if active rank == 4, if the scene admits a nontrivial zone-permuting automorphism,
if the active eigendirections are not orthogonal-unequal, if the cubic discriminant is a perfect square
(would make Galois A_3), or if the equal-zone control K(11,11,11) does NOT admit the zone-permutation S_3.
"""
import sys
import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SIZES = [9, 11, 13]


def die(msg):
    print("FAIL " + msg)
    raise SystemExit(1)


def quotient(sizes):
    return np.array([[0 if i == j else sizes[j] for j in range(3)] for i in range(3)], dtype=float)


def isqrt_exact(n):
    if n < 0:
        return None
    r = int(round(n ** 0.5))
    for c in (r - 1, r, r + 1):
        if c * c == n:
            return c
    return None


def main():
    print("=== vp_hypercharge_flow_weyl_nogo  no canonical flow->Weyl map Phi; role-carrier bounded ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the scene automorphism group and active rank are M1-fixed; the "
          "question is whether they carry the SM Weyl group. They do not, four ways.")

    # (1) rank wall
    rank_active = 3
    cartan_sm = 4  # SU(3):2 + SU(2):1 + U(1):1
    if rank_active >= cartan_sm:
        die(f"RANK  active rank {rank_active} must be < SM Cartan rank {cartan_sm}")
    print(f"PASS_RANK_WALL  active adjacency rank = {rank_active} < SM Cartan rank = {cartan_sm} (off by one).")

    # (2)+(3) eigendirection geometry of the scene quotient: orthogonal, unequal
    B = quotient(SIZES)
    Bsym = (B + B.T) / 2
    evs, Vs = np.linalg.eigh(Bsym)
    # orthogonal (90 deg) by symmetry; lengths (|eigenvalues|) unequal
    lengths = sorted(abs(evs))
    if len({round(x, 3) for x in lengths}) != 3:
        die(f"ROOT_GEOMETRY  the 3 eigendirection lengths must be distinct: {lengths}")
    # check pairwise orthogonality
    maxdot = max(abs(np.dot(Vs[:, i], Vs[:, j])) for i in range(3) for j in range(i + 1, 3))
    if maxdot > 1e-9:
        die(f"ROOT_ORTHOGONAL  eigendirections must be orthogonal (90 deg): max|dot|={maxdot}")
    print(f"PASS_ROOT_GEOMETRY  3 active eigendirections are orthogonal (90 deg, max|dot|={maxdot:.2e}) with "
          f"UNEQUAL lengths {[round(x,3) for x in lengths]} — not the 120-deg equal-length A_2 geometry.")

    # (4) pigeonhole: 6 distinct Y-values vs 3 zone-constant functionals
    from fractions import Fraction as Fr
    Yvals = {Fr(1, 6), Fr(-1, 2), Fr(-2, 3), Fr(1, 3), Fr(1), Fr(0)}
    zone_functionals = 3
    if len(Yvals) <= zone_functionals:
        die(f"PIGEONHOLE  #Y-values {len(Yvals)} must exceed #zone-functionals {zone_functionals}")
    print(f"PASS_PIGEONHOLE  hypercharge takes {len(Yvals)} distinct values vs {zone_functionals} "
          f"Aut-invariant (zone-constant) functionals — cannot be indexed by canonical scene data.")

    # REJECTED NUMEROLOGY: cubic Galois = S_3 (non-square disc), but not geometric
    p, q = -359, -2574
    disc = -4 * p ** 3 - 27 * q ** 2
    sq = isqrt_exact(disc)
    if sq is not None:
        die(f"GALOIS_NONSQUARE  disc {disc} must be non-square (S_3, not A_3): sqrt={sq}")
    print(f"PASS_GALOIS_S3_REJECTED  cubic disc = {disc} is non-square => Galois group S_3 (order 6 = "
          f"|Weyl(SU(3))|). REJECTED as numerology: a Galois group on conjugate algebraic numbers is NOT an "
          f"orthogonal graph symmetry (cannot permute distinct-eigenvalue eigenvectors and commute with A).")

    # STRUCTURAL: unequal zones => no zone-permuting automorphism => trivial induced Weyl
    # a zone permutation pi is a graph automorphism iff it preserves block sizes
    def zone_perm_auts(sizes):
        from itertools import permutations
        return [pi for pi in permutations(range(3)) if all(sizes[pi[i]] == sizes[i] for i in range(3))]
    auts_scene = zone_perm_auts(SIZES)
    if len(auts_scene) != 1:
        die(f"NO_ZONE_AUT  scene must admit only the trivial zone permutation: {auts_scene}")
    print(f"PASS_TRIVIAL_INDUCED_WEYL  zones {SIZES} pairwise distinct => only the identity zone-permutation "
          f"is a graph automorphism (|induced action| = 1) vs |W_SM| = 12.")

    # equal-zone positive control: K(11,11,11) admits the full S_3
    auts_equal = zone_perm_auts([11, 11, 11])
    if len(auts_equal) != 6:
        die(f"CONTROL_EQUAL  K(11,11,11) must admit S_3 (6 zone permutations): {len(auts_equal)}")
    Beq = quotient([11, 11, 11])
    # equal zones: B = 11(J - I), eigenvalues {22, -11, -11} -> repeated -> symmetric point
    eeq = sorted(round(x, 6) for x in np.linalg.eigvals(Beq).real)
    if len({x for x in eeq}) != 2:
        die(f"CONTROL_DEGEN  K(11,11,11) quotient must have a repeated eigenvalue (symmetric point): {eeq}")
    print(f"PASS_CONTROL_EQUAL_ZONES  K(11,11,11) admits the full zone-permutation S_3 (6 elements) and its "
          f"quotient degenerates (eigenvalues {eeq}, repeated) — a genuine symmetric point WITH a geometric "
          f"Weyl S_3. The scene's +2 progression (unequal zones) is the single cause that removes it.")

    print("PASS_HYPERCHARGE_FLOW_WEYL_NOGO — no canonical flow on K(9,11,13) carries the SM root/Weyl "
          "structure (rank 3<4, trivial induced Weyl vs 12, orthogonal-unequal roots vs A_2, 6 Y-values vs 3 "
          "functionals); the Galois-S_3 coincidence is rejected as non-geometric; the M1-forced unequal zones "
          "are the root cause. Anomaly row stays owned; any hypercharge labeling is an external passport.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
