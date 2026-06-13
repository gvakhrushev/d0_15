import D0.Core.Phi

/-!
# D0-VIETA-GALOIS-ABCD-001 — ABCD = Vieta/Galois data of x² - x - 1 (per-claim module)

Mirrors the Python certificate `05_CERTS/vp_vieta_galois_abcd.py`.

The four terminal roles ABCD are the Vieta/Galois data of the self-description
equation `x² - x - 1 = 0`, whose roots are `φ = (1+√5)/2` and `ψ = 1 - φ = (1-√5)/2`:

* **A**: `φ + ψ = 1`        (Vieta sum    = Galois trace, rational ⇒ Galois-invariant)
* **B**: `φ · ψ = -1`       (Vieta product = Galois norm,  rational ⇒ Galois-invariant)
* **C**: `φ² = φ + 1`        (active-branch recursion)
* **D**: `ψ² = ψ + 1`        (conjugate-branch recursion; C,D are the Galois pair)
* **delta0** `= φ - 3/2 = 1/(2 φ³)`  is the forced cut offset, and `φ⁻³ = 2·delta0`.

Galois content: conjugation `Gal(ℚ(√5)/ℚ) = ℤ₂` swaps the roots (`φ ↔ ψ`), so it
swaps C and D, while fixing the rational invariants A (=1) and B (=-1).

This is a leaf per-claim module: it imports only the (frozen, proved) `D0.Core.Phi`
and reuses its theorems `phi_add_psi`, `phi_mul_psi`, `phi_sq`, `psi_sq`, plus the
exact `√5² = 5` lemma, so it builds in seconds and stays parallel-editable.
-/

namespace D0.Claims

open D0

/-- The forced cut offset `delta0 = φ - 3/2`, as an exact real of `ℚ(φ)`. -/
noncomputable def delta0 : ℝ := phi - 3 / 2

/-- **THE** Vieta/Galois/forced-cut package for ABCD, exactly mirroring the cert.

All five lines are proved over `ℝ` from the closed forms of `φ, ψ`:

* A `φ + ψ = 1`,  B `φ·ψ = -1`,  C `φ² = φ+1`,  D `ψ² = ψ+1`;
* the conjugate pairing `ψ = 1 - φ` (so Galois conjugation `φ ↦ 1-φ` swaps the
  roots, i.e. swaps C and D while fixing the rational invariants A, B);
* the forced offset identities `delta0·(2 φ³) = 1` (so `delta0 = 1/(2 φ³)`) and
  `φ⁻³ = 2·delta0`. -/
theorem vieta_galois_abcd :
    -- A: Vieta sum = Galois trace (rational ⇒ invariant)
    phi + psi = 1
    -- B: Vieta product = Galois norm (rational ⇒ invariant)
  ∧ phi * psi = -1
    -- C: active-branch recursion
  ∧ phi ^ 2 = phi + 1
    -- D: conjugate-branch recursion
  ∧ psi ^ 2 = psi + 1
    -- Galois pairing: ψ is the conjugate root φ ↦ 1 - φ (swaps C and D)
  ∧ psi = 1 - phi
    -- delta0 is the forced cut offset: delta0 = 1/(2 φ³)
  ∧ delta0 * (2 * phi ^ 3) = 1
    -- and the half-cut identity φ⁻³ = 2·delta0
  ∧ phi⁻¹ ^ 3 = 2 * delta0 := by
  have h5 : (Real.sqrt 5) ^ 2 = (5 : ℝ) := sqrt_five_sq
  have h53 : (Real.sqrt 5) ^ 3 = 5 * Real.sqrt 5 := by
    have : (Real.sqrt 5) ^ 3 = (Real.sqrt 5) ^ 2 * Real.sqrt 5 := by ring
    rw [this, h5]
  have h54 : (Real.sqrt 5) ^ 4 = 25 := by
    have : (Real.sqrt 5) ^ 4 = ((Real.sqrt 5) ^ 2) ^ 2 := by ring
    rw [this, h5]; norm_num
  have hphi_ne : phi ≠ 0 := by
    unfold phi
    have : (0 : ℝ) < (1 + Real.sqrt 5) / 2 := by positivity
    exact ne_of_gt this
  refine ⟨phi_add_psi, phi_mul_psi, phi_sq, psi_sq, ?_, ?_, ?_⟩
  · -- ψ = 1 - φ  (the Galois conjugate of φ)
    unfold phi psi; ring
  · -- delta0 * (2 φ³) = 1
    unfold delta0 phi
    ring_nf
    nlinarith [h5, h53, h54]
  · -- φ⁻³ = 2 delta0, equivalently (2 delta0) * φ³ = 1
    unfold delta0
    rw [inv_pow]
    rw [inv_eq_iff_eq_inv, eq_comm, inv_eq_iff_eq_inv]
    have hpow_ne : phi ^ 3 ≠ 0 := pow_ne_zero 3 hphi_ne
    field_simp
    unfold phi
    ring_nf
    nlinarith [h5, h53, h54]

end D0.Claims
