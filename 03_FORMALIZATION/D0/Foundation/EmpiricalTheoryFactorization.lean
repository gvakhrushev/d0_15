import D0.Foundation.M1ClassAdmissibility
import D0.Synthesis.DetectorLayerEquivalence

/-!
# Universal empirical factorization, with the concrete D0 boundary explicit

States may include apparatus, preparation and records. Tests may include full protocols;
outcomes may be probability laws, not just single Boolean samples. This interface does not
prove physical realizability of its supplied carriers or completeness of its test family.

After identifying states indistinguishable by every supplied test and catalogue, evaluation
is injective without a representation-injectivity axiom. Catalogue independence descends to
that quotient. Operations with a test pullback descend as well.
The universal object is relative to the supplied tests, not a fixed finite D0 table.
-/
namespace D0.Foundation.EmpiricalTheoryFactorization

open D0.Foundation.M1ClassAdmissibility

structure EmpiricalTheory where
  State : Type
  Test : Type
  Catalogue : Type
  Outcome : Type
  observe : State → Catalogue → Test → Outcome

def signature (T : EmpiricalTheory) (s : T.State) : T.Catalogue → T.Test → T.Outcome :=
  T.observe s

def observationalSetoid (T : EmpiricalTheory) : Setoid T.State :=
  Setoid.ker (signature T)

abbrev EmpiricalState (T : EmpiricalTheory) := Quotient (observationalSetoid T)

def empiricalClass (T : EmpiricalTheory) (s : T.State) : EmpiricalState T :=
  Quotient.mk _ s

def evaluate (T : EmpiricalTheory) :
    EmpiricalState T → T.Catalogue → T.Test → T.Outcome :=
  Quotient.lift (signature T) (fun _ _ h => h)

/-- Injectivity is proved after empirical equivalence, not required of raw state names. -/
theorem evaluate_injective (T : EmpiricalTheory) : Function.Injective (evaluate T) := by
  intro q r
  refine Quotient.inductionOn₂ q r ?_
  intro s t h
  exact Quotient.sound h

def empiricalEmbedding (T : EmpiricalTheory) :
    EmpiricalState T ↪ (T.Catalogue → T.Test → T.Outcome) :=
  ⟨evaluate T, evaluate_injective T⟩

/-- Any summary constant on empirical equivalence has exactly one factor through the quotient. -/
theorem universal_factorization (T : EmpiricalTheory) {Y : Type*}
    (f : T.State → Y)
    (hf : ∀ s t, signature T s = signature T t → f s = f t) :
    ∃! g : EmpiricalState T → Y, ∀ s, g (empiricalClass T s) = f s := by
  refine ⟨Quotient.lift f hf, fun _ => rfl, ?_⟩
  intro g hg
  funext q
  refine Quotient.inductionOn q ?_
  exact hg

/-- Any empirically sufficient summary cannot merge distinct empirical classes. -/
theorem sufficient_summary_reflects_equivalence (T : EmpiricalTheory) {Y : Type*}
    (encode : T.State → Y) (decode : Y → T.Catalogue → T.Test → T.Outcome)
    (correct : ∀ s, decode (encode s) = signature T s)
    {s t : T.State} (h : encode s = encode t) :
    empiricalClass T s = empiricalClass T t := by
  apply Quotient.sound
  exact (correct s).symm.trans ((congrArg decode h).trans (correct t))

/-- Every surjective presentation with exactly the same empirical distinctions is equivalent
to the canonical quotient. Uniqueness is relative to the full chosen experimental interface. -/
noncomputable def minimalPresentationEquiv (T : EmpiricalTheory) {Y : Type}
    (encode : T.State → Y)
    (sound : ∀ s t, signature T s = signature T t → encode s = encode t)
    (faithful : ∀ s t, encode s = encode t → signature T s = signature T t)
    (onto : Function.Surjective encode) : EmpiricalState T ≃ Y :=
  Equiv.ofBijective (Quotient.lift encode sound) ⟨by
    intro q r
    refine Quotient.inductionOn₂ q r ?_
    intro s t h
    exact Quotient.sound (faithful s t h), by
    intro y
    obtain ⟨s, hs⟩ := onto y
    exact ⟨empiricalClass T s, hs⟩⟩

def rawCatalogueSystem (T : EmpiricalTheory) : CatalogueSystem :=
  ⟨T.State, T.Catalogue, T.Test → T.Outcome, T.observe⟩

def quotientCatalogueSystem (T : EmpiricalTheory) : CatalogueSystem :=
  ⟨EmpiricalState T, T.Catalogue, T.Test → T.Outcome, evaluate T⟩

def profileCatalogueSystem (T : EmpiricalTheory) : CatalogueSystem :=
  ⟨T.Catalogue → T.Test → T.Outcome, T.Catalogue, T.Test → T.Outcome,
    fun f c => f c⟩

theorem catalogue_admissibility_preserved (T : EmpiricalTheory) (s : T.State) :
    M1ClassAdmissible (quotientCatalogueSystem T) (empiricalClass T s) ↔
      M1ClassAdmissible (rawCatalogueSystem T) s := Iff.rfl

/-- A constructed class representation: the former injectivity field follows from the quotient. -/
def empiricalClassRepresentation (T : EmpiricalTheory) :
    ClassRepresentation (profileCatalogueSystem T) (EmpiricalState T) where
  candidate := evaluate T
  admissible := M1ClassAdmissible (quotientCatalogueSystem T)
  admissible_iff := fun _ => Iff.rfl
  candidate_injective_on_admissible := fun _ _ h => evaluate_injective T h

/-- Compatibility with future tests supplies contextual, rather than merely current, equivalence. -/
structure OperationalProcess (T : EmpiricalTheory) where
  run : T.State → T.State
  pullTest : T.Test → T.Test
  compatible : ∀ s c e, T.observe (run s) c e = T.observe s c (pullTest e)

theorem process_respects_equivalence (T : EmpiricalTheory) (P : OperationalProcess T)
    {s t : T.State} (h : signature T s = signature T t) :
    signature T (P.run s) = signature T (P.run t) := by
  funext c e
  change T.observe (P.run s) c e = T.observe (P.run t) c e
  rw [P.compatible, P.compatible]
  exact congrFun (congrFun h c) (P.pullTest e)

def empiricalProcess (T : EmpiricalTheory) (P : OperationalProcess T) :
    EmpiricalState T → EmpiricalState T :=
  Quotient.lift (fun s => empiricalClass T (P.run s))
    (fun _ _ h => Quotient.sound (process_respects_equivalence T P h))

theorem process_preserves_admissibility (T : EmpiricalTheory) (P : OperationalProcess T)
    {s : T.State} (hs : M1ClassAdmissible (rawCatalogueSystem T) s) :
    M1ClassAdmissible (rawCatalogueSystem T) (P.run s) := by
  intro c d
  funext e
  change T.observe (P.run s) c e = T.observe (P.run s) d e
  rw [P.compatible, P.compatible]
  exact congrFun (hs c d) (P.pullTest e)

def composeProcess (T : EmpiricalTheory) (P Q : OperationalProcess T) :
    OperationalProcess T where
  run := Q.run ∘ P.run
  pullTest := P.pullTest ∘ Q.pullTest
  compatible := by
    intro s c e
    change T.observe (Q.run (P.run s)) c e = _
    rw [Q.compatible, P.compatible]
    rfl

theorem empiricalProcess_composition (T : EmpiricalTheory) (P Q : OperationalProcess T) :
    empiricalProcess T (composeProcess T P Q) =
      empiricalProcess T Q ∘ empiricalProcess T P := by
  funext q
  refine Quotient.inductionOn q ?_
  intro s
  rfl


/-! ## ENDOGENOUS FUTURE-CONTEXT MDL — no privileged infinite test catalogue

An instantaneous observer may identify states which DIFFER after one or
more already admitted operations.  The correct MDL quotient of a retained
history is the kernel of the WHOLE future test signature, not that of the
current bare readout.  The universe of test words is GENERATED from the
already supplied native actions (free finite lists), not externally assumed.
Unlike a bare observational quotient, this quotient ALWAYS admits all
original operations as well-defined state dynamics, without separately
postulating any pullback compatibility.

This is a theorem about a supplied operational action/test class.  It does
not choose the action alphabet, its physical cost or the G0/Book apparatus.
-/

/-- A D0-like native finite-history interface.  The State is understood to
include all actually retained records and prepared controller states. -/
structure FutureExecution where
  State : Type
  Action : Type
  Test : Type
  Outcome : Type
  step : Action → State → State
  observe : State → Test → Outcome

/-- Chronological execution of any FINITE word of allowed operations. -/
def FutureExecution.run (F : FutureExecution)
    (w : List F.Action) (s : F.State) : F.State :=
  w.foldl (fun x a => F.step a x) s

/-- Complete future observational profile, including the empty word. -/
def FutureExecution.profile (F : FutureExecution) (s : F.State) :
    List F.Action → F.Test → F.Outcome :=
  fun w t => F.observe (F.run w s) t

/-- Applying a primitive action pulls a future experiment back to the
same original source state preceded by that exact primitive. -/
theorem FutureExecution.profile_step (F : FutureExecution)
    (a : F.Action) (s : F.State) (w : List F.Action) (t : F.Test) :
    F.profile (F.step a s) w t = F.profile s (a :: w) t := rfl

/-- The canonical equivalence is EXACT equality in ALL possible future
tests generated by the original legal operations, not merely at t=0. -/
def FutureExecution.futureSetoid (F : FutureExecution) : Setoid F.State :=
  Setoid.ker (F.profile)

/-- The canonical minimal retained-history STATE relative to the test/
action alphabet itself.  No preferred original state labels survive. -/
abbrev FutureExecution.FutureClass (F : FutureExecution) :=
  Quotient F.futureSetoid

/-- Equal complete futures stay equal after EVERY existing action.
This is the missing composition congruence, now derived, not assumed. -/
theorem FutureExecution.profile_step_congr (F : FutureExecution)
    {s t : F.State} (h : F.profile s = F.profile t) (a : F.Action) :
    F.profile (F.step a s) = F.profile (F.step a t) := by
  funext w e
  exact congrFun (congrFun h (a :: w)) e

/-- All original actions AUTOMATICALLY descend to the canonical future
quotient, even if the instantaneous observation quotient does NOT. -/
def FutureExecution.quotientStep (F : FutureExecution) (a : F.Action) :
    F.FutureClass → F.FutureClass :=
  Quotient.lift
    (fun s => Quotient.mk F.futureSetoid (F.step a s))
    (by
      intro s t h
      exact Quotient.sound (F.profile_step_congr h a))

/-- No dynamics is lost by quotienting future-indistinguishable histories. -/
theorem FutureExecution.quotientStep_mk (F : FutureExecution)
    (a : F.Action) (s : F.State) :
    F.quotientStep a (Quotient.mk F.futureSetoid s) =
      Quotient.mk F.futureSetoid (F.step a s) := rfl

/-- The complete observational profile on the canonical quotient is
faithful by CONSTRUCTION; no extra representational injectivity axiom. -/
def FutureExecution.quotientProfile (F : FutureExecution) :
    F.FutureClass → List F.Action → F.Test → F.Outcome :=
  Quotient.lift F.profile (fun _ _ h => h)

/-- The future-profile embedding is injective, even for infinite carriers. -/
theorem FutureExecution.quotientProfile_injective (F : FutureExecution) :
    Function.Injective F.quotientProfile := by
  intro q r h
  revert h
  refine Quotient.inductionOn₂ q r ?_
  intro s t h
  exact Quotient.sound h

/-- Any decoder of ALL future profiles from a compressed memory C must
retain every distinction in the canonical future quotient. -/
theorem FutureExecution.sufficient_memory_reflects_future
    (F : FutureExecution) {C : Type}
    (encode : F.State → C)
    (decode : C → List F.Action → F.Test → F.Outcome)
    (correct : ∀ s, decode (encode s) = F.profile s)
    {s t : F.State} (heq : encode s = encode t) :
    (Quotient.mk F.futureSetoid s : F.FutureClass) =
      Quotient.mk F.futureSetoid t := by
  apply Quotient.sound
  exact (correct s).symm.trans ((congrArg decode heq).trans (correct t))

/-- In any sufficiently expressive future-complete memory, the canonical
future equivalence is EXACTLY the coarsest relation preserved by every
allowed state transition and every current readout. -/
theorem FutureExecution.largest_observation_stable_relation
    (F : FutureExecution) (R : F.State → F.State → Prop)
    (reads : ∀ s t, R s t → ∀ e, F.observe s e = F.observe t e)
    (steps : ∀ a s t, R s t → R (F.step a s) (F.step a t))
    {s t : F.State} (h : R s t) :
    F.profile s = F.profile t := by
  have extend : ∀ w : List F.Action, ∀ x y : F.State, R x y →
      R (F.run w x) (F.run w y) := by
    intro w
    induction w with
    | nil =>
        intro x y hxy
        exact hxy
    | cons a w ih =>
        intro x y hxy
        exact ih (F.step a x) (F.step a y) (steps a x y hxy)
  funext w e
  exact reads (F.run w s) (F.run w t) (extend w s t h) e

/-- The general empirical-theory factorization already owned by D0
applies to this FUTURE test family with no extra representation axiom. -/
def FutureExecution.futureEmpiricalTheory (F : FutureExecution) :
    EmpiricalTheory where
  State := F.State
  Test := List F.Action × F.Test
  Catalogue := Unit
  Outcome := F.Outcome
  observe := fun s _ context => F.profile s context.1 context.2

/-- An ORIGINAL operation supplies its own canonical pullback on
generated experimental contexts, hence automatically descends to the
existing universal empirical quotient theorem. -/
def FutureExecution.asOperationalProcess (F : FutureExecution)
    (a : F.Action) : OperationalProcess F.futureEmpiricalTheory where
  run := F.step a
  pullTest := fun context => (a :: context.1, context.2)
  compatible := by
    intro s _ context
    exact F.profile_step a s context.1 context.2

/-! ## Exact negative control: CURRENT equivalence can delete REAL archive

A current Boolean detector reads only one bit of a two-bit actual state.
One admissible future action copies its archival bit into the detector bit.
Current observations equate two states which that one future action
separates.  A future-complete state memory therefore needs four states,
not the two naive current-result states.  This has an explicit M1
interpretation: trimming the unseen archive is UNSOUND when an admitted
future operation can reveal it.
-/

/-- State = (visible bit, hidden-but-retained archive bit). -/
def hiddenBitExecution : FutureExecution where
  State := Bool × Bool
  Action := Bool
  Test := Unit
  Outcome := Bool
  step := fun a s => if a then (s.2, s.2) else s
  observe := fun s _ => s.1

theorem hiddenBit_same_current :
    hiddenBitExecution.observe (false, false) () =
      hiddenBitExecution.observe (false, true) () := rfl

theorem hiddenBit_different_future :
    hiddenBitExecution.profile (false, false) ≠
      hiddenBitExecution.profile (false, true) := by
  intro h
  have hh := congrFun (congrFun h [true]) ()
  have impossible : false = true := by
    simpa [FutureExecution.profile, FutureExecution.run, hiddenBitExecution] using hh
  cases impossible

/-- Complete future experiments recover BOTH actual record bits; thus the
archive bit is genuinely forced by FUTURE predictability, not chosen for
convenience. -/
theorem hiddenBit_futureProfile_injective :
    Function.Injective hiddenBitExecution.profile := by
  intro s t h
  rcases s with ⟨s0, s1⟩
  rcases t with ⟨t0, t1⟩
  have h0 : s0 = t0 := by
    simpa [FutureExecution.profile, FutureExecution.run, hiddenBitExecution] using
      (congrFun (congrFun h []) ())
  have h1 : s1 = t1 := by
    simpa [FutureExecution.profile, FutureExecution.run, hiddenBitExecution] using
      (congrFun (congrFun h [true]) ())
  cases h0
  cases h1
  rfl

/-- Any memory predicting the WHOLE original future correctly must
distinguish all four original hidden/visible-bit states. -/
theorem hiddenBit_sufficient_encoder_injective {C : Type}
    (encode : hiddenBitExecution.State → C)
    (decode : C → List hiddenBitExecution.Action →
       hiddenBitExecution.Test → hiddenBitExecution.Outcome)
    (correct : ∀ s, decode (encode s) = hiddenBitExecution.profile s) :
    Function.Injective encode := by
  intro s t h
  apply hiddenBit_futureProfile_injective
  exact (correct s).symm.trans ((congrArg decode h).trans (correct t))

/-- The lower bound is FOUR archived states, not TWO current Boolean
outcomes. It is independent of the choice of source encodings. -/
theorem hiddenBit_minimum_future_memory_four {C : Type} [Fintype C]
    (encode : hiddenBitExecution.State → C)
    (decode : C → List hiddenBitExecution.Action →
       hiddenBitExecution.Test → hiddenBitExecution.Outcome)
    (correct : ∀ s, decode (encode s) = hiddenBitExecution.profile s) :
    4 ≤ Fintype.card C := by
  have hinj := hiddenBit_sufficient_encoder_injective encode decode correct
  simpa using (Fintype.card_le_of_injective encode hinj)

end D0.Foundation.EmpiricalTheoryFactorization
