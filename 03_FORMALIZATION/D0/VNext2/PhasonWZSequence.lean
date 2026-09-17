import Mathlib.Tactic
import Mathlib.Analysis.SpecificLimits.Basic
import D0.Core.Phi

/-!
# D0-PHASON-WZ-FINITE-SEQUENCE-SCAFFOLD-001 — the internal pressure/energy ratio sequence

The finite internal archive pressure-energy ratio is `w_n = φ^{n-1} / (φ^n − 1)` on the common window
`n ≥ 1` (energy `R_n`, relative pressure `dR_n`, `D0-IM-COSMO-001/002`). This module owns the two exact
analytic facts the numeric cert checks pointwise:

* **Closed excess form** `w_n = φ⁻¹ + φ⁻¹/(φ^n − 1)` — an exact rearrangement (`φ^{n-1}/(φ^n−1) =
  φ⁻¹·φ^n/(φ^n−1) = φ⁻¹·(1 + 1/(φ^n−1))`).
* **Bounded below by the limit**: `w_n > φ⁻¹` for every `n ≥ 1` (the excess `φ⁻¹/(φ^n−1)` is strictly
  positive because `φ^n > 1`), and the excess is **strictly decreasing** in `n` (because `φ^n − 1` is
  strictly increasing), so `w_n ↓ φ⁻¹` monotonically from above.

The limit `φ⁻¹` is a *positive* internal ratio — NOT the physical dark-energy `w(z) < 0`; the sign/
normalization map to `w_DE` stays the separate PROOF-TARGET `D0-PHASON-WZ-EXPLICIT-FUNCTION-001`.
-/

namespace D0.VNext2.PhasonWZSequence

open D0

/-- The internal pressure/energy ratio `w_n = φ^{n-1}/(φ^n − 1)`. -/
noncomputable def w (n : ℕ) : ℝ := phi ^ (n - 1) / (phi ^ n - 1)

private lemma sqrt5_gt_two : (2 : ℝ) < Real.sqrt 5 := by
  have h : ((2:ℝ))^2 < (Real.sqrt 5)^2 := by rw [sqrt_five_sq]; norm_num
  nlinarith [Real.sqrt_nonneg 5, h]

private lemma phi_gt_one : (1 : ℝ) < phi := by
  unfold phi; nlinarith [sqrt5_gt_two]

private lemma phi_pos : (0 : ℝ) < phi := lt_trans one_pos phi_gt_one

/-- `φ^n > 1` for `n ≥ 1`, hence `φ^n − 1 > 0`. -/
theorem phipow_sub_one_pos {n : ℕ} (hn : 1 ≤ n) : (0 : ℝ) < phi ^ n - 1 := by
  have : (1 : ℝ) < phi ^ n := by
    calc (1:ℝ) = phi ^ 0 := by simp
    _ < phi ^ n := by
        apply pow_lt_pow_right₀ phi_gt_one
        omega
  linarith

/-- **Closed excess form**: `w_n = φ⁻¹ + φ⁻¹/(φ^n − 1)` for `n ≥ 1`. -/
theorem w_excess_form {n : ℕ} (hn : 1 ≤ n) :
    w n = phi⁻¹ + phi⁻¹ / (phi ^ n - 1) := by
  unfold w
  have hp : phi ≠ 0 := ne_of_gt phi_pos
  have hd : phi ^ n - 1 ≠ 0 := ne_of_gt (phipow_sub_one_pos hn)
  -- φ^(n-1) = φ^n / φ  (since n ≥ 1)
  have hpow : phi ^ (n - 1) = phi ^ n / phi := by
    rw [eq_div_iff hp, ← pow_succ]
    congr 1
    omega
  rw [hpow]
  field_simp
  ring

/-- **The sequence stays above its limit**: `w_n > φ⁻¹` for every `n ≥ 1`. -/
theorem w_gt_limit {n : ℕ} (hn : 1 ≤ n) : phi⁻¹ < w n := by
  rw [w_excess_form hn]
  have hpos : (0 : ℝ) < phi⁻¹ / (phi ^ n - 1) :=
    div_pos (inv_pos.mpr phi_pos) (phipow_sub_one_pos hn)
  linarith

/-- **Strictly decreasing**: `w_{n+1} < w_n` for `n ≥ 1`. The excess `φ⁻¹/(φ^n − 1)` shrinks because
    `φ^n − 1` strictly increases. -/
theorem w_strictly_decreasing {n : ℕ} (hn : 1 ≤ n) : w (n + 1) < w n := by
  rw [w_excess_form hn, w_excess_form (by omega : 1 ≤ n + 1)]
  have hpos_n : (0 : ℝ) < phi ^ n - 1 := phipow_sub_one_pos hn
  have hpos_n1 : (0 : ℝ) < phi ^ (n + 1) - 1 := phipow_sub_one_pos (by omega)
  have hlt : phi ^ n - 1 < phi ^ (n + 1) - 1 := by
    have : phi ^ n < phi ^ (n + 1) := by
      apply pow_lt_pow_right₀ phi_gt_one; omega
    linarith
  have hpinv : (0 : ℝ) < phi⁻¹ := inv_pos.mpr phi_pos
  have := div_lt_div_of_pos_left hpinv hpos_n hlt
  linarith

end D0.VNext2.PhasonWZSequence
