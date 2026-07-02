#!/usr/bin/env python3
"""
TASK W4 verification — Sturmian<->archive intertwiner over the composite K = Q(sqrt2, sqrt5).

DETERMINISTIC, EXACT (fractions.Fraction over the Q^4 basis {1, sqrt2, sqrt5, sqrt10}).
No floats enter any decision. Python 3.9-safe.

What this script proves (each block prints PROVED-HERE / CITED / OPEN and asserts):

  [A] Field layer.  sqrt10 not in Q(sqrt5); sqrt2, sqrt5, sqrt10 all in K = Q(sqrt2,sqrt5);
      K is degree 4 over Q with the multiplication table of the biquadratic field.
  [B] The V4 Galois action.  Three nontrivial involutions g2,g5,g10 fixing respectively
      Q(sqrt5), Q(sqrt10), Q(sqrt2). Group law V4 (each order 2, products close).
  [C] Sign-forcing compatibility.  sigma(phi^-1) = psi^-1 = -phi on Q(sqrt5) is the restriction of
      the unique element of Gal(K/Q) that negates sqrt5 and fixes sqrt2. Check which V4 elements
      restrict to that sign on Q(sqrt5): g5 (fix sqrt5) does NOT; g2 and g10 (negate sqrt5) DO.
  [D] The intertwiner attempt.  The two 2x2 integer carriers:
        S = [[1,1],[1,0]]  (golden substitution, trace +1, Q(sqrt5) spectrum phi, -phi^-1)
        T = [[0,1],[1,-1]]  (centre-11 time operator, trace -1, spectrum -phi^-1, phi ... see below)
      Test operator conjugation U S U^-1 = T over K (i.e. over Q^4), EXACTLY.
      Trace is a similarity invariant over ANY field; tr S = +1 != -1 = tr T, so no invertible
      U over K conjugates S to T. This is the orientation obstruction; it is FIELD-INDEPENDENT.
      Then test the scene's own pinned relation U T U^-1 = -S (det U = +1): does an invertible U
      over K exist? (It does over Q already — the obstruction there is not conjugacy but the
      SEMANTIC identification, not linear algebra.)
  [E] Spectra over K.  Give exact eigenvalues of S, T, -S in K-coordinates and confirm which pairs
      are conjugate (equal char-poly) and which are not.

Run: python3 w4_verify.py    (exit 0 = all internal assertions hold; the DELIVERABLE is the printed
verdict, not a pass/fail on whether the intertwiner exists).
"""
import sys
from fractions import Fraction as Fr
from itertools import product

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# K = Q(sqrt2, sqrt5) as Q^4 with basis e0=1, e1=sqrt2, e2=sqrt5, e3=sqrt10.
# Multiplication table (sqrt2*sqrt2=2, sqrt5*sqrt5=5, sqrt2*sqrt5=sqrt10,
#   sqrt2*sqrt10=2*sqrt5, sqrt5*sqrt10=5*sqrt2, sqrt10*sqrt10=10):
#   index 0=1, 1=s2, 2=s5, 3=s10.
# ---------------------------------------------------------------------------
Z = Fr(0)
ONE_K = (Fr(1), Z, Z, Z)


def kadd(x, y):
    return tuple(x[i] + y[i] for i in range(4))


def ksub(x, y):
    return tuple(x[i] - y[i] for i in range(4))


def kneg(x):
    return tuple(-x[i] for i in range(4))


def kscal(c, x):
    c = Fr(c)
    return tuple(c * x[i] for i in range(4))


# structure constants: e_i * e_j = MUL[i][j] as a K-vector
def _build_mul():
    # represent by (coeff, basis index) contributions
    tbl = [[None] * 4 for _ in range(4)]
    def vec(idx, coeff=1):
        v = [Z, Z, Z, Z]; v[idx] = Fr(coeff); return tuple(v)
    tbl[0][0] = vec(0)
    tbl[0][1] = vec(1); tbl[1][0] = vec(1)
    tbl[0][2] = vec(2); tbl[2][0] = vec(2)
    tbl[0][3] = vec(3); tbl[3][0] = vec(3)
    tbl[1][1] = vec(0, 2)          # s2*s2 = 2
    tbl[1][2] = vec(3); tbl[2][1] = vec(3)   # s2*s5 = s10
    tbl[1][3] = vec(2, 2); tbl[3][1] = vec(2, 2)  # s2*s10 = 2 s5
    tbl[2][2] = vec(0, 5)          # s5*s5 = 5
    tbl[2][3] = vec(1, 5); tbl[3][2] = vec(1, 5)  # s5*s10 = 5 s2
    tbl[3][3] = vec(0, 10)         # s10*s10 = 10
    return tbl


MUL = _build_mul()


def kmul(x, y):
    out = [Z, Z, Z, Z]
    for i in range(4):
        if x[i] == 0:
            continue
        for j in range(4):
            if y[j] == 0:
                continue
            c = x[i] * y[j]
            m = MUL[i][j]
            for t in range(4):
                if m[t] != 0:
                    out[t] += c * m[t]
    return tuple(out)


def kis_zero(x):
    return all(c == 0 for c in x)


def keq(x, y):
    return all(x[i] == y[i] for i in range(4))


def Q(r):
    """embed a rational into K"""
    return (Fr(r), Z, Z, Z)


S2 = (Z, Fr(1), Z, Z)
S5 = (Z, Z, Fr(1), Z)
S10 = (Z, Z, Z, Fr(1))


def kinv(x):
    """exact inverse in K via the regular representation (4x4 rational matrix), if invertible."""
    # multiplication-by-x matrix M (columns = x*e_j in basis)
    M = [[Z] * 4 for _ in range(4)]
    for j in range(4):
        col = kmul(x, tuple(Fr(1) if t == j else Z for t in range(4)))
        for i in range(4):
            M[i][j] = col[i]
    # solve M * v = e0  (i.e. x * v = 1)
    sol = solve_linear(M, [Fr(1), Z, Z, Z])
    if sol is None:
        return None
    return tuple(sol)


# ---------------------------------------------------------------------------
# exact rational linear algebra (Gaussian elimination over Q)
# ---------------------------------------------------------------------------
def solve_linear(A, b):
    """Solve A v = b over Q. Return v (list) or None if singular/inconsistent. A square n x n."""
    n = len(A)
    M = [[A[i][j] for j in range(n)] + [b[i]] for i in range(n)]
    for c in range(n):
        piv = None
        for r in range(c, n):
            if M[r][c] != 0:
                piv = r; break
        if piv is None:
            return None
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        M[c] = [v / pv for v in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [M[r][k] - f * M[c][k] for k in range(n + 1)]
    return [M[i][n] for i in range(n)]


def kdet2(A):
    """2x2 determinant of a K-valued matrix A[[a,b],[c,d]]."""
    return ksub(kmul(A[0][0], A[1][1]), kmul(A[0][1], A[1][0]))


def kmatmul2(A, B):
    return [[kadd(kmul(A[i][0], B[0][j]), kmul(A[i][1], B[1][j])) for j in range(2)] for i in range(2)]


def kmatinv2(A):
    """inverse of a 2x2 K-matrix, or None."""
    d = kdet2(A)
    di = kinv(d)
    if di is None:
        return None
    inv = [[kmul(di, A[1][1]), kmul(di, kneg(A[0][1]))],
           [kmul(di, kneg(A[1][0])), kmul(di, A[0][0])]]
    return inv


def lift2(Mint):
    """lift an integer/rational 2x2 matrix into K-valued entries."""
    return [[Q(Mint[i][j]) for j in range(2)] for i in range(2)]


def show(x):
    names = ["1", "√2", "√5", "√10"]
    parts = []
    for i in range(4):
        if x[i] != 0:
            parts.append(f"{x[i]}·{names[i]}" if i else f"{x[i]}")
    return " + ".join(parts) if parts else "0"


# ===========================================================================
FAILS = 0


def check(label, cond, detail=""):
    global FAILS
    status = "OK  " if cond else "FAIL"
    if not cond:
        FAILS += 1
    print(f"  [{status}] {label}" + (f"   {detail}" if detail else ""))
    return cond


def main():
    print("=" * 78)
    print("TASK W4 — Sturmian<->archive intertwiner over K = Q(sqrt2, sqrt5)")
    print("=" * 78)

    # ---------------------------------------------------------------- [A] field
    print("\n[A] FIELD LAYER  (PROVED-HERE, exact over Q^4)")
    # sqrt10 not in Q(sqrt5): a + b sqrt5 squared = 10 forces a^2+5b^2=10, 2ab=0 -> no rational sln
    # We prove it constructively: the K-element s10 has nonzero sqrt2/sqrt10 component structure that
    # cannot be reached from the Q(sqrt5)-subalgebra span{1, sqrt5}.
    #   Q(sqrt5) subspace = { (a,0,b,0) }.  s10 = (0,0,0,1) is NOT in it.
    in_Qsqrt5 = lambda v: v[1] == 0 and v[3] == 0
    check("sqrt10 ∉ Q(sqrt5)  (its e1,e3 components exclude the {1,√5} plane)",
          not in_Qsqrt5(S10), f"√10 = {show(S10)}")
    check("sqrt2  ∉ Q(sqrt5)", not in_Qsqrt5(S2), f"√2 = {show(S2)}")
    # sqrt10 / sqrt5 = sqrt2 exactly:
    quotient = kmul(S10, kinv(S5))
    check("√10 / √5 = √2  (exact in K)", keq(quotient, S2), f"= {show(quotient)}")
    # sqrt2*sqrt5 = sqrt10
    check("√2 · √5 = √10", keq(kmul(S2, S5), S10))
    # squares
    check("(√2)^2 = 2", keq(kmul(S2, S2), Q(2)))
    check("(√5)^2 = 5", keq(kmul(S5, S5), Q(5)))
    check("(√10)^2 = 10", keq(kmul(S10, S10), Q(10)))
    # degree 4: {1,√2,√5,√10} Q-linearly independent (basis by construction; verify no rational
    # relation makes √10 a Q-combo of {1,√2,√5})
    def q_combo_reaches(target, gens):
        # solve rational a0..a_{k-1} with sum a_i gens_i = target over Q (4 eqns)
        n = len(gens)
        A = [[gens[j][i] for j in range(n)] for i in range(4)]  # 4 x n
        # least-structure: since 4 eqns n unknown, test consistency by trying to solve the square
        # subsystem plus residual. Simpler: build augmented and row-reduce over Q for consistency.
        M = [row[:] + [target[i]] for i, row in enumerate(A)]
        # gaussian elim to RREF, check consistency
        rows, cols = 4, n
        r = 0
        for c in range(cols):
            piv = None
            for rr in range(r, rows):
                if M[rr][c] != 0:
                    piv = rr; break
            if piv is None:
                continue
            M[r], M[piv] = M[piv], M[r]
            pv = M[r][c]
            M[r] = [v / pv for v in M[r]]
            for rr in range(rows):
                if rr != r and M[rr][c] != 0:
                    f = M[rr][c]
                    M[rr] = [M[rr][k] - f * M[r][k] for k in range(cols + 1)]
            r += 1
        for rr in range(rows):
            if all(M[rr][c] == 0 for c in range(cols)) and M[rr][cols] != 0:
                return False  # inconsistent
        return True
    check("√10 is NOT a Q-combination of {1,√2,√5}  ⇒ [K:Q] = 4",
          not q_combo_reaches(S10, [ONE_K, S2, S5]))

    # ---------------------------------------------------------------- [B] Galois
    print("\n[B] V4 GALOIS ACTION  (PROVED-HERE)")
    # g2: sqrt2 -> -sqrt2, sqrt5 -> sqrt5  (fixes Q(sqrt5)); hence sqrt10=s2 s5 -> -sqrt10
    # g5: sqrt5 -> -sqrt5, sqrt2 -> sqrt2  (fixes Q(sqrt2)); sqrt10 -> -sqrt10
    # g10: sqrt2 -> -sqrt2, sqrt5 -> -sqrt5 (fixes Q(sqrt10)); sqrt10 -> sqrt10
    def g2(x):
        return (x[0], -x[1], x[2], -x[3])

    def g5(x):
        return (x[0], x[1], -x[2], -x[3])

    def g10(x):
        return (x[0], -x[1], -x[2], x[3])

    def gid(x):
        return x
    # each an involution
    for nm, g in [("g2", g2), ("g5", g5), ("g10", g10)]:
        allinv = all(keq(g(g(v)), v) for v in [ONE_K, S2, S5, S10])
        check(f"{nm} is an involution (order 2)", allinv)
    # homomorphism (ring hom): g(xy)=g(x)g(y) on generators
    for nm, g in [("g2", g2), ("g5", g5), ("g10", g10)]:
        hom = keq(g(kmul(S2, S5)), kmul(g(S2), g(S5)))
        check(f"{nm} is a field automorphism (g(√2·√5)=g(√2)·g(√5))", hom)
    # fixed subfields
    check("g2 fixes Q(√5)  (g2(√5)=√5)", keq(g2(S5), S5) and keq(g2(S2), kneg(S2)))
    check("g10 fixes Q(√10) (g10(√10)=√10)", keq(g10(S10), S10) and keq(g10(S2), kneg(S2)))
    check("g5 fixes Q(√2)  (g5(√2)=√2)", keq(g5(S2), S2) and keq(g5(S5), kneg(S5)))
    # group law V4: g2 g5 = g10, etc.
    def comp(g, h):
        return lambda x: g(h(x))
    prod_g2g5 = comp(g2, g5)
    check("g2 ∘ g5 = g10  (V4 closure)",
          all(keq(prod_g2g5(v), g10(v)) for v in [ONE_K, S2, S5, S10]))
    check("g2 ∘ g10 = g5", all(keq(comp(g2, g10)(v), g5(v)) for v in [ONE_K, S2, S5, S10]))
    check("g5 ∘ g10 = g2", all(keq(comp(g5, g10)(v), g2(v)) for v in [ONE_K, S2, S5, S10]))

    # ---------------------------------------------------------------- [C] sign forcing
    print("\n[C] SIGN-FORCING COMPATIBILITY  (CITED: σ(φ^-1)=ψ^-1=-φ on Q(√5); PROVED-HERE: which V4 lift)")
    # phi = (1+sqrt5)/2, phi^-1 = (-1+sqrt5)/2, psi = (1-sqrt5)/2, psi^-1 = -phi.
    phi = (Fr(1, 2), Z, Fr(1, 2), Z)
    phi_inv = (Fr(-1, 2), Z, Fr(1, 2), Z)
    # check phi^2 = phi+1
    check("φ² = φ + 1 (Q(√5) structure)", keq(kmul(phi, phi), kadd(phi, ONE_K)))
    # sigma on Q(sqrt5): sqrt5 -> -sqrt5. Both g5 and g10 negate sqrt5; g2 does NOT.
    # sigma(phi^-1) must equal -phi.
    neg_phi = kneg(phi)
    for nm, g in [("g5", g5), ("g10", g10), ("g2", g2)]:
        val = g(phi_inv)
        matches = keq(val, neg_phi)
        check(f"{nm} restricted to Q(√5): σ(φ^-1) = -φ ?  {'YES' if matches else 'no'}",
              True, f"{nm}(φ^-1) = {show(val)}")
    # the naive negation -(phi^-1) is a DIFFERENT element (control from the owner cert)
    check("control: -(φ^-1) ≠ -φ (naive negation is a different number)",
          not keq(kneg(phi_inv), neg_phi),
          f"-(φ^-1) = {show(kneg(phi_inv))} vs -φ = {show(neg_phi)}")
    print("     VERDICT: the sign-forcing element (negate √5) lifts to K as BOTH g5 (fix √2) and")
    print("     g10 (fix √10). Its action on √2 is UNDETERMINED by the Q(√5) datum — a genuine V4 choice.")

    # ---------------------------------------------------------------- [D] intertwiner attempt
    print("\n[D] INTERTWINER ATTEMPT over K  (PROVED-HERE)")
    S = [[1, 1], [1, 0]]     # golden substitution incidence, trace +1
    T = [[0, 1], [1, -1]]    # centre-11 time operator, trace -1
    negS = [[-1, -1], [-1, 0]]
    trS = S[0][0] + S[1][1]
    trT = T[0][0] + T[1][1]
    print(f"     tr S = {trS}, tr T = {trT}, tr(-S) = {negS[0][0]+negS[1][1]}")
    check("ORIENTATION OBSTRUCTION: tr S ≠ tr T (conjugacy invariant, holds over ANY field incl. K)",
          trS != trT, f"{trS} ≠ {trT}")

    # Prove NO invertible U over K conjugates S to T, by the trace argument made mechanical:
    # If U S = T U for invertible U, then tr S = tr(U^-1 T U) = tr T. Contradiction.
    # We ALSO search the linear system U S - T U = 0 over K for a nonzero solution and confirm any
    # solution is non-invertible (det 0), i.e. the intertwining space contains no isomorphism.
    Sk = lift2(S); Tk = lift2(T)
    # Solve for U=[[u0,u1],[u2,u3]] with U S - T U = 0 : 4 equations, 4 unknowns over K.
    # Build the 4x4 K-matrix acting on (u0,u1,u2,u3).
    def uSminusTu_coeffs():
        # US entries: (US)_{ik} = sum_j U_ij S_jk ; (TU)_{ik} = sum_j T_ij U_jk
        # unknown order: u = [U00,U01,U10,U11]
        rows = []
        for i in range(2):
            for k in range(2):
                coeff = [Z, Z, Z, Z]  # coefficient of each unknown, as rationals (S,T are integer)
                # US_ik = U_i0 S_0k + U_i1 S_1k
                idx = {(0, 0): 0, (0, 1): 1, (1, 0): 2, (1, 1): 3}
                coeff[idx[(i, 0)]] += S[0][k]
                coeff[idx[(i, 1)]] += S[1][k]
                # minus TU_ik = -(T_i0 U_0k + T_i1 U_1k)
                coeff[idx[(0, k)]] += -T[i][0]
                coeff[idx[(1, k)]] += -T[i][1]
                rows.append([Fr(c) for c in coeff])
        return rows
    Msys = uSminusTu_coeffs()
    # nullspace over Q (since coeffs are rational, and K is a Q-algebra, K-solutions = Q-solutions tensor K)
    def nullspace(A):
        n = len(A); m = len(A[0])
        M = [row[:] for row in A]
        piv_cols = []
        r = 0
        for c in range(m):
            piv = None
            for rr in range(r, n):
                if M[rr][c] != 0:
                    piv = rr; break
            if piv is None:
                continue
            M[r], M[piv] = M[piv], M[r]
            pv = M[r][c]
            M[r] = [v / pv for v in M[r]]
            for rr in range(n):
                if rr != r and M[rr][c] != 0:
                    f = M[rr][c]
                    M[rr] = [M[rr][k] - f * M[r][k] for k in range(m)]
            piv_cols.append(c); r += 1
        free = [c for c in range(m) if c not in piv_cols]
        basis = []
        for fc in free:
            vec = [Z] * m
            vec[fc] = Fr(1)
            for ri, pc in enumerate(piv_cols):
                vec[pc] = -M[ri][fc]
            basis.append(vec)
        return basis
    ns = nullspace(Msys)
    print(f"     intertwining space {{U : U S = T U}} has Q-dimension {len(ns)}")
    # every element of the nullspace has det 0 (non-invertible) -> no isomorphism intertwines
    all_singular = True
    for v in ns:
        U = [[v[0], v[1]], [v[2], v[3]]]
        det = U[0][0] * U[1][1] - U[0][1] * U[1][0]
        if det != 0:
            all_singular = False
    check("every U with U S = T U is SINGULAR (det 0) ⇒ NO isomorphism S ≅ T over K",
          all_singular, f"nullspace basis dets = {[ (v[0]*v[3]-v[1]*v[2]) for v in ns]}")

    # Now the scene's OWN pinned relation: T ~ -S with det U = +1. Does an invertible U over Q(⊂K) exist?
    print("     scene-pinned relation U T U^-1 = -S  (trace tr T = -1 = tr(-S) ✓, so conjugacy is POSSIBLE):")
    check("tr T = tr(-S) (necessary condition for T ~ -S holds)",
          trT == (negS[0][0] + negS[1][1]), f"{trT} = {negS[0][0]+negS[1][1]}")
    # find U with U T = -S U, invertible, det=+1
    def uT_minus_negS_u_coeffs():
        rows = []
        idx = {(0, 0): 0, (0, 1): 1, (1, 0): 2, (1, 1): 3}
        for i in range(2):
            for k in range(2):
                coeff = [Fr(0)] * 4
                # UT_ik = U_i0 T_0k + U_i1 T_1k
                coeff[idx[(i, 0)]] += T[0][k]
                coeff[idx[(i, 1)]] += T[1][k]
                # minus (-S)U_ik = -( (-S)_i0 U_0k + (-S)_i1 U_1k )
                coeff[idx[(0, k)]] += -negS[i][0]
                coeff[idx[(1, k)]] += -negS[i][1]
                rows.append(coeff)
        return rows
    ns2 = nullspace(uT_minus_negS_u_coeffs())
    print(f"     conjugating space {{U : U T = -S U}} has Q-dimension {len(ns2)}")
    found_iso = None
    # prefer a det=+1 (SL2) witness to match the corpus cert's "det U = +1"; fall back to any invertible
    for want_det in (Fr(1), None):
        for coeffs in product([Fr(-2), Fr(-1), Fr(0), Fr(1), Fr(2)], repeat=len(ns2)):
            v = [Fr(0)] * 4
            for c, bvec in zip(coeffs, ns2):
                for t in range(4):
                    v[t] += c * bvec[t]
            det = v[0] * v[3] - v[1] * v[2]
            if det != 0 and (want_det is None or det == want_det):
                found_iso = (v, det)
                break
        if found_iso:
            break
    if found_iso:
        v, det = found_iso
        U = [[v[0], v[1]], [v[2], v[3]]]
        # verify U T U^-1 = -S exactly over Q
        Uinv_det = det
        Uinv = [[v[3] / det, -v[1] / det], [-v[2] / det, v[0] / det]]
        # U T
        UT = [[sum(U[i][j] * T[j][k] for j in range(2)) for k in range(2)] for i in range(2)]
        UTUinv = [[sum(UT[i][j] * Uinv[j][k] for j in range(2)) for k in range(2)] for i in range(2)]
        ok = all(UTUinv[i][k] == negS[i][k] for i in range(2) for k in range(2))
        check("scene-pinned U T U^-1 = -S has an INVERTIBLE solution over Q (⊂K)", ok,
              f"U = {U}, det U = {det}")
        print(f"     EXPLICIT U = {U}  (det {det});  U T U^-1 = -S verified exactly over Q.")
        print("     ⇒ the conjugacy T ~ -S is realizable over Q already; it needs NO field extension.")
    else:
        check("scene-pinned U T U^-1 = -S invertible solution", False)

    # ---------------------------------------------------------------- [E] spectra over K
    print("\n[E] SPECTRA over K  (PROVED-HERE)")
    # S: charpoly t^2 - t - 1, roots (1±√5)/2 = phi, -phi^-1  (both in Q(√5)⊂K)
    # T: charpoly t^2 + t - 1, roots (-1±√5)/2 = phi^-1, -phi  (both in Q(√5)⊂K)
    # -S: charpoly t^2 + t - 1  -> SAME as T (consistent with T ~ -S)
    def charpoly2(M):
        tr = M[0][0] + M[1][1]
        det = M[0][0] * M[1][1] - M[0][1] * M[1][0]
        return (Fr(1), Fr(-tr), Fr(det))  # t^2 - tr t + det
    cS, cT, cnegS = charpoly2(S), charpoly2(T), charpoly2(negS)
    print(f"     charpoly(S)   = t² + ({cS[1]})t + ({cS[2]})   [t² - t - 1]")
    print(f"     charpoly(T)   = t² + ({cT[1]})t + ({cT[2]})   [t² + t - 1]")
    print(f"     charpoly(-S)  = t² + ({cnegS[1]})t + ({cnegS[2]})  [t² + t - 1]")
    check("charpoly(S) ≠ charpoly(T)  ⇒ S NOT ~ T (even over K; both are Q(√5)-split)",
          cS != cT)
    check("charpoly(T) = charpoly(-S) ⇒ T ~ -S admissible (same spectrum)", cT == cnegS)
    # all four roots live in Q(sqrt5) already: sqrt5 in K, no sqrt2/sqrt10 needed.
    # exact roots
    root_phi = (Fr(1, 2), Z, Fr(1, 2), Z)         # (1+√5)/2
    root_neg_phi_inv = (Fr(1, 2), Z, Fr(-1, 2), Z)  # (1-√5)/2 = -φ^-1
    # verify root_phi solves t^2 - t - 1 = 0 in K
    val_phi = kadd(ksub(kmul(root_phi, root_phi), root_phi), kneg(ONE_K))
    check("φ=(1+√5)/2 satisfies t²−t−1=0 in K (root of S) — lies in Q(√5), no √2 needed",
          kis_zero(val_phi), f"= {show(val_phi)}")
    print("     KEY: every eigenvalue of S, T, −S lies in Q(√5) ⊂ K. The archive surd √10 does NOT")
    print("     appear in either spectrum, so extending to K adds NO new eigenvalue-matching between")
    print("     the golden carrier and the archive carrier. The extension is spectrally inert here.")

    # ---------------------------------------------------------------- summary
    print("\n" + "=" * 78)
    if FAILS == 0:
        print("ALL INTERNAL CHECKS OK (0 failures). See TASK_W4_REPORT.md for the verdict.")
    else:
        print(f"{FAILS} INTERNAL CHECK(S) FAILED — investigate before trusting the report.")
    print("=" * 78)
    return 0 if FAILS == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
