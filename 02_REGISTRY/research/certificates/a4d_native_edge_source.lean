import D0.Geometry.ArchiveStressEdgeReadout
import D0.Geometry.ArchiveVariation
import D0.Geometry.ArchiveVariationDual

namespace D0.Research.NativeEdgeRiesz
open D0 D0.Geometry
open D0.Geometry.ArchiveRolePhaseProductCarrier
open scoped BigOperators
noncomputable section
variable {I : Type} [Fintype I] [DecidableEq I]

def spike (i : I) (a : I) : ℝ := if a=i then 1 else 0

def edgeMatrix (i j : I) : Matrix I I ℝ :=
  fun a b => (spike i a-spike j a)*(spike i b-spike j b)

omit [Fintype I] in
theorem edgeMatrix_symmetric (i j : I) : MatrixSymmetric (edgeMatrix i j) := by
  intro a b
  simp only [edgeMatrix]
  ring

 theorem edgeMatrix_row_zero (i j a : I) : (∑ b, edgeMatrix i j a b)=0 := by
  simp only [edgeMatrix,← Finset.mul_sum,Finset.sum_sub_distrib]
  simp [spike]

 theorem pairing_edge (T : Matrix I I ℝ) (i j : I) :
    matrixInnerProduct T (edgeMatrix i j)=T i i+T j j-T i j-T j i := by
  unfold matrixInnerProduct edgeMatrix
  simp_rw [mul_sub,sub_mul,mul_sub,Finset.sum_sub_distrib]
  simp [spike]
  ring

 theorem pairing_edge_symmetric (T : Matrix I I ℝ) (hT : MatrixSymmetric T) (i j : I) :
    matrixInnerProduct T (edgeMatrix i j)=T i i+T j j-2*T i j := by
  rw [pairing_edge,hT j i]
  ring

omit [Fintype I] in
theorem edgeMatrix_off_diagonal (i j a b : I) (hab : a≠b)
    (h1 : ¬(a=i ∧ b=j)) (h2 : ¬(a=j ∧ b=i)) : edgeMatrix i j a b=0 := by
  unfold edgeMatrix spike
  split_ifs <;> simp_all

 theorem role_edge_local (n : ℕ) (i j : ArchiveRolePhasePoint n)
    (hij : rolePhaseAdjacent n i j) : LocalLaplacianPredicates n (edgeMatrix i j) := by
  refine ⟨edgeMatrix_symmetric i j,edgeMatrix_row_zero i j,?_⟩
  intro a b hab hnot
  apply edgeMatrix_off_diagonal i j a b hab
  · rintro ⟨rfl,rfl⟩
    exact hnot hij
  · rintro ⟨rfl,rfl⟩
    exact hnot (rolePhaseAdjacent_symmetric n hij)

 theorem actual_readout_on_edge (n : ℕ) (T : Matrix (ArchiveRolePhasePoint n) (ArchiveRolePhasePoint n) ℝ)
    (hT : MatrixSymmetric T) (i j : ArchiveRolePhasePoint n) :
    edgeStressReadout (ArchivePhaseEdgeMetricScale.archiveMetricLaplacianScale n)
      (T i i) (T j j) (T i j) =
      ArchivePhaseEdgeMetricScale.archiveMetricLaplacianScale n *
        matrixInnerProduct T (edgeMatrix i j) := by
  rw [pairing_edge_symmetric T hT]
  rfl

omit [DecidableEq I] in
theorem diagonal_potential_pairing_zero (v : I → ℝ) (D : Matrix I I ℝ)
    (hD : MatrixSymmetric D) (hr : ∀ i, ∑ j, D i j=0) :
    matrixInnerProduct (fun i j => (v i+v j)/2) D=0 := by
  have h1 : (∑ i, ∑ j, v i*D i j)=0 := by
    simp_rw [← Finset.mul_sum,hr,mul_zero]
    simp
  have h2 : (∑ i, ∑ j, v j*D i j)=0 := by
    rw [symmetric_matrix_sum_comm (fun i _ => v i) D hD]
    exact h1
  change (∑ i, ∑ j, ((v i+v j)/2)*D i j)=0
  have hterm : ∀ i j, ((v i+v j)/2)*D i j=(v i*D i j+v j*D i j)/2 := by
    intros; ring
  simp only [hterm,← Finset.sum_div,Finset.sum_add_distrib,h1,h2,add_zero,zero_div]

 theorem actual_local_annihilator_iff_edges (n : ℕ)
    (T : Matrix (ArchiveRolePhasePoint n) (ArchiveRolePhasePoint n) ℝ)
    (hT : MatrixSymmetric T) :
    (∀ D : LocalLaplacianVariation n, matrixInnerProduct T D.1=0) ↔
    ∀ i j, rolePhaseAdjacent n i j →
      edgeStressReadout (ArchivePhaseEdgeMetricScale.archiveMetricLaplacianScale n)
        (T i i) (T j j) (T i j)=0 := by
  constructor
  · intro h i j hij
    rw [actual_readout_on_edge n T hT]
    have he := h ⟨edgeMatrix i j,role_edge_local n i j hij⟩
    change matrixInnerProduct T (edgeMatrix i j)=0 at he
    rw [he,mul_zero]
  · intro h D
    have hp : matrixInnerProduct T D.1=
        matrixInnerProduct (fun i j => (T i i+T j j)/2) D.1 := by
      unfold matrixInnerProduct
      apply Finset.sum_congr rfl
      intro i _
      apply Finset.sum_congr rfl
      intro j _
      by_cases heq : i=j
      · subst j; ring
      · by_cases hadj : rolePhaseAdjacent n i j
        · have hh := h i j hadj
          unfold edgeStressReadout at hh
          have hz := (mul_eq_zero.mp hh).resolve_left (archiveMetricLaplacianScale_ne_zero n)
          have hentry : T i j=(T i i+T j j)/2 := by linarith
          rw [hentry]
        · rw [D.2.2.2 i j heq hadj]
          ring
    rw [hp]
    exact diagonal_potential_pairing_zero (fun i => T i i) D.1 D.2.1 D.2.2.1

 theorem actual_local_sources_equivalent_iff (n : ℕ)
    (T U : Matrix (ArchiveRolePhasePoint n) (ArchiveRolePhasePoint n) ℝ)
    (hT : MatrixSymmetric T) (hU : MatrixSymmetric U) :
    (∀ D : LocalLaplacianVariation n, matrixInnerProduct T D.1=matrixInnerProduct U D.1) ↔
    ∀ i j, rolePhaseAdjacent n i j →
      edgeStressReadout (ArchivePhaseEdgeMetricScale.archiveMetricLaplacianScale n)
        (T i i) (T j j) (T i j)=
      edgeStressReadout (ArchivePhaseEdgeMetricScale.archiveMetricLaplacianScale n)
        (U i i) (U j j) (U i j) := by
  have hs : MatrixSymmetric (T-U) := by
    intro i j; simp only [Matrix.sub_apply,hT i j,hU i j]
  have hp (D : Matrix (ArchiveRolePhasePoint n) (ArchiveRolePhasePoint n) ℝ) :
      matrixInnerProduct (T-U) D=matrixInnerProduct T D-matrixInnerProduct U D := by
    simp only [matrixInnerProduct,Matrix.sub_apply,sub_mul,Finset.sum_sub_distrib]
  have hr (i j : ArchiveRolePhasePoint n) :
      edgeStressReadout (ArchivePhaseEdgeMetricScale.archiveMetricLaplacianScale n)
        ((T-U) i i) ((T-U) j j) ((T-U) i j)=
      edgeStressReadout (ArchivePhaseEdgeMetricScale.archiveMetricLaplacianScale n)
        (T i i) (T j j) (T i j)-
      edgeStressReadout (ArchivePhaseEdgeMetricScale.archiveMetricLaplacianScale n)
        (U i i) (U j j) (U i j) := by
    unfold edgeStressReadout
    simp only [Matrix.sub_apply]
    ring
  simpa only [hp,hr,sub_eq_zero] using actual_local_annihilator_iff_edges n (T-U) hs

end
end D0.Research.NativeEdgeRiesz

#print axioms D0.Research.NativeEdgeRiesz.edgeMatrix_symmetric
#print axioms D0.Research.NativeEdgeRiesz.edgeMatrix_row_zero
#print axioms D0.Research.NativeEdgeRiesz.pairing_edge
#print axioms D0.Research.NativeEdgeRiesz.pairing_edge_symmetric
#print axioms D0.Research.NativeEdgeRiesz.edgeMatrix_off_diagonal
#print axioms D0.Research.NativeEdgeRiesz.role_edge_local
#print axioms D0.Research.NativeEdgeRiesz.actual_readout_on_edge
#print axioms D0.Research.NativeEdgeRiesz.diagonal_potential_pairing_zero
#print axioms D0.Research.NativeEdgeRiesz.actual_local_annihilator_iff_edges
#print axioms D0.Research.NativeEdgeRiesz.actual_local_sources_equivalent_iff
#print axioms D0.Geometry.archive_local_laplacian_variation_isomorphism_owner

#check D0.Research.NativeEdgeRiesz.role_edge_local
#check D0.Research.NativeEdgeRiesz.actual_local_annihilator_iff_edges
#check D0.Research.NativeEdgeRiesz.actual_local_sources_equivalent_iff
