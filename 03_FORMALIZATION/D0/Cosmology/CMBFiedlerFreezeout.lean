import Mathlib.Tactic

/-!
# D0-CMB-FIEDLER-FREEZEOUT-OWNER-001 — the freeze-out scale is the Fiedler value λ₂ = 20

The lowest transmissible connected spectral scale is the algebraic connectivity (Fiedler value)
`λ₂ = 20` of the `K(9,11,13)` Laplacian, i.e. the minimum NONZERO eigenvalue of the spectrum
`{0:1, 20:12, 22:10, 24:8, 33:2}`. The freeze-out wavenumber is `k_*² = λ₂ = 20`. Finite decidable fact
off the frozen spectrum (reuses `D0-CONNECTIVITY-SPECTRAL-GAP-SPEED-001`); no survey `k_*` and no Planck
datum enters. "Minimum" is encoded as membership + a lower bound (both `decide`able).
-/

namespace D0.Cosmology.CMBFiedlerFreezeout

/-- The nonzero Laplacian eigenvalues of `K(9,11,13)` (the zero mode is excluded). -/
def nonzeroEigs : List Nat := [20, 22, 24, 33]

/-- The Fiedler value (algebraic connectivity) = lowest nonzero eigenvalue. -/
def fiedler : Nat := 20

/-- **`λ₂ = 20` is the minimum of the nonzero spectrum**: it is a member, and a lower bound for all. -/
theorem fiedler_value_eq_twenty :
    fiedler ∈ nonzeroEigs ∧ ∀ lam ∈ nonzeroEigs, fiedler ≤ lam := by decide

/-- **Every nonzero eigenvalue is ≥ λ₂ = 20** (the Fiedler value is the lower edge). -/
theorem fiedler_is_min_nonzero : ∀ lam ∈ nonzeroEigs, fiedler ≤ lam := fiedler_value_eq_twenty.2

/-- The freeze-out wavenumber squared `k_*² = λ₂ = 20`. -/
def freezeoutKSq : Nat := fiedler

/-- **The freeze-out scale is the Fiedler value**, `k_*² = 20`, the strict lower edge of the nonzero
spectrum (it is a nonzero eigenvalue, no nonzero eigenvalue lies strictly below it, and it is positive). -/
theorem cmb_fiedler_freezeout_owner :
    (20 ∈ nonzeroEigs)
      ∧ freezeoutKSq = 20
      ∧ (∀ lam ∈ nonzeroEigs, 20 ≤ lam)
      ∧ (0 : Nat) < freezeoutKSq := by
  refine ⟨fiedler_value_eq_twenty.1, rfl, fiedler_is_min_nonzero, by decide⟩

end D0.Cosmology.CMBFiedlerFreezeout
