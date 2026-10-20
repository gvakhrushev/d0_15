import D0.Foundation.VerifiabilityNecessity
import D0.Foundation.FutureExecution
import Mathlib.Computability.Partrec

/-!
# One verification kernel on the complete future carrier

The existing necessity, empirical-factorization and future-memory owners are
composed here on the SAME carrier.  A supplied `TheoryVerification` of the
future empirical theory gives a represented state, record and comparator for
every native state.  Their kernel is proved to be equality of all admitted
future profiles.  Every original action and every finite word commute with
that representation.

The book's coded Sigma interface is conditional on an explicit finite-code
presentation.  Round trips, shortlex minimality and genuine `Computable`
witnesses are supplied separately; they are not extracted from an abstract
quotient or from classical decidable equality.  Finite chronological archive
access is constructed and its computability is proved.

No physical admission, causal independence of apparatus lines, action price,
prospective optimum, gravitational equation or clock calibration is assumed
or concluded here.
-/

namespace D0.Foundation.EmpiricalTheoryFactorization

theorem FutureExecution.run_append (F : FutureExecution)
    (u v : List F.Action) (s : F.State) :
    F.run (u ++ v) s = F.run v (F.run u s) := by
  simp only [FutureExecution.run, List.foldl_append]

theorem FutureExecution.profile_run (F : FutureExecution)
    (u : List F.Action) (s : F.State) (v : List F.Action) (t : F.Test) :
    F.profile (F.run u s) v t = F.profile s (u ++ v) t := by
  simp only [FutureExecution.profile, F.run_append]

theorem FutureExecution.empiricalClass_eq_iff_profile (F : FutureExecution)
    (s t : F.State) :
    empiricalClass F.futureEmpiricalTheory s =
      empiricalClass F.futureEmpiricalTheory t ↔ F.profile s = F.profile t := by
  constructor
  · intro h
    have hs := Quotient.exact h
    funext w q
    exact congrFun (congrFun hs ()) (w, q)
  · intro h
    apply Quotient.sound
    funext c context
    exact congrFun (congrFun h context.1) context.2

/-- The two owned quotients identify exactly the same states.  This map is
constructed from their defining profiles; no quotient equivalence is assumed. -/
def FutureExecution.futureClassEquivEmpirical (F : FutureExecution) :
    F.FutureClass ≃ EmpiricalState F.futureEmpiricalTheory where
  toFun := Quotient.lift (empiricalClass F.futureEmpiricalTheory) (by
    intro s t h
    exact (F.empiricalClass_eq_iff_profile s t).mpr h)
  invFun := Quotient.lift (fun s => Quotient.mk F.futureSetoid s) (by
    intro s t h
    apply Quotient.sound
    funext w q
    exact congrFun (congrFun h ()) (w, q))
  left_inv := by
    intro q
    refine Quotient.inductionOn q ?_
    intro s
    rfl
  right_inv := by
    intro q
    refine Quotient.inductionOn q ?_
    intro s
    rfl

@[simp] theorem FutureExecution.futureClassEquivEmpirical_mk (F : FutureExecution)
    (s : F.State) :
    F.futureClassEquivEmpirical (Quotient.mk F.futureSetoid s) =
      empiricalClass F.futureEmpiricalTheory s := rfl

theorem FutureExecution.futureClassEquivEmpirical_step (F : FutureExecution)
    (a : F.Action) (q : F.FutureClass) :
    F.futureClassEquivEmpirical (F.quotientStep a q) =
      empiricalProcess F.futureEmpiricalTheory (F.asOperationalProcess a)
        (F.futureClassEquivEmpirical q) := by
  refine Quotient.inductionOn q ?_
  intro s
  rfl

theorem FutureExecution.futureClassEquivEmpirical_evaluate (F : FutureExecution)
    (q : F.FutureClass) (w : List F.Action) (t : F.Test) :
    evaluate F.futureEmpiricalTheory (F.futureClassEquivEmpirical q) () (w, t) =
      F.quotientProfile q w t := by
  refine Quotient.inductionOn q ?_
  intro s
  rfl

end D0.Foundation.EmpiricalTheoryFactorization

namespace D0.Foundation.VerificationCore

open D0.Foundation.EmpiricalTheoryFactorization
open D0.Foundation.VerifiabilityNecessity
open D0.Foundation.M1ClassAdmissibility

variable {F : FutureExecution}

/-- The verified state representing the complete native future class. -/
def representedState (E : TheoryVerification F.futureEmpiricalTheory)
    (s : F.State) : E.protocol.State :=
  E.represents.symm (empiricalClass F.futureEmpiricalTheory s)

def representedStep (E : TheoryVerification F.futureEmpiricalTheory)
    (a : F.Action) (p : E.protocol.State) : E.protocol.State :=
  E.represents.symm
    (empiricalProcess F.futureEmpiricalTheory (F.asOperationalProcess a)
      (E.represents p))

def representedRun (E : TheoryVerification F.futureEmpiricalTheory)
    (w : List F.Action) (p : E.protocol.State) : E.protocol.State :=
  w.foldl (fun x a => representedStep E a x) p

def representedRead (E : TheoryVerification F.futureEmpiricalTheory)
    (p : E.protocol.State) (w : List F.Action) (t : F.Test) : F.Outcome :=
  evaluate F.futureEmpiricalTheory (E.represents p) () (w, t)

/-- The same supplied verified states are exactly the native future quotient. -/
def verifiedStateFutureEquiv (E : TheoryVerification F.futureEmpiricalTheory) :
    E.protocol.State ≃ F.FutureClass :=
  E.represents.trans F.futureClassEquivEmpirical.symm

theorem representedState_eq_iff (E : TheoryVerification F.futureEmpiricalTheory)
    (s t : F.State) :
    representedState E s = representedState E t ↔ F.profile s = F.profile t := by
  constructor
  · intro h
    exact (F.empiricalClass_eq_iff_profile s t).mp (E.represents.symm.injective h)
  · intro h
    exact congrArg E.represents.symm ((F.empiricalClass_eq_iff_profile s t).mpr h)

theorem representedState_step (E : TheoryVerification F.futureEmpiricalTheory)
    (a : F.Action) (s : F.State) :
    representedState E (F.step a s) =
      representedStep E a (representedState E s) := by
  simp only [representedState, representedStep, Equiv.apply_symm_apply]
  rfl

theorem representedRun_state (E : TheoryVerification F.futureEmpiricalTheory)
    (w : List F.Action) (s : F.State) :
    representedRun E w (representedState E s) = representedState E (F.run w s) := by
  induction w generalizing s with
  | nil => rfl
  | cons a w ih =>
      change representedRun E w (representedStep E a (representedState E s)) =
        representedState E (F.run w (F.step a s))
      rw [← representedState_step]
      exact ih (F.step a s)

theorem representedRun_append (E : TheoryVerification F.futureEmpiricalTheory)
    (u v : List F.Action) (p : E.protocol.State) :
    representedRun E (u ++ v) p = representedRun E v (representedRun E u p) := by
  simp only [representedRun, List.foldl_append]

theorem representedRead_state (E : TheoryVerification F.futureEmpiricalTheory)
    (s : F.State) (w : List F.Action) (t : F.Test) :
    representedRead E (representedState E s) w t = F.profile s w t := by
  simp only [representedRead, representedState, Equiv.apply_symm_apply]
  rfl

def representedRecord (E : TheoryVerification F.futureEmpiricalTheory)
    (s : F.State) : E.protocol.Record := E.protocol.record (representedState E s)

/-- Persistent verified records have precisely the complete future kernel. -/
theorem representedRecord_eq_iff (E : TheoryVerification F.futureEmpiricalTheory)
    (s t : F.State) :
    representedRecord E s = representedRecord E t ↔ F.profile s = F.profile t := by
  constructor
  · intro h
    exact (representedState_eq_iff E s t).mp (record_injective E.contract h)
  · intro h
    exact congrArg E.protocol.record ((representedState_eq_iff E s t).mpr h)

theorem representedComparison_iff (E : TheoryVerification F.futureEmpiricalTheory)
    (l : E.protocol.Line) (c : E.protocol.Catalogue) (s t : F.State) :
    E.protocol.compare l c (representedRecord E s) (representedRecord E t) = true ↔
      F.profile s ≠ F.profile t := by
  change E.protocol.compare l c
    (E.protocol.record (representedState E s))
    (E.protocol.record (representedState E t)) = true ↔ _
  rw [E.contract.correct]
  simp only [decide_eq_true_eq]
  exact not_congr (representedState_eq_iff E s t)

theorem representedComparison_catalogue_independent
    (E : TheoryVerification F.futureEmpiricalTheory)
    (l l' : E.protocol.Line) (c c' : E.protocol.Catalogue) (s t : F.State) :
    E.protocol.compare l c (representedRecord E s) (representedRecord E t) =
      E.protocol.compare l' c' (representedRecord E s) (representedRecord E t) :=
  verification_lines_agree E.contract l l' c c' (representedState E s) (representedState E t)

/-- Any sufficient native memory is also sufficient for the SAME represented
record: the memory theorem and record necessity now meet on their actual maps. -/
theorem sufficient_memory_preserves_record
    (E : TheoryVerification F.futureEmpiricalTheory) {Memory : Type}
    (encode : F.State → Memory)
    (decode : Memory → List F.Action → F.Test → F.Outcome)
    (correct : ∀ s, decode (encode s) = F.profile s)
    {s t : F.State} (h : encode s = encode t) :
    representedRecord E s = representedRecord E t := by
  have hq := F.sufficient_memory_reflects_future encode decode correct h
  apply (representedRecord_eq_iff E s t).mpr
  exact Quotient.exact hq

/-- The retained hidden bit stays distinguishable in EVERY verified realization. -/
theorem hiddenBit_records_distinct
    (E : TheoryVerification hiddenBitExecution.futureEmpiricalTheory) :
    representedRecord E (false, false) ≠ representedRecord E (false, true) := by
  intro h
  exact hiddenBit_different_future ((representedRecord_eq_iff E _ _).mp h)

/-- A completely uncoupled bit creates no new represented empirical record. -/
theorem uncoupledCenter_records_equal (F : FutureExecution)
    (E : TheoryVerification F.uncoupledCenter.futureEmpiricalTheory)
    (s : F.State) (b b' : Bool) :
    representedRecord E (s, b) = representedRecord E (s, b') :=
  (representedRecord_eq_iff E _ _).mpr (F.uncoupledCenter_profile_independent s b b')

/-- A scoped kernel theorem, with the actual commutation and record maps.
The E hypothesis is the owned verification representation of this exact future
interface; it does not assert that every abstract theory already has one. -/
theorem verification_core (E : TheoryVerification F.futureEmpiricalTheory) :
    FunctionalTuple E.protocol ∧
    (¬ CatalogueOutsourced E.protocol) ∧
    (∀ s t, representedRecord E s = representedRecord E t ↔ F.profile s = F.profile t) ∧
    (∀ w s, representedRun E w (representedState E s) = representedState E (F.run w s)) ∧
    (∀ l c s t,
      E.protocol.compare l c (representedRecord E s) (representedRecord E t) = true ↔
        F.profile s ≠ F.profile t) := by
  have owned := m1_regress_closure_via_verifiability E
  exact ⟨owned.1, owned.2.2, representedRecord_eq_iff E,
    representedRun_state E, representedComparison_iff E⟩

/-! ## Explicit finite-code realization of the Book 01 Sigma roles -/

/-- The book order is length followed by lexicographic order. -/
def ShortlexLE {Symbol : Type} [LT Symbol] (s t : List Symbol) : Prop :=
  s.length < t.length ∨
    (s.length = t.length ∧ (s = t ∨ List.Lex (fun a b => a < b) s t))

/-- A supplied code presentation, not a conclusion of bare verifiability.
The minimality premise states the exact shortlex property on valid codes.
Invalid strings remain syntax; no new physical object is decoded from them. -/
structure CodePresentation (Symbol Object : Type) [LinearOrder Symbol] where
  encode : Object → List Symbol
  decode : List Symbol → Option Object
  decode_encode : ∀ x, decode (encode x) = some x
  shortlex_minimal : ∀ x c, decode c = some x → ShortlexLE (encode x) c

namespace CodePresentation

variable {Symbol Object : Type} [LinearOrder Symbol]

theorem encode_injective (K : CodePresentation Symbol Object) :
    Function.Injective K.encode := by
  intro x y h
  have hd := congrArg K.decode h
  rw [K.decode_encode, K.decode_encode] at hd
  exact Option.some.inj hd

def canon (K : CodePresentation Symbol Object) (c : List Symbol) : List Symbol :=
  match K.decode c with
  | none => c
  | some x => K.encode x

@[simp] theorem canon_encode (K : CodePresentation Symbol Object) (x : Object) :
    K.canon (K.encode x) = K.encode x := by
  simp [canon, K.decode_encode]

theorem canon_idempotent (K : CodePresentation Symbol Object) (c : List Symbol) :
    K.canon (K.canon c) = K.canon c := by
  cases hc : K.decode c with
  | none => simp [canon, hc]
  | some x => simp [canon, hc, K.decode_encode]

theorem canon_minimal (K : CodePresentation Symbol Object)
    (c : List Symbol) (x : Object) (h : K.decode c = some x) :
    ShortlexLE (K.canon c) c := by
  simpa [canon, h] using K.shortlex_minimal x c h

def delta (K : CodePresentation Symbol Object) (c d : List Symbol) : Bool :=
  decide (K.canon c ≠ K.canon d)

theorem delta_refl (K : CodePresentation Symbol Object) (c : List Symbol) :
    K.delta c c = false := by simp [delta]

theorem delta_encode_iff (K : CodePresentation Symbol Object) (x y : Object) :
    K.delta (K.encode x) (K.encode y) = true ↔ x ≠ y := by
  simp only [delta, canon_encode, decide_eq_true_eq]
  constructor
  · intro h hxy
    exact h (congrArg K.encode hxy)
  · intro h hcode
    exact h (K.encode_injective hcode)

end CodePresentation

/-- A finite supplied enumeration has a concrete singleton-code realization.
This is a consistency witness, not a claim that this alphabet is physically
selected or globally optimal among all possible alphabets. -/
def singletonCodePresentation {Object : Type} {n : Nat} (e : Object ≃ Fin n) :
    CodePresentation (Fin n) Object where
  encode x := [e x]
  decode c := match c with
    | [i] => some (e.symm i)
    | _ => none
  decode_encode := by intro x; simp
  shortlex_minimal := by
    intro x c h
    cases c with
    | nil => cases h
    | cons i rest =>
        cases rest with
        | nil =>
            have hx : e.symm i = x := Option.some.inj h
            have hi : e x = i := by rw [← hx]; exact e.apply_symm_apply i
            exact Or.inr ⟨rfl, Or.inl (congrArg (fun j => [j]) hi)⟩
        | cons j rest => cases h

theorem singletonCodePresentation_canon {Object : Type} {n : Nat}
    (e : Object ≃ Fin n) (c : List (Fin n)) :
    (singletonCodePresentation e).canon c = c := by
  cases c with
  | nil => rfl
  | cons i rest =>
      cases rest with
      | nil => simp [CodePresentation.canon, singletonCodePresentation]
      | cons j rest => rfl

theorem singletonCodePresentation_canonical_computable {Object : Type} {n : Nat}
    (e : Object ≃ Fin n) : Computable (singletonCodePresentation e).canon :=
  Computable.id.of_eq (fun c => (singletonCodePresentation_canon e c).symm)

theorem singletonCodePresentation_comparison_computable {Object : Type} {n : Nat}
    (e : Object ≃ Fin n) : Computable₂ (singletonCodePresentation e).delta := by
  have hne : Primrec₂ (fun c d : List (Fin n) => decide (c ≠ d)) :=
    PrimrecRel.decide (PrimrecPred.not Primrec.eq)
  have hdelta : (singletonCodePresentation e).delta =
      (fun c d : List (Fin n) => decide (c ≠ d)) := by
    funext c d
    simp only [CodePresentation.delta, singletonCodePresentation_canon]
  rw [hdelta]
  exact hne.to_comp

/-- State facts and registered state-plus-line facts share one tagged code
universe.  The tags and line coordinate are internal data, not an external
format/provenance catalogue. -/
abbrev SigmaObject (E : TheoryVerification F.futureEmpiricalTheory) :=
  Sum E.protocol.State (E.protocol.State × E.protocol.Line)

structure SigmaWitness (E : TheoryVerification F.futureEmpiricalTheory) where
  Symbol : Type
  [symbolFinite : Fintype Symbol]
  [symbolOrder : LinearOrder Symbol]
  [symbolCoding : Primcodable Symbol]
  coding : CodePresentation Symbol (SigmaObject E)
  canonical_computable : Computable coding.canon
  comparison_computable : Computable₂ coding.delta

attribute [instance] SigmaWitness.symbolFinite SigmaWitness.symbolOrder SigmaWitness.symbolCoding

/-- The coded interface is inhabited whenever the verified state and line
carriers have supplied finite enumerations.  The semantic enumeration is
noncomputable in this generic construction; canonization is literally the
identity and comparison/access are nevertheless proved computable on codes.
No encoder for arbitrary infinite raw states is inferred. -/
noncomputable def finiteSigmaWitness
    (E : TheoryVerification F.futureEmpiricalTheory)
    [Fintype E.protocol.State] [Fintype E.protocol.Line] : SigmaWitness E where
  Symbol := Fin (Fintype.card (SigmaObject E))
  coding := singletonCodePresentation (Fintype.equivFin (SigmaObject E))
  canonical_computable :=
    singletonCodePresentation_canonical_computable (Fintype.equivFin (SigmaObject E))
  comparison_computable :=
    singletonCodePresentation_comparison_computable (Fintype.equivFin (SigmaObject E))

namespace SigmaWitness

variable {E : TheoryVerification F.futureEmpiricalTheory}

def dmin (W : SigmaWitness E) (s : F.State) : List W.Symbol :=
  W.coding.encode (Sum.inl (representedState E s))

def archiveCode (W : SigmaWitness E) (entry : F.State × E.protocol.Line) : List W.Symbol :=
  W.coding.encode (Sum.inr (representedState E entry.1, entry.2))

def archive (W : SigmaWitness E) (history : List (F.State × E.protocol.Line)) :
    List (List W.Symbol) := history.map W.archiveCode

/-- R(n) is the finite frame of codes registered up to this chronological
index.  The ordered list remains available: taking its set does not erase the
positions used by access.  This is not a calibrated physical duration. -/
def historyFrame (W : SigmaWitness E) (history : List (List W.Symbol))
    (n : Nat) : Set (List W.Symbol) := {c | c ∈ history.take (n + 1)}

/-- O reads an already stored code by its recorded position. -/
def query (W : SigmaWitness E) (history : List (List W.Symbol))
    (n : Nat) : Option (List W.Symbol) := history[n]?

theorem query_computable (W : SigmaWitness E) : Computable₂ W.query :=
  Computable.list_getElem?

theorem dmin_canonical (W : SigmaWitness E) (s : F.State) :
    W.coding.canon (W.dmin s) = W.dmin s :=
  W.coding.canon_encode _

theorem dmin_minimal (W : SigmaWitness E) (s : F.State) (c : List W.Symbol)
    (h : W.coding.decode c = some (Sum.inl (representedState E s))) :
    ShortlexLE (W.dmin s) c := W.coding.shortlex_minimal _ c h

theorem dmin_eq_iff (W : SigmaWitness E) (s t : F.State) :
    W.dmin s = W.dmin t ↔ F.profile s = F.profile t := by
  constructor
  · intro h
    exact (representedState_eq_iff E s t).mp (Sum.inl.inj (W.coding.encode_injective h))
  · intro h
    exact congrArg (fun p => W.coding.encode (Sum.inl p))
      ((representedState_eq_iff E s t).mpr h)

theorem delta_dmin_iff (W : SigmaWitness E) (s t : F.State) :
    W.coding.delta (W.dmin s) (W.dmin t) = true ↔ F.profile s ≠ F.profile t := by
  change W.coding.delta (W.coding.encode _) (W.coding.encode _) = true ↔ _
  rw [W.coding.delta_encode_iff]
  constructor
  · intro h hprof
    exact h (congrArg Sum.inl ((representedState_eq_iff E s t).mpr hprof))
  · intro h heq
    exact h ((representedState_eq_iff E s t).mp (Sum.inl.inj heq))

/-- All future distinctions AND independent-line provenance survive encoding. -/
theorem archiveCode_eq_iff (W : SigmaWitness E)
    (s t : F.State) (l l' : E.protocol.Line) :
    W.archiveCode (s, l) = W.archiveCode (t, l') ↔
      F.profile s = F.profile t ∧ l = l' := by
  constructor
  · intro h
    have hp := Sum.inr.inj (W.coding.encode_injective h)
    exact ⟨(representedState_eq_iff E s t).mp (congrArg Prod.fst hp),
      congrArg Prod.snd hp⟩
  · rintro ⟨hp, hl⟩
    have hs := (representedState_eq_iff E s t).mpr hp
    exact congrArg (fun p => W.coding.encode (Sum.inr p)) (Prod.ext hs hl)

theorem archive_preserves_line (W : SigmaWitness E)
    (s : F.State) (l l' : E.protocol.Line) (h : l ≠ l') :
    W.archiveCode (s, l) ≠ W.archiveCode (s, l') := by
  intro heq
  exact h ((W.archiveCode_eq_iff s s l l').mp heq).2

theorem archive_length (W : SigmaWitness E)
    (history : List (F.State × E.protocol.Line)) :
    (W.archive history).length = history.length := by simp [archive]

theorem query_archive (W : SigmaWitness E)
    (history : List (F.State × E.protocol.Line)) (n : Nat) :
    W.query (W.archive history) n = (history[n]?).map W.archiveCode := by
  induction history generalizing n with
  | nil => cases n <;> rfl
  | cons a history ih =>
      cases n with
      | zero => rfl
      | succ n => exact ih n

theorem query_append_retains (W : SigmaWitness E)
    (history later : List (List W.Symbol)) (n : Nat) (hn : n < history.length) :
    W.query (history ++ later) n = W.query history n := by
  induction history generalizing n with
  | nil => simp at hn
  | cons a history ih =>
      cases n with
      | zero => rfl
      | succ n =>
          apply ih n
          simpa only [List.length_cons, Nat.succ_lt_succ_iff] using hn

/-- The coded book roles realize the already proved future kernel.  Effective
canonization/comparison are named hypotheses of W; archive access is proved
computable.  None is inferred from mere existence of a semantic quotient. -/
theorem coded_verification_core (W : SigmaWitness E) :
    FunctionalTuple E.protocol ∧
    (∀ s t, W.dmin s = W.dmin t ↔ F.profile s = F.profile t) ∧
    (∀ s t, W.coding.delta (W.dmin s) (W.dmin t) = true ↔ F.profile s ≠ F.profile t) ∧
    (∀ s t l l', W.archiveCode (s, l) = W.archiveCode (t, l') ↔
      F.profile s = F.profile t ∧ l = l') ∧
    Computable W.coding.canon ∧ Computable₂ W.coding.delta ∧ Computable₂ W.query :=
  ⟨verifiability_forces_functional_tuple E, W.dmin_eq_iff, W.delta_dmin_iff,
    W.archiveCode_eq_iff, W.canonical_computable, W.comparison_computable,
    W.query_computable⟩

end SigmaWitness
end D0.Foundation.VerificationCore
