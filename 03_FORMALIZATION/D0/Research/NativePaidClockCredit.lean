import D0.Foundation.EndogenousActionQuantum
import D0.Foundation.ProspectiveExecution

/-!
# The necessary net credit for a paid round-trip clock family

This module formalizes the algebraic ER5 consequence of the existing
`ActionProtocol` unit floor and a stated complete-price binding. The link from
an admitted physical execution to the protocol cost, the selected Info/work,
the heat bound, and common-task admission remain explicit hypotheses.
-/

namespace D0.Research.NativePaidClockCredit

open D0.Foundation.EndogenousActionQuantum

/-- Primitive protocol cost of repeating the same distinguishable round trip
`x → y → x` exactly `m` times. -/
def repeatedRoundTripCost
    {P : D0.Foundation.VerifiabilityNecessity.VerificationProtocol}
    (A : ActionProtocol P) (x y : P.State) (m : ℕ) : ℝ :=
  (m : ℝ) * (A.action x y + A.action y x)

/-- Each realized round trip pays at least two primitive action quanta. -/
theorem repeated_roundtrip_cost_lower_bound
    {P : D0.Foundation.VerifiabilityNecessity.VerificationProtocol}
    (A : ActionProtocol P)
    (x y : P.State) (hxy : x ≠ y) (m : ℕ) :
    2 * (m : ℝ) ≤ repeatedRoundTripCost A x y m := by
  have hcycle := D0.Foundation.EndogenousActionQuantum.original_roundtrip_forces_paid_history
    A x y hxy
  have hm := mul_le_mul_of_nonneg_left hcycle (show 0 ≤ (m : ℝ) by positivity)
  simpa [repeatedRoundTripCost, mul_comm] using hm

/-- The ER5 necessary credit inequality under an explicit same-history binding
`C - I + W = κ B + b + e` and the declared logarithmic upper bound on `B`.

`hRealizedCost` is the application map from this protocol's repeated
round trips to the actual complete Cost. The theorem does not assert that a
physical D0 execution supplies that map or that the price binding is selected.
-/
theorem er5_required_net_credit
    {P : D0.Foundation.VerifiabilityNecessity.VerificationProtocol}
    (A : ActionProtocol P)
    (x y : P.State) (hxy : x ≠ y) (m : ℕ)
    (C I W B κ β J₀ D₀ d b e : ℝ)
    (hRealizedCost : repeatedRoundTripCost A x y m ≤ C)
    (hκ : 0 < κ)
    (hHeat : B ≤ J₀ +
      Real.log (425 * (D₀ + 2 * (m : ℝ) * d)) / β)
    (hPrice : C - I + W = κ * B + b + e) :
    I - W ≥ 2 * (m : ℝ) - κ * J₀ -
      (κ / β) * Real.log (425 * (D₀ + 2 * (m : ℝ) * d)) - b - e := by
  have hCost := repeated_roundtrip_cost_lower_bound A x y hxy m
  have hCompleteCost : 2 * (m : ℝ) ≤ C := le_trans hCost hRealizedCost
  have hBookUpper := mul_le_mul_of_nonneg_left hHeat (le_of_lt hκ)
  have hBookUpper' : κ * B ≤ κ * J₀ +
      (κ / β) * Real.log (425 * (D₀ + 2 * (m : ℝ) * d)) := by
    calc
      κ * B ≤ κ * (J₀ +
          Real.log (425 * (D₀ + 2 * (m : ℝ) * d)) / β) := hBookUpper
      _ = κ * J₀ +
          (κ / β) * Real.log (425 * (D₀ + 2 * (m : ℝ) * d)) := by ring
  linarith

/-- Finite telescoping form of the ER6 clock-source obstruction. If the
primitive Cost grows by at least two per added round trip, and the *change* in
net Info/work credit and Book clock is bounded above, then the accumulated
source residual has the corresponding lower bound. The one-sided
`limsup (Iₘ-Wₘ)/m ≤ 0` hypothesis and logarithmic heat estimate are supplied
by callers when deriving the asymptotic statement. -/
theorem er6_finite_telescoping_lower_bound
    (m : ℕ) (Cₘ C₀ κ Bₘ B₀ b eₘ e₀ Iₘ Wₘ I₀ W₀ creditBound bookBound : ℝ)
    (hκ : 0 < κ)
    (hCost : 2 * (m : ℝ) ≤ Cₘ - C₀)
    (hCredit : (Iₘ - Wₘ) - (I₀ - W₀) ≤ creditBound)
    (hBook : Bₘ - B₀ ≤ bookBound)
    (hPriceₘ : Cₘ - Iₘ + Wₘ = κ * Bₘ + b + eₘ)
    (hPrice₀ : C₀ - I₀ + W₀ = κ * B₀ + b + e₀) :
    eₘ - e₀ ≥ 2 * (m : ℝ) - creditBound - κ * bookBound := by
  have hBook' := mul_le_mul_of_nonneg_left hBook (le_of_lt hκ)
  have hCostIdentity : Cₘ - C₀ =
      κ * (Bₘ - B₀) + (eₘ - e₀) +
        ((Iₘ - Wₘ) - (I₀ - W₀)) := by
    linarith [hPriceₘ, hPrice₀]
  linarith

end D0.Research.NativePaidClockCredit
