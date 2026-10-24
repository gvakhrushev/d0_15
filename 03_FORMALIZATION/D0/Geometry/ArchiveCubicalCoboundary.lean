import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import D0.Geometry.ArchiveCubicalDifferential
import D0.Geometry.ArchiveCubicalCochainCarrier

namespace D0.Geometry

open D0
open scoped BigOperators

noncomputable section

/-!
# D0.Geometry.ArchiveCubicalCoboundary

Owner: `D0-ARCHIVE-CUBICAL-COBOUNDARY-001`.

This adapter gives the registered cubical coboundary as the unscaled operator
`sum_r (U_r - I) c_r†`.  The already-owned `dForward` implementation uses the
same forward translations with the refinement scale `L = N + 2`; normalizing by
`L` recovers the registered unit-step operator exactly.  Its nilpotency and
degree raising are transferred from the compiled `dForward` theorems, with the
nonzero scale discharged on every refinement.
-/

/-- Number of coboundary direction operators, derived from the role carrier. -/
def coboundaryDirectionCount : ℕ := Fintype.card Role

theorem coboundary_direction_count : coboundaryDirectionCount = 4 := card_role

/-- Exact unscaled cubical coboundary, recovered from the scaled finite operator. -/
def cubicalCoboundary (N : ℕ) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  (forwardDifferenceScale N)⁻¹ • dForward N ψ

/-- Pointwise site-weighted cubical coboundary `sqrt(w) * d`. This generic
operator is kept beside its unweighted source so concrete finite profiles can
reuse the same typed cochain API. -/
noncomputable def weightedCubicalDifferential (N : ℕ)
    (w : ArchiveRolePhaseGroup N → ℝ) (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => Real.sqrt (w p.1) * cubicalCoboundary N ψ p

/-- The scale used by `dForward` is nonzero at every refinement. -/
theorem forwardDifferenceScale_ne_zero (N : ℕ) : forwardDifferenceScale N ≠ 0 := by
  simp only [forwardDifferenceScale, archiveFibers]
  exact_mod_cast (show N + 2 ≠ 0 by omega)

/-- Pointwise construction of `d = sum_r (U_r - I) c_r†`. -/
theorem cubicalCoboundary_apply (N : ℕ) (ψ : ArchiveCochain N)
    (x : ArchiveRolePhaseGroup N) (bra : ArchiveFockState) :
    cubicalCoboundary N ψ (x, bra) =
      ∑ r : Role, ∑ ket : ArchiveFockState,
        carCreate r bra ket *
          (ψ (roleTranslatePlus N r x, ket) - ψ (x, ket)) := by
  classical
  simp only [cubicalCoboundary, Pi.smul_apply, smul_eq_mul,
    dForward, forwardCreateDirection, forwardDifference_apply]
  let L := forwardDifferenceScale N
  let term : Role → ArchiveFockState → ℝ := fun r ket =>
    carCreate r bra ket * (ψ (roleTranslatePlus N r x, ket) - ψ (x, ket))
  have hsum :
      (∑ r : Role, ∑ ket : ArchiveFockState, L * term r ket) =
        L * (∑ r : Role, ∑ ket : ArchiveFockState, term r ket) := by
    calc
      (∑ r : Role, ∑ ket : ArchiveFockState, L * term r ket) =
          ∑ r : Role, L * (∑ ket : ArchiveFockState, term r ket) := by
        apply Finset.sum_congr rfl
        intro r hr
        rw [Finset.mul_sum]
      _ = L * (∑ r : Role, ∑ ket : ArchiveFockState, term r ket) := by
        rw [Finset.mul_sum]
  calc
    L⁻¹ * (∑ r : Role, ∑ ket : ArchiveFockState,
        carCreate r bra ket * (L *
          (ψ (roleTranslatePlus N r x, ket) - ψ (x, ket)))) =
        L⁻¹ * (∑ r : Role, ∑ ket : ArchiveFockState, L * term r ket) := by
          apply congrArg (fun z : ℝ => L⁻¹ * z)
          apply Finset.sum_congr rfl
          intro r hr
          apply Finset.sum_congr rfl
          intro ket hk
          simp only [term]
          ring
    _ = L⁻¹ * (L * (∑ r : Role, ∑ ket : ArchiveFockState, term r ket)) := by
          rw [hsum]
    _ = ∑ r : Role, ∑ ket : ArchiveFockState, term r ket := by
          field_simp [show L ≠ 0 from forwardDifferenceScale_ne_zero N]

/-- Nilpotency stated as a proposition about the actual operator, not a Boolean flag. -/
def CoboundaryNilpotent (N : ℕ) : Prop :=
  ∀ ψ : ArchiveCochain N, cubicalCoboundary N (cubicalCoboundary N ψ) = 0

/-- Scalar multiplication preserves homogeneous cochain degree. -/
theorem homogeneousCochain_smul (N k : ℕ) (c : ℝ) (ψ : ArchiveCochain N)
    (hψ : HomogeneousCochain N k ψ) :
    HomogeneousCochain N k (c • ψ) := by
  intro x S hS
  simp [hψ x S hS]

/-- The unit-step cubical coboundary squares to zero, by transfer from `dForward`. -/
theorem d_squared_eq_zero (N : ℕ) (ψ : ArchiveCochain N) :
    cubicalCoboundary N (cubicalCoboundary N ψ) = 0 := by
  change (forwardDifferenceScale N)⁻¹ •
    dForward N ((forwardDifferenceScale N)⁻¹ • dForward N ψ) = 0
  rw [dForward_smul, dForward_sq_zero]
  simp

/-- The normalized cubical coboundary is linear in its cochain input. -/
theorem cubicalCoboundary_smul (N : ℕ) (c : ℝ) (ψ : ArchiveCochain N) :
    cubicalCoboundary N (c • ψ) = c • cubicalCoboundary N ψ := by
  change (forwardDifferenceScale N)⁻¹ • dForward N (c • ψ) =
    c • ((forwardDifferenceScale N)⁻¹ • dForward N ψ)
  calc
    _ = ((forwardDifferenceScale N)⁻¹ * c) • dForward N ψ := by
      rw [dForward_smul, smul_smul]
    _ = (c * (forwardDifferenceScale N)⁻¹) • dForward N ψ := by
      rw [mul_comm]
    _ = _ := by rw [smul_smul]

/-- A constant site profile scales the coboundary by one scalar, so its square
still vanishes at every refinement. -/
theorem weightedCubicalDifferential_constant_square_zero (N : ℕ) (a : ℝ)
    (ψ : ArchiveCochain N) :
    weightedCubicalDifferential N (fun _ => a)
      (weightedCubicalDifferential N (fun _ => a) ψ) = 0 := by
  have hinner :
      weightedCubicalDifferential N (fun _ => a) ψ =
        (Real.sqrt a) • cubicalCoboundary N ψ := by
    funext p
    rfl
  change (fun p => Real.sqrt a *
      cubicalCoboundary N
        (weightedCubicalDifferential N (fun _ => a) ψ) p) = 0
  rw [hinner, cubicalCoboundary_smul, d_squared_eq_zero]
  funext p
  simp

/-- The unit-step cubical coboundary raises homogeneous Fock degree by one. -/
theorem cubicalCoboundary_degree_raise (N k : ℕ) (ψ : ArchiveCochain N)
    (hψ : HomogeneousCochain N k ψ) :
    HomogeneousCochain N (k + 1) (cubicalCoboundary N ψ) := by
  exact homogeneousCochain_smul N (k + 1) (forwardDifferenceScale N)⁻¹
    (dForward N ψ) (dForward_degree_raise N k ψ hψ)

/-- **D0-ARCHIVE-CUBICAL-COBOUNDARY-001 (Owner)**:
The concrete unit-step operator has four directions, a 16-state cubical fiber,
`d² = 0`, and maps degree `k` to degree `k + 1`. -/
theorem archive_cubical_coboundary_owner :
    (coboundaryDirectionCount = 4) ∧
    (Fintype.card CubicalCellType = 16) ∧
    (∀ N : ℕ, CoboundaryNilpotent N) ∧
    (∀ N k (ψ : ArchiveCochain N), HomogeneousCochain N k ψ →
      HomogeneousCochain N (k + 1) (cubicalCoboundary N ψ)) := by
  refine ⟨coboundary_direction_count, card_archive_fock_state, ?_, ?_⟩
  · intro N ψ
    exact d_squared_eq_zero N ψ
  · intro N k ψ hψ
    exact cubicalCoboundary_degree_raise N k ψ hψ

end

end D0.Geometry
