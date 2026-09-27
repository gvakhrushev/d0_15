#!/usr/bin/env python3
"""Owned affine order four for one e2 component on role 0 or role 1.

Does not import the section 9.24 e2 closed form. The translation slots are
b0.e2 (index 2) and b1.e2 (index 6), inside the same resp as section 9.25.
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
new_beta = "for beta,inds in enumerate(((0,),(8,),(12,),(2,),(6,))):"
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
sig = s.symbols('sig')
def slot(row, raw, k):
    return s.cancel(sum((coef[ch] * raw[ch][k].as_expr() for ch in range(4)), s.Integer(0)))
for row_i in range(16):
    if s.simplify(slot(row_i, R0[row_i], 3) + slot(row_i, R0[row_i], 4)) != 0:
        raise AssertionError(f'weighted base role1 e2 row {row_i}')
    for col in cols:
        if s.simplify(slot(row_i, col[row_i], 3) + slot(row_i, col[row_i], 4)) != 0:
            raise AssertionError(f'weighted amplitude role1 e2 row {row_i}')
check('B1_E2_WEIGHTED_COLUMNS_ARE_NEGATIVES', True)
Et = s.Matrix([slot(row_i, R0[row_i], 3) for row_i in range(16)]).subs(sub).applyfunc(s.cancel)
Ct = s.Matrix([[slot(row_i, col[row_i], 3) for col in cols] for row_i in range(16)]).subs(sub).applyfunc(s.cancel)
amp = part[10:, :]
trans = (Et + Ct * amp).applyfunc(s.cancel)
for i in (1, 2, 3, 0, 8, 12):
    print('E2_SOURCE', i, s.factor(source[i]), flush=True)
    print('E2_TRANS', i, s.factor(trans[i]), flush=True)
check('E2_TRANSVERSE_ROW3_IS_ZERO', s.simplify(trans[3]) == 0)
N1 = 8 * rho * t * t - 132 * rho * t + 104 * rho - t * t - 54 * t - 16
N3 = 5 * t * t - 6 * rho * t - 96 * t + 12 * rho + 44
den = 5 * t * t - 78 * t + 8
sig_e2 = s.together(-2 * N1 / (3 * (t - 2) * (t - 1)))
p_e2 = s.together(rho * (40 * rho * t**4 - 1566 * rho * t**3 + 14882 * rho * t**2 - 18720 * rho * t + 6184 * rho - 23 * t**4 - 60 * t**3 + 5138 * t**2 - 1176 * t - 968) / (2048 * den * N1))
sol = {p: p_e2, sig: sig_e2}
for i in (1, 2):
    check(f'E2_OWNED_ROW_{i}_CLEARED', s.simplify(s.together((source[i] + sig * trans[i]).subs(sol))) == 0)
check('E2_ROW3_REMAINS_N3', s.simplify(s.together((source[3] + sig * trans[3]) * den / (-64 * rho) - N3)) == 0)
deriv = ((Cp + sig_e2 * Ct) * Ka).applyfunc(lambda e: s.together(s.simplify(e)))
check('E2_KA_DERIVATIVE_ZERO_AT_OWNED_SOLUTION', all(s.simplify(deriv[i, j]) == 0 for i in range(16) for j in range(4)))
row0 = s.together(s.simplify((source[0] + sig * trans[0]).subs(sol)))
row8 = s.together(s.simplify((source[8] + sig * trans[8]).subs(sol)))
def cleared_poly(expr):
    num, _den = s.fraction(s.together(expr))
    poly = s.Poly(s.expand(num), t)
    for fac in (s.Poly(t - 2, t), s.Poly(den, t), s.Poly(s.expand(N1), t)):
        q, r = s.div(poly, fac, domain=s.QQ.frac_field(rho))
        while r == 0 and poly.degree() >= fac.degree():
            poly = q
            q, r = s.div(poly, fac, domain=s.QQ.frac_field(rho))
    g = s.gcd(poly, s.Poly(rho, t))
    if g.degree() > 0:
        poly = s.quo(poly, g)
    return poly
P0 = cleared_poly(row0)
P8 = cleared_poly(row8)
Pn3 = s.Poly(s.expand(N3), t)
Res0 = s.Poly(s.expand(s.resultant(P0, Pn3)), rho)
Res8 = s.Poly(s.expand(s.resultant(P8, Pn3)), rho)
# strip rho after constructing the resultants
def strip_rho(poly):
    rp = s.Poly(rho, rho)
    while poly.degree() > 0 and s.gcd(poly, rp).degree() > 0:
        poly = s.quo(poly, s.gcd(poly, rp))
    return poly
Res0s, Res8s = strip_rho(Res0), strip_rho(Res8)
check('E2_N3_DOES_NOT_KILL_ROW0_AND_ROW8_TOGETHER', s.gcd(Res0s, Res8s).degree() == 0)
check('E2_T2_NOT_ON_N3', s.expand(N3.subs(t, 2)) == -128)
# At t=1 the transverse row 1 vanishes, so N3(1)=0 cannot be repaired by sigma.
check('E2_T1_TRANSVERSE_ROW1_ZERO', s.simplify(trans[1].subs(t, 1)) == 0)
check('E2_T1_SOURCE_ROW1_NONZERO_ON_N3', s.simplify(s.together(source[1].subs({t: 1, rho: s.Rational(47, 6)}))) != 0)
seam = s.resultant(s.Poly(s.expand(N1), t), s.Poly(s.expand(N3), t))
row2_seam = s.resultant(s.Poly(s.expand(N3), t), s.Poly(t + 5 * rho - 1, t))
check('E2_N1_N3_SEAM_MISSES_COLLINEAR_ROW2', s.gcd(s.Poly(s.expand(seam), rho), s.Poly(s.expand(row2_seam), rho)).degree() == 0)
check('E2_N3_MINUS_DEN_IS_CHART_FACTOR', s.expand(N3 - den - 6 * (rho + 3) * (2 - t)) == 0)
print('E2_OWNED_NO_GO', 'N3=0 is necessary and does not meet row 0 and row 8', flush=True)
specs = list(o.SELECTED_SPECS)
def X_of(c):
    Xs = [f.mz(4) for _ in range(4)]
    for k, (_, role, g) in enumerate(specs):
        if c[k] == 0:
            continue
        Xs[role] = f.madd(Xs[role], f.mscale(K.from_expr(s.Integer(int(c[k]))), f.mc(g)))
    return Xs
def add_r(A, B):
    return [[[a + b for a, b in zip(x, y)] for x, y in zip(ra, rb)] for ra, rb in zip(A, B)]
def sub_r(A, B):
    return [[[a - b for a, b in zip(x, y)] for x, y in zip(ra, rb)] for ra, rb in zip(A, B)]
def scale_r(s0, A):
    return [[[s0 * a for a in x] for x in row] for row in A]
d3 = (0, 0, -1, 0, 0, 0, 1)
print('RESP_KA3', flush=True)
f1 = resp(X_of(d3))
print('RESP_KA3_DOUBLE', flush=True)
f2 = resp(X_of(tuple(2 * x for x in d3)))
half = K.from_expr(s.Rational(1, 2))
M3 = scale_r(half, add_r(sub_r(f2, scale_r(K.from_expr(s.Integer(2)), f1)), R0))
hits = [(row_i, ch, beta, M3[row_i][ch][beta].as_expr()) for row_i in range(16) for ch in range(4) for beta in range(5) if M3[row_i][ch][beta] != zz]
print('E2_KA3_SQUARE_HITS', hits, flush=True)
# beta 3 is b0.e2. Observer channels 2 and 3 must match so q and -q cancel.
for row_i, _ch, beta, _val in hits:
    if beta == 3 or M3[row_i][2][beta] != M3[row_i][3][beta]:
        raise AssertionError(f'e2 quadratic not observer-cancelled at row {row_i} beta {beta}')
check('E2_KA3_SQUARE_IS_OBSERVER_EVEN_AND_MISSES_E2_SLOT', True)
print('SECONDS', monotonic() - st, flush=True)
raise SystemExit(0)
""", 1)
exec(compile(src, str(CERT), "exec"), {"__name__": "__main__", "__file__": str(CERT)})
