import D0.Core.Phi
import D0.Dynamics.PisotContraction
import Mathlib.Tactic

/-!
# D0-IM-003 — continuum from the fractal tick (trace semigroup)

BOOK_01/06. Python certificate: `05_CERTS/vp_continuum_from_fractal_tick.py`.

The discrete fractal-tick map is a one-parameter trace semigroup whose contraction rate is `1/φ`. The
substrate decays geometrically `Aₙ = (1/φ)ⁿ` with the CONSTANT per-tick ratio `1/φ` (the discrete form
of the cert's constant log-gradient `log Aₙ − log Aₙ₋₁ = −log φ`, dodging the transcendental log), the
complement accumulates exactly the lost amount so the total `Aₙ + Bₙ = 1` is conserved (column-stochastic
tick matrix), and `1/φ = primitiveRoot`.

This module machine-checks that finite ladder core. The literal matrix-exponential identity
`M_tick = exp(G)` for the continuous generator, and the "continuum emerges as the envelope" limit reading,
are the genuine continuum residual and stay in the cert.
-/

namespace D0.IM

open D0

/-- Active substrate after `n` ticks: `Aₙ = (1/φ)ⁿ` (column-stochastic decay). -/
noncomputable def ladderAmount (n : ℕ) : ℝ := phi⁻¹ ^ n

/-- Accumulated archive after `n` ticks: `Bₙ = 1 − (1/φ)ⁿ` (`A₀ = 1`, `B₀ = 0`). -/
noncomputable def ladderComplement (n : ℕ) : ℝ := 1 - phi⁻¹ ^ n

/-- **Constant per-tick ratio:** `Aₙ₊₁ = Aₙ · (1/φ)` for every `n` (constant log gradient, exponentiated). -/
theorem ladder_constant_ratio (n : ℕ) : ladderAmount (n + 1) = ladderAmount n * phi⁻¹ := by
  unfold ladderAmount; rw [pow_succ]

/-- **Substrate conserved:** `Aₙ + Bₙ = 1` for every `n` (column-stochastic invariant). -/
theorem ladder_substrate_conserved (n : ℕ) : ladderAmount n + ladderComplement n = 1 := by
  unfold ladderAmount ladderComplement; ring

/-- The decay rate is the golden contracting root: `1/φ = primitiveRoot`. -/
theorem ladder_rate_eq_primitiveRoot : phi⁻¹ = primitiveRoot := phi_inv_eq_primitiveRoot

/-- The rate lies strictly in `(0,1)` — a genuine contraction. -/
theorem ladder_rate_mem_unit : 0 < phi⁻¹ ∧ phi⁻¹ < 1 := by
  rw [phi_inv_eq_primitiveRoot]; unfold primitiveRoot
  exact ⟨by linarith [sqrt_five_gt_two], by linarith [sqrt_five_lt_three]⟩

/-- **D0-IM-003.** The fractal-tick ladder: constant per-tick ratio `1/φ`, conserved total `Aₙ+Bₙ=1`
for every `n`, rate `= primitiveRoot ∈ (0,1)`. -/
theorem continuum_from_fractal_tick_cert :
    (∀ n : ℕ, ladderAmount (n + 1) = ladderAmount n * phi⁻¹) ∧
    (∀ n : ℕ, ladderAmount n + ladderComplement n = 1) ∧
    phi⁻¹ = primitiveRoot ∧
    (0 < phi⁻¹ ∧ phi⁻¹ < 1) :=
  ⟨ladder_constant_ratio, ladder_substrate_conserved, ladder_rate_eq_primitiveRoot,
   ladder_rate_mem_unit⟩

end D0.IM
