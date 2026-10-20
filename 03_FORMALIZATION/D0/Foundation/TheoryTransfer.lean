import D0.Foundation.VerificationCore
import D0.Foundation.M1Universality

/-!
# Finite-program interpretation and theorem transfer

An interpretation supplies primitive state, program, test and outcome maps.
All-word commutation, empirical faithfulness on the common sector and transfer
of existing proofs are derived below. No theorem-preservation or physical-law
equivalence field is assumed.

The common sector uses exactly the source actions and tests, interpreted on
the full native state carrier. Extra native experiments remain present in the
native system. A separate context-coverage witness is required to obtain the
stronger statement about every native experiment. The final finite control
shows that this additional requirement cannot be omitted.

The assertion interface consists of arbitrary predicates on future empirical
classes. `DescSystem.derivable` is instantiated by semantic entailment under
an explicit regime predicate. An imported Lean proof of that entailment is
reused; this construction does not parse an arbitrary external proof calculus.
Physical admission, full action/source, clocks, units and limiting estimates
belong to the concrete interpretation that subsequently applies this theorem.
-/

namespace D0.Foundation.TheoryTransfer

open D0.Foundation.EmpiricalTheoryFactorization
open D0.Foundation.VerifiabilityNecessity
open D0.Foundation.M1Universality

/-- Primitive operational interpretation. Raw state injectivity is unnecessary:
only distinctions exposed by admitted future experiments must survive. -/
structure Interpretation (F G : FutureExecution) where
  stateMap : F.State → G.State
  actionWord : F.Action → List G.Action
  testMap : F.Test → G.Test
  outcomeMap : F.Outcome → G.Outcome
  outcome_injective : Function.Injective outcomeMap
  step_commutes : ∀ a s,
    stateMap (F.step a s) = G.run (actionWord a) (stateMap s)
  observe_commutes : ∀ s t,
    G.observe (stateMap s) (testMap t) = outcomeMap (F.observe s t)

/-- Translate an entire chronological source word by concatenating the actual
native programs assigned to its primitive actions. -/
def Interpretation.compile {F G : FutureExecution} (I : Interpretation F G) :
    List F.Action → List G.Action
  | [] => []
  | a :: w => I.actionWord a ++ I.compile w

@[simp] theorem Interpretation.compile_nil {F G : FutureExecution}
    (I : Interpretation F G) : I.compile [] = [] := rfl

theorem Interpretation.compile_append {F G : FutureExecution}
    (I : Interpretation F G) (u v : List F.Action) :
    I.compile (u ++ v) = I.compile u ++ I.compile v := by
  induction u with
  | nil => rfl
  | cons a u ih =>
      simp only [List.cons_append, Interpretation.compile, ih, List.append_assoc]

/-- The finite execution diagram follows by induction from primitive diagrams. -/
theorem Interpretation.run_commutes {F G : FutureExecution}
    (I : Interpretation F G) (w : List F.Action) (s : F.State) :
    I.stateMap (F.run w s) = G.run (I.compile w) (I.stateMap s) := by
  induction w generalizing s with
  | nil => rfl
  | cons a w ih =>
      change I.stateMap (F.run w (F.step a s)) =
        G.run (I.actionWord a ++ I.compile w) (I.stateMap s)
      rw [G.run_append, ← I.step_commutes]
      exact ih (F.step a s)

/-- All generated future tests commute, with their declared outcome encoding. -/
theorem Interpretation.profile_commutes {F G : FutureExecution}
    (I : Interpretation F G) (s : F.State) (w : List F.Action) (t : F.Test) :
    G.profile (I.stateMap s) (I.compile w) (I.testMap t) =
      I.outcomeMap (F.profile s w t) := by
  change G.observe (G.run (I.compile w) (I.stateMap s)) (I.testMap t) = _
  rw [← I.run_commutes]
  exact I.observe_commutes (F.run w s) t

/-- Identity interpretation retains the original primitives and observations. -/
def Interpretation.identity (F : FutureExecution) : Interpretation F F where
  stateMap := id
  actionWord := fun a => [a]
  testMap := id
  outcomeMap := id
  outcome_injective := Function.injective_id
  step_commutes := fun _ _ => rfl
  observe_commutes := fun _ _ => rfl

@[simp] theorem Interpretation.identity_compile (F : FutureExecution)
    (w : List F.Action) : (Interpretation.identity F).compile w = w := by
  induction w with
  | nil => rfl
  | cons a w ih =>
      change a :: (Interpretation.identity F).compile w = a :: w
      rw [ih]

/-- Interpretation composition compiles every intermediate primitive program;
it does not identify an intermediate primitive with one native gate. -/
def Interpretation.comp {F G H : FutureExecution}
    (I : Interpretation F G) (J : Interpretation G H) : Interpretation F H where
  stateMap := J.stateMap ∘ I.stateMap
  actionWord := fun a => J.compile (I.actionWord a)
  testMap := J.testMap ∘ I.testMap
  outcomeMap := J.outcomeMap ∘ I.outcomeMap
  outcome_injective := J.outcome_injective.comp I.outcome_injective
  step_commutes := by
    intro a s
    change J.stateMap (I.stateMap (F.step a s)) = _
    rw [I.step_commutes]
    exact J.run_commutes (I.actionWord a) (I.stateMap s)
  observe_commutes := by
    intro s t
    change H.observe (J.stateMap (I.stateMap s)) (J.testMap (I.testMap t)) = _
    rw [J.observe_commutes, I.observe_commutes]
    rfl

/-- Compilation itself composes on every finite word. -/
theorem Interpretation.comp_compile {F G H : FutureExecution}
    (I : Interpretation F G) (J : Interpretation G H) (w : List F.Action) :
    (I.comp J).compile w = J.compile (I.compile w) := by
  induction w with
  | nil => rfl
  | cons a w ih =>
      change J.compile (I.actionWord a) ++ (I.comp J).compile w =
        J.compile (I.actionWord a ++ I.compile w)
      rw [J.compile_append, ih]

/-- The declared common sector keeps the entire native state but exposes exactly
the compiled source operations and mapped source tests. The original `G` is
unchanged and still contains every additional native operation and test. -/
def Interpretation.commonExecution {F G : FutureExecution}
    (I : Interpretation F G) : FutureExecution where
  State := G.State
  Action := F.Action
  Test := F.Test
  Outcome := G.Outcome
  step := fun a s => G.run (I.actionWord a) s
  observe := fun s t => G.observe s (I.testMap t)

theorem Interpretation.common_run {F G : FutureExecution}
    (I : Interpretation F G) (w : List F.Action) (s : G.State) :
    I.commonExecution.run w s = G.run (I.compile w) s := by
  induction w generalizing s with
  | nil => rfl
  | cons a w ih =>
      change I.commonExecution.run w (G.run (I.actionWord a) s) =
        G.run (I.actionWord a ++ I.compile w) s
      rw [G.run_append]
      exact ih (G.run (I.actionWord a) s)

theorem Interpretation.common_profile_commutes {F G : FutureExecution}
    (I : Interpretation F G) (s : F.State) (w : List F.Action) (t : F.Test) :
    I.commonExecution.profile (I.stateMap s) w t =
      I.outcomeMap (F.profile s w t) := by
  change G.observe (I.commonExecution.run w (I.stateMap s)) (I.testMap t) = _
  rw [I.common_run]
  exact I.profile_commutes s w t

/-- Preservation and reflection are derived on the exact common future sector.
Outcome injectivity is used in the reflection direction. -/
theorem Interpretation.common_profile_eq_iff {F G : FutureExecution}
    (I : Interpretation F G) (s t : F.State) :
    I.commonExecution.profile (I.stateMap s) =
        I.commonExecution.profile (I.stateMap t) ↔
      F.profile s = F.profile t := by
  constructor
  · intro h
    funext w q
    apply I.outcome_injective
    rw [← I.common_profile_commutes, ← I.common_profile_commutes]
    exact congrFun (congrFun h w) q
  · intro h
    funext w q
    rw [I.common_profile_commutes, I.common_profile_commutes]
    exact congrArg I.outcomeMap (congrFun (congrFun h w) q)

/-- The state map descends to future classes; well-definedness is proved by
the all-word result, without requiring raw state injectivity. -/
def Interpretation.futureMap {F G : FutureExecution} (I : Interpretation F G) :
    F.FutureClass → I.commonExecution.FutureClass :=
  Quotient.lift (fun s => Quotient.mk I.commonExecution.futureSetoid (I.stateMap s))
    (by
      intro s t h
      apply Quotient.sound
      exact (I.common_profile_eq_iff s t).mpr h)

theorem Interpretation.futureMap_injective {F G : FutureExecution}
    (I : Interpretation F G) : Function.Injective I.futureMap := by
  intro q r
  refine Quotient.inductionOn₂ q r ?_
  intro s t h
  apply Quotient.sound
  exact (I.common_profile_eq_iff s t).mp (Quotient.exact h)

/-- The quotient map commutes with every original source operation. -/
theorem Interpretation.futureMap_step {F G : FutureExecution}
    (I : Interpretation F G) (a : F.Action) (q : F.FutureClass) :
    I.futureMap (F.quotientStep a q) =
      I.commonExecution.quotientStep a (I.futureMap q) := by
  refine Quotient.inductionOn q ?_
  intro s
  change Quotient.mk I.commonExecution.futureSetoid (I.stateMap (F.step a s)) =
    Quotient.mk I.commonExecution.futureSetoid
      (G.run (I.actionWord a) (I.stateMap s))
  rw [I.step_commutes]

/-- Empirical image is explicit. No claim is made that every native state is
represented by the source theory. -/
abbrev Interpretation.EmpiricalImage {F G : FutureExecution}
    (I : Interpretation F G) :=
  {q : I.commonExecution.FutureClass // ∃ p : F.FutureClass, I.futureMap p = q}

/-- A constructed equivalence onto the declared common empirical image. -/
noncomputable def Interpretation.imageEquiv {F G : FutureExecution}
    (I : Interpretation F G) : F.FutureClass ≃ I.EmpiricalImage :=
  Equiv.ofBijective (fun q => ⟨I.futureMap q, q, rfl⟩) ⟨by
    intro q r h
    exact I.futureMap_injective (congrArg Subtype.val h), by
    intro ⟨q, p, hp⟩
    exact ⟨p, Subtype.ext hp⟩⟩

/-- The common empirical image is closed under the interpreted source actions. -/
def Interpretation.imageStep {F G : FutureExecution}
    (I : Interpretation F G) (a : F.Action) (q : I.EmpiricalImage) :
    I.EmpiricalImage :=
  ⟨I.commonExecution.quotientStep a q.val, by
    obtain ⟨p, hp⟩ := q.property
    refine ⟨F.quotientStep a p, ?_⟩
    rw [I.futureMap_step, hp]⟩

theorem Interpretation.imageEquiv_step {F G : FutureExecution}
    (I : Interpretation F G) (a : F.Action) (q : F.FutureClass) :
    I.imageEquiv (F.quotientStep a q) = I.imageStep a (I.imageEquiv q) := by
  apply Subtype.ext
  exact I.futureMap_step a q

/-- Use the foundation's actual empirical/future bridge to identify the supplied
verified state carrier with this same common image. -/
noncomputable def Interpretation.verifiedStateImageEquiv {F G : FutureExecution}
    (I : Interpretation F G) (E : TheoryVerification F.futureEmpiricalTheory) :
    E.protocol.State ≃ I.EmpiricalImage :=
  E.represents.trans (F.futureClassEquivEmpirical.symm.trans I.imageEquiv)

/-- The composed representation sends the ACTUAL foundation state of `s` to
the class of its interpreted native state. -/
theorem Interpretation.verifiedStateImageEquiv_representedState
    {F G : FutureExecution} (I : Interpretation F G)
    (E : TheoryVerification F.futureEmpiricalTheory) (s : F.State) :
    I.verifiedStateImageEquiv E (VerificationCore.representedState E s) =
      I.imageEquiv (Quotient.mk F.futureSetoid s) := by
  change I.imageEquiv
    (F.futureClassEquivEmpirical.symm
      (E.represents (E.represents.symm (empiricalClass F.futureEmpiricalTheory s)))) = _
  rw [Equiv.apply_symm_apply]
  rfl

/-- Every foundation execution reaches the class of the actual compiled native
execution, through the same verified-state/image map. -/
theorem Interpretation.verifiedRun_image {F G : FutureExecution}
    (I : Interpretation F G) (E : TheoryVerification F.futureEmpiricalTheory)
    (w : List F.Action) (s : F.State) :
    (I.verifiedStateImageEquiv E
      (VerificationCore.representedRun E w (VerificationCore.representedState E s))).val =
      Quotient.mk I.commonExecution.futureSetoid
        (G.run (I.compile w) (I.stateMap s)) := by
  rw [VerificationCore.representedRun_state,
    I.verifiedStateImageEquiv_representedState]
  change Quotient.mk I.commonExecution.futureSetoid (I.stateMap (F.run w s)) = _
  rw [I.run_commutes]

/-- Arbitrary assertions on empirical classes retain their exact regime and
all supplied hypotheses under the constructed equivalence. -/
noncomputable def Interpretation.translate {F G : FutureExecution}
    (I : Interpretation F G) (P : F.FutureClass → Prop) : I.EmpiricalImage → Prop :=
  fun q => P (I.imageEquiv.symm q)

@[simp] theorem Interpretation.translate_at_image {F G : FutureExecution}
    (I : Interpretation F G) (P : F.FutureClass → Prop) (q : F.FutureClass) :
    I.translate P (I.imageEquiv q) ↔ P q := by
  simp [Interpretation.translate]

/-- Translated observational assertions are the ACTUAL common native quotient
readouts with the declared outcome encoding, not opaque predicate labels. -/
theorem Interpretation.translate_future_observation {F G : FutureExecution}
    (I : Interpretation F G) (w : List F.Action) (t : F.Test) (o : F.Outcome)
    (q : I.EmpiricalImage) :
    I.translate (fun p => F.quotientProfile p w t = o) q ↔
      I.commonExecution.quotientProfile q.val w t = I.outcomeMap o := by
  obtain ⟨p, rfl⟩ := I.imageEquiv.surjective q
  rw [I.translate_at_image]
  change F.quotientProfile p w t = o ↔
    I.commonExecution.quotientProfile (I.futureMap p) w t = I.outcomeMap o
  refine Quotient.inductionOn p ?_
  intro s
  change F.profile s w t = o ↔
    I.commonExecution.profile (I.stateMap s) w t = I.outcomeMap o
  rw [I.common_profile_commutes]
  exact ⟨fun h => congrArg I.outcomeMap h, fun h => I.outcome_injective h⟩

theorem Interpretation.translate_conjunction {F G : FutureExecution}
    (I : Interpretation F G) (P Q : F.FutureClass → Prop) (q : I.EmpiricalImage) :
    I.translate (fun x => P x ∧ Q x) q ↔ I.translate P q ∧ I.translate Q q := Iff.rfl

theorem Interpretation.translate_negation {F G : FutureExecution}
    (I : Interpretation F G) (P : F.FutureClass → Prop) (q : I.EmpiricalImage) :
    I.translate (fun x => ¬ P x) q ↔ ¬ I.translate P q := Iff.rfl

theorem Interpretation.translate_implication {F G : FutureExecution}
    (I : Interpretation F G) (P Q : F.FutureClass → Prop) (q : I.EmpiricalImage) :
    I.translate (fun x => P x → Q x) q ↔ (I.translate P q → I.translate Q q) := Iff.rfl

theorem Interpretation.translate_forall {F G : FutureExecution}
    (I : Interpretation F G) {ι : Type*} (P : ι → F.FutureClass → Prop)
    (q : I.EmpiricalImage) :
    I.translate (fun x => ∀ i, P i x) q ↔ ∀ i, I.translate (P i) q := Iff.rfl

/-- Source assertion system: entailment under an explicit regime, not a new
assumption that an arbitrary external proof language has been implemented. -/
def sourceAssertionSystem (F : FutureExecution) (H : F.FutureClass → Prop) :
    DescSystem where
  Sent := F.FutureClass → Prop
  derivable := fun P => ∀ q, H q → P q

noncomputable def Interpretation.imageAssertionSystem {F G : FutureExecution}
    (I : Interpretation F G) (H : F.FutureClass → Prop) : DescSystem where
  Sent := I.EmpiricalImage → Prop
  derivable := fun P => ∀ q, I.translate H q → P q

/-- The proof-transport interface is constructed from operational commutation
and the proved quotient equivalence. Its `iff_derivable` field is not assumed. -/
noncomputable def Interpretation.assertionFaithful {F G : FutureExecution}
    (I : Interpretation F G) (H : F.FutureClass → Prop) :
    Faithful (sourceAssertionSystem F H) (I.imageAssertionSystem H) where
  map := I.translate
  iff_derivable := by
    intro P
    constructor
    · intro h q hq
      exact h (I.imageEquiv.symm q) hq
    · intro h q hq
      have hn : I.translate H (I.imageEquiv q) :=
        (I.translate_at_image H q).mpr hq
      exact (I.translate_at_image P q).mp (h (I.imageEquiv q) hn)

/-- Reuse an already proved source theorem. The only application inputs are
the constructed interpretation and the explicit translated regime premise. -/
theorem Interpretation.transfer_theorem {F G : FutureExecution}
    (I : Interpretation F G) (H P : F.FutureClass → Prop)
    (source_proof : ∀ q, H q → P q) :
    ∀ q : I.EmpiricalImage, I.translate H q → I.translate P q :=
  faithful_preserves_derivable (I.assertionFaithful H) P source_proof

/-- Each imported premise remains visible; no regime hypothesis is discharged
merely by compiling a theorem's syntax. -/
theorem Interpretation.transfer_from_premises {F G : FutureExecution}
    (I : Interpretation F G) {ι : Type*} (A : ι → F.FutureClass → Prop)
    (P : F.FutureClass → Prop)
    (source_proof : ∀ q, (∀ i, A i q) → P q)
    (q : I.EmpiricalImage) (premises : ∀ i, I.translate (A i) q) :
    I.translate P q :=
  I.transfer_theorem (fun x => ∀ i, A i x) P source_proof q premises

/-- Dynamical assertions are transported along the same interpreted action. -/
theorem Interpretation.translate_after_step {F G : FutureExecution}
    (I : Interpretation F G) (P : F.FutureClass → Prop)
    (a : F.Action) (q : F.FutureClass) :
    I.translate P (I.imageStep a (I.imageEquiv q)) ↔ P (F.quotientStep a q) := by
  rw [← I.imageEquiv_step]
  exact I.translate_at_image P (F.quotientStep a q)

/-- A sufficient all-native coverage witness. Every native finite experiment
has a specified source future experiment and readout postprocessing on the
represented states. This is stronger than agreement on mapped source tests. -/
structure NativeContextCoverage {F G : FutureExecution} (I : Interpretation F G) where
  context : List G.Action → G.Test → List F.Action × F.Test
  readout : List G.Action → G.Test → F.Outcome → G.Outcome
  correct : ∀ s w t,
    G.profile (I.stateMap s) w t =
      readout w t (F.profile s (context w t).1 (context w t).2)

/-- Full native indistinguishability always reflects source indistinguishability,
because compiled source experiments are among the native experiments. -/
theorem Interpretation.native_profile_reflects {F G : FutureExecution}
    (I : Interpretation F G) {s t : F.State}
    (h : G.profile (I.stateMap s) = G.profile (I.stateMap t)) :
    F.profile s = F.profile t := by
  funext w q
  apply I.outcome_injective
  rw [← I.profile_commutes, ← I.profile_commutes]
  exact congrFun (congrFun h (I.compile w)) (I.testMap q)

/-- With actual coverage, source equivalence also preserves every extra native
experiment. The stronger full-native statement is thus proved conditionally. -/
theorem NativeContextCoverage.native_profile_eq_iff {F G : FutureExecution}
    {I : Interpretation F G} (C : NativeContextCoverage I) (s t : F.State) :
    G.profile (I.stateMap s) = G.profile (I.stateMap t) ↔ F.profile s = F.profile t := by
  constructor
  · exact I.native_profile_reflects
  · intro h
    funext w q
    rw [C.correct, C.correct]
    exact congrArg (C.readout w q)
      (congrFun (congrFun h (C.context w q).1) (C.context w q).2)

/-- An extra native distinction obstructs all-native coverage while leaving the
already proved common-sector interpretation intact. -/
theorem no_coverage_of_extra_distinction {F G : FutureExecution}
    (I : Interpretation F G) {s t : F.State}
    (hsource : F.profile s = F.profile t)
    (hnative : G.profile (I.stateMap s) ≠ G.profile (I.stateMap t)) :
    ¬ Nonempty (NativeContextCoverage I) := by
  rintro ⟨C⟩
  exact hnative ((C.native_profile_eq_iff s t).mpr hsource)

/-! ## Non-vacuous interpretations and the extra-test boundary -/

/-- The existing uncoupled-center construction gives an interpretation whose
raw state map is a projection. This uses its actual unchanged operations. -/
def forgetUncoupledCenter (F : FutureExecution) : Interpretation F.uncoupledCenter F where
  stateMap := Prod.fst
  actionWord := fun a => [a]
  testMap := id
  outcomeMap := id
  outcome_injective := Function.injective_id
  step_commutes := fun _ _ => rfl
  observe_commutes := fun _ _ => rfl

/-- In this example all native contexts really are covered. The existing
uncoupled-center run theorem supplies the required operational-interface equality. -/
def forgetUncoupledCenterCoverage (F : FutureExecution) :
    NativeContextCoverage (forgetUncoupledCenter F) where
  context := fun w t => (w, t)
  readout := fun _ _ => id
  correct := by
    intro s w t
    change F.profile s.1 w t = F.observe ((F.uncoupledCenter.run w s).1) t
    rcases s with ⟨s, b⟩
    rw [F.uncoupledCenter_run]
    rfl

/-- Two-bit carrier with an admitted current test of only its visible bit. -/
def visibleBitSystem : FutureExecution where
  State := Bool × Bool
  Action := Unit
  Test := Unit
  Outcome := Bool
  step := fun _ s => s
  observe := fun s _ => s.1

/-- The native system contains an additional test of the second bit. -/
def extraBitTestSystem : FutureExecution where
  State := Bool × Bool
  Action := Unit
  Test := Bool
  Outcome := Bool
  step := fun _ s => s
  observe := fun s t => if t then s.2 else s.1

/-- All primitive and observation diagrams commute on the common test family. -/
def visibleBitInterpretation : Interpretation visibleBitSystem extraBitTestSystem where
  stateMap := id
  actionWord := fun _ => [()]
  testMap := fun _ => false
  outcomeMap := id
  outcome_injective := Function.injective_id
  step_commutes := fun _ _ => rfl
  observe_commutes := fun _ _ => rfl

theorem visibleBit_run (w : List visibleBitSystem.Action) (s : visibleBitSystem.State) :
    visibleBitSystem.run w s = s := by
  induction w with
  | nil => rfl
  | cons a w ih => exact ih

theorem visibleBit_same_all_source_futures :
    visibleBitSystem.profile (false, false) = visibleBitSystem.profile (false, true) := by
  funext w t
  change visibleBitSystem.observe (visibleBitSystem.run w (false, false)) t =
    visibleBitSystem.observe (visibleBitSystem.run w (false, true)) t
  rw [visibleBit_run, visibleBit_run]
  rfl

theorem extraBit_different_native_futures :
    extraBitTestSystem.profile (false, false) ≠
      extraBitTestSystem.profile (false, true) := by
  intro h
  have impossible : false = true := congrFun (congrFun h []) true
  cases impossible

/-- Exact counterexample: the forward interpretation exists, yet a full-native
faithful claim fails because the additional admitted test observes more. -/
theorem extra_native_test_prevents_coverage :
    ¬ Nonempty (NativeContextCoverage visibleBitInterpretation) :=
  no_coverage_of_extra_distinction visibleBitInterpretation
    visibleBit_same_all_source_futures extraBit_different_native_futures

end D0.Foundation.TheoryTransfer
