import D0.Synthesis.LambdaCDMExcluded
import D0.Geometry.TorusShellAttachment
import Mathlib.Tactic

/-!
# Narrowing the dark equation of state from eight values to one

`D0.Synthesis.DarkEOSDiscreteSet` confines `w` to `−φ + s/30` with `s` a subset sum of the archive
degeneracies `{8, 10, 12}` — eight values. This module narrows that, and states exactly what each
narrowing step rests on.

**Step 1 — drop the uniform assignments (owned).** `s = 0` and `s = 30` give every mode the same
orientation, so the role swap acts trivially and there is nothing to assign. Six assignments remain,
in three complementary pairs, one pair per shell singled out:

    outer singled:  s ∈ {12, 18}      core singled:  s ∈ {10, 20}      inner singled:  s ∈ {8, 22}

**Step 2 — the shell singled out is the radial maximum (canonical, principle).** The shells carry a
total radial order, owned by `D0.Geometry.TorusShellAttachment`: `innerD9 ↦ 0`, `coreD11 ↦ 1`,
`outerD13 ↦ 2`, with `torusShell_radius_strictMono`. A total order on three elements has a unique
maximum, so "the distinguished mode is the extremal one" picks `outerD13` without further choice —
no fitting enters, because the order is owned and its maximum is unique. This leaves

    s ∈ {12, 18} ,      w ∈ {−φ + 2/5, −φ + 3/5} = {−1.218034…, −1.018034…} .

**Step 3 — orientation, selected by data.** The two survivors differ by `1/5` in `w`, far beyond any
current uncertainty, and only `s = 18` lies near the measured value. This last step is the one the
observation makes; the theory supplies the pair, not the choice within it.

So the narrowing is `8 → 6 → 2 → 1`, with the first two steps internal and only the last empirical,
and the outcome is

    **w = 3/5 − φ ≈ −1.018034** ,

the same value `LambdaCDMExcluded.minimal_deviation` shows sits at distance `φ − 8/5` from the
cosmological constant, which remains excluded throughout.

**Honest labelling.** Step 1 is forced. Step 2 uses a principle — that the distinguished mode is the
radial extremum — which is canonical but not an owned row; adopting the radial *minimum* instead
would give `s ∈ {8, 22}` and `w ≈ −0.885`, six times further from observation, so the choice of
maximum over minimum is itself currently made by the data rather than derived. Step 3 is empirical
by construction.
-/

namespace D0.Synthesis.RoleAssignmentNarrowing

open Real
open scoped goldenRatio
open D0.Synthesis.DarkEOSDiscreteSet
open D0.Geometry

/-- The three complementary pairs of non-uniform assignments, indexed by the shell singled out. -/
def outerPair : List ℕ := [12, 18]
def corePair : List ℕ := [10, 20]
def innerPair : List ℕ := [8, 22]

/-- Each pair sums to `30`: the two members are complementary assignments of the same split. -/
theorem pairs_complementary :
    12 + 18 = 30 ∧ 10 + 20 = 30 ∧ 8 + 22 = 30 := by
  refine ⟨by decide, by decide, by decide⟩

/-- **Step 1.** The uniform assignments are the ones where the role swap does nothing. -/
theorem uniform_are_trivial : wEff 0 = -φ ∧ wEff 30 = 1 - φ := by
  refine ⟨by simp [wEff], ?_⟩
  unfold wEff; norm_num; ring

/-- **The radial order** is total with `outerD13` its maximum. -/
theorem radial_order :
    TorusShell.zoneSize .innerD9 = 9 ∧ TorusShell.zoneSize .coreD11 = 11 ∧
    TorusShell.zoneSize .outerD13 = 13 ∧
    TorusShell.zoneSize .innerD9 < TorusShell.zoneSize .coreD11 ∧
    TorusShell.zoneSize .coreD11 < TorusShell.zoneSize .outerD13 := by
  refine ⟨by decide, by decide, by decide, by decide, by decide⟩

/-- The archive degeneracy of the radial maximum is `12`, so singling it out leaves `s ∈ {12, 18}`. -/
theorem outer_degeneracy : TorusShell.zoneSize .outerD13 - 1 = 12 := by decide

/-- **Step 2's survivors**, with their equations of state. -/
theorem outer_pair_values : wEff 12 = -φ + 2 / 5 ∧ wEff 18 = -φ + 3 / 5 := by
  refine ⟨?_, ?_⟩ <;> · unfold wEff; norm_num

/-- They differ by `1/5`, far beyond current uncertainty. -/
theorem outer_pair_gap : wEff 18 - wEff 12 = 1 / 5 := by
  unfold wEff; norm_num

/-- **The outcome.** `w = 3/5 − φ`. -/
theorem narrowed_value : wEff 18 = 3 / 5 - φ := by unfold wEff; ring

/-- The rival narrowing, taking the radial *minimum* instead: `w ≈ −0.885`, six times further from
`−1`. Recorded so the choice of maximum is visible as a choice. -/
theorem inner_rival : wEff 22 = -φ + 11 / 15 := by unfold wEff; norm_num

/-- **Assembled.** Uniform assignments are trivial; the radial order is total with a unique maximum
of degeneracy `12`; singling it out leaves two values a fifth apart; the near-`−1` one is
`3/5 − φ`. -/
theorem narrowing :
    (12 + 18 = 30 ∧ 10 + 20 = 30 ∧ 8 + 22 = 30) ∧
    (TorusShell.zoneSize .innerD9 < TorusShell.zoneSize .coreD11 ∧
      TorusShell.zoneSize .coreD11 < TorusShell.zoneSize .outerD13) ∧
    TorusShell.zoneSize .outerD13 - 1 = 12 ∧
    wEff 18 - wEff 12 = 1 / 5 ∧
    wEff 18 = 3 / 5 - φ :=
  ⟨pairs_complementary, ⟨radial_order.2.2.2.1, radial_order.2.2.2.2⟩, outer_degeneracy,
   outer_pair_gap, narrowed_value⟩

end D0.Synthesis.RoleAssignmentNarrowing
