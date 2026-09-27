#!/usr/bin/env python3
"""Mode-1100 translation components on the section 9.23 reduction.

Collinear inputs b0.e0, b2.e0, b3.e0 stay inside the owned weights
(z, r, 1). The other thirteen components are free. Each column is the
weighted affine derivative at the particular solder amplitude, after
r=-1, z=-4, u=ut(t), q=qt(t). Ka is the owned 7x4 solder quotient.
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
# Beta positions. The owned response() reads positions 0, 1, 2 as the
# collinear weights z, r, 1, so those three stay translation indices 0, 8, 12.
FREE = (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
NAME = {
    3: 'b0.e1', 4: 'b0.e2', 5: 'b0.e3', 6: 'b1.e0', 7: 'b1.e1',
    8: 'b1.e2', 9: 'b1.e3', 10: 'b2.e1', 11: 'b2.e2', 12: 'b2.e3',
    13: 'b3.e1', 14: 'b3.e2', 15: 'b3.e3',
}
# Rows 10 and 11 vanish by the owned z and q(u-2) checks. Row 15 follows
# from the owned row sum at r=-1. Row 14 is not used to solve for those
# values; the certificate checks that it vanishes after the substitution.
CLOSED = {4, 5, 8, 9}
def slot(row, raw, k):
    return s.cancel(sum((coef[ch] * raw[ch][k].as_expr() for ch in range(4)), s.Integer(0)))
amp = part[10:, :]
check('SOURCE_ROW10_ZERO_ON_REDUCTION', s.cancel(source[10]) == 0)
check('SOURCE_ROW11_ZERO_ON_REDUCTION', s.cancel(source[11]) == 0)
check('SOURCE_ROW14_ZERO_ON_REDUCTION', s.cancel(source[14]) == 0)
check('SOURCE_ROW15_ZERO_ON_REDUCTION', s.cancel(source[15]) == 0)
for a, b in ((0, 4), (1, 5), (2, 6), (3, 7), (8, 9), (12, 13)):
    check(f'SOURCE_ROW_{b}_IS_MINUS_ROW_{a}', s.cancel(source[a] + source[b]) == 0)
zero_rows = [i for i in range(16) if s.cancel(source[i]) == 0]
print('SOURCE_ZERO_ROWS', zero_rows, flush=True)
for i in range(16):
    if i not in zero_rows:
        text = str(s.factor(source[i]))
        print('SOURCE', i, text if len(text) < 180 else text[:180] + '...', flush=True)
columns = {}
for k in FREE:
    name = NAME[k]
    Et = s.Matrix([slot(i, R0[i], k) for i in range(16)]).subs(sub).applyfunc(s.cancel)
    Ct = s.Matrix([[slot(i, col[i], k) for col in cols] for i in range(16)]).subs(sub).applyfunc(s.cancel)
    trans = (Et + Ct * amp).applyfunc(s.cancel)
    D = (Ct * Ka).applyfunc(s.cancel)
    bad = [(i, j) for i in range(16) for j in range(4) if D[i, j] != 0]
    if bad:
        print('KA_NONZERO', name, bad[:4], D[bad[0][0], bad[0][1]], flush=True)
    check(name + '_KA_DERIVATIVE_ZERO', not bad)
    if k in CLOSED:
        for i in (10, 11, 14, 15):
            check(name + f'_REDUCTION_ROW_{i}_ZERO', s.cancel(trans[i]) == 0)
    columns[k] = trans
    print('SLOT', name, 'KA0', flush=True)
unit = s.together(rho * (t - 2) / den)
WITNESS = {
    3: (10, -384 * unit),
    6: (10, 384 * unit),
    7: (10, -384 * unit),
    10: (15, -768 * unit),
    11: (11, 768 * unit),
    12: (10, 768 * unit),
    13: (15, 768 * unit),
    14: (10, 768 * unit),
    15: (11, -768 * unit),
}
for k, (row_i, expected) in WITNESS.items():
    check(NAME[k] + '_WITNESS_ROW', s.cancel(columns[k][row_i] - expected) == 0)
# The one-component statement is the witness identity above: on each of the
# nine slots, a source-zero row equals a nonzero chart unit times sigma.
# Joint kernel of every source-zero row, over the thirteen free components.
A = s.Matrix([[columns[k][i] for k in FREE] for i in zero_rows]).applyfunc(s.together)
print('HOMOGENEOUS_SHAPE', A.rows, A.cols, flush=True)
check('HOMOGENEOUS_RANK_3', A.rank() == 3)
def row_unit(exprs):
    parts = [s.fraction(s.together(e)) for e in exprs]
    common = s.Integer(1)
    for _n, d in parts:
        common = s.lcm(s.Poly(s.expand(d), t), s.Poly(common, t)).as_expr()
    return common
for r_i, row_i in enumerate(zero_rows):
    common = row_unit([A[r_i, j] for j in range(A.cols)])
    check(f'ROW_UNIT_{row_i}_IS_DEN', s.expand(common - den) == 0)
Ac = (den * A).applyfunc(lambda e: s.expand(s.together(e)))
check('CLEARED_RANK_3', Ac.rank() == 3)
check('CLEARED_NULLITY_10', len(Ac.nullspace()) == 10)
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
check('EXPLICIT_KERNEL_RANK_10', B.subs(t, 0).rank() == 10)
for j in range(10):
    image = (A * B[:, j]).applyfunc(lambda e: s.expand(s.together(e)))
    check(f'EXPLICIT_KERNEL_VECTOR_{j}', image == s.zeros(4, 1))
inh_rows = (1, 2, 3)
S3 = s.Matrix([[columns[k][i] for k in FREE] for i in inh_rows])
M3 = (S3 * B).applyfunc(lambda e: s.factor(s.together(e)))
check('ROW123_KERNEL_IMAGE_RANK_3', M3.rank() == 3)
print('SECONDS', monotonic() - st, flush=True)
raise SystemExit(0)
""", 1)
exec(compile(src, str(CERT), "exec"), {"__name__": "__main__", "__file__": str(CERT)})
