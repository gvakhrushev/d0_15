import D0.Synthesis.TopHodgeKirchhoffStationaryBridge
import Mathlib.Combinatorics.SimpleGraph.LapMatrix
import Mathlib.LinearAlgebra.Matrix.SchurComplement
import Mathlib.Tactic

/-!
# Complete tripartite Laplacian-cofactor bridge

This module closes the operator half of the Matrix--Tree boundary for the
complete tripartite graph.  It constructs the actual `SimpleGraph`
`K(p+1,q+1,r+1)`, deletes one literal vertex from its graph Laplacian, and
computes the determinant of that cofactor.

The result is exactly `topHodgeHighFactor p q r`.

The remaining boundary is deliberately explicit: the current mathlib
dependency has definitions of finite simple graphs and trees, but no
Matrix--Tree theorem equating this cofactor with the cardinality of spanning
tree subgraphs.  Consequently this file does not rename the cofactor as a
tree count.
-/

namespace D0.Synthesis.CompleteTripartiteMatrixTreeBridge

open scoped BigOperators
open Matrix
open D0.Synthesis.TopHodgeKirchhoffStationaryBridge

abbrev Vertex (p q r : ℕ) :=
  Fin (p + 1) ⊕ (Fin (q + 1) ⊕ Fin (r + 1))

abbrev ReducedVertex (p q r : ℕ) :=
  Fin p ⊕ (Fin (q + 1) ⊕ Fin (r + 1))

def zone {p q r : ℕ} : Vertex p q r → Fin 3
  | Sum.inl _ => 0
  | Sum.inr (Sum.inl _) => 1
  | Sum.inr (Sum.inr _) => 2

def reducedZone {p q r : ℕ} : ReducedVertex p q r → Fin 3
  | Sum.inl _ => 0
  | Sum.inr (Sum.inl _) => 1
  | Sum.inr (Sum.inr _) => 2

/-- The actual complete tripartite simple graph. -/
def completeTripartiteGraph (p q r : ℕ) : SimpleGraph (Vertex p q r) :=
  SimpleGraph.comap zone ⊤

@[simp] theorem completeTripartiteGraph_adj
    {p q r : ℕ} (u v : Vertex p q r) :
    (completeTripartiteGraph p q r).Adj u v ↔ zone u ≠ zone v := by
  rfl

instance completeTripartiteGraph_decidableAdj (p q r : ℕ) :
    DecidableRel (completeTripartiteGraph p q r).Adj :=
  fun u v => decidable_of_iff (zone u ≠ zone v)
    (completeTripartiteGraph_adj u v).symm

private def neighborAEquiv {p q r : ℕ} (i : Fin (p + 1)) :
    (completeTripartiteGraph p q r).neighborSet (Sum.inl i) ≃
      (Fin (q + 1) ⊕ Fin (r + 1)) where
  toFun x := by
    rcases x with ⟨j | jk, h⟩
    · exact False.elim ((completeTripartiteGraph_adj _ _).mp h (by rfl))
    · exact jk
  invFun
    | Sum.inl j =>
        ⟨Sum.inr (Sum.inl j), (completeTripartiteGraph_adj _ _).mpr (by
          simp [zone])⟩
    | Sum.inr k =>
        ⟨Sum.inr (Sum.inr k), (completeTripartiteGraph_adj _ _).mpr (by
          simp [zone])⟩
  left_inv x := by
    rcases x with ⟨j | jk, h⟩
    · exact False.elim ((completeTripartiteGraph_adj _ _).mp h (by rfl))
    · rcases jk with j | k <;> rfl
  right_inv x := by rcases x with j | k <;> rfl

private def neighborBEquiv {p q r : ℕ} (j : Fin (q + 1)) :
    (completeTripartiteGraph p q r).neighborSet (Sum.inr (Sum.inl j)) ≃
      (Fin (p + 1) ⊕ Fin (r + 1)) where
  toFun x := by
    rcases x with ⟨i | jk, h⟩
    · exact Sum.inl i
    · rcases jk with j' | k
      · exact False.elim ((completeTripartiteGraph_adj _ _).mp h (by rfl))
      · exact Sum.inr k
  invFun
    | Sum.inl i =>
        ⟨Sum.inl i, (completeTripartiteGraph_adj _ _).mpr (by simp [zone])⟩
    | Sum.inr k =>
        ⟨Sum.inr (Sum.inr k), (completeTripartiteGraph_adj _ _).mpr (by
          simp [zone])⟩
  left_inv x := by
    rcases x with ⟨i | jk, h⟩
    · rfl
    · rcases jk with j' | k
      · exact False.elim ((completeTripartiteGraph_adj _ _).mp h (by rfl))
      · rfl
  right_inv x := by rcases x with i | k <;> rfl

private def neighborCEquiv {p q r : ℕ} (k : Fin (r + 1)) :
    (completeTripartiteGraph p q r).neighborSet (Sum.inr (Sum.inr k)) ≃
      (Fin (p + 1) ⊕ Fin (q + 1)) where
  toFun x := by
    rcases x with ⟨i | jk, h⟩
    · exact Sum.inl i
    · rcases jk with j | k'
      · exact Sum.inr j
      · exact False.elim ((completeTripartiteGraph_adj _ _).mp h (by rfl))
  invFun
    | Sum.inl i =>
        ⟨Sum.inl i, (completeTripartiteGraph_adj _ _).mpr (by simp [zone])⟩
    | Sum.inr j =>
        ⟨Sum.inr (Sum.inl j), (completeTripartiteGraph_adj _ _).mpr (by
          simp [zone])⟩
  left_inv x := by
    rcases x with ⟨i | jk, h⟩
    · rfl
    · rcases jk with j | k'
      · rfl
      · exact False.elim ((completeTripartiteGraph_adj _ _).mp h (by rfl))
  right_inv x := by rcases x with i | j <;> rfl

theorem degree_zoneA {p q r : ℕ} (i : Fin (p + 1)) :
    (completeTripartiteGraph p q r).degree (Sum.inl i) = degreeA q r := by
  classical
  rw [← SimpleGraph.card_neighborSet_eq_degree]
  calc
    _ = Fintype.card (Fin (q + 1) ⊕ Fin (r + 1)) :=
      Fintype.card_congr
        (neighborAEquiv (p := p) (q := q) (r := r) i)
    _ = degreeA q r := by simp [degreeA]; omega

theorem degree_zoneB {p q r : ℕ} (j : Fin (q + 1)) :
    (completeTripartiteGraph p q r).degree (Sum.inr (Sum.inl j)) =
      degreeB p r := by
  classical
  rw [← SimpleGraph.card_neighborSet_eq_degree]
  calc
    _ = Fintype.card (Fin (p + 1) ⊕ Fin (r + 1)) :=
      Fintype.card_congr
        (neighborBEquiv (p := p) (q := q) (r := r) j)
    _ = degreeB p r := by simp [degreeB]; omega

theorem degree_zoneC {p q r : ℕ} (k : Fin (r + 1)) :
    (completeTripartiteGraph p q r).degree (Sum.inr (Sum.inr k)) =
      degreeC p q := by
  classical
  rw [← SimpleGraph.card_neighborSet_eq_degree]
  calc
    _ = Fintype.card (Fin (p + 1) ⊕ Fin (q + 1)) :=
      Fintype.card_congr
        (neighborCEquiv (p := p) (q := q) (r := r) k)
    _ = degreeC p q := by simp [degreeC]; omega

/-- Inclusion of all vertices except the distinguished first vertex of zone A. -/
def reducedVertexEmbedding (p q r : ℕ) :
    ReducedVertex p q r ↪ Vertex p q r where
  toFun
    | Sum.inl i => Sum.inl i.succ
    | Sum.inr (Sum.inl j) => Sum.inr (Sum.inl j)
    | Sum.inr (Sum.inr k) => Sum.inr (Sum.inr k)
  inj' := by
    intro u v h
    rcases u with i | jk
    · rcases v with i' | jk'
      · simp only [Sum.inl.injEq, Fin.succ_inj] at h
        exact congrArg Sum.inl h
      · rcases jk' with j' | k' <;> simp at h
    · rcases jk with j | k
      · rcases v with i' | jk'
        · simp at h
        · rcases jk' with j' | k'
          · simp only [Sum.inr.injEq, Sum.inl.injEq] at h
            exact congrArg (fun x => Sum.inr (Sum.inl x)) h
          · simp at h
      · rcases v with i' | jk'
        · simp at h
        · rcases jk' with j' | k'
          · simp at h
          · simp only [Sum.inr.injEq] at h
            exact congrArg (fun x => Sum.inr (Sum.inr x)) h

@[simp] theorem zone_reducedVertexEmbedding
    {p q r : ℕ} (v : ReducedVertex p q r) :
    zone (reducedVertexEmbedding p q r v) = reducedZone v := by
  rcases v with i | jk
  · rfl
  · rcases jk with j | k <;> rfl

def reducedDegree (p q r : ℕ) : ReducedVertex p q r → ℚ
  | Sum.inl _ => degreeA q r
  | Sum.inr (Sum.inl _) => degreeB p r
  | Sum.inr (Sum.inr _) => degreeC p q

/-- Explicit reduced graph Laplacian. -/
def explicitReducedLaplacian (p q r : ℕ) :
    Matrix (ReducedVertex p q r) (ReducedVertex p q r) ℚ :=
  fun u v =>
    if u = v then reducedDegree p q r u
    else if reducedZone u ≠ reducedZone v then -1 else 0

/-- The actual graph-Laplacian cofactor obtained by deleting the first
zone-A vertex. -/
noncomputable def graphLaplacianCofactor (p q r : ℕ) :
    Matrix (ReducedVertex p q r) (ReducedVertex p q r) ℚ := by
  classical
  exact ((completeTripartiteGraph p q r).lapMatrix ℚ).submatrix
    (reducedVertexEmbedding p q r) (reducedVertexEmbedding p q r)

theorem graphLaplacianCofactor_eq_explicit (p q r : ℕ) :
    graphLaplacianCofactor p q r = explicitReducedLaplacian p q r := by
  classical
  ext u v
  rcases u with i | jk
  · rcases v with i' | jk'
    · simp [graphLaplacianCofactor, explicitReducedLaplacian,
        reducedVertexEmbedding, reducedZone, zone,
        SimpleGraph.lapMatrix, SimpleGraph.degMatrix,
        SimpleGraph.adjMatrix]
      by_cases h : i = i'
      · subst i'
        rw [Matrix.diagonal_apply_eq,
          degree_zoneA (p := p) (q := q) (r := r)]
        simp [reducedDegree]
      · rw [Matrix.diagonal_apply_ne _ (by simpa using h)]
        simp [h]
    · rcases jk' with j' | k' <;>
        simp [graphLaplacianCofactor, explicitReducedLaplacian,
          reducedVertexEmbedding, reducedZone, zone,
          SimpleGraph.lapMatrix, SimpleGraph.degMatrix,
          SimpleGraph.adjMatrix]
  · rcases jk with j | k
    · rcases v with i' | jk'
      · simp [graphLaplacianCofactor, explicitReducedLaplacian,
          reducedVertexEmbedding, reducedZone, zone,
          SimpleGraph.lapMatrix, SimpleGraph.degMatrix,
          SimpleGraph.adjMatrix]
      · rcases jk' with j' | k' <;>
          simp [graphLaplacianCofactor, explicitReducedLaplacian,
            reducedVertexEmbedding, reducedZone, zone,
            SimpleGraph.lapMatrix, SimpleGraph.degMatrix,
            SimpleGraph.adjMatrix]
        by_cases h : j = j'
        · subst j'
          rw [Matrix.diagonal_apply_eq,
            degree_zoneB (p := p) (q := q) (r := r)]
          simp [reducedDegree]
        · rw [Matrix.diagonal_apply_ne _ (by simpa using h)]
          simp [h]
    · rcases v with i' | jk'
      · simp [graphLaplacianCofactor, explicitReducedLaplacian,
          reducedVertexEmbedding, reducedZone, zone,
          SimpleGraph.lapMatrix, SimpleGraph.degMatrix,
          SimpleGraph.adjMatrix]
      · rcases jk' with j' | k' <;>
          simp [graphLaplacianCofactor, explicitReducedLaplacian,
            reducedVertexEmbedding, reducedZone, zone,
            SimpleGraph.lapMatrix, SimpleGraph.degMatrix,
            SimpleGraph.adjMatrix]
        by_cases h : k = k'
        · subst k'
          rw [Matrix.diagonal_apply_eq,
            degree_zoneC (p := p) (q := q) (r := r)]
          simp [reducedDegree]
        · rw [Matrix.diagonal_apply_ne _ (by simpa using h)]
          simp [h]

/-! ## Rank-three determinant reduction -/

def reducedDegreeDiagonal (p q r : ℕ) :
    Matrix (ReducedVertex p q r) (ReducedVertex p q r) ℚ :=
  Matrix.diagonal (reducedDegree p q r)

def reducedDegreeInverse (p q r : ℕ) :
    Matrix (ReducedVertex p q r) (ReducedVertex p q r) ℚ :=
  Matrix.diagonal fun v => (reducedDegree p q r v)⁻¹

def zoneIndicator (p q r : ℕ) :
    Matrix (ReducedVertex p q r) (Fin 3) ℚ :=
  fun v z => if reducedZone v = z then 1 else 0

def zoneInteraction : Matrix (Fin 3) (Fin 3) ℚ :=
  fun z w => if z = w then 0 else 1

theorem reducedDegree_ne_zero (p q r : ℕ) (v : ReducedVertex p q r) :
    reducedDegree p q r v ≠ 0 := by
  rcases v with i | jk
  · simp only [reducedDegree, degreeA, Nat.cast_add, Nat.cast_ofNat]
    positivity
  · rcases jk with j | k
    · simp only [reducedDegree, degreeB, Nat.cast_add, Nat.cast_ofNat]
      positivity
    · simp only [reducedDegree, degreeC, Nat.cast_add, Nat.cast_ofNat]
      positivity

theorem reducedDegreeDiagonal_mul_inverse (p q r : ℕ) :
    reducedDegreeDiagonal p q r * reducedDegreeInverse p q r = 1 := by
  ext u v
  by_cases h : u = v
  · subst v
    simp [reducedDegreeDiagonal, reducedDegreeInverse,
      reducedDegree_ne_zero]
  · simp [reducedDegreeDiagonal, reducedDegreeInverse, h]

theorem explicitReducedLaplacian_lowRank (p q r : ℕ) :
    explicitReducedLaplacian p q r =
      reducedDegreeDiagonal p q r -
        zoneIndicator p q r * zoneInteraction *
          (zoneIndicator p q r)ᵀ := by
  ext u v
  rcases u with i | jk
  · rcases v with i' | jk'
    · simp [explicitReducedLaplacian, reducedDegreeDiagonal,
        reducedZone, zoneIndicator, zoneInteraction,
        Matrix.mul_apply, Fin.sum_univ_succ]
      by_cases h : i = i'
      · subst i'
        rw [Matrix.diagonal_apply_eq]
        simp [reducedDegree]
      · rw [Matrix.diagonal_apply_ne _ (by simpa using h)]
        simp [h]
    · rcases jk' with j' | k' <;>
        simp [explicitReducedLaplacian, reducedDegreeDiagonal,
          reducedZone, zoneIndicator, zoneInteraction,
          Matrix.mul_apply, Fin.sum_univ_succ]
  · rcases jk with j | k
    · rcases v with i' | jk'
      · simp [explicitReducedLaplacian, reducedDegreeDiagonal,
          reducedZone, zoneIndicator, zoneInteraction,
          Matrix.mul_apply, Fin.sum_univ_succ]
      · rcases jk' with j' | k' <;>
          simp [explicitReducedLaplacian, reducedDegreeDiagonal,
            reducedZone, zoneIndicator, zoneInteraction,
            Matrix.mul_apply, Fin.sum_univ_succ]
        by_cases h : j = j'
        · subst j'
          rw [Matrix.diagonal_apply_eq]
          simp [reducedDegree]
        · rw [Matrix.diagonal_apply_ne _ (by simpa using h)]
          simp [h]
    · rcases v with i' | jk'
      · simp [explicitReducedLaplacian, reducedDegreeDiagonal,
          reducedZone, zoneIndicator, zoneInteraction,
          Matrix.mul_apply, Fin.sum_univ_succ]
      · rcases jk' with j' | k' <;>
          simp [explicitReducedLaplacian, reducedDegreeDiagonal,
            reducedZone, zoneIndicator, zoneInteraction,
            Matrix.mul_apply, Fin.sum_univ_succ]
        by_cases h : k = k'
        · subst k'
          rw [Matrix.diagonal_apply_eq]
          simp [reducedDegree]
        · rw [Matrix.diagonal_apply_ne _ (by simpa using h)]
          simp [h]

theorem explicitReducedLaplacian_factorization (p q r : ℕ) :
    explicitReducedLaplacian p q r =
      reducedDegreeDiagonal p q r *
        (1 -
          (reducedDegreeInverse p q r * zoneIndicator p q r *
            zoneInteraction) * (zoneIndicator p q r)ᵀ) := by
  rw [explicitReducedLaplacian_lowRank]
  rw [Matrix.mul_sub, Matrix.mul_one]
  have hmul :
      reducedDegreeDiagonal p q r *
          (reducedDegreeInverse p q r * zoneIndicator p q r *
            zoneInteraction * (zoneIndicator p q r)ᵀ) =
        zoneIndicator p q r * zoneInteraction *
          (zoneIndicator p q r)ᵀ := by
    calc
      _ = (((reducedDegreeDiagonal p q r *
              reducedDegreeInverse p q r) *
                zoneIndicator p q r) * zoneInteraction) *
                  (zoneIndicator p q r)ᵀ := by
            simp only [Matrix.mul_assoc]
      _ = _ := by
        rw [reducedDegreeDiagonal_mul_inverse]
        simp
  rw [hmul]

/-- The `3 × 3` matrix left after eliminating all within-zone directions. -/
def compressedCofactorMatrix (p q r : ℕ) : Matrix (Fin 3) (Fin 3) ℚ :=
  !![1, -(p : ℚ) / degreeA q r, -(p : ℚ) / degreeA q r;
     -(q + 1 : ℕ) / degreeB p r, 1, -(q + 1 : ℕ) / degreeB p r;
     -(r + 1 : ℕ) / degreeC p q, -(r + 1 : ℕ) / degreeC p q, 1]

def zoneMassMatrix (p q r : ℕ) : Matrix (Fin 3) (Fin 3) ℚ :=
  !![(p : ℚ) / degreeA q r, 0, 0;
     0, (q + 1 : ℕ) / degreeB p r, 0;
     0, 0, (r + 1 : ℕ) / degreeC p q]

theorem zoneMassMatrix_owner (p q r : ℕ) :
    (zoneIndicator p q r)ᵀ * reducedDegreeInverse p q r *
        zoneIndicator p q r =
      zoneMassMatrix p q r := by
  ext i j
  rw [Matrix.mul_apply]
  simp_rw [reducedDegreeInverse, Matrix.mul_diagonal]
  fin_cases i <;> fin_cases j <;>
    simp [zoneMassMatrix, zoneIndicator,
      reducedDegree, reducedZone, degreeA, degreeB, degreeC,
      Fintype.sum_sum_type] <;>
    field_simp

theorem compressedCofactorMatrix_owner (p q r : ℕ) :
    1 - (zoneIndicator p q r)ᵀ *
        (reducedDegreeInverse p q r * zoneIndicator p q r *
          zoneInteraction) =
      compressedCofactorMatrix p q r := by
  rw [← Matrix.mul_assoc, ← Matrix.mul_assoc, zoneMassMatrix_owner]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [compressedCofactorMatrix, zoneMassMatrix, zoneInteraction,
      Matrix.vecMul, dotProduct, Fin.sum_univ_succ] <;>
    ring

theorem compressedCofactorMatrix_det (p q r : ℕ) :
    (compressedCofactorMatrix p q r).det =
      (totalVertices p q r : ℚ) /
        ((degreeB p r : ℚ) * (degreeC p q : ℚ)) := by
  simp [compressedCofactorMatrix, Matrix.det_fin_three,
    totalVertices, degreeA, degreeB, degreeC]
  field_simp
  ring

theorem reducedDegreeDiagonal_det (p q r : ℕ) :
    (reducedDegreeDiagonal p q r).det =
      (degreeA q r : ℚ) ^ p *
        (degreeB p r : ℚ) ^ (q + 1) *
          (degreeC p q : ℚ) ^ (r + 1) := by
  rw [reducedDegreeDiagonal, Matrix.det_diagonal]
  simp [reducedDegree, Fintype.prod_sum_type]
  ring

/-- Determinant of the actual reduced graph Laplacian.  This is the full
operator-side statement needed by Matrix--Tree. -/
theorem graphLaplacianCofactor_det (p q r : ℕ) :
    (graphLaplacianCofactor p q r).det =
      (topHodgeHighFactor p q r : ℚ) := by
  rw [graphLaplacianCofactor_eq_explicit,
    explicitReducedLaplacian_factorization, Matrix.det_mul,
    Matrix.det_one_sub_mul_comm,
    compressedCofactorMatrix_owner,
    compressedCofactorMatrix_det,
    reducedDegreeDiagonal_det]
  simp only [topHodgeHighFactor, totalVertices, degreeA, degreeB, degreeC,
    Nat.cast_mul, Nat.cast_pow]
  field_simp
  simp [pow_succ]
  ring

/-- The high sector of the actual top-Hodge pseudodeterminant is exactly the
determinant of an actual graph-Laplacian cofactor.  No spanning-tree
interpretation is used in this theorem. -/
theorem topHodge_graphLaplacianCofactor_bridge (p q r : ℕ) :
    topHodgePositivePseudoDet p q r =
      (topHodgeLowFactor p q r : ℚ) *
        (graphLaplacianCofactor p q r).det := by
  rw [topHodgePositivePseudoDet_formula, graphLaplacianCofactor_det]
  push_cast
  ring

end D0.Synthesis.CompleteTripartiteMatrixTreeBridge
