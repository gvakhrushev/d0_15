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


# ---------------------------------------------------------------------------
# 6. Full forward-coframe tangent: finite non-gauge, asymptotically joint-null.
# ---------------------------------------------------------------------------

HAB = _ns["HAB"]


def lorentz_coeffs(X):
    return sp.Matrix([
        X[0, 1], X[0, 2], X[0, 3],
        X[1, 2], X[1, 3], X[2, 3],
    ])


def coframe_to_joint_symbolic(phase):
    G = sp.zeros(34, 4)
    for col in range(4):
        xi = sp.eye(4)[:, col]
        Hraw = sp.zeros(4)
        for r in range(4):
            for a in range(4):
                Hraw[r, a] = (phase[r] - 1) * xi[a]
        qm = sp.expand(Hraw * ETA + ETA * Hraw.T)
        Hsec = sp.expand(sp.Rational(1, 2) * qm * ETA)
        Delta = sp.expand(Hraw - Hsec)
        lam = sp.expand(Delta.T)
        for m, (a, b) in enumerate(SYM):
            G[m, col] = qm[a, b]
        for r in range(4):
            Xr = sp.expand((phase[r] - 1) * lam)
            coeff = lorentz_coeffs(Xr)
            for j in range(6):
                G[10 + 6 * r + j, col] = coeff[j]
    return G


Gcof = coframe_to_joint_symbolic(z)
qcof = Gcof[:10, :]
xcof = Gcof[10:, :]
cof_top = sp.expand(HAQ.T * xcof)
cof_bottom = sp.expand(HAQ * qcof + HAB * xcof)

tau = sp.symbols("tau")
kap = sp.symbols("kap0:4")
near_id = {z[r]: 1 + tau * kap[r] for r in range(4)}


def valuation_tau(expr):
    ex = sp.cancel(expr.subs(near_id))
    if ex == 0:
        return sp.oo
    num, den = sp.fraction(ex)
    check("DEN_NONZERO_AT_IDENTITY_" + str(abs(hash(str(expr))) % 10**8),
          sp.simplify(den.subs(tau, 0)) != 0)
    P = sp.Poly(sp.expand(num), tau)
    return min(mon[0] for mon, coeff in P.terms() if coeff != 0)


top_vals = [valuation_tau(cof_top[i, j])
            for i in range(cof_top.rows) for j in range(cof_top.cols)]
bottom_vals = [valuation_tau(cof_bottom[i, j])
               for i in range(cof_bottom.rows) for j in range(cof_bottom.cols)]
top_finite = [v for v in top_vals if v is not sp.oo]
bottom_finite = [v for v in bottom_vals if v is not sp.oo]

check("COFRAME_METRIC_EULER_ORDER_AT_LEAST_4",
      min(top_finite) == 4 and all(v >= 4 for v in top_finite),
      str(sorted(set(top_finite))))
check("COFRAME_CONNECTION_EULER_ORDER_AT_LEAST_3",
      min(bottom_finite) == 3 and all(v >= 3 for v in bottom_finite),
      str(sorted(set(bottom_finite))))


# ---------------------------------------------------------------------------
# 7. Flat smooth Schur complement: exact linearized Einstein symbol.
# ---------------------------------------------------------------------------
#
# The joint stationarity equations are
#
#   C^T x = 0,
#   C q + A x = 0.
#
# At the trivial character A0=A(1) is invertible. Eliminating x gives the
# effective metric Euler operator -C^T A^{-1} C. Its leading nonzero symbol
# is quadratic because C is first order in the character difference.

A0 = HAB.subs({z[r]: 1 for r in range(4)})
check("TRIVIAL_CONNECTION_BLOCK_DET_256", sp.factor(A0.det()) == 256)

eps = sp.symbols("eps")
mom = sp.symbols("mom0:4")
smooth_path = {z[r]: 1 + eps * mom[r] for r in range(4)}

C1 = sp.zeros(24, 10)
for i in range(24):
    for j in range(10):
        entry = sp.cancel(HAQ[i, j].subs(smooth_path))
        C1[i, j] = sp.simplify(sp.diff(entry, eps).subs(eps, 0))

check("C1_GENERIC_RANK_9", C1.rank() == 9)
S2 = sp.simplify(C1.T * A0.inv() * C1)
check("SCHUR_LEADING_SYMMETRIC", S2 == S2.T)
check("SCHUR_LEADING_RANK_6", S2.rank() == 6)

# Leading forward-coframe metric image.  For a fixed xi,
# H_raw = eps * mom * xi^T and q = H_raw eta + eta H_raw^T.
F1 = sp.zeros(10, 4)
for col in range(4):
    xi = sp.eye(4)[:, col]
    Hraw1 = sp.zeros(4)
    for r in range(4):
        for a in range(4):
            Hraw1[r, a] = mom[r] * xi[a]
    q1 = sp.expand(Hraw1 * ETA + ETA * Hraw1.T)
    for m, (a, b) in enumerate(SYM):
        F1[m, col] = q1[a, b]

check("LEADING_COFRAME_METRIC_RANK_4", F1.rank() == 4)
check("SCHUR_KILLS_FULL_LEADING_COFRAME_IMAGE",
      sp.simplify(S2 * F1) == sp.zeros(10, 4))
# rank S2=6 and rank F1=4 imply ker S2 = im F1 over the generic momentum field.

# Standard flat linearized Einstein tensor for a symmetric covariant metric
# perturbation h_{mu nu}.  mom is the covector k_mu, kup=eta^{mu nu} k_nu.
# The output is raised to G^{mu nu}, then converted to the repository's ten
# symmetric metric-coordinate Euler components: off-diagonal variations
# receive the usual factor two.

kvec = sp.Matrix(mom)
kup = ETA * kvec
k2 = (kvec.T * ETA * kvec)[0]


def metric_basis_matrix(j):
    H = sp.zeros(4)
    a, b = SYM[j]
    H[a, b] = 1
    H[b, a] = 1
    return H


def einstein_linear_lower(H):
    trH = sum(ETA[a, a] * H[a, a] for a in range(4))
    kkH = (kup.T * H * kup)[0]
    G = sp.zeros(4)
    for mu in range(4):
        for nu in range(4):
            t1 = kvec[mu] * sum(kup[r] * H[nu, r] for r in range(4))
            t2 = kvec[nu] * sum(kup[r] * H[mu, r] for r in range(4))
            G[mu, nu] = sp.Rational(1, 2) * (
                t1 + t2
                - k2 * H[mu, nu]
                - kvec[mu] * kvec[nu] * trH
                - ETA[mu, nu] * (kkH - k2 * trH)
            )
    return sp.expand(G)


Ein = sp.zeros(10, 10)
for j in range(10):
    Glow = einstein_linear_lower(metric_basis_matrix(j))
    Gup = sp.expand(ETA * Glow * ETA)
    for i, (a, b) in enumerate(SYM):
        factor = 1 if a == b else 2
        Ein[i, j] = sp.expand(factor * Gup[a, b])

check("LINEAR_EINSTEIN_SYMBOL_RANK_6", Ein.rank() == 6)
check("SCHUR_EQUALS_HALF_LINEAR_EINSTEIN",
      sp.simplify(S2 - sp.Rational(1, 2) * Ein) == sp.zeros(10, 10))

# The actual eliminated metric Euler carries the minus sign:
#   E_eff = - C^T A^{-1} C q
# so its leading term is exactly -1/2 G^(1) in this convention.

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
print("ASYMPTOTIC_COFRAME: the full forward-coframe joint residual is O(tau^4) in the metric Euler leg and O(tau^3) in the connection Euler leg near z=1.")
print("EINSTEIN_SCHUR: the leading eliminated metric operator is exactly -1/2 times the flat linearized Einstein symbol; its generic kernel is exactly the four-dimensional leading coframe image.")
print("SCOPE: exact finite symbol theorem only; no nonlinear response-decoupling or gauge/Einstein promotion.")
