import D0.Geometry.ArchiveAffineExteriorLink
import D0.Geometry.A4DRawSolderFrameAction

/-! Research capsule: actual native link readout, transported center, and a
generic complete periodic affine-recurrence fiber theorem. The analytical
cycle determinant, quantitative bounds and smooth preparation are separate
in A4D_NATIVE_TRANSPORTED_CONNECTION_REALIZATION.md. -/
open D0 D0.Geometry
open Matrix

namespace D0.Research.NativeTransportedConnection
noncomputable section

def nativeLink (U : Matrix Role Role ℝ) (hU : IsRoleLorentz U)
    (b : RoleSpace) : AffineCartanMap ℝ RoleSpace :=
  ⟨(lorentzVectorEquiv U hU).symm, b⟩

theorem native_link_apply (U : Matrix Role Role ℝ) (hU : IsRoleLorentz U)
    (b v : RoleSpace) : (nativeLink U hU b).lin v = U *ᵥ v := by
  rfl

theorem native_link_matrix (U : Matrix Role Role ℝ) (hU : IsRoleLorentz U)
    (b : RoleSpace) :
    LinearMap.toMatrix archiveRoleBasis archiveRoleBasis
      (nativeLink U hU b).lin.toLinearMap = U := by
  change LinearMap.toMatrix' (Matrix.toLin' U) = U
  exact LinearMap.toMatrix'_toLin' U

theorem native_link_inverse_apply (U : Matrix Role Role ℝ) (hU : IsRoleLorentz U)
    (b v : RoleSpace) : (nativeLink U hU b).lin.symm v = U⁻¹ *ᵥ v := by
  exact lorentzVectorEquiv_apply U hU v

theorem native_lorentz_connection (N : ℕ)
    (U : ArchiveRolePhaseGroup N → Role → Matrix Role Role ℝ)
    (hU : ∀ x r, IsRoleLorentz (U x r))
    (b : ArchiveRolePhaseGroup N → Role → RoleSpace) :
    IsLorentzAffineExteriorConnection
      (fun x r => nativeLink (U x r) (hU x r) (b x r)) := by
  intro x r
  rw [native_link_matrix]
  exact hU x r

theorem native_shift_fiber (U : Matrix Role Role ℝ) (hU : IsRoleLorentz U)
    (b c : RoleSpace) : nativeLink U hU b = nativeLink U hU c ↔ b=c := by
  constructor
  · intro h
    exact congrArg AffineCartanMap.shift h
  · intro h; rw [h]

theorem actual_open_holonomy_matrix (N : ℕ)
    (U : LinkConnection N ℝ RoleSpace) (r s : Role)
    (x : ArchiveRolePhaseGroup N) :
    LinearMap.toMatrix archiveRoleBasis archiveRoleBasis (openCurvature U r s x) =
      (LinearMap.toMatrix archiveRoleBasis archiveRoleBasis
        (basedHolonomy U r s x).toLinearMap - 1) *
      LinearMap.toMatrix archiveRoleBasis archiveRoleBasis
        (squarePathB U r s x).toLinearMap := by
  rw [curvature_eq_holonomy_defect,
    LinearMap.toMatrix_comp archiveRoleBasis archiveRoleBasis archiveRoleBasis]
  simp

theorem actual_native_holonomy_apply (N : ℕ)
    (U : ArchiveRolePhaseGroup N → Role → Matrix Role Role ℝ)
    (hU : ∀ x r, IsRoleLorentz (U x r))
    (b : ArchiveRolePhaseGroup N → Role → RoleSpace)
    (r s : Role) (x : ArchiveRolePhaseGroup N) (v : RoleSpace) :
    basedHolonomy (fun y t => (nativeLink (U y t) (hU y t) (b y t)).lin) r s x v =
      (U x r * U (roleTranslatePlus N r x) s *
        (U (roleTranslatePlus N s x) r)⁻¹ * (U x s)⁻¹) *ᵥ v := by
  simp only [basedHolonomy, squarePathA, squarePathB, LinearEquiv.trans_apply,
    LinearEquiv.symm_trans_apply, native_link_apply, native_link_inverse_apply,
    Matrix.mulVec_mulVec, Matrix.mul_assoc]

theorem actual_native_torsion (N : ℕ)
    (U : ArchiveRolePhaseGroup N → Role → Matrix Role Role ℝ)
    (hU : ∀ x r, IsRoleLorentz (U x r))
    (b : ArchiveRolePhaseGroup N → Role → RoleSpace)
    (r s : Role) (x : ArchiveRolePhaseGroup N) :
    affineOpenTorsion (fun y t => nativeLink (U y t) (hU y t) (b y t)) r s x =
      b x r + U x r *ᵥ b (roleTranslatePlus N r x) s -
        (b x s + U x s *ᵥ b (roleTranslatePlus N s x) r) := by
  rw [affineOpenTorsion_expand]
  rfl

theorem actual_transport_center_flat (N : ℕ) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) :
    transportedSolderCenter N (rawSolderMatrix N e) (fun _ _ => 1) x =
      solderMatrix N e x := by
  ext r a
  simp [transportedSolderCenter, solderMatrix, rawSolderMatrix,
    centeredCoframeMatrix, backwardAverage]
  ring

theorem actual_transport_center_row_equation (N : ℕ)
    (E : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (R : ArchiveRolePhaseGroup N → Role → Matrix Role Role ℝ)
    (T : Matrix Role Role ℝ) (x : ArchiveRolePhaseGroup N) :
    transportedSolderCenter N E R x = T ↔
      ∀ r a, E x r a = 2*T r a -
        (E (roleTranslateMinus N r x)*R (roleTranslateMinus N r x) r) r a := by
  constructor
  · intro h r a
    have hx := congrFun (congrFun h r) a
    simp only [transportedSolderCenter] at hx
    linarith
  · intro h
    ext r a
    simp only [transportedSolderCenter]
    have hx := h r a
    linarith

def mixedCenter (N : ℕ)
    (F : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (K : ArchiveRolePhaseGroup N → Role → Matrix Role Role ℝ)
    (x : ArchiveRolePhaseGroup N) : Matrix Role Role ℝ :=
  fun r a => (F (roleTranslateMinus N r x)*K (roleTranslateMinus N r x) r) r a / 2

theorem actual_joint_center_polynomial (N : ℕ)
    (F H : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (R K : ArchiveRolePhaseGroup N → Role → Matrix Role Role ℝ)
    (t : ℝ) (x : ArchiveRolePhaseGroup N) :
    transportedSolderCenter N (F+t • H) (R+t • K) x =
      transportedSolderCenter N F R x +
      t • (transportedSolderCenter N H R x + mixedCenter N F K x) +
      t^2 • mixedCenter N H K x := by
  ext r a
  simp [transportedSolderCenter, mixedCenter, Matrix.add_mul, Matrix.mul_add]
  ring

section Recurrence
variable {V : Type*} [AddCommGroup V] [Module ℝ V]

def sweep (T : ℕ → V →ₗ[ℝ] V) (b : ℕ → V) (u : V) : ℕ → V
  | 0 => u
  | n+1 => b n - T n (sweep T b u n)

def orderedProduct (T : ℕ → V →ₗ[ℝ] V) : ℕ → V →ₗ[ℝ] V
  | 0 => LinearMap.id
  | n+1 => (T n).comp (orderedProduct T n)

def cycleDefect (T : ℕ → V →ₗ[ℝ] V) (n : ℕ) : V →ₗ[ℝ] V :=
  LinearMap.id - ((-1:ℝ)^n) • orderedProduct T n

theorem sweep_affine (T : ℕ → V →ₗ[ℝ] V) (b : ℕ → V) (u : V) (n : ℕ) :
    sweep T b u n = sweep T b 0 n + ((-1:ℝ)^n) • orderedProduct T n u := by
  induction n with
  | zero => simp [sweep, orderedProduct]
  | succ n ih =>
    rw [sweep, ih, map_add, map_smul]
    simp only [sweep, orderedProduct, LinearMap.comp_apply, pow_succ,
      mul_neg_one, neg_smul]
    abel

theorem periodic_gate_iff (T : ℕ → V →ₗ[ℝ] V) (b : ℕ → V) (u : V) (n : ℕ) :
    sweep T b u n = u ↔ cycleDefect T n u = sweep T b 0 n := by
  rw [sweep_affine]
  simp only [cycleDefect, LinearMap.sub_apply, LinearMap.id_apply,
    LinearMap.smul_apply]
  constructor
  · intro h; exact sub_eq_iff_eq_add.mpr h.symm
  · intro h; exact (sub_eq_iff_eq_add.mp h).symm

theorem periodic_existence_iff_range (T : ℕ → V →ₗ[ℝ] V) (b : ℕ → V) (n : ℕ) :
    (∃ u, sweep T b u n=u) ↔ sweep T b 0 n ∈ LinearMap.range (cycleDefect T n) := by
  simp only [periodic_gate_iff, LinearMap.mem_range]

theorem periodic_fiber_iff_kernel (T : ℕ → V →ₗ[ℝ] V) (b : ℕ → V)
    (u v : V) (n : ℕ) (hv : sweep T b v n=v) :
    sweep T b u n=u ↔ u-v ∈ LinearMap.ker (cycleDefect T n) := by
  have hv' := (periodic_gate_iff T b v n).mp hv
  rw [periodic_gate_iff]
  simp only [LinearMap.mem_ker, map_sub, sub_eq_zero, hv']

theorem periodic_unique_if_injective (T : ℕ → V →ₗ[ℝ] V) (b : ℕ → V)
    (u v : V) (n : ℕ) (h : Function.Injective (cycleDefect T n))
    (hu : sweep T b u n=u) (hv : sweep T b v n=v) : u=v := by
  apply h
  rw [(periodic_gate_iff T b u n).mp hu, (periodic_gate_iff T b v n).mp hv]

end Recurrence

theorem cayley_congruence (D : Matrix Role Role ℝ)
    (hD : D*roleLorentzMetric + roleLorentzMetric*D.transpose=0) :
    (1+D)*roleLorentzMetric*(1+D).transpose =
      (1-D)*roleLorentzMetric*(1-D).transpose := by
  simp only [Matrix.transpose_add, Matrix.transpose_sub, Matrix.transpose_one,
    Matrix.add_mul, Matrix.mul_add, Matrix.sub_mul, Matrix.mul_sub,
    Matrix.one_mul, Matrix.mul_one]
  ext r a
  have hh := congrFun (congrFun hD r) a
  simp only [Matrix.add_apply, Matrix.zero_apply] at hh
  simp only [Matrix.add_apply, Matrix.sub_apply]
  linarith

theorem cayley_is_lorentz (D : Matrix Role Role ℝ)
    (hD : D*roleLorentzMetric + roleLorentzMetric*D.transpose=0)
    (hdet : IsUnit (1-D).det) :
    IsRoleLorentz ((1-D)⁻¹*(1+D)) := by
  have hi := Matrix.nonsing_inv_mul (1-D) hdet
  have hit : (1-D).transpose*((1-D)⁻¹).transpose=1 := by
    simpa only [Matrix.transpose_mul, Matrix.transpose_one] using
      congrArg Matrix.transpose hi
  change _ * roleLorentzMetric * _ = roleLorentzMetric
  rw [Matrix.transpose_mul]
  calc
    _ = (1-D)⁻¹*((1+D)*roleLorentzMetric*(1+D).transpose)*((1-D)⁻¹).transpose := by
      simp only [Matrix.mul_assoc]
    _ = (1-D)⁻¹*((1-D)*roleLorentzMetric*(1-D).transpose)*((1-D)⁻¹).transpose := by
      rw [cayley_congruence D hD]
    _ = ((1-D)⁻¹*(1-D))*roleLorentzMetric*
        ((1-D).transpose*((1-D)⁻¹).transpose) := by
      simp only [Matrix.mul_assoc]
    _ = roleLorentzMetric := by rw [hi, hit, Matrix.one_mul, Matrix.mul_one]

#print axioms native_link_apply
#print axioms native_link_matrix
#print axioms native_link_inverse_apply
#print axioms native_lorentz_connection
#print axioms native_shift_fiber
#print axioms actual_open_holonomy_matrix
#print axioms actual_native_holonomy_apply
#print axioms actual_native_torsion
#print axioms actual_transport_center_flat
#print axioms actual_transport_center_row_equation
#print axioms actual_joint_center_polynomial
#print axioms sweep_affine
#print axioms periodic_gate_iff
#print axioms periodic_existence_iff_range
#print axioms periodic_fiber_iff_kernel
#print axioms periodic_unique_if_injective
#print axioms cayley_congruence
#print axioms cayley_is_lorentz
#print axioms D0.Geometry.transportedSolderCenter_covariance
#print axioms D0.Geometry.curvature_eq_holonomy_defect
#check D0.Geometry.IsLorentzAffineExteriorConnection
#check D0.Geometry.transportedSolderCenter
#check D0.Geometry.lorentzVectorEquiv_apply
#check periodic_existence_iff_range
#check periodic_fiber_iff_kernel

end
end D0.Research.NativeTransportedConnection
