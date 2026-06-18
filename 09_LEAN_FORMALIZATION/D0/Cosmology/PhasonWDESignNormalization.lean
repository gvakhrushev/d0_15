import D0.Core.Phi
import Mathlib.Tactic

/-!
# D0-PHASON-WDE-SIGN-NORMALIZATION-OWNER-001 — the dark-energy sign is Galois-forced (Lean)

Python certificate: `05_CERTS/vp_phason_wde_sign_normalization_owner.py`.

Front D construction. The finite internal archive pressure-energy ratio converges to a POSITIVE value
`w_N → +φ⁻¹` (`D0-PHASON-WZ-FINITE-SEQUENCE-SCAFFOLD-001`). A physical dark-energy equation of state
must be NEGATIVE. The sign map between them is **not an inserted minus sign**: the archive and the
retained (observable) sectors are the two Galois-conjugate sectors of `ℚ(φ)/ℚ` (the integer Galois-pair
balance `det(Tⁿ)² = 1`, active·archive eigenvalue product `= −1`, owned by
`D0.Dynamics.GaloisConjugateBalance`; the conjugate-root relations `φ+ψ = 1`, `φ·ψ = −1`).

The nontrivial Galois automorphism `σ : ℚ(φ) → ℚ(φ)` sends `φ ↦ ψ`. Applied to the positive archive
ratio `φ⁻¹`, it gives `σ(φ⁻¹) = ψ⁻¹ = −φ < 0` (because `φ·ψ = −1`). So the retained-sector reading of
the positive archive ratio is NEGATIVE, and the value is the SPECIFIC Galois conjugate `−φ`, provably
**distinct** from the naive negation `−φ⁻¹`. Hence the dark-energy sign is *forced* by the field
automorphism, not chosen.

HONESTY BOUNDARY. What is owned here is the SIGN (negative, Galois-forced) and the conjugate value
`−φ`. The exact physical magnitude/normalization of `w_DE` and the identification "observable sector =
the retained Galois conjugate" stay open: the magnitude is `D0-PHASON-WZ-EXPLICIT-FUNCTION-001`
(PROOF-TARGET), and the redshift/CPL reading is passport-only (`D0-PHASON-WZ-CPL-PASSPORT-001`).
-/

namespace D0.Cosmology

open D0

private lemma two_lt_sqrt5 : (2 : ℝ) < Real.sqrt 5 := by
  nlinarith [sqrt_five_sq, Real.sqrt_nonneg 5]

private lemma phi_pos : 0 < phi := by unfold phi; positivity

/-- The positive internal archive ratio (the limit of the finite `w_N` sequence). -/
noncomputable def archiveRatio : ℝ := phi⁻¹

/-- The retained-sector (observable) reading: the Galois conjugate `σ(φ⁻¹) = ψ⁻¹`. -/
noncomputable def retainedReading : ℝ := psi⁻¹

/-- The internal archive ratio is positive (`+φ⁻¹ > 0`). -/
theorem archive_ratio_pos : 0 < archiveRatio := by
  unfold archiveRatio; exact inv_pos.mpr phi_pos

/-- The Galois-conjugate root `ψ = (1−√5)/2` is negative. -/
theorem psi_neg : psi < 0 := by
  unfold psi; nlinarith [two_lt_sqrt5]

/-- **The Galois conjugate of `φ⁻¹` is `−φ`:** `ψ⁻¹ = −φ`, forced by `φ·ψ = −1`. -/
theorem psi_inv_eq_neg_phi : psi⁻¹ = -phi :=
  inv_eq_of_mul_eq_one_right (by linear_combination -phi_mul_psi)

/-- **The retained-sector reading is negative:** `σ(φ⁻¹) = ψ⁻¹ = −φ < 0`. -/
theorem retained_reading_neg : retainedReading < 0 := by
  unfold retainedReading; rw [psi_inv_eq_neg_phi]; linarith [phi_pos]

/-- The retained reading equals the specific Galois conjugate `−φ`. -/
theorem retained_reading_eq_neg_phi : retainedReading = -phi := by
  unfold retainedReading; exact psi_inv_eq_neg_phi

/-- **Negative control — the sign is not an arbitrary flip.** The naive negation of the archive
ratio, `−φ⁻¹`, is NOT the Galois-conjugate value `ψ⁻¹ = −φ` (since `φ⁻¹ ≠ φ`, i.e. `φ² ≠ 1`). So the
retained negative reading is the *specific* field-conjugate value, not a free minus sign. -/
theorem galois_conjugate_is_not_naive_negation : -(phi⁻¹) ≠ psi⁻¹ := by
  rw [psi_inv_eq_neg_phi]
  intro h
  have heq : phi⁻¹ = phi := neg_injective h
  have h1 : phi * phi⁻¹ = 1 := mul_inv_cancel₀ (ne_of_gt phi_pos)
  rw [heq] at h1
  have h2 : phi ^ 2 = 1 := by rw [pow_two]; exact h1
  rw [phi_sq] at h2
  linarith [phi_pos]

/-- **D0-PHASON-WDE-SIGN-NORMALIZATION-OWNER-001.** The dark-energy sign is Galois-forced: the
positive internal archive ratio `φ⁻¹ > 0` maps, under the Galois conjugation `σ : φ ↦ ψ` (with `ψ < 0`,
`φ·ψ = −1`), to the NEGATIVE retained-sector value `σ(φ⁻¹) = ψ⁻¹ = −φ < 0`, which is provably the
specific conjugate (not the arbitrary negation `−φ⁻¹`). The magnitude/normalization stays open
(`D0-PHASON-WZ-EXPLICIT-FUNCTION-001`). -/
theorem phason_wde_sign_normalization_owner :
    (0 < archiveRatio)
      ∧ (psi < 0)
      ∧ (psi⁻¹ = -phi)
      ∧ (retainedReading < 0)
      ∧ (-(phi⁻¹) ≠ psi⁻¹) :=
  ⟨archive_ratio_pos, psi_neg, psi_inv_eq_neg_phi, retained_reading_neg,
   galois_conjugate_is_not_naive_negation⟩

end D0.Cosmology
