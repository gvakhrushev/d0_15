import D0.Geometry.OriginalBookAnalyticBoost
import Mathlib.Analysis.Matrix.Order
import Mathlib.Tactic

/-!
The moved (mode 1, role D) left Julia defect from source `native` at
commit eebcb5e467742df3e9cf7fa9702042d7294aa742, uniform blob
`ee8de4635d24c668949ac9a0186616ab7d59f2ed` and modular checker blob
`d111c5bfeae3c384a4fe725f4a6d19277ea0005a`.

The actual complex, phased analytic operand is (3i/200) times the explicitly
computed integer matrix 40 c_D U. Its left defect is derived to be diagonal,
strictly positive definite, with the unique positive CFC square root displayed
below. No spectral premise is assumed. The right moved root, 128 Kraus
operators, their span and any physical admission remain separate obligations.
-/

open D0
open D0.Geometry.OriginalBookBoost
open D0.Geometry.OriginalBookCreatorBridge
open D0.Geometry.CubicExponential
open Matrix
open scoped MatrixOrder ComplexOrder

namespace D0.Geometry.OriginalBookMovedJuliaLeft

/-- Forty times the source's rational boost, over the integers. -/
def fortyBoost : SourceMatrix :=
  (40 : ℤ) • (1 : SourceMatrix) + sourceBoostGenerator * sourceBoostGenerator +
    (9 : ℤ) • sourceBoostGenerator

/-- Forty times c₁ U, before the source scale 3/5 and phase i. -/
def fortyMoved : SourceMatrix := sourceCreatorMatrix D0.D * fortyBoost

/-- Equivalent form using the already proved sparse generator and square. -/
def reducedFortyMoved : SourceMatrix :=
  sourceCreatorMatrix D0.D *
    ((40 : ℤ) • (1 : SourceMatrix) + sparseBoostSquare + (9 : ℤ) • sparseBoostGenerator)

lemma fortyMoved_eq_reduced : fortyMoved = reducedFortyMoved := by
  simp [fortyMoved, fortyBoost, reducedFortyMoved, sourceBoostGenerator_eq_sparse,
    sparseBoost_square_and_cube.1]

/-- Explicit finite matrix derived from the actual c₁ and U. -/
def sparseFortyMoved : SourceMatrix := fun bra ket =>
  if (bra = 2 ∧ ket = 0) ∨ (bra = 14 ∧ ket = 12) then 40
  else if (bra = 6 ∧ ket = 4) ∨ (bra = 10 ∧ ket = 8) then -40
  else if (bra = 7 ∧ ket = 5) ∨ (bra = 11 ∧ ket = 9) then 41
  else if (bra = 3 ∧ ket = 1) ∨ (bra = 15 ∧ ket = 13) then -41
  else if (bra = 3 ∧ ket = 2) ∨ (bra = 7 ∧ ket = 6) ∨
      (bra = 11 ∧ ket = 10) ∨ (bra = 15 ∧ ket = 14) then -9
  else 0

set_option maxRecDepth 100000 in
private theorem moved_ket_0 : ∀ bra : Fin 16,
    reducedFortyMoved bra (0 : Fin 16) = sparseFortyMoved bra (0 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_ket_1 : ∀ bra : Fin 16,
    reducedFortyMoved bra (1 : Fin 16) = sparseFortyMoved bra (1 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_ket_2 : ∀ bra : Fin 16,
    reducedFortyMoved bra (2 : Fin 16) = sparseFortyMoved bra (2 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_ket_3 : ∀ bra : Fin 16,
    reducedFortyMoved bra (3 : Fin 16) = sparseFortyMoved bra (3 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_ket_4 : ∀ bra : Fin 16,
    reducedFortyMoved bra (4 : Fin 16) = sparseFortyMoved bra (4 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_ket_5 : ∀ bra : Fin 16,
    reducedFortyMoved bra (5 : Fin 16) = sparseFortyMoved bra (5 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_ket_6 : ∀ bra : Fin 16,
    reducedFortyMoved bra (6 : Fin 16) = sparseFortyMoved bra (6 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_ket_7 : ∀ bra : Fin 16,
    reducedFortyMoved bra (7 : Fin 16) = sparseFortyMoved bra (7 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_ket_8 : ∀ bra : Fin 16,
    reducedFortyMoved bra (8 : Fin 16) = sparseFortyMoved bra (8 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_ket_9 : ∀ bra : Fin 16,
    reducedFortyMoved bra (9 : Fin 16) = sparseFortyMoved bra (9 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_ket_10 : ∀ bra : Fin 16,
    reducedFortyMoved bra (10 : Fin 16) = sparseFortyMoved bra (10 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_ket_11 : ∀ bra : Fin 16,
    reducedFortyMoved bra (11 : Fin 16) = sparseFortyMoved bra (11 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_ket_12 : ∀ bra : Fin 16,
    reducedFortyMoved bra (12 : Fin 16) = sparseFortyMoved bra (12 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_ket_13 : ∀ bra : Fin 16,
    reducedFortyMoved bra (13 : Fin 16) = sparseFortyMoved bra (13 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_ket_14 : ∀ bra : Fin 16,
    reducedFortyMoved bra (14 : Fin 16) = sparseFortyMoved bra (14 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_ket_15 : ∀ bra : Fin 16,
    reducedFortyMoved bra (15 : Fin 16) = sparseFortyMoved bra (15 : Fin 16) := by
  decide

theorem fortyMoved_eq_sparse : fortyMoved = sparseFortyMoved := by
  rw [fortyMoved_eq_reduced]
  ext bra ket
  fin_cases ket
  · exact moved_ket_0 bra
  · exact moved_ket_1 bra
  · exact moved_ket_2 bra
  · exact moved_ket_3 bra
  · exact moved_ket_4 bra
  · exact moved_ket_5 bra
  · exact moved_ket_6 bra
  · exact moved_ket_7 bra
  · exact moved_ket_8 bra
  · exact moved_ket_9 bra
  · exact moved_ket_10 bra
  · exact moved_ket_11 bra
  · exact moved_ket_12 bra
  · exact moved_ket_13 bra
  · exact moved_ket_14 bra
  · exact moved_ket_15 bra

/-- Left Gram diagonal before multiplying by 9/40000. -/
def movedGramInt : SourceMatrix := fun bra ket =>
  if bra = ket then
    if ket = 2 ∨ ket = 6 ∨ ket = 10 ∨ ket = 14 then 1600
    else if ket = 3 ∨ ket = 7 ∨ ket = 11 ∨ ket = 15 then 1762
    else 0
  else 0

set_option maxRecDepth 100000 in
private theorem moved_gram_ket_0 : ∀ bra : Fin 16,
    (sparseFortyMoved * sparseFortyMoved.transpose) bra (0 : Fin 16) =
      movedGramInt bra (0 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_gram_ket_1 : ∀ bra : Fin 16,
    (sparseFortyMoved * sparseFortyMoved.transpose) bra (1 : Fin 16) =
      movedGramInt bra (1 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_gram_ket_2 : ∀ bra : Fin 16,
    (sparseFortyMoved * sparseFortyMoved.transpose) bra (2 : Fin 16) =
      movedGramInt bra (2 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_gram_ket_3 : ∀ bra : Fin 16,
    (sparseFortyMoved * sparseFortyMoved.transpose) bra (3 : Fin 16) =
      movedGramInt bra (3 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_gram_ket_4 : ∀ bra : Fin 16,
    (sparseFortyMoved * sparseFortyMoved.transpose) bra (4 : Fin 16) =
      movedGramInt bra (4 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_gram_ket_5 : ∀ bra : Fin 16,
    (sparseFortyMoved * sparseFortyMoved.transpose) bra (5 : Fin 16) =
      movedGramInt bra (5 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_gram_ket_6 : ∀ bra : Fin 16,
    (sparseFortyMoved * sparseFortyMoved.transpose) bra (6 : Fin 16) =
      movedGramInt bra (6 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_gram_ket_7 : ∀ bra : Fin 16,
    (sparseFortyMoved * sparseFortyMoved.transpose) bra (7 : Fin 16) =
      movedGramInt bra (7 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_gram_ket_8 : ∀ bra : Fin 16,
    (sparseFortyMoved * sparseFortyMoved.transpose) bra (8 : Fin 16) =
      movedGramInt bra (8 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_gram_ket_9 : ∀ bra : Fin 16,
    (sparseFortyMoved * sparseFortyMoved.transpose) bra (9 : Fin 16) =
      movedGramInt bra (9 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_gram_ket_10 : ∀ bra : Fin 16,
    (sparseFortyMoved * sparseFortyMoved.transpose) bra (10 : Fin 16) =
      movedGramInt bra (10 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_gram_ket_11 : ∀ bra : Fin 16,
    (sparseFortyMoved * sparseFortyMoved.transpose) bra (11 : Fin 16) =
      movedGramInt bra (11 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_gram_ket_12 : ∀ bra : Fin 16,
    (sparseFortyMoved * sparseFortyMoved.transpose) bra (12 : Fin 16) =
      movedGramInt bra (12 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_gram_ket_13 : ∀ bra : Fin 16,
    (sparseFortyMoved * sparseFortyMoved.transpose) bra (13 : Fin 16) =
      movedGramInt bra (13 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_gram_ket_14 : ∀ bra : Fin 16,
    (sparseFortyMoved * sparseFortyMoved.transpose) bra (14 : Fin 16) =
      movedGramInt bra (14 : Fin 16) := by
  decide

set_option maxRecDepth 100000 in
private theorem moved_gram_ket_15 : ∀ bra : Fin 16,
    (sparseFortyMoved * sparseFortyMoved.transpose) bra (15 : Fin 16) =
      movedGramInt bra (15 : Fin 16) := by
  decide

theorem fortyMoved_leftGram : fortyMoved * fortyMoved.transpose = movedGramInt := by
  rw [fortyMoved_eq_sparse]
  ext bra ket
  fin_cases ket
  · exact moved_gram_ket_0 bra
  · exact moved_gram_ket_1 bra
  · exact moved_gram_ket_2 bra
  · exact moved_gram_ket_3 bra
  · exact moved_gram_ket_4 bra
  · exact moved_gram_ket_5 bra
  · exact moved_gram_ket_6 bra
  · exact moved_gram_ket_7 bra
  · exact moved_gram_ket_8 bra
  · exact moved_gram_ket_9 bra
  · exact moved_gram_ket_10 bra
  · exact moved_gram_ket_11 bra
  · exact moved_gram_ket_12 bra
  · exact moved_gram_ket_13 bra
  · exact moved_gram_ket_14 bra
  · exact moved_gram_ket_15 bra

end D0.Geometry.OriginalBookMovedJuliaLeft


open Matrix
open D0.Geometry.OriginalBookBoost
open D0.Geometry.CubicExponential
open scoped MatrixOrder ComplexOrder

namespace D0.Geometry.OriginalBookMovedJuliaLeft

abbrev mediumIndex (i : Fin 16) : Prop := i = 2 ∨ i = 6 ∨ i = 10 ∨ i = 14

abbrev largeIndex (i : Fin 16) : Prop := i = 3 ∨ i = 7 ∨ i = 11 ∨ i = 15

noncomputable def rootValue (i : Fin 16) : ℂ :=
  if mediumIndex i then 4 / 5 else if largeIndex i then (Real.sqrt (12071 / 20000) : ℝ) else 1

noncomputable def defectValue (i : Fin 16) : ℂ :=
  if mediumIndex i then 16 / 25 else if largeIndex i then 12071 / 20000 else 1

noncomputable def candidateRoot : Matrix (Fin 16) (Fin 16) ℂ := Matrix.diagonal rootValue

noncomputable def diagonalDefect : Matrix (Fin 16) (Fin 16) ℂ := Matrix.diagonal defectValue

lemma candidate_nonneg : 0 ≤ candidateRoot := by
  apply Matrix.PosSemidef.nonneg
  apply Matrix.PosSemidef.diagonal
  intro i
  simp only [Pi.zero_apply, rootValue]
  split_ifs <;> positivity

lemma candidate_square : candidateRoot * candidateRoot = diagonalDefect := by
  have hq : ((Real.sqrt (12071 / 20000) : ℝ) : ℂ) ^ 2 = 12071 / 20000 := by
    rw [← Complex.ofReal_pow, Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 12071 / 20000)]
    norm_num
  unfold candidateRoot diagonalDefect
  rw [Matrix.diagonal_mul_diagonal]
  congr 1
  funext i
  simp only [rootValue, defectValue]
  split_ifs
  · norm_num
  · simpa [pow_two] using hq
  · norm_num

theorem diagonal_root : CFC.sqrt diagonalDefect = candidateRoot :=
  CFC.sqrt_unique candidate_square candidate_nonneg

lemma defect_posDef : diagonalDefect.PosDef := by
  apply Matrix.posDef_diagonal_iff.mpr
  intro i
  simp only [defectValue]
  split_ifs <;> norm_num


noncomputable def fortyBoostC : Matrix (Fin 16) (Fin 16) ℂ :=
  fortyBoost.map (Int.castRingHom ℂ)

noncomputable def fortyMovedC : Matrix (Fin 16) (Fin 16) ℂ :=
  fortyMoved.map (Int.castRingHom ℂ)

lemma fortyBoostC_eq :
    fortyBoostC = (40 : ℝ) • sourceRationalBoost.map (Rat.castHom ℂ) := by
  ext i j
  by_cases h : i = j <;>
    simp [fortyBoostC, fortyBoost, sourceRationalBoost, sourceBoostGeneratorRat,
      Matrix.mul_apply, Matrix.ofNat_apply, h] <;> ring

lemma fortyMovedC_eq :
    fortyMovedC = sourceCreatorComplex D0.D *
      ((40 : ℝ) • sourceRationalBoost.map (Rat.castHom ℂ)) := by
  unfold fortyMovedC
  change (sourceCreatorMatrix D0.D * fortyBoost).map (Int.castRingHom ℂ) = _
  rw [Matrix.map_mul]
  change sourceCreatorComplex D0.D * fortyBoostC = _
  rw [fortyBoostC_eq]

lemma movedAnalytic_eq :
    sourceAnalyticOperand D0.D = ((3 / 200 : ℂ) * Complex.I) • fortyMovedC := by
  rw [sourceAnalyticOperand_eq_polynomial, fortyMovedC_eq]
  ext i j
  simp [sourcePolynomialOperand, sourceRolePhase, D0.D, D0.A,
    Matrix.mul_apply, Complex.real_smul]
  ring

lemma fortyMovedC_leftGram :
    fortyMovedC * fortyMovedCᴴ = movedGramInt.map (Int.castRingHom ℂ) := by
  have h := congrArg (fun m : SourceMatrix => m.map (Int.castRingHom ℂ)) fortyMoved_leftGram
  change ((fortyMoved * fortyMoved.transpose).map (Int.castRingHom ℂ)) =
    movedGramInt.map (Int.castRingHom ℂ) at h
  rw [Matrix.map_mul] at h
  have ht : fortyMoved.transpose.map (Int.castRingHom ℂ) = fortyMovedCᴴ := by
    ext i j
    simp [fortyMovedC, Matrix.conjTranspose_apply]
  rw [ht] at h
  exact h

lemma movedAnalytic_leftGram :
    sourceAnalyticOperand D0.D * (sourceAnalyticOperand D0.D)ᴴ =
      (9 / 40000 : ℂ) • (fortyMovedC * fortyMovedCᴴ) := by
  rw [movedAnalytic_eq]
  have hz : -(((3 / 200 : ℂ) * Complex.I) * ((3 / 200 : ℂ) * Complex.I)) = 9 / 40000 := by
    calc
      -(((3 / 200 : ℂ) * Complex.I) * ((3 / 200 : ℂ) * Complex.I)) =
          -((3 / 200 : ℂ) ^ 2) * (Complex.I * Complex.I) := by ring
      _ = 9 / 40000 := by rw [Complex.I_mul_I]; norm_num
  simp [Matrix.conjTranspose_smul, smul_smul]
  rw [← neg_smul, hz]

theorem movedAnalytic_leftDefect :
    1 - sourceAnalyticOperand D0.D * (sourceAnalyticOperand D0.D)ᴴ = diagonalDefect := by
  rw [movedAnalytic_leftGram, fortyMovedC_leftGram]
  ext i j
  by_cases h : i = j
  · subst i
    fin_cases j <;> norm_num [diagonalDefect, defectValue, mediumIndex, largeIndex,
      movedGramInt, Matrix.diagonal, Fin.ext_iff]
  · simp [diagonalDefect, defectValue, movedGramInt, Matrix.diagonal, h]

theorem movedAnalytic_leftRoot :
    CFC.sqrt (1 - sourceAnalyticOperand D0.D * (sourceAnalyticOperand D0.D)ᴴ) =
      candidateRoot := by
  rw [movedAnalytic_leftDefect]
  exact diagonal_root

theorem movedAnalytic_leftDefect_posDef :
    (1 - sourceAnalyticOperand D0.D * (sourceAnalyticOperand D0.D)ᴴ).PosDef := by
  rw [movedAnalytic_leftDefect]
  exact defect_posDef

end D0.Geometry.OriginalBookMovedJuliaLeft
