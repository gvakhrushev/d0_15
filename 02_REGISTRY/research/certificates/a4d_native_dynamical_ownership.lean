import D0.Foundation.EndogenousActionQuantum
import D0.Foundation.ObservableCompletionCanonicity
import D0.Geometry.A4DPathWordParentWard
import D0.Geometry.A4DActionGroupoidSecondJet
import D0.Geometry.A4DScalarDeltaSecondJet
import Mathlib.Analysis.Normed.Algebra.MatrixExponential
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Tactic

/-! G0: complete fibers of the actual primitive action interface and of
passive/invariant action data. No new physical action is selected. -/
namespace D0.Research.NativeDynamicalOwnership
open D0.Foundation
open D0.Foundation.VerifiabilityNecessity
open D0.Foundation.PopperianBootstrap
open D0.Foundation.EndogenousActionQuantum
open D0.Foundation.ObservableCompletionCanonicity
open D0.Geometry
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

end
end D0.Research.NativeDynamicalOwnership
