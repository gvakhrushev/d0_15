import Mathlib.Tactic

/-!
# D0-CKM-YUKAWA-KERNEL-CROSSGATE-001 — gauge-compatibility of the Yukawa over the kernel family

Cross-track gate (Track A ∩ Track B). The massless-`U(1)` kernel is the 2-dimensional anomaly-free family
`span{Y, B−L}` (Track A, Case A2, `D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001`). The compatibility requirement is
that the Yukawa coupling intertwine the gauge action — `[Q, Y_u] = [Q, Y_d] = 0` — for **every** generator in
the kernel family, NOT just for a hand-picked hypercharge row.

For one generation with Higgs `H` of charges `(Y=1/2, B−L=0)`, the Yukawa-invariance residuals are
`up = X_Q − X_{u_R} + X_H` and `down = X_Q − X_{d_R} − X_H`. They vanish for **both** `Y` and `B−L`
(`crossgate_holds`), so the Yukawa is invariant under the full kernel family — it does NOT select the
hypercharge row over `B−L` (consistent with the 2-dim Track-A kernel; this is exactly the protection against a
hidden hypercharge-row choice). A generator outside `span{Y, B−L}` breaks invariance (`crossgate_control`).

FIREWALL: charges are the frozen SM assignment; no fitted values; the row selection still requires `Ξ_Y`
(the bridge), which this gate does NOT supply.
-/

namespace D0.ParallelClosure.CrossGate

/-- Yukawa-invariance residuals `(up, down)` of a `U(1)` generator with charges `(X_Q, X_{u_R}, X_{d_R}, X_H)`. -/
def residuals (XQ XuR XdR XH : ℚ) : ℚ × ℚ := (XQ - XuR + XH, XQ - XdR - XH)

/-- Hypercharge `Y` leaves both Yukawas invariant. -/
theorem Y_invariant : residuals (1/6) (2/3) (-1/3) (1/2) = (0, 0) := by native_decide
/-- `B−L` leaves both Yukawas invariant. -/
theorem BL_invariant : residuals (1/3) (1/3) (1/3) 0 = (0, 0) := by native_decide

/-- **Cross-gate over the kernel family.** Both basis generators `Y` and `B−L` of the 2-dim massless kernel
satisfy `[Q, Y_{u/d}] = 0` — so the Yukawa is invariant under the entire `span{Y, B−L}` and does not select the
hypercharge row. -/
theorem crossgate_holds :
    residuals (1/6) (2/3) (-1/3) (1/2) = (0, 0) ∧ residuals (1/3) (1/3) (1/3) 0 = (0, 0) :=
  ⟨Y_invariant, BL_invariant⟩

/-- **Negative control.** A generator outside `span{Y, B−L}` (here a wrong Higgs charge `X_H = 1`) breaks
Yukawa invariance — the gate is not vacuous. -/
theorem crossgate_control : residuals (1/6) (2/3) (-1/3) 1 ≠ (0, 0) := by native_decide

end D0.ParallelClosure.CrossGate
