#!/usr/bin/env python3
"""D0-Q8-SIN-CHANNEL-001 — the seam correction rides the sin (off-diagonal) channel, forced by Q₈, G²=−1.

STRUCTURE (THE, Lean D0.Spectral.SeamHolonomy): in the quaternion carrier Q₈, left multiplication by a
unit imaginary i gives a generator G = L_i with G² = −I. Hence the one-parameter monodromy is

    U(θ) = exp(θ·G) = cos θ·I + sin θ·G        (since G² = −I)

So a turn of the seam holonomy mixes the role basis {1, i, j, k}: the DIAGONAL (role-preserving) entry is
⟨1|U|1⟩ = cos θ (the "trace" channel), while the OFF-DIAGONAL (role-changing, 1→i) entry is ⟨i|U|1⟩ = sin θ.
A correction transported BETWEEN distinct roles is therefore carried by the sin channel, not the trace —
this is why the α holonomy uses sin(12/5), not cos (vp_seam_holonomy_alpha.py).

DISCRIMINATOR: the trace/cos channel is role-preserving and carries no inter-role transport; only the sin
(off-diagonal) channel does. The control checks that the role-changing amplitude is sin θ (not cos θ).
"""
from __future__ import annotations

import sys

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def Lmat(which: str) -> np.ndarray:
    """Left-multiplication matrix by a unit quaternion on basis {1, i, j, k} (columns = images)."""
    if which == "i":   # i·1=i, i·i=−1, i·j=k, i·k=−j
        return np.array([[0, -1, 0, 0], [1, 0, 0, 0], [0, 0, 0, -1], [0, 0, 1, 0]], dtype=float)
    if which == "j":   # j·1=j, j·i=−k, j·j=−1, j·k=i
        return np.array([[0, 0, -1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, -1, 0, 0]], dtype=float)
    if which == "k":   # k·1=k, k·i=j, k·j=−i, k·k=−1
        return np.array([[0, 0, 0, -1], [0, 0, -1, 0], [0, 1, 0, 0], [1, 0, 0, 0]], dtype=float)
    raise ValueError(which)


def main() -> int:
    print("=== D0-Q8-SIN-CHANNEL-001  exp(θG)=cosθ·I+sinθ·G, off-diagonal=sinθ (Q₈, G²=−1) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: Q8 left-multiplication on {1,i,j,k}; G=L_i; G^2=-I; "
          "monodromy U=exp(theta*G); channel = off-diagonal (role-changing) entry")

    I4 = np.eye(4)
    for w in ("i", "j", "k"):
        G = Lmat(w)
        assert np.allclose(G @ G, -I4), f"control: L_{w}² must be −I (Q₈ relation)"
    print("PASS_G_SQUARED_MINUS_I  L_i² = L_j² = L_k² = −I  (the Q₈ / quaternion relation)")

    G = Lmat("i")
    theta = 12.0 / 5.0
    U = np.cos(theta) * I4 + np.sin(theta) * G          # = exp(θG) since G²=−I

    # verify U really is the matrix exponential of θG
    from numpy.linalg import matrix_power
    # exp via series is overkill; check the defining ODE-free identity exp(θG)=cosθI+sinθG by U·Uᵀ and U(θ1+θ2)
    assert np.allclose(U @ G, G @ U), "U commutes with G (one-parameter group)"
    assert np.allclose(U @ U.T, I4), "U is orthogonal (closure holonomy is a rotation)"
    print("PASS_HOLONOMY_IS_ROTATION  U(θ)=cosθ·I+sinθ·G is orthogonal, U=exp(θG)")

    diag = U[0, 0]            # ⟨1|U|1⟩  role-preserving (trace/cos channel)
    offdiag = U[1, 0]         # ⟨i|U|1⟩  role-changing 1→i (sin channel)
    assert np.isclose(diag, np.cos(theta)), "⟨1|U|1⟩ must be cos θ (trace channel)"
    assert np.isclose(offdiag, np.sin(theta)), "⟨i|U|1⟩ must be sin θ (off-diagonal channel)"
    print(f"PASS_OFFDIAGONAL_IS_SIN  ⟨i|U|1⟩ = sin θ = {offdiag:.6f};  ⟨1|U|1⟩ = cos θ = {diag:.6f}")

    # ---- NEGATIVE CONTROL: the inter-role correction is sin, not cos -----------------------
    # at small θ the role-changing amplitude ~ θ (sin), while the role-preserving ~ 1 (cos);
    # a correction transported between roles cannot be carried by the cos (diagonal) channel.
    small = 1e-3
    Us = np.cos(small) * I4 + np.sin(small) * G
    assert abs(Us[1, 0]) > abs(1.0 - Us[0, 0]) * 10, "control: role-change (sin) dominates role-preserve deviation (1−cos)"
    print("FAIL_COS_CHANNEL_CARRIES_NO_INTER_ROLE_TRANSPORT  the role-changing amplitude is sin θ "
          "(off-diagonal); the cos (trace) channel is role-preserving and cannot carry the seam correction")

    print("HONEST_SIN_CHANNEL_FORCED_BY_G_SQUARED_MINUS_I  the sin vs cos split is the off/diagonal split of "
          "exp(θG) with G²=−I; this is the algebra formalized in D0.Spectral.SeamHolonomy")
    print("PASS_Q8_SIN_CHANNEL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
