import Mathlib.Tactic
import D0.Geometry.ArchiveAffineCartanConnection
import D0.Geometry.ArchiveExteriorFrameLift
import D0.Core.DyadABCD

/-!
# Reference-junction compression boundary

Lean-owns the exact two-link reference-junction identity (memo §12 / PR #114)
and the precise iff criterion for compressing two conditional edge mismatches
to one endpoint-origin mismatch.

This module does **not** select an intrinsic `q(A,e)`, does not impose
`q₁ = v₂` as a physical law, and does not claim that endpoint compression
holds in general. The mixed-Role flat witness shows why zero edge mismatch
does not imply naive endpoint-origin compression across a mixed labelled
junction.
-/

namespace D0.Geometry

open D0
open AffineCartanMap

/-- Local `LinearOrder Role` for this module only; uniquely named to avoid
collision with `transportedRefMismatchRoleLinearOrder` /
`nilpotentAffineRoleLinearOrder`. -/
local instance referenceJunctionRoleLinearOrder : LinearOrder Role :=
  LinearOrder.lift' roleCode roleCode_injective

set_option linter.unusedSimpArgs false

noncomputable section

variable {K V : Type*} [Field K] [AddCommGroup V] [Module K V]

/-! ## Conditional edge mismatch and junction assembly -/

/-- Conditional edge mismatch `κ = A(q) - v` for a **supplied** reference `q`. -/
def edgeMismatch (A : AffineCartanMap K V) (q v : V) : V :=
  AffineCartanMap.apply A q - v

/-- Semidirect / labelled-path assembly of two edge mismatches. -/
def junctionAssembled (κ1 : V) (L1 : V ≃ₗ[K] V) (κ2 : V) : V :=
  κ1 + L1 κ2

/-! ## 1. Exact junction identity (memo 12.1) -/

/-- Exact two-link reference-junction identity:
`κ₁ + L₁ κ₂ = (A₁ A₂)(q₂) - v₁ + L₁(q₁ - v₂)`. -/
theorem referenceJunctionIdentity
    (A1 A2 : AffineCartanMap K V) (q1 q2 v1 v2 : V) :
    let κ1 := edgeMismatch A1 q1 v1
    let κ2 := edgeMismatch A2 q2 v2
    junctionAssembled κ1 A1.lin κ2 =
      AffineCartanMap.apply (A1 * A2) q2 - v1 + A1.lin (q1 - v2) := by
  simp only [junctionAssembled, edgeMismatch, AffineCartanMap.apply,
    AffineCartanMap.apply_mul, map_sub, AffineCartanMap.mul_lin,
    AffineCartanMap.mul_shift, LinearEquiv.trans_apply, map_add]
  abel

/-- Alias matching the naming suggestion `referenceJunction_eq`. -/
theorem referenceJunction_eq
    (A1 A2 : AffineCartanMap K V) (q1 q2 v1 v2 : V) :
    edgeMismatch A1 q1 v1 + A1.lin (edgeMismatch A2 q2 v2) =
      AffineCartanMap.apply (A1 * A2) q2 - v1 + A1.lin (q1 - v2) :=
  referenceJunctionIdentity A1 A2 q1 q2 v1 v2

/-! ## 2. Telescoping sufficient condition -/

/-- If `q₁ = v₂`, the junction defect vanishes and the edge mismatches telescope
to the single endpoint-origin mismatch `(A₁ A₂)(q₂) - v₁`. -/
theorem referenceJunction_compress_of_eq
    (A1 A2 : AffineCartanMap K V) (q1 q2 v1 v2 : V) (hq : q1 = v2) :
    edgeMismatch A1 q1 v1 + A1.lin (edgeMismatch A2 q2 v2) =
      AffineCartanMap.apply (A1 * A2) q2 - v1 := by
  rw [referenceJunction_eq, hq, sub_self, map_zero, add_zero]

/-! ## 3. Exact iff compression criterion (MAIN BOUNDARY) -/

/-- Because `L₁` is a linear equivalence (hence injective), the assembled
mismatch equals the endpoint-origin mismatch if and only if `q₁ = v₂`.
This is the main compression boundary: the extra junction condition is
necessary as well as sufficient, and is not generic. -/
theorem referenceJunction_compress_iff
    (A1 A2 : AffineCartanMap K V) (q1 q2 v1 v2 : V) :
    edgeMismatch A1 q1 v1 + A1.lin (edgeMismatch A2 q2 v2) =
        AffineCartanMap.apply (A1 * A2) q2 - v1 ↔
      q1 = v2 := by
  constructor
  · intro h
    have hid := referenceJunction_eq A1 A2 q1 q2 v1 v2
    have hsum :
        AffineCartanMap.apply (A1 * A2) q2 - v1 + A1.lin (q1 - v2) =
          AffineCartanMap.apply (A1 * A2) q2 - v1 := by
      rw [← hid, h]
    have hJ : A1.lin (q1 - v2) = 0 := by
      have := congrArg (fun z => z - (AffineCartanMap.apply (A1 * A2) q2 - v1)) hsum
      simpa [add_sub_cancel_left] using this
    exact sub_eq_zero.mp (A1.lin.injective (by simpa using hJ))
  · intro hq
    exact referenceJunction_compress_of_eq A1 A2 q1 q2 v1 v2 hq

/-! ## 4. Mixed-Role flat witness -/

/-- Flat identity affine map on Role-space (the brief's `A₁ = A₂ = 1`). -/
def mixedRoleFlatAffine : AffineCartanMap ℝ RoleSpace := 1

/-- Exact Role-space witness with two distinct Roles `r ≠ s`:
`A₁ = A₂ = 1`, `q₁ = v₁ = e_r`, `q₂ = v₂ = e_s`. -/
structure MixedRoleFlatJunctionWitness where
  r : Role
  s : Role
  hrs : r ≠ s

namespace MixedRoleFlatJunctionWitness

variable (W : MixedRoleFlatJunctionWitness)

/-- `q₁ = e_r`. -/
def q1 : RoleSpace := archiveRoleBasis W.r
/-- `v₁ = e_r`. -/
def v1 : RoleSpace := archiveRoleBasis W.r
/-- `q₂ = e_s`. -/
def q2 : RoleSpace := archiveRoleBasis W.s
/-- `v₂ = e_s`. -/
def v2 : RoleSpace := archiveRoleBasis W.s

theorem κ1_eq_zero :
    edgeMismatch mixedRoleFlatAffine W.q1 W.v1 = 0 := by
  simp [edgeMismatch, mixedRoleFlatAffine, q1, v1, AffineCartanMap.apply,
    AffineCartanMap.one_lin, AffineCartanMap.one_shift, LinearEquiv.refl_apply,
    sub_self]

theorem κ2_eq_zero :
    edgeMismatch mixedRoleFlatAffine W.q2 W.v2 = 0 := by
  simp [edgeMismatch, mixedRoleFlatAffine, q2, v2, AffineCartanMap.apply,
    AffineCartanMap.one_lin, AffineCartanMap.one_shift, LinearEquiv.refl_apply,
    sub_self]

/-- The junction difference `q₁ - v₂ = e_r - e_s` is nonzero. -/
theorem q1_sub_v2_ne_zero : W.q1 - W.v2 ≠ 0 := by
  intro h
  apply_fun (fun z : RoleSpace => z W.r) at h
  simp [q1, v2, archiveRoleBasis, Pi.basisFun_apply, Pi.single_apply, W.hrs,
    Pi.sub_apply] at h

/-- Assembled left-hand side stays zero (both edge mismatches vanish). -/
theorem junctionAssembled_eq_zero :
    junctionAssembled
        (edgeMismatch mixedRoleFlatAffine W.q1 W.v1)
        mixedRoleFlatAffine.lin
        (edgeMismatch mixedRoleFlatAffine W.q2 W.v2) = 0 := by
  simp [junctionAssembled, κ1_eq_zero, κ2_eq_zero, map_zero]

/-- Endpoint-origin term equals `e_s - e_r`. -/
theorem endpoint_term_eq :
    AffineCartanMap.apply (mixedRoleFlatAffine * mixedRoleFlatAffine) W.q2 - W.v1 =
      archiveRoleBasis W.s - archiveRoleBasis W.r := by
  simp [mixedRoleFlatAffine, q2, v1, AffineCartanMap.apply,
    AffineCartanMap.apply_mul, AffineCartanMap.one_lin, AffineCartanMap.one_shift,
    LinearEquiv.refl_apply]

/-- Junction defect equals `e_r - e_s`. -/
theorem junction_defect_eq :
    mixedRoleFlatAffine.lin (W.q1 - W.v2) =
      archiveRoleBasis W.r - archiveRoleBasis W.s := by
  simp [mixedRoleFlatAffine, q1, v2, AffineCartanMap.one_lin,
    LinearEquiv.refl_apply]

/-- Explicit cancellation: endpoint term + junction defect = 0. -/
theorem endpoint_and_junction_cancel :
    (AffineCartanMap.apply (mixedRoleFlatAffine * mixedRoleFlatAffine) W.q2 - W.v1) +
        mixedRoleFlatAffine.lin (W.q1 - W.v2) = 0 := by
  rw [endpoint_term_eq, junction_defect_eq]
  abel

/-- The compression equality fails for this witness (`q₁ ≠ v₂`). -/
theorem compress_condition_fails :
    ¬ (W.q1 = W.v2) := by
  intro h
  exact W.q1_sub_v2_ne_zero (by simp [h])

/-- Packaged firewall demonstration: zero edge mismatches compose to zero via
endpoint/junction cancellation, yet `q₁ = v₂` fails, so naive endpoint-origin
compression does not hold. -/
theorem mixedRoleFlatJunctionWitness_summary :
    edgeMismatch mixedRoleFlatAffine W.q1 W.v1 = 0 ∧
    edgeMismatch mixedRoleFlatAffine W.q2 W.v2 = 0 ∧
    W.q1 - W.v2 ≠ 0 ∧
    (AffineCartanMap.apply (mixedRoleFlatAffine * mixedRoleFlatAffine) W.q2 - W.v1) +
        mixedRoleFlatAffine.lin (W.q1 - W.v2) = 0 ∧
    ¬ (W.q1 = W.v2) ∧
    ¬ (edgeMismatch mixedRoleFlatAffine W.q1 W.v1 +
          mixedRoleFlatAffine.lin (edgeMismatch mixedRoleFlatAffine W.q2 W.v2) =
        AffineCartanMap.apply (mixedRoleFlatAffine * mixedRoleFlatAffine) W.q2 - W.v1) := by
  refine ⟨κ1_eq_zero W, κ2_eq_zero W, q1_sub_v2_ne_zero W,
    endpoint_and_junction_cancel W, compress_condition_fails W, ?_⟩
  intro hcompress
  have hq : W.q1 = W.v2 :=
    (referenceJunction_compress_iff mixedRoleFlatAffine mixedRoleFlatAffine
      W.q1 W.q2 W.v1 W.v2).mp hcompress
  exact compress_condition_fails W hq

end MixedRoleFlatJunctionWitness

/-- Concrete witness with `r = A`, `s = B`. -/
def mixedRoleFlatJunctionWitnessAB : MixedRoleFlatJunctionWitness where
  r := A
  s := B
  hrs := by decide

theorem mixedRoleFlatJunctionWitnessAB_summary :
    edgeMismatch mixedRoleFlatAffine mixedRoleFlatJunctionWitnessAB.q1
        mixedRoleFlatJunctionWitnessAB.v1 = 0 ∧
    edgeMismatch mixedRoleFlatAffine mixedRoleFlatJunctionWitnessAB.q2
        mixedRoleFlatJunctionWitnessAB.v2 = 0 ∧
    mixedRoleFlatJunctionWitnessAB.q1 - mixedRoleFlatJunctionWitnessAB.v2 ≠ 0 ∧
    (AffineCartanMap.apply
        (mixedRoleFlatAffine * mixedRoleFlatAffine)
        mixedRoleFlatJunctionWitnessAB.q2 -
      mixedRoleFlatJunctionWitnessAB.v1) +
        mixedRoleFlatAffine.lin
          (mixedRoleFlatJunctionWitnessAB.q1 - mixedRoleFlatJunctionWitnessAB.v2) = 0 ∧
    ¬ (mixedRoleFlatJunctionWitnessAB.q1 = mixedRoleFlatJunctionWitnessAB.v2) :=
  let ⟨h1, h2, h3, h4, h5, _⟩ :=
    MixedRoleFlatJunctionWitness.mixedRoleFlatJunctionWitness_summary
      mixedRoleFlatJunctionWitnessAB
  ⟨h1, h2, h3, h4, h5⟩

end

end D0.Geometry
