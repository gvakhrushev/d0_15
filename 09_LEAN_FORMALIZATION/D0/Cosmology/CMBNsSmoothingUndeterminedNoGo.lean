import Mathlib.Tactic

/-!
# D0-CMB-NS-SMOOTHING-UNDETERMINED-NOGO-001 — spectrum + unforced (k,u) ⊬ n_s (closed-negative)

The phason power proxy on the nonzero connected modes of `K(9,11,13)` is
`P(k) = Σ_i w_i / (k² + λ_i)` with `λ_i ∈ {20,22,24,33}` and smoothing weights `w_i = mult_i·e^{−u λ_i}`
(`Π_perp` removes the zero mode). The discrete spectral tilt is `n_eff − 1 = (k/P)·P'(k)` with
`P'(k) = Σ_i w_i·(−2k)/(k² + λ_i)²`.

**This module proves the tilt is NOT a function of the spectrum alone**: it varies (i) with the
evaluation wavenumber `k` and (ii) with the smoothing measure `(w_i)`. Hence the bare spectrum, together
with an *unforced* evaluation point `k` and an *unforced* smoothing window `u`, does NOT determine a
single scalar `n_s`. This is a finite, decidable, closed-negative no-go (exact `ℚ` arithmetic; no Planck
`n_s`, no inflaton, no survey datum).

Admissible smoothing = any positive weights; the heat family `w_i = mult_i e^{−u λ_i}` is a one-parameter
subfamily. `wA = (12,10,8,2)` is the `u = 0` weighting (`w = mult`); `wB = (12,5,2,1)` is a low-`λ`-
emphasising admissible smoothing. The EXACT missing artifact (named, still open,
`D0-CMB-IDS-SMOOTHING-OWNER-001`): a canonical internally-FORCED `(k,u)` selection turning `n_eff − 1`
into a single determined value.
-/

namespace D0.Cosmology.CMBNsSmoothingUndeterminedNoGo

/-- The discrete spectral tilt `n_eff − 1 = (k/P)·P'(k)` of the heat-smoothed phason power proxy on the
nonzero modes `{20,22,24,33}`, as an exact rational of the wavenumber `k` and smoothing weights `w_i`. -/
def tilt (k w20 w22 w24 w33 : ℚ) : ℚ :=
  k * (w20 * (-2 * k) / (k ^ 2 + 20) ^ 2 + w22 * (-2 * k) / (k ^ 2 + 22) ^ 2
        + w24 * (-2 * k) / (k ^ 2 + 24) ^ 2 + w33 * (-2 * k) / (k ^ 2 + 33) ^ 2)
    / (w20 / (k ^ 2 + 20) + w22 / (k ^ 2 + 22) + w24 / (k ^ 2 + 24) + w33 / (k ^ 2 + 33))

/-- **The tilt varies with the wavenumber `k`** (same smoothing `wA = mult`): `n_eff−1` at `k=1`
differs from `k=2`. So the evaluation point is a free degree of freedom the spectrum does not fix. -/
theorem tilt_varies_with_wavenumber : tilt 1 12 10 8 2 ≠ tilt 2 12 10 8 2 := by
  unfold tilt; norm_num

/-- **The tilt varies with the smoothing measure** (same `k = 1`): the `u = 0` weighting `wA = mult`
gives a different tilt from the low-`λ`-emphasising admissible smoothing `wB = (12,5,2,1)`. So the
smoothing window `u` is a free degree of freedom the spectrum does not fix. -/
theorem tilt_varies_with_smoothing_window : tilt 1 12 10 8 2 ≠ tilt 1 12 5 2 1 := by
  unfold tilt; norm_num

/-- **D0-CMB-NS-SMOOTHING-UNDETERMINED-NOGO-001 (closed-negative).** The discrete spectral tilt is not
constant over the `(k, positive-smoothing)` evaluation domain — it varies on BOTH axes — so the bare
`K(9,11,13)` spectrum plus an unforced `(k,u)` does NOT determine a single `n_s`. A canonical forced
`(k,u)` selection is the exact missing artifact (`D0-CMB-IDS-SMOOTHING-OWNER-001`, still PROOF-TARGET). -/
theorem cmb_ns_smoothing_undetermined_nogo :
    tilt 1 12 10 8 2 ≠ tilt 2 12 10 8 2
      ∧ tilt 1 12 10 8 2 ≠ tilt 1 12 5 2 1 :=
  ⟨tilt_varies_with_wavenumber, tilt_varies_with_smoothing_window⟩

end D0.Cosmology.CMBNsSmoothingUndeterminedNoGo
