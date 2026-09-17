import D0.Foundation.LucasDefectSign
import D0.Foundation.CascadeChain

/-!
# CASCADE FLOOR — orientation closure forces the `+2` address step

A further floor of `D0-CASCADE-INSUFFICIENCY-CHAIN-001` (BOOK_01 §01.6.1c), carried in the shape
`D0.Foundation.CascadeStep` fixes:

```
Floor        the address ladder with a unit junction step
Obligation   ORIENTATION CLOSURE — the splice across a junction needs no external orientation bit,
             i.e. the orientation class is the same at both ends of the step, at every address
insufficient ¬ OrientationClosed 1        -- a +1 step flips the class
control      OrientationClosed 2          -- a +2 step preserves it, so the demand is satisfiable
minimal      any admissible step is even, hence at least 2
```

The content is **not** re-proved here. The orientation class is the sign of the Lucas defect, owned
by `D0-LUCAS-DEFECT-SIGN-001` (`D0.Foundation.LucasDefectSign.lucas_defect_sign`:
`0 < φⁿ − Lₙ ↔ Odd n`). What this module adds is the *floor*: that the obligation keyed to that sign
fails at step 1, holds at step 2, and admits exactly the even steps — which is the cascade-shaped
form of BOOK_01 §01.6.1c's "the address ladder is forced to advance by `+2`, never `+1`, because a
`+1` step would demand an external orientation bit — a sign catalog — which is `⊥M1`" (BOOK_01:2246).

**Why the control is the point.** `insufficient` alone could be vacuous: an obligation no step
satisfies would force nothing, since the repair would fail it too. Exhibiting the `+2` step as a
structure that *does* splice without an orientation bit is what makes the failure at `+1` a real
obstruction. This is the `check_cert_can_fail` discipline applied to the spine.

**Honest scope.** This carries the *increment* forcing — that the ladder advances by 2 — as a
cascade floor. It does **not** derive the three zone cardinalities, does not claim the exact count
three, and does not close `D0-CASCADE-INSUFFICIENCY-CHAIN-001`: the floors defect⇒closure⇒shell
named in §01.6.1c remain open. The identification of "orientation class" with the defect sign, and
of "junction splice" with the address step, is the reading owned by BOOK_01 §01.6.1c / :2246;
what is machine-checked here is the parity statement and the floor shape.
-/

namespace D0.Foundation.CascadeFloorOrientationParity

open Real
open scoped goldenRatio
open D0.Foundation.LucasDefectSign

/-- **The orientation class of an address.** The sign of the Lucas defect at `n`; by
`D0-LUCAS-DEFECT-SIGN-001` it is positive exactly when `n` is odd. -/
def OrientationPositive (n : ℕ) : Prop := 0 < φ ^ n - lucasR n

/-- The class is the parity of the address — the owned theorem, reused, not re-proved. -/
theorem orientationPositive_iff_odd (n : ℕ) : OrientationPositive n ↔ Odd n :=
  lucas_defect_sign n

/-- **The obligation.** A junction step of size `k` is *orientation-closed* when, at every address,
both ends of the step carry the same orientation class — so the splice needs no external `Z₂` bit. -/
def OrientationClosed (k : ℕ) : Prop :=
  ∀ n : ℕ, (OrientationPositive n ↔ OrientationPositive (n + k))

/-- **The obligation is exactly evenness of the step.** Stated at full generality, so the failure is
a property of the step size itself and not an accident of one address. -/
theorem orientationClosed_iff_even (k : ℕ) : OrientationClosed k ↔ Even k := by
  constructor
  · intro h
    by_contra hodd
    have hk : Odd k := Nat.not_even_iff_odd.mp hodd
    have h0 := h 0
    rw [orientationPositive_iff_odd, orientationPositive_iff_odd, Nat.zero_add] at h0
    have hz : ¬ Odd (0 : ℕ) := by simp
    exact hz (h0.mpr hk)
  · intro hk n
    rw [orientationPositive_iff_odd, orientationPositive_iff_odd, Nat.odd_add]
    simp [hk]

/-- **`insufficient` — the unit step fails.** A `+1` junction flips the orientation class, so the
two layers cannot be spliced without importing an orientation bit the address does not contain. -/
theorem unit_step_insufficient : ¬ OrientationClosed 1 := by
  rw [orientationClosed_iff_even]
  decide

/-- **`control` — the obligation is satisfiable, so the insufficiency is not vacuous.** The `+2`
step preserves the orientation class at every address. -/
theorem two_step_control : OrientationClosed 2 := by
  rw [orientationClosed_iff_even]
  decide

/-- **`minimal` — `+2` is the least admissible junction step.** Every orientation-closed step is
even, so no positive step below 2 survives. -/
theorem two_is_minimal (k : ℕ) (hk : 0 < k) (h : OrientationClosed k) : 2 ≤ k := by
  rw [orientationClosed_iff_even] at h
  rcases Nat.lt_or_ge k 2 with hlt | hge
  · interval_cases k
    · exact absurd h (by decide)
  · exact hge

/-- The floor, packaged in the chain's own shape so it plugs into `carriedFloors` without being
re-argued. -/
def stepOrientationParity : D0.Foundation.CascadeStep where
  name := "orientation closure (+1 fails, +2 splices)"
  ObligationBelow := OrientationClosed 1
  ObligationAbove := OrientationClosed 2
  insufficient := unit_step_insufficient
  control := two_step_control

/-- **The floor, complete.** The obligation fails at the unit step, is satisfiable at the `+2` step
(so the failure is a real obstruction, not a vacuous demand), holds exactly for the even steps, and
`2` is the least admissible one. -/
theorem cascade_floor_orientation_parity :
    (¬ OrientationClosed 1) ∧
    OrientationClosed 2 ∧
    (∀ k : ℕ, OrientationClosed k ↔ Even k) ∧
    (∀ k : ℕ, 0 < k → OrientationClosed k → 2 ≤ k) :=
  ⟨unit_step_insufficient, two_step_control, orientationClosed_iff_even, two_is_minimal⟩

/-- The packaged floor is a genuine, non-vacuous step by the chain's own criteria. -/
theorem stepOrientationParity_genuine :
    ¬ (stepOrientationParity.ObligationBelow ↔ stepOrientationParity.ObligationAbove) :=
  D0.Foundation.step_discriminates stepOrientationParity

end D0.Foundation.CascadeFloorOrientationParity
