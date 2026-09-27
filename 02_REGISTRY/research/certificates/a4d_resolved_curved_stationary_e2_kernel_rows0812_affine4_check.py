#!/usr/bin/env python3
"""Rows 0, 8, 12 on the section 9.27 mode-1100 kernel.

The thirteen free mode-1100 components are reduced to the function-field
kernel of source-zero rows 10, 11, 14, 15. Rows 1, 2, 3 do not see Ka.
This certificate asks whether that kernel, together with the four Ka
coordinates, can clear rows 0, 8, and 12.
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
print('SECONDS', monotonic() - st, flush=True)
raise SystemExit(0)
""", 1)
exec(compile(src, str(CERT), "exec"), {"__name__": "__main__", "__file__": str(CERT)})
