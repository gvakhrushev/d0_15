import D0.Geometry.A4DConstitutiveKernelClassification
import Mathlib.Analysis.Calculus.LocalExtr.Basic
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Mul

/-! Research: actual derivatives of the complete nonnegative homogeneous
field-action class. No action, positivity hypothesis or field constraint is
installed in the native theory. -/
namespace D0.Research.NativePositiveSource
open D0 D0.Geometry Filter
open scoped BigOperators Topology
noncomputable section
set_option linter.unusedSectionVars false
variable {V : Type*} [AddCommGroup V] [Module ℝ V]

/-- Full stationarity tests independently chosen affine field directions. -/
def FullFieldGate (E : V → ℝ) (z : V) : Prop :=
  ∀ v, HasDerivAt (fun t : ℝ => E (z+t • v)) 0 0

theorem homogeneous_radial_derivative (E : V → ℝ) (z : V) (p : ℕ)
    (hhom : ∀ t : ℝ, E (t • z)=t^p*E z) :
    HasDerivAt (fun t : ℝ => E (z+t • z)) ((p:ℝ)*E z) 0 := by
  have heq : (fun t : ℝ => E (z+t • z))=(fun t : ℝ => (1+t)^p*E z) := by
    funext t
    rw [show z+t • z=(1+t) • z by simp [add_smul],hhom]
  rw [heq]
  simpa using (((hasDerivAt_const (0:ℝ) (1:ℝ)).add (hasDerivAt_id 0)).pow p).mul_const (E z)

theorem homogeneous_full_root_value_zero (E : V → ℝ) (z : V) (p : ℕ)
    (hp : p≠0) (hhom : ∀ t : ℝ, E (t • z)=t^p*E z)
    (hgate : FullFieldGate E z) : E z=0 := by
  have h := (homogeneous_radial_derivative E z p hhom).unique (hgate z)
  exact (mul_eq_zero.mp h).resolve_left (by exact_mod_cast hp)

/-- Nonnegativity is needed along the actual two-sided background curve. -/
theorem zero_value_nonnegative_source (f : ℝ → ℝ) (sigma : ℝ)
    (h0 : f 0=0) (hnonneg : ∀ᶠ t in 𝓝 (0:ℝ), 0≤f t)
    (hderiv : HasDerivAt f sigma 0) : sigma=0 := by
  have hmin : IsLocalMin f 0 := by
    change ∀ᶠ t in 𝓝 (0:ℝ), f 0≤f t
    simpa only [h0] using hnonneg
  exact hmin.hasDerivAt_eq_zero hderiv

theorem homogeneous_nonnegative_full_root_source (E : ℝ → V → ℝ)
    (z : V) (p : ℕ) (hp : p≠0) (sigma : ℝ)
    (hhom : ∀ t : ℝ, E 0 (t • z)=t^p*E 0 z)
    (hgate : FullFieldGate (E 0) z)
    (hnonneg : ∀ᶠ t in 𝓝 (0:ℝ), 0≤E t z)
    (hderiv : HasDerivAt (fun t => E t z) sigma 0) : sigma=0 :=
  zero_value_nonnegative_source _ _
    (homogeneous_full_root_value_zero _ z p hp hhom hgate) hnonneg hderiv

variable {n : Type*} [Fintype n] [DecidableEq n]
abbrev Mat (n : Type*) := Matrix n n ℝ
def quad (M : Mat n) (z : n → ℝ) : ℝ := (1/2:ℝ)*∑ i, z i*(M.mulVec z) i

theorem literal_squared_flux_binding (alpha : ℝ) (H : Mat n) (z : n → ℝ) :
    squaredFluxEnergy alpha H z=quad (kernelPoly alpha H) z := rfl

theorem quad_smul (M : Mat n) (z : n → ℝ) (t : ℝ) :
    quad M (t • z)=t^2*quad M z := by
  simp only [quad,Matrix.mulVec_smul,Pi.smul_apply,smul_eq_mul]
  have hs : (∑ i, t*z i*(t*M.mulVec z i))=t^2*(∑ i, z i*M.mulVec z i) := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i _
    ring
  rw [hs]
  ring

theorem quad_field_exact_variation (M : Mat n) (hM : M.transpose=M)
    (z v : n → ℝ) (t : ℝ) :
    quad M (z+t • v)=quad M z+t*(∑ i, v i*M.mulVec z i)+t^2*quad M v := by
  have hs := symm_dot_mulVec M hM z v
  have heq : (∑ i, z i*M.mulVec v i)=(∑ i, v i*M.mulVec z i) := by
    simpa only [mul_comm] using hs
  simp only [quad,Matrix.mulVec_add,Matrix.mulVec_smul,Pi.add_apply,Pi.smul_apply,smul_eq_mul]
  have ht : ∀ i, (z i+t*v i)*(M.mulVec z i+t*M.mulVec v i)=
      z i*M.mulVec z i+t*(z i*M.mulVec v i)+t*(v i*M.mulVec z i)+t^2*(v i*M.mulVec v i) := by
    intro i; ring
  simp_rw [ht]
  simp only [Finset.sum_add_distrib,←Finset.mul_sum]
  rw [heq]
  ring

theorem quad_field_hasDerivAt (M : Mat n) (hM : M.transpose=M) (z v : n → ℝ) :
    HasDerivAt (fun t : ℝ => quad M (z+t • v)) (∑ i, v i*M.mulVec z i) 0 := by
  have h := ((hasDerivAt_const (0:ℝ) (quad M z)).add
    ((hasDerivAt_id 0).mul_const (∑ i, v i*M.mulVec z i))).add
      (((hasDerivAt_id 0).pow 2).mul_const (quad M v))
  simpa [quad_field_exact_variation M hM z v] using h

theorem quad_full_field_gate_iff_kernel (M : Mat n) (hM : M.transpose=M) (z : n → ℝ) :
    FullFieldGate (quad M) z ↔ M.mulVec z=0 := by
  constructor
  · intro h
    funext i
    have hi := (quad_field_hasDerivAt M hM z (Pi.single i 1)).unique (h (Pi.single i 1))
    simpa [Pi.single_apply] using hi
  · intro h v
    simpa [h] using quad_field_hasDerivAt M hM z v

theorem arbitrary_positive_quadratic_source_zero (M : ℝ → Mat n) (z : n → ℝ)
    (hM : (M 0).transpose=M 0) (hroot : (M 0).mulVec z=0) (sigma : ℝ)
    (hpos : ∀ᶠ t in 𝓝 (0:ℝ), ∀ v, 0≤quad (M t) v)
    (hderiv : HasDerivAt (fun t => quad (M t) z) sigma 0) : sigma=0 := by
  exact homogeneous_nonnegative_full_root_source (fun t v => quad (M t) v)
    z 2 (by decide) sigma (quad_smul (M 0) z)
    ((quad_full_field_gate_iff_kernel _ hM z).mpr hroot)
    (hpos.mono (fun _ ht => ht z)) hderiv

theorem owned_square_form (alpha : ℝ) (H : Mat n) (hH : H.transpose=H) (z : n → ℝ) :
    squaredFluxEnergy alpha H z=(1/2:ℝ)*
      ((∑ i, (z i)^2)+(∑ i,z i*H.mulVec z i)+alpha*(∑ i,(H.mulVec z i)^2)) := by
  have hh := symm_square_norm H hH z
  unfold squaredFluxEnergy kernelPoly
  simp only [Matrix.add_mulVec,Matrix.one_mulVec,Matrix.smul_mulVec,
    Pi.add_apply,Pi.smul_apply,smul_eq_mul,mul_add,Finset.sum_add_distrib]
  simp_rw [show ∀ i, z i*(alpha*(H*H).mulVec z i)=alpha*(z i*(H*H).mulVec z i) by
    intro i; ring,←Finset.mul_sum,hh]
  simp [pow_two]

theorem owned_completed_square (alpha : ℝ) (H : Mat n) (hH : H.transpose=H) (z : n → ℝ) :
    squaredFluxEnergy alpha H z=(1/2:ℝ)*
      ((∑ i,(z i+(H.mulVec z i)/2)^2)+(alpha-1/4)*(∑ i,(H.mulVec z i)^2)) := by
  rw [owned_square_form alpha H hH z]
  have hs : (∑ i,(z i+(H.mulVec z i)/2)^2)=
      (∑ i,(z i)^2)+(∑ i,z i*H.mulVec z i)+(1/4:ℝ)*(∑ i,(H.mulVec z i)^2) := by
    simp only [←Finset.sum_add_distrib,Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i _; ring
  rw [hs]
  ring

theorem owned_nonnegative_at_and_above_quarter (alpha : ℝ) (ha : 1/4≤alpha)
    (H : Mat n) (hH : H.transpose=H) (z : n → ℝ) : 0≤squaredFluxEnergy alpha H z := by
  rw [owned_completed_square alpha H hH z]
  have : 0≤alpha-1/4 := sub_nonneg.mpr ha
  positivity

theorem owned_source_zero (alpha : ℝ → ℝ) (H : ℝ → Mat n) (z : n → ℝ) (sigma : ℝ)
    (hgate : FullFieldGate (squaredFluxEnergy (alpha 0) (H 0)) z)
    (hpos : ∀ᶠ t in 𝓝 (0:ℝ), 1/4≤alpha t ∧ (H t).transpose=H t)
    (hderiv : HasDerivAt (fun t => squaredFluxEnergy (alpha t) (H t) z) sigma 0) : sigma=0 := by
  apply homogeneous_nonnegative_full_root_source (fun t v => squaredFluxEnergy (alpha t) (H t) v)
    z 2 (by decide) sigma _ hgate _ hderiv
  · exact quad_smul (kernelPoly (alpha 0) (H 0)) z
  · exact hpos.mono (fun t ht => owned_nonnegative_at_and_above_quarter _ ht.1 _ ht.2 z)

/-- P is the support projection and G is its inverse on that support. -/
def firstJetLift (G B P : Mat n) : Mat n := G*B-(1/2:ℝ) • (G*B*P)

theorem first_jet_reconstruction (A G P B : Mat n)
    (hAG : A*G=P) (hGA : G*A=P) (hG : G.transpose=G)
    (hP : P.transpose=P) (hB : B.transpose=B)
    (hker : (1-P)*B*(1-P)=0) :
    A*firstJetLift G B P+(firstJetLift G B P).transpose*A=B := by
  have hdecomp : P*B+B*P-P*B*P=B := by
    have hid : (1-P)*B*(1-P)=B-(P*B+B*P-P*B*P) := by noncomm_ring
    rw [hid] at hker
    exact (sub_eq_zero.mp hker).symm
  have hl : A*(G*B)=P*B := by rw [←Matrix.mul_assoc,hAG]
  have hlp : A*(G*B*P)=P*B*P := by rw [←Matrix.mul_assoc,hl]
  have hr : (B*G)*A=B*P := by rw [Matrix.mul_assoc,hGA]
  have hrp : (P*(B*G))*A=P*B*P := by rw [Matrix.mul_assoc,hr,←Matrix.mul_assoc]
  simp only [firstJetLift,Matrix.mul_sub,Matrix.mul_smul,Matrix.transpose_sub,
    Matrix.transpose_smul,Matrix.transpose_mul,hG,hP,hB,Matrix.sub_mul,Matrix.smul_mul,
    hl,hlp,hr,hrp]
  ext i j
  have hh := congrArg (fun M : Mat n => M i j) hdecomp
  simp only [Matrix.add_apply,Matrix.sub_apply,Matrix.smul_apply,smul_eq_mul] at hh ⊢
  linarith

/-- The two Taylor bounds require independently proved uniform constants. -/
theorem two_sided_positive_source_bound (E sigma M s : ℝ) (hs : 0<s)
    (hp : 0≤E+s*sigma+M*s^2/2) (hm : 0≤E-s*sigma+M*s^2/2) :
    |sigma|≤E/s+M*s/2 := by
  apply abs_le.mpr
  constructor
  · have heq : -(E/s+M*s/2)=(-E-M*s^2/2)/s := by
      field_simp [hs.ne']
      ring
    rw [heq]
    apply (div_le_iff₀ hs).mpr
    nlinarith
  · have heq : E/s+M*s/2=(E+M*s^2/2)/s := by
      field_simp [hs.ne']
    rw [heq]
    apply (le_div_iff₀ hs).mpr
    nlinarith

theorem one_point_positive_control_field :
    HasDerivAt (fun z : ℝ => (0:ℝ)*z^2) 0 1 := by
  simpa using hasDerivAt_const (1:ℝ) (0:ℝ)

theorem one_point_positive_control_source :
    HasDerivAt (fun t : ℝ => t*(1:ℝ)^2) 1 0 := by
  simpa using hasDerivAt_id (0:ℝ)

end
end D0.Research.NativePositiveSource

#print axioms D0.Research.NativePositiveSource.homogeneous_radial_derivative
#print axioms D0.Research.NativePositiveSource.homogeneous_full_root_value_zero
#print axioms D0.Research.NativePositiveSource.zero_value_nonnegative_source
#print axioms D0.Research.NativePositiveSource.homogeneous_nonnegative_full_root_source
#print axioms D0.Research.NativePositiveSource.literal_squared_flux_binding
#print axioms D0.Research.NativePositiveSource.quad_smul
#print axioms D0.Research.NativePositiveSource.quad_field_exact_variation
#print axioms D0.Research.NativePositiveSource.quad_field_hasDerivAt
#print axioms D0.Research.NativePositiveSource.quad_full_field_gate_iff_kernel
#print axioms D0.Research.NativePositiveSource.arbitrary_positive_quadratic_source_zero
#print axioms D0.Research.NativePositiveSource.owned_square_form
#print axioms D0.Research.NativePositiveSource.owned_completed_square
#print axioms D0.Research.NativePositiveSource.owned_nonnegative_at_and_above_quarter
#print axioms D0.Research.NativePositiveSource.owned_source_zero
#print axioms D0.Research.NativePositiveSource.first_jet_reconstruction
#print axioms D0.Research.NativePositiveSource.two_sided_positive_source_bound
#print axioms D0.Research.NativePositiveSource.one_point_positive_control_field
#print axioms D0.Research.NativePositiveSource.one_point_positive_control_source

#check D0.Research.NativePositiveSource.homogeneous_nonnegative_full_root_source

#check D0.Research.NativePositiveSource.quad_full_field_gate_iff_kernel

#check D0.Research.NativePositiveSource.arbitrary_positive_quadratic_source_zero

#check D0.Research.NativePositiveSource.owned_source_zero

#check D0.Research.NativePositiveSource.first_jet_reconstruction

#check D0.Research.NativePositiveSource.two_sided_positive_source_bound
