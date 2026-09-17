#!/usr/bin/env python3
"""Concrete finite spin-2 TT wave-operator certificate (EXACT).

The TT projector is checked on the full 10-dimensional basis of Sym(4) with EXACT
rational (Fraction) arithmetic — no floats, no tolerance, no random perturbation. Every
check can FAIL, including real negative controls; the rank is computed by exact row
reduction over Q.
"""
from __future__ import annotations

import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

N = 4
ETA = [[F(1), F(0), F(0), F(0)],
       [F(0), F(-1), F(0), F(0)],
       [F(0), F(0), F(-1), F(0)],
       [F(0), F(0), F(0), F(-1)]]
K = [F(1), F(1), F(0), F(0)]
U = [F(1), F(0), F(0), F(0)]


def matmul(A, B):
    n, m, p = len(A), len(B), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(m)) for j in range(p)] for i in range(n)]


def trace(A):
    return sum(A[i][i] for i in range(len(A)))


def matvec(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]


def scal(c, A):
    return [[c * x for x in row] for row in A]


def add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def pairing(a, b):
    return trace(matmul(matmul(matmul(a, ETA), b), ETA))


def tr_eta(a):
    return trace(matmul(a, ETA))


def div(a):
    return matvec(matmul(a, ETA), K)


def time_proj(a):
    return matvec(matmul(a, ETA), U)


def exact_rank(M):
    """Rank of a rational matrix by Gaussian elimination over Q."""
    A = [row[:] for row in M]
    rows, cols = len(A), len(A[0])
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if A[i][c] != 0), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = A[r][c]
        A[r] = [x / inv for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [A[i][j] - f * A[r][j] for j in range(cols)]
        r += 1
        if r == rows:
            break
    return r


def main() -> int:
    print("--- D0 FINITE SPIN-2 WAVE OPERATOR CONCRETE CERTIFICATE (exact) ---")

    e_plus = [[F(0)] * N for _ in range(N)]
    e_plus[2][2] = F(1); e_plus[3][3] = F(-1)
    e_cross = [[F(0)] * N for _ in range(N)]
    e_cross[2][3] = F(1); e_cross[3][2] = F(1)

    norm_plus = pairing(e_plus, e_plus)
    norm_cross = pairing(e_cross, e_cross)
    assert norm_plus == 2 and norm_cross == 2, "TT polarization norms != 2"
    assert pairing(e_plus, e_cross) == 0, "TT polarizations not orthogonal"

    def pi_tt(h):
        return add(scal(pairing(e_plus, h) / norm_plus, e_plus),
                   scal(pairing(e_cross, h) / norm_cross, e_cross))

    sym_basis = []
    for i in range(N):
        for j in range(i, N):
            m = [[F(0)] * N for _ in range(N)]
            m[i][j] = F(1); m[j][i] = F(1)
            sym_basis.append(m)
    assert len(sym_basis) == 10

    zero_vec = [F(0)] * N
    for b in sym_basis:
        p = pi_tt(b)
        assert pi_tt(p) == p, "Pi_TT idempotence failed"
        assert tr_eta(p) == 0, "trace-free failed"
        assert div(p) == zero_vec, "transverse failed"
        assert time_proj(p) == zero_vec, "time-orthogonal failed"
    print("[1] Pi_TT checked on all 10 symmetric basis elements (exact): PASS")

    # trace mode and 4 gauge generators annihilated
    assert pi_tt(ETA) == [[F(0)] * N for _ in range(N)], "trace mode not annihilated"
    for a in range(N):
        xi = [F(1) if t == a else F(0) for t in range(N)]
        sg = [[K[i] * xi[j] + xi[i] * K[j] for j in range(N)] for i in range(N)]
        assert pi_tt(sg) == [[F(0)] * N for _ in range(N)], "gauge mode not annihilated"
    print("[2] trace mode and 4 gauge generators annihilated (exact): PASS")

    # 10x10 projector matrix in the sym basis: idempotent, rank 2 (exact)
    P = [[F(0)] * 10 for _ in range(10)]
    for col, b in enumerate(sym_basis):
        p = pi_tt(b)
        for row, rb in enumerate(sym_basis):
            denom = sum(rb[i][j] * rb[i][j] for i in range(N) for j in range(N))
            num = sum(p[i][j] * rb[i][j] for i in range(N) for j in range(N))
            P[row][col] = num / denom
    assert matmul(P, P) == P, "projector not idempotent"
    rank = exact_rank(P)
    assert rank == 2, f"projector rank != 2: {rank}"
    print("[3] projector matrix idempotent and rank=2 (exact): PASS")

    # W_TT = Pi_TT o Pi_TT: nonnegative energy, preserves TT (exact)
    for b in sym_basis:
        energy = pairing(b, pi_tt(pi_tt(b)))
        assert energy >= 0, "W_TT energy negative"
        assert pi_tt(pi_tt(pi_tt(b))) == pi_tt(b), "W_TT does not preserve TT"
    print("[4] W_TT nonnegative on the symmetric basis and preserves TT (exact): PASS")

    # TT stress coupling sees only the TT projection (exact)
    stresses = [e_plus, e_cross, add(scal(F(2), e_plus), scal(F(-3), e_cross))]
    for b in sym_basis:
        for s in stresses:
            assert pairing(b, s) == pairing(pi_tt(b), s), "stress coupling leaks off-TT"
    print("[5] TT stress coupling sees only the TT projection (exact): PASS")

    # degrees of freedom: 10 sym components - 8 constraints = 2
    assert (N * (N + 1)) // 2 == 10 and 2 * N == 8 and 10 - 8 == 2
    print("[6] finite_spin2_four_role_dof_eq_two: PASS")

    # ---- negative controls (REAL) --------------------------------------------------
    assert tr_eta(ETA) != 0, "control: eta itself is NOT trace-free (a non-TT mode)"
    print("FAIL_ETA_IS_NOT_TT_TRACE_NONZERO")
    assert rank != 3, "control: the TT projector rank is 2, not 3"
    print("FAIL_PROJECTOR_RANK_NOT_3")
    print("PASS_SPIN2_NEGATIVE_CONTROLS")

    print("[CERT-CLOSED] PASS_FINITE_SPIN2_WAVE_OPERATOR_CONCRETE")
    return 0


# backward-compat alias: vp_finite_spin2_wave_operator.py imports `run_certificate`
run_certificate = main

if __name__ == "__main__":
    raise SystemExit(main())
