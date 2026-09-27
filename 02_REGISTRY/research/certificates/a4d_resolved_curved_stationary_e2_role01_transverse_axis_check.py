#!/usr/bin/env python3
"""Scoped opening for one e2 or e3 component on role 0 or role 1.

After memo section 9.23, collinear mode-1100 translations are excluded.
This file adds one component, b0.e2, b0.e3, b1.e2, or b1.e3, in that same
mode. Those four columns are invisible to the five leading link responses
and to affine rows 10, 11, 14 and 15, so r=-1, z=-4 and q(u-2)=rho/512
survive, and rows 1, 2 and 3 have an explicit rational solution. Role 1's
affine column is the negative of role 0's. Rows 0 and 8 are not cleared.
Second-amplitude quotient directions are not tested: an order-1 K1 shift
is not a column of that quotient. Link order three and the full Euler stay
open. e1 on roles 1, 2 and 3, and e2/e3 on roles 2 and 3, are not classified.
Role 0's e1 component is only a boundary check that the axis cut is nonempty.
"""
from __future__ import annotations

import ast
import types
from itertools import permutations
from pathlib import Path
from time import monotonic

import sympy as s
from sympy import QQ
from sympy.polys.fields import field

st = monotonic()
here = Path(__file__).resolve().parent

def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)

path = here / "a4d_resolved_curved_stationary_e2_conformal_solder_order3_check.py"
tree = ast.parse(path.read_text())
prefix = []
for node in tree.body:
    if isinstance(node, ast.Assign) and any(
        isinstance(x, ast.Name) and x.id == "ss" for x in node.targets
    ):
        break
    prefix.append(node)
rho, lam = s.symbols("rho lam")
ns = {"__file__": str(path), "__name__": "owned_generic_solder_jet", "rho": rho}
source = ast.unparse(ast.Module(body=prefix, type_ignores=[])).replace(
    "-4 * o.K1", "-4 * rho * o.K1"
)
exec(compile(source, str(path), "exec"), ns)
o = ns["o"]
K, _rf, _uf, _tf = field("rho,u,t", QQ)
zz, oo = K.zero, K.one
fp = here / "a4d_resolved_curved_stationary_e2_support7_finite_solder_check.py"
ft = ast.parse(fp.read_text())
funcs = [
    n
    for n in ft.body
    if isinstance(n, ast.FunctionDef)
    and n.name in ("mc", "mz", "madd", "mscale", "mmul", "mt", "minv", "md")
]
fns = {"K": K, "zero": zz, "one": oo, "permutations": permutations}
exec(compile(ast.Module(body=funcs, type_ignores=[]), str(fp), "exec"), fns)
f = types.SimpleNamespace(**{n.name: fns[n.name] for n in funcs})
u, t = s.symbols("u t")
base_v = [f.mc(m) for m in [-4 * rho * o.K1 + t * o.N3, t * o.N3, u * o.K1 - o.N2, o.N3]]
base = [f.mc(x) for x in o.generators0]
I = f.mc(s.eye(4))
Z = f.mz(4)
signs = (-1, -1, 1, 1)
B = []
for role in range(4):
    b = f.mz(4, 16)
    for i in range(4):
        b[i][4 * role + i] = oo
    B.append(b)
half = K.from_expr(s.Rational(1, 2))
AXES = ("e0", "e1", "e2", "e3")
E2E3 = [4 * role + axis for role in range(4) for axis in (2, 3)]
E1 = [4 * role + 1 for role in range(4)]

def ja(a, b):
    return [f.madd(x, y) for x, y in zip(a, b)]

def jn(a):
    return [f.mscale(-oo, x) for x in a]

def jm(a, b):
    out = []
    for k in range(4):
        m = f.mz(len(a[0]), len(b[0][0]))
        for i in range(k + 1):
            m = f.madd(m, f.mmul(a[i], b[k - i]))
        out.append(m)
    return out

def ji(a):
    out = [f.minv(a[0])]
    for k in range(1, 4):
        m = f.mz(len(a[0]))
        for i in range(1, k + 1):
            m = f.madd(m, f.mmul(a[i], out[k - i]))
        out.append(f.mscale(-oo, f.mmul(out[0], m)))
    return out

def jc(m):
    return [m, f.mz(len(m), len(m[0])), f.mz(len(m), len(m[0])), f.mz(len(m), len(m[0]))]

def sm(a, b):
    return [sum((a[i] * b[k - i] for i in range(k + 1)), zz) for k in range(4)]

def jd(a):
    out = [zz] * 4
    n = len(a[0])
    for p in permutations(range(n)):
        z = [oo, zz, zz, zz]
        for i, c in enumerate(p):
            z = sm(z, [a[k][i][c] for k in range(4)])
        sign = -1 if sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n)) % 2 else 1
        out = [x + sign * y for x, y in zip(out, z)]
    return out

def jad(a):
    out = [f.mz(4) for _ in range(4)]
    for i in range(4):
        for j in range(4):
            val = jd([[[M[r][c] for c in range(4) if c != i] for r in range(4) if r != j] for M in a])
            for k in range(4):
                out[k][i][j] = (-1) ** (i + j) * val[k]
    return out

def sum_m(ms):
    m = f.mz(len(ms[0]), len(ms[0][0]))
    for x in ms:
        m = f.madd(m, x)
    return m

def sM(a, b):
    return [sum_m([f.mscale(a[i], b[k - i]) for i in range(k + 1)]) for k in range(4)]

def maps(h):
    X = [Z] * 4
    U = [
        jm(
            [f.madd(I, f.mscale(half, a)), f.mscale(half, hh), f.mscale(half, x), Z],
            ji([f.madd(I, f.mscale(-half, a)), f.mscale(-half, hh), f.mscale(-half, x), Z]),
        )
        for a, hh, x in zip(base, h, X)
    ]
    Ui = [ji(x) for x in U]
    F = {}
    T = {}
    for r, ss in o.PAIRS:
        P = jm(jm(jm(U[r], U[ss]), Ui[r]), Ui[ss])
        M = ja(jc(I), jn(P))
        F[r, ss] = (P, M, jd(M), jad(M))
        aa = ja(jc(B[r]), jm(U[r], jc(f.mscale(K.from_expr(signs[r]), B[ss]))))
        bb = ja(jc(B[ss]), jm(U[ss], jc(f.mscale(K.from_expr(signs[ss]), B[r]))))
        T[r, ss] = ja(aa, jn(jm(P, bb)))
    Rall = {}
    for ff in o.PAIRS:
        for gg in o.PAIRS:
            if ff == gg:
                continue
            _P, _M, D, A = F[ff]
            Rall[ff, gg] = ja(sM(D, T[gg]), jn(jm(jm(F[gg][1], A), T[ff])))
    return Rall

def q2(h):
    R = maps(h)
    out = [f.mz(16) for _ in range(4)]
    for (ff, gg), V in R.items():
        cls = 0 if len(set(ff) & set(gg)) == 1 else 1
        for kind, metric in enumerate(((1, -1, -1, -1), (1, 1, 1, 1))):
            ch = 2 * kind + cls
            for i in range(16):
                for j in (2, 3, 6, 7):
                    out[ch][i][j] += 16 * sum(
                        (metric[a] * V[1][a][i] * V[1][a][j] for a in range(4)),
                        zz,
                    )
                    out[ch][j][i] += 16 * sum(
                        (metric[a] * V[1][a][j] * V[1][a][i] for a in range(4)),
                        zz,
                    )
    return out

def q3(h):
    R = maps(h)
    out = [f.mz(16) for _ in range(4)]
    for (ff, gg), V in R.items():
        cls = 0 if len(set(ff) & set(gg)) == 1 else 1
        assert V[0] == f.mz(4, 16)
        for kind, metric in enumerate(((1, -1, -1, -1), (1, 1, 1, 1))):
            ch = 2 * kind + cls
            for i in range(16):
                for j in range(16):
                    out[ch][i][j] += 16 * sum(
                        (
                            metric[a]
                            * (V[1][a][i] * V[2][a][j] + V[2][a][i] * V[1][a][j])
                            for a in range(4)
                        ),
                        zz,
                    )
    return out

def el4(h):
    R = maps(h)
    out = [f.mz(16) for _ in range(4)]
    for (ff, gg), V in R.items():
        cls = 0 if len(set(ff) & set(gg)) == 1 else 1
        for kind, metric in enumerate(((1, -1, -1, -1), (1, 1, 1, 1))):
            ch = 2 * kind + cls
            for row in range(16):
                for col in range(16):
                    acc = zz
                    for i in (1, 2, 3):
                        for a in range(4):
                            acc += metric[a] * V[i][a][row] * V[4 - i][a][col]
                    out[ch][row][col] += 32 * acc
    return out

def copy_h(h):
    return [[row[:] for row in M] for M in h]

def add_gen(h, role, gen, scale):
    out = copy_h(h)
    out[role] = f.madd(out[role], f.mscale(scale, f.mc(gen)))
    return out

def only_gen(role, gen):
    out = [f.mz(4) for _ in range(4)]
    out[role] = f.mc(gen)
    return out

def sub_mat(a, b):
    return [[a[i][j] - b[i][j] for j in range(16)] for i in range(16)]

def scale_mat(s0, a):
    return [[s0 * a[i][j] for j in range(16)] for i in range(16)]

def ax_name(idx):
    return f"b{idx // 4}.{AXES[idx % 4]}"

print("SETUP", round(monotonic() - st, 2), flush=True)
E = el4(base_v)
print("EL4_READY", round(monotonic() - st, 2), flush=True)
r, p, q, z = s.symbols("r p q z")
Gamma = -rho / (512 * (r * r + 1))
coef = (Gamma / 2 + p, Gamma / 2 - p, q, -q)

def entry(row, col):
    return sum((coef[ch] * E[ch][row][col].as_expr() for ch in range(4)), s.Integer(0))

def sym_entry(row, col):
    return s.together(s.simplify(entry(row, col)))

check("COLLINEAR_ROW_SUM_MATCHES_SECTION_9_23", s.simplify(
    sym_entry(10, 0) * z + sym_entry(10, 8) * r + sym_entry(10, 12)
    + sym_entry(15, 0) * z + sym_entry(15, 8) * r + sym_entry(15, 12)
    + 128 * rho * (r + 1) / (r * r + 1)
) == 0)
for col, other in ((2, 6), (3, 7)):
    for row in range(16):
        if s.simplify(entry(row, col) + entry(row, other)) != 0:
            raise AssertionError(f"role1 is not the negative of role0 at {row},{col}")
check("ROLE1_TRANSVERSE_COLUMNS_ARE_ROLE0_NEGATIVES", True)
for col in (2, 3, 6, 7):
    for row in (10, 11, 14, 15):
        if entry(row, col) != 0:
            raise AssertionError(f"row {row} sees {ax_name(col)}")
check("ROWS_10_11_14_15_IGNORE_ROLE01_E2_E3", True)
Q2 = q2(base_v)
for ch in range(4):
    for i in range(16):
        for j in (2, 3, 6, 7):
            if Q2[ch][i][j] != zz or Q2[ch][j][i] != zz:
                raise AssertionError(f"Q2 sees {j} at {i} ch {ch}")
check("LEADING_Q2_IGNORES_ROLE01_E2_E3", True)

den = 5 * t * t - 78 * t + 8
N1 = 8 * rho * t * t - 132 * rho * t + 104 * rho - t * t - 54 * t - 16
N2f = (t - 2) * (t + 5 * rho - 1)
N3 = 5 * t * t - 6 * rho * t - 96 * t + 12 * rho + 44
u_red = -(5 * t * t - 90 * t + 32) / (6 * (t - 2))
q_red = s.together(rho / (512 * (u_red - 2)))
src = {
    1: s.together(64 * rho * N1 / den),
    2: s.together(384 * rho * N2f / den),
    3: s.together(-64 * rho * N3 / den),
}
Qpoly = 200 * rho**3 + 555 * rho**2 + 260 * rho - 71
Dsig = 125 * rho**2 + 430 * rho - 47
Dp = 25 * rho**2 + 68 * rho - 13
sig_e3 = s.together(4 * Qpoly / Dsig)
p_e3 = s.together(
    rho * (50000 * rho**5 + 303375 * rho**4 + 438050 * rho**3 + 1620 * rho**2 - 45938 * rho + 3613)
    / (20480 * Dp * Qpoly)
)
t_e3 = 1 - 5 * rho
sub_e3 = {
    r: -1,
    t: t_e3,
    u: s.together(u_red.subs(t, t_e3)),
    q: s.together(q_red.subs(t, t_e3)),
    p: p_e3,
}
for row in (1, 2, 3):
    total = s.together(src[row].subs(t, t_e3) + sig_e3 * entry(row, 3).subs(sub_e3))
    check(f"E3_ROW_{row}_CLEARED_BY_EXPLICIT_P_AND_SIGMA", s.simplify(total) == 0)
check("E3_SIGMA_NUMERATOR_IS_THE_SECTION_9_23_POLYNOMIAL", s.expand(s.fraction(s.together(sig_e3))[0] - 4 * Qpoly) == 0)
check("E3_SIGMA_DENOMINATOR_COPIME_TO_Q", s.gcd(s.Poly(Qpoly, rho), s.Poly(Dsig, rho)).degree() == 0)
# sigma=0 returns to the dead collinear point. Q=0 is not a root of this chart.
check("E3_SIGMA_VANISHES_ONLY_ON_Q", s.expand(s.fraction(s.together(sig_e3))[0] - 4 * Qpoly) == 0)

sig_e2 = s.together(-2 * N1 / (3 * (t - 2) * (t - 1)))
p_e2 = s.together(
    rho * (
        40 * rho * t**4 - 1566 * rho * t**3 + 14882 * rho * t**2 - 18720 * rho * t + 6184 * rho
        - 23 * t**4 - 60 * t**3 + 5138 * t**2 - 1176 * t - 968
    ) / (2048 * den * N1)
)
sub_e2 = {r: -1, u: u_red, q: q_red, p: p_e2}
for row in (1, 2):
    total = s.together(src[row] + sig_e2 * entry(row, 2).subs(sub_e2))
    check(f"E2_ROW_{row}_CLEARED_FOR_EVERY_TANGENT", s.simplify(total) == 0)
row3_e2 = s.together(src[3] + sig_e2 * entry(3, 2).subs(sub_e2))
check("E2_ROW3_REMAINS_THE_N3_CONDITION", s.simplify(row3_e2 - src[3]) == 0)
# Rows 0 and 8 are deliberately not cleared. An order-1 shift of K1 is not
# a column of the section-9.23 second-amplitude quotient, so it is not used.

print("LINK_START", round(monotonic() - st, 2), flush=True)
tests = ((2, o.N2, "R2N2"), (2, o.N3, "R2N3"), (3, o.N2, "R3N2"), (3, o.N3, "R3N3"), (0, o.N3, "R0N3"))
role01 = (2, 3, 6, 7)
collinear_slots = (0, 8, 12)
saw_e1 = False
for role, gen, name in tests:
    plus = q3(add_gen(base_v, role, gen, oo))
    minus = q3(add_gen(base_v, role, gen, -oo))
    pure = q3(only_gen(role, gen))
    deriv = []
    for ch in range(4):
        diff = scale_mat(K.from_expr(s.Rational(1, 2)), sub_mat(plus[ch], minus[ch]))
        deriv.append(sub_mat(diff, pure[ch]))
    for col in role01:
        for ch in range(4):
            if deriv[ch][col][col] != zz:
                raise AssertionError(f"{name} square {col} {ch}")
            for i in collinear_slots:
                if deriv[ch][i][col] + deriv[ch][col][i] != zz:
                    raise AssertionError(f"{name} cross {i} {col} {ch}")
    # Boundary: e1 of role 0 is not in this class.
    col = 1
    for ch in range(4):
        if deriv[ch][col][col] != zz or any(deriv[ch][i][col] + deriv[ch][col][i] != zz for i in collinear_slots):
            saw_e1 = True
    check(f"{name}_ROLE01_E2_E3_LINK_INVISIBLE", True)
    print(name, round(monotonic() - st, 2), flush=True)
check("E1_OF_ROLE0_CHANGES_SOME_LEADING_LINK_RESPONSE", saw_e1)
print("EXACT_SCOPED_OPENING: role 0/1 axes e2 and e3 keep the section 9.23 link reduction and clear affine rows 1-3. Rows outside that set, other transverse components, and any stationary witness stay open.", flush=True)
print("SECONDS", monotonic() - st, flush=True)
