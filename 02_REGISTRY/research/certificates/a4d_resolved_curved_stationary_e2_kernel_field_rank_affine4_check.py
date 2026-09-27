#!/usr/bin/env python3
"""Function-field rank of the section 9.28 mode-1100 system.

Same 12x14 matrix as the three chart points: ten kernel coordinates and
four Ka columns on the twelve affine rows outside {10, 11, 14, 15}.
A 6x6 minor and the row dependencies are tested as rational functions.
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
B = s.Matrix(explicit).T
LIVE = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13)
S = s.Matrix([[columns[k][i] for k in FREE] for i in LIVE])
SB = (S * B).applyfunc(lambda e: s.together(e))
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
dt = s.factor(P.subs({rho: 1, p: 0}).det(method='bareiss'))
print('MINOR_AT_RHO1_P0', dt, flush=True)
check('PIVOT_MINOR_NOT_IDENTICALLY_ZERO', s.simplify(dt) != 0)
line = {rho: 1, p: 0}
Pu = P.subs(line).applyfunc(lambda e: s.cancel(s.together(e)))
for aff in (4, 5):
    i = LIVE.index(aff)
    row_p = s.Matrix([sysm[i, j].subs(line) for j in pivots]).applyfunc(lambda e: s.cancel(s.together(e)))
    coeff = Pu.T.solve(row_p)
    pred = sum((coeff[k] * sysm.row(indep[k]).subs(line) for k in range(6)), s.zeros(1, 14))
    diff = (pred - sysm.row(i).subs(line)).applyfunc(lambda e: s.expand(s.together(e)))
    nz = []
    for j in range(14):
        num_e, _den_e = s.fraction(s.together(diff[j]))
        if s.expand(num_e) != 0:
            nz.append(j)
    print('LINE_ROW_DIFF_COLS', aff, nz, flush=True)
    check(f'LINE_ROW_{aff}_IN_PIVOT_SPAN', not nz)
rhs_p = s.Matrix([rhs[i].subs(line) for i in indep]).applyfunc(lambda e: s.cancel(s.together(e)))
y6 = Pu.solve(rhs_p)
full_y = s.zeros(14, 1)
for a, j in enumerate(pivots):
    full_y[j] = s.together(y6[a])
residual = (sysm.subs(line) * full_y - rhs.subs(line)).applyfunc(lambda e: s.expand(s.together(e)))
bad_res = []
for i in range(12):
    num_e, _den_e = s.fraction(s.together(residual[i]))
    if s.expand(num_e) != 0:
        bad_res.append(LIVE[i])
print('LINE_RESIDUAL_ROWS', bad_res, flush=True)
check('LINE_PARTICULAR_CLEARS_TWELVE_ROWS', not bad_res)
for label, point in (('T6', {rho: 1, t: 6, p: 0}), ('R3T6', {rho: 3, t: 6, p: 4})):
    Sp = sysm.subs(point).applyfunc(s.together)
    Ap = aug.subs(point).applyfunc(s.together)
    r_sys, r_aug = Sp.rank(), Ap.rank()
    print('OFF_POINT', label, r_sys, r_aug, flush=True)
    check(f'{label}_CONSISTENT', r_sys == r_aug)
    check(f'{label}_RANK_6', r_sys == 6)
print('SECONDS', monotonic() - st, flush=True)
raise SystemExit(0)
""", 1)
exec(compile(src, str(CERT), "exec"), {"__name__": "__main__", "__file__": str(CERT)})
