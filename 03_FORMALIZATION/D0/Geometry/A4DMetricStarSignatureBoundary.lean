import Mathlib.Tactic
import D0.Geometry.ArchiveExteriorFrameLift
import D0.Geometry.A4DSolderMetricCompletion
import D0.Geometry.A4DPrimalDualCellPairing
import D0.Geometry.A4DLocatedTopologicalStar
import D0.Geometry.A4DRawSolderFrameAction

/-!
# Metric-star / signature boundary

Common-fiber Lorentz metric-star boundary theorems. This is a signature/pointwise
boundary package, not the physical located star `J`.
-/

namespace D0.Geometry

open D0
open scoped BigOperators Matrix

noncomputable section

abbrev flatLorentzMetric : Matrix Role Role ℝ := roleLorentzMetric

/-- Compound/Jacobi control on the rational boost: `det(g) = 1` and the top
exterior minor equals `det g`. -/
theorem jacobi_complement_det_control :
    Matrix.det rationalABBoostQ = 1 ∧
    exteriorLiftQ rationalABBoostQ (fun _ => true) (fun _ => true) = 1 := by
  native_decide

abbrev exteriorOrientation (S : ArchiveFockState) : ℝ := complementOrientation S

def flatLorentzStarCoeff (S : ArchiveFockState) : ℝ :=
  exteriorOrientation S *
    ∏ r : Role, if S r then roleLorentzSign r else 1

theorem flatLorentzStarCoeff_vacuum :
    flatLorentzStarCoeff fockVacuumState = complementOrientation fockVacuumState := by
  simp [flatLorentzStarCoeff, fockVacuumState]

def lorentzDoubleStarSign (k : ℕ) : ℤ :=
  if (k * (4 - k) + 3) % 2 = 0 then 1 else -1

theorem lorentzDoubleStarSign_values :
    lorentzDoubleStarSign 0 = -1 ∧ lorentzDoubleStarSign 1 = 1 ∧
    lorentzDoubleStarSign 2 = -1 ∧ lorentzDoubleStarSign 3 = 1 ∧
    lorentzDoubleStarSign 4 = -1 := by
  native_decide

theorem lorentzDoubleStarSign_eq_koszul_times_neg (k : ℕ) (hk : k ≤ 4) :
    (lorentzDoubleStarSign k : ℝ) = koszulDegreeSign k * (-1 : ℝ) := by
  interval_cases k <;> simp [lorentzDoubleStarSign, koszulDegreeSign]

theorem degree_one_flat_metric_is_eta_not_counting :
    flatLorentzMetric A A = 1 ∧ flatLorentzMetric B B = -1 ∧
    (1 : Matrix Role Role ℝ) B B = 1 :=
  ⟨roleLorentzSign_A, roleLorentzSign_B, rfl⟩

theorem flat_metric_ne_counting_on_B :
    flatLorentzMetric B B ≠ (1 : ℝ) := by
  simp [flatLorentzMetric, roleLorentzSign_B]
  norm_num

def pointwiseCoeffOperator (N : ℕ) (m : ArchiveRolePhaseGroup N → ℝ)
    (ψ : ArchiveCochain N) : ArchiveCochain N :=
  fun p => m p.1 * ψ p

theorem pointwise_coeff_constant_factor (N : ℕ) (c : ℝ) (ψ : ArchiveCochain N) :
    pointwiseCoeffOperator N (fun _ => c) ψ = fun p => c * ψ p := rfl

theorem centered_solder_blind_to_L2_Nyquist :
    ((nyquistVal0 + nyquistVal1) / 2 = 0) ∧ (nyquistVal0 = -2) :=
  ⟨nyquistVals_avg_zero, nyquistVal0_eq⟩

theorem a4d_metric_star_signature_boundary_owner :
    (lorentzDoubleStarSign 0 = -1) ∧
    (flatLorentzMetric A A = 1 ∧ flatLorentzMetric B B = -1) ∧
    flatLorentzMetric B B ≠ (1 : ℝ) ∧
    ((nyquistVal0 + nyquistVal1) / 2 = 0) ∧
    (Matrix.det rationalABBoostQ = 1) ∧
    (exteriorLiftQ rationalABBoostQ (fun _ => true) (fun _ => true) = 1) :=
  ⟨lorentzDoubleStarSign_values.1,
    ⟨roleLorentzSign_A, roleLorentzSign_B⟩,
    flat_metric_ne_counting_on_B,
    nyquistVals_avg_zero,
    jacobi_complement_det_control.1,
    jacobi_complement_det_control.2⟩

end

end D0.Geometry
