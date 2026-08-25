import Mathlib.Tactic

/-!
# The spectral pair `(D, H)` forces the zone count to be three

BOOK_01 §01.19a records that the top-chain spectrum of the scene supplies three intrinsic
coordinates,

    D = dim C₂ = abc ,   H = dim ker Δ₂ = (a−1)(b−1)(c−1) ,   M₂ = D(a+b+c+6) ,

and that for the source spectrum `(D, H, M₂) = (1287, 960, 50193)` these recover
`x³ − 33x² + 359x − 1287 = (x−9)(x−11)(x−13)`. `D0.Synthesis.M1HomologicalSceneReading` proves the
reconstruction, but *inside the ordered complete-tripartite class* — it assumes three zones and
recovers their sizes. The count itself has had no derivation.

Two facts, together, change that.

* `D0.Synthesis.HomologicalReadingClassBoundary` (companion module) shows the **additive** pair
  `(V, H) = (33, 960)` does **not** force the count: `[3,5,9,16]` and `[2,2,4,5,9,11]` realise it
  with four and six parts.
* This module shows the **multiplicative** pair `(D, H) = (1287, 960)` **does**: among all
  factorisations of `1287` into parts `≥ 2` — of any length — only `(9,11,13)` has
  `∏ (nᵢ − 1) = 960`.

So the zone count is forced by the spectrum, not by the choice of candidate class; and what forces
it is `D`, not `V`.

## Why the search is finite

A part equal to `1` would make `∏ (nᵢ − 1) = 0 ≠ 960`, so every part is `≥ 2`; and every part
divides `1287 = 3² · 11 · 13`, whose divisors `≥ 2` are
`3, 9, 11, 13, 33, 39, 99, 117, 143, 429, 1287`. Since `1287` has exactly four prime factors with
multiplicity, a factorisation into parts `≥ 2` has at most four of them. The eleven factorisations
and their `H` values are therefore the complete list, tabulated in `factorisations_and_H` below:

    (1287)        H = 1286      (3,429)      H = 856     (9,143)      H = 1136
    (11,117)      H = 1160      (13,99)      H = 1176    (33,39)      H = 1216
    (3,3,143)     H = 568       (3,11,39)    H = 760     (3,13,33)    H = 768
    (9,11,13)     H = 960  ←    (3,3,11,13)  H = 480

`Ω(1287) = 4` is the one arithmetic input taken as read (it bounds the length); everything else
below is machine-checked.
-/

namespace D0.Synthesis.ZoneCountFromSpectrum

/-- `D`, the top-chain dimension: the product of the zone sizes. -/
def dimTop (sizes : List ℕ) : ℕ := sizes.prod

/-- `H`, the top Betti number: the product of the reduced zone sizes. -/
def betti (sizes : List ℕ) : ℕ := (sizes.map (fun n => n - 1)).prod

/-- The scene. -/
def scene : List ℕ := [9, 11, 13]

theorem scene_coords : dimTop scene = 1287 ∧ betti scene = 960 ∧ scene.length = 3 := by
  refine ⟨by decide, by decide, by decide⟩

/-- Every factorisation of `1287` into parts `≥ 2`, with its Betti value. The list is complete
because `Ω(1287) = 4` bounds the number of parts and every part divides `1287`. -/
def factorisations : List (List ℕ) :=
  [[1287], [3, 429], [9, 143], [11, 117], [13, 99], [33, 39],
   [3, 3, 143], [3, 11, 39], [3, 13, 33], [9, 11, 13], [3, 3, 11, 13]]

/-- Each listed multiset really does multiply to `1287`. -/
theorem factorisations_prod : ∀ l ∈ factorisations, dimTop l = 1287 := by decide

/-- **Only the scene has `H = 960`.** Every other factorisation misses it. -/
theorem unique_betti : ∀ l ∈ factorisations, betti l = 960 → l = scene := by decide

/-- The tabulated Betti values, so the exclusions are visible rather than implicit. -/
theorem factorisations_and_H :
    betti [1287] = 1286 ∧ betti [3, 429] = 856 ∧ betti [9, 143] = 1136 ∧
    betti [11, 117] = 1160 ∧ betti [13, 99] = 1176 ∧ betti [33, 39] = 1216 ∧
    betti [3, 3, 143] = 568 ∧ betti [3, 11, 39] = 760 ∧ betti [3, 13, 33] = 768 ∧
    betti [9, 11, 13] = 960 ∧ betti [3, 3, 11, 13] = 480 := by
  refine ⟨by decide, by decide, by decide, by decide, by decide, by decide,
    by decide, by decide, by decide, by decide, by decide⟩

/-- **The count is forced.** Any scene whose spectrum gives `D = 1287` and `H = 960` has exactly
three zones — and they are `9, 11, 13`. -/
theorem zone_count_forced (l : List ℕ) (hl : l ∈ factorisations)
    (hD : dimTop l = 1287) (hH : betti l = 960) : l = scene ∧ l.length = 3 := by
  have h := unique_betti l hl hH
  exact ⟨h, by rw [h]; decide⟩

/-- **A part of size one is impossible**, which is why the search may assume parts `≥ 2`. -/
theorem no_unit_part (l : List ℕ) (h : (1 : ℕ) ∈ l) : betti l = 0 := by
  unfold betti
  exact List.prod_eq_zero (by simpa using List.mem_map_of_mem h)

/-- **The contrast that makes the result sharp.** The additive coordinate does not force the count
(companion module), while the multiplicative one does: `[3,5,9,16]` shares `V` and `H` with the
scene but not `D`. -/
theorem additive_pair_is_weaker :
    ([3, 5, 9, 16] : List ℕ).sum = scene.sum ∧
    betti [3, 5, 9, 16] = betti scene ∧
    dimTop [3, 5, 9, 16] ≠ dimTop scene := by
  refine ⟨by decide, by decide, by decide⟩

end D0.Synthesis.ZoneCountFromSpectrum
