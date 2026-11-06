import Mathlib.Data.Matrix.Mul
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic
import D0.Geometry.A4DSolderMetricCompletion

/-!
# Path dressing, stabilizers, and centered-metric obstructions

Path dressing of a supplied seed is unambiguous exactly when relative holonomy
lies in that seed's stabilizer. Nonzero curvature is not a hypothesis and is
not claimed to force Hodge ambiguity.

The remaining theorems are obstructions to reading a constitutive kernel off
weaker data: full scalar closure, flat plaquette curvature, a pointwise
multiplication kernel, the centered solder metric at even period, and the flat
first jet. None of them selects a Hodge law.
-/

namespace D0.Geometry

open D0

section MatrixDressing

variable {n R : Type*} [Fintype n] [DecidableEq n] [CommRing R]

/-- `W^U = Uᵀ W U` equals `W^V` iff `H = U V⁻¹` stabilizes `W`. -/
theorem pathDressing_eq_iff_relativeHolonomy_stabilizes
    (U V W : Matrix n n R) [Invertible V] :
    U.transpose * W * U = V.transpose * W * V ↔
      (U * ⅟V).transpose * W * (U * ⅟V) = W := by
  constructor
  · intro h
    have h1 : (⅟V).transpose * (U.transpose * W * U) * ⅟V =
        (⅟V).transpose * (V.transpose * W * V) * ⅟V := by rw [h]
    have hL : (⅟V).transpose * (U.transpose * W * U) * ⅟V =
        (U * ⅟V).transpose * W * (U * ⅟V) := by
      calc
        (⅟V).transpose * (U.transpose * W * U) * ⅟V =
            (⅟V).transpose * U.transpose * W * (U * ⅟V) := by
              simp only [Matrix.mul_assoc]
        _ = (U * ⅟V).transpose * W * (U * ⅟V) := by
              rw [← Matrix.transpose_mul]
    have hR : (⅟V).transpose * (V.transpose * W * V) * ⅟V = W := by
      calc
        (⅟V).transpose * (V.transpose * W * V) * ⅟V =
            (⅟V).transpose * V.transpose * W * (V * ⅟V) := by
              simp only [Matrix.mul_assoc]
        _ = (V * ⅟V).transpose * W * (V * ⅟V) := by
              rw [← Matrix.transpose_mul]
        _ = W := by
              simp [Matrix.transpose_one]
    rw [hL, hR] at h1
    exact h1
  · intro h
    have h1 : V.transpose * ((U * ⅟V).transpose * W * (U * ⅟V)) * V =
        V.transpose * W * V := by rw [h]
    have hU : (U * ⅟V) * V = U := by
      rw [Matrix.mul_assoc, invOf_mul_self, Matrix.mul_one]
    have hL : V.transpose * ((U * ⅟V).transpose * W * (U * ⅟V)) * V =
        U.transpose * W * U := by
      calc
        V.transpose * ((U * ⅟V).transpose * W * (U * ⅟V)) * V =
            V.transpose * (U * ⅟V).transpose * W * ((U * ⅟V) * V) := by
              simp only [Matrix.mul_assoc]
        _ = ((U * ⅟V) * V).transpose * W * ((U * ⅟V) * V) := by
              rw [← Matrix.transpose_mul]
        _ = U.transpose * W * U := by
              simp [Matrix.mul_assoc]
    rw [hL] at h1
    exact h1

end MatrixDressing

section Family

variable {K V ι : Type*} [CommRing K] [AddCommGroup V] [Module K V]

/-- Every transport in a fixed-endpoint family dresses the seed equally iff every
relative holonomy `Uᵢ ∘ Uⱼ⁻¹` stabilizes the seed.

The index is the supplied family. No curvature hypothesis is used, and none is
produced: holonomy outside the stabilizer changes the dressing, while holonomy
inside it does not. -/
theorem all_pathDressing_independent_iff_holonomy_subset_stabilizer
    (U : ι → V ≃ₗ[K] V) (B : V →ₗ[K] V →ₗ[K] K) :
    (∀ i j,
        B.compl₁₂ (U i).toLinearMap (U i).toLinearMap =
          B.compl₁₂ (U j).toLinearMap (U j).toLinearMap) ↔
      (∀ i j,
        B.compl₁₂ ((U j).symm.trans (U i)).toLinearMap
            ((U j).symm.trans (U i)).toLinearMap = B) := by
  constructor
  · intro h i j
    ext a b
    have h1 := congrFun (congrArg DFunLike.coe (h i j)) ((U j).symm a)
    have h2 := congrFun (congrArg DFunLike.coe h1) ((U j).symm b)
    simpa [LinearMap.compl₁₂_apply, LinearEquiv.trans_apply] using h2
  · intro h i j
    ext a b
    have h1 := congrFun (congrArg DFunLike.coe (h i j)) ((U j) a)
    have h2 := congrFun (congrArg DFunLike.coe h1) ((U j) b)
    simpa [LinearMap.compl₁₂_apply, LinearEquiv.trans_apply,
      LinearEquiv.apply_symm_apply] using h2

end Family

/-! ## Explicit stabilizer exception and shear witness -/

/-- Orientation-preserving holonomy can move the transport and still fix the seed `I`. -/
theorem nontrivial_holonomy_can_preserve_seed :
    let R : Matrix (Fin 3) (Fin 3) ℚ := !![0, -1, 0; 1, 0, 0; 0, 0, 1]
    let S : Matrix (Fin 3) (Fin 3) ℚ := !![1, 0, 0; 0, 0, -1; 0, 1, 0]
    let U := R * S
    let V := S * R
    let H := U * V.transpose
    U ≠ V ∧ H ≠ 1 ∧ H.transpose * H = 1 ∧
      U.transpose * U = 1 ∧ V.transpose * V = 1 ∧
      Matrix.det R = 1 ∧ Matrix.det S = 1 := by
  native_decide

/-- Shears whose relative holonomy leaves the seed `I`. -/
theorem holonomy_outside_stabilizer_changes_dressing :
    let A : Matrix (Fin 2) (Fin 2) ℚ := !![1, 1; 0, 1]
    let B : Matrix (Fin 2) (Fin 2) ℚ := !![1, 0; 1, 1]
    let U := A * B
    let V := B * A
    U ≠ V ∧ U.transpose * (1 : Matrix (Fin 2) (Fin 2) ℚ) * U ≠
      V.transpose * (1 : Matrix (Fin 2) (Fin 2) ℚ) * V := by
  native_decide

/-! ## Full scalar closure kills a fixed nonzero kernel

`h_X = {G | G 1 = 0}` is imposed directly. This does not use a Lie-closure theorem.
-/

def preservesOnes {n : ℕ} {K : Type*} [AddCommMonoid K] (G : Matrix (Fin n) (Fin n) K) : Prop :=
  ∀ i, ∑ j, G i j = 0

def edgeGenerator {n : ℕ} {K : Type*} [DecidableEq (Fin n)] [Ring K]
    (p q : Fin n) : Matrix (Fin n) (Fin n) K :=
  fun a b =>
    (if a = p ∧ b = q then (1 : K) else 0) -
      (if a = p ∧ b = p then (1 : K) else 0)

theorem edgeGenerator_preservesOnes {n : ℕ} {K : Type*} [Ring K]
    (p q : Fin n) : preservesOnes (edgeGenerator (K := K) p q) := by
  intro i
  classical
  simp only [edgeGenerator]
  rw [Finset.sum_sub_distrib]
  have hleft :
      (∑ b : Fin n, if i = p ∧ b = q then (1 : K) else 0) =
        if i = p then 1 else 0 := by
    by_cases hip : i = p
    · simp [hip, Finset.mem_univ]
    · simp [hip]
  have hright :
      (∑ b : Fin n, if i = p ∧ b = p then (1 : K) else 0) =
        if i = p then 1 else 0 := by
    by_cases hip : i = p
    · simp [hip, Finset.mem_univ]
    · simp [hip]
  rw [hleft, hright]
  by_cases hip : i = p <;> simp [hip]

theorem fullScalarClosure_invariantBilinear_zero
    {n : ℕ} (hn : 2 ≤ n) {K : Type*} [Field K] (hchar : (2 : K) ≠ 0)
    (W : Matrix (Fin n) (Fin n) K)
    (hinv : ∀ G : Matrix (Fin n) (Fin n) K, preservesOnes G →
      G.transpose * W + W * G = 0) :
    W = 0 := by
  classical
  have entry : ∀ p q : Fin n, p ≠ q →
      ((if p = q then (1 : K) else 0) - 1) * W p p +
        W p p * ((if p = q then 1 else 0) - 1) = 0 ∧
      ((0 : K) - 1) * W p q + W p p * ((1 : K) - (if q = p then 1 else 0)) = 0 := by
    intro p q hpq
    have hG := hinv (edgeGenerator p q) (edgeGenerator_preservesOnes p q)
    have hmul : ∀ i k,
        ((W * edgeGenerator p q : Matrix (Fin n) (Fin n) K) i k) =
          W i p * ((if k = q then (1 : K) else 0) - (if k = p then 1 else 0)) ∧
        ((((edgeGenerator p q).transpose * W : Matrix (Fin n) (Fin n) K)) i k) =
          ((if i = q then (1 : K) else 0) - (if i = p then 1 else 0)) * W p k := by
      intro i k
      constructor
      · simp only [Matrix.mul_apply, edgeGenerator]
        have hterm : ∀ j,
            W i j * ((if j = p ∧ k = q then (1 : K) else 0) -
              (if j = p ∧ k = p then 1 else 0)) =
            if j = p then
              W i p * ((if k = q then 1 else 0) - (if k = p then 1 else 0))
            else 0 := by
          intro j
          by_cases hjp : j = p <;> simp [hjp]
        simp only [hterm]
        simp [Finset.mem_univ]
      · simp only [Matrix.mul_apply, Matrix.transpose_apply, edgeGenerator]
        have hterm : ∀ j,
            ((if j = p ∧ i = q then (1 : K) else 0) -
              (if j = p ∧ i = p then 1 else 0)) * W j k =
            if j = p then
              ((if i = q then 1 else 0) - (if i = p then 1 else 0)) * W p k
            else 0 := by
          intro j
          by_cases hjp : j = p <;> simp [hjp]
        simp only [hterm]
        simp [Finset.mem_univ]
    have hzero : ∀ i k,
        (((edgeGenerator p q).transpose * W + W * edgeGenerator p q :
            Matrix (Fin n) (Fin n) K) i k) = 0 := by
      intro i k
      simpa [Matrix.add_apply] using congrFun (congrFun hG i) k
    have hpk := congrFun (congrFun hG p) p
    have hqk := congrFun (congrFun hG p) q
    simp only [Matrix.add_apply, (hmul p p).1, (hmul p p).2] at hpk
    simp only [Matrix.add_apply, (hmul p q).1, (hmul p q).2] at hqk
    constructor
    · simpa [hpq] using hpk
    · simpa [hpq, eq_comm] using hqk
  have hdiag : ∀ p : Fin n, W p p = 0 := by
    intro p
    haveI : NeZero n := ⟨by omega⟩
    rcases (show ∃ q : Fin n, p ≠ q by
        by_cases hp : p = 0
        · refine ⟨1, ?_⟩
          rw [hp]
          intro h
          have hv := congrArg Fin.val h
          simp at hv
          omega
        · exact ⟨0, hp⟩) with ⟨q, hpq⟩
    have h := (entry p q hpq).1
    have h2 : (-2 : K) * W p p = 0 := by
      simp only [if_neg hpq, sub_eq_add_neg, zero_add, mul_comm] at h
      linear_combination h
    have hne : (-2 : K) ≠ 0 := by
      intro hzero
      apply hchar
      simpa using congrArg Neg.neg hzero
    rcases mul_eq_zero.mp h2 with hbad | hW
    · exact absurd hbad hne
    · exact hW
  ext i j
  by_cases hij : i = j
  · simp [hij, hdiag]
  · have h := (entry i j hij).2
    rw [hdiag i] at h
    simpa using h

/-! ## Flat plaquettes do not kill affine periods

Commuting constant translations have vanishing plaquette commutator.
The length-three power is still a nontrivial affine translation.
This is contractible flatness separated from global period triviality.
-/

theorem flat_plaquettes_do_not_force_trivial_periods :
    let Tx : Matrix (Fin 3) (Fin 3) ℚ := !![1, 0, 1; 0, 1, 0; 0, 0, 1]
    let Ty : Matrix (Fin 3) (Fin 3) ℚ := !![1, 0, 0; 0, 1, 1; 0, 0, 1]
    Tx * Ty = Ty * Tx ∧ Tx * Tx * Tx ≠ 1 := by
  native_decide

/-! ## Pointwise multiplication cannot match the staggered scalar tangent -/

def cycleShift3 (i : Fin 3) : Fin 3 := ⟨(i.val + 1) % 3, by omega⟩

def cycleUnshift3 (i : Fin 3) : Fin 3 := ⟨(i.val + 2) % 3, by omega⟩

/-- `e = Δ δ₀` on the 3-cycle, with `Δ = 3 (U - I)`. -/
def staggeredEdge3 : Fin 3 → ℚ :=
  fun i => (3 : ℚ) * ((if cycleShift3 i = 0 then 1 else 0) - (if i = 0 then 1 else 0))

/-- `H₀(e) = ½ (M_e U + U⁻¹ M_e)`. -/
def staggeredScalarTangent3 : Matrix (Fin 3) (Fin 3) ℚ :=
  fun i j =>
    (1 / 2 : ℚ) * (
      (if j = cycleShift3 i then staggeredEdge3 i else 0) +
      (if j = cycleUnshift3 i then staggeredEdge3 (cycleUnshift3 i) else 0))

def IsPointwiseMultiplication (M : Matrix (Fin 3) (Fin 3) ℚ) : Prop :=
  ∀ i j, i ≠ j → M i j = 0

theorem pointwiseKernel_cannot_realize_staggeredTangent :
    staggeredScalarTangent3 0 1 = (-3 / 2 : ℚ) ∧
      ¬ IsPointwiseMultiplication staggeredScalarTangent3 := by
  refine ⟨?_, ?_⟩
  · native_decide
  · intro h
    have h0 := h (0 : Fin 3) 1 (by decide)
    have hentry : staggeredScalarTangent3 0 1 = (-3 / 2 : ℚ) := by native_decide
    rw [hentry] at h0
    norm_num at h0

/-! ## Even period: centered solder is blind to the one-form tangent -/

lemma zmod_two_dichotomy : ∀ z : ZMod 2, z = 0 ∨ z = 1 := by
  decide

/-- `L = 2` Nyquist coframe along role `A`: values `(-2, 2)` on that axis. -/
def periodTwoNyquistCoframe : LocalCoframeField 0 :=
  fun y r a =>
    if r = A ∧ a = A then
      if y A = 0 then (-2 : ℝ) else 2
    else 0

lemma periodTwoNyquist_AA (y : ArchiveRolePhaseGroup 0) :
    periodTwoNyquistCoframe y A A =
      if y A = 0 then (-2 : ℝ) else 2 := by
  dsimp only [periodTwoNyquistCoframe]
  rw [if_pos (And.intro rfl rfl)]

lemma periodTwoNyquist_zero (y : ArchiveRolePhaseGroup 0) (hy : y A = 0) :
    periodTwoNyquistCoframe y A A = -2 := by
  rw [periodTwoNyquist_AA, if_pos hy]

lemma periodTwoNyquist_offZero (y : ArchiveRolePhaseGroup 0) (hy : y A ≠ 0) :
    periodTwoNyquistCoframe y A A = 2 := by
  rw [periodTwoNyquist_AA, if_neg hy]

theorem periodTwoNyquist_centeredCoframe_zero (x : ArchiveRolePhaseGroup 0) :
    centeredCoframeMatrix 0 periodTwoNyquistCoframe x = 0 := by
  ext r a
  by_cases hra : r = A ∧ a = A
  · rcases hra with ⟨rfl, rfl⟩
    have hcoord : roleTranslateMinus 0 A x A = x A + -1 := by
      rw [roleTranslateMinus_apply]
      simp only [Pi.sub_apply, roleStep, if_true, sub_eq_add_neg]
    rw [centeredCoframeMatrix_apply, backwardAverage_apply]
    rcases zmod_two_dichotomy (x A) with hx | hx
    · have hstep : roleTranslateMinus 0 A x A = 1 := by
        rw [hcoord, hx]
        simp only [archiveFibers]
        decide
      have hne : roleTranslateMinus 0 A x A ≠ 0 := by
        rw [hstep]
        intro h
        have hn : archiveFibers 0 = 1 := ZMod.one_eq_zero_iff.mp h
        simp [archiveFibers] at hn
      rw [periodTwoNyquist_zero x hx, periodTwoNyquist_offZero _ hne]
      norm_num
    · have hne : x A ≠ 0 := by
        rw [hx]
        simp only [archiveFibers]
        decide
      have hstep : roleTranslateMinus 0 A x A = 0 := by
        rw [hcoord, hx]
        simp only [archiveFibers]
        decide
      rw [periodTwoNyquist_offZero x hne, periodTwoNyquist_zero _ hstep]
      norm_num
  · rw [centeredCoframeMatrix_apply, backwardAverage_apply]
    have hzero : ∀ y, periodTwoNyquistCoframe y r a = 0 := by
      intro y
      simp only [periodTwoNyquistCoframe, if_neg hra]
    rw [hzero x, hzero (roleTranslateMinus 0 r x)]
    simp

theorem periodTwo_centeredSolder_constant (t : ℝ) (x : ArchiveRolePhaseGroup 0) :
    solderMetricMatrix 0 ((t : ℝ) • periodTwoNyquistCoframe) x = roleLorentzMetric := by
  have hC : centeredCoframeMatrix 0 ((t : ℝ) • periodTwoNyquistCoframe) x = 0 := by
    rw [centeredCoframeMatrix_smul, periodTwoNyquist_centeredCoframe_zero, smul_zero]
  rw [solderMetricMatrix, solderMatrix, hC, add_zero, roleLorentzMetric_transpose,
    roleLorentzMetric_sq, Matrix.one_mul]

/-- Any readout of the centered solder metric is constant on the Nyquist family,
while the one-form value `e(A,A)` is not. -/
theorem periodTwo_centeredMetric_blind_oneFormTangent
    (K : (ArchiveRolePhaseGroup 0 → Matrix Role Role ℝ) → ArchiveRolePhaseGroup 0 → ℝ)
    (hK : ∀ t x,
      K (fun y => solderMetricMatrix 0 ((t : ℝ) • periodTwoNyquistCoframe) y) x =
        ((t : ℝ) • periodTwoNyquistCoframe) x A A) :
    False := by
  let z0 : ArchiveRolePhaseGroup 0 := fun _ => 0
  have hfield :
      (fun y => solderMetricMatrix 0 ((0 : ℝ) • periodTwoNyquistCoframe) y) =
        fun y => solderMetricMatrix 0 ((1 : ℝ) • periodTwoNyquistCoframe) y := by
    funext y
    rw [periodTwo_centeredSolder_constant, periodTwo_centeredSolder_constant]
  have h0 := hK 0 z0
  have h1 := hK 1 z0
  rw [hfield] at h0
  have hsame : ((0 : ℝ) • periodTwoNyquistCoframe) z0 A A =
      ((1 : ℝ) • periodTwoNyquistCoframe) z0 A A := by
    rw [← h0, h1]
  simp [periodTwoNyquistCoframe, Pi.smul_apply, z0] at hsame

/-! ## Flat value and first jet do not fix the quadratic term -/

def flatJetExtension (α t : ℚ) (H : Matrix (Fin 2) (Fin 2) ℚ) :
    Matrix (Fin 2) (Fin 2) ℚ :=
  1 + t • H + (α * t ^ 2) • (H * H)

/-- Same value and same linear coefficient, distinct quadratic coefficient.
Members of the family are not claimed to be physical Hodge operators. -/
theorem flatFirstJet_extensions_not_unique :
    let H : Matrix (Fin 2) (Fin 2) ℚ := !![0, 1; 1, 0]
    flatJetExtension 0 0 H = 1 ∧
      flatJetExtension 1 0 H = 1 ∧
      (∀ t, flatJetExtension 0 t H = 1 + t • H) ∧
      (∀ t, flatJetExtension 1 t H = 1 + t • H + (t ^ 2) • (H * H)) ∧
      H * H ≠ 0 ∧
      flatJetExtension 0 1 H ≠ flatJetExtension 1 1 H := by
  dsimp
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · simp [flatJetExtension]
  · simp [flatJetExtension]
  · intro t
    ext i j
    fin_cases i <;> fin_cases j <;> simp [flatJetExtension]
  · intro t
    ext i j
    fin_cases i <;> fin_cases j <;> simp [flatJetExtension]
  · native_decide
  · native_decide

end D0.Geometry
