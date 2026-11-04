import D0.Foundation.TheoryTransfer

/-!
# Full profile equivalence need not supply single-context coverage

Book02 §02.3b, bytes `[14760,15284)` of commit
`a4d0d3919e9c2b8e9f27aeaacaafd6dcf06e6c38`, blob
`00d7c597abb99856719b274bb86b115b17af139f`, says that full-native
equivalence "requires" `NativeContextCoverage`. If read as a claim that
coverage is logically necessary, this finite example refutes that reading.
It does not refute the existing conditional transfer theorem: a supplied
coverage witness remains sufficient for full profile equivalence.

Both systems retain both state bits through identity actions. The source can
query either bit; the native system can also query their XOR. The source and
native complete profiles determine exactly the same states, but no ONE source
query followed by a Boolean postprocessor computes XOR on all four states.
The example is abstract; it proves no physical test, admission, or GR claim.
-/

namespace D0.Foundation.NativeCoverageSufficiencyCounterexample

open D0.Foundation.EmpiricalTheoryFactorization
open D0.Foundation.TheoryTransfer

/-- The source can inspect either of the two state bits. -/
def source : FutureExecution where
  State := Bool × Bool
  Action := Unit
  Test := Bool
  Outcome := Bool
  step := fun _ s => s
  observe := fun s t => if t then s.2 else s.1

/-- The native carrier exposes both source tests and an extra XOR test. -/
def native : FutureExecution where
  State := Bool × Bool
  Action := Unit
  Test := Fin 3
  Outcome := Bool
  step := fun _ s => s
  observe := fun s t => if t = 0 then s.1 else if t = 1 then s.2 else xor s.1 s.2

/-- The common source tests are interpreted as the first two native tests. -/
def interpretation : Interpretation source native where
  stateMap := id
  actionWord := fun _ => [()]
  testMap := fun (t : Bool) => if t then (1 : Fin 3) else (0 : Fin 3)
  outcomeMap := id
  outcome_injective := Function.injective_id
  step_commutes := fun _ _ => rfl
  observe_commutes := by
    intro s t
    cases t <;> rfl

theorem source_run (w : List Unit) (s : Bool × Bool) : source.run w s = s := by
  induction w with
  | nil => rfl
  | cons a w ih => exact ih

/-- The two native profiles agree exactly when the two source profiles agree. -/
theorem native_profile_eq_iff_source (s t : source.State) :
    native.profile (interpretation.stateMap s) = native.profile (interpretation.stateMap t) ↔
      source.profile s = source.profile t := by
  constructor
  · exact interpretation.native_profile_reflects
  · intro h
    have h₁ := congrFun (congrFun h []) false
    have h₂ := congrFun (congrFun h []) true
    rcases s with ⟨a,b⟩
    rcases t with ⟨c,d⟩
    change a = c at h₁
    change b = d at h₂
    cases h₁
    cases h₂
    rfl

/-- The added native test has the exact Boolean XOR truth table. -/
theorem native_xor_truth_table :
    native.observe (false, false) (2 : Fin 3) = false ∧
    native.observe (false, true) (2 : Fin 3) = true ∧
    native.observe (true, false) (2 : Fin 3) = true ∧
    native.observe (true, true) (2 : Fin 3) = false := by
  exact ⟨rfl, rfl, rfl, rfl⟩

/-- XOR is not a postprocessing of either single source bit on all states. -/
theorem xor_not_single_source_test :
    ∀ (test : Bool) (post : Bool → Bool),
      ∃ s : Bool × Bool, post (source.observe s test) ≠ native.observe s (2 : Fin 3) := by
  decide

/-- Despite full equivalence, no `NativeContextCoverage` witness exists. -/
theorem no_single_context_coverage : ¬ Nonempty (NativeContextCoverage interpretation) := by
  rintro ⟨cov⟩
  obtain ⟨s, hs⟩ := xor_not_single_source_test (cov.context [] (2 : Fin 3)).2 (cov.readout [] (2 : Fin 3))
  have hc := cov.correct s [] (2 : Fin 3)
  change native.observe s (2 : Fin 3) =
    cov.readout [] (2 : Fin 3) (source.observe (source.run (cov.context [] (2 : Fin 3)).1 s) (cov.context [] (2 : Fin 3)).2) at hc
  rw [source_run] at hc
  exact hs hc.symm

/-- The concrete example combines both conclusions without invoking physical
interpretation or changing the scope of the existing sufficiency theorem. -/
theorem full_equivalence_without_coverage :
    (∀ s t, native.profile (interpretation.stateMap s) = native.profile (interpretation.stateMap t) ↔
      source.profile s = source.profile t) ∧
      ¬ Nonempty (NativeContextCoverage interpretation) :=
  ⟨native_profile_eq_iff_source, no_single_context_coverage⟩

end D0.Foundation.NativeCoverageSufficiencyCounterexample
