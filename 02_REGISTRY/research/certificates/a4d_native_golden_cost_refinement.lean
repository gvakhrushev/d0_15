import D0.CondensedAnchor.DetectorSupportGoldenWeight
import D0.Algebra.FibonacciAFTower
import D0.Representation.GoldenCoherentMemory
import Mathlib.Data.Matrix.Block
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic

/-! The actual golden cylinder cost gives a rooted Fibonacci refinement.
The matrix inclusion and its full conditional expectation are constructed,
not supplied as premises of the generic GNS isometry theorem. No physical
heat law, operation admission or metric readout is asserted. -/
namespace D0.Research.GoldenCostRefinement
open Matrix
open scoped BigOperators
noncomputable section
set_option linter.unusedSectionVars false

/-- Direct branch is one code symbol; the return branch is 10. -/
def code : List Bool → List Bool
  | [] => []
  | true :: w => false :: code w
  | false :: w => true :: false :: code w

theorem code_length (w : List Bool) :
    (code w).length = D0.CondensedAnchor.weightExp w := by
  induction w with
  | nil => rfl
  | cons b w ih =>
    cases b with
    | false => simp [code, D0.CondensedAnchor.weightExp, ih, Nat.add_comm]; omega
    | true => simp [code, D0.CondensedAnchor.weightExp, ih, Nat.add_comm]

theorem code_append (u v : List Bool) : code (u ++ v) = code u ++ code v := by
  induction u with
  | nil => rfl
  | cons b u ih => cases b <;> simp [code, ih]

def counts : ℕ → ℕ × ℕ
  | 0 => (1, 0)
  | n + 1 => ((counts n).1 + (counts n).2, (counts n).1)

/-- The rooted cut has one initial state; after one step it is the owner's tower. -/
theorem counts_bind_owner (n : ℕ) :
    counts (n+1) = D0.Algebra.FibonacciAFTower.pathCount n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    change ((counts (n+1)).1 + (counts (n+1)).2, (counts (n+1)).1) =
      ((D0.Algebra.FibonacciAFTower.pathCount n).1 +
        (D0.Algebra.FibonacciAFTower.pathCount n).2,
        (D0.Algebra.FibonacciAFTower.pathCount n).1)
    rw [ih]

theorem mass_one (p : ℝ) (hp : p + p^2 = 1) (n : ℕ) :
    (counts n).1 * p^n + (counts n).2 * p^(n+1) = 1 := by
  induction n with
  | zero => simp [counts]
  | succ n ih =>
    simp only [counts, Nat.cast_add]
    simp only [pow_succ] at ih ⊢
    calc
      ((counts n).1 + (counts n).2 : ℝ) * (p^n * p) +
          (counts n).1 * (p^n * p * p) =
          (counts n).1 * p^n * (p+p^2) + (counts n).2 * (p^n*p) := by ring
      _ = 1 := by rw [hp]; simpa using ih

theorem owner_trace_normalized (p : ℝ) (hp : p+p^2=1) (n : ℕ) :
    (D0.Algebra.FibonacciAFTower.pathCount n).1 * p^(n+1) +
      (D0.Algebra.FibonacciAFTower.pathCount n).2 * p^(n+2) = 1 := by
  simpa only [counts_bind_owner] using mass_one p hp (n+1)

variable {I J : Type*} [Fintype I] [Fintype J] [DecidableEq I] [DecidableEq J]

def diagInclude (A : Matrix I I ℝ) (B : Matrix J J ℝ) :
    Matrix (I ⊕ J) (I ⊕ J) ℝ := fromBlocks A 0 0 B

theorem diagInclude_mul (A C : Matrix I I ℝ) (B D : Matrix J J ℝ) :
    diagInclude A B * diagInclude C D = diagInclude (A*C) (B*D) := by
  simp [diagInclude, fromBlocks_multiply]

theorem diagInclude_transpose (A : Matrix I I ℝ) (B : Matrix J J ℝ) :
    (diagInclude A B).transpose = diagInclude A.transpose B.transpose := by
  simp [diagInclude, fromBlocks_transpose]

theorem diagInclude_one :
    diagInclude (1 : Matrix I I ℝ) (1 : Matrix J J ℝ) = 1 := by
  ext i j
  cases i <;> cases j <;> simp [diagInclude, fromBlocks, Matrix.one_apply]

theorem trace_diagInclude (A : Matrix I I ℝ) (B : Matrix J J ℝ) :
    trace (diagInclude A B) = trace A + trace B := by
  simp [diagInclude, trace, Matrix.diag, Fintype.sum_sum_type]

theorem trace_full_blocks (X : Matrix I I ℝ) (Y : Matrix J J ℝ)
    (U : Matrix I J ℝ) (V : Matrix J I ℝ) :
    trace (fromBlocks X U V Y) = trace X + trace Y := by
  simp [trace, Matrix.diag, Fintype.sum_sum_type]

def coarseTrace (p t : ℝ) (A : Matrix I I ℝ) (B : Matrix J J ℝ) : ℝ :=
  t * trace A + p*t * trace B

def fineTrace (p t : ℝ) (Z : Matrix (I ⊕ J) (I ⊕ J) ℝ)
    (W : Matrix I I ℝ) : ℝ := p*t * trace Z + p^2*t * trace W

/-- Literal full algebra inclusion (A,B) ↦ (diag(A,B),A), with no trace premise. -/
theorem actual_trace_preservation (p t : ℝ) (hp : p+p^2=1)
    (A : Matrix I I ℝ) (B : Matrix J J ℝ) :
    fineTrace p t (diagInclude A B) A = coarseTrace p t A B := by
  rw [fineTrace, trace_diagInclude, coarseTrace]
  linear_combination t * trace A * hp

/-- Actual all-size GNS isometry, with the inclusion and trace already constructed. -/
theorem actual_gns_isometry (p t : ℝ) (hp : p+p^2=1)
    (A C : Matrix I I ℝ) (B D : Matrix J J ℝ) :
    fineTrace p t ((diagInclude C D).transpose * diagInclude A B) (C.transpose*A)
      = coarseTrace p t (C.transpose*A) (D.transpose*B) := by
  rw [diagInclude_transpose, diagInclude_mul]
  exact actual_trace_preservation p t hp _ _

/-- The complete conditional adjoint on actual matrices, including both off-diagonal blocks. -/
theorem actual_conditional_adjoint (p t : ℝ)
    (A X W : Matrix I I ℝ) (B Y : Matrix J J ℝ)
    (U : Matrix I J ℝ) (V : Matrix J I ℝ) :
    fineTrace p t ((diagInclude A B).transpose * fromBlocks X U V Y) (A.transpose*W)
      = coarseTrace p t (A.transpose*(p • X+p^2 • W)) (B.transpose*Y) := by
  simp only [fineTrace, coarseTrace, diagInclude, fromBlocks_transpose,
    transpose_zero, fromBlocks_multiply, Matrix.zero_mul, zero_add, add_zero,
    trace_full_blocks, Matrix.mul_add, Matrix.mul_smul, trace_add, trace_smul]
  ring

/-- Orthogonal complement energy on the two copies, before summing matrix entries. -/
theorem complete_pair_residual (p x w : ℝ) (hp : p+p^2=1) :
    p*x^2 + p^2*w^2 - (p*x+p^2*w)^2 = p^3*(x-w)^2 := by
  linear_combination -(p*x^2+p^2*w^2)*hp

/-- The full matrix-entry conditional expectation; cross blocks stay in its kernel. -/
theorem full_entry_pythagoras (p t x y w u v : ℝ) (hp : p+p^2=1) :
    t*(p*(x^2+y^2+u^2+v^2)+p^2*w^2) -
      t*((p*x+p^2*w)^2+p*y^2) =
      t*(p^3*(x-w)^2+p*(u^2+v^2)) := by
  have h := complete_pair_residual p x w hp
  linear_combination t*h

theorem conditional_adjoint_entry (p t a b x y w : ℝ) :
    t*(p*(a*x+b*y)+p^2*a*w) = t*(a*(p*x+p^2*w)+p*b*y) := by ring

theorem conditional_retraction_entry (p x : ℝ) (hp : p+p^2=1) :
    p*x+p^2*x=x := by linear_combination x*hp

/-- Full block-vector conditional expectation, including both rectangular blocks. -/
def expect (p : ℝ) (X : Matrix I I ℝ) (Y : Matrix J J ℝ)
    (W : Matrix I I ℝ) : Matrix I I ℝ × Matrix J J ℝ := (p • X + p^2 • W, Y)

theorem expect_retraction (p : ℝ) (hp : p+p^2=1)
    (A : Matrix I I ℝ) (B : Matrix J J ℝ) : expect p A B A = (A,B) := by
  apply Prod.ext
  · ext i j
    exact conditional_retraction_entry p (A i j) hp
  · rfl

theorem cross_blocks_not_removed_from_carrier (X : Matrix I I ℝ) (Y : Matrix J J ℝ)
    (U : Matrix I J ℝ) (V : Matrix J I ℝ) :
    (fromBlocks X U V Y).toBlocks₁₂ = U ∧
      (fromBlocks X U V Y).toBlocks₂₁ = V := by simp

def golden (a p : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![a,-p;p,a]
def retained (a p : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![a^2,a*p;a*p,p^2]
def blank : Matrix (Fin 2) (Fin 2) ℝ := !![1,0;0,0]

theorem golden_orthogonal (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    (golden a p).transpose * golden a p = 1 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [golden, Matrix.mul_apply, Fin.sum_univ_two] <;> nlinarith

theorem refined_projection (a p : ℝ) :
    golden a p * blank * (golden a p).transpose = retained a p := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [golden, blank, retained, Matrix.mul_apply, Fin.sum_univ_two] <;> ring

theorem normalized_GNS_column (a p x : ℝ) :
    (golden a p).mulVec ![x,0] = ![a*x,p*x] := by
  ext i
  fin_cases i <;> simp [golden, Matrix.mulVec, dotProduct, Fin.sum_univ_two]

/-- Bind this two-copy block to the actual recorded gate's blank input. -/
theorem recorded_gate_same_column (a p x : ℝ) :
    (D0.Representation.GoldenCoherentMemory.fullStep a p).mulVec ![x,0,0,0]
      = ![a*x,0,0,p*x] := by
  simpa using D0.Representation.GoldenCoherentMemory.blank_record_evolution a p x 0

theorem total_block_dimensions (a b : ℕ) :
    (a+b)^2+a^2 = (a^2+b^2) + (a^2+2*a*b) := by ring

end
end D0.Research.GoldenCostRefinement

#check D0.Research.GoldenCostRefinement.code_length
#check D0.Research.GoldenCostRefinement.code_append
#check D0.Research.GoldenCostRefinement.counts_bind_owner
#check D0.Research.GoldenCostRefinement.mass_one
#check D0.Research.GoldenCostRefinement.owner_trace_normalized
#check D0.Research.GoldenCostRefinement.diagInclude_mul
#check D0.Research.GoldenCostRefinement.diagInclude_transpose
#check D0.Research.GoldenCostRefinement.diagInclude_one
#check D0.Research.GoldenCostRefinement.trace_diagInclude
#check D0.Research.GoldenCostRefinement.trace_full_blocks
#check D0.Research.GoldenCostRefinement.actual_trace_preservation
#check D0.Research.GoldenCostRefinement.actual_gns_isometry
#check D0.Research.GoldenCostRefinement.actual_conditional_adjoint
#check D0.Research.GoldenCostRefinement.complete_pair_residual
#check D0.Research.GoldenCostRefinement.full_entry_pythagoras
#check D0.Research.GoldenCostRefinement.conditional_adjoint_entry
#check D0.Research.GoldenCostRefinement.conditional_retraction_entry
#check D0.Research.GoldenCostRefinement.expect_retraction
#check D0.Research.GoldenCostRefinement.cross_blocks_not_removed_from_carrier
#check D0.Research.GoldenCostRefinement.golden_orthogonal
#check D0.Research.GoldenCostRefinement.refined_projection
#check D0.Research.GoldenCostRefinement.normalized_GNS_column
#check D0.Research.GoldenCostRefinement.recorded_gate_same_column
#check D0.Research.GoldenCostRefinement.total_block_dimensions
#print axioms D0.Research.GoldenCostRefinement.code_length
#print axioms D0.Research.GoldenCostRefinement.code_append
#print axioms D0.Research.GoldenCostRefinement.counts_bind_owner
#print axioms D0.Research.GoldenCostRefinement.mass_one
#print axioms D0.Research.GoldenCostRefinement.owner_trace_normalized
#print axioms D0.Research.GoldenCostRefinement.diagInclude_mul
#print axioms D0.Research.GoldenCostRefinement.diagInclude_transpose
#print axioms D0.Research.GoldenCostRefinement.diagInclude_one
#print axioms D0.Research.GoldenCostRefinement.trace_diagInclude
#print axioms D0.Research.GoldenCostRefinement.trace_full_blocks
#print axioms D0.Research.GoldenCostRefinement.actual_trace_preservation
#print axioms D0.Research.GoldenCostRefinement.actual_gns_isometry
#print axioms D0.Research.GoldenCostRefinement.actual_conditional_adjoint
#print axioms D0.Research.GoldenCostRefinement.complete_pair_residual
#print axioms D0.Research.GoldenCostRefinement.full_entry_pythagoras
#print axioms D0.Research.GoldenCostRefinement.conditional_adjoint_entry
#print axioms D0.Research.GoldenCostRefinement.conditional_retraction_entry
#print axioms D0.Research.GoldenCostRefinement.expect_retraction
#print axioms D0.Research.GoldenCostRefinement.cross_blocks_not_removed_from_carrier
#print axioms D0.Research.GoldenCostRefinement.golden_orthogonal
#print axioms D0.Research.GoldenCostRefinement.refined_projection
#print axioms D0.Research.GoldenCostRefinement.normalized_GNS_column
#print axioms D0.Research.GoldenCostRefinement.recorded_gate_same_column
#print axioms D0.Research.GoldenCostRefinement.total_block_dimensions
