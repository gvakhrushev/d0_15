import Mathlib.Data.Fin.VecNotation
import Mathlib.Tactic

/-!
# D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001 — closing the hypercharge-direction obligation as a minimal bridge

The corpus proves (`D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001`, NO-GO) that anomaly-freedom leaves a
**2-dimensional** gaugeable family `span{Y, B−L}`; anomaly cancellation alone does NOT select the SM
hypercharge row. Its own honesty boundary records that the only thing removing `B−L` is imposing
`Y_{ν^c}=0` — which, taken bare, is question-begging.

This module **closes that open obligation in the only honest way**: not as a present-core `THE` (that would
contradict the standing NO-GO without a forced primitive), but as a **rigorous minimal-extension bridge** —
exactly the v16 `ℬ_row` pattern. We name the single bridge `Ξ_Y` and prove it **necessary, sufficient, and
minimal**:

* **`Ξ_Y` (the bridge).** "The gauged charge vanishes on the sterile state `ν^c`" — i.e. `charge(ν^c)=0`.
  Under the D0 graph→physics map this is exactly `ν_R ∈ ker(A)` (the 30-dim zone-balanced archive kernel of
  `D0-TRIPARTITE-IMAGE-KERNEL-001` / `KernelZoneSplit`). **This identification is the R2 graph→physics
  localization, which is a MECH-LIMIT, NOT a forced identity** — hence the bridge status, not `THE`. The net
  structural result is the **linkage**: the hypercharge-direction obligation *is* the R2 localization
  obligation; they are one open obligation, not two.

* **Necessity** (`necessity_two_directions`): without `Ξ_Y`, `Y` and `B−L` are two `ℚ`-independent
  anomaly-free directions, and `B−L` charges `ν^c` (`combo 0 1 5 = 1 ≠ 0`) — a genuine second completion.
* **Sufficiency** (`sufficiency`): imposing `Ξ_Y` (`combo a b 5 = 0`) forces `b = 0`, collapsing the family to
  `span{Y}` — the SM hypercharge ray.
* **Minimality** (`minimal_bridge_coordinate`): `ν^c` is the UNIQUE coordinate that reads the `B−L` coefficient
  alone (`Y_i = 0 ∧ (B−L)_i ≠ 0` iff `i = 5`); no weaker functional cuts the family.

Field order `(q_L, u^c, d^c, ℓ_L, e^c, ν^c)`. All arithmetic is decidable over `ℚ`. Cites the NO-GO; does not
re-mint it. **FIREWALL:** no numerical mass/charge input; `Ξ_Y` is a single ℤ₂ "sterile-or-not" bit.
-/

namespace D0.Matter.HyperchargeBLDirectionBridge

/-- SM hypercharge row in field order `(q_L, u^c, d^c, ℓ_L, e^c, ν^c)`. -/
def Yhc : Fin 6 → ℚ := ![1/6, -2/3, 1/3, -1/2, 1, 0]
/-- `B−L` row in the same field order (`ν^c` carries `B−L = 1`). -/
def bMinusL : Fin 6 → ℚ := ![1/3, -1/3, -1/3, -1, 1, 1]
/-- A general element of the gaugeable family `a·Y + b·(B−L)`. -/
def combo (a b : ℚ) : Fin 6 → ℚ := fun i => a * Yhc i + b * bMinusL i

/-! ## Both generators are anomaly-free (decidable) -/

/-- Gravitational·U(1) anomaly (multiplicity-weighted sum). -/
def grav (X : Fin 6 → ℚ) : ℚ := 6 * X 0 + 3 * X 1 + 3 * X 2 + 2 * X 3 + X 4 + X 5
/-- SU(2)²·U(1) anomaly (doublets `q_L ×3 colour`, `ℓ_L`). -/
def su2 (X : Fin 6 → ℚ) : ℚ := 3 * X 0 + X 3
/-- SU(3)²·U(1) anomaly (colour triplets `q_L ×2 weak`, `u^c`, `d^c`). -/
def su3 (X : Fin 6 → ℚ) : ℚ := 2 * X 0 + X 1 + X 2
/-- U(1)³ cubic anomaly. -/
def cubic (X : Fin 6 → ℚ) : ℚ := 6*(X 0)^3 + 3*(X 1)^3 + 3*(X 2)^3 + 2*(X 3)^3 + (X 4)^3 + (X 5)^3

theorem Y_anomaly_free : grav Yhc = 0 ∧ su2 Yhc = 0 ∧ su3 Yhc = 0 ∧ cubic Yhc = 0 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [grav, su2, su3, cubic, Yhc] <;> norm_num

theorem bMinusL_anomaly_free : grav bMinusL = 0 ∧ su2 bMinusL = 0 ∧ su3 bMinusL = 0 ∧ cubic bMinusL = 0 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [grav, su2, su3, cubic, bMinusL] <;> norm_num

/-! ## The bridge functional reads the `B−L` coefficient -/

/-- The charge on the sterile state `ν^c` (coordinate `5`) equals the `B−L` coefficient `b`. -/
theorem nu_charge_eq_b (a b : ℚ) : combo a b 5 = b := by
  simp [combo, Yhc, bMinusL]

/-! ## Necessity / Sufficiency / Minimality of `Ξ_Y` -/

/-- **Necessity.** `Y` and `B−L` are `ℚ`-independent (a `2×2` minor on columns `{0,1}` is nonzero), and
`B−L` charges `ν^c` — so without `Ξ_Y` there are ≥ 2 inequivalent anomaly-free completions. -/
theorem necessity_two_directions :
    Yhc 0 * bMinusL 1 - Yhc 1 * bMinusL 0 ≠ 0 ∧ combo 0 1 5 = 1 := by
  refine ⟨?_, ?_⟩
  · simp [Yhc, bMinusL]; norm_num
  · rw [nu_charge_eq_b]

/-- **Sufficiency.** Imposing `Ξ_Y` (`ν^c` uncharged) forces the `B−L` coefficient to vanish. -/
theorem sufficiency (a b : ℚ) (h : combo a b 5 = 0) : b = 0 := by
  rw [nu_charge_eq_b] at h; exact h

/-- With `Ξ_Y` the family collapses to the pure-hypercharge ray `span{Y}`. -/
theorem collapses_to_Y (a b : ℚ) (h : combo a b 5 = 0) : combo a b = fun i => a * Yhc i := by
  have hb : b = 0 := sufficiency a b h
  subst hb; funext i; simp [combo]

/-- **Minimality.** `ν^c` is the UNIQUE coordinate that reads the `B−L` coefficient alone
(`Y_i = 0 ∧ (B−L)_i ≠ 0` iff `i = 5`); the bridge functional is minimal. -/
theorem minimal_bridge_coordinate (i : Fin 6) :
    (Yhc i = 0 ∧ bMinusL i ≠ 0) ↔ i = 5 := by
  fin_cases i <;> simp [Yhc, bMinusL] <;> norm_num

/-- **D0-HYPERCHARGE-BL-DIRECTION-BRIDGE-001 (BRIDGE-ASSUMPTIONS-EXPLICIT).** Given the explicit bridge `Ξ_Y`
(`ν^c` uncharged — i.e. `ν_R ∈ ker(A)`, the R2 graph→physics localization, a MECH-LIMIT not a forced identity),
the anomaly-free gaugeable family collapses from the 2-dimensional `span{Y, B−L}` to the unique hypercharge
ray `span{Y}`. The bridge is necessary, sufficient, and minimal. -/
theorem hypercharge_bl_direction_bridge (a b : ℚ) (h_localize : combo a b 5 = 0) :
    b = 0 ∧ combo a b = fun i => a * Yhc i :=
  ⟨sufficiency a b h_localize, collapses_to_Y a b h_localize⟩

end D0.Matter.HyperchargeBLDirectionBridge
