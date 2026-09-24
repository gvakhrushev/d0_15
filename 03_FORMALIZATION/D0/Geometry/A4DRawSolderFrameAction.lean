import Mathlib.Tactic
import D0.Geometry.A4DSolderMetricCompletion

/-!
# Raw solder frame action

Raw row/covector and vector conventions for the uncentered solder, local right
Lorentz action, exact centered-frame defect, and transported-center repair.
The raw Nyquist field is kept independently of any centered average.
-/

namespace D0.Geometry

open D0
open scoped BigOperators Matrix

noncomputable section

/-- Uncentered raw solder `E = η + e`. -/
def rawSolderFromPerturbation (e : Matrix Role Role ℝ) : Matrix Role Role ℝ :=
  roleLorentzMetric + e

@[simp] theorem rawSolderFromPerturbation_zero :
    rawSolderFromPerturbation 0 = roleLorentzMetric := by
  simp [rawSolderFromPerturbation]

/-- Right Lorentz action on raw solder rows: `E' = E Λ`. -/
def rawSolderRightAction (E Λ : Matrix Role Role ℝ) : Matrix Role Role ℝ :=
  E * Λ

theorem rawSolder_right_lorentz_preserves_gram (E Λ : Matrix Role Role ℝ)
    (hΛ : IsRoleLorentz Λ) :
    (rawSolderRightAction E Λ) * roleLorentzMetric * (rawSolderRightAction E Λ).transpose =
      E * roleLorentzMetric * E.transpose :=
  solderGram_right_lorentz_invariant E Λ hΛ

/-- Exact centered-frame defect (memo 3.2). -/
theorem centeredFrame_defect_factor (E Eback Λ Λback : Matrix Role Role ℝ) :
    E * Λ + Eback * Λback - (E * Λ + Eback * Λ) = Eback * Λback - Eback * Λ := by
  abel

theorem centeredFrame_defect_factor' (E Eback Λ Λback : Matrix Role Role ℝ) :
    E * Λ + Eback * Λback - (E + Eback) * Λ = Eback * Λback - Eback * Λ := by
  convert centeredFrame_defect_factor E Eback Λ Λback using 1
  simp [Matrix.add_mul]

/-- Equivalent factored form of the defect. -/
theorem centeredFrame_defect_factored (_E Eback Λ Λback : Matrix Role Role ℝ) :
    Eback * Λback - Eback * Λ = Eback * (Λback - Λ) := by
  simp [Matrix.mul_sub]

/-- Transported-center repaired solder. -/
def repairedCenteredSolder (E Eback R : Matrix Role Role ℝ) : Matrix Role Role ℝ :=
  (1 / 2 : ℝ) • (E + Eback * R)

/-- L=2 Nyquist raw edge values. -/
def nyquistVal0 : ℝ := -2
def nyquistVal1 : ℝ := 2

theorem nyquistVals_avg_zero : (nyquistVal0 + nyquistVal1) / 2 = 0 := by
  norm_num [nyquistVal0, nyquistVal1]

theorem nyquistVal0_eq : nyquistVal0 = -2 := rfl

theorem a4d_raw_solder_frame_action_owner :
    (∀ (E Λ : Matrix Role Role ℝ), IsRoleLorentz Λ →
        (rawSolderRightAction E Λ) * roleLorentzMetric *
          (rawSolderRightAction E Λ).transpose = E * roleLorentzMetric * E.transpose) ∧
    (∀ (E Eback Λ Λback : Matrix Role Role ℝ),
        E * Λ + Eback * Λback - (E + Eback) * Λ = Eback * Λback - Eback * Λ) ∧
    (nyquistVal0 = -2) ∧
    ((nyquistVal0 + nyquistVal1) / 2 = 0) :=
  ⟨rawSolder_right_lorentz_preserves_gram, centeredFrame_defect_factor',
    nyquistVal0_eq, nyquistVals_avg_zero⟩

end

end D0.Geometry
