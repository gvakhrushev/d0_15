import D0.Geometry.ArchiveMetricMeasureHodgeLift
import D0.Geometry.A4DMetricStarSignatureBoundary
import D0.Geometry.A4DStarFiniteLorentzQuotient
import D0.Gauge.YangMillsKillingPositivity
import Mathlib.Analysis.Calculus.Deriv.Polynomial
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

/-! Research bindings for the existing Hodge and scalar-action owners.
No new physical action, matter source or on-shell definition is selected.
The two actual finite preparations and the continuum contrast obstruction
are proved analytically in the companion memo, not assumed Lean theorems. -/
namespace D0.Research.NativeCoupledHodgeScale
open D0 D0.Geometry D0.Gauge
open scoped BigOperators Matrix
noncomputable section

theorem actual_hodge_middle (mu p : ℝ) :
    hodgeMetricMeasureWeight 2 mu p = p / mu := by
  simp [hodgeMetricMeasureWeight, muExponent, div_eq_mul_inv, mul_comm]

theorem actual_hodge_middle_scale (s mu p : ℝ) (hs : s ≠ 0) (hm : mu ≠ 0) :
    hodgeMetricMeasureWeight 2 (s^2*mu) (s^2*p) =
      hodgeMetricMeasureWeight 2 mu p := by
  rw [actual_hodge_middle, actual_hodge_middle]
  field_simp

/-- The full five-degree formula, including the middle-degree exception.
Signed conductances are permitted by the actual scalar definition. This
does not import the positive-measure interpretation into Lorentz signature. -/
theorem actual_hodge_all_degrees (k : Fin 5) (s mu p : ℝ)
    (hs : s ≠ 0) (hm : mu ≠ 0) :
    hodgeMetricMeasureWeight k.val (s^2*mu) (s^k.val*p) =
      s ^ ((2 : ℤ) - (k.val : ℤ)) * hodgeMetricMeasureWeight k.val mu p := by
  fin_cases k <;>
    simp [hodgeMetricMeasureWeight, muExponent, zpow_neg, mul_zpow] <;> field_simp

theorem actual_transport_scale (N : ℕ)
    (F : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (R : ArchiveRolePhaseGroup N → Role → Matrix Role Role ℝ) (c : ℝ)
    (x : ArchiveRolePhaseGroup N) :
    transportedSolderCenter N (fun y => c • F y) R x =
      c • transportedSolderCenter N F R x := by
  ext r a
  simp only [transportedSolderCenter, Matrix.smul_mul, Matrix.smul_apply,
    smul_eq_mul]
  ring

theorem actual_transport_gram_scale (N : ℕ)
    (F : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (R : ArchiveRolePhaseGroup N → Role → Matrix Role Role ℝ) (c : ℝ)
    (x : ArchiveRolePhaseGroup N) :
    let T := transportedSolderCenter N F R x
    let Tc := transportedSolderCenter N (fun y => c • F y) R x
    Tc * roleLorentzMetric * Tc.transpose =
      c^2 • (T * roleLorentzMetric * T.transpose) := by
  dsimp
  rw [actual_transport_scale]
  simp only [Matrix.smul_mul, Matrix.transpose_smul, Matrix.mul_smul, smul_smul]
  rw [pow_two]

theorem actual_dressed_link_scale
    (F L G : Matrix Role Role ℝ) (c : ℝ) (hc : c ≠ 0)
    (hG : IsUnit G.det) :
    a4dDressedLink (c • F) L (c • G) = a4dDressedLink F L G := by
  letI : Invertible c := invertibleOfNonzero hc
  unfold a4dDressedLink
  rw [Matrix.inv_smul G c hG]
  simp [smul_smul, invOf_eq_inv, hc]

/-- An explicit instance of the old supplied-pairing action, rather than a
claim that this pairing or its curvature binding is already selected. -/
theorem actual_supplied_hodge_action
    {i k : Type} [Fintype i] [Fintype k]
    (W : Matrix i i ℝ) (C : i → Matrix k k ℝ) :
    discreteYangMillsAction
      (fun X Y : i → Matrix k k ℝ =>
        ∑ a, ∑ b, W a b * Matrix.trace (X a * Y b))
      (fun (_ _ : Unit) => C) =
        -(∑ a, ∑ b, W a b * Matrix.trace (C a * C b)) := by
  simp [discreteYangMillsAction]

theorem middle_compound_scale
    (M : Matrix (Fin 4) (Fin 4) ℝ) (mu s : ℝ) (hs : s ≠ 0)
    (a b c d : Fin 4) :
    (s^2*mu) * ((s⁻¹*M a c)*(s⁻¹*M b d)-(s⁻¹*M a d)*(s⁻¹*M b c)) =
      mu * (M a c*M b d-M a d*M b c) := by
  field_simp

/-- Every coefficient variation is retained. Vanishing curvature, not
vanishing indefinite action value, is the hypothesis. -/
theorem variable_weight_zero_curvature_stationary
    {i : Type} [Fintype i]
    (W : ℝ → Matrix i i ℝ) (dW : Matrix i i ℝ)
    (C : ℝ → i → ℝ) (dC : i → ℝ)
    (hw : ∀ a b, HasDerivAt (fun t => W t a b) (dW a b) 0)
    (hc : ∀ a, HasDerivAt (fun t => C t a) (dC a) 0)
    (hzero : ∀ a, C 0 a = 0) :
    HasDerivAt (fun t => ∑ a, ∑ b, W t a b * C t a * C t b) 0 0 := by
  have hterm : ∀ a b,
      HasDerivAt (fun t => W t a b * C t a * C t b) 0 0 := by
    intro a b
    simpa [hzero] using ((hw a b).mul (hc a)).mul (hc b)
  have hf : (fun t => ∑ a, ∑ b, W t a b * C t a * C t b) =
      ∑ a, ∑ b, fun t => W t a b * C t a * C t b := by
    ext t
    simp
  rw [hf]
  simpa using HasDerivAt.sum (u := Finset.univ) (fun a _ =>
    HasDerivAt.sum (u := Finset.univ) (fun b _ => hterm a b))

theorem scale_invariant_derivative (A : ℝ → ℝ) (v : ℝ)
    (hA : ∀ t, A t = v) : HasDerivAt A 0 0 := by
  have hfun : A = fun _ => v := funext hA
  rw [hfun]
  exact hasDerivAt_const 0 v

theorem volume_scale_derivative (A lam V : ℝ) :
    HasDerivAt (fun t : ℝ => A+lam*(1+t)^2*V) (2*lam*V) 0 := by
  simpa [mul_assoc, mul_left_comm, mul_comm] using
    (((((hasDerivAt_id (0 : ℝ)).const_add 1).pow 2).const_mul lam).mul_const V).const_add A

theorem volume_term_full_gate_forces_zero (A lam V : ℝ) (hV : V ≠ 0)
    (hgate : HasDerivAt (fun t : ℝ => A+lam*(1+t)^2*V) 0 0) : lam = 0 := by
  have hz := (volume_scale_derivative A lam V).unique hgate
  rcases mul_eq_zero.mp hz with h | h
  · rcases mul_eq_zero.mp h with h | h
    · norm_num at h
    · exact h
  · exact (hV h).elim

/-- The scale-invariant parts may differ between experiments. Only their
own plus/minus equality and the equal volume readings are used. -/
theorem equal_volume_scale_contrasts (A B vp vm : ℝ) :
    ((A+vp)-(A+vm))/2 = ((B+vp)-(B+vm))/2 := by ring

theorem paired_physical_contrast (eps I0 : ℝ) :
    (((1+eps)*I0-(1-eps)*I0)/2) -
      (((1+eps)*(I0/4)-(1-eps)*(I0/4))/2) = (3/4:ℝ)*eps*I0 := by ring

theorem paired_error_lower_bound (x y d : ℝ) (h : |x-y| ≥ d) :
    max |x| |y| ≥ d/2 := by
  have htri : |x-y| ≤ |x|+|y| := by
    simpa using abs_sub_le x 0 y
  have hx := le_max_left |x| |y|
  have hy := le_max_right |x| |y|
  linarith

/-- Exact inverse of the periodic row average on the single first harmonic. -/
theorem exact_temporal_center (a theta delta : ℝ) (hd : Real.cos delta ≠ 0) :
    ((1+a/Real.cos delta*Real.cos (theta+delta)) +
      (1+a/Real.cos delta*Real.cos (theta-delta)))/2 = 1+a*Real.cos theta := by
  rw [Real.cos_add, Real.cos_sub]
  field_simp
  ring

/-- Exact inverse for rows constant along their own spatial direction. -/
theorem exact_spatial_cayley_center
    (A F : Matrix (Fin 4) (Fin 4) ℝ) (h : IsUnit (1-A).det) :
    (F*(1-A))*(1+(1-A)⁻¹*(1+A)) = (2:ℝ) • F := by
  have hc : (1-A)*(1+(1-A)⁻¹*(1+A)) = (2:ℝ) • (1:Matrix (Fin 4) (Fin 4) ℝ) := by
    rw [Matrix.mul_add, Matrix.mul_one, ← Matrix.mul_assoc,
      Matrix.mul_nonsing_inv (1-A) h, Matrix.one_mul]
    module
  rw [Matrix.mul_assoc, hc, Matrix.mul_smul, Matrix.mul_one]

theorem exact_equal_volume_solder (c f : ℝ) (hc : c ≠ 0) :
    (Matrix.diagonal (![c*f,-f/c,-f,-f]) : Matrix (Fin 4) (Fin 4) ℝ).det = -f^4 := by
  rw [Matrix.det_diagonal]
  simp [Fin.prod_univ_succ]
  field_simp

#print archive_metric_measure_hodge_lift_owner
#print hodgeMetricMeasureWeight
#check a4dDressedLink
#check discreteYangMillsAction
#check discreteYangMillsAction_nonnegative_of_killing_nonpos
#print axioms actual_hodge_middle
#print axioms actual_hodge_middle_scale
#print axioms actual_hodge_all_degrees
#print axioms actual_transport_scale
#print axioms actual_transport_gram_scale
#print axioms actual_dressed_link_scale
#print axioms actual_supplied_hodge_action
#print axioms middle_compound_scale
#print axioms variable_weight_zero_curvature_stationary
#print axioms scale_invariant_derivative
#print axioms volume_scale_derivative
#print axioms volume_term_full_gate_forces_zero
#print axioms equal_volume_scale_contrasts
#print axioms paired_physical_contrast
#print axioms paired_error_lower_bound
#print axioms exact_temporal_center
#print axioms exact_spatial_cayley_center
#print axioms exact_equal_volume_solder
end
end D0.Research.NativeCoupledHodgeScale
