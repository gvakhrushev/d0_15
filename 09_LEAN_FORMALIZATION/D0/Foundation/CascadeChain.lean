import D0.Foundation.CascadeFloorComparison
import D0.Foundation.CascadeFloorOneLoop
import D0.Foundation.CascadeFloorOrderMemory
import D0.Foundation.CascadeFloorScaleRatio

/-!
# D0-CASCADE-CHAIN-SCAFFOLD-001 — the composition shape of the insufficiency cascade

`D0-CASCADE-INSUFFICIENCY-CHAIN-001` (BOOK_01 §01.6.1c) claims the corpus's structure is not
assembled but *unfolded*: each level exists because the one below it provably fails a named
distinguishability obligation. This module fixes the shape that claim has to take, so that floors
plug in rather than being re-argued, and so that the final composition is mechanical.

A step is genuine only when **both** halves hold:

* `insufficient` — the lower carrier fails the obligation. Alone this is not enough: an obligation
  that nothing satisfies forces nothing, because the repair would fail it too.
* `control` — the upper carrier satisfies it. This is what makes the obligation a real requirement
  rather than an unsatisfiable demand, and it is the spine-level form of the corpus's
  `check_cert_can_fail` rule.

From the pair it follows that the step is not a renaming: the obligation *discriminates* between the
two carriers, so the cascade genuinely moves. That is `step_discriminates` below, and it is the
property a chain of such steps accumulates.

Four floors are instantiated here, each machine-checked in its own module:

| step | obligation | fails on | repaired by |
|---|---|---|---|
| 2→3 | verifiability — the acceptor must be able to fail | a monopoly (constant) acceptor | the dyad: direct vs return |
| 4→5 | operation memory — the state must determine its history | one ℤ register | two registers |
| 5→6 | order memory — the record must distinguish `ab` from `ba` | `π₁(T²) = ℤ×ℤ` (abelian) | any non-commutative carrier (`S₃`, `Q₈`) |
| 6→7 | non-capture — no finite stage matches the scale ratio | any rational ratio | an irrational one; `φ` after the owned canonization |

Honest scope: this is the **scaffold plus the four floors that exist**, not the finished chain. The
remaining floors of §01.6.1c — defect⇒closure⇒shell, three insufficiencies⇒three zones — are open, and `D0-CASCADE-INSUFFICIENCY-CHAIN-001` stays `PROOF-TARGET` until they are carried in
this same shape. What this module removes is the excuse that the shape was unclear, and what
`chain_linked_four_five_to_five_six` adds is the reason the unfolding cannot stop at a repair.
-/

namespace D0.Foundation

/-- One step of the cascade. The obligation is recorded **at both carriers** — as the proposition it
actually becomes there — because that is what makes the step checkable: the same requirement must
come out false below and true above. Carrying it as an abstract predicate over types would force a
uniform structure class the floors do not share (one is a register model, the next a group). -/
structure CascadeStep where
  /-- what the step is called in the books -/
  name : String
  /-- the named obligation, instantiated at the floor that fails -/
  ObligationBelow : Prop
  /-- the same obligation, instantiated at the minimal repair -/
  ObligationAbove : Prop
  /-- the load-bearing lemma: the floor provably fails it -/
  insufficient : ¬ ObligationBelow
  /-- the non-vacuity control: the repair provably satisfies it -/
  control : ObligationAbove

/-- **A genuine step discriminates.** The obligation fails below and holds above, so it separates
the two levels — the step is a real change of structure, not a renaming. This is the content a chain
of such steps accumulates. -/
theorem step_discriminates (s : CascadeStep) : ¬ (s.ObligationBelow ↔ s.ObligationAbove) := by
  intro h
  exact s.insufficient (h.mpr s.control)

/-- **A genuine step is non-vacuous.** The obligation is satisfiable, so the failure below is an
obstruction and not an impossible demand — without this the step would force nothing. -/
theorem step_not_vacuous (s : CascadeStep) : ∃ p : Prop, p ∧ p = s.ObligationAbove :=
  ⟨s.ObligationAbove, s.control, rfl⟩

/-- **Floor 4→5**, instantiated with the real obligation: *the carrier's final state separates the
two histories*. False for one register (they collapse at every initial state), true for two. -/
def stepOneLoop : CascadeStep where
  name := "one loop cannot carry memory (4→5)"
  ObligationBelow := ∀ k : ℤ, runOne h₁ k ≠ runOne h₂ k
  ObligationAbove := runTwo h₁ (0, 0) ≠ runTwo h₂ (0, 0)
  insufficient := fun h => h 0 (one_loop_insufficient 0)
  control := two_loops_control

/-- **Floor 5→6**, instantiated with the real obligation: *order is encoded in the record*. False on
the abelian torus carrier, true on a non-commutative one. -/
def stepOrderMemory : CascadeStep where
  name := "the torus is abelian, so order is not encoded (5→6)"
  ObligationBelow := OrderEncoded (Multiplicative (ℤ × ℤ))
  ObligationAbove := OrderEncoded (Equiv.Perm (Fin 3))
  insufficient := torus_insufficient
  control := control_orderEncoded

/-- **Floor 2→3**, instantiated with the real obligation: *the acceptor can fail*. False for the
monopoly acceptor (constant, so it either admits everything or refuses everything), true for the
dyadic acceptor that compares a direct branch against a return branch. -/
def stepComparison : CascadeStep where
  name := "a trace without comparison is not a trace (2→3)"
  ObligationBelow := Verifies (fun _ : Reading ℕ => True)
  ObligationAbove := Verifies (dyadAcceptor (α := ℕ))
  insufficient := accept_all_not_verifying
  control := dyad_verifies

/-- **Floor 6→7**, instantiated with the real obligation: *the scale ratio is not captured at any
finite stage*. False for every rational ratio (a rational is exactly its own value), true for `φ`.
Note the floor reaches "irrational", not "`φ`" — the narrowing is the owned canonization step. -/
def stepScaleRatio : CascadeStep where
  name := "a rational scale is captured (6→7)"
  ObligationBelow := ∃ q : ℚ, NonCaptured (q : ℝ)
  ObligationAbove := NonCaptured ((1 + Real.sqrt 5) / 2)
  insufficient := rational_floor_insufficient
  control := phi_non_captured

/-- The carried floors, in the order §01.6.1c gives them. -/
def carriedFloors : List CascadeStep :=
  [stepComparison, stepOneLoop, stepOrderMemory, stepScaleRatio]

/-- **Every carried floor is a genuine, non-vacuous step.** This is the chain property, checked on
the floors that exist rather than asserted for the ones that do not. -/
theorem carried_floors_are_genuine :
    ∀ s ∈ carriedFloors, ¬ (s.ObligationBelow ↔ s.ObligationAbove) :=
  fun s _ => step_discriminates s

/-! ## The chain is linked: each repair is what fails next

This is the property that makes the cascade a *cascade* rather than a list of unrelated
obligations. If a repair satisfied every later obligation too, the unfolding would stop there and
the corpus would owe an explanation for continuing. It does not stop, and the reason is exact and
checkable at the floor already carried: the two-register carrier repaired at floor 4→5 **is**
`ℤ × ℤ`, and `ℤ × ℤ` is abelian, so it is precisely the carrier that fails floor 5→6.

The repair does not anticipate the next obligation; it creates the object on which the next
obligation is asked, and fails it. That is what "each floor forced by the insufficiency of the
previous" means, made checkable. -/

/-- **`chain_linked` — the floor 4→5 repair is the floor 5→6 failure.** The two-register carrier
that separates operation histories is `ℤ × ℤ`; being abelian it cannot encode order, so the very
object that fixed the previous floor is the one the next floor rejects. The cascade is therefore
forced to continue past floor 5 — it does not terminate at its own repair. -/
theorem chain_linked_four_five_to_five_six :
    (runTwo h₁ (0, 0) ≠ runTwo h₂ (0, 0)) ∧ ¬ OrderEncoded (Multiplicative (ℤ × ℤ)) :=
  ⟨two_loops_control, torus_insufficient⟩

/-- **The obligations do not collapse into one another.** Operation memory and order memory are
independent requirements: the two-register carrier meets the first and fails the second. So the two
floors are two, not one requirement counted twice — the count of floors is the count of genuinely
distinct insufficiencies. -/
theorem obligations_independent :
    stepOneLoop.ObligationAbove ∧ ¬ stepOrderMemory.ObligationBelow :=
  ⟨two_loops_control, torus_insufficient⟩

/-! ### How long the chain must be

"Three insufficiencies = three zones" (§01.6.1c) is a *counting* claim: the structure needs as many
additions as there are genuinely distinct insufficiencies. The lower-bound half of that is provable
now and is stated here; the exact count is not, and is not claimed.

The lower bound is this: whenever a step's repair fails a later step's obligation, no single
structural addition can discharge both, so the chain cannot be shortened by merging them. Applied to
the floors carried, it says the cascade needs at least two distinct additions past the register
model — which is what `chain_linked_four_five_to_five_six` exhibits concretely. -/

/-- **Two obligations that a single carrier cannot both discharge force two distinct additions.**
Abstract form of the non-merging argument: if `A` holds of a carrier while `B` fails of it, then `A`
and `B` are not the same requirement, so a repair aimed at `A` cannot be counted as a repair of
`B`. -/
theorem repairs_do_not_merge {A B : Prop} (hA : A) (hB : ¬ B) : ¬ (A ↔ B) :=
  fun h => hB (h.mp hA)

/-- **`chain_length_lower_bound` — the carried floors need two distinct additions.** The repair that
discharges operation memory (`ℤ × ℤ`) provably fails order memory, so those two obligations cannot
be met by one structural addition. The cascade past the single register is therefore at least two
steps long, independently of how the remaining floors turn out. -/
theorem chain_length_lower_bound :
    ¬ (stepOneLoop.ObligationAbove ↔ stepOrderMemory.ObligationBelow) :=
  repairs_do_not_merge two_loops_control torus_insufficient

/- The exact count is not represented by a vacuous `True` theorem here. Its precise reduction
boundary is formalized in `D0.Foundation.SceneCountReduction`: two typed interpretation maps must
connect the owner facts above and `D0.Tower.no_extension_theorem` to bounds on a variable scene
candidate. Neither map is currently constructed from M1/M1+. -/

/-- **D0-CASCADE-CHAIN-SCAFFOLD-001.** Every step of the cascade discriminates its two carriers and
is non-vacuous, given the two halves the shape demands. The two carried floors supply those halves
in their own modules (`cascade_floor_one_loop`, `cascade_floor_order_memory`); this theorem states
the composition property the chain accumulates. -/
theorem cascade_chain_scaffold :
    (∀ s : CascadeStep, ¬ (s.ObligationBelow ↔ s.ObligationAbove)) ∧
    (∀ s ∈ carriedFloors, ¬ (s.ObligationBelow ↔ s.ObligationAbove)) ∧
    (h₁ ≠ h₂ ∧ (∀ k : ℤ, runOne h₁ k = runOne h₂ k) ∧ runTwo h₁ (0, 0) ≠ runTwo h₂ (0, 0)) ∧
    (¬ OrderEncoded (Multiplicative (ℤ × ℤ)) ∧ OrderEncoded (Equiv.Perm (Fin 3))) ∧
    ((runTwo h₁ (0, 0) ≠ runTwo h₂ (0, 0)) ∧ ¬ OrderEncoded (Multiplicative (ℤ × ℤ))) ∧
    (¬ (stepOneLoop.ObligationAbove ↔ stepOrderMemory.ObligationBelow)) :=
  ⟨step_discriminates, carried_floors_are_genuine,
   ⟨histories_differ, one_loop_insufficient, two_loops_control⟩,
   ⟨torus_insufficient, control_orderEncoded⟩,
   chain_linked_four_five_to_five_six, chain_length_lower_bound⟩

end D0.Foundation
