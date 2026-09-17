import Mathlib.Tactic
import Mathlib.NumberTheory.Real.Irrational
import D0.NumberTheory.HurwitzClassCanonization

/-!
# D0-CASCADE-FLOOR-SCALE-RATIO-001 — a rational scale is captured (cascade floor 6→7)

Fourth formalized floor of `D0-CASCADE-INSUFFICIENCY-CHAIN-001` (BOOK_01 §01.6.1c), owning the step
*return without an external clock ⇒ the scale ratio is the fixed point of refinement*.

```
Floor        a rational scale ratio p/q
Obligation   NON-CAPTURE — the ratio is not exactly matched at any finite stage
insufficient every rational ratio IS captured: it is its own value at stage q
control      irrational ratios exist and are never captured (√5, and φ itself)
minimal      among the non-captured, M1⁺ canonization selects φ — owned upstream
```

**The M1 clause this instantiates.** §01.21.1 states it for rotation numbers: *any rational `p/q`
is captured at some finite stage, becoming indistinguishable from a periodic catalogue entry, hence
`⊥M1`*. The same clause is what selects the irrational Jones slot in
`D0-JONES-SLOT-SELECTOR-001`. Here it is carried as a floor: rationality is exactly capturability,
so a rational scale cannot be the self-consistent one.

**Why the control matters.** "Not captured at any finite stage" would force nothing if nothing
satisfied it. Irrationality is exhibited, so the obligation is a real requirement that rationals
fail and some reals meet.

**Where φ comes from, and where it does not.** This floor gets you to *irrational*, not to φ.
Narrowing the survivors to φ is the separate, already-repaired step
`D0-PHI-HURWITZ-CLASS-CANONIZATION-001`: Hurwitz selects the `GL(2,ℤ)` noble class, `M1⁺`
canonization selects its minimal-description representative, and `x² − x − 1 = 0` comes out as the
conclusion. Keeping the two apart is the point — collapsing them is exactly the error the route
audit found elsewhere, where a floor was credited with a conclusion its premises did not reach.

Honest scope: this owns *rationality ⇒ capture*. The identification of "capture at a finite stage"
with the operational readout stage is the reading, owned by §01.21.1.
-/

namespace D0.Foundation

/-- **The obligation.** A scale ratio is admissible only if no finite stage matches it exactly —
otherwise the ratio is indistinguishable from a periodic catalogue entry, which is the external
catalogue M1 forbids. Formally: the ratio is irrational. -/
def NonCaptured (r : ℝ) : Prop := Irrational r

/-- **`insufficient` — every rational scale is captured.** A rational ratio is exactly its own
value, so the requirement fails for the whole floor at once, not for some unlucky choice of `p/q`. -/
theorem rational_is_captured (q : ℚ) : ¬ NonCaptured (q : ℝ) :=
  Rat.not_irrational q

/-- Restated at the floor: no rational ratio whatever satisfies the obligation. -/
theorem rational_floor_insufficient : ¬ ∃ q : ℚ, NonCaptured (q : ℝ) := by
  rintro ⟨q, hq⟩
  exact rational_is_captured q hq

/-- **`control` — the obligation is satisfiable.** `√5` is irrational, so non-capture is a real
requirement and the floor's failure is an obstruction rather than an impossible demand. -/
theorem sqrt_five_non_captured : NonCaptured (Real.sqrt 5) := by
  simpa using (by norm_num : Nat.Prime 5).irrational_sqrt

/-- **`control` (the corpus's own survivor).** `φ = (1+√5)/2` is itself non-captured, so the
repair the cascade actually takes is admissible at this floor. -/
theorem phi_non_captured : NonCaptured ((1 + Real.sqrt 5) / 2) := by
  have h5 : Irrational (Real.sqrt 5) := by
    simpa using (by norm_num : Nat.Prime 5).irrational_sqrt
  rintro ⟨q, hq⟩
  exact h5 ⟨2 * q - 1, by push_cast; linarith [hq]⟩

/-- The floor is genuinely crossed: the repair `φ` satisfies exactly what every rational fails. -/
theorem floor_is_crossed :
    (¬ ∃ q : ℚ, NonCaptured (q : ℝ)) ∧ NonCaptured ((1 + Real.sqrt 5) / 2) :=
  ⟨rational_floor_insufficient, phi_non_captured⟩

/-- **`minimal` — this floor stops at "irrational", and says so.** Non-capture is satisfied by many
reals, `√5` among them, so it does not by itself select `φ`. The narrowing is the separate owned
step: Hurwitz selects the noble class and `M1⁺` canonization its minimal representative
(`D0.NumberTheory.HurwitzClassCanonization`), where the golden quadratic appears as the conclusion.
Stated here so the floor cannot be read as forcing more than it does. -/
theorem floor_does_not_select_phi :
    NonCaptured (Real.sqrt 5) ∧ NonCaptured ((1 + Real.sqrt 5) / 2) ∧
    Real.sqrt 5 ≠ (1 + Real.sqrt 5) / 2 := by
  refine ⟨sqrt_five_non_captured, phi_non_captured, ?_⟩
  intro h
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have hpos : 0 < Real.sqrt 5 := Real.sqrt_pos.mpr (by norm_num)
  nlinarith [h, h5, hpos]

/-- The upstream narrowing, cited not re-proved: within the period-one family the minimal-description
representative is `n = 1`, whose value is `(1+√5)/2` and whose equation `x² − x − 1 = 0` is the
output. -/
theorem narrowing_is_owned_upstream :
    D0.NumberTheory.periodOneValue 1 = (1 + Real.sqrt 5) / 2 :=
  D0.NumberTheory.periodOneValue_one_eq_phi

/-- **D0-CASCADE-FLOOR-SCALE-RATIO-001.** The rational-scale floor of the cascade, complete: every
rational ratio is captured and so fails the obligation; non-capture is satisfiable, witnessed twice;
the repair the corpus takes satisfies it; and the floor is explicitly *not* credited with selecting
`φ`, which is the separately owned canonization step. -/
theorem cascade_floor_scale_ratio :
    (∀ q : ℚ, ¬ NonCaptured (q : ℝ)) ∧
    NonCaptured (Real.sqrt 5) ∧
    NonCaptured ((1 + Real.sqrt 5) / 2) ∧
    Real.sqrt 5 ≠ (1 + Real.sqrt 5) / 2 ∧
    D0.NumberTheory.periodOneValue 1 = (1 + Real.sqrt 5) / 2 :=
  ⟨rational_is_captured, sqrt_five_non_captured, phi_non_captured,
   floor_does_not_select_phi.2.2, narrowing_is_owned_upstream⟩

end D0.Foundation
