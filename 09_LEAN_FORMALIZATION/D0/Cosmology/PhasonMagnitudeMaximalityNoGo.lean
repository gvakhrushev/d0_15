import D0.Cosmology.PhasonWDESignNormalization

/-!
# D0-PHASON-MAGNITUDE-MAXIMALITY-NOGO-001 — the dark-energy magnitude map is not forced

The dark-energy SIGN is owned (`D0-PHASON-WDE-SIGN-NORMALIZATION-OWNER-001`: `w_DE` is Galois-forced
negative, retained reading `= −φ`). What present-core does NOT own is the **magnitude map** `z ↦ w_DE(z)`
(the `z`-profile of `|w_DE|`). Present-core fixes only (i) the sign (negative) and (ii) the conjugate
anchor value `−φ`.

Maximality witness: exhibit **two admissible magnitude maps** `w₁, w₂ : ℝ → ℝ`, both respecting every
owned invariant — negative on the window and equal to the owned anchor `−φ` at `z = 0` — yet differing at
`z = 1`. Hence the magnitude profile is **underdetermined by present-core**: no canonical `|w_DE(z)|` is
forced. The magnitude requires an EXTERNAL physical-branch passport (DESI/CPL comparison), not a
present-core theorem. Closed-negative; the sign owner is untouched.
-/

namespace D0.Cosmology.PhasonMagnitudeMaximalityNoGo

open D0.Cosmology D0

/-- Admissible magnitude map A: `w₁(z) = −φ − z` (negative, anchor `−φ` at `z=0`). -/
noncomputable def w1 (z : ℝ) : ℝ := -phi - z

/-- Admissible magnitude map B: `w₂(z) = −φ − 2z` (negative, anchor `−φ` at `z=0`). -/
noncomputable def w2 (z : ℝ) : ℝ := -phi - 2 * z

/-- Both maps hit the owned anchor `−φ` at `z = 0`. -/
theorem both_anchor_at_neg_phi : w1 0 = -phi ∧ w2 0 = -phi := by
  constructor <;> simp [w1, w2]

/-- Both maps preserve the owned SIGN (negative on the window `z ≥ 0`, since `−φ < 0`). -/
theorem both_negative_on_window (z : ℝ) (hz : 0 ≤ z) : w1 z < 0 ∧ w2 z < 0 := by
  have hp : (0 : ℝ) < phi := by unfold phi; positivity
  constructor <;> · simp only [w1, w2]; linarith

/-- **The two admissible maps differ** at `z = 1` (`−φ−1 ≠ −φ−2`). -/
theorem maps_differ : w1 1 ≠ w2 1 := by
  simp only [w1, w2]; intro h; norm_num at h

/-- **D0-PHASON-MAGNITUDE-MAXIMALITY-NOGO-001 (closed-negative).** Two admissible magnitude maps agree on
every owned invariant (sign negative, anchor `−φ` at `z=0`) yet differ at `z=1`: the dark-energy
magnitude map is not forced by present-core. The magnitude needs an external physical-branch passport;
the Galois-forced SIGN owner is untouched. -/
theorem phason_magnitude_maximality_nogo :
    (w1 0 = -phi ∧ w2 0 = -phi)
      ∧ (∀ z : ℝ, 0 ≤ z → w1 z < 0 ∧ w2 z < 0)
      ∧ w1 1 ≠ w2 1 :=
  ⟨both_anchor_at_neg_phi, both_negative_on_window, maps_differ⟩

end D0.Cosmology.PhasonMagnitudeMaximalityNoGo
