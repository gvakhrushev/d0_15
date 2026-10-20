import D0.Foundation.EndogenousActionQuantum
import D0.Foundation.ObservableCompletionCanonicity
import D0.Geometry.A4DPathWordParentWard
import D0.Geometry.A4DActionGroupoidSecondJet
import D0.Geometry.A4DScalarDeltaSecondJet
import D0.Geometry.A4DScalarAdvectiveGroupoidObstruction
import D0.Geometry.A4DDiscreteEnergyKernel
import D0.Geometry.A4DAffineMatterLiftObstruction
import D0.Geometry.A4DCellHessianTransverseModulus
import D0.Gravity.A4DParentWardStressDescent
import Mathlib.Analysis.Normed.Algebra.MatrixExponential
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Tactic
import Lean

/-! G0: complete fibers of the actual primitive action interface and of
passive/invariant action data. No new physical action is selected. -/
namespace D0.Research.NativeDynamicalOwnership
open D0.Foundation
open D0.Foundation.VerifiabilityNecessity
open D0.Foundation.PopperianBootstrap
open D0.Foundation.EndogenousActionQuantum
open D0.Foundation.ObservableCompletionCanonicity
open D0.Geometry
open D0.Gravity
noncomputable section

abbrev DistinctPair (P : VerificationProtocol) :=
  {xy : P.State × P.State // xy.1 ≠ xy.2}

abbrev ExcessCosts (P : VerificationProtocol) := DistinctPair P → {r : ℝ // 0 ≤ r}

def actionFromExcess (P : VerificationProtocol) (c : ExcessCosts P) :
    ActionProtocol P where
  action x y := if h : x = y then 0 else 1 + (c ⟨(x,y),h⟩).val
  action_refl := by intro x; simp
  action_nontrivial := by
    intro x y h
    simp only [dif_neg h]
    linarith [(c ⟨(x,y),h⟩).property]

def excessFromAction (P : VerificationProtocol) (A : ActionProtocol P) :
    ExcessCosts P := fun xy =>
  ⟨A.action xy.val.1 xy.val.2 - 1, by
    linarith [A.action_nontrivial xy.val.1 xy.val.2 xy.property]⟩

theorem action_ext {P : VerificationProtocol} (A B : ActionProtocol P)
    (h : ∀ x y, A.action x y = B.action x y) : A = B := by
  cases A with
  | mk a ar an =>
    cases B with
    | mk b br bn =>
      have hab : a = b := funext (fun x => funext (h x))
      cases hab
      rfl

theorem excess_action_left_inverse (P : VerificationProtocol) (A : ActionProtocol P) :
    actionFromExcess P (excessFromAction P A) = A := by
  apply action_ext
  intro x y
  by_cases h : x=y
  · subst y
    simp [actionFromExcess, A.action_refl]
  · change (if h' : x = y then (0 : ℝ) else
        1 + (excessFromAction P A ⟨(x,y),h'⟩).val) = A.action x y
    rw [dif_neg h]
    change 1 + (A.action x y - 1) = A.action x y
    ring

theorem excess_action_right_inverse (P : VerificationProtocol) (c : ExcessCosts P) :
    excessFromAction P (actionFromExcess P c) = c := by
  funext xy
  apply Subtype.ext
  change (actionFromExcess P c).action xy.val.1 xy.val.2 - 1 = (c xy).val
  simp only [actionFromExcess, dif_neg xy.property]
  change 1 + (c xy).val - 1 = (c xy).val
  ring

/-- Every actual ActionProtocol is represented, not just a tested subfamily. -/
def completeActionFiber (P : VerificationProtocol) : ActionProtocol P ≃ ExcessCosts P where
  toFun := excessFromAction P
  invFun := actionFromExcess P
  left_inv := excess_action_left_inverse P
  right_inv := excess_action_right_inverse P

theorem canonical_action_has_zero_excess (P : VerificationProtocol) :
    excessFromAction P (canonicalActionProtocol P) = fun _ => ⟨0,le_rfl⟩ := by
  funext xy
  apply Subtype.ext
  change (canonicalActionProtocol P).action xy.val.1 xy.val.2 - 1 = 0
  simp [canonicalActionProtocol, xy.property]

theorem canonical_action_is_least (P : VerificationProtocol)
    (A : ActionProtocol P) (x y : P.State) :
    (canonicalActionProtocol P).action x y ≤ A.action x y := by
  by_cases h : x = y
  · subst y
    simp [canonicalActionProtocol, A.action_refl]
  · simpa [canonicalActionProtocol, h] using A.action_nontrivial x y h

theorem least_action_iff_canonical (P : VerificationProtocol) (A : ActionProtocol P) :
    (∀ (B : ActionProtocol P) x y, A.action x y ≤ B.action x y) ↔
      A = canonicalActionProtocol P := by
  constructor
  · intro h
    apply action_ext
    intro x y
    exact le_antisymm (h _ x y) (canonical_action_is_least P A x y)
  · intro h
    subst A
    exact fun B x y => canonical_action_is_least P B x y

abbrev threeStateProtocol : VerificationProtocol where
  State := Fin 3
  Record := Fin 3
  Line := Bool
  Catalogue := Unit
  stateDecidableEq := inferInstance
  record := id
  compare := fun _ _ x y => decide (x ≠ y)

theorem threeState_killing_test : KillingTest threeStateProtocol where
  prediction_violation := ⟨0,1,by decide⟩
  two_witnesses := ⟨true,false,by decide⟩
  runnable := ⟨()⟩
  verdict := by intro _ _ x y; rfl

def metricCost (x y : Fin 3) : ℝ :=
  if x=y then 0 else if (x=0 ∧ y=2) ∨ (x=2 ∧ y=0) then 2 else 1

def secondAction : ActionProtocol threeStateProtocol where
  action := metricCost
  action_refl := by intro x; simp [metricCost]
  action_nontrivial := by
    intro x y h
    simp only [metricCost, if_neg h]
    split_ifs <;> norm_num

def normalizedMetricCosts (A : ActionProtocol threeStateProtocol) : Prop :=
  (∀ x y, A.action x y = A.action y x) ∧
  (∀ x y z, A.action x z ≤ A.action x y + A.action y z) ∧
  A.action 0 1 = 1

theorem canonical_normalized_metric :
    normalizedMetricCosts (canonicalActionProtocol threeStateProtocol) := by
  constructor
  · intro x y
    by_cases h : x = y
    · subst y; rfl
    · simp [canonicalActionProtocol, h, Ne.symm h]
  constructor
  · intro x y z
    by_cases hxy : x = y
    · subst y; simp [canonicalActionProtocol]
    by_cases hyz : y = z
    · subst z; simp [canonicalActionProtocol]
    simp only [canonicalActionProtocol, if_neg hxy, if_neg hyz]
    split_ifs <;> norm_num
  · norm_num [canonicalActionProtocol, threeStateProtocol, Fin.ext_iff]

theorem second_normalized_metric : normalizedMetricCosts secondAction := by
  constructor
  · intro x y
    fin_cases x <;> fin_cases y <;> norm_num [secondAction,metricCost, threeStateProtocol, Fin.ext_iff]
  constructor
  · intro x y z
    fin_cases x <;> fin_cases y <;> fin_cases z <;> norm_num [secondAction,metricCost, threeStateProtocol, Fin.ext_iff]
  · norm_num [secondAction,metricCost, threeStateProtocol, Fin.ext_iff]

def relativeCost (A : ActionProtocol threeStateProtocol) : ℝ :=
  A.action 0 2 / A.action 0 1

theorem distinct_normalized_action_ratios :
    relativeCost (canonicalActionProtocol threeStateProtocol) = 1 ∧
    relativeCost secondAction = 2 := by
  norm_num [relativeCost,canonicalActionProtocol,secondAction,metricCost, threeStateProtocol, Fin.ext_iff]
  decide

theorem action_ratio_not_m1_forced :
    ¬ ∃ o, M1Forced
      (CompletionForcesReadout normalizedMetricCosts relativeCost) o := by
  apply distinct_readouts_no_m1_forced normalizedMetricCosts relativeCost
    canonical_normalized_metric second_normalized_metric
  rw [distinct_normalized_action_ratios.1,distinct_normalized_action_ratios.2]
  norm_num

theorem action_cost_difference_survives_calibration
    (cal : ExtrinsicCalibration) :
    scaledAction (canonicalActionProtocol threeStateProtocol) cal 0 2 /
      scaledAction (canonicalActionProtocol threeStateProtocol) cal 0 1 = 1 ∧
    scaledAction secondAction cal 0 2 / scaledAction secondAction cal 0 1 = 2 := by
  rw [relative_action_scale_invariant (canonicalActionProtocol threeStateProtocol) cal 0 2 0 1
    (by norm_num [canonicalActionProtocol, threeStateProtocol, Fin.ext_iff])]
  rw [relative_action_scale_invariant secondAction cal 0 2 0 1
    (by norm_num [secondAction,metricCost, threeStateProtocol, Fin.ext_iff])]
  exact distinct_normalized_action_ratios

theorem action_cost_difference_survives_all_relabelings
    (e : Fin 3 ≃ Fin 3) (a : ℝ) :
    ¬ ∀ x y, (canonicalActionProtocol threeStateProtocol).action x y =
      a * secondAction.action (e x) (e y) := by
  intro h
  have h01 : e.symm (0 : Fin 3) ≠ e.symm 1 := e.symm.injective.ne (by decide)
  have h02 : e.symm (0 : Fin 3) ≠ e.symm 2 := e.symm.injective.ne (by decide)
  have h1 := h (e.symm 0) (e.symm 1)
  have h2 := h (e.symm 0) (e.symm 2)
  simp [canonicalActionProtocol,secondAction,metricCost,h01] at h1
  simp [canonicalActionProtocol,secondAction,metricCost,h02] at h2
  linarith

/-- For any declared equivalence relation, the whole invariant-action
fiber is exactly the space of arbitrary functions on the quotient. -/
def InvariantActions {B : Type} (r : Setoid B) :=
  {f : B → ℝ // ∀ x y, r x y → f x = f y}

def completeInvariantActionFiber {B : Type} (r : Setoid B) :
    InvariantActions r ≃ (Quotient r → ℝ) where
  toFun f := Quotient.lift f.val f.property
  invFun f := ⟨fun b => f (Quotient.mk r b),by
    intro x y h
    exact congrArg f (Quotient.sound h)⟩
  left_inv f := by apply Subtype.ext; rfl
  right_inv f := by
    funext q
    exact Quotient.inductionOn q (fun _ => rfl)

def symmetryOrbit {B : Type} (symmetry : B → B) : Setoid B :=
  Relation.EqvGen.setoid (fun x y => y = symmetry x)

theorem invariant_iff_constant_on_symmetry_orbits
    {B : Type} (symmetry : B → B) (f : B → ℝ) :
    (∀ b, f (symmetry b) = f b) ↔
      ∀ x y, (symmetryOrbit symmetry) x y → f x = f y := by
  constructor
  · intro h x y hxy
    induction hxy with
    | rel x y he => subst y; exact (h x).symm
    | refl => rfl
    | symm _ _ _ ih => exact ih.symm
    | trans _ _ _ _ _ ih1 ih2 => exact ih1.trans ih2
  · intro h b
    exact (h b (symmetry b) (Relation.EqvGen.rel _ _ rfl)).symm

theorem arbitrary_profile_of_invariant_observable
    {B : Type} (symmetry : B → B) (q : B → ℝ)
    (hq : ∀ b, q (symmetry b) = q b) (profile : ℝ → ℝ) :
    ∀ b, profile (q (symmetry b)) = profile (q b) := by
  intro b
  rw [hq]

theorem two_profiles_same_nontrivial_symmetry :
    (∀ _b : ℝ × ℝ, (0 : ℝ) = 0) ∧
    (∀ b : ℝ × ℝ, (b.1,-b.2).1 ^ 2 - 1 = b.1 ^ 2 - 1) := by
  constructor <;> intro b <;> rfl

theorem invariant_profiles_different_variations :
    HasDerivAt (fun _ : ℝ => (0 : ℝ)) 0 1 ∧
    HasDerivAt (fun x : ℝ => x^2 - 1) 2 1 := by
  constructor
  · exact hasDerivAt_const 1 0
  · convert (hasDerivAt_pow 2 (1 : ℝ)).sub_const 1 using 1; norm_num

theorem passive_hodge_recovers_seed
    {P D : Type*} [AddCommGroup P] [Module ℝ P]
    [AddCommGroup D] [Module ℝ D]
    (QD : D ≃ₗ[ℝ] D) (QP : P ≃ₗ[ℝ] P) (S : P →ₗ[ℝ] D) :
    movingHodge QD.symm (movingHodge QD S QP) QP.symm = S := by
  ext p
  simp [movingHodge]

theorem passive_hodge_seed_injective
    {P D : Type*} [AddCommGroup P] [Module ℝ P]
    [AddCommGroup D] [Module ℝ D]
    (QD : D ≃ₗ[ℝ] D) (QP : P ≃ₗ[ℝ] P) :
    Function.Injective (fun S : P →ₗ[ℝ] D => movingHodge QD S QP) := by
  intro S T h
  have hh := congrArg (fun U => movingHodge QD.symm U QP.symm) h
  simpa [passive_hodge_recovers_seed] using hh

/-- The actual conditional Ward conclusion follows from its four map
covariance hypotheses alone. Its background-action slot is dispensable. -/
theorem actual_ward_needs_only_map_covariance
    {P0 P1 D3 D4 : Type*}
    [Fintype P0] [Fintype P1] [Fintype D3] [Fintype D4]
    [DecidableEq P0] [DecidableEq P1] [DecidableEq D3] [DecidableEq D4]
    {Background : Type*} (symmetry : Background → Background) (b : Background)
    (e0 : FiniteRealCarrier P0 ≃ₗ[ℝ] Module.Dual ℝ (FiniteRealCarrier D4))
    (e1 : FiniteRealCarrier P1 ≃ₗ[ℝ] Module.Dual ℝ (FiniteRealCarrier D3))
    (Q0 : FiniteRealCarrier P0 ≃ₗ[ℝ] FiniteRealCarrier P0)
    (Q1 : FiniteRealCarrier P1 ≃ₗ[ℝ] FiniteRealCarrier P1)
    (dPof : Background → FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier P1)
    (dDof : Background → FiniteRealCarrier D3 →ₗ[ℝ] FiniteRealCarrier D4)
    (S0of : Background → FiniteRealCarrier P0 →ₗ[ℝ] FiniteRealCarrier D4)
    (S1of : Background → FiniteRealCarrier P1 →ₗ[ℝ] FiniteRealCarrier D3)
    (psi chi lambda : FiniteRealCarrier P0)
    (hMaps :
      dPof (symmetry b) = movedPrimalDifferential Q0 Q1 (dPof b) ∧
      dDof (symmetry b) =
        movedDualDifferential (dualAction e1 Q1) (dualAction e0 Q0) (dDof b) ∧
      S0of (symmetry b) = movedStar (dualAction e0 Q0) Q0 (S0of b) ∧
      S1of (symmetry b) = movedStar (dualAction e1 Q1) Q1 (S1of b)) :
    let pairing : FiniteRealCarrier P0 → FiniteRealCarrier D4 → ℝ := fun p d => e0 p d
    let A : FinitePrimalDualHodgeData P0 P1 D3 D4 :=
      { dP := dPof b, dD := dDof b, star0 := S0of b, star1 := S1of b }
    let A' : FinitePrimalDualHodgeData P0 P1 D3 D4 :=
      { dP := dPof (symmetry b), dD := dDof (symmetry b),
        star0 := S0of (symmetry b), star1 := S1of (symmetry b) }
    mixedPrimalDualAction pairing A' (Q0 psi) (Q0 chi) (Q0 lambda) =
      mixedPrimalDualAction pairing A psi chi lambda := by
  exact physicalMovingWard_of_constitutiveAction (fun _ => 0) symmetry b
    e0 e1 Q0 Q1 dPof dDof S0of S1of psi chi lambda ⟨rfl,hMaps⟩


/-! Actual composition premise versus a genuine order-two law. -/
section Composition
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

private theorem five_coefficients (x a e b c : ℚ)
    (h : ∀ s t : ℚ, s*t*x + s*t^2*a + s*t^3*e + s^2*t*b + s^2*t^2*c = 0) :
    x = 0 ∧ a = 0 ∧ e = 0 ∧ b = 0 ∧ c = 0 := by
  have h1 := h 1 1
  have h2 := h (-1) 1
  have h3 := h 1 (-1)
  have h4 := h (-1) (-1)
  have h5 := h 1 2
  refine ⟨?_,?_,?_,?_,?_⟩
  · linear_combination (3/4:ℚ)*h1-(1/4:ℚ)*h2-(1/12:ℚ)*h3+(1/4:ℚ)*h4-(1/6:ℚ)*h5
  · linear_combination (1/4:ℚ)*h1-(1/4:ℚ)*h2+(1/4:ℚ)*h3-(1/4:ℚ)*h4
  · linear_combination -(1/2:ℚ)*h1-(1/6:ℚ)*h3+(1/6:ℚ)*h5
  · linear_combination (1/4:ℚ)*h1+(1/4:ℚ)*h2-(1/4:ℚ)*h3-(1/4:ℚ)*h4
  · linear_combination (1/4:ℚ)*h1+(1/4:ℚ)*h2+(1/4:ℚ)*h3+(1/4:ℚ)*h4

/-- Full classification of the literal polynomial-composition premise. -/
theorem exact_polynomial_composition_iff (G D K : Matrix ι ι ℚ) :
    (∀ s t, groupoidMoved G D K s t * groupoidBase G K t = groupoidSum G K s t) ↔
      G*G+D-K = 0 ∧ (1/2:ℚ) • (G*K)+D*G = 0 ∧
      (1/2:ℚ) • (D*K) = 0 ∧ (1/2:ℚ) • (K*G) = 0 ∧
      (1/4:ℚ) • (K*K) = 0 := by
  constructor
  · intro h
    have hc (i j : ι) := five_coefficients ((G*G+D-K) i j)
      (((1/2:ℚ) • (G*K)+D*G) i j) (((1/2:ℚ) • (D*K)) i j)
      (((1/2:ℚ) • (K*G)) i j) (((1/4:ℚ) • (K*K)) i j) (by
        intro s t
        have he := congrArg (fun M : Matrix ι ι ℚ => M i j)
          (groupoidProduct_expansion G D K s t)
        rw [h s t] at he
        simp only [Matrix.add_apply, Matrix.smul_apply, smul_eq_mul] at he ⊢
        linarith)
    refine ⟨?_,?_,?_,?_,?_⟩
    · ext i j; exact (hc i j).1
    · ext i j; exact (hc i j).2.1
    · ext i j; exact (hc i j).2.2.1
    · ext i j; exact (hc i j).2.2.2.1
    · ext i j; exact (hc i j).2.2.2.2
  · rintro ⟨hx,ha,he,hb,hc⟩ s t
    rw [groupoidProduct_expansion,hx,ha,he,hb,hc]
    simp

/-- In the zero-background-derivative slice, the extra condition is G³=0. -/
theorem frozen_exact_composition_iff (G K : Matrix ι ι ℚ) :
    (∀ s t, groupoidMoved G 0 K s t * groupoidBase G K t = groupoidSum G K s t) ↔
      K = G*G ∧ (G*G)*G = 0 := by
  constructor
  · intro h
    have hk : K = G*G := by simpa using actionGroupoid_secondJet G 0 K h
    have hb := ((exact_polynomial_composition_iff G 0 K).mp h).2.2.2.1
    have hkg : K*G = 0 := (smul_eq_zero.mp hb).resolve_left (by norm_num)
    exact ⟨hk,by simpa [hk] using hkg⟩
  · rintro ⟨rfl,h3⟩
    apply (exact_polynomial_composition_iff G 0 (G*G)).mpr
    have h4 : (G*G)*(G*G) = 0 := by
      simpa [Matrix.mul_assoc] using congrArg (fun M : Matrix ι ι ℚ => M*G) h3
    have h3' : G*(G*G) = 0 := by simpa only [Matrix.mul_assoc] using h3
    simp [h3,h3',h4]

/-- All the terms discarded by total-degree-two truncation are explicit. -/
def groupoidRemainder (G D K : Matrix ι ι ℚ) (s t : ℚ) : Matrix ι ι ℚ :=
  (s*t^2) • ((1/2:ℚ) • (G*K)+D*G) +
  (s*t^3) • ((1/2:ℚ) • (D*K)) +
  (s^2*t) • ((1/2:ℚ) • (K*G)) +
  (s^2*t^2) • ((1/4:ℚ) • (K*K))

theorem product_with_exact_remainder (G D K : Matrix ι ι ℚ) (s t : ℚ) :
    groupoidMoved G D K s t * groupoidBase G K t - groupoidRemainder G D K s t =
      groupoidSum G K s t + (s*t) • (G*G+D-K) := by
  rw [groupoidProduct_expansion]
  unfold groupoidRemainder
  abel

/-- Equality of total-degree-two jets, not equality of the truncated polynomials. -/
def ComposesToOrderTwo (G D K : Matrix ι ι ℚ) : Prop :=
  ∀ s t, groupoidMoved G D K s t * groupoidBase G K t -
    groupoidRemainder G D K s t = groupoidSum G K s t

theorem order_two_composition_iff (G D K : Matrix ι ι ℚ) :
    ComposesToOrderTwo G D K ↔ K = G*G+D := by
  constructor
  · intro h
    have hh := h 1 1
    rw [product_with_exact_remainder] at hh
    have hz : G*G+D-K = 0 := by
      simpa using hh
    exact (sub_eq_zero.mp hz).symm
  · intro hk s t
    rw [product_with_exact_remainder,hk]
    simp

theorem order_two_fiber_nonempty (G D : Matrix ι ι ℚ) :
    ComposesToOrderTwo G D (G*G+D) :=
  (order_two_composition_iff _ _ _).mpr rfl

end Composition

/-- The actual native scalar translation is constant in its coframe direction. -/
theorem native_constant_displacement_zero (n : ℕ) [NeZero n] :
    scalarDisplacement (scalarOnes n) = 0 := by
  funext i
  simp [scalarDisplacement,scalarOnes]

theorem native_cycle4_generator_cube :
    ((scalarCycleG (scalarOnes 4)*scalarCycleG (scalarOnes 4))*
      scalarCycleG (scalarOnes 4)) (0 : Fin 4) (1 : Fin 4) = -32 := by
  have hM : scalarCycleMul (scalarOnes 4) = (1 : Matrix (Fin 4) (Fin 4) ℚ) := by
    ext i j
    simp [scalarCycleMul,scalarOnes,Matrix.diagonal,Matrix.one_apply]
  have hG : scalarCycleG (scalarOnes 4) = scalarCycleD 4 := by
    rw [scalarCycleG,hM,Matrix.one_mul]
  have hD : scalarCycleD 4 = !![0,2,0,-2; -2,0,2,0; 0,-2,0,2; 2,0,-2,0] := by
    ext i j
    fin_cases i <;> fin_cases j <;>
      norm_num [scalarCycleD,scalarCycleShift,Matrix.transpose_apply,Fin.ext_iff,Fin.val_add]
  rw [hG,hD]
  norm_num [Matrix.mul_apply,Fin.sum_univ_succ]

theorem native_cycle4_exact_quadratic_premise_empty :
    ¬ ∃ K : Matrix (Fin 4) (Fin 4) ℚ, ∀ s t,
      groupoidMoved (scalarCycleG (scalarOnes 4)) 0 K s t *
        groupoidBase (scalarCycleG (scalarOnes 4)) K t =
          groupoidSum (scalarCycleG (scalarOnes 4)) K s t := by
  rintro ⟨K,h⟩
  have hz := ((frozen_exact_composition_iff _ K).mp h).2
  have he := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℚ => M 0 1) hz
  change ((scalarCycleG (scalarOnes 4)*scalarCycleG (scalarOnes 4))*
      scalarCycleG (scalarOnes 4)) 0 1 = 0 at he
  rw [native_cycle4_generator_cube] at he
  norm_num at he

theorem native_cycle4_order_two_premise_nonempty :
    ComposesToOrderTwo (scalarCycleG (scalarOnes 4)) 0
      (scalarCycleG (scalarOnes 4)*scalarCycleG (scalarOnes 4)) := by
  simpa using order_two_fiber_nonempty (scalarCycleG (scalarOnes 4)) 0

section RealFlowControl
open scoped Matrix.Norms.Operator
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- A full mathematical flow is a control against confusing Taylor truncation
with exact finite composition. This does not select native dynamics. -/
def realFlow (G : Matrix ι ι ℝ) (t : ℝ) := NormedSpace.exp (t • G)

theorem real_flow_composes (G : Matrix ι ι ℝ) (s t : ℝ) :
    realFlow G (s+t) = realFlow G s * realFlow G t := by
  unfold realFlow
  rw [add_smul]
  exact Matrix.exp_add_of_commute _ _ (((Commute.refl G).smul_left s).smul_right t)

theorem real_flow_first_two_derivatives (G : Matrix ι ι ℝ) :
    HasDerivAt (realFlow G) G 0 ∧
      HasDerivAt (fun t => realFlow G t * G) (G*G) 0 := by
  constructor
  · simpa [realFlow] using hasDerivAt_exp_smul_const G (0 : ℝ)
  · simpa [realFlow] using (hasDerivAt_exp_smul_const G (0 : ℝ)).mul_const G
end RealFlowControl

open D0
open scoped BigOperators

section SplitGroupoid
variable {X H K : Type*} [Group H] [Group K]

/-- Pair groupoid times the full stabilizer, with no isotropy erased. -/
structure SplitTransport (X H K : Type*) [Group H] [Group K] where
  map : X → X → H → K
  identity : ∀ x, map x x 1 = 1
  composition : ∀ x y z h k, map x y h * map y z k = map x z (h*k)

@[ext] theorem splitTransport_ext (T S : SplitTransport X H K)
    (h : ∀ x y k, T.map x y k = S.map x y k) : T = S := by
  cases T with
  | mk t ti tc =>
    cases S with
    | mk s si sc =>
      have hs : t=s := funext fun x => funext fun y => funext (h x y)
      cases hs
      rfl

def transportFromData (U : X → K) (rho : H →* K) : SplitTransport X H K where
  map x y h := U x * rho h * (U y)⁻¹
  identity := by intro x; simp
  composition := by intro x y z h k; simp [map_mul, mul_assoc]

def transportIsotropy (b : X) (T : SplitTransport X H K) : H →* K where
  toFun h := T.map b b h
  map_one' := T.identity b
  map_mul' h k := (T.composition b b b h k).symm

theorem split_transport_factorization (b : X) (T : SplitTransport X H K)
    (x y : X) (h : H) :
    T.map x y h = T.map x b 1 * (transportIsotropy b T) h * (T.map y b 1)⁻¹ := by
  have hi : T.map b y 1 = (T.map y b 1)⁻¹ := by
    apply eq_inv_of_mul_eq_one_left
    simpa [T.identity] using T.composition b y b 1 1
  have h1 := T.composition x b b 1 h
  have h2 := T.composition x b y h 1
  change T.map x y h = T.map x b 1 * T.map b b h * (T.map y b 1)⁻¹
  rw [← hi]
  simp only [one_mul,mul_one] at h1 h2
  rw [h1,h2]

/-- Every strict transport on this entire split groupoid, with unique normalized data. -/
def completeSplitTransportFiber (b : X) :
    SplitTransport X H K ≃ ({U : X → K // U b = 1} × (H →* K)) where
  toFun T := (⟨fun x => T.map x b 1,T.identity b⟩,transportIsotropy b T)
  invFun p := transportFromData p.1.val p.2
  left_inv T := by
    apply splitTransport_ext
    intro x y h
    exact (split_transport_factorization b T x y h).symm
  right_inv p := by
    rcases p with ⟨⟨U,hU⟩,rho⟩
    apply Prod.ext
    · apply Subtype.ext
      funext x
      simp [transportFromData,hU]
    · ext h
      simp [transportIsotropy,transportFromData,hU]

/-- Normalized trivialization freedom has an explicit intertwiner; this is
not a declaration of native physical gauge or readout equivalence. -/
theorem split_transport_intertwiner (U V : X → K) (rho : H →* K)
    (x y : X) (h : H) :
    (V x * (U x)⁻¹) * (transportFromData U rho).map x y h =
      (transportFromData V rho).map x y h * (V y * (U y)⁻¹) := by
  simp [transportFromData,mul_assoc]

/-- Full classification of covariant sections for the given group action:
a value at the base must be invariant under every isotropy element. -/
theorem transported_section_covariant_iff {Y : Type*} [MulAction K Y]
    (b : X) (U : X → K) (hU : U b=1) (rho : H →* K) (v : Y) :
    (∀ x y h, (transportFromData U rho).map x y h • (U y • v) = U x • v) ↔
      (∀ h, rho h • v = v) := by
  constructor
  · intro hc h
    simpa [transportFromData,hU] using hc b b h
  · intro hv x y h
    simp [transportFromData,mul_smul,hv]
end SplitGroupoid

section NativeKernel
open scoped BigOperators
variable {n : ℕ} [NeZero n]

theorem native_scalar_displacement_kernel (v : Fin n → ℚ) :
    scalarDisplacement v = 0 ↔ ∃ c : ℚ, ∀ i, v i = c := by
  constructor
  · intro hz
    have hn : n ≠ 0 := NeZero.ne n
    have step : ∀ i : Fin n, v (i+1)=v i := by
      intro i
      have h := congrFun hz i
      change (n:ℚ)*(v (i+1)-v i)=0 at h
      exact sub_eq_zero.mp ((mul_eq_zero.mp h).resolve_left (Nat.cast_ne_zero.mpr hn))
    obtain ⟨m,rfl⟩ := Nat.exists_eq_succ_of_ne_zero hn
    refine ⟨v 0,?_⟩
    intro i
    induction i using Fin.induction with
    | zero => rfl
    | succ i ih =>
      have hi := i.isLt
      have he : (i.castSucc : Fin (m+1))+1=i.succ := by
        apply Fin.ext
        change (i.val + 1 % (m+1)) % (m+1) = i.val+1
        rw [Nat.mod_eq_of_lt (by omega : 1 < m+1),
          Nat.mod_eq_of_lt (by omega : i.val+1 < m+1)]
      rw [← he,step,ih]
  · rintro ⟨c,hc⟩
    funext i
    simp [scalarDisplacement,hc]

def scalarMean (v : Fin n → ℚ) : ℚ := (∑ i,v i)/(n:ℚ)
def scalarCentered (v : Fin n → ℚ) : Fin n → ℚ := fun i => v i-scalarMean v

theorem native_scalar_centered_same_displacement (v : Fin n → ℚ) :
    scalarDisplacement (scalarCentered v) = scalarDisplacement v := by
  funext i
  simp [scalarDisplacement,scalarCentered]

theorem native_scalar_mean_centered_zero (v : Fin n → ℚ) :
    scalarMean (scalarCentered v)=0 := by
  have hn : (n:ℚ)≠0 := Nat.cast_ne_zero.mpr (NeZero.ne n)
  simp only [scalarMean,scalarCentered,Finset.sum_sub_distrib,Finset.sum_const,
    Finset.card_univ,Fintype.card_fin,nsmul_eq_mul]
  field_simp
  ring

theorem native_scalar_centered_unique (v w : Fin n → ℚ)
    (hd : scalarDisplacement v=scalarDisplacement w)
    (hv : scalarMean v=0) (hw : scalarMean w=0) : v=w := by
  have hd0 : scalarDisplacement (v-w)=0 := by
    funext i
    have hh := congrFun hd i
    simp only [scalarDisplacement,Pi.sub_apply] at hh ⊢
    change (n:ℚ)*((v (i+1)-w (i+1))-(v i-w i))=0
    linarith
  obtain ⟨c,hc⟩ := (native_scalar_displacement_kernel (v-w)).mp hd0
  have hm : scalarMean (v-w)=0 := by
    change ((∑ i, (v i-w i))/(n:ℚ))=0
    rw [Finset.sum_sub_distrib,sub_div]
    change scalarMean v-scalarMean w=0
    rw [hv,hw,sub_self]
  have hn : (n:ℚ)≠0 := Nat.cast_ne_zero.mpr (NeZero.ne n)
  have hc0 : c=0 := by
    simpa [scalarMean,hc,hn] using hm
  funext i
  have hh := hc i
  exact sub_eq_zero.mp (by simpa [Pi.sub_apply,hc0] using hh)
end NativeKernel


section JetAlgebra
variable {ι : Type*} [Fintype ι] [DecidableEq ι]
def splitMixed (H A : Matrix ι ι ℚ) (B E : Matrix ι ι ℚ) : Matrix ι ι ℚ :=
  H + (1/2:ℚ) • (A*B-B*A) + (A*E-E*A)

theorem split_mixed_integrability (H A C B E : Matrix ι ι ℚ)
    (hCE : C*E=E*C) :
    splitMixed H A B E - splitMixed H B A C +
      ((B+E)*(A+C)-(A+C)*(B+E)) = 0 := by
  simp only [splitMixed,add_mul,mul_add]
  rw [hCE]
  module

theorem split_diagonal_second_jet (H A C : Matrix ι ι ℚ) :
    (A+C)*(A+C)+splitMixed H A A C =
      A*A+(2:ℚ) • (A*C)+C*C+H := by
  simp only [splitMixed,add_mul,mul_add]
  module

/-- This is the complete flat mixed equation on the actual scalar interface;
values on transverse backgrounds are intentionally not constrained. -/
theorem native_mixed_fiber_iff_symmetric {n : ℕ} [NeZero n] (hn : 3≤n)
    (B : (Fin n → ℚ) → (Fin n → ℚ) → Matrix (Fin n) (Fin n) ℚ) :
    (∀ ξ ζ, B ζ (scalarDisplacement ξ)-B ξ (scalarDisplacement ζ)+
      (scalarCycleG ζ*scalarCycleG ξ-scalarCycleG ξ*scalarCycleG ζ)=0) ↔
    (∀ ξ ζ, B ζ (scalarDisplacement ξ)-
      advectiveBackgroundDerivative ζ (scalarDisplacement ξ) =
      B ξ (scalarDisplacement ζ)-
      advectiveBackgroundDerivative ξ (scalarDisplacement ζ)) := by
  constructor
  · intro h ξ ζ
    exact flatComparison_difference_symmetric B advectiveBackgroundDerivative ξ ζ
      (h ξ ζ) (advective_mixedCocycle hn ξ ζ)
  · intro h ξ ζ
    have hc := advective_mixedCocycle hn ξ ζ
    have hs := h ξ ζ
    calc
      _ = (B ζ (scalarDisplacement ξ)-advectiveBackgroundDerivative ζ (scalarDisplacement ξ)-
          (B ξ (scalarDisplacement ζ)-advectiveBackgroundDerivative ξ (scalarDisplacement ζ))) +
          (advectiveBackgroundDerivative ζ (scalarDisplacement ξ)-
          advectiveBackgroundDerivative ξ (scalarDisplacement ζ)+
          (scalarCycleG ζ*scalarCycleG ξ-scalarCycleG ξ*scalarCycleG ζ)) := by abel
      _ = 0 := by rw [hs,sub_self,hc,zero_add]

/-- An arbitrary symmetric background Hessian supplies every free correction
along the native exact-translation orbit. -/
theorem native_symmetric_correction_is_mixed_cocycle {n : ℕ} [NeZero n] (hn : 3≤n)
    (S : (Fin n → ℚ) → (Fin n → ℚ) → Matrix (Fin n) (Fin n) ℚ)
    (hS : ∀ h k, S h k=S k h) :
    ∀ ξ ζ,
      (advectiveBackgroundDerivative ζ (scalarDisplacement ξ)+
        S (scalarDisplacement ζ) (scalarDisplacement ξ)) -
      (advectiveBackgroundDerivative ξ (scalarDisplacement ζ)+
        S (scalarDisplacement ξ) (scalarDisplacement ζ)) +
      (scalarCycleG ζ*scalarCycleG ξ-scalarCycleG ξ*scalarCycleG ζ)=0 := by
  intro ξ ζ
  rw [hS (scalarDisplacement ζ) (scalarDisplacement ξ)]
  have hc := advective_mixedCocycle hn ξ ζ
  convert hc using 1; abel
end JetAlgebra

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem native_car_mixed_kernel : ∀ r s : Role, ∀ bra ket : ArchiveFockState,
    anticommutatorInt (carAnnihilateInt r) (carCreateInt s) bra ket =
      roleDeltaInt r s * fockIdentityInt bra ket := by
  decide +kernel

/-- Replays the source proof through the kernel after replacing its finite
native-decide CAR leaf by the proposition-identical kernel proof above.
Only D0 theorem bodies are unfolded. The result is checked as a new theorem;
this elaborator cannot add an axiom or modify an imported owner. -/
private partial def kernelCARProof (env : Lean.Environment) (e : Lean.Expr) : Lean.Expr :=
  e.replace fun t => match t with
  | .const n ls =>
      if n == ``car_mixed_anticommutator_int then
        some (.const ``native_car_mixed_kernel ls)
      else if (`D0).isPrefixOf n || "_private.D0.".isPrefixOf n.toString then
        match env.find? n with
        | some (.thmInfo v) => some (kernelCARProof env (v.value.instantiateLevelParams v.levelParams ls))
        | _ => none
      else none
  | _ => none

open Lean Elab Term in
elab "kernelCartanExpansion" : term => do
  let env ← getEnv
  let some (.thmInfo v) := env.find? ``cartanGenerator_exact_expansion
    | throwError "owned Cartan expansion theorem not found"
  return kernelCARProof env v.value

theorem native_cartan_expansion_kernel : ∀ (N : ℕ) (ξ : LocalRoleVector N)
    (ψ : ArchiveCochain N),
    a4dCartanGenerator N ξ ψ = cartanGeneratorExpansion N ξ ψ := kernelCartanExpansion


section A4DBinding
/-- The same d is the actual affine owner's flat coframe orbit. -/
theorem native_flat_orbit_binding (N : ℕ) (t : ℝ) (ξ : LocalRoleVector N)
    (x : ArchiveRolePhaseGroup N) (r a : Role) :
    (affineGauge (translationGauge N (t • ξ)) (flatAffineConnection N) x r).shift a =
      t * forwardGaugeCoframe N ξ x r a := ownedFlatTranslation_is_linear N t ξ x r a

/-- Literal four-role/Fock owner, without a scalar-embedding assumption. -/
theorem native_a4d_constant_tangent (N : ℕ) (c : Role → ℝ) (ψ : ArchiveCochain N) :
    a4dCartanGenerator N (fun _ => c) ψ =
      fun p => ∑ r, c r * centeredDifference N r (fun x => ψ (x,p.2)) p.1 := by
  rw [native_cartan_expansion_kernel]
  funext p
  simp only [cartanGeneratorExpansion,Pi.add_apply,Finset.sum_apply,
    cochainMultiply,forwardDifference_const,Pi.zero_apply,zero_mul,
    Finset.sum_const_zero,add_zero]
  apply Finset.sum_congr rfl
  intro r _
  congr 1
  exact (congrFun (centeredDifference_eq_average_forward N r (fun x => ψ (x,p.2))) p.1).symm

/-- These are the actual isotropy generators; their commutation is required
for integrating the full additive stabilizer, not all local translations. -/
theorem native_a4d_constant_tangents_commute (N : ℕ) (c b : Role → ℝ)
    (ψ : ArchiveCochain N) :
    a4dCartanGenerator N (fun _ => c) (a4dCartanGenerator N (fun _ => b) ψ) =
      a4dCartanGenerator N (fun _ => b) (a4dCartanGenerator N (fun _ => c) ψ) := by
  simp_rw [native_a4d_constant_tangent]
  funext p
  have hsum (r : Role) (b : Role → ℝ) :
      centeredDifference N r (fun x => ∑ s, b s *
        centeredDifference N s (fun y => ψ (y,p.2)) x) p.1 =
      ∑ s, b s * centeredDifference N r
        (centeredDifference N s (fun y => ψ (y,p.2))) p.1 := by
    simp only [centeredDifference_apply]
    rw [← Finset.sum_sub_distrib,Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro s _
    ring
  simp_rw [hsum,Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro s _
  apply Finset.sum_congr rfl
  intro r _
  rw [centeredDifference_comm]
  ring
end A4DBinding


/-- Bind the full raw kernel to the existing all-size owner, not a new rank census. -/
theorem native_full_translation_kernel (N : ℕ) (xi : LocalRoleVector N) :
    forwardGaugeCoframe N xi = 0 ↔ ∀ x a, xi x a = xi 0 a :=
  coframeDifferential_ker_constant N xi

theorem native_centered_translation_entry (N : ℕ) (xi : LocalRoleVector N)
    (x : ArchiveRolePhaseGroup N) (r a : Role) :
    centeredCoframeMatrix N (forwardGaugeCoframe N xi) x r a =
      centeredDifference N r (fun y => xi y a) x := by
  exact (congrFun (centeredDifference_eq_average_forward N r (fun y => xi y a)) x).symm

/-- Exact closure is retained by the actual row-centered readout. -/
theorem native_centered_translation_curl_zero (N : ℕ) (xi : LocalRoleVector N)
    (x : ArchiveRolePhaseGroup N) (r s a : Role) :
    centeredDifference N r
        (fun y => centeredCoframeMatrix N (forwardGaugeCoframe N xi) y s a) x -
      centeredDifference N s
        (fun y => centeredCoframeMatrix N (forwardGaugeCoframe N xi) y r a) x = 0 := by
  simp_rw [native_centered_translation_entry]
  rw [centeredDifference_comm]
  exact sub_self _

/-- This tangent is the existing metric readout, not an independently chosen operator. -/
theorem native_metric_translation_tangent (N : ℕ) (xi : LocalRoleVector N)
    (t : ℝ) (x : ArchiveRolePhaseGroup N) :
    solderMetricMatrix N (t • forwardGaugeCoframe N xi) x - roleLorentzMetric =
      t • (symmetricRoleGradient N xi x).toMatrix + t^2 •
        (centeredCoframeMatrix N (forwardGaugeCoframe N xi) x * roleLorentzMetric *
          (centeredCoframeMatrix N (forwardGaugeCoframe N xi) x).transpose) :=
  solderMetric_forwardGauge_flat_tangent N xi t x

/-- Testing every native flat translation is exactly divergence zero; it is
not testing every independent symmetric metric variation. -/
theorem native_translation_annihilator_iff (N : ℕ) (T : LocalSymRoleField N) :
    (∀ xi, tensorInnerProduct N T
      (coframeMetricReadout N (forwardGaugeCoframe N xi)) = 0) ↔
      divergenceVector N T = 0 := by
  simp_rw [coframeMetricReadout_forwardGauge]
  constructor
  · exact centeredRoleDivergence_zero_of_metric_pairing N T
  · intro h xi
    rw [tensorInnerProduct_symm, symmetricRoleGradient_adjoint, h]
    simp [roleVectorInnerProduct, scalarInnerProduct]

def constantMetricIdentity (N : ℕ) : LocalSymRoleField N :=
  fun _ => ⟨1, by intro a b; simp [Matrix.one_apply, eq_comm]⟩


/-- The separating smooth metric probe has a literal raw-coframe lift. -/
theorem native_constant_metric_probe_has_coframe_lift (N : ℕ) :
    coframeMetricReadout N (fun _ r a => if r=a then (1/2:ℝ) else 0) =
      constantMetricIdentity N := by
  funext x
  apply SymRoleTensor.ext
  funext a b
  by_cases hab : a=b
  · subst b
    norm_num [coframeMetricReadout, backwardAverage, constantMetricIdentity]
  · simp [coframeMetricReadout, backwardAverage, constantMetricIdentity,
      hab, Ne.symm hab]

theorem native_constant_metric_divergence_zero (N : ℕ) :
    divergenceVector N (constantMetricIdentity N) = 0 := by
  funext x b
  simp [divergenceVector, roleDivergence, tensorEntry, constantMetricIdentity]

theorem native_constant_metric_self_pairing (N : ℕ) :
    tensorInnerProduct N (constantMetricIdentity N) (constantMetricIdentity N) =
      4 * (archiveModes N : ℝ) := by
  simp [tensorInnerProduct, scalarInnerProduct, tensorEntry, constantMetricIdentity,
    Matrix.one_apply, archiveModes]

/-- An actual nonzero symmetric covector obeys all translation tests but
fails a smooth constant metric test. No source or action is selected. -/
theorem native_translation_tests_not_all_metric_tests (N : ℕ) :
    (∀ xi, tensorInnerProduct N (constantMetricIdentity N)
      (coframeMetricReadout N (forwardGaugeCoframe N xi)) = 0) ∧
    tensorInnerProduct N (constantMetricIdentity N) (constantMetricIdentity N) ≠ 0 := by
  constructor
  · exact (native_translation_annihilator_iff N _).mpr
      (native_constant_metric_divergence_zero N)
  · rw [native_constant_metric_self_pairing]
    simp only [archiveModes, archiveFibers, Nat.cast_pow, Nat.cast_add, Nat.cast_ofNat]
    positivity

/-- Generic nonzero-frequency symbol injectivity over C. Fourier completeness,
the real dimension count and the smooth-limit theorem are proved in the memo. -/
theorem metric_translation_symbol_injective (q v : Role → ℂ)
    (hq : ∃ r, q r ≠ 0)
    (h : ∀ r a, q r * v a + q a * v r = 0) : v = 0 := by
  obtain ⟨r,hr⟩ := hq
  have hrr : (2:ℂ) * (q r * v r) = 0 := by linear_combination h r r
  have hv : v r = 0 := (mul_eq_zero.mp
    ((mul_eq_zero.mp hrr).resolve_left (by norm_num))).resolve_left hr
  funext a
  have ha := h r a
  rw [hv,mul_zero,add_zero] at ha
  exact (mul_eq_zero.mp ha).resolve_left hr

#print axioms native_full_translation_kernel
#print axioms native_centered_translation_entry
#print axioms native_centered_translation_curl_zero
#print axioms native_metric_translation_tangent
#print axioms native_translation_annihilator_iff
#print axioms native_constant_metric_probe_has_coframe_lift
#print axioms native_constant_metric_divergence_zero
#print axioms native_constant_metric_self_pairing
#print axioms native_translation_tests_not_all_metric_tests
#print axioms metric_translation_symbol_injective


/-! The actual primitive gap and the existence of native field variations. -/

theorem action_gap_eventually_constant {P : VerificationProtocol} (A : ActionProtocol P)
    (x : ℝ → P.State) (t0 : ℝ)
    (h : ContinuousAt (fun t => A.action (x t0) (x t)) t0) :
    ∀ᶠ t in nhds t0, x t=x t0 := by
  have hf : ∀ᶠ t in nhds t0, A.action (x t0) (x t)<1 :=
    h.eventually (gt_mem_nhds (by simpa only [A.action_refl] using (zero_lt_one : (0:ℝ)<1)))
  filter_upwards [hf] with t ht
  by_contra hn
  exact (not_lt_of_ge (A.action_nontrivial _ _ (Ne.symm hn))) ht

/-- Complete classification for every actual ActionProtocol, without smoothness
or finite-dimensional assumptions on the state type. -/
theorem action_gap_continuity_iff {P : VerificationProtocol} (A : ActionProtocol P)
    (x : ℝ → P.State) (t0 : ℝ) :
    ContinuousAt (fun t => A.action (x t0) (x t)) t0 ↔
      ∀ᶠ t in nhds t0, x t=x t0 := by
  constructor
  · exact action_gap_eventually_constant A x t0
  · intro h
    have heq : (fun t => A.action (x t0) (x t)) =ᶠ[nhds t0] fun _ => (0:ℝ) := by
      filter_upwards [h] with t ht
      rw [ht,A.action_refl]
    exact continuousAt_const.congr_of_eventuallyEq heq

/-- A genuine derivative of an identity-based primitive cost can only be zero.
No conclusion is drawn merely from Lean's totalized `deriv` value. -/
theorem action_gap_hasDerivAt_zero {P : VerificationProtocol} (A : ActionProtocol P)
    (x : ℝ → P.State) (t0 a : ℝ)
    (h : HasDerivAt (fun t => A.action (x t0) (x t)) a t0) : a=0 := by
  have hc := action_gap_eventually_constant A x t0 h.continuousAt
  have heq : (fun t => A.action (x t0) (x t)) =ᶠ[nhds t0] fun _ => (0:ℝ) := by
    filter_upwards [hc] with t ht
    rw [ht,A.action_refl]
  have hz : HasDerivAt (fun t => A.action (x t0) (x t)) 0 t0 :=
    (hasDerivAt_const t0 (0:ℝ)).congr_of_eventuallyEq heq
  exact h.unique hz

theorem nonconstant_germ_no_primitive_derivative {P : VerificationProtocol}
    (A : ActionProtocol P) (x : ℝ → P.State) (t0 : ℝ)
    (hx : ¬ ∀ᶠ t in nhds t0, x t=x t0) :
    ¬ DifferentiableAt ℝ (fun t => A.action (x t0) (x t)) t0 := by
  intro hd
  exact hx (action_gap_eventually_constant A x t0 hd.continuousAt)

/-- The owned primitive action quantum applies to a faithful field-state
embedding only if that embedding exists. Every nonzero affine field germ
then violates differentiability of the identity-based transition cost. -/
theorem affine_field_germ_not_locally_constant {V : Type*}
    [AddCommGroup V] [Module ℝ V] (u v : V) (hv : v≠0) :
    ¬ ∀ᶠ t in nhds (0:ℝ), u+t • v=u := by
  intro h
  have hz : ∀ᶠ t in nhds (0:ℝ), t=0 := by
    filter_upwards [h] with t ht
    have htv : t • v=0 := add_left_cancel (show u+t • v=u+0 by simpa using ht)
    exact (smul_eq_zero.mp htv).resolve_right hv
  have hi : HasDerivAt (fun t : ℝ => t) 0 0 :=
    (hasDerivAt_const (0:ℝ) (0:ℝ)).congr_of_eventuallyEq hz
  have hn := (hasDerivAt_id (0:ℝ)).unique hi
  norm_num at hn


theorem faithful_affine_field_cost_not_differentiable {P : VerificationProtocol}
    (A : ActionProtocol P) {V : Type*} [AddCommGroup V] [Module ℝ V]
    (encode : V → P.State) (he : Function.Injective encode)
    (u v : V) (hv : v≠0) :
    ¬ DifferentiableAt ℝ (fun t : ℝ => A.action (encode u) (encode (u+t • v))) 0 := by
  have hx : ¬ ∀ᶠ t in nhds (0:ℝ), encode (u+t • v)=encode (u+(0:ℝ) • v) := by
    intro h
    apply affine_field_germ_not_locally_constant u v hv
    filter_upwards [h] with t ht
    simpa using he ht
  simpa using nonconstant_germ_no_primitive_derivative A (fun t => encode (u+t • v)) 0 hx

theorem faithful_native_coframe_cost_not_differentiable {P : VerificationProtocol}
    (A : ActionProtocol P) (N : ℕ) (encode : LocalCoframeField N → P.State)
    (he : Function.Injective encode) (e v : LocalCoframeField N) (hv : v≠0) :
    ¬ DifferentiableAt ℝ (fun t : ℝ => A.action (encode e) (encode (e+t • v))) 0 :=
  faithful_affine_field_cost_not_differentiable A encode he e v hv

theorem calibrated_gap_continuity_iff {P : VerificationProtocol} (A : ActionProtocol P)
    (x : ℝ → P.State) (t0 a : ℝ) (ha : a≠0) :
    ContinuousAt (fun t => a*A.action (x t0) (x t)) t0 ↔
      ∀ᶠ t in nhds t0, x t=x t0 := by
  rw [← action_gap_continuity_iff A x t0]
  constructor
  · intro h
    have h' := h.const_mul a⁻¹
    simpa only [← mul_assoc, inv_mul_cancel₀ ha, one_mul] using h'
  · intro h
    exact h.const_mul a

/-- A zero `deriv` at a discontinuous cost is Lean's totalization, not an
Euler equation. The non-differentiability premise is proved, not supplied. -/
theorem primitive_nondifferentiable_deriv_zero {P : VerificationProtocol}
    (A : ActionProtocol P) (x : ℝ → P.State) (t0 : ℝ)
    (hx : ¬ ∀ᶠ t in nhds t0, x t=x t0) :
    deriv (fun t => A.action (x t0) (x t)) t0=0 :=
  deriv_zero_of_not_differentiableAt (nonconstant_germ_no_primitive_derivative A x t0 hx)

/-- Explicit shrinking-gap countercontrol for arbitrary nonnegative target
profiles. This is a completion of the primitive interface, not a selected
native physical action or a native refinement law. -/
def shrinkingGapAction (P : VerificationProtocol) (epsilon : ℝ) (he : 0<epsilon)
    (F : P.State → P.State → ℝ) (hF : ∀ x y, 0≤F x y) : ActionProtocol P :=
  actionFromExcess P (fun xy => ⟨F xy.val.1 xy.val.2 / epsilon,
    div_nonneg (hF _ _) (le_of_lt he)⟩)

theorem shrinking_gap_exact_error (P : VerificationProtocol)
    (epsilon : ℝ) (he : 0<epsilon) (F : P.State → P.State → ℝ)
    (hF : ∀ x y, 0≤F x y) (hdiag : ∀ x, F x x=0) (x y : P.State) :
    epsilon*(shrinkingGapAction P epsilon he F hF).action x y-F x y =
      if x=y then 0 else epsilon := by
  by_cases hxy : x=y
  · subst y
    simp [ActionProtocol.action_refl,hdiag]
  · simp only [shrinkingGapAction,actionFromExcess,dif_neg hxy,if_neg hxy]
    field_simp [ne_of_gt he]
    ring

theorem shrinking_gap_uniform_error (P : VerificationProtocol)
    (epsilon : ℝ) (he : 0<epsilon) (F : P.State → P.State → ℝ)
    (hF : ∀ x y, 0≤F x y) (hdiag : ∀ x, F x x=0) (x y : P.State) :
    |epsilon*(shrinkingGapAction P epsilon he F hF).action x y-F x y|≤epsilon := by
  rw [shrinking_gap_exact_error P epsilon he F hF hdiag]
  split_ifs <;> simp [abs_of_pos he,le_of_lt he]

/-- Centered finite readings can exist without an infinitesimal primitive
derivative: the canonical profile gives exactly zero at two distinct ends. -/
theorem canonical_centered_probe_zero (P : VerificationProtocol)
    (center plus minus : P.State) (hp : center≠plus) (hm : center≠minus)
    (epsilon : ℝ) :
    ((canonicalActionProtocol P).action center plus-
      (canonicalActionProtocol P).action center minus)/(2*epsilon)=0 := by
  simp [canonicalActionProtocol,hp,hm]

def squaredReadingAction (P : VerificationProtocol) (q : P.State → ℝ) (k : ℝ) :
    ActionProtocol P := actionFromExcess P
  (fun xy => ⟨(1+k*(q xy.val.2-q xy.val.1))^2,sq_nonneg _⟩)

/-- One fixed cost profile realizes this centered value at every separation;
the action is not fitted separately at each epsilon. -/
theorem squared_reading_centered_value (P : VerificationProtocol)
    (q : P.State → ℝ) (k epsilon : ℝ) (he : epsilon≠0)
    (center plus minus : P.State)
    (hp : q plus-q center=epsilon) (hm : q minus-q center= -epsilon) :
    ((squaredReadingAction P q k).action center plus-
      (squaredReadingAction P q k).action center minus)/(2*epsilon)=2*k := by
  have hcp : center≠plus := by
    intro hc; subst plus; simp at hp; exact he hp.symm
  have hcm : center≠minus := by
    intro hc; subst minus; simp at hm; exact he hm
  simp only [squaredReadingAction,actionFromExcess,dif_neg hcp,dif_neg hcm,hp,hm]
  field_simp [he]
  ring

theorem every_centered_readout_has_primitive_completion (P : VerificationProtocol)
    (q : P.State → ℝ) (c epsilon : ℝ) (he : epsilon≠0)
    (center plus minus : P.State)
    (hp : q plus-q center=epsilon) (hm : q minus-q center= -epsilon) :
    ∃ A : ActionProtocol P,
      (A.action center plus-A.action center minus)/(2*epsilon)=c := by
  refine ⟨squaredReadingAction P q (c/2),?_⟩
  rw [squared_reading_centered_value P q (c/2) epsilon he center plus minus hp hm]
  ring

#print axioms action_gap_eventually_constant
#print axioms action_gap_continuity_iff
#print axioms action_gap_hasDerivAt_zero
#print axioms nonconstant_germ_no_primitive_derivative
#print axioms affine_field_germ_not_locally_constant
#print axioms faithful_affine_field_cost_not_differentiable
#print axioms faithful_native_coframe_cost_not_differentiable
#print axioms calibrated_gap_continuity_iff
#print axioms primitive_nondifferentiable_deriv_zero
#print axioms shrinking_gap_exact_error
#print axioms shrinking_gap_uniform_error
#print axioms canonical_centered_probe_zero
#print axioms squared_reading_centered_value
#print axioms every_centered_readout_has_primitive_completion
#check action_gap_eventually_constant
#check action_gap_continuity_iff
#check action_gap_hasDerivAt_zero
#check nonconstant_germ_no_primitive_derivative
#check affine_field_germ_not_locally_constant
#check faithful_affine_field_cost_not_differentiable
#check faithful_native_coframe_cost_not_differentiable
#check calibrated_gap_continuity_iff
#check primitive_nondifferentiable_deriv_zero
#check shrinking_gap_exact_error
#check shrinking_gap_uniform_error
#check canonical_centered_probe_zero
#check squared_reading_centered_value
#check every_centered_readout_has_primitive_completion

#print ActionProtocol
#print VerificationContract
#print physicalMovingWard_of_constitutiveAction
#check mixedAction_transform
#check movingHodge_comp
#print axioms action_ext
#print axioms excess_action_left_inverse
#print axioms excess_action_right_inverse
#print axioms completeActionFiber
#print axioms canonical_action_has_zero_excess
#print axioms canonical_action_is_least
#print axioms least_action_iff_canonical
#print axioms threeState_killing_test
#print axioms canonical_normalized_metric
#print axioms second_normalized_metric
#print axioms distinct_normalized_action_ratios
#print axioms action_ratio_not_m1_forced
#print axioms action_cost_difference_survives_calibration
#print axioms action_cost_difference_survives_all_relabelings
#print axioms completeInvariantActionFiber
#print axioms invariant_iff_constant_on_symmetry_orbits
#print axioms arbitrary_profile_of_invariant_observable
#print axioms two_profiles_same_nontrivial_symmetry
#print axioms invariant_profiles_different_variations
#print axioms passive_hodge_recovers_seed
#print axioms passive_hodge_seed_injective
#print axioms actual_ward_needs_only_map_covariance
#print actionGroupoid_secondJet
#print axioms exact_polynomial_composition_iff
#print axioms frozen_exact_composition_iff
#print axioms product_with_exact_remainder
#print axioms order_two_composition_iff
#print axioms order_two_fiber_nonempty
#print axioms native_constant_displacement_zero
#print axioms native_cycle4_generator_cube
#print axioms native_cycle4_exact_quadratic_premise_empty
#print axioms native_cycle4_order_two_premise_nonempty
#print axioms real_flow_composes
#print axioms real_flow_first_two_derivatives

#print axioms splitTransport_ext
#print axioms split_transport_factorization
#print axioms completeSplitTransportFiber
#print axioms split_transport_intertwiner
#print axioms transported_section_covariant_iff
#print axioms native_scalar_displacement_kernel
#print axioms native_scalar_centered_same_displacement
#print axioms native_scalar_mean_centered_zero
#print axioms native_scalar_centered_unique
#print axioms split_mixed_integrability
#print axioms split_diagonal_second_jet
#print axioms native_mixed_fiber_iff_symmetric
#print axioms native_symmetric_correction_is_mixed_cocycle
#print axioms native_car_mixed_kernel
#print axioms native_cartan_expansion_kernel
#print axioms native_flat_orbit_binding
#print axioms native_a4d_constant_tangent
#print axioms native_a4d_constant_tangents_commute

end
end D0.Research.NativeDynamicalOwnership
