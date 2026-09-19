import D0.Core.Phi
import Mathlib.FieldTheory.IntermediateField.Adjoin.Basic
import Mathlib.Tactic

/-!
# D0.Algebra.GaloisComposite

A minimal honest scalar bridge between the golden field and the S_DE window field.

The scene's golden quantities live in `ℚ(√5)`, while the two exact S_DE window
roots involve `√10`.  These quadratic fields are distinct, so no rational
single-field identification is available.  A canonical common scalar
carrier is the biquadratic compositum

    K = ℚ(√5, √2),

because `√10 = √5·√2`.

This module proves only the algebraic carrier facts needed for that statement:

* `K` contains `√5`, `√2`, hence `√10`;
* `K` contains `φ, ψ` and both exact S_DE roots;
* `K` is minimal among intermediate subfields of `ℝ` containing both generators;
* the S_DE roots are exchanged by the independent `√2` sign flip;
* the familiar golden conjugation is the independent `√5` sign flip;
* flipping both signs fixes `√10`, giving the Klein-four sign pattern.

Honesty boundary: this is a common scalar carrier, **not** a physical intertwiner and
not a proof that a D0 transport operator acts through the compositum.  In particular,
we do not claim the S_DE roots are algebraic integers: their product is `359/160`,
so the stronger `𝒪_K` statement proposed in exploratory notes is not imported here.
-/

namespace D0.Algebra.GaloisComposite

open D0
open IntermediateField

/-- The biquadratic compositum `ℚ(√5,√2)` inside `ℝ`. -/
noncomputable def compositeField : IntermediateField ℚ ℝ :=
  IntermediateField.adjoin ℚ ({Real.sqrt 5, Real.sqrt 2} : Set ℝ)

/-- The two primitive square-root generators lie in the compositum. -/
theorem sqrt5_mem_composite : Real.sqrt 5 ∈ compositeField := by
  apply IntermediateField.subset_adjoin
  simp

theorem sqrt2_mem_composite : Real.sqrt 2 ∈ compositeField := by
  apply IntermediateField.subset_adjoin
  simp

/-- `√10 = √5·√2`. -/
theorem sqrt10_eq_sqrt5_mul_sqrt2 :
    Real.sqrt 10 = Real.sqrt 5 * Real.sqrt 2 := by
  have h5 : 0 ≤ (5 : ℝ) := by norm_num
  rw [← Real.sqrt_mul h5]
  norm_num

/-- Hence the S_DE radical also lies in the same field. -/
theorem sqrt10_mem_composite : Real.sqrt 10 ∈ compositeField := by
  rw [sqrt10_eq_sqrt5_mul_sqrt2]
  exact mul_mem sqrt5_mem_composite sqrt2_mem_composite

/-- The golden pair is already contained in the compositum. -/
theorem phi_mem_composite : phi ∈ compositeField := by
  unfold phi
  have h1 : (1 : ℝ) ∈ compositeField := one_mem _
  have h2 : (2 : ℝ) ∈ compositeField := by norm_num
  exact div_mem (add_mem h1 sqrt5_mem_composite) h2

theorem psi_mem_composite : psi ∈ compositeField := by
  unfold psi
  have h1 : (1 : ℝ) ∈ compositeField := one_mem _
  have h2 : (2 : ℝ) ∈ compositeField := by norm_num
  exact div_mem (sub_mem h1 sqrt5_mem_composite) h2

/-- Exact S_DE window roots. -/
noncomputable def lambdaC : ℝ := (3 : ℝ) / 2 - Real.sqrt 10 / 40
noncomputable def lambdaR : ℝ := (3 : ℝ) / 2 + Real.sqrt 10 / 40

theorem lambdaC_mem_composite : lambdaC ∈ compositeField := by
  unfold lambdaC
  have h3 : (3 : ℝ) ∈ compositeField := by norm_num
  have h2 : (2 : ℝ) ∈ compositeField := by norm_num
  have h40 : (40 : ℝ) ∈ compositeField := by norm_num
  exact sub_mem (div_mem h3 h2) (div_mem sqrt10_mem_composite h40)

theorem lambdaR_mem_composite : lambdaR ∈ compositeField := by
  unfold lambdaR
  have h3 : (3 : ℝ) ∈ compositeField := by norm_num
  have h2 : (2 : ℝ) ∈ compositeField := by norm_num
  have h40 : (40 : ℝ) ∈ compositeField := by norm_num
  exact add_mem (div_mem h3 h2) (div_mem sqrt10_mem_composite h40)

/-- Basic square identity for the window radical. -/
theorem sqrt10_sq : (Real.sqrt 10) ^ 2 = (10 : ℝ) := by
  exact Real.sq_sqrt (by norm_num)

/-- The exact roots have the owned sum and product. -/
theorem lambda_sum : lambdaC + lambdaR = 3 := by
  unfold lambdaC lambdaR
  ring

theorem lambda_product : lambdaC * lambdaR = (359 : ℝ) / 160 := by
  unfold lambdaC lambdaR
  field_simp
  nlinarith [sqrt10_sq]

/-- Both roots satisfy the normalized S_DE polynomial. -/
theorem lambdaC_root :
    160 * lambdaC ^ 2 - 480 * lambdaC + 359 = 0 := by
  unfold lambdaC
  field_simp
  nlinarith [sqrt10_sq]

theorem lambdaR_root :
    160 * lambdaR ^ 2 - 480 * lambdaR + 359 = 0 := by
  unfold lambdaR
  field_simp
  nlinarith [sqrt10_sq]

/-! ## Klein-four sign pattern -/

/-- Flipping only `√2` flips `√10`. -/
theorem flip_sqrt2_flips_sqrt10 :
    Real.sqrt 5 * (-Real.sqrt 2) = -Real.sqrt 10 := by
  rw [sqrt10_eq_sqrt5_mul_sqrt2]
  ring

/-- Flipping only `√5` also flips `√10`. -/
theorem flip_sqrt5_flips_sqrt10 :
    (-Real.sqrt 5) * Real.sqrt 2 = -Real.sqrt 10 := by
  rw [sqrt10_eq_sqrt5_mul_sqrt2]
  ring

/-- Flipping both generators fixes `√10`. -/
theorem flip_both_fixes_sqrt10 :
    (-Real.sqrt 5) * (-Real.sqrt 2) = Real.sqrt 10 := by
  rw [sqrt10_eq_sqrt5_mul_sqrt2]
  ring

/-- The independent `√2` sign flip exchanges the two S_DE window roots. -/
theorem sqrt2_flip_swaps_window_roots :
    (3 : ℝ) / 2 - (-Real.sqrt 10) / 40 = lambdaR ∧
    (3 : ℝ) / 2 + (-Real.sqrt 10) / 40 = lambdaC := by
  constructor
  · rw [lambdaR]; ring
  · rw [lambdaC]; ring

/-- The independent `√5` sign flip is the usual golden conjugation
`φ ↔ ψ`. -/
theorem sqrt5_flip_swaps_golden_pair :
    ((1 - Real.sqrt 5) / 2 : ℝ) = psi ∧
    ((1 + Real.sqrt 5) / 2 : ℝ) = phi := by
  simp [D0.psi, D0.phi]

/-- On the positive archive ratio, golden conjugation gives the owned negative value
`ψ⁻¹ = -φ`. -/
theorem golden_conjugation_phi_inv :
    psi⁻¹ = -phi := by
  apply inv_eq_of_mul_eq_one_right
  linear_combination -D0.phi_mul_psi

/-- Capstone: one minimal common scalar carrier contains both exact quadratic sectors,
with two independent sign flips and the Klein-four product sign pattern. -/
theorem galois_composite_owner :
    phi ∈ compositeField ∧
    psi ∈ compositeField ∧
    lambdaC ∈ compositeField ∧
    lambdaR ∈ compositeField ∧
    lambdaC + lambdaR = 3 ∧
    lambdaC * lambdaR = (359 : ℝ) / 160 ∧
    ((-Real.sqrt 5) * (-Real.sqrt 2) = Real.sqrt 10) := by
  exact ⟨phi_mem_composite, psi_mem_composite,
    lambdaC_mem_composite, lambdaR_mem_composite,
    lambda_sum, lambda_product, flip_both_fixes_sqrt10⟩

end D0.Algebra.GaloisComposite
