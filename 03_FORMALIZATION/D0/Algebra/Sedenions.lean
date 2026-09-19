import Mathlib.Data.Fintype.Perm
import Mathlib.GroupTheory.Perm.Basic
import Mathlib.Tactic
import D0.Algebra.SedenionTower

/-!
# Legacy three-label S3 scaffold — not a sedenion realization

The historical version of this file called a three-element type
`OctonionBranch` a formalization of sedenions and inferred three fermion
generations from hand-written permutations.  That was status inflation.

The actual Cayley--Dickson carrier now lives in
`D0.Algebra.CayleyDickson` and `D0.Algebra.SedenionTower`.
This file retains only the finite three-label S3-set because it can be useful
as a combinatorial indexing scaffold.

Crucially, the scaffold does **not** determine an algebra structure.  We give
two distinct binary products on the same carrier, both equivariant under every
relabeling permutation.  Therefore cardinality three plus an S3 action cannot
establish a sedenion multiplication, octonionic subalgebras, algebra
automorphisms, Clifford left action, minimal ideals, or a D0 generation
representation functor.
-/

namespace D0.Algebra.Sedenions

/-- A legacy three-label indexing carrier.  The constructors are names only;
they are not octonionic subalgebras until an actual embedding theorem is supplied. -/
inductive OctonionBranch : Type
  | O1 : OctonionBranch
  | O2 : OctonionBranch
  | O3 : OctonionBranch
  deriving DecidableEq, Fintype, Repr

open OctonionBranch

theorem octonion_branch_card : Fintype.card OctonionBranch = 3 := by
  decide

def branchToFin : OctonionBranch → Fin 3
  | O1 => 0
  | O2 => 1
  | O3 => 2

def finToBranch : Fin 3 → OctonionBranch
  | ⟨0, _⟩ => O1
  | ⟨1, _⟩ => O2
  | ⟨2, _⟩ => O3

theorem branchToFin_finToBranch (i : Fin 3) :
    branchToFin (finToBranch i) = i := by
  fin_cases i <;> rfl

theorem finToBranch_branchToFin (b : OctonionBranch) :
    finToBranch (branchToFin b) = b := by
  cases b <;> rfl

theorem branch_generation_bijective :
    ∃ h : OctonionBranch → Fin 3, Function.Bijective h := by
  refine ⟨branchToFin, ?_, ?_⟩
  · intro x y hxy
    cases x <;> cases y <;> simp [branchToFin] at hxy ⊢
  · intro y
    exact ⟨finToBranch y, branchToFin_finToBranch y⟩

/-- Cyclic permutation of the three labels. -/
def s3_cycle : OctonionBranch → OctonionBranch
  | O1 => O2
  | O2 => O3
  | O3 => O1

/-- Transposition of the first two labels. -/
def s3_swap : OctonionBranch → OctonionBranch
  | O1 => O2
  | O2 => O1
  | O3 => O3

theorem s3_cycle_order3 : s3_cycle ∘ s3_cycle ∘ s3_cycle = id := by
  funext b
  cases b <;> rfl

theorem s3_swap_order2 : s3_swap ∘ s3_swap = id := by
  funext b
  cases b <;> rfl

theorem s3_action_transitive (x y : OctonionBranch) :
    ∃ f : OctonionBranch → OctonionBranch,
      (f = id ∨ f = s3_cycle ∨ f = s3_cycle ∘ s3_cycle ∨
       f = s3_swap ∨ f = s3_swap ∘ s3_cycle ∨ f = s3_cycle ∘ s3_swap) ∧
      f x = y := by
  cases x <;> cases y
  · use id; simp
  · use s3_cycle; simp [s3_cycle]
  · use s3_cycle ∘ s3_cycle; simp [s3_cycle]
  · use s3_cycle ∘ s3_cycle; simp [s3_cycle]
  · use id; simp
  · use s3_cycle; simp [s3_cycle]
  · use s3_cycle; simp [s3_cycle]
  · use s3_cycle ∘ s3_cycle; simp [s3_cycle]
  · use id; simp

/-! ## Negative control: an S3-set does not determine multiplication -/

/-- First projection product on the same three-label carrier. -/
def leftProduct (x _y : OctonionBranch) : OctonionBranch := x

/-- Second projection product on the same three-label carrier. -/
def rightProduct (_x y : OctonionBranch) : OctonionBranch := y

theorem leftProduct_ne_rightProduct : leftProduct ≠ rightProduct := by
  intro h
  have hh := congrFun (congrFun h O1) O2
  simp [leftProduct, rightProduct] at hh

/-- Every relabeling permutation is an automorphism of the left-projection magma. -/
theorem leftProduct_equivariant (σ : Equiv.Perm OctonionBranch) (x y : OctonionBranch) :
    σ (leftProduct x y) = leftProduct (σ x) (σ y) := by
  rfl

/-- Every relabeling permutation is also an automorphism of the distinct
right-projection magma. -/
theorem rightProduct_equivariant (σ : Equiv.Perm OctonionBranch) (x y : OctonionBranch) :
    σ (rightProduct x y) = rightProduct (σ x) (σ y) := by
  rfl

/-- The exact negative control required by the sedenion audit: the same
three-element S3 carrier admits distinct fully relabeling-equivariant products.
Hence the S3-set data do not determine even a multiplication law. -/
theorem bare_threeset_insufficient_for_sedenion_realization :
    leftProduct ≠ rightProduct ∧
    (∀ (σ : Equiv.Perm OctonionBranch) x y,
      σ (leftProduct x y) = leftProduct (σ x) (σ y)) ∧
    (∀ (σ : Equiv.Perm OctonionBranch) x y,
      σ (rightProduct x y) = rightProduct (σ x) (σ y)) := by
  exact ⟨leftProduct_ne_rightProduct,
    leftProduct_equivariant,
    rightProduct_equivariant⟩

/-- Honest capstone for the legacy file: exactly a transitive three-label S3
scaffold plus the proof that this scaffold is algebraically insufficient. -/
theorem branch_label_s3_scaffold :
    Fintype.card OctonionBranch = 3 ∧
    (∀ x y : OctonionBranch, ∃ f : OctonionBranch → OctonionBranch,
      (f = id ∨ f = s3_cycle ∨ f = s3_cycle ∘ s3_cycle ∨
       f = s3_swap ∨ f = s3_swap ∘ s3_cycle ∨ f = s3_cycle ∘ s3_swap) ∧
      f x = y) ∧
    leftProduct ≠ rightProduct := by
  exact ⟨octonion_branch_card, s3_action_transitive, leftProduct_ne_rightProduct⟩

end D0.Algebra.Sedenions
