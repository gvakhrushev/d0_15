#!/usr/bin/env python3
"""Exact metric-null Hessian/Koszul complex certificate.

Task: WRK-A4D-METRIC-NULL-HESSIAN-COMPLEX

Rebuilds the accepted polarized metric-response symbol C(z)=H_AQ(z),
rewrites it in the backward character difference d_r=z_r^{-1}-1, and
certifies that it has the same constant row module as the universal map

    W_d(q)_{ab|c} = d_a q_{bc} - d_b q_{ac}

from Sym^2(Role) to Lambda^2(Role) x Role.

Consequences:
  * for every d != 0, ker C(d) = span{d d^T}, hence rank C(d)=9;
  * the conjugate-paired real metric-only block is two-dimensional;
  * character detuning transports this null line:
        (D_j C) q = - C(D_j q);
    the fixed-q FUGU detune vector is therefore in im C identically;
  * on the nine owned L=4 singular orbit representatives, the null line
    lies in the forward-coframe metric image exactly on orbits 0 and 4;
  * for z_r=exp(i h k_r), backward and forward rank-one metric shadows
    agree through h^2 and differ first at O(h^3).

No nonlinear decoupling, diffeomorphism-gauge theorem, E_eta/E_sp
identification, or continuum Einstein claim is made.

Terminal: J2-METRIC-NULL-HESSIAN-COMPLEX-EXACT
"""
from __future__ import annotations

import os
import sys
import sympy as sp

FAILS = []


def check(name, cond, detail=""):
    if cond:
        print("PASS_" + name)
    else:
        FAILS.append(name)
        print("FAIL_" + name + (" :: " + detail if detail else ""))


HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# Reuse only the accepted symbol-construction section of the exact L=4 census.
src_path = os.path.join(HERE, "a4d_joint_resonance_linear_kernel_check.py")
_src = open(src_path, encoding="utf-8").read()
_cut = _src.index("# ---------------------------------------------------------------------------\n# 2. Reproduce")
_ns = {"__name__": "_metric_null_owner", "__file__": src_path}
exec(compile(_src[:_cut], src_path, "exec"), _ns)

HAQ = _ns["HAQ"]                 # 24 x 10, connection x metric
z = _ns["z"]
SYM = _ns["SYM"]
ETA = _ns["ETA"]
ROOT_E = [sp.Integer(1), sp.I, sp.Integer(-1), -sp.I]
EXPECTED_IDS = [
    (0, 0, 1, 1), (0, 0, 1, 3), (0, 1, 1, 2),
    (1, 0, 1, 2), (1, 1, 1, 1), (1, 1, 3, 3),
    (2, 0, 1, 1), (2, 1, 1, 2), (2, 1, 2, 3),
]

check("ACCEPTED_SHAPE", HAQ.shape == (24, 10))

# ---------------------------------------------------------------------------
# 1. Rewrite the accepted symbol in d_r = z_r^{-1} - 1.
# ---------------------------------------------------------------------------

d = sp.symbols("d0:4")
z_of_d = {z[r]: 1 / (1 + d[r]) for r in range(4)}
Cd = HAQ.subs(z_of_d).applyfunc(sp.cancel).applyfunc(sp.expand)

check("C_IS_LINEAR_IN_D",
      all(sp.Poly(Cd[i, j], *d).total_degree() <= 1
          for i in range(Cd.rows) for j in range(Cd.cols)))
check("C_AT_D_ZERO_IS_ZERO", Cd.subs({x: 0 for x in d}) == sp.zeros(24, 10))

# ---------------------------------------------------------------------------
# 2. Universal Koszul/symmetric-column wedge operator W_d.
# ---------------------------------------------------------------------------

PAIRS = [(a, b) for a in range(4) for b in range(a + 1, 4)]
SINDEX = {p: i for i, p in enumerate(SYM)}


def sidx(a, b):
    return SINDEX[(a, b) if a <= b else (b, a)]


Wd = sp.zeros(24, 10)
row = 0
for a, b in PAIRS:
    for c in range(4):
        Wd[row, sidx(b, c)] += d[a]
        Wd[row, sidx(a, c)] -= d[b]
        row += 1


def coefficient_row(M, i):
    return sp.Matrix([
        sp.expand(M[i, j]).coeff(d[k])
        for k in range(4) for j in range(10)
    ]).T


CF = sp.Matrix.vstack(*[coefficient_row(Cd, i) for i in range(24)])
WF = sp.Matrix.vstack(*[coefficient_row(Wd, i) for i in range(24)])
rC = CF.rank()
rW = WF.rank()
rJoin = sp.Matrix.vstack(CF, WF).rank()

check("COEFFICIENT_ROW_RANK_C_20", rC == 20, str(rC))
check("COEFFICIENT_ROW_RANK_W_20", rW == 20, str(rW))
check("CONSTANT_ROW_MODULES_EQUAL", rJoin == rC == rW,
      f"rC={rC} rW={rW} joined={rJoin}")

# Equality of the coefficient-row spans means there exist constant rational
# row operations in both directions C(d) <-> W(d), for every d. Hence their
# kernels agree pointwise.

qnull = sp.Matrix([d[a] * d[b] for a, b in SYM])
check("C_DD_ZERO_IDENTICALLY",
      all(sp.expand(x) == 0 for x in Cd * qnull))
check("W_DD_ZERO_IDENTICALLY",
      all(sp.expand(x) == 0 for x in Wd * qnull))

# Patch proof of the full kernel theorem. Let x=(x_ab) be a symbolic
# symmetric metric. For any j with d_j != 0, W_d x=0 implies
#
#   d_j^2 x_ac - d_a d_c x_jj
#     = d_j (d_j x_ac - d_a x_jc)
#       + d_a (d_j x_jc - d_c x_jj) = 0.
#
# The identities below certify this reconstruction algebraically for all
# j,a,c. Division by d_j is used only in the prose theorem on that patch.
xv = sp.symbols("x0:10")


def x(a, b):
    return xv[sidx(a, b)]


def wedge_eq(a, b, c):
    return sp.expand(d[a] * x(b, c) - d[b] * x(a, c))


for j in range(4):
    for a in range(4):
        for c in range(4):
            lhs = sp.expand(d[j] ** 2 * x(a, c)
                            - d[a] * d[c] * x(j, j))
            rhs = sp.expand(
                d[j] * wedge_eq(j, a, c)
                + d[a] * wedge_eq(j, c, j)
            )
            check(f"PATCH_RECON_{j}_{a}_{c}", sp.expand(lhs - rhs) == 0)

# ---------------------------------------------------------------------------
# 3. Exact transport under character detuning.
# ---------------------------------------------------------------------------

qz = sp.Matrix([
    (1 / z[a] - 1) * (1 / z[b] - 1) for a, b in SYM
])
check("ACCEPTED_C_Q_ZERO",
      all(sp.cancel(x) == 0 for x in HAQ * qz))

for j in range(4):
    DjC = HAQ.diff(z[j]) * z[j]
    Djq = qz.diff(z[j]) * z[j]
    transport = (DjC * qz + HAQ * Djq).applyfunc(sp.cancel)
    check(f"DETUNE_TRANSPORT_{j}",
          all(x == 0 for x in transport))

# ---------------------------------------------------------------------------
# 4. L=4 hostile controls and the forward-coframe metric shadow.
# ---------------------------------------------------------------------------


def forward_metric_map(zeta):
    """10 x 4 map xi -> q from the flat forward-coframe tangent.

    H_raw[r,a]=(z_r-1) xi_a and q=H_raw eta + eta H_raw^T.
    """
    F = sp.zeros(10, 4)
    for col in range(4):
        xi = sp.eye(4)[:, col]
        Hraw = sp.zeros(4)
        for r in range(4):
            for a in range(4):
                Hraw[r, a] = (zeta[r] - 1) * xi[a]
        qm = sp.expand(Hraw * ETA + ETA * Hraw.T)
        for m, (a, b) in enumerate(SYM):
            F[m, col] = qm[a, b]
    return F


aligned = []
for n, ids in enumerate(EXPECTED_IDS):
    zeta = [ROOT_E[i] for i in ids]
    sub = {z[r]: zeta[r] for r in range(4)}
    Cz = HAQ.subs(sub)
    qv = qz.subs(sub)
    rankC = Cz.rank()
    check(f"ORBIT_{n}_RANK_C_9", rankC == 9, str(rankC))
    check(f"ORBIT_{n}_NULL_GENERATOR", Cz * qv == sp.zeros(24, 1))

    F = forward_metric_map(zeta)
    in_forward = F.row_join(qv).rank() == F.rank()
    if in_forward:
        aligned.append(n)

    for j in range(4):
        w = (HAQ.diff(z[j]) * z[j] * qz).subs(sub)
        dq = (qz.diff(z[j]) * z[j]).subs(sub)
        check(f"ORBIT_{n}_DETUNE_{j}_IN_IM_C",
              w == -Cz * dq)

check("AFFINE_METRIC_ALIGNMENT_ONLY_ORBITS_0_4",
      aligned == [0, 4], str(aligned))

# ---------------------------------------------------------------------------
# 5. Smooth-character expansion: backward vs forward scalar rank-one shadow.
# ---------------------------------------------------------------------------

h = sp.symbols("h", real=True)
k = sp.symbols("k0:4", real=True)
aa = [
    sp.I * h * k[r]
    - sp.Rational(1, 2) * h**2 * k[r]**2
    - sp.I * sp.Rational(1, 6) * h**3 * k[r]**3
    for r in range(4)
]
dd = [
    -sp.I * h * k[r]
    - sp.Rational(1, 2) * h**2 * k[r]**2
    + sp.I * sp.Rational(1, 6) * h**3 * k[r]**3
    for r in range(4)
]
for a, b in SYM:
    delta = sp.expand(dd[a] * dd[b] - aa[a] * aa[b])
    check(f"SMOOTH_H2_MATCH_{a}_{b}", delta.coeff(h, 2) == 0)
    expected_h3 = sp.I * k[a] * k[b] * (k[a] + k[b])
    check(f"SMOOTH_H3_DEFECT_{a}_{b}",
          sp.expand(delta.coeff(h, 3) - expected_h3) == 0)

if FAILS:
    print("J2-METRIC-NULL-HESSIAN-COMPLEX: FAIL (%d)" % len(FAILS))
    for f in FAILS:
        print("  - " + f)
    sys.exit(1)

print("J2-METRIC-NULL-HESSIAN-COMPLEX-EXACT")
print("ROW_MODULE: accepted C(d) and W_d have the same constant rational row module.")
print("KERNEL: for every d != 0, ker C(d)=span{d d^T}; rank C(d)=9.")
print("REALIFICATION: one complex null line gives the owned two-real-dimensional metric-only block.")
print("DETUNE: (D_j C)q=-C(D_j q) identically; the raw fixed-q FUGU detune vector is kernel transport, not a quotient obstruction.")
print("AFFINE_ALIGNMENT: among the nine owned L=4 singular orbit types, the null line is in the forward-coframe metric image exactly on orbits 0 and 4.")
print("SMOOTH_LIMIT: backward and forward rank-one metric shadows agree through h^2; their first mismatch is O(h^3), hence O(h) after h^-2 normalization.")
print("SCOPE: exact finite symbol theorem only; no nonlinear response-decoupling or gauge/Einstein promotion.")
