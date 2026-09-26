#!/usr/bin/env python3
"""Exact flat 2-jet vanishing for quadratic joint-residual completions.

Research-only certificate. Exact rational / symbolic arithmetic over Q.

Locked statement (seed / completion split):
  R_{2|1} = det(X_1) t_2 - X_2 adj(X_1) t_1,   X_i = I - P_i.
  In dimension 4, det is homogeneous of degree 4 and adj of degree 3, so
      R_{2|1} = O(X^4 t)
  for every quadratic readout Q(R) = R^T H R with constant H,
      Q = O(X^8 t^2) multi-homogeneously.
  If the flat perturbation moreover takes t = O(eps) with X = O(eps), then
      Q = O(eps^10).
  In all cases the flat 2-jet vanishes:
      j^2_flat Q = 0,
  hence
      j^2_flat (S_star + Q) = j^2_flat S_star.

No continuum Einstein importation, no Holst/phi, no Lean/claim promotion.
Does not edit or depend on unmerged #201/#202 primary artifacts.
"""

from __future__ import annotations

import sympy as sp

ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)


def check(name: str, cond) -> None:
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)


def joint_residual(X1, t1, X2, t2):
    """R = det(X1) t2 - X2 adj(X1) t1  (X_i = I - P_i)."""
    return sp.expand(sp.det(X1) * t2 - X2 * X1.adjugate() * t1)


# Concrete rational 4x4 witnesses (generic enough: full rank, non-scalar).
A = sp.Matrix([
    [2, 1, 0, -1],
    [0, 3, 1,  2],
    [1, 0, 2, -1],
    [-1, 2, 0, 4],
])
B = sp.Matrix([
    [1, 0, 2, 1],
    [2, -1, 0, 3],
    [0, 1, 3, -2],
    [1, 2, -1, 1],
])
u = sp.Matrix([1, -2, 3, 0])
w = sp.Matrix([0, 1, -1, 2])
A2 = sp.Matrix([
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
    [1, 0, 0, 0],
])
B2 = sp.Matrix([
    [3, 1, -1, 0],
    [0, 2, 1, 1],
    [1, 0, -2, 1],
    [0, 1, 0, 2],
])

lam, mu, eps = sp.symbols("lam mu eps")

# ---------------------------------------------------------------------------
# 1. Homogeneous degree facts for 4 x 4 det / adjugate
# ---------------------------------------------------------------------------
for tag, M in (("A", A), ("B", B), ("A2", A2), ("B2", B2)):
    check(
        "DET_HOMOGENEOUS_DEGREE_4_" + tag,
        sp.expand(sp.det(lam * M) - lam**4 * sp.det(M)) == 0,
    )
    check(
        "ADJ_HOMOGENEOUS_DEGREE_3_" + tag,
        sp.expand(sp.Matrix(lam * M).adjugate() - lam**3 * M.adjugate()) == sp.zeros(4),
    )
    check(
        "CAYLEY_A_ADJ_EQ_DET_I_" + tag,
        sp.expand(M * M.adjugate() - sp.det(M) * I4) == sp.zeros(4),
    )

# ---------------------------------------------------------------------------
# 2. Multi-homogeneous order of the polynomial residual
# ---------------------------------------------------------------------------
for tag, Xa, Xb, ta, tb in (
    ("W1", A, B, u, w),
    ("W2", A2, B2, w, u),
    ("W3", A, B2, u, u),
):
    R = joint_residual(lam * Xa, mu * ta, lam * Xb, mu * tb)
    R_core = joint_residual(Xa, ta, Xb, tb)
    check(
        "RESIDUAL_MULTIHOMOGENEOUS_LAM4_MU_" + tag,
        sp.expand(R - lam**4 * mu * R_core) == sp.zeros(4, 1),
    )
    check("CORE_RESIDUAL_NONZERO_" + tag, R_core != sp.zeros(4, 1))

# ---------------------------------------------------------------------------
# 3. Quadratic readout order: Q = R^T H R
# ---------------------------------------------------------------------------
h_n = sp.eye(4)
H_mix = ETA + sp.Rational(3, 7) * h_n
H_gen = sp.Matrix([
    [2, 1, 0, -1],
    [1, 3, 2, 0],
    [0, 2, -1, 1],
    [-1, 0, 1, 4],
])
check("H_GEN_SYMMETRIC", H_gen - H_gen.T == sp.zeros(4))

for htag, H in (("ETA", ETA), ("HN", h_n), ("MIX", H_mix), ("GEN", H_gen)):
    for wtag, Xa, Xb, ta, tb in (("W1", A, B, u, w), ("W2", A2, B2, w, u)):
        R = joint_residual(lam * Xa, mu * ta, lam * Xb, mu * tb)
        R_core = joint_residual(Xa, ta, Xb, tb)
        Q = sp.expand((R.T * H * R)[0])
        Q_core = sp.expand((R_core.T * H * R_core)[0])
        check(
            "Q_MULTIHOMOGENEOUS_LAM8_MU2_" + htag + "_" + wtag,
            sp.expand(Q - lam**8 * mu**2 * Q_core) == 0,
        )

# ---------------------------------------------------------------------------
# 4. Flat 2-jet vanishing: X = O(eps), t fixed or t = O(eps)
# ---------------------------------------------------------------------------
def assert_jet2_zero(Qexpr, tag: str) -> None:
    for n in range(0, 3):
        check(
            "FLAT_JET2_DERIV_ZERO_" + tag + "_" + str(n),
            sp.diff(Qexpr, eps, n).subs(eps, 0) == 0,
        )


def assert_sharp_order(Qexpr, order: int, tag: str) -> None:
    for n in range(order):
        check(
            "NO_LOWER_ORDER_" + tag + "_" + str(n),
            sp.diff(Qexpr, eps, n).subs(eps, 0) == 0,
        )
    leading = sp.simplify(Qexpr / eps**order)
    check("SHARP_LEADING_" + tag, leading.subs(eps, 0) != 0)


for htag, H in (("ETA", ETA), ("HN", h_n), ("GEN", H_gen)):
    # Case A: t fixed => Q = O(eps^8)
    R_a = joint_residual(eps * A, u, eps * B, w)
    Q_a = sp.expand((R_a.T * H * R_a)[0])
    assert_jet2_zero(Q_a, "TFIXED_" + htag)
    assert_sharp_order(Q_a, 8, "TFIXED_" + htag)

    # Case B: t = O(eps) => Q = O(eps^10)
    R_b = joint_residual(eps * A, eps * u, eps * B, eps * w)
    Q_b = sp.expand((R_b.T * H * R_b)[0])
    assert_jet2_zero(Q_b, "TSCALED_" + htag)
    assert_sharp_order(Q_b, 10, "TSCALED_" + htag)

# Second witness pair, t-scaled only (cheap extra control).
R_c = joint_residual(eps * A2, eps * w, eps * B2, eps * u)
for htag, H in (("ETA", ETA), ("HN", h_n)):
    Q_c = sp.expand((R_c.T * H * R_c)[0])
    assert_jet2_zero(Q_c, "TSCALED2_" + htag)
    assert_sharp_order(Q_c, 10, "TSCALED2_" + htag)

# ---------------------------------------------------------------------------
# 5. Seed / completion split: j^2_flat(S_star + Q) = j^2_flat S_star
# ---------------------------------------------------------------------------
S0, S1, S2, F = sp.symbols("S0 S1 S2 F0")
S_poly = S0 + S1 * eps + S2 * eps**2 / 2
for order, tag in ((8, "E8"), (10, "E10")):
    Q_model = eps**order * F
    for k in range(0, 3):
        check(
            "SEED_COMPLETION_SPLIT_" + tag + "_ORDER_" + str(k),
            sp.diff(S_poly + Q_model, eps, k).subs(eps, 0)
            == sp.diff(S_poly, eps, k).subs(eps, 0),
        )

# ---------------------------------------------------------------------------
# 6. Q-family generators I^eta, I^n inherit the vanishing
# ---------------------------------------------------------------------------
R_w = joint_residual(eps * A, eps * u, eps * B, eps * w)
I_eta = sp.expand((R_w.T * ETA * R_w)[0])
I_n = sp.expand((R_w.T * h_n * R_w)[0])
assert_jet2_zero(I_eta, "IETA")
assert_jet2_zero(I_n, "IN")
assert_sharp_order(I_eta, 10, "IETA")
assert_sharp_order(I_n, 10, "IN")

print("RESULT_ORDER: R_{2|1}=O(X^4 t); Q=R^T H R = O(X^8 t^2); with t=O(eps),X=O(eps): Q=O(eps^10).")
print("RESULT_JET: j^2_flat Q = 0 exactly (all derivatives of order <= 2 vanish at the flat point).")
print("RESULT_SPLIT: j^2_flat (S_star + Q) = j^2_flat S_star (seed/completion split locked).")
print("TERMINAL: DISCRETE-FLAT-JET-Q-VANISHES")
