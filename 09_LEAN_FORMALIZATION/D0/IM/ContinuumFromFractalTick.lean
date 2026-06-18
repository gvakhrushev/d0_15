import D0.Core.Phi
import D0.Dynamics.PisotContraction
import Mathlib.Analysis.SpecialFunctions.Log.Basic
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

/-! ## Continuous envelope of the discrete tick ladder (φ-ladder as the first internal continuum)

The continuum parameter in D0 is NOT an externally imported real coordinate: it is the unique
multiplicative (cocycle) envelope of the certified discrete φ-tick. BOOK_02 §02.41 ("Semigroup
Uniqueness Theorem", `A(s+t)=A(s)A(t)/A₀`) and BOOK_06 §06.v15 (`A(s)=A₀·e^{−s·logφ}`) state this in
prose / the cert (`vp_continuum_from_fractal_tick.py`); the two theorems below lift it into Lean. This
is the Gate-0 "first continuum"; it is NOT the smooth-manifold limit (that stays the Rieffel/GHP +
Connes owner-edge, `D0-RIEFFEL-GHP-CONTINUUM-OWNER-001`). -/

/-- Continuous scale envelope `A(t) = A₀·exp(−t·log φ)`, the real-parameter extension of the discrete
ladder `Aₙ = A₀·(1/φ)ⁿ`. -/
noncomputable def envAmount (A0 t : ℝ) : ℝ := A0 * Real.exp (-(t * Real.log phi))

/-- **Semigroup / cocycle law** (BOOK_02 §02.41, lifted to Lean): for `A₀ ≠ 0`,
`A(s+t) = A(s)·A(t)/A₀`. The unique multiplicative one-parameter extension of the φ-tick. -/
theorem env_cocycle (A0 s t : ℝ) (hA0 : A0 ≠ 0) :
    envAmount A0 (s + t) = envAmount A0 s * envAmount A0 t / A0 := by
  unfold envAmount
  rw [show -((s + t) * Real.log phi) = (-(s * Real.log phi)) + (-(t * Real.log phi)) by ring,
      Real.exp_add]
  field_simp

/-- The envelope restricts on the integers to the certified discrete ladder: `A(n) = A₀·(1/φ)ⁿ`. So the
continuum envelope and the finite tick ladder are the same object seen continuously vs discretely. -/
theorem env_restricts_to_ladder (A0 : ℝ) (n : ℕ) :
    envAmount A0 (n : ℝ) = A0 * ladderAmount n := by
  have hpos : (0 : ℝ) < phi := by unfold phi; positivity
  unfold envAmount ladderAmount
  rw [show -((n : ℝ) * Real.log phi) = (n : ℝ) * (-(Real.log phi)) by ring,
      Real.exp_nat_mul, Real.exp_neg, Real.exp_log hpos]

/-- **Continuum-envelope cert (Lean leg of D0-IM-003).** The φ-ladder is the internal discrete↔continuum
bridge: the continuous envelope obeys the multiplicative cocycle and restricts on integers to the
certified discrete tick ladder. (The matrix-exponential `M_tick = exp(G)` identity and the "this IS the
physical/smooth continuum limit" reading stay the owner-edge residual, not claimed here.) -/
theorem continuum_envelope_cert :
    (∀ A0 s t : ℝ, A0 ≠ 0 → envAmount A0 (s + t) = envAmount A0 s * envAmount A0 t / A0) ∧
    (∀ A0 : ℝ, ∀ n : ℕ, envAmount A0 (n : ℝ) = A0 * ladderAmount n) :=
  ⟨env_cocycle, env_restricts_to_ladder⟩

end D0.IM
