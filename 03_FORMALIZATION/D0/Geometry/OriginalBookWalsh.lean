import D0.Geometry.OriginalBookJuliaWords
import Mathlib.Tactic

/-!
# Original Walsh rows

The source `check_uniform_book_source.py`, blob
`ee8de4635d24c668949ac9a0186616ab7d59f2ed`, lines 87–94, constructs 32
Walsh labels, each with two operator endpoints; the modular source at blob
`d111c5bfeae3c384a4fe725f4a6d19277ea0005a`, lines 160–174, repeats this
exact order. Both refs are at commit eebcb5e467742df3e9cf7fa9702042d7294aa742.
This module constructs the actual rows from the verified Julia words, without
asserting Golden Kraus, CPTP, effect rank/span or physical admission.
-/

open D0.Geometry.OriginalBookJuliaWords
open Matrix
open scoped BigOperators

namespace D0.Geometry.OriginalBookWalsh

/-- Population count of the five common source label/word bits. -/
def commonBitCount (label word : Fin 32) : ℕ :=
  ∑ bit : Fin 5, if label.val.testBit bit.val && word.val.testBit bit.val then 1 else 0

/-- Exact integer Walsh character, `(-1)^popcount(label AND word)`. -/
def walshSign (label word : Fin 32) : ℤ := (-1 : ℤ) ^ commonBitCount label word

/-- The two ordered operator endpoints in one actual source Julia pair. -/
noncomputable def wordEndpoint (word : Fin 32) (endpoint : Fin 2) : Operator :=
  if endpoint = 0 then (sourceWord word).1 else (sourceWord word).2

/-- Original 1/32 Walsh row for a label and endpoint, before flattening. -/
noncomputable def walshPairRow (label : Fin 32) (endpoint : Fin 2) : Operator :=
  (1 / 32 : ℝ) • ∑ word : Fin 32, (walshSign label word) • wordEndpoint word endpoint

/-- The source appends the two endpoints for each label in this order. -/
def rowIndex (label : Fin 32) (endpoint : Fin 2) : Fin 64 :=
  ⟨2 * label.val + endpoint.val, by omega⟩

def rowLabel (row : Fin 64) : Fin 32 := ⟨row.val / 2, by omega⟩
def rowEndpoint (row : Fin 64) : Fin 2 := ⟨row.val % 2, by omega⟩

lemma rowIndex_coordinates (label : Fin 32) (endpoint : Fin 2) :
    rowLabel (rowIndex label endpoint) = label ∧ rowEndpoint (rowIndex label endpoint) = endpoint := by
  fin_cases label <;> fin_cases endpoint <;> decide

lemma rowIndex_reconstruct (row : Fin 64) :
    rowIndex (rowLabel row) (rowEndpoint row) = row := by
  fin_cases row <;> rfl

/-- The actual 64 source endpoint rows in original flattened order. -/
noncomputable def sourceWalshRow (row : Fin 64) : Operator :=
  walshPairRow (rowLabel row) (rowEndpoint row)

theorem sourceWalshRow_order (label : Fin 32) (endpoint : Fin 2) :
    sourceWalshRow (rowIndex label endpoint) = walshPairRow label endpoint := by
  unfold sourceWalshRow
  rw [(rowIndex_coordinates label endpoint).1, (rowIndex_coordinates label endpoint).2]

/-- Low- and high-bit controls catch parity and bit-width/order mistakes. -/
theorem walsh_sign_controls :
    walshSign 0 0 = 1 ∧ walshSign 1 0 = 1 ∧ walshSign 1 1 = -1 ∧
      walshSign 16 16 = -1 := by decide

theorem row_index_controls : rowIndex 0 0 = 0 ∧ rowIndex 0 1 = 1 ∧ rowIndex 1 0 = 2 := by decide


/-- Source word indices 2k and 2k+1 as a finite product. -/
def pairedWord (k : Fin 16) (duplicate : Fin 2) : Fin 32 :=
  finProdFinEquiv (k, duplicate)

lemma paired_words_equal (k : Fin 16) :
    sourceWord (pairedWord k 0) = sourceWord (pairedWord k 1) := by
  fin_cases k
  · exact adjacent_words_equal 0 0
  · exact adjacent_words_equal 0 1
  · exact adjacent_words_equal 0 2
  · exact adjacent_words_equal 0 3
  · exact adjacent_words_equal 1 0
  · exact adjacent_words_equal 1 1
  · exact adjacent_words_equal 1 2
  · exact adjacent_words_equal 1 3
  · exact adjacent_words_equal 2 0
  · exact adjacent_words_equal 2 1
  · exact adjacent_words_equal 2 2
  · exact adjacent_words_equal 2 3
  · exact adjacent_words_equal 3 0
  · exact adjacent_words_equal 3 1
  · exact adjacent_words_equal 3 2
  · exact adjacent_words_equal 3 3

set_option maxRecDepth 100000 in
private lemma odd_sign_0 : ∀ label : Fin 32, label.val % 2 = 1 →
    walshSign label (pairedWord 0 0) = -walshSign label (pairedWord 0 1) := by
  decide

set_option maxRecDepth 100000 in
private lemma odd_sign_1 : ∀ label : Fin 32, label.val % 2 = 1 →
    walshSign label (pairedWord 1 0) = -walshSign label (pairedWord 1 1) := by
  decide

set_option maxRecDepth 100000 in
private lemma odd_sign_2 : ∀ label : Fin 32, label.val % 2 = 1 →
    walshSign label (pairedWord 2 0) = -walshSign label (pairedWord 2 1) := by
  decide

set_option maxRecDepth 100000 in
private lemma odd_sign_3 : ∀ label : Fin 32, label.val % 2 = 1 →
    walshSign label (pairedWord 3 0) = -walshSign label (pairedWord 3 1) := by
  decide

set_option maxRecDepth 100000 in
private lemma odd_sign_4 : ∀ label : Fin 32, label.val % 2 = 1 →
    walshSign label (pairedWord 4 0) = -walshSign label (pairedWord 4 1) := by
  decide

set_option maxRecDepth 100000 in
private lemma odd_sign_5 : ∀ label : Fin 32, label.val % 2 = 1 →
    walshSign label (pairedWord 5 0) = -walshSign label (pairedWord 5 1) := by
  decide

set_option maxRecDepth 100000 in
private lemma odd_sign_6 : ∀ label : Fin 32, label.val % 2 = 1 →
    walshSign label (pairedWord 6 0) = -walshSign label (pairedWord 6 1) := by
  decide

set_option maxRecDepth 100000 in
private lemma odd_sign_7 : ∀ label : Fin 32, label.val % 2 = 1 →
    walshSign label (pairedWord 7 0) = -walshSign label (pairedWord 7 1) := by
  decide

set_option maxRecDepth 100000 in
private lemma odd_sign_8 : ∀ label : Fin 32, label.val % 2 = 1 →
    walshSign label (pairedWord 8 0) = -walshSign label (pairedWord 8 1) := by
  decide

set_option maxRecDepth 100000 in
private lemma odd_sign_9 : ∀ label : Fin 32, label.val % 2 = 1 →
    walshSign label (pairedWord 9 0) = -walshSign label (pairedWord 9 1) := by
  decide

set_option maxRecDepth 100000 in
private lemma odd_sign_10 : ∀ label : Fin 32, label.val % 2 = 1 →
    walshSign label (pairedWord 10 0) = -walshSign label (pairedWord 10 1) := by
  decide

set_option maxRecDepth 100000 in
private lemma odd_sign_11 : ∀ label : Fin 32, label.val % 2 = 1 →
    walshSign label (pairedWord 11 0) = -walshSign label (pairedWord 11 1) := by
  decide

set_option maxRecDepth 100000 in
private lemma odd_sign_12 : ∀ label : Fin 32, label.val % 2 = 1 →
    walshSign label (pairedWord 12 0) = -walshSign label (pairedWord 12 1) := by
  decide

set_option maxRecDepth 100000 in
private lemma odd_sign_13 : ∀ label : Fin 32, label.val % 2 = 1 →
    walshSign label (pairedWord 13 0) = -walshSign label (pairedWord 13 1) := by
  decide

set_option maxRecDepth 100000 in
private lemma odd_sign_14 : ∀ label : Fin 32, label.val % 2 = 1 →
    walshSign label (pairedWord 14 0) = -walshSign label (pairedWord 14 1) := by
  decide

set_option maxRecDepth 100000 in
private lemma odd_sign_15 : ∀ label : Fin 32, label.val % 2 = 1 →
    walshSign label (pairedWord 15 0) = -walshSign label (pairedWord 15 1) := by
  decide

lemma odd_sign_pair (label : Fin 32) (h : label.val % 2 = 1) (k : Fin 16) :
    walshSign label (pairedWord k 0) = -walshSign label (pairedWord k 1) := by
  fin_cases k
  · exact odd_sign_0 label h
  · exact odd_sign_1 label h
  · exact odd_sign_2 label h
  · exact odd_sign_3 label h
  · exact odd_sign_4 label h
  · exact odd_sign_5 label h
  · exact odd_sign_6 label h
  · exact odd_sign_7 label h
  · exact odd_sign_8 label h
  · exact odd_sign_9 label h
  · exact odd_sign_10 label h
  · exact odd_sign_11 label h
  · exact odd_sign_12 label h
  · exact odd_sign_13 label h
  · exact odd_sign_14 label h
  · exact odd_sign_15 label h

/-- Odd Walsh labels cancel because the original neighboring words coincide. -/
theorem odd_label_row_zero (label : Fin 32) (h : label.val % 2 = 1) (endpoint : Fin 2) :
    walshPairRow label endpoint = 0 := by
  unfold walshPairRow
  have hs : (∑ word : Fin 32, (walshSign label word) • wordEndpoint word endpoint) = 0 := by
    rw [← (finProdFinEquiv : Fin 16 × Fin 2 ≃ Fin 32).sum_comp]
    rw [Fintype.sum_prod_type]
    simp only [Fin.sum_univ_two]
    apply Finset.sum_eq_zero
    intro k _
    change (walshSign label (pairedWord k 0)) • wordEndpoint (pairedWord k 0) endpoint +
      (walshSign label (pairedWord k 1)) • wordEndpoint (pairedWord k 1) endpoint = 0
    have hw : wordEndpoint (pairedWord k 0) endpoint = wordEndpoint (pairedWord k 1) endpoint := by
      simp [wordEndpoint, paired_words_equal]
    rw [odd_sign_pair label h k, hw]
    simp
  rw [hs]
  exact smul_zero _

theorem odd_label_flat_row_zero (label : Fin 32) (h : label.val % 2 = 1) (endpoint : Fin 2) :
    sourceWalshRow (rowIndex label endpoint) = 0 := by
  rw [sourceWalshRow_order]
  exact odd_label_row_zero label h endpoint

theorem odd_label_count :
    (Finset.univ.filter (fun label : Fin 32 => label.val % 2 = 1)).card = 16 := by decide

end D0.Geometry.OriginalBookWalsh
