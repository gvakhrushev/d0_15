#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=1200
"""Quadratic remainder on free translations and Ka at (rho,t,p)=(1,0,0).

The linear 12x14 system is solved by six kernel columns. This run
evaluates the rational particular amplitude, its four Ka directions and
their polarizations. Exact contractions test the solved translation and
four independent free Ka=0 translations. This is a projected affine-order
jet at one modulus point, not the untruncated stationary Euler system.
"""
from __future__ import annotations

import pathlib
import sys

CERT = pathlib.Path(__file__).resolve().parent / (
    "a4d_resolved_curved_stationary_e2_conformal_translation_ratio_affine4_check.py"
)
src = CERT.read_text()
src = src.replace(
    "out=[[[zz,zz,zz]for ch in range(4)]for row in range(16)]",
    "out=[[[zz]*16 for ch in range(4)]for row in range(16)]",
    1,
)
old_beta = "for beta,inds in enumerate(((0,),(8,),(12,))):"
new_beta = (
    "for beta,inds in enumerate(((0,),(8,),(12,),(1,),(2,),(3,),(4,),(5,),(6,),(7,),"
    "(9,),(10,),(11,),(13,),(14,),(15,))):"
)
if old_beta not in src:
    sys.exit("beta pattern missing")
src = src.replace(old_beta, new_beta, 1)
needle = (
    "check('EXACT_BEZOUT_ONE_FOR_FINAL_REAL_RHO_SEAM',g.as_expr()==1 "
    "and s.expand((bp*P+bq*Q).as_expr()-1)==0)\n"
)
if needle not in src:
    sys.exit("bezout needle missing")
src = src.replace(needle, needle + r"""
FREE = (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
NAME = {
    3: 'b0.e1', 4: 'b0.e2', 5: 'b0.e3', 6: 'b1.e0', 7: 'b1.e1',
    8: 'b1.e2', 9: 'b1.e3', 10: 'b2.e1', 11: 'b2.e2', 12: 'b2.e3',
    13: 'b3.e1', 14: 'b3.e2', 15: 'b3.e3',
}
CLOSED = {4, 5, 8, 9}
def slot(row, raw, k):
    return s.cancel(sum((coef[ch] * raw[ch][k].as_expr() for ch in range(4)), s.Integer(0)))
amp = part[10:, :]
for i in (10, 11, 14, 15):
    check(f'SOURCE_ROW_{i}_ZERO', s.cancel(source[i]) == 0)
columns = {}
for k in FREE:
    Et = s.Matrix([slot(i, R0[i], k) for i in range(16)]).subs(sub).applyfunc(s.cancel)
    Ct = s.Matrix([[slot(i, col[i], k) for col in cols] for i in range(16)]).subs(sub).applyfunc(s.cancel)
    trans = (Et + Ct * amp).applyfunc(s.cancel)
    D = (Ct * Ka).applyfunc(s.cancel)
    bad = [(i, j) for i in range(16) for j in range(4) if D[i, j] != 0]
    check(NAME[k] + '_KA_DERIVATIVE_ZERO', not bad)
    columns[k] = trans
    print('SLOT', NAME[k], flush=True)
NINE = tuple(k for k in FREE if k not in CLOSED)
HELD = ((2, 6), (3, 7), (8, 9), (12, 13))
BROKEN = ((0, 4), (1, 5))
for k in FREE:
    for a, b in HELD:
        check(NAME[k] + f'_ROW_{b}_IS_MINUS_ROW_{a}', s.cancel(columns[k][a] + columns[k][b]) == 0)
for k in CLOSED:
    for a, b in BROKEN:
        check(NAME[k] + f'_ROW_{b}_IS_MINUS_ROW_{a}', s.cancel(columns[k][a] + columns[k][b]) == 0)
for k in NINE:
    for a, b in BROKEN:
        check(NAME[k] + f'_ROW_{b}_IS_NOT_MINUS_ROW_{a}', s.cancel(columns[k][a] + columns[k][b]) != 0)
Ka_aff = (Cp * Ka).applyfunc(s.cancel)
for row in (1, 2, 3, 10, 11, 14, 15):
    check(f'COLLINEAR_KA_ROW_{row}_ZERO', Ka_aff.row(row) == s.zeros(1, 4))
for a, b in ((0, 4), (8, 9), (12, 13)):
    same = s.expand(Ka_aff.row(a) + Ka_aff.row(b)) == s.zeros(1, 4)
    print('KA_SIGN', a, b, 'MINUS' if same else 'BROKEN', flush=True)
t2 = t - 2
Q4 = 25 * t**4 - 660 * t**3 + 3764 * t**2 + 3840 * t - 1472
R4 = -(25 * t**4 - 660 * t**3 + 3476 * t**2 + 4992 * t - 2624)
explicit = [
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [-1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [-4, 0, 0, 0, 0, 0, 0, -1, 0, 0, 1, 0, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 1],
    [Q4 / (72 * t2**2), 0, 0, 0, 0, 0, 0, -ut, ut / 2, 1, 0, 0, 0],
    [R4 / (72 * t2**2), 0, 0, 0, 0, 0, 0, ut, -ut / 2, 0, 0, 1, 0],
]
BK = s.Matrix(explicit).T
LIVE = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13)
S = s.Matrix([[columns[k][i] for k in FREE] for i in LIVE])
SB = (S * BK).applyfunc(lambda e: s.together(e))
Klive = Ka_aff.extract(list(LIVE), list(range(4)))
rhs = s.Matrix([-source[i] for i in LIVE])
sysm = SB.row_join(Klive)
aug = sysm.row_join(rhs)
points = ((0, 0, {rho: 1, t: 0, p: 0}), (3, 1, {rho: 1, t: 3, p: 1}), (4, 0, {rho: 2, t: 4, p: 0}))
seen = []
for tv, pv, point in points:
    Sp = sysm.subs(point).applyfunc(s.together)
    Ap = aug.subs(point).applyfunc(s.together)
    r_sys, r_aug = Sp.rank(), Ap.rank()
    print('POINT', tv, pv, r_sys, r_aug, flush=True)
    seen.append((tv, pv, r_sys, r_aug, Sp, Ap))
    check(f'POINT_T{tv}_P{pv}_CONSISTENT', r_sys == r_aug)
check('POINT_T0_RANK_6', seen[0][2] == 6)
check('POINT_T3_RANK_6', seen[1][2] == 6)
check('POINT_T4_RANK_6', seen[2][2] == 6)
sol, params = seen[0][4].gauss_jordan_solve(seen[0][5][:, -1])
ns = seen[0][4].nullspace()
print('NULL_DIAG', seen[0][4].cols, params.cols, len(ns), params.rank(), flush=True)
check('POINT_T0_PARTICULAR', (seen[0][4] * sol - seen[0][5][:, -1]).applyfunc(s.together) == s.zeros(12, 1))
N = s.Matrix.hstack(*ns)
check('POINT_T0_NULLITY_8', len(ns) == 8 and N.rank() == 8 and (seen[0][4] * N).applyfunc(s.together) == s.zeros(12, 8))
for a, b in ((1, 5), (2, 6), (3, 7)):
    check(f'KA_ROW_{b}_IS_MINUS_ROW_{a}', s.expand(Ka_aff.row(a) + Ka_aff.row(b)) == s.zeros(1, 4))
for a, b in ((2, 6), (3, 7), (8, 9), (12, 13)):
    ia, ib = LIVE.index(a), LIVE.index(b)
    row_diff = (sysm.row(ia) + sysm.row(ib)).applyfunc(lambda e: s.expand(s.together(e)))
    rhs_diff = s.expand(s.together(rhs[ia] + rhs[ib]))
    check(f'JOINT_ROW_{b}_IS_MINUS_ROW_{a}', row_diff == s.zeros(1, 14) and rhs_diff == 0)
indep = [LIVE.index(aff) for aff in (0, 1, 2, 3, 8, 12)]
pivots = [0, 1, 2, 3, 6, 8]
P = sysm[indep, pivots].applyfunc(lambda e: s.cancel(s.together(e)))
print('PIVOT_ENTRY_CHARS', max(len(str(P[i, j])) for i in range(6) for j in range(6)), flush=True)
d0 = s.together(P.subs({rho: 1, t: 0, p: 0}).det())
check('PIVOT_MINOR_NONZERO_AT_T0', d0 != 0)
for a, b in ((0, 4), (1, 5)):
    ia, ib = LIVE.index(a), LIVE.index(b)
    row_diff = (sysm.row(ia) + sysm.row(ib)).applyfunc(lambda e: s.expand(s.together(e)))
    rhs_diff = s.expand(s.together(rhs[ia] + rhs[ib]))
    check(f'JOINT_ROW_{b}_IS_MINUS_ROW_{a}', row_diff == s.zeros(1, 14) and rhs_diff == 0)
print('SIX_ROWS_WITH_INVERTIBLE_MINOR', [LIVE[i] for i in indep], pivots, flush=True)
point = {rho: 1, t: 0, p: 0}
Pp = P.subs(point).applyfunc(s.together)
bp = rhs.extract(indep, [0]).subs(point).applyfunc(s.together)
y6 = Pp.solve(bp)
check('POINT_PIVOT_SOLVE', (Pp * y6 - bp).applyfunc(s.together) == s.zeros(6, 1))
full_y = s.zeros(14, 1)
for a, j in enumerate(pivots):
    full_y[j] = s.together(y6[a])
print('PIVOT_Y', [str(full_y[j]) for j in pivots], flush=True)
amp_pt = [s.together(s.simplify(part[10 + k].subs({rho: 1, t: 0}))) for k in range(7)]
print('AMP_PT', amp_pt, flush=True)
specs = list(o.SELECTED_SPECS)
def X_of(c):
    Xs = [f.mz(4) for _ in range(4)]
    for k, (_, role, g) in enumerate(specs):
        ck = s.together(s.simplify(c[k]))
        if ck == 0:
            continue
        Xs[role] = f.madd(Xs[role], f.mscale(K.from_expr(ck), f.mc(g)))
    return Xs
print('RESP_PARTICULAR', flush=True)
Rp = resp(X_of(amp_pt))
def raw_linear(row_i, ch, beta):
    acc = zz
    for k in range(7):
        if amp_pt[k] == 0:
            continue
        acc += K.from_expr(amp_pt[k]) * cols[k][row_i][ch][beta]
    return acc
rem = [[[Rp[row_i][ch][beta] - R0[row_i][ch][beta] - raw_linear(row_i, ch, beta) for beta in range(16)] for ch in range(4)] for row_i in range(16)]
ut0 = s.together(ut.subs(t, 0))
qt0 = s.together(qt.subs({rho: 1, t: 0}))
coef_pt = [s.together(c.subs({rho: 1, r: -1, p: 0, q: qt0})) for c in coef]
Bpt = BK.subs(point).applyfunc(s.together)
sigma = Bpt * full_y[:10, :]
BETA_TRANS = (0, 8, 12, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 14, 15)
tau = [s.Integer(0)] * 16
tau[0] = s.Integer(-4)
tau[1] = s.Integer(-1)
tau[2] = s.Integer(1)
for i in range(13):
    tau[3 + i] = s.together(sigma[i])
def weighted(block, tau_vec):
    out = []
    for row_i in range(16):
        acc = 0
        for ch in range(4):
            mix = 0
            for beta in range(16):
                mix += tau_vec[beta] * block[row_i][ch][beta].as_expr()
            acc += coef_pt[ch] * mix
        out.append(s.together(s.expand(acc)))
    return out
quad = weighted(rem, tau)
six = (0, 1, 2, 3, 8, 12)
print('QUAD_PART', [(i, quad[i]) for i in six], flush=True)
free_kernel = [j for j in range(10) if j not in pivots]
cols_q = []
for j in free_kernel:
    tau_j = [s.Integer(0)] * 16
    for i in range(13):
        tau_j[3 + i] = s.together(Bpt[i, j])
    qj = weighted(rem, tau_j)
    cols_q.append([qj[i] for i in six])
base_q = s.Matrix([quad[i] for i in six])
Mq = s.Matrix(cols_q).T
aug_q = Mq.row_join(base_q)
print('QUAD_FREE', free_kernel, 'RANK', Mq.rank(), 'AUG', aug_q.rank(), flush=True)
check('QUAD_PART_SIX_ROWS_ZERO', all(quad[i] == 0 for i in six))
check('QUAD_KA0_FAMILY_STAYS_ZERO', Mq == s.zeros(6, 4) and aug_q.rank() == 0)
check('PIVOT_Y_AT_T0', [s.together(full_y[j]) for j in pivots] == [s.Integer(0), s.Integer(0), s.Integer(-4), s.Integer(-4), s.Integer(1), s.Integer(0)])
ka_dirs = (
    (1, 0, 0, 0, 0, 0, 0),
    (0, 1, 0, 0, 0, 0, 0),
    (0, 0, 0, 1, 1, 0, 0),
    (0, 0, -1, 0, 0, 0, 1),
)
def block_sub(A, B, C, D):
    return [[[A[row_i][ch][beta] - B[row_i][ch][beta] - C[row_i][ch][beta] + D[row_i][ch][beta] for beta in range(16)] for ch in range(4)] for row_i in range(16)]
def six_zero(vals, name):
    bad = [(row_i, vals[row_i]) for row_i in six if vals[row_i] != 0]
    if bad:
        print(name, bad, flush=True)
    check(name, not bad)
ka_resp = []
free_translation_taus = {}
for j in free_kernel:
    tau_j = [s.Integer(0)] * 16
    for k in range(13):
        tau_j[3 + k] = s.together(Bpt[k, j])
    free_translation_taus[j] = tau_j
T_free = s.Matrix([[tau_j[3 + k] for j, tau_j in free_translation_taus.items()]
                   for k in range(13)])
check('FOUR_FREE_TRANSLATION_DIRECTIONS_INDEPENDENT', T_free.rank() == 4)
for i, d in enumerate(ka_dirs):
    print('RESP_KA', i, flush=True)
    Rd = resp(X_of(d))
    ka_resp.append(Rd)
    Rpd = resp(X_of([amp_pt[k] + d[k] for k in range(7)]))
    R2 = resp(X_of([2 * d[k] for k in range(7)]))
    cross = block_sub(Rpd, Rp, Rd, R0)
    square = block_sub(R2, Rd, Rd, R0)
    six_zero(weighted(cross, tau), f'KA_CROSS_{i}_SIX_ZERO')
    six_zero(weighted(square, tau), f'KA_SQUARE_{i}_SIX_ZERO')
    for j, tau_j in free_translation_taus.items():
        mixed = weighted(cross, tau_j)
        vals = tuple(s.cancel(mixed[row_i]) for row_i in six)
        print('FREE_TRANSLATION_KA_CROSS', j, i, vals, flush=True)
        check(f'FREE_TRANSLATION_{j}_KA_CROSS_{i}_SIX_ZERO',
              all(value == 0 for value in vals))
        six_zero(weighted(square, tau_j),
                 f'FREE_TRANSLATION_{j}_KA_SQUARE_{i}_SIX_ZERO')
for i in range(4):
    for j in range(i + 1, 4):
        print('RESP_PAIR', i, j, flush=True)
        Rij = resp(X_of([ka_dirs[i][k] + ka_dirs[j][k] for k in range(7)]))
        pair = block_sub(Rij, ka_resp[i], ka_resp[j], R0)
        six_zero(weighted(pair, tau), f'KA_PAIR_{i}_{j}_SIX_ZERO')
        for k, tau_k in free_translation_taus.items():
            six_zero(weighted(pair, tau_k),
                     f'FREE_TRANSLATION_{k}_KA_PAIR_{i}_{j}_SIX_ZERO')
print('SECONDS', monotonic() - st, flush=True)
raise SystemExit(0)
""", 1)
exec(compile(src, str(CERT), "exec"), {"__name__": "__main__", "__file__": str(CERT)})
