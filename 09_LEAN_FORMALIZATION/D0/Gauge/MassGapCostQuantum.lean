import D0.Core.Phi
import Mathlib.Tactic

/-!
# D0-MASSGAP-COSTQUANTUM-001 — §26 Yang–Mills: the positive step-cost quantum

The §26 (Yang–Mills mass gap) D0-reformulation rests on a positive minimal cost per elementary cycle.
This module proves the cost-quantum sub-fact: the corpus-fixed step weights `W_ext = φ⁻¹`,
`W_int = φ⁻²` satisfy `W_ext + W_int = 1` (`D0.Core.Phi.phi_inv_satisfies_primitive`), so the minimal
internal cost quantum `ΔS_min = φ⁻²` is a FIXED POSITIVE fraction `> 0` — it cannot be sent to `0` by
refinement (that would require an exogenous infinitely-fine spacing, an unprovable input).

**Register (honest):** this is the positive cost-quantum ONLY — `ΔS_min = φ⁻² > 0`, a fixed corpus
weight. It is NOT the spectral mass gap `E₁ − E₀ ≥ c·ΔS_min` of an operator: that needs a gauge
Hamiltonian / transfer operator with a spectral-gap predicate (no Mathlib operator; constant `c`
undefined) and stays D0-CVFT-F6 / PROOF-TARGET. Two passports: physics (φ-weight step cost) +
Clay-math (§26 positive-cost-quantum core).
-/

namespace D0.Gauge

open D0

/-- The minimal internal step-cost quantum `ΔS_min := W_int = φ⁻²`. -/
noncomputable def deltaS_min : ℝ := phi⁻¹ ^ 2

/-- `φ > 0`. -/
private theorem phi_pos : (0 : ℝ) < phi := by
  unfold phi; positivity

/-- **Positive cost quantum:** `ΔS_min = φ⁻² > 0`. The minimal elementary-cycle cost is a fixed
positive fraction — it cannot vanish under refinement. -/
theorem deltaS_min_pos : 0 < deltaS_min := by
  unfold deltaS_min
  exact pow_pos (inv_pos.mpr phi_pos) 2

/-- The two step weights sum to one: `W_ext + W_int = φ⁻¹ + φ⁻² = 1` (THE 6.1.2), so `ΔS_min = φ⁻²`
is a forced positive fraction, not a tunable parameter. -/
theorem cost_weights_sum_one : phi⁻¹ + deltaS_min = 1 :=
  phi_inv_satisfies_primitive

/-- **§26 cost-quantum core.** The minimal step-cost quantum is positive (`φ⁻² > 0`) and the two
weights sum to one (`φ⁻¹ + φ⁻² = 1`) — a fixed positive minimal cost. NOT the operator mass gap. -/
theorem positive_cost_quantum : 0 < deltaS_min ∧ phi⁻¹ + deltaS_min = 1 :=
  ⟨deltaS_min_pos, cost_weights_sum_one⟩

end D0.Gauge
