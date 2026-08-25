import Mathlib.Tactic
import D0.Foundation.CascadeFloorProofreading

/-!
# The arrow interlock: equilibrium pathways of ANY depth collapse — irreversibility is
forced for verified records

**Upgrade of the proofreading floor's insufficiency from depth 1 to ALL depths.** The
floor (`D0-CASCADE-FLOOR-PROOFREADING-001`) proved that ONE equilibrium test cannot reach
the proofread error level `errOf (δ²)`. The obvious escape — "then take many equilibrium
tests in sequence" — is closed here: an equilibrium pathway's stage factors TELESCOPE to
the endpoint ratio (detailed balance: stationary discrimination depends only on the
endpoint energies, not on the intermediate structure — the cited external content, the
path-independence of equilibrium constants; Hopfield 1974's own starting point, cited as
the physical reading of the carrier definition, docstring grade, not load-bearing). In
the model: an equilibrium pathway is a nonempty list of positive stage factors whose
product IS the endpoint ratio `δ`. Theorems:

1. `equilibrium_collapses_to_one_test`: every equilibrium pathway IS extensionally a
   single test — the collapse as a statement about the carriers, any depth;
2. `equilibrium_depth_collapse`: no equilibrium pathway of ANY depth reaches
   `errOf (δ²)` — the floor's insufficiency is depth-universal;
3. `repair_breaks_equilibrium`: the proofreading repair's stage product `δ²` cannot
   telescope to the endpoint ratio `δ` (for `0 < δ < 1`) — the repair carrier lies
   OUTSIDE the equilibrium class: the exit from equilibrium is FORCED;
4. assembly `interlock_proofreading_arrow`.

**The interlock reading (graded).** The Lean-forced part, exactly: no carrier
representable as a nonempty positive factor list telescoping to `δ` reaches `errOf (δ²)`
at any depth, while the two-stage carrier does — the necessity is CLASS-RELATIVE.
Reading class-exit as "some step must break detailed balance" is the cited
defining-hypothesis gloss, NOT Lean-forced; carriers not representable as factor lists
are outside the statement; no exhaustion of un-modeled carrier shapes is claimed. The
identification of the class-exit with the time arrow's owned carrier (Pisot
expansion/contraction, `D0-PISOT-CONTRACTION-TIME-ARROW-001`) is DOCSTRING-ANCHORED new
prose with no book-prose owner yet and no arrow-side formal object — strictly BELOW
interlock link 4's grade (link 4 has the independently owned §03.23.5); the book-prose
target (a §01.6.1c arrow-interlock subsection with a §06.36 cross-reference) is the named
continuation. What is new relative to the floor: equilibrium alternatives of every depth
are now provably insufficient, so within the modeled class the exit is necessary, not
stipulated.

**Honest scope (pre-registered).**
1. The equilibrium class (product = endpoint ratio) is a DEFINING hypothesis carrying the
   cited detailed-balance structure; a rival record semantics would need its own class.
2. `repair_breaks_equilibrium` is elementary arithmetic (`δ² ≠ δ`); its content is the
   WIRING: the same product that the two-stage carrier needs is the one the equilibrium
   class forbids.
3. No claim about the arrow floor's own content is made or needed; no biochemical claim;
   no n-stage floor family (the ladder caveat of the floor row stands).
-/

namespace D0.Foundation

/-- The equilibrium-pathway carrier: a nonempty list of positive stage factors whose
product telescopes to the endpoint ratio `δ` (detailed balance — discrimination depends
only on endpoint energies). `target` is reached if the compound error meets it. -/
def EquilibriumPathReaches (δ target : ℚ) : Prop :=
  ∃ fs : List ℚ, fs ≠ [] ∧ (∀ f ∈ fs, 0 < f) ∧ fs.prod = δ ∧ errOf fs.prod ≤ target

/-- **Non-vacuity of the equilibrium class**: it is inhabited at every depth ≥ 1 — the
singleton `[δ]` and the padded `[δ, 1]` both telescope to `δ` and reach the one-test
error level. The depth-universal insufficiency below is therefore an obstruction over an
inhabited class, not a statement about an empty one. -/
theorem equilibrium_class_inhabited (δ : ℚ) (h₀ : 0 < δ) :
    EquilibriumPathReaches δ (errOf δ) ∧
      ∃ fs : List ℚ, fs.length = 2 ∧ fs ≠ [] ∧ (∀ f ∈ fs, 0 < f) ∧ fs.prod = δ :=
  ⟨⟨[δ], by simp, by simpa using h₀, by simp, by simp⟩,
    ⟨[δ, 1], by simp, by simp, by
      intro f hf
      rcases List.mem_pair.mp hf with rfl | rfl
      · exact h₀
      · norm_num, by simp⟩⟩

/-- **The collapse, as a carrier statement**: every equilibrium pathway is extensionally
a single test — whatever an equilibrium pathway reaches, one test at the endpoint ratio
reaches. Depth adds nothing at equilibrium. -/
theorem equilibrium_collapses_to_one_test {δ target : ℚ}
    (h : EquilibriumPathReaches δ target) : OneTestReaches δ target := by
  obtain ⟨fs, _, _, hprod, herr⟩ := h
  exact ⟨δ, le_refl δ, by rwa [hprod] at herr⟩

/-- **Depth-universal insufficiency**: no equilibrium pathway of ANY depth reaches the
proofread error level. The proofreading floor's insufficiency survives arbitrary
equilibrium depth — the "just add more equilibrium tests" escape is closed. -/
theorem equilibrium_depth_collapse (δ : ℚ) (h₀ : 0 < δ) (h₁ : δ < 1) :
    ¬ EquilibriumPathReaches δ (errOf (δ * δ)) := fun h =>
  one_test_insufficient δ h₀ h₁ (equilibrium_collapses_to_one_test h)

/-- **The exit is forced**: the proofreading repair's stage product `δ²` cannot telescope
to the endpoint ratio `δ` — the repair carrier lies outside the equilibrium class, so
some step must break detailed balance. -/
theorem repair_breaks_equilibrium (δ : ℚ) (h₀ : 0 < δ) (h₁ : δ < 1) :
    δ * δ ≠ δ := by nlinarith

/-- **Assembly (the arrow interlock, Lean-forced part)**: equilibrium pathways of every
depth fail the proofread level; the two-stage repair reaches it; and the repair's product
is un-telescopable — the exit from equilibrium is necessary, not stipulated. The
identification of the exit with the time arrow's owned carrier is prose-anchored (module
docstring), not part of this statement. -/
theorem interlock_proofreading_arrow (δ : ℚ) (h₀ : 0 < δ) (h₁ : δ < 1) :
    (¬ EquilibriumPathReaches δ (errOf (δ * δ)))
      ∧ TwoStageReaches δ (errOf (δ * δ))
      ∧ δ * δ ≠ δ :=
  ⟨equilibrium_depth_collapse δ h₀ h₁, two_stage_control δ,
    repair_breaks_equilibrium δ h₀ h₁⟩

end D0.Foundation
