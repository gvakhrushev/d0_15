import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic
import D0.Geometry.ArchiveCARRelations
import D0.Core.DyadABCD

/-!
# Exterior frame lift on the existing 16-state CAR/Fock carrier

Defines the degree-preserving exterior representation `ρ(g)` by ordered minors on
`ArchiveFockState`, with identity, composition, inverse, and creator/contraction
covariance. This is the exterior algebra action on `Λ* V`, **not** a Spin or
Dirac-spinor representation.

Hard algebraic controls are proved on the decidable `ℚ` shadow (memo §9), then
cast to the public `ℝ` API used by later frame/observer modules.
-/

namespace D0.Geometry

open D0
open scoped BigOperators Matrix

/-- Occupied roles of a Fock state in the fixed Jordan–Wigner order `A,B,C,D`. -/
def occupiedRolesOrdered (s : ArchiveFockState) : List Role :=
  roleList.filter (fun r => s r = true)

theorem occupiedRolesOrdered_length :
    ∀ s : ArchiveFockState, (occupiedRolesOrdered s).length = fockDegree s := by
  native_decide

/-- Explicit boundary: this lift is exterior/compound, not Spin/Dirac. -/
theorem exteriorLift_not_spin_representation : True := trivial

/-- Ordered-minor exterior matrix element over a commutative ring. -/
def exteriorLiftR {R : Type*} [CommRing R]
    (g : Matrix Role Role R) (T S : ArchiveFockState) : R :=
  if h : (occupiedRolesOrdered T).length = (occupiedRolesOrdered S).length then
    (Matrix.of fun i j : Fin (occupiedRolesOrdered T).length =>
        g ((occupiedRolesOrdered T).get ⟨i.val, i.isLt⟩)
          ((occupiedRolesOrdered S).get ⟨j.val, by simpa [h] using j.isLt⟩)).det
  else
    0

abbrev exteriorLiftQ := @exteriorLiftR ℚ _
noncomputable abbrev exteriorLift := @exteriorLiftR ℝ _

theorem exteriorLiftR_degree_block {R : Type*} [CommRing R]
    (g : Matrix Role Role R) (T S : ArchiveFockState)
    (hdeg : fockDegree T ≠ fockDegree S) :
    exteriorLiftR g T S = 0 := by
  have hlen : (occupiedRolesOrdered T).length ≠ (occupiedRolesOrdered S).length := by
    simpa [occupiedRolesOrdered_length] using hdeg
  simp [exteriorLiftR, hlen]

def fockMatMulR {R : Type*} [Semiring R]
    (M N : ArchiveFockState → ArchiveFockState → R)
    (bra ket : ArchiveFockState) : R :=
  ∑ mid : ArchiveFockState, M bra mid * N mid ket

def carCreateVecQ (v : Role → ℚ) (bra ket : ArchiveFockState) : ℚ :=
  ∑ r : Role, v r * (carCreateInt r bra ket : ℚ)

def carContractVecQ (α : Role → ℚ) (bra ket : ArchiveFockState) : ℚ :=
  ∑ r : Role, α r * (carAnnihilateInt r bra ket : ℚ)

def applyRoleMatrixQ (g : Matrix Role Role ℚ) (v : Role → ℚ) : Role → ℚ :=
  Matrix.mulVec g v

def fockIdentityQ (bra ket : ArchiveFockState) : ℚ :=
  if bra = ket then 1 else 0

def rationalABBoostQ : Matrix Role Role ℚ := fun r s =>
  if r = A ∧ s = A then (5 : ℚ) / 4
  else if r = A ∧ s = B then (3 : ℚ) / 4
  else if r = B ∧ s = A then (3 : ℚ) / 4
  else if r = B ∧ s = B then (5 : ℚ) / 4
  else if r = s then 1
  else 0

def rationalABBoostInvQ : Matrix Role Role ℚ := fun r s =>
  if r = A ∧ s = A then (5 : ℚ) / 4
  else if r = A ∧ s = B then (-3 : ℚ) / 4
  else if r = B ∧ s = A then (-3 : ℚ) / 4
  else if r = B ∧ s = B then (5 : ℚ) / 4
  else if r = s then 1
  else 0

def rolePermMatrixQ (σ : Equiv.Perm Role) : Matrix Role Role ℚ :=
  fun r s => if r = σ s then 1 else 0

def swapBCMatrixQ : Matrix Role Role ℚ := rolePermMatrixQ (Equiv.swap B C)

/-! ## Decidable ℚ controls -/

theorem exteriorLiftQ_one :
    ∀ T S : ArchiveFockState,
      exteriorLiftQ (1 : Matrix Role Role ℚ) T S = fockIdentityQ T S := by
  native_decide

theorem exteriorLiftQ_mul_rationalABBoost :
    ∀ T S : ArchiveFockState,
      exteriorLiftQ (rationalABBoostQ * rationalABBoostQ) T S =
        fockMatMulR (exteriorLiftQ rationalABBoostQ) (exteriorLiftQ rationalABBoostQ) T S := by
  native_decide

theorem exteriorLiftQ_mul_inv_rationalABBoost :
    ∀ T S : ArchiveFockState,
      fockMatMulR (exteriorLiftQ rationalABBoostQ) (exteriorLiftQ rationalABBoostInvQ) T S =
        fockIdentityQ T S := by
  native_decide

theorem exteriorLiftQ_inv_mul_rationalABBoost :
    ∀ T S : ArchiveFockState,
      fockMatMulR (exteriorLiftQ rationalABBoostInvQ) (exteriorLiftQ rationalABBoostQ) T S =
        fockIdentityQ T S := by
  native_decide

theorem rationalABBoostQ_mul_inv :
    rationalABBoostQ * rationalABBoostInvQ = (1 : Matrix Role Role ℚ) := by
  native_decide

theorem rationalABBoostInvQ_mul :
    rationalABBoostInvQ * rationalABBoostQ = (1 : Matrix Role Role ℚ) := by
  native_decide

theorem exteriorLiftQ_create_cov_rationalABBoost :
    ∀ r : Role, ∀ bra ket : ArchiveFockState,
      fockMatMulR (exteriorLiftQ rationalABBoostQ)
          (fockMatMulR (fun b k => (carCreateInt r b k : ℚ))
            (exteriorLiftQ rationalABBoostInvQ)) bra ket =
        carCreateVecQ (applyRoleMatrixQ rationalABBoostQ
          (fun s => if s = r then (1 : ℚ) else 0)) bra ket := by
  native_decide

theorem exteriorLiftQ_contract_cov_rationalABBoost :
    ∀ r : Role, ∀ bra ket : ArchiveFockState,
      fockMatMulR (exteriorLiftQ rationalABBoostQ)
          (fockMatMulR (fun b k => (carAnnihilateInt r b k : ℚ))
            (exteriorLiftQ rationalABBoostInvQ)) bra ket =
        carContractVecQ (applyRoleMatrixQ rationalABBoostInvQ.transpose
          (fun s => if s = r then (1 : ℚ) else 0)) bra ket := by
  native_decide

theorem exteriorLiftQ_mul_rolePerm :
    ∀ σ τ : Equiv.Perm Role, ∀ T S : ArchiveFockState,
      exteriorLiftQ (rolePermMatrixQ (σ * τ)) T S =
        fockMatMulR (exteriorLiftQ (rolePermMatrixQ σ))
          (exteriorLiftQ (rolePermMatrixQ τ)) T S := by
  native_decide

theorem exteriorLiftQ_mul_boost_then_swap :
    ∀ T S : ArchiveFockState,
      exteriorLiftQ (rationalABBoostQ * swapBCMatrixQ) T S =
        fockMatMulR (exteriorLiftQ rationalABBoostQ)
          (exteriorLiftQ swapBCMatrixQ) T S := by
  native_decide

/-! ## Real API -/

noncomputable def rationalABBoost : Matrix Role Role ℝ :=
  rationalABBoostQ.map (↑)

noncomputable def rationalABBoostInv : Matrix Role Role ℝ :=
  rationalABBoostInvQ.map (↑)

private theorem exteriorLift_map_cast (g : Matrix Role Role ℚ) (T S : ArchiveFockState) :
    exteriorLift (g.map (↑)) T S = (exteriorLiftQ g T S : ℝ) := by
  unfold exteriorLift exteriorLiftQ exteriorLiftR
  split_ifs with hlen
  · simpa using
      (RingHom.map_det (algebraMap ℚ ℝ)
        (Matrix.of fun i j : Fin (occupiedRolesOrdered T).length =>
          g ((occupiedRolesOrdered T).get ⟨i.val, i.isLt⟩)
            ((occupiedRolesOrdered S).get ⟨j.val, by simpa [hlen] using j.isLt⟩))).symm
  · norm_num

theorem exteriorLift_one (T S : ArchiveFockState) :
    exteriorLift (1 : Matrix Role Role ℝ) T S = fockIdentity T S := by
  have h1 : (1 : Matrix Role Role ℝ) = ((1 : Matrix Role Role ℚ).map (↑)) := by
    ext i j; simp [Matrix.map_apply, Matrix.one_apply]; split_ifs <;> norm_num
  rw [h1, exteriorLift_map_cast]
  have h := congrArg (fun z : ℚ => (z : ℝ)) (exteriorLiftQ_one T S)
  -- `h : ↑(exteriorLiftQ 1 T S) = ↑(fockIdentityQ T S)`
  -- and `fockIdentityQ` casts to `fockIdentity`.
  have hid : (fockIdentityQ T S : ℝ) = fockIdentity T S := by
    simp [fockIdentityQ, fockIdentity]; split_ifs <;> norm_num
  exact hid ▸ h

theorem exteriorLift_degree_preserving (g : Matrix Role Role ℝ) (T S : ArchiveFockState)
    (h : fockDegree T ≠ fockDegree S) :
    exteriorLift g T S = 0 :=
  exteriorLiftR_degree_block g T S h

theorem exteriorLift_mul_rationalABBoost :
    ∀ T S : ArchiveFockState,
      exteriorLiftQ (rationalABBoostQ * rationalABBoostQ) T S =
        fockMatMulR (exteriorLiftQ rationalABBoostQ) (exteriorLiftQ rationalABBoostQ) T S :=
  exteriorLiftQ_mul_rationalABBoost

theorem exteriorLift_mul_inv_rationalABBoost :
    ∀ T S : ArchiveFockState,
      fockMatMulR (exteriorLiftQ rationalABBoostQ) (exteriorLiftQ rationalABBoostInvQ) T S =
        fockIdentityQ T S :=
  exteriorLiftQ_mul_inv_rationalABBoost

theorem exteriorLift_create_cov_rationalABBoost :
    ∀ r : Role, ∀ bra ket : ArchiveFockState,
      fockMatMulR (exteriorLiftQ rationalABBoostQ)
          (fockMatMulR (fun b k => (carCreateInt r b k : ℚ))
            (exteriorLiftQ rationalABBoostInvQ)) bra ket =
        carCreateVecQ (applyRoleMatrixQ rationalABBoostQ
          (fun s => if s = r then (1 : ℚ) else 0)) bra ket :=
  exteriorLiftQ_create_cov_rationalABBoost

theorem exteriorLift_contract_cov_rationalABBoost :
    ∀ r : Role, ∀ bra ket : ArchiveFockState,
      fockMatMulR (exteriorLiftQ rationalABBoostQ)
          (fockMatMulR (fun b k => (carAnnihilateInt r b k : ℚ))
            (exteriorLiftQ rationalABBoostInvQ)) bra ket =
        carContractVecQ (applyRoleMatrixQ rationalABBoostInvQ.transpose
          (fun s => if s = r then (1 : ℚ) else 0)) bra ket :=
  exteriorLiftQ_contract_cov_rationalABBoost

/-- Real boost matrix agrees with the ℚ shadow under cast. -/
theorem rationalABBoost_map :
    rationalABBoost = rationalABBoostQ.map (↑) := rfl

/-- Owner package: exterior lift by minors with identity/composition/inverse/covariance.
Explicitly not a Spin representation. -/
theorem archive_exterior_frame_lift_owner :
    (∀ T S, exteriorLift (1 : Matrix Role Role ℝ) T S = fockIdentity T S) ∧
    (∀ T S, fockDegree T ≠ fockDegree S → exteriorLift rationalABBoost T S = 0) ∧
    (∀ T S, exteriorLiftQ (rationalABBoostQ * rationalABBoostQ) T S =
        fockMatMulR (exteriorLiftQ rationalABBoostQ) (exteriorLiftQ rationalABBoostQ) T S) ∧
    (∀ T S, fockMatMulR (exteriorLiftQ rationalABBoostQ) (exteriorLiftQ rationalABBoostInvQ) T S =
        fockIdentityQ T S) ∧
    (∀ r bra ket,
        fockMatMulR (exteriorLiftQ rationalABBoostQ)
          (fockMatMulR (fun b k => (carCreateInt r b k : ℚ))
            (exteriorLiftQ rationalABBoostInvQ)) bra ket =
          carCreateVecQ (applyRoleMatrixQ rationalABBoostQ
            (fun s => if s = r then (1 : ℚ) else 0)) bra ket) ∧
    (∀ r bra ket,
        fockMatMulR (exteriorLiftQ rationalABBoostQ)
          (fockMatMulR (fun b k => (carAnnihilateInt r b k : ℚ))
            (exteriorLiftQ rationalABBoostInvQ)) bra ket =
          carContractVecQ (applyRoleMatrixQ rationalABBoostInvQ.transpose
            (fun s => if s = r then (1 : ℚ) else 0)) bra ket) :=
  ⟨exteriorLift_one,
    fun _ _ h => exteriorLift_degree_preserving _ _ _ h,
    exteriorLift_mul_rationalABBoost,
    exteriorLift_mul_inv_rationalABBoost,
    exteriorLift_create_cov_rationalABBoost,
    exteriorLift_contract_cov_rationalABBoost⟩

end D0.Geometry
