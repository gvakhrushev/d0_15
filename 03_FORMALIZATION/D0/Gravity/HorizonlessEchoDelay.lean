import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic

/-!
# D0-ECHO-DELAY-COMPACTNESS-OWNER-001 — horizonless echo delay τ_echo/M (falsifier target)

Frozen internal input (Book 07 causal-compactness owner): the causal compactness ceiling `C_max = 3/8`
places the reflecting surface at `R = 8M/3`, strictly inside the photon sphere `r_ph = 3M` and outside the
would-be horizon `2M`. The echo round-trip uses the GR tortoise coordinate
`r_star(r) = r + 2M·log(r/(2M) − 1)` (declared EXTERNAL formalism, not a D0 core deduction):

`τ_echo/M = 2·[r_star(3M) − r_star(8M/3)]/M = 2/3 + 4·log(3/2) ≈ 2.2885`.

The `M`'s cancel (`r/(2M)−1` is mass-free at `r ∈ {3M, 8M/3}`), so the target is dimensionless and
mass-rescaling invariant. As `R → 2M` the near-horizon delay diverges (`r_star → −∞`); the `C_max = 3/8`
value gives a SHORT, finite delay. This is a PASSPORT-CLOSED pre-registered rejection target — not a
detection, not a fit, not CORE.
-/

namespace D0.Gravity.HorizonlessEchoDelay

/-- Causal compactness ceiling (frozen). -/
def Cmax : ℚ := 3 / 8

/-- Reflecting surface radius in units of `M`: `R/M = 8/3` (from `C_max = 3/8`). -/
noncomputable def Rsurf : ℝ := 8 / 3

/-- Photon-sphere radius in units of `M`. -/
def rPhoton : ℝ := 3

/-- GR tortoise coordinate in units of `M`: `r_star(x) = x + 2·log(x/2 − 1)`. -/
noncomputable def rstar (x : ℝ) : ℝ := x + 2 * Real.log (x / 2 - 1)

/-- The dimensionless echo round-trip delay `τ_echo/M = 2·[r_star(3) − r_star(8/3)]`. -/
noncomputable def tauOverM : ℝ := 2 * (rstar 3 - rstar Rsurf)

/-- **The surface lies strictly between the horizon and the photon sphere**: `2M < R < 3M`. -/
theorem echo_surface_between_horizon_and_photon : (2 : ℝ) < Rsurf ∧ Rsurf < rPhoton := by
  unfold Rsurf rPhoton; constructor <;> norm_num

/-- **The cavity interval `[R, r_ph]` is nonempty**: `R < r_ph` (`8/3 < 3`). -/
theorem echo_cavity_nonempty : Rsurf < rPhoton := by unfold Rsurf rPhoton; norm_num

/-- **Exact echo delay**: `τ_echo/M = 2/3 + 4·log(3/2)`. -/
theorem tau_echo_exact : tauOverM = 2 / 3 + 4 * Real.log (3 / 2) := by
  have h1 : (3 : ℝ) / 2 - 1 = (2 : ℝ)⁻¹ := by norm_num
  have h2 : (8 : ℝ) / 3 / 2 - 1 = (3 : ℝ)⁻¹ := by norm_num
  have e3 : Real.log ((3 : ℝ) / 2) = Real.log 3 - Real.log 2 :=
    Real.log_div (by norm_num) (by norm_num)
  unfold tauOverM rstar Rsurf
  rw [h1, h2, Real.log_inv, Real.log_inv, e3]
  ring

/-- **Mass-rescaling invariance** (the log argument is mass-free): for every `M ≠ 0`,
`r/(2M) − 1` at `r = 3M` equals its `M = 1` value `1/2`, and at `r = 8M/3` equals `1/3`. Hence `τ_echo/M`
carries no `M`. -/
theorem echo_log_argument_mass_free (M : ℝ) (hM : M ≠ 0) :
    3 * M / (2 * M) - 1 = 3 / 2 - 1 ∧ 8 * M / 3 / (2 * M) - 1 = 8 / 3 / 2 - 1 := by
  constructor <;> · field_simp

/-- **D0-ECHO-DELAY-COMPACTNESS-OWNER-001.** From the frozen `C_max = 3/8` surface `R = 8M/3` (inside the
photon sphere, outside `2M`, nonempty cavity), the dimensionless mass-invariant echo delay is exactly
`τ_echo/M = 2/3 + 4·log(3/2)`. -/
theorem horizonless_echo_delay_owner :
    ((2 : ℝ) < Rsurf ∧ Rsurf < rPhoton)
      ∧ Rsurf < rPhoton
      ∧ tauOverM = 2 / 3 + 4 * Real.log (3 / 2) :=
  ⟨echo_surface_between_horizon_and_photon, echo_cavity_nonempty, tau_echo_exact⟩

end D0.Gravity.HorizonlessEchoDelay
