import Mathlib.Analysis.InnerProductSpace.ProdL2
import Mathlib.LinearAlgebra.Isomorphisms
import Mathlib.Tactic
import D0.Geometry.ArchiveExteriorFrameLift

/-!
# Rank-stratified relative A/e comparison span

Lean owner for the positive span/relation construction isolated by research PR #123.

The coefficient carrier is the finite Role-labelled Euclidean space
Role → ℝ. Local output-frame changes act on the target fibre, not on this
coefficient slot.

For synthesis maps B S : LabelCoeff →ₗ[ℝ] V, the generated relation records
the labelled pairs (B c, S c). The strict generator assignment descends to
range B exactly when ker B ≤ ker S. Without that condition there is still
a canonical partial comparison: project coefficients onto (ker B)ᗮ, then
apply S. The discarded kernel component is the exact vertical relative defect.

No raw-solder inverse, observer-dependent source, full-fibre extension, or
finite graded E dressing is introduced here.  This file is the formal owner
for the rank-stratified comparison layer only.
-/

namespace D0.Geometry.A4DRelativeAEComparisonSpan

open D0
open scoped InnerProductSpace

noncomputable section

/-- Coefficient space of the four labelled Role generators.

This has the canonical Euclidean/counting inner product inherited from the
finite function space. It is a label coefficient carrier, not the moving
Lorentz fibre. -/
abbrev LabelCoeff := EuclideanSpace ℝ Role

variable {V : Type*} [AddCommGroup V] [Module ℝ V]

/-- The combined labelled synthesis map c ↦ (B c, S c). -/
def pairSynthesis (B S : LabelCoeff →ₗ[ℝ] V) : LabelCoeff →ₗ[ℝ] V × V where
  toFun c := (B c, S c)
  map_add' x y := by simp
  map_smul' a x := by simp

/-- Generated relative A/e linear relation. -/
def comparisonRelation (B S : LabelCoeff →ₗ[ℝ] V) : Submodule ℝ (V × V) :=
  LinearMap.range (pairSynthesis B S)

/-- Actual affine-increment span. -/
def comparisonDomain (B : LabelCoeff →ₗ[ℝ] V) : Submodule ℝ V :=
  LinearMap.range B

/-- Label-relation kernel. -/
def coefficientKernel (B : LabelCoeff →ₗ[ℝ] V) : Submodule ℝ LabelCoeff :=
  LinearMap.ker B

/-- Counting-orthogonal complement of the coefficient kernel. -/
def coefficientComplement (B : LabelCoeff →ₗ[ℝ] V) : Submodule ℝ LabelCoeff :=
  (coefficientKernel B)ᗮ

/-- Vertical part of the generated relation. -/
def verticalDefect (B S : LabelCoeff →ₗ[ℝ] V) : Submodule ℝ V :=
  (LinearMap.ker B).map S

/-- A canonical element of range B represented by coefficient c. -/
def rangeElem (B : LabelCoeff →ₗ[ℝ] V) (c : LabelCoeff) : LinearMap.range B :=
  ⟨B c, ⟨c, rfl⟩⟩

@[simp]
theorem rangeElem_coe (B : LabelCoeff →ₗ[ℝ] V) (c : LabelCoeff) :
    (rangeElem B c : V) = B c :=
  rfl

/-! ## The generated relation and its vertical part -/

theorem zero_pair_mem_comparisonRelation_iff
    (B S : LabelCoeff →ₗ[ℝ] V) (v : V) :
    (0, v) ∈ comparisonRelation B S ↔ v ∈ verticalDefect B S := by
  constructor
  · rintro ⟨c, hc⟩
    have hB : B c = 0 := by
      simpa [pairSynthesis] using congrArg Prod.fst hc
    have hS : S c = v := by
      simpa [pairSynthesis] using congrArg Prod.snd hc
    exact ⟨c, LinearMap.mem_ker.mpr hB, hS⟩
  · rintro ⟨c, hc, rfl⟩
    refine ⟨c, ?_⟩
    ext
    · simpa [pairSynthesis] using LinearMap.mem_ker.mp hc
    · simp [pairSynthesis]

theorem verticalDefect_eq_bot_iff
    (B S : LabelCoeff →ₗ[ℝ] V) :
    verticalDefect B S = ⊥ ↔ LinearMap.ker B ≤ LinearMap.ker S := by
  constructor
  · intro h c hc
    rw [LinearMap.mem_ker]
    have hm : S c ∈ verticalDefect B S := ⟨c, hc, rfl⟩
    rw [h] at hm
    simpa using hm
  · intro h
    apply le_antisymm
    · rintro v ⟨c, hc, rfl⟩
      have hs : S c = 0 := LinearMap.mem_ker.mp (h hc)
      simpa [hs]
    · exact bot_le

/-! ## Strict span-map criterion -/

/-- A supplied strict comparison on range B calibrates every labelled
generator exactly. -/
def SpanCalibration (B S : LabelCoeff →ₗ[ℝ] V) : Prop :=
  ∃ J : LinearMap.range B →ₗ[ℝ] V, ∀ c : LabelCoeff, J (rangeElem B c) = S c

/-- The quotient-factor comparison under the exact kernel inclusion. -/
def factoredComparison (B S : LabelCoeff →ₗ[ℝ] V)
    (h : LinearMap.ker B ≤ LinearMap.ker S) :
    LinearMap.range B →ₗ[ℝ] V :=
  (Submodule.liftQ (LinearMap.ker B) S h).comp
    B.quotKerEquivRange.symm.toLinearMap

private theorem quotKerEquivRange_symm_rangeElem
    (B : LabelCoeff →ₗ[ℝ] V) (c : LabelCoeff) :
    B.quotKerEquivRange.symm (rangeElem B c) = Submodule.Quotient.mk c := by
  apply B.quotKerEquivRange.injective
  simp [rangeElem]

@[simp]
theorem factoredComparison_rangeElem
    (B S : LabelCoeff →ₗ[ℝ] V)
    (h : LinearMap.ker B ≤ LinearMap.ker S) (c : LabelCoeff) :
    factoredComparison B S h (rangeElem B c) = S c := by
  rw [factoredComparison, LinearMap.comp_apply]
  change (LinearMap.ker B).liftQ S h
      (B.quotKerEquivRange.symm (rangeElem B c)) = S c
  rw [quotKerEquivRange_symm_rangeElem]
  simp

theorem spanCalibration_iff_kernel_le
    (B S : LabelCoeff →ₗ[ℝ] V) :
    SpanCalibration B S ↔ LinearMap.ker B ≤ LinearMap.ker S := by
  constructor
  · rintro ⟨J, hJ⟩ c hc
    rw [LinearMap.mem_ker]
    have hrange : rangeElem B c = 0 := by
      apply Subtype.ext
      simpa [rangeElem] using LinearMap.mem_ker.mp hc
    have hcal := hJ c
    rw [hrange, map_zero] at hcal
    exact hcal.symm
  · intro h
    exact ⟨factoredComparison B S h, factoredComparison_rangeElem B S h⟩

theorem strictComparison_unique
    (B S : LabelCoeff →ₗ[ℝ] V)
    (J₁ J₂ : LinearMap.range B →ₗ[ℝ] V)
    (h₁ : ∀ c, J₁ (rangeElem B c) = S c)
    (h₂ : ∀ c, J₂ (rangeElem B c) = S c) :
    J₁ = J₂ := by
  ext u
  rcases u with ⟨u, c, rfl⟩
  exact (h₁ c).trans (h₂ c).symm

/-! ## Canonical quotient comparison -/

/-- S descends modulo the vertical defect even when it does not descend
literally to range B. -/
def quotientComparison (B S : LabelCoeff →ₗ[ℝ] V) :
    LinearMap.range B →ₗ[ℝ] V ⧸ verticalDefect B S :=
  ((LinearMap.ker B).mapQ (verticalDefect B S) S (by
      intro c hc
      exact ⟨c, hc, rfl⟩)).comp
    B.quotKerEquivRange.symm.toLinearMap

@[simp]
theorem quotientComparison_rangeElem
    (B S : LabelCoeff →ₗ[ℝ] V) (c : LabelCoeff) :
    quotientComparison B S (rangeElem B c) =
      Submodule.Quotient.mk (S c) := by
  rw [quotientComparison, LinearMap.comp_apply]
  change ((LinearMap.ker B).mapQ (verticalDefect B S) S _)
      (B.quotKerEquivRange.symm (rangeElem B c)) =
        Submodule.Quotient.mk (S c)
  rw [quotKerEquivRange_symm_rangeElem]
  simp

/-! ## Canonical counting-orthogonal representative -/

/-- Counting-orthogonal coefficient representative: projection onto
(ker B)ᗮ. -/
def coefficientRepresentative (B : LabelCoeff →ₗ[ℝ] V) :
    LabelCoeff →ₗ[ℝ] LabelCoeff :=
  (coefficientComplement B).starProjection.toLinearMap

/-- Complementary kernel component. -/
def kernelComponent (B : LabelCoeff →ₗ[ℝ] V) :
    LabelCoeff →ₗ[ℝ] LabelCoeff :=
  LinearMap.id - coefficientRepresentative B

theorem coefficientRepresentative_mem_orthogonal
    (B : LabelCoeff →ₗ[ℝ] V) (c : LabelCoeff) :
    coefficientRepresentative B c ∈ coefficientComplement B := by
  rw [coefficientRepresentative]
  exact Submodule.starProjection_apply_mem _ _

theorem kernelComponent_mem_kernel
    (B : LabelCoeff →ₗ[ℝ] V) (c : LabelCoeff) :
    kernelComponent B c ∈ LinearMap.ker B := by
  change c -
      (((LinearMap.ker B)ᗮ : Submodule ℝ LabelCoeff).starProjection c) ∈
        LinearMap.ker B
  rw [Submodule.starProjection_orthogonal_val]
  simpa only [sub_sub_cancel] using
    Submodule.starProjection_apply_mem (LinearMap.ker B) c

theorem B_coefficientRepresentative
    (B : LabelCoeff →ₗ[ℝ] V) (c : LabelCoeff) :
    B (coefficientRepresentative B c) = B c := by
  have hk := kernelComponent_mem_kernel B c
  have hz := LinearMap.mem_ker.mp hk
  have hsub : B c - B (coefficientRepresentative B c) = 0 := by
    simpa [kernelComponent, map_sub] using hz
  exact (sub_eq_zero.mp hsub).symm

/-- Apply S to the canonical coefficient representative. -/
def canonicalOnCoeff (B S : LabelCoeff →ₗ[ℝ] V) :
    LabelCoeff →ₗ[ℝ] V :=
  S.comp (coefficientRepresentative B)

/-- The canonical coefficient representative vanishes on ker B. -/
theorem coefficientRepresentative_eq_zero_of_mem_kernel
    (B : LabelCoeff →ₗ[ℝ] V) {c : LabelCoeff}
    (hc : c ∈ LinearMap.ker B) :
    coefficientRepresentative B c = 0 := by
  change
    (((LinearMap.ker B)ᗮ : Submodule ℝ LabelCoeff).starProjection c) = 0
  rw [Submodule.starProjection_orthogonal_val,
    Submodule.starProjection_eq_self_iff.mpr hc]
  simp

theorem kernel_le_canonicalOnCoeff_ker
    (B S : LabelCoeff →ₗ[ℝ] V) :
    LinearMap.ker B ≤ LinearMap.ker (canonicalOnCoeff B S) := by
  intro c hc
  rw [LinearMap.mem_ker]
  simp [canonicalOnCoeff, coefficientRepresentative_eq_zero_of_mem_kernel B hc]

/-- Canonical rank-stratified partial comparison on the actual span range B. -/
def canonicalComparison (B S : LabelCoeff →ₗ[ℝ] V) :
    LinearMap.range B →ₗ[ℝ] V :=
  (Submodule.liftQ (LinearMap.ker B) (canonicalOnCoeff B S)
      (kernel_le_canonicalOnCoeff_ker B S)).comp
    B.quotKerEquivRange.symm.toLinearMap

@[simp]
theorem canonicalComparison_rangeElem
    (B S : LabelCoeff →ₗ[ℝ] V) (c : LabelCoeff) :
    canonicalComparison B S (rangeElem B c) =
      S (coefficientRepresentative B c) := by
  rw [canonicalComparison, LinearMap.comp_apply]
  change (LinearMap.ker B).liftQ (canonicalOnCoeff B S) _
      (B.quotKerEquivRange.symm (rangeElem B c)) =
        S (coefficientRepresentative B c)
  rw [quotKerEquivRange_symm_rangeElem]
  simp [canonicalOnCoeff]

/-- Exact vertical relative defect. -/
def canonicalResidual (B S : LabelCoeff →ₗ[ℝ] V) :
    LabelCoeff →ₗ[ℝ] V :=
  S.comp (kernelComponent B)

theorem canonicalResidual_mem_vertical
    (B S : LabelCoeff →ₗ[ℝ] V) (c : LabelCoeff) :
    canonicalResidual B S c ∈ verticalDefect B S := by
  exact ⟨kernelComponent B c, kernelComponent_mem_kernel B c, rfl⟩

theorem synthesis_eq_comparison_add_residual
    (B S : LabelCoeff →ₗ[ℝ] V) (c : LabelCoeff) :
    S c =
      canonicalComparison B S (rangeElem B c) + canonicalResidual B S c := by
  rw [canonicalComparison_rangeElem]
  simp only [canonicalResidual, kernelComponent, LinearMap.comp_apply,
    LinearMap.sub_apply, LinearMap.id_apply, map_sub]
  abel

theorem canonicalResidual_eq_zero_of_kernel_le
    (B S : LabelCoeff →ₗ[ℝ] V)
    (h : LinearMap.ker B ≤ LinearMap.ker S) :
    canonicalResidual B S = 0 := by
  apply LinearMap.ext
  intro c
  have hk := h (kernelComponent_mem_kernel B c)
  simpa [canonicalResidual] using LinearMap.mem_ker.mp hk

theorem canonicalComparison_calibrates_of_kernel_le
    (B S : LabelCoeff →ₗ[ℝ] V)
    (h : LinearMap.ker B ≤ LinearMap.ker S)
    (c : LabelCoeff) :
    canonicalComparison B S (rangeElem B c) = S c := by
  have hr := congrArg (fun f : LabelCoeff →ₗ[ℝ] V => f c)
    (canonicalResidual_eq_zero_of_kernel_le B S h)
  rw [synthesis_eq_comparison_add_residual B S c]
  simpa using hr

/-! ## Output-frame covariance -/

/-- An invertible output-frame map does not change coefficient relations. -/
theorem ker_frame_comp
    (g : V ≃ₗ[ℝ] V) (B : LabelCoeff →ₗ[ℝ] V) :
    LinearMap.ker (g.toLinearMap.comp B) = LinearMap.ker B := by
  ext c
  simp [LinearMap.mem_ker]

/-- The counting-orthogonal coefficient representative is output-frame
independent. -/
theorem coefficientRepresentative_frame
    (g : V ≃ₗ[ℝ] V) (B : LabelCoeff →ₗ[ℝ] V) :
    coefficientRepresentative (g.toLinearMap.comp B) =
      coefficientRepresentative B := by
  apply LinearMap.ext
  intro c
  simp [coefficientRepresentative, coefficientComplement, coefficientKernel,
    ker_frame_comp]

/-- Generator-level covariance of the canonical partial comparison. -/
theorem canonicalComparison_frame_rangeElem
    (g : V ≃ₗ[ℝ] V) (B S : LabelCoeff →ₗ[ℝ] V) (c : LabelCoeff) :
    canonicalComparison (g.toLinearMap.comp B) (g.toLinearMap.comp S)
        (rangeElem (g.toLinearMap.comp B) c) =
      g (canonicalComparison B S (rangeElem B c)) := by
  rw [canonicalComparison_rangeElem, canonicalComparison_rangeElem,
    coefficientRepresentative_frame]
  rfl

/-- The vertical relative defect transforms in the output fibre. -/
theorem canonicalResidual_frame
    (g : V ≃ₗ[ℝ] V) (B S : LabelCoeff →ₗ[ℝ] V) (c : LabelCoeff) :
    canonicalResidual (g.toLinearMap.comp B) (g.toLinearMap.comp S) c =
      g (canonicalResidual B S c) := by
  simp [canonicalResidual, kernelComponent, coefficientRepresentative_frame,
    LinearMap.comp_apply]

/-- Relation-as-graph and strict span calibration are the same kernel
condition. -/
theorem spanCalibration_iff_verticalDefect_eq_bot
    (B S : LabelCoeff →ₗ[ℝ] V) :
    SpanCalibration B S ↔ verticalDefect B S = ⊥ := by
  rw [spanCalibration_iff_kernel_le, verticalDefect_eq_bot_iff]

/-! ## Exact gauge specialization -/

theorem canonicalComparison_comp_self
    (B : LabelCoeff →ₗ[ℝ] V) (T : V →ₗ[ℝ] V) (c : LabelCoeff) :
    canonicalComparison B (T.comp B) (rangeElem B c) = T (B c) := by
  rw [canonicalComparison_rangeElem, LinearMap.comp_apply,
    B_coefficientRepresentative]

theorem verticalDefect_comp_self_eq_bot
    (B : LabelCoeff →ₗ[ℝ] V) (T : V →ₗ[ℝ] V) :
    verticalDefect B (T.comp B) = ⊥ := by
  rw [verticalDefect_eq_bot_iff]
  intro c hc
  rw [LinearMap.mem_ker, LinearMap.comp_apply]
  simp [LinearMap.mem_ker.mp hc]

/-! ## Exact controls -/

theorem zero_synthesis_vertical_zero :
    verticalDefect (0 : LabelCoeff →ₗ[ℝ] RoleSpace) 0 = ⊥ := by
  simp [verticalDefect]

theorem zero_synthesis_canonical_zero :
    canonicalResidual (0 : LabelCoeff →ₗ[ℝ] RoleSpace) 0 = 0 := by
  apply canonicalResidual_eq_zero_of_kernel_le
  simp

/-- A coframe-only/vertical relation has zero affine domain and keeps the
entire solder synthesis in the vertical defect. -/
theorem zero_B_verticalDefect
    (S : LabelCoeff →ₗ[ℝ] RoleSpace) :
    verticalDefect 0 S = LinearMap.range S := by
  ext v
  constructor
  · rintro ⟨c, _, rfl⟩
    exact ⟨c, rfl⟩
  · rintro ⟨c, rfl⟩
    exact ⟨c, by simp, rfl⟩

/-- No strict generator calibration exists for B=0 when S is nonzero. -/
theorem zero_B_no_strict_calibration
    (S : LabelCoeff →ₗ[ℝ] RoleSpace) (hS : S ≠ 0) :
    ¬ SpanCalibration 0 S := by
  rw [spanCalibration_iff_kernel_le]
  intro h
  apply hS
  apply LinearMap.ext
  intro c
  have hc : c ∈ LinearMap.ker (0 : LabelCoeff →ₗ[ℝ] RoleSpace) := by simp
  exact LinearMap.mem_ker.mp (h hc)

/-! ## Duplicate-generator and rank-jump controls -/

/-- Role-coordinate functional on the Euclidean label coefficient space. -/
def coeffRole (r : Role) : LabelCoeff →ₗ[ℝ] ℝ where
  toFun c := c r
  map_add' x y := by rfl
  map_smul' a x := by rfl

/-- One-generator rank-jump affine synthesis. -/
def rankJumpB (t : ℝ) : LabelCoeff →ₗ[ℝ] ℝ :=
  t • coeffRole A

/-- One-generator solder synthesis retained at the rank drop. -/
def rankJumpS : LabelCoeff →ₗ[ℝ] ℝ :=
  coeffRole A

theorem rankJump_strict_of_ne_zero (t : ℝ) (ht : t ≠ 0) :
    SpanCalibration (rankJumpB t) rankJumpS := by
  rw [spanCalibration_iff_kernel_le]
  intro c hc
  have hbc : t * c A = 0 := by
    simpa [rankJumpB, coeffRole] using LinearMap.mem_ker.mp hc
  have hca : c A = 0 := (mul_eq_zero.mp hbc).resolve_left ht
  exact LinearMap.mem_ker.mpr (by simpa [rankJumpS, coeffRole] using hca)

theorem rankJump_zero_vertical_relation :
    (0, (1 : ℝ)) ∈ comparisonRelation (rankJumpB 0) rankJumpS := by
  refine ⟨EuclideanSpace.single A 1, ?_⟩
  ext
  · simp [pairSynthesis, rankJumpB, coeffRole, EuclideanSpace.single_apply]
  · simp [pairSynthesis, rankJumpS, coeffRole, EuclideanSpace.single_apply]

theorem rankJump_zero_no_strict :
    ¬ SpanCalibration (rankJumpB 0) rankJumpS := by
  rw [spanCalibration_iff_kernel_le]
  intro h
  let eA : LabelCoeff := EuclideanSpace.single A 1
  have hk : eA ∈ LinearMap.ker (rankJumpB 0) := by
    rw [LinearMap.mem_ker]
    simp [eA, rankJumpB, coeffRole, EuclideanSpace.single_apply]
  have hs := LinearMap.mem_ker.mp (h hk)
  have hone : rankJumpS eA = 1 := by
    simp [eA, rankJumpS, coeffRole, EuclideanSpace.single_apply]
  rw [hone] at hs
  norm_num at hs

/-- Two labels synthesize the same affine increment but opposite solder
outputs. -/
def duplicateB : LabelCoeff →ₗ[ℝ] ℝ :=
  coeffRole A + coeffRole B

def duplicateS : LabelCoeff →ₗ[ℝ] ℝ :=
  coeffRole A - coeffRole B

theorem duplicate_generator_vertical_relation :
    (0, (2 : ℝ)) ∈ comparisonRelation duplicateB duplicateS := by
  let c : LabelCoeff :=
    EuclideanSpace.single A 1 - EuclideanSpace.single B 1
  refine ⟨c, ?_⟩
  ext
  · simp [pairSynthesis, duplicateB, coeffRole, c, EuclideanSpace.single_apply,
      show A ≠ B by decide, show B ≠ A by decide]
  · simp [pairSynthesis, duplicateS, coeffRole, c,
      show A ≠ B by decide, show B ≠ A by decide] <;> norm_num

theorem duplicate_generator_no_strict :
    ¬ SpanCalibration duplicateB duplicateS := by
  rw [spanCalibration_iff_kernel_le]
  intro h
  let c : LabelCoeff :=
    EuclideanSpace.single A 1 - EuclideanSpace.single B 1
  have hk : c ∈ LinearMap.ker duplicateB := by
    rw [LinearMap.mem_ker]
    simp [duplicateB, coeffRole, c, EuclideanSpace.single_apply,
      show A ≠ B by decide, show B ≠ A by decide]
  have hs := LinearMap.mem_ker.mp (h hk)
  have htwo : duplicateS c = 2 := by
    simp [duplicateS, coeffRole, c,
      show A ≠ B by decide, show B ≠ A by decide] <;> norm_num
  rw [htwo] at hs
  norm_num at hs

/-! ## Full-extension firewall -/

/-- At zero affine span, two distinct full-fibre endomorphisms agree on every
actual affine increment. Hence a full extension is not determined by the
span data. -/
theorem zero_span_full_extension_nonunique :
    (0 : RoleSpace →ₗ[ℝ] RoleSpace) ≠ LinearMap.id ∧
      ∀ c : LabelCoeff,
        (0 : RoleSpace →ₗ[ℝ] RoleSpace)
            ((0 : LabelCoeff →ₗ[ℝ] RoleSpace) c) =
          (LinearMap.id : RoleSpace →ₗ[ℝ] RoleSpace)
            ((0 : LabelCoeff →ₗ[ℝ] RoleSpace) c) := by
  constructor
  · intro h
    have hfun := congrArg
      (fun T : RoleSpace →ₗ[ℝ] RoleSpace => T (archiveRoleBasis A)) h
    have hcoord := congrArg (fun v : RoleSpace => v A) hfun
    simpa [archiveRoleBasis, Pi.basisFun_apply] using hcoord
  · intro c
    simp

end
end D0.Geometry.A4DRelativeAEComparisonSpan
