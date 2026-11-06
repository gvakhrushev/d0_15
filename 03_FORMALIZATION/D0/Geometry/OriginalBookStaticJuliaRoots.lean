import D0.Geometry.OriginalBookAnalyticBoost
import Mathlib.Analysis.Matrix.Order


/-!
# Original Book static Julia roots

The precise source is `check_uniform_book_source.py`, blob
`ee8de4635d24c668949ac9a0186616ab7d59f2ed`, lines 77–87, and its
modular checker `check_future_even_algebra_modprime.py`, blob
`d111c5bfeae3c384a4fe725f4a6d19277ea0005a`, lines 144–157, both at
commit eebcb5e467742df3e9cf7fa9702042d7294aa742. The upstream routine
uses positive square roots, so this file establishes positive definiteness
and identifies the principal CFC square root, not merely a square identity.

For every role, the base operand has scale nu=3/5 and left/right roots
`I - c c†/5`, `I - c† c/5`. For the source's actual phased input, these
are also its roots when the role is A, B or C (`r ≠ D`), because the boost
is applied only at D. The two moved D roots, 128 Kraus operators, effect
span, execution admission and physical interpretation remain open.
-/

namespace D0.Geometry.OriginalBookStaticRoots
open D0
open OriginalBookBoost
open OriginalBookCreatorBridge
open CubicExponential
open scoped MatrixOrder

def creatorInt (r : Role) : SourceMatrix := sourceCreatorMatrix r

def sourceIntCAR (r : Role) : SourceMatrix :=
  creatorInt r * (creatorInt r).transpose + (creatorInt r).transpose * creatorInt r

set_option maxRecDepth 100000 in
private theorem sourceCAR_ket0 : ∀ (r : Role) (bra : Fin 16),
    sourceIntCAR r bra (0 : Fin 16) = (1 : SourceMatrix) bra (0 : Fin 16) ∧
    (creatorInt r * creatorInt r) bra (0 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem sourceCAR_ket1 : ∀ (r : Role) (bra : Fin 16),
    sourceIntCAR r bra (1 : Fin 16) = (1 : SourceMatrix) bra (1 : Fin 16) ∧
    (creatorInt r * creatorInt r) bra (1 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem sourceCAR_ket2 : ∀ (r : Role) (bra : Fin 16),
    sourceIntCAR r bra (2 : Fin 16) = (1 : SourceMatrix) bra (2 : Fin 16) ∧
    (creatorInt r * creatorInt r) bra (2 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem sourceCAR_ket3 : ∀ (r : Role) (bra : Fin 16),
    sourceIntCAR r bra (3 : Fin 16) = (1 : SourceMatrix) bra (3 : Fin 16) ∧
    (creatorInt r * creatorInt r) bra (3 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem sourceCAR_ket4 : ∀ (r : Role) (bra : Fin 16),
    sourceIntCAR r bra (4 : Fin 16) = (1 : SourceMatrix) bra (4 : Fin 16) ∧
    (creatorInt r * creatorInt r) bra (4 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem sourceCAR_ket5 : ∀ (r : Role) (bra : Fin 16),
    sourceIntCAR r bra (5 : Fin 16) = (1 : SourceMatrix) bra (5 : Fin 16) ∧
    (creatorInt r * creatorInt r) bra (5 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem sourceCAR_ket6 : ∀ (r : Role) (bra : Fin 16),
    sourceIntCAR r bra (6 : Fin 16) = (1 : SourceMatrix) bra (6 : Fin 16) ∧
    (creatorInt r * creatorInt r) bra (6 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem sourceCAR_ket7 : ∀ (r : Role) (bra : Fin 16),
    sourceIntCAR r bra (7 : Fin 16) = (1 : SourceMatrix) bra (7 : Fin 16) ∧
    (creatorInt r * creatorInt r) bra (7 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem sourceCAR_ket8 : ∀ (r : Role) (bra : Fin 16),
    sourceIntCAR r bra (8 : Fin 16) = (1 : SourceMatrix) bra (8 : Fin 16) ∧
    (creatorInt r * creatorInt r) bra (8 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem sourceCAR_ket9 : ∀ (r : Role) (bra : Fin 16),
    sourceIntCAR r bra (9 : Fin 16) = (1 : SourceMatrix) bra (9 : Fin 16) ∧
    (creatorInt r * creatorInt r) bra (9 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem sourceCAR_ket10 : ∀ (r : Role) (bra : Fin 16),
    sourceIntCAR r bra (10 : Fin 16) = (1 : SourceMatrix) bra (10 : Fin 16) ∧
    (creatorInt r * creatorInt r) bra (10 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem sourceCAR_ket11 : ∀ (r : Role) (bra : Fin 16),
    sourceIntCAR r bra (11 : Fin 16) = (1 : SourceMatrix) bra (11 : Fin 16) ∧
    (creatorInt r * creatorInt r) bra (11 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem sourceCAR_ket12 : ∀ (r : Role) (bra : Fin 16),
    sourceIntCAR r bra (12 : Fin 16) = (1 : SourceMatrix) bra (12 : Fin 16) ∧
    (creatorInt r * creatorInt r) bra (12 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem sourceCAR_ket13 : ∀ (r : Role) (bra : Fin 16),
    sourceIntCAR r bra (13 : Fin 16) = (1 : SourceMatrix) bra (13 : Fin 16) ∧
    (creatorInt r * creatorInt r) bra (13 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem sourceCAR_ket14 : ∀ (r : Role) (bra : Fin 16),
    sourceIntCAR r bra (14 : Fin 16) = (1 : SourceMatrix) bra (14 : Fin 16) ∧
    (creatorInt r * creatorInt r) bra (14 : Fin 16) = 0 := by
  decide

set_option maxRecDepth 100000 in
private theorem sourceCAR_ket15 : ∀ (r : Role) (bra : Fin 16),
    sourceIntCAR r bra (15 : Fin 16) = (1 : SourceMatrix) bra (15 : Fin 16) ∧
    (creatorInt r * creatorInt r) bra (15 : Fin 16) = 0 := by
  decide

theorem sourceIntCAR_eq_one (r : Role) : sourceIntCAR r = 1 := by
  ext bra ket
  fin_cases ket
  · exact (sourceCAR_ket0 r bra).1
  · exact (sourceCAR_ket1 r bra).1
  · exact (sourceCAR_ket2 r bra).1
  · exact (sourceCAR_ket3 r bra).1
  · exact (sourceCAR_ket4 r bra).1
  · exact (sourceCAR_ket5 r bra).1
  · exact (sourceCAR_ket6 r bra).1
  · exact (sourceCAR_ket7 r bra).1
  · exact (sourceCAR_ket8 r bra).1
  · exact (sourceCAR_ket9 r bra).1
  · exact (sourceCAR_ket10 r bra).1
  · exact (sourceCAR_ket11 r bra).1
  · exact (sourceCAR_ket12 r bra).1
  · exact (sourceCAR_ket13 r bra).1
  · exact (sourceCAR_ket14 r bra).1
  · exact (sourceCAR_ket15 r bra).1

theorem creatorInt_sq_zero (r : Role) : creatorInt r * creatorInt r = 0 := by
  ext bra ket
  fin_cases ket
  · exact (sourceCAR_ket0 r bra).2
  · exact (sourceCAR_ket1 r bra).2
  · exact (sourceCAR_ket2 r bra).2
  · exact (sourceCAR_ket3 r bra).2
  · exact (sourceCAR_ket4 r bra).2
  · exact (sourceCAR_ket5 r bra).2
  · exact (sourceCAR_ket6 r bra).2
  · exact (sourceCAR_ket7 r bra).2
  · exact (sourceCAR_ket8 r bra).2
  · exact (sourceCAR_ket9 r bra).2
  · exact (sourceCAR_ket10 r bra).2
  · exact (sourceCAR_ket11 r bra).2
  · exact (sourceCAR_ket12 r bra).2
  · exact (sourceCAR_ket13 r bra).2
  · exact (sourceCAR_ket14 r bra).2
  · exact (sourceCAR_ket15 r bra).2

end D0.Geometry.OriginalBookStaticRoots



open scoped MatrixOrder ComplexOrder
open Matrix

namespace D0.Geometry.OriginalBookStaticRoots

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- The original 3/5 contraction has the positive defect root 1-P/5
for every Hermitian projection P. -/
theorem projection_root (p : Matrix n n ℂ) (hh : pᴴ = p) (hp : p * p = p) :
    CFC.sqrt (1 - (9 / 25 : ℝ) • p) = 1 - (1 / 5 : ℝ) • p := by
  have hn : 0 ≤ p := by
    have h := (Matrix.posSemidef_conjTranspose_mul_self p).nonneg
    simpa [hh, hp] using h
  have hq : (1 - p) * (1 - p) = 1 - p := by
    simp [sub_mul, mul_sub, hp]
  have hqn : 0 ≤ (1 - p) := by
    have h := (Matrix.posSemidef_conjTranspose_mul_self (1 - p)).nonneg
    simpa [Matrix.conjTranspose_sub, hh, hq] using h
  have hroot : 0 ≤ (1 - (1 / 5 : ℝ) • p) := by
    have he : 1 - (1 / 5 : ℝ) • p = (4 / 5 : ℝ) • p + (1 - p) := by module
    rw [he]
    exact add_nonneg (smul_nonneg (by norm_num) hn) hqn
  apply CFC.sqrt_unique _ hroot
  simp only [sub_mul, mul_sub, one_mul, mul_one, smul_mul_assoc, mul_smul_comm, hp]
  module

/-- The source's root is strictly positive, with an explicit inverse. -/
theorem projection_root_posDef (p : Matrix n n ℂ) (hh : pᴴ = p) (hp : p * p = p) :
    (1 - (1 / 5 : ℝ) • p).PosDef := by
  have hn : 0 ≤ (1 - (1 / 5 : ℝ) • p) := by
    rw [← projection_root p hh hp]
    exact CFC.sqrt_nonneg _
  have h1 : (1 - (1 / 5 : ℝ) • p) * (1 + (1 / 4 : ℝ) • p) = 1 := by
    simp only [sub_mul, mul_add, one_mul, mul_one, smul_mul_assoc, mul_smul_comm, hp]
    module
  have h2 : (1 + (1 / 4 : ℝ) • p) * (1 - (1 / 5 : ℝ) • p) = 1 := by
    simp only [add_mul, mul_sub, one_mul, mul_one, smul_mul_assoc, mul_smul_comm, hp]
    module
  have hu : IsUnit (1 - (1 / 5 : ℝ) • p) :=
    ⟨⟨1 - (1 / 5 : ℝ) • p, 1 + (1 / 4 : ℝ) • p, h1, h2⟩, rfl⟩
  exact hn.posSemidef.posDef_iff_isUnit.mpr hu

/-- Thus the argument tested by upstream's positive-root routine is positive definite. -/
theorem projection_defect_posDef (p : Matrix n n ℂ) (hh : pᴴ = p) (hp : p * p = p) :
    (1 - (9 / 25 : ℝ) • p).PosDef := by
  let b : Matrix n n ℂ := 1 - (1 / 5 : ℝ) • p
  have hb : b.PosDef := projection_root_posDef p hh hp
  have hs : b * b = 1 - (9 / 25 : ℝ) • p := by
    dsimp [b]
    simp only [sub_mul, mul_sub, one_mul, mul_one, smul_mul_assoc, mul_smul_comm, hp]
    module
  have hpos : (b * b).PosSemidef := by
    have h := Matrix.posSemidef_conjTranspose_mul_self b
    have hbH : bᴴ = b := hb.isHermitian
    rw [hbH] at h
    exact h
  rw [← hs]
  exact hpos.posDef_iff_isUnit.mpr (hb.isUnit.mul hb.isUnit)


open D0
open OriginalBookBoost

lemma creatorComplex_conjTranspose (r : Role) :
    (creatorInt r).transpose.map (Int.castRingHom ℂ) =
      (sourceCreatorComplex r).conjTranspose := by
  ext i j
  simp [creatorInt, sourceCreatorComplex, Matrix.conjTranspose_apply]

lemma creatorComplex_car (r : Role) :
    sourceCreatorComplex r * (sourceCreatorComplex r).conjTranspose +
      (sourceCreatorComplex r).conjTranspose * sourceCreatorComplex r = 1 := by
  ext i j
  have h := congrArg (fun z : ℤ => (z : ℂ))
    (congrFun (congrFun (sourceIntCAR_eq_one r) i) j)
  by_cases hij : i = j <;>
    simpa [sourceIntCAR, creatorInt, sourceCreatorComplex, Matrix.mul_apply,
      Matrix.conjTranspose_apply, Matrix.one_apply, hij] using h

lemma creatorComplex_nil (r : Role) : sourceCreatorComplex r * sourceCreatorComplex r = 0 := by
  have h := congrArg (fun m : SourceMatrix => m.map (Int.castRingHom ℂ)) (creatorInt_sq_zero r)
  change ((creatorInt r * creatorInt r).map (Int.castRingHom ℂ)) =
    (0 : SourceMatrix).map (Int.castRingHom ℂ) at h
  rw [Matrix.map_mul] at h
  simpa [sourceCreatorComplex, creatorInt] using h

lemma projection_of_car (c : Matrix (Fin 16) (Fin 16) ℂ)
    (hc : c * cᴴ + cᴴ * c = 1) (hn : c * c = 0) :
    (c * cᴴ) * (c * cᴴ) = c * cᴴ := by
  have hq : cᴴ * c = 1 - c * cᴴ := by rw [← hc]; noncomm_ring
  calc
    (c * cᴴ) * (c * cᴴ) = c * (cᴴ * c) * cᴴ := by noncomm_ring
    _ = c * (1 - c * cᴴ) * cᴴ := by rw [hq]
    _ = c * cᴴ - (c * c) * (cᴴ * cᴴ) := by noncomm_ring
    _ = c * cᴴ := by rw [hn, zero_mul, sub_zero]

lemma creatorComplex_nil_adjoint (r : Role) :
    (sourceCreatorComplex r)ᴴ * (sourceCreatorComplex r)ᴴ = 0 := by
  have h := congrArg Matrix.conjTranspose (creatorComplex_nil r)
  simpa [Matrix.conjTranspose_mul] using h

noncomputable def leftProjection (r : Role) : Matrix (Fin 16) (Fin 16) ℂ :=
  sourceCreatorComplex r * (sourceCreatorComplex r)ᴴ

noncomputable def rightProjection (r : Role) : Matrix (Fin 16) (Fin 16) ℂ :=
  (sourceCreatorComplex r)ᴴ * sourceCreatorComplex r

lemma leftProjection_sq (r : Role) : leftProjection r * leftProjection r = leftProjection r := by
  exact projection_of_car _ (creatorComplex_car r) (creatorComplex_nil r)

lemma rightProjection_sq (r : Role) : rightProjection r * rightProjection r = rightProjection r := by
  have hc : (sourceCreatorComplex r)ᴴ * ((sourceCreatorComplex r)ᴴ)ᴴ +
      ((sourceCreatorComplex r)ᴴ)ᴴ * (sourceCreatorComplex r)ᴴ = 1 := by
    simpa [add_comm] using creatorComplex_car r
  have h := projection_of_car ((sourceCreatorComplex r)ᴴ) hc (creatorComplex_nil_adjoint r)
  simpa [rightProjection] using h

lemma leftProjection_hermitian (r : Role) : (leftProjection r)ᴴ = leftProjection r := by
  simp [leftProjection, Matrix.conjTranspose_mul]

lemma rightProjection_hermitian (r : Role) : (rightProjection r)ᴴ = rightProjection r := by
  simp [rightProjection, Matrix.conjTranspose_mul]

noncomputable def sourceBase (r : Role) : Matrix (Fin 16) (Fin 16) ℂ :=
  (3 / 5 : ℝ) • sourceCreatorComplex r

lemma sourceBase_left (r : Role) :
    sourceBase r * (sourceBase r)ᴴ = (9 / 25 : ℝ) • leftProjection r := by
  simp [sourceBase, leftProjection, Matrix.conjTranspose_smul, smul_smul]
  norm_num

lemma sourceBase_right (r : Role) :
    (sourceBase r)ᴴ * sourceBase r = (9 / 25 : ℝ) • rightProjection r := by
  simp [sourceBase, rightProjection, Matrix.conjTranspose_smul, smul_smul]
  norm_num

theorem baseline_left_root (r : Role) :
    CFC.sqrt (1 - sourceBase r * (sourceBase r)ᴴ) =
      1 - (1 / 5 : ℝ) • leftProjection r := by
  rw [sourceBase_left]
  exact projection_root _ (leftProjection_hermitian r) (leftProjection_sq r)

theorem baseline_right_root (r : Role) :
    CFC.sqrt (1 - (sourceBase r)ᴴ * sourceBase r) =
      1 - (1 / 5 : ℝ) • rightProjection r := by
  rw [sourceBase_right]
  exact projection_root _ (rightProjection_hermitian r) (rightProjection_sq r)

theorem baseline_left_defect_posDef (r : Role) :
    (1 - sourceBase r * (sourceBase r)ᴴ).PosDef := by
  rw [sourceBase_left]
  exact projection_defect_posDef _ (leftProjection_hermitian r) (leftProjection_sq r)

theorem baseline_right_defect_posDef (r : Role) :
    (1 - (sourceBase r)ᴴ * sourceBase r).PosDef := by
  rw [sourceBase_right]
  exact projection_defect_posDef _ (rightProjection_hermitian r) (rightProjection_sq r)

lemma sourceRolePhase_unit (r : Role) :
    star (sourceRolePhase r) * sourceRolePhase r = 1 := by
  rcases r with ⟨a, b⟩
  fin_cases a <;> fin_cases b <;>
    norm_num [sourceRolePhase, D0.A, D0.B, D0.C, D0.D, Complex.I_mul_I]

lemma static_operand_eq_phase_base (r : Role) (hr : r ≠ D0.D) :
    CubicExponential.sourceAnalyticOperand r = sourceRolePhase r • sourceBase r := by
  ext i j
  simp [CubicExponential.sourceAnalyticOperand, sourceBase, hr, Complex.real_smul]

lemma static_operand_left (r : Role) (hr : r ≠ D0.D) :
    CubicExponential.sourceAnalyticOperand r * (CubicExponential.sourceAnalyticOperand r)ᴴ =
      sourceBase r * (sourceBase r)ᴴ := by
  rw [static_operand_eq_phase_base r hr]
  have hu : (starRingEnd ℂ) (sourceRolePhase r) * sourceRolePhase r = 1 :=
    sourceRolePhase_unit r
  simp [Matrix.conjTranspose_smul, smul_smul, hu]

lemma static_operand_right (r : Role) (hr : r ≠ D0.D) :
    (CubicExponential.sourceAnalyticOperand r)ᴴ * CubicExponential.sourceAnalyticOperand r =
      (sourceBase r)ᴴ * sourceBase r := by
  rw [static_operand_eq_phase_base r hr]
  have hu : sourceRolePhase r * (starRingEnd ℂ) (sourceRolePhase r) = 1 := by
    simpa [mul_comm] using sourceRolePhase_unit r
  simp [Matrix.conjTranspose_smul, smul_smul, hu]

theorem static_operand_left_root (r : Role) (hr : r ≠ D0.D) :
    CFC.sqrt (1 - CubicExponential.sourceAnalyticOperand r *
      (CubicExponential.sourceAnalyticOperand r)ᴴ) =
      1 - (1 / 5 : ℝ) • leftProjection r := by
  rw [static_operand_left r hr]
  exact baseline_left_root r

theorem static_operand_right_root (r : Role) (hr : r ≠ D0.D) :
    CFC.sqrt (1 - (CubicExponential.sourceAnalyticOperand r)ᴴ *
      CubicExponential.sourceAnalyticOperand r) =
      1 - (1 / 5 : ℝ) • rightProjection r := by
  rw [static_operand_right r hr]
  exact baseline_right_root r

theorem static_operand_left_defect_posDef (r : Role) (hr : r ≠ D0.D) :
    (1 - CubicExponential.sourceAnalyticOperand r *
      (CubicExponential.sourceAnalyticOperand r)ᴴ).PosDef := by
  rw [static_operand_left r hr]
  exact baseline_left_defect_posDef r

theorem static_operand_right_defect_posDef (r : Role) (hr : r ≠ D0.D) :
    (1 - (CubicExponential.sourceAnalyticOperand r)ᴴ *
      CubicExponential.sourceAnalyticOperand r).PosDef := by
  rw [static_operand_right r hr]
  exact baseline_right_defect_posDef r

end D0.Geometry.OriginalBookStaticRoots
