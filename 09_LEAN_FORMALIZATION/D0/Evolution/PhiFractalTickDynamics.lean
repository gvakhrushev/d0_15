import D0.Core.Phi
import D0.IM.ContinuumFromFractalTick
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic

/-!
# D0-PHI-FRACTAL-TICK-DYNAMICS-OWNER-001 — the tick-weight connector

BOOK_06 §06.6. Python certificates:
`05_CERTS/vp_phi_fractal_tick_dynamics.py`, `05_CERTS/vp_continuous_time_semigroup_envelope.py`.

This module is the CONNECTOR between Block II (the archive-delay tick, index `k`) and the already-owned
φ-ladder / continuous-envelope substrate of `D0.IM.ContinuumFromFractalTick` (claims D0-IM-003 and
D0-PHI-LADDER-SEMIGROUP-001). The substrate theorems
  * `ladder_constant_ratio` : `A_{k+1} = A_k · φ⁻¹`,
  * `ladder_substrate_conserved` : `p + p² = 1` with `p = φ⁻¹` (column-stochastic split),
  * `env_restricts_to_ladder`, `env_cocycle` : the continuous envelope `A(t) = A₀·exp(−t·log φ)`,
are NOT re-derived here; they are imported and REUSED.

The NEW content is the reading: each archive-delay tick (Block II index `k`) multiplies the active
amplitude by `φ⁻¹` BECAUSE the self-return detector split is `p + p² = 1` (the active fraction is the
unique contracting root `p = φ⁻¹`). So the tick weight is not a chosen decay constant — it is FORCED by
the binary self-readout balance. The envelope rate `log φ` is then the per-tick entropy rate.

Honest scope: these are finite/decidable identities on the contraction domain. No primitive time object,
external clock, or SI unit (c, h, ħ, seconds) enters — the only rate is the dimensionless `log φ`.
-/

namespace D0.Evolution.PhiFractalTickDynamics

open D0
open D0.IM

/-! ## 1. The tick weight is forced to `φ⁻¹` by the self-return split `p + p² = 1` -/

/-- **Self-return split forces the tick weight.** The detector split `p + p² = 1` has a unique root in
`(0,1)` — the contracting golden root `φ⁻¹` — so the per-tick active fraction (the "tick weight") is
forced to be `φ⁻¹`, not a freely chosen decay constant. Reuses `phi_inv_satisfies_primitive`
(`p + p² = 1` at `p = φ⁻¹`), `ladder_rate_mem_unit` (`0 < φ⁻¹ < 1`), and the substrate's
`primitive_quadratic_unique_pos_root` (uniqueness of the positive root). -/
theorem phi_split_forces_tick_weight {p : ℝ} (hp0 : 0 < p) (hp1 : p < 1) (hp : p + p ^ 2 = 1) :
    p = phi⁻¹ := by
  rw [phi_inv_eq_primitiveRoot]
  exact primitive_quadratic_unique_pos_root hp0 hp1 hp

/-- The forced tick weight itself satisfies the self-return split `φ⁻¹ + (φ⁻¹)² = 1`. (Reuses the
core substrate identity; recorded here so the connector is self-contained.) -/
theorem tick_weight_satisfies_split : phi⁻¹ + (phi⁻¹) ^ 2 = 1 := phi_inv_satisfies_primitive

/-- The forced tick weight is a genuine contraction: `0 < φ⁻¹ < 1`. (Reuses `ladder_rate_mem_unit`.) -/
theorem tick_weight_mem_unit : 0 < phi⁻¹ ∧ phi⁻¹ < 1 := ladder_rate_mem_unit

/-! ## 2. One archive tick multiplies the active amplitude by `φ⁻¹` -/

/-- **One archive tick = multiply by `φ⁻¹`.** Direct reuse of the substrate's `ladder_constant_ratio`:
advancing the Block II archive index `k → k+1` multiplies the active amplitude `A_k = ladderAmount k`
by the forced tick weight `φ⁻¹`. -/
theorem archive_tick_multiplies_by_phi_inv (k : ℕ) :
    ladderAmount (k + 1) = ladderAmount k * phi⁻¹ :=
  ladder_constant_ratio k

/-- The active amplitude is strictly nonincreasing per tick (`A_{k+1} ≤ A_k`), since multiplying by the
contraction weight `φ⁻¹ ∈ (0,1)` shrinks a nonnegative amplitude. A finite WITNESS of monotone decay,
not a universal continuum statement. -/
theorem archive_tick_nonincreasing (k : ℕ) : ladderAmount (k + 1) ≤ ladderAmount k := by
  rw [archive_tick_multiplies_by_phi_inv]
  have hform : ladderAmount k = (phi⁻¹) ^ k := rfl
  have hnn : (0 : ℝ) ≤ ladderAmount k := by
    rw [hform]; exact pow_nonneg tick_weight_mem_unit.1.le k
  nlinarith [tick_weight_mem_unit.1, tick_weight_mem_unit.2, hnn]

/-! ## 3. Closed form of the discrete ladder: `A_k = A₀ · φ⁻ᵏ` -/

/-- The closed form at the canonical normalization `A₀ = 1`: `A_k = φ⁻ᵏ`, definitionally
(`ladderAmount k := phi⁻¹ ^ k`). -/
theorem discrete_ladder_closed_form_unit (k : ℕ) : ladderAmount k = (phi⁻¹) ^ k := rfl

/-- **Discrete ladder closed form** with explicit normalization `A₀`: after `k` archive ticks the active
amplitude is `A₀ · (φ⁻¹)ᵏ`. Here `ladderAmount k = (φ⁻¹)ᵏ` is the `A₀ = 1` substrate, so the general
normalized amplitude is `A₀ * ladderAmount k`; rewriting by the unit closed form gives the explicit form. -/
theorem discrete_ladder_closed_form (A0 : ℝ) (k : ℕ) :
    A0 * ladderAmount k = A0 * (phi⁻¹) ^ k := by
  rw [discrete_ladder_closed_form_unit]

/-! ## 4. The continuous envelope restricts to the discrete ladder and obeys the cocycle -/

/-- **Continuous envelope restricts to the integer ladder.** Direct reuse of the substrate's
`env_restricts_to_ladder`: the continuous envelope `A(t) = A₀·exp(−t·log φ)` evaluated at integer
`t = k` equals the certified discrete tick ladder `A₀ · (φ⁻¹)ᵏ`. -/
theorem continuous_envelope_restricts_to_ladder (A0 : ℝ) (k : ℕ) :
    envAmount A0 (k : ℝ) = A0 * ladderAmount k :=
  env_restricts_to_ladder A0 k

/-- **Continuous envelope cocycle / semigroup law.** Direct reuse of the substrate's `env_cocycle`: for
`A₀ ≠ 0` the envelope obeys `A(s+t) = A(s)·A(t)/A₀`, the unique multiplicative one-parameter extension of
the φ-tick (holds on the convergence/resolvent domain of the real exponential). -/
theorem continuous_envelope_cocycle (A0 s t : ℝ) (hA0 : A0 ≠ 0) :
    envAmount A0 (s + t) = envAmount A0 s * envAmount A0 t / A0 :=
  env_cocycle A0 s t hA0

/-! ## 5. The envelope rate is the per-tick entropy rate `log φ` -/

/-- **The envelope rate is `log φ`.** Advancing the continuous parameter by one tick (`t → t+1`)
multiplies the envelope by `exp(−log φ) = φ⁻¹`, the forced tick weight; equivalently the log-amplitude
drops by exactly `log φ` per unit, so the (dimensionless) decay/entropy rate of the tick semigroup is
`log φ`. This is the continuous shadow of the discrete constant ratio — no SI clock enters. -/
theorem log_phi_is_tick_entropy_rate (A0 t : ℝ) :
    envAmount A0 (t + 1) = envAmount A0 t * Real.exp (-(Real.log phi)) := by
  unfold envAmount
  rw [show -((t + 1) * Real.log phi) = (-(t * Real.log phi)) + (-(Real.log phi)) by ring,
      Real.exp_add]
  ring

/-- The per-tick rate factor `exp(−log φ)` equals the forced tick weight `φ⁻¹`. So the continuous rate
`log φ` and the discrete tick weight `φ⁻¹` are the same datum (`φ⁻¹ = e^{−log φ}`). -/
theorem rate_factor_eq_tick_weight : Real.exp (-(Real.log phi)) = phi⁻¹ := by
  have hpos : (0 : ℝ) < phi := by unfold phi; positivity
  rw [Real.exp_neg, Real.exp_log hpos]

/-! ## 6. Combined connector certificate -/

/-- **D0-PHI-FRACTAL-TICK-DYNAMICS-OWNER-001 / D0-CONTINUOUS-TIME-SEMIGROUP-ENVELOPE-001.**
The tick-weight connector bundle:
  1. the self-return split `p + p² = 1` forces the tick weight `p = φ⁻¹`;
  2. one archive tick multiplies the active amplitude by `φ⁻¹`;
  3. the discrete ladder closed form is `A₀ · (φ⁻¹)ᵏ`;
  4. the continuous envelope restricts on integers to that discrete ladder;
  5. the envelope obeys the multiplicative cocycle `A(s+t) = A(s)A(t)/A₀`;
  6. the per-tick rate factor is `exp(−log φ) = φ⁻¹`, i.e. the entropy rate is `log φ`.
Items 2,4,5 are direct reuse of the D0-IM-003 / D0-PHI-LADDER-SEMIGROUP-001 substrate; items 1,3,6 are
the new connector content (the tick weight is FORCED, not chosen). -/
theorem phi_fractal_tick_dynamics_cert :
    (∀ p : ℝ, 0 < p → p < 1 → p + p ^ 2 = 1 → p = phi⁻¹) ∧
    (∀ k : ℕ, ladderAmount (k + 1) = ladderAmount k * phi⁻¹) ∧
    (∀ A0 : ℝ, ∀ k : ℕ, A0 * ladderAmount k = A0 * (phi⁻¹) ^ k) ∧
    (∀ A0 : ℝ, ∀ k : ℕ, envAmount A0 (k : ℝ) = A0 * ladderAmount k) ∧
    (∀ A0 s t : ℝ, A0 ≠ 0 → envAmount A0 (s + t) = envAmount A0 s * envAmount A0 t / A0) ∧
    Real.exp (-(Real.log phi)) = phi⁻¹ :=
  ⟨fun _ hp0 hp1 hp => phi_split_forces_tick_weight hp0 hp1 hp,
   archive_tick_multiplies_by_phi_inv,
   discrete_ladder_closed_form,
   continuous_envelope_restricts_to_ladder,
   continuous_envelope_cocycle,
   rate_factor_eq_tick_weight⟩

end D0.Evolution.PhiFractalTickDynamics
