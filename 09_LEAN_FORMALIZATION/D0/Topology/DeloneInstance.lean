import D0.Dynamics.PisotContraction
import Mathlib.Analysis.AperiodicOrder.Delone.Basic
import Mathlib.Algebra.Order.Round
import Mathlib.Tactic

/-!
# D0-DELONE-PHI-001 — the D0 φ-quasicrystal carrier as a genuine Mathlib `Delone.DeloneSet ℝ`

The D0 hull's point set is the golden-ratio Beatty / 1-D cut-and-project set
`{ ⌊nφ⌋ : n ∈ ℤ } ⊂ ℝ` (the canonical Sturmian/Fibonacci quasicrystal on the line). This module
proves it is a genuine **Delone set** in the sense of `Mathlib.Analysis.AperiodicOrder.Delone`:
uniformly discrete (packing radius `1/2` — distinct points are distinct integers, hence `≥ 1` apart)
and relatively dense (covering radius `2` — consecutive points are `< 2` apart, since `1 < φ < 2`).

This replaces the former vacuous `D0.Topology.TilingHull` `Prop := true` stub (the over-claim corrected
this iteration) with a real Mathlib-typed object. Deriving finite-local-complexity / aperiodicity *as
`DeloneSet` consequences* stays a theorem-target (those downstream theorems are absent from the pin);
the underlying aperiodicity is already proved number-theoretically (`D0.Claims.KTheoryGapModule`).
-/

namespace D0.Topology

open Metric D0
open scoped NNReal ENNReal

/-- The Beatty / 1-D cut-and-project point set of the golden ratio: position `⌊nφ⌋` for each `n ∈ ℤ`. -/
noncomputable def beattyPhi (n : ℤ) : ℝ := (⌊(n : ℝ) * phi⌋ : ℝ)

/-- The D0 φ-quasicrystal carrier as a subset of the line. -/
def d0BeattyCarrier : Set ℝ := Set.range beattyPhi

/-- `φ < 2` (since `√5 < 3`). -/
theorem phi_lt_two : phi < 2 := by
  unfold phi; nlinarith [sqrt_five_lt_three]

/-- The Beatty floor is strictly monotone: `m < n ⟹ ⌊mφ⌋ < ⌊nφ⌋` (because the gap `(n−m)φ ≥ φ > 1`). -/
theorem beatty_floor_lt {m n : ℤ} (h : m < n) : ⌊(m : ℝ) * phi⌋ < ⌊(n : ℝ) * phi⌋ := by
  have hphi1 : (1 : ℝ) < phi := phi_gt_one
  have hcast : (m : ℝ) + 1 ≤ (n : ℝ) := by exact_mod_cast h
  have hgap : (m : ℝ) * phi + 1 ≤ (n : ℝ) * phi := by nlinarith [hphi1, hcast]
  have key : ((⌊(m : ℝ) * phi⌋ + 1 : ℤ) : ℝ) ≤ (n : ℝ) * phi := by
    push_cast
    have hfl : (⌊(m : ℝ) * phi⌋ : ℝ) ≤ (m : ℝ) * phi := Int.floor_le _
    linarith [hgap, hfl]
  have hle : ⌊(m : ℝ) * phi⌋ + 1 ≤ ⌊(n : ℝ) * phi⌋ := Int.le_floor.mpr key
  omega

/-- Distinct `n` give distinct Beatty floors. -/
theorem beatty_floor_ne {m n : ℤ} (hmn : m ≠ n) : ⌊(m : ℝ) * phi⌋ ≠ ⌊(n : ℝ) * phi⌋ := by
  rcases lt_or_gt_of_ne hmn with h | h
  · exact (beatty_floor_lt h).ne
  · exact (beatty_floor_lt h).ne'

/-- Distinct Beatty points are at least `1` apart (they are distinct integers). -/
theorem beatty_dist_ge_one {m n : ℤ} (hmn : m ≠ n) :
    (1 : ℝ) ≤ dist (beattyPhi m) (beattyPhi n) := by
  have hfne : ⌊(m : ℝ) * phi⌋ ≠ ⌊(n : ℝ) * phi⌋ := beatty_floor_ne hmn
  have hz : (1 : ℤ) ≤ |⌊(m : ℝ) * phi⌋ - ⌊(n : ℝ) * phi⌋| :=
    Int.one_le_abs (sub_ne_zero.mpr hfne)
  rw [Real.dist_eq]; simp only [beattyPhi]
  exact_mod_cast hz

/-- Every real is within `2` of a Beatty point: take `n = round(x/φ)`; then
`|x − ⌊nφ⌋| ≤ |x − nφ| + (nφ − ⌊nφ⌋) ≤ φ/2 + (< 1) < 2` because `1 < φ < 2`. -/
theorem beatty_cover (x : ℝ) : dist x (beattyPhi (round (x / phi))) ≤ 2 := by
  have hphi0 : (0 : ℝ) < phi := by linarith [phi_gt_one]
  have hphi2 : phi < 2 := phi_lt_two
  set n := round (x / phi) with hn
  have hround : |x / phi - (n : ℝ)| ≤ 1 / 2 := abs_sub_round (x / phi)
  have hxn : |x - (n : ℝ) * phi| ≤ phi / 2 := by
    have hrw : x - (n : ℝ) * phi = phi * (x / phi - (n : ℝ)) := by field_simp
    rw [hrw, abs_mul, abs_of_pos hphi0]
    nlinarith [hround, hphi0]
  have hfl_le : (⌊(n : ℝ) * phi⌋ : ℝ) ≤ (n : ℝ) * phi := Int.floor_le _
  have hfl_lt : (n : ℝ) * phi < (⌊(n : ℝ) * phi⌋ : ℝ) + 1 := Int.lt_floor_add_one _
  rw [Real.dist_eq]; simp only [beattyPhi]
  have htri : |x - (⌊(n : ℝ) * phi⌋ : ℝ)| ≤
      |x - (n : ℝ) * phi| + |(n : ℝ) * phi - (⌊(n : ℝ) * phi⌋ : ℝ)| := abs_sub_le _ _ _
  have hfrac : |(n : ℝ) * phi - (⌊(n : ℝ) * phi⌋ : ℝ)| < 1 := by
    rw [abs_of_nonneg (by linarith)]; linarith
  nlinarith [htri, hxn, hfrac, hphi2]

/-- **The D0 φ-quasicrystal carrier is a genuine Mathlib `Delone.DeloneSet ℝ`** — uniformly discrete
(packing radius `1/2`) and relatively dense (covering radius `2`). -/
noncomputable def d0BeattyDelone : Delone.DeloneSet ℝ where
  carrier := d0BeattyCarrier
  packingRadius := 1 / 2
  packingRadius_pos := by norm_num
  isSeparated_packingRadius := by
    intro x hx y hy hxy
    obtain ⟨m, rfl⟩ := hx
    obtain ⟨n, rfl⟩ := hy
    have hmn : m ≠ n := by rintro rfl; exact hxy rfl
    have hd : (1 : ℝ) ≤ dist (beattyPhi m) (beattyPhi n) := beatty_dist_ge_one hmn
    rw [edist_dist]
    have h1 : (1 : ℝ≥0∞) ≤ ENNReal.ofReal (dist (beattyPhi m) (beattyPhi n)) := by
      rw [← ENNReal.ofReal_one]; exact ENNReal.ofReal_le_ofReal hd
    have h2 : ((1 / 2 : ℝ≥0) : ℝ≥0∞) < 1 := by
      rw [show (1 : ℝ≥0∞) = ((1 : ℝ≥0) : ℝ≥0∞) from by simp]
      exact_mod_cast (by norm_num : (1 / 2 : ℝ≥0) < 1)
    exact lt_of_lt_of_le h2 h1
  coveringRadius := 2
  coveringRadius_pos := by norm_num
  isCover_coveringRadius := by
    rw [Metric.isCover_iff_subset_iUnion_closedBall]
    intro x _
    simp only [Set.mem_iUnion, Metric.mem_closedBall, exists_prop]
    refine ⟨beattyPhi (round (x / phi)), ⟨round (x / phi), rfl⟩, ?_⟩
    have := beatty_cover x
    have hc : ((2 : ℝ≥0) : ℝ) = 2 := by norm_num
    rw [hc]; exact this

end D0.Topology
