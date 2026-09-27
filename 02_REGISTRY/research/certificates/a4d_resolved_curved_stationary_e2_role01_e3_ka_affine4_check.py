#!/usr/bin/env python3
"""Affine order four on the section 9.24 role-0/1 e3 chart, inside Ka.

Reuses the owned collinear certificate and adds the translation slot b0.e3
(index 3) and b1.e3 (index 7). The second-amplitude columns are the same
finite differences resp(generator)-resp(0) as section 9.23, then restricted
to the solder quotient Ka. A separate second-difference probe tests whether
those columns already contain the quadratic amplitude piece.
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
    "out=[[[zz,zz,zz,zz,zz]for ch in range(4)]for row in range(16)]",
    1,
)
old_beta = "for beta,inds in enumerate(((0,),(8,),(12,))):"
new_beta = "for beta,inds in enumerate(((0,),(8,),(12,),(3,),(7,))):"
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
def slot(row, raw, k):
    return s.cancel(sum((coef[ch] * raw[ch][k].as_expr() for ch in range(4)), s.Integer(0)))
for row_i in range(16):
    if s.simplify(slot(row_i, R0[row_i], 3) + slot(row_i, R0[row_i], 4)) != 0:
        raise AssertionError(f'weighted base role1 e3 row {row_i}')
    for col in cols:
        if s.simplify(slot(row_i, col[row_i], 3) + slot(row_i, col[row_i], 4)) != 0:
            raise AssertionError(f'weighted amplitude role1 e3 row {row_i}')
check('B1_E3_WEIGHTED_COLUMNS_ARE_NEGATIVES', True)
Et = s.Matrix([slot(row_i, R0[row_i], 3) for row_i in range(16)]).subs(sub).applyfunc(s.cancel)
Ct = s.Matrix([[slot(row_i, col[row_i], 3) for col in cols] for row_i in range(16)]).subs(sub).applyfunc(s.cancel)
amp = part[10:, :]
Qpoly = 200 * rho**3 + 555 * rho**2 + 260 * rho - 71
Dsig = 125 * rho**2 + 430 * rho - 47
Dp = 25 * rho**2 + 68 * rho - 13
sig_e3 = s.together(4 * Qpoly / Dsig)
p_e3 = s.together(rho * (50000 * rho**5 + 303375 * rho**4 + 438050 * rho**3 + 1620 * rho**2 - 45938 * rho + 3613) / (20480 * Dp * Qpoly))
tt = 1 - 5 * rho
chart = {t: tt, p: p_e3}
inhom = (source + sig_e3 * (Et + Ct * amp)).subs(chart).applyfunc(lambda e: s.together(s.simplify(e)))
deriv = ((Cp + sig_e3 * Ct) * Ka).subs(chart).applyfunc(lambda e: s.together(s.simplify(e)))
check('E3_KA_DERIVATIVE_IDENTICALLY_ZERO', all(s.simplify(deriv[i, j]) == 0 for i in range(16) for j in range(4)))
for cleared in (1, 2, 3, 5, 6, 7, 10, 11, 14, 15):
    check(f'E3_INHOM_ROW_{cleared}_ZERO', s.simplify(inhom[cleared]) == 0)
check('E3_ROW4_IS_MINUS_ROW0', s.simplify(inhom[4] + inhom[0]) == 0)
check('E3_ROW9_IS_MINUS_ROW8', s.simplify(inhom[9] + inhom[8]) == 0)
check('E3_ROW13_IS_MINUS_ROW12', s.simplify(inhom[13] + inhom[12]) == 0)
def numer(expr):
    num_e, _den_e = s.fraction(s.together(expr))
    _content, prim = s.primitive(s.Poly(s.expand(num_e), rho))
    return prim
N0, N8, N12 = numer(inhom[0]), numer(inhom[8]), numer(inhom[12])
g08, g012 = s.gcd(N0, N8), s.gcd(N0, N12)
print('E3_GCD_ROW0_ROW8', g08.as_expr(), flush=True)
print('E3_GCD_ROW0_ROW12', g012.as_expr(), flush=True)
print('E3_ROW0_NUMER', N0.as_expr(), flush=True)
reduced = []
for label, poly in (('N0', N0), ('N8', N8), ('N12', N12)):
    cur = poly
    rho_poly = s.Poly(rho, rho)
    g_rho = s.gcd(cur, rho_poly)
    if g_rho.degree() > 0:
        cur = s.quo(cur, g_rho)
        print('E3_CHART_ZERO_FACTOR', label, g_rho.as_expr(), flush=True)
    for dens in (s.Poly(Dp, rho), s.Poly(Qpoly, rho), s.Poly(5 * rho + 1, rho), s.Poly(Dsig, rho)):
        g = s.gcd(cur, dens)
        if g.degree() > 0:
            print('E3_POLE_FACTOR', label, g.as_expr(), flush=True)
            cur = s.quo(cur, g)
    reduced.append(cur)
check('E3_REDUCED_ROW0_ROW8_COPRIME', s.gcd(reduced[0], reduced[1]).degree() == 0)
check('E3_REDUCED_ROW0_ROW12_COPRIME', s.gcd(reduced[0], reduced[2]).degree() == 0)
print('E3_LINEAR_KA_NO_GO', 'rows 0 and 8 have no common zero and Ka does not move them', flush=True)

specs = list(o.SELECTED_SPECS)
def X_of(c):
    Xs = [f.mz(4) for _ in range(4)]
    for k, (_, role, g) in enumerate(specs):
        if c[k] == 0:
            continue
        Xs[role] = f.madd(Xs[role], f.mscale(K.from_expr(s.Integer(int(c[k]))), f.mc(g)))
    return Xs
def resp_c(c):
    print('RESP_C', c, flush=True)
    return resp(X_of(c))
def add_r(A, B):
    return [[[a + b for a, b in zip(x, y)] for x, y in zip(ra, rb)] for ra, rb in zip(A, B)]
def sub_r(A, B):
    return [[[a - b for a, b in zip(x, y)] for x, y in zip(ra, rb)] for ra, rb in zip(A, B)]
def scale_r(s0, A):
    return [[[s0 * a for a in x] for x in row] for row in A]
dirs = (
    (1, 0, 0, 0, 0, 0, 0),
    (0, 1, 0, 0, 0, 0, 0),
    (0, 0, 0, 1, 1, 0, 0),
    (0, 0, -1, 0, 0, 0, 1),
)
cached = {}
def get(c):
    key = tuple(c)
    if key not in cached:
        cached[key] = resp_c(key)
    return cached[key]
half = K.from_expr(s.Rational(1, 2))
def second(c):
    return scale_r(half, add_r(sub_r(get(tuple(2 * x for x in c)), scale_r(K.from_expr(s.Integer(2)), get(c))), R0))
def cross(c, d):
    both = tuple(a + b for a, b in zip(c, d))
    return scale_r(half, add_r(sub_r(sub_r(get(both), get(c)), get(d)), R0))
def quad_hits(M, name):
    hits = []
    for row_i in range(16):
        for ch in range(4):
            for beta in range(5):
                if M[row_i][ch][beta] != zz:
                    hits.append((row_i, ch, beta, M[row_i][ch][beta]))
    if not hits:
        check(name, True)
    else:
        print('QUAD_HITS', name, [(a, b, c, d.as_expr()) for a, b, c, d in hits], flush=True)
    return hits
squares = [quad_hits(second(d), f'KA_DIRECTION_{i}_SQUARE_ZERO') for i, d in enumerate(dirs)]
crosses = []
for i in range(4):
    for j in range(i + 1, 4):
        crosses.append(quad_hits(cross(dirs[i], dirs[j]), f'KA_CROSS_{i}_{j}_ZERO'))
# The only quadratic piece is the square of Ka direction 3. Weight it on the
# e3 chart and compare with the frozen linear rows.
M3 = second(dirs[3])
def weighted_quad(row_i):
    acc = 0
    for ch in range(4):
        mix = z * M3[row_i][ch][0].as_expr() + r * M3[row_i][ch][1].as_expr() + M3[row_i][ch][2].as_expr() + sig_e3 * M3[row_i][ch][3].as_expr()
        acc += coef[ch] * mix
    return s.together(s.simplify(acc.subs(sub).subs(chart)))
W = [weighted_quad(i) for i in range(16)]
check('E3_QUADRATIC_DOES_NOT_TOUCH_ROW0', s.simplify(W[0]) == 0)
check('E3_WEIGHTED_QUADRATIC_ROW8_ZERO', s.simplify(W[8]) == 0)
check('E3_WEIGHTED_QUADRATIC_ROW12_ZERO', s.simplify(W[12]) == 0)
# A common zero of row 0 and a y3^2-cancellation of rows 8 and 12 would need
# inhom8*W12 - inhom12*W8 = 0 on the row-0 numerator.
compat = s.together(inhom[8] * W[12] - inhom[12] * W[8])
num_c, _den_c = s.fraction(s.together(compat))
num_c = s.Poly(s.expand(num_c), rho)
row0_factor = s.quo(N0, s.gcd(N0, s.Poly(rho, rho)))
g_compat = s.gcd(num_c, row0_factor)
print('E3_QUADRATIC_COMPAT_GCD_WITH_ROW0', g_compat.as_expr(), flush=True)
check('E3_ROW0_ROOTS_DO_NOT_CANCEL_ROWS_8_AND_12', g_compat.degree() == 0 or s.simplify(W[8]) == 0)
amp_chart = [s.together(s.simplify(amp[i].subs(chart))) for i in range(7)]
print('AMP_CHART', amp_chart, flush=True)
def X_of_expr(c):
    Xs = [f.mz(4) for _ in range(4)]
    for k, (_, role, g) in enumerate(specs):
        ck = s.together(s.simplify(c[k]))
        if ck == 0:
            continue
        Xs[role] = f.madd(Xs[role], f.mscale(K.from_expr(ck), f.mc(g)))
    return Xs
print('RESP_PARTICULAR', flush=True)
Rp = resp(X_of_expr(amp_chart))
# Quadratic self-energy of the particular amplitude: resp(part)-resp(0)-linear(part).
# linear(part) on raw slots is the sum of amp_k * cols[k].
def raw_linear(row_i, ch, beta):
    acc = zz
    for k in range(7):
        if amp_chart[k] == 0:
            continue
        acc += K.from_expr(amp_chart[k]) * cols[k][row_i][ch][beta]
    return acc
def weight_block(block, row_i):
    acc = 0
    for ch in range(4):
        mix = z * block[row_i][ch][0].as_expr() + r * block[row_i][ch][1].as_expr() + block[row_i][ch][2].as_expr() + sig_e3 * block[row_i][ch][3].as_expr()
        acc += coef[ch] * mix
    return s.together(s.simplify(acc.subs(sub).subs(chart)))
self_block = [[[Rp[row_i][ch][beta] - R0[row_i][ch][beta] - raw_linear(row_i, ch, beta) for beta in range(5)] for ch in range(4)] for row_i in range(16)]
for row_i in (0, 8, 12):
    check(f'PART_SELF_WEIGHTED_ROW_{row_i}_ZERO', s.simplify(weight_block(self_block, row_i)) == 0)
for i, d in enumerate(dirs):
    mixed = [amp_chart[k] + d[k] for k in range(7)]
    print('RESP_PART_PLUS', i, flush=True)
    Rm = resp(X_of_expr(mixed))
    Rv = get(d)
    cross_block = [[[Rm[row_i][ch][beta] - Rp[row_i][ch][beta] - Rv[row_i][ch][beta] + R0[row_i][ch][beta] for beta in range(5)] for ch in range(4)] for row_i in range(16)]
    for row_i in (0, 8, 12):
        check(f'PART_CROSS_{i}_WEIGHTED_ROW_{row_i}_ZERO', s.simplify(weight_block(cross_block, row_i)) == 0)
print('SECONDS', monotonic() - st, flush=True)
raise SystemExit(0)
""", 1)
exec(compile(src, str(CERT), "exec"), {"__name__": "__main__", "__file__": str(CERT)})
