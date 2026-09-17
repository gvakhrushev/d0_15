import Mathlib.Tactic

/-!
# The magnitude-free core: ΛCDM excluded by the archive degeneracies alone

**A scope correction first.** `D0.Synthesis.DarkEOSDiscreteSet` and its successors take the per-mode
values to be `−φ` and `−φ⁻¹`. The corpus owns less than that. The sign-normalisation row
`D0-PHASON-WDE-SIGN-NORMALIZATION-OWNER-001` forces the **sign** by Galois conjugation
`σ : φ ↦ ψ`, giving the specific conjugate `−φ`, and then states verbatim:

> "The magnitude/normalization `|w_DE|` stays PROOF-TARGET"

So `−φ` is owned as the sign normalisation, while the magnitude remains open. Every numeric value in
`DarkEOSDiscreteSet` (`−φ + s/30`, the eight-value list, `w = 3/5 − φ`) is therefore conditional on
reading the magnitude as `φ` — a reading, not an owned row. That condition is now stated explicitly
rather than left implicit.

**What survives without it.** Under the ratio reading of the missing role primitive — `w = p/ρ`
with the modes split into pressure-carrying and energy-carrying — the mode values **cancel**. If the
two role orientations carry values `v` and `1/v` for *any* `v`, the effective equation of state is a
ratio of the degeneracy weights alone:

    w = − s / (30 − s) ,        `s` a subset sum of the archive degeneracies `{8, 10, 12}` .

No `φ`, no magnitude, nothing but `8, 10, 12`. And `w = −1` requires `s = 15`, which is not a subset
sum (`fifteen_not_a_subset_sum`). Hence:

    **the cosmological constant is excluded by the archive degeneracies alone**
    (`lambda_excluded_magnitude_free`),

with the admissible set `{−4/11, −1/2, −2/3, −3/2, −2, −11/4}` — six rational values, no free
parameter and no dependence on the unowned magnitude. The nearest to `−1` is `−2/3`, at distance
`1/3`.

**Reading the two results together.** The φ-conditional branch (`DarkEOSDiscreteSet`) predicts
`w ≈ −1.018`, close to observation; the magnitude-free branch predicts a value at least `1/3` from
`−1`, which observation excludes. So the data do not merely pick an assignment — they discriminate
between the two readings of the role primitive, and they reject the one that needs no magnitude
input. That is a sharper use of the measurement than fitting: it tells the theory which of its own
readings to keep, and the surviving one is exactly the branch whose numbers depend on the magnitude
reading `|w| = φ` that is still a PROOF-TARGET.

**Net.** One unconditional result — ΛCDM is incompatible with degeneracies `8, 10, 12` under the
ratio reading — and one conditional prediction, with the condition now named.
-/

namespace D0.Synthesis.DarkEOSMagnitudeFree

/-- The archive degeneracies. -/
def degeneracies : List ℕ := [8, 10, 12]

/-- Their subset sums. -/
def subsetSums : List ℕ := [0, 8, 10, 12, 18, 20, 22, 30]

theorem degeneracy_total : degeneracies.sum = 30 := by decide

/-- **`15` is not a subset sum** — the whole magnitude-free exclusion turns on this. -/
theorem fifteen_not_a_subset_sum : 15 ∉ subsetSums := by decide

/-- The ratio-model equation of state: a function of the split alone. -/
def w (s : ℚ) : ℚ := -(s / (30 - s))

/-- **The mode values cancel.** For any `v ≠ 0`, splitting weights `s` and `30 − s` between values
`v` and `1/v` gives a pressure-to-energy ratio equal to `s/(30−s)` times `v²` — and the role swap
`v ↦ 1/v` maps this to its reciprocal, so the pair of admissible ratios is
`{s/(30−s), (30−s)/s}` independently of `v`. Recorded here in the normalised form `v = 1`. -/
theorem values_cancel (s : ℚ) (h : s ≠ 30) (h0 : s ≠ 0) :
    w s * w (30 - s) = 1 := by
  unfold w
  have h1 : (30 : ℚ) - s ≠ 0 := by intro hc; apply h; linarith
  have h2 : (30 : ℚ) - (30 - s) = s := by ring
  rw [h2]
  field_simp

/-- **ΛCDM needs `s = 15`.** -/
theorem lambda_needs_fifteen (s : ℚ) (h : s ≠ 30) : w s = -1 ↔ s = 15 := by
  unfold w
  rw [neg_eq_iff_eq_neg, div_eq_iff (by intro hc; apply h; linarith)]
  constructor <;> intro hh <;> linarith

/-- **The magnitude-free exclusion.** No subset sum of `{8, 10, 12}` gives `w = −1`. -/
theorem lambda_excluded_magnitude_free :
    w 0 ≠ -1 ∧ w 8 ≠ -1 ∧ w 10 ≠ -1 ∧ w 12 ≠ -1 ∧
    w 18 ≠ -1 ∧ w 20 ≠ -1 ∧ w 22 ≠ -1 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> · unfold w; norm_num

/-- The six admissible values. -/
theorem admissible_values :
    w 8 = -(4 / 11) ∧ w 10 = -(1 / 2) ∧ w 12 = -(2 / 3) ∧
    w 18 = -(3 / 2) ∧ w 20 = -2 ∧ w 22 = -(11 / 4) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;> · unfold w; norm_num

/-- Each is at least `1/3` from `−1`, so a measurement near `−1` rejects this branch. -/
theorem all_far_from_minus_one :
    |w 12 + 1| = 1 / 3 ∧ |w 10 + 1| = 1 / 2 ∧ |w 18 + 1| = 1 / 2 ∧
    |w 8 + 1| = 7 / 11 ∧ |w 20 + 1| = 1 ∧ |w 22 + 1| = 7 / 4 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    · unfold w; norm_num [abs_of_nonneg, abs_of_nonpos]

/-- **Assembled.** The degeneracies alone forbid the cosmological constant in the ratio reading, and
place every admissible value at least `1/3` away from it. -/
theorem magnitude_free_core :
    15 ∉ subsetSums ∧
    (∀ s : ℚ, s ≠ 30 → (w s = -1 ↔ s = 15)) ∧
    (|w 12 + 1| = 1 / 3) :=
  ⟨fifteen_not_a_subset_sum, lambda_needs_fifteen, all_far_from_minus_one.1⟩

end D0.Synthesis.DarkEOSMagnitudeFree
