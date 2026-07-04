#!/usr/bin/env python3
"""vp_rank3_cubic_symmetric_functions - D0-RANK3-CUBIC-SYMMETRIC-FUNCTIONS-001 (POSITIVE, forced).

The rank-3 characteristic cubic lambda^3 - 359 lambda - 2574 -- shared by the isotropization residual
(D0-ISOTROPIZATION-MECH-001) and the causal-cone forcing (D0-RANK3-CAUSAL-CONE-FORCING-001) -- has BOTH
non-leading coefficients equal to exact elementary symmetric functions of the scene zone sizes, via the
zone-quotient adjacency B (B_ij = n_j for i != j, 0 on the diagonal):
    e1(B) = tr B = 0,
    e2(B) = -(n1 n2 + n1 n3 + n2 n3) = -359 = -|E|,
    e3(B) = det B = 2 n1 n2 n3 = 2*1287 = 2574.
So the cubic is exactly  lambda^3 - |E| * lambda - 2 * (prod of zone sizes).

Two identities make this forced, not a readout:
  (i)  the sum of pairwise zone products EQUALS the edge count of the complete multipartite graph:
       n1 n2 + n1 n3 + n2 n3 = (N^2 - sum n_i^2)/2 = |E|  (each zone pair contributes n_i n_j edges);
  (ii) the zone-quotient determinant is TWICE the product: det B = 2 n1 n2 n3 (a 3x3 zero-diagonal
       identity: det[[0,b,c],[a,0,c],[a,b,0]] = 2abc when the columns share the pattern B_ij = n_j).
Both are forced by the +2 zone sizes {9,11,13} alone (the same object underlying the forced Laplacian
spectrum, D0-SCENE-LAPLACIAN-SPECTRUM-FORCED-001). This SHARPENS the prior note 'coeffs = scene symmetric
functions (e2=359, 2e3=2574)' to the exact named-invariant identification e2 = -|E|, e3 = 2*prod, so the
cubic that fixes the 3 reversible spacelike modes carries zero free integers.

Honest scope: this owns the COEFFICIENTS as forced scene invariants. It does NOT touch the two standing
limits: the isotropization dimensionful amplitude stays MECH-LIMIT (no number claimed), and the
rank<->metric-cone physical identification stays a NAMED BRIDGE (ASSUMP-CONNES-RECONSTRUCTION). The
discriminant 6185264 > 0 (3 distinct real roots) is re-checked here as the downstream consequence.

Falsifiable: breaks (rc=1) if e2(B) != -|E|, if e3(B) != 2*prod, if the pairwise-sum != |E| identity fails,
if the cubic coefficients != (0, -359, -2574), or if the discriminant is not > 0.
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SIZES = [9, 11, 13]
N = sum(SIZES)


def die(msg):
    print("FAIL " + msg)
    raise SystemExit(1)


def main():
    print("=== vp_rank3_cubic_symmetric_functions  lambda^3 - |E| lambda - 2*prod, forced coeffs ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the zone sizes {9,11,13} are M1-forced; the cubic coefficients "
          "are their elementary symmetric functions, computed not fit.")

    n1, n2, n3 = SIZES
    E = (N * N - (n1 * n1 + n2 * n2 + n3 * n3)) // 2
    prod = n1 * n2 * n3
    pairwise = n1 * n2 + n1 * n3 + n2 * n3

    # zone-quotient adjacency B_ij = n_j (i != j), 0 diagonal
    B = [[0 if i == j else SIZES[j] for j in range(3)] for i in range(3)]

    # e1 = trace
    e1 = sum(B[i][i] for i in range(3))
    if e1 != 0:
        die(f"E1_TRACE  tr(B) must be 0: {e1}")
    # e2 = sum of 2x2 principal minors
    e2 = 0
    for i in range(3):
        for j in range(i + 1, 3):
            e2 += B[i][i] * B[j][j] - B[i][j] * B[j][i]
    # e3 = det(B)
    e3 = (B[0][0] * (B[1][1] * B[2][2] - B[1][2] * B[2][1])
          - B[0][1] * (B[1][0] * B[2][2] - B[1][2] * B[2][0])
          + B[0][2] * (B[1][0] * B[2][1] - B[1][1] * B[2][0]))

    # (i) pairwise product sum = |E|
    if pairwise != E:
        die(f"PAIRWISE_IS_EDGES  n1n2+n1n3+n2n3={pairwise} must equal |E|={E}")
    print(f"PASS_PAIRWISE_IS_EDGECOUNT  n1n2+n1n3+n2n3 = {pairwise} = |E| = (N^2-sum n^2)/2 = {E} "
          f"(each zone pair contributes n_i n_j edges of the complete multipartite graph).")

    # e2 = -pairwise = -|E|
    if e2 != -pairwise or e2 != -E:
        die(f"E2_IS_EDGES  e2(B)={e2} must equal -|E|={-E}")
    print(f"PASS_E2_IS_MINUS_EDGES  e2(B) = -(sum pairwise) = {e2} = -|E|: the linear coefficient of the "
          f"cubic is -|E| = -359.")

    # (ii) det B = 2*prod
    if e3 != 2 * prod:
        die(f"E3_IS_TWICE_PROD  det(B)={e3} must equal 2*prod={2*prod}")
    print(f"PASS_E3_IS_TWICE_PRODUCT  e3(B) = det(B) = {e3} = 2*n1*n2*n3 = 2*{prod}: the constant term is "
          f"2*(product of zone sizes) = 2574.")

    # assemble cubic: lambda^3 - e1 lambda^2 + e2' ... standard: char poly = lambda^3 - e1 lambda^2 + e2sym lambda - e3
    # for zero trace: lambda^3 + e2 lambda - e3  where e2 here is the 2nd elementary symmetric fn = -pairwise
    # => lambda^3 - pairwise*lambda - det = lambda^3 - 359 lambda - 2574
    coeffs = (1, -e1, e2, -e3)  # (lam^3, lam^2, lam^1, lam^0)
    if coeffs != (1, 0, -359, -2574):
        die(f"CUBIC_COEFFS  characteristic cubic must be (1,0,-359,-2574): {coeffs}")
    print(f"PASS_CUBIC_IS_FORCED  characteristic cubic of the zone quotient = lambda^3 - |E|*lambda "
          f"- 2*prod = lambda^3 - 359 lambda - 2574 (both non-leading coeffs forced scene invariants).")

    # downstream: discriminant of depressed cubic lambda^3 + p lambda + q, p=-359, q=-2574: disc=-4p^3-27q^2
    p, q = -359, -2574
    disc = -4 * p ** 3 - 27 * q ** 2
    if disc <= 0:
        die(f"DISCRIMINANT  depressed-cubic discriminant must be > 0: {disc}")
    if disc != 6185264:
        die(f"DISCRIMINANT_VALUE  discriminant must be 6185264: {disc}")
    print(f"PASS_DISCRIMINANT_POSITIVE  disc = -4p^3-27q^2 = {disc} > 0: 3 distinct REAL roots (the 3 "
          f"reversible spacelike modes) — the downstream causal-cone consequence, re-checked.")

    print("PASS_RANK3_CUBIC_SYMMETRIC_FUNCTIONS — the rank-3 cubic lambda^3-359lambda-2574 is exactly "
          "lambda^3 - |E|*lambda - 2*prod(zones), both coefficients forced elementary symmetric functions "
          "of the zone quotient; isotropization amplitude stays MECH-LIMIT, cone identification stays a "
          "named bridge (neither claimed here).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
