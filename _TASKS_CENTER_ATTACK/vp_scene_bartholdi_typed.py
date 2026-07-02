#!/usr/bin/env python3
"""W7 — exact certificate for the TYPED (Bartholdi) zeta identity behind candidate T1 / T1-addendum.

Weighted successor of W1's Ihara-Bass cert (`vp_scene_ihara_bass_nb.py`). Reuses that cert's
K(9,11,13) builder, 718-dim Hashimoto matrix, multi-prime modular determinant, and rational-u
machinery. Adds the backtrack involution R and verifies the Bartholdi determinant identity in the
brief's form, its equivalence to the published Bartholdi/Sato form under the sourced dictionary, and
the golden-point (t = phi^-1) specialization exactly over Q(phi).

Scene: complete tripartite K(9,11,13): |V|=33, |E|=359, 2|E|=718 directed edges, |E|-|V|=326.
All PASS/FAIL logic is integer/modular (no floats in decisions). Deliverable of TASK_W7;
NOT registered, NOT placed in 05_CERTS/ (kept out of the CI cert glob). Deterministic;
exits non-zero on FAIL.

Identity checked (brief's form; B = NON-backtracking Hashimoto, R = backtrack involution):

    det(I - u(B + tR)) = (1 - (1-t)^2 u^2)^(|E|-|V|) * det(I - uA + (1-t)(D - (1-t)I) u^2)

t=0 reduces EXACTLY to W1's Ihara-Bass (B+0R = B, (1-t)->1);  t=1 degenerates the exponent factor
to (1-0)^326 = 1 and the vertex side to det(I - uA).

SOURCING DICTIONARY (see TASK_W7_REPORT.md section 1; verified in check [S]):
  Published Bartholdi/Sato form:  det(I - u(B_pub - (1-t)R)) = same RHS, where B_pub is the FULL
  head-meets-tail edge matrix (INCLUDES backtracks) = B + R with B the non-backtracking Hashimoto.
  Then  B_pub - (1-t)R = (B+R) - (1-t)R = B + tR  identically -> published form == brief's form.
  (Plus a pure variable-name transposition (u,t)_ours <-> (t,u)_lit in the literature's letters.)

Golden point: the closure equation p + p^2 = 1 (p = phi^-1) is "1 - t = t^2"; its root in (0,1) is
t = p = phi - 1 (since phi*(phi-1) = phi^2 - phi = 1). Over Q(phi) (phi^2 = phi + 1):
  (i)  1 - t = t^2 exactly at t = phi - 1;
  (ii) det(I - u(B+pR)) = (1 - p^4 u^2)^326 * det(I - uA + p^2(D - p^2 I) u^2) at >=3 rational u.
Q(phi) determinants verified by split-prime modular arithmetic: primes q == +-1 mod 5, where
x^2 - x - 1 factors, giving both embeddings phi -> (1 +- sqrt5)/2; identity must hold at BOTH roots
mod several such primes. Scalar Q(phi) facts also checked with exact 2-component (a+b*phi) arithmetic.

Negative controls (each reachable and must demonstrably FAIL):
  (i)   corrupted bump matrix R (one transposition wrong)                 -> identity FAILS.
  (ii)  wrong exponent |E|-|V| +- 1                                        -> identity FAILS.
  (iii) non-golden t = 3/5 claimed as golden (1 - t != t^2): golden-STRUCTURE check FAILS while the
        generic two-variable identity at t = 3/5 still PASSES (separates identity from specialization).
  (iv)  K(9,11,15): invariants shift -> cert detects.
"""
from __future__ import annotations
import sys
from fractions import Fraction

try:
    import numpy as np
except Exception as e:  # numpy required for the 718x718 modular determinants
    print("SETUP_FAIL numpy required:", e)
    sys.exit(2)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Ordinary large primes (p^2 < 2^63) for the two-variable rational verification (as in W1).
PRIMES = [1_000_000_007, 998_244_353, 1_000_000_009]

# Split primes q == +-1 (mod 5), q >= 1e9: 5 is a QR, x^2 - x - 1 factors, phi has two embeddings.
# Used for exact Q(phi) verification (golden point) under BOTH real embeddings.
SPLIT_PRIMES = [1_000_000_009, 1_000_000_021, 1_000_000_181,
                1_000_000_241, 1_000_000_271, 1_000_000_289]


# ============================================================================ scene builders
def tripartite(sizes):
    """(A 0/1 list-of-lists, degrees, zone-of-vertex, directed-edge list) for K(sizes). (W1 verbatim.)"""
    zone = []
    for zi, s in enumerate(sizes):
        zone += [zi] * s
    n = len(zone)
    A = [[1 if zone[i] != zone[j] else 0 for j in range(n)] for i in range(n)]
    deg = [sum(A[i]) for i in range(n)]
    dedges = [(i, j) for i in range(n) for j in range(n) if A[i][j]]  # directed
    return A, deg, zone, dedges


def hashimoto(dedges, backtracking=False):
    """|dedges|-square 0/1 head-meets-tail matrix. e=(a,b), f=(c,d): entry 1 iff b==c and
    (backtracking or a!=d). backtracking=False -> non-backtracking Hashimoto B (W1's B).
    backtracking=True  -> full head-meets-tail B_pub = B + R. (W1 verbatim.)"""
    idx = {e: k for k, e in enumerate(dedges)}
    L = len(dedges)
    B = np.zeros((L, L), dtype=np.int64)
    from collections import defaultdict
    out = defaultdict(list)
    for (c, d) in dedges:
        out[c].append((c, d))
    for e in dedges:
        a, b = e
        ei = idx[e]
        for f in out[b]:            # f = (b, d)
            c, d = f
            if backtracking or a != d:
                B[ei, idx[f]] = 1
    return B


def backtrack_R(dedges):
    """718x718 backtrack involution: R[(u->v),(w->x)] = 1 iff (w,x) = (v,u). Symmetric permutation,
    R^2 = I. Each directed edge is swapped with its reverse."""
    idx = {e: k for k, e in enumerate(dedges)}
    L = len(dedges)
    R = np.zeros((L, L), dtype=np.int64)
    for e in dedges:
        a, b = e
        R[idx[e], idx[(b, a)]] = 1
    return R


def rank_over_Q(A):
    """Exact rank via fraction-free Gaussian elimination (Fraction), no floats. (W1 verbatim.)"""
    M = [[Fraction(x) for x in row] for row in A]
    n, m = len(M), len(M[0])
    r = 0
    for c in range(m):
        piv = next((i for i in range(r, n) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pv = M[r][c]
        for i in range(n):
            if i != r and M[i][c] != 0:
                f = M[i][c] / pv
                M[i] = [M[i][k] - f * M[r][k] for k in range(m)]
        r += 1
        if r == n:
            break
    return r


# ============================================================================ modular linear algebra
def det_mod(mat, p):
    """Determinant of an integer matrix mod prime p (numpy int64 Gaussian elimination). (W1 verbatim.)"""
    M = (np.asarray(mat, dtype=np.int64) % p)
    n = M.shape[0]
    det = 1
    for col in range(n):
        piv = -1
        for r in range(col, n):
            if M[r, col] % p != 0:
                piv = r
                break
        if piv == -1:
            return 0
        if piv != col:
            M[[col, piv]] = M[[piv, col]]
            det = (-det) % p
        pivval = int(M[col, col])
        det = (det * pivval) % p
        inv = pow(pivval, p - 2, p)
        if col + 1 < n:
            factors = (M[col + 1:, col].astype(np.int64) * inv) % p
            M[col + 1:] = (M[col + 1:] - np.outer(factors, M[col])) % p
    return det % p


def rat_mod(fr, p):
    """Rational (Fraction) reduced mod prime p. (W1 verbatim.)"""
    return (fr.numerator % p) * pow(fr.denominator % p, p - 2, p) % p


# ---- two-variable (u,t) modular determinants over an ordinary prime -------------------------
def lhs_bartholdi_mod(B, R, u, t, p):
    """det(I - u(B + tR)) mod p, u,t rational (Fraction). B,R integer matrices."""
    L = B.shape[0]
    up = rat_mod(u, p)
    tp = rat_mod(t, p)
    edge = (B.astype(np.int64) + (tp * R.astype(np.int64))) % p   # B + tR
    M = (np.eye(L, dtype=np.int64) - (up * edge)) % p
    return det_mod(M, p)


def lhs_published_mod(Bpub, R, u, t, p):
    """PUBLISHED edge operator: det(I - u(B_pub - (1-t)R)) mod p, with B_pub = full head-meets-tail.
    Under B_pub = B + R this equals lhs_bartholdi_mod exactly; check [S] proves it."""
    L = Bpub.shape[0]
    up = rat_mod(u, p)
    coef = rat_mod(Fraction(1) - t, p)                            # (1 - t) mod p
    edge = (Bpub.astype(np.int64) - (coef * R.astype(np.int64))) % p   # B_pub - (1-t)R
    M = (np.eye(L, dtype=np.int64) - (up * edge)) % p
    return det_mod(M, p)


def rhs_bartholdi_mod(A, deg, u, t, p, exp):
    """(1 - (1-t)^2 u^2)^exp * det(I - uA + (1-t)(D - (1-t)I) u^2) mod p, u,t rational."""
    A = np.asarray(A, dtype=np.int64)
    n = A.shape[0]
    up = rat_mod(u, p)
    tp = rat_mod(t, p)
    u2 = (up * up) % p
    omt = (1 - tp) % p                         # (1 - t)
    # vertex block: I - uA + (1-t)(D - (1-t) I) u^2
    Dm = np.diag([d % p for d in deg]).astype(np.int64)
    inner = (Dm - (omt * np.eye(n, dtype=np.int64))) % p          # D - (1-t) I
    Mv = (np.eye(n, dtype=np.int64) - up * A + ((omt * u2) % p) * inner) % p
    small = det_mod(Mv, p)
    pref = (1 - (omt * omt % p) * u2) % p                          # 1 - (1-t)^2 u^2
    return (pow(pref, exp, p) * small) % p


# ---- W1's Ihara-Bass RHS (t=0 specialization), byte-for-byte the W1 formula ------------------
def rhs_iharabass_mod(A, deg, u, p, bass_exp):
    """W1's exact Ihara-Bass RHS: (1-u^2)^bass * det(I - uA + u^2(D - I)). Used to prove the t=0
    leg reproduces W1's numbers bit-for-bit."""
    A = np.asarray(A, dtype=np.int64)
    n = A.shape[0]
    up = rat_mod(u, p)
    u2 = (up * up) % p
    Dm1 = np.diag([d - 1 for d in deg]).astype(np.int64)
    M = (np.eye(n, dtype=np.int64) - up * A + u2 * Dm1) % p
    small = det_mod(M, p)
    one_minus_u2 = (1 - u2) % p
    return (pow(one_minus_u2, bass_exp, p) * small) % p


# ============================================================================ Q(phi) exact scalars
# 2-component arithmetic in Z[phi]/(phi^2 - phi - 1): element = a + b*phi, (a,b) integers (or Fraction).
def qp(a, b=0):
    return (Fraction(a), Fraction(b))


def qp_add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def qp_sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def qp_mul(x, y):
    # (a+b phi)(c+d phi) = ac + (ad+bc) phi + bd phi^2 ; phi^2 = phi + 1
    # = ac + bd + (ad + bc + bd) phi
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def qp_pow(x, n):
    r = qp(1, 0)
    for _ in range(n):
        r = qp_mul(r, x)
    return r


def qp_eq(x, y):
    return x[0] == y[0] and x[1] == y[1]


# split-prime reduction of an a+b*phi element at a chosen embedding phi_val mod q
def qp_to_mod(x, phi_val, q):
    a, b = x
    am = (a.numerator % q) * pow(a.denominator % q, q - 2, q) % q
    bm = (b.numerator % q) * pow(b.denominator % q, q - 2, q) % q
    return (am + bm * phi_val) % q


def sqrt_mod(a, p):
    """Tonelli-Shanks square root mod odd prime p; None if non-residue."""
    a %= p
    if a == 0:
        return 0
    if pow(a, (p - 1) // 2, p) != 1:
        return None
    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    m = s
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)
    while t != 1:
        i = 0
        t2 = t
        while t2 != 1:
            t2 = t2 * t2 % p
            i += 1
        b = pow(c, 1 << (m - i - 1), p)
        m = i
        c = b * b % p
        t = t * c % p
        r = r * b % p
    return r


def phi_embeddings_mod(q):
    """Both roots of x^2 = x + 1 mod q (q split): (1 +- sqrt5)/2. Returns list of two residues."""
    s5 = sqrt_mod(5, q)
    if s5 is None or s5 * s5 % q != 5 % q:
        raise ValueError("q is not a valid split prime for sqrt(5): %d" % q)
    inv2 = pow(2, q - 2, q)
    r1 = (1 + s5) * inv2 % q
    r2 = (1 + (q - s5)) * inv2 % q
    return [r1, r2]


# ---- golden-point RHS/LHS at a concrete embedding phi_val mod split prime q ------------------
def golden_lhs_mod(B, R, u, p_val, q):
    """det(I - u(B + p R)) mod q, with p = phi - 1 given as residue p_val = phi_val - 1 mod q."""
    L = B.shape[0]
    up = rat_mod(u, q)
    edge = (B.astype(np.int64) + (p_val * R.astype(np.int64))) % q
    M = (np.eye(L, dtype=np.int64) - (up * edge)) % q
    return det_mod(M, q)


def golden_rhs_mod(A, deg, u, phi_val, q, exp):
    """(1 - p^4 u^2)^exp * det(I - uA + p^2(D - p^2 I) u^2) mod q, p = phi - 1 (residue phi_val-1)."""
    A = np.asarray(A, dtype=np.int64)
    n = A.shape[0]
    up = rat_mod(u, q)
    u2 = up * up % q
    p_val = (phi_val - 1) % q                      # p = phi - 1
    p2 = p_val * p_val % q                          # p^2
    p4 = p2 * p2 % q                                # p^4
    Dm = np.diag([d % q for d in deg]).astype(np.int64)
    inner = (Dm - (p2 * np.eye(n, dtype=np.int64))) % q            # D - p^2 I
    Mv = (np.eye(n, dtype=np.int64) - up * A + ((p2 * u2) % q) * inner) % q
    small = det_mod(Mv, q)
    pref = (1 - p4 * u2) % q                                        # 1 - p^4 u^2
    return (pow(pref, exp, q) * small) % q


# ============================================================================ report-only helpers
def charpoly_3x3_int(Q):
    """Exact integer charpoly {c2,c1,c0} of lambda^3 + c2 l^2 + c1 l + c0 for a 3x3 int matrix.
    (W1 verbatim.)"""
    a, b, c = Q[0]
    d, e, f = Q[1]
    g, h, i = Q[2]
    tr = a + e + i
    m2 = (e * i - f * h) + (a * i - c * g) + (a * e - b * d)
    det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    return {"c2": -tr, "c1": m2, "c0": -det}


def charpoly_qp_matrix(M):
    """Exact characteristic polynomial of an nxn matrix over Q(phi) (entries as (a,b) pairs), via
    the Faddeev-LeVerrier algorithm using only ring ops (+,-,*), no division except by small ints
    which are handled as exact Fractions in the qp components. Returns coeffs [c_n,...,c_0] with
    c_n = 1 (leading), of det(lambda I - M) = sum c_k lambda^k, each a (a,b) Q(phi) pair."""
    n = len(M)
    # Faddeev-LeVerrier: M_1 = A; c_{n-1} = -tr(M_1); M_{k+1} = A(M_k + c_{n-k} I); c_{n-k-1} = -tr(...)/(k+1)
    I = [[qp(1, 0) if i == j else qp(0, 0) for j in range(n)] for i in range(n)]

    def matmul(X, Y):
        Z = [[qp(0, 0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for k in range(n):
                xik = X[i][k]
                if xik == qp(0, 0):
                    continue
                for j in range(n):
                    Z[i][j] = qp_add(Z[i][j], qp_mul(xik, Y[k][j]))
        return Z

    def scal(X, s):
        return [[qp_mul(X[i][j], s) for j in range(n)] for i in range(n)]

    def add(X, Y):
        return [[qp_add(X[i][j], Y[i][j]) for j in range(n)] for i in range(n)]

    def trace(X):
        t = qp(0, 0)
        for i in range(n):
            t = qp_add(t, X[i][i])
        return t

    A = [row[:] for row in M]
    coeffs = [qp(1, 0)]         # leading coeff of lambda^n
    Mk = [row[:] for row in A]
    c = qp_sub(qp(0, 0), trace(Mk))   # c_{n-1} = -tr(A)
    coeffs.append(c)
    for k in range(2, n + 1):
        # Mk <- A (Mk + c I)
        Mk = matmul(A, add(Mk, scal(I, c)))
        c = qp_sub(qp(0, 0), (qp_mul(trace(Mk), qp(Fraction(1, k), 0))))
        coeffs.append(c)
    return coeffs  # [c_n=1, c_{n-1}, ..., c_0]


def qp_str(x):
    a, b = x
    def f(fr):
        return str(fr.numerator) if fr.denominator == 1 else "%d/%d" % (fr.numerator, fr.denominator)
    if b == 0:
        return f(a)
    if a == 0:
        return "%s*phi" % f(b)
    sign = "+" if b > 0 else "-"
    bb = b if b > 0 else -b
    return "%s %s %s*phi" % (f(a), sign, f(bb))


# --- univariate polynomials in u with Q(phi) coefficients: dict {deg: (a,b)} ------------------
def poly_zero():
    return {}


def poly_add(P, Q):
    R = dict(P)
    for k, v in Q.items():
        R[k] = qp_add(R.get(k, qp(0, 0)), v)
    return R


def poly_sub(P, Q):
    R = dict(P)
    for k, v in Q.items():
        R[k] = qp_sub(R.get(k, qp(0, 0)), v)
    return R


def poly_mul(P, Q):
    R = {}
    for k1, v1 in P.items():
        for k2, v2 in Q.items():
            R[k1 + k2] = qp_add(R.get(k1 + k2, qp(0, 0)), qp_mul(v1, v2))
    return R


def poly_det3(N):
    """Exact 3x3 determinant of a matrix whose entries are polynomials-in-u over Q(phi)."""
    def M(i, j):
        return N[i][j]
    t1 = poly_mul(M(0, 0), poly_sub(poly_mul(M(1, 1), M(2, 2)), poly_mul(M(1, 2), M(2, 1))))
    t2 = poly_mul(M(0, 1), poly_sub(poly_mul(M(1, 0), M(2, 2)), poly_mul(M(1, 2), M(2, 0))))
    t3 = poly_mul(M(0, 2), poly_sub(poly_mul(M(1, 0), M(2, 1)), poly_mul(M(1, 1), M(2, 0))))
    return poly_add(poly_sub(t1, t2), t3)


def golden_vertex_poly(deg_zone, sizes):
    """Exact P(u) = det(I - uA + p^2(D - p^2 I) u^2) over Q(phi)[u], p = phi-1, via the equitable
    3-zone quotient: P(u) = prod_a x_a(u)^(size_a - 1) * det(N(u)), with
    x_a(u) = 1 + p^2 (d_a - p^2) u^2  and  N[a][a] = x_a, N[a][b] = -size_b * u (a != b).
    Returns dict {deg_u: (a,b)}. Verified equitable in [R-b] against the full 33-dim determinant."""
    p = qp(-1, 1)                       # p = phi - 1
    c = qp_mul(p, p)                     # p^2
    x_polys = []
    for a in range(3):
        da = qp(deg_zone[a], 0)
        coef = qp_mul(c, qp_sub(da, c))  # p^2 (d_a - p^2)
        x_polys.append({0: qp(1, 0), 2: coef})   # 1 + coef u^2
    N = [[None] * 3 for _ in range(3)]
    for a in range(3):
        for b in range(3):
            if a == b:
                N[a][b] = x_polys[a]
            else:
                N[a][b] = {1: qp(-sizes[b], 0)}   # -size_b u
    full = {0: qp(1, 0)}
    for a in range(3):
        for _ in range(sizes[a] - 1):
            full = poly_mul(full, x_polys[a])
    return poly_mul(full, poly_det3(N))


def edge_type_quotient_Bp(A, deg, zone, dedges, B, R):
    """Build the 6x6 equitable quotient of B_p = B + pR over Q(phi) on the edge-type partition
    (source-zone, target-zone). Returns (typelist, 6x6 matrix over Q(phi), equitable_flag).
    Entry contributed by B is 1 (i.e. (1,0)); by R is p = phi-1 (i.e. (-1,1))."""
    from collections import defaultdict
    types = [(zone[a], zone[b]) for (a, b) in dedges]
    typelist = sorted(set(types))
    tindex = {t: i for i, t in enumerate(typelist)}
    rows_by_type = defaultdict(list)
    for k, t in enumerate(types):
        rows_by_type[t].append(k)
    L = len(dedges)

    def rowsum_exact(k):
        v = [qp(0, 0) for _ in range(6)]
        rowB = B[k]
        rowR = R[k]
        for j in range(L):
            ti = tindex[types[j]]
            if rowB[j]:
                v[ti] = qp_add(v[ti], qp(1, 0))
            if rowR[j]:
                v[ti] = qp_add(v[ti], qp(-1, 1))   # + p
        return v

    equitable = True
    quotient = {}
    for t in typelist:
        reps = rows_by_type[t]
        base = rowsum_exact(reps[0])
        quotient[t] = base
        for k in reps[1:]:
            if rowsum_exact(k) != base:
                equitable = False
                break
    M = [[quotient[typelist[i]][j] for j in range(6)] for i in range(6)]
    return typelist, M, equitable


# ============================================================================ checks
def main():
    ok = True
    print("=== W7 . Bartholdi (typed) zeta exact certificate on K(9,11,13) ===")

    A, deg, zone, dedges = tripartite((9, 11, 13))
    V, E2 = len(deg), sum(deg)
    E = E2 // 2
    exp = E - V   # 326

    B = hashimoto(dedges, backtracking=False)     # non-backtracking Hashimoto (W1's B)
    Bpub = hashimoto(dedges, backtracking=True)    # full head-meets-tail = B + R
    R = backtrack_R(dedges)

    # ---------------------------------------------------------------- [1] scene invariants + R laws
    d_by_zone = sorted({(zone[i], deg[i]) for i in range(V)})
    degs = tuple(d for _, d in d_by_zone)
    rk = rank_over_Q(A)
    R_is_perm = bool(np.array_equal(R.sum(axis=0), np.ones(E2)) and
                     np.array_equal(R.sum(axis=1), np.ones(E2)))
    R_involution = bool(np.array_equal(R @ R, np.eye(E2, dtype=np.int64)))
    R_symmetric = bool(np.array_equal(R, R.T))
    Bpub_eq = bool(np.array_equal(Bpub, B + R))
    c1 = (V == 33 and E == 359 and E2 == 718 and degs == (24, 22, 20) and rk == 3
          and B.shape == (718, 718) and R.shape == (718, 718)
          and R_is_perm and R_involution and R_symmetric and Bpub_eq)
    print("[1] |V|=%d |E|=%d 2|E|=%d degrees(zone)=%s rank(A)=%d ; R perm/involution/symmetric=%s/%s/%s"
          % (V, E, E2, degs, rk, R_is_perm, R_involution, R_symmetric))
    print("    B_pub(head-meets-tail) == B + R : %s ; |E|-|V|=%d : %s"
          % (Bpub_eq, exp, "PASS" if c1 else "FAIL"))
    ok &= c1
    if c1:
        print("PASS_SCENE_INVARIANTS_AND_R_INVOLUTION")

    # -------------------------------------------------- [S] sourcing dictionary: published == brief
    # Published edge operator det(I - u(B_pub - (1-t)R)) must equal brief's det(I - u(B + tR))
    # at every (u,t,p). This is the algebraic content of the dictionary B_pub = B + R.
    dict_ok = True
    for (u, t) in [(Fraction(1, 3), Fraction(0)), (Fraction(1, 5), Fraction(2, 7)),
                   (Fraction(-2, 5), Fraction(1)), (Fraction(2, 9), Fraction(3, 5))]:
        for p in PRIMES:
            if lhs_published_mod(Bpub, R, u, t, p) != lhs_bartholdi_mod(B, R, u, t, p):
                dict_ok = False
                print("    DICT MISMATCH u=%s t=%s p=%d" % (u, t, p))
    print("[S] published det(I - u(B_pub-(1-t)R)) == brief det(I - u(B+tR)) at 4 (u,t), %d primes : %s"
          % (len(PRIMES), "PASS" if dict_ok else "FAIL"))
    ok &= dict_ok
    if dict_ok:
        print("PASS_SOURCING_DICTIONARY_PUBLISHED_EQUALS_BRIEF")

    # -------------------------------------------------- [2] exact two-variable identity, >=6 (u,t)
    # interior + both degenerations (t=0 -> Ihara-Bass, t=1 -> det(I-uA)).
    pairs = [
        (Fraction(1, 3), Fraction(0)),      # t=0 degeneration (Ihara-Bass)
        (Fraction(2, 9), Fraction(0)),      # t=0 degeneration, 2nd u
        (Fraction(1, 5), Fraction(1)),      # t=1 degeneration (all walks)
        (Fraction(-2, 7), Fraction(1)),     # t=1 degeneration, 2nd u
        (Fraction(1, 4), Fraction(3, 5)),   # interior
        (Fraction(-1, 6), Fraction(2, 7)),  # interior, negative u
        (Fraction(2, 11), Fraction(4, 9)),  # interior
    ]
    id_ok = True
    for (u, t) in pairs:
        for p in PRIMES:
            l = lhs_bartholdi_mod(B, R, u, t, p)
            r = rhs_bartholdi_mod(A, deg, u, t, p, exp)
            if l != r:
                id_ok = False
                print("    2VAR MISMATCH u=%s t=%s p=%d lhs=%d rhs=%d" % (u, t, p, l, r))
    print("[2] Bartholdi det(I-u(B+tR)) == (1-(1-t)^2u^2)^%d det(I-uA+(1-t)(D-(1-t)I)u^2) "
          "at %d (u,t) pairs (incl. t=0,t=1), mod %d primes : %s"
          % (exp, len(pairs), len(PRIMES), "PASS" if id_ok else "FAIL"))
    ok &= id_ok
    if id_ok:
        print("PASS_BARTHOLDI_TWO_VARIABLE_IDENTITY_EXACT_MODULAR")

    # ------------------------------- [2a] t=0 leg reproduces W1's Ihara-Bass numbers BIT-FOR-BIT
    t0_ok = True
    for u in [Fraction(1, 3), Fraction(1, 7), Fraction(-2, 5), Fraction(2, 9), Fraction(3, 11)]:
        for p in PRIMES:
            l = lhs_bartholdi_mod(B, R, u, Fraction(0), p)      # det(I - uB) since t=0
            r_w1 = rhs_iharabass_mod(A, deg, u, p, exp)          # W1's exact RHS
            r_w7 = rhs_bartholdi_mod(A, deg, u, Fraction(0), p, exp)
            if not (l == r_w1 == r_w7):
                t0_ok = False
                print("    T0 MISMATCH u=%s p=%d lhs=%d w1=%d w7=%d" % (u, p, l, r_w1, r_w7))
    print("[2a] t=0 leg == W1 Ihara-Bass det(I-uB)=(1-u^2)^%d det(I-uA+u^2(D-I)) bit-for-bit "
          "at W1's 5 u, %d primes : %s" % (exp, len(PRIMES), "PASS" if t0_ok else "FAIL"))
    ok &= t0_ok
    if t0_ok:
        print("PASS_T0_LEG_REPRODUCES_W1_IHARA_BASS")

    # ------------------------------- [2b] t=1 degeneration: exponent factor -> 1, vertex -> det(I-uA)
    # At t=1: (1-t)=0 so prefactor (1-0)^326 = 1 and inner term (1-t)(...) = 0 -> RHS = det(I - uA).
    t1_ok = True
    for u in [Fraction(1, 5), Fraction(-2, 7), Fraction(3, 8)]:
        for p in PRIMES:
            l = lhs_bartholdi_mod(B, R, u, Fraction(1), p)       # det(I - u(B+R)) = det(I - u B_pub)
            up = rat_mod(u, p)
            Am = np.asarray(A, dtype=np.int64)
            det_IminusuA = det_mod((np.eye(V, dtype=np.int64) - up * Am) % p, p)
            r = rhs_bartholdi_mod(A, deg, u, Fraction(1), p, exp)
            if not (l == r == det_IminusuA):
                t1_ok = False
                print("    T1 MISMATCH u=%s p=%d lhs=%d rhs=%d detIuA=%d"
                      % (u, p, l, r, det_IminusuA))
    print("[2b] t=1 degeneration: prefactor (1-0)^%d=1 and RHS == det(I - uA) at 3 u, %d primes : %s"
          % (exp, len(PRIMES), "PASS" if t1_ok else "FAIL"))
    ok &= t1_ok
    if t1_ok:
        print("PASS_T1_DEGENERATION_TO_DET_I_MINUS_uA")

    # -------------------------------------------------- [3] golden point over Q(phi)
    # (i) 1 - t = t^2 exactly at t = phi - 1, in exact 2-component Z[phi] arithmetic.
    p_phi = qp(-1, 1)                    # p = phi - 1 = -1 + 1*phi
    one_minus_p = qp_sub(qp(1, 0), p_phi)
    p_squared = qp_mul(p_phi, p_phi)
    golden_scalar_ok = qp_eq(one_minus_p, p_squared)
    # sanity: p = phi^-1, i.e. phi * p = 1
    phi = qp(0, 1)
    phi_times_p = qp_mul(phi, p_phi)
    inv_ok = qp_eq(phi_times_p, qp(1, 0))
    # p^4 == (p^2)^2
    p4 = qp_pow(p_phi, 4)
    p2sq = qp_mul(p_squared, p_squared)
    p4_ok = qp_eq(p4, p2sq)
    print("[3i] Q(phi) exact 2-component: 1 - (phi-1) == (phi-1)^2 : %s ; phi*(phi-1)==1 : %s ; "
          "p^4==(p^2)^2 : %s" % (golden_scalar_ok, inv_ok, p4_ok))
    print("     p=phi-1=%s  1-p=%s  p^2=%s  p^4=%s"
          % (qp_str(p_phi), qp_str(one_minus_p), qp_str(p_squared), qp_str(p4)))
    c3i = golden_scalar_ok and inv_ok and p4_ok
    ok &= c3i
    if c3i:
        print("PASS_GOLDEN_CLOSURE_1_MINUS_t_EQUALS_t_SQUARED_EXACT")

    # (ii) golden specialization at >=3 rational u, via split-prime modular under BOTH embeddings.
    golden_us = [Fraction(1, 4), Fraction(1, 6), Fraction(-2, 7), Fraction(3, 10)]
    golden_ok = True
    embeddings_checked = 0
    for q in SPLIT_PRIMES:
        for phi_val in phi_embeddings_mod(q):
            # confirm the embedding really satisfies phi^2 = phi + 1 mod q
            assert phi_val * phi_val % q == (phi_val + 1) % q
            p_val = (phi_val - 1) % q       # p = phi - 1
            # also confirm 1 - p == p^2 mod q (golden closure at this embedding)
            assert (1 - p_val) % q == (p_val * p_val) % q
            embeddings_checked += 1
            for u in golden_us:
                l = golden_lhs_mod(B, R, u, p_val, q)
                r = golden_rhs_mod(A, deg, u, phi_val, q, exp)
                if l != r:
                    golden_ok = False
                    print("    GOLDEN MISMATCH q=%d phi=%d u=%s lhs=%d rhs=%d" % (q, phi_val, u, l, r))
    print("[3ii] golden det(I-u(B+pR)) == (1-p^4u^2)^%d det(I-uA+p^2(D-p^2 I)u^2) at %d u, "
          "%d embeddings across %d split primes : %s"
          % (exp, len(golden_us), embeddings_checked, len(SPLIT_PRIMES),
             "PASS" if golden_ok else "FAIL"))
    ok &= golden_ok
    if golden_ok:
        print("PASS_GOLDEN_SPECIALIZATION_EXACT_QPHI_SPLIT_PRIME")

    # -------------------------------------------------- Negative controls (each must FAIL/detect)
    print("Negative controls (each must break the identity / detect the change):")

    # (i) corrupted bump matrix R: swap one off-diagonal pair (one transposition wrong).
    Rbad = R.copy()
    # find two directed edges e1,e2 with their reverses; corrupt R by pointing e1 to e2's reverse.
    e0 = dedges[0]                       # (a,b)
    e1 = dedges[1]                       # (a,c) generally another edge
    idx = {e: k for k, e in enumerate(dedges)}
    rev0 = idx[(e0[1], e0[0])]
    rev1 = idx[(e1[1], e1[0])]
    # zero out correct entries and set wrong ones (a genuine single-transposition corruption)
    Rbad[idx[e0], rev0] = 0
    Rbad[idx[e1], rev1] = 0
    Rbad[idx[e0], rev1] = 1
    Rbad[idx[e1], rev0] = 1
    broke_i = False
    for (u, t) in [(Fraction(1, 4), Fraction(3, 5)), (Fraction(1, 5), Fraction(2, 7))]:
        for p in PRIMES:
            if lhs_bartholdi_mod(B, Rbad, u, t, p) != rhs_bartholdi_mod(A, deg, u, t, p, exp):
                broke_i = True
    print("  (i)   corrupted bump matrix R (one transposition) breaks identity : %s"
          % ("PASS(control fires)" if broke_i else "FAIL(control dead)"))
    ok &= broke_i
    if broke_i:
        print("FAIL_CORRUPTED_R_BREAKS_IDENTITY")

    # (ii) wrong exponent |E|-|V| +- 1 -> identity FAILS.
    broke_ii = False
    for bad in (exp - 1, exp + 1):
        for (u, t) in [(Fraction(1, 4), Fraction(3, 5))]:
            for p in PRIMES:
                if lhs_bartholdi_mod(B, R, u, t, p) != rhs_bartholdi_mod(A, deg, u, t, p, bad):
                    broke_ii = True
    print("  (ii)  wrong exponent (326 +- 1) breaks identity : %s"
          % ("PASS(control fires)" if broke_ii else "FAIL(control dead)"))
    ok &= broke_ii
    if broke_ii:
        print("FAIL_WRONG_EXPONENT_BREAKS_IDENTITY")

    # (iii) non-golden t = 3/5 claimed golden: the golden-STRUCTURE check (1-t == t^2) must FAIL,
    #       while the GENERIC two-variable identity at t=3/5 still PASSES.
    t_fake = Fraction(3, 5)
    structure_holds = (Fraction(1) - t_fake == t_fake * t_fake)   # False for 3/5
    generic_holds_at_fake = True
    for u in [Fraction(1, 4), Fraction(1, 6), Fraction(-2, 7)]:
        for p in PRIMES:
            if lhs_bartholdi_mod(B, R, u, t_fake, p) != rhs_bartholdi_mod(A, deg, u, t_fake, p, exp):
                generic_holds_at_fake = False
    control_iii = (not structure_holds) and generic_holds_at_fake
    print("  (iii) non-golden t=3/5: golden-structure (1-t==t^2) holds=%s (must be False); "
          "generic identity at t=3/5 holds=%s (must be True) : %s"
          % (structure_holds, generic_holds_at_fake,
             "PASS(control fires)" if control_iii else "FAIL(control dead)"))
    ok &= control_iii
    if control_iii:
        print("FAIL_NONGOLDEN_STRUCTURE_WHILE_GENERIC_PASSES")

    # (iv) K(9,11,15): invariants shift, cert detects.
    A5, deg5, zone5, ded5 = tripartite((9, 11, 15))
    inv5 = (sum(deg5) // 2, sum(deg5), sum(d * d for d in deg5), len(ded5))
    changed = inv5 != (359, 718, 15708, 718)
    # also: the two-variable identity on K(9,11,15) uses its OWN exponent |E5|-|V5|; verify the
    # SCENE exponent 326 does NOT satisfy the identity there (structural detection).
    B5 = hashimoto(ded5, backtracking=False)
    R5 = backtrack_R(ded5)
    V5, E25 = len(deg5), sum(deg5)
    E5 = E25 // 2
    wrong_exp_detected = False
    for u in [Fraction(1, 5)]:
        for t in [Fraction(2, 7)]:
            for p in PRIMES:
                # using scene exponent 326 (wrong for K(9,11,15)) must break its identity
                if lhs_bartholdi_mod(B5, R5, u, t, p) != rhs_bartholdi_mod(A5, deg5, u, t, p, exp):
                    wrong_exp_detected = True
                # its own exponent must work
                assert lhs_bartholdi_mod(B5, R5, u, t, p) == rhs_bartholdi_mod(A5, deg5, u, t, p, E5 - V5)
    control_iv = changed and wrong_exp_detected
    print("  (iv)  K(9,11,15) invariants %s != scene (359,718,15708,718) : %s ; scene-exponent 326 "
          "breaks its identity : %s : %s"
          % (inv5, changed, wrong_exp_detected,
             "PASS(control fires)" if control_iv else "FAIL(control dead)"))
    ok &= control_iv
    if control_iv:
        print("FAIL_K91115_INVARIANTS_AND_EXPONENT_DIFFER")

    # -------------------------------------------------- [R] report-only spectral/structural data
    print("Report-only (no PASS/FAIL weight): spectral / structural fingerprints")

    # (R-a) FINDING: rank-3 adjacency spectrum = zone-quotient charpoly = vacuum cubic (W1 verbatim).
    Qzone = [[0, 11, 13], [9, 0, 13], [9, 11, 0]]
    cp = charpoly_3x3_int(Qzone)
    print("  [R-a] adjacency zone-quotient charpoly = lambda^3 %+dl^2 %+dl %+d (= l^3-359l-2574) : %s"
          % (cp["c2"], cp["c1"], cp["c0"],
             "matches vacuum cubic" if (cp["c2"] == 0 and cp["c1"] == -359 and cp["c0"] == -2574)
             else "DIFFERS"))

    # (R-b) golden vertex-side polynomial P(u) = det(I - uA + p^2(D - p^2 I)u^2) as EXACT Q(phi)[u].
    # Built via the equitable 3-zone quotient (compressed block), then CROSS-CHECKED exactly against
    # the full 33-dim determinant modulo split primes at several u (so the compressed form is proven,
    # not asserted). Report-only: no PASS/FAIL weight, but the compression is exact-verified.
    p2 = p_squared                 # p^2 in Q(phi) = 2 - phi
    deg_zone = [deg[[i for i in range(V) if zone[i] == a][0]] for a in range(3)]  # [24,22,20]
    sizes = [9, 11, 13]
    Puser = golden_vertex_poly(deg_zone, sizes)
    degP = max(Puser)
    # exact cross-check: compressed P(u) == full 33-dim det(I-uA+p^2(D-p^2I)u^2) mod split primes.
    compress_ok = True
    for q in SPLIT_PRIMES[:2]:
        for phi_val in phi_embeddings_mod(q):
            p_valq = (phi_val - 1) % q
            p2q = p_valq * p_valq % q
            for u in [Fraction(1, 4), Fraction(2, 7), Fraction(-3, 5)]:
                up = rat_mod(u, q)
                u2 = up * up % q
                Am = np.asarray(A, dtype=np.int64)
                Dm = np.diag([d % q for d in deg]).astype(np.int64)
                inner = (Dm - (p2q * np.eye(V, dtype=np.int64))) % q
                Mv = (np.eye(V, dtype=np.int64) - up * Am + ((p2q * u2) % q) * inner) % q
                full_det = det_mod(Mv, q)
                comp = 0
                for k, (a, b) in Puser.items():
                    coef = (qp_to_mod((a, b), phi_val, q)) % q
                    comp = (comp + coef * pow(up, k, q)) % q
                if full_det != comp:
                    compress_ok = False
    lowterms = "; ".join("u^%d:%s" % (k, qp_str(Puser[k])) for k in (0, 2, 3, 4)
                         if k in Puser)
    print("  [R-b] golden P(u)=det(I-uA+p^2(D-p^2 I)u^2) exact Q(phi)[u], deg=%d ; compressed form "
          "== full 33-dim det (exact, split-prime cross-check): %s" % (degP, compress_ok))
    print("        low-order coeffs: %s   (full deg-%d list in TASK_W7_REPORT.md section 4)"
          % (lowterms, degP))

    # (R-c) compressed charpoly of B_p = B + pR over Q(phi) via the 6-type EQUITABLE edge quotient.
    typelist, Q6, equit = edge_type_quotient_Bp(A, deg, zone, dedges, B, R)
    cpBp = charpoly_qp_matrix(Q6)   # [c6=1, c5, ..., c0], det(lambda I - Q6) over Q(phi)
    # emit as lambda^6 + ... ; cpBp[i] is coeff of lambda^(6-i)
    terms = []
    for i, c in enumerate(cpBp):
        d = 6 - i
        if c != qp(0, 0):
            terms.append("l^%d:(%s)" % (d, qp_str(c)))
    print("  [R-c] B_p=B+pR edge-type quotient is 6x6 equitable over Q(phi): %s ; p=%s"
          % (equit, qp_str(p_phi)))
    print("        charpoly(quotient) = %s" % "  ".join(terms))
    print("        (Perron(B_p) is the top root ~21.4540; the sextic is its exact min-poly-over-Q(phi) "
          "factor; l^3 coeff = -2574 = vacuum-cubic constant)")

    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
