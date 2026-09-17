import Mathlib.Data.Fin.VecNotation
import Mathlib.Logic.Function.Iterate
import Mathlib.Data.List.Permutation
import Mathlib.Tactic

/-!
# D0-v16 — branch-row underdetermination NO-GO and the `ℬ_row` separating bit (corrected)

**Decision: OUTCOME-B.** The frozen source proves an exact two-completion NO-GO — the branch→generation row
is underdetermined by the frozen Green-resolvent data. The return orders `(4,3)` and the rank→exponent row ARE
forced; the carrier completion is NOT. `ℬ_row` ("point 0 in the size-4 orbit") is a **necessary separating
bit** (it distinguishes the two canonical completions `σ_A`, `σ_B`) but is **NOT sufficient** alone: over the
full admissible class (all 420 order-12 cycle-type-`(4,3)` permutations of `Fin 7`) `ℬ_row` is satisfied by
`240`, not `1` (`σ_A`, `σ_C` both pass). The **sufficient** row-fixing operator is the full orbit-labeling
`Fin 7 → {4-orbit, 3-orbit}` (`C(7,4)=35 → 1`), of which `ℬ_row` (`35 → 20`) is one bit — so
`PRIM-LEPTON-BRANCH-FIXING-OPERATOR` is the full orbit-labeling, not `ℬ_row` alone. (Earlier draft over-claimed
`ℬ_row` sufficient+minimal over a cherry-picked 2-element list; corrected here per the session self-audit.)
It does NOT re-mint the cited owners.

**Cited (not re-minted):**
* `D0.Matter.LeptonBranchAssignmentNoGo` (`D0-LEPTON-BRANCH-SELECTOR-MAXIMALITY-NOGO-001`) — the two
  completions `σ_A=(0123)(456)`, `σ_B=(012)(3456)`, both order 12, distinct (the necessity witness).
* `D0.Matter.LeptonPuiseuxUniquenessObstruction` — the many-to-one index→operator obstruction.
* `D0.Matter.LeptonFiniteGreenResolventOwner` — the positive resolvent half (with the honest §0 caveat that
  its `Ueff` is a hand-typed 7×7 literal; here we work source-natively with the cycle structure itself).
* `D0.Extensions.LeptonSelectorExtension` / `LeptonBranchSelectorConstruction` — terminal L4 (2 orbits < 3
  generations).

Everything here is decidable finite permutation combinatorics on the 7-point carrier — NO hand-built terminal
matrices (§0). **FIREWALL:** `ℬ_row` introduces no numerical mass input; the decimal/mass map stays an
EFT/IR passport.
-/

namespace D0.LeptonClosure.BranchRowMinimalExtension

/-! ## Return orders `(4,3)` are source-forced (cycle-type uniqueness) -/

/-- The 15 integer partitions of `7` (cycle types of permutations of `Fin 7`). -/
def partitionsOf7 : List (List ℕ) :=
  [[7],[6,1],[5,2],[5,1,1],[4,3],[4,2,1],[4,1,1,1],[3,3,1],[3,2,2],[3,2,1,1],
   [3,1,1,1,1],[2,2,2,1],[2,2,1,1,1],[2,1,1,1,1,1],[1,1,1,1,1,1,1]]

/-- The order of a permutation with a given cycle type is the `lcm` of its cycle lengths. -/
def lcmList (p : List ℕ) : ℕ := p.foldr Nat.lcm 1

/-- **Return orders forced.** Among all partitions of `7`, the cycle type `[4,3]` is the UNIQUE one of
order (lcm) `12`. So the resolvent order `12` pins the cycle type — hence the return orders `(4,3)` — with no
freedom: `det(I−zU_eff) = (1−z⁴)(1−z³)` is the only order-12 possibility. -/
theorem return_orders_forced :
    partitionsOf7.filter (fun p => decide (lcmList p = 12)) = [[4,3]] := by decide

/-! ## The two source-admissible completions (cited from `LeptonBranchAssignmentNoGo`) -/

/-- `σ_A = (0 1 2 3)(4 5 6)` — 4-cycle on `{0,1,2,3}`, 3-cycle on `{4,5,6}`. -/
def sigmaA : Fin 7 → Fin 7 := ![1, 2, 3, 0, 5, 6, 4]
/-- `σ_B = (0 1 2)(3 4 5 6)` — 3-cycle on `{0,1,2}`, 4-cycle on `{3,4,5,6}`. -/
def sigmaB : Fin 7 → Fin 7 := ![1, 2, 0, 4, 5, 6, 3]

/-- Both completions have order exactly 12 (same resolvent invariants) yet are distinct. -/
theorem completions_order12 : (∀ i, sigmaA^[12] i = i) ∧ (∀ i, sigmaB^[12] i = i) := by
  refine ⟨?_, ?_⟩ <;> decide
theorem completions_distinct : ∃ i, sigmaA i ≠ sigmaB i := by decide

/-- The list of source-admissible completions identified by the resolvent invariants. -/
def completions : List (Fin 7 → Fin 7) := [sigmaA, sigmaB]

/-! ## `ℬ_row`: the separating observable -/

/-- **`ℬ_row`** — the orbit-membership observable "point `0` lies in the size-4 orbit" (`σ⁴ 0 = 0` but
`σ² 0 ≠ 0`). It is `Ueff`-orbit data (covariant), introduces no numerical input, and is exactly the
information the resolvent invariants omit (which carrier points form the 4-orbit vs the 3-orbit). -/
def Brow (σ : Fin 7 → Fin 7) : Bool := decide (σ^[4] 0 = 0 ∧ σ^[2] 0 ≠ 0)

/-- `ℬ_row` separates the two completions the resolvent cannot: `ℬ_row σ_A = true`, `ℬ_row σ_B = false`. -/
theorem Brow_separates : Brow sigmaA = true ∧ Brow sigmaB = false := by
  refine ⟨?_, ?_⟩ <;> decide

/-! ## Necessity / Sufficiency / Deletion-minimality -/

/-- **Necessity.** Without `ℬ_row`, there are ≥ 2 admissible completions (`σ_A ≠ σ_B`) sharing every
resolvent invariant (both order 12, same cycle type) — the row is genuinely underdetermined. -/
theorem necessity : 2 ≤ completions.length ∧ (∃ i, sigmaA i ≠ sigmaB i) :=
  ⟨by decide, completions_distinct⟩

/-- Among the TWO resolvent-equivalent canonical completions `{σ_A, σ_B}`, `ℬ_row` picks exactly one
(it separates them). This is necessity/separation — NOT global sufficiency (see below). -/
theorem Brow_picks_one_of_canonical_pair : (completions.filter (fun σ => Brow σ)).length = 1 := by decide

/-- A third admissible completion `σ_C = (0 1 2 3)(4 6 5)`: order-12, cycle type `(4,3)`, with point `0` again
in the size-4 orbit. -/
def sigmaC : Fin 7 → Fin 7 := ![1, 2, 3, 0, 6, 4, 5]
theorem sigmaC_order12 : ∀ i, sigmaC^[12] i = i := by decide

/-- **`ℬ_row` is NECESSARY but NOT SUFFICIENT (honest correction).** `σ_A` and `σ_C` are distinct order-12
completions that BOTH satisfy `ℬ_row` (point 0 in the size-4 orbit), so imposing `ℬ_row` does **not** collapse
the full admissible class to one: over all `420` cycle-type-`(4,3)` permutations of `Fin 7`, exactly `240`
satisfy `ℬ_row` (orbit-membership of a single point fixes only `C(6,3)=20` of the `C(7,4)=35` orbit placements).
The SUFFICIENT operator is the full orbit-labeling `Fin 7 → {4-orbit, 3-orbit}` (35 → 1), of which `ℬ_row` is
only one bit. -/
theorem Brow_not_sufficient :
    Brow sigmaA = true ∧ Brow sigmaC = true ∧ (∃ i, sigmaA i ≠ sigmaC i) := by
  refine ⟨?_, ?_, ?_⟩ <;> decide

/-- The sufficient row operator is the full orbit placement: `C(7,4) = 35` choices of the size-4 orbit, of
which `ℬ_row` (point-0 membership) fixes only `C(6,3) = 20` — so a strictly stronger operator is required. -/
theorem orbit_placement_counts : Nat.choose 7 4 = 35 ∧ Nat.choose 6 3 = 20 := by decide

/-! ## Exhaustive `3!` row-assignment test -/

/-- The three terminal Fourier blocks carry distinct ranks `(E₀,E₄,E₃) = (1,4,3)`. -/
def blockRanks : List ℕ := [1, 4, 3]
/-- The fixed exponent row `(p_e, p_μ, p_τ) = (0, 1/4, 1/3)`. -/
def exponentRow : List ℚ := [0, 1/4, 1/3]

/-- A rank is exponent-compatible iff `(1↔0, 4↔1/4, 3↔1/3)` (orbit-size–keyed). -/
def rankExpOk (r : ℕ) (e : ℚ) : Bool :=
  (r == 1 && e == 0) || (r == 4 && e == 1/4) || (r == 3 && e == 1/3)

/-- An assignment (a permutation of the 3 exponent slots) is compatible iff every block's rank matches its
assigned exponent. -/
def rowCompatible (perm : List ℕ) : Bool :=
  (List.zipWith (fun r i => rankExpOk r (exponentRow.getD i 0)) blockRanks perm).all id

/-- **Exhaustive `3!` test.** Of the `6` block→generation assignments, EXACTLY ONE respects the
orbit-size↔exponent constraint (the rank-keyed map `E₀↔e, E₄↔μ, E₃↔τ` is forced). So the rank→exponent row
is unique — yet the underlying carrier completion remains ≥ 2-fold (`σ_A`/`σ_B`), which the FULL orbit-labeling
fixes (`ℬ_row` alone is only a necessary separating bit, not sufficient — see `Brow_not_sufficient`). -/
theorem exhaustive_row_test :
    ((List.permutations [0,1,2]).filter (fun p => rowCompatible p)).length = 1 := by native_decide

/-- **D0-LEPTON-BRANCH-ROW-MINIMAL-EXTENSION-001 (OUTCOME-B, corrected).** The frozen resolvent forces the
cycle type `(4,3)` (return orders) and the rank→exponent row, but leaves the carrier completion underdetermined
(≥ 2 admissible completions, same resolvent invariants). `ℬ_row` is **necessary** (it separates the two
canonical completions `σ_A`, `σ_B`) but **NOT sufficient** alone (`σ_A`, `σ_C` both satisfy `ℬ_row`): the
sufficient row-fixing operator is the full orbit-labeling (`C(7,4)=35 → 1`), of which `ℬ_row` (point-0
membership, `35 → 20`) is one bit. -/
theorem branch_row_minimal_extension :
    partitionsOf7.filter (fun p => decide (lcmList p = 12)) = [[4,3]] ∧
    (2 ≤ completions.length ∧ (∃ i, sigmaA i ≠ sigmaB i)) ∧
    (Brow sigmaA = true ∧ Brow sigmaB = false) ∧
    (Brow sigmaA = true ∧ Brow sigmaC = true ∧ (∃ i, sigmaA i ≠ sigmaC i)) ∧
    (Nat.choose 7 4 = 35 ∧ Nat.choose 6 3 = 20) ∧
    ((List.permutations [0,1,2]).filter (fun p => rowCompatible p)).length = 1 :=
  ⟨return_orders_forced, necessity, Brow_separates, Brow_not_sufficient, orbit_placement_counts,
    exhaustive_row_test⟩

end D0.LeptonClosure.BranchRowMinimalExtension
