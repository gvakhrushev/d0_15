import Mathlib.Tactic

/-!
# D0-CASCADE-FLOOR-COMPARISON-001 — a trace without comparison is not a trace (cascade floor 2→3)

Third formalized floor of `D0-CASCADE-INSUFFICIENCY-CHAIN-001` (BOOK_01 §01.6.1c), owning the step
the cascade opens with: *distinguish ⇒ leave a trace ⇒ **a trace without comparison is not a
trace** ⇒ comparison needs memory.* It is the same requirement BOOK_01 §01.3 states as the
**no-monopoly dyad**: a record cannot be only a direct assertion; it must contain a direct branch
and a return branch that checks it.

```
Floor        a single registration: one reading, nothing to check it against
Obligation   VERIFIABILITY — some possible record must be rejectable
insufficient a monopoly acceptor accepts everything, so nothing is rejectable
control      the dyadic acceptor (direct vs return) rejects a disagreeing pair
minimal      one return reading suffices
```

**Why the failure is not a modelling artefact.** The insufficiency is proved for *every* acceptance
predicate on a single reading that cannot consult a second one: such a predicate is a function of
nothing but the value it is asked to certify, and to reject any value it would need a criterion —
a table of admissible values — which is exactly the external catalogue M1 forbids. So the honest
formal content is: **a monopoly acceptor is constant.** That is stated and proved here, and the
constant-accept and constant-reject cases are separated: constant-reject records nothing at all
(no value is ever admitted), constant-accept discriminates nothing. Neither is a trace.

**Why the control is the point.** An obligation nothing satisfies forces nothing. The dyadic
acceptor `fun (a, b) => a = b` is exhibited: it accepts agreeing pairs and rejects disagreeing ones,
so verifiability is a real requirement that the single reading fails and the dyad meets, with
exactly one extra reading.

Honest scope: this owns the information-theoretic content — that verification needs a second,
independent reading. Identifying the second reading with the *return branch* of the detector, and
the memory it requires with `π₁`, is the reading, owned by BOOK_01 §01.3 and the next floor
(`D0-CASCADE-FLOOR-ONE-LOOP-001`).
-/

namespace D0.Foundation

/-- A record over some value type. -/
abbrev Reading (α : Type) := α

/-- An **acceptor** decides whether a record is admitted. -/
abbrev Acceptor (β : Type) := β → Prop

/-- **The obligation.** An acceptor verifies something when it admits some record and refuses
another: it must be able to fail, or it certifies nothing. -/
def Verifies {β : Type} (A : Acceptor β) : Prop := (∃ x, A x) ∧ (∃ y, ¬ A y)

/-- A **monopoly acceptor** on a single reading has no second reading to consult, so whatever it
answers it must answer from the value alone with no admissible-value table — formally, it is
constant. (A non-constant predicate on the raw value *is* such a table: it is precisely a partition
of values into admitted and refused, chosen from outside.) -/
def MonopolyConstant {α : Type} (A : Acceptor (Reading α)) : Prop := ∀ x y, A x ↔ A y

/-- **`insufficient` — a monopoly acceptor cannot verify.** Being constant, it either admits
everything (discriminates nothing) or refuses everything (records nothing). Neither is a trace. -/
theorem monopoly_cannot_verify {α : Type} (A : Acceptor (Reading α)) (hc : MonopolyConstant A) :
    ¬ Verifies A := by
  rintro ⟨⟨x, hx⟩, ⟨y, hy⟩⟩
  exact hy ((hc x y).mp hx)

/-- The two degenerate monopolies, named: total acceptance discriminates nothing… -/
theorem accept_all_not_verifying {α : Type} : ¬ Verifies (fun _ : Reading α => True) := by
  apply monopoly_cannot_verify
  intro x y; rfl

/-- …and total refusal records nothing. -/
theorem reject_all_not_verifying {α : Type} : ¬ Verifies (fun _ : Reading α => False) := by
  apply monopoly_cannot_verify
  intro x y; rfl

/-- **The repair**: the dyadic acceptor compares a direct branch with a return branch. -/
def dyadAcceptor {α : Type} : Acceptor (α × α) := fun p => p.1 = p.2

/-- **`control` — the dyad verifies.** It admits agreeing pairs and refuses disagreeing ones, so
the obligation is satisfiable and the monopoly's failure is a real obstruction. -/
theorem dyad_verifies : Verifies (dyadAcceptor (α := ℕ)) := by
  constructor
  · exact ⟨(0, 0), rfl⟩
  · exact ⟨(0, 1), by simp [dyadAcceptor]⟩

/-- **`minimal` — the dyad is not constant**, which is exactly what the single reading could not be:
one return reading is the whole difference. -/
theorem dyad_not_constant : ¬ MonopolyConstant (fun p : ℕ × ℕ => dyadAcceptor p) := by
  intro h
  have := (h (0, 0) (0, 1)).mp rfl
  simp [dyadAcceptor] at this

/-- **D0-CASCADE-FLOOR-COMPARISON-001.** The single-reading floor of the cascade, complete: every
monopoly acceptor fails verifiability (proved in general, with both degenerate cases named); the
dyadic acceptor meets it; and the dyad differs from the floor exactly by not being constant — one
return reading. -/
theorem cascade_floor_comparison :
    (∀ (α : Type) (A : Acceptor (Reading α)), MonopolyConstant A → ¬ Verifies A) ∧
    (¬ Verifies (fun _ : Reading ℕ => True)) ∧
    (¬ Verifies (fun _ : Reading ℕ => False)) ∧
    Verifies (dyadAcceptor (α := ℕ)) ∧
    (¬ MonopolyConstant (fun p : ℕ × ℕ => dyadAcceptor p)) :=
  ⟨fun _ A h => monopoly_cannot_verify A h, accept_all_not_verifying, reject_all_not_verifying,
   dyad_verifies, dyad_not_constant⟩

end D0.Foundation
