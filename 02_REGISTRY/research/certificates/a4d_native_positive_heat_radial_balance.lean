import a4d_native_composed_feedback_dynamics
import a4d_native_weighted_dirac_boundary
import D0.Geometry.ArchiveCovariantCubicalDifferential

/-! Full-price radial balance for the positive graded Hodge binding.
This does not select W, a physical preparation, a heat normalization, or a gate.
The grade/spectral argument and uniform all-L bound have separate analytic scope.
Prior research capsules are compiled unchanged into an isolated import directory
by the companion checker's --compile mode. -/
namespace D0.Research.NativePositiveHeatRadialBalance
noncomputable section
open Matrix
open scoped BigOperators
open D0.Research.NativeComposedFeedbackDynamics

section Thermal
variable {ι : Type*} [Fintype ι] [DecidableEq ι] [Nonempty ι]

def thermalEnergy (beta : ℝ) (lambda : ι → ℝ) : ℝ :=
  (∑ i, Real.exp (-beta * lambda i) * lambda i) / thermalPartition beta lambda

def radialSpectrum (lambda : ι → ℝ) (t : ℝ) (i : ι) : ℝ :=
  Real.exp (-2*t) * lambda i

omit [Fintype ι] [DecidableEq ι] [Nonempty ι] in
theorem radialSpectrum_zero (lambda : ι → ℝ) : radialSpectrum lambda 0 = lambda := by
  funext i
  simp [radialSpectrum]

omit [Fintype ι] [DecidableEq ι] [Nonempty ι] in
theorem radialSpectrum_derivative (lambda : ι → ℝ) (i : ι) :
    HasDerivAt (fun t => radialSpectrum lambda t i) (-2 * lambda i) 0 := by
  convert (((hasDerivAt_id (0 : ℝ)).const_mul (-2)).exp).mul_const (lambda i) using 1
  norm_num [radialSpectrum]

omit [DecidableEq ι] [Nonempty ι] in
theorem radial_thermal_source (beta : ℝ) (lambda : ι → ℝ) :
    thermalSource beta lambda (fun i => -2 * lambda i) = 2 * thermalEnergy beta lambda := by
  unfold thermalSource thermalEnergy
  rw [show (∑ i, Real.exp (-beta*lambda i) * (-2*lambda i)) =
      (-2)*(∑ i, Real.exp (-beta*lambda i)*lambda i) by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i _
    ring]
  ring

theorem actual_heat_radial_derivative (beta : ℝ) (lambda : ι → ℝ) (hb : beta ≠ 0) :
    HasDerivAt (fun t => heatContribution beta (radialSpectrum lambda t))
      (2 * thermalEnergy beta lambda) 0 := by
  have h := genuine_thermal_source beta 0 (radialSpectrum lambda)
    (fun i => -2 * lambda i) hb (radialSpectrum_derivative lambda)
  simpa only [radialSpectrum_zero, radial_thermal_source] using h

/-- The literal diagonal constant-metric pencil, on each full Fourier mode. -/
def shapeSpectrum (a b c : ι → ℝ) (t : ℝ) (i : ι) : ℝ :=
  a i / (1+t) + b i / (1-t) + c i

def modeMean (beta : ℝ) (lambda v : ι → ℝ) : ℝ :=
  (∑ i, Real.exp (-beta * lambda i) * v i) / thermalPartition beta lambda

omit [Fintype ι] [DecidableEq ι] [Nonempty ι] in
theorem shapeSpectrum_zero (a b c : ι → ℝ) :
    shapeSpectrum a b c 0 = fun i => a i + b i + c i := by
  funext i
  simp [shapeSpectrum]

omit [Fintype ι] [DecidableEq ι] [Nonempty ι] in
theorem shapeSpectrum_derivative (a b c : ι → ℝ) (i : ι) :
    HasDerivAt (fun t => shapeSpectrum a b c t i) (-a i + b i) 0 := by
  have h₁ := (hasDerivAt_const (0 : ℝ) (a i)).div
    ((hasDerivAt_const (0 : ℝ) 1).add (hasDerivAt_id (0 : ℝ))) (by norm_num)
  have h₂ := (hasDerivAt_const (0 : ℝ) (b i)).div
    ((hasDerivAt_const (0 : ℝ) 1).sub (hasDerivAt_id (0 : ℝ))) (by norm_num)
  have h := (h₁.add h₂).add_const (c i)
  simpa [shapeSpectrum] using h

omit [DecidableEq ι] [Nonempty ι] in
theorem shape_thermal_source (beta : ℝ) (lambda a b : ι → ℝ) :
    thermalSource beta lambda (fun i => -a i + b i) =
      modeMean beta lambda a - modeMean beta lambda b := by
  unfold thermalSource modeMean
  simp_rw [mul_add, mul_neg, Finset.sum_add_distrib, Finset.sum_neg_distrib]
  ring

theorem actual_shape_heat_derivative (beta : ℝ) (a b c : ι → ℝ) (hb : beta ≠ 0) :
    HasDerivAt (fun t => heatContribution beta (shapeSpectrum a b c t))
      (modeMean beta (fun i => a i+b i+c i) a -
       modeMean beta (fun i => a i+b i+c i) b) 0 := by
  have h := genuine_thermal_source beta 0 (shapeSpectrum a b c)
    (fun i => -a i+b i) hb (shapeSpectrum_derivative a b c)
  simpa only [shapeSpectrum_zero, shape_thermal_source] using h

theorem thermalEnergy_nonnegative (beta : ℝ) (lambda : ι → ℝ)
    (hl : ∀ i, 0 ≤ lambda i) : 0 ≤ thermalEnergy beta lambda := by
  apply div_nonneg
  · exact Finset.sum_nonneg (fun i _ => mul_nonneg (Real.exp_pos _).le (hl i))
  · exact (thermal_partition_positive beta lambda).le

theorem thermalEnergy_positive (beta : ℝ) (lambda : ι → ℝ)
    (hl : ∀ i, 0 ≤ lambda i) (hp : ∃ i, 0 < lambda i) :
    0 < thermalEnergy beta lambda := by
  apply div_pos _ (thermal_partition_positive beta lambda)
  rcases hp with ⟨i, hi⟩
  exact Finset.sum_pos' (fun j _ => mul_nonneg (Real.exp_pos _).le (hl j))
    ⟨i, Finset.mem_univ i, mul_pos (Real.exp_pos _) hi⟩

theorem full_price_radial_derivative (beta : ℝ) (lambda : ι → ℝ) (hb : beta ≠ 0)
    (remainder : ℝ → ℝ) (r : ℝ) (hr : HasDerivAt remainder r 0) :
    HasDerivAt (fun t => heatContribution beta (radialSpectrum lambda t) + remainder t)
      (2 * thermalEnergy beta lambda + r) 0 :=
  (actual_heat_radial_derivative beta lambda hb).add hr

omit [DecidableEq ι] [Nonempty ι] in
theorem complete_radial_balance (beta : ℝ) (lambda : ι → ℝ) (r : ℝ) :
    2 * thermalEnergy beta lambda + r = 0 ↔ r = -2 * thermalEnergy beta lambda := by
  constructor <;> intro h <;> linarith

theorem scale_stationary_remainder_excludes_stationarity
    (beta : ℝ) (lambda : ι → ℝ) (hb : beta ≠ 0)
    (hl : ∀ i, 0 ≤ lambda i) (hp : ∃ i, 0 < lambda i)
    (remainder : ℝ → ℝ) (hr : HasDerivAt remainder 0 0) :
    ¬ HasDerivAt (fun t => heatContribution beta (radialSpectrum lambda t) + remainder t) 0 0 := by
  intro hz
  have he := (full_price_radial_derivative beta lambda hb remainder 0 hr).unique hz
  have hpos := thermalEnergy_positive beta lambda hl hp
  linarith

theorem nonzero_calibration_retains_radial_source (beta a : ℝ) (lambda : ι → ℝ)
    (ha : a ≠ 0) (hl : ∀ i, 0 ≤ lambda i) (hp : ∃ i, 0 < lambda i) :
    a⁻¹ * (2 * thermalEnergy beta lambda) ≠ 0 := by
  apply mul_ne_zero (inv_ne_zero ha)
  exact ne_of_gt (mul_pos (by norm_num) (thermalEnergy_positive beta lambda hl hp))

omit [DecidableEq ι] [Nonempty ι] in
theorem zero_operator_control (beta : ℝ) : thermalEnergy beta (fun _ : ι => 0) = 0 := by
  simp [thermalEnergy]

def retainZeroModes {κ : Type*} (lambda : ι → ℝ) : ι ⊕ κ → ℝ :=
  Sum.elim lambda (fun _ => 0)

omit [DecidableEq ι] [Nonempty ι] in
theorem retained_zero_modes_partition {κ : Type*} [Fintype κ] [DecidableEq κ]
    (beta : ℝ) (lambda : ι → ℝ) :
    thermalPartition beta (retainZeroModes (κ := κ) lambda) =
      thermalPartition beta lambda + Fintype.card κ := by
  simp [thermalPartition, retainZeroModes, Fintype.sum_sum_type]

theorem all_retained_zero_modes_keep_strict_sign {κ : Type*} [Fintype κ] [DecidableEq κ]
    (beta : ℝ) (lambda : ι → ℝ)
    (hl : ∀ i, 0 ≤ lambda i) (hp : ∃ i, 0 < lambda i) :
    0 < thermalEnergy beta (retainZeroModes (κ := κ) lambda) := by
  apply thermalEnergy_positive
  · intro i
    cases i with
    | inl i => exact hl i
    | inr j => exact le_refl 0
  · rcases hp with ⟨i, hi⟩
    exact ⟨Sum.inl i, hi⟩

end Thermal

section JointAndGrade
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

theorem full_joint_radial_tangent (qS qT D : Matrix ι ι ℝ)
    (h : D*qT*D.transpose = qS) :
    D*((2 : ℝ) • qT)*D.transpose + (0 : Matrix ι ι ℝ)*qT*D.transpose +
      D*qT*(0 : Matrix ι ι ℝ).transpose = (2 : ℝ) • qS := by
  simp [h]

/-- No nilpotency or flat-link hypothesis enters the square similarity. -/
theorem scaled_square_similarity (A J JI : Matrix ι ι ℝ) (r : ℝ)
    (h : JI*J=1) :
    (r • (J*A*JI))*(r • (J*A*JI)) = r^2 • (J*(A*A)*JI) := by
  simp only [Matrix.smul_mul, Matrix.mul_smul, smul_smul, pow_two]
  congr 1
  rw [show (J*A*JI)*(J*A*JI) = J*A*(JI*J)*A*JI by noncomm_ring, h]
  simp [Matrix.mul_assoc]

theorem actual_weighted_dirac_square (N : ℕ)
    (W : D0.Geometry.ArchiveCochain N ≃ₗ[ℝ] D0.Geometry.ArchiveCochain N)
    (u : D0.Geometry.ArchiveCochain N) :
    D0.Research.NativeWeightedDiracBoundary.weightedDirac N W
      (D0.Research.NativeWeightedDiracBoundary.weightedDirac N W u) =
    D0.Geometry.dForward N (D0.Research.NativeWeightedDiracBoundary.weightedCodiff N W u) +
      D0.Research.NativeWeightedDiracBoundary.weightedCodiff N W (D0.Geometry.dForward N u) :=
  D0.Research.NativeWeightedDiracBoundary.weighted_dirac_square N W u

end JointAndGrade

section ActualCurvedGrade
open D0 D0.Geometry

theorem kernel_create_degree_raise_int : ∀ r bra ket,
    carCreateInt r bra ket ≠ 0 → fockDegree bra = fockDegree ket + 1 := by decide

theorem kernel_create_degree_raise (r : Role) (bra ket : ArchiveFockState)
    (h : carCreate r bra ket ≠ 0) : fockDegree bra = fockDegree ket + 1 := by
  apply kernel_create_degree_raise_int r bra ket
  intro hz
  apply h
  simp [hz]

theorem actual_covariant_d_raises_degree {N : ℕ} {V : Type*}
    [AddCommGroup V] [Module ℝ V] (U : LinkConnection N ℝ V) (k : ℕ)
    (ψ : CoeffCochain N V) (hψ : CoeffHomogeneous k ψ) :
    CoeffHomogeneous (k + 1) (dConn U ψ) := by
  intro x bra hdeg
  simp only [dConn, coeffCreate, coeffShift, coeffTransport, Pi.sub_apply]
  rw [smul_eq_zero]
  right
  refine Finset.sum_eq_zero ?_
  intro r _
  refine Finset.sum_eq_zero ?_
  intro ket _
  by_cases hc : carCreate r bra ket = 0
  · rw [hc]
    simp
  · have hd := kernel_create_degree_raise r bra ket hc
    have hk : fockDegree ket ≠ k := by
      intro h
      apply hdeg
      omega
    simp [hψ x ket hk, hψ _ ket hk]
end ActualCurvedGrade

end
end D0.Research.NativePositiveHeatRadialBalance

#check D0.Research.NativePositiveHeatRadialBalance.radialSpectrum_zero
#print axioms D0.Research.NativePositiveHeatRadialBalance.radialSpectrum_zero
#check D0.Research.NativePositiveHeatRadialBalance.radialSpectrum_derivative
#print axioms D0.Research.NativePositiveHeatRadialBalance.radialSpectrum_derivative
#check D0.Research.NativePositiveHeatRadialBalance.radial_thermal_source
#print axioms D0.Research.NativePositiveHeatRadialBalance.radial_thermal_source
#check D0.Research.NativePositiveHeatRadialBalance.actual_heat_radial_derivative
#print axioms D0.Research.NativePositiveHeatRadialBalance.actual_heat_radial_derivative
#check D0.Research.NativePositiveHeatRadialBalance.thermalEnergy_nonnegative
#print axioms D0.Research.NativePositiveHeatRadialBalance.thermalEnergy_nonnegative
#check D0.Research.NativePositiveHeatRadialBalance.thermalEnergy_positive
#print axioms D0.Research.NativePositiveHeatRadialBalance.thermalEnergy_positive
#check D0.Research.NativePositiveHeatRadialBalance.full_price_radial_derivative
#print axioms D0.Research.NativePositiveHeatRadialBalance.full_price_radial_derivative
#check D0.Research.NativePositiveHeatRadialBalance.complete_radial_balance
#print axioms D0.Research.NativePositiveHeatRadialBalance.complete_radial_balance
#check D0.Research.NativePositiveHeatRadialBalance.scale_stationary_remainder_excludes_stationarity
#print axioms D0.Research.NativePositiveHeatRadialBalance.scale_stationary_remainder_excludes_stationarity
#check D0.Research.NativePositiveHeatRadialBalance.nonzero_calibration_retains_radial_source
#print axioms D0.Research.NativePositiveHeatRadialBalance.nonzero_calibration_retains_radial_source
#check D0.Research.NativePositiveHeatRadialBalance.zero_operator_control
#print axioms D0.Research.NativePositiveHeatRadialBalance.zero_operator_control
#check D0.Research.NativePositiveHeatRadialBalance.retained_zero_modes_partition
#print axioms D0.Research.NativePositiveHeatRadialBalance.retained_zero_modes_partition
#check D0.Research.NativePositiveHeatRadialBalance.all_retained_zero_modes_keep_strict_sign
#print axioms D0.Research.NativePositiveHeatRadialBalance.all_retained_zero_modes_keep_strict_sign
#check D0.Research.NativePositiveHeatRadialBalance.full_joint_radial_tangent
#print axioms D0.Research.NativePositiveHeatRadialBalance.full_joint_radial_tangent
#check D0.Research.NativePositiveHeatRadialBalance.scaled_square_similarity
#print axioms D0.Research.NativePositiveHeatRadialBalance.scaled_square_similarity
#check D0.Research.NativePositiveHeatRadialBalance.actual_weighted_dirac_square
#print axioms D0.Research.NativePositiveHeatRadialBalance.actual_weighted_dirac_square
#check D0.Geometry.dConn_raises_degree
#print axioms D0.Geometry.dConn_raises_degree
#check D0.Research.NativeComposedFeedbackDynamics.genuine_thermal_source
#print axioms D0.Research.NativeComposedFeedbackDynamics.genuine_thermal_source
#check D0.Research.NativeWeightedDiracBoundary.identity_weight_binding
#print axioms D0.Research.NativeWeightedDiracBoundary.identity_weight_binding

#check D0.Research.NativePositiveHeatRadialBalance.kernel_create_degree_raise_int
#print axioms D0.Research.NativePositiveHeatRadialBalance.kernel_create_degree_raise_int

#check D0.Research.NativePositiveHeatRadialBalance.kernel_create_degree_raise
#print axioms D0.Research.NativePositiveHeatRadialBalance.kernel_create_degree_raise

#check D0.Research.NativePositiveHeatRadialBalance.actual_covariant_d_raises_degree
#print axioms D0.Research.NativePositiveHeatRadialBalance.actual_covariant_d_raises_degree

#check D0.Research.NativePositiveHeatRadialBalance.shapeSpectrum_zero
#print axioms D0.Research.NativePositiveHeatRadialBalance.shapeSpectrum_zero
#check D0.Research.NativePositiveHeatRadialBalance.shapeSpectrum_derivative
#print axioms D0.Research.NativePositiveHeatRadialBalance.shapeSpectrum_derivative
#check D0.Research.NativePositiveHeatRadialBalance.shape_thermal_source
#print axioms D0.Research.NativePositiveHeatRadialBalance.shape_thermal_source
#check D0.Research.NativePositiveHeatRadialBalance.actual_shape_heat_derivative
#print axioms D0.Research.NativePositiveHeatRadialBalance.actual_shape_heat_derivative
