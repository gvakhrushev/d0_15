#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exact SD/ASD replay for the owned A4D character symbol.

The script rebuilds A from the finite star-action definition and compares all
576 entries with the pinned sparse owner table before checking the Hodge
identities.  On the complex torus it proves the additive rank formula
rank(A)=rank(M)+rank(sigma(M)); doubling is restricted to the unit torus.
An exact algebraic rank-23 witness rejects universal complex rank doubling.

Run: python3 a4d_sd_asd_reduction_check.py
"""
import hashlib
import json
from pathlib import Path
from itertools import combinations
import sympy as sp

z = sp.symbols('z0:4'); x = sp.symbols('x'); I = sp.I
eta = sp.diag(1, -1, -1, -1)
PAIR = list(combinations(range(4), 2)); pidx = {p: i for i, p in enumerate(PAIR)}

# star on the 6 external-pair components: 01->-23, 02->13, 03->-12, 12->03, 13->-02, 23->01
STAR = sp.zeros(6)
for src, (dst, s) in {(0,1):((2,3),-1),(0,2):((1,3),1),(0,3):((1,2),-1),
                      (1,2):((0,3),1),(1,3):((0,2),-1),(2,3):((0,1),1)}.items():
    STAR[pidx[dst], pidx[src]] = s
G2 = sp.diag(*[eta[a, a]*eta[b, b] for a, b in PAIR])

def boost(j):
    m = sp.zeros(4); m[0, j] = m[j, 0] = 1; return m
def rot(i, j):
    m = sp.zeros(4); m[i, j] = 1; m[j, i] = -1; return m
GEN = [boost(1), boost(2), boost(3), rot(1, 2), rot(1, 3), rot(2, 3)]

def eps_rs(r, s):
    u, v = [q for q in range(4) if q not in (r, s)]
    seq = (r, s, u, v); inv = sum(seq[i] > seq[j] for i in range(4) for j in range(i+1, 4))
    return -1 if inv % 2 else 1

def biv(M):
    Y = M*eta; return sp.Matrix([Y[p[0], p[1]] for p in PAIR])

def build_A():
    a = [[sp.Symbol(f'a{d}_{k}') for k in range(6)] for d in range(4)]
    b = [[sp.Symbol(f'b{d}_{k}') for k in range(6)] for d in range(4)]
    def X(d, shift, sign):
        Zs = sp.prod([z[i]**shift[i] for i in range(4)]); M = sp.zeros(4)
        for k in range(6):
            M += GEN[k]*(a[d][k]*Zs + b[d][k]/Zs)
        return sign*M
    A = sp.zeros(24, 24)
    for r, s in combinations(range(4), 2):
        u, v = [q for q in range(4) if q not in (r, s)]
        e_r = [1 if i == r else 0 for i in range(4)]; e_s = [1 if i == s else 0 for i in range(4)]
        Xs = [X(r, [0,0,0,0], 1), X(s, e_r, 1), X(r, e_s, -1), X(s, [0,0,0,0], -1)]
        P1 = sum(Xs, sp.zeros(4))
        P2 = sum((M2*M2 for M2 in Xs), sp.zeros(4))/2 + \
             sum((Xs[i]*Xs[j] for i in range(4) for j in range(i+1, 4)), sp.zeros(4))
        F2 = sp.expand(P2 - P1*P1/2)
        V = sp.expand((G2*STAR*biv(F2))[pidx[(u, v)]]*eps_rs(r, s))
        for d1 in range(4):
            for d2 in range(4):
                for k1 in range(6):
                    for k2 in range(6):
                        c = V.coeff(a[d1][k1]).coeff(b[d2][k2])
                        if c != 0:
                            A[d1*6 + k1, d2*6 + k2] += c
    return A

def main():
    A = build_A()
    here = Path(__file__).resolve().parent
    source_path = here / 'A_and_mixed_symbol_entries.json'
    source = json.loads(source_path.read_text())
    owner_A = sp.zeros(24, 24)
    for row, col, expression in source['A_entries']:
        owner_A[row, col] = sp.sympify(
            expression, locals=dict(zip(source['coordinates'], z))
        )
    source_matches = all(
        sp.cancel(A[row, col] - owner_A[row, col]) == 0
        for row in range(24) for col in range(24)
    )
    # Omega: lift star (via biv) to the generator slots, one 6x6 block per role
    Mbiv = sp.Matrix.hstack(*[biv(G) for G in GEN])
    Sgen = sp.simplify(Mbiv.inv()*STAR*Mbiv)
    OM = sp.zeros(24, 24)
    for d in range(4):
        OM[d*6:(d+1)*6, d*6:(d+1)*6] = Sgen

    ok = {'owner_table_matches_all_576_entries': source_matches}
    ok['A_nnz_96'] = sum(1 for i in range(24) for j in range(24) if A[i, j] != 0) == 96
    ok['A_real_no_i'] = not any(sp.sympify(A[i, j]).has(I) for i in range(24) for j in range(24))
    ok['Omega_integral'] = all(OM[i, j] == int(OM[i, j]) for i in range(24) for j in range(24))
    ok['Omega_antisym'] = (OM + OM.T).is_zero_matrix
    ok['Omega_sq_eq_minusI'] = (OM*OM + sp.eye(24)).is_zero_matrix
    ok['A_anticommutes_Omega'] = (A*OM + OM*A).is_zero_matrix
    ok['blocks_rank4'] = all(sp.Matrix(A[d1*6:(d1+1)*6, d2*6:(d2+1)*6]).rank() == 4
                             for d1 in range(4) for d2 in range(4))

    # Constant SD/ASD basis from Omega-eigenvectors (+i x3, -i x3 per role) + chirality permutation
    plus  = [sp.Matrix([0, 0, -I, 1, 0, 0]), sp.Matrix([0, I, 0, 0, 1, 0]), sp.Matrix([-I, 0, 0, 0, 0, 1])]
    minus = [sp.Matrix([0, 0,  I, 1, 0, 0]), sp.Matrix([0, -I, 0, 0, 1, 0]), sp.Matrix([ I, 0, 0, 0, 0, 1])]
    C6 = sp.Matrix.hstack(*(plus + minus)); C6i = sp.simplify(C6.inv())
    B = sp.zeros(24, 24)
    for d1 in range(4):
        for d2 in range(4):
            B[d1*6:(d1+1)*6, d2*6:(d2+1)*6] = \
                sp.simplify(C6i*sp.Matrix(A[d1*6:(d1+1)*6, d2*6:(d2+1)*6])*C6)
    perm = [d*6 + k for d in range(4) for k in range(3)] + [d*6 + 3 + k for d in range(4) for k in range(3)]
    Bp = B[:, perm][perm, :]
    M = sp.expand(Bp[:12, 12:])
    def conj(e): return sp.expand(sp.expand(e).xreplace({I: -I}))
    ok['A_blockdiag'] = sp.expand(Bp[:12, :12]).is_zero_matrix and sp.expand(Bp[12:, 12:]).is_zero_matrix
    ok['lower_eq_conj_upper'] = all(sp.expand(sp.expand(Bp[12:, :12][i, j]) - conj(M[i, j])) == 0
                                    for i in range(12) for j in range(12))
    ok['M_blocks_skew'] = all((sp.Matrix(M[3*r:3*r+3, 3*c:3*c+3]) +
                               sp.Matrix(M[3*r:3*r+3, 3*c:3*c+3]).T).is_zero_matrix
                              for r in range(4) for c in range(4))
    ok['M_nnz_48'] = sum(1 for i in range(12) for j in range(12) if M[i, j] != 0) == 48
    Minv = sp.Matrix(12, 12, lambda i, j: sp.simplify(M[i, j].subs({z[k]: 1/z[k] for k in range(4)})))
    ok['M_Zinv_eq_MT'] = sp.expand(Minv - M.T).is_zero_matrix

    # Exact rank-23 witness on the same character symbol.
    u = z[0]
    f = ((151-48*I)*u**6 - 396*u**5 + (-178+252*I)*u**4
         - 2216*u**3 + (-97-252*I)*u**2 - 876*u + 124+48*I)
    M_slice = M.subs(dict(zip(z[1:], (1, -1, 2))))
    det_M_slice = sp.cancel(M_slice.det(method='domain-ge'))
    fpoly = sp.Poly(f, u, extension=I)
    fbarpoly = sp.Poly(f.xreplace({I: -I}), u, extension=I)
    ok['rank23_sextic_determinant_exact'] = sp.cancel(
        det_M_slice - f/(128*u**3)
    ) == 0
    ok['rank23_sextic_roots_simple'] = sp.gcd(fpoly, fpoly.diff()).degree() == 0
    ok['rank23_sextic_disjoint_from_conjugate'] = sp.gcd(
        fpoly, fbarpoly
    ).degree() == 0
    ok['rank23_sextic_has_no_zero_root'] = fpoly.TC() != 0

    # det A = det M * conj(det M) on the five pinned #317 slices + the diagonal
    sl = {'(x,1,1,1)': (x, 1, 1, 1), '(x,x,1,1)': (x, x, 1, 1), '(x,1/x,1,1)': (x, 1/x, 1, 1),
          '(x,x,x,1)': (x, x, x, 1), '(x,-1,1,1)': (x, -1, 1, 1), '(x,x,x,x)': (x, x, x, x)}
    ok['det_factorization'] = {}
    for nm, sub in sl.items():
        dA = sp.factor(sp.simplify(A.subs(dict(zip(z, sub))).det()))
        dM = sp.factor(sp.simplify(M.subs(dict(zip(z, sub))).det()))
        ok['det_factorization'][nm] = bool(sp.simplify(dA - dM*conj(dM)) == 0)

    # Exact diagonal chiral determinant. Clearing a denominator from every
    # row multiplies the determinant by den**12; do not label that numerator
    # as det(M).
    w = sp.symbols('w')
    Mw = sp.Matrix(12, 12, lambda i, j: M[i, j].subs({z[k]: I + w for k in range(4)}))
    den = sp.lcm([sp.denom(sp.together(Mw[i, j])) for i in range(12) for j in range(12)])
    Pm = sp.Matrix(12, 12, lambda i, j: sp.expand(sp.together(Mw[i, j]*den)))
    detM_diagonal = sp.factor(sp.cancel(Mw.det(method='domain-ge')))
    det_cleared = sp.factor(sp.cancel(Pm.det(method='domain-ge')))
    expected_detM_diagonal = -w**6*(w + 2*I)**6/(4*(w + I)**6)
    ok['detM_diagonal_rational_exact'] = sp.cancel(
        detM_diagonal - expected_detM_diagonal
    ) == 0
    ok['cleared_determinant_has_denominator_power_12'] = sp.cancel(
        det_cleared - den**12*detM_diagonal
    ) == 0
    ok['detA_diagonal_order_12'] = sp.cancel(
        A.subs(dict.fromkeys(z, I+w)).det(method='domain-ge')
        - w**12*(w+2*I)**12/(16*(w+I)**12)
    ) == 0

    for k, v in ok.items():
        if isinstance(v, dict):
            print(k, '->', v)
        else:
            print(('PASS ' if v else 'FAIL ') + k)
    assert all((all(vv for vv in v.values()) if isinstance(v, dict) else v)
               for v in ok.values()), "certificate failed"
    print('RANK(A)=RANK(M)+RANK(SIGMA(M)); DOUBLING_ONLY_ON_UNIT_TORUS')
    print('RANK_23_WITNESS: det(M)=f(u)/(128*u^3), alpha any simple root of f')
    print('det(M(i+w)) =', detM_diagonal)
    print('det(den*M(i+w)) =', det_cleared)
    result = {
        'schema': 1,
        'owner_symbol_sha256': hashlib.sha256(source_path.read_bytes()).hexdigest(),
        'checks': ok,
        'rank_23_witness': {
            'characters': ['alpha', '1', '-1', '2'],
            'f': str(sp.expand(f)),
            'det_M': str(f/(128*u**3)),
            'rank_M': 11,
            'rank_sigma_M': 12,
            'rank_A': 23,
            'exact_reason': 'simple zero of det M and coprimality with conjugate determinant',
        },
        'diagonal': {
            'det_M': str(detM_diagonal),
            'clearing_denominator': str(den),
            'det_cleared_matrix': str(det_cleared),
            'cleared_determinant_relation': 'det(den*M)=den^12*det(M)',
        },
        'rank_scope': {
            'complex_torus': 'rank(A)=rank(M)+rank(sigma(M))',
            'unit_torus': 'sigma(M)=M^dagger; rank(A)=2*rank(M)',
        },
        'terminal': 'A4D_SD_ASD_REDUCTION_WITH_COMPLEX_RANK_SCOPE_CERTIFIED',
    }
    result_path = here / 'a4d_sd_asd_reduction_results.json'
    result_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print('PASS', len(ok), 'exact checks')
    print('A4D-SD-ASD-REDUCTION-WITH-SCOPE-CERTIFIED')

if __name__ == '__main__':
    main()
