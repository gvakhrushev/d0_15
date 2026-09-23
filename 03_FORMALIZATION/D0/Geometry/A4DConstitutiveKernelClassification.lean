import Mathlib.Data.Matrix.Mul
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic
import D0.Geometry.A4DSolderMetricCompletion
import D0.Geometry.A4DStaggeredHodgeSelector
import D0.Geometry.Archive1DCochainRefinement
import D0.Geometry.ArchiveGradedRefinementChainMap
import D0.Geometry.ArchiveRefinementHodgeWeights

/-!
# Polynomial constitutive family and the flat first jet

`H` is an independently supplied symmetric linear symbol. The constructive
flux operator is not on this baseline, so the family is stated for that
supplied `H`. Counting positivity for `α > 1/4` is not Lorentzian Hodge
positivity. No value of `α` is selected. Determinant density is an invariant
candidate, not a selected kernel. Refinement traces do not choose `α`.

The Ward-only tangent class stays the 24-dimensional space of
`WardKernel`. Equality with a fully supplied derivative is extensionality.
-/

namespace D0.Geometry

open D0
open scoped BigOperators Matrix

variable {n : Type*} [Fintype n] [DecidableEq n]

def kernelPoly {K : Type*} [CommRing K] (α : K) (H : Matrix n n K) : Matrix n n K :=
  1 + H + α • (H * H)

noncomputable def squaredFluxEnergy {n : Type*} [Fintype n] [DecidableEq n]
    (α : ℝ) (H : Matrix n n ℝ) (ψ : n → ℝ) : ℝ :=
  (1 / 2) * ∑ i, ψ i * (kernelPoly α H).mulVec ψ i

theorem squaredFlux_same_flat_value_and_firstJet {K : Type*} [CommRing K]
    (α t : K) (H : Matrix n n K) :
    kernelPoly α (0 : Matrix n n K) = 1 ∧
      kernelPoly α (t • H) = 1 + t • H + (α * t ^ 2) • (H * H) := by
  constructor
  · simp [kernelPoly]
  · simp [kernelPoly, Matrix.mul_smul, Matrix.smul_mul, smul_smul, mul_comm, mul_left_comm, pow_two]

theorem kernelPoly_degree_preserving {K V : Type*} [CommRing K] [AddCommGroup V] [Module K V]
    (D H : V →ₗ[K] V) (α : K) (h : D.comp H = H.comp D) :
    D.comp (LinearMap.id + H + α • (H.comp H)) =
      (LinearMap.id + H + α • (H.comp H)).comp D := by
  ext v
  have h1 : D (H v) = H (D v) := by
    simpa [LinearMap.comp_apply] using congr_fun (congrArg DFunLike.coe h) v
  have h2 : D (H (H v)) = H (H (D v)) := by
    have hH := congr_fun (congrArg DFunLike.coe h) (H v)
    simpa [LinearMap.comp_apply, h1] using hH
  simp [LinearMap.comp_apply, h1, h2, smul_eq_mul]

theorem kernelPoly_parity_preserving {K V : Type*} [CommRing K] [AddCommGroup V] [Module K V]
    (P H : V →ₗ[K] V) (α : K) (h : P.comp H = H.comp P) :
    P.comp (LinearMap.id + H + α • (H.comp H)) =
      (LinearMap.id + H + α • (H.comp H)).comp P :=
  kernelPoly_degree_preserving P H α h

theorem kernelPoly_matterPathLength_le_four {X K : Type*} [CommRing K]
    (dist : X → X → ℕ) (htri : ∀ x y z, dist x z ≤ dist x y + dist y z)
    (H : (X → K) →ₗ[K] (X → K))
    (hH : ∀ ψ x, (∀ y, dist x y ≤ 2 → ψ y = 0) → H ψ x = 0) :
    ∀ ψ x, (∀ y, dist x y ≤ 4 → ψ y = 0) → (H.comp H) ψ x = 0 := by
  intro ψ x hψ
  apply hH
  intro y hy
  apply hH
  intro z hz
  apply hψ
  exact le_trans (htri x y z) (add_le_add hy hz)

lemma symm_dot_mulVec (A : Matrix n n ℝ) (hA : A.transpose = A) (v w : n → ℝ) :
    ∑ i, v i * A.mulVec w i = ∑ i, A.mulVec v i * w i := by
  classical
  have hL : ∑ i, v i * A.mulVec w i = ∑ i, ∑ j, v i * A i j * w j := by
    simp only [Matrix.mulVec, dotProduct, Finset.mul_sum, mul_assoc]
  have hR : ∑ i, A.mulVec v i * w i = ∑ j, ∑ i, v i * A i j * w j := by
    simp only [Matrix.mulVec, dotProduct, Finset.sum_mul]
    refine Finset.sum_congr rfl ?_
    intro i _
    refine Finset.sum_congr rfl ?_
    intro j _
    have hswap : A j i = A i j := by
      simpa [Matrix.transpose] using (congr_fun (congr_fun hA j) i).symm
    rw [hswap]
    ring
  rw [hL, hR, Finset.sum_comm]

lemma symm_square_norm (A : Matrix n n ℝ) (hA : A.transpose = A) (v : n → ℝ) :
    ∑ i, v i * (A * A).mulVec v i = ∑ i, (A.mulVec v i) ^ 2 := by
  have hmul : (A * A).mulVec v = A.mulVec (A.mulVec v) := by
    ext i
    simp [Matrix.mulVec, Matrix.mul_apply, dotProduct, Finset.mul_sum, Finset.sum_mul]
    rw [Finset.sum_comm]
    refine Finset.sum_congr rfl ?_
    intro j _
    refine Finset.sum_congr rfl ?_
    intro k _
    ring
  rw [hmul, symm_dot_mulVec A hA v (A.mulVec v)]
  simp [pow_two, mul_comm]

theorem kernelPoly_positive_of_quarter_lt (α : ℝ) (hα : (1 : ℝ) / 4 < α)
    (H : Matrix n n ℝ) (hH : H.transpose = H) :
    ∀ v, v ≠ 0 → 0 < ∑ i, v i * (kernelPoly α H).mulVec v i := by
  intro v hv
  let c : ℝ := 1 / (2 * α)
  let β : ℝ := 1 - 1 / (4 * α)
  let A : Matrix n n ℝ := H + c • 1
  have hα0 : 0 < α := lt_trans (by norm_num) hα
  have hβ : 0 < β := by
    have h4 : 0 < 4 * α := by nlinarith
    have hlt : 1 / (4 * α) < 1 := by
      rw [div_lt_one h4]
      nlinarith
    exact sub_pos.mpr hlt
  have hA : A.transpose = A := by
    simp [A, hH, Matrix.transpose_add, Matrix.transpose_smul, Matrix.transpose_one]
  have hsquare : (H + c • (1 : Matrix n n ℝ)) * (H + c • 1) =
      H * H + (2 * c) • H + (c * c) • 1 := by
    simp only [Matrix.add_mul, Matrix.mul_add, Matrix.one_mul, Matrix.mul_one,
      Matrix.smul_mul, Matrix.mul_smul, smul_add, smul_smul]
    have htwo : c • H + c • H = (2 * c) • H := by
      rw [← add_smul]
      congr 1
      ring
    calc
      H * H + c • H + (c • H + (c * c) • 1) =
          H * H + (c • H + c • H) + (c * c) • 1 := by abel
      _ = H * H + (2 * c) • H + (c * c) • 1 := by rw [htwo]
  have halg : kernelPoly α H = α • (A * A) + β • 1 := by
    have hc : α * (2 * c) = 1 := by
      simp only [c]
      field_simp
    have hc2 : α * (c * c) + β = 1 := by
      simp only [c, β]
      field_simp
      ring
    unfold kernelPoly
    rw [show A * A = H * H + (2 * c) • H + (c * c) • 1 from hsquare]
    simp only [smul_add, smul_smul]
    have hlin : (α * (2 * c)) • H = H := by simp [hc]
    have hconst : (α * (c * c)) • (1 : Matrix n n ℝ) + β • 1 = (1 : Matrix n n ℝ) := by
      rw [← add_smul, hc2, one_smul]
    rw [hlin]
    abel_nf
    rw [hconst]
    abel
  have hnorm : 0 < ∑ i, v i ^ 2 := by
    classical
    have hnn : ∀ i, 0 ≤ v i ^ 2 := fun i => sq_nonneg _
    by_contra hle
    have hsumle : (∑ i, v i ^ 2) ≤ 0 := le_of_not_gt hle
    have hsumge : 0 ≤ ∑ i, v i ^ 2 := Finset.sum_nonneg (fun i _ => hnn i)
    have hzero : ∑ i, v i ^ 2 = 0 := le_antisymm hsumle hsumge
    have hterm : ∀ i, v i ^ 2 = 0 := by
      intro i
      exact (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => hnn j)).1 hzero i (Finset.mem_univ i)
    apply hv
    funext i
    exact (sq_eq_zero_iff).1 (hterm i)
  have hform : ∑ i, v i * (kernelPoly α H).mulVec v i =
      α * ∑ i, (A.mulVec v i) ^ 2 + β * ∑ i, v i ^ 2 := by
    rw [halg]
    simp only [Matrix.add_mulVec, Matrix.smul_mulVec, Matrix.one_mulVec, Pi.add_apply,
      Pi.smul_apply, smul_eq_mul]
    have hsplit : ∀ i, v i * (α * (A * A).mulVec v i + β * v i) =
        α * (v i * (A * A).mulVec v i) + β * (v i * v i) := by
      intro i
      ring
    simp only [hsplit, Finset.sum_add_distrib]
    congr 1
    · rw [← Finset.mul_sum]
      simpa [mul_comm] using congrArg (fun t => α * t) (symm_square_norm A hA v)
    · rw [← Finset.mul_sum]
      simp [pow_two, mul_assoc, mul_comm, mul_left_comm]
  have hsq : 0 ≤ ∑ i, (A.mulVec v i) ^ 2 :=
    Finset.sum_nonneg (fun i _ => sq_nonneg _)
  have hpos : 0 < β * ∑ i, v i ^ 2 := mul_pos hβ hnorm
  have hge : β * ∑ i, v i ^ 2 ≤ α * ∑ i, (A.mulVec v i) ^ 2 + β * ∑ i, v i ^ 2 := by
    have : 0 ≤ α * ∑ i, (A.mulVec v i) ^ 2 := mul_nonneg (le_of_lt hα0) hsq
    linarith
  rw [hform]
  exact lt_of_lt_of_le hpos hge

def hopSwap : Matrix (Fin 2) (Fin 2) ℚ := !![0, 1; 1, 0]

theorem nonlinearSelector_not_from_flatJet :
    hopSwap * hopSwap ≠ 0 ∧
      kernelPoly (1 : ℚ) hopSwap ≠ kernelPoly (2 : ℚ) hopSwap := by
  native_decide

/-! ## Determinant density. Not a selected kernel. -/

theorem roleLorentzMetric_det : Matrix.det roleLorentzMetric = -1 := by
  rw [roleLorentzMetric, Matrix.det_diagonal]
  have huniv : (Finset.univ : Finset Role) = insert A (insert C (insert D {B})) := by
    decide
  rw [huniv]
  repeat rw [Finset.prod_insert (by decide)]
  simp [Finset.prod_singleton, roleLorentzSign_A, roleLorentzSign_C,
    roleLorentzSign_D, roleLorentzSign_B]

lemma det_lorentz_sq (Λ : Matrix Role Role ℝ) (hΛ : IsRoleLorentz Λ) :
    (Matrix.det Λ) ^ 2 = 1 := by
  have hdet := congrArg Matrix.det hΛ
  simp only [Matrix.det_mul, Matrix.det_transpose] at hdet
  rw [roleLorentzMetric_det] at hdet
  have : (Matrix.det Λ) ^ 2 * (-1) = -1 := by
    simpa [pow_two, mul_assoc, mul_left_comm, mul_comm] using hdet
  linarith

def detDensity (Θ : Matrix Role Role ℝ) : ℝ := ((Matrix.det Θ) ^ 2 - 1) ^ 2

theorem detDensity_rightLorentz (Θ Λ : Matrix Role Role ℝ) (hΛ : IsRoleLorentz Λ) :
    detDensity (Θ * Λ) = detDensity Θ := by
  have hmul : Matrix.det (Θ * Λ) = Matrix.det Θ * Matrix.det Λ := Matrix.det_mul _ _
  have hsq : (Matrix.det Λ) ^ 2 = 1 := det_lorentz_sq Λ hΛ
  simp only [detDensity, hmul, mul_pow, hsq, mul_one]

def diagonalSolder (t : ℝ) : Matrix Role Role ℝ :=
  Matrix.diagonal (fun r => if r = A then 1 + t else roleLorentzSign r)

theorem det_diagonalSolder (t : ℝ) : Matrix.det (diagonalSolder t) = -(1 + t) := by
  rw [diagonalSolder, Matrix.det_diagonal]
  have huniv : (Finset.univ : Finset Role) = insert A (insert C (insert D {B})) := by
    decide
  rw [huniv]
  repeat rw [Finset.prod_insert (by decide)]
  simp [Finset.prod_singleton, roleLorentzSign_C, roleLorentzSign_D, roleLorentzSign_B,
    show C ≠ A by decide, show D ≠ A by decide, show B ≠ A by decide]

theorem detDensity_firstJet_zero (t : ℝ) :
    detDensity (diagonalSolder 0) = 0 ∧
      detDensity (diagonalSolder t) = (2 * t + t ^ 2) ^ 2 := by
  constructor
  · simp [detDensity, det_diagonalSolder]
  · simp [detDensity, det_diagonalSolder]
    ring

theorem detDensity_constantDiagonal_nonzero :
    detDensity (diagonalSolder 1) ≠ 0 := by
  have h := (detDensity_firstJet_zero 1).2
  rw [h]
  norm_num

def SolderNondegenerate (N : ℕ) (e : LocalCoframeField N) : Prop :=
  ∀ x, Matrix.det (solderMatrix N e x) ≠ 0

theorem detSolder_nonzero_flat (N : ℕ) (x : ArchiveRolePhaseGroup N) :
    Matrix.det (solderMatrix N 0 x) ≠ 0 := by
  simp [solderMatrix_zero, roleLorentzMetric_det]

theorem detDomain_Lorentz_invariant (Θ Λ : Matrix Role Role ℝ) (hΛ : IsRoleLorentz Λ)
    (hΘ : Matrix.det Θ ≠ 0) : Matrix.det (Θ * Λ) ≠ 0 := by
  rw [Matrix.det_mul]
  exact mul_ne_zero hΘ (by
    intro h
    have := det_lorentz_sq Λ hΛ
    rw [h] at this
    norm_num at this)

/-- Relabeling the site at which an already evaluated solder matrix is read.
Centering does not automatically commute with an arbitrary pullback of `e`. -/
theorem detDomain_siteRelabel (N : ℕ) (Θ : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (σ : ArchiveRolePhaseGroup N ≃ ArchiveRolePhaseGroup N) :
    (∀ x, Matrix.det (Θ x) ≠ 0) ↔ (∀ x, Matrix.det (Θ (σ x)) ≠ 0) := by
  constructor
  · intro h x
    exact h (σ x)
  · intro h x
    simpa using h (σ.symm x)

theorem solder_not_always_nondegenerate (N : ℕ) :
    ∃ e : LocalCoframeField N, ∃ x, Matrix.det (solderMatrix N e x) = 0 := by
  refine ⟨fun _ r a => -roleLorentzMetric r a, 0, ?_⟩
  have hconst : centeredCoframeMatrix N (fun _ r a => -roleLorentzMetric r a) 0 =
      -roleLorentzMetric := by
    ext r a
    simp [centeredCoframeMatrix, backwardAverage, Matrix.neg_apply]
  simp [solderMatrix, hconst, Matrix.det_zero]

/-- Supplied equality on every coframe is extensionality. The Ward-only class
remains 24-dimensional for `L ≥ 4` and is a different statement. -/
theorem suppliedDerivative_zero_by_extensionality {E F : Type*}
    (H J : E → F) (h : ∀ e, J e = H e) : J = H :=
  funext h

theorem wardClass_remains_twentyFour (N : ℕ) (hN : 2 ≤ N) :
    Module.finrank ℚ (WardKernel N) = 24 :=
  selfAdjoint_radiusOneWardKernel_finrank_twentyFour N hN

/-! ## Refinement traces do not select a kernel

`Archive1DCochainRefinement`, `ArchiveGradedRefinementChainMap`, and
`ArchiveRefinementHodgeWeights` own trace numbers. Their literal theorem
surfaces do not contain typed refinement maps `B_P` or `B_D`. Equal trace
does not determine a symmetric matrix, and these numbers do not select `α`.
-/

theorem refinement_sameTrace_distinct :
    ∃ A B : Matrix (Fin 2) (Fin 2) ℚ,
      A.transpose = A ∧ B.transpose = B ∧ A ≠ B ∧ ∑ i, A i i = ∑ i, B i i := by
  refine ⟨!![1, 0; 0, 1], !![2, 0; 0, 0], ?_⟩
  native_decide

theorem refinementOwners_are_traces :
    massMatrixTrace1D = 3 ∧ edgeGramMatrixTrace1D = 2 ∧
      hodgeGramTraceDegree 0 = 81 ∧ hodgeGramTraceDegree 1 = 27 ∧
      hodgeGramTraceDegree 2 = 9 ∧ hodgeGramTraceDegree 3 = 3 ∧
      hodgeGramTraceDegree 4 = 1 ∧ totalHodgeGramTraceSum = 256 ∧
      roleProductDim = 4 := by
  simp [massMatrixTrace1D, edgeGramMatrixTrace1D, hodgeGramTraceDegree,
    totalHodgeGramTraceSum, roleProductDim, hodge_gram_trace_0, hodge_gram_trace_1,
    hodge_gram_trace_2, hodge_gram_trace_3, hodge_gram_trace_4,
    total_hodge_gram_trace_sum_eq]

end D0.Geometry
