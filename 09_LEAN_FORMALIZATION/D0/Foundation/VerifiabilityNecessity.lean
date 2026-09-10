import Mathlib.Tactic
import D0.Foundation.EmpiricalTheoryFactorization
import D0.Foundation.InformationConnectivity

/-!
# Verifiability forces the D0 functional tuple and class-level M1

This module moves M1 one logical floor downward.  It does not postulate catalogue-freedom.
Instead it starts from the operational content of an independently verifiable distinction:

* there are at least two distinguishable states;
* a state leaves a persistent record;
* at least two registered verification lines compare records;
* every line returns the same equality/difference truth for every catalogue value.

From that contract Lean derives, rather than assumes:

1. the record map is injective, so a record cannot erase a distinction and still verify it;
2. every verification line is class-M1 admissible (catalogue independent);
3. all lines agree, including across different catalogue values;
4. record connectivity is exactly equality on verified states;
5. the operational empirical quotient is equivalent to the verified state carrier.
6. bare verified outcomes collapse independent-line identity, so any faithful provenance archive
   must distinguish the lines and has the corresponding finite capacity lower bound.

The three role names below are only semantic labels.  `RoleImplementation`-style coverage is
formalized independently of names: every complete language has the same three-element semantic
image, a renamed language is equivalent, and a duplicated fourth name is removable.  Thus the
MDL statement concerns necessary functions, not English words or hardware component count.

The finite controls are load-bearing:

* one state removes distinction;
* one record value destroys retention;
* a constant comparator destroys verification;
* one line destroys independent repetition;
* a catalogue-sensitive comparator can work under one privileged catalogue but is not verifiable.

Exact scope: this is a theorem about operationally verifiable empirical descriptions.  It does
not assert that a physical apparatus instantiates the contract; that remains the ordinary
representation/application obligation, as in T50--T52.
-/

namespace D0.Foundation.VerifiabilityNecessity

open D0.Foundation.M1ClassAdmissibility
open D0.Foundation.EmpiricalTheoryFactorization

/-- A verification apparatus before correctness is imposed.  `State` may already be an
observational quotient, so this interface does not require microscopic state discrimination. -/
structure VerificationProtocol where
  State : Type
  Record : Type
  Line : Type
  Catalogue : Type
  [stateDecidableEq : DecidableEq State]
  record : State → Record
  compare : Line → Catalogue → Record → Record → Bool

attribute [instance] VerificationProtocol.stateDecidableEq

/-- The operational verification contract.  The two line labels register independent repetition;
their physical causal independence is an application obligation.  Correctness is required for
every catalogue value, so no privileged background choice can carry the result. -/
structure VerificationContract (P : VerificationProtocol) : Prop where
  state_nontrivial : Nontrivial P.State
  line_nontrivial : Nontrivial P.Line
  catalogue_nonempty : Nonempty P.Catalogue
  correct : ∀ l c x y,
    P.compare l c (P.record x) (P.record y) = decide (x ≠ y)

/-- The three irreducible semantic functions.  Names and physical implementations may vary. -/
inductive FunctionalRole
  | distinction
  | retention
  | comparison
  deriving DecidableEq, Fintype, Repr

/-- The tuple forced by an operational verification contract. -/
structure FunctionalTuple (P : VerificationProtocol) : Prop where
  distinction : ∃ x y : P.State, x ≠ y
  retention : Function.Injective P.record
  comparison : ∀ l c x y,
    P.compare l c (P.record x) (P.record y) = true ↔ x ≠ y
  repeated_line : ∃ l₀ l₁ : P.Line, l₀ ≠ l₁
  catalogue_invariant : ∀ l c c' x y,
    P.compare l c (P.record x) (P.record y) =
      P.compare l c' (P.record x) (P.record y)

/-- The catalogue system seen by one registered line on pairs of verified states. -/
def verificationCatalogueSystem (P : VerificationProtocol) : CatalogueSystem where
  Candidate := P.Line
  Catalogue := P.Catalogue
  Output := P.State → P.State → Bool
  eval l c x y := P.compare l c (P.record x) (P.record y)

/-- Retention is forced by correctness: if two states left one record, comparing that record with
itself would have to return both "same" and "different". -/
theorem record_injective {P : VerificationProtocol} (V : VerificationContract P) :
    Function.Injective P.record := by
  intro x y hrecord
  by_contra hxy
  obtain ⟨l, _, _⟩ := V.line_nontrivial.exists_pair_ne
  obtain ⟨c⟩ := V.catalogue_nonempty
  have hdiff : P.compare l c (P.record x) (P.record y) = true := by
    simpa [hxy] using V.correct l c x y
  have hsame : P.compare l c (P.record y) (P.record y) = false := by
    simpa using V.correct l c y y
  rw [hrecord] at hdiff
  cases hdiff.symm.trans hsame

/-- M1 is a consequence of public correctness: changing a catalogue cannot change a result that
is already fixed by the same independently checkable truth value. -/
theorem m1_as_verifiability_necessity {P : VerificationProtocol}
    (V : VerificationContract P) (l : P.Line) :
    M1ClassAdmissible (verificationCatalogueSystem P) l := by
  intro c c'
  funext x y
  change P.compare l c (P.record x) (P.record y) =
    P.compare l c' (P.record x) (P.record y)
  rw [V.correct, V.correct]

/-- Different registered lines and different catalogue values all agree on verified content. -/
theorem verification_lines_agree {P : VerificationProtocol}
    (V : VerificationContract P) (l l' : P.Line) (c c' : P.Catalogue)
    (x y : P.State) :
    P.compare l c (P.record x) (P.record y) =
      P.compare l' c' (P.record x) (P.record y) := by
  rw [V.correct, V.correct]

/-- The complete observable behaviour of one registered verification line. -/
def verificationLineOutcome (P : VerificationProtocol) (l : P.Line) :
    P.Catalogue → P.State → P.State → Bool :=
  fun c x y => P.compare l c (P.record x) (P.record y)

/-- Correct independent lines are extensionally identical in the bare outcome layer. -/
theorem verificationLineOutcome_eq {P : VerificationProtocol}
    (V : VerificationContract P) (l l' : P.Line) :
    verificationLineOutcome P l = verificationLineOutcome P l' := by
  funext c x y
  exact verification_lines_agree V l l' c c x y

/-- A bare detector-output table cannot faithfully retain the identity of two independent lines:
correctness makes every line's table equal, while verification requires at least two lines. -/
theorem verified_lines_collapse_in_outcome_layer {P : VerificationProtocol}
    (V : VerificationContract P) :
    ¬ Function.Injective (verificationLineOutcome P) := by
  intro hinjective
  obtain ⟨l, l', hne⟩ := V.line_nontrivial.exists_pair_ne
  exact hne (hinjective (verificationLineOutcome_eq V l l'))

/-- Add an explicit provenance/archive coordinate to the common detector outcome. -/
def archivedVerificationLine (P : VerificationProtocol) (l : P.Line) :
    (P.Catalogue → P.State → P.State → Bool) × P.Line :=
  (verificationLineOutcome P l, l)

theorem archivedVerificationLine_injective (P : VerificationProtocol) :
    Function.Injective (archivedVerificationLine P) := by
  intro l l' h
  exact congrArg Prod.snd h

/-- Strong necessity theorem: because verified outcome tables are equal, any auxiliary memory
that makes the joint `(outcome,memory)` representation faithful must itself distinguish every
registered line.  Provenance cannot be reconstructed from the detector outcome afterward. -/
theorem provenance_memory_injective_of_joint_injective {P : VerificationProtocol}
    (V : VerificationContract P) {Memory : Type} (memory : P.Line → Memory)
    (hjoint : Function.Injective
      (fun l => (verificationLineOutcome P l, memory l))) :
    Function.Injective memory := by
  intro l l' hmemory
  apply hjoint
  apply Prod.ext
  · exact verificationLineOutcome_eq V l l'
  · exact hmemory

/-- Finite capacity consequence: a faithful provenance archive has at least as many states as
there are registered independent verification lines. -/
theorem provenance_memory_card_lower_bound {P : VerificationProtocol}
    (V : VerificationContract P) {Memory : Type}
    [Fintype P.Line] [Fintype Memory]
    (memory : P.Line → Memory)
    (hjoint : Function.Injective
      (fun l => (verificationLineOutcome P l, memory l))) :
    Fintype.card P.Line ≤ Fintype.card Memory :=
  Fintype.card_le_of_injective memory
    (provenance_memory_injective_of_joint_injective V memory hjoint)

/-- A one-value provenance archive cannot preserve independent line identity. -/
theorem unit_provenance_memory_insufficient {P : VerificationProtocol}
    (V : VerificationContract P) :
    ¬ Function.Injective
      (fun l => (verificationLineOutcome P l, (Unit.unit : Unit))) := by
  intro hjoint
  have hmemory := provenance_memory_injective_of_joint_injective V
    (fun _ : P.Line => (Unit.unit : Unit)) hjoint
  obtain ⟨l, l', hne⟩ := V.line_nontrivial.exists_pair_ne
  exact hne (hmemory rfl)

/-- Detector/archive stratification capstone: the result layer necessarily collapses line
identity, while the paired provenance archive retains it faithfully and is capacity bounded. -/
theorem independent_verification_forces_provenance_archive {P : VerificationProtocol}
    (V : VerificationContract P) :
    ¬ Function.Injective (verificationLineOutcome P)
      ∧ Function.Injective (archivedVerificationLine P)
      ∧ ¬ Function.Injective
          (fun l => (verificationLineOutcome P l, (Unit.unit : Unit))) :=
  ⟨verified_lines_collapse_in_outcome_layer V,
    archivedVerificationLine_injective P,
    unit_provenance_memory_insufficient V⟩

/-- The full functional tuple is derived from one verification contract. -/
theorem protocol_verifiability_forces_functional_tuple {P : VerificationProtocol}
    (V : VerificationContract P) : FunctionalTuple P where
  distinction := V.state_nontrivial.exists_pair_ne
  retention := record_injective V
  comparison := by
    intro l c x y
    rw [V.correct]
    simp
  repeated_line := V.line_nontrivial.exists_pair_ne
  catalogue_invariant := by
    intro l c c' x y
    exact congrFun (congrFun (m1_as_verifiability_necessity V l c c') x) y

/-- A faithful verified record identifies exactly the original state. -/
def VerificationRecordRelation (P : VerificationProtocol) (x y : P.State) : Prop :=
  P.record x = P.record y

theorem verificationRecordRelation_iff_eq {P : VerificationProtocol}
    (V : VerificationContract P) (x y : P.State) :
    VerificationRecordRelation P x y ↔ x = y := by
  constructor
  · intro h
    apply record_injective V
    exact h
  · intro h
    exact congrArg P.record h

/-- T25 strengthened on a verified carrier: the equivalence closure of the record relation does
not manufacture extra identifications; record connectivity is exactly verified state identity. -/
theorem verificationRecordConnectivity_iff_eq {P : VerificationProtocol}
    (V : VerificationContract P) (x y : P.State) :
    SameComponent (VerificationRecordRelation P) x y ↔ x = y := by
  constructor
  · intro h
    induction h with
    | rel a b hab => exact (verificationRecordRelation_iff_eq V a b).mp hab
    | refl => rfl
    | symm _ _ _ ih => exact ih.symm
    | trans _ _ _ _ _ ih₁ ih₂ => exact ih₁.trans ih₂
  · intro h
    subst y
    exact @Relation.EqvGen.refl _ (VerificationRecordRelation P) x

/-- A verification protocol viewed as an empirical theory.  A test chooses a registered line and
a reference state; the outcome compares the tested state's record with that reference record. -/
def operationalEmpiricalTheory (P : VerificationProtocol) : EmpiricalTheory where
  State := P.State
  Test := P.Line × P.State
  Catalogue := P.Catalogue
  Outcome := Bool
  observe s c e := P.compare e.1 c (P.record s) (P.record e.2)

/-- Complete verification separates raw states at the level of full experimental signatures. -/
theorem operational_signature_injective {P : VerificationProtocol}
    (V : VerificationContract P) :
    Function.Injective (signature (operationalEmpiricalTheory P)) := by
  intro x y hsig
  by_contra hxy
  obtain ⟨l, _, _⟩ := V.line_nontrivial.exists_pair_ne
  obtain ⟨c⟩ := V.catalogue_nonempty
  have hs := congrFun (congrFun hsig c) (l, x)
  change P.compare l c (P.record x) (P.record x) =
    P.compare l c (P.record y) (P.record x) at hs
  have hx : P.compare l c (P.record x) (P.record x) = false := by
    simpa using V.correct l c x x
  have hy : P.compare l c (P.record y) (P.record x) = true := by
    rw [V.correct]
    exact decide_eq_true (Ne.symm hxy)
  cases hx.symm.trans (hs.trans hy)

/-- On a verified protocol the canonical empirical quotient loses no verified distinction. -/
noncomputable def operationalEmpiricalQuotientEquivState {P : VerificationProtocol}
    (V : VerificationContract P) :
    EmpiricalState (operationalEmpiricalTheory P) ≃ P.State :=
  minimalPresentationEquiv (operationalEmpiricalTheory P) id
    (fun s t h => operational_signature_injective V h)
    (fun _ _ h => by cases h; rfl)
    Function.surjective_id

/-- An arbitrary empirical theory is operationally verified when a correct protocol represents
its canonical empirical quotient.  This is the exact interface external physical formalisms fill. -/
structure TheoryVerification (T : EmpiricalTheory) where
  protocol : VerificationProtocol
  contract : VerificationContract protocol
  represents : protocol.State ≃ EmpiricalState T

/-- Scientific/verifiable theory: it has an operational verification representation. -/
def OperationallyVerifiable (T : EmpiricalTheory) : Prop := Nonempty (TheoryVerification T)

/-- Unverifiable story: no operational verification representation exists. -/
def UnverifiableStory (T : EmpiricalTheory) : Prop := ¬ OperationallyVerifiable T

/-- The verification/fantasy boundary is exhaustive and exclusive at the stated interface. -/
theorem operationally_verifiable_or_unverifiable_story (T : EmpiricalTheory) :
    OperationallyVerifiable T ∨ UnverifiableStory T :=
  Classical.em _

theorem operationally_verifiable_not_story {T : EmpiricalTheory}
    (h : OperationallyVerifiable T) : ¬ UnverifiableStory T := by
  exact fun hn => hn h

/-- Every correct protocol supplies a non-vacuous theory-level verification witness for its own
operational empirical theory. -/
noncomputable def protocolTheoryVerification {P : VerificationProtocol}
    (V : VerificationContract P) : TheoryVerification (operationalEmpiricalTheory P) where
  protocol := P
  contract := V
  represents := (operationalEmpiricalQuotientEquivState V).symm

/-- The theorem requested at theory level: every operationally verified empirical theory carries
the same forced functional tuple, independently of its domain-specific vocabulary. -/
theorem verifiability_forces_functional_tuple {T : EmpiricalTheory}
    (E : TheoryVerification T) : FunctionalTuple E.protocol :=
  protocol_verifiability_forces_functional_tuple E.contract

/-- T50--T52 generalized: every verification line embeds in a class-M1 admissible carrier. -/
def verifiableLineEmbedding {P : VerificationProtocol} (V : VerificationContract P) :
    P.Line ↪ M1AdmissibleCarrier (verificationCatalogueSystem P) where
  toFun l := ⟨l, m1_as_verifiability_necessity V l⟩
  inj' := by
    intro l l' h
    exact congrArg Subtype.val h

/-- A verified representation followed by the universal empirical embedding. -/
noncomputable def verifiedTheorySignatureEmbedding {T : EmpiricalTheory}
    (E : TheoryVerification T) :
    E.protocol.State ↪ (T.Catalogue → T.Test → T.Outcome) :=
  E.represents.toEmbedding.trans (empiricalEmbedding T)

/-- Outcome-affecting dependence on a privileged external catalogue. -/
def CatalogueOutsourced (P : VerificationProtocol) : Prop :=
  ∃ l c c' x y,
    P.compare l c (P.record x) (P.record y) ≠
      P.compare l c' (P.record x) (P.record y)

/-- Class-M1 admissibility is exactly the absence of an outcome-affecting privileged catalogue. -/
theorem all_lines_M1_iff_not_catalogue_outsourced (P : VerificationProtocol) :
    (∀ l, M1ClassAdmissible (verificationCatalogueSystem P) l) ↔
      ¬ CatalogueOutsourced P := by
  constructor
  · intro h ⟨l, c, c', x, y, hne⟩
    exact hne (congrFun (congrFun (h l c c') x) y)
  · intro hno l c c'
    funext x y
    by_contra hne
    exact hno ⟨l, c, c', x, y, hne⟩

/-- Regress closure: M1 and the tuple are consequences of the verification contract, so applying
them here introduces no second catalogue-removal axiom. -/
theorem m1_regress_closure_via_verifiability {T : EmpiricalTheory}
    (E : TheoryVerification T) :
    FunctionalTuple E.protocol
      ∧ (∀ l, M1ClassAdmissible
          (verificationCatalogueSystem E.protocol) l)
      ∧ ¬ CatalogueOutsourced E.protocol := by
  refine ⟨verifiability_forces_functional_tuple E, ?_, ?_⟩
  · exact m1_as_verifiability_necessity E.contract
  · exact (all_lines_M1_iff_not_catalogue_outsourced E.protocol).mp
      (m1_as_verifiability_necessity E.contract)

/-! ## Operational MDL on functions rather than names -/

/-- A vocabulary covers a role when one active name denotes that semantic function. -/
def CoversRole {Name : Type} [DecidableEq Name]
    (meaning : Name → FunctionalRole) (active : Finset Name)
    (role : FunctionalRole) : Prop :=
  ∃ name ∈ active, meaning name = role

def FunctionallyComplete {Name : Type} [DecidableEq Name]
    (meaning : Name → FunctionalRole) (active : Finset Name) : Prop :=
  ∀ role, CoversRole meaning active role

/-- MDL counts the semantic image.  Synonyms do not create new functions. -/
def SemanticImage {Name : Type} [DecidableEq Name]
    (meaning : Name → FunctionalRole) (active : Finset Name) : Finset FunctionalRole :=
  active.image meaning

def SemanticCost {Name : Type} [DecidableEq Name]
    (meaning : Name → FunctionalRole) (active : Finset Name) : Nat :=
  (SemanticImage meaning active).card

/-- A raw vocabulary is minimal when every active name is load-bearing for functional coverage. -/
def NameMinimal {Name : Type} [DecidableEq Name]
    (meaning : Name → FunctionalRole) (active : Finset Name) : Prop :=
  FunctionallyComplete meaning active ∧
    ∀ name ∈ active, ¬ FunctionallyComplete meaning (active.erase name)

theorem semanticImage_eq_univ_of_complete {Name : Type} [DecidableEq Name]
    {meaning : Name → FunctionalRole} {active : Finset Name}
    (h : FunctionallyComplete meaning active) :
    SemanticImage meaning active = Finset.univ := by
  apply Finset.eq_univ_of_forall
  intro role
  obtain ⟨name, hname, hmeaning⟩ := h role
  exact Finset.mem_image.mpr ⟨name, hname, hmeaning⟩

/-- Every complete language has exactly three semantic roles; the count is computed from the
inductive role carrier, not supplied as a premise. -/
theorem semanticCost_eq_three_of_complete {Name : Type} [DecidableEq Name]
    {meaning : Name → FunctionalRole} {active : Finset Name}
    (h : FunctionallyComplete meaning active) :
    SemanticCost meaning active = 3 := by
  rw [SemanticCost, semanticImage_eq_univ_of_complete h]
  decide

theorem canonicalRoles_complete :
    FunctionallyComplete (fun r : FunctionalRole => r) Finset.univ := by
  intro role
  exact ⟨role, Finset.mem_univ _, rfl⟩

theorem canonicalRoles_nameMinimal :
    NameMinimal (fun r : FunctionalRole => r) Finset.univ := by
  refine ⟨canonicalRoles_complete, ?_⟩
  intro role _ hcomplete
  obtain ⟨name, hname, hmeaning⟩ := hcomplete role
  have hne : name ≠ role := (Finset.mem_erase.mp hname).1
  exact hne hmeaning

/-- Any bijective renaming carries exactly the canonical semantic image. -/
theorem same_functions_different_language_equivalent
    {Name : Type} [Fintype Name] [DecidableEq Name]
    (rename : Name ≃ FunctionalRole) :
    SemanticImage (fun n => rename n) Finset.univ =
      SemanticImage (fun r : FunctionalRole => r) Finset.univ := by
  rw [semanticImage_eq_univ_of_complete canonicalRoles_complete]
  apply semanticImage_eq_univ_of_complete
  intro role
  exact ⟨rename.symm role, Finset.mem_univ _, rename.apply_symm_apply role⟩

/-- Four names with the last two denoting the same comparison function. -/
def redundantMeaning (name : Fin 4) : FunctionalRole :=
  if name = 0 then FunctionalRole.distinction
  else if name = 1 then FunctionalRole.retention
  else FunctionalRole.comparison

theorem redundantRoles_complete :
    FunctionallyComplete redundantMeaning (Finset.univ : Finset (Fin 4)) := by
  intro role
  cases role with
  | distinction => exact ⟨0, by simp, by simp [redundantMeaning]⟩
  | retention => exact ⟨1, by simp, by simp [redundantMeaning]⟩
  | comparison => exact ⟨2, by simp, by simp [redundantMeaning]⟩

/-- The duplicate fourth name is removable without losing any function. -/
theorem redundantRole_removed_still_complete :
    FunctionallyComplete redundantMeaning
      ((Finset.univ : Finset (Fin 4)).erase 3) := by
  intro role
  cases role with
  | distinction => exact ⟨0, by decide, by simp [redundantMeaning]⟩
  | retention => exact ⟨1, by decide, by simp [redundantMeaning]⟩
  | comparison => exact ⟨2, by decide, by simp [redundantMeaning]⟩

theorem redundantRoles_not_nameMinimal :
    ¬ NameMinimal redundantMeaning (Finset.univ : Finset (Fin 4)) := by
  intro h
  exact h.2 3 (by simp) redundantRole_removed_still_complete

/-- Operational MDL capstone: all complete languages have cost three, canonical roles are
deletion-minimal, and a duplicated fourth name is rejected by an explicit deletion control. -/
theorem operational_mdl_role_minimality :
    NameMinimal (fun r : FunctionalRole => r) Finset.univ
      ∧ (∀ {Name : Type} [DecidableEq Name]
          (meaning : Name → FunctionalRole) (active : Finset Name),
          FunctionallyComplete meaning active → SemanticCost meaning active = 3)
      ∧ FunctionallyComplete redundantMeaning (Finset.univ : Finset (Fin 4))
      ∧ ¬ NameMinimal redundantMeaning (Finset.univ : Finset (Fin 4))
      ∧ FunctionallyComplete redundantMeaning
          ((Finset.univ : Finset (Fin 4)).erase 3) :=
  ⟨canonicalRoles_nameMinimal,
    fun meaning active h =>
      semanticCost_eq_three_of_complete (meaning := meaning) (active := active) h,
    redundantRoles_complete,
    redundantRoles_not_nameMinimal,
    redundantRole_removed_still_complete⟩

/-! ## Non-vacuity and negative controls -/

def canonicalProtocol : VerificationProtocol where
  State := Bool
  Record := Bool
  Line := Bool
  Catalogue := PUnit
  stateDecidableEq := inferInstance
  record := id
  compare := fun _ _ x y => decide (x ≠ y)

theorem canonicalProtocol_verifiable : VerificationContract canonicalProtocol := by
  refine ⟨⟨⟨false, true, by intro h; cases h⟩⟩,
    ⟨⟨false, true, by intro h; cases h⟩⟩, ⟨PUnit.unit⟩, ?_⟩
  intro l c x y
  rfl

/-- Removing distinction: a singleton state carrier cannot meet the verification contract. -/
def noDistinctionProtocol : VerificationProtocol where
  State := PUnit
  Record := PUnit
  Line := Bool
  Catalogue := PUnit
  stateDecidableEq := inferInstance
  record := id
  compare := fun _ _ _ _ => false

theorem removing_distinction_breaks_verification :
    ¬ VerificationContract noDistinctionProtocol := by
  intro V
  obtain ⟨x, y, hxy⟩ := V.state_nontrivial.exists_pair_ne
  cases x
  cases y
  exact hxy rfl

/-- Removing retention: both Boolean states collapse to one record. -/
def noRetentionProtocol : VerificationProtocol where
  State := Bool
  Record := PUnit
  Line := Bool
  Catalogue := PUnit
  stateDecidableEq := inferInstance
  record := fun _ => PUnit.unit
  compare := fun _ _ _ _ => false

theorem removing_retention_breaks_verification :
    ¬ VerificationContract noRetentionProtocol := by
  intro V
  have hinj := record_injective V
  have h := hinj (show noRetentionProtocol.record false =
    noRetentionProtocol.record true from rfl)
  cases h

/-- Removing comparison: a constant comparator cannot separate `false` from `true`. -/
def noComparisonProtocol : VerificationProtocol where
  State := Bool
  Record := Bool
  Line := Bool
  Catalogue := PUnit
  stateDecidableEq := inferInstance
  record := id
  compare := fun _ _ _ _ => false

theorem removing_comparison_breaks_verification :
    ¬ VerificationContract noComparisonProtocol := by
  intro V
  have hfalse : noComparisonProtocol.compare false PUnit.unit
      (noComparisonProtocol.record false)
      (noComparisonProtocol.record true) = false := rfl
  have htrue : noComparisonProtocol.compare false PUnit.unit
      (noComparisonProtocol.record false)
      (noComparisonProtocol.record true) = true := by
    have h := V.correct false PUnit.unit false true
    change noComparisonProtocol.compare false PUnit.unit
        (noComparisonProtocol.record false)
        (noComparisonProtocol.record true) =
      decide ((false : Bool) ≠ true) at h
    exact h.trans (by decide)
  cases hfalse.symm.trans htrue

/-- Removing the second registered line destroys independent repetition. -/
def oneLineProtocol : VerificationProtocol where
  State := Bool
  Record := Bool
  Line := PUnit
  Catalogue := PUnit
  stateDecidableEq := inferInstance
  record := id
  compare := fun _ _ x y => decide (x ≠ y)

theorem removing_second_line_breaks_verification :
    ¬ VerificationContract oneLineProtocol := by
  intro V
  obtain ⟨x, y, hxy⟩ := V.line_nontrivial.exists_pair_ne
  cases x
  cases y
  exact hxy rfl

/-- A comparator that succeeds only when a privileged catalogue bit is `true`. -/
def privilegedCatalogueProtocol : VerificationProtocol where
  State := Bool
  Record := Bool
  Line := Bool
  Catalogue := Bool
  stateDecidableEq := inferInstance
  record := id
  compare := fun _ catalogue x y => if catalogue then decide (x ≠ y) else false

theorem privileged_catalogue_can_distinguish :
    privilegedCatalogueProtocol.compare false true
      (privilegedCatalogueProtocol.record false)
      (privilegedCatalogueProtocol.record true) = true := by
  decide

theorem privileged_catalogue_is_outcome_affecting :
    CatalogueOutsourced privilegedCatalogueProtocol := by
  refine ⟨false, false, true, false, true, ?_⟩
  decide

theorem privileged_catalogue_not_M1 (l : privilegedCatalogueProtocol.Line) :
    ¬ M1ClassAdmissible
      (verificationCatalogueSystem privilegedCatalogueProtocol) l := by
  intro h
  have hx := congrFun (congrFun (h false true) false) true
  change privilegedCatalogueProtocol.compare l false
      (privilegedCatalogueProtocol.record false)
      (privilegedCatalogueProtocol.record true) =
    privilegedCatalogueProtocol.compare l true
      (privilegedCatalogueProtocol.record false)
      (privilegedCatalogueProtocol.record true) at hx
  have hfalse : privilegedCatalogueProtocol.compare l false
      (privilegedCatalogueProtocol.record false)
      (privilegedCatalogueProtocol.record true) = false := rfl
  have htrue : privilegedCatalogueProtocol.compare l true
      (privilegedCatalogueProtocol.record false)
      (privilegedCatalogueProtocol.record true) = true := by
    rfl
  cases hfalse.symm.trans (hx.trans htrue)

theorem necessary_role_outsourced_loses_verifiability :
    ¬ VerificationContract privilegedCatalogueProtocol := by
  intro V
  exact (all_lines_M1_iff_not_catalogue_outsourced privilegedCatalogueProtocol).mp
    (m1_as_verifiability_necessity V) privileged_catalogue_is_outcome_affecting

/-- One capstone exposes both the positive construction and all load-bearing mutations. -/
theorem verifiability_necessity_controls :
    VerificationContract canonicalProtocol
      ∧ ¬ VerificationContract noDistinctionProtocol
      ∧ ¬ VerificationContract noRetentionProtocol
      ∧ ¬ VerificationContract noComparisonProtocol
      ∧ ¬ VerificationContract oneLineProtocol
      ∧ CatalogueOutsourced privilegedCatalogueProtocol
      ∧ ¬ VerificationContract privilegedCatalogueProtocol :=
  ⟨canonicalProtocol_verifiable,
    removing_distinction_breaks_verification,
    removing_retention_breaks_verification,
    removing_comparison_breaks_verification,
    removing_second_line_breaks_verification,
    privileged_catalogue_is_outcome_affecting,
    necessary_role_outsourced_loses_verifiability⟩

end D0.Foundation.VerifiabilityNecessity
