import D0.Core.Phi
import Mathlib.Tactic

/-!
# D0-PHASON-ARCHIVE-CAPACITY-REDSHIFT-001 — the redshift map `1+z = φⁿ` and the integer-window
ratio `w_N = φ^(n-1)/(φⁿ-1)` (CERT-CLOSED, narrow)

Python certificate: `05_CERTS/vp_phason_archive_capacity_redshift.py`.

Front F4. The archive-capacity redshift map is `1+z = φⁿ`. On the integer window `n ≥ 1` the internal
archive pressure-energy ratio is
  `w_N = pressure / energy = (φⁿ − φ^(n−1)) / (φⁿ − 1) = φ^(n−1) / (φⁿ − 1)`,
because the pressure increment is `dR_n = R_{n+1} − R_n = φ^(n+1) − φⁿ = φⁿ(φ−1) = φ^(n−1)` and the
energy is `R_n = φⁿ − 1` (these instantiate `D0-IM-COSMO-001/002`, owned elsewhere).

What is proved here (the **narrow** closable scope), with `φ` the real golden ratio `(1+√5)/2`:

* `one_lt_phi` : `1 < φ` (the structural anchor for every monotonicity statement below);
* `redshift_strictMono` : `m < n → φ^m < φ^n` — the redshift map `1+z = φⁿ` is a **strict monotone**
  (hence injective on the integer/rational samples) increasing function; larger `n` ⇒ larger `z`;
* `energy_pos` : `1 ≤ n → 0 < φⁿ − 1` — the energy `R_n` is strictly positive on `n ≥ 1`, so `w_N` is
  **well-defined** there; `n = 0` gives `φ⁰ − 1 = 0` (the **excluded pole**, `energy_zero_at_n0`);
* `dR_closed_form` : `φ^(n+1) − φⁿ = φⁿ * (φ − 1)` and `phi_sub_one_eq_inv : φ − 1 = φ⁻¹`, giving the
  exact `ℚ(φ)` reduction of the pressure increment to `φ^(n−1)`;
* `wN_one_eq_phi` : `w_N 1 = φ` and `wN_two_eq_one : w_N 2 = 1` — the first two exact `ℚ(φ)` values
  (the cert checks all of `n = 1..8` symbolically in `ℤ[φ]`);
* `wN_strictAnti` : `1 ≤ n → w_N (n+1) < w_N n` — `w_N` is **strictly decreasing** in `n` on `n ≥ 1`.

DIRECTION HONESTY (the verdict's load-bearing correction). `w_N → φ⁻¹` is the limit as `n → ∞`, i.e.
`1+z = φⁿ → ∞` ⇒ `z → ∞`, the **EARLY-time** end. It is **NOT** the late-time `z → 0` dark-energy
value. As `n → 0⁺` (`z → 0`) the energy `φⁿ − 1 → 0⁺`, so `w_N` **diverges**; on the integer window the
largest sample is `w_N 1 = φ ≈ 1.618` at the small-`z` end (`z = φ−1`). The theorem
`wN_late_end_exceeds_early_limit` records this: the late-`z` (small-`n`) sample `w_N 1 = φ` is strictly
ABOVE the early-time limit `φ⁻¹`, so the limit cannot be the `z → 0` value.

HONESTY BOUNDARY. This module owns the FINITE-WINDOW facts only (bijection, exact values, monotonicity,
direction). The physical dark-energy reading — a proven continuum interpolation `w_N → w_D0(u)` PLUS the
magnitude/sign normalization map onto the physical NEGATIVE `w_DE` on the late-time window — is NOT
here; it is the PROOF-TARGET `D0-PHASON-WDE-Z-MAP-OWNER-001`. No survey datum (DESI/CPL/H0) enters.
-/

namespace D0.Cosmology

open D0

/-- `1 < φ` : the golden ratio exceeds one. Anchor for every monotonicity fact below. -/
theorem one_lt_phi : (1 : ℝ) < phi := by
  unfold phi
  nlinarith [sqrt_five_sq, Real.sqrt_nonneg 5, Real.sq_sqrt (show (0:ℝ) ≤ 5 by norm_num)]

/-- `0 < φ`. -/
theorem phi_pos : (0 : ℝ) < phi := lt_trans one_pos one_lt_phi

/-- **Redshift map is a strict monotone bijection (on the samples).** `1+z = φⁿ` is strictly
increasing in `n`: `m < n → φ^m < φ^n`. Strict monotonicity gives injectivity of `n ↦ 1+z`. -/
theorem redshift_strictMono {m n : ℕ} (h : m < n) : phi ^ m < phi ^ n :=
  pow_lt_pow_right₀ one_lt_phi h

/-- The energy `R_n = φⁿ − 1` is strictly positive on the integer window `n ≥ 1`, so `w_N` is
well-defined there. -/
theorem energy_pos {n : ℕ} (hn : 1 ≤ n) : (0 : ℝ) < phi ^ n - 1 := by
  have h1 : phi ^ 0 < phi ^ n := redshift_strictMono (lt_of_lt_of_le Nat.zero_lt_one hn)
  rw [pow_zero] at h1
  linarith

/-- The **excluded pole**: at `n = 0` the energy vanishes (`φ⁰ − 1 = 0`), so `w_N` is undefined
there. The well-defined window is `n ≥ 1`. -/
theorem energy_zero_at_n0 : phi ^ (0 : ℕ) - 1 = 0 := by simp

/-- `φ⁻¹ = φ − 1` : the exact `ℚ(φ)` reduction from `φ² = φ + 1`, forced by `φ·(φ−1) = 1`. -/
theorem phi_inv_eq_sub_one : phi⁻¹ = phi - 1 :=
  inv_eq_of_mul_eq_one_right (by linear_combination phi_sq)

/-- `φ − 1 = φ⁻¹`. -/
theorem phi_sub_one_eq_inv : phi - 1 = phi⁻¹ := (phi_inv_eq_sub_one).symm

/-- **Pressure increment, closed form.** `dR_n = R_{n+1} − R_n = φ^(n+1) − φⁿ = φⁿ (φ − 1)`. -/
theorem dR_closed_form (n : ℕ) : phi ^ (n + 1) - phi ^ n = phi ^ n * (phi - 1) := by
  ring

/-- The internal archive window ratio `w_N` on the index `n` (physical sample `m = n + 1 ≥ 1`):
`w_N = φ^m / (φ^(m+1) − 1)`. Indexed by the shift `m = n+1` so the energy `φ^(n+1) − 1` is always on
the well-defined window `n+1 ≥ 1` (the `n = 0` pole is excluded by construction). -/
noncomputable def wN (n : ℕ) : ℝ := phi ^ n / (phi ^ (n + 1) - 1)

/-- **Exact value** `w_N 1 = φ` (physical `m = 1`, the late-`z` window edge `z = φ − 1`). -/
theorem wN_one_eq_phi : wN 0 = phi := by
  unfold wN
  have hpos : (0 : ℝ) < phi ^ (0 + 1) - 1 := energy_pos (by norm_num)
  rw [div_eq_iff (ne_of_gt hpos)]
  have hp1 : phi ^ (0 + 1) = phi := by rw [zero_add, pow_one]
  rw [pow_zero, hp1]
  linear_combination -phi_sq

/-- **Exact value** `w_N 2 = 1` (physical `m = 2`). -/
theorem wN_two_eq_one : wN 1 = 1 := by
  unfold wN
  have hpos : (0 : ℝ) < phi ^ (1 + 1) - 1 := energy_pos (by norm_num)
  rw [div_eq_iff (ne_of_gt hpos)]
  have hp2 : phi ^ (1 + 1) = phi + 1 := by
    have h22 : phi ^ (1 + 1) = phi ^ 2 := by ring
    rw [h22, phi_sq]
  rw [pow_one, hp2]; ring

/-- **`w_N` is strictly DECREASING** in the physical index on `n ≥ 1`:
`w_N (m+1) < w_N m`. Cross-multiplying the two positive-denominator fractions reduces to
`φ^(m−1) < φ^m`, which holds because `φ > 1`. -/
theorem wN_strictAnti (n : ℕ) : wN (n + 1) < wN n := by
  unfold wN
  have hd1 : (0 : ℝ) < phi ^ (n + 1) - 1 := energy_pos (Nat.le_add_left 1 n)
  have hd2 : (0 : ℝ) < phi ^ (n + 1 + 1) - 1 := energy_pos (by omega)
  rw [div_lt_div_iff₀ hd2 hd1]
  -- goal: φ^(n+1) * (φ^(n+1) − 1) < φ^n * (φ^(n+1+1) − 1)
  have hpn : (0 : ℝ) < phi ^ n := pow_pos phi_pos n
  have hq1 : (1 : ℝ) < phi := one_lt_phi
  -- expand the powers so the comparison is purely in `P := φ^n` and `φ`
  have e1 : phi ^ (n + 1) = phi ^ n * phi := by rw [pow_succ]
  have e2 : phi ^ (n + 1 + 1) = phi ^ n * phi * phi := by rw [pow_succ, pow_succ]
  rw [e1, e2]
  -- after expansion: (P·φ)(P·φ−1) < P(P·φ²−1) ⟺ P²φ²−Pφ < P²φ²−P ⟺ P(φ−1) > 0
  have hkey : (0 : ℝ) < phi ^ n * (phi - 1) := mul_pos hpn (by linarith)
  nlinarith [hkey, hpn, hq1, mul_pos hpn hpn]

/-- **DIRECTION fact (limit is `z → ∞`, EARLY, not `z → 0`).** The late-`z` window edge sample
`w_N 1 = φ` is strictly ABOVE the `n → ∞` early-time limit `φ⁻¹`. Hence `φ⁻¹` is the `z → ∞`
(early-time) limit of the DECREASING `w_N`, and cannot be the late-time `z → 0` value. -/
theorem wN_late_end_exceeds_early_limit : phi⁻¹ < wN 0 := by
  rw [wN_one_eq_phi]
  have h : phi⁻¹ < 1 := by
    rw [inv_lt_one_iff₀]; right; exact one_lt_phi
  linarith [one_lt_phi]

/-- **D0-PHASON-ARCHIVE-CAPACITY-REDSHIFT-001 (CERT-CLOSED, narrow).** On the integer window the
redshift map `1+z = φⁿ` is a strict monotone bijection (`redshift_strictMono`); the energy `φⁿ − 1`
is strictly positive for `n ≥ 1` so `w_N` is well-defined (`energy_pos`) while `n = 0` is the excluded
pole; the first exact `ℚ(φ)` values are `w_N 1 = φ`, `w_N 2 = 1`; `w_N` is strictly decreasing
(`wN_strictAnti`); and the limit `φ⁻¹` is the `z → ∞` EARLY-time limit, lying strictly BELOW the
late-`z` window edge `w_N 1 = φ` — it is NOT the late-time `z → 0` dark-energy value. The continuum
interpolation + magnitude/sign normalization onto physical `w_DE` is PROOF-TARGET
(`D0-PHASON-WDE-Z-MAP-OWNER-001`). -/
theorem phason_archive_capacity_redshift :
    (∀ {m n : ℕ}, m < n → phi ^ m < phi ^ n)
      ∧ (∀ {n : ℕ}, 1 ≤ n → (0 : ℝ) < phi ^ n - 1)
      ∧ (phi ^ (0 : ℕ) - 1 = 0)
      ∧ (wN 0 = phi)
      ∧ (wN 1 = 1)
      ∧ (∀ n : ℕ, wN (n + 1) < wN n)
      ∧ (phi⁻¹ < wN 0) :=
  ⟨fun h => redshift_strictMono h, fun h => energy_pos h, energy_zero_at_n0,
   wN_one_eq_phi, wN_two_eq_one, wN_strictAnti, wN_late_end_exceeds_early_limit⟩

end D0.Cosmology
