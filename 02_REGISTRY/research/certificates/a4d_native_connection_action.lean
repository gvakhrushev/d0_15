import D0.Gauge.YangMillsKillingPositivity
import D0.Gauge.MatrixRepGaugeTransform
import D0.Gauge.NonAbelianSeamObstructionGap
import D0.Geometry.A4DRawSolderFrameAction
import Mathlib.Analysis.Calculus.Deriv.Polynomial

/-! Existing connection functionals and the actual transported Gram map.
This research capsule does not choose a new action or assert that a supplied
curvature is the curvature of a native connection. The infinite-mesh contrast
obstruction and its smooth preparation are proved in the companion memo. -/
namespace D0.Research.NativeConnectionAction
open scoped BigOperators Matrix
open D0 D0.Geometry D0.Gauge
noncomputable section

theorem matrix_action_is_trace_instance
    {i j k : Type} [Fintype i] [Fintype j] [Fintype k]
    (K : Matrix i j (Matrix k k ℝ)) :
    matrixRepYangMillsAction K =
      discreteYangMillsAction (fun X Y : Matrix k k ℝ => Matrix.trace (X * Y)) K := rfl

theorem matrix_action_smul
    {i j k : Type} [Fintype i] [Fintype j] [Fintype k]
    (K : Matrix i j (Matrix k k ℝ)) (t : ℝ) :
    matrixRepYangMillsAction (fun a b => t • K a b) =
      t ^ 2 * matrixRepYangMillsAction K := by
  unfold matrixRepYangMillsAction
  simp only [Matrix.smul_mul, Matrix.mul_smul, smul_smul, Matrix.trace_smul,
    smul_eq_mul, ← Finset.mul_sum]
  ring

theorem matrix_action_singleton {k : Type} [Fintype k]
    (X : Matrix k k ℝ) :
    matrixRepYangMillsAction (fun (_ _ : Unit) => X) = -Matrix.trace (X * X) := by
  simp [matrixRepYangMillsAction]

theorem matrix_action_polarization
    {i j k : Type} [Fintype i] [Fintype j] [Fintype k]
    (K V : Matrix i j (Matrix k k ℝ)) (t : ℝ) :
    matrixRepYangMillsAction (fun a b => K a b + t • V a b) =
      matrixRepYangMillsAction K -
      2*t*(∑ a, ∑ b, Matrix.trace (K a b * V a b)) +
      t^2*matrixRepYangMillsAction V := by
  have hx : ∀ a b, Matrix.trace ((K a b + t • V a b) * (K a b + t • V a b)) =
      Matrix.trace (K a b * K a b) + 2*t*Matrix.trace (K a b * V a b) +
      t^2*Matrix.trace (V a b * V a b) := by
    intro a b
    simp only [Matrix.add_mul, Matrix.mul_add, Matrix.smul_mul,
      Matrix.mul_smul, Matrix.trace_add, Matrix.trace_smul, smul_eq_mul]
    rw [Matrix.trace_mul_comm (V a b) (K a b)]
    ring
  unfold matrixRepYangMillsAction
  simp_rw [hx]
  simp only [Finset.sum_add_distrib, ← Finset.mul_sum]
  ring

theorem matrix_action_first_variation
    {i j k : Type} [Fintype i] [Fintype j] [Fintype k]
    (K V : Matrix i j (Matrix k k ℝ)) :
    HasDerivAt (fun t : ℝ => matrixRepYangMillsAction (fun a b => K a b+t • V a b))
      (-2*(∑ a, ∑ b, Matrix.trace (K a b * V a b))) 0 := by
  simp_rw [matrix_action_polarization]
  convert ((hasDerivAt_const (0 : ℝ) (matrixRepYangMillsAction K)).sub
    (((hasDerivAt_id (0 : ℝ)).const_mul 2).mul_const
      (∑ a, ∑ b, Matrix.trace (K a b * V a b)))).add
    (((hasDerivAt_id (0 : ℝ)).pow 2).mul_const (matrixRepYangMillsAction V)) using 1
  simp [id]

theorem seam_action_smul {n : Type} [Fintype n]
    (B : FiniteSeamMap n) (X : Matrix n n ℝ) (t : ℝ) :
    seamEnergy B (t • X) = t^2*seamEnergy B X := by
  simp only [seamEnergy, seamCommutator, D0.Algebra.commutator,
    Matrix.mul_smul, Matrix.smul_mul, ← smul_sub, Matrix.smul_apply, smul_eq_mul,
    mul_pow, ← Finset.mul_sum]

/-- Zero supplied curvature is stationary along every differentiable
curvature path. Applying this to a link binding still requires that binding
and its differentiability; it is not a converse for nonzero curvature. -/
theorem zero_curvature_path_stationary
    {i j k : Type} [Fintype i] [Fintype j] [Fintype k]
    (K : ℝ → Matrix i j (Matrix k k ℝ)) (V : Matrix i j (Matrix k k ℝ))
    (h0 : ∀ a b u v, K 0 a b u v = 0)
    (hderiv : ∀ a b u v, HasDerivAt (fun t => K t a b u v) (V a b u v) 0) :
    HasDerivAt (fun t => matrixRepYangMillsAction (K t)) 0 0 := by
  have hp : ∀ a b u v,
      HasDerivAt (fun t => K t a b u v * K t a b v u) 0 0 := by
    intro a b u v
    simpa [h0] using (hderiv a b u v).mul (hderiv a b v u)
  have hs := (HasDerivAt.sum (u := Finset.univ) (fun a _ =>
    HasDerivAt.sum (u := Finset.univ) (fun b _ =>
    HasDerivAt.sum (u := Finset.univ) (fun u _ =>
    HasDerivAt.sum (u := Finset.univ) (fun v _ => hp a b u v))))).neg
  have hf : (fun t => matrixRepYangMillsAction (K t)) =
      -(∑ a, ∑ b, ∑ u, ∑ v, fun t => K t a b u v * K t a b v u) := by
    ext t
    simp [matrixRepYangMillsAction, Matrix.trace, Matrix.diag, Matrix.mul_apply]
  rw [hf]
  simpa using hs

theorem actual_transport_smul (N : ℕ)
    (F : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (R : ArchiveRolePhaseGroup N → Role → Matrix Role Role ℝ) (c : ℝ)
    (x : ArchiveRolePhaseGroup N) :
    transportedSolderCenter N (fun y => c • F y) R x =
      c • transportedSolderCenter N F R x := by
  ext r a
  simp only [transportedSolderCenter, Matrix.smul_mul, Matrix.smul_apply,
    smul_eq_mul]
  ring

theorem actual_transport_gram_smul (N : ℕ)
    (F : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (R : ArchiveRolePhaseGroup N → Role → Matrix Role Role ℝ) (c : ℝ)
    (x : ArchiveRolePhaseGroup N) :
    let T := transportedSolderCenter N F R x
    let Tc := transportedSolderCenter N (fun y => c • F y) R x
    Tc * roleLorentzMetric * Tc.transpose =
      c^2 • (T * roleLorentzMetric * T.transpose) := by
  dsimp
  rw [actual_transport_smul]
  simp only [Matrix.smul_mul, Matrix.transpose_smul, Matrix.mul_smul, smul_smul]
  rw [pow_two]

/-- Geometry-blind factorization is a hypothesis, not a definition of a gate. -/
theorem coframe_blind_contrast {F Z : Type*} (S : F → Z → ℝ) (Phi : Z → ℝ)
    (hfactor : ∀ f z, S f z = Phi z) (fp fm : F) (z : Z) :
    (S fp z - S fm z)/2 = 0 := by rw [hfactor, hfactor]; ring

theorem coframe_blind_variation {F Z : Type*} (S : F → Z → ℝ) (Phi : Z → ℝ)
    (hfactor : ∀ f z, S f z = Phi z) (curve : ℝ → F) (z : Z) :
    HasDerivAt (fun t => S (curve t) z) 0 0 := by
  simp_rw [hfactor]
  exact hasDerivAt_const 0 (Phi z)

/-- At a fixed retained connection the complete value set of an auxiliary
gate independent of the coframe is exactly independent of that coframe. -/
theorem coframe_blind_stationary_value_set {F Z : Type*}
    (S : F → Z → ℝ) (Phi : Z → ℝ) (gate : Z → Prop)
    (hfactor : ∀ f z, S f z = Phi z) (f g : F) :
    {v : ℝ | ∃ z, gate z ∧ S f z = v} = {v : ℝ | ∃ z, gate z ∧ S g z = v} := by
  simp_rw [hfactor]

theorem homothetic_physical_contrast (eps I0 : ℝ) :
    ((1+eps)*I0-(1-eps)*I0)/2 = eps*I0 := by ring

/-- The calibrated native value cancels for every calibration, even if a
mesh-dependent multiplier were allowed. This does not select such a multiplier. -/
theorem calibrated_contrast_gap (a n eps I0 : ℝ) :
    a⁻¹*((n-n)/2)-((1+eps)*I0-(1-eps)*I0)/2 = -eps*I0 := by ring

def eta4 : Matrix (Fin 4) (Fin 4) ℝ := !![1,0,0,0; 0,-1,0,0; 0,0,-1,0; 0,0,0,-1]
def lorentzSix (b0 b1 b2 r0 r1 r2 : ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  !![0,b0,b1,b2; b0,0,r0,r1; b1,-r0,0,r2; b2,-r1,-r2,0]

theorem lorentzSix_is_tangent (b0 b1 b2 r0 r1 r2 : ℝ) :
    (lorentzSix b0 b1 b2 r0 r1 r2).transpose * eta4 +
      eta4 * lorentzSix b0 b1 b2 r0 r1 r2 = 0 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [lorentzSix, eta4, Matrix.mul_apply, Fin.sum_univ_succ]

theorem lorentzSix_trace_action (b0 b1 b2 r0 r1 r2 : ℝ) :
    matrixRepYangMillsAction (fun (_ _ : Unit) => lorentzSix b0 b1 b2 r0 r1 r2) =
      2*(r0^2+r1^2+r2^2-b0^2-b1^2-b2^2) := by
  rw [matrix_action_singleton]
  simp [lorentzSix, Matrix.trace, Matrix.diag, Matrix.mul_apply, Fin.sum_univ_succ]
  ring

theorem euclidean_skew_loses_boosts (b0 b1 b2 r0 r1 r2 : ℝ) :
    D0.Matter.isSkew (lorentzSix b0 b1 b2 r0 r1 r2) ↔
      b0=0 ∧ b1=0 ∧ b2=0 := by
  constructor
  · intro h
    have h0 := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M 0 1) h
    have h1 := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M 0 2) h
    have h2 := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M 0 3) h
    simp [lorentzSix] at h0 h1 h2
    exact ⟨by linarith, by linarith, by linarith⟩
  · rintro ⟨rfl,rfl,rfl⟩
    ext i j
    fin_cases i <;> fin_cases j <;> simp [lorentzSix]

theorem lorentz_null_value_not_stationary :
    matrixRepYangMillsAction (fun (_ _ : Unit) => lorentzSix 1 0 0 1 0 0) = 0 ∧
    HasDerivAt (fun t : ℝ =>
      matrixRepYangMillsAction (fun (_ _ : Unit) => lorentzSix (1+t) 0 0 1 0 0)) (-4) 0 := by
  constructor
  · norm_num [lorentzSix_trace_action]
  · simp_rw [lorentzSix_trace_action]
    convert ((((hasDerivAt_id (0 : ℝ)).const_add 1).pow 2).const_sub 1).const_mul 2 using 1 <;>
      norm_num [id]

/-- Once the invariant quadratic family has been classified, no coefficient
choice in that family gives a nonzero positive semidefinite form. -/
theorem invariant_quadratic_positive_only_zero (a b : ℝ)
    (h : ∀ x y : ℝ, 0 ≤ a*(x^2-y^2)+2*b*x*y) : a=0 ∧ b=0 := by
  have h10 := h 1 0
  have h01 := h 0 1
  have ha : a=0 := by norm_num at h10 h01; linarith
  have h11 := h 1 1
  have h1n := h 1 (-1)
  constructor
  · exact ha
  · norm_num at h11 h1n; linarith

/-- A generic continuity consequence; a native conjugacy sequence must still
be constructed. It does not identify zero value with stationarity. -/
theorem continuous_orbit_contraction_value {X : Type*} [TopologicalSpace X]
    (Phi : X → ℝ) (x0 x : X) (seq : ℕ → X)
    (hcont : ContinuousAt Phi x0)
    (hlim : Filter.Tendsto seq Filter.atTop (nhds x0))
    (hvalue : ∀ n, Phi (seq n)=Phi x) : Phi x=Phi x0 := by
  have hv := hcont.tendsto.comp hlim
  have he : (fun n => Phi (seq n)) = fun _ => Phi x := funext hvalue
  change Filter.Tendsto (fun n => Phi (seq n)) Filter.atTop (nhds (Phi x0)) at hv
  rw [he] at hv
  exact tendsto_nhds_unique tendsto_const_nhds hv

#check discreteYangMillsAction
#check discreteYangMillsAction_nonnegative_of_killing_nonpos
#check matrix_rep_yang_mills_action_nonnegative_of_skew
#check exact_bianchi_identity_replaced_by_graded_incidence_closure
#print exactBianchiIdentityReplacedByGradedIncidenceClosure
#check FiniteSeamMap
#print axioms matrix_action_is_trace_instance
#print axioms matrix_action_smul
#print axioms matrix_action_singleton
#print axioms matrix_action_polarization
#print axioms matrix_action_first_variation
#print axioms seam_action_smul
#print axioms zero_curvature_path_stationary
#print axioms actual_transport_smul
#print axioms actual_transport_gram_smul
#print axioms coframe_blind_contrast
#print axioms coframe_blind_variation
#print axioms coframe_blind_stationary_value_set
#print axioms homothetic_physical_contrast
#print axioms calibrated_contrast_gap
#print axioms lorentzSix_is_tangent
#print axioms lorentzSix_trace_action
#print axioms euclidean_skew_loses_boosts
#print axioms lorentz_null_value_not_stationary
#print axioms invariant_quadratic_positive_only_zero
#print axioms continuous_orbit_contraction_value
end
end D0.Research.NativeConnectionAction
