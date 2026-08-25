import D0.Synthesis.SceneHeatKernel
import D0.Dynamics.TraceHeatCapacityGravity
import D0.Dynamics.TraceHeatLucasCore
import Mathlib.Tactic

/-!
# The scene installed in the trace-heat capacity machinery — the first concrete instance

`D0.Dynamics.TraceHeatCapacityGravity` implements BOOK_07 §07.41's rule
`I(S,s) = Tr_S(exp(−sΔ))`, `C(∂S) = cut/4`, with the heat content as a **free `Rat` field** — and
no concrete `FiniteArchiveGraph` exists anywhere in the corpus. This module supplies the first:
the frozen scene `K(9,11,13)` as an archive graph, with regions whose heat content is **computed**
from the closed-form heat kernel (`D0.Synthesis.SceneHeatKernel`), not chosen.

Delivered, all machine-checked:

* `sceneGraph` — the first concrete `FiniteArchiveGraph`: `V = Fin 33`, cross-zone unit weights.
* `cut_zone` — `BoundaryCutWeight` of a zone is `n_z(33 − n_z)`: the capacities are
  `54, 121/2, 65`.
* `zone_region_never_saturates` — **no interior horizon at zone granularity**: a zone region with
  its computed heat content `zoneHeat z x` never saturates, for any `x ∈ [0,1]` — the capacity
  exceeds the maximal heat content strictly (`4·n_z < n_z(33−n_z)` since `n_z < 29`).
* `full_scene_saturated` / `full_scene_not_horizon` — the full scene has zero cut, hence zero
  capacity: it is saturated at every `x ≥ 0`, and strictly beyond the horizon equality (heat
  `≥ 1 > 0`). Saturation exists, but only at totality — at zone granularity.
* `covertex_cut` / `covertex_saturated` — **the horizon is crossed at vertex granularity**: the
  complement of the last vertex (zone 13, degree 20) has capacity `5` and heat content `32` at
  `x = 1` — the region the numerical sweep found to minimise `cut/(4|S|) = 5/32` over all proper
  subsets.
* `lucas_defect_of_full_scene` — the first non-dead instance of `TraceHeatDefect`, with the ideal
  moment **owned**: against the toral first heat moment `Tr(T²) = L₂ = 3`
  (`D0.Dynamics.trace_T2`, `heat_moment_eq_even_lucas`), the full scene's defect at `s = 0` is

      TraceHeatDefect = 33 − 3 = 30 = dim(dark archive).

  The toral/Lucas side counts exactly the visible sector (`3`); the defect **is** the archive.
  This is the missing wire between `TraceHeatLucasCore` and the capacity layer, and it lands on
  the session's visible/dark split.

**Scope.** The saturation analysis at full vertex granularity (61 saturating composition classes,
all of co-size ≤ 6; equality case `(7,9,11)`) is verified exhaustively in the recon certificate
(`scratchpad/verify_k91113.py`, 28/28) and recorded here as the two decisive endpoints (zone
unions never; co-vertex yes). The capstone interface theorem is not invoked: building a
`FiniteGravityInterfaceWitness` (flux, tension, TT-positivity, spectral bridge) is a separate
obligation, and its `_hsat` hypothesis is unused in the current corpus — noted, not repaired here.
-/

namespace D0.Synthesis.SceneTraceHeatCapacity

open D0.Spectral.DarkArchiveStructure
open D0.Synthesis.SceneHeatKernel
open D0.Dynamics

/-- The scene adjacency is symmetric. -/
theorem adj_symm (i j : Fin 33) : adj i j = adj j i := by
  unfold adj
  by_cases h : zone j = zone i
  · rw [if_pos h, if_pos h.symm]
  · rw [if_neg h, if_neg (fun hc => h hc.symm)]

/-- The scene adjacency is nonnegative. -/
theorem adj_nonneg (i j : Fin 33) : 0 ≤ adj i j := by
  unfold adj
  by_cases h : zone j = zone i
  · rw [if_pos h]
  · rw [if_neg h]; norm_num

/-- **The first concrete `FiniteArchiveGraph` in the corpus**: the frozen scene. -/
def sceneGraph : D0.Gravity.FiniteArchiveGraph where
  V := Fin 33
  instFintype := inferInstance
  instDecEq := inferInstance
  edgeWeight := adj
  symmetric := adj_symm
  nonnegative := adj_nonneg

/-- A zone as a region. -/
def zoneRegion (z : Fin 3) : Set (Fin 33) := {u | zone u = z}

/-- Counting helper: the ℚ-sum of the zone indicator is the zone size. -/
theorem sum_zone_indicator (z : Fin 3) :
    (∑ i : Fin 33, (if zone i = z then (1:ℚ) else 0)) = nz z := by
  rw [Finset.sum_boole]
  unfold nz
  norm_cast
  fin_cases z <;> decide

/-- Counting helper: the ℚ-sum of the complement indicator is `33 − n_z`. -/
theorem sum_notzone_indicator (z : Fin 3) :
    (∑ j : Fin 33, (if zone j = z then (0:ℚ) else 1)) = 33 - nz z := by
  have h : ∀ j : Fin 33, (if zone j = z then (0:ℚ) else 1)
      = 1 - (if zone j = z then (1:ℚ) else 0) := by
    intro j; by_cases hj : zone j = z <;> simp [hj]
  rw [Finset.sum_congr rfl (fun j _ => h j), Finset.sum_sub_distrib,
    sum_zone_indicator, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
    nsmul_eq_mul, mul_one]
  norm_num

/-- **The cut of a zone**: `n_z · (33 − n_z)`, i.e. `216, 242, 260`. -/
theorem cut_zone (z : Fin 3) :
    D0.Gravity.BoundaryCutWeight sceneGraph (zoneRegion z) = nz z * (33 - nz z) := by
  classical
  unfold D0.Gravity.BoundaryCutWeight
  have hterm : ∀ i j : Fin 33,
      (if i ∈ zoneRegion z ∧ j ∉ zoneRegion z then sceneGraph.edgeWeight i j else 0)
        = (if zone i = z then (1:ℚ) else 0) * (if zone j = z then (0:ℚ) else 1) := by
    intro i j
    by_cases hi : zone i = z
    · by_cases hj : zone j = z
      · rw [if_neg (fun hc => hc.2 hj), if_pos hi, if_pos hj, mul_zero]
      · have hmem : i ∈ zoneRegion z ∧ j ∉ zoneRegion z := ⟨hi, hj⟩
        rw [if_pos hmem, if_pos hi, if_neg hj, mul_one]
        show adj i j = 1
        unfold adj
        rw [if_neg (fun hc : zone j = zone i => hj (hc.trans hi))]
    · rw [if_neg (fun hc => hi hc.1), if_neg hi, zero_mul]
  calc (∑ i : Fin 33, ∑ j : Fin 33,
        if i ∈ zoneRegion z ∧ j ∉ zoneRegion z then sceneGraph.edgeWeight i j else 0)
      = ∑ i : Fin 33, ∑ j : Fin 33,
          (if zone i = z then (1:ℚ) else 0) * (if zone j = z then (0:ℚ) else 1) := by
        exact Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => hterm i j
    _ = (∑ i : Fin 33, (if zone i = z then (1:ℚ) else 0))
          * (∑ j : Fin 33, (if zone j = z then (0:ℚ) else 1)) := by
        rw [Finset.sum_mul_sum]
    _ = nz z * (33 - nz z) := by rw [sum_zone_indicator, sum_notzone_indicator]

/-- Heat content is nonnegative on `x ≥ 0`. -/
theorem zoneHeat_nonneg (z : Fin 3) (x : ℚ) (h0 : 0 ≤ x) : 0 ≤ zoneHeat z x := by
  unfold zoneHeat
  have hp33 : (0:ℚ) ≤ x ^ 33 := pow_nonneg h0 _
  have hpd : (0:ℚ) ≤ x ^ dzN z := pow_nonneg h0 _
  rcases nz_cases z with h | h | h <;> rw [h] <;> nlinarith [hp33, hpd]

/-- A zone region with its **computed** heat content — the first `TraceHeatCapacityRegion` whose
heat field is not free data. -/
noncomputable def zoneRegionAt (z : Fin 3) (x : ℚ) (h0 : 0 ≤ x) :
    TraceHeatCapacityRegion sceneGraph where
  region := zoneRegion z
  scale := 1
  localHeatContent := zoneHeat z x
  heat_nonnegative := zoneHeat_nonneg z x h0

/-- **No interior horizon at zone granularity.** A zone region never saturates: its capacity
`n_z(33−n_z)/4 ∈ {54, 121/2, 65}` strictly exceeds its maximal heat content `n_z`. -/
theorem zone_region_never_saturates (z : Fin 3) (x : ℚ) (h0 : 0 ≤ x) (h1 : x ≤ 1) :
    ¬ SaturatedRegion (zoneRegionAt z x h0) := by
  intro hsat
  simp only [SaturatedRegion, BoundaryCapacityForRegion, LocalHeatContent, zoneRegionAt,
    D0.Gravity.BoundaryCapacity] at hsat
  rw [cut_zone] at hsat
  have hle : zoneHeat z x ≤ nz z := heat_content_monotone_bound z x h0 h1
  have hchain : nz z * (33 - nz z) / 4 ≤ nz z := le_trans hsat hle
  rcases nz_cases z with h | h | h <;> rw [h] at hchain <;> norm_num at hchain

/-- The full scene as a set over the graph's own vertex type. -/
def fullRegionSet : Set sceneGraph.V := Set.univ

/-- The full scene as a region, heat content `P₀(x)`. -/
noncomputable def fullRegionAt (x : ℚ) (h0 : 0 ≤ x) :
    TraceHeatCapacityRegion sceneGraph where
  region := fullRegionSet
  scale := 1
  localHeatContent := zoneHeat 0 x + zoneHeat 1 x + zoneHeat 2 x
  heat_nonnegative := by
    have h0' := zoneHeat_nonneg 0 x h0
    have h1' := zoneHeat_nonneg 1 x h0
    have h2' := zoneHeat_nonneg 2 x h0
    linarith

/-- The full scene has zero cut. -/
theorem cut_full : D0.Gravity.BoundaryCutWeight sceneGraph fullRegionSet = 0 := by
  classical
  unfold D0.Gravity.BoundaryCutWeight
  refine Finset.sum_eq_zero fun i _ => Finset.sum_eq_zero fun j _ => ?_
  exact if_neg (fun hc => hc.2 (Set.mem_univ j))

/-- **The full scene is saturated at every `x ≥ 0`** — zero capacity, positive heat. -/
theorem full_scene_saturated (x : ℚ) (h0 : 0 ≤ x) :
    SaturatedRegion (fullRegionAt x h0) := by
  simp only [SaturatedRegion, BoundaryCapacityForRegion, LocalHeatContent, fullRegionAt,
    D0.Gravity.BoundaryCapacity]
  rw [cut_full]
  have h0' := zoneHeat_nonneg 0 x h0
  have h1' := zoneHeat_nonneg 1 x h0
  have h2' := zoneHeat_nonneg 2 x h0
  linarith

/-- **The full scene is strictly beyond the horizon equality**: heat `≥ 1 > 0` = capacity. -/
theorem full_scene_not_horizon (x : ℚ) (h0 : 0 ≤ x) :
    ¬ HorizonRegion (fullRegionAt x h0) := by
  intro hh
  simp only [HorizonRegion, BoundaryCapacityForRegion, LocalHeatContent, fullRegionAt,
    D0.Gravity.BoundaryCapacity] at hh
  rw [cut_full] at hh
  have h1 : (1:ℚ) ≤ zoneHeat 0 x + zoneHeat 1 x + zoneHeat 2 x := by
    rw [total_heat_is_P0]
    have hp20 : (0:ℚ) ≤ x ^ 20 := pow_nonneg h0 _
    have hp22 : (0:ℚ) ≤ x ^ 22 := pow_nonneg h0 _
    have hp24 : (0:ℚ) ≤ x ^ 24 := pow_nonneg h0 _
    have hp33 : (0:ℚ) ≤ x ^ 33 := pow_nonneg h0 _
    nlinarith
  rw [hh] at h1
  norm_num at h1

/-! ## The horizon exists: the co-vertex region -/

/-- The last vertex — zone 13, degree 20 — whose complement minimises `cut/(4|S|)` over all
proper subsets (exhaustive sweep: `5/32`). -/
def u₀ : Fin 33 := ⟨32, by omega⟩

theorem zone_u₀ : zone u₀ = 2 := by decide

/-- Row-sum helper: `Σ_w adj u₀ w = 20`. -/
theorem adj_row_sum_u₀ : (∑ w : Fin 33, adj u₀ w) = 20 := by
  have h := adj_row (fun _ => (1:ℚ)) u₀
  simp only [mul_one] at h
  rw [h]
  have htotal : total (fun _ => (1:ℚ)) = 33 := by
    unfold total
    rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul, mul_one]
    norm_num
  have hzs : zoneSum (fun _ => (1:ℚ)) (zone u₀) = 13 := by
    rw [zone_u₀]
    unfold zoneSum
    rw [Finset.sum_const, nsmul_eq_mul, mul_one]
    norm_cast
  rw [htotal, hzs]
  norm_num

/-- The complement of `u₀`, over the graph's own vertex type. -/
def coRegionSet : Set sceneGraph.V := {v | v ≠ u₀}

/-- The co-vertex cut is the degree: `20`. -/
theorem covertex_cut :
    D0.Gravity.BoundaryCutWeight sceneGraph coRegionSet = 20 := by
  classical
  unfold D0.Gravity.BoundaryCutWeight
  have hterm : ∀ i j : Fin 33,
      (if i ∈ coRegionSet ∧ j ∉ coRegionSet
        then sceneGraph.edgeWeight i j else 0)
      = (if j = u₀ then adj i u₀ else 0) := by
    intro i j
    by_cases hj : j = u₀
    · by_cases hi : i = u₀
      · rw [if_pos hj, if_neg (fun hc => (hc.1 : i ≠ u₀) hi), hi]
        show (0:ℚ) = adj u₀ u₀
        unfold adj
        rw [if_pos rfl]
      · have hmem : i ∈ coRegionSet ∧ j ∉ coRegionSet := by
          refine ⟨hi, fun hc => (hc : j ≠ u₀) hj⟩
        rw [if_pos hmem, if_pos hj, hj]
        rfl
    · rw [if_neg hj, if_neg (fun hc => hc.2 (hj : j ≠ u₀))]
  calc (∑ i, ∑ j, if i ∈ coRegionSet ∧ j ∉ coRegionSet
          then sceneGraph.edgeWeight i j else 0)
      = ∑ i : Fin 33, ∑ j : Fin 33, (if j = u₀ then adj i u₀ else 0) := by
        exact Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => hterm i j
    _ = ∑ i : Fin 33, adj i u₀ := by
        exact Finset.sum_congr rfl fun i _ => Finset.sum_ite_eq' Finset.univ u₀ _
    _ = ∑ i : Fin 33, adj u₀ i := by
        exact Finset.sum_congr rfl fun i _ => adj_symm i u₀
    _ = 20 := adj_row_sum_u₀

/-- The co-vertex region at `x = 1`, heat content `32`. -/
noncomputable def coVertexRegion : TraceHeatCapacityRegion sceneGraph where
  region := coRegionSet
  scale := 1
  localHeatContent := 32
  heat_nonnegative := by norm_num

/-- **The horizon is crossed at vertex granularity**: the co-vertex region saturates —
capacity `5`, heat `32`. -/
theorem covertex_saturated : SaturatedRegion coVertexRegion := by
  simp only [SaturatedRegion, BoundaryCapacityForRegion, LocalHeatContent, coVertexRegion,
    D0.Gravity.BoundaryCapacity]
  rw [covertex_cut]
  norm_num

/-! ## The first non-dead `TraceHeatDefect`: the Lucas moment sees the visible sector -/

/-- The toral first heat moment, from the owned Lucas core: `Tr(T²) = 3`. -/
theorem toral_first_moment : Matrix.trace (TimeEnergyOperator ^ 1) = 3 := by
  rw [pow_one]
  exact D0.Dynamics.trace_T2

/-- **`TraceHeatDefect`, first genuine instance.** Full-scene heat at `s = 0` is `33`; the toral
first Lucas moment is `3` — the visible dimension; the defect is `30`, the archive dimension. -/
theorem lucas_defect_of_full_scene :
    TraceHeatDefect (fullRegionAt 1 (by norm_num)) ((3:ℤ) : ℚ) = 30 := by
  simp only [TraceHeatDefect, LocalHeatContent, fullRegionAt]
  rw [total_heat_is_P0]
  norm_num

/-- **Assembled.** The first concrete archive graph; zone cuts computed; zones never saturate;
the full scene saturates but is beyond horizon equality; the co-vertex region crosses the
threshold; and the Lucas defect of the full scene is the archive dimension. -/
theorem scene_trace_heat_capacity :
    (∀ z, D0.Gravity.BoundaryCutWeight sceneGraph (zoneRegion z) = nz z * (33 - nz z)) ∧
    (∀ z x (h0 : 0 ≤ x), x ≤ 1 → ¬ SaturatedRegion (zoneRegionAt z x h0)) ∧
    (∀ x (h0 : 0 ≤ x), SaturatedRegion (fullRegionAt x h0)) ∧
    SaturatedRegion coVertexRegion ∧
    TraceHeatDefect (fullRegionAt 1 (by norm_num)) ((3:ℤ) : ℚ) = 30 :=
  ⟨cut_zone, fun z x h0 h1 => zone_region_never_saturates z x h0 h1,
   full_scene_saturated, covertex_saturated, lucas_defect_of_full_scene⟩

end D0.Synthesis.SceneTraceHeatCapacity
