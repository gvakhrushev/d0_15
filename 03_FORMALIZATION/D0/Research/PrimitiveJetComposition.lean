import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Algebra.Ring.MinimalAxioms
import Mathlib.Analysis.Normed.Ring.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic.Abel
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NoncommRing
import Mathlib.Tactic.NormNum.Basic
import Mathlib.Tactic.Ring

/-!
# Ordered primitive words and their first jets

`empiricalProcess_composition` already transports observational equivalence along composed
processes, and `chainTransport_telescopes` folds endpoint transports. Neither expands the
operator residual `V_w I - I U_w`.

For a finite word `w = [a_m, …, a_1]`, written left to right so that `List.prod` is
`V_{a_m} ⋯ V_{a_1}`, this file proves

```text
V_w I - I U_w
  = ∑_k (V prefix before k) (V_k I - I U_k) (U suffix after k).
```

Empty products are `1`. The factors inside each summand stay in the word order.

A first jet is the pair `(value, derivative)` with the product rule
`(x * y).deriv = x.deriv * y.val + x.val * y.deriv`. The summand `x.val * y.deriv` is kept:
freezing the derivative of the intertwiner is not this rule.

Under a supplied contraction bound `‖V‖ ≤ 1`, `‖U‖ ≤ 1` and one-step bounds
`‖R‖ ≤ ε`, `‖dR‖ ≤ δ`, `‖dV‖ ≤ M`, `‖dU‖ ≤ M`,

```text
‖R_w‖ ≤ m ε
‖dR_w‖ ≤ m δ + m (m - 1) M ε.
```

Branch labels, preparations, tests, and postselection normalization are separate hypotheses.
The word identity does not prove them, and a sum of labelled residuals does not split into
each label. No v8 primitive is admitted here, and no physical or Einstein equation is claimed.
-/

namespace D0.Research.PrimitiveJetComposition

open Finset

variable {R : Type*}

/-- First jet: value and derivative. Multiplication is the noncommutative product rule. -/
@[ext]
structure Jet (R : Type*) where
  val : R
  deriv : R

namespace Jet

variable [Ring R]

instance : Zero (Jet R) := ⟨⟨0, 0⟩⟩
instance : One (Jet R) := ⟨⟨1, 0⟩⟩
instance : Add (Jet R) := ⟨fun x y => ⟨x.val + y.val, x.deriv + y.deriv⟩⟩
instance : Neg (Jet R) := ⟨fun x => ⟨-x.val, -x.deriv⟩⟩
instance : Mul (Jet R) :=
  ⟨fun x y => ⟨x.val * y.val, x.deriv * y.val + x.val * y.deriv⟩⟩

@[simp] lemma val_zero : (0 : Jet R).val = 0 := rfl
@[simp] lemma deriv_zero : (0 : Jet R).deriv = 0 := rfl
@[simp] lemma val_one : (1 : Jet R).val = 1 := rfl
@[simp] lemma deriv_one : (1 : Jet R).deriv = 0 := rfl
@[simp] lemma val_add (x y : Jet R) : (x + y).val = x.val + y.val := rfl
@[simp] lemma deriv_add (x y : Jet R) : (x + y).deriv = x.deriv + y.deriv := rfl
@[simp] lemma val_neg (x : Jet R) : (-x).val = -x.val := rfl
@[simp] lemma deriv_neg (x : Jet R) : (-x).deriv = -x.deriv := rfl
@[simp] lemma val_mul (x y : Jet R) : (x * y).val = x.val * y.val := rfl
@[simp] lemma deriv_mul (x y : Jet R) : (x * y).deriv = x.deriv * y.val + x.val * y.deriv := rfl

private lemma add_assoc' (a b c : Jet R) : a + b + c = a + (b + c) := by
  ext <;> simp [add_assoc]

private lemma zero_add' (a : Jet R) : 0 + a = a := by
  ext <;> simp

private lemma neg_add_cancel' (a : Jet R) : -a + a = 0 := by
  ext <;> simp

private lemma mul_assoc' (a b c : Jet R) : a * b * c = a * (b * c) := by
  ext
  · simp [mul_assoc]
  · simp only [deriv_mul, val_mul]
    noncomm_ring

private lemma one_mul' (a : Jet R) : (1 : Jet R) * a = a := by
  ext <;> simp

private lemma mul_one' (a : Jet R) : a * (1 : Jet R) = a := by
  ext <;> simp

private lemma left_distrib' (a b c : Jet R) : a * (b + c) = a * b + a * c := by
  ext
  · simp [mul_add]
  · simp only [deriv_mul, val_add, deriv_add]
    noncomm_ring

private lemma right_distrib' (a b c : Jet R) : (a + b) * c = a * c + b * c := by
  ext
  · simp [add_mul]
  · simp only [deriv_mul, val_add, deriv_add]
    noncomm_ring

instance : Ring (Jet R) :=
  Ring.ofMinimalAxioms add_assoc' zero_add' neg_add_cancel' mul_assoc' one_mul' mul_one'
    left_distrib' right_distrib'

@[simp] lemma val_sub (x y : Jet R) : (x - y).val = x.val - y.val := by
  simp [sub_eq_add_neg]

@[simp] lemma deriv_sub (x y : Jet R) : (x - y).deriv = x.deriv - y.deriv := by
  simp [sub_eq_add_neg]

lemma deriv_sum {ι : Type*} [DecidableEq ι] (s : Finset ι) (f : ι → Jet R) :
    (∑ i ∈ s, f i).deriv = ∑ i ∈ s, (f i).deriv := by
  induction s using Finset.induction with
  | empty => simp
  | insert a s ha ih =>
      rw [Finset.sum_insert ha, Finset.sum_insert ha, deriv_add, ih]

lemma deriv_fin_sum {n : ℕ} (f : Fin n → Jet R) :
    (∑ i, f i).deriv = ∑ i, (f i).deriv :=
  deriv_sum Finset.univ f

/-- Three-factor product rule. Both `x.val * y.deriv` and `y.val` placements are kept. -/
lemma deriv_mul_mul (x y z : Jet R) :
    (x * y * z).deriv =
      x.deriv * y.val * z.val + x.val * y.deriv * z.val + x.val * y.val * z.deriv := by
  simp only [deriv_mul, val_mul]
  noncomm_ring

end Jet

/-- One primitive step: representation `V` and native operator `U`. -/
structure Step (R : Type*) where
  V : R
  U : R

section Algebra

variable [Ring R]

/-- One-step residual `V I - I U`. -/
def stepResidual (I : R) (s : Step R) : R :=
  s.V * I - I * s.U

/-- Left-to-right word of representation operators. The head is the leftmost factor. -/
def wordV (w : List (Step R)) : R :=
  (w.map Step.V).prod

/-- Left-to-right word of native operators. -/
def wordU (w : List (Step R)) : R :=
  (w.map Step.U).prod

/-- Word residual `V_w I - I U_w`. -/
def wordResidual (I : R) (w : List (Step R)) : R :=
  wordV w * I - I * wordU w

/-- One ordered summand. Prefix `V`s stay on the left and suffix `U`s stay on the right. -/
def insertTerm (I : R) (w : List (Step R)) (k : Fin w.length) : R :=
  ((w.take k.1).map Step.V).prod *
    stepResidual I (w.get k) *
    ((w.drop (k.1 + 1)).map Step.U).prod

/-- Same letters, factors reversed. Used only as a negative control. -/
def reversedInsertTerm (I : R) (w : List (Step R)) (k : Fin w.length) : R :=
  ((w.drop (k.1 + 1)).map Step.U).prod *
    stepResidual I (w.get k) *
    ((w.take k.1).map Step.V).prod

/-- Ordered telescoping sum. The index runs left to right; addition does not reorder factors. -/
def orderedResidualSum (I : R) (w : List (Step R)) : R :=
  ∑ k : Fin w.length, insertTerm I w k

/-- Reversed-factor sum. Not equal to the word residual in general. -/
def reversedResidualSum (I : R) (w : List (Step R)) : R :=
  ∑ k : Fin w.length, reversedInsertTerm I w k

@[simp] lemma wordV_nil : wordV ([] : List (Step R)) = 1 := by simp [wordV]
@[simp] lemma wordU_nil : wordU ([] : List (Step R)) = 1 := by simp [wordU]

@[simp] lemma wordV_cons (s : Step R) (w : List (Step R)) :
    wordV (s :: w) = s.V * wordV w := by simp [wordV]

@[simp] lemma wordU_cons (s : Step R) (w : List (Step R)) :
    wordU (s :: w) = s.U * wordU w := by simp [wordU]

lemma insertTerm_zero (I : R) (s : Step R) (w : List (Step R)) :
    insertTerm I (s :: w) 0 = stepResidual I s * wordU w := by
  simp [insertTerm, wordU]

lemma insertTerm_succ (I : R) (s : Step R) (w : List (Step R)) (i : Fin w.length) :
    insertTerm I (s :: w) i.succ = s.V * insertTerm I w i := by
  simp only [insertTerm, Fin.val_succ, List.take_succ_cons, List.drop_succ_cons,
    List.get_cons_succ', List.map_cons, List.prod_cons]
  -- `((s.V * left) * mid) * right = s.V * ((left * mid) * right)`
  set left : R := ((w.take i.1).map Step.V).prod
  set mid : R := stepResidual I (w.get i)
  set right : R := ((w.drop (i.1 + 1)).map Step.U).prod
  calc
    (s.V * left) * mid * right = (s.V * (left * mid)) * right := by rw [mul_assoc s.V left mid]
    _ = s.V * (left * mid * right) := by rw [mul_assoc s.V (left * mid) right]

/-- Exact ordered decomposition of `V_w I - I U_w` for every finite word. -/
theorem wordResidual_eq_orderedSum (I : R) (w : List (Step R)) :
    wordResidual I w = orderedResidualSum I w := by
  induction w with
  | nil =>
      simp [wordResidual, orderedResidualSum]
  | cons s w ih =>
      have hsplit :
          orderedResidualSum I (s :: w) =
            stepResidual I s * wordU w + s.V * orderedResidualSum I w := by
        unfold orderedResidualSum
        erw [Fin.sum_univ_succ]
        rw [insertTerm_zero]
        congr 1
        rw [Finset.mul_sum]
        refine Finset.sum_congr rfl ?_
        intro i _
        exact insertTerm_succ I s w i
      calc
        wordResidual I (s :: w) = s.V * wordV w * I - I * (s.U * wordU w) := by
          simp [wordResidual]
        _ = stepResidual I s * wordU w + s.V * (wordV w * I - I * wordU w) := by
          simp only [stepResidual]
          noncomm_ring
        _ = stepResidual I s * wordU w + s.V * wordResidual I w := by
          simp [wordResidual]
        _ = stepResidual I s * wordU w + s.V * orderedResidualSum I w := by rw [ih]
        _ = orderedResidualSum I (s :: w) := by rw [hsplit]

/-- The same identity in the jet ring. Derivatives use the product rule, so `dI` is kept. -/
theorem jet_wordResidual_eq_orderedSum {S : Type*} [Ring S]
    (I : Jet S) (w : List (Step (Jet S))) :
    wordResidual I w = orderedResidualSum I w :=
  wordResidual_eq_orderedSum I w

/-- One-step derivative. The two `I.deriv` summands are the moving intertwiner. -/
theorem stepResidual_deriv {S : Type*} [Ring S] (I : Jet S) (s : Step (Jet S)) :
    (stepResidual I s).deriv =
      s.V.deriv * I.val + s.V.val * I.deriv
        - (I.deriv * s.U.val + I.val * s.U.deriv) := by
  simp [stepResidual]

/-- Derivative with `dI` deleted. This is not `stepResidual_deriv`. -/
def frozenStepDeriv {S : Type*} [Ring S] (I : Jet S) (s : Step (Jet S)) : S :=
  s.V.deriv * I.val - I.val * s.U.deriv

/-- The frozen formula misses `V dI - dI U`. -/
theorem stepResidual_deriv_eq_frozen_add_dI {S : Type*} [Ring S]
    (I : Jet S) (s : Step (Jet S)) :
    (stepResidual I s).deriv =
      frozenStepDeriv I s + (s.V.val * I.deriv - I.deriv * s.U.val) := by
  simp only [stepResidual_deriv, frozenStepDeriv]
  abel

/-- One-step intertwiners give the word intertwiner. Steps are supplied data. -/
theorem word_intertwining_of_steps (I : R) (w : List (Step R))
    (h : ∀ s ∈ w, s.V * I = I * s.U) :
    wordV w * I = I * wordU w := by
  have hres : wordResidual I w = 0 := by
    rw [wordResidual_eq_orderedSum, orderedResidualSum]
    refine Finset.sum_eq_zero ?_
    intro k _
    have hk : stepResidual I (w.get k) = 0 := by
      rw [stepResidual, sub_eq_zero]
      exact h _ (List.get_mem w k)
    rw [insertTerm, hk]
    simp
  simpa [wordResidual, sub_eq_zero] using hres

/-- Labels, preparations, tests, and postselection. None of these is a word residual. -/
structure BranchAgreement where
  labelsAgree : Prop
  preparationsAgree : Prop
  testsAgree : Prop
  postselectionNormalized : Prop

/-- The three instrument agreements a branching or comparison program must still prove. -/
def BranchAgreement.instrumentsAgree (B : BranchAgreement) : Prop :=
  B.labelsAgree ∧ B.preparationsAgree ∧ B.testsAgree

/-- A branched reading needs the word identity and a separate agreement hypothesis. -/
theorem branched_program_requires_agreement (I : R) (w : List (Step R))
    (B : BranchAgreement) (h : ∀ s ∈ w, s.V * I = I * s.U)
    (hB : B.instrumentsAgree) :
    wordV w * I = I * wordU w ∧ B.labelsAgree ∧ B.preparationsAgree ∧ B.testsAgree := by
  obtain ⟨hL, hP, hT⟩ := hB
  exact ⟨word_intertwining_of_steps I w h, hL, hP, hT⟩

/-- Vanishing of the empty word does not force branch agreement or postselection. -/
theorem word_residual_does_not_force_branch (I : R) :
    wordResidual I ([] : List (Step R)) = 0 ∧
      ¬ (BranchAgreement.mk False True True False).instrumentsAgree ∧
      ¬ (BranchAgreement.mk True True True False).postselectionNormalized := by
  refine ⟨?_, ?_, ?_⟩
  · simp [wordResidual]
  · simp [BranchAgreement.instrumentsAgree]
  · simp

/-- An exact one-step identity still does not normalize postselection. -/
theorem exact_step_does_not_normalize_postselection (I : R) :
    let s : Step R := ⟨1, 1⟩
    wordV [s] * I = I * wordU [s] ∧
      ¬ (BranchAgreement.mk True True True False).postselectionNormalized := by
  refine ⟨?_, by simp⟩
  have h : ∀ t ∈ [({ V := (1 : R), U := 1 } : Step R)], t.V * I = I * t.U := by
    intro t ht
    simp at ht
    simp [ht]
  exact word_intertwining_of_steps I [{ V := 1, U := 1 }] h

end Algebra

private lemma mul_le_mul3 {a b c a' b' c' : ℝ}
    (ha : a ≤ a') (hb : b ≤ b') (hc : c ≤ c')
    (hb0 : 0 ≤ b) (hc0 : 0 ≤ c) (ha'0 : 0 ≤ a') (hb'0 : 0 ≤ b') :
    a * b * c ≤ a' * b' * c' :=
  mul_le_mul (mul_le_mul ha hb hb0 ha'0) hc hc0 (mul_nonneg ha'0 hb'0)

section Norm

variable [NormedRing R] [NormOneClass R]

lemma prod_contraction (xs : List R) (h : ∀ x ∈ xs, ‖x‖ ≤ 1) : ‖xs.prod‖ ≤ 1 := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
      rw [List.prod_cons]
      have hx : ‖x‖ ≤ 1 := h x (by simp)
      have htail : ‖xs.prod‖ ≤ 1 :=
        ih fun y hy => h y (List.mem_cons_of_mem x hy)
      calc
        ‖x * xs.prod‖ ≤ ‖x‖ * ‖xs.prod‖ := norm_mul_le _ _
        _ ≤ 1 * 1 := mul_le_mul hx htail (norm_nonneg _) zero_le_one
        _ = 1 := by ring

lemma insertTerm_norm_le (I : R) (w : List (Step R)) (ε : ℝ)
    (hV : ∀ s ∈ w, ‖s.V‖ ≤ 1) (hU : ∀ s ∈ w, ‖s.U‖ ≤ 1)
    (hR : ∀ s ∈ w, ‖stepResidual I s‖ ≤ ε) (k : Fin w.length) :
    ‖insertTerm I w k‖ ≤ ε := by
  have hLeft : ‖((w.take k.1).map Step.V).prod‖ ≤ 1 := by
    refine prod_contraction _ ?_
    intro x hx
    obtain ⟨s, hs, rfl⟩ := List.mem_map.mp hx
    exact hV s (List.mem_of_mem_take hs)
  have hRight : ‖((w.drop (k.1 + 1)).map Step.U).prod‖ ≤ 1 := by
    refine prod_contraction _ ?_
    intro x hx
    obtain ⟨s, hs, rfl⟩ := List.mem_map.mp hx
    exact hU s (List.mem_of_mem_drop hs)
  have hMid : ‖stepResidual I (w.get k)‖ ≤ ε := hR _ (List.get_mem w k)
  have hε0 : 0 ≤ ε := le_trans (norm_nonneg _) hMid
  calc
    ‖insertTerm I w k‖ ≤
        ‖((w.take k.1).map Step.V).prod * stepResidual I (w.get k)‖ *
          ‖((w.drop (k.1 + 1)).map Step.U).prod‖ := by
      simpa [insertTerm] using
        norm_mul_le
          (((w.take k.1).map Step.V).prod * stepResidual I (w.get k))
          (((w.drop (k.1 + 1)).map Step.U).prod)
    _ ≤ (‖((w.take k.1).map Step.V).prod‖ * ‖stepResidual I (w.get k)‖) *
          ‖((w.drop (k.1 + 1)).map Step.U).prod‖ :=
      mul_le_mul_of_nonneg_right (norm_mul_le _ _) (norm_nonneg _)
    _ ≤ (1 * ε) * 1 := by
      refine mul_le_mul ?_ hRight (norm_nonneg _) ?_
      · exact mul_le_mul hLeft hMid (norm_nonneg _) zero_le_one
      · exact mul_nonneg zero_le_one hε0
    _ = ε := by ring

/-- Contraction bound on the word residual by the sum of one-step residuals. -/
theorem wordResidual_norm_le (I : R) (w : List (Step R)) (ε : ℝ)
    (hV : ∀ s ∈ w, ‖s.V‖ ≤ 1) (hU : ∀ s ∈ w, ‖s.U‖ ≤ 1)
    (hR : ∀ s ∈ w, ‖stepResidual I s‖ ≤ ε) :
    ‖wordResidual I w‖ ≤ (w.length : ℝ) * ε := by
  rw [wordResidual_eq_orderedSum, orderedResidualSum]
  calc
    ‖∑ k : Fin w.length, insertTerm I w k‖ ≤ ∑ k : Fin w.length, ‖insertTerm I w k‖ :=
      norm_sum_le _ _
    _ ≤ ∑ _ : Fin w.length, ε := by
      refine Finset.sum_le_sum ?_
      intro k _
      exact insertTerm_norm_le I w ε hV hU hR k
    _ = (w.length : ℝ) * ε := by
      simp [Finset.sum_const, Finset.card_univ]

end Norm

section JetNorm

variable {S : Type*} [NormedRing S] [NormOneClass S]

lemma jetProd_val_le (js : List (Jet S)) (h : ∀ j ∈ js, ‖j.val‖ ≤ 1) :
    ‖js.prod.val‖ ≤ 1 := by
  induction js with
  | nil => simp
  | cons j js ih =>
      rw [List.prod_cons, Jet.val_mul]
      have hj : ‖j.val‖ ≤ 1 := h j (by simp)
      have htail : ‖js.prod.val‖ ≤ 1 :=
        ih fun y hy => h y (List.mem_cons_of_mem j hy)
      calc
        ‖j.val * js.prod.val‖ ≤ ‖j.val‖ * ‖js.prod.val‖ := norm_mul_le _ _
        _ ≤ 1 * 1 := mul_le_mul hj htail (norm_nonneg _) zero_le_one
        _ = 1 := by ring

lemma jetProd_deriv_le (js : List (Jet S)) (M : ℝ) (hM : 0 ≤ M)
    (hv : ∀ j ∈ js, ‖j.val‖ ≤ 1) (hd : ∀ j ∈ js, ‖j.deriv‖ ≤ M) :
    ‖js.prod.deriv‖ ≤ (js.length : ℝ) * M := by
  induction js with
  | nil => simp
  | cons j js ih =>
      rw [List.prod_cons, Jet.deriv_mul]
      have hjv : ‖j.val‖ ≤ 1 := hv j (by simp)
      have hjd : ‖j.deriv‖ ≤ M := hd j (by simp)
      have htailv : ‖js.prod.val‖ ≤ 1 :=
        jetProd_val_le js fun y hy => hv y (List.mem_cons_of_mem j hy)
      have htaild : ‖js.prod.deriv‖ ≤ (js.length : ℝ) * M :=
        ih (fun y hy => hv y (List.mem_cons_of_mem j hy))
          (fun y hy => hd y (List.mem_cons_of_mem j hy))
      calc
        ‖j.deriv * js.prod.val + j.val * js.prod.deriv‖ ≤
            ‖j.deriv * js.prod.val‖ + ‖j.val * js.prod.deriv‖ := norm_add_le _ _
        _ ≤ ‖j.deriv‖ * ‖js.prod.val‖ + ‖j.val‖ * ‖js.prod.deriv‖ :=
          add_le_add (norm_mul_le _ _) (norm_mul_le _ _)
        _ ≤ M * 1 + 1 * ((js.length : ℝ) * M) :=
          add_le_add
            (mul_le_mul hjd htailv (norm_nonneg _) hM)
            (mul_le_mul hjv htaild (norm_nonneg _) zero_le_one)
        _ = ((j :: js).length : ℝ) * M := by
          simp [List.length_cons, Nat.cast_add]
          ring

omit [NormOneClass S] in
lemma norm_add3_le (a b c : S) : ‖a + b + c‖ ≤ ‖a‖ + ‖b‖ + ‖c‖ := by
  calc
    ‖a + b + c‖ ≤ ‖a + b‖ + ‖c‖ := norm_add_le _ _
    _ ≤ ‖a‖ + ‖b‖ + ‖c‖ := add_le_add (norm_add_le _ _) le_rfl

omit [NormOneClass S] in
lemma norm_mul3_le (a b c : S) : ‖a * b * c‖ ≤ ‖a‖ * ‖b‖ * ‖c‖ := by
  calc
    ‖a * b * c‖ ≤ ‖a * b‖ * ‖c‖ := norm_mul_le _ _
    _ ≤ (‖a‖ * ‖b‖) * ‖c‖ := mul_le_mul_of_nonneg_right (norm_mul_le _ _) (norm_nonneg _)

lemma insertTerm_deriv_le (I : Jet S) (w : List (Step (Jet S))) (M ε δ : ℝ)
    (hM : 0 ≤ M) (hε : 0 ≤ ε)
    (hV : ∀ s ∈ w, ‖s.V.val‖ ≤ 1) (hU : ∀ s ∈ w, ‖s.U.val‖ ≤ 1)
    (hdV : ∀ s ∈ w, ‖s.V.deriv‖ ≤ M) (hdU : ∀ s ∈ w, ‖s.U.deriv‖ ≤ M)
    (hR : ∀ s ∈ w, ‖(stepResidual I s).val‖ ≤ ε)
    (hdR : ∀ s ∈ w, ‖(stepResidual I s).deriv‖ ≤ δ)
    (k : Fin w.length) :
    ‖(insertTerm I w k).deriv‖ ≤ δ + ((w.length : ℝ) - 1) * M * ε := by
  set left : Jet S := ((w.take k.1).map Step.V).prod with hleft
  set mid : Jet S := stepResidual I (w.get k) with hmid
  set right : Jet S := ((w.drop (k.1 + 1)).map Step.U).prod with hright
  have hLeftMemV : ∀ j ∈ (w.take k.1).map Step.V, ‖j.val‖ ≤ 1 := by
    intro j hj
    obtain ⟨s, hs, rfl⟩ := List.mem_map.mp hj
    exact hV s (List.mem_of_mem_take hs)
  have hLeftMemD : ∀ j ∈ (w.take k.1).map Step.V, ‖j.deriv‖ ≤ M := by
    intro j hj
    obtain ⟨s, hs, rfl⟩ := List.mem_map.mp hj
    exact hdV s (List.mem_of_mem_take hs)
  have hRightMemV : ∀ j ∈ (w.drop (k.1 + 1)).map Step.U, ‖j.val‖ ≤ 1 := by
    intro j hj
    obtain ⟨s, hs, rfl⟩ := List.mem_map.mp hj
    exact hU s (List.mem_of_mem_drop hs)
  have hRightMemD : ∀ j ∈ (w.drop (k.1 + 1)).map Step.U, ‖j.deriv‖ ≤ M := by
    intro j hj
    obtain ⟨s, hs, rfl⟩ := List.mem_map.mp hj
    exact hdU s (List.mem_of_mem_drop hs)
  have hLeftVal : ‖left.val‖ ≤ 1 := jetProd_val_le _ hLeftMemV
  have hRightVal : ‖right.val‖ ≤ 1 := jetProd_val_le _ hRightMemV
  have hLeftDeriv : ‖left.deriv‖ ≤ ((w.take k.1).length : ℝ) * M := by
    rw [hleft]
    simpa [List.length_map] using
      jetProd_deriv_le ((w.take k.1).map Step.V) M hM hLeftMemV hLeftMemD
  have hRightDeriv : ‖right.deriv‖ ≤ ((w.drop (k.1 + 1)).length : ℝ) * M := by
    rw [hright]
    simpa [List.length_map] using
      jetProd_deriv_le ((w.drop (k.1 + 1)).map Step.U) M hM hRightMemV hRightMemD
  have hTake : (w.take k.1).length = k.1 := by
    rw [List.length_take, Nat.min_eq_left (Nat.le_of_lt k.2)]
  have hDrop : (w.drop (k.1 + 1)).length = w.length - (k.1 + 1) := by
    rw [List.length_drop]
  have hk : k.1 + 1 ≤ w.length := Nat.succ_le_of_lt k.2
  have hMidVal : ‖mid.val‖ ≤ ε := hR _ (List.get_mem w k)
  have hMidDeriv : ‖mid.deriv‖ ≤ δ := hdR _ (List.get_mem w k)
  have hmul :
      ‖(left * mid * right).deriv‖ ≤
        ‖left.deriv‖ * ‖mid.val‖ * ‖right.val‖ +
          ‖left.val‖ * ‖mid.deriv‖ * ‖right.val‖ +
          ‖left.val‖ * ‖mid.val‖ * ‖right.deriv‖ := by
    calc
      ‖(left * mid * right).deriv‖ =
          ‖left.deriv * mid.val * right.val + left.val * mid.deriv * right.val +
            left.val * mid.val * right.deriv‖ := by
        rw [Jet.deriv_mul_mul]
      _ ≤ ‖left.deriv * mid.val * right.val‖ + ‖left.val * mid.deriv * right.val‖ +
            ‖left.val * mid.val * right.deriv‖ := norm_add3_le _ _ _
      _ ≤ ‖left.deriv‖ * ‖mid.val‖ * ‖right.val‖ +
            ‖left.val‖ * ‖mid.deriv‖ * ‖right.val‖ +
            ‖left.val‖ * ‖mid.val‖ * ‖right.deriv‖ :=
        add_le_add (add_le_add (norm_mul3_le _ _ _) (norm_mul3_le _ _ _)) (norm_mul3_le _ _ _)
  have hδ0 : 0 ≤ δ := le_trans (norm_nonneg _) hMidDeriv
  have h1 : ‖left.deriv‖ * ‖mid.val‖ * ‖right.val‖ ≤ (k.1 : ℝ) * M * ε := by
    have hstep :
        ‖left.deriv‖ * ‖mid.val‖ * ‖right.val‖ ≤
          ((w.take k.1).length : ℝ) * M * ‖mid.val‖ * ‖right.val‖ :=
      mul_le_mul_of_nonneg_right
        (mul_le_mul_of_nonneg_right hLeftDeriv (norm_nonneg _)) (norm_nonneg _)
    rw [hTake] at hstep
    have hrest :
        (k.1 : ℝ) * M * ‖mid.val‖ * ‖right.val‖ ≤ (k.1 : ℝ) * M * ε * 1 :=
      mul_le_mul3 (le_refl ((k.1 : ℝ) * M)) hMidVal hRightVal
        (norm_nonneg _) (norm_nonneg _) (mul_nonneg (Nat.cast_nonneg _) hM) hε
    have hunit : (k.1 : ℝ) * M * ε * 1 = (k.1 : ℝ) * M * ε := by ring
    exact le_trans hstep (le_trans hrest (le_of_eq hunit))
  have h2 : ‖left.val‖ * ‖mid.deriv‖ * ‖right.val‖ ≤ δ := by
    have hrest :
        ‖left.val‖ * ‖mid.deriv‖ * ‖right.val‖ ≤ 1 * δ * 1 :=
      mul_le_mul3 hLeftVal hMidDeriv hRightVal
        (norm_nonneg _) (norm_nonneg _) zero_le_one hδ0
    have hunit : (1 : ℝ) * δ * 1 = δ := by ring
    exact le_trans hrest (le_of_eq hunit)
  have h3 :
      ‖left.val‖ * ‖mid.val‖ * ‖right.deriv‖ ≤
        ((w.length - (k.1 + 1) : ℕ) : ℝ) * M * ε := by
    have hstep :
        ‖left.val‖ * ‖mid.val‖ * ‖right.deriv‖ ≤
          1 * ε * (((w.drop (k.1 + 1)).length : ℝ) * M) :=
      mul_le_mul3 hLeftVal hMidVal hRightDeriv
        (norm_nonneg _) (norm_nonneg _) zero_le_one hε
    rw [hDrop] at hstep
    exact le_trans hstep (le_of_eq (by ring))
  have hcoeff :
      (k.1 : ℝ) * M * ε + δ + ((w.length - (k.1 + 1) : ℕ) : ℝ) * M * ε =
        δ + ((w.length : ℝ) - 1) * M * ε := by
    rw [Nat.cast_sub hk, Nat.cast_add, Nat.cast_one]
    ring
  calc
    ‖(insertTerm I w k).deriv‖ = ‖(left * mid * right).deriv‖ := by
      simp only [insertTerm]
      rw [← hleft, ← hmid, ← hright]
    _ ≤ ‖left.deriv‖ * ‖mid.val‖ * ‖right.val‖ +
          ‖left.val‖ * ‖mid.deriv‖ * ‖right.val‖ +
          ‖left.val‖ * ‖mid.val‖ * ‖right.deriv‖ := hmul
    _ ≤ (k.1 : ℝ) * M * ε + δ + ((w.length - (k.1 + 1) : ℕ) : ℝ) * M * ε :=
      add_le_add (add_le_add h1 h2) h3
    _ = δ + ((w.length : ℝ) - 1) * M * ε := hcoeff

/-- Derivative bound. Each of the `m` summands contributes `δ`, and each of its `m - 1`
outer factors contributes one `M ε`. -/
theorem jet_wordDeriv_norm_le (I : Jet S) (w : List (Step (Jet S))) (M ε δ : ℝ)
    (hM : 0 ≤ M) (hε : 0 ≤ ε)
    (hV : ∀ s ∈ w, ‖s.V.val‖ ≤ 1) (hU : ∀ s ∈ w, ‖s.U.val‖ ≤ 1)
    (hdV : ∀ s ∈ w, ‖s.V.deriv‖ ≤ M) (hdU : ∀ s ∈ w, ‖s.U.deriv‖ ≤ M)
    (hR : ∀ s ∈ w, ‖(stepResidual I s).val‖ ≤ ε)
    (hdR : ∀ s ∈ w, ‖(stepResidual I s).deriv‖ ≤ δ) :
    ‖(wordResidual I w).deriv‖ ≤
      (w.length : ℝ) * δ + (w.length : ℝ) * ((w.length : ℝ) - 1) * M * ε := by
  rw [jet_wordResidual_eq_orderedSum, orderedResidualSum, Jet.deriv_fin_sum]
  calc
    ‖∑ k : Fin w.length, (insertTerm I w k).deriv‖ ≤
        ∑ k : Fin w.length, ‖(insertTerm I w k).deriv‖ := norm_sum_le _ _
    _ ≤ ∑ _ : Fin w.length, (δ + ((w.length : ℝ) - 1) * M * ε) := by
      refine Finset.sum_le_sum ?_
      intro k _
      exact insertTerm_deriv_le I w M ε δ hM hε hV hU hdV hdU hR hdR k
    _ = (w.length : ℝ) * δ + (w.length : ℝ) * ((w.length : ℝ) - 1) * M * ε := by
      simp [Finset.sum_const, Finset.card_univ]
      ring

end JetNorm

/-! ### Noncommuting `2 × 2` controls

These matrices do not commute. The ordered identity still holds. The reversed factor order
does not, and deleting `dI` does not. -/

abbrev M2 := Matrix (Fin 2) (Fin 2) ℝ

def e00 : M2 := !![1, 0; 0, 0]
def e01 : M2 := !![0, 1; 0, 0]
def e10 : M2 := !![0, 0; 1, 0]

/-- Diagonal intertwiner whose two scales do not commute with the matrix units below. -/
def sampleI : M2 := !![1, 0; 0, 2]

def stepHead : Step M2 := ⟨e01, e10⟩
def stepTail : Step M2 := ⟨e10, e00⟩

/-- Word `[head, tail]`, so `V_w = e01 * e10` and `U_w = e10 * e00`. -/
def sampleWord : List (Step M2) := [stepHead, stepTail]

theorem sample_factors_do_not_commute :
    stepHead.V * stepTail.V ≠ stepTail.V * stepHead.V := by
  intro h
  have h00 := congr_fun (congr_fun h 0) 0
  simp only [stepHead, stepTail, e01, e10] at h00
  rw [Matrix.mul_fin_two, Matrix.mul_fin_two] at h00
  norm_num at h00

/-- The ordered residual on these matrices is the concrete nonzero value `!![1, 0; -2, 0]`. -/
theorem sample_ordered_residual :
    wordResidual sampleI sampleWord = !![1, 0; -2, 0] ∧
      orderedResidualSum sampleI sampleWord = !![1, 0; -2, 0] ∧
      stepHead.V * stepTail.V ≠ stepTail.V * stepHead.V := by
  have hword : wordResidual sampleI sampleWord = !![1, 0; -2, 0] := by
    simp only [wordResidual, wordV, wordU, sampleWord, stepHead, stepTail, sampleI,
      e01, e10, e00, List.map_cons, List.map_nil, List.prod_cons, List.prod_nil, mul_one]
    have hV : !![0, (1 : ℝ); 0, 0] * !![0, 0; 1, 0] = !![1, 0; 0, 0] := by
      rw [Matrix.mul_fin_two]; norm_num
    have hU : !![0, 0; (1 : ℝ), 0] * !![1, 0; 0, 0] = !![0, 0; 1, 0] := by
      rw [Matrix.mul_fin_two]; norm_num
    rw [hV, hU]
    have hL : !![1, (0 : ℝ); 0, 0] * !![1, 0; 0, 2] = !![1, 0; 0, 0] := by
      rw [Matrix.mul_fin_two]; norm_num
    have hR : !![1, (0 : ℝ); 0, 2] * !![0, 0; 1, 0] = !![0, 0; 2, 0] := by
      rw [Matrix.mul_fin_two]; norm_num
    rw [hL, hR]
    ext i j
    fin_cases i <;> fin_cases j <;> simp [Matrix.sub_apply]
  refine ⟨hword, ?_, sample_factors_do_not_commute⟩
  rw [← wordResidual_eq_orderedSum]
  exact hword

/-- Reversing the factors around each one-step residual changes the value. -/
theorem reversed_order_fails :
    reversedResidualSum sampleI sampleWord ≠ wordResidual sampleI sampleWord := by
  intro h
  have hword : wordResidual sampleI sampleWord = !![1, 0; -2, 0] :=
    sample_ordered_residual.1
  have hHead : stepResidual sampleI stepHead = !![0, (2 : ℝ); -2, 0] := by
    simp only [stepResidual, stepHead, sampleI, e01, e10]
    rw [Matrix.mul_fin_two, Matrix.mul_fin_two]
    ext i j
    fin_cases i <;> fin_cases j <;> simp [Matrix.sub_apply]
  have hTail : stepResidual sampleI stepTail = !![(-1 : ℝ), 0; 1, 0] := by
    simp only [stepResidual, stepTail, sampleI, e10, e00]
    rw [Matrix.mul_fin_two, Matrix.mul_fin_two]
    ext i j
    fin_cases i <;> fin_cases j <;> simp [Matrix.sub_apply]
  have h0 : reversedInsertTerm sampleI [stepHead, stepTail] 0 = !![0, (2 : ℝ); 0, 0] := by
    unfold reversedInsertTerm
    simp only [Fin.val_zero, zero_add, List.drop_one, List.take_zero, List.get_cons_zero,
      List.map_nil, List.prod_nil, mul_one, stepTail]
    rw [hHead]
    simp only [List.tail_cons, e00, List.map_cons, List.map_nil, List.prod_cons,
      List.prod_nil, mul_one]
    rw [Matrix.mul_fin_two]
    ext i j
    fin_cases i <;> fin_cases j <;> simp
  have h1 : reversedInsertTerm sampleI [stepHead, stepTail] 1 = !![0, (-1 : ℝ); 0, 1] := by
    unfold reversedInsertTerm
    rw [show (1 : Fin 2) = Fin.succ (0 : Fin 1) by rfl]
    simp only [Fin.val_succ, Fin.val_zero, zero_add, List.drop_succ_cons, List.drop_nil,
      List.take_succ_cons, List.take_zero, List.get_cons_succ', List.get_cons_zero,
      List.map_cons, List.map_nil, List.prod_cons, List.prod_nil, one_mul, mul_one, stepHead]
    rw [hTail]
    simp only [e01]
    rw [Matrix.mul_fin_two]
    ext i j
    fin_cases i <;> fin_cases j <;> simp
  have hrev : reversedResidualSum sampleI sampleWord = !![0, (1 : ℝ); 0, 1] := by
    simp only [reversedResidualSum, sampleWord]
    erw [Fin.sum_univ_two]
    rw [h0, h1]
    ext i j
    fin_cases i <;> fin_cases j <;> simp [Matrix.add_apply]; norm_num
  rw [hrev, hword] at h
  have h00 := congr_fun (congr_fun h 0) 0
  simp at h00

/-- Moving intertwiner `I = 1 + ε e01`, with both steps equal to `e10` at derivative zero. -/
def movingI : Jet M2 := ⟨1, e01⟩
def jetStep : Step (Jet M2) := ⟨⟨e10, 0⟩, ⟨e10, 0⟩⟩

theorem kept_dI_value :
    (wordResidual movingI [jetStep]).deriv = !![(-1 : ℝ), 0; 0, 1] := by
  have hword :
      wordResidual movingI [jetStep] = stepResidual movingI jetStep := by
    simp [wordResidual, wordV, wordU, stepResidual, mul_one]
  rw [hword, stepResidual_deriv]
  simp only [movingI, jetStep, e10, e01, zero_mul, mul_zero, add_zero, zero_add]
  rw [Matrix.mul_fin_two, Matrix.mul_fin_two]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Matrix.sub_apply]

/-- Freezing `dI` replaces the word derivative by zero on this step. -/
theorem frozen_dI_is_zero :
    (wordResidual (⟨(1 : M2), 0⟩ : Jet M2) [jetStep]).deriv = 0 := by
  have hword :
      wordResidual (⟨(1 : M2), 0⟩ : Jet M2) [jetStep] =
        stepResidual (⟨(1 : M2), 0⟩ : Jet M2) jetStep := by
    simp [wordResidual, wordV, wordU, stepResidual, mul_one]
  rw [hword, stepResidual_deriv]
  simp [jetStep, zero_mul, mul_zero, add_zero]

/-- Deleting `dI` does not preserve the first jet. -/
theorem frozen_dI_fails :
    (wordResidual movingI [jetStep]).deriv ≠
      (wordResidual (⟨(1 : M2), 0⟩ : Jet M2) [jetStep]).deriv ∧
      frozenStepDeriv movingI jetStep = 0 ∧
      (stepResidual movingI jetStep).deriv =
        jetStep.V.val * movingI.deriv - movingI.deriv * jetStep.U.val := by
  refine ⟨?_, ?_, ?_⟩
  · intro h
    rw [kept_dI_value, frozen_dI_is_zero] at h
    have h00 := congr_fun (congr_fun h 0) 0
    simp at h00
  · simp [frozenStepDeriv, movingI, jetStep, mul_zero]
  · simp only [stepResidual_deriv, movingI, jetStep, zero_mul, mul_zero, add_zero, zero_add]

/-- A sum of two opposite labelled residuals vanishes without either label vanishing. -/
theorem branch_sum_does_not_give_each_label :
    ∃ r : Fin 2 → M2, (∑ i, r i) = 0 ∧ r 0 ≠ 0 ∧ r 1 ≠ 0 := by
  refine ⟨![e01, -e01], ?_, ?_, ?_⟩
  · simp [Fin.sum_univ_two, e01]
    ext i j
    fin_cases i <;> fin_cases j <;> simp
  · intro h
    have := congr_fun (congr_fun h 0) 1
    simp [e01] at this
  · intro h
    have := congr_fun (congr_fun h 0) 1
    simp [e01] at this

#print axioms wordResidual_eq_orderedSum
#print axioms jet_wordResidual_eq_orderedSum
#print axioms stepResidual_deriv
#print axioms stepResidual_deriv_eq_frozen_add_dI
#print axioms word_intertwining_of_steps
#print axioms branched_program_requires_agreement
#print axioms word_residual_does_not_force_branch
#print axioms exact_step_does_not_normalize_postselection
#print axioms wordResidual_norm_le
#print axioms jet_wordDeriv_norm_le
#print axioms sample_factors_do_not_commute
#print axioms sample_ordered_residual
#print axioms reversed_order_fails
#print axioms kept_dI_value
#print axioms frozen_dI_is_zero
#print axioms frozen_dI_fails
#print axioms branch_sum_does_not_give_each_label

end D0.Research.PrimitiveJetComposition
