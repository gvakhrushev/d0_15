import Mathlib.Tactic
import D0.Geometry.A4DObserverPositiveExterior

/-!
# Finite Lorentz-covariant positive quadratic forms vanish

This is the algebraic core of the finite-dimensional unitary affine
translation obstruction.  For a Hermitian translation generator P(v),
Q(v) = Tr(P(v)^2) is a nonnegative Lorentz-invariant quadratic form.
The theorem below proves directly, from a finite set of rotations and one
exact rational boost, that such a Q is zero.
-/

namespace D0.Research.FiniteLorentzCovariantPositiveQuadratic

structure Coefficients where
  tt : ℝ
  tx : ℝ
  ty : ℝ
  tz : ℝ
  xx : ℝ
  xy : ℝ
  xz : ℝ
  yy : ℝ
  yz : ℝ
  zz : ℝ

def quadratic (c : Coefficients) (t x y z : ℝ) : ℝ :=
  c.tt*t^2 + c.xx*x^2 + c.yy*y^2 + c.zz*z^2 +
  c.tx*t*x + c.ty*t*y + c.tz*t*z +
  c.xy*x*y + c.xz*x*z + c.yz*y*z

/-- Rotation by pi about the x axis. -/
def rotX (t x y z : ℝ) : ℝ × ℝ × ℝ × ℝ := (t, x, -y, -z)

/-- Rotation by pi about the y axis. -/
def rotY (t x y z : ℝ) : ℝ × ℝ × ℝ × ℝ := (t, -x, y, -z)

/-- A quarter turn about the z axis. -/
def quarterZ (t x y z : ℝ) : ℝ × ℝ × ℝ × ℝ := (t, -y, x, z)

/-- A quarter turn about the y axis. -/
def quarterY (t x y z : ℝ) : ℝ × ℝ × ℝ × ℝ := (t, z, y, -x)

/-- The exact Lorentz boost with gamma=5/3 and gamma*beta=4/3. -/
noncomputable def rationalBoost (t x y z : ℝ) : ℝ × ℝ × ℝ × ℝ :=
  ((5*t+4*x)/3, (4*t+5*x)/3, y, z)

/-- Identify the four coefficient coordinates with the owned A/B/C/D roles. -/
def roleCoordinates (t x y z : ℝ) : D0.Geometry.RoleVector := fun r =>
  if r = D0.A then t else
  if r = D0.B then x else
  if r = D0.C then y else z

/-- Any nonnegative quadratic form invariant under spatial rotations and one
nontrivial Lorentz boost is zero.  The finite transformations listed here
generate exactly the coefficient constraints needed for the proof. -/
theorem invariant_nonnegative_quadratic_eq_zero (c : Coefficients)
    (hnonneg : ∀ t x y z, 0 ≤ quadratic c t x y z)
    (hrotX : ∀ t x y z,
      quadratic c (rotX t x y z).1 (rotX t x y z).2.1
        (rotX t x y z).2.2.1 (rotX t x y z).2.2.2 = quadratic c t x y z)
    (hrotY : ∀ t x y z,
      quadratic c (rotY t x y z).1 (rotY t x y z).2.1
        (rotY t x y z).2.2.1 (rotY t x y z).2.2.2 = quadratic c t x y z)
    (hquarterZ : ∀ t x y z,
      quadratic c (quarterZ t x y z).1 (quarterZ t x y z).2.1
        (quarterZ t x y z).2.2.1 (quarterZ t x y z).2.2.2 = quadratic c t x y z)
    (hquarterY : ∀ t x y z,
      quadratic c (quarterY t x y z).1 (quarterY t x y z).2.1
        (quarterY t x y z).2.2.1 (quarterY t x y z).2.2.2 = quadratic c t x y z)
    (hboost : ∀ t x y z,
      quadratic c (rationalBoost t x y z).1 (rationalBoost t x y z).2.1
        (rationalBoost t x y z).2.2.1 (rationalBoost t x y z).2.2.2 = quadratic c t x y z) :
    ∀ t x y z, quadratic c t x y z = 0 := by
  have hty : c.ty = 0 := by
    have h := hrotX 1 0 1 0
    simp [rotX, quadratic] at h
    nlinarith
  have htz : c.tz = 0 := by
    have h := hrotX 1 0 0 1
    simp [rotX, quadratic] at h
    nlinarith
  have hxy : c.xy = 0 := by
    have h := hrotX 0 1 1 0
    simp [rotX, quadratic] at h
    nlinarith
  have hxz : c.xz = 0 := by
    have h := hrotX 0 1 0 1
    simp [rotX, quadratic] at h
    nlinarith
  have htx : c.tx = 0 := by
    have h := hrotY 1 1 0 0
    simp [rotY, quadratic] at h
    nlinarith
  have hyz : c.yz = 0 := by
    have h := hrotY 0 0 1 1
    simp [rotY, quadratic] at h
    nlinarith
  have hxx_yy : c.xx = c.yy := by
    have h := hquarterZ 0 1 0 0
    simp [quarterZ, quadratic] at h
    nlinarith
  have hxx_zz : c.xx = c.zz := by
    have h := hquarterY 0 1 0 0
    simp [quarterY, quadratic] at h
    nlinarith
  have hboost0 := hboost 1 0 0 0
  simp [rationalBoost, quadratic, htx] at hboost0
  have hsum : c.tt + c.xx = 0 := by
    field_simp at hboost0
    nlinarith
  have htt_nonneg : 0 ≤ c.tt := by
    have h := hnonneg 1 0 0 0
    simp [quadratic] at h
    exact h
  have hxx_nonneg : 0 ≤ c.xx := by
    have h := hnonneg 0 1 0 0
    simp [quadratic] at h
    exact h
  have htt_zero : c.tt = 0 := by linarith
  have hxx_zero : c.xx = 0 := by linarith
  have hyy_zero : c.yy = 0 := by rw [← hxx_yy, hxx_zero]
  have hzz_zero : c.zz = 0 := by rw [← hxx_zz, hxx_zero]
  intro t x y z
  simp [quadratic, htt_zero, htx, hty, htz, hxx_zero, hxy, hxz,
    hyy_zero, hyz, hzz_zero]

/-- The rational A/B boost used above is the already-owned D0 Lorentz boost. -/
theorem owned_role_boost_is_lorentz :
    D0.Geometry.IsRoleLorentz D0.Geometry.rationalABBoost :=
  D0.Geometry.rationalABBoost_lorentz

/-- The rational matrix in the invariant-form proof is exactly the owned
A/B boost, in the declared (time,x,y,z) role coordinates. -/
theorem rational_boost_matches_owned_role_boost (t x y z : ℝ) :
    D0.Geometry.rationalABBoostObserver (roleCoordinates t x y z) =
      roleCoordinates (rationalBoost t x y z).1 (rationalBoost t x y z).2.1
        (rationalBoost t x y z).2.2.1 (rationalBoost t x y z).2.2.2 := by
  funext r
  fin_cases r <;>
    norm_num [D0.Geometry.rationalABBoostObserver,
      D0.Geometry.rationalABBoost, roleCoordinates, rationalBoost,
      D0.A, D0.B, D0.C, D0.D, Fintype.sum_prod_type] <;>
    ring

#print axioms invariant_nonnegative_quadratic_eq_zero
#print axioms owned_role_boost_is_lorentz
#print axioms rational_boost_matches_owned_role_boost
#check D0.Geometry.rationalABBoost_lorentz

end D0.Research.FiniteLorentzCovariantPositiveQuadratic
