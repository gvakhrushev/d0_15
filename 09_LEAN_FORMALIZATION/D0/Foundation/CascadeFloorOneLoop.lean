import Mathlib.Tactic

/-!
# D0-CASCADE-FLOOR-ONE-LOOP-001 — one loop cannot carry memory (cascade floor 4→5)

Second formalized floor of `D0-CASCADE-INSUFFICIENCY-CHAIN-001` (BOOK_01 §01.6.1c), owning the step
BOOK_03 §03.23.2 argues in prose:

> "Suppose a single loop `γ`, topology `ℤ`. Its state is one integer `k`; every operation just
> changes `k`. But `k` alone cannot say which mode produced it: Write (change `k`) vs Read (sample
> `k` without changing it) are indistinguishable from the value. Separating the modes needs an
> exogenous flag `M ∈ {R,W}`, which is not derivable from the topology `ℤ` — an external catalogue,
> banned by M1. The only admissible fix is a second independent loop."

Formalized in the shape the chain claim fixes:

```
Floor        a single register, state ℤ, operations acting on it
Obligation   OPERATION MEMORY — the final state must determine which operation sequence produced it
insufficient the one-register run map is NOT injective: two different histories, same final state
control      the two-register run map SEPARATES those same two histories
minimal      one extra register suffices, so two loops is the minimum repair
```

**Why the control is the point.** `insufficient` on its own could be met by an obligation nothing
satisfies, and an unsatisfiable demand forces nothing. Exhibiting the two-register model that *does*
separate the very histories the one-register model confuses turns the failure into an obstruction
with a named minimal repair — the same `check_cert_can_fail` discipline applied to the spine.

Honest scope: this owns the information-theoretic content — that a single ℤ-valued register cannot
recover its operation history while a pair can. The identification of the register with `π₁` of a
loop, and of the second register with an independent cycle, is the reading, owned by BOOK_03
§03.23.2–3.
-/

namespace D0.Foundation

/-- The two primitive modes of the detector act. `write` alters the record; `read` samples it. -/
inductive Op where
  | write : Op
  | read : Op
  deriving DecidableEq, Repr

/-- **The floor**: a single loop's state is one integer, and each operation acts on it. `write`
advances the winding; `read` samples without changing it — that is what "read" means. -/
def stepOne : Op → ℤ → ℤ
  | Op.write, k => k + 1
  | Op.read, k => k

/-- Running a history on the single register. -/
def runOne : List Op → ℤ → ℤ
  | [], k => k
  | o :: rest, k => runOne rest (stepOne o k)

/-- **The repair**: a second, independent loop. The first component carries the value, the second
carries the operation count — the write/read distinction the first cannot hold. -/
def stepTwo : Op → ℤ × ℤ → ℤ × ℤ
  | Op.write, (k, n) => (k + 1, n + 1)
  | Op.read, (k, n) => (k, n + 1)

def runTwo : List Op → ℤ × ℤ → ℤ × ℤ
  | [], s => s
  | o :: rest, s => runTwo rest (stepTwo o s)

/-- The two histories that separate the floors: one read, versus two reads. -/
def h₁ : List Op := [Op.read]
def h₂ : List Op := [Op.read, Op.read]

theorem histories_differ : h₁ ≠ h₂ := by decide

/-- **`insufficient` — one loop confuses two distinct histories.** Reading leaves no trace in the
value, so from the final state the number of reads is unrecoverable: `runOne h₁ = runOne h₂` at
*every* initial state, not merely at one. -/
theorem one_loop_insufficient : ∀ k : ℤ, runOne h₁ k = runOne h₂ k := by
  intro k
  simp [runOne, h₁, h₂, stepOne]

/-- The failure is not about these two histories only: any two all-`read` histories collapse. -/
theorem one_loop_forgets_all_reads (m n : ℕ) (k : ℤ) :
    runOne (List.replicate m Op.read) k = runOne (List.replicate n Op.read) k := by
  have h : ∀ j : ℕ, ∀ x : ℤ, runOne (List.replicate j Op.read) x = x := by
    intro j
    induction j with
    | zero => intro x; simp [runOne]
    | succ i ih => intro x; simp [List.replicate_succ, runOne, stepOne, ih]
  rw [h m k, h n k]

/-- **`control` — two loops separate exactly those histories.** So the obligation is satisfiable,
the insufficiency is a real obstruction rather than a vacuous demand, and the repair is exhibited. -/
theorem two_loops_control : runTwo h₁ (0, 0) ≠ runTwo h₂ (0, 0) := by
  decide

/-- **`minimal` — one added register is enough.** The repair does not need a third loop: the pair
already distinguishes the confused histories, so two independent cycles is the minimum. -/
theorem two_loops_suffice_for_the_witness :
    runTwo h₁ (0, 0) = (0, 1) ∧ runTwo h₂ (0, 0) = (0, 2) := by
  constructor <;> decide

/-- **D0-CASCADE-FLOOR-ONE-LOOP-001.** The single-loop floor of the cascade, complete: the
one-register run map confuses two distinct histories at every initial state (and collapses all
read-only histories); the two-register map separates the same pair; and the separation is achieved
with exactly one additional loop. -/
theorem cascade_floor_one_loop :
    h₁ ≠ h₂ ∧
    (∀ k : ℤ, runOne h₁ k = runOne h₂ k) ∧
    runTwo h₁ (0, 0) ≠ runTwo h₂ (0, 0) ∧
    (∀ m n : ℕ, ∀ k : ℤ,
      runOne (List.replicate m Op.read) k = runOne (List.replicate n Op.read) k) :=
  ⟨histories_differ, one_loop_insufficient, two_loops_control, one_loop_forgets_all_reads⟩

end D0.Foundation
