import D0.Core.Delta
import Mathlib.Tactic

/-!
# D0-BARYON-ASYMMETRY-DELTA0-001 — three-zone additive CP/asymmetry coordinate `η̄ = 3·δ₀`

The K(9,11,13) scene has three zones `{9, 11, 13}`. Their CP-carrying seams form the directed 3-cycle
`9 → 11 → 13 → 9`, so there are exactly **three** zone-interfaces — a finite, decidable count fixed by
the scene, NOT a chosen literal. The internal three-zone CP/asymmetry coordinate adds one seam unit
`δ₀ = 1/(2φ³)` per interface (equal weights: an unequal weighting would require an external
zone-weight catalogue, M1-forbidden). Hence

  `η̄ = (interface count)·δ₀ = 3·δ₀`,

with the multiplier `3` forced by `interfaces.card`, proved by `decide`.

SCOPE (honest): this is the D0-INTERNAL coordinate only. Its identification with the observed
baryon-to-photon ratio is a separate empirical passport (no cosmological datum enters here).
Cert: `05_CERTS/vp_baryon_asymmetry_delta0.py`.
-/

namespace D0.Matter

open D0

/-- The three zones of K(9,11,13), as a 3-element index. -/
abbrev Zone := Fin 3

/-- The directed zone-interfaces forming the 3-cycle `9 → 11 → 13 → 9` (one CP-carrying seam per
adjacent zone pair). -/
def baryonInterfaces : Finset (Zone × Zone) := {(0, 1), (1, 2), (2, 0)}

/-- The three-zone 3-cycle has exactly **3** interfaces — forced by the scene, not a literal. -/
theorem baryon_interface_count_three : baryonInterfaces.card = 3 := by decide

/-- Three-zone additive CP/asymmetry coordinate: one seam unit `δ₀` per forced zone-interface,
equal-weighted. -/
noncomputable def baryonCPCoordinate : ℝ := (baryonInterfaces.card : ℝ) * delta0

/-- **D0-BARYON-ASYMMETRY-DELTA0-001 (internal coordinate).** `η̄ = 3·δ₀`, the multiplier `3` forced
by the three-zone interface count (`baryon_interface_count_three`), not a chosen constant. Internal
CP coordinate only; the observed baryon-to-photon ratio is an empirical passport, not this object. -/
theorem baryon_cp_eq_three_delta0 : baryonCPCoordinate = 3 * delta0 := by
  unfold baryonCPCoordinate
  rw [baryon_interface_count_three]
  push_cast
  ring

end D0.Matter
