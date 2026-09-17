import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Real.StarOrdered
import Mathlib.Tactic

/-!
# D0-FORGETTING-CHANNEL-PTP-001 — D0 forgetting as a positive trace-preserving channel

D0 reads "forgetting" / archive integration as a decoherence channel: structure is discarded and only
the conserved total (the trace) survives, spread uniformly. The canonical model is the fully
depolarizing channel `M ↦ (tr M / n) • I` on `n×n` matrices. This module proves it is a genuine
**positive trace-preserving (PTP)** linear map over real matrices, reusing Mathlib's `Matrix.PosSemidef`
machinery (PSD is preserved because the trace of a PSD matrix is `≥ 0`).

Scope (honest): this proves the channel is additive, scalar-linear, trace-preserving, and PSD-preserving
(positive) — the operational core of a quantum/stochastic channel. FULL complete positivity (a genuine
`Mathlib.Analysis.CStarAlgebra.CompletelyPositiveMap` over `CStarMatrix`, requiring the
`map_cstarMatrix_nonneg'` obligation over all `k×k` amplifications) is a named THEOREM-TARGET: the
depolarizing channel is classically CPTP, but the Lean CP obligation quantifies over every matrix
amplification and is not a bounded hand-proof; the trace channel is not a `*`-homomorphism, so the easy
`NonUnitalStarAlgHomClass` CP route does not apply.
-/

namespace D0.Probability

open Matrix

/-- The D0 **forgetting (fully depolarizing) channel** on `n×n` real matrices: discard all structure,
returning the conserved trace spread uniformly over the identity, `M ↦ (tr M / n) • I`. -/
noncomputable def d0ForgetChannel (n : ℕ) (M : Matrix (Fin n) (Fin n) ℝ) :
    Matrix (Fin n) (Fin n) ℝ :=
  (Matrix.trace M / n) • (1 : Matrix (Fin n) (Fin n) ℝ)

/-- The forgetting channel is additive. -/
theorem d0ForgetChannel_add (n : ℕ) (M N : Matrix (Fin n) (Fin n) ℝ) :
    d0ForgetChannel n (M + N) = d0ForgetChannel n M + d0ForgetChannel n N := by
  unfold d0ForgetChannel
  rw [Matrix.trace_add, add_div, add_smul]

/-- The forgetting channel is homogeneous (commutes with real scalars). With additivity this is
linearity. -/
theorem d0ForgetChannel_smul (n : ℕ) (c : ℝ) (M : Matrix (Fin n) (Fin n) ℝ) :
    d0ForgetChannel n (c • M) = c • d0ForgetChannel n M := by
  unfold d0ForgetChannel
  rw [Matrix.trace_smul, smul_eq_mul, smul_smul, mul_div_assoc]

/-- **Trace-preserving.** The forgetting channel preserves the trace (for `n ≥ 1`): the discarded
structure leaves the conserved total intact. -/
theorem d0ForgetChannel_trace_preserving (n : ℕ) (hn : 0 < n) (M : Matrix (Fin n) (Fin n) ℝ) :
    (d0ForgetChannel n M).trace = M.trace := by
  have hn' : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hn.ne'
  unfold d0ForgetChannel
  rw [Matrix.trace_smul, Matrix.trace_one, Fintype.card_fin, smul_eq_mul]
  field_simp

/-- **Positive.** The forgetting channel sends positive-semidefinite states to positive-semidefinite
states: `M ≥ 0 ⟹ (tr M / n) • I ≥ 0`, since the trace of a PSD matrix is `≥ 0` and a nonnegative
multiple of the identity is PSD. -/
theorem d0ForgetChannel_posSemidef (n : ℕ) (M : Matrix (Fin n) (Fin n) ℝ)
    (hM : M.PosSemidef) : (d0ForgetChannel n M).PosSemidef := by
  unfold d0ForgetChannel
  exact Matrix.PosSemidef.one.smul (div_nonneg hM.trace_nonneg (Nat.cast_nonneg n))

/-- **Positive trace-preserving (PTP).** Bundles the operational channel properties: the forgetting
channel is additive, homogeneous, trace-preserving (for `n ≥ 1`), and PSD-preserving. -/
theorem d0ForgetChannel_isPTP (n : ℕ) (hn : 0 < n) :
    (∀ M N, d0ForgetChannel n (M + N) = d0ForgetChannel n M + d0ForgetChannel n N) ∧
    (∀ (c : ℝ) M, d0ForgetChannel n (c • M) = c • d0ForgetChannel n M) ∧
    (∀ M, (d0ForgetChannel n M).trace = M.trace) ∧
    (∀ M, M.PosSemidef → (d0ForgetChannel n M).PosSemidef) :=
  ⟨d0ForgetChannel_add n, d0ForgetChannel_smul n,
   d0ForgetChannel_trace_preserving n hn, d0ForgetChannel_posSemidef n⟩

end D0.Probability
