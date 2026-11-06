import D0.Foundation.VerificationCore
import D0.Foundation.TheoryTransfer

/-!
# A concrete verification-to-transfer application

This module instantiates the existing future-record and theory-transfer
theorems on the finite visible-bit example already owned by
`D0.Foundation.TheoryTransfer`.  The verification protocol represents the
complete empirical quotient: the retained second bit is intentionally not a
distinction in this example.  We then transport an actual false-readout
assertion through the declared state/action/test/outcome maps.

The hidden-bit control exercises the opposite boundary.  A memory retaining
only the current detector cannot decode every future profile, and an
interpretation that erases the action which reveals the archive cannot satisfy
the primitive execution diagram.  These are finite interface checks; they do
not select a physical D0 apparatus or its cost.
-/

namespace D0.Foundation.VerificationTransferApplication

open EmpiricalTheoryFactorization
open VerifiabilityNecessity
open VerificationCore
open TheoryTransfer

private theorem visibleBit_encoding_sound
    (s t : TheoryTransfer.visibleBitSystem.State)
    (h : signature TheoryTransfer.visibleBitSystem.futureEmpiricalTheory s =
      signature TheoryTransfer.visibleBitSystem.futureEmpiricalTheory t) :
    s.1 = t.1 := by
  have hread := congrFun (congrFun h ()) (([], ()) : List TheoryTransfer.visibleBitSystem.Action ×
    TheoryTransfer.visibleBitSystem.Test)
  change TheoryTransfer.visibleBitSystem.profile s [] () =
    TheoryTransfer.visibleBitSystem.profile t [] () at hread
  simpa [FutureExecution.profile, FutureExecution.run, TheoryTransfer.visibleBitSystem] using hread

private theorem visibleBit_encoding_faithful
    (s t : TheoryTransfer.visibleBitSystem.State) (h : s.1 = t.1) :
    signature TheoryTransfer.visibleBitSystem.futureEmpiricalTheory s =
      signature TheoryTransfer.visibleBitSystem.futureEmpiricalTheory t := by
  funext catalogue context
  rcases context with ⟨word, test⟩
  change TheoryTransfer.visibleBitSystem.profile s word test =
    TheoryTransfer.visibleBitSystem.profile t word test
  simp [FutureExecution.profile, FutureExecution.run, TheoryTransfer.visibleBitSystem, h]

private noncomputable def visibleBitEmpiricalRepresentation :
    Bool ≃ EmpiricalState TheoryTransfer.visibleBitSystem.futureEmpiricalTheory :=
  (minimalPresentationEquiv TheoryTransfer.visibleBitSystem.futureEmpiricalTheory
    (fun s => s.1)
    visibleBit_encoding_sound
    visibleBit_encoding_faithful
    (by
      intro b
      exact ⟨(b, false), rfl⟩)).symm

/-- A concrete two-line protocol for the actual future-profile quotient of
the existing visible-bit execution. -/
noncomputable def visibleBitVerification :
    TheoryVerification TheoryTransfer.visibleBitSystem.futureEmpiricalTheory where
  protocol := {
    State := Bool
    Record := Bool
    Line := Bool
    Catalogue := Unit
    record := id
    compare := fun _ _ x y => decide (x ≠ y)
  }
  contract := {
    state_nontrivial := ⟨false, true, by decide⟩
    line_nontrivial := ⟨false, true, by decide⟩
    catalogue_nonempty := ⟨()⟩
    correct := by intro line catalogue x y; rfl
  }
  represents := visibleBitEmpiricalRepresentation

/-- The hidden archive bit is omitted exactly because no admitted future
operation in this source system can reveal it. -/
theorem visibleBit_records_follow_complete_future_equivalence :
    representedRecord visibleBitVerification (false, false) =
      representedRecord visibleBitVerification (false, true) := by
  apply (representedRecord_eq_iff visibleBitVerification _ _).2
  exact TheoryTransfer.visibleBit_same_all_source_futures

private def visibleFalseClass : TheoryTransfer.visibleBitSystem.FutureClass :=
  Quotient.mk TheoryTransfer.visibleBitSystem.futureSetoid (false, false)

private def visibleFalseReadout
    (q : TheoryTransfer.visibleBitSystem.FutureClass) : Prop :=
  TheoryTransfer.visibleBitSystem.quotientProfile q [] () = false

private theorem visibleFalseReadout_holds : visibleFalseReadout visibleFalseClass := by
  change TheoryTransfer.visibleBitSystem.profile (false, false) [] () = false
  rfl

/-- A source assertion about an actual class and profile is transported to
the common native sector using its declared interpretation maps. -/
theorem visibleFalseReadout_transfers_to_common_execution :
    TheoryTransfer.visibleBitInterpretation.commonExecution.quotientProfile
      (TheoryTransfer.visibleBitInterpretation.imageEquiv visibleFalseClass).val [] () =
      TheoryTransfer.visibleBitInterpretation.outcomeMap false := by
  let I := TheoryTransfer.visibleBitInterpretation
  have htranslated : I.translate visibleFalseReadout (I.imageEquiv visibleFalseClass) := by
    exact I.transfer_theorem
      (fun q => q = visibleFalseClass)
      visibleFalseReadout
      (by
        intro q hq
        subst q
        exact visibleFalseReadout_holds)
      (I.imageEquiv visibleFalseClass)
      ((I.translate_at_image (fun q => q = visibleFalseClass) visibleFalseClass).2 rfl)
  have hread :=
    (I.translate_future_observation [] () false (I.imageEquiv visibleFalseClass)).mp htranslated
  simpa [I, visibleFalseReadout] using hread

/-- The foundation representation and the concrete transfer map compose on
the same false state: its verified state reaches the common-sector readout. -/
theorem verified_visibleFalseReadout_transfers_to_common_execution :
    TheoryTransfer.visibleBitInterpretation.commonExecution.quotientProfile
      (TheoryTransfer.visibleBitInterpretation.verifiedStateImageEquiv
        visibleBitVerification
        (VerificationCore.representedState visibleBitVerification (false, false))).val [] () =
      TheoryTransfer.visibleBitInterpretation.outcomeMap false := by
  rw [TheoryTransfer.Interpretation.verifiedStateImageEquiv_representedState
    TheoryTransfer.visibleBitInterpretation visibleBitVerification (false, false)]
  exact visibleFalseReadout_transfers_to_common_execution

/-- The current detector alone cannot decode the future profile after the
archive-revealing action.  This consumes the owned lower-bound theorem with
the concrete projection encoder, rather than assuming a decoder exists. -/
theorem visible_only_memory_cannot_decode_hiddenBit_futures
    (decode : Bool → List EmpiricalTheoryFactorization.hiddenBitExecution.Action →
      EmpiricalTheoryFactorization.hiddenBitExecution.Test →
        EmpiricalTheoryFactorization.hiddenBitExecution.Outcome)
    (correct : ∀ s, decode s.1 = EmpiricalTheoryFactorization.hiddenBitExecution.profile s) :
    False := by
  have hinjective :=
    EmpiricalTheoryFactorization.hiddenBit_sufficient_encoder_injective Prod.fst decode correct
  have hsame : Prod.fst (false, false) = Prod.fst (false, true) := rfl
  have hstates := hinjective hsame
  have hne : (false, false) ≠ (false, true) := by decide
  exact hne hstates

/-- An action map that drops the admitted archive-revealing operation cannot
satisfy the real primitive step diagram. -/
theorem erased_hiddenBit_operation_map_is_impossible
    (I : Interpretation EmpiricalTheoryFactorization.hiddenBitExecution
      EmpiricalTheoryFactorization.hiddenBitExecution)
    (state_identity : I.stateMap = id)
    (action_erased : I.actionWord = fun _ => []) : False := by
  have h := I.step_commutes true (false, true)
  have hstates : (true, true) = (false, true) := by
    simpa [state_identity, action_erased, FutureExecution.run,
      EmpiricalTheoryFactorization.hiddenBitExecution] using h
  have hne : (true, true) ≠ (false, true) := by decide
  exact hne hstates

end D0.Foundation.VerificationTransferApplication
