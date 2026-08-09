import Mathlib.Tactic
import Mathlib.GroupTheory.SpecificGroups.Quaternion
import D0.Foundation.CascadeChain

/-!
# The second interlock link: the order-memory repair fails the scale floor

**Target: `D0-CASCADE-INSUFFICIENCY-CHAIN-001`** (the corpus's central thesis, its
highest-value open umbrella row). The chain property — *each floor forced by the
insufficiency of the previous* — is carried at ONE link by the scaffold
(`CascadeChain.chain_linked_four_five_to_five_six`: the 4→5 repair `ℤ × ℤ` IS the 5→6
failure). This module carries the SECOND link, in the scaffold's own registered floor order
(the `CascadeChain` table: order memory 5→6, scale ratio 6→7):

**the 5→6 repair — a finite non-commutative carrier (`S₃`, and `Q₈`) — realizes only
CAPTURED scale ratios, so it is precisely the object the 6→7 floor rejects.**

The bridge reading, stated as this module's own definition (scoped, not smuggled): the scale
ratios AVAILABLE INSIDE a carrier are the quotients of cardinalities of its finite stages
(`carrierRealizedRatio` — for a finite carrier these are exactly the ratios of subset sizes,
the only finite-stage values a finite object owns; the capture reading itself is the 6→7
floor's own, `NonCaptured = Irrational`, owned at §01.21.1 grade by
`D0-CASCADE-FLOOR-SCALE-RATIO-001`). Under that reading the link is a theorem: EVERY
stage-realized ratio is rational (`finite_carrier_ratio_captured`, fully generic — the
failure is intrinsic to finite-STAGE realization; for a finite carrier the finite stages
exhaust it, which is what scopes the bridging reading to the repair carriers), while the 5→6
obligation is genuinely met on BOTH repair carriers — `control_orderEncoded` (S₃) and
`control_quaternion_orderEncoded` (Q₈), both OWNED at `D0-CASCADE-FLOOR-ORDER-MEMORY-001`
and cited, not re-proved. So the repair does not anticipate the next
obligation; it creates the object on which the next obligation is asked, and fails it — the
cascade is forced past the finite non-commutative stage toward an irrational
(infinite-refinement) scale, which is exactly where the 6→7 control (`phi_non_captured`)
lives.

**Honest scope (pre-registered).**
1. ADJACENCY: the link is between adjacent floors OF THE SCAFFOLD'S CARRIED ORDER
   (`CascadeChain` table and `carriedFloors` list: 5→6 then 6→7). The §01.6.1c PROSE order
   places the scale-ratio step before the torus/order steps; the scaffold's registered
   numbering is the adjacency owner cited here, and the SEMANTIC content — "the finite
   non-commutative repair realizes only rational scales" — is numbering-independent. An
   owner re-ordering of the floors would re-label, not refute, this link.
2. The `carrierRealizedRatio` reading is THIS module's bridging definition; a different
   reading of "the scale a carrier realizes" is new work with its own audit.
3. The umbrella stays OPEN: floors defect⇒closure⇒shell and "three insufficiencies = three
   zones" remain unformalized; this adds one link, it does not finish the chain.
4. Nothing here selects `φ` — the 6→7 floor reaches "irrational" only, and the narrowing to
   `φ` is the separate owned canonization step (stated by the floor module itself,
   `floor_does_not_select_phi`).
-/

namespace D0.Foundation

open scoped Classical

/-- The scale ratios available inside a carrier: quotients of cardinalities of its finite
stages (subsets). For a finite carrier these are the only finite-stage values it owns. This
is the module's bridging definition — scoped as such in the docstring. -/
def carrierRealizedRatio (G : Type*) (r : ℝ) : Prop :=
  ∃ s t : Finset G, t.Nonempty ∧ r = (s.card : ℝ) / (t.card : ℝ)

/-- **Every ratio a carrier realizes is rational, hence CAPTURED** (fails the 6→7 obligation
`NonCaptured = Irrational`). Fully generic: the failure is intrinsic to finite-stage
realization, not to any particular group. -/
theorem finite_carrier_ratio_captured {G : Type*} {r : ℝ}
    (h : carrierRealizedRatio G r) : ¬ NonCaptured r := by
  obtain ⟨s, t, _, rfl⟩ := h
  have hcast : ((s.card : ℝ) / (t.card : ℝ)) = (((s.card : ℚ) / (t.card : ℚ) : ℚ) : ℝ) := by
    push_cast
    ring
  rw [hcast]
  exact Rat.not_irrational _

/-- **The second interlock link (5→6 → 6→7), at the scaffold's carried order**: the carrier
that repairs order memory (`S₃`; `Q₈` likewise — both controls cited from the owned floor
module) realizes only captured scale ratios — the
very object that fixed the previous floor is one the next floor rejects. Conjuncts: the 5→6
obligation holds on both repair carriers (both controls cited from
`D0-CASCADE-FLOOR-ORDER-MEMORY-001`), and every scale ratio either carrier realizes fails
the 6→7 obligation. -/
theorem chain_linked_five_six_to_six_seven :
    OrderEncoded (Equiv.Perm (Fin 3))
      ∧ OrderEncoded (QuaternionGroup 2)
      ∧ (∀ r : ℝ, carrierRealizedRatio (Equiv.Perm (Fin 3)) r → ¬ NonCaptured r)
      ∧ (∀ r : ℝ, carrierRealizedRatio (QuaternionGroup 2) r → ¬ NonCaptured r) :=
  ⟨control_orderEncoded, control_quaternion_orderEncoded,
    fun _ h => finite_carrier_ratio_captured h,
    fun _ h => finite_carrier_ratio_captured h⟩

/-- **The floors do not collapse**: the 6→7 obligation is satisfiable (by the corpus's own
survivor `φ`, cited from the floor module) while no carrier-realized ratio satisfies it —
the scale requirement genuinely forces the cascade OUT of the finite carrier, it does not
merely restate order memory. -/
theorem scale_floor_forces_out :
    NonCaptured ((1 + Real.sqrt 5) / 2)
      ∧ ∀ r : ℝ, carrierRealizedRatio (Equiv.Perm (Fin 3)) r → ¬ NonCaptured r :=
  ⟨phi_non_captured, fun _ h => finite_carrier_ratio_captured h⟩

end D0.Foundation
