import Mathlib.NumberTheory.Real.GoldenRatio
import Mathlib.Tactic

/-!
# Lucas-capacity muon/electron ratio: exact algebraic form and interval

Anti-numerology firewall (BOOK_00 §00.9, `D0-BARE-GRAPH-DECIMAL-NOGO-001`): 17-digit decimal
mass coefficients are frozen EFT/IR matching imports and carry status HYP. The *internal*
combinatorial candidate for the charged-lepton ratio is the Lucas-capacity sum

  `m_μ/m_e = L₁₁ + L₄ + 2φ⁻²`,

an element of `ℤ[φ]` with no decimal input. This module proves:

* `lucas 4 = 7`, `lucas 11 = 199` (integer Lucas capacities);
* the exact closed form `L₁₁ + L₄ + 2φ⁻² = 209 − √5` (so the ratio lies in `ℚ(√5)`, degree 2);
* the rigorous interval `206.7639 < 209 − √5 < 206.76394`;
* the defect from the PDG value `206.7682830` lies in `(4.34·10⁻³, 4.36·10⁻³)`.

The last statement is a **falsifiable interval prediction**, not a fit: it has zero adjustable
parameters and is refuted by any measurement placing `m_μ/m_e` outside the stated window
relative to the algebraic value. The `4.35·10⁻³` residual is thereby an exact, owned quantity
(a target for the shell-transfer sector), not a hidden decimal.
-/

namespace D0.Matter.LucasMuonElectronRatio

open Real
open scoped goldenRatio

/-- Integer Lucas numbers `L₀=2, L₁=1, Lₙ₊₂ = Lₙ₊₁ + Lₙ`. -/
def lucas : ℕ → ℤ
  | 0 => 2
  | 1 => 1
  | (n + 2) => lucas (n + 1) + lucas n

theorem lucas_four : lucas 4 = 7 := by decide
theorem lucas_eleven : lucas 11 = 199 := by decide
theorem lucas_five : lucas 5 = 11 := by decide

/-- `φ⁻² = 2 − φ` (from `φ² = φ + 1`). -/
theorem phi_inv_sq : φ⁻¹ ^ 2 = 2 - φ := by
  have h : φ ^ 2 = φ + 1 := goldenRatio_sq
  have hne : φ ≠ 0 := goldenRatio_ne_zero
  have h1 : φ⁻¹ = φ - 1 := by rw [inv_goldenRatio]; ring
  rw [h1]
  linear_combination h

/-- The internal Lucas-capacity charged-lepton ratio. -/
noncomputable def lucasRatio : ℝ := (lucas 11 : ℝ) + (lucas 4 : ℝ) + 2 * φ⁻¹ ^ 2

/-- **Exact closed form:** `L₁₁ + L₄ + 2φ⁻² = 209 − √5`. -/
theorem lucasRatio_eq : lucasRatio = 209 - Real.sqrt 5 := by
  unfold lucasRatio
  rw [lucas_eleven, lucas_four, phi_inv_sq]
  push_cast
  unfold goldenRatio
  ring

private lemma sqrt5_bounds : 2.2360679 < Real.sqrt 5 ∧ Real.sqrt 5 < 2.2360680 := by
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have hnn : 0 ≤ Real.sqrt 5 := Real.sqrt_nonneg 5
  constructor <;> nlinarith [h5, hnn]

/-- **Rigorous interval:** `206.7639 < L₁₁ + L₄ + 2φ⁻² < 206.76394`. -/
theorem lucasRatio_interval : 206.7639 < lucasRatio ∧ lucasRatio < 206.76394 := by
  rw [lucasRatio_eq]
  obtain ⟨h1, h2⟩ := sqrt5_bounds
  constructor <;> linarith

/-- PDG reference value for `m_μ/m_e` (external passport datum, 2024). -/
noncomputable def pdgRatio : ℝ := 206.7682830

/-- **The owned residual:** `pdg − lucasRatio ∈ (4.34·10⁻³, 4.36·10⁻³)`. -/
theorem lucasRatio_pdg_defect :
    0.00434 < pdgRatio - lucasRatio ∧ pdgRatio - lucasRatio < 0.00436 := by
  rw [lucasRatio_eq]; unfold pdgRatio
  obtain ⟨h1, h2⟩ := sqrt5_bounds
  constructor <;> linarith

/-- The ratio is a **degree-2 algebraic number**: it is a root of `x² − 418x + 43676 = 0`. -/
theorem lucasRatio_algebraic : lucasRatio ^ 2 - 418 * lucasRatio + 43676 = 0 := by
  rw [lucasRatio_eq]
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  nlinarith [h5]

/-- **Owner package.** Exact `ℚ(√5)` form, rigorous interval, and owned PDG residual. -/
theorem lucas_muon_electron_owner :
    lucasRatio = 209 - Real.sqrt 5
      ∧ (206.7639 < lucasRatio ∧ lucasRatio < 206.76394)
      ∧ (0.00434 < pdgRatio - lucasRatio ∧ pdgRatio - lucasRatio < 0.00436) :=
  ⟨lucasRatio_eq, lucasRatio_interval, lucasRatio_pdg_defect⟩

end D0.Matter.LucasMuonElectronRatio
