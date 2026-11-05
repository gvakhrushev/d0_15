import D0.Geometry.OriginalBookGoldenKraus
import Mathlib.Analysis.Matrix.Order
import Mathlib.Tactic

/-!
# Chronological source effects

The original modular checker `check_future_even_algebra_modprime.py`, blob
`d111c5bfeae3c384a4fe725f4a6d19277ea0005a` at commit
eebcb5e467742df3e9cf7fa9702042d7294aa742, lines 217–222, starts from I
and processes a chronological word backwards by X ↦ K† X K.
This module proves that ordering for the actual 128 source matrices and shows
individual effects are positive semidefinite. No completeness/CPTP, span,
rank or physical-admission statement follows.
-/

open Matrix
open scoped ComplexOrder

namespace D0.Geometry.ChronologicalEffect

variable {ι n : Type*} [Fintype n] [DecidableEq n]
abbrev Operator (n : Type*) := Matrix n n ℂ

/-- One exact Heisenberg update for an operator outcome. -/
noncomputable def update (K : ι → Operator n) (j : ι) (X : Operator n) : Operator n :=
  (K j)ᴴ * X * K j

/-- Chronological word: the last outcome acts first on the terminal identity. -/
noncomputable def effect (K : ι → Operator n) : List ι → Operator n
  | [] => 1
  | j :: tail => update K j (effect K tail)

/-- Literal loop form used by the source checker. -/
noncomputable def reverseLoop (K : ι → Operator n) (path : List ι) : Operator n :=
  path.reverse.foldl (fun X j => update K j X) 1

theorem reverseLoop_eq_effect (K : ι → Operator n) (path : List ι) :
    reverseLoop K path = effect K path := by
  induction path with
  | nil => rfl
  | cons j tail ih =>
    simp [reverseLoop, effect, List.reverse_cons, List.foldl_append, ← ih]

/-- This is positivity of each effect, not trace preservation or completeness. -/
theorem effect_posSemidef (K : ι → Operator n) (path : List ι) : (effect K path).PosSemidef := by
  induction path with
  | nil => exact Matrix.PosSemidef.one
  | cons j tail ih =>
    exact ih.conjTranspose_mul_mul_same (K j)

/-- A single zero operator anywhere in a word forces its effect to vanish. -/
theorem effect_of_mem_zero (K : ι → Operator n) (path : List ι) (j : ι)
    (hj : j ∈ path) (hz : K j = 0) : effect K path = 0 := by
  induction path with
  | nil => simp at hj
  | cons first tail ih =>
    rcases List.mem_cons.mp hj with h | h
    · subst first
      simp [effect, update, hz]
    · simp [effect, update, ih h]

/-- A finite noncommuting-order control; it is not a claim about source ranks. -/
def testA : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, 0]
def testB : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 1, 0]
def testK (j : Fin 2) : Matrix (Fin 2) (Fin 2) ℂ := if j = 0 then testA else testB

theorem chronological_order_negative_control : effect testK [0, 1] ≠ effect testK [1, 0] := by
  intro h
  have entry := congrArg (fun (M : Matrix (Fin 2) (Fin 2) ℂ) => M 0 0) h
  norm_num [effect, update, testK, testA, testB, Matrix.mul_apply, Fin.sum_univ_two] at entry

end D0.Geometry.ChronologicalEffect

namespace D0.Geometry.OriginalBookEffectWords

open D0.Geometry.OriginalBookGoldenKraus
open D0.Geometry.OriginalBookWalsh
open D0.Geometry.ChronologicalEffect

/-- Actual source effect on an ordered, finite list of the 128 source slots. -/
noncomputable def sourceEffect (path : List (Fin 128)) : Matrix (Fin 16) (Fin 16) ℂ :=
  effect sourceKraus path

theorem sourceEffect_eq_original_reverseLoop (path : List (Fin 128)) :
    reverseLoop sourceKraus path = sourceEffect path :=
  reverseLoop_eq_effect sourceKraus path

theorem sourceEffect_empty : sourceEffect [] = 1 := rfl

theorem sourceEffect_cons (j : Fin 128) (tail : List (Fin 128)) :
    sourceEffect (j :: tail) = (sourceKraus j)ᴴ * sourceEffect tail * sourceKraus j := rfl

theorem sourceEffect_posSemidef (path : List (Fin 128)) : (sourceEffect path).PosSemidef :=
  effect_posSemidef sourceKraus path

/-- Any history containing one of the 64 proved dark slots has zero effect. -/
theorem sourceEffect_of_marked_slot (path : List (Fin 128)) (slot : Fin 128)
    (hmem : slot ∈ path) (hmark : (rowLabel (krausRow slot)).val % 2 = 1) :
    sourceEffect path = 0 :=
  effect_of_mem_zero sourceKraus path slot hmem (marked_slot_zero slot hmark)

end D0.Geometry.OriginalBookEffectWords
