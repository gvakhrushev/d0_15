import Mathlib.Analysis.Matrix.Normed
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Tactic
import D0.Geometry.A4DPrimalDualCellPairing
import D0.Geometry.A4DCoframeParentConstraint
import D0.Geometry.ArchiveCARDegreePreserving
import D0.Geometry.ArchiveCubicalCartan
import D0.Geometry.ArchiveHodgeCARDiracSquare
import D0.Geometry.ArchiveHodgeGradingSymmetry
import D0.Geometry.A4DPathCovariantHodge

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

/-- Centered CAR contraction `Σ_r M_{ξʳ} A_r c_r` used by the staggered
Cartan generator. -/
def cochainCenteredContraction (N : ℕ) (ξ : LocalRoleVector N)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => ∑ r : Role, ξ p.1 r *
    cochainBackwardAverage N r (annihilateAction N r ψ) p

/-- Forward Cartan generator built from the centered contraction. -/
def a4dCartanGenerator (N : ℕ) (ξ : LocalRoleVector N)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  dForward N (cochainCenteredContraction N ξ ψ) +
    cochainCenteredContraction N ξ (dForward N ψ)

/-- Explicit first-jet and mixed-role expansion of the centered Cartan generator. -/
def cartanGeneratorExpansion (N : ℕ) (ξ : LocalRoleVector N)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  (∑ r : Role, cochainMultiply N (fun x => ξ x r)
      (cochainBackwardAverage N r (forwardSite N r ψ))) +
  ∑ s : Role, ∑ r : Role,
    cochainMultiply N (forwardDifference N s (fun x => ξ x r))
      (cochainForwardShift N s
        (cochainBackwardAverage N r (cochainCarEnd N s r ψ)))

/-- Finite forward product rule, with the shifted second factor retained literally. -/
private theorem cochainForwardSite_product (N : ℕ) (s : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) (ψ : ArchiveCochain N) :
    forwardSite N s (cochainMultiply N f ψ) =
      cochainMultiply N f (forwardSite N s ψ) +
        cochainMultiply N (forwardDifference N s f)
          (cochainForwardShift N s ψ) := by
  funext p
  simp [forwardSite, forwardDifference, cochainMultiply, cochainForwardShift]
  ring

private theorem createAction_add (N : ℕ) (s : Role)
    (ψ φ : ArchiveCochain N) :
    createAction N s (ψ + φ) = createAction N s ψ + createAction N s φ := by
  funext p
  unfold createAction
  simp only [Pi.add_apply]
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro ket _
  ring

private theorem createAction_smul (N : ℕ) (s : Role) (c : ℝ)
    (ψ : ArchiveCochain N) :
    createAction N s (c • ψ) = c • createAction N s ψ := by
  funext p
  unfold createAction
  simp only [Pi.smul_apply, smul_eq_mul]
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro ket _
  ring

private theorem createAction_multiply (N : ℕ) (s : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) (ψ : ArchiveCochain N) :
    createAction N s (cochainMultiply N f ψ) =
      cochainMultiply N f (createAction N s ψ) := by
  funext p
  unfold createAction cochainMultiply
  change (∑ ket : ArchiveFockState,
      carCreate s p.2 ket * (f p.1 * ψ (p.1, ket))) =
    f p.1 * (∑ ket : ArchiveFockState,
      carCreate s p.2 ket * ψ (p.1, ket))
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro ket _
  ring

private theorem createAction_forwardShift (N : ℕ) (s t : Role)
    (ψ : ArchiveCochain N) :
    createAction N s (cochainForwardShift N t ψ) =
      cochainForwardShift N t (createAction N s ψ) := by
  funext p
  simp [createAction, cochainForwardShift]

private theorem createAction_backwardShift (N : ℕ) (s t : Role)
    (ψ : ArchiveCochain N) :
    createAction N s (cochainBackwardShift N t ψ) =
      cochainBackwardShift N t (createAction N s ψ) := by
  funext p
  simp [createAction, cochainBackwardShift]

private theorem cochainBackwardAverage_smul_add (N : ℕ) (t : Role)
    (ψ : ArchiveCochain N) :
    cochainBackwardAverage N t ψ =
      (1 / 2 : ℝ) • (ψ + cochainBackwardShift N t ψ) := by
  funext p
  simp [cochainBackwardAverage, backwardAverage, cochainBackwardShift,
    smul_eq_mul]
  ring

private theorem cochainBackwardAverage_add (N : ℕ) (t : Role)
    (ψ φ : ArchiveCochain N) :
    cochainBackwardAverage N t (ψ + φ) =
      cochainBackwardAverage N t ψ + cochainBackwardAverage N t φ := by
  funext p
  simp [cochainBackwardAverage, backwardAverage]
  ring

private theorem cochainBackwardAverage_smul (N : ℕ) (t : Role) (c : ℝ)
    (ψ : ArchiveCochain N) :
    cochainBackwardAverage N t (c • ψ) =
      c • cochainBackwardAverage N t ψ := by
  funext p
  simp [cochainBackwardAverage, backwardAverage, Pi.smul_apply, smul_eq_mul]
  ring

private theorem cochainBackwardAverage_sum {ι : Type*} [Fintype ι]
    (N : ℕ) (t : Role) (F : ι → ArchiveCochain N) :
    cochainBackwardAverage N t (∑ i, F i) =
      ∑ i, cochainBackwardAverage N t (F i) := by
  funext p
  unfold cochainBackwardAverage backwardAverage
  simp only [Finset.sum_apply]
  change ((∑ i, F i p) +
      (∑ i, F i (roleTranslateMinus N t p.1, p.2))) / 2 =
    ∑ i, (F i p + F i (roleTranslateMinus N t p.1, p.2)) / 2
  rw [← Finset.sum_div, Finset.sum_add_distrib]

private theorem cochainCenteredContraction_sum (N : ℕ) (ξ : LocalRoleVector N)
    (ψ : ArchiveCochain N) :
    cochainCenteredContraction N ξ ψ =
      ∑ r : Role, cochainMultiply N (fun x => ξ x r)
        (cochainBackwardAverage N r (annihilateAction N r ψ)) := by
  funext p
  simp [cochainCenteredContraction, cochainMultiply]

private theorem cochainMultiply_sum {ι : Type*} [Fintype ι]
    (N : ℕ) (f : ArchiveRolePhaseGroup N → ℝ) (F : ι → ArchiveCochain N) :
    cochainMultiply N f (∑ i, F i) =
      ∑ i, cochainMultiply N f (F i) := by
  funext p
  simp only [cochainMultiply, Finset.sum_apply]
  rw [Finset.mul_sum]

private theorem forwardSite_smul (N : ℕ) (s : Role) (c : ℝ)
    (ψ : ArchiveCochain N) :
    forwardSite N s (c • ψ) = c • forwardSite N s ψ := by
  funext p
  simp [forwardSite, forwardDifference, Pi.smul_apply, smul_eq_mul]
  ring

private theorem createAction_backwardAverage (N : ℕ) (s t : Role)
    (ψ : ArchiveCochain N) :
    createAction N s (cochainBackwardAverage N t ψ) =
      cochainBackwardAverage N t (createAction N s ψ) := by
  rw [cochainBackwardAverage_smul_add, createAction_smul,
    createAction_add, createAction_backwardShift,
    ← cochainBackwardAverage_smul_add]

private theorem annihilateAction_backwardAverage (N : ℕ) (s t : Role)
    (ψ : ArchiveCochain N) :
    annihilateAction N s (cochainBackwardAverage N t ψ) =
      cochainBackwardAverage N t (annihilateAction N s ψ) := by
  rw [cochainBackwardAverage_smul_add, annihilateAction_smul,
    annihilateAction_add]
  have hshift : annihilateAction N s (cochainBackwardShift N t ψ) =
      cochainBackwardShift N t (annihilateAction N s ψ) := by
    funext p
    simp [annihilateAction, cochainBackwardShift]
  rw [hshift, ← cochainBackwardAverage_smul_add]

private theorem forwardSite_backwardAverage (N : ℕ) (s t : Role)
    (ψ : ArchiveCochain N) :
    forwardSite N s (cochainBackwardAverage N t ψ) =
      cochainBackwardAverage N t (forwardSite N s ψ) := by
  have hdecomp := cochainBackwardAverage_smul_add N t ψ
  rw [hdecomp]
  have hadd : forwardSite N s (ψ + cochainBackwardShift N t ψ) =
      forwardSite N s ψ + forwardSite N s (cochainBackwardShift N t ψ) := by
    funext p
    simp [forwardSite, forwardDifference]
    ring
  rw [forwardSite_smul, hadd]
  have hshift : forwardSite N s (cochainBackwardShift N t ψ) =
      cochainBackwardShift N t (forwardSite N s ψ) := by
    funext p
    simp [forwardSite, forwardDifference, cochainBackwardShift,
      roleTranslatePlus, roleTranslateMinus, roleTranslate, sub_eq_add_neg]
    have hx : p.1 + roleStep N s + -roleStep N t =
        p.1 + -roleStep N t + roleStep N s := by abel
    rw [hx]
    simp
  rw [hshift, ← cochainBackwardAverage_smul_add]

private theorem forwardCreateDirection_backwardAverage (N : ℕ) (s t : Role)
    (ψ : ArchiveCochain N) :
    forwardCreateDirection N s (cochainBackwardAverage N t ψ) =
      cochainBackwardAverage N t (forwardCreateDirection N s ψ) := by
  rw [forwardCreateDirection_eq_createAction_forwardSite,
    forwardSite_backwardAverage, createAction_backwardAverage,
    ← forwardCreateDirection_eq_createAction_forwardSite]

private theorem forwardCreateDirection_product (N : ℕ) (s : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) (ψ : ArchiveCochain N) :
    forwardCreateDirection N s (cochainMultiply N f ψ) =
      cochainMultiply N f (forwardCreateDirection N s ψ) +
        cochainMultiply N (forwardDifference N s f)
          (cochainForwardShift N s (createAction N s ψ)) := by
  rw [forwardCreateDirection_eq_createAction_forwardSite,
    cochainForwardSite_product, createAction_add, createAction_multiply,
    createAction_multiply, createAction_forwardShift,
    ← forwardCreateDirection_eq_createAction_forwardSite]

private theorem centeredForwardCAR (N : ℕ) (s r : Role)
    (ψ : ArchiveCochain N) :
    forwardCreateDirection N s
        (cochainBackwardAverage N r (annihilateAction N r ψ)) +
      cochainBackwardAverage N r
        (annihilateAction N r (forwardCreateDirection N s ψ)) =
      (roleDelta r s : ℝ) •
        cochainBackwardAverage N r (forwardSite N s ψ) := by
  rw [forwardCreateDirection_backwardAverage, ← cochainBackwardAverage_add,
    forwardCreateDirection_mixed, cochainBackwardAverage_smul]

private theorem centeredCartanRolePair (N : ℕ) (s r : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) (ψ : ArchiveCochain N) :
    cochainMultiply N f
        (forwardCreateDirection N s
          (cochainBackwardAverage N r (annihilateAction N r ψ))) +
      cochainMultiply N f
        (cochainBackwardAverage N r
          (annihilateAction N r (forwardCreateDirection N s ψ))) +
      cochainMultiply N (forwardDifference N s f)
        (cochainForwardShift N s
          (createAction N s
            (cochainBackwardAverage N r (annihilateAction N r ψ)))) =
    cochainMultiply N f
        ((roleDelta r s : ℝ) •
          cochainBackwardAverage N r (forwardSite N s ψ)) +
      cochainMultiply N (forwardDifference N s f)
        (cochainForwardShift N s
          (cochainBackwardAverage N r (cochainCarEnd N s r ψ))) := by
  have hcar := centeredForwardCAR N s r ψ
  have hcarEnd : cochainCarEnd N s r ψ =
      createAction N s (annihilateAction N r ψ) := by
    funext q
    rw [createAction_annihilateAction_comp_apply]
    rfl
  have hmix : createAction N s
      (cochainBackwardAverage N r (annihilateAction N r ψ)) =
      cochainBackwardAverage N r (cochainCarEnd N s r ψ) := by
    rw [createAction_backwardAverage, ← hcarEnd]
  funext p
  have hpoint := congrFun hcar p
  simp only [cochainMultiply, Pi.add_apply, Pi.smul_apply, smul_eq_mul] at *
  rw [hmix]
  calc
    f p.1 * forwardCreateDirection N s
          (cochainBackwardAverage N r (annihilateAction N r ψ)) p +
        f p.1 * cochainBackwardAverage N r
          (annihilateAction N r (forwardCreateDirection N s ψ)) p +
        forwardDifference N s f p.1 * cochainForwardShift N s
          (cochainBackwardAverage N r (cochainCarEnd N s r ψ)) p =
      f p.1 * (forwardCreateDirection N s
          (cochainBackwardAverage N r (annihilateAction N r ψ)) p +
        cochainBackwardAverage N r
          (annihilateAction N r (forwardCreateDirection N s ψ)) p) +
        forwardDifference N s f p.1 * cochainForwardShift N s
          (cochainBackwardAverage N r (cochainCarEnd N s r ψ)) p := by ring
    _ = f p.1 * ((roleDelta r s : ℝ) *
          cochainBackwardAverage N r (forwardSite N s ψ) p) +
        forwardDifference N s f p.1 * cochainForwardShift N s
          (cochainBackwardAverage N r (cochainCarEnd N s r ψ)) p := by
          rw [hpoint]

/-- Exact centered Cartan expansion by the shifted product rule and CAR. -/
theorem cartanGenerator_exact_expansion (N : ℕ) (ξ : LocalRoleVector N)
    (ψ : ArchiveCochain N) :
    a4dCartanGenerator N ξ ψ = cartanGeneratorExpansion N ξ ψ := by
  classical
  unfold a4dCartanGenerator
  simp_rw [cochainCenteredContraction_sum]
  rw [dForward_sum]
  simp_rw [dForward_eq_sum_directions, annihilateAction_sum,
    cochainBackwardAverage_sum]
  unfold cartanGeneratorExpansion
  simp_rw [forwardCreateDirection_product, cochainMultiply_sum,
    Finset.sum_add_distrib]
  have hFirst :
      (∑ r : Role, ∑ s : Role,
        cochainMultiply N (fun x => ξ x r)
          (forwardCreateDirection N s
            (cochainBackwardAverage N r (annihilateAction N r ψ)))) =
      ∑ s : Role, ∑ r : Role,
        cochainMultiply N (fun x => ξ x r)
          (forwardCreateDirection N s
            (cochainBackwardAverage N r (annihilateAction N r ψ))) := by
    exact Finset.sum_comm
  have hMixed :
      (∑ r : Role, ∑ s : Role,
        cochainMultiply N (forwardDifference N s (fun x => ξ x r))
          (cochainForwardShift N s
            (createAction N s
              (cochainBackwardAverage N r (annihilateAction N r ψ))))) =
      ∑ s : Role, ∑ r : Role,
        cochainMultiply N (forwardDifference N s (fun x => ξ x r))
          (cochainForwardShift N s
            (createAction N s
              (cochainBackwardAverage N r (annihilateAction N r ψ)))) := by
    exact Finset.sum_comm
  have hSecond :
      (∑ r : Role, ∑ s : Role,
        cochainMultiply N (fun x => ξ x r)
          (cochainBackwardAverage N r
            (annihilateAction N r (forwardCreateDirection N s ψ)))) =
      ∑ s : Role, ∑ r : Role,
        cochainMultiply N (fun x => ξ x r)
          (cochainBackwardAverage N r
            (annihilateAction N r (forwardCreateDirection N s ψ))) := by
    exact Finset.sum_comm
  rw [hFirst, hMixed, hSecond]
  simp only [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro s hs
  have hPairSum :
      (∑ r : Role,
        (cochainMultiply N (fun x => ξ x r)
            (forwardCreateDirection N s
              (cochainBackwardAverage N r (annihilateAction N r ψ))) +
          cochainMultiply N (forwardDifference N s (fun x => ξ x r))
            (cochainForwardShift N s
              (createAction N s
                (cochainBackwardAverage N r (annihilateAction N r ψ)))) +
          cochainMultiply N (fun x => ξ x r)
            (cochainBackwardAverage N r
              (annihilateAction N r (forwardCreateDirection N s ψ))))) =
      ∑ r : Role,
        (cochainMultiply N (fun x => ξ x r)
            ((roleDelta r s : ℝ) •
              cochainBackwardAverage N r (forwardSite N s ψ)) +
          cochainMultiply N (forwardDifference N s (fun x => ξ x r))
            (cochainForwardShift N s
              (cochainBackwardAverage N r (cochainCarEnd N s r ψ)))) := by
    apply Finset.sum_congr rfl
    intro r hr
    have h := centeredCartanRolePair N s r (fun x => ξ x r) ψ
    calc
      cochainMultiply N (fun x => ξ x r)
            (forwardCreateDirection N s
              (cochainBackwardAverage N r (annihilateAction N r ψ))) +
          cochainMultiply N (forwardDifference N s (fun x => ξ x r))
            (cochainForwardShift N s
              (createAction N s
                (cochainBackwardAverage N r (annihilateAction N r ψ)))) +
          cochainMultiply N (fun x => ξ x r)
            (cochainBackwardAverage N r
              (annihilateAction N r (forwardCreateDirection N s ψ))) = _ := by
        abel
      _ = _ := h
  rw [hPairSum, Finset.sum_add_distrib]
  congr 1
  funext p
  simp only [Finset.sum_apply, cochainMultiply]
  simp only [roleDelta, Pi.smul_apply, smul_eq_mul]
  simp only [ite_mul, one_mul, zero_mul, mul_ite, mul_zero, mul_one]
  simpa only [eq_comm] using
    (Fintype.sum_ite_eq s
      (fun x : Role => ξ p.1 x *
        cochainBackwardAverage N x (forwardSite N s ψ) p))

/-- Counting adjoint of the centered Cartan generator, written in its
first-jet/mixed-flux expansion. -/
def cartanGeneratorAdjoint (N : ℕ) (ξ : LocalRoleVector N)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  (∑ r : Role,
    -backwardSite N r
      (cochainForwardAverage N r
        (cochainMultiply N (fun x => ξ x r) ψ))) +
  ∑ s : Role, ∑ r : Role,
    cochainFluxAdjoint N (forwardDifference N s (fun x => ξ x r)) s r ψ

/-- The symmetric first-jet term is the negative symmetric link response to
the forward gauge strain. -/
theorem centeredCartanDiagonal_eq_negative_link (N : ℕ) (ξ : LocalRoleVector N)
    (ψ : ArchiveCochain N) :
    (∑ r : Role,
      (cochainMultiply N (fun x => ξ x r)
          (cochainBackwardAverage N r (forwardSite N r ψ)) -
        backwardSite N r
          (cochainForwardAverage N r
            (cochainMultiply N (fun x => ξ x r) ψ)))) =
      -∑ r : Role,
        cochainLinkSymmetric N r (forwardDifference N r (fun x => ξ x r)) ψ := by
  funext p
  simp only [Finset.sum_apply, Pi.neg_apply, Finset.sum_neg_distrib]
  rw [← Finset.sum_neg_distrib]
  apply Finset.sum_congr rfl
  intro r hr
  simp [cochainMultiply, cochainBackwardAverage, backwardAverage, cochainForwardAverage,
    backwardSite, backwardDifference, forwardSite, forwardDifference,
    cochainLinkSymmetric, roleTranslatePlus, roleTranslateMinus, roleTranslate]
  ring

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

/-- Exact Ward tangent for the forward gauge strain of the uncentered coframe. -/
theorem H_forwardGauge_eq_negative_sym_Cartan (N : ℕ)
    (ξ : LocalRoleVector N) (ψ : ArchiveCochain N) :
    flatStaggeredH N (forwardGaugeCoframe N ξ) ψ =
      -(cartanGeneratorAdjoint N ξ ψ + a4dCartanGenerator N ξ ψ) := by
  rw [cartanGenerator_exact_expansion]
  funext p
  simp only [flatStaggeredH, cartanGeneratorAdjoint,
    cartanGeneratorExpansion, forwardGaugeCoframe, Pi.add_apply,
    Pi.neg_apply, Finset.sum_apply, cochainFluxForward]
  have hdiag := congrFun
    (centeredCartanDiagonal_eq_negative_link N ξ ψ) p
  simp only [Finset.sum_apply, Pi.neg_apply] at hdiag
  have hlink :
      (∑ r : Role,
        cochainLinkSymmetric N r (forwardDifference N r (fun x => ξ x r)) ψ p) =
        -∑ r : Role,
          (cochainMultiply N (fun x => ξ x r)
              (cochainBackwardAverage N r (forwardSite N r ψ)) p -
            backwardSite N r
              (cochainForwardAverage N r
                (cochainMultiply N (fun x => ξ x r) ψ)) p) := by
    have hn := congrArg (fun z : ℝ => -z) hdiag
    simpa only [neg_neg] using hn.symm
  rw [hlink]
  simp only [Finset.sum_sub_distrib, Finset.sum_add_distrib]
  simp only [Finset.sum_neg_distrib, neg_neg]
  ring

/-- The general exact Cartan/Ward theorems specialize to the archive cycle of
length five (`N = 3`), providing the required odd-cycle regression. -/
theorem periodFive_centeredCartanWard_regression
    (ξ : LocalRoleVector 3) (ψ : ArchiveCochain 3) :
    a4dCartanGenerator 3 ξ ψ = cartanGeneratorExpansion 3 ξ ψ ∧
      flatStaggeredH 3 (forwardGaugeCoframe 3 ξ) ψ =
        -(cartanGeneratorAdjoint 3 ξ ψ + a4dCartanGenerator 3 ξ ψ) := by
  exact ⟨cartanGenerator_exact_expansion 3 ξ ψ,
    H_forwardGauge_eq_negative_sym_Cartan 3 ξ ψ⟩

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

theorem cartanGeneratorAdjoint_is_adjoint (N : ℕ) (ξ : LocalRoleVector N)
    (ψ φ : ArchiveCochain N) :
    cochainPairing N (a4dCartanGenerator N ξ ψ) φ =
      cochainPairing N ψ (cartanGeneratorAdjoint N ξ φ) := by
  rw [cartanGenerator_exact_expansion]
  unfold cartanGeneratorExpansion cartanGeneratorAdjoint
  rw [cochainPairing_add_left, cochainPairing_add_right]
  simp_rw [cochainPairing_sum_left, cochainPairing_sum_right]
  apply congrArg₂ (fun a b : ℝ => a + b)
  · apply Finset.sum_congr rfl
    intro r hr
    have hmul :
        cochainPairing N
          (cochainMultiply N (fun x => ξ x r)
            (cochainBackwardAverage N r (forwardSite N r ψ))) φ =
        cochainPairing N ψ
          (-backwardSite N r
            (cochainForwardAverage N r
              (cochainMultiply N (fun x => ξ x r) φ))) := by
      calc
        _ = cochainPairing N
              (cochainBackwardAverage N r (forwardSite N r ψ))
              (cochainMultiply N (fun x => ξ x r) φ) :=
            cochainMultiply_adjoint N _ _ _
        _ = cochainPairing N (forwardSite N r ψ)
              (cochainForwardAverage N r
                (cochainMultiply N (fun x => ξ x r) φ)) :=
            cochainBackwardAverage_adjoint N _ _ _
        _ = -cochainPairing N ψ
              (backwardSite N r
                (cochainForwardAverage N r
                  (cochainMultiply N (fun x => ξ x r) φ))) :=
            forwardSite_adjoint N _ _ _
        _ = cochainPairing N ψ
              (-backwardSite N r
                (cochainForwardAverage N r
                  (cochainMultiply N (fun x => ξ x r) φ))) := by
            calc
              _ = -cochainPairing N (backwardSite N r
                    (cochainForwardAverage N r
                      (cochainMultiply N (fun x => ξ x r) φ))) ψ := by
                    rw [cochainPairing_symm]
              _ = cochainPairing N
                    (-backwardSite N r
                      (cochainForwardAverage N r
                        (cochainMultiply N (fun x => ξ x r) φ))) ψ := by
                    rw [cochainPairing_neg_left]
              _ = _ := cochainPairing_symm N _ _
    exact hmul
  · apply Finset.sum_congr rfl
    intro s hs
    apply Finset.sum_congr rfl
    intro r hr
    simpa [cochainFluxForward] using
      (cochainFluxForward_adjoint N
        (forwardDifference N s (fun x => ξ x r)) s r ψ φ)

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

/-- Explicit L=3 instance of the graded corner-distance control. -/
theorem periodThree_gradedH_corner_distance_two
    (e : ArchiveRolePhaseGroup 1 → ℝ) (s r : Role) (hsr : s ≠ r)
    (ψ : ArchiveCochain 1) (x : ArchiveRolePhaseGroup 1)
    (S : ArchiveFockState) :
    cochainFluxForward 1 e s r ψ (x, S) =
      e x * (cochainCarEnd 1 s r ψ (roleTranslatePlus 1 s x, S) +
        cochainCarEnd 1 s r ψ
          (roleTranslateMinus 1 r (roleTranslatePlus 1 s x), S)) / 2 ∧
      roleTranslateMinus 1 r (roleTranslatePlus 1 s x) ≠ x ∧
      roleTranslateMinus 1 r (roleTranslatePlus 1 s x) ≠
        roleTranslatePlus 1 s x :=
  gradedH_requires_corner_distance_two 1 e s r hsr ψ x S

/-- L=3 sparse diagonal coframe used to probe the scalar sector one site away. -/
def periodThreeOffsiteCoframe : LocalCoframeField 1 :=
  fun y s r => if y = 0 ∧ s = A ∧ r = A then 1 else 0

/-- A scalar vacuum amplitude supported at the forward A-neighbor of the origin. -/
def periodThreeOffsiteScalar : ArchiveCochain 1 :=
  fun p => if p.1 = roleTranslatePlus 1 A 0 ∧ p.2 = fockVacuumState then 1 else 0

/-- At period three the first jet has a nonzero off-site scalar response. -/
theorem periodThree_offsite_scalar_response :
    scalarComponent 1
      (flatStaggeredH 1 periodThreeOffsiteCoframe periodThreeOffsiteScalar) 0 =
        (1 / 2 : ℝ) := by
  norm_num [scalarComponent, flatStaggeredH, periodThreeOffsiteCoframe,
    periodThreeOffsiteScalar, cochainLinkSymmetric, cochainFluxForward,
    cochainFluxAdjoint, cochainMultiply, cochainForwardShift,
    cochainBackwardShift, cochainBackwardAverage, cochainForwardAverage,
    cochainCarEnd, backwardAverage, carEnd, carCreate, carAnnihilate,
    roleTranslatePlus, roleTranslateMinus, roleTranslate, roleStep,
    roleDelta, A, fockVacuumState]
  have hstep_eq : ∀ r : Role, roleStep 1 r = roleStep 1 A ↔ r = A := by
    intro r
    constructor
    · intro h
      by_contra hne
      have hv := congrFun h A
      have hAr : A ≠ r := Ne.symm hne
      simp only [roleStep, if_neg hAr, if_pos] at hv
      have h01 : (0 : ZMod (archiveFibers 1)) ≠ 1 := by decide
      exact h01 hv
    · rintro rfl
      rfl
  have hterm : ∀ r : Role,
      ((if roleStep 1 r = roleStep 1 A then
          (if r = A then (1 : ℝ) else 0) else 0) +
        if -roleStep 1 r = roleStep 1 A then
          (if roleStep 1 r = 0 ∧ r = A then (1 : ℝ) else 0) else 0) / 2 =
        if r = A then (1 / 2 : ℝ) else 0 := by
    intro r
    by_cases hr : r = A
    · subst r
      have hnonzero : roleStep 1 A ≠ 0 := roleStep_ne_zero 1 A
      simp [hnonzero]
    · have hneq : roleStep 1 r ≠ roleStep 1 A :=
        (hstep_eq r).not.mpr hr
      simp [hneq, hr]
  calc
    _ = ∑ r : Role, if r = A then (1 / 2 : ℝ) else 0 := by
      apply Finset.sum_congr rfl
      intro r hr
      exact hterm r
    _ = 1 / 2 := by simp

/-- Constant A one-form amplitude on the period-two carrier. -/
def periodTwoOneFormProbe : ArchiveCochain 0 :=
  fun p => if p.2 = singletonFockState A then 1 else 0

private theorem carEnd_singleton_A_diagonal (s r : Role) :
    carEnd s r (singletonFockState A) (singletonFockState A) =
      if s = A ∧ r = A then (1 : ℝ) else 0 := by
  have hint : ∀ s r : Role,
      carEndInt s r (singletonFockState A) (singletonFockState A) =
        if s = A ∧ r = A then (1 : ℤ) else 0 := by
    native_decide
  rw [carEnd_eq_intCast, hint s r]
  split_ifs <;> norm_num

private theorem cochainCarEnd_supported_singleton_A (N : ℕ)
    (ψ : ArchiveCochain N)
    (hψ : ∀ x S, S ≠ singletonFockState A → ψ (x, S) = 0)
    (s r : Role) (x : ArchiveRolePhaseGroup N) :
    cochainCarEnd N s r ψ (x, singletonFockState A) =
      (if s = A ∧ r = A then (1 : ℝ) else 0) *
        ψ (x, singletonFockState A) := by
  unfold cochainCarEnd
  rw [Finset.sum_eq_single (singletonFockState A)]
  · simp [carEnd_singleton_A_diagonal]
  · intro ket hket hne
    rw [hψ x ket hne]
    ring
  · simp

/-- The centered Nyquist coframe remains visible in the actual one-form energy
kernel, despite its centered solder/metric blindness. -/
theorem centeredNyquist_nonzero_H_oneForm :
    (∀ x : ArchiveRolePhaseGroup 0,
      centeredCoframeMatrix 0 periodTwoNyquistCoframe x = 0) ∧
    (∀ (t : ℝ) (x : ArchiveRolePhaseGroup 0),
      solderMetricMatrix 0 (t • periodTwoNyquistCoframe) x = roleLorentzMetric) ∧
    flatStaggeredH 0 periodTwoNyquistCoframe periodTwoOneFormProbe
      (0, singletonFockState A) = 2 := by
  refine ⟨periodTwoNyquist_centeredCoframe_zero,
    periodTwo_centeredSolder_constant, ?_⟩
  have hprobe : ∀ x S, S ≠ singletonFockState A →
      periodTwoOneFormProbe (x, S) = 0 := by
    intro x S hS
    simp [periodTwoOneFormProbe, hS]
  have hcar (s r : Role) (x : ArchiveRolePhaseGroup 0) :
      cochainCarEnd 0 s r periodTwoOneFormProbe
        (x, singletonFockState A) =
        if s = A ∧ r = A then (1 : ℝ) else 0 := by
    rw [cochainCarEnd_supported_singleton_A 0 _ hprobe]
    simp [periodTwoOneFormProbe]
  have hlink (r : Role) :
      cochainLinkSymmetric 0 r (fun x => periodTwoNyquistCoframe x r r)
        periodTwoOneFormProbe (0, singletonFockState A) = 0 := by
    have hM := congrArg (fun M : Matrix Role Role ℝ => M r r)
      (periodTwoNyquist_centeredCoframe_zero
        (0 : ArchiveRolePhaseGroup 0))
    simpa [centeredCoframeMatrix, cochainLinkSymmetric,
      periodTwoOneFormProbe, backwardAverage] using hM
  have hforward (s r : Role) :
      cochainFluxForward 0 (fun x => periodTwoNyquistCoframe x s r) s r
        periodTwoOneFormProbe (0, singletonFockState A) =
        periodTwoNyquistCoframe 0 s r *
          (if s = A ∧ r = A then (1 : ℝ) else 0) := by
    rw [cochainFluxForward_corner_expansion]
    rw [hcar, hcar]
    ring
  have hf : (∑ s : Role, ∑ r : Role,
      cochainFluxForward 0 (fun x => periodTwoNyquistCoframe x s r) s r
        periodTwoOneFormProbe (0, singletonFockState A)) = -2 := by
    simp_rw [hforward]
    rw [Finset.sum_eq_single A]
    · rw [Finset.sum_eq_single A]
      · norm_num [periodTwoNyquistCoframe]
      · intro r hr hne
        simp [periodTwoNyquistCoframe, hne]
      · simp
    · intro s hs hne
      simp [periodTwoNyquistCoframe, hne]
    · simp
  have hadjoint (s r : Role) :
      cochainFluxAdjoint 0 (fun x => periodTwoNyquistCoframe x s r) s r
        periodTwoOneFormProbe (0, singletonFockState A) = 0 := by
    let q := cochainForwardAverage 0 r
      (cochainBackwardShift 0 s
        (cochainMultiply 0 (fun x => periodTwoNyquistCoframe x s r)
          periodTwoOneFormProbe))
    have hq : ∀ x S, S ≠ singletonFockState A → q (x, S) = 0 := by
      intro x S hS
      simp [q, cochainForwardAverage, cochainBackwardShift,
        cochainMultiply, periodTwoOneFormProbe, hS]
    change cochainCarEnd 0 r s q (0, singletonFockState A) = 0
    rw [cochainCarEnd_supported_singleton_A 0 q hq r s 0]
    by_cases hsr : r = A ∧ s = A
    · rcases hsr with ⟨rfl, rfl⟩
      have hM := congrArg (fun M : Matrix Role Role ℝ => M A A)
        (periodTwoNyquist_centeredCoframe_zero
          (0 : ArchiveRolePhaseGroup 0))
      have hval : q (0, singletonFockState A) = 0 := by
        simpa [q, cochainForwardAverage, cochainBackwardShift,
          cochainMultiply, periodTwoOneFormProbe, centeredCoframeMatrix,
          backwardAverage, roleTranslateMinus, roleTranslatePlus,
          roleTranslate, add_comm] using hM
      simp [hval]
    · simp [hsr]
  change (∑ r : Role,
      cochainLinkSymmetric 0 r (fun x => periodTwoNyquistCoframe x r r)
        periodTwoOneFormProbe (0, singletonFockState A)) -
      (∑ s : Role, ∑ r : Role,
        (cochainFluxForward 0 (fun x => periodTwoNyquistCoframe x s r) s r
          periodTwoOneFormProbe (0, singletonFockState A) +
         cochainFluxAdjoint 0 (fun x => periodTwoNyquistCoframe x s r) s r
          periodTwoOneFormProbe (0, singletonFockState A))) = 2
  simp [hlink, hadjoint, hf]

/-- The first jet cannot be recovered from the full centered solder metric
field: the zero coframe and the period-two Nyquist coframe have the same metric
field but different actions on a one-form probe. -/
theorem no_centeredMetricFactorization_firstJet :
    ¬ ∃ K : (ArchiveRolePhaseGroup 0 → Matrix Role Role ℝ) →
        ArchiveCochain 0 → ArchiveCochain 0,
      ∀ (e : LocalCoframeField 0) (ψ : ArchiveCochain 0),
        flatStaggeredH 0 e ψ =
          K (fun x => solderMetricMatrix 0 e x) ψ := by
  rintro ⟨K, hK⟩
  have hmetric :
      (fun x => solderMetricMatrix 0 periodTwoNyquistCoframe x) =
        (fun x => solderMetricMatrix 0 (0 : LocalCoframeField 0) x) := by
    funext x
    calc
      solderMetricMatrix 0 periodTwoNyquistCoframe x = roleLorentzMetric := by
        simpa using periodTwo_centeredSolder_constant 1 x
      _ = solderMetricMatrix 0 (0 : LocalCoframeField 0) x := by
        simpa using (periodTwo_centeredSolder_constant 0 x).symm
  have hsame : flatStaggeredH 0 periodTwoNyquistCoframe periodTwoOneFormProbe =
      flatStaggeredH 0 0 periodTwoOneFormProbe := by
    calc
      flatStaggeredH 0 periodTwoNyquistCoframe periodTwoOneFormProbe =
          K (fun x => solderMetricMatrix 0 periodTwoNyquistCoframe x)
            periodTwoOneFormProbe := hK _ _
      _ = K (fun x => solderMetricMatrix 0 (0 : LocalCoframeField 0) x)
            periodTwoOneFormProbe := by rw [hmetric]
      _ = flatStaggeredH 0 0 periodTwoOneFormProbe := (hK _ _).symm
  have hvalue := congrFun hsame (0, singletonFockState A)
  have hnonzero := centeredNyquist_nonzero_H_oneForm.2.2
  have hzero : flatStaggeredH 0 0 periodTwoOneFormProbe
      (0, singletonFockState A) = 0 := by
    simp [flatStaggeredH_zero]
  rw [hnonzero, hzero] at hvalue
  norm_num at hvalue

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
theorem fluxEnergy_riesz_unique (N k : ℕ) (hk : k ≤ 4)
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
      rw [algebraicComplementPairing_sub_right_eval N k hk φ]
      rw [hz φ, fluxEnergy_Riesz_abstractDual_represents]
      ring
    have hsep := (algebraicComplementPairing_perfect N k hk).2
      (z - fluxEnergy_Riesz_abstractDual N k hk e ψ) hzero
    exact sub_eq_zero.mp hsep

end

end D0.Geometry

namespace D0.Geometry
open D0 Matrix
open scoped BigOperators

noncomputable section

private abbrev FluxBasis (N : ℕ) := ArchiveCochainBasis N

private local instance (N : ℕ) : NormedRing (Matrix (FluxBasis N) (FluxBasis N) ℝ) :=
  Matrix.linftyOpNormedRing
private local instance (N : ℕ) : NormedSpace ℝ (Matrix (FluxBasis N) (FluxBasis N) ℝ) :=
  Matrix.linftyOpNormedSpace

private def fluxShiftPlus (N : ℕ) (r : Role) : Matrix (FluxBasis N) (FluxBasis N) ℝ :=
  fun p q => if q = (roleTranslatePlus N r p.1, p.2) then 1 else 0
private def fluxShiftMinus (N : ℕ) (r : Role) : Matrix (FluxBasis N) (FluxBasis N) ℝ :=
  fun p q => if q = (roleTranslateMinus N r p.1, p.2) then 1 else 0
private def fluxMultiply (N : ℕ) (m : ArchiveRolePhaseGroup N → ℝ) :
    Matrix (FluxBasis N) (FluxBasis N) ℝ :=
  Matrix.diagonal (fun p => m p.1)
private def fluxCAR (N : ℕ) (s r : Role) : Matrix (FluxBasis N) (FluxBasis N) ℝ :=
  fun p q => if p.1 = q.1 then carEnd s r p.2 q.2 else 0

private theorem fluxShiftPlus_apply (N : ℕ) (r : Role) (ψ : ArchiveCochain N) :
    fluxShiftPlus N r *ᵥ ψ = cochainForwardShift N r ψ := by
  funext p
  simp [fluxShiftPlus, cochainForwardShift, Matrix.mulVec, dotProduct]

private theorem fluxShiftMinus_apply (N : ℕ) (r : Role) (ψ : ArchiveCochain N) :
    fluxShiftMinus N r *ᵥ ψ = cochainBackwardShift N r ψ := by
  funext p
  simp [fluxShiftMinus, cochainBackwardShift, Matrix.mulVec, dotProduct]

private theorem fluxMultiply_apply (N : ℕ) (m : ArchiveRolePhaseGroup N → ℝ)
    (ψ : ArchiveCochain N) :
    fluxMultiply N m *ᵥ ψ = cochainMultiply N m ψ := by
  funext p
  simp [fluxMultiply, cochainMultiply, Matrix.mulVec, dotProduct, Matrix.diagonal]

private theorem fluxCAR_apply (N : ℕ) (s r : Role) (ψ : ArchiveCochain N) :
    fluxCAR N s r *ᵥ ψ = cochainCarEnd N s r ψ := by
  funext p
  simp [fluxCAR, cochainCarEnd, Matrix.mulVec, dotProduct,
    Fintype.sum_prod_type]

private theorem fluxShiftPlus_norm_le (N : ℕ) (r : Role) :
    ‖fluxShiftPlus N r‖ ≤ 1 := by
  rw [Matrix.linfty_opNorm_def]
  norm_cast
  apply Finset.sup_le
  intro p hp
  simp only [fluxShiftPlus]
  simp_rw [apply_ite (fun x : ℝ => ‖x‖₊)]
  simp

private theorem fluxShiftMinus_norm_le (N : ℕ) (r : Role) :
    ‖fluxShiftMinus N r‖ ≤ 1 := by
  rw [Matrix.linfty_opNorm_def]
  norm_cast
  apply Finset.sup_le
  intro p hp
  simp only [fluxShiftMinus]
  simp_rw [apply_ite (fun x : ℝ => ‖x‖₊)]
  simp

private theorem fluxMultiply_norm_le (N : ℕ) (m : ArchiveRolePhaseGroup N → ℝ)
    (ε : ℝ) (hm : ∀ x, |m x| ≤ ε) : ‖fluxMultiply N m‖ ≤ ε := by
  rw [fluxMultiply, Matrix.linfty_opNorm_diagonal, Pi.norm_def]
  have hε : 0 ≤ ε := (abs_nonneg (m 0)).trans (hm 0)
  rw [← Real.coe_toNNReal ε hε]
  norm_cast
  apply Finset.sup_le
  intro p hp
  apply NNReal.coe_le_coe.mp
  simpa [Real.norm_eq_abs, Real.coe_toNNReal, hε] using hm p.1

private theorem carAnnihilate_abs_le_one (r : Role) (bra ket : ArchiveFockState) :
    |carAnnihilate r bra ket| ≤ 1 := by
  unfold carAnnihilate jwPhase
  split_ifs <;> norm_num

private theorem carCreate_abs_le_one (r : Role) (bra ket : ArchiveFockState) :
    |carCreate r bra ket| ≤ 1 := by
  simpa [carCreate] using carAnnihilate_abs_le_one r ket bra

private theorem carEnd_abs_le_sixteen (s r : Role) (bra ket : ArchiveFockState) :
    |carEnd s r bra ket| ≤ 16 := by
  unfold carEnd
  calc
    |∑ mid : ArchiveFockState, carCreate s bra mid * carAnnihilate r mid ket| ≤
        ∑ mid : ArchiveFockState,
          |carCreate s bra mid * carAnnihilate r mid ket| :=
            Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ _mid : ArchiveFockState, (1 : ℝ) := by
      apply Finset.sum_le_sum
      intro mid hmid
      rw [abs_mul]
      have hc := carCreate_abs_le_one s bra mid
      have ha := carAnnihilate_abs_le_one r mid ket
      nlinarith [mul_nonneg (abs_nonneg (carCreate s bra mid))
        (sub_nonneg.mpr ha)]
    _ = 16 := by simp [card_archive_fock_state]

private theorem fluxCAR_norm_le (N : ℕ) (s r : Role) : ‖fluxCAR N s r‖ ≤ 256 := by
  rw [Matrix.linfty_opNorm_def]
  norm_cast
  apply Finset.sup_le
  intro p hp
  change (∑ q : ArchiveRolePhaseGroup N × ArchiveFockState,
    ‖if p.1 = q.1 then carEnd s r p.2 q.2 else 0‖₊) ≤ 256
  rw [Fintype.sum_prod_type]
  simp_rw [apply_ite (fun x : ℝ => ‖x‖₊)]
  simp only [nnnorm_zero]
  rw [Finset.sum_comm]
  simp
  calc
    (∑ ket : ArchiveFockState, ‖carEnd s r p.2 ket‖₊) ≤
        (∑ ket : ArchiveFockState, (16 : NNReal)) := by
          apply Finset.sum_le_sum
          intro ket hket
          apply NNReal.coe_le_coe.mp
          simpa [Real.norm_eq_abs] using carEnd_abs_le_sixteen s r p.2 ket
    _ = 256 := by simp [card_archive_fock_state]; norm_num

private def fluxAvgMinus (N : ℕ) (r : Role) : Matrix (FluxBasis N) (FluxBasis N) ℝ :=
  (1 / 2 : ℝ) • (1 + fluxShiftMinus N r)
private def fluxAvgPlus (N : ℕ) (r : Role) : Matrix (FluxBasis N) (FluxBasis N) ℝ :=
  (1 / 2 : ℝ) • (1 + fluxShiftPlus N r)

private theorem fluxAvgMinus_apply (N : ℕ) (r : Role) (ψ : ArchiveCochain N) :
    fluxAvgMinus N r *ᵥ ψ = cochainBackwardAverage N r ψ := by
  funext p
  simp [fluxAvgMinus, Matrix.smul_mulVec, Matrix.add_mulVec,
    fluxShiftMinus_apply, cochainBackwardShift, cochainBackwardAverage, backwardAverage,
    Matrix.one_mulVec, Pi.smul_apply, smul_eq_mul]
  ring

private theorem fluxAvgPlus_apply (N : ℕ) (r : Role) (ψ : ArchiveCochain N) :
    fluxAvgPlus N r *ᵥ ψ = cochainForwardAverage N r ψ := by
  funext p
  simp [fluxAvgPlus, Matrix.smul_mulVec, Matrix.add_mulVec,
    fluxShiftPlus_apply, cochainForwardShift, cochainForwardAverage,
    Matrix.one_mulVec, Pi.smul_apply, smul_eq_mul]
  ring

private theorem fluxAvgMinus_norm_le (N : ℕ) (r : Role) : ‖fluxAvgMinus N r‖ ≤ 1 := by
  unfold fluxAvgMinus
  calc
    ‖(1 / 2 : ℝ) • (1 + fluxShiftMinus N r)‖ =
        (1 / 2 : ℝ) * ‖1 + fluxShiftMinus N r‖ := by rw [norm_smul]; norm_num
    _ ≤ (1 / 2 : ℝ) * (‖(1 : Matrix (FluxBasis N) (FluxBasis N) ℝ)‖ +
        ‖fluxShiftMinus N r‖) := by gcongr; exact norm_add_le _ _
    _ ≤ 1 := by have h := fluxShiftMinus_norm_le N r; norm_num at *; linarith

private theorem fluxAvgPlus_norm_le (N : ℕ) (r : Role) : ‖fluxAvgPlus N r‖ ≤ 1 := by
  unfold fluxAvgPlus
  calc
    ‖(1 / 2 : ℝ) • (1 + fluxShiftPlus N r)‖ =
        (1 / 2 : ℝ) * ‖1 + fluxShiftPlus N r‖ := by rw [norm_smul]; norm_num
    _ ≤ (1 / 2 : ℝ) * (‖(1 : Matrix (FluxBasis N) (FluxBasis N) ℝ)‖ +
        ‖fluxShiftPlus N r‖) := by gcongr; exact norm_add_le _ _
    _ ≤ 1 := by have h := fluxShiftPlus_norm_le N r; norm_num at *; linarith

private def fluxLinkMatrix (N : ℕ) (r : Role)
    (m : ArchiveRolePhaseGroup N → ℝ) : Matrix (FluxBasis N) (FluxBasis N) ℝ :=
  (1 / 2 : ℝ) •
    (fluxMultiply N m * fluxShiftPlus N r + fluxShiftMinus N r * fluxMultiply N m)

private def fluxForwardMatrix (N : ℕ) (s r : Role)
    (m : ArchiveRolePhaseGroup N → ℝ) : Matrix (FluxBasis N) (FluxBasis N) ℝ :=
  fluxMultiply N m * fluxShiftPlus N s * fluxAvgMinus N r * fluxCAR N s r

private def fluxAdjointMatrix (N : ℕ) (s r : Role)
    (m : ArchiveRolePhaseGroup N → ℝ) : Matrix (FluxBasis N) (FluxBasis N) ℝ :=
  fluxCAR N r s * fluxAvgPlus N r * fluxShiftMinus N s * fluxMultiply N m

def fluxHMatrix (N : ℕ) (e : LocalCoframeField N) :
    Matrix (FluxBasis N) (FluxBasis N) ℝ :=
  (∑ r : Role, fluxLinkMatrix N r (fun x => e x r r)) -
    ∑ s : Role, ∑ r : Role,
      (fluxForwardMatrix N s r (fun x => e x s r) +
        fluxAdjointMatrix N s r (fun x => e x s r))

private theorem fluxLinkMatrix_apply (N : ℕ) (r : Role)
    (m : ArchiveRolePhaseGroup N → ℝ) (ψ : ArchiveCochain N) :
    fluxLinkMatrix N r m *ᵥ ψ = cochainLinkSymmetric N r m ψ := by
  funext p
  simp [fluxLinkMatrix, Matrix.smul_mulVec, Matrix.add_mulVec,
    ← Matrix.mulVec_mulVec, fluxMultiply_apply, fluxShiftPlus_apply,
    fluxShiftMinus_apply, cochainLinkSymmetric, cochainMultiply,
    cochainForwardShift, cochainBackwardShift, Pi.smul_apply, smul_eq_mul]
  ring

private theorem fluxForwardMatrix_apply (N : ℕ) (s r : Role)
    (m : ArchiveRolePhaseGroup N → ℝ) (ψ : ArchiveCochain N) :
    fluxForwardMatrix N s r m *ᵥ ψ = cochainFluxForward N m s r ψ := by
  simp [fluxForwardMatrix, ← Matrix.mulVec_mulVec, fluxMultiply_apply,
    fluxShiftPlus_apply, fluxAvgMinus_apply, fluxCAR_apply,
    cochainFluxForward]

private theorem fluxAdjointMatrix_apply (N : ℕ) (s r : Role)
    (m : ArchiveRolePhaseGroup N → ℝ) (ψ : ArchiveCochain N) :
    fluxAdjointMatrix N s r m *ᵥ ψ = cochainFluxAdjoint N m s r ψ := by
  simp [fluxAdjointMatrix, ← Matrix.mulVec_mulVec, fluxMultiply_apply,
    fluxShiftMinus_apply, fluxAvgPlus_apply, fluxCAR_apply,
    cochainFluxAdjoint]

private theorem fluxMatrix_sum_mulVec {ι : Type*} [DecidableEq ι]
    (f : ι → Matrix (FluxBasis N) (FluxBasis N) ℝ) (S : Finset ι)
    (ψ : ArchiveCochain N) :
    (∑ i ∈ S, f i) *ᵥ ψ = ∑ i ∈ S, f i *ᵥ ψ := by
  classical
  induction S using Finset.induction_on with
  | empty => simp
  | @insert a S ha ih => simp [ha, ih, Matrix.add_mulVec]

theorem fluxHMatrix_apply (N : ℕ) (e : LocalCoframeField N)
    (ψ : ArchiveCochain N) :
    fluxHMatrix N e *ᵥ ψ = flatStaggeredH N e ψ := by
  funext p
  simp [fluxHMatrix, flatStaggeredH, Matrix.sub_mulVec,
    Matrix.sum_mulVec, Matrix.add_mulVec,
    fluxLinkMatrix_apply, fluxForwardMatrix_apply, fluxAdjointMatrix_apply]

private theorem fluxLinkMatrix_norm_le (N : ℕ) (r : Role)
    (m : ArchiveRolePhaseGroup N → ℝ) (ε : ℝ)
    (hm : ∀ x, |m x| ≤ ε) : ‖fluxLinkMatrix N r m‖ ≤ ε := by
  have hε : 0 ≤ ε := (abs_nonneg (m 0)).trans (hm 0)
  have hM := fluxMultiply_norm_le N m ε hm
  have hU := fluxShiftPlus_norm_le N r
  have hV := fluxShiftMinus_norm_le N r
  have h1 : ‖fluxMultiply N m * fluxShiftPlus N r‖ ≤ ε := by
    calc
      _ ≤ ‖fluxMultiply N m‖ * ‖fluxShiftPlus N r‖ := norm_mul_le _ _
      _ ≤ ε * 1 := by gcongr
      _ = ε := by ring
  have h2 : ‖fluxShiftMinus N r * fluxMultiply N m‖ ≤ ε := by
    calc
      _ ≤ ‖fluxShiftMinus N r‖ * ‖fluxMultiply N m‖ := norm_mul_le _ _
      _ ≤ 1 * ε := by gcongr
      _ = ε := by ring
  unfold fluxLinkMatrix
  calc
    ‖(1 / 2 : ℝ) • (fluxMultiply N m * fluxShiftPlus N r +
      fluxShiftMinus N r * fluxMultiply N m)‖ =
      (1 / 2 : ℝ) * ‖fluxMultiply N m * fluxShiftPlus N r +
      fluxShiftMinus N r * fluxMultiply N m‖ := by rw [norm_smul]; norm_num
    _ ≤ (1 / 2 : ℝ) * (‖fluxMultiply N m * fluxShiftPlus N r‖ +
      ‖fluxShiftMinus N r * fluxMultiply N m‖) := by
        gcongr; exact norm_add_le _ _
    _ ≤ ε := by linarith

private theorem fluxForwardMatrix_norm_le (N : ℕ) (s r : Role)
    (m : ArchiveRolePhaseGroup N → ℝ) (ε : ℝ)
    (hm : ∀ x, |m x| ≤ ε) : ‖fluxForwardMatrix N s r m‖ ≤ 256 * ε := by
  have hε : 0 ≤ ε := (abs_nonneg (m 0)).trans (hm 0)
  unfold fluxForwardMatrix
  calc
    _ ≤ ‖fluxMultiply N m‖ * ‖fluxShiftPlus N s‖ *
          ‖fluxAvgMinus N r‖ * ‖fluxCAR N s r‖ := by
          calc
            _ ≤ ‖fluxMultiply N m * fluxShiftPlus N s * fluxAvgMinus N r‖ *
                ‖fluxCAR N s r‖ := norm_mul_le _ _
            _ ≤ ‖fluxMultiply N m * fluxShiftPlus N s‖ *
                ‖fluxAvgMinus N r‖ * ‖fluxCAR N s r‖ := by
                  gcongr; exact norm_mul_le _ _
            _ ≤ _ := by gcongr; exact norm_mul_le _ _
    _ ≤ ε * 1 * 1 * 256 := by
      gcongr
      · exact fluxMultiply_norm_le N m ε hm
      · exact fluxShiftPlus_norm_le N s
      · exact fluxAvgMinus_norm_le N r
      · exact fluxCAR_norm_le N s r
    _ = 256 * ε := by ring

private theorem fluxAdjointMatrix_norm_le (N : ℕ) (s r : Role)
    (m : ArchiveRolePhaseGroup N → ℝ) (ε : ℝ)
    (hm : ∀ x, |m x| ≤ ε) : ‖fluxAdjointMatrix N s r m‖ ≤ 256 * ε := by
  have hε : 0 ≤ ε := (abs_nonneg (m 0)).trans (hm 0)
  unfold fluxAdjointMatrix
  calc
    _ ≤ ‖fluxCAR N r s‖ * ‖fluxAvgPlus N r‖ *
          ‖fluxShiftMinus N s‖ * ‖fluxMultiply N m‖ := by
          calc
            _ ≤ ‖fluxCAR N r s * fluxAvgPlus N r * fluxShiftMinus N s‖ *
                ‖fluxMultiply N m‖ := norm_mul_le _ _
            _ ≤ ‖fluxCAR N r s * fluxAvgPlus N r‖ *
                ‖fluxShiftMinus N s‖ * ‖fluxMultiply N m‖ := by
                  gcongr; exact norm_mul_le _ _
            _ ≤ _ := by gcongr; exact norm_mul_le _ _
    _ ≤ 256 * 1 * 1 * ε := by
      gcongr
      · exact fluxCAR_norm_le N r s
      · exact fluxAvgPlus_norm_le N r
      · exact fluxShiftMinus_norm_le N s
      · exact fluxMultiply_norm_le N m ε hm
    _ = 256 * ε := by ring

theorem fluxHMatrix_norm_le (N : ℕ) (e : LocalCoframeField N)
    (ε : ℝ) (he : ∀ x s r, |e x s r| ≤ ε) :
    ‖fluxHMatrix N e‖ ≤ 8196 * ε := by
  have hε : 0 ≤ ε := (abs_nonneg (e 0 0 0)).trans (he 0 0 0)
  have hlinks : ‖∑ r : Role, fluxLinkMatrix N r (fun x => e x r r)‖ ≤ 4 * ε := by
    calc
      _ ≤ ∑ r : Role, ‖fluxLinkMatrix N r (fun x => e x r r)‖ := norm_sum_le _ _
      _ ≤ ∑ _r : Role, ε := by
        apply Finset.sum_le_sum
        intro r hr
        exact fluxLinkMatrix_norm_le N r (fun x => e x r r) ε (fun x => he x r r)
      _ = 4 * ε := by simp [card_role]
  have hcross : ‖∑ s : Role, ∑ r : Role,
      (fluxForwardMatrix N s r (fun x => e x s r) +
        fluxAdjointMatrix N s r (fun x => e x s r))‖ ≤ 8192 * ε := by
    calc
      _ ≤ ∑ s : Role, ∑ r : Role,
          ‖fluxForwardMatrix N s r (fun x => e x s r) +
            fluxAdjointMatrix N s r (fun x => e x s r)‖ := by
              apply (norm_sum_le _ _).trans
              apply Finset.sum_le_sum
              intro s hs
              exact norm_sum_le _ _
      _ ≤ ∑ _s : Role, ∑ _r : Role, 512 * ε := by
        apply Finset.sum_le_sum
        intro s hs
        apply Finset.sum_le_sum
        intro r hr
        have hf := fluxForwardMatrix_norm_le N s r (fun x => e x s r) ε (fun x => he x s r)
        have ha := fluxAdjointMatrix_norm_le N s r (fun x => e x s r) ε (fun x => he x s r)
        linarith [norm_add_le (fluxForwardMatrix N s r (fun x => e x s r))
          (fluxAdjointMatrix N s r (fun x => e x s r))]
      _ = 8192 * ε := by simp [card_role]; ring
  unfold fluxHMatrix
  linarith [norm_sub_le (∑ r : Role, fluxLinkMatrix N r (fun x => e x r r))
    (∑ s : Role, ∑ r : Role,
      (fluxForwardMatrix N s r (fun x => e x s r) +
        fluxAdjointMatrix N s r (fun x => e x s r)))]

private theorem matrix_quad_row_bound {ι : Type*} [Fintype ι] [DecidableEq ι]
    (A : Matrix ι ι ℝ) (hA : A.IsHermitian) (c : ℝ)
    (hc : ∀ i, ∑ j, |A i j| ≤ c) (v : ι → ℝ) :
    |dotProduct v (A *ᵥ v)| ≤ c * ∑ i, v i ^ 2 := by
  classical
  have hsym : ∀ i j, A i j = A j i := by
    intro i j
    simpa only [star_trivial] using (hA.apply i j).symm
  have hterm : ∀ i j, |A i j * v i * v j| ≤
      |A i j| * ((v i)^2 + (v j)^2) / 2 := by
    intro i j
    have hsq : 2 * (|v i| * |v j|) ≤ (v i)^2 + (v j)^2 := by
      nlinarith [sq_nonneg (|v i| - |v j|), sq_abs (v i), sq_abs (v j)]
    calc
      |A i j * v i * v j| = |A i j| * (|v i| * |v j|) := by rw [abs_mul, abs_mul]; ring
      _ ≤ |A i j| * ((v i)^2 + (v j)^2) / 2 := by
        have h := mul_le_mul_of_nonneg_left hsq (abs_nonneg (A i j))
        nlinarith
  have hsum : |∑ i, ∑ j, A i j * v i * v j| ≤
      ∑ i, ∑ j, |A i j| * ((v i)^2 + (v j)^2) / 2 := by
    calc
      _ ≤ ∑ i, |∑ j, A i j * v i * v j| := Finset.abs_sum_le_sum_abs _ _
      _ ≤ ∑ i, ∑ j, |A i j * v i * v j| := by
        apply Finset.sum_le_sum
        intro i hi
        exact Finset.abs_sum_le_sum_abs _ _
      _ ≤ _ := by
        apply Finset.sum_le_sum
        intro i hi
        apply Finset.sum_le_sum
        intro j hj
        exact hterm i j
  have hsplit : (∑ i, ∑ j, |A i j| * ((v i)^2 + (v j)^2) / 2) =
      ∑ i, (∑ j, |A i j|) * (v i)^2 := by
    have hfirst : (∑ i, ∑ j, |A i j| * (v i)^2) =
        ∑ i, (∑ j, |A i j|) * (v i)^2 := by
      apply Finset.sum_congr rfl
      intro i hi
      rw [Finset.sum_mul]
    have hsecond : (∑ i, ∑ j, |A i j| * (v j)^2) =
        ∑ i, (∑ j, |A i j|) * (v i)^2 := by
      rw [Finset.sum_comm]
      calc
        _ = ∑ i, ∑ j, |A i j| * (v i)^2 := by
          apply Finset.sum_congr rfl
          intro i hi
          apply Finset.sum_congr rfl
          intro j hj
          rw [hsym j i]
        _ = _ := hfirst
    calc
      _ = ((∑ i, ∑ j, |A i j| * (v i)^2) +
          (∑ i, ∑ j, |A i j| * (v j)^2)) / 2 := by
            simp_rw [mul_add, add_div, Finset.sum_add_distrib, Finset.sum_div]
      _ = _ := by rw [hfirst, hsecond]; ring
  have hfinal : (∑ i, (∑ j, |A i j|) * (v i)^2) ≤
      c * ∑ i, (v i)^2 := by
    rw [Finset.mul_sum]
    apply Finset.sum_le_sum
    intro i hi
    exact mul_le_mul_of_nonneg_right (hc i) (sq_nonneg _)
  have hformula : dotProduct v (A *ᵥ v) = ∑ i, ∑ j, A i j * v i * v j := by
    change (∑ i, v i * (∑ j, A i j * v j)) = _
    simp_rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i hi
    apply Finset.sum_congr rfl
    intro j hj
    ring
  rw [hformula]
  exact (hsum.trans_eq hsplit).trans hfinal

private theorem fluxHMatrix_isHermitian (N : ℕ) (e : LocalCoframeField N) :
    (fluxHMatrix N e).IsHermitian := by
  apply Matrix.IsHermitian.ext
  intro p q
  rcases p with ⟨xp, sp⟩
  rcases q with ⟨xq, sq⟩
  have hadj := flatStaggeredH_selfAdjoint N e
    (Pi.single (xq, sq) (1 : ℝ)) (Pi.single (xp, sp) (1 : ℝ))
  rw [← fluxHMatrix_apply, ← fluxHMatrix_apply] at hadj
  simp only [cochainPairing, Matrix.mulVec_single_one, Pi.single_apply,
    Prod.mk.injEq, ite_and] at hadj
  simpa using hadj.symm

private theorem fluxHMatrix_row_bound (N : ℕ) (e : LocalCoframeField N)
    (ε : ℝ) (he : ∀ x s r, |e x s r| ≤ ε) (p : FluxBasis N) :
    (∑ q : FluxBasis N, |fluxHMatrix N e p q|) ≤ 8196 * ε := by
  have hnorm := fluxHMatrix_norm_le N e ε he
  have hrow : (∑ q : FluxBasis N, ‖fluxHMatrix N e p q‖₊) ≤
      (Finset.univ.sup fun i : FluxBasis N =>
        ∑ q : FluxBasis N, ‖fluxHMatrix N e i q‖₊) :=
    Finset.le_sup (f := fun i : FluxBasis N =>
      ∑ q : FluxBasis N, ‖fluxHMatrix N e i q‖₊) (Finset.mem_univ p)
  have hrowReal : (∑ q : FluxBasis N, |fluxHMatrix N e p q|) ≤
      ‖fluxHMatrix N e‖ := by
    rw [Matrix.linfty_opNorm_def]
    have hcast := NNReal.coe_le_coe.mpr hrow
    simpa [NNReal.coe_sum, Real.norm_eq_abs] using hcast
  exact hrowReal.trans hnorm

/-- Uniform finite counting-energy positivity in the small coframe regime. -/
theorem fluxEnergy_small_e_positive (N : ℕ) (e : LocalCoframeField N)
    (ε : ℝ) (he : ∀ x s r, |e x s r| ≤ ε) (hsmall : 8196 * ε < 1)
    (ψ : ArchiveCochain N) (hψ : ψ ≠ 0) : 0 < fluxEnergy N e ψ := by
  have hbase : 0 < ∑ p : FluxBasis N, ψ p ^ 2 := by
    have hnonzero : ∃ p : FluxBasis N, ψ p ≠ 0 := by
      by_contra h
      push Not at h
      exact hψ (funext h)
    obtain ⟨p, hp⟩ := hnonzero
    apply (Finset.sum_pos_iff_of_nonneg (fun q hq => sq_nonneg (ψ q))).mpr
    exact ⟨p, Finset.mem_univ p, sq_pos_of_ne_zero hp⟩
  have hquad := matrix_quad_row_bound (fluxHMatrix N e)
    (fluxHMatrix_isHermitian N e) (8196 * ε)
    (fluxHMatrix_row_bound N e ε he) ψ
  have hlow := (abs_le.mp hquad).1
  have hdot : dotProduct ψ ψ = ∑ p : FluxBasis N, ψ p ^ 2 := by
    simp [dotProduct, pow_two]
  have hpos : 0 < dotProduct ψ (ψ + fluxHMatrix N e *ᵥ ψ) := by
    rw [dotProduct_add, hdot]
    nlinarith [mul_pos (sub_pos.mpr hsmall) hbase]
  have hbridge : cochainPairing N ψ (ψ + flatStaggeredH N e ψ) =
      dotProduct ψ (ψ + fluxHMatrix N e *ᵥ ψ) := by
    rw [fluxHMatrix_apply]
    simp [cochainPairing, dotProduct, Fintype.sum_prod_type]
  have henergy : 0 < 2 * fluxEnergy N e ψ := by
    rw [fluxEnergy_polarization_eq_H, hbridge]
    exact hpos
  linarith

/-- The coframe's finite sup norm is the maximum absolute site/role coefficient. -/
theorem coframe_abs_le_norm (N : ℕ) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) (s r : Role) : |e x s r| ≤ ‖e‖ := by
  simpa [Real.norm_eq_abs] using
    (norm_le_pi_norm (e x s) r).trans
      ((norm_le_pi_norm (e x) s).trans (norm_le_pi_norm e x))

/-- Explicit uniform matrix norm bound with `ε = max |e_s^r(x)|`. -/
theorem fluxHMatrix_norm_le_max (N : ℕ) (e : LocalCoframeField N) :
    ‖fluxHMatrix N e‖ ≤ 8196 * ‖e‖ :=
  fluxHMatrix_norm_le N e ‖e‖ (coframe_abs_le_norm N e)

/-- Positive counting flux energy under the explicit maximum-coefficient threshold. -/
theorem fluxEnergy_small_e_positive_max (N : ℕ) (e : LocalCoframeField N)
    (hsmall : 8196 * ‖e‖ < 1) (ψ : ArchiveCochain N) (hψ : ψ ≠ 0) :
    0 < fluxEnergy N e ψ :=
  fluxEnergy_small_e_positive N e ‖e‖ (coframe_abs_le_norm N e) hsmall ψ hψ

end
end D0.Geometry
