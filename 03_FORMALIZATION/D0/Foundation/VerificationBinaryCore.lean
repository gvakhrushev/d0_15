import D0.Foundation.PopperianBootstrap

/-! Native #334 extension extracted without changing the accepted base owner.
Original declarations: `03_FORMALIZATION/D0/Foundation/PopperianBootstrap.lean` at
`07f2f2b15b7050a612d0075aa73db8dc46087a95`.
The shared definitions are imported from their maintained main modules. -/

namespace D0.Foundation.PopperianBootstrap

open D0.Foundation.VerifiabilityNecessity

/-- The two-line reduction uses ONLY existing original lines and actual
record values; there are no synthetic new verification witnesses. -/
def twoLineImageProtocol (P : VerificationProtocol) (l₀ l₁ : P.Line) :
    VerificationProtocol where
  State := P.State
  Record := { r : P.Record // ∃ x : P.State, P.record x = r }
  Line := Bool
  Catalogue := P.Catalogue
  stateDecidableEq := P.stateDecidableEq
  record := fun x => ⟨P.record x, ⟨x, rfl⟩⟩
  compare := fun b c r s =>
    P.compare (if b then l₁ else l₀) c r.1 s.1

/-- Chosen original source lines remain genuinely distinct after reduction. -/
theorem twoLineImageProtocol_selected_lines_injective {P : VerificationProtocol}
    {l₀ l₁ : P.Line} (h : l₀ ≠ l₁) :
    Function.Injective (fun b : Bool => if b then l₁ else l₀) := by
  intro b b' he
  cases b <;> cases b' <;> simp_all

/-- Binary core still has the WHOLE exact original falsification contract. -/
theorem twoLineImageProtocol_killingTest {P : VerificationProtocol}
    (K : KillingTest P) (l₀ l₁ : P.Line) (h : l₀ ≠ l₁) :
    KillingTest (twoLineImageProtocol P l₀ l₁) := by
  have hinj := twoLineImageProtocol_selected_lines_injective h
  have hselected :
      (if (false : Bool) then l₁ else l₀) ≠
      (if (true : Bool) then l₁ else l₀) := by
    intro he
    have heq : (false : Bool) = true := hinj he
    cases heq
  refine {
    prediction_violation := K.prediction_violation
    two_witnesses := by
      change ∃ b₀ b₁ : Bool, b₀ ≠ b₁
      exact ⟨false, true, by decide⟩
    runnable := K.runnable
    verdict := ?_ }
  intro b c x y
  change Bool at b
  exact K.verdict (if b then l₁ else l₀) c x y

/-- No unused record addresses survive: every image record is produced by
an actual original state, without adding an external record catalogue. -/
theorem twoLineImageProtocol_record_surjective (P : VerificationProtocol)
    (l₀ l₁ : P.Line) :
    Function.Surjective (twoLineImageProtocol P l₀ l₁).record := by
  intro r
  obtain ⟨x, hx⟩ := r.property
  refine ⟨x, ?_⟩
  apply Subtype.ext
  exact hx

/-- The original forced injective retention is preserved. -/
theorem twoLineImageProtocol_record_injective {P : VerificationProtocol}
    (K : KillingTest P) (l₀ l₁ : P.Line) :
    Function.Injective (twoLineImageProtocol P l₀ l₁).record := by
  intro x y h
  apply killingTest_record_injective K
  exact congrArg Subtype.val h

/-- The choice of an arbitrary original pair changes its provenance but
never the comparison verdict: two-line cores factor through the SAME
exact verified outcome, without any preferred external line catalogue. -/
theorem twoLineImageProtocol_pair_choice_independent {P : VerificationProtocol}
    (K : KillingTest P) (l₀ l₁ l₂ l₃ : P.Line)
    (b b' : Bool) (c : P.Catalogue) (x y : P.State) :
    (twoLineImageProtocol P l₀ l₁).compare b c
      ((twoLineImageProtocol P l₀ l₁).record x)
      ((twoLineImageProtocol P l₀ l₁).record y) =
    (twoLineImageProtocol P l₂ l₃).compare b' c
      ((twoLineImageProtocol P l₂ l₃).record x)
      ((twoLineImageProtocol P l₂ l₃).record y) := by
  change P.compare (if b then l₁ else l₀) c (P.record x) (P.record y) =
    P.compare (if b' then l₃ else l₂) c (P.record x) (P.record y)
  rw [K.verdict, K.verdict]

/-- Every EXTRA correct detector line adds no new verdict distinction,
as long as the required tests are EXACT and fault-free. -/
theorem extra_line_verdict_redundant {P : VerificationProtocol}
    (K : KillingTest P) (l l₀ l₁ : P.Line)
    (b : Bool) (c : P.Catalogue) (x y : P.State) :
    P.compare l c (P.record x) (P.record y) =
    (twoLineImageProtocol P l₀ l₁).compare b c
      ((twoLineImageProtocol P l₀ l₁).record x)
      ((twoLineImageProtocol P l₀ l₁).record y) := by
  change P.compare l c (P.record x) (P.record y) =
    P.compare (if b then l₁ else l₀) c (P.record x) (P.record y)
  rw [K.verdict, K.verdict]

/-- A single existing line, no matter how many raw record symbols,
cannot fulfil the formal independent-witness requirement. -/
def oneLineProjection (P : VerificationProtocol) (l : P.Line) :
    VerificationProtocol where
  State := P.State
  Record := P.Record
  Line := Unit
  Catalogue := P.Catalogue
  stateDecidableEq := P.stateDecidableEq
  record := P.record
  compare := fun _ c r s => P.compare l c r s

theorem oneLineProjection_not_killingTest (P : VerificationProtocol)
    (l : P.Line) : ¬ KillingTest (oneLineProjection P l) := by
  letI : Subsingleton (oneLineProjection P l).Line := by
    change Subsingleton Unit
    infer_instance
  exact no_killingTest_single_line (oneLineProjection P l)

/-- The existing hostile 3-line protocol contracts to a 2-line core;
it refutes carrier uniqueness, NOT the two-line generating minimum. -/
theorem fin3Protocol_binary_core_killingTest :
    KillingTest (twoLineImageProtocol fin3Protocol (0 : Fin 3) (1 : Fin 3)) :=
  twoLineImageProtocol_killingTest fin3Protocol_killingTest (0 : Fin 3) (1 : Fin 3)
    fin3_zero_ne_one

/-- Exact generator: some pair of EXISTING independent line labels suffices;
zero or one source line does not. No fault-tolerance, absolute MDL work or
physical independence of these labels is inferred from a mere type inequality. -/
theorem killingTest_has_minimal_binary_generator {P : VerificationProtocol}
    (K : KillingTest P) :
    (∃ l₀ l₁ : P.Line, l₀ ≠ l₁ ∧
       KillingTest (twoLineImageProtocol P l₀ l₁)) ∧
    (∀ l : P.Line, ¬ KillingTest (oneLineProjection P l)) := by
  constructor
  · obtain ⟨l₀, l₁, h⟩ := K.two_witnesses
    exact ⟨l₀, l₁, h, twoLineImageProtocol_killingTest K l₀ l₁ h⟩
  · exact fun l => oneLineProjection_not_killingTest P l


/-! ## Cross-level bridge: two-line core over ANY SHARED future operation

This is the exact point where the MDL argument meets the endorsed future
contextual quotient.  A third correct verification line may be removed
as a primitive witness while retaining the outcomes of ALL FUTURE words,
provided the actions are the same original admissible operations on
the recorded state regardless of which witness line is used.

This does NOT delete a third source of a novel, line-specific operation.
Such a deletion would change the future TEST family, rather than merely
compress an observationally equivalent representation. -/

/-- The pair of existing witnesses generates the same exact verdict even
after any future sequence of the SAME admitted state operations. -/
theorem binary_core_preserves_all_shared_action_histories
    {P : VerificationProtocol} (K : KillingTest P)
    {Action : Type} (step : Action → P.State → P.State)
    (word : List Action) (l l₀ l₁ : P.Line) (b : Bool)
    (c : P.Catalogue) (x y : P.State) :
    P.compare l c
      (P.record (word.foldl (fun s a => step a s) x))
      (P.record (word.foldl (fun s a => step a s) y)) =
    (twoLineImageProtocol P l₀ l₁).compare b c
      ((twoLineImageProtocol P l₀ l₁).record
        (word.foldl (fun s a => step a s) x))
      ((twoLineImageProtocol P l₀ l₁).record
        (word.foldl (fun s a => step a s) y)) := by
  exact extra_line_verdict_redundant K l l₀ l₁ b c
    (word.foldl (fun s a => step a s) x)
    (word.foldl (fun s a => step a s) y)

end D0.Foundation.PopperianBootstrap
