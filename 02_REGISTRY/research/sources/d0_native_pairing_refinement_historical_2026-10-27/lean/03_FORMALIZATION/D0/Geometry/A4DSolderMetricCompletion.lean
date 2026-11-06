import D0.Geometry.A4DCoframeParentConstraint
import D0.Geometry.ArchiveRoleEquivalence

/-!
# Finite solder Gram completion of the centered coframe readout

The exact polynomial tangent is the existing `coframeMetricReadout`. The right
Lorentz action is on solder matrices, not a claimed action on pre-centered
coframes. The Gram matrix can be degenerate for arbitrary perturbations. No
physical metric, Cartan connection, constitutive law, nonlinear diffeomorphism
covariance, or observer representation is asserted.

Directional centering does not preserve arbitrary sitewise skew fields.
Readout-nullity below is unconditional for constant frame directions and
conditional on a literal centered lift for variable directions. No odd-cycle
kernel equality or removal of the even-cycle Nyquist residue is asserted.
-/

namespace D0.Geometry
open D0
open scoped BigOperators
noncomputable section

def roleLorentzSign (r : Role) : ℝ := (roleSign (roleRoleSigEquiv r) : ℝ)
@[simp] theorem roleLorentzSign_A : roleLorentzSign A = 1 := by
  norm_num [roleLorentzSign, roleRoleSigEquiv_A, roleSign]
@[simp] theorem roleLorentzSign_B : roleLorentzSign B = -1 := by
  norm_num [roleLorentzSign, roleRoleSigEquiv_B, roleSign]
@[simp] theorem roleLorentzSign_C : roleLorentzSign C = -1 := by
  norm_num [roleLorentzSign, roleRoleSigEquiv_C, roleSign]
@[simp] theorem roleLorentzSign_D : roleLorentzSign D = -1 := by
  norm_num [roleLorentzSign, roleRoleSigEquiv_D, roleSign]

theorem roleLorentzSign_mul_self (r : Role) : roleLorentzSign r * roleLorentzSign r = 1 := by
  rcases r with ⟨a,b⟩
  fin_cases a <;> fin_cases b <;> norm_num [roleLorentzSign, roleRoleSigEquiv, roleSign, A, B, C, D]

def roleLorentzMetric : Matrix Role Role ℝ := Matrix.diagonal roleLorentzSign
@[simp] theorem roleLorentzMetric_diagonal (r : Role) :
    roleLorentzMetric r r = roleLorentzSign r := Matrix.diagonal_apply_eq _ _
@[simp] theorem roleLorentzMetric_transpose : roleLorentzMetric.transpose = roleLorentzMetric := by
  exact Matrix.diagonal_transpose _
@[simp] theorem roleLorentzMetric_sq : roleLorentzMetric * roleLorentzMetric = 1 := by
  rw [roleLorentzMetric, Matrix.diagonal_mul_diagonal]
  simp only [roleLorentzSign_mul_self]
  exact Matrix.diagonal_one

/-- Row r is centered along the existing backward r-link average. -/
def centeredCoframeMatrix (N : ℕ) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) : Matrix Role Role ℝ :=
  fun r a => backwardAverage N r (fun y => e y r a) x
@[simp] theorem centeredCoframeMatrix_apply (N : ℕ) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) (r a : Role) :
    centeredCoframeMatrix N e x r a = backwardAverage N r (fun y => e y r a) x := rfl

theorem coframeMetricReadout_eq_centered_add_transpose (N : ℕ) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) :
    (coframeMetricReadout N e x).toMatrix =
      centeredCoframeMatrix N e x + (centeredCoframeMatrix N e x).transpose := rfl
@[simp] theorem centeredCoframeMatrix_zero (N : ℕ) (x : ArchiveRolePhaseGroup N) :
    centeredCoframeMatrix N 0 x = 0 := by
  ext r a
  simp [centeredCoframeMatrix, backwardAverage]
@[simp] theorem centeredCoframeMatrix_smul (N : ℕ) (e : LocalCoframeField N)
    (t : ℝ) (x : ArchiveRolePhaseGroup N) :
    centeredCoframeMatrix N (t • e) x = t • centeredCoframeMatrix N e x := by
  ext r a
  simp [centeredCoframeMatrix, backwardAverage]
  ring

def solderMatrix (N : ℕ) (e : LocalCoframeField N) (x : ArchiveRolePhaseGroup N) :
    Matrix Role Role ℝ := roleLorentzMetric + centeredCoframeMatrix N e x
@[simp] theorem solderMatrix_zero (N : ℕ) (x : ArchiveRolePhaseGroup N) :
    solderMatrix N 0 x = roleLorentzMetric := by simp [solderMatrix]

/-- Nonlinear candidate; nondegeneracy is not automatic for arbitrary e. -/
def solderMetricMatrix (N : ℕ) (e : LocalCoframeField N) (x : ArchiveRolePhaseGroup N) :
    Matrix Role Role ℝ := solderMatrix N e x * roleLorentzMetric * (solderMatrix N e x).transpose

theorem solderMetric_symmetric (N : ℕ) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) :
    (solderMetricMatrix N e x).transpose = solderMetricMatrix N e x := by
  simp [solderMetricMatrix, Matrix.transpose_mul, Matrix.mul_assoc]

theorem solderMetric_expand (N : ℕ) (e : LocalCoframeField N) (x : ArchiveRolePhaseGroup N) :
    solderMetricMatrix N e x = roleLorentzMetric + centeredCoframeMatrix N e x +
      (centeredCoframeMatrix N e x).transpose +
      centeredCoframeMatrix N e x * roleLorentzMetric * (centeredCoframeMatrix N e x).transpose := by
  unfold solderMetricMatrix solderMatrix
  rw [Matrix.transpose_add, roleLorentzMetric_transpose]
  simp only [Matrix.add_mul, Matrix.mul_add, roleLorentzMetric_sq, Matrix.one_mul]
  rw [Matrix.mul_assoc (centeredCoframeMatrix N e x) roleLorentzMetric roleLorentzMetric,
    roleLorentzMetric_sq, Matrix.mul_one]
  abel

theorem solderMetric_minus_background (N : ℕ) (e : LocalCoframeField N)
    (x : ArchiveRolePhaseGroup N) :
    solderMetricMatrix N e x - roleLorentzMetric = (coframeMetricReadout N e x).toMatrix +
      centeredCoframeMatrix N e x * roleLorentzMetric * (centeredCoframeMatrix N e x).transpose := by
  rw [solderMetric_expand, coframeMetricReadout_eq_centered_add_transpose]
  abel

/-- Exact algebraic flat tangent: the linear coefficient is the frozen readout. -/
theorem solderMetric_smul_expand (N : ℕ) (e : LocalCoframeField N)
    (t : ℝ) (x : ArchiveRolePhaseGroup N) :
    solderMetricMatrix N (t • e) x - roleLorentzMetric =
      t • (coframeMetricReadout N e x).toMatrix + t^2 •
        (centeredCoframeMatrix N e x * roleLorentzMetric * (centeredCoframeMatrix N e x).transpose) := by
  rw [solderMetric_minus_background, coframeMetricReadout_eq_centered_add_transpose,
    centeredCoframeMatrix_smul, coframeMetricReadout_eq_centered_add_transpose]
  simp only [Matrix.transpose_smul, smul_add, Matrix.smul_mul, Matrix.mul_smul, smul_smul, pow_two]

/-- Difference quotient with its exact remainder, requiring no calculus API. -/
theorem solderMetric_flat_tangent (N : ℕ) (e : LocalCoframeField N)
    (t : ℝ) (ht : t ≠ 0) (x : ArchiveRolePhaseGroup N) :
    t⁻¹ • (solderMetricMatrix N (t • e) x - roleLorentzMetric) =
      (coframeMetricReadout N e x).toMatrix + t •
        (centeredCoframeMatrix N e x * roleLorentzMetric * (centeredCoframeMatrix N e x).transpose) := by
  rw [solderMetric_smul_expand]
  simp [smul_add, smul_smul, pow_two, ht]

theorem solderMetric_forwardGauge_flat_tangent (N : ℕ) (xi : LocalRoleVector N)
    (t : ℝ) (x : ArchiveRolePhaseGroup N) :
    solderMetricMatrix N (t • forwardGaugeCoframe N xi) x - roleLorentzMetric =
      t • (symmetricRoleGradient N xi x).toMatrix + t^2 •
        (centeredCoframeMatrix N (forwardGaugeCoframe N xi) x * roleLorentzMetric *
          (centeredCoframeMatrix N (forwardGaugeCoframe N xi) x).transpose) := by
  rw [solderMetric_smul_expand, coframeMetricReadout_forwardGauge]

def IsRoleLorentz (Λ : Matrix Role Role ℝ) : Prop :=
  Λ * roleLorentzMetric * Λ.transpose = roleLorentzMetric

/-- Right frame action on arbitrary solder matrices, pointwise at each site. -/
theorem solderGram_right_lorentz_invariant (Θ Λ : Matrix Role Role ℝ) (hΛ : IsRoleLorentz Λ) :
    (Θ * Λ) * roleLorentzMetric * (Θ * Λ).transpose = Θ * roleLorentzMetric * Θ.transpose := by
  rw [Matrix.transpose_mul]
  calc
    Θ * Λ * roleLorentzMetric * (Λ.transpose * Θ.transpose) =
        Θ * (Λ * roleLorentzMetric * Λ.transpose) * Θ.transpose := by simp only [Matrix.mul_assoc]
    _ = _ := by rw [hΛ]

/-- At the flat solder η, the right-action variation is ηa. -/
def IsRoleLorentzTangent (a : Matrix Role Role ℝ) : Prop :=
  a.transpose * roleLorentzMetric + roleLorentzMetric * a = 0

theorem lorentzTangent_flat_solder_skew (a : Matrix Role Role ℝ) (ha : IsRoleLorentzTangent a) :
    roleLorentzMetric * a + (roleLorentzMetric * a).transpose = 0 := by
  simpa [IsRoleLorentzTangent, Matrix.transpose_mul, add_comm] using ha

/-- The tangent convention also kills the linear term of ΛηΛᵀ.
This connects the ηa flat-solder variation to the finite right action above. -/
theorem lorentzTangent_right_condition (a : Matrix Role Role ℝ) (ha : IsRoleLorentzTangent a) :
    a * roleLorentzMetric + roleLorentzMetric * a.transpose = 0 := by
  have hsandwich :
      roleLorentzMetric * (a.transpose * roleLorentzMetric + roleLorentzMetric * a) *
          roleLorentzMetric = a * roleLorentzMetric + roleLorentzMetric * a.transpose := by
    rw [Matrix.mul_add, Matrix.add_mul]
    simp only [← Matrix.mul_assoc, roleLorentzMetric_sq, Matrix.one_mul]
    rw [Matrix.mul_assoc (roleLorentzMetric * a.transpose) roleLorentzMetric roleLorentzMetric,
      roleLorentzMetric_sq, Matrix.mul_one]
    abel
  rw [← hsandwich, ha]
  simp

/-- Variable frame fields are readout-null if a literal centered lift is supplied. -/
theorem lorentzTangent_centeredLift_readout_zero (N : ℕ) (e : LocalCoframeField N)
    (a : ArchiveRolePhaseGroup N → Matrix Role Role ℝ)
    (ha : ∀ x, IsRoleLorentzTangent (a x))
    (he : ∀ x, centeredCoframeMatrix N e x = roleLorentzMetric * a x) :
    ∀ x, (coframeMetricReadout N e x).toMatrix = 0 := by
  intro x
  rw [coframeMetricReadout_eq_centered_add_transpose, he]
  exact lorentzTangent_flat_solder_skew _ (ha x)

/-- Constant pre-centered frame directions genuinely lie in the frozen readout kernel. -/
theorem lorentzTangent_centeredReadout_zero (N : ℕ) (a : Matrix Role Role ℝ)
    (ha : IsRoleLorentzTangent a) :
    ∀ x, (coframeMetricReadout N (fun _ => roleLorentzMetric * a) x).toMatrix = 0 := by
  apply lorentzTangent_centeredLift_readout_zero N _ (fun _ => a) (fun _ => ha)
  intro x
  ext r s
  simp [centeredCoframeMatrix, backwardAverage]

/-! ## Exact six-dimensional Lorentz tangent space -/

/-- This is a frame tangent carrier, not the symmetric metric shear carrier. -/
def roleSkewMatrices : Submodule ℝ (Matrix Role Role ℝ) where
  carrier := {m | ∀ a b, m a b = -m b a}
  zero_mem' := by intro a b; simp
  add_mem' := by
    intro m n hm hn a b
    simp only [Matrix.add_apply, hm a b, hn a b]
    ring
  smul_mem' := by
    intro t m hm a b
    simp only [Matrix.smul_apply, smul_eq_mul, hm a b]
    ring

def roleLorentzTangentSpace : Submodule ℝ (Matrix Role Role ℝ) where
  carrier := {a | IsRoleLorentzTangent a}
  zero_mem' := by simp [IsRoleLorentzTangent]
  add_mem' := by
    intro a b ha hb
    change a.transpose * roleLorentzMetric + roleLorentzMetric * a = 0 at ha
    change b.transpose * roleLorentzMetric + roleLorentzMetric * b = 0 at hb
    change (a + b).transpose * roleLorentzMetric + roleLorentzMetric * (a + b) = 0
    simp only [Matrix.transpose_add, Matrix.add_mul, Matrix.mul_add]
    calc
      _ = (a.transpose * roleLorentzMetric + roleLorentzMetric * a) +
          (b.transpose * roleLorentzMetric + roleLorentzMetric * b) := by abel
      _ = 0 := by rw [ha, hb, add_zero]
  smul_mem' := by
    intro t a ha
    simpa [IsRoleLorentzTangent, Matrix.transpose_smul, Matrix.smul_mul, Matrix.mul_smul,
      ← smul_add] using congrArg (fun m => t • m) ha

abbrev RoleLorentzTangent := roleLorentzTangentSpace

def lorentzTangentEquivSkew : RoleLorentzTangent ≃ₗ[ℝ] roleSkewMatrices where
  toFun a := ⟨roleLorentzMetric * a.val, by
    intro r s
    have h := congrArg (fun m : Matrix Role Role ℝ => m r s)
      (lorentzTangent_flat_solder_skew a.val a.property)
    simp only [Matrix.add_apply, Matrix.transpose_apply, Matrix.zero_apply] at h
    linarith⟩
  invFun e := ⟨roleLorentzMetric * e.val, by
    change (roleLorentzMetric * e.val).transpose * roleLorentzMetric +
      roleLorentzMetric * (roleLorentzMetric * e.val) = 0
    rw [Matrix.transpose_mul, roleLorentzMetric_transpose,
      Matrix.mul_assoc e.val.transpose roleLorentzMetric roleLorentzMetric,
      roleLorentzMetric_sq, Matrix.mul_one, ← Matrix.mul_assoc,
      roleLorentzMetric_sq, Matrix.one_mul]
    ext r s
    have h := e.property r s
    simp only [Matrix.add_apply, Matrix.transpose_apply, Matrix.zero_apply]
    linarith⟩
  left_inv a := by apply Subtype.ext; simp [← Matrix.mul_assoc]
  right_inv e := by apply Subtype.ext; simp [← Matrix.mul_assoc]
  map_add' a b := by apply Subtype.ext; exact Matrix.mul_add _ _ _
  map_smul' t a := by apply Subtype.ext; exact Matrix.mul_smul _ _ _

/-- Six independent coordinates use RolePair only as a finite index set.
The resulting matrix is antisymmetric, never identified with symmetric shear. -/
def skewFromRolePairs (u : RolePair → ℝ) : Matrix Role Role ℝ :=
  fun a b => if h : a = b then 0 else
    if roleCode a < roleCode b then u (rolePairOfDistinct a b h)
    else -u (rolePairOfDistinct a b h)

theorem skewFromRolePairs_skew (u : RolePair → ℝ) : skewFromRolePairs u ∈ roleSkewMatrices := by
  intro a b
  by_cases h : a = b
  · subst b; simp [skewFromRolePairs]
  · have hcode : roleCode a ≠ roleCode b := fun he => h (roleCode_injective he)
    rcases lt_or_gt_of_ne hcode with hab | hba
    · simp [skewFromRolePairs, h, Ne.symm h, hab, not_lt_of_ge hab.le,
        rolePairOfDistinct_swap a b h]
    · simp [skewFromRolePairs, h, Ne.symm h, hba, not_lt_of_ge hba.le,
        rolePairOfDistinct_swap a b h]

@[simp] theorem skewFromRolePairs_upper (u : RolePair → ℝ) (p : RolePair) :
    skewFromRolePairs u p.val.1 p.val.2 = u p := by
  simp [skewFromRolePairs, rolePair_ne p, p.property, rolePairOfDistinct_ordered]

def rolePairsEquivSkew : (RolePair → ℝ) ≃ₗ[ℝ] roleSkewMatrices where
  toFun u := ⟨skewFromRolePairs u, skewFromRolePairs_skew u⟩
  invFun e p := e.val p.val.1 p.val.2
  left_inv u := by funext p; exact skewFromRolePairs_upper u p
  right_inv e := by
    apply Subtype.ext
    funext a b
    change skewFromRolePairs (fun p => e.val p.val.1 p.val.2) a b = e.val a b
    by_cases h : a = b
    · subst b
      have hdiag := e.property a a
      simp only [skewFromRolePairs, dite_true]
      linarith
    · by_cases hab : roleCode a < roleCode b
      · simp [skewFromRolePairs, h, hab, rolePairOfDistinct]
      · have hba : roleCode b < roleCode a :=
          (lt_or_gt_of_ne (fun he => h (roleCode_injective he))).resolve_left hab
        simpa [skewFromRolePairs, h, hab, rolePairOfDistinct] using (e.property a b).symm
  map_add' u v := by
    apply Subtype.ext
    funext a b
    by_cases h : a = b <;> by_cases hab : roleCode a < roleCode b <;>
      simp [skewFromRolePairs, h, hab, add_comm]
  map_smul' t u := by
    apply Subtype.ext
    funext a b
    by_cases h : a = b <;> by_cases hab : roleCode a < roleCode b <;>
      simp [skewFromRolePairs, h, hab]

/-- Structural coordinate equivalence, not a dimension-only identification. -/
def rolePairsEquivLorentzTangent : (RolePair → ℝ) ≃ₗ[ℝ] RoleLorentzTangent :=
  rolePairsEquivSkew.trans lorentzTangentEquivSkew.symm

theorem roleLorentzTangent_finrank : Module.finrank ℝ RoleLorentzTangent = 6 := by
  rw [← rolePairsEquivLorentzTangent.finrank_eq, Module.finrank_pi, rolePair_card]

/-- Dimension of independent centered frame tangents; no pre-centering lift is implicit. -/
theorem localLorentzTangentField_finrank (N : ℕ) :
    Module.finrank ℝ (ArchiveRolePhaseGroup N → RoleLorentzTangent) = 6 * archiveModes N := by
  rw [Module.finrank_pi_fintype]
  simp [roleLorentzTangent_finrank, archiveModes, Nat.mul_comm]

end
end D0.Geometry
