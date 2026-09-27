#!/usr/bin/env python3
"""Direct exact identification of the A4D IR Schur symbol with linearized Einstein.

Task: WRK-A4D-SCHUR-EINSTEIN-DIRECT-IDENTIFICATION

Consumes the merged #270 finite symbol owner only up to the construction of

    K_SCHUR = - C(k)^T A0^{-1} C(k).

It deliberately stops BEFORE #270 constructs E_eta.  This checker then
independently rebuilds the standard flat linearized Einstein tensor from its
index formula in Minkowski signature and compares all 100 polynomial entries.

Terminal: J2-SCHUR-DIRECT-LINEAR-EINSTEIN-IDENTIFICATION-EXACT
"""
from __future__ import annotations

import os
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
OWNER = os.path.join(HERE, "a4d_metric_null_hessian_complex_check.py")

# Consume the exact finite owner, but cut before its E_eta construction.
_src = open(OWNER, encoding="utf-8").read()
_cut_marker = "# Exact E_eta quadratic symbol in the #201 convention."
_cut = _src.index(_cut_marker)
_ns = {"__name__": "_schur_direct_owner", "__file__": OWNER}
exec(compile(_src[:_cut], OWNER, "exec"), _ns)

# Upstream finite-symbol objects.  No E_eta/K_EETA object exists at this cut.
K = _ns["K_SCHUR"]
A0 = _ns["A0"]
C = _ns["C"]
d = _ns["d"]
ETA = _ns["ETA"]
SYM = _ns["SYM"]

FAILS = []


def check(name, cond, detail=""):
    if cond:
        print("PASS_" + name)
    else:
        FAILS.append(name)
        print("FAIL_" + name + (" :: " + detail if detail else ""))


check("OWNER_CUT_BEFORE_E_ETA", "K_EETA" not in _ns and "EETA" not in _ns)
check("A0_DET_256", sp.factor(A0.det()) == 256)
check("SCHUR_SHAPE_10", K.shape == (10, 10))

# ---------------------------------------------------------------------------
# Standard flat linearized Einstein tensor, independently reconstructed.
# ---------------------------------------------------------------------------

qvars = sp.symbols("q0:10")
H = sp.zeros(4)
for j, (a, b) in enumerate(SYM):
    H[a, b] = qvars[j]
    H[b, a] = qvars[j]

k_cov = sp.Matrix(d)
k_up = ETA * k_cov
k2 = sp.expand((k_cov.T * ETA * k_cov)[0])
tr_h = sp.expand(sum(ETA[a, a] * H[a, a] for a in range(4)))
kk_h = sp.expand((k_up.T * H * k_up)[0])

G_lower = sp.zeros(4)
for mu in range(4):
    for nu in range(4):
        k_h_nu = sum(k_up[r] * H[nu, r] for r in range(4))
        k_h_mu = sum(k_up[r] * H[mu, r] for r in range(4))
        G_lower[mu, nu] = sp.expand(sp.Rational(1, 2) * (
            k_cov[mu] * k_h_nu
            + k_cov[nu] * k_h_mu
            - k2 * H[mu, nu]
            - k_cov[mu] * k_cov[nu] * tr_h
            - ETA[mu, nu] * (kk_h - k2 * tr_h)
        ))

# Raise the output tensor because the repository metric Euler coordinates pair
# with covariant q_{mu nu}.  Off-diagonal symmetric coordinate variations
# occur twice in sum_{mu,nu} G^{mu nu} delta q_{mu nu}.
G_up = sp.expand(ETA * G_lower * ETA)
G_coord = sp.zeros(10, 1)
for i, (a, b) in enumerate(SYM):
    G_coord[i] = sp.expand((1 if a == b else 2) * G_up[a, b])

K_G = sp.Matrix([
    [sp.diff(G_coord[i], qvars[j]) for j in range(10)]
    for i in range(10)
])

check("STANDARD_EINSTEIN_LINEAR_IN_H",
      all(sp.Poly(x, *qvars).total_degree() <= 1 for x in G_coord))
check("STANDARD_EINSTEIN_SYMBOL_SHAPE", K_G.shape == (10, 10))

# Central direct identity.  This does not use E_eta=-2G.
diff = (K + sp.Rational(1, 2) * K_G).applyfunc(sp.expand)
check("SCHUR_EQUALS_MINUS_HALF_STANDARD_EINSTEIN",
      diff == sp.zeros(10, 10))

# ---------------------------------------------------------------------------
# Hostile convention controls: the correct identity must fail if we change
# any of the three convention choices that commonly hide sign/factor errors.
# ---------------------------------------------------------------------------

# 1. Do not raise the Einstein output.
G_lower_coord = sp.zeros(10, 1)
for i, (a, b) in enumerate(SYM):
    G_lower_coord[i] = sp.expand((1 if a == b else 2) * G_lower[a, b])
K_G_lower = sp.Matrix([
    [sp.diff(G_lower_coord[i], qvars[j]) for j in range(10)]
    for i in range(10)
])
check("HOSTILE_LOWER_OUTPUT_MISMATCH",
      sp.simplify(K + sp.Rational(1, 2) * K_G_lower) != sp.zeros(10, 10))

# 2. Forget the factor two on off-diagonal symmetric output coordinates.
G_no2 = sp.Matrix([sp.expand(G_up[a, b]) for a, b in SYM])
K_G_no2 = sp.Matrix([
    [sp.diff(G_no2[i], qvars[j]) for j in range(10)]
    for i in range(10)
])
check("HOSTILE_NO_OFFDIAGONAL_FACTOR_MISMATCH",
      sp.simplify(K + sp.Rational(1, 2) * K_G_no2) != sp.zeros(10, 10))

# 3. Reverse the Schur sign.
check("HOSTILE_SCHUR_SIGN_MISMATCH",
      sp.simplify(K - sp.Rational(1, 2) * K_G) != sp.zeros(10, 10))

# ---------------------------------------------------------------------------
# Bianchi identity, gauge kernel, and characteristic rank.
# ---------------------------------------------------------------------------

# Direct tensor Bianchi identity k_mu G^{mu nu}=0 for every symmetric input.
for nu in range(4):
    bianchi = sp.expand(sum(k_cov[mu] * G_up[mu, nu] for mu in range(4)))
    check("BIANCHI_NU_%d" % nu, bianchi == 0)

# Leading vector/coframe metric image:
# h_{mu nu}=k_mu xi_nu + k_nu xi_mu after the repository's eta conversion.
F = sp.zeros(10, 4)
for col in range(4):
    xi = sp.eye(4)[:, col]
    Hraw = sp.Matrix(d) * xi.T
    qmat = sp.expand(Hraw * ETA + ETA * Hraw.T)
    for i, (a, b) in enumerate(SYM):
        F[i, col] = qmat[a, b]

check("GENERIC_COFRAME_IMAGE_RANK_4", F.rank() == 4)
check("SCHUR_KILLS_COFRAME_IMAGE", sp.expand(K * F) == sp.zeros(10, 4))
check("GENERIC_SCHUR_RANK_6", K.rank() == 6)
# In a ten-dimensional metric carrier, rank(K)=6 gives nullity 4, hence the
# contained rank-4 coframe image is exactly the generic kernel.
check("GENERIC_KERNEL_EQUALS_COFRAME_BY_DIMENSION",
      K.rank() + F.rank() == 10 and sp.expand(K * F) == sp.zeros(10, 4))

for tag, kval, expected in (
    ("TIMELIKE", (1, 0, 0, 0), 6),
    ("SPACELIKE", (0, 1, 0, 0), 6),
    ("GENERIC", (1, 2, 3, 4), 6),
    ("NULL", (1, 1, 0, 0), 4),
):
    sub = {d[j]: kval[j] for j in range(4)}
    check("SCHUR_RANK_" + tag, K.subs(sub).rank() == expected)
    check("STANDARD_EINSTEIN_RANK_" + tag, K_G.subs(sub).rank() == expected)

if FAILS:
    print("J2-SCHUR-DIRECT-LINEAR-EINSTEIN-IDENTIFICATION: FAIL (%d)" % len(FAILS))
    for f in FAILS:
        print("  - " + f)
    raise SystemExit(1)

print("J2-SCHUR-DIRECT-LINEAR-EINSTEIN-IDENTIFICATION-EXACT")
print("DIRECT_IDENTITY: K_SCHUR = -1/2 K_G^(1) coefficient-by-coefficient.")
print("INDEPENDENCE: the comparison is cut before the #270 E_eta construction.")
print("BIANCHI: k_mu G^{mu nu}=0 identically in all four output columns.")
print("GAUGE_KERNEL: generic rank 6; the rank-4 leading coframe image is exactly the generic kernel.")
print("CHARACTERISTIC: rank 6 on timelike/spacelike/generic controls and rank 4 on k=(1,1,0,0).")
print("HOSTILE_CONTROLS: wrong index position, off-diagonal factor, and Schur sign all fail.")
print("SCOPE: flat linear exact symbol cross-check only; no nonlinear continuum Einstein theorem.")
