import D0.Geometry.OriginalBookStaticJuliaRoots
import D0.Geometry.OriginalBookMovedJuliaLeft
import D0.Geometry.OriginalBookMovedJuliaRight
import Mathlib.Tactic

/-!
# The original 32 paired Julia words

Source: `check_uniform_book_source.py`, blob
`ee8de4635d24c668949ac9a0186616ab7d59f2ed`, lines 64–93, and
`check_future_even_algebra_modprime.py`, blob
`d111c5bfeae3c384a4fe725f4a6d19277ea0005a`, lines 125–172, both at
commit eebcb5e467742df3e9cf7fa9702042d7294aa742.
For each bit-mode (A,D,B,C), the source forms four ordered pairs of complex
16×16 operators and duplicates each adjacent pair. Here the previously proven
positive roots are reused literally, and matched to the real source inputs.
No Walsh transform, 128 Kraus family, CPTP statement or effect-span result is
claimed by this module; those are subsequent obligations. The actual physical
admission remains open.
-/

open D0
open D0.Geometry.OriginalBookBoost
open D0.Geometry.OriginalBookCreatorBridge
open D0.Geometry.CubicExponential
open D0.Geometry.OriginalBookStaticRoots
open Matrix
open scoped MatrixOrder ComplexOrder

namespace D0.Geometry.OriginalBookJuliaWords

abbrev Operator := Matrix (Fin 16) (Fin 16) ℂ

/-- Source bit-mode order: `creators()[0,1,2,3]` = A,D,B,C. -/
def modeRole (m : Fin 4) : Role :=
  if m = 0 then A else if m = 1 then D else if m = 2 then B else C

lemma modeRole_sourceBit (m : Fin 4) : sourceBit (modeRole m) = m.val := by
  fin_cases m <;> decide

/-- The previously verified positive left defect root for the actual input. -/
noncomputable def liveLeft (r : Role) : Operator :=
  if r = D then D0.Geometry.OriginalBookMovedJuliaLeft.candidateRoot
  else 1 - (1 / 5 : ℝ) • leftProjection r

/-- The previously verified positive right defect root for the actual input. -/
noncomputable def liveRight (r : Role) : Operator :=
  if r = D then D0.Geometry.OrthogonalProjectionRoot.rootCandidate
    D0.Geometry.OriginalBookMovedJuliaRight.regularC D0.Geometry.OriginalBookMovedJuliaRight.boostedC
  else 1 - (1 / 5 : ℝ) • rightProjection r

noncomputable def baseLeft (r : Role) : Operator := 1 - (1 / 5 : ℝ) • leftProjection r
noncomputable def baseRight (r : Role) : Operator := 1 - (1 / 5 : ℝ) • rightProjection r

lemma liveLeft_is_source_root (r : Role) :
    liveLeft r = CFC.sqrt (1 - sourceAnalyticOperand r * (sourceAnalyticOperand r)ᴴ) := by
  by_cases h : r = D
  · subst r
    exact D0.Geometry.OriginalBookMovedJuliaLeft.movedAnalytic_leftRoot.symm
  · simpa [liveLeft, h] using (static_operand_left_root r h).symm

lemma liveRight_is_source_root (r : Role) :
    liveRight r = CFC.sqrt (1 - (sourceAnalyticOperand r)ᴴ * sourceAnalyticOperand r) := by
  by_cases h : r = D
  · subst r
    exact D0.Geometry.OriginalBookMovedJuliaRight.movedAnalytic_rightRoot.symm
  · simpa [liveRight, h] using (static_operand_right_root r h).symm

lemma baseLeft_is_source_root (r : Role) :
    baseLeft r = CFC.sqrt (1 - sourceBase r * (sourceBase r)ᴴ) :=
  (baseline_left_root r).symm

lemma baseRight_is_source_root (r : Role) :
    baseRight r = CFC.sqrt (1 - (sourceBase r)ᴴ * sourceBase r) :=
  (baseline_right_root r).symm

/-- The positive-definiteness guard used by the source is discharged. -/
theorem source_defects_posDef (r : Role) :
    (1 - sourceAnalyticOperand r * (sourceAnalyticOperand r)ᴴ).PosDef ∧
    (1 - (sourceAnalyticOperand r)ᴴ * sourceAnalyticOperand r).PosDef ∧
    (1 - sourceBase r * (sourceBase r)ᴴ).PosDef ∧
    (1 - (sourceBase r)ᴴ * sourceBase r).PosDef := by
  refine ⟨?_, ?_, baseline_left_defect_posDef r, baseline_right_defect_posDef r⟩
  · by_cases h : r = D
    · subst r
      exact D0.Geometry.OriginalBookMovedJuliaLeft.movedAnalytic_leftDefect_posDef
    · exact static_operand_left_defect_posDef r h
  · by_cases h : r = D
    · subst r
      exact D0.Geometry.OriginalBookMovedJuliaRight.movedAnalytic_rightDefect_posDef
    · exact static_operand_right_defect_posDef r h

/-- One of the four *ordered pairs* for one original creator mode. -/
noncomputable def rowPair (mode row : Fin 4) : Operator × Operator :=
  let r := modeRole mode
  if row = 0 then (sourceAnalyticOperand r, liveLeft r)
  else if row = 1 then ((sourceAnalyticOperand r)ᴴ, liveRight r)
  else if row = 2 then (-sourceBase r, -baseLeft r)
  else (-(sourceBase r)ᴴ, -baseRight r)

/-- Source loop position: `8*mode + 2*row + duplicate`. -/
def wordIndex (mode row : Fin 4) (duplicate : Fin 2) : Fin 32 :=
  ⟨8 * mode.val + 2 * row.val + duplicate.val, by omega⟩

def wordMode (word : Fin 32) : Fin 4 := ⟨word.val / 8, by omega⟩
def wordRow (word : Fin 32) : Fin 4 := ⟨(word.val % 8) / 2, by omega⟩
def wordDuplicate (word : Fin 32) : Fin 2 := ⟨word.val % 2, by omega⟩

lemma wordIndex_coordinates (mode row : Fin 4) (duplicate : Fin 2) :
    wordMode (wordIndex mode row duplicate) = mode ∧
      wordRow (wordIndex mode row duplicate) = row ∧
      wordDuplicate (wordIndex mode row duplicate) = duplicate := by
  fin_cases mode <;> fin_cases row <;> fin_cases duplicate <;> decide

lemma wordIndex_reconstruct (word : Fin 32) :
    wordIndex (wordMode word) (wordRow word) (wordDuplicate word) = word := by
  fin_cases word <;> rfl

/-- The complete ordered 32-word source sequence; each word has two endpoints. -/
noncomputable def sourceWord (word : Fin 32) : Operator × Operator :=
  rowPair (wordMode word) (wordRow word)

theorem sourceWord_order (mode row : Fin 4) (duplicate : Fin 2) :
    sourceWord (wordIndex mode row duplicate) = rowPair mode row := by
  unfold sourceWord
  rw [(wordIndex_coordinates mode row duplicate).1, (wordIndex_coordinates mode row duplicate).2.1]

theorem adjacent_words_equal (mode row : Fin 4) :
    sourceWord (wordIndex mode row 0) = sourceWord (wordIndex mode row 1) := by
  rw [sourceWord_order, sourceWord_order]

theorem rowPair_live (mode : Fin 4) :
    rowPair mode 0 = (sourceAnalyticOperand (modeRole mode), liveLeft (modeRole mode)) ∧
    rowPair mode 1 = ((sourceAnalyticOperand (modeRole mode))ᴴ, liveRight (modeRole mode)) := by
  simp [rowPair]

theorem rowPair_baseline (mode : Fin 4) :
    rowPair mode 2 = (-sourceBase (modeRole mode), -baseLeft (modeRole mode)) ∧
    rowPair mode 3 = (-(sourceBase (modeRole mode))ᴴ, -baseRight (modeRole mode)) := by
  simp [rowPair]

/-- A concrete nonzero source creator entry used for hostile ordering controls. -/
lemma creator_A_entry : sourceCreatorComplex A 1 0 = 1 := by
  have h : sourceCreator (sourceBit A) 1 0 = 1 := by decide
  change ((sourceCreator (sourceBit A) 1 0 : ℤ) : ℂ) = 1
  exact_mod_cast h

theorem live_A_word_entry :
    ((sourceWord (wordIndex 0 0 0)).1) 1 0 = (3 / 5 : ℂ) * Complex.I := by
  rw [sourceWord_order]
  change sourceAnalyticOperand A 1 0 = _
  rw [sourceAnalyticOperand_eq_polynomial]
  have hAD : A ≠ D := by decide
  simp [sourcePolynomialOperand, sourceRolePhase, hAD, creator_A_entry]
  ring

theorem baseline_A_word_entry :
    ((sourceWord (wordIndex 0 2 0)).1) 1 0 = -(3 / 5 : ℂ) := by
  rw [sourceWord_order]
  change (-sourceBase A) 1 0 = _
  simp [sourceBase, creator_A_entry, Complex.real_smul]

/-- Duplicates agree, but distinct live and baseline rows do not collapse. -/
theorem distinct_A_live_and_baseline :
    sourceWord (wordIndex 0 0 0) ≠ sourceWord (wordIndex 0 2 0) := by
  intro h
  have he := congrArg (fun p : Operator × Operator => p.1 1 0) h
  change ((sourceWord (wordIndex 0 0 0)).1) 1 0 =
    ((sourceWord (wordIndex 0 2 0)).1) 1 0 at he
  rw [live_A_word_entry, baseline_A_word_entry] at he
  have hi := congrArg Complex.im he
  norm_num at hi

end D0.Geometry.OriginalBookJuliaWords
