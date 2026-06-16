import D0.Core.Phi
import D0.Dynamics.PisotContraction
import Mathlib.Tactic

/-!
# D0-IM-002 — fractal informational tick (golden-ratio time step)

BOOK_01/06. Python certificate: `05_CERTS/vp_fractal_tick_informational_mechanics.py`.

A single informational time-step is the golden-ratio-weighted orthogonal map on a 4D info space split
into an active sector `P` and a clock/trace sector `Q`. The retained (active) fraction per tick is exactly
`p = 1/φ = φ−1` and the fraction routed into the trace is exactly `p² = 2−φ`, with `p + p² = 1`
(unitarity / substrate conservation). Iterating the tick is a Pisot contraction `Aₙ = pⁿ·A₀` that never
reaches zero in finitely many ticks while the conserved total `Aₙ + Bₙ` stays fixed.

This module machine-checks that finite φ-algebra core (`p = primitiveRoot = 1/φ`). The unitarity
`p + p² = 1` reuses `D0.primitive_root_satisfies` verbatim. The 4×4 orthogonal-block matrix layer and the
"time as trace order" / model-rejection readings stay in the cert.
-/

namespace D0.IM

open D0

/-- Active amplitude after `n` ticks: `Aₙ = pⁿ·A₀` with `p = primitiveRoot = 1/φ`. -/
noncomputable def tickA (A0 : ℝ) (n : ℕ) : ℝ := primitiveRoot ^ n * A0

/-- Archive (trace) amount after `n` ticks: `Bₙ = B₀ + (1 − pⁿ)·A₀`. -/
noncomputable def tickB (A0 B0 : ℝ) (n : ℕ) : ℝ := B0 + (1 - primitiveRoot ^ n) * A0

/-- **Unitarity / substrate conservation core:** `p + p² = 1` (the `UᵀU = I` block identity). -/
theorem tick_unitarity : primitiveRoot + primitiveRoot ^ 2 = 1 := primitive_root_satisfies

/-- Retained fraction per tick: `p = φ − 1`. -/
theorem tick_retained_fraction : primitiveRoot = phi - 1 := by
  unfold primitiveRoot phi; ring

/-- Trace fraction per tick: `p² = 2 − φ`. -/
theorem tick_trace_fraction : primitiveRoot ^ 2 = 2 - phi := by
  rw [tick_retained_fraction]; linear_combination phi_sq

/-- The conservation increment vanishes: `(p − 1) + p² = 0`. -/
theorem tick_increment_zero : (primitiveRoot - 1) + primitiveRoot ^ 2 = 0 := by
  linear_combination primitive_root_satisfies

/-- **Substrate conservation, all `n`:** `Aₙ + Bₙ = A₀ + B₀`. -/
theorem tick_substrate_conserved (A0 B0 : ℝ) (n : ℕ) :
    tickA A0 n + tickB A0 B0 n = A0 + B0 := by
  unfold tickA tickB; ring

/-- **Active never zero in finite ticks:** `0 < A₀ ⇒ 0 < Aₙ` for every `n` (Pisot positivity). -/
theorem tick_active_never_zero (A0 : ℝ) (hA : 0 < A0) (n : ℕ) : 0 < tickA A0 n := by
  unfold tickA
  have hpos : 0 < primitiveRoot := by unfold primitiveRoot; linarith [sqrt_five_gt_two]
  exact mul_pos (pow_pos hpos n) hA

/-- **D0-IM-002.** The golden tick: `p + p² = 1`, `p = φ−1`, `p² = 2−φ`, substrate is conserved for
every `n`, and the active amplitude never vanishes in finitely many ticks. -/
theorem fractal_tick_cert :
    primitiveRoot + primitiveRoot ^ 2 = 1 ∧
    primitiveRoot = phi - 1 ∧
    primitiveRoot ^ 2 = 2 - phi ∧
    (∀ A0 B0 : ℝ, ∀ n : ℕ, tickA A0 n + tickB A0 B0 n = A0 + B0) ∧
    (∀ A0 : ℝ, 0 < A0 → ∀ n : ℕ, 0 < tickA A0 n) :=
  ⟨tick_unitarity, tick_retained_fraction, tick_trace_fraction,
   tick_substrate_conserved, fun A0 hA n => tick_active_never_zero A0 hA n⟩

end D0.IM
