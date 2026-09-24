import Mathlib.Tactic
import Mathlib.Analysis.Matrix.PosDef
import Mathlib.LinearAlgebra.Matrix.BilinearForm
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.LinearAlgebra.Matrix.ToLin
import D0.Geometry.ArchiveExteriorFrameLift
import D0.Geometry.A4DSolderMetricCompletion

/-!
# Observer Lorentz form on role vectors

This module keeps the observer metric distinct from the located primal/dual
placement.  The rest observer is a reference gauge; this package does not call
it physical time.  The exterior action used below is the algebraic lift owned
in `ArchiveExteriorFrameLift`.
-/

namespace D0.Geometry

open D0
open scoped BigOperators Matrix

noncomputable section

local instance : LinearOrder Role := LinearOrder.lift' roleCode roleCode_injective

abbrev RoleVector := Role → ℝ

def observerCovector (n : RoleVector) (r : Role) : ℝ :=
  roleLorentzSign r * n r

/-- `h_n = -η + 2 n♭⊗n♭`. -/
def observerMetric (n : RoleVector) : Matrix Role Role ℝ :=
  fun r s => -roleLorentzMetric r s +
    2 * observerCovector n r * observerCovector n s

def lorentzUnitObserver (n : RoleVector) : Prop :=
  ∑ r : Role, roleLorentzSign r * n r ^ 2 = 1

def restObserver : RoleVector := fun r => if r = A then 1 else 0

theorem observerMetric_symmetric (n : RoleVector) :
    (observerMetric n).transpose = observerMetric n := by
  ext r s
  by_cases h : r = s
  · subst s
    simp [observerMetric, roleLorentzMetric, Matrix.diagonal_apply]
  · simp [observerMetric, roleLorentzMetric, Matrix.diagonal_apply, h, Ne.symm h]
    ring

theorem restObserver_lorentzUnit : lorentzUnitObserver restObserver := by
  unfold lorentzUnitObserver restObserver
  simp [observerCovector, roleLorentzSign_A, roleLorentzSign_B,
    roleLorentzSign_C, roleLorentzSign_D]

/-- The reference observer gives the positive counting form. -/
theorem observerMetric_restObserver (r s : Role) :
    observerMetric restObserver r s = if r = s then 1 else 0 := by
  fin_cases r <;> fin_cases s <;>
    norm_num [observerMetric, observerCovector, restObserver,
      roleLorentzMetric, roleLorentzSign, roleRoleSigEquiv, roleSign,
      A, B, C, D]

theorem observerMetric_restObserver_positive (v : RoleVector) (hv : v ≠ 0) :
    0 < ∑ r : Role, ∑ s : Role,
      v r * observerMetric restObserver r s * v s := by
  have hdiag : ∀ r s, observerMetric restObserver r s = if r = s then 1 else 0 :=
    observerMetric_restObserver
  rw [show (∑ r : Role, ∑ s : Role,
      v r * observerMetric restObserver r s * v s) = ∑ r : Role, v r ^ 2 by
        simp_rw [hdiag]
        simp [pow_two]]
  have hpos : ∃ r, v r ≠ 0 := by
    by_contra h
    push_neg at h
    exact hv (funext h)
  obtain ⟨r, hr⟩ := hpos
  have hs : 0 < v r ^ 2 := sq_pos_of_ne_zero hr
  exact lt_of_lt_of_le hs (Finset.single_le_sum (fun i hi => sq_nonneg (v i))
    (Finset.mem_univ r))

/-- Coordinate form of the observer quadratic form. -/
theorem observerMetric_quadratic_coords (n v : RoleVector) :
    (∑ r : Role, ∑ s : Role, v r * observerMetric n r s * v s) =
      -(v A)^2 + (v B)^2 + (v C)^2 + (v D)^2 +
        2 * (n A * v A - n B * v B - n C * v C - n D * v D)^2 := by
  simp [observerMetric, observerCovector, roleLorentzMetric,
    roleLorentzSign, roleRoleSigEquiv, roleSign, Role, Dyad,
    Fintype.sum_prod_type, A, B, C, D, Matrix.diagonal_apply]
  ring

theorem lorentzUnitObserver_coords (n : RoleVector)
    (hn : lorentzUnitObserver n) :
    (n A)^2 = 1 + (n B)^2 + (n C)^2 + (n D)^2 := by
  simp [lorentzUnitObserver, roleLorentzSign, roleRoleSigEquiv,
    roleSign, Role, Dyad, Fintype.sum_prod_type, A, B, C, D] at hn
  simp only [A, B, C, D]
  nlinarith

/-- The arbitrary unit timelike observer induces a strictly positive real
quadratic form on the role space.  The sum-of-squares identity below uses only
the unit Lorentz norm; it does not choose a time direction. -/
theorem observerMetric_positive (n v : RoleVector)
    (hn : lorentzUnitObserver n) (hv : v ≠ 0) :
    0 < ∑ r : Role, ∑ s : Role,
      v r * observerMetric n r s * v s := by
  let t := n A
  let u := n B
  let p := n C
  let q := n D
  let a := v A
  let b := v B
  let c := v C
  let d := v D
  let β := t * a - u * b - p * c - q * d
  let zB := t * b - u * a
  let zC := t * c - p * a
  let zD := t * d - q * a
  let ζ := t * (u * b + p * c + q * d) - (u^2 + p^2 + q^2) * a
  have ht : t^2 = 1 + u^2 + p^2 + q^2 :=
    lorentzUnitObserver_coords n hn
  have htpos : 0 < t^2 := by nlinarith [sq_nonneg u, sq_nonneg p, sq_nonneg q]
  have hident :
      t^2 * (∑ r : Role, ∑ s : Role,
        v r * observerMetric n r s * v s) =
        t^2 * β^2 + zB^2 + zC^2 + zD^2 + ζ^2 := by
    rw [observerMetric_quadratic_coords]
    dsimp [t, u, p, q, a, b, c, d, β, zB, zC, zD, ζ] at ht ⊢
    calc
      _ = ((n A)^2 - (1 + (n B)^2 + (n C)^2 + (n D)^2)) *
          ((v A) * ((v A) * ((n A)^2 + (n B)^2 + (n C)^2 + (n D)^2) -
            2 * (n A) * ((n B)*(v B)+(n C)*(v C)+(n D)*(v D)))) +
          ((n A)^2 * (n A * v A - n B * v B - n C * v C - n D * v D)^2 +
            (n A * v B - n B * v A)^2 +
            (n A * v C - n C * v A)^2 +
            (n A * v D - n D * v A)^2 +
            (n A * (n B * v B + n C * v C + n D * v D) -
              ((n B)^2 + (n C)^2 + (n D)^2) * v A)^2) := by ring
      _ = _ := by rw [ht]; ring
  have hnonneg : 0 ≤ ∑ r : Role, ∑ s : Role,
      v r * observerMetric n r s * v s := by
    have hsos : 0 ≤ t^2 * β^2 + zB^2 + zC^2 + zD^2 + ζ^2 := by
      positivity
    nlinarith
  by_contra hnot
  have hzero : ∑ r : Role, ∑ s : Role,
      v r * observerMetric n r s * v s = 0 := by linarith
  rw [hzero] at hident
  have hβ : β = 0 := by
    have hzeroβ : t^2 * β^2 = 0 := by
      nlinarith only [hident, sq_nonneg zB, sq_nonneg zC,
        sq_nonneg zD, sq_nonneg ζ]
    have hβsq : β^2 = 0 := (mul_eq_zero.mp hzeroβ).resolve_left (ne_of_gt htpos)
    nlinarith
  have hsum : zB^2 + zC^2 + zD^2 + ζ^2 = 0 := by
    simpa [hβ] using hident.symm
  have hzB : zB = 0 := by
    nlinarith only [hsum, sq_nonneg zC, sq_nonneg zD, sq_nonneg ζ]
  have hzC : zC = 0 := by
    nlinarith only [hsum, sq_nonneg zB, sq_nonneg zD, sq_nonneg ζ]
  have hzD : zD = 0 := by
    nlinarith only [hsum, sq_nonneg zB, sq_nonneg zC, sq_nonneg ζ]
  have ha : a = 0 := by
    calc
      a = (t^2 - (u^2+p^2+q^2))*a := by rw [ht]; ring
      _ = t*β + u*zB + p*zC + q*zD := by dsimp [β,zB,zC,zD]; ring
      _ = 0 := by simp [hβ,hzB,hzC,hzD]
  have htne : t ≠ 0 := by nlinarith
  have hb : b = 0 := by
    have : t*b = 0 := by simpa [zB, ha] using hzB
    exact (mul_eq_zero.mp this).resolve_left htne
  have hc : c = 0 := by
    have : t*c = 0 := by simpa [zC, ha] using hzC
    exact (mul_eq_zero.mp this).resolve_left htne
  have hd : d = 0 := by
    have : t*d = 0 := by simpa [zD, ha] using hzD
    exact (mul_eq_zero.mp this).resolve_left htne
  apply hv
  funext r
  fin_cases r
  · simpa [a, A] using ha
  · simpa [c, C] using hc
  · simpa [d, D] using hd
  · simpa [b, B] using hb

/-- Matrix-level positive definiteness of the observer form. -/
theorem observerMetric_posDef (n : RoleVector)
    (hn : lorentzUnitObserver n) : (observerMetric n).PosDef := by
  apply Matrix.PosDef.of_dotProduct_mulVec_pos
  · change Matrix.conjTranspose (observerMetric n) = observerMetric n
    ext r s
    have hs := congrArg (fun M : Matrix Role Role ℝ => M r s)
      (observerMetric_symmetric n)
    simpa [Matrix.conjTranspose_apply, Matrix.transpose_apply] using hs
  · intro v hv
    simpa [dotProduct, Matrix.mulVec, Finset.mul_sum,
      mul_assoc] using observerMetric_positive n v hn hv

/-- On every exterior degree, each ordered basis blade has positive observer
Gram determinant.  This records the principal minors of the induced exterior
pairing; it does not identify that pairing with the located `J`. -/
theorem observerExteriorBladeGram_pos (n : RoleVector)
    (hn : lorentzUnitObserver n) (k : ℕ)
    (S : Set.powersetCard Role k) :
    0 < (observerMetric n |>.submatrix
      (Set.powersetCard.ofFinEmbEquiv.symm S)
      (Set.powersetCard.ofFinEmbEquiv.symm S)).det := by
  exact ((observerMetric_posDef n hn).submatrix
    (Set.powersetCard.ofFinEmbEquiv.symm S).injective).det_pos

/-- The canonical induced bilinear form on each exterior degree.  It uses the
exterior power of the one-form map and Mathlib's determinant pairing between
exterior powers of a space and its dual. -/
def observerExteriorPairing (n : RoleVector) (k : ℕ)
    (z w : ⋀[ℝ]^k RoleSpace) : ℝ :=
  exteriorPower.pairingDual ℝ RoleSpace k
    (exteriorPower.map k ((observerMetric n).toBilin' :
      RoleSpace →ₗ[ℝ] Module.Dual ℝ RoleSpace) z) w

def exteriorPairingFromBilin (k : ℕ) (B : LinearMap.BilinForm ℝ RoleSpace) :
    LinearMap.BilinForm ℝ (⋀[ℝ]^k RoleSpace) :=
  (exteriorPower.pairingDual ℝ RoleSpace k).comp
    (exteriorPower.map k (B : RoleSpace →ₗ[ℝ] Module.Dual ℝ RoleSpace))

/-- Exterior determinant pairing commutes with a simultaneous change of
frame in both arguments. -/
theorem exteriorPairingFromBilin_natural (k : ℕ)
    (B : LinearMap.BilinForm ℝ RoleSpace) (L : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    (exteriorPairingFromBilin k B).comp
      (exteriorPower.map k L.toLinearMap)
      (exteriorPower.map k L.toLinearMap) =
    exteriorPairingFromBilin k (B.comp L.toLinearMap L.toLinearMap) := by
  apply LinearMap.ext_on (exteriorPower.ιMulti_span ℝ k RoleSpace)
  rintro z ⟨v, rfl⟩
  apply LinearMap.ext_on (exteriorPower.ιMulti_span ℝ k RoleSpace)
  rintro w ⟨u, rfl⟩
  simp [exteriorPairingFromBilin, LinearMap.BilinForm.comp_apply,
    exteriorPower.map_apply_ιMulti, exteriorPower.pairingDual_ιMulti_ιMulti,
    Matrix.det_apply]

theorem observerExteriorPairing_blades (n : RoleVector) (k : ℕ)
    (S T : Set.powersetCard Role k) :
    observerExteriorPairing n k
      (archiveRoleBasis.exteriorPower k S)
      (archiveRoleBasis.exteriorPower k T) =
      (Matrix.of fun i j => observerMetric n
        (Set.powersetCard.ofFinEmbEquiv.symm S j)
        (Set.powersetCard.ofFinEmbEquiv.symm T i)).det := by
  simp only [observerExteriorPairing, exteriorPower.basis_apply,
    exteriorPower.map_apply_ιMulti_family]
  unfold exteriorPower.ιMulti_family
  rw [exteriorPower.pairingDual_ιMulti_ιMulti]
  congr 1
  ext i j
  simp [Matrix.toBilin'_single, Matrix.toBilin'_apply,
    archiveRoleBasis, Pi.basisFun_apply, Pi.single_apply]

/-- Rational A/B boost with `cosh = 5/3`, `sinh = 4/3`. -/
def rationalABBoost : Matrix Role Role ℝ := fun r s =>
  if r = A then
    if s = A then 5 / 3 else if s = B then 4 / 3 else 0
  else if r = B then
    if s = A then 4 / 3 else if s = B then 5 / 3 else 0
  else if r = s then 1 else 0

def rationalABBoostInverse : Matrix Role Role ℝ := fun r s =>
  if r = A then
    if s = A then 5 / 3 else if s = B then -4 / 3 else 0
  else if r = B then
    if s = A then -4 / 3 else if s = B then 5 / 3 else 0
  else if r = s then 1 else 0

theorem rationalABBoostInverse_mul :
    rationalABBoostInverse * rationalABBoost = 1 := by
  ext r s
  fin_cases r <;> fin_cases s <;>
    norm_num [Matrix.mul_apply, rationalABBoostInverse, rationalABBoost,
      Fintype.sum_prod_type, A, B, C, D]

theorem rationalABBoost_mul_inverse :
    rationalABBoost * rationalABBoostInverse = 1 := by
  ext r s
  fin_cases r <;> fin_cases s <;>
    norm_num [Matrix.mul_apply, rationalABBoostInverse, rationalABBoost,
      Fintype.sum_prod_type, A, B, C, D]

def rationalABBoostEquiv : RoleSpace ≃ₗ[ℝ] RoleSpace :=
  Matrix.toLin'OfInv rationalABBoostInverse_mul rationalABBoost_mul_inverse

theorem rationalABBoost_lorentz : IsRoleLorentz rationalABBoost := by
  unfold IsRoleLorentz
  ext r s
  fin_cases r <;> fin_cases s <;>
    norm_num [rationalABBoost, roleLorentzMetric, Matrix.mul_apply,
      Matrix.transpose_apply, Matrix.diagonal_apply,
      roleLorentzSign, roleRoleSigEquiv, roleSign, Fintype.sum_prod_type,
      A, B, C, D]

def rationalABBoostObserver (n : RoleVector) : RoleVector :=
  fun r => ∑ s : Role, rationalABBoost r s * n s

theorem rationalABBoostObserver_rest (r : Role) :
    rationalABBoostObserver restObserver r =
      if r = A then 5 / 3 else if r = B then 4 / 3 else 0 := by
  fin_cases r <;> norm_num [rationalABBoostObserver, rationalABBoost,
    restObserver, A, B, C, D]

theorem rationalABBoostObserver_lorentzUnit :
    lorentzUnitObserver (rationalABBoostObserver restObserver) := by
  unfold lorentzUnitObserver
  have hv := rationalABBoostObserver_rest
  simp_rw [hv]
  norm_num [Role, Dyad, roleLorentzSign, roleRoleSigEquiv, roleSign,
    Fintype.sum_prod_type, A, B, C, D]

set_option maxHeartbeats 1000000 in
/-- The observer is transported along the rational Lorentz boost.  Its
positive form transforms by inverse congruence, as a bilinear form must. -/
theorem rationalABBoost_observerMetric_congruence (n : RoleVector) :
    rationalABBoost.transpose * observerMetric (rationalABBoostObserver n) *
        rationalABBoost = observerMetric n := by
  ext r s
  fin_cases r <;> fin_cases s <;>
    norm_num [Matrix.mul_apply, Matrix.transpose_apply, observerMetric,
      observerCovector, rationalABBoostObserver, rationalABBoost,
      roleLorentzMetric, roleLorentzSign, roleRoleSigEquiv, roleSign,
      Fintype.sum_prod_type, A, B, C, D, Matrix.diagonal_apply] <;>
    ring

/-- Exact observer congruence in every exterior degree.  The exterior lift
uses the same rational boost as the vector representation. -/
theorem rationalABBoost_observerExteriorPairing_congruence
    (n : RoleVector) (k : ℕ) (z w : ⋀[ℝ]^k RoleSpace) :
    observerExteriorPairing (rationalABBoostObserver n) k
      (exteriorPower.map k rationalABBoostEquiv.toLinearMap z)
      (exteriorPower.map k rationalABBoostEquiv.toLinearMap w) =
    observerExteriorPairing n k z w := by
  have hL : rationalABBoostEquiv.toLinearMap = Matrix.toLin' rationalABBoost := rfl
  have hB :
      ((observerMetric (rationalABBoostObserver n)).toBilin').comp
        rationalABBoostEquiv.toLinearMap rationalABBoostEquiv.toLinearMap =
      (observerMetric n).toBilin' := by
    rw [hL, Matrix.toBilin'_comp, rationalABBoost_observerMetric_congruence]
  change (exteriorPairingFromBilin k
      ((observerMetric (rationalABBoostObserver n)).toBilin')).comp
        (exteriorPower.map k rationalABBoostEquiv.toLinearMap)
        (exteriorPower.map k rationalABBoostEquiv.toLinearMap) z w =
      exteriorPairingFromBilin k ((observerMetric n).toBilin') z w
  rw [exteriorPairingFromBilin_natural, hB]

/-- The observer form is preserved when vectors and the observer move by `L`. -/
def preservesObserverForm (L : RoleSpace ≃ₗ[ℝ] RoleSpace) (n : RoleVector) : Prop :=
  ((observerMetric (L n)).toBilin').comp L.toLinearMap L.toLinearMap =
    (observerMetric n).toBilin'

/-- All-degree congruence for an arbitrary frame that preserves `h_n`.
The rational boost below is one control, not the only case. -/
theorem observerExteriorPairing_congruence
    (L : RoleSpace ≃ₗ[ℝ] RoleSpace) (n : RoleVector)
    (hL : preservesObserverForm L n) (k : ℕ) (z w : ⋀[ℝ]^k RoleSpace) :
    observerExteriorPairing (L n) k
        (exteriorPower.map k L.toLinearMap z)
        (exteriorPower.map k L.toLinearMap w) =
      observerExteriorPairing n k z w := by
  change (exteriorPairingFromBilin k ((observerMetric (L n)).toBilin')).comp
      (exteriorPower.map k L.toLinearMap)
      (exteriorPower.map k L.toLinearMap) z w =
    exteriorPairingFromBilin k ((observerMetric n).toBilin') z w
  rw [exteriorPairingFromBilin_natural, hL]


/-- Observer-flat `v ↦ h_n(v, ·)`. -/
def observerFlat (n : RoleVector) (v : RoleSpace) : Module.Dual ℝ RoleSpace :=
  (observerMetric n).toBilin' v

theorem observerFlat_contragredient (L : RoleSpace ≃ₗ[ℝ] RoleSpace) (n : RoleVector)
    (hL : preservesObserverForm L n) (v : RoleSpace) :
    observerFlat (L n) (L v) = (observerFlat n v).comp L.symm.toLinearMap := by
  refine LinearMap.ext ?_
  intro w
  have h := congrArg (fun B : LinearMap.BilinForm ℝ RoleSpace => B v (L.symm w)) hL
  simpa [observerFlat, LinearMap.BilinForm.comp_apply, LinearEquiv.symm_apply_apply] using h

theorem observer_creator_adjoint_covariant (L : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (n : RoleVector) (hL : preservesObserverForm L n) (v : RoleSpace)
    (ψ : ArchiveFockState → ℝ) :
    archiveExteriorFrameLift L
        (archiveExteriorContraction (observerFlat n v) ψ) =
      archiveExteriorContraction (observerFlat (L n) (L v))
        (archiveExteriorFrameLift L ψ) := by
  rw [archiveExteriorFrameLift_contraction_covariant, ← observerFlat_contragredient L n hL v]

theorem observerFlat_rest_basis (r : Role) :
    observerFlat restObserver (archiveRoleBasis r) = archiveRoleBasis.coord r := by
  ext v
  simp [observerFlat, Matrix.toBilin'_apply, observerMetric_restObserver, archiveRoleBasis,
    Pi.basisFun_apply, Pi.single_apply, Module.Basis.coord_apply, eq_comm]

/-- The observer contraction is the metric adjoint of the creator, transported
with the observer. -/
theorem observer_contraction_adjoint_covariant
    (L : RoleSpace ≃ₗ[ℝ] RoleSpace) (n : RoleVector)
    (hL : preservesObserverForm L n) (v : RoleSpace)
    (ψ : ArchiveFockState → ℝ) :
    archiveExteriorContraction (observerFlat n v) ψ =
      archiveExteriorFrameLift L.symm
        (archiveExteriorContraction (observerFlat (L n) (L v))
          (archiveExteriorFrameLift L ψ)) := by
  have hcancel (φ : ArchiveFockState → ℝ) :
      φ = archiveExteriorFrameLift L.symm (archiveExteriorFrameLift L φ) := by
    have hinv := (archiveExteriorFrameLift_inverse L).2
    have happ := congrArg
      (fun T : (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ) => T φ) hinv
    simpa [LinearMap.comp_apply, LinearMap.id_apply] using happ.symm
  exact (hcancel _).trans (by rw [observer_creator_adjoint_covariant L n hL v ψ])

theorem roleLorentzMetric_det_sq_one :
    roleLorentzMetric.det * roleLorentzMetric.det = 1 := by
  have hη := congrArg Matrix.det roleLorentzMetric_sq
  rw [Matrix.det_mul, Matrix.det_one] at hη
  exact hη

theorem roleLorentzMetric_det_isUnit : IsUnit roleLorentzMetric.det :=
  IsUnit.of_mul_eq_one roleLorentzMetric.det roleLorentzMetric_det_sq_one

theorem roleLorentzMetric_inv : roleLorentzMetric⁻¹ = roleLorentzMetric :=
  Matrix.inv_eq_right_inv roleLorentzMetric_sq

theorem isRoleLorentz_det_sq (Λ : Matrix Role Role ℝ) (hΛ : IsRoleLorentz Λ) :
    Λ.det * Λ.det = 1 := by
  have hdet : ((Λ * roleLorentzMetric) * Λ.transpose).det = roleLorentzMetric.det := by
    simpa [Matrix.mul_assoc] using congrArg Matrix.det hΛ
  rw [Matrix.det_mul, Matrix.det_mul, Matrix.det_transpose] at hdet
  have hstep :
      Λ.det * Λ.det * 1 =
        ((Λ.det * roleLorentzMetric.det) * Λ.det) * roleLorentzMetric.det := by
    calc
      Λ.det * Λ.det * 1 =
          Λ.det * Λ.det * (roleLorentzMetric.det * roleLorentzMetric.det) := by
            rw [roleLorentzMetric_det_sq_one]
      _ = ((Λ.det * roleLorentzMetric.det) * Λ.det) * roleLorentzMetric.det := by ring
  rw [hdet, roleLorentzMetric_det_sq_one] at hstep
  simpa using hstep

theorem isRoleLorentz_det_isUnit (Λ : Matrix Role Role ℝ) (hΛ : IsRoleLorentz Λ) :
    IsUnit Λ.det :=
  IsUnit.of_mul_eq_one Λ.det (isRoleLorentz_det_sq Λ hΛ)

/-- Vector representative `g = Λ⁻¹` of a right Lorentz matrix. -/
def lorentzVectorEquiv (Λ : Matrix Role Role ℝ) (hΛ : IsRoleLorentz Λ) :
    RoleSpace ≃ₗ[ℝ] RoleSpace :=
  Matrix.toLin'OfInv
    (Matrix.mul_nonsing_inv Λ (isRoleLorentz_det_isUnit Λ hΛ))
    (Matrix.nonsing_inv_mul Λ (isRoleLorentz_det_isUnit Λ hΛ))

theorem lorentzVectorEquiv_apply (Λ : Matrix Role Role ℝ) (hΛ : IsRoleLorentz Λ)
    (v : RoleVector) :
    lorentzVectorEquiv Λ hΛ v = Λ⁻¹ *ᵥ v := by
  dsimp [lorentzVectorEquiv, Matrix.toLin'OfInv]

theorem lorentz_inv_transpose_metric (Λ : Matrix Role Role ℝ) (hΛ : IsRoleLorentz Λ) :
    (Λ⁻¹).transpose * roleLorentzMetric * Λ⁻¹ = roleLorentzMetric := by
  have hprod : (Λ * roleLorentzMetric * Λ.transpose)⁻¹ =
      (Λ.transpose)⁻¹ * roleLorentzMetric⁻¹ * Λ⁻¹ := by
    rw [Matrix.mul_inv_rev (Λ * roleLorentzMetric) Λ.transpose,
      Matrix.mul_inv_rev Λ roleLorentzMetric, ← Matrix.mul_assoc]
  rw [hΛ, roleLorentzMetric_inv, ← Matrix.transpose_nonsing_inv] at hprod
  exact hprod.symm

theorem observerCovector_eq_mulVec (n : RoleVector) (r : Role) :
    observerCovector n r = (roleLorentzMetric *ᵥ n) r := by
  rw [observerCovector, roleLorentzMetric, Matrix.mulVec_diagonal]

theorem observerMetric_eq_outer (n : RoleVector) :
    observerMetric n =
      -roleLorentzMetric +
        (2 : ℝ) • Matrix.vecMulVec (roleLorentzMetric *ᵥ n) (roleLorentzMetric *ᵥ n) := by
  ext r s
  unfold observerMetric
  rw [observerCovector_eq_mulVec n r, observerCovector_eq_mulVec n s]
  simp [Matrix.vecMulVec_apply, Matrix.smul_apply, Matrix.add_apply, Matrix.neg_apply]
  ring

/-- Moving the observer and every vector by `Λ⁻¹` preserves `h_n`. -/
theorem observerMetric_vector_congruence (Λ : Matrix Role Role ℝ) (hΛ : IsRoleLorentz Λ)
    (n : RoleVector) :
    (Λ⁻¹).transpose * observerMetric (Λ⁻¹ *ᵥ n) * Λ⁻¹ = observerMetric n := by
  have hmet := lorentz_inv_transpose_metric Λ hΛ
  rw [observerMetric_eq_outer (Λ⁻¹ *ᵥ n), observerMetric_eq_outer n]
  have hsplit :
      (Λ⁻¹).transpose *
          (-roleLorentzMetric +
            (2 : ℝ) • Matrix.vecMulVec (roleLorentzMetric *ᵥ (Λ⁻¹ *ᵥ n))
              (roleLorentzMetric *ᵥ (Λ⁻¹ *ᵥ n))) * Λ⁻¹ =
        (Λ⁻¹).transpose * (-roleLorentzMetric) * Λ⁻¹ +
          (Λ⁻¹).transpose *
            ((2 : ℝ) • Matrix.vecMulVec (roleLorentzMetric *ᵥ (Λ⁻¹ *ᵥ n))
              (roleLorentzMetric *ᵥ (Λ⁻¹ *ᵥ n))) * Λ⁻¹ := by
    rw [Matrix.mul_add, Matrix.add_mul]
  rw [hsplit]
  have hneg : (Λ⁻¹).transpose * (-roleLorentzMetric) * Λ⁻¹ = -roleLorentzMetric := by
    rw [Matrix.mul_neg, Matrix.neg_mul, hmet]
  rw [hneg]
  have hscale :
      (Λ⁻¹).transpose *
          ((2 : ℝ) • Matrix.vecMulVec (roleLorentzMetric *ᵥ (Λ⁻¹ *ᵥ n))
            (roleLorentzMetric *ᵥ (Λ⁻¹ *ᵥ n))) * Λ⁻¹ =
        (2 : ℝ) • ((Λ⁻¹).transpose *
          Matrix.vecMulVec (roleLorentzMetric *ᵥ (Λ⁻¹ *ᵥ n))
            (roleLorentzMetric *ᵥ (Λ⁻¹ *ᵥ n)) * Λ⁻¹) := by
    rw [Matrix.mul_smul, Matrix.smul_mul]
  rw [hscale]
  refine congrArg (fun M => -roleLorentzMetric + M) ?_
  refine congrArg (fun M => (2 : ℝ) • M) ?_
  let u : RoleVector := roleLorentzMetric *ᵥ (Λ⁻¹ *ᵥ n)
  have hu : u = (roleLorentzMetric * Λ⁻¹) *ᵥ n := by
    ext i
    simp [u, Matrix.mulVec_mulVec]
  have houter :
      (Λ⁻¹).transpose * Matrix.vecMulVec u u * Λ⁻¹ =
        Matrix.vecMulVec ((Λ⁻¹).transpose *ᵥ u) (u ᵥ* Λ⁻¹) := by
    calc
      (Λ⁻¹).transpose * Matrix.vecMulVec u u * Λ⁻¹ =
          (Λ⁻¹).transpose * (Matrix.vecMulVec u u * Λ⁻¹) := by rw [Matrix.mul_assoc]
      _ = (Λ⁻¹).transpose * Matrix.vecMulVec u (u ᵥ* Λ⁻¹) := by
            rw [Matrix.vecMulVec_mul]
      _ = Matrix.vecMulVec ((Λ⁻¹).transpose *ᵥ u) (u ᵥ* Λ⁻¹) := by
            rw [Matrix.mul_vecMulVec]
  rw [houter]
  have hvec : u ᵥ* Λ⁻¹ = (Λ⁻¹).transpose *ᵥ u :=
    (Matrix.mulVec_transpose Λ⁻¹ u).symm
  rw [hvec]
  have hback : (Λ⁻¹).transpose *ᵥ u = roleLorentzMetric *ᵥ n := by
    rw [hu]
    calc
      (Λ⁻¹).transpose *ᵥ ((roleLorentzMetric * Λ⁻¹) *ᵥ n) =
          ((Λ⁻¹).transpose * (roleLorentzMetric * Λ⁻¹)) *ᵥ n := by
            rw [Matrix.mulVec_mulVec]
      _ = ((Λ⁻¹).transpose * roleLorentzMetric * Λ⁻¹) *ᵥ n := by
            rw [← Matrix.mul_assoc]
      _ = roleLorentzMetric *ᵥ n := by rw [hmet]
  rw [hback]

theorem preservesObserverForm_lorentz (Λ : Matrix Role Role ℝ) (hΛ : IsRoleLorentz Λ)
    (n : RoleVector) :
    preservesObserverForm (lorentzVectorEquiv Λ hΛ) n := by
  have happ : (lorentzVectorEquiv Λ hΛ).toLinearMap = Matrix.toLin' Λ⁻¹ := by
    apply LinearMap.ext
    intro v
    simpa [Matrix.toLin'_apply] using lorentzVectorEquiv_apply Λ hΛ v
  rw [preservesObserverForm, happ, lorentzVectorEquiv_apply, Matrix.toBilin'_comp,
    observerMetric_vector_congruence Λ hΛ n]

end
end D0.Geometry
