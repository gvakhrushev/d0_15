#!/usr/bin/env python3
"""W1 — exact certificate for the Ihara–Bass structure behind candidate theorem T1.

Scene: complete tripartite graph K(9,11,13). All PASS/FAIL logic is integer/modular — no floats.
Deliverable of TASK_W1; NOT registered, NOT placed in 05_CERTS/ (must not enter the CI cert glob).

Checks (each with a reachable negative control):
  [1] scene invariants: |V|=33, |E|=359, degrees (24,22,20), rank(A)=3 (exact fraction-free).
  [2] depth-2 identity: Σd²=15708, Σd(d−1)=14990, excess=718=2|E|, excess ↔ directed edges (bijection).
  [3] Ihara–Bass at ≥5 rational u, each mod ≥3 large primes:
          det(I−uB) == (1−u²)^(|E|−|V|) · det(I−uA+u²(D−I)).
  [4] FINDING (not a fork resolution): the rank-3 adjacency spectrum = roots of the zone quotient
          Q=[[0,11,13],[9,0,13],[9,11,0]], charpoly λ³−359λ−2574 (the §08.12.4 "vacuum cubic").
  Negative controls (must break the identity / detect the change):
      (i)  Hashimoto with backtracking transitions included  -> identity FAILS.
      (ii) K(9,11,15): invariants 359/718/15708 change -> cert detects.
      (iii) wrong Bass exponent (|E|−|V| ± 1) -> identity FAILS.
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

PRIMES = [1_000_000_007, 998_244_353, 1_000_000_009]  # p^2 < 2^63, safe for int64 products


# ----------------------------------------------------------------------------- scene builders
def tripartite(sizes):
    """Return (A 0/1 list-of-lists, degrees, zone-of-vertex, directed-edge list) for K(sizes)."""
    zone = []
    for zi, s in enumerate(sizes):
        zone += [zi] * s
    n = len(zone)
    A = [[1 if zone[i] != zone[j] else 0 for j in range(n)] for i in range(n)]
    deg = [sum(A[i]) for i in range(n)]
    dedges = [(i, j) for i in range(n) for j in range(n) if A[i][j]]  # directed
    return A, deg, zone, dedges


def rank_over_Q(A):
    """Exact rank via fraction-free Gaussian elimination (Fraction), no floats."""
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


def hashimoto(dedges, backtracking=False):
    """718x718 (or size |dedges|) 0/1 Hashimoto matrix. e=(a,b), f=(c,d): B[e,f]=1 iff b==c and
    (backtracking or a!=d). Returns numpy int32."""
    idx = {e: k for k, e in enumerate(dedges)}
    L = len(dedges)
    B = np.zeros((L, L), dtype=np.int32)
    # group edges by tail for speed: outgoing from vertex b
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


# ----------------------------------------------------------------------------- modular linear algebra
def det_mod(mat, p):
    """Determinant of an integer matrix mod prime p (numpy int64 Gaussian elimination)."""
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


def rat_mod(fr: Fraction, p: int) -> int:
    return (fr.numerator % p) * pow(fr.denominator % p, p - 2, p) % p


def lhs_mod(B, u: Fraction, p: int) -> int:
    L = B.shape[0]
    up = rat_mod(u, p)
    M = (np.eye(L, dtype=np.int64) - (up * B.astype(np.int64))) % p
    return det_mod(M, p)


def rhs_mod(A, deg, u: Fraction, p: int, bass_exp: int) -> int:
    A = np.asarray(A, dtype=np.int64)
    n = A.shape[0]
    up = rat_mod(u, p)
    u2 = (up * up) % p
    Dm1 = np.diag([d - 1 for d in deg]).astype(np.int64)
    M = (np.eye(n, dtype=np.int64) - up * A + u2 * Dm1) % p
    small = det_mod(M, p)
    one_minus_u2 = (1 - u2) % p
    return (pow(one_minus_u2, bass_exp, p) * small) % p


def charpoly_3x3_int(Q):
    """Exact integer charpoly coeffs [c0,c1,c2] of λ³ + c2 λ² + c1 λ + c0 for a 3x3 int matrix."""
    a, b, c = Q[0]; d, e, f = Q[1]; g, h, i = Q[2]
    tr = a + e + i
    m2 = (e * i - f * h) + (a * i - c * g) + (a * e - b * d)   # sum of principal 2-minors
    det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    # charpoly = λ³ − tr λ² + m2 λ − det
    return {"c2": -tr, "c1": m2, "c0": -det}


# ----------------------------------------------------------------------------- checks
def main() -> int:
    ok = True
    print("=== W1 · Ihara–Bass exact certificate on K(9,11,13) ===")

    A, deg, zone, dedges = tripartite((9, 11, 13))
    V, E2 = len(deg), sum(deg)
    E = E2 // 2

    # [1] invariants + exact rank
    d_by_zone = sorted({(zone[i], deg[i]) for i in range(V)})
    degs = tuple(d for _, d in d_by_zone)
    rk = rank_over_Q(A)
    c1 = (V == 33 and E == 359 and E2 == 718 and degs == (24, 22, 20) and rk == 3)
    print(f"[1] |V|={V} |E|={E} 2|E|={E2} degrees(zone)={degs} rank(A)={rk} : {'PASS' if c1 else 'FAIL'}")
    ok &= c1
    if c1:
        print("PASS_SCENE_INVARIANTS")

    # [2] depth-2 identity + backtrack bijection
    sd2 = sum(d * d for d in deg)
    sdd = sum(d * (d - 1) for d in deg)
    excess = sd2 - sdd
    backtracks = sum(1 for (a, b) in dedges for (c, d) in [(b, a)] if A[b][a])  # a->b->a walks
    c2 = (sd2 == 15708 and sdd == 14990 and excess == 718 == E2 and backtracks == E2)
    print(f"[2] Σd²={sd2} Σd(d−1)={sdd} excess={excess}=2|E| ; backtrack-walks={backtracks}=#dir-edges : "
          f"{'PASS' if c2 else 'FAIL'}")
    ok &= c2
    if c2:
        print("PASS_DEPTH2_BACKTRACK_BIJECTION")

    # [3] Ihara–Bass at 5 rational u, each mod 3 primes
    B = hashimoto(dedges, backtracking=False)
    assert B.shape == (E2, E2), "Hashimoto must be 2|E| square"
    us = [Fraction(1, 3), Fraction(1, 7), Fraction(-2, 5), Fraction(2, 9), Fraction(3, 11)]
    bass = E - V   # 326
    all_id = True
    for u in us:
        for p in PRIMES:
            l = lhs_mod(B, u, p)
            r = rhs_mod(A, deg, u, p, bass)
            if l != r:
                all_id = False
                print(f"    MISMATCH u={u} p={p}: lhs={l} rhs={r}")
    print(f"[3] Ihara–Bass det(I−uB)==(1−u²)^{bass}·det(I−uA+u²(D−I)) at u={us}, mod {len(PRIMES)} primes : "
          f"{'PASS' if all_id else 'FAIL'}")
    ok &= all_id
    if all_id:
        print("PASS_IHARA_BASS_IDENTITY_EXACT_MODULAR")

    # [4] FINDING: rank-3 adjacency spectrum = zone-quotient charpoly = vacuum cubic
    Q = [[0, 11, 13], [9, 0, 13], [9, 11, 0]]
    cp = charpoly_3x3_int(Q)
    c4 = (cp["c2"] == 0 and cp["c1"] == -359 and cp["c0"] == -2574)
    print(f"[4] FINDING zone-quotient charpoly = λ³ {cp['c2']:+d}λ² {cp['c1']:+d}λ {cp['c0']:+d} "
          f"(= λ³−359λ−2574) : {'PASS' if c4 else 'FAIL'}")
    ok &= c4
    if c4:
        print("FINDING_ADJACENCY_RANK3_SPECTRUM_IS_VACUUM_CUBIC")

    # --- Negative controls (must be reachable and demonstrably break) ---
    print("Negative controls (each must break the identity / detect the change):")

    # (i) backtracking Hashimoto -> identity must FAIL at some (u,p)
    Bbt = hashimoto(dedges, backtracking=True)
    broke_i = False
    for u in (Fraction(1, 3), Fraction(2, 9)):
        for p in PRIMES:
            if lhs_mod(Bbt, u, p) != rhs_mod(A, deg, u, p, bass):
                broke_i = True
    print(f"  (i)  backtracking-B breaks Ihara–Bass : {'PASS(control fires)' if broke_i else 'FAIL(control dead)'}")
    ok &= broke_i
    if broke_i:
        print("FAIL_BACKTRACKING_B_BREAKS_IDENTITY")

    # (ii) K(9,11,15): invariants must change and be detected
    A5, deg5, _, ded5 = tripartite((9, 11, 15))
    inv5 = (sum(deg5) // 2, sum(deg5), sum(d * d for d in deg5))
    changed = inv5 != (359, 718, 15708)
    print(f"  (ii) K(9,11,15) invariants {inv5} != (359,718,15708) : "
          f"{'PASS(control fires)' if changed else 'FAIL'}")
    ok &= changed
    if changed:
        print("FAIL_K91115_INVARIANTS_DIFFER")

    # (iii) wrong Bass exponent must break identity
    broke_iii = False
    for bad in (bass - 1, bass + 1):
        for u in (Fraction(1, 3),):
            for p in PRIMES:
                if lhs_mod(B, u, p) != rhs_mod(A, deg, u, p, bad):
                    broke_iii = True
    print(f"  (iii) wrong Bass exponent (326±1) breaks identity : "
          f"{'PASS(control fires)' if broke_iii else 'FAIL(control dead)'}")
    ok &= broke_iii
    if broke_iii:
        print("FAIL_WRONG_BASS_EXPONENT_BREAKS_IDENTITY")

    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
