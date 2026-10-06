import D0.Geometry.A4DDiscreteEnergyKernel
import D0.Geometry.A4DConstitutiveKernelClassification
import D0.Geometry.A4DRawSolderFrameAction

/-! Research boundary for spectral functions of the literal flux symbol.
The existing kernelPoly and squaredFluxEnergy are evaluated, not replaced.
Scalar frame descent is a necessary covariance test, never a native EOM. -/
open scoped BigOperators
open D0 D0.Geometry
namespace D0.Research.NativeSpectralFrame
noncomputable section

private lemma sum_role (f : Role → ℝ) : (∑ r, f r) = f A + f B + f C + f D := by
  simp [Fintype.sum_prod_type, Fin.sum_univ_two, A, B, C, D]
  ring

lemma carEnd_vacuum (s r : Role) (S : ArchiveFockState) :
    carEnd s r S fockVacuumState = 0 := by
  simp [carEnd, carAnnihilate, fockVacuumState]

lemma carEnd_scalar (N : ℕ) (s r : Role) (f : ArchiveRolePhaseGroup N → ℝ) :
    cochainCarEnd N s r (scalarCochain N f) = 0 := by
  funext p
  simp [cochainCarEnd, scalarCochain, vacuumFockState, mul_ite, carEnd_vacuum]

lemma multiply_scalar (N : ℕ) (m f : ArchiveRolePhaseGroup N → ℝ) :
    cochainMultiply N m (scalarCochain N f) = scalarCochain N (fun x => m x * f x) := by
  funext p
  simp [cochainMultiply, scalarCochain, mul_ite]

lemma backwardShift_scalar (N : ℕ) (r : Role) (f : ArchiveRolePhaseGroup N → ℝ) :
    cochainBackwardShift N r (scalarCochain N f) =
      scalarCochain N (fun x => f (roleTranslateMinus N r x)) := rfl

lemma forwardAverage_scalar (N : ℕ) (r : Role) (f : ArchiveRolePhaseGroup N → ℝ) :
    cochainForwardAverage N r (scalarCochain N f) =
      scalarCochain N (fun x => (f x + f (roleTranslatePlus N r x)) / 2) := by
  funext p
  by_cases h : p.2 = vacuumFockState <;> simp [cochainForwardAverage, scalarCochain, h]

lemma fluxAdjoint_scalar (N : ℕ) (s r : Role) (m f : ArchiveRolePhaseGroup N → ℝ) :
    cochainFluxAdjoint N m s r (scalarCochain N f) = 0 := by
  unfold cochainFluxAdjoint
  rw [multiply_scalar, backwardShift_scalar, forwardAverage_scalar, carEnd_scalar]

lemma fluxForward_scalar (N : ℕ) (s r : Role) (m f : ArchiveRolePhaseGroup N → ℝ) :
    cochainFluxForward N m s r (scalarCochain N f) = 0 := by
  funext p
  simp [cochainFluxForward, carEnd_scalar, cochainMultiply, cochainForwardShift,
    cochainBackwardAverage, backwardAverage]

/-- Literal constant scalar eigenvector, for all finite stages and coframes. -/
theorem actual_flux_scalar_eigen (N : ℕ) (e : Matrix Role Role ℝ) :
    (fluxHMatrix N (fun _ => e)).mulVec (scalarCochain N (fun _ => 1)) =
      (Matrix.trace e) • scalarCochain N (fun _ => 1) := by
  rw [fluxHMatrix_apply]
  funext p
  simp only [flatStaggeredH, fluxForward_scalar, fluxAdjoint_scalar,
    Pi.zero_apply, add_zero, Finset.sum_const_zero, sub_zero]
  by_cases h : p.2 = vacuumFockState
  · simp [cochainLinkSymmetric, scalarCochain, h, Matrix.trace]
  · simp [cochainLinkSymmetric, scalarCochain, h]

theorem kernel_eigen {n : Type*} [Fintype n] [DecidableEq n]
    (α s : ℝ) (H : Matrix n n ℝ) (v : n → ℝ)
    (hv : H.mulVec v = s • v) :
    (kernelPoly α H).mulVec v = (1+s+α*s^2) • v := by
  have hsq : (H*H).mulVec v = (s*s) • v := by
    rw [← Matrix.mulVec_mulVec, hv, Matrix.mulVec_smul, hv, smul_smul]
  simp only [kernelPoly, Matrix.add_mulVec, Matrix.one_mulVec,
    Matrix.smul_mulVec, hv, hsq]
  funext i
  simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
  ring

theorem owned_energy_eigen {n : Type*} [Fintype n] [DecidableEq n]
    (α s : ℝ) (H : Matrix n n ℝ) (v : n → ℝ)
    (hv : H.mulVec v = s • v) :
    squaredFluxEnergy α H v = (1/2 : ℝ)*(1+s+α*s^2)*(∑ i, (v i)^2) := by
  unfold squaredFluxEnergy
  rw [kernel_eigen α s H v hv]
  simp only [Pi.smul_apply, smul_eq_mul]
  have hs : (∑ i, v i * ((1+s+α*s^2)*v i)) =
      (1+s+α*s^2)*(∑ i, (v i)^2) := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i _
    ring
  rw [hs]
  ring

theorem actual_flux_symmetric (N : ℕ) (e : LocalCoframeField N) :
    (fluxHMatrix N e).transpose = fluxHMatrix N e := by
  ext p q
  rcases p with ⟨xp, sp⟩
  rcases q with ⟨xq, sq⟩
  have hadj := flatStaggeredH_selfAdjoint N e
    (Pi.single (xq, sq) (1 : ℝ)) (Pi.single (xp, sp) (1 : ℝ))
  rw [← fluxHMatrix_apply, ← fluxHMatrix_apply] at hadj
  simp only [cochainPairing, Matrix.mulVec_single_one, Pi.single_apply,
    Prod.mk.injEq, ite_and] at hadj
  simpa [Matrix.transpose_apply] using hadj.symm

/-- Finite square form, valid also for nonconstant coframes after actual binding. -/
theorem owned_energy_square_form {n : Type*} [Fintype n] [DecidableEq n]
    (α : ℝ) (H : Matrix n n ℝ) (hH : H.transpose = H) (v : n → ℝ) :
    squaredFluxEnergy α H v = (1/2 : ℝ)*
      ((∑ i, (v i)^2)+(∑ i, v i*H.mulVec v i)+α*(∑ i, (H.mulVec v i)^2)) := by
  have hh := symm_square_norm H hH v
  unfold squaredFluxEnergy kernelPoly
  simp only [Matrix.add_mulVec, Matrix.one_mulVec, Matrix.smul_mulVec,
    Pi.add_apply, Pi.smul_apply, smul_eq_mul, mul_add, Finset.sum_add_distrib]
  simp_rw [show ∀ i, v i*(α*(H*H).mulVec v i)=α*(v i*(H*H).mulVec v i) by
    intro i; ring, ← Finset.mul_sum, hh]
  simp [pow_two]

/-- Positive quadratic coefficients preserve the two-sided linear obstruction. -/
theorem paired_positive_coefficients_defect (α δ bm bp : ℝ)
    (hm : 0 ≤ bm) (hp : 0 ≤ bp) :
    δ ≤ max |-δ+α*bm| |δ+α*bp| := by
  by_cases ha : 0 ≤ α
  · have hmul := mul_nonneg ha hp
    have hb := le_abs_self (δ+α*bp)
    exact le_trans (by linarith) (le_max_right _ _)
  · have hmul := mul_nonpos_of_nonpos_of_nonneg (le_of_not_ge ha) hm
    have hb := neg_le_abs (-δ+α*bm)
    exact le_trans (by linarith) (le_max_left _ _)

def boost (a b : ℝ) : Matrix Role Role ℝ := fun r s =>
  if r = A then (if s = A then a else if s = B then b else 0)
  else if r = B then (if s = A then b else if s = B then a else 0)
  else if r = s then 1 else 0

def thetaMinus : Matrix Role Role ℝ := Matrix.diagonal (fun r =>
  if r = A then 1 else if r = B then -2 else -(1/2 : ℝ))

def thetaPlus : Matrix Role Role ℝ := Matrix.diagonal (fun r =>
  if r = A then 2 else if r = B then -1 else -(3/2 : ℝ))

def scalarReadout (Θ : Matrix Role Role ℝ) : ℝ := Matrix.trace (Θ-roleLorentzMetric)

theorem boost_lorentz (a b : ℝ) (h : a^2-b^2=1) : IsRoleLorentz (boost a b) := by
  unfold IsRoleLorentz
  ext ⟨r1,r2⟩ ⟨s1,s2⟩
  fin_cases r1 <;> fin_cases r2 <;> fin_cases s1 <;> fin_cases s2 <;>
    norm_num [boost, roleLorentzMetric, Matrix.mul_apply, Matrix.transpose_apply,
      Matrix.diagonal_apply, sum_role, A, B, C, D, roleLorentzSign, roleRoleSigEquiv, roleSign] <;>
    nlinarith [h]

theorem boost_exists (a : ℝ) (ha : 1 ≤ a) :
    ∃ b, a^2-b^2=1 ∧ IsRoleLorentz (boost a b) := by
  have hn : 0 ≤ a^2-1 := by nlinarith
  have hb : a^2-(Real.sqrt (a^2-1))^2=1 := by
    rw [Real.sq_sqrt hn]
    ring
  exact ⟨Real.sqrt (a^2-1), hb, boost_lorentz a _ hb⟩

theorem thetaMinus_det : Matrix.det thetaMinus = -(1/2 : ℝ) := by
  rw [thetaMinus, Matrix.det_diagonal]
  norm_num [Fintype.prod_prod_type, Fin.prod_univ_two, A, B, C, D]

theorem thetaPlus_det : Matrix.det thetaPlus = -(9/2 : ℝ) := by
  rw [thetaPlus, Matrix.det_diagonal]
  norm_num [Fintype.prod_prod_type, Fin.prod_univ_two, A, B, C, D]

theorem negative_ray (a b : ℝ) :
    scalarReadout (thetaMinus * boost a b) = 1-a := by
  norm_num [scalarReadout, Matrix.trace, thetaMinus, boost, Matrix.mul_apply,
    Matrix.sub_apply, roleLorentzMetric, Matrix.diagonal_apply, sum_role,
    A, B, C, D, roleLorentzSign, roleRoleSigEquiv, roleSign]
  ring

theorem positive_ray (a b : ℝ) :
    scalarReadout (thetaPlus * boost a b) = a-1 := by
  norm_num [scalarReadout, Matrix.trace, thetaPlus, boost, Matrix.mul_apply,
    Matrix.sub_apply, roleLorentzMetric, Matrix.diagonal_apply, sum_role,
    A, B, C, D, roleLorentzSign, roleRoleSigEquiv, roleSign]
  ring

private theorem ray_base : scalarReadout thetaMinus = 0 ∧ scalarReadout thetaPlus = 0 := by
  constructor <;> norm_num [scalarReadout, Matrix.trace, thetaMinus, thetaPlus,
    Matrix.sub_apply, roleLorentzMetric, Matrix.diagonal_apply, sum_role,
    A, B, C, D, roleLorentzSign, roleRoleSigEquiv, roleSign]

/-- Necessary covariance under the explicit connected AB boost family,
not an on-shell definition. -/
def ScalarFrameDescent (f : ℝ → ℝ) : Prop :=
  ∀ (Θ : Matrix Role Role ℝ) (a b : ℝ),
    Matrix.det Θ ≠ 0 → 1 ≤ a → a^2-b^2=1 →
      f (scalarReadout (Θ*boost a b)) = f (scalarReadout Θ)

/-- No regularity, degree bound, or analytic-continuation hypothesis is needed. -/
theorem scalar_descent_forces_constant (f : ℝ → ℝ) (h : ScalarFrameDescent f) :
    ∀ s : ℝ, f s = f 0 := by
  intro s
  by_cases hs : s ≤ 0
  · obtain ⟨b,hb⟩ := boost_exists (1-s) (by linarith)
    have hh := h thetaMinus (1-s) b (by rw [thetaMinus_det]; norm_num) (by linarith) hb.1
    rw [negative_ray, ray_base.1] at hh
    convert hh using 1; congr 1; ring
  · obtain ⟨b,hb⟩ := boost_exists (1+s) (by linarith)
    have hh := h thetaPlus (1+s) b (by rw [thetaPlus_det]; norm_num) (by linarith) hb.1
    rw [positive_ray, ray_base.2] at hh
    convert hh using 1; congr 1; ring

/-- One fixed rational proper boost gives a uniform obstruction for every α. -/
theorem quadratic_uniform_defect (α : ℝ) :
    (1/4 : ℝ) ≤ max
      |(1+scalarReadout (thetaMinus*boost (5/4) (3/4))+
          α*(scalarReadout (thetaMinus*boost (5/4) (3/4)))^2)-1|
      |(1+scalarReadout (thetaPlus*boost (5/4) (3/4))+
          α*(scalarReadout (thetaPlus*boost (5/4) (3/4)))^2)-1| := by
  rw [negative_ray, positive_ray]
  have hm : (1+(1-(5/4 : ℝ))+α*(1-5/4)^2)-1 = -(1/4 : ℝ)+α/16 := by ring
  have hp : (1+((5/4 : ℝ)-1)+α*(5/4-1)^2)-1 = (1/4 : ℝ)+α/16 := by ring
  rw [hm, hp]
  have hL := (abs_le.mp (le_max_left |-(1/4 : ℝ)+α/16| |(1/4 : ℝ)+α/16|)).1
  have hR := (abs_le.mp (le_max_right |-(1/4 : ℝ)+α/16| |(1/4 : ℝ)+α/16|)).2
  linarith

#print axioms actual_flux_scalar_eigen
#print axioms kernel_eigen
#print axioms owned_energy_eigen
#print axioms actual_flux_symmetric
#print axioms owned_energy_square_form
#print axioms paired_positive_coefficients_defect
#print axioms boost_lorentz
#print axioms boost_exists
#print axioms thetaMinus_det
#print axioms thetaPlus_det
#print axioms negative_ray
#print axioms positive_ray
#print axioms scalar_descent_forces_constant
#print axioms quadratic_uniform_defect
end
end D0.Research.NativeSpectralFrame
