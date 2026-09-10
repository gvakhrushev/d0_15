import D0.Foundation.ConcreteIndependentDetectionRepairSemantics

/-!
# Independent detection does not force left/right repair identification

`ConcreteIndependentDetectionRepairSemantics` quotiented physical comparisons by the *cardinality*
of their left/right history support. This merges `{left}` and `{right}`. The present module checks
whether that merge follows from the owned M1 and independent-detection premises.

It does not.

* left-history and right-history repairs are extensionally distinct;
* their exact history supports are distinct singletons;
* their support cardinalities are equal, so the arity quotient merges them;
* argument swap carries one to the other, so the merge is valid **only modulo side relabeling**;
* class-M1 admissibility itself does not force side-exchange symmetry: left-current and
  right-current comparisons are distinct, catalogue-independent admissible comparisons.

Consequently the exact physical support grammar has four realised support profiles
`∅, {left}, {right}, {left,right}`. The three-class arity grammar is the orbit quotient under an
additional "input sides are relabeling gauge" principle. Independent repetition and M1 alone do
not prove that principle.
-/

namespace D0.Foundation.IndependentDetectionSideSymmetryBoundary

open D0.Foundation
open D0.Foundation.CurrentDataFactorization
open D0.Foundation.DetectionCapabilityBoundary
open D0.Foundation.ConcreteIndependentDetectionRepairSemantics
open D0.Foundation.IndependentDetectionRepairGrammar
open D0.Synthesis.ConcretePhysicalDetectorRepresentation

/-- Read only the right history: the mirror of the previous left-history witness. -/
def rightArityComparison : Comparison := fun _ y => y.history

theorem rightArity_not_uses_left :
    ¬ UsesHistorySide rightArityComparison .left := by
  rintro ⟨x, x', y, _, hneq⟩
  exact hneq rfl

theorem rightArity_uses_right :
    UsesHistorySide rightArityComparison .right := by
  refine ⟨obsHistoryFalse, obsHistoryFalse, obsHistoryTrue, ?_, ?_⟩
  · exact ⟨rfl, rfl⟩
  · decide

theorem rightArity_support :
    historySupport rightArityComparison = {.right} := by
  ext s
  cases s <;>
    simp [historySupport, rightArity_not_uses_left, rightArity_uses_right]

theorem rightArity_value :
    comparisonRepairArity rightArityComparison = 1 := by
  apply Fin.ext
  simp [comparisonRepairArity, rightArity_support]

theorem left_right_repairs_distinct :
    oneArityComparison ≠ rightArityComparison := by
  intro h
  have hv := congrFun
    (congrFun h obsHistoryTrue) obsHistoryFalse
  simp [oneArityComparison, rightArityComparison,
    obsHistoryTrue, obsHistoryFalse] at hv

theorem left_right_supports_distinct :
    historySupport oneArityComparison ≠
      historySupport rightArityComparison := by
  rw [oneArity_support, rightArity_support]
  decide

/-- The arity quotient merges two physically distinct exact supports. -/
theorem arity_quotient_not_support_injective :
    comparisonRepairArity oneArityComparison =
        comparisonRepairArity rightArityComparison
      ∧ historySupport oneArityComparison ≠
        historySupport rightArityComparison :=
  ⟨oneArity_value.trans rightArity_value.symm,
    left_right_supports_distinct⟩

/-- Swap the two binary detector arguments. -/
def swapComparison (cmp : Comparison) : Comparison :=
  fun x y => cmp y x

theorem swap_left_history_is_right :
    swapComparison oneArityComparison = rightArityComparison := by
  rfl

/-- Side-exchange symmetry is the extra principle needed to turn the four exact profiles into three
arity orbits. -/
def ExchangeSymmetric (cmp : Comparison) : Prop :=
  ∀ x y, cmp x y = cmp y x

/-- A catalogue-independent current comparison may still prefer the left input. -/
def leftCurrentComparison : Comparison := fun x _ => x.member

def rightCurrentComparison : Comparison := fun _ y => y.member

theorem leftCurrent_admissible :
    concretePhysicalRepresentation.admissible leftCurrentComparison := by
  change HistoryInvariant (Bool × Bool) Bool
    (transportComparison leftCurrentComparison)
  intro _ _ _ _ _ _
  rfl

theorem rightCurrent_admissible :
    concretePhysicalRepresentation.admissible rightCurrentComparison := by
  change HistoryInvariant (Bool × Bool) Bool
    (transportComparison rightCurrentComparison)
  intro _ _ _ _ _ _
  rfl

def obsMemberFalse : Observation := ⟨false, false, false⟩
def obsMemberTrue : Observation := ⟨true, false, false⟩

theorem leftCurrent_not_exchange_symmetric :
    ¬ ExchangeSymmetric leftCurrentComparison := by
  intro h
  have hv := h obsMemberTrue obsMemberFalse
  simp [leftCurrentComparison, obsMemberTrue, obsMemberFalse] at hv

/-- **M1 no-go:** class-M1 admissibility does not force exchange symmetry. -/
theorem M1_does_not_force_side_exchange :
    ∃ cmp : Comparison,
      concretePhysicalRepresentation.admissible cmp
        ∧ ¬ ExchangeSymmetric cmp :=
  ⟨leftCurrentComparison,
    leftCurrent_admissible,
    leftCurrent_not_exchange_symmetric⟩

/-- Four exact support profiles. -/
def fourSupport : Fin 4 → Finset InputSide
  | 0 => ∅
  | 1 => {.left}
  | 2 => {.right}
  | 3 => Finset.univ

theorem fourSupport_injective :
    Function.Injective fourSupport := by
  intro i j h
  fin_cases i <;> fin_cases j <;>
    first | rfl | (exact absurd h (by decide))

def comparisonOfFourSupport : Fin 4 → Comparison
  | 0 => zeroArityComparison
  | 1 => oneArityComparison
  | 2 => rightArityComparison
  | 3 => twoArityComparison

theorem four_exact_supports_realised (i : Fin 4) :
    historySupport (comparisonOfFourSupport i) = fourSupport i := by
  fin_cases i <;>
    simp [comparisonOfFourSupport, fourSupport, zeroArity_support,
      oneArity_support, rightArity_support, twoArity_support]

/-- Capstone: the physical support grammar has at least four distinct classes, while the three-class
arity quotient is valid only after adding side-relabeling gauge. -/
theorem independent_detection_side_symmetry_boundary :
    Function.Injective fourSupport
      ∧ (∀ i : Fin 4,
          historySupport (comparisonOfFourSupport i) = fourSupport i)
      ∧ comparisonRepairArity oneArityComparison =
          comparisonRepairArity rightArityComparison
      ∧ oneArityComparison ≠ rightArityComparison
      ∧ (∃ cmp : Comparison,
          concretePhysicalRepresentation.admissible cmp
            ∧ ¬ ExchangeSymmetric cmp) :=
  ⟨fourSupport_injective,
    four_exact_supports_realised,
    oneArity_value.trans rightArity_value.symm,
    left_right_repairs_distinct,
    M1_does_not_force_side_exchange⟩

end D0.Foundation.IndependentDetectionSideSymmetryBoundary
