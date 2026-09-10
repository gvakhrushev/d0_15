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

end D0.Foundation.EmpiricalTheoryFactorization
