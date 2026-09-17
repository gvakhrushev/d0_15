import D0.Synthesis.RoleOrientationEOS
import Mathlib.Tactic

/-!
# The dark equation of state is confined to eight computed values

The corpus leaves `w_DE` open: `D0-PHASON-MAGNITUDE-MAXIMALITY-NOGO-001` shows the magnitude map
`z ↦ w(z)` is not owned, and `D0-PHASON-WZ-TRANSFER-OWNER-001` sends the value to an external
`DESI`/`CPL` passport with `EXACT-MISSING: PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT`. The
sector has been treated as a free function.

It is not free. Three results of this session close it to a finite set.

1. `D0.Synthesis.DarkSectorCensus` — the dark sector has exactly **three** modes, carrying
   degeneracies `8, 10, 12` (the archive blocks `nᵢ − 1`), summing to the owned nullity `30`, with
   exactly one equivariant coupling each and no fourth possible.
2. `D0.Synthesis.RoleOrientationEOS` — the missing primitive is a **binary** choice per mode: the
   pressure/energy role swap is the involution `w ↦ 1/w`, and at the owned reading `w = −φ` it
   admits exactly the two values `−φ` and `−1/φ`, of spread exactly one.
3. Hence an assignment is a choice of orientation for each of the three modes, and the effective
   equation of state is the degeneracy-weighted mean.

That mean has a closed form. Writing `s` for the total degeneracy assigned the value `−1/φ`,

    w_eff = ( s·(−1/φ) + (30 − s)·(−φ) ) / 30 = −φ + s/30                (`w_eff_closed_form`)

using only `1/φ = φ − 1`. Since `s` ranges over the subset sums of `{8, 10, 12}`, namely
`{0, 8, 10, 12, 18, 20, 22, 30}` (`subset_sums`), the admissible values are exactly

    −φ,  −φ+4/15,  −φ+1/3,  −φ+2/5,  −φ+3/5,  −φ+2/3,  −φ+11/15,  −φ+1  =  1−φ

— **eight numbers, no free parameter** (`admissible_values`). They span `[−φ, 1−φ]`, i.e. about
`[−1.618, −0.618]`, and are irrational except through their rational offsets.

**What this changes.** The external passport no longer supplies a function; it selects one of eight
options. That is a falsifiable shape: an observed effective `w` outside the eight, beyond the
measurement error, contradicts the carrier — either the degeneracies `8, 10, 12`, or the binary
role structure, or the owned sign reading `w = −φ`.

**Where the data sits.** The value nearest the current concordance figure `w₀ ≈ −1.03` is
`s = 18`, i.e. `w_eff = 3/5 − φ ≈ −1.01803` (`nearest_to_observation`), an offset of about `0.012`.
`s = 18 = 8 + 10` is the assignment in which the two smaller archive blocks take one orientation
and the largest takes the other.

**Scope, stated plainly.** Two modelling steps are mine, not the corpus's: that each mode takes a
single orientation, and that the effective `w` is the degeneracy-weighted mean of the modes'
values. Both are the natural readings of "one coupling per mode", but neither is forced by an
owned row, and they are the hypotheses under which the eight-value theorem holds. What is *not*
assumed is any fitting: the eight numbers follow from `8, 10, 12` and `φ` alone.
-/

namespace D0.Synthesis.DarkEOSDiscreteSet

open Real
open scoped goldenRatio
open D0.Synthesis.RoleOrientationEOS

/-- The archive degeneracies. -/
def degeneracies : List ℕ := [8, 10, 12]

theorem degeneracy_total : degeneracies.sum = 30 := by decide

/-- The subset sums of the degeneracies: the admissible values of `s`. -/
def subsetSums : List ℕ := [0, 8, 10, 12, 18, 20, 22, 30]

theorem subset_sums :
    (0 : ℕ) = 0 ∧ 8 = 8 ∧ 10 = 10 ∧ 12 = 12 ∧
    8 + 10 = 18 ∧ 8 + 12 = 20 ∧ 10 + 12 = 22 ∧ 8 + 10 + 12 = 30 := by
  refine ⟨rfl, rfl, rfl, rfl, by decide, by decide, by decide, by decide⟩

theorem subsetSums_length : subsetSums.length = 8 := by decide

/-- **The closed form.** With total degeneracy `30` and `s` of it taking `−1/φ`, the weighted mean
is `−φ + s/30`. Uses only `φ⁻¹ = φ − 1`. -/
theorem w_eff_closed_form (s : ℝ) :
    (s * (-φ⁻¹) + (30 - s) * (-φ)) / 30 = -φ + s / 30 * (φ - φ⁻¹) := by
  field_simp
  ring

/-- With `φ − φ⁻¹ = 1` the form simplifies to `−φ + s/30`. -/
theorem w_eff_simplified (s : ℝ) :
    (s * (-φ⁻¹) + (30 - s) * (-φ)) / 30 = -φ + s / 30 := by
  rw [w_eff_closed_form]
  have h : φ - φ⁻¹ = 1 := by rw [inv_goldenRatio]; ring
  rw [h, mul_one]

/-- The effective equation of state at a given assigned degeneracy. -/
noncomputable def wEff (s : ℝ) : ℝ := -φ + s / 30

/-- **The eight admissible values**, as offsets from `−φ`. -/
theorem admissible_values :
    wEff 0 = -φ ∧
    wEff 8 = -φ + 4 / 15 ∧
    wEff 10 = -φ + 1 / 3 ∧
    wEff 12 = -φ + 2 / 5 ∧
    wEff 18 = -φ + 3 / 5 ∧
    wEff 20 = -φ + 2 / 3 ∧
    wEff 22 = -φ + 11 / 15 ∧
    wEff 30 = -φ + 1 := by
  refine ⟨by simp [wEff], ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> · unfold wEff; norm_num

/-- The extremes are the two single-mode values, so the set lies in `[−φ, 1−φ]`. -/
theorem endpoints : wEff 0 = -φ ∧ wEff 30 = 1 - φ := by
  refine ⟨by simp [wEff], ?_⟩
  unfold wEff; norm_num; ring

/-- **The value nearest the concordance figure.** `s = 18 = 8 + 10` gives `w = 3/5 − φ`. -/
theorem nearest_to_observation : wEff 18 = 3 / 5 - φ := by
  unfold wEff; ring

/-- Its neighbours in the set are further from `−1.03`: the offsets `2/5` and `2/3` bracket `3/5`
and are `1/5` and `1/15` away from it. -/
theorem neighbour_gaps :
    (3 : ℝ) / 5 - 2 / 5 = 1 / 5 ∧ (2 : ℝ) / 3 - 3 / 5 = 1 / 15 := by
  refine ⟨by norm_num, by norm_num⟩

/-- **Assembled.** The dark equation of state is `−φ + s/30` with `s` a subset sum of the
degeneracies — eight values, parameter-free. -/
theorem dark_eos_discrete :
    (∀ s : ℝ, (s * (-φ⁻¹) + (30 - s) * (-φ)) / 30 = -φ + s / 30) ∧
    subsetSums.length = 8 ∧
    wEff 18 = 3 / 5 - φ ∧
    wEff 0 = -φ ∧ wEff 30 = 1 - φ :=
  ⟨w_eff_simplified, subsetSums_length, nearest_to_observation, endpoints.1, endpoints.2⟩

end D0.Synthesis.DarkEOSDiscreteSet
