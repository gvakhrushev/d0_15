import D0.Geometry.TorusCore13GeometryOrigin
import Mathlib.Tactic

/-!
# R2 — TorusShell structural attachment (DRAFT; lives in _TASKS_CENTER_ATTACK until minted)

Closes the named gap of `T2_PRIME_REVIEW_VERDICT.md` §2 / `R1_FINAL_STATE.md` R2: the abbrev chain
`GenerationPhasonMode := PhasonMode := TorusShell` transports only `card = 3`, because no Lean map
attaches the `TorusShell` constructors to the `Shell3` radial machinery or to the zone data their
names carry (`innerD9/coreD11/outerD13` are bare spellings). This module supplies the attachment:

* `toShell3 : TorusShell ≃ Fin 3` — the radial-order equivalence (inner ↦ 0, core ↦ 1, outer ↦ 2),
  making the radial machinery (`shellRadius`, `radialAdjacency`, `phaseDrift`, the commutator
  theorems) available on the generation carrier itself;
* `zoneSize / zoneDegree : TorusShell → ℕ` — the zone data the constructor names promise, with the
  closure theorem `zoneDegree = 33 − zoneSize` (complete-tripartite degree law);
* radius facts: the inner shell is the parameter-independent unit shell, and radii are strictly
  increasing along the constructor order for every admissible torus parameter (`1 < a`).

Nothing here is a physical claim: this is carrier plumbing (an equivalence and two label maps),
promotable only via the closure protocol. No status row is created or edited.
-/

namespace D0.Geometry

open TorusParameter

/-- Radial-order attachment of the named shells to the `Shell3 = Fin 3` carrier. -/
def TorusShell.toShell3 : TorusShell → Shell3
  | .innerD9  => 0
  | .coreD11  => 1
  | .outerD13 => 2

/-- Inverse attachment. -/
def TorusShell.ofShell3 : Shell3 → TorusShell :=
  fun i => if i = 0 then .innerD9 else if i = 1 then .coreD11 else .outerD13

/-- The attachment is an equivalence: the generation carrier IS the radial carrier. -/
def torusShellEquivShell3 : TorusShell ≃ Shell3 where
  toFun := TorusShell.toShell3
  invFun := TorusShell.ofShell3
  left_inv := by intro s; cases s <;> rfl
  right_inv := by intro i; fin_cases i <;> rfl

/-- Zone size carried by each shell's name. -/
def TorusShell.zoneSize : TorusShell → ℕ
  | .innerD9  => 9
  | .coreD11  => 11
  | .outerD13 => 13

/-- Zone degree carried by each shell's name (complete tripartite on 33 vertices). -/
def TorusShell.zoneDegree : TorusShell → ℕ
  | .innerD9  => 24
  | .coreD11  => 22
  | .outerD13 => 20

/-- Degree law: on `K(9,11,13)` every zone's degree is `33 − |zone|`. -/
theorem torusShell_degree_law :
    ∀ s : TorusShell, s.zoneDegree = 33 - s.zoneSize := by
  intro s; cases s <;> rfl

/-- Zone sizes are strictly increasing along the radial order (the +2 ladder). -/
theorem torusShell_zoneSize_ladder :
    TorusShell.zoneSize .innerD9 + 2 = TorusShell.zoneSize .coreD11 ∧
    TorusShell.zoneSize .coreD11 + 2 = TorusShell.zoneSize .outerD13 := by
  exact ⟨rfl, rfl⟩

/-- Radius readout on the generation carrier, through the attachment. -/
def TorusShell.radius (T : TorusParameter) (s : TorusShell) : ℚ :=
  T.shellRadius s.toShell3

/-- Reduction lemmas for the radial readout on the three shells. -/
theorem torusShell_radius_inner (T : TorusParameter) :
    TorusShell.radius T .innerD9 = T.inner := rfl
theorem torusShell_radius_core (T : TorusParameter) :
    TorusShell.radius T .coreD11 = T.core := rfl
theorem torusShell_radius_outer (T : TorusParameter) :
    TorusShell.radius T .outerD13 = T.outer := rfl

/-- The inner shell is the parameter-independent unit shell. -/
theorem torusShell_inner_unit (T : TorusParameter) :
    TorusShell.radius T .innerD9 = 1 := rfl

/-- Radii are strictly increasing along the constructor (radial) order, for every `1 < a`. -/
theorem torusShell_radius_strictMono (T : TorusParameter) :
    TorusShell.radius T .innerD9 < TorusShell.radius T .coreD11 ∧
    TorusShell.radius T .coreD11 < TorusShell.radius T .outerD13 := by
  have h := T.h_gt_one
  refine ⟨?_, ?_⟩
  · rw [torusShell_radius_inner, torusShell_radius_core]
    show (1 : ℚ) < (T.a + 1) / 2
    linarith
  · rw [torusShell_radius_core, torusShell_radius_outer]
    show (T.a + 1) / 2 < T.a
    linarith

end D0.Geometry
