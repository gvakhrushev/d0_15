import Mathlib.Data.Matrix.Basic
import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Algebra.BigOperators.Fin
import D0.Core.FiniteTypes
import D0.Core.DyadABCD
import D0.Geometry.ArchiveProductLaplacian
import D0.Geometry.ArchivePhaseEdgeMetricScale
import D0.Geometry.ArchiveRolePhaseProductCarrier

open scoped BigOperators

namespace D0.Geometry

open D0
open ArchiveRolePhaseProductCarrier
open ArchivePhaseEdgeMetricScale

/-!
# D0.Geometry.ArchiveLocalLaplacianVariation

Owner: `D0-ARCHIVE-LOCAL-LAPLACIAN-VARIATION-ISOMORPHISM-001`.

This file gives the literal finite algebra behind the archive local Laplacian
variation claim.  An edge is an element of the `SimpleGraph.edgeSet` of the
role/product nearest-neighbour graph, so the edge carrier is genuinely
undirected.  The forward map puts an edge conductance on the two off-diagonal
entries and chooses the diagonal by the row-sum constraint.  The inverse reads
the conductance from either orientation of an edge.

No curvature, continuum, Bianchi, or gravitational interpretation is used here.
-/

/-- The existing role/product nearest-neighbour relation on the 4D carrier. -/
def rolePhaseAdjacent (n : ℕ) (x y : ArchiveRolePhasePoint n) : Prop :=
  ∃ r : Role,
    (∀ r' : Role, r' ≠ r → x r' = y r') ∧
      archiveAdjacent n (x r) (y r)

theorem rolePhaseAdjacent_symmetric (n : ℕ) :
    Symmetric (rolePhaseAdjacent n) := by
  intro x y h
  rcases h with ⟨r, h_match, h_adj⟩
  refine ⟨r, ?_, archiveAdjacent_symmetric n h_adj⟩
  intro r' hr'
  exact (h_match r' hr').symm

theorem rolePhaseAdjacent_irreflexive (n : ℕ) :
    ∀ x, ¬ rolePhaseAdjacent n x x := by
  intro x h
  rcases h with ⟨r, _, h_adj⟩
  exact archiveAdjacent_irreflexive n (x r) h_adj

noncomputable instance rolePhaseAdjacent_decidable (n : ℕ) :
    DecidableRel (rolePhaseAdjacent n) := by
  intro x y
  classical
  exact Classical.propDecidable (rolePhaseAdjacent n x y)

/-- The undirected nearest-neighbour graph on `ArchiveRolePhasePoint n`. -/
noncomputable def rolePhaseGraph (n : ℕ) : SimpleGraph (ArchiveRolePhasePoint n) where
  Adj := rolePhaseAdjacent n
  symm := rolePhaseAdjacent_symmetric n
  loopless := ⟨rolePhaseAdjacent_irreflexive n⟩

/-- The typed quotient of undirected nearest-neighbour edges. -/
abbrev ArchiveNearestNeighborEdge (n : ℕ) := (rolePhaseGraph n).edgeSet

/-- Conductance variations, one real coordinate per undirected edge. -/
abbrev EdgeConductanceVariation (n : ℕ) := ArchiveNearestNeighborEdge n → ℝ

/-- The matrix predicate owned by the local Laplacian variation space. -/
abbrev LocalLaplacianPredicates (n : ℕ)
    (dL : Matrix (ArchiveRolePhasePoint n) (ArchiveRolePhasePoint n) ℝ) : Prop :=
  MatrixSymmetric dL ∧
    (∀ x : ArchiveRolePhasePoint n,
      (∑ y : ArchiveRolePhasePoint n, dL x y) = 0) ∧
    (∀ x y : ArchiveRolePhasePoint n, x ≠ y → ¬ rolePhaseAdjacent n x y → dL x y = 0)

/-- The declared finite local Laplacian variation subspace. -/
def LocalLaplacianVariation (n : ℕ) :
    Submodule ℝ (Matrix (ArchiveRolePhasePoint n) (ArchiveRolePhasePoint n) ℝ) :=
  { carrier := {dL | LocalLaplacianPredicates n dL}
    zero_mem' := by
      change LocalLaplacianPredicates n 0
      refine ⟨?_, ?_, ?_⟩
      · intro x y
        simp
      · intro x
        simp
      · intro x y _ _
        simp
    add_mem' := by
      intro dL₁ dL₂ h₁ h₂
      change LocalLaplacianPredicates n (dL₁ + dL₂)
      change LocalLaplacianPredicates n dL₁ at h₁
      change LocalLaplacianPredicates n dL₂ at h₂
      refine ⟨?_, ?_, ?_⟩
      · intro x y
        simp [h₁.1 x y, h₂.1 x y]
      · intro x
        simp [h₁.2.1 x, h₂.2.1 x, Finset.sum_add_distrib]
      · intro x y hxy h_adj
        simp [h₁.2.2 x y hxy h_adj, h₂.2.2 x y hxy h_adj]
    smul_mem' := by
      intro c dL h
      change LocalLaplacianPredicates n (c • dL)
      change LocalLaplacianPredicates n dL at h
      refine ⟨?_, ?_, ?_⟩
      · intro x y
        simp [h.1 x y]
      · intro x
        change (∑ y : ArchiveRolePhasePoint n, c * dL x y) = 0
        rw [← Finset.mul_sum, h.2.1 x, mul_zero]
      · intro x y hxy h_adj
        simp [h.2.2 x y hxy h_adj] }

theorem archiveMetricLaplacianScale_ne_zero (n : ℕ) :
    archiveMetricLaplacianScale n ≠ 0 := by
  exact ne_of_gt (archive_phase_edge_metric_scale_owner.2.2 n)

/-- The edge subtype attached to an adjacent ordered pair. -/
def adjacentEdge {n : ℕ} {x y : ArchiveRolePhasePoint n}
    (h : rolePhaseAdjacent n x y) : ArchiveNearestNeighborEdge n :=
  ⟨s(x, y), h⟩

/-- The off-diagonal entry contributed by a conductance variation. -/
noncomputable def offDiagonalEntry (n : ℕ)
    (dw : EdgeConductanceVariation n)
    (x y : ArchiveRolePhasePoint n) : ℝ :=
  if h : rolePhaseAdjacent n x y then
    -archiveMetricLaplacianScale n * dw (adjacentEdge h)
  else
    0

theorem offDiagonalEntry_self (n : ℕ) (dw : EdgeConductanceVariation n)
    (x : ArchiveRolePhasePoint n) : offDiagonalEntry n dw x x = 0 := by
  classical
  simp [offDiagonalEntry, rolePhaseAdjacent_irreflexive n x]

theorem offDiagonalEntry_symmetric (n : ℕ) (dw : EdgeConductanceVariation n)
    (x y : ArchiveRolePhasePoint n) :
    offDiagonalEntry n dw x y = offDiagonalEntry n dw y x := by
  classical
  by_cases h : rolePhaseAdjacent n x y
  · have h' : rolePhaseAdjacent n y x := rolePhaseAdjacent_symmetric n h
    simp only [offDiagonalEntry, dif_pos h, dif_pos h']
    congr 2
    apply Subtype.ext
    exact Sym2.eq_swap
  · have h' : ¬ rolePhaseAdjacent n y x := by
      intro hyx
      exact h (rolePhaseAdjacent_symmetric n hyx)
    simp [offDiagonalEntry, h, h']

theorem offDiagonalEntry_add (n : ℕ) (dw₁ dw₂ : EdgeConductanceVariation n)
    (x y : ArchiveRolePhasePoint n) :
    offDiagonalEntry n (dw₁ + dw₂) x y =
      offDiagonalEntry n dw₁ x y + offDiagonalEntry n dw₂ x y := by
  classical
  by_cases h : rolePhaseAdjacent n x y
  · simp [offDiagonalEntry, h]
    ring
  · simp [offDiagonalEntry, h]

theorem offDiagonalEntry_smul (n : ℕ) (c : ℝ) (dw : EdgeConductanceVariation n)
    (x y : ArchiveRolePhasePoint n) :
    offDiagonalEntry n (c • dw) x y = c * offDiagonalEntry n dw x y := by
  classical
  by_cases h : rolePhaseAdjacent n x y
  · simp [offDiagonalEntry, h, smul_eq_mul]
    ring
  · simp [offDiagonalEntry, h]

/-- The forward matrix: off-diagonal conductance entries and compensating diagonal. -/
noncomputable def forwardMatrix (n : ℕ)
    (dw : EdgeConductanceVariation n) :
    Matrix (ArchiveRolePhasePoint n) (ArchiveRolePhasePoint n) ℝ :=
  fun x y =>
    if x = y then
      -∑ z : ArchiveRolePhasePoint n, offDiagonalEntry n dw x z
    else
      offDiagonalEntry n dw x y

theorem forwardMatrix_row_sum_zero (n : ℕ) (dw : EdgeConductanceVariation n)
    (x : ArchiveRolePhasePoint n) :
    (∑ y, forwardMatrix n dw x y) = 0 := by
  classical
  let f : ArchiveRolePhasePoint n → ℝ := fun y => offDiagonalEntry n dw x y
  let s : ℝ := ∑ y, f y
  have h_split := Finset.sum_erase_add (Finset.univ : Finset (ArchiveRolePhasePoint n))
    (fun y => if x = y then -s else f y) (Finset.mem_univ x)
  have h_erase :
      (∑ y ∈ Finset.univ.erase x, (if x = y then -s else f y)) =
        ∑ y ∈ Finset.univ.erase x, f y := by
    apply Finset.sum_congr rfl
    intro y hy
    simp only [if_neg (Ne.symm (Finset.ne_of_mem_erase hy))]
  have h_f_split := Finset.sum_erase_add (Finset.univ : Finset (ArchiveRolePhasePoint n))
    f (Finset.mem_univ x)
  have h_fx : f x = 0 := by
    simpa [f] using offDiagonalEntry_self n dw x
  change (∑ y : ArchiveRolePhasePoint n, if x = y then -s else f y) = 0
  have h_erase_f : (∑ y ∈ Finset.univ.erase x, f y) = s := by
    change (∑ y ∈ Finset.univ.erase x, f y) = ∑ y, f y
    rw [← h_f_split, h_fx, add_zero]
  rw [← h_split, h_erase]
  have h_diag : (fun y => if x = y then -s else f y) x = -s := by simp
  rw [h_diag, h_erase_f]
  simp

theorem forwardMatrix_symmetric (n : ℕ) (dw : EdgeConductanceVariation n) :
    MatrixSymmetric (forwardMatrix n dw) := by
  intro x y
  classical
  by_cases hxy : x = y
  · subst y
    rfl
  · simp only [forwardMatrix, if_neg hxy, if_neg (Ne.symm hxy)]
    exact offDiagonalEntry_symmetric n dw x y

theorem forwardMatrix_supported (n : ℕ) (dw : EdgeConductanceVariation n)
    (x y : ArchiveRolePhasePoint n) (hxy : x ≠ y)
    (h_adj : ¬ rolePhaseAdjacent n x y) :
    forwardMatrix n dw x y = 0 := by
  rw [forwardMatrix, if_neg hxy]
  simp [offDiagonalEntry, h_adj]

/-- The linear forward map into the declared matrix subspace. -/
noncomputable def archiveLocalLaplacianForward (n : ℕ) :
    EdgeConductanceVariation n →ₗ[ℝ] LocalLaplacianVariation n where
  toFun dw :=
    ⟨forwardMatrix n dw,
      ⟨forwardMatrix_symmetric n dw,
       forwardMatrix_row_sum_zero n dw,
       forwardMatrix_supported n dw⟩⟩
  map_add' dw₁ dw₂ := by
    apply Subtype.ext
    funext x y
    classical
    change forwardMatrix n (dw₁ + dw₂) x y =
      forwardMatrix n dw₁ x y + forwardMatrix n dw₂ x y
    by_cases hxy : x = y
    · subst y
      simp only [forwardMatrix, if_true]
      simp_rw [offDiagonalEntry_add]
      rw [Finset.sum_add_distrib]
      ring
    · rw [forwardMatrix, if_neg hxy, forwardMatrix, if_neg hxy,
        forwardMatrix, if_neg hxy]
      exact offDiagonalEntry_add n dw₁ dw₂ x y
  map_smul' c dw := by
    apply Subtype.ext
    funext x y
    classical
    change forwardMatrix n (c • dw) x y = c * forwardMatrix n dw x y
    by_cases hxy : x = y
    · subst y
      simp only [forwardMatrix, if_true]
      simp_rw [offDiagonalEntry_smul]
      rw [← Finset.mul_sum]
      ring
    · rw [forwardMatrix, if_neg hxy, forwardMatrix, if_neg hxy]
      exact offDiagonalEntry_smul n c dw x y

theorem archiveLocalLaplacianForward_apply (n : ℕ)
    (dw : EdgeConductanceVariation n) (x y : ArchiveRolePhasePoint n) :
    (archiveLocalLaplacianForward n dw : Matrix _ _ ℝ) x y = forwardMatrix n dw x y :=
  rfl

/-- Conductance recovered from a symmetric matrix on an undirected edge. -/
noncomputable def recover (n : ℕ) (dL : LocalLaplacianVariation n) :
    EdgeConductanceVariation n :=
  fun e =>
    Sym2.lift
      ⟨fun x y => -dL.1 x y / archiveMetricLaplacianScale n,
       fun x y => by
         dsimp
         rw [dL.2.1 y x]⟩ e.1

theorem recover_apply_of_eq (n : ℕ) (dL : LocalLaplacianVariation n)
    (e : ArchiveNearestNeighborEdge n) (x y : ArchiveRolePhasePoint n)
    (he : e.1 = s(x, y)) :
    recover n dL e = -dL.1 x y / archiveMetricLaplacianScale n := by
  classical
  unfold recover
  rw [he, Sym2.lift_mk]

noncomputable def archiveLocalLaplacianRecover (n : ℕ) :
    LocalLaplacianVariation n →ₗ[ℝ] EdgeConductanceVariation n where
  toFun := recover n
  map_add' dL₁ dL₂ := by
    funext e
    rcases e with ⟨e, he⟩
    induction e using Sym2.inductionOn with
    | _ x y =>
      simp [recover, Sym2.lift_mk, div_eq_mul_inv]
      ring
  map_smul' c dL := by
    funext e
    rcases e with ⟨e, he⟩
    induction e using Sym2.inductionOn with
    | _ x y =>
      simp [recover, Sym2.lift_mk, smul_eq_mul, div_eq_mul_inv]
      ring

theorem forward_recover_off_diagonal (n : ℕ) (dL : LocalLaplacianVariation n)
    (x y : ArchiveRolePhasePoint n) (hxy : x ≠ y)
    (h_adj : rolePhaseAdjacent n x y) :
    forwardMatrix n (archiveLocalLaplacianRecover n dL) x y = dL.1 x y := by
  classical
  let e : ArchiveNearestNeighborEdge n := adjacentEdge h_adj
  have he : e.1 = s(x, y) := rfl
  have hr := recover_apply_of_eq n dL e x y he
  simp only [forwardMatrix, if_neg hxy, offDiagonalEntry, dif_pos h_adj]
  change -archiveMetricLaplacianScale n * recover n dL e = dL.1 x y
  rw [hr]
  field_simp [archiveMetricLaplacianScale_ne_zero n]

theorem forward_recover_diagonal (n : ℕ) (dL : LocalLaplacianVariation n)
    (x : ArchiveRolePhasePoint n) :
    forwardMatrix n (archiveLocalLaplacianRecover n dL) x x = dL.1 x x := by
  classical
  have h_row := dL.2.2.1 x
  have h_point : ∀ y : ArchiveRolePhasePoint n,
      (if rolePhaseAdjacent n x y then dL.1 x y else 0) =
        (if x = y then 0 else dL.1 x y) := by
    intro y
    by_cases hy : rolePhaseAdjacent n x y
    · by_cases hxy : x = y
      · subst y
        exact ((rolePhaseAdjacent_irreflexive n x) hy).elim
      · simp [hy, hxy]
    · by_cases hxy : x = y
      · subst y
        simp [hy]
      · simp [hy, hxy, dL.2.2.2 x y hxy hy]
  have h_adj_sum :
      (∑ y : ArchiveRolePhasePoint n,
        (if rolePhaseAdjacent n x y then dL.1 x y else 0)) =
        ∑ y ∈ Finset.univ.erase x, dL.1 x y := by
    simp_rw [h_point]
    have h_split := Finset.sum_erase_add
      (Finset.univ : Finset (ArchiveRolePhasePoint n))
      (fun y => if x = y then 0 else dL.1 x y) (Finset.mem_univ x)
    rw [← h_split]
    simp only [if_true]
    rw [add_zero]
    apply Finset.sum_congr rfl
    intro y hy
    simp [Ne.symm (Finset.ne_of_mem_erase hy)]
  have h_erase : (∑ y ∈ Finset.univ.erase x, dL.1 x y) = -dL.1 x x := by
    have h_split := Finset.sum_erase_add
      (Finset.univ : Finset (ArchiveRolePhasePoint n))
      (fun y => dL.1 x y) (Finset.mem_univ x)
    linarith
  unfold forwardMatrix
  rw [if_pos rfl]
  have h_entry : ∀ y : ArchiveRolePhasePoint n,
      offDiagonalEntry n (archiveLocalLaplacianRecover n dL) x y =
        if rolePhaseAdjacent n x y then dL.1 x y else 0 := by
    intro y
    by_cases hy : rolePhaseAdjacent n x y
    · by_cases hxy : x = y
      · subst y
        exact ((rolePhaseAdjacent_irreflexive n x) hy).elim
      · rw [show offDiagonalEntry n (archiveLocalLaplacianRecover n dL) x y =
          forwardMatrix n (archiveLocalLaplacianRecover n dL) x y by
            simp [forwardMatrix, hxy]]
        simpa [hy] using forward_recover_off_diagonal n dL x y hxy hy
    · simp [offDiagonalEntry, hy]
  simp_rw [h_entry]
  rw [h_adj_sum, h_erase]
  ring

theorem forward_recover (n : ℕ) (dL : LocalLaplacianVariation n) :
    archiveLocalLaplacianForward n (archiveLocalLaplacianRecover n dL) = dL := by
  apply Subtype.ext
  funext x y
  by_cases hxy : x = y
  · subst y
    exact forward_recover_diagonal n dL x
  · by_cases h_adj : rolePhaseAdjacent n x y
    · exact forward_recover_off_diagonal n dL x y hxy h_adj
    · rw [archiveLocalLaplacianForward_apply]
      exact (forwardMatrix_supported n (archiveLocalLaplacianRecover n dL) x y hxy h_adj).trans
        (dL.2.2.2 x y hxy h_adj).symm

theorem recover_forward (n : ℕ) (dw : EdgeConductanceVariation n) :
    archiveLocalLaplacianRecover n (archiveLocalLaplacianForward n dw) = dw := by
  funext e
  rcases e with ⟨e, he⟩
  induction e using Sym2.inductionOn with
  | _ x y =>
    have h_adj : rolePhaseAdjacent n x y := he
    have h_edge : adjacentEdge h_adj = (⟨s(x, y), he⟩ : ArchiveNearestNeighborEdge n) :=
      Subtype.ext (by rfl)
    have h_ne : x ≠ y := by
      intro hxy
      subst y
      exact rolePhaseAdjacent_irreflexive n x he
    simp only [archiveLocalLaplacianRecover, LinearMap.coe_mk, AddHom.coe_mk,
      recover, Sym2.lift_mk, archiveLocalLaplacianForward_apply,
      forwardMatrix, if_neg h_ne, offDiagonalEntry, dif_pos h_adj]
    rw [h_edge]
    field_simp [archiveMetricLaplacianScale_ne_zero n]

/-- The literal linear equivalence between edge conductances and local matrices. -/
noncomputable def archiveLocalLaplacianVariationEquiv (n : ℕ) :
    EdgeConductanceVariation n ≃ₗ[ℝ] LocalLaplacianVariation n :=
  LinearEquiv.ofBijective (archiveLocalLaplacianForward n)
    ⟨(fun dw₁ dw₂ h => by
        calc
          dw₁ = archiveLocalLaplacianRecover n
              (archiveLocalLaplacianForward n dw₁) := (recover_forward n dw₁).symm
          _ = archiveLocalLaplacianRecover n
              (archiveLocalLaplacianForward n dw₂) := congrArg (archiveLocalLaplacianRecover n) h
          _ = dw₂ := recover_forward n dw₂),
      (fun dL => by
        refine ⟨archiveLocalLaplacianRecover n dL, ?_⟩
        exact forward_recover n dL)⟩

theorem archiveLocalLaplacianVariationEquiv_apply (n : ℕ)
    (dw : EdgeConductanceVariation n) :
    archiveLocalLaplacianVariationEquiv n dw = archiveLocalLaplacianForward n dw :=
  rfl

/-- The owner theorem records the actual two-sided maps, not dimension arithmetic. -/
theorem archive_local_laplacian_variation_isomorphism_owner (n : ℕ)
    (dw : EdgeConductanceVariation n) :
    archiveLocalLaplacianRecover n (archiveLocalLaplacianForward n dw) = dw ∧
    (∀ dL : LocalLaplacianVariation n,
      archiveLocalLaplacianForward n (archiveLocalLaplacianRecover n dL) = dL) := by
  exact ⟨recover_forward n dw, forward_recover n⟩

/-- The legacy finite edge-count notation is retained only as an arithmetic helper. -/
def localLaplacianVariationDim (num_edges : ℕ) : ℕ := num_edges

def torusEdgeCount4D (L : ℕ) : ℕ := 4 * (L ^ 4)

theorem torus_edge_count_eq (L : ℕ) :
    torusEdgeCount4D L = 4 * (L ^ 4) := rfl

end D0.Geometry
