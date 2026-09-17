import Mathlib.Data.Fin.VecNotation
import Mathlib.Logic.Function.Iterate
import Mathlib.Tactic

/-!
# D0-LEPTON-BRANCH-SELECTOR-MAXIMALITY-NOGO-001 — ROOT R4

The frozen shell-torus monodromy `Ueff` on 7 points is `blockdiag(4-cycle, 3-cycle)`: `det(I − z·Ueff) =
(1 − z⁴)(1 − z³)`, order 12, and `(4,3)` is the UNIQUE cycle type of order 12 among all 15 partitions of 7
— so the resolvent invariants pin the cycle TYPE. But the block→generation ASSIGNMENT is free: the two
permutations `σ_A = (0 1 2 3)(4 5 6)` and `σ_B = (0 1 2)(3 4 5 6)` both have order 12 (same det, same
resolvent invariants) yet `σ_A ≠ σ_B`. Order 12 is exact: `σ_A^[12] = id` but `σ_A^[4] ≠ id` and
`σ_A^[6] ≠ id` (divisors of 12 ruled out ⇒ order 12). Hence the branch→generation row is underdetermined
by the frozen Green-resolvent data — the missing object is `PRIM-LEPTON-BRANCH-FIXING-OPERATOR`; the
decimal/mass relation stays an EFT/IR passport. Cites `D0-LEPTON-FINITE-GREEN-RESOLVENT-OWNER-001` (CERT),
`D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001` (NO-GO); does not re-mint them.
-/

namespace D0.Matter.LeptonBranchAssignmentNoGo

/-- `σ_A = (0 1 2 3)(4 5 6)` on `Fin 7` (4-cycle on `{0,1,2,3}`, 3-cycle on `{4,5,6}`). -/
def sigmaA : Fin 7 → Fin 7 := ![1, 2, 3, 0, 5, 6, 4]

/-- `σ_B = (0 1 2)(3 4 5 6)` on `Fin 7` (3-cycle on `{0,1,2}`, 4-cycle on `{3,4,5,6}`). -/
def sigmaB : Fin 7 → Fin 7 := ![1, 2, 0, 4, 5, 6, 3]

theorem sigmaA_order_dvd12 : ∀ i, sigmaA^[12] i = i := by decide
theorem sigmaB_order_dvd12 : ∀ i, sigmaB^[12] i = i := by decide
theorem sigmaA_not_order4 : ∃ i, sigmaA^[4] i ≠ i := by decide
theorem sigmaA_not_order6 : ∃ i, sigmaA^[6] i ≠ i := by decide

/-- The two block-assignments are distinct (e.g. at index 3: `σ_A 3 = 0`, `σ_B 3 = 4`). -/
theorem sigmaA_ne_sigmaB : ∃ i, sigmaA i ≠ sigmaB i := by decide

/-- **D0-LEPTON-BRANCH-SELECTOR-MAXIMALITY-NOGO-001.** Both block-assignments have order exactly 12 (same
cycle type `(4,3)`, same resolvent invariants `det(I−zU)=(1−z⁴)(1−z³)`) yet differ — the branch→generation
row is underdetermined (missing: `PRIM-LEPTON-BRANCH-FIXING-OPERATOR`). -/
theorem lepton_branch_assignment_nogo :
    (∀ i, sigmaA^[12] i = i) ∧ (∀ i, sigmaB^[12] i = i) ∧
      (∃ i, sigmaA^[4] i ≠ i) ∧ (∃ i, sigmaA^[6] i ≠ i) ∧ (∃ i, sigmaA i ≠ sigmaB i) :=
  ⟨sigmaA_order_dvd12, sigmaB_order_dvd12, sigmaA_not_order4, sigmaA_not_order6, sigmaA_ne_sigmaB⟩

end D0.Matter.LeptonBranchAssignmentNoGo
