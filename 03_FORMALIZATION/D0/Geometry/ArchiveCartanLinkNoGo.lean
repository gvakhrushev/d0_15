import Mathlib.Tactic
import D0.Geometry.A4DCenteredCartanClosureNoGo
import D0.Geometry.ArchiveCARRelations
import D0.Geometry.ArchiveChainCurvature
import D0.Geometry.RoleFockPermutation

/-!
# Scoped Cartan / link no-gos

Three exact negative controls.

1. On the five-cycle, conjugation of the unit link by `G_{δ_0}` has entry
   `(0,2) = 5/2`. Every elementary one-link tangent misses that entry.
   This does not forbid every possible connection.

2. Ordinary repeated-direction plaquette curvature is identically zero, while
   the owned centered-generator commutator has entry `25/4`. The centered
   defect is not that flat-vanishing plaquette curvature.

3. Commuting diagonal frames `diag(1,2,7,1)` and `diag(3,5,11,1)` have
   vanishing frame commutator. The frozen-creator operator on the same Fock
   space still has square entry `-62` on `|C⟩ → |ABC⟩`. Frame flatness does
   not repair frozen creators.
-/

namespace D0.Geometry

open D0
open RoleFockPermutation

noncomputable section

def unitShift5 (f : Cycle5Scalar) : Cycle5Scalar :=
  fun i => f (cycle5Next i)

def centeredLinkConjugation5 (f : Cycle5Scalar) : Cycle5Scalar :=
  centeredGenerator5 xiWitness5 (unitShift5 f) -
    unitShift5 (centeredGenerator5 xiWitness5 f)

/-- `[G_{δ_0}, U]_{0,2} = 5/2` for the unit shift on the five-cycle. -/
theorem centered_conjugation_distance_two_entry :
    centeredLinkConjugation5 distanceTwoBasis5 0 = (5 / 2 : ℚ) := by
  native_decide

/-- Tangent to multiplying one forward link by a site coefficient. -/
def elementaryLinkTangent (a : Cycle5Scalar) (f : Cycle5Scalar) : Cycle5Scalar :=
  fun i => a i * f (cycle5Next i)

theorem elementaryLinkTangent_misses_distance_two (a : Cycle5Scalar) :
    elementaryLinkTangent a distanceTwoBasis5 0 = 0 := by
  simp [elementaryLinkTangent, distanceTwoBasis5, delta5, cycle5Next]

/-- The centered conjugation direction is not tangent to the elementary link family. -/
theorem centered_conjugation_not_elementary_link_tangent :
    ∀ a : Cycle5Scalar, elementaryLinkTangent a ≠ centeredLinkConjugation5 := by
  intro a h
  have hentry := congrFun (congrFun h distanceTwoBasis5) (0 : Fin 5)
  rw [centered_conjugation_distance_two_entry,
    elementaryLinkTangent_misses_distance_two] at hentry
  norm_num at hentry

/-- A repeated role has only one square, so its open-path defect vanishes. -/
theorem single_direction_curvature_zero {N : ℕ} {K V : Type*} [Field K]
    [AddCommGroup V] [Module K V]
    (U : LinkConnection N K V) (r : Role) (x : ArchiveRolePhaseGroup N) :
    openCurvature U r r x = 0 := by
  ext v
  simp [openCurvature, squarePathA, squarePathB]

/-- Unit links are flat, and the one-role centered defect is still nonzero. -/
theorem flat_wilson_curvature_cannot_equal_centered_defect :
    (∀ (N : ℕ) (r s : Role) (x : ArchiveRolePhaseGroup N),
      openCurvature (trivialLink N ℚ ℚ) r s x = 0) ∧
    centeredGeneratorCommutator5 xiWitness5 etaWitness5 distanceTwoBasis5 0 ≠ 0 ∧
    (∀ (U : LinkConnection 3 ℚ ℚ) (r : Role) (x : ArchiveRolePhaseGroup 3),
      openCurvature U r r x = 0) := by
  refine ⟨?_, ?_, ?_⟩
  · intro N r s x
    exact trivialLink_curvature_zero r s x
  · rw [centered_commutator_distance_two_entry]
    norm_num
  · intro U r x
    exact single_direction_curvature_zero U r x

/-! ## Same-Fock frozen creators -/

def diagWeight (w : Role → ℤ) (s : ArchiveFockState) : ℤ :=
  ∏ r : Role, if s r = true then w r else 1

def diagFrame (w : Role → ℤ) (bra ket : ArchiveFockState) : ℤ :=
  if bra = ket then diagWeight w bra else 0

def frameG0 : Role → ℤ :=
  fun r => if r = A then 1 else if r = B then 2 else if r = C then 7 else 1

def frameG1 : Role → ℤ :=
  fun r => if r = A then 3 else if r = B then 5 else if r = C then 11 else 1

theorem diagFrame_commute (w z : Role → ℤ) (bra ket : ArchiveFockState) :
    fockMatMul (diagFrame w) (diagFrame z) bra ket =
      fockMatMul (diagFrame z) (diagFrame w) bra ket := by
  classical
  unfold fockMatMul diagFrame
  by_cases h : bra = ket
  · simp [h, diagWeight]
    ring
  · simp [h]

def sameFockShift (w : Role → ℤ) (bra ket : ArchiveFockState) : ℤ :=
  diagFrame w bra ket - fockIdentityInt bra ket

def sameFockDirection (w : Role → ℤ) (r : Role) (bra ket : ArchiveFockState) : ℤ :=
  fockMatMul (carCreateInt r) (sameFockShift w) bra ket

def sameFockNaiveSquare (bra ket : ArchiveFockState) : ℤ :=
  fockMatMul
    (fun b k => sameFockDirection frameG0 A b k + sameFockDirection frameG1 B b k)
    (fun b k => sameFockDirection frameG0 A b k + sameFockDirection frameG1 B b k)
    bra ket

def stateRoleC : ArchiveFockState := fun r => r = C

def stateABC : ArchiveFockState := fun r => r = A ∨ r = B ∨ r = C

/-- Frozen creators on commuting diagonal frames: the square entry is `-62`. -/
theorem sameFock_flat_links_square_entry :
    sameFockNaiveSquare stateABC stateRoleC = -62 := by
  native_decide

theorem sameFock_flat_frames_commute (bra ket : ArchiveFockState) :
    fockMatMul (diagFrame frameG0) (diagFrame frameG1) bra ket =
      fockMatMul (diagFrame frameG1) (diagFrame frameG0) bra ket :=
  diagFrame_commute frameG0 frameG1 bra ket

end

end D0.Geometry
