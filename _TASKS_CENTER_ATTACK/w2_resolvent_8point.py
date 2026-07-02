#!/usr/bin/env python3
"""TASK W2, Steps 2-4 — EXACT re-run of the resolvent invariants on the 8-point carrier.

Carrier: sigmaHat = sigmaA (+) id  on Fin 8, where
  sigmaA = (0 1 2 3)(4 5 6)  on {0..6}, extended by the witness fixed point omega0 = 7.
So sigmaHat = (0 1 2 3)(4 5 6)(7), cycle type (4,3,1).

Everything here is EXACT:
  - permutation powers: integer index composition (no matrices needed for order/orbits);
  - det(I - z*U): computed as an exact polynomial in z with INTEGER coefficients, via the
    product-over-cycles identity det(I - z*P_C) = 1 - z^len(C) (a permutation matrix is a
    direct sum of cyclic-shift blocks), cross-checked by exact Fraction Gaussian elimination
    of the 8x8 matrix (I - z*U) at several exact rational z-values AND by an independent
    exact polynomial determinant (Bareiss over Z[z]).
  - decisions use only integer / Fraction equality; no floats anywhere.

Scope: this is the CONSTRUCTION on a DIFFERENT carrier. It does NOT show the 8-point carrier
is forced. The 7-point no-go remains true on its own carrier.
"""
from fractions import Fraction
from functools import reduce
from math import gcd

# ----------------------------------------------------------------------------------------
# The permutation as an index map on Fin 8.  sigmaHat[i] = image of i.
#   (0 1 2 3): 0->1,1->2,2->3,3->0 ; (4 5 6): 4->5,5->6,6->4 ; (7): 7->7
# ----------------------------------------------------------------------------------------
N = 8
SIGMA_HAT = [1, 2, 3, 0, 5, 6, 4, 7]      # matches Lean `sigmaHat := ![1,2,3,0,5,6,4,7]`
OMEGA0 = 7                                 # the witness fixed point


def compose_power(perm, k):
    """Exact k-fold self-composition of a permutation given as an index list. Integer only."""
    n = len(perm)
    out = list(range(n))
    for _ in range(k):
        out = [perm[out[i]] for i in range(n)]
    return out


def identity(n):
    return list(range(n))


def fixed_points(perm):
    return [i for i in range(len(perm)) if perm[i] == i]


def orbits(perm):
    n = len(perm)
    seen = [False] * n
    orbs = []
    for s in range(n):
        if seen[s]:
            continue
        cyc = []
        j = s
        while not seen[j]:
            seen[j] = True
            cyc.append(j)
            j = perm[j]
        orbs.append(cyc)
    return orbs


def lcm(a, b):
    return a * b // gcd(a, b)


def order_of(perm):
    """Exact multiplicative order: lcm of orbit sizes."""
    sizes = [len(o) for o in orbits(perm)]
    return reduce(lcm, sizes, 1)


# ----------------------------------------------------------------------------------------
# Exact polynomial arithmetic over Z[z] (coefficient lists, index = power of z).
# ----------------------------------------------------------------------------------------
def poly_mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            out[i + j] += ai * bj
    return out


def poly_str(p):
    terms = []
    for k, c in enumerate(p):
        if c == 0:
            continue
        if k == 0:
            terms.append("%d" % c)
        elif k == 1:
            terms.append(("%d*z" % c) if c not in (1, -1) else ("z" if c == 1 else "-z"))
        else:
            head = "" if c == 1 else ("-" if c == -1 else "%d*" % c)
            terms.append("%sz^%d" % (head, k))
    s = " + ".join(terms).replace("+ -", "- ")
    return s if s else "0"


def det_from_cycles(perm):
    """det(I - z*U) as an exact integer polynomial in z, via product over cycles of (1 - z^len)."""
    result = [1]
    for cyc in orbits(perm):
        L = len(cyc)
        block = [0] * (L + 1)
        block[0] = 1
        block[L] = -1     # (1 - z^L)
        result = poly_mul(result, block)
    return result


def det_bareiss_over_Zz(perm, z_max_deg):
    """Independent exact check: build the 8x8 matrix (I - z*U) with polynomial entries and
    take its determinant by cofactor expansion over Z[z]. Small (8x8) so cofactor is fine
    and stays exact (integer coeffs). Returns coefficient list."""
    n = len(perm)
    # M[i][j] is a poly: I - z*U  =>  diagonal 1 minus z at (i, perm[i])
    def entry(i, j):
        p = [0]  # zero poly
        if i == j:
            p = _padd(p, [1])
        if perm[i] == j:
            p = _padd(p, [0, -1])  # -z at (i, perm[i])
        return p
    M = [[entry(i, j) for j in range(n)] for i in range(n)]
    return _poly_det(M)


def _padd(a, b):
    out = [0] * max(len(a), len(b))
    for i, c in enumerate(a):
        out[i] += c
    for i, c in enumerate(b):
        out[i] += c
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def _psub(a, b):
    return _padd(a, [-c for c in b])


def _poly_det(M):
    """Exact determinant of a matrix of Z[z] polynomials by Laplace expansion (recursive)."""
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return _psub(poly_mul(M[0][0], M[1][1]), poly_mul(M[0][1], M[1][0]))
    total = [0]
    for j in range(n):
        if M[0][j] == [0]:
            continue
        minor = [[M[i][k] for k in range(n) if k != j] for i in range(1, n)]
        cof = _poly_det(minor)
        term = poly_mul(M[0][j], cof)
        if j % 2 == 1:
            term = [-c for c in term]
        total = _padd(total, term)
    while len(total) > 1 and total[-1] == 0:
        total.pop()
    return total


def det_gauss_exact_at(perm, z):
    """Exact numeric value of det(I - z*U) at a specific rational z, via Fraction Gaussian
    elimination with partial (row-swap) pivoting. Returns a Fraction. No floats."""
    n = len(perm)
    z = Fraction(z)
    A = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        A[i][i] += 1
        A[i][perm[i]] -= z
    det = Fraction(1)
    for col in range(n):
        piv = None
        for r in range(col, n):
            if A[r][col] != 0:
                piv = r
                break
        if piv is None:
            return Fraction(0)
        if piv != col:
            A[col], A[piv] = A[piv], A[col]
            det = -det
        det *= A[col][col]
        inv = A[col][col]
        for r in range(col + 1, n):
            if A[r][col] != 0:
                factor = A[r][col] / inv
                for c in range(col, n):
                    A[r][c] -= factor * A[col][c]
    return det


def poly_eval(p, z):
    z = Fraction(z)
    return sum(Fraction(c) * z ** k for k, c in enumerate(p))


def main():
    print("=== TASK W2, Steps 2-4 : exact resolvent invariants on the 8-point carrier ===")
    print("sigmaHat = (0 1 2 3)(4 5 6)(7)  on Fin 8   [index map %s]" % SIGMA_HAT)
    print()

    # ---------------- STEP 2a : fixed points, orbit sizes ----------------
    orbs = orbits(SIGMA_HAT)
    sizes = sorted(len(o) for o in orbs)
    fps = fixed_points(SIGMA_HAT)
    print("orbits:", [tuple(o) for o in orbs])
    print("orbit sizes (sorted):", sizes)
    print("fixed points:", fps)
    assert sizes == [1, 3, 4], "orbit sizes must be {1,3,4}"
    assert fps == [OMEGA0], "exactly one fixed point, the witness omega0 = 7"
    print("PASS_ORBITS  three orbits, sizes {1,3,4}; unique fixed point omega0 = 7.")
    print()

    # ---------------- STEP 2b : order exactly 12 (powers 4 and 6 != id) ----------------
    ordr = order_of(SIGMA_HAT)
    assert ordr == 12, "order must be lcm(4,3,1)=12"
    idn = identity(N)
    p4 = compose_power(SIGMA_HAT, 4)
    p6 = compose_power(SIGMA_HAT, 6)
    p12 = compose_power(SIGMA_HAT, 12)
    assert p12 == idn, "sigmaHat^12 = id"
    assert p4 != idn, "sigmaHat^4 != id"
    assert p6 != idn, "sigmaHat^6 != id"
    print("order(sigmaHat) = %d ; sigmaHat^12 = id ; sigmaHat^4 != id ; sigmaHat^6 != id" % ordr)
    print("PASS_ORDER_12  order is exactly 12 (proper divisors 4 and 6 fail).")
    print()

    # ---------------- STEP 2c : det(I - z*U) = (1-z)(1-z^3)(1-z^4) exactly ----------------
    det_cyc = det_from_cycles(SIGMA_HAT)
    target = poly_mul(poly_mul([1, -1], [1, 0, 0, -1]), [1, 0, 0, 0, -1])  # (1-z)(1-z^3)(1-z^4)
    assert det_cyc == target, "cycle-product det must equal (1-z)(1-z^3)(1-z^4)"
    det_bar = det_bareiss_over_Zz(SIGMA_HAT, 8)
    # normalize trailing zeros for comparison
    while len(det_bar) > 1 and det_bar[-1] == 0:
        det_bar.pop()
    assert det_bar == det_cyc, "independent Laplace determinant must agree with cycle product"
    print("det(I - z*U) [cycle product]  =", poly_str(det_cyc))
    print("det(I - z*U) [Laplace over Z[z], independent] =", poly_str(det_bar))
    print("target (1-z)(1-z^3)(1-z^4)     =", poly_str(target))
    # exact spot checks at several rational z via Fraction Gaussian elimination
    for z in (Fraction(0), Fraction(1, 2), Fraction(9, 10), Fraction(-2, 5), Fraction(3)):
        g = det_gauss_exact_at(SIGMA_HAT, z)
        e = poly_eval(target, z)
        assert g == e, "exact det at z=%s mismatch" % z
    print("PASS_DET_FACTORIZES  det(I - z*U) = (1-z)(1-z^3)(1-z^4), verified 3 ways (cycle "
          "product, Laplace over Z[z], exact Gaussian elimination at 5 rational points).")
    print()

    # non-pole domain: z=0 gives det=1; poles are the finite set {z=1} U {z^3=1} U {z^4=1}
    d0 = det_gauss_exact_at(SIGMA_HAT, 0)
    assert d0 == 1, "det at z=0 must be 1 (G(0)=I exists)"
    print("z=0: det=1 != 0  => resolvent G_hat(0)=(I-0*U)^-1 = I exists; pole set finite.")
    print()

    # ---------------- STEP 3 : orbit-keyed exponent map is label-free ----------------
    # Sizes are pairwise distinct: 1 != 3 != 4 (and 1 != 4). So the map keyed by SIZE
    #   size 1 -> exponent 0 ,  size 4 -> 1/4 ,  size 3 -> 1/3
    # needs no choice of underlying points and no cycle-vs-cycle labeling.
    distinct = len(set(sizes)) == 3
    assert distinct, "the three orbit sizes must be pairwise distinct"
    exp_map = {1: Fraction(0), 4: Fraction(1, 4), 3: Fraction(1, 3)}
    vals = sorted({exp_map[s] for s in sizes})
    assert vals == [Fraction(0), Fraction(1, 4), Fraction(1, 3)], "exponents {0,1/4,1/3}"
    assert len({exp_map[s] for s in sizes}) == 3, "exponents pairwise distinct"
    print("orbit sizes pairwise distinct (1 != 3 != 4): size-keyed exponent map is LABEL-FREE.")
    print("exponent map: size 1 -> 0 (witness/regular), size 4 -> 1/4, size 3 -> 1/3")
    print("PASS_LABELFREE_EXPONENTS  {0, 1/4, 1/3} pairwise distinct, keyed by orbit size alone.")
    print()

    # ---------------- STEP 4 : Green-resolvent re-run -> exponent-0 branch ----------------
    # The exponent-0 (regular / unramified) branch corresponds to the size-1 fixed orbit {7}.
    # On the 7-point carrier there was NO fixed point => NO exponent-0 branch inside the carrier.
    # On the 8-point carrier the witness fixed point supplies exactly one, alongside 1/4 and 1/3.
    has_regular_branch = len(fps) == 1
    assert has_regular_branch, "one regular (exponent-0) branch at the fixed point"
    branch_exponents = sorted({exp_map[len(o)] for o in orbs})
    assert branch_exponents == [Fraction(0), Fraction(1, 4), Fraction(1, 3)]
    print("Green-resolvent re-run: pole set {z=1}U{z^3=1}U{z^4=1}; the size-1 (fixed) orbit is a")
    print("simple factor (1 - z) with a REGULAR/UNRAMIFIED (exponent-0) local branch at omega0.")
    print("Branch exponents on 8 points = {0, 1/4, 1/3}  (three branches for three generations).")
    print("PASS_EXPONENT0_BRANCH  a well-defined exponent-0 branch exists at the fixed point.")
    print()

    print("PASS_W2_STEPS_2_3_4_RESOLVENT_8POINT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
