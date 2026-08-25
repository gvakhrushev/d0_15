import Mathlib.NumberTheory.Real.GoldenRatio
import D0.Dynamics.ToralAutomorphism
import D0.Synthesis.LefschetzZoneExclusion

/-!
# The toral composition law for the depth exponent 17 = 5 + 12

**Target context (obligation (i), row `D0-ALPHA-SEAM-FORM-FORCED-001`).** The registered total
(hypothesis (γ) of `SeamCrossingWeightForced`) is `φ⁻¹⁷ = ξ₅·φ⁻¹²`, graded "owned only as prose".
Until now the composition's only Lean content was exponent arithmetic (`seventeen_ticks`,
`pow_add`) and a `native_decide` trace value (`trace_T17`, excluded from the endgame assembly).
This module upgrades the LEAD — "17 has a toral address" — to a toral composition LAW, with
clean axioms throughout (no `native_decide`):

1. **Return-defect addresses for BOTH factors.** The real-level defect identity is OWNED:
   `D0-LUCAS-DEFECT-SIGN-001` (`LucasDefectSign.lucas_defect`, THE) carries
   `φⁿ − lucasR n = (−1)^{n+1}(φⁿ)⁻¹` with `lucasR n = φⁿ + ψⁿ`. NEW here is the
   **integer bridge**: `lucas_gold : (lucas n : ℝ) = φⁿ + (1−φ)ⁿ` ties the recursive integer
   `D0.Dynamics.lucas` to that closed form (LucasDefectSign never identifies `lucasR` with an
   integer), giving `golden_return_defect : (φ⁻¹)ⁿ = (−1)ⁿ(Lₙ − φⁿ)` over the REGISTRY's own
   Lucas object, and the numeral instantiations:
   * `ξ₅ = φ⁻⁵ = φ⁵ − 11` — the seam-factor address (integer level owned at
     `D0-XI5-TORUS-DEFECT-001`; real level at `D0-LUCAS-DEFECT-SIGN-001`; here the two are
     joined clean), and
   * `φ⁻¹² = 322 − φ¹² = L₁₂ − φ¹²` — the numeral-instantiated twelfth-return address for
     the OPEN transport factor: the same defect shape as the seam factor
     (`transport_factor_toral_address`; the instantiation and the integer bridge are the new
     content, not the identity shape).
2. **The composition as a return law, not exponent arithmetic.** The Lucas composition law
   `L_{m+n} = L_m·L_n − (−1)ⁿ·L_{m−n}` (`lucas_composition`, proved through the golden closed
   form, no induction on the identity itself) transports to the toral traces through the owned
   dictionary `Tr(Tᵏ) = (−1)ᵏLₖ` (`trace_T_pow_clean`): for `n ≤ m`,
   `Tr(T^{m+n}) = Tr(T^m)·Tr(T^n) − (det T)ⁿ·Tr(T^{m−n})` (`trace_return_composition`).
   At the depth split `(m,n) = (12,5)`: `Tr(T¹⁷) = Tr(T¹²)·Tr(T⁵) − (det T)⁵·Tr(T⁷)`, i.e.
   `L₁₇ = L₁₂·L₅ + L₇` (`3571 = 322·11 + 29`): the seventeenth return factors through the
   fifth and twelfth returns, and the correction `+L₇` is FORCED by the orientation reversal
   of the odd return (`det T⁵ = −1`, `fifth_return_orientation`). This also re-derives
   `Tr(T¹⁷) = −3571` cleanly (`trace_T17_clean`), removing the endgame's need for the
   `ofReduceBool`-carrying `trace_T17`.
3. **The registered total in toral addresses.** `φ⁻¹⁷ = (φ⁵ − 11)·(322 − φ¹²)`
   (`registered_total_toral_form`): both factors of (γ)'s form are return defects of the SAME
   toral automorphism, at the returns 5 and 12, composing to the 17-defect.

**Honest scope (kill-shape guarded).** This module does NOT own (γ). The identification
"seam depth = contracting-eigenvalue composition at the toral returns 5 and 12" remains the
open content of `PRIM-SEAM-CROSSING-TICK-IDENTIFICATION`; everything here is unconditional
mathematics of the toral side only. The return INDEX 12 is not bound to any dim-12 carrier
(door 1 `dim g_light`, door 2 `|V₁₁|+1`, door 5 commutant — all untouched; binding a return
index to a carrier dimension via the shared numeral 12 would be exactly the carrier-mismatch
trap). What changes for the obligation, SCOPED TO THE TORAL (door-2-adjacent) ROUTE: the
transport factor `φ⁻¹²`, previously located only by the prose word "electroweak", now has an
owned toral-address FORM, and the composition has an owned toral LAW — on THAT route the
missing step narrows to identifying the seam transport with the twelfth toral return, a
sharpened primitive, not a discharged one. Door 1 (`dim g_light`) remains the live rival
(row `D0-TRANSPORT-FORK-ENDGAME-001` phrasing): a door-1 discharge would own the transport
factor with no seam-return identification at all — the obligation's missing step over ALL
routes does not narrow here.
-/

namespace D0.Synthesis.ToralCompositionSeventeen

open Real
open scoped goldenRatio
open D0.Dynamics
open D0.Synthesis.LefschetzZoneExclusion

/-! ## Layer 1 — the Lucas–golden closed form and the return-defect addresses -/

/-- `φ⁻¹ = φ − 1` (the golden quadratic, inverse form). -/
theorem phi_inv_eq_phi_sub_one : φ⁻¹ = φ - 1 :=
  inv_eq_of_mul_eq_one_right (by linear_combination goldenRatio_sq)

/-- The conjugate root `1 − φ` satisfies the same recurrence quadratic. -/
theorem conj_sq : (1 - φ) ^ 2 = (1 - φ) + 1 := by
  nlinarith [goldenRatio_sq]

/-- The golden–conjugate product: `φ·(1−φ) = −1`. -/
theorem gold_mul_conj : φ * (1 - φ) = -1 := by
  linear_combination -goldenRatio_sq

/-- Lucas–golden closed form: `Lₙ = φⁿ + (1−φ)ⁿ`, clean two-step induction. -/
theorem lucas_gold : ∀ n : ℕ, (lucas n : ℝ) = φ ^ n + (1 - φ) ^ n := by
  have step : ∀ x : ℝ, x ^ 2 = x + 1 → ∀ k : ℕ, x ^ (k + 2) = x ^ (k + 1) + x ^ k := by
    intro x hx k
    calc x ^ (k + 2) = x ^ k * x ^ 2 := by ring
    _ = x ^ k * (x + 1) := by rw [hx]
    _ = x ^ (k + 1) + x ^ k := by ring
  intro n
  induction n using Nat.twoStepInduction with
  | zero => norm_num [lucas]
  | one => norm_num [lucas]
  | more n ih1 ih2 =>
    have hl : lucas (n + 2) = lucas (n + 1) + lucas n := rfl
    rw [hl, step φ goldenRatio_sq n, step (1 - φ) conj_sq n]
    push_cast
    rw [ih1, ih2]
    ring

/-- **The general return-defect address**: `(φ⁻¹)ⁿ = (−1)ⁿ·(Lₙ − φⁿ)`. -/
theorem golden_return_defect (n : ℕ) :
    (φ⁻¹) ^ n = (-1 : ℝ) ^ n * ((lucas n : ℝ) - φ ^ n) := by
  have hconj : (1 - φ : ℝ) = -φ⁻¹ := by rw [phi_inv_eq_phi_sub_one]; ring
  have h := lucas_gold n
  rw [hconj] at h
  have hpow : (-φ⁻¹ : ℝ) ^ n = (-1) ^ n * (φ⁻¹) ^ n := by
    rw [neg_pow]
  have hsq : ((-1 : ℝ)) ^ n * ((-1 : ℝ)) ^ n = 1 := by
    rw [← mul_pow]; norm_num
  calc (φ⁻¹) ^ n = ((-1 : ℝ)) ^ n * ((-1 : ℝ)) ^ n * (φ⁻¹) ^ n := by rw [hsq, one_mul]
  _ = (-1 : ℝ) ^ n * ((-1) ^ n * (φ⁻¹) ^ n) := by ring
  _ = (-1 : ℝ) ^ n * ((lucas n : ℝ) - φ ^ n) := by
      rw [← hpow]
      congr 1
      linarith [h]

/-- The seam factor's owned address, re-derived clean at the real level:
`ξ₅ = φ⁻⁵ = φ⁵ − 11` (`L₅ = 11`, the `D0-XI5-TORUS-DEFECT-001` object). -/
theorem seam_factor_toral_address : (φ⁻¹) ^ 5 = φ ^ 5 - 11 := by
  have h := golden_return_defect 5
  have hl : lucas 5 = 11 := by norm_num [lucas]
  rw [hl] at h
  push_cast at h
  linarith [h]

/-- **NEW address for the OPEN transport factor**: `φ⁻¹² = 322 − φ¹² = L₁₂ − φ¹²` —
the same defect shape as the seam factor, at the twelfth return. -/
theorem transport_factor_toral_address : (φ⁻¹) ^ 12 = 322 - φ ^ 12 := by
  have h := golden_return_defect 12
  have hl : lucas 12 = 322 := by norm_num [lucas]
  rw [hl] at h
  push_cast at h
  linarith [h]

/-- The composed 17-defect: `φ⁻¹⁷ = φ¹⁷ − 3571 = φ¹⁷ − L₁₇`. -/
theorem composed_defect_seventeen : (φ⁻¹) ^ 17 = φ ^ 17 - 3571 := by
  have h := golden_return_defect 17
  have hl : lucas 17 = 3571 := by norm_num [lucas]
  rw [hl] at h
  push_cast at h
  linarith [h]

/-- **The registered total in toral addresses**: `φ⁻¹⁷ = (φ⁵ − 11)·(322 − φ¹²)` — both
factors of (γ)'s form are return defects of the same toral automorphism. -/
theorem registered_total_toral_form :
    (φ⁻¹) ^ 17 = (φ ^ 5 - 11) * (322 - φ ^ 12) := by
  rw [← seam_factor_toral_address, ← transport_factor_toral_address, ← pow_add]

/-! ## Layer 2 — the Lucas composition law and its toral-trace transport -/

/-- **The Lucas composition law**: for `n ≤ m`, `L_{m+n} = L_m·L_n − (−1)ⁿ·L_{m−n}`.
Proved through the golden closed form — no induction on the identity itself. -/
theorem lucas_composition {m n : ℕ} (h : n ≤ m) :
    lucas (m + n) = lucas m * lucas n - (-1 : ℤ) ^ n * lucas (m - n) := by
  have key : ((lucas (m + n) : ℝ)) =
      (lucas m : ℝ) * (lucas n : ℝ) - (-1 : ℝ) ^ n * (lucas (m - n) : ℝ) := by
    have hm : φ ^ (m - n) * φ ^ n = φ ^ m := by
      rw [← pow_add]; congr 1; omega
    have hc : (1 - φ) ^ (m - n) * (1 - φ) ^ n = (1 - φ) ^ m := by
      rw [← pow_add]; congr 1; omega
    have hmn : φ ^ (m + n) = φ ^ m * φ ^ n := pow_add φ m n
    have hcn : (1 - φ) ^ (m + n) = (1 - φ) ^ m * (1 - φ) ^ n := pow_add (1 - φ) m n
    have hprod : ((-1 : ℝ)) ^ n = φ ^ n * (1 - φ) ^ n := by
      rw [← mul_pow, gold_mul_conj]
    rw [lucas_gold, lucas_gold, lucas_gold, lucas_gold, hmn, hcn, hprod]
    linear_combination ((1 - φ) ^ n) * hm + (φ ^ n) * hc
  exact_mod_cast key

/-- The Lucas composition transported to the toral traces through the owned dictionary
`Tr(Tᵏ) = (−1)ᵏLₖ`: for `n ≤ m`,
`Tr(T^{m+n}) = Tr(T^m)·Tr(T^n) − (det T)ⁿ·Tr(T^{m−n})`. -/
theorem trace_return_composition {m n : ℕ} (h : n ≤ m) :
    Matrix.trace (T ^ (m + n)) =
      Matrix.trace (T ^ m) * Matrix.trace (T ^ n)
        - (Matrix.det T) ^ n * Matrix.trace (T ^ (m - n)) := by
  rw [trace_T_pow_clean, trace_T_pow_clean, trace_T_pow_clean, trace_T_pow_clean, detT_clean]
  unfold signedLucasTrace
  have hcomp := lucas_composition h
  have hsplit : ((-1 : ℤ)) ^ m = (-1) ^ (m - n) * (-1) ^ n := by
    rw [← pow_add]; congr 1; omega
  have hadd : ((-1 : ℤ)) ^ (m + n) = (-1) ^ m * (-1) ^ n := by
    rw [pow_add]
  rw [hadd, hcomp]
  have hnn : ((-1 : ℤ)) ^ n * (-1) ^ n = 1 := by
    rw [← mul_pow]; norm_num
  calc ((-1 : ℤ)) ^ m * (-1) ^ n * (lucas m * lucas n - (-1) ^ n * lucas (m - n))
      = ((-1) ^ m * lucas m) * ((-1) ^ n * lucas n)
        - (-1) ^ m * ((-1) ^ n * (-1) ^ n) * lucas (m - n) := by ring
  _ = ((-1) ^ m * lucas m) * ((-1) ^ n * lucas n)
        - ((-1) ^ (m - n) * (-1) ^ n) * lucas (m - n) := by rw [hnn, hsplit]; ring
  _ = ((-1) ^ m * lucas m) * ((-1) ^ n * lucas n)
        - (-1) ^ n * ((-1) ^ (m - n) * lucas (m - n)) := by ring

/-- The instance at the depth split `(m, n) = (12, 5)`:
`Tr(T¹⁷) = Tr(T¹²)·Tr(T⁵) − (det T)⁵·Tr(T⁷)` — the seventeenth return factors through the
fifth and twelfth returns. -/
theorem seventeenth_return_composition :
    Matrix.trace (T ^ 17) =
      Matrix.trace (T ^ 12) * Matrix.trace (T ^ 5)
        - (Matrix.det T) ^ 5 * Matrix.trace (T ^ 7) := by
  have h := trace_return_composition (show 5 ≤ 12 by norm_num)
  norm_num at h
  exact h

/-- Clean re-derivation of the seventeenth trace (replaces the `native_decide` route of
`TransportForkEndgame.trace_T17` for downstream use): `Tr(T¹⁷) = −L₁₇ = −3571`. -/
theorem trace_T17_clean : Matrix.trace (T ^ 17) = -3571 := by
  rw [trace_T_pow_clean 17]
  unfold signedLucasTrace
  norm_num [lucas]

/-- The Lucas composition with the forced correction: `L₁₇ = L₁₂·L₅ + L₇`
(`3571 = 322·11 + 29`), the `+L₇` term pinned by the odd return's orientation reversal. -/
theorem lucas_seventeen_composition : lucas 17 = lucas 12 * lucas 5 + lucas 7 := by
  norm_num [lucas]

/-- The orientation reversal that forces the correction sign: `(det T)⁵ = −1`
(the fifth return is orientation-reversing). -/
theorem fifth_return_orientation : (Matrix.det T) ^ 5 = -1 := by
  rw [detT_clean]
  norm_num

/-! ## Assembly -/

/-- **The toral composition law for 17 = 5 + 12** (assembly, clean axioms):
the seventeenth return factors through the fifth and twelfth returns with the `+L₇`
correction forced by `det T⁵ = −1`; the registered total `φ⁻¹⁷ = ξ₅·φ⁻¹²` is expressed with
BOTH factors as toral return defects. Unconditional toral-side mathematics; (γ) not owned. -/
theorem toral_composition_seventeen :
    Matrix.trace (T ^ 17) =
        Matrix.trace (T ^ 12) * Matrix.trace (T ^ 5)
          - (Matrix.det T) ^ 5 * Matrix.trace (T ^ 7)
      ∧ lucas 17 = lucas 12 * lucas 5 + lucas 7
      ∧ (Matrix.det T) ^ 5 = -1
      ∧ (φ⁻¹) ^ 17 = (φ ^ 5 - 11) * (322 - φ ^ 12) :=
  ⟨seventeenth_return_composition, lucas_seventeen_composition,
    fifth_return_orientation, registered_total_toral_form⟩

end D0.Synthesis.ToralCompositionSeventeen
