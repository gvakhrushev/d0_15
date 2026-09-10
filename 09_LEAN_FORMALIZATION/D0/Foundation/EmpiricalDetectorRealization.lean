import D0.Foundation.EmpiricalTheoryFactorization
import D0.Synthesis.ConcretePhysicalDetectorRepresentation

/-!
# Exact addressed detector representation and a closed scope boundary

A finite outcome profile is losslessly stored as addressed equality bits and read by the
actual D0 value comparison. This realizes a retained table, not a physical preparation
algorithm for an arbitrary abstract theory. Against the unrestricted EmpiricalTheory
interface, no countably coded family of total evaluators can realize every profile.
-/
namespace D0.Foundation.EmpiricalDetectorRealization

open D0.Foundation.EmpiricalTheoryFactorization
open D0.Foundation.DetectionCapabilityBoundary

def profileBits {E O : Type} [DecidableEq O] (f : E → O) : E × O → Bool :=
  fun address => decide (f address.1 = address.2)

theorem profileBits_injective {E O : Type} [DecidableEq O] :
    Function.Injective (@profileBits E O _) := by
  intro f g h
  funext e
  have he := congrFun h (e, f e)
  have hg : g e = f e := by simpa [profileBits] using he.symm
  exact hg.symm

/-- The stored value bit and its history are explicitly internal observation coordinates. -/
def storedObservation (bit history : Bool) : Observation := ⟨true, bit, history⟩

theorem existing_detector_reads_bit (bit h k : Bool) :
    valueComparison (storedObservation bit h) (storedObservation true k) = bit := by
  cases bit <;> rfl

/-- Exact decoding by the existing comparison, for arbitrary retained histories. -/
theorem addressed_readout_correct {E O : Type} [DecidableEq O]
    (f : E → O) (e : E) (o : O) (h k : Bool) :
    valueComparison (storedObservation (profileBits f (e,o)) h)
      (storedObservation true k) = decide (f e = o) :=
  existing_detector_reads_bit _ h k

theorem existing_detector_family_faithful {E O : Type} [DecidableEq O]
    (f g : E → O)
    (h : ∀ e o,
      valueComparison (storedObservation (profileBits f (e,o)) false)
        (storedObservation true false) =
      valueComparison (storedObservation (profileBits g (e,o)) false)
        (storedObservation true false)) : f = g := by
  apply profileBits_injective
  funext address
  simpa only [existing_detector_reads_bit] using h address.1 address.2

/-- Every finite profile uses a finite, explicitly counted address carrier. -/
theorem address_count {E O : Type} [Fintype E] [Fintype O] :
    Fintype.card (E × O) = Fintype.card E * Fintype.card O :=
  Fintype.card_prod _ _

/-- Protocol pullback compiles to address pullback; no replacement by marginal ranks occurs. -/
theorem profileBits_pullback {E O : Type} [DecidableEq O]
    (f : E → O) (pull : E → E) :
    profileBits (f ∘ pull) = fun eo => profileBits f (pull eo.1, eo.2) := rfl

/-- The generic empirical quotient now embeds in an addressed family of stored D0 value bits.
Finiteness of catalogue, tests and outcomes makes the whole table finite. -/
def addressedEmpiricalEmbedding (T : EmpiricalTheory) [DecidableEq T.Outcome] :
    EmpiricalState T ↪ ((T.Catalogue × T.Test) × T.Outcome → Bool) where
  toFun q := profileBits (fun ce => evaluate T q ce.1 ce.2)
  inj' := by
    intro q r h
    apply evaluate_injective T
    have he := profileBits_injective h
    funext c e
    exact congrFun he (c,e)

/-- A retained table can be copied into a blank output register without deleting its source.
This is a basis-register permutation, not cloning an arbitrary superposition. -/
def readInto {Address : Type} (table : Address → Bool) (address : Address)
    (output : Bool) : Bool := Bool.xor output (table address)

theorem readInto_involutive {Address : Type} (table : Address → Bool) (address : Address) :
    Function.Involutive (readInto table address) := by
  intro output
  cases output <;> cases h : table address <;> simp [readInto, h]

theorem readInto_blank {Address : Type} (table : Address → Bool) (address : Address) :
    readInto table address false = table address := by
  cases h : table address <;> simp [readInto, h]

/-! ## The unrestricted interface is too broad for a finitely coded completeness theorem -/

def arbitraryProfileTheory : EmpiricalTheory where
  State := ℕ → Bool
  Test := ℕ
  Catalogue := Unit
  Outcome := Bool
  observe f _ n := f n

/-- Every profile in this abstract interface is catalogue-independent. This does not make an
arbitrary infinite profile physically preparable. -/
theorem arbitrary_profile_admissible (f : ℕ → Bool) :
    D0.Foundation.M1ClassAdmissibility.M1ClassAdmissible
      (rawCatalogueSystem arbitraryProfileTheory) f := by
  intro c d
  rfl

/-- Diagonal obstruction for any countably coded total evaluator, irrespective of its gates.
It closes the unrestricted claim; it does not exclude a constructive physical subclass. -/
theorem no_countably_coded_universal_realization (run : ℕ → ℕ → Bool) :
    ∃ profile : ℕ → Bool, ∀ code : ℕ, ∃ test : ℕ,
      run code test ≠ profile test := by
  refine ⟨fun n => !(run n n), fun code => ⟨code, ?_⟩⟩
  change run code code ≠ !(run code code)
  cases run code code <;> decide

/-- Catalogue independence alone cannot discharge the physical-realization obligation. -/
theorem catalogue_independence_not_realization (run : ℕ → ℕ → Bool) :
    ∃ profile : arbitraryProfileTheory.State,
      D0.Foundation.M1ClassAdmissibility.M1ClassAdmissible
        (rawCatalogueSystem arbitraryProfileTheory) profile ∧
      ∀ code : ℕ, ∃ test : ℕ, run code test ≠ profile test := by
  obtain ⟨profile, h⟩ := no_countably_coded_universal_realization run
  exact ⟨profile, arbitrary_profile_admissible profile, h⟩

end D0.Foundation.EmpiricalDetectorRealization
