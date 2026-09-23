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

/-!
## Exact square

`D_H = d + d†`. Creation squares and codifferential squares cancel by the CAR
anticommutators because the directional differences commute. The cross terms
leave one copy of `-∑_r ∇_r⁻ ∇_r⁺` on every Fock component.
-/

theorem pairwise_real_sum_zero {ι : Type*} [Fintype ι]
    (A : ι → ι → ℝ) (h : ∀ i j, A i j + A j i = 0) :
    ∑ i, ∑ j, A i j = 0 := by
  classical
  have hpair : ∑ i, ∑ j, (A i j + A j i) = 0 := by
    apply Finset.sum_eq_zero
    intro i _
    apply Finset.sum_eq_zero
    intro j _
    exact h i j
  have hsplit :
      ∑ i, ∑ j, (A i j + A j i) =
        (∑ i, ∑ j, A i j) + (∑ i, ∑ j, A i j) := by
    simp_rw [Finset.sum_add_distrib]
    congr 1
    rw [Finset.sum_comm]
  have htwice : (∑ i, ∑ j, A i j) + (∑ i, ∑ j, A i j) = 0 := by
    rw [← hsplit, hpair]
  have hmul : (2 : ℝ) * ∑ i, ∑ j, A i j = 0 := by
    simpa [two_mul] using htwice
  exact (mul_eq_zero.mp hmul).resolve_left (by norm_num)

theorem forwardCreateDirection_zero (N : ℕ) (r : Role) :
    forwardCreateDirection N r (0 : ArchiveCochain N) = 0 := by
  funext p
  unfold forwardCreateDirection
  simp [forwardDifference_zero]

theorem forwardCreateDirection_add (N : ℕ) (r : Role)
    (ψ φ : ArchiveCochain N) :
    forwardCreateDirection N r (ψ + φ) =
      forwardCreateDirection N r ψ + forwardCreateDirection N r φ := by
  funext p
  unfold forwardCreateDirection
  simp only [Pi.add_apply]
  rw [← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl ?_
  intro ket _
  simp only [forwardDifference_apply, Pi.add_apply]
  ring

theorem forwardCreateDirection_sum {ι : Type*} [Fintype ι] (N : ℕ) (r : Role)
    (F : ι → ArchiveCochain N) :
    forwardCreateDirection N r (∑ i, F i) =
      ∑ i, forwardCreateDirection N r (F i) := by
  classical
  have hfin : ∀ s : Finset ι,
      forwardCreateDirection N r (∑ i ∈ s, F i) =
        ∑ i ∈ s, forwardCreateDirection N r (F i) := by
    intro s
    induction s using Finset.induction_on with
    | empty => simp [forwardCreateDirection_zero]
    | @insert a s ha ih =>
      rw [Finset.sum_insert ha, forwardCreateDirection_add, Finset.sum_insert ha, ih]
  exact hfin Finset.univ

theorem forwardCreateDirection_neg (N : ℕ) (r : Role) (ψ : ArchiveCochain N) :
    forwardCreateDirection N r (-ψ) = -forwardCreateDirection N r ψ := by
  funext p
  unfold forwardCreateDirection
  simp only [Pi.neg_apply]
  rw [← Finset.sum_neg_distrib]
  refine Finset.sum_congr rfl ?_
  intro ket _
  simp only [forwardDifference_apply, Pi.neg_apply]
  ring

theorem dForward_eq_sum (N : ℕ) (ψ : ArchiveCochain N) :
    dForward N ψ = ∑ r : Role, forwardCreateDirection N r ψ := by
  funext p
  simp [dForward, Finset.sum_apply]

theorem dForward_sq (N : ℕ) (ψ : ArchiveCochain N) :
    dForward N (dForward N ψ) = 0 := by
  classical
  rw [dForward_eq_sum, dForward_eq_sum]
  simp_rw [forwardCreateDirection_sum]
  funext p
  simp only [Finset.sum_apply, Pi.zero_apply]
  exact pairwise_real_sum_zero
    (fun s r => forwardCreateDirection N s (forwardCreateDirection N r ψ) p)
    (fun s r => by
      simpa [Pi.add_apply, Pi.zero_apply, add_comm] using
        congrFun (forwardCreateDirection_anticommute N s r ψ) p)

theorem backwardSite_add (N : ℕ) (r : Role) (ψ φ : ArchiveCochain N) :
    backwardSite N r (ψ + φ) = backwardSite N r ψ + backwardSite N r φ := by
  funext p
  simp [backwardSite, backwardDifference_apply, Pi.add_apply]
  ring

theorem backwardSite_neg (N : ℕ) (r : Role) (ψ : ArchiveCochain N) :
    backwardSite N r (-ψ) = -backwardSite N r ψ := by
  funext p
  simp [backwardSite, backwardDifference_apply, Pi.neg_apply]
  ring

theorem annihilateAction_neg (N : ℕ) (r : Role) (ψ : ArchiveCochain N) :
    annihilateAction N r (-ψ) = -annihilateAction N r ψ := by
  simpa [neg_one_smul] using annihilateAction_smul N r (-1) ψ

theorem backwardAnnihilateDirection_add (N : ℕ) (r : Role)
    (ψ φ : ArchiveCochain N) :
    backwardAnnihilateDirection N r (ψ + φ) =
      backwardAnnihilateDirection N r ψ + backwardAnnihilateDirection N r φ := by
  unfold backwardAnnihilateDirection
  rw [backwardSite_add, annihilateAction_add]

theorem backwardAnnihilateDirection_neg (N : ℕ) (r : Role)
    (ψ : ArchiveCochain N) :
    backwardAnnihilateDirection N r (-ψ) =
      -backwardAnnihilateDirection N r ψ := by
  unfold backwardAnnihilateDirection
  rw [backwardSite_neg, annihilateAction_neg]

theorem codiffDirection_add (N : ℕ) (r : Role) (ψ φ : ArchiveCochain N) :
    codiffDirection N r (ψ + φ) =
      codiffDirection N r ψ + codiffDirection N r φ := by
  unfold codiffDirection
  rw [backwardAnnihilateDirection_add]
  abel

theorem hodgeCodifferential_add (N : ℕ) (ψ φ : ArchiveCochain N) :
    hodgeCodifferential N (ψ + φ) =
      hodgeCodifferential N ψ + hodgeCodifferential N φ := by
  simp_rw [hodgeCodifferential_eq_sum]
  rw [← Finset.sum_add_distrib]
  refine Finset.sum_congr rfl ?_
  intro r _
  exact codiffDirection_add N r ψ φ

theorem codiffDirection_eq_neg (N : ℕ) (r : Role) (ψ : ArchiveCochain N) :
    codiffDirection N r ψ = -backwardAnnihilateDirection N r ψ := rfl

theorem backwardAnnihilateDirection_sum {ι : Type*} [Fintype ι] (N : ℕ) (r : Role)
    (F : ι → ArchiveCochain N) :
    backwardAnnihilateDirection N r (∑ i, F i) =
      ∑ i, backwardAnnihilateDirection N r (F i) := by
  classical
  have hfin : ∀ s : Finset ι,
      backwardAnnihilateDirection N r (∑ i ∈ s, F i) =
        ∑ i ∈ s, backwardAnnihilateDirection N r (F i) := by
    intro s
    induction s using Finset.induction_on with
    | empty =>
      simp only [Finset.sum_empty]
      unfold backwardAnnihilateDirection
      have hsite : backwardSite N r (0 : ArchiveCochain N) = 0 := by
        funext p
        simp [backwardSite, backwardDifference_apply]
      rw [hsite, annihilateAction_zero]
    | @insert a s ha ih =>
      rw [Finset.sum_insert ha, backwardAnnihilateDirection_add,
        Finset.sum_insert ha, ih]
  exact hfin Finset.univ

theorem codiffDirection_sum {ι : Type*} [Fintype ι] (N : ℕ) (r : Role)
    (F : ι → ArchiveCochain N) :
    codiffDirection N r (∑ i, F i) = ∑ i, codiffDirection N r (F i) := by
  unfold codiffDirection
  rw [backwardAnnihilateDirection_sum, ← Finset.sum_neg_distrib]

theorem hodgeCodifferential_sq (N : ℕ) (ψ : ArchiveCochain N) :
    hodgeCodifferential N (hodgeCodifferential N ψ) = 0 := by
  classical
  have hψ : hodgeCodifferential N ψ = ∑ s : Role, codiffDirection N s ψ :=
    hodgeCodifferential_eq_sum N ψ
  rw [hψ]
  have hinner :
      hodgeCodifferential N (∑ s : Role, codiffDirection N s ψ) =
        ∑ r : Role, codiffDirection N r (∑ s : Role, codiffDirection N s ψ) :=
    hodgeCodifferential_eq_sum N _
  rw [hinner]
  simp_rw [codiffDirection_sum]
  funext p
  simp only [Finset.sum_apply, Pi.zero_apply]
  refine pairwise_real_sum_zero
    (fun r s => codiffDirection N r (codiffDirection N s ψ) p) ?_
  intro r s
  have hneg :
      codiffDirection N r (codiffDirection N s ψ) p =
        backwardAnnihilateDirection N r (backwardAnnihilateDirection N s ψ) p := by
    simpa using congrFun
      (by
        rw [codiffDirection_eq_neg, codiffDirection_eq_neg, backwardAnnihilateDirection_neg]
        abel :
        codiffDirection N r (codiffDirection N s ψ) =
          backwardAnnihilateDirection N r (backwardAnnihilateDirection N s ψ)) p
  have hneg' :
      codiffDirection N s (codiffDirection N r ψ) p =
        backwardAnnihilateDirection N s (backwardAnnihilateDirection N r ψ) p := by
    simpa using congrFun
      (by
        rw [codiffDirection_eq_neg, codiffDirection_eq_neg, backwardAnnihilateDirection_neg]
        abel :
        codiffDirection N s (codiffDirection N r ψ) =
          backwardAnnihilateDirection N s (backwardAnnihilateDirection N r ψ)) p
  dsimp
  rw [hneg, hneg']
  simpa [Pi.add_apply, Pi.zero_apply] using
    congrFun (backwardAnnihilateDirection_anticommute N r s ψ) p

theorem create_annihilate_delta (N : ℕ) (r s : Role) (φ : ArchiveCochain N) :
    createAction N r (annihilateAction N s φ) +
      annihilateAction N s (createAction N r φ) =
        if r = s then φ else 0 := by
  classical
  by_cases hrs : r = s
  · subst hrs
    simpa using create_annihilate_resolve N r φ
  · simpa [hrs] using create_annihilate_off N r s hrs φ

theorem forwardCreate_of_backwardAnnihilate (N : ℕ) (r s : Role)
    (ψ : ArchiveCochain N) :
    forwardCreateDirection N r (backwardAnnihilateDirection N s ψ) =
      createAction N r
        (annihilateAction N s (forwardSite N r (backwardSite N s ψ))) := by
  rw [show forwardCreateDirection N r (backwardAnnihilateDirection N s ψ) =
      createAction N r (forwardSite N r (backwardAnnihilateDirection N s ψ)) from
    forwardCreateDirection_eq_createAction_forwardSite N r _]
  rw [show backwardAnnihilateDirection N s ψ =
      annihilateAction N s (backwardSite N s ψ) from rfl]
  rw [forwardSite_annihilateAction_comm]

theorem backwardAnnihilate_of_forwardCreate (N : ℕ) (r s : Role)
    (ψ : ArchiveCochain N) :
    backwardAnnihilateDirection N s (forwardCreateDirection N r ψ) =
      annihilateAction N s
        (createAction N r (forwardSite N r (backwardSite N s ψ))) := by
  rw [show forwardCreateDirection N r ψ =
      createAction N r (forwardSite N r ψ) from
    forwardCreateDirection_eq_createAction_forwardSite N r _]
  rw [show backwardAnnihilateDirection N s (createAction N r (forwardSite N r ψ)) =
      annihilateAction N s (backwardSite N s (createAction N r (forwardSite N r ψ))) from rfl]
  rw [backwardSite_createAction_comm]
  rw [show backwardSite N s (forwardSite N r ψ) =
      forwardSite N r (backwardSite N s ψ) from
    (forwardSite_backwardSite_comm N r s ψ).symm]

theorem cochainDifferenceLaplacian_eq_backward_forward (N : ℕ)
    (ψ : ArchiveCochain N) :
    cochainDifferenceLaplacian N ψ =
      ∑ r : Role, -backwardSite N r (forwardSite N r ψ) := by
  funext p
  simp [cochainDifferenceLaplacian, scalarDifferenceLaplacian, backwardSite,
    forwardSite, Finset.sum_apply]

theorem hodgeCarDirac_cross (N : ℕ) (ψ : ArchiveCochain N) :
    dForward N (hodgeCodifferential N ψ) +
      hodgeCodifferential N (dForward N ψ) =
        cochainDifferenceLaplacian N ψ := by
  classical
  have hδ : hodgeCodifferential N ψ = ∑ s : Role, codiffDirection N s ψ :=
    hodgeCodifferential_eq_sum N ψ
  have hd : dForward N ψ = ∑ r : Role, forwardCreateDirection N r ψ :=
    dForward_eq_sum N ψ
  rw [hδ, hd]
  have hD :
      dForward N (∑ s : Role, codiffDirection N s ψ) =
        ∑ r : Role, forwardCreateDirection N r
          (∑ s : Role, codiffDirection N s ψ) :=
    dForward_eq_sum N _
  rw [hD]
  simp_rw [forwardCreateDirection_sum, codiffDirection_eq_neg, forwardCreateDirection_neg]
  have hDelta :
      hodgeCodifferential N (∑ r : Role, forwardCreateDirection N r ψ) =
        ∑ s : Role, -backwardAnnihilateDirection N s
          (∑ r : Role, forwardCreateDirection N r ψ) := by
    rw [hodgeCodifferential_eq_sum]
    refine Finset.sum_congr rfl ?_
    intro s _
    rfl
  rw [hDelta]
  simp_rw [backwardAnnihilateDirection_sum, ← Finset.sum_neg_distrib]
  funext p
  suffices
      (∑ r : Role, ∑ s : Role,
          -forwardCreateDirection N r (backwardAnnihilateDirection N s ψ) p) +
        (∑ s : Role, ∑ r : Role,
          -backwardAnnihilateDirection N s (forwardCreateDirection N r ψ) p) =
        cochainDifferenceLaplacian N ψ p by
    simpa [Pi.add_apply, Finset.sum_apply, Pi.neg_apply] using this
  have hpair : ∀ r s : Role,
      -forwardCreateDirection N r (backwardAnnihilateDirection N s ψ) p +
        -backwardAnnihilateDirection N s (forwardCreateDirection N r ψ) p =
          -(if r = s then forwardSite N r (backwardSite N s ψ) else 0) p := by
    intro r s
    rw [forwardCreate_of_backwardAnnihilate, backwardAnnihilate_of_forwardCreate]
    have happ := congrFun
      (create_annihilate_delta N r s (forwardSite N r (backwardSite N s ψ))) p
    simp only [Pi.add_apply] at happ
    rw [← neg_add, happ]
  have hjoined :
      (∑ r : Role, ∑ s : Role,
          -forwardCreateDirection N r (backwardAnnihilateDirection N s ψ) p) +
        (∑ r : Role, ∑ s : Role,
          -backwardAnnihilateDirection N s (forwardCreateDirection N r ψ) p) =
        ∑ r : Role, ∑ s : Role,
          -(if r = s then forwardSite N r (backwardSite N s ψ) else 0) p := by
    rw [← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl ?_
    intro r _
    rw [← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl ?_
    intro s _
    exact hpair r s
  have horder :
      (∑ s : Role, ∑ r : Role,
          -backwardAnnihilateDirection N s (forwardCreateDirection N r ψ) p) =
        ∑ r : Role, ∑ s : Role,
          -backwardAnnihilateDirection N s (forwardCreateDirection N r ψ) p :=
    Finset.sum_comm
  rw [horder, hjoined]
  have hdiag :
      ∑ r : Role, ∑ s : Role,
          -(if r = s then forwardSite N r (backwardSite N s ψ) else 0) p =
        ∑ r : Role, -(forwardSite N r (backwardSite N r ψ) p) := by
    refine Finset.sum_congr rfl ?_
    intro r _
    rw [Finset.sum_eq_single r]
    · simp
    · intro s _ hrs
      simp [Ne.symm hrs]
    · simp
  rw [hdiag]
  have hcomm :
      ∑ r : Role, -(forwardSite N r (backwardSite N r ψ) p) =
        ∑ r : Role, -(backwardSite N r (forwardSite N r ψ) p) := by
    refine Finset.sum_congr rfl ?_
    intro r _
    exact congrArg Neg.neg (congrFun (forwardSite_backwardSite_comm N r r ψ) p)
  rw [hcomm]
  simpa [Finset.sum_apply, Pi.neg_apply] using
    (congrFun (cochainDifferenceLaplacian_eq_backward_forward N ψ) p).symm

/-- Exact square: `D_H²` is the fibrewise oriented difference Laplacian. -/
theorem hodgeCarDirac_sq (N : ℕ) (ψ : ArchiveCochain N) :
    hodgeCarDirac N (hodgeCarDirac N ψ) = cochainDifferenceLaplacian N ψ := by
  have hsplit : hodgeCarDirac N ψ = dForward N ψ + hodgeCodifferential N ψ := rfl
  rw [hsplit]
  unfold hodgeCarDirac
  rw [dForward_add, hodgeCodifferential_add]
  rw [dForward_sq, hodgeCodifferential_sq]
  abel_nf
  exact hodgeCarDirac_cross N ψ

/-- The same identity read on one phase/Fock point: the Fock label is a spectator. -/
theorem hodgeCarDirac_sq_fibre (N : ℕ) (ψ : ArchiveCochain N)
    (p : ArchiveCochainBasis N) :
    hodgeCarDirac N (hodgeCarDirac N ψ) p =
      scalarDifferenceLaplacian N (fun x => ψ (x, p.2)) p.1 := by
  rw [hodgeCarDirac_sq, cochainDifferenceLaplacian]

end

end D0.Geometry
