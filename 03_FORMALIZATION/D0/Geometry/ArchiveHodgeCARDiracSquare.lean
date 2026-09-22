import Mathlib.Tactic
import D0.Geometry.ArchiveHodgeCARDirac
import D0.Geometry.ArchiveRoleProductLaplacian

namespace D0.Geometry

open D0
open scoped BigOperators

noncomputable section

/-!
# Square of the Hodge/difference CAR operator

`D_H²` acts as the oriented difference Laplacian on every Fock component.
At `L = 2` that Laplacian double-counts the single undirected neighbour of the
graph metric Laplacian.
-/

def codiffDirection (N : ℕ) (r : Role) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  -backwardAnnihilateDirection N r ψ

theorem fibreCompose {N : ℕ}
    (M Nmat : ArchiveFockState → ArchiveFockState → ℝ)
    (ψ : ArchiveCochain N) (x : ArchiveRolePhaseGroup N) (bra : ArchiveFockState) :
    (∑ mid, M bra mid * ∑ ket, Nmat mid ket * ψ (x, ket)) =
      ∑ ket, (∑ mid, M bra mid * Nmat mid ket) * ψ (x, ket) := by
  classical
  calc
    (∑ mid, M bra mid * ∑ ket, Nmat mid ket * ψ (x, ket)) =
        ∑ mid, ∑ ket, M bra mid * (Nmat mid ket * ψ (x, ket)) := by
          apply Finset.sum_congr rfl
          intro mid _
          rw [Finset.mul_sum]
    _ = ∑ ket, ∑ mid, M bra mid * Nmat mid ket * ψ (x, ket) := by
          rw [Finset.sum_comm]
          apply Finset.sum_congr rfl
          intro ket _
          apply Finset.sum_congr rfl
          intro mid _
          ring
    _ = ∑ ket, (∑ mid, M bra mid * Nmat mid ket) * ψ (x, ket) := by
          apply Finset.sum_congr rfl
          intro ket _
          rw [← Finset.sum_mul]

theorem create_annihilate_resolve (N : ℕ) (r : Role) (ψ : ArchiveCochain N) :
    createAction N r (annihilateAction N r ψ) +
      annihilateAction N r (createAction N r ψ) = ψ := by
  classical
  funext p
  unfold createAction annihilateAction
  simp only [Pi.add_apply]
  rw [fibreCompose (carCreate r) (carAnnihilate r) ψ p.1 p.2,
    fibreCompose (carAnnihilate r) (carCreate r) ψ p.1 p.2,
    ← Finset.sum_add_distrib]
  rw [Finset.sum_eq_single p.2]
  · have hcar := car_mixed_anticommutator_create_first r r p.2 p.2
    unfold anticommutator at hcar
    rw [← add_mul, hcar]
    simp [roleDelta, fockIdentity]
  · intro ket _ hket
    have hcar := car_mixed_anticommutator_create_first r r p.2 ket
    unfold anticommutator at hcar
    rw [← add_mul, hcar]
    simp only [roleDelta, fockIdentity]
    rw [if_neg (Ne.symm hket)]
    simp
  · simp

theorem create_annihilate_off (N : ℕ) (r s : Role) (hrs : r ≠ s)
    (ψ : ArchiveCochain N) :
    createAction N r (annihilateAction N s ψ) +
      annihilateAction N s (createAction N r ψ) = 0 := by
  classical
  funext p
  unfold createAction annihilateAction
  simp only [Pi.add_apply, Pi.zero_apply]
  rw [fibreCompose (carCreate r) (carAnnihilate s) ψ p.1 p.2,
    fibreCompose (carAnnihilate s) (carCreate r) ψ p.1 p.2,
    ← Finset.sum_add_distrib]
  apply Finset.sum_eq_zero
  intro ket _
  have hcar := car_mixed_anticommutator_create_first r s p.2 ket
  unfold anticommutator at hcar
  rw [← add_mul, hcar]
  simp [roleDelta, hrs]

theorem forward_backward_difference_comm (N : ℕ) (r s : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) :
    forwardDifference N r (backwardDifference N s f) =
      backwardDifference N s (forwardDifference N r f) := by
  funext x
  simp only [forwardDifference_apply, backwardDifference_apply]
  have h :
      roleTranslateMinus N s (roleTranslatePlus N r x) =
        roleTranslatePlus N r (roleTranslateMinus N s x) := by
    dsimp [roleTranslatePlus, roleTranslateMinus, roleTranslate]
    abel
  rw [h]
  ring

theorem forwardSite_backwardSite_comm (N : ℕ) (r s : Role) (ψ : ArchiveCochain N) :
    forwardSite N r (backwardSite N s ψ) =
      backwardSite N s (forwardSite N r ψ) := by
  funext p
  exact congrFun
    (forward_backward_difference_comm N r s (fun x => ψ (x, p.2))) p.1

theorem backwardSite_comm (N : ℕ) (r s : Role) (ψ : ArchiveCochain N) :
    backwardSite N r (backwardSite N s ψ) =
      backwardSite N s (backwardSite N r ψ) := by
  funext p
  have h := forward_backward_difference_comm N r s
  -- both backward: use the scalar identity twice via translates
  simp only [backwardSite, backwardDifference_apply] at *
  have hcomm :
      roleTranslateMinus N s (roleTranslateMinus N r p.1) =
        roleTranslateMinus N r (roleTranslateMinus N s p.1) := by
    dsimp [roleTranslateMinus, roleTranslate]
    abel
  rw [hcomm]
  ring

theorem annihilateAction_comp_apply (N : ℕ) (r s : Role)
    (ψ : ArchiveCochain N) (p : ArchiveCochainBasis N) :
    annihilateAction N r (annihilateAction N s ψ) p =
      ∑ ket, (∑ mid, carAnnihilate r p.2 mid * carAnnihilate s mid ket) *
        ψ (p.1, ket) := by
  classical
  exact fibreCompose (carAnnihilate r) (carAnnihilate s) ψ p.1 p.2

theorem annihilateAction_anticommute (N : ℕ) (r s : Role) (ψ : ArchiveCochain N) :
    annihilateAction N r (annihilateAction N s ψ) +
      annihilateAction N s (annihilateAction N r ψ) = 0 := by
  classical
  funext p
  simp only [Pi.add_apply, Pi.zero_apply]
  rw [annihilateAction_comp_apply, annihilateAction_comp_apply, ← Finset.sum_add_distrib]
  apply Finset.sum_eq_zero
  intro ket _
  have hcar := car_annihilate_anticommutator r s p.2 ket
  unfold anticommutator at hcar
  rw [← add_mul, hcar]
  simp

theorem backwardAnnihilateDirection_anticommute (N : ℕ) (r s : Role)
    (ψ : ArchiveCochain N) :
    backwardAnnihilateDirection N r (backwardAnnihilateDirection N s ψ) +
      backwardAnnihilateDirection N s (backwardAnnihilateDirection N r ψ) = 0 := by
  change
    annihilateAction N r
        (backwardSite N r (annihilateAction N s (backwardSite N s ψ))) +
      annihilateAction N s
        (backwardSite N s (annihilateAction N r (backwardSite N r ψ))) = 0
  rw [backwardSite_annihilateAction_comm N r s (backwardSite N s ψ)]
  rw [backwardSite_annihilateAction_comm N s r (backwardSite N r ψ)]
  rw [backwardSite_comm N s r ψ]
  exact annihilateAction_anticommute N r s
    (backwardSite N r (backwardSite N s ψ))

theorem hodgeCodifferential_eq_sum (N : ℕ) (ψ : ArchiveCochain N) :
    hodgeCodifferential N ψ = ∑ r : Role, codiffDirection N r ψ := by
  funext p
  simp [hodgeCodifferential, codiffDirection, Finset.sum_apply]

theorem scalarDifferenceLaplacian_apply (N : ℕ)
    (f : ArchiveRolePhaseGroup N → ℝ) (x : ArchiveRolePhaseGroup N) :
    scalarDifferenceLaplacian N f x =
      ∑ r : Role, forwardDifferenceScale N ^ 2 *
        (2 * f x - f (roleTranslatePlus N r x) - f (roleTranslateMinus N r x)) := by
  unfold scalarDifferenceLaplacian
  apply Finset.sum_congr rfl
  intro r _
  simp only [backwardDifference_apply, forwardDifference_apply]
  have hback : roleTranslatePlus N r (roleTranslateMinus N r x) = x := by
    dsimp [roleTranslatePlus, roleTranslateMinus, roleTranslate]
    abel
  rw [hback]
  ring_nf

theorem scalarDifference_direction_double_count_at_l2 (r : Role)
    (f : ArchiveRolePhaseGroup 0 → ℝ) (x : ArchiveRolePhaseGroup 0) :
    -backwardDifference 0 r (forwardDifference 0 r f) x =
      2 * forwardDifferenceScale 0 ^ 2 *
        (f x - f (roleTranslatePlus 0 r x)) := by
  have h := roleTranslatePlus_eq_minus_at_zero r x
  have hback : roleTranslatePlus 0 r (roleTranslateMinus 0 r x) = x := by
    dsimp [roleTranslatePlus, roleTranslateMinus, roleTranslate]
    abel
  simp only [backwardDifference_apply, forwardDifference_apply, h, hback]
  ring_nf

/-- At `L = 2` the oriented diagonal is twice the undirected metric-graph diagonal. -/
theorem hodge_difference_diagonal_double_metric_at_l2
    (x : ArchiveRolePhaseGroup 0) (y : D0.Geometry.ArchiveRolePhaseProductCarrier.ArchiveRolePhasePoint 0) :
    scalarDifferenceLaplacian 0 (fun z => if z = x then (1 : ℝ) else 0) x =
      2 * D0.Geometry.ArchiveRoleProductLaplacian.archiveMetricProductLaplacian 0 y y := by
  classical
  have hdir : ∀ r : Role,
      -backwardDifference 0 r (forwardDifference 0 r
        (fun z => if z = x then (1 : ℝ) else 0)) x =
        2 * forwardDifferenceScale 0 ^ 2 := by
    intro r
    rw [scalarDifference_direction_double_count_at_l2]
    have hne : roleTranslatePlus 0 r x ≠ x := by
      intro h
      have hstep : roleStep 0 r = 0 := by
        have hx : x + roleStep 0 r = x + 0 := by
          simpa [roleTranslatePlus, roleTranslate] using h
        exact add_left_cancel hx
      have hcoord := congrFun hstep r
      simp [roleStep] at hcoord
      exact absurd hcoord (by decide : (1 : ZMod (archiveFibers 0)) ≠ 0)
    simp [hne]
  unfold scalarDifferenceLaplacian
  simp_rw [hdir, Finset.sum_const, Finset.card_univ, card_role]
  have hgraph :=
    D0.Geometry.ArchiveRoleProductLaplacian.small_cycle_diagonal_at_zero y
  unfold D0.Geometry.ArchiveRoleProductLaplacian.archiveMetricProductLaplacian
  rw [hgraph]
  simp [D0.Geometry.ArchivePhaseEdgeMetricScale.archiveMetricLaplacianScale,
    forwardDifferenceScale, archiveFibers]
  norm_num

end

end D0.Geometry
