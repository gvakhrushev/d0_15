import Mathlib.Tactic
import D0.Foundation.VerifiabilityNecessity

/-!
# Popperian bootstrap: a killing test already carries the functional tuple

Methodological inversion of the "show that no other realization exists" demand.

A *killing test* (Popper) is the minimal operational structure that could refute a theory:
1. two admissible outcomes that the theory distinguishes (a prediction and its violation),
2. a record of the realised outcome that survives until it is checked,
3. at least two independent checking lines (so that the verdict is not the private opinion of
   one apparatus), and
4. a verdict that does not depend on a privileged external catalogue.

Theorems in this file:

* `KillingTest.toContract` — every killing test *is* a verification contract.
* `contract_toKillingTest` — every verification contract yields a killing test.
  So `∃ killing test ↔ VerificationContract`: falsifiability and the M1 contract are the same
  structure, not two hypotheses.
* `killingTest_forces_functional_tuple` — hence the functional tuple (distinction, retention,
  comparison, repeated independent line, catalogue invariance) is a consequence of the mere
  *possibility* of being refuted.
* `no_killingTest_single_line` — with one checking line no killing test exists: a theory that
  admits only a solitary witness is unfalsifiable in this sense.
* `alternative_burden` — any proposed alternative realization that still admits a killing test
  carries the same functional tuple; an alternative can differ from the canonical realization only
  by giving up falsifiability.
-/

namespace D0.Foundation.PopperianBootstrap

open D0.Foundation.VerifiabilityNecessity

/-- A Popperian killing test over a protocol `P`. -/
structure KillingTest (P : VerificationProtocol) : Prop where
  /-- The theory predicts one outcome and forbids another. -/
  prediction_violation : ∃ x y : P.State, x ≠ y
  /-- The verdict must be checkable by two distinct lines. -/
  two_witnesses : ∃ l₀ l₁ : P.Line, l₀ ≠ l₁
  /-- Some background catalogue is available to run the check. -/
  runnable : Nonempty P.Catalogue
  /-- Verdict soundness on every line and every catalogue value: the test says "refuted" exactly
  when the realised outcome differs from the prediction. -/
  verdict : ∀ l c x y, P.compare l c (P.record x) (P.record y) = decide (x ≠ y)

/-- A killing test is a verification contract. -/
theorem KillingTest.toContract {P : VerificationProtocol} (K : KillingTest P) :
    VerificationContract P where
  state_nontrivial := by
    obtain ⟨x, y, hxy⟩ := K.prediction_violation
    exact ⟨⟨x, y, hxy⟩⟩
  line_nontrivial := by
    obtain ⟨l₀, l₁, h⟩ := K.two_witnesses
    exact ⟨⟨l₀, l₁, h⟩⟩
  catalogue_nonempty := K.runnable
  correct := K.verdict

/-- A verification contract is a killing test. -/
theorem contract_toKillingTest {P : VerificationProtocol} (V : VerificationContract P) :
    KillingTest P where
  prediction_violation := V.state_nontrivial.exists_pair_ne
  two_witnesses := V.line_nontrivial.exists_pair_ne
  runnable := V.catalogue_nonempty
  verdict := V.correct

/-- Falsifiability and the verification contract coincide. -/
theorem killingTest_iff_contract (P : VerificationProtocol) :
    KillingTest P ↔ VerificationContract P :=
  ⟨KillingTest.toContract, contract_toKillingTest⟩

/-- The functional tuple is forced by the bare possibility of refutation. -/
theorem killingTest_forces_functional_tuple {P : VerificationProtocol} (K : KillingTest P) :
    FunctionalTuple P :=
  protocol_verifiability_forces_functional_tuple K.toContract

/-- Retention (injective record) is forced by a killing test alone. -/
theorem killingTest_record_injective {P : VerificationProtocol} (K : KillingTest P) :
    Function.Injective P.record :=
  record_injective K.toContract

/-- Catalogue independence (M1) is forced by a killing test alone. -/
theorem killingTest_catalogue_invariant {P : VerificationProtocol} (K : KillingTest P)
    (l : P.Line) (c c' : P.Catalogue) (x y : P.State) :
    P.compare l c (P.record x) (P.record y) = P.compare l c' (P.record x) (P.record y) :=
  (killingTest_forces_functional_tuple K).catalogue_invariant l c c' x y

/-- With a single checking line there is no killing test. -/
theorem no_killingTest_single_line (P : VerificationProtocol) [Subsingleton P.Line] :
    ¬ KillingTest P := by
  intro K
  obtain ⟨l₀, l₁, h⟩ := K.two_witnesses
  exact h (Subsingleton.elim l₀ l₁)

/-- Burden of proof for alternatives.  Any alternative protocol `Q` that still admits a killing
test carries the same functional tuple as the canonical one; there is no falsifiable alternative
outside the tuple. -/
theorem alternative_burden (Q : VerificationProtocol) :
    (KillingTest Q → FunctionalTuple Q) ∧ (¬ FunctionalTuple Q → ¬ KillingTest Q) :=
  ⟨killingTest_forces_functional_tuple, fun h K => h (killingTest_forces_functional_tuple K)⟩

/-- Sanity instance: the two-line Boolean protocol admits a killing test. -/
def boolProtocol : VerificationProtocol where
  State := Bool
  Record := Bool
  Line := Bool
  Catalogue := Unit
  stateDecidableEq := inferInstance
  record := id
  compare := fun _ _ x y => decide (x ≠ y)

theorem boolProtocol_killingTest : KillingTest boolProtocol where
  prediction_violation := ⟨true, false, by simp⟩
  two_witnesses := ⟨true, false, by simp⟩
  runnable := ⟨()⟩
  verdict := by intro _ _ x y; rfl

/-! ## The killing test does not fix the carrier

Both protocols below admit a killing test, hence both carry the functional
tuple.  Their line sets and record sets are not bijective.  The tuple is not
a classification of all contract carriers.
-/

def fin3Protocol : VerificationProtocol where
  State := Bool
  Record := Bool
  Line := Fin 3
  Catalogue := Unit
  stateDecidableEq := inferInstance
  record := id
  compare := fun _ _ x y => decide (x ≠ y)

lemma fin3_zero_ne_one : (0 : Fin 3) ≠ 1 := by
  intro h
  exact absurd (congrArg Fin.val h) (by decide)

theorem fin3Protocol_killingTest : KillingTest fin3Protocol where
  prediction_violation := ⟨true, false, by simp⟩
  two_witnesses := ⟨(0 : Fin 3), (1 : Fin 3), fin3_zero_ne_one⟩
  runnable := ⟨()⟩
  verdict := by intro _ _ x y; rfl

/-- Unused record values.  Retention stays injective, but the record type is larger. -/
def silentRecordProtocol : VerificationProtocol where
  State := Bool
  Record := Bool × Fin 2
  Line := Bool
  Catalogue := Unit
  stateDecidableEq := inferInstance
  record := fun b => (b, 0)
  compare := fun _ _ x y => decide (x.1 ≠ y.1)

theorem silentRecordProtocol_killingTest : KillingTest silentRecordProtocol where
  prediction_violation := ⟨true, false, by simp⟩
  two_witnesses := ⟨true, false, by simp⟩
  runnable := ⟨()⟩
  verdict := by
    intro _ _ x y
    simp [silentRecordProtocol]

theorem boolProtocol_line_is_bool : boolProtocol.Line = Bool := rfl

theorem fin3Protocol_line_is_fin3 : fin3Protocol.Line = Fin 3 := rfl

theorem silentRecord_record_is_product : silentRecordProtocol.Record = (Bool × Fin 2) := rfl

theorem killing_test_does_not_fix_line_card :
    KillingTest boolProtocol ∧ KillingTest fin3Protocol ∧
      Fintype.card Bool ≠ Fintype.card (Fin 3) := by
  refine ⟨boolProtocol_killingTest, fin3Protocol_killingTest, ?_⟩
  decide

theorem killing_test_does_not_fix_record_card :
    KillingTest boolProtocol ∧ KillingTest silentRecordProtocol ∧
      Fintype.card Bool ≠ Fintype.card (Bool × Fin 2) := by
  refine ⟨boolProtocol_killingTest, silentRecordProtocol_killingTest, ?_⟩
  decide

theorem bool_and_fin3_lines_not_equiv :
    ¬ Nonempty (Bool ≃ Fin 3) := by
  intro ⟨e⟩
  have hcard := Fintype.card_congr e
  simp at hcard

end D0.Foundation.PopperianBootstrap
