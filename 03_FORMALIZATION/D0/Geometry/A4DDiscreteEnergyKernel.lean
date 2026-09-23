import Mathlib.Tactic
import D0.Geometry.A4DPrimalDualCellPairing
import D0.Geometry.A4DCoframeParentConstraint
import D0.Geometry.ArchiveCARDegreePreserving
import D0.Geometry.ArchiveCubicalCartan
import D0.Geometry.ArchiveHodgeCARDiracSquare
import D0.Geometry.ArchiveHodgeGradingSymmetry

namespace D0.Geometry

open D0
open scoped BigOperators

noncomputable section

/-!
# Flat staggered energy kernel on the literal archive cochains

All coefficients below retain the uncentered coframe `e x s r`.  Centered
readouts occur only in separately stated controls; they do not define this
operator or its energy.
-/

/-- Translation `U_r` on archive cochains, with the literal forward site shift. -/
def cochainForwardShift (N : ℕ) (r : Role) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => ψ (roleTranslatePlus N r p.1, p.2)

/-- Inverse translation `U_r⁻¹` on archive cochains. -/
def cochainBackwardShift (N : ℕ) (r : Role) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => ψ (roleTranslateMinus N r p.1, p.2)

/-- Pointwise multiplication by a scalar archive field. -/
def cochainMultiply (N : ℕ) (m : ArchiveRolePhaseGroup N → ℝ)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => m p.1 * ψ p

/-- Backward link average `A_r=(I+U_r⁻¹)/2`, applied on each Fock component. -/
def cochainBackwardAverage (N : ℕ) (r : Role) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => backwardAverage N r (fun x => ψ (x, p.2)) p.1

/-- The counting adjoint `A_r*=(I+U_r)/2`. -/
def cochainForwardAverage (N : ℕ) (r : Role) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => (ψ p + ψ (roleTranslatePlus N r p.1, p.2)) / 2

/-- The existing number-bilinear CAR operator `E_sr=c_s†c_r` on each site. -/
def cochainCarEnd (N : ℕ) (s r : Role) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => ∑ ket : ArchiveFockState, carEnd s r p.2 ket * ψ (p.1, ket)

/-- Symmetric link transport `B_r(e)=(M_e U_r+U_r⁻¹ M_e)/2`. -/
def cochainLinkSymmetric (N : ℕ) (r : Role)
    (e : ArchiveRolePhaseGroup N → ℝ) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p =>
    (e p.1 * ψ (roleTranslatePlus N r p.1, p.2) +
      e (roleTranslateMinus N r p.1) * ψ (roleTranslateMinus N r p.1, p.2)) / 2

/-- Ordered flux term `M_e U_s A_r E_sr`. -/
def cochainFluxForward (N : ℕ) (e : ArchiveRolePhaseGroup N → ℝ)
    (s r : Role) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  cochainMultiply N e
    (cochainForwardShift N s
      (cochainBackwardAverage N r (cochainCarEnd N s r ψ)))

/-- Counting adjoint of the ordered flux term. -/
def cochainFluxAdjoint (N : ℕ) (e : ArchiveRolePhaseGroup N → ℝ)
    (s r : Role) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  cochainCarEnd N r s
    (cochainForwardAverage N r
      (cochainBackwardShift N s (cochainMultiply N e ψ)))

/-- Full uncentered staggered first jet `H(e)` on literal archive cochains. -/
def flatStaggeredH (N : ℕ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) : ArchiveCochain N := fun p =>
  (∑ r : Role,
    cochainLinkSymmetric N r (fun x => e x r r) ψ p) -
  ∑ s : Role, ∑ r : Role,
    (cochainFluxForward N (fun x => e x s r) s r ψ p +
      cochainFluxAdjoint N (fun x => e x s r) s r ψ p)

/-- Independent site/edge/corner finite flux energy. -/
def fluxEnergy (N : ℕ) (e : LocalCoframeField N) (ψ : ArchiveCochain N) : ℝ :=
  (1 / 2 : ℝ) * (∑ x, ∑ S, ψ (x, S) * ψ (x, S)) +
  (1 / 2 : ℝ) * (∑ r : Role, ∑ x, ∑ S,
    e x r r * ψ (x, S) * ψ (roleTranslatePlus N r x, S)) -
  ∑ s : Role, ∑ r : Role, ∑ x, ∑ S,
    e x s r * ψ (x, S) *
      cochainForwardShift N s
        (cochainBackwardAverage N r (cochainCarEnd N s r ψ)) (x, S)

theorem sum_translate_product (N : ℕ) (r : Role)
    (f g : ArchiveRolePhaseGroup N → ℝ) :
    (∑ x, f (roleTranslatePlus N r x) * g x) =
      ∑ x, f x * g (roleTranslateMinus N r x) := by
  simp only [roleTranslatePlus_apply, roleTranslateMinus_apply]
  let e := roleStep N r
  have h : (∑ x, f (x + e) * g x) = ∑ x, f x * g (x - e) := by
    simpa [e, roleTranslateEquiv] using
      (sum_translate N e (fun y => f y * g (y - e)))
  simpa [e] using h

theorem cochainPairing_add_left (N : ℕ) (ψ φ χ : ArchiveCochain N) :
    cochainPairing N (ψ + φ) χ =
      cochainPairing N ψ χ + cochainPairing N φ χ := by
  unfold cochainPairing
  simp_rw [Pi.add_apply, add_mul, Finset.sum_add_distrib]

theorem cochainPairing_add_right (N : ℕ) (ψ φ χ : ArchiveCochain N) :
    cochainPairing N ψ (φ + χ) =
      cochainPairing N ψ φ + cochainPairing N ψ χ := by
  calc
    cochainPairing N ψ (φ + χ) =
        cochainPairing N (φ + χ) ψ := cochainPairing_symm N _ _
    _ = cochainPairing N φ ψ + cochainPairing N χ ψ :=
        cochainPairing_add_left N φ χ ψ
    _ = cochainPairing N ψ φ + cochainPairing N ψ χ := by
        rw [cochainPairing_symm N φ ψ, cochainPairing_symm N χ ψ]

theorem cochainPairing_smul_left (N : ℕ) (c : ℝ) (ψ φ : ArchiveCochain N) :
    cochainPairing N (c • ψ) φ = c * cochainPairing N ψ φ := by
  unfold cochainPairing
  simp only [Pi.smul_apply, smul_eq_mul]
  calc
    (∑ x, ∑ S, (c * ψ (x, S)) * φ (x, S)) =
        ∑ x, c * ∑ S, ψ (x, S) * φ (x, S) := by
          apply Finset.sum_congr rfl
          intro x hx
          rw [Finset.mul_sum]
          apply Finset.sum_congr rfl
          intro S hS
          ring
    _ = c * ∑ x, ∑ S, ψ (x, S) * φ (x, S) := by rw [Finset.mul_sum]

theorem cochainPairing_smul_right (N : ℕ) (c : ℝ) (ψ φ : ArchiveCochain N) :
    cochainPairing N ψ (c • φ) = c * cochainPairing N ψ φ := by
  calc
    cochainPairing N ψ (c • φ) = cochainPairing N (c • φ) ψ := cochainPairing_symm N _ _
    _ = c * cochainPairing N φ ψ := cochainPairing_smul_left N c φ ψ
    _ = c * cochainPairing N ψ φ := by rw [cochainPairing_symm N φ ψ]

theorem cochainPairing_neg_left (N : ℕ) (ψ φ : ArchiveCochain N) :
    cochainPairing N (-ψ) φ = -cochainPairing N ψ φ := by
  rw [show -ψ = (-1 : ℝ) • ψ by simp]
  rw [cochainPairing_smul_left]
  norm_num

theorem cochainPairing_sub_left (N : ℕ) (ψ φ χ : ArchiveCochain N) :
    cochainPairing N (ψ - φ) χ =
      cochainPairing N ψ χ - cochainPairing N φ χ := by
  rw [sub_eq_add_neg, cochainPairing_add_left, cochainPairing_neg_left]
  ring

theorem cochainPairing_sub_right (N : ℕ) (ψ φ χ : ArchiveCochain N) :
    cochainPairing N ψ (φ - χ) =
      cochainPairing N ψ φ - cochainPairing N ψ χ := by
  rw [cochainPairing_symm, cochainPairing_sub_left]
  rw [cochainPairing_symm N φ ψ, cochainPairing_symm N χ ψ]

theorem cochainPairing_double_sum_left {ι κ : Type*} [Fintype ι] [Fintype κ]
    (N : ℕ) (F : ι → κ → ArchiveCochain N) (φ : ArchiveCochain N) :
    cochainPairing N (∑ i, ∑ j, F i j) φ =
      ∑ i, ∑ j, cochainPairing N (F i j) φ := by
  calc
    cochainPairing N (∑ i, ∑ j, F i j) φ =
        ∑ i, cochainPairing N (∑ j, F i j) φ := cochainPairing_sum_left N _ _
    _ = ∑ i, ∑ j, cochainPairing N (F i j) φ := by
      apply Finset.sum_congr rfl
      intro i _
      exact cochainPairing_sum_left N _ _

theorem cochainPairing_double_sum_right {ι κ : Type*} [Fintype ι] [Fintype κ]
    (N : ℕ) (ψ : ArchiveCochain N) (F : ι → κ → ArchiveCochain N) :
    cochainPairing N ψ (∑ i, ∑ j, F i j) =
      ∑ i, ∑ j, cochainPairing N ψ (F i j) := by
  calc
    cochainPairing N ψ (∑ i, ∑ j, F i j) =
        ∑ i, cochainPairing N ψ (∑ j, F i j) := cochainPairing_sum_right N _ _
    _ = ∑ i, ∑ j, cochainPairing N ψ (F i j) := by
      apply Finset.sum_congr rfl
      intro i _
      exact cochainPairing_sum_right N _ _

theorem cochainForwardShift_adjoint (N : ℕ) (r : Role)
    (ψ φ : ArchiveCochain N) :
    cochainPairing N (cochainForwardShift N r ψ) φ =
      cochainPairing N ψ (cochainBackwardShift N r φ) := by
  classical
  unfold cochainPairing cochainForwardShift cochainBackwardShift
  calc
    (∑ x, ∑ S, ψ (roleTranslatePlus N r x, S) * φ (x, S)) =
        ∑ S, ∑ x, ψ (roleTranslatePlus N r x, S) * φ (x, S) := by
          rw [Finset.sum_comm]
    _ = ∑ S, ∑ x, ψ (x, S) * φ (roleTranslateMinus N r x, S) := by
          apply Finset.sum_congr rfl
          intro S hS
          exact sum_translate_product N r (fun x => ψ (x, S)) (fun x => φ (x, S))
    _ = ∑ x, ∑ S, ψ (x, S) * φ (roleTranslateMinus N r x, S) := by
          rw [Finset.sum_comm]

theorem cochainBackwardShift_adjoint (N : ℕ) (r : Role)
    (ψ φ : ArchiveCochain N) :
    cochainPairing N (cochainBackwardShift N r ψ) φ =
      cochainPairing N ψ (cochainForwardShift N r φ) := by
  calc
    cochainPairing N (cochainBackwardShift N r ψ) φ =
        cochainPairing N φ (cochainBackwardShift N r ψ) := cochainPairing_symm N _ _
    _ = cochainPairing N (cochainForwardShift N r φ) ψ :=
        (cochainForwardShift_adjoint N r φ ψ).symm
    _ = cochainPairing N ψ (cochainForwardShift N r φ) := cochainPairing_symm N _ _

theorem cochainMultiply_adjoint (N : ℕ) (m : ArchiveRolePhaseGroup N → ℝ)
    (ψ φ : ArchiveCochain N) :
    cochainPairing N (cochainMultiply N m ψ) φ =
      cochainPairing N ψ (cochainMultiply N m φ) := by
  unfold cochainPairing cochainMultiply
  apply Finset.sum_congr rfl
  intro x hx
  apply Finset.sum_congr rfl
  intro S hS
  ring

theorem cochainBackwardAverage_adjoint (N : ℕ) (r : Role)
    (ψ φ : ArchiveCochain N) :
    cochainPairing N (cochainBackwardAverage N r ψ) φ =
      cochainPairing N ψ (cochainForwardAverage N r φ) := by
  have hleft : cochainBackwardAverage N r ψ =
      (1 / 2 : ℝ) • (ψ + cochainBackwardShift N r ψ) := by
    funext p
    change (ψ p + ψ (roleTranslateMinus N r p.1, p.2)) / 2 =
      (1 / 2 : ℝ) * (ψ p + ψ (roleTranslateMinus N r p.1, p.2))
    ring
  have hright : cochainForwardAverage N r φ =
      (1 / 2 : ℝ) • (φ + cochainForwardShift N r φ) := by
    funext p
    change (φ p + φ (roleTranslatePlus N r p.1, p.2)) / 2 =
      (1 / 2 : ℝ) * (φ p + φ (roleTranslatePlus N r p.1, p.2))
    ring
  rw [hleft, cochainPairing_smul_left, cochainPairing_add_left,
    cochainBackwardShift_adjoint]
  rw [hright, cochainPairing_smul_right, cochainPairing_add_right]

theorem carEnd_transpose (s r : Role) (bra ket : ArchiveFockState) :
    carEnd s r bra ket = carEnd r s ket bra := by
  unfold carEnd
  apply Finset.sum_congr rfl
  intro mid hmid
  simp only [carCreate]
  ring

theorem annihilateAction_adjoint (N : ℕ) (r : Role)
    (ψ φ : ArchiveCochain N) :
    cochainPairing N (annihilateAction N r ψ) φ =
      cochainPairing N ψ (createAction N r φ) := by
  calc
    cochainPairing N (annihilateAction N r ψ) φ =
        cochainPairing N φ (annihilateAction N r ψ) := cochainPairing_symm N _ _
    _ = cochainPairing N (createAction N r φ) ψ :=
        (createAction_adjoint N r φ ψ).symm
    _ = cochainPairing N ψ (createAction N r φ) := cochainPairing_symm N _ _

theorem cochainCarEnd_eq_createAnnihilate (N : ℕ) (s r : Role)
    (ψ : ArchiveCochain N) :
    cochainCarEnd N s r ψ = createAction N s (annihilateAction N r ψ) := by
  funext p
  rw [createAction_annihilateAction_comp_apply]
  rfl

theorem cochainCarEnd_adjoint (N : ℕ) (s r : Role)
    (ψ φ : ArchiveCochain N) :
    cochainPairing N (cochainCarEnd N s r ψ) φ =
      cochainPairing N ψ (cochainCarEnd N r s φ) := by
  rw [cochainCarEnd_eq_createAnnihilate, createAction_adjoint,
    annihilateAction_adjoint, ← cochainCarEnd_eq_createAnnihilate]

theorem cochainLinkSymmetric_adjoint (N : ℕ) (r : Role)
    (e : ArchiveRolePhaseGroup N → ℝ) (ψ φ : ArchiveCochain N) :
    cochainPairing N (cochainLinkSymmetric N r e ψ) φ =
      cochainPairing N ψ (cochainLinkSymmetric N r e φ) := by
  have hB (χ : ArchiveCochain N) : cochainLinkSymmetric N r e χ =
      (1 / 2 : ℝ) •
        (cochainMultiply N e (cochainForwardShift N r χ) +
          cochainBackwardShift N r (cochainMultiply N e χ)) := by
    funext p
    simp [cochainLinkSymmetric, cochainMultiply, cochainForwardShift,
      cochainBackwardShift, smul_eq_mul]
    ring
  calc
    cochainPairing N (cochainLinkSymmetric N r e ψ) φ =
        (1 / 2 : ℝ) *
          (cochainPairing N ψ (cochainBackwardShift N r
                (cochainMultiply N e φ)) +
            cochainPairing N ψ
              (cochainMultiply N e (cochainForwardShift N r φ))) := by
          rw [hB, cochainPairing_smul_left, cochainPairing_add_left,
            cochainMultiply_adjoint, cochainForwardShift_adjoint,
            cochainBackwardShift_adjoint, cochainMultiply_adjoint]
    _ = cochainPairing N ψ (cochainLinkSymmetric N r e φ) := by
          rw [hB, cochainPairing_smul_right, cochainPairing_add_right]
          ring

theorem cochainFluxForward_adjoint (N : ℕ) (e : ArchiveRolePhaseGroup N → ℝ)
    (s r : Role) (ψ φ : ArchiveCochain N) :
    cochainPairing N (cochainFluxForward N e s r ψ) φ =
    cochainPairing N ψ (cochainFluxAdjoint N e s r φ) := by
  unfold cochainFluxForward cochainFluxAdjoint
  rw [cochainMultiply_adjoint,
    cochainForwardShift_adjoint, cochainBackwardAverage_adjoint,
    cochainCarEnd_adjoint]

theorem cochainFluxSymmetric_adjoint (N : ℕ) (e : ArchiveRolePhaseGroup N → ℝ)
    (s r : Role) (ψ φ : ArchiveCochain N) :
    cochainPairing N
        (cochainFluxForward N e s r ψ + cochainFluxAdjoint N e s r ψ) φ =
      cochainPairing N ψ
        (cochainFluxForward N e s r φ + cochainFluxAdjoint N e s r φ) := by
  have hadj : cochainPairing N (cochainFluxAdjoint N e s r ψ) φ =
      cochainPairing N ψ (cochainFluxForward N e s r φ) := by
    calc
      cochainPairing N (cochainFluxAdjoint N e s r ψ) φ =
          cochainPairing N φ (cochainFluxAdjoint N e s r ψ) :=
            cochainPairing_symm N _ _
      _ = cochainPairing N (cochainFluxForward N e s r φ) ψ :=
            (cochainFluxForward_adjoint N e s r φ ψ).symm
      _ = cochainPairing N ψ (cochainFluxForward N e s r φ) :=
            cochainPairing_symm N _ _
  rw [cochainPairing_add_left, cochainFluxForward_adjoint, hadj,
    cochainPairing_add_right]
  ring

private theorem homogeneousCochain_neg (N k : ℕ) (ψ : ArchiveCochain N)
    (hψ : HomogeneousCochain N k ψ) : HomogeneousCochain N k (-ψ) := by
  intro x S hS
  simp [hψ x S hS]

private theorem homogeneousCochain_sub (N k : ℕ) (ψ φ : ArchiveCochain N)
    (hψ : HomogeneousCochain N k ψ) (hφ : HomogeneousCochain N k φ) :
    HomogeneousCochain N k (ψ - φ) := by
  exact homogeneousCochain_add N k ψ (-φ) hψ (homogeneousCochain_neg N k φ hφ)

private theorem homogeneousCochain_sum {ι : Type*} [Fintype ι]
    (N k : ℕ) (F : ι → ArchiveCochain N)
    (hF : ∀ i, HomogeneousCochain N k (F i)) :
    HomogeneousCochain N k (∑ i, F i) := by
  intro x S hS
  simp only [Finset.sum_apply]
  apply Finset.sum_eq_zero
  intro i _
  exact hF i x S hS

private theorem cochainMultiply_homogeneous (N k : ℕ)
    (m : ArchiveRolePhaseGroup N → ℝ) (ψ : ArchiveCochain N)
    (hψ : HomogeneousCochain N k ψ) :
    HomogeneousCochain N k (cochainMultiply N m ψ) := by
  intro x S hS
  simp [cochainMultiply, hψ x S hS]

private theorem cochainForwardShift_homogeneous (N k : ℕ) (r : Role)
    (ψ : ArchiveCochain N) (hψ : HomogeneousCochain N k ψ) :
    HomogeneousCochain N k (cochainForwardShift N r ψ) := by
  intro x S hS
  exact hψ (roleTranslatePlus N r x) S hS

private theorem cochainBackwardShift_homogeneous (N k : ℕ) (r : Role)
    (ψ : ArchiveCochain N) (hψ : HomogeneousCochain N k ψ) :
    HomogeneousCochain N k (cochainBackwardShift N r ψ) := by
  intro x S hS
  exact hψ (roleTranslateMinus N r x) S hS

private theorem cochainBackwardAverage_homogeneous (N k : ℕ) (r : Role)
    (ψ : ArchiveCochain N) (hψ : HomogeneousCochain N k ψ) :
    HomogeneousCochain N k (cochainBackwardAverage N r ψ) := by
  intro x S hS
  simp [cochainBackwardAverage, backwardAverage, hψ x S hS,
    hψ (roleTranslateMinus N r x) S hS]

private theorem cochainForwardAverage_homogeneous (N k : ℕ) (r : Role)
    (ψ : ArchiveCochain N) (hψ : HomogeneousCochain N k ψ) :
    HomogeneousCochain N k (cochainForwardAverage N r ψ) := by
  intro x S hS
  simp [cochainForwardAverage, hψ x S hS,
    hψ (roleTranslatePlus N r x) S hS]

private theorem cochainCarEnd_homogeneous (N k : ℕ) (s r : Role)
    (ψ : ArchiveCochain N) (hψ : HomogeneousCochain N k ψ) :
    HomogeneousCochain N k (cochainCarEnd N s r ψ) := by
  intro x S hS
  unfold cochainCarEnd
  apply Finset.sum_eq_zero
  intro ket _
  by_cases hc : carEnd s r S ket = 0
  · simp [hc]
  · have hdegree : fockDegree S = fockDegree ket := by
      by_contra hne
      exact hc (carEnd_degree_preserving s r S ket hne)
    simp [hψ x ket (by omega : fockDegree ket ≠ k)]

private theorem cochainLinkSymmetric_homogeneous (N k : ℕ) (r : Role)
    (e : ArchiveRolePhaseGroup N → ℝ) (ψ : ArchiveCochain N)
    (hψ : HomogeneousCochain N k ψ) :
    HomogeneousCochain N k (cochainLinkSymmetric N r e ψ) := by
  intro x S hS
  simp [cochainLinkSymmetric, hψ (roleTranslatePlus N r x) S hS,
    hψ (roleTranslateMinus N r x) S hS]

private theorem cochainFluxForward_homogeneous (N k : ℕ)
    (e : ArchiveRolePhaseGroup N → ℝ) (s r : Role) (ψ : ArchiveCochain N)
    (hψ : HomogeneousCochain N k ψ) :
    HomogeneousCochain N k (cochainFluxForward N e s r ψ) := by
  unfold cochainFluxForward
  exact cochainMultiply_homogeneous N k e _
    (cochainForwardShift_homogeneous N k s _
      (cochainBackwardAverage_homogeneous N k r _
        (cochainCarEnd_homogeneous N k s r ψ hψ)))

private theorem cochainFluxAdjoint_homogeneous (N k : ℕ)
    (e : ArchiveRolePhaseGroup N → ℝ) (s r : Role) (ψ : ArchiveCochain N)
    (hψ : HomogeneousCochain N k ψ) :
    HomogeneousCochain N k (cochainFluxAdjoint N e s r ψ) := by
  unfold cochainFluxAdjoint
  exact cochainCarEnd_homogeneous N k r s _
    (cochainForwardAverage_homogeneous N k r _
      (cochainBackwardShift_homogeneous N k s _
        (cochainMultiply_homogeneous N k e ψ hψ)))

/-- The full uncentered staggered first jet preserves each literal Fock degree. -/
theorem flatStaggeredH_preserves_degree (N k : ℕ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) (hψ : HomogeneousCochain N k ψ) :
    HomogeneousCochain N k (flatStaggeredH N e ψ) := by
  unfold flatStaggeredH
  apply homogeneousCochain_sub
  · change HomogeneousCochain N k
      (∑ r : Role, cochainLinkSymmetric N r (fun x => e x r r) ψ)
    apply homogeneousCochain_sum
    intro r
    exact cochainLinkSymmetric_homogeneous N k r (fun x => e x r r) ψ hψ
  · change HomogeneousCochain N k
      (∑ s : Role, ∑ r : Role,
        (cochainFluxForward N (fun x => e x s r) s r ψ +
          cochainFluxAdjoint N (fun x => e x s r) s r ψ))
    apply homogeneousCochain_sum
    intro s
    apply homogeneousCochain_sum
    intro r
    exact homogeneousCochain_add N k
      (cochainFluxForward N (fun x => e x s r) s r ψ)
      (cochainFluxAdjoint N (fun x => e x s r) s r ψ)
      (cochainFluxForward_homogeneous N k (fun x => e x s r) s r ψ hψ)
      (cochainFluxAdjoint_homogeneous N k (fun x => e x s r) s r ψ hψ)

private theorem cochainMultiply_parity (N : ℕ) (m : ArchiveRolePhaseGroup N → ℝ)
    (ψ : ArchiveCochain N) :
    cochainMultiply N m (parityCochain N ψ) =
      parityCochain N (cochainMultiply N m ψ) := by
  funext p
  simp [cochainMultiply, parityCochain]
  ring

private theorem cochainForwardShift_parity (N : ℕ) (r : Role)
    (ψ : ArchiveCochain N) :
    cochainForwardShift N r (parityCochain N ψ) =
      parityCochain N (cochainForwardShift N r ψ) := by
  funext p
  rfl

private theorem cochainBackwardShift_parity (N : ℕ) (r : Role)
    (ψ : ArchiveCochain N) :
    cochainBackwardShift N r (parityCochain N ψ) =
      parityCochain N (cochainBackwardShift N r ψ) := by
  funext p
  rfl

private theorem cochainCarEnd_parity (N : ℕ) (s r : Role)
    (ψ : ArchiveCochain N) :
    cochainCarEnd N s r (parityCochain N ψ) =
      parityCochain N (cochainCarEnd N s r ψ) := by
  funext p
  classical
  unfold cochainCarEnd parityCochain
  calc
    (∑ ket : ArchiveFockState,
        carEnd s r p.2 ket * (fockParitySign ket * ψ (p.1, ket))) =
      ∑ ket : ArchiveFockState,
        fockParitySign p.2 * (carEnd s r p.2 ket * ψ (p.1, ket)) := by
          apply Finset.sum_congr rfl
          intro ket _
          by_cases hc : carEnd s r p.2 ket = 0
          · simp [hc]
          · have hd : fockDegree p.2 = fockDegree ket := by
              by_contra hne
              exact hc (carEnd_degree_preserving s r p.2 ket hne)
            rw [fockParitySign_eq_degree p.2 ket hd]
            ring
    _ = fockParitySign p.2 *
        ∑ ket : ArchiveFockState, carEnd s r p.2 ket * ψ (p.1, ket) := by
          rw [Finset.mul_sum]

private theorem cochainBackwardAverage_parity (N : ℕ) (r : Role)
    (ψ : ArchiveCochain N) :
    cochainBackwardAverage N r (parityCochain N ψ) =
      parityCochain N (cochainBackwardAverage N r ψ) := by
  funext p
  simp [cochainBackwardAverage, backwardAverage, parityCochain]
  ring

private theorem cochainForwardAverage_parity (N : ℕ) (r : Role)
    (ψ : ArchiveCochain N) :
    cochainForwardAverage N r (parityCochain N ψ) =
      parityCochain N (cochainForwardAverage N r ψ) := by
  funext p
  simp [cochainForwardAverage, parityCochain]
  ring

private theorem cochainLinkSymmetric_parity (N : ℕ) (r : Role)
    (e : ArchiveRolePhaseGroup N → ℝ) (ψ : ArchiveCochain N) :
    cochainLinkSymmetric N r e (parityCochain N ψ) =
      parityCochain N (cochainLinkSymmetric N r e ψ) := by
  funext p
  simp [cochainLinkSymmetric, parityCochain]
  ring

private theorem cochainFluxForward_parity (N : ℕ)
    (e : ArchiveRolePhaseGroup N → ℝ) (s r : Role) (ψ : ArchiveCochain N) :
    cochainFluxForward N e s r (parityCochain N ψ) =
      parityCochain N (cochainFluxForward N e s r ψ) := by
  unfold cochainFluxForward
  rw [cochainCarEnd_parity, cochainBackwardAverage_parity,
    cochainForwardShift_parity, cochainMultiply_parity]

private theorem cochainFluxAdjoint_parity (N : ℕ)
    (e : ArchiveRolePhaseGroup N → ℝ) (s r : Role) (ψ : ArchiveCochain N) :
    cochainFluxAdjoint N e s r (parityCochain N ψ) =
      parityCochain N (cochainFluxAdjoint N e s r ψ) := by
  unfold cochainFluxAdjoint
  rw [cochainMultiply_parity, cochainBackwardShift_parity,
    cochainForwardAverage_parity, cochainCarEnd_parity]

/-- The full first jet commutes with fermion parity. -/
theorem flatStaggeredH_preserves_parity (N : ℕ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) :
    flatStaggeredH N e (parityCochain N ψ) =
      parityCochain N (flatStaggeredH N e ψ) := by
  funext p
  simp only [flatStaggeredH]
  simp_rw [cochainLinkSymmetric_parity, cochainFluxForward_parity,
    cochainFluxAdjoint_parity, parityCochain]
  simp_rw [Finset.sum_add_distrib]
  simp_rw [← Finset.mul_sum]
  have hsum :
      (∑ s : Role, ∑ r : Role,
        (cochainFluxForward N (fun x => e x s r) s r ψ p +
          cochainFluxAdjoint N (fun x => e x s r) s r ψ p)) =
      (∑ s : Role, ∑ r : Role,
        cochainFluxForward N (fun x => e x s r) s r ψ p) +
      (∑ s : Role, ∑ r : Role,
        cochainFluxAdjoint N (fun x => e x s r) s r ψ p) := by
    simp_rw [Finset.sum_add_distrib]
  conv_rhs => unfold flatStaggeredH
  rw [hsum]
  ring

/-- The research first jet is symmetric in the counting pairing. -/
theorem flatStaggeredH_selfAdjoint (N : ℕ) (e : LocalCoframeField N)
    (ψ φ : ArchiveCochain N) :
    cochainPairing N (flatStaggeredH N e ψ) φ =
      cochainPairing N ψ (flatStaggeredH N e φ) := by
  have hlink : cochainPairing N
      (∑ r : Role, cochainLinkSymmetric N r (fun x => e x r r) ψ) φ =
      cochainPairing N ψ
        (∑ r : Role, cochainLinkSymmetric N r (fun x => e x r r) φ) := by
    rw [cochainPairing_sum_left, cochainPairing_sum_right]
    apply Finset.sum_congr rfl
    intro r _
    exact cochainLinkSymmetric_adjoint N r (fun x => e x r r) ψ φ
  have hflux : cochainPairing N
      (∑ s : Role, ∑ r : Role,
        (cochainFluxForward N (fun x => e x s r) s r ψ +
          cochainFluxAdjoint N (fun x => e x s r) s r ψ)) φ =
      cochainPairing N ψ
        (∑ s : Role, ∑ r : Role,
            (cochainFluxForward N (fun x => e x s r) s r φ +
            cochainFluxAdjoint N (fun x => e x s r) s r φ)) := by
    calc
      cochainPairing N
          (∑ s : Role, ∑ r : Role,
            (cochainFluxForward N (fun x => e x s r) s r ψ +
              cochainFluxAdjoint N (fun x => e x s r) s r ψ)) φ =
          ∑ s : Role, ∑ r : Role,
            cochainPairing N
              (cochainFluxForward N (fun x => e x s r) s r ψ +
                cochainFluxAdjoint N (fun x => e x s r) s r ψ) φ :=
              cochainPairing_double_sum_left N
                (fun s r => cochainFluxForward N (fun x => e x s r) s r ψ +
                  cochainFluxAdjoint N (fun x => e x s r) s r ψ) φ
      _ = ∑ s : Role, ∑ r : Role,
            cochainPairing N ψ
              (cochainFluxForward N (fun x => e x s r) s r φ +
                cochainFluxAdjoint N (fun x => e x s r) s r φ) := by
                  apply Finset.sum_congr rfl
                  intro s _
                  apply Finset.sum_congr rfl
                  intro r _
                  exact cochainFluxSymmetric_adjoint N (fun x => e x s r) s r ψ φ
      _ = cochainPairing N ψ
            (∑ s : Role, ∑ r : Role,
              (cochainFluxForward N (fun x => e x s r) s r φ +
                cochainFluxAdjoint N (fun x => e x s r) s r φ)) := by
                  exact (cochainPairing_double_sum_right N ψ
                    (fun s r => cochainFluxForward N (fun x => e x s r) s r φ +
                      cochainFluxAdjoint N (fun x => e x s r) s r φ)).symm
  change cochainPairing N
      ((∑ r : Role, cochainLinkSymmetric N r (fun x => e x r r) ψ) -
        ∑ s : Role, ∑ r : Role,
          (cochainFluxForward N (fun x => e x s r) s r ψ +
            cochainFluxAdjoint N (fun x => e x s r) s r ψ)) φ =
    cochainPairing N ψ
      ((∑ r : Role, cochainLinkSymmetric N r (fun x => e x r r) φ) -
        ∑ s : Role, ∑ r : Role,
          (cochainFluxForward N (fun x => e x s r) s r φ +
            cochainFluxAdjoint N (fun x => e x s r) s r φ))
  rw [cochainPairing_sub_left, cochainPairing_sub_right, hlink, hflux]

theorem flatStaggeredH_zero (N : ℕ) : flatStaggeredH N 0 = 0 := by
  funext ψ
  funext p
  simp [flatStaggeredH, cochainLinkSymmetric, cochainFluxForward,
    cochainFluxAdjoint, cochainMultiply, cochainCarEnd,
    cochainForwardAverage, cochainBackwardShift]

theorem fluxEnergy_flat_eq_counting (N : ℕ) (ψ : ArchiveCochain N) :
    fluxEnergy N 0 ψ = (1 / 2 : ℝ) * cochainPairing N ψ ψ := by
  simp [fluxEnergy, cochainPairing]

/-- At the flat coframe the independently defined Riesz kernel is the identity. -/
theorem flatRieszKernel_eq_identity (N : ℕ) (ψ : ArchiveCochain N) :
    cochainPairing N ψ (ψ + flatStaggeredH N 0 ψ) =
      cochainPairing N ψ ψ := by
  rw [flatStaggeredH_zero]
  simp

/-- Independent flat check: the flux energy is counting energy, while the
existing Hodge--Dirac square remains the archive codifferential Laplacian. -/
theorem fluxEnergy_flatDirac_check (N : ℕ) (ψ : ArchiveCochain N) :
    fluxEnergy N 0 ψ = (1 / 2 : ℝ) * cochainPairing N ψ ψ ∧
      hodgeCarDirac N (hodgeCarDirac N ψ) = cochainDifferenceLaplacian N ψ := by
  exact ⟨fluxEnergy_flat_eq_counting N ψ, hodgeCarDirac_sq N ψ⟩

/-- Literal corner expansion of the forward staggered flux.  Its second source
is transported by `U_r^{-1} U_s`, i.e. the Role offset `s-r`. -/
theorem cochainFluxForward_corner_expansion (N : ℕ)
    (e : ArchiveRolePhaseGroup N → ℝ) (s r : Role)
    (ψ : ArchiveCochain N) (x : ArchiveRolePhaseGroup N) (S : ArchiveFockState) :
    cochainFluxForward N e s r ψ (x, S) =
      e x * (cochainCarEnd N s r ψ
        (roleTranslatePlus N s x, S) +
        cochainCarEnd N s r ψ
          (roleTranslateMinus N r (roleTranslatePlus N s x), S)) / 2 := by
  simp [cochainFluxForward, cochainMultiply, cochainForwardShift,
    cochainBackwardAverage, backwardAverage]
  ring

private theorem roleStep_ne_zero (N : ℕ) (r : Role) : roleStep N r ≠ 0 := by
  intro h
  have hr := congrFun h r
  have hone : (1 : ZMod (archiveFibers N)) ≠ 0 := by
    intro hz
    have hdiv : archiveFibers N ∣ 1 :=
      (ZMod.natCast_eq_zero_iff 1 (archiveFibers N)).mp (by simpa using hz)
    have hle : archiveFibers N ≤ 1 := Nat.le_of_dvd (by norm_num) hdiv
    have hge : 2 ≤ archiveFibers N := by simp [archiveFibers]
    omega
  apply hone
  simpa [roleStep] using hr

/-- Structural distance-two corner capstone for distinct Role directions: the
ordered hopping term samples the mixed `U_r⁻¹ U_s` source as well as its direct
source. No path-word or arbitrary-radius claim is made. -/
theorem gradedH_requires_corner_distance_two (N : ℕ)
    (e : ArchiveRolePhaseGroup N → ℝ) (s r : Role) (hsr : s ≠ r)
    (ψ : ArchiveCochain N) (x : ArchiveRolePhaseGroup N) (S : ArchiveFockState) :
    cochainFluxForward N e s r ψ (x, S) =
      e x * (cochainCarEnd N s r ψ
        (roleTranslatePlus N s x, S) +
        cochainCarEnd N s r ψ
          (roleTranslateMinus N r (roleTranslatePlus N s x), S)) / 2 ∧
      roleTranslateMinus N r (roleTranslatePlus N s x) ≠ x ∧
      roleTranslateMinus N r (roleTranslatePlus N s x) ≠
        roleTranslatePlus N s x := by
  refine ⟨cochainFluxForward_corner_expansion N e s r ψ x S, ?_, ?_⟩
  · intro h
    have hmixed :
        roleTranslateMinus N r (roleTranslatePlus N s x) + roleStep N r =
          x + roleStep N s := by
      simp [roleTranslateMinus, roleTranslatePlus, roleTranslate, sub_eq_add_neg]
    rw [h] at hmixed
    have hsum : x + roleStep N r = x + roleStep N s := by
      simpa [roleTranslatePlus] using hmixed
    have hstep : roleStep N r = roleStep N s := add_left_cancel hsum
    have hcoord := congrFun hstep s
    have hone : (1 : ZMod (archiveFibers N)) ≠ 0 := by
      intro hz
      have hdiv : archiveFibers N ∣ 1 :=
        (ZMod.natCast_eq_zero_iff 1 (archiveFibers N)).mp (by simpa using hz)
      have hle : archiveFibers N ≤ 1 := Nat.le_of_dvd (by norm_num) hdiv
      have hge : 2 ≤ archiveFibers N := by simp [archiveFibers]
      omega
    apply hone
    simpa [roleStep, hsr] using hcoord.symm
  · intro h
    have hcancel : roleTranslateMinus N r (roleTranslatePlus N s x) +
        roleStep N r = roleTranslatePlus N s x + roleStep N r :=
      congrArg (fun y : ArchiveRolePhaseGroup N => y + roleStep N r) h
    have hback : roleTranslateMinus N r (roleTranslatePlus N s x) +
        roleStep N r = roleTranslatePlus N s x := by
      simp [roleTranslateMinus, roleTranslatePlus, roleTranslate, sub_eq_add_neg]
    have hzero : roleTranslatePlus N s x + roleStep N r =
        roleTranslatePlus N s x := hcancel.symm.trans hback
    have hstep : roleStep N r = 0 := by
      have hzero' : roleStep N r + roleTranslatePlus N s x =
          0 + roleTranslatePlus N s x := by
        simpa [add_comm] using hzero
      exact add_right_cancel hzero'
    exact roleStep_ne_zero N r hstep

theorem cochainLinkSymmetric_quadratic (N : ℕ) (r : Role)
    (e : ArchiveRolePhaseGroup N → ℝ) (ψ : ArchiveCochain N) :
    cochainPairing N ψ (cochainLinkSymmetric N r e ψ) =
      ∑ x, ∑ S, e x * ψ (x, S) * ψ (roleTranslatePlus N r x, S) := by
  have hdecomp : cochainLinkSymmetric N r e ψ =
      (1 / 2 : ℝ) •
        (cochainMultiply N e (cochainForwardShift N r ψ) +
          cochainBackwardShift N r (cochainMultiply N e ψ)) := by
    funext p
    simp [cochainLinkSymmetric, cochainMultiply, cochainForwardShift,
      cochainBackwardShift, smul_eq_mul]
    ring
  have hsecond : cochainPairing N ψ
      (cochainBackwardShift N r (cochainMultiply N e ψ)) =
      cochainPairing N ψ (cochainMultiply N e (cochainForwardShift N r ψ)) := by
    calc
      cochainPairing N ψ (cochainBackwardShift N r (cochainMultiply N e ψ)) =
          cochainPairing N (cochainBackwardShift N r (cochainMultiply N e ψ)) ψ :=
            cochainPairing_symm N _ _
      _ = cochainPairing N (cochainMultiply N e ψ)
            (cochainForwardShift N r ψ) := cochainBackwardShift_adjoint N r _ _
      _ = cochainPairing N ψ (cochainMultiply N e (cochainForwardShift N r ψ)) :=
            cochainMultiply_adjoint N e _ _
  calc
    cochainPairing N ψ (cochainLinkSymmetric N r e ψ) =
        (1 / 2 : ℝ) *
          (cochainPairing N ψ (cochainMultiply N e (cochainForwardShift N r ψ)) +
            cochainPairing N ψ (cochainBackwardShift N r (cochainMultiply N e ψ))) := by
          rw [hdecomp, cochainPairing_smul_right, cochainPairing_add_right]
    _ = cochainPairing N ψ (cochainMultiply N e (cochainForwardShift N r ψ)) := by
          rw [hsecond]
          ring
    _ = ∑ x, ∑ S, e x * ψ (x, S) * ψ (roleTranslatePlus N r x, S) := by
          unfold cochainPairing cochainMultiply cochainForwardShift
          apply Finset.sum_congr rfl
          intro x _
          apply Finset.sum_congr rfl
          intro S _
          ring

theorem cochainFluxForward_quadratic (N : ℕ) (e : ArchiveRolePhaseGroup N → ℝ)
    (s r : Role) (ψ : ArchiveCochain N) :
    cochainPairing N ψ (cochainFluxForward N e s r ψ) =
      ∑ x, ∑ S, e x * ψ (x, S) *
        cochainForwardShift N s
          (cochainBackwardAverage N r (cochainCarEnd N s r ψ)) (x, S) := by
  unfold cochainPairing cochainFluxForward cochainMultiply
  apply Finset.sum_congr rfl
  intro x _
  apply Finset.sum_congr rfl
  intro S _
  ring

theorem fluxEnergy_polarization_eq_H (N : ℕ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) :
    2 * fluxEnergy N e ψ =
      cochainPairing N ψ (ψ + flatStaggeredH N e ψ) := by
  have hlink : (∑ r : Role, ∑ x, ∑ S,
      e x r r * ψ (x, S) * ψ (roleTranslatePlus N r x, S)) =
      cochainPairing N ψ
        (∑ r : Role, cochainLinkSymmetric N r (fun x => e x r r) ψ) := by
    calc
      (∑ r : Role, ∑ x, ∑ S,
          e x r r * ψ (x, S) * ψ (roleTranslatePlus N r x, S)) =
          ∑ r : Role, cochainPairing N ψ
            (cochainLinkSymmetric N r (fun x => e x r r) ψ) := by
              apply Finset.sum_congr rfl
              intro r _
              exact (cochainLinkSymmetric_quadratic N r (fun x => e x r r) ψ).symm
      _ = cochainPairing N ψ
            (∑ r : Role, cochainLinkSymmetric N r (fun x => e x r r) ψ) :=
              (cochainPairing_sum_right N ψ _).symm
  have hforward : (∑ s : Role, ∑ r : Role, ∑ x, ∑ S,
      e x s r * ψ (x, S) * cochainForwardShift N s
        (cochainBackwardAverage N r (cochainCarEnd N s r ψ)) (x, S)) =
      cochainPairing N ψ (∑ s : Role, ∑ r : Role,
        cochainFluxForward N (fun x => e x s r) s r ψ) := by
    calc
      (∑ s : Role, ∑ r : Role, ∑ x, ∑ S,
          e x s r * ψ (x, S) * cochainForwardShift N s
            (cochainBackwardAverage N r (cochainCarEnd N s r ψ)) (x, S)) =
          ∑ s : Role, ∑ r : Role,
            cochainPairing N ψ
              (cochainFluxForward N (fun x => e x s r) s r ψ) := by
                apply Finset.sum_congr rfl
                intro s _
                apply Finset.sum_congr rfl
                intro r _
                exact (cochainFluxForward_quadratic N (fun x => e x s r) s r ψ).symm
      _ = cochainPairing N ψ
            (∑ s : Role, ∑ r : Role,
              cochainFluxForward N (fun x => e x s r) s r ψ) := by
                calc
                  (∑ s : Role, ∑ r : Role,
                    cochainPairing N ψ
                      (cochainFluxForward N (fun x => e x s r) s r ψ)) =
                      ∑ s : Role, cochainPairing N ψ
                        (∑ r : Role,
                          cochainFluxForward N (fun x => e x s r) s r ψ) := by
                            apply Finset.sum_congr rfl
                            intro s _
                            exact (cochainPairing_sum_right N ψ _).symm
                  _ = cochainPairing N ψ
                        (∑ s : Role, ∑ r : Role,
                          cochainFluxForward N (fun x => e x s r) s r ψ) :=
                        (cochainPairing_sum_right N ψ _).symm
  have hstar : cochainPairing N ψ
      (∑ s : Role, ∑ r : Role,
        cochainFluxAdjoint N (fun x => e x s r) s r ψ) =
      cochainPairing N ψ (∑ s : Role, ∑ r : Role,
        cochainFluxForward N (fun x => e x s r) s r ψ) := by
    calc
      cochainPairing N ψ
          (∑ s : Role, ∑ r : Role,
            cochainFluxAdjoint N (fun x => e x s r) s r ψ) =
          ∑ s : Role, ∑ r : Role,
            cochainPairing N ψ
              (cochainFluxAdjoint N (fun x => e x s r) s r ψ) := by
                rw [cochainPairing_sum_right]
                apply Finset.sum_congr rfl
                intro s _
                exact cochainPairing_sum_right N ψ _
      _ = ∑ s : Role, ∑ r : Role,
            cochainPairing N ψ
              (cochainFluxForward N (fun x => e x s r) s r ψ) := by
                apply Finset.sum_congr rfl
                intro s _
                apply Finset.sum_congr rfl
                intro r _
                calc
                  cochainPairing N ψ
                      (cochainFluxAdjoint N (fun x => e x s r) s r ψ) =
                      cochainPairing N (cochainFluxForward N (fun x => e x s r) s r ψ) ψ :=
                        (cochainFluxForward_adjoint N (fun x => e x s r) s r ψ ψ).symm
                  _ = cochainPairing N ψ
                        (cochainFluxForward N (fun x => e x s r) s r ψ) :=
                        cochainPairing_symm N _ _
      _ = cochainPairing N ψ
            (∑ s : Role, ∑ r : Role,
              cochainFluxForward N (fun x => e x s r) s r ψ) := by
                exact (cochainPairing_double_sum_right N ψ
                  (fun s r => cochainFluxForward N (fun x => e x s r) s r ψ)).symm
  have hcross : cochainPairing N ψ
      (∑ s : Role, ∑ r : Role,
        (cochainFluxForward N (fun x => e x s r) s r ψ +
          cochainFluxAdjoint N (fun x => e x s r) s r ψ)) =
      2 * (∑ s : Role, ∑ r : Role, ∑ x, ∑ S,
        e x s r * ψ (x, S) * cochainForwardShift N s
          (cochainBackwardAverage N r (cochainCarEnd N s r ψ)) (x, S)) := by
    have hstarSum : (∑ s : Role, ∑ r : Role,
        cochainPairing N ψ (cochainFluxAdjoint N (fun x => e x s r) s r ψ)) =
        ∑ s : Role, ∑ r : Role,
          cochainPairing N ψ (cochainFluxForward N (fun x => e x s r) s r ψ) := by
      calc
        (∑ s : Role, ∑ r : Role,
          cochainPairing N ψ (cochainFluxAdjoint N (fun x => e x s r) s r ψ)) =
          cochainPairing N ψ
            (∑ s : Role, ∑ r : Role,
              cochainFluxAdjoint N (fun x => e x s r) s r ψ) := by
                exact (cochainPairing_double_sum_right N ψ
                  (fun s r => cochainFluxAdjoint N (fun x => e x s r) s r ψ)).symm
        _ = cochainPairing N ψ
            (∑ s : Role, ∑ r : Role,
              cochainFluxForward N (fun x => e x s r) s r ψ) := hstar
        _ = ∑ s : Role, ∑ r : Role,
              cochainPairing N ψ (cochainFluxForward N (fun x => e x s r) s r ψ) := by
                exact cochainPairing_double_sum_right N ψ
                  (fun s r => cochainFluxForward N (fun x => e x s r) s r ψ)
    have hforwardPairs : (∑ s : Role, ∑ r : Role,
        cochainPairing N ψ (cochainFluxForward N (fun x => e x s r) s r ψ)) =
        ∑ s : Role, ∑ r : Role, ∑ x, ∑ S,
          e x s r * ψ (x, S) * cochainForwardShift N s
            (cochainBackwardAverage N r (cochainCarEnd N s r ψ)) (x, S) := by
      calc
        (∑ s : Role, ∑ r : Role,
          cochainPairing N ψ (cochainFluxForward N (fun x => e x s r) s r ψ)) =
            cochainPairing N ψ
              (∑ s : Role, ∑ r : Role,
                cochainFluxForward N (fun x => e x s r) s r ψ) := by
                  exact (cochainPairing_double_sum_right N ψ
                    (fun s r => cochainFluxForward N (fun x => e x s r) s r ψ)).symm
        _ = ∑ s : Role, ∑ r : Role, ∑ x, ∑ S,
              e x s r * ψ (x, S) * cochainForwardShift N s
                (cochainBackwardAverage N r (cochainCarEnd N s r ψ)) (x, S) := hforward.symm
    calc
      cochainPairing N ψ
          (∑ s : Role, ∑ r : Role,
            (cochainFluxForward N (fun x => e x s r) s r ψ +
              cochainFluxAdjoint N (fun x => e x s r) s r ψ)) =
          ∑ s : Role, ∑ r : Role,
            (cochainPairing N ψ (cochainFluxForward N (fun x => e x s r) s r ψ) +
              cochainPairing N ψ (cochainFluxAdjoint N (fun x => e x s r) s r ψ)) := by
                rw [cochainPairing_sum_right]
                apply Finset.sum_congr rfl
                intro s _
                rw [cochainPairing_sum_right]
                apply Finset.sum_congr rfl
                intro r _
                exact cochainPairing_add_right N ψ _ _
      _ = 2 * (∑ s : Role, ∑ r : Role,
            cochainPairing N ψ (cochainFluxForward N (fun x => e x s r) s r ψ)) := by
              simp_rw [Finset.sum_add_distrib]
              rw [hstarSum]
              ring
      _ = 2 * (∑ s : Role, ∑ r : Role, ∑ x, ∑ S,
            e x s r * ψ (x, S) * cochainForwardShift N s
              (cochainBackwardAverage N r (cochainCarEnd N s r ψ)) (x, S)) := by
              rw [hforwardPairs]
  unfold fluxEnergy
  rw [cochainPairing_add_right]
  unfold flatStaggeredH
  change 2 * ((1 / 2 : ℝ) * (∑ x, ∑ S, ψ (x, S) * ψ (x, S)) +
      (1 / 2 : ℝ) *
        (∑ r : Role, ∑ x, ∑ S,
          e x r r * ψ (x, S) * ψ (roleTranslatePlus N r x, S)) -
      ∑ s : Role, ∑ r : Role, ∑ x, ∑ S,
        e x s r * ψ (x, S) * cochainForwardShift N s
          (cochainBackwardAverage N r (cochainCarEnd N s r ψ)) (x, S)) =
    cochainPairing N ψ ψ +
      cochainPairing N ψ
        ((∑ r : Role, cochainLinkSymmetric N r (fun x => e x r r) ψ) -
          ∑ s : Role, ∑ r : Role,
            (cochainFluxForward N (fun x => e x s r) s r ψ +
              cochainFluxAdjoint N (fun x => e x s r) s r ψ))
  rw [cochainPairing_sub_right, ← hlink, hcross]
  simp only [cochainPairing]
  ring

/-! ## Algebraic-dual Riesz candidate

The map below is the complementary-label representative of the bilinear form
`Q_e(φ, ψ) = <φ, (I + H(e)) ψ>`. It is an algebraic dual representative;
it does not select a located geometric Hodge star.
-/

def fluxEnergyBilinear (N k : ℕ) (e : LocalCoframeField N)
    (φ ψ : archiveDegreeSubmodule N k) : ℝ :=
  cochainPairing N φ.1 (ψ.1 + flatStaggeredH N e ψ.1)

/-- Candidate `J_k⁻¹ Q_k♭` in the occupation-complement dual coordinates. -/
noncomputable def fluxEnergy_Riesz_abstractDual (N k : ℕ) (hk : k ≤ 4)
    (e : LocalCoframeField N) (ψ : archiveDegreeSubmodule N k) :
    archiveDegreeSubmodule N (4 - k) :=
  (algebraicComplementEquiv N k hk).symm
    ⟨ψ.1 + flatStaggeredH N e ψ.1,
      homogeneousCochain_add N k ψ.1 (flatStaggeredH N e ψ.1) ψ.2
        (flatStaggeredH_preserves_degree N k e ψ.1 ψ.2)⟩

theorem fluxEnergy_Riesz_abstractDual_represents (N k : ℕ) (hk : k ≤ 4)
    (e : LocalCoframeField N) (φ ψ : archiveDegreeSubmodule N k) :
    algebraicComplementPairing N k hk φ
        (fluxEnergy_Riesz_abstractDual N k hk e ψ) = fluxEnergyBilinear N k e φ ψ := by
  unfold algebraicComplementPairing fluxEnergyBilinear
  have hinv : algebraicComplementToPrimal N k hk
      (fluxEnergy_Riesz_abstractDual N k hk e ψ) =
      ⟨ψ.1 + flatStaggeredH N e ψ.1,
        homogeneousCochain_add N k ψ.1 (flatStaggeredH N e ψ.1) ψ.2
          (flatStaggeredH_preserves_degree N k e ψ.1 ψ.2)⟩ :=
    (algebraicComplementEquiv N k hk).apply_symm_apply _
  rw [hinv]

theorem fluxEnergyBilinear_symmetric (N k : ℕ) (e : LocalCoframeField N)
    (φ ψ : archiveDegreeSubmodule N k) :
    fluxEnergyBilinear N k e φ ψ = fluxEnergyBilinear N k e ψ φ := by
  unfold fluxEnergyBilinear
  rw [cochainPairing_add_right, cochainPairing_add_right,
    cochainPairing_symm N ψ.1 φ.1]
  apply congrArg (fun t : ℝ => cochainPairing N φ.1 ψ.1 + t)
  calc
    cochainPairing N φ.1 (flatStaggeredH N e ψ.1) =
        cochainPairing N (flatStaggeredH N e ψ.1) φ.1 :=
          cochainPairing_symm N φ.1 _
    _ = cochainPairing N ψ.1 (flatStaggeredH N e φ.1) :=
          flatStaggeredH_selfAdjoint N e ψ.1 φ.1

/-- Existence and uniqueness of the complementary representative of this supplied
finite bilinear energy, relative to the explicit algebraic pairing. -/
theorem energy_riesz_unique (N k : ℕ) (hk : k ≤ 4)
    (e : LocalCoframeField N) (ψ : archiveDegreeSubmodule N k) :
    ∃! z : archiveDegreeSubmodule N (4 - k),
      ∀ φ : archiveDegreeSubmodule N k,
        algebraicComplementPairing N k hk φ z = fluxEnergyBilinear N k e φ ψ := by
  refine ⟨fluxEnergy_Riesz_abstractDual N k hk e ψ, ?_, ?_⟩
  · intro φ
    exact fluxEnergy_Riesz_abstractDual_represents N k hk e φ ψ
  · intro z hz
    have hzero : ∀ φ : archiveDegreeSubmodule N k,
        algebraicComplementPairing N k hk φ
          (z - fluxEnergy_Riesz_abstractDual N k hk e ψ) = 0 := by
      intro φ
      rw [algebraicComplementPairing_sub_right]
      rw [hz φ, fluxEnergy_Riesz_abstractDual_represents]
      ring
    have hsep := (algebraicComplementPairing_perfect N k hk).2
      (z - fluxEnergy_Riesz_abstractDual N k hk e ψ) hzero
    exact sub_eq_zero.mp hsep

end

end D0.Geometry
