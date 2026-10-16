import D0.Geometry.ArchiveWeightedHodgeDirac
import D0.Geometry.ArchiveHodgeCARDiracKernel
import D0.Geometry.ArchiveMetricMeasureHodgeLift
import D0.Geometry.SpectralActionLadder
import Mathlib.Analysis.Complex.Exponential
import Mathlib.Tactic

/-! Construct the documented weighted adjoint on the actual cochains.
W is a supplied invertible operator; neither its physical selection nor
positivity is inferred from the old Boolean owner. The flat signed spectral
binding and all-size analytic arguments are in the companion proof. -/
namespace D0.Research.NativeWeightedDiracBoundary
open D0 D0.Geometry
open scoped BigOperators
noncomputable section

-- Kernel reduction replaces the upstream native_decide CAR leaf proofs.
-- The carrier and matrices are the literal D0 declarations, not a new model.
set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem kernel_annihilate_int : ∀ r s bra ket,
    anticommutatorInt (carAnnihilateInt r) (carAnnihilateInt s) bra ket = 0 := by decide

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem kernel_create_int : ∀ r s bra ket,
    anticommutatorInt (carCreateInt r) (carCreateInt s) bra ket = 0 := by decide

theorem kernel_annihilate_car (r s : Role) (bra ket : ArchiveFockState) :
    anticommutator (carAnnihilate r) (carAnnihilate s) bra ket = 0 := by
  have h := congrArg (fun z : ℤ => (z : ℝ)) (kernel_annihilate_int r s bra ket)
  simpa [anticommutator, anticommutatorInt] using h

theorem kernel_create_car (r s : Role) (bra ket : ArchiveFockState) :
    anticommutator (carCreate r) (carCreate s) bra ket = 0 := by
  have h := congrArg (fun z : ℤ => (z : ℝ)) (kernel_create_int r s bra ket)
  simpa [anticommutator, anticommutatorInt] using h

theorem kernel_create_action_anticommute (N : ℕ) (r s : Role)
    (ψ : ArchiveCochain N) :
    createAction N r (createAction N s ψ) +
      createAction N s (createAction N r ψ) = 0 := by
  classical
  funext p
  simp only [Pi.add_apply, Pi.zero_apply]
  rw [createAction_comp_apply, createAction_comp_apply]
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_eq_zero
  intro ket hket
  rw [← add_mul]
  have hcar := kernel_create_car r s p.2 ket
  unfold anticommutator at hcar
  rw [hcar]
  simp

/-- Directional forward-create pieces anticommute. -/
theorem kernel_forward_direction_anticommute (N : ℕ) (r s : Role)
    (ψ : ArchiveCochain N) :
    forwardCreateDirection N r (forwardCreateDirection N s ψ) +
      forwardCreateDirection N s (forwardCreateDirection N r ψ) = 0 := by
  change
    createAction N r
        (forwardSite N r (createAction N s (forwardSite N s ψ))) +
      createAction N s
        (forwardSite N s (createAction N r (forwardSite N r ψ))) = 0
  rw [forwardSite_createAction_comm N r s (forwardSite N s ψ)]
  rw [forwardSite_createAction_comm N s r (forwardSite N r ψ)]
  rw [forwardSite_comm N s r ψ]
  exact kernel_create_action_anticommute N r s
    (forwardSite N r (forwardSite N s ψ))


theorem kernel_d_sq (N : ℕ) (ψ : ArchiveCochain N) :
    dForward N (dForward N ψ) = 0 := by
  classical
  rw [dForward_eq_sum_directions N ψ, dForward_sum]
  simp_rw [dForward_eq_sum_directions]
  funext p
  simp only [Finset.sum_apply, Pi.zero_apply]
  let X : Role → Role → ℝ :=
    fun r s => forwardCreateDirection N r
      (forwardCreateDirection N s ψ) p
  change (∑ s : Role, ∑ r : Role, X r s) = 0
  have hanti : ∀ r s : Role, X r s + X s r = 0 := by
    intro r s
    have h := congrFun (kernel_forward_direction_anticommute N r s ψ) p
    simpa [X] using h
  have hpair : (∑ s : Role, ∑ r : Role, (X r s + X s r)) = 0 := by
    apply Finset.sum_eq_zero
    intro s hs
    apply Finset.sum_eq_zero
    intro r hr
    exact hanti r s
  have hswap :
      (∑ s : Role, ∑ r : Role, X s r) =
        ∑ s : Role, ∑ r : Role, X r s := by
    rw [Finset.sum_comm]
  simp only [Finset.sum_add_distrib] at hpair
  rw [hswap] at hpair
  linarith


theorem kernel_annihilate_action_anticommute (N : ℕ) (r s : Role) (ψ : ArchiveCochain N) :
    annihilateAction N r (annihilateAction N s ψ) +
      annihilateAction N s (annihilateAction N r ψ) = 0 := by
  classical
  funext p
  simp only [Pi.add_apply, Pi.zero_apply]
  rw [annihilateAction_comp_apply, annihilateAction_comp_apply, ← Finset.sum_add_distrib]
  apply Finset.sum_eq_zero
  intro ket _
  have hcar := kernel_annihilate_car r s p.2 ket
  unfold anticommutator at hcar
  rw [← add_mul, hcar]
  simp

theorem kernel_backward_direction_anticommute (N : ℕ) (r s : Role)
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
  exact kernel_annihilate_action_anticommute N r s
    (backwardSite N r (backwardSite N s ψ))


theorem kernel_codiff_sq (N : ℕ) (ψ : ArchiveCochain N) :
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
    congrFun (kernel_backward_direction_anticommute N r s ψ) p


def weightedCodiff (N : ℕ)
    (W : ArchiveCochain N ≃ₗ[ℝ] ArchiveCochain N)
    (u : ArchiveCochain N) : ArchiveCochain N :=
  W.symm (hodgeCodifferential N (W u))

def weightedDirac (N : ℕ)
    (W : ArchiveCochain N ≃ₗ[ℝ] ArchiveCochain N)
    (u : ArchiveCochain N) : ArchiveCochain N :=
  dForward N u + weightedCodiff N W u

def weightedPairing (N : ℕ)
    (W : ArchiveCochain N ≃ₗ[ℝ] ArchiveCochain N)
    (u v : ArchiveCochain N) : ℝ := cochainPairing N u (W v)

theorem weighted_codiff_add (N : ℕ)
    (W : ArchiveCochain N ≃ₗ[ℝ] ArchiveCochain N)
    (u v : ArchiveCochain N) :
    weightedCodiff N W (u+v) = weightedCodiff N W u + weightedCodiff N W v := by
  simp [weightedCodiff, hodgeCodifferential_add]

theorem weighted_codiff_smul (N : ℕ)
    (W : ArchiveCochain N ≃ₗ[ℝ] ArchiveCochain N)
    (a : ℝ) (u : ArchiveCochain N) :
    weightedCodiff N W (a • u) = a • weightedCodiff N W u := by
  simp [weightedCodiff, hodgeCodifferential_smul]

theorem weighted_codiff_sq (N : ℕ)
    (W : ArchiveCochain N ≃ₗ[ℝ] ArchiveCochain N)
    (u : ArchiveCochain N) :
    weightedCodiff N W (weightedCodiff N W u) = 0 := by
  simp [weightedCodiff, kernel_codiff_sq]

theorem weighted_dirac_square (N : ℕ)
    (W : ArchiveCochain N ≃ₗ[ℝ] ArchiveCochain N)
    (u : ArchiveCochain N) :
    weightedDirac N W (weightedDirac N W u) =
      dForward N (weightedCodiff N W u) + weightedCodiff N W (dForward N u) := by
  unfold weightedDirac
  rw [dForward_add, weighted_codiff_add, kernel_d_sq, weighted_codiff_sq]
  simp

theorem weighted_d_adjoint (N : ℕ)
    (W : ArchiveCochain N ≃ₗ[ℝ] ArchiveCochain N)
    (u v : ArchiveCochain N) :
    weightedPairing N W (dForward N u) v =
      weightedPairing N W u (weightedCodiff N W v) := by
  simp only [weightedPairing, weightedCodiff, LinearEquiv.apply_symm_apply]
  exact dForward_adjoint N u (W v)

theorem weighted_pairing_symm (N : ℕ)
    (W : ArchiveCochain N ≃ₗ[ℝ] ArchiveCochain N)
    (hW : ∀ u v, cochainPairing N (W u) v = cochainPairing N u (W v))
    (u v : ArchiveCochain N) :
    weightedPairing N W u v = weightedPairing N W v u := by
  unfold weightedPairing
  rw [← hW, cochainPairing_symm]

theorem weighted_codiff_adjoint (N : ℕ)
    (W : ArchiveCochain N ≃ₗ[ℝ] ArchiveCochain N)
    (hW : ∀ u v, cochainPairing N (W u) v = cochainPairing N u (W v))
    (u v : ArchiveCochain N) :
    weightedPairing N W (weightedCodiff N W u) v =
      weightedPairing N W u (dForward N v) := by
  rw [weighted_pairing_symm N W hW, ← weighted_d_adjoint,
    weighted_pairing_symm N W hW]

theorem weighted_pairing_add_left (N : ℕ)
    (W : ArchiveCochain N ≃ₗ[ℝ] ArchiveCochain N)
    (u v z : ArchiveCochain N) :
    weightedPairing N W (u+v) z = weightedPairing N W u z + weightedPairing N W v z := by
  simp [weightedPairing, cochainPairing, add_mul, Finset.sum_add_distrib]

theorem weighted_pairing_add_right (N : ℕ)
    (W : ArchiveCochain N ≃ₗ[ℝ] ArchiveCochain N)
    (u v z : ArchiveCochain N) :
    weightedPairing N W u (v+z) = weightedPairing N W u v + weightedPairing N W u z := by
  simp [weightedPairing, cochainPairing, mul_add, Finset.sum_add_distrib]

theorem weighted_dirac_symmetric (N : ℕ)
    (W : ArchiveCochain N ≃ₗ[ℝ] ArchiveCochain N)
    (hW : ∀ u v, cochainPairing N (W u) v = cochainPairing N u (W v))
    (u v : ArchiveCochain N) :
    weightedPairing N W (weightedDirac N W u) v =
      weightedPairing N W u (weightedDirac N W v) := by
  unfold weightedDirac
  rw [weighted_pairing_add_left, weighted_pairing_add_right,
    weighted_d_adjoint, weighted_codiff_adjoint N W hW]
  exact add_comm _ _

theorem identity_weight_binding (N : ℕ) (u : ArchiveCochain N) :
    weightedDirac N (LinearEquiv.refl ℝ (ArchiveCochain N)) u = hodgeCarDirac N u := rfl

/-- A nonconstant positive diagonal mass need not commute with d.
The omitted inverse is not a weighted adjoint. -/
theorem inverse_weight_derivative
    {i : Type} [Fintype i] [DecidableEq i]
    (W Wi dW dWi : Matrix i i ℝ)
    (hr : W*Wi=1)
    (hderiv : dWi*W+Wi*dW=0) : dWi = -Wi*dW*Wi := by
  have hh := congrArg (fun A : Matrix i i ℝ => A*Wi) hderiv
  simp only [Matrix.add_mul, Matrix.mul_assoc, hr, Matrix.mul_one, Matrix.zero_mul] at hh
  simpa [Matrix.neg_mul, Matrix.mul_assoc] using eq_neg_of_add_eq_zero_left hh

def rotationBlock (L : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![0, 2*L; -2*L, 0]

theorem spatial_block_square (L : ℝ) :
    rotationBlock L * rotationBlock L = (-4*L^2) • (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [rotationBlock, Matrix.mul_apply, Fin.sum_univ_succ] <;> ring

/-- Any positive definite real G has positive diagonal entries, so the two
displayed positivity hypotheses are weaker than positive definiteness. -/
theorem spatial_block_has_no_positive_metric (L : ℝ) (hL : L ≠ 0)
    (G : Matrix (Fin 2) (Fin 2) ℝ) (h0 : 0 < G 0 0) (h1 : 0 < G 1 1)
    (hadj : (rotationBlock L).transpose * G = G * rotationBlock L) : False := by
  have hh := congrArg (fun M : Matrix (Fin 2) (Fin 2) ℝ => M 0 1) hadj
  simp [rotationBlock, Matrix.mul_apply, Fin.sum_univ_succ] at hh
  have hz : (2*L)*(G 0 0+G 1 1)=0 := by nlinarith [hh]
  have hs : G 0 0+G 1 1=0 := (mul_eq_zero.mp hz).resolve_left (mul_ne_zero (by norm_num) hL)
  linarith

theorem exp_cubic_lower (x : ℝ) (hx : 0 ≤ x) : x^3/6 ≤ Real.exp x := by
  simpa using Real.pow_div_factorial_le_exp x hx 3

/-- Conditional on the independently computed spectrum/trace lower bound.
This does not define a heat trace by that bound. -/
theorem normalized_heat_lower (t L H : ℝ) (ht : 0 ≤ t) (hL : 0 < L)
    (hH : 16*Real.exp (12*t*L^2) ≤ H) :
    4608*t^3*L^2 ≤ H/L^4 := by
  have hexp := exp_cubic_lower (12*t*L^2) (by positivity)
  have hp : 0 < L^4 := by positivity
  apply (le_div_iff₀ hp).mpr
  nlinarith [hexp]

theorem scaled_codiff_square (N : ℕ)
    (W : ArchiveCochain N ≃ₗ[ℝ] ArchiveCochain N)
    (r : ℝ) (u : ArchiveCochain N) :
    (dForward N (dForward N u+r • weightedCodiff N W u) +
      r • weightedCodiff N W (dForward N u+r • weightedCodiff N W u)) =
      r • (dForward N (weightedCodiff N W u)+weightedCodiff N W (dForward N u)) := by
  rw [dForward_add, dForward_smul, kernel_d_sq,
    weighted_codiff_add, weighted_codiff_smul, weighted_codiff_sq]
  simp [smul_add]

theorem actual_spectral_trace_binding
    {i : Type} [Fintype i] [DecidableEq i]
    (M : Matrix i i ℝ) (k : ℕ) :
    D0.Geometry.SpectralActionLadder.spectralTracePower M (fun _ => 1) k =
      Matrix.trace (M^k) := by
  have h : D0.Geometry.SpectralActionLadder.conformalLaplacian M (fun _ => 1) = M := by
    ext a b
    unfold D0.Geometry.SpectralActionLadder.conformalLaplacian
    unfold weightedLaplacian
    rw [weighted_laplacian_entry M (fun _ => 1) (by intro a; norm_num)]
    simp
  simp only [D0.Geometry.SpectralActionLadder.spectralTracePower, h]

theorem scalar_matrix_power
    {i : Type} [Fintype i] [DecidableEq i]
    (M : Matrix i i ℝ) (r : ℝ) (k : ℕ) : (r • M)^k = r^k • M^k := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [pow_succ, ih, Matrix.smul_mul, Matrix.mul_smul, smul_smul, pow_succ]
    rw [mul_comm (r^k) r]
    rfl

theorem trace_power_homogeneity
    {i : Type} [Fintype i] [DecidableEq i]
    (M : Matrix i i ℝ) (r : ℝ) (k : ℕ) :
    Matrix.trace ((r • M)^k) = r^k*Matrix.trace (M^k) := by
  rw [scalar_matrix_power, Matrix.trace_smul]
  rfl

/-- A finite annihilator works for arbitrary coefficients, including
unbounded coefficients that depend on the mesh. -/
theorem finite_moment_annihilator
    {i j : Type} [Fintype i] [Fintype j]
    (w : i → ℝ) (c : j → ℝ) (v : j → i → ℝ)
    (hv : ∀ q, ∑ a, w a*v q a=0) :
    (∑ a, w a*(∑ q, c q*v q a))=0 := by
  simp_rw [Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_eq_zero
  intro q _
  calc
    (∑ a, w a*(c q*v q a)) = c q*(∑ a, w a*v q a) := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro a _
      ring
    _ = 0 := by rw [hv]; ring

theorem finite_annihilator_error_bound
    {i : Type} [Fintype i]
    (w x : i → ℝ) (E g : ℝ) (hx : ∀ a, |x a| ≤ E)
    (hg : ∑ a, w a*x a=g) : |g| ≤ E*(∑ a, |w a|) := by
  rw [← hg]
  calc
    |∑ a, w a*x a| ≤ ∑ a, |w a*x a| := Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ a, |w a| * E := by
      apply Finset.sum_le_sum
      intro a _
      rw [abs_mul]
      exact mul_le_mul_of_nonneg_left (hx a) (abs_nonneg _)
    _ = E*(∑ a, |w a|) := by rw [← Finset.sum_mul, mul_comm]

/-- On a nonzero null Fourier mode, an explicit CAR contraction gives
DK+KD=id. The independently computed contraction is not an Euler gate. -/
theorem null_mode_kernel_eq_range
    {V : Type} [AddCommGroup V] [Module ℝ V]
    (D K : V →ₗ[ℝ] V) (hD : ∀ v, D (D v) = 0)
    (hK : ∀ v, D (K v) + K (D v) = v) :
    LinearMap.ker D = LinearMap.range D := by
  ext v
  constructor
  · intro hv
    have hz : D v = 0 := (LinearMap.mem_ker).mp hv
    refine ⟨K v, ?_⟩
    simpa [hz] using hK v
  · rintro ⟨u, rfl⟩
    exact (LinearMap.mem_ker).mpr (hD u)

theorem null_mode_kernel_half_dimension
    {V : Type} [AddCommGroup V] [Module ℝ V] [FiniteDimensional ℝ V]
    (D K : V →ₗ[ℝ] V) (hD : ∀ v, D (D v) = 0)
    (hK : ∀ v, D (K v) + K (D v) = v) :
    2*Module.finrank ℝ (LinearMap.ker D) = Module.finrank ℝ V := by
  have h := LinearMap.finrank_range_add_finrank_ker D
  rw [← null_mode_kernel_eq_range D K hD hK] at h
  omega

#print archive_weighted_hodge_dirac_owner
#print archive_metric_measure_hodge_lift_owner
#check dForward_degree_raise
#check dForward_sq_zero
#check hodgeCodifferential_sq
#check hodgeCarDirac_kernel_finrank
#print axioms kernel_annihilate_int
#print axioms kernel_create_int
#print axioms kernel_annihilate_car
#print axioms kernel_create_car
#print axioms kernel_create_action_anticommute
#print axioms kernel_forward_direction_anticommute
#print axioms kernel_d_sq
#print axioms kernel_annihilate_action_anticommute
#print axioms kernel_backward_direction_anticommute
#print axioms kernel_codiff_sq
#print axioms null_mode_kernel_eq_range
#print axioms null_mode_kernel_half_dimension
#print axioms weighted_codiff_add
#print axioms weighted_codiff_smul
#print axioms weighted_codiff_sq
#print axioms weighted_dirac_square
#print axioms weighted_d_adjoint
#print axioms weighted_pairing_symm
#print axioms weighted_codiff_adjoint
#print axioms weighted_pairing_add_left
#print axioms weighted_pairing_add_right
#print axioms weighted_dirac_symmetric
#print axioms identity_weight_binding
#print axioms inverse_weight_derivative
#print axioms spatial_block_square
#print axioms spatial_block_has_no_positive_metric
#print axioms exp_cubic_lower
#print axioms normalized_heat_lower
#print axioms scaled_codiff_square
#print axioms actual_spectral_trace_binding
#print axioms scalar_matrix_power
#print axioms trace_power_homogeneity
#print axioms finite_moment_annihilator
#print axioms finite_annihilator_error_bound
end
end D0.Research.NativeWeightedDiracBoundary
