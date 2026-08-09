import D0.Spectral.DarkArchiveStructure
import D0.Geometry.SpectralActionLadder
import Mathlib.Tactic

/-!
# The spectral-action ladder instantiated at the scene: the EH proxy is the edge count

The corpus owns a generic spectral-action ladder (`D0-GEOM-SPECTRAL-ACTION-LADDER-001`,
`D0-GEOM-HEAT-TRACE-A2-DECOMP-001`; BOOK_08): for any `(L, ρ)` the weighted trace powers satisfy

    a₀ :  Tr(Δ_ρ)  = Σ L_ii / ρ_i
    a₂ :  Tr(Δ_ρ²) = Σ L_ii²/ρ_i² + 2 · EH_proxy ,   EH_proxy = ½ Σ_{i≠j} L_ij²/(ρ_i ρ_j).

The ladder has **never been instantiated at any scene** — the only recorded numbers were toy CSV
values. This module instantiates it at the frozen scene (`L = D − A` of `K(9,11,13)`, unit
conformal weight) and closes the arithmetic:

    a₀ = 718 = 2E = ζ_L(−1)
    a₂ = 16426 = ζ_L(−2) = Tr L²  =  15708 + 2 · 359

with each piece identified against an owned object:

* the **diagonal square term is `15708 = Σ n_z d_z²`** — precisely the *all-walks depth-2 carrier*
  of the vNext2 refinement no-go (`D0-VNEXT2-SCENE-NATIVE-REFINEMENT-NOGO-001`), and the
  rival-rule identity `allwalks − nonbacktracking = 2E` (`GenericSceneCalculus`) becomes the
  ladder-side identity `diag² − (diag² − a₀) = a₀`;
* the **discrete Einstein–Hilbert action proxy is `359` — the edge count**
  (`eh_proxy_is_edge_count`). Mechanism, not numerology: the scene Laplacian's off-diagonal
  entries are `−1` exactly on edges, so their squares are edge indicators and the half-sum over
  ordered pairs counts each edge once.

**The gravity ↔ α bridge.** `359 = e₂ = |E|` is the identical owned object that the α-line's top
term consumes: `α_top⁻¹ = 359·φ⁻² − ξ₅` with `359 = |E|` by the corpus's own reading. So the
scene's discrete EH action and the α numerator are two consumers of one invariant — the edge
count — and this is now theorem-level on both sides (here for the EH proxy; in the α owner for
the top term). No identification beyond the shared object is claimed.

Consistency wires: `a₀` and `a₂` agree with `D0.Synthesis.SceneHeatKernel.zetaL` at `−1, −2`, and
`Tr L² = 16426` matches the three-level assembly's level-0 second moment.
-/

namespace D0.Synthesis.SceneSpectralAction

open D0.Spectral.DarkArchiveStructure
open D0.Geometry.SpectralActionLadder
open D0.Geometry.HeatTraceA2Decomposition

/-- Zone sizes and degrees (ℕ), and their ℝ casts. -/
def nzRN (z : Fin 3) : ℕ := if z = 0 then 9 else if z = 1 then 11 else 13
def dRN (z : Fin 3) : ℕ := if z = 0 then 24 else if z = 1 then 22 else 20
def nzR (z : Fin 3) : ℝ := (nzRN z : ℝ)
def dR (z : Fin 3) : ℝ := (dRN z : ℝ)

theorem nzRN_vals : nzRN 0 = 9 ∧ nzRN 1 = 11 ∧ nzRN 2 = 13 := by decide
theorem dRN_vals : dRN 0 = 24 ∧ dRN 1 = 22 ∧ dRN 2 = 20 := by decide

theorem nzR_vals : nzR 0 = 9 ∧ nzR 1 = 11 ∧ nzR 2 = 13 := by
  refine ⟨?_, ?_, ?_⟩
  · unfold nzR; rw [nzRN_vals.1]; norm_num
  · unfold nzR; rw [nzRN_vals.2.1]; norm_num
  · unfold nzR; rw [nzRN_vals.2.2]; norm_num

theorem dR_vals : dR 0 = 24 ∧ dR 1 = 22 ∧ dR 2 = 20 := by
  refine ⟨?_, ?_, ?_⟩
  · unfold dR; rw [dRN_vals.1]; norm_num
  · unfold dR; rw [dRN_vals.2.1]; norm_num
  · unfold dR; rw [dRN_vals.2.2]; norm_num

/-- The scene Laplacian over ℝ: degrees on the diagonal, `−1` on cross-zone pairs. -/
def Lr : Matrix (Fin 33) (Fin 33) ℝ := fun i j =>
  if i = j then dR (zone i) else if zone i = zone j then 0 else -1

/-- Unit conformal weight. -/
def ρ1 : Fin 33 → ℝ := fun _ => 1

theorem ρ1_pos : ∀ i, ρ1 i > 0 := fun _ => by unfold ρ1; norm_num

/-- The scene Laplacian is symmetric. -/
theorem Lr_symm : ∀ i j, Lr i j = Lr j i := by
  intro i j
  unfold Lr
  by_cases hij : i = j
  · rw [hij]
  · rw [if_neg hij, if_neg (fun h : j = i => hij h.symm)]
    by_cases hz : zone i = zone j
    · rw [if_pos hz, if_pos hz.symm]
    · rw [if_neg hz, if_neg (fun h : zone j = zone i => hz h.symm)]

/-- Zone cardinalities cast to ℝ. -/
theorem card_zone (z : Fin 3) :
    ((Finset.univ.filter (fun i : Fin 33 => zone i = z)).card : ℝ) = nzR z := by
  unfold nzR
  norm_cast
  fin_cases z <;> decide

/-- **The workhorse**: a sum of a zone function over the vertices collapses to the three zone
totals. -/
theorem sum_zonefun (f : Fin 3 → ℝ) :
    (∑ i : Fin 33, f (zone i)) = nzR 0 * f 0 + nzR 1 * f 1 + nzR 2 * f 2 := by
  have hfib : (∑ i : Fin 33, f (zone i))
      = ∑ z : Fin 3, ∑ i ∈ Finset.univ.filter (fun i : Fin 33 => zone i = z), f (zone i) := by
    rw [← Finset.sum_fiberwise Finset.univ zone (fun i => f (zone i))]
  rw [hfib]
  have hz : ∀ z : Fin 3,
      (∑ i ∈ Finset.univ.filter (fun i : Fin 33 => zone i = z), f (zone i))
        = nzR z * f z := by
    intro z
    rw [Finset.sum_congr rfl (fun i hi => by rw [(Finset.mem_filter.mp hi).2]),
      Finset.sum_const, nsmul_eq_mul, card_zone]
  rw [Fin.sum_univ_three, hz 0, hz 1, hz 2]

/-- The diagonal sum: `Tr L = 718 = 2E`. -/
theorem trace_Lr : (∑ i : Fin 33, Lr i i) = 718 := by
  have hdiag : ∀ i : Fin 33, Lr i i = dR (zone i) := by
    intro i; unfold Lr; rw [if_pos rfl]
  rw [Finset.sum_congr rfl (fun i _ => hdiag i), sum_zonefun]
  rw [nzR_vals.1, nzR_vals.2.1, nzR_vals.2.2, dR_vals.1, dR_vals.2.1, dR_vals.2.2]
  norm_num

/-- **a₀ at the scene**: the volume proxy is `718 = 2E = ζ_L(−1)`. -/
theorem a0_at_scene : spectralTracePower Lr ρ1 1 = 718 := by
  rw [a0_is_volume_proxy Lr ρ1 ρ1_pos]
  have h : ∀ i : Fin 33, Lr i i / ρ1 i = Lr i i := by
    intro i; unfold ρ1; rw [div_one]
  rw [Finset.sum_congr rfl (fun i _ => h i), trace_Lr]

/-- Squared degrees, named so the fiberwise rewrite has a constant head. -/
def dSq (z : Fin 3) : ℝ := (dR z) ^ 2

/-- The diagonal square term: `15708 = Σ n_z d_z²` — the all-walks depth-2 carrier. -/
theorem diag_sq_at_scene : diagonalSquareTerm Lr ρ1 = 15708 := by
  unfold diagonalSquareTerm
  have h : ∀ i : Fin 33, (Lr i i) ^ 2 / (ρ1 i) ^ 2 = dSq (zone i) := by
    intro i
    unfold ρ1 Lr dSq
    rw [if_pos rfl]
    norm_num
  rw [Finset.sum_congr rfl (fun i _ => h i), sum_zonefun dSq]
  unfold dSq
  rw [nzR_vals.1, nzR_vals.2.1, nzR_vals.2.2, dR_vals.1, dR_vals.2.1, dR_vals.2.2]
  norm_num

/-- The complement indicator of a zone, named for the fiberwise rewrite. -/
def indNe (z w : Fin 3) : ℝ := if w = z then 0 else 1

/-- The cross-zone count seen from a fixed zone: `Σ_j [zone j ≠ z] = 33 − n_z`. -/
theorem sum_cross (z : Fin 3) :
    (∑ j : Fin 33, if zone j = z then (0:ℝ) else 1) = 33 - nzR z := by
  have h : ∀ j : Fin 33, (if zone j = z then (0:ℝ) else 1) = indNe z (zone j) := fun _ => rfl
  rw [Finset.sum_congr rfl (fun j _ => h j), sum_zonefun (indNe z)]
  have h3 : ∀ y : Fin 3, y = 0 ∨ y = 1 ∨ y = 2 := by decide
  rcases h3 z with hz | hz | hz
  · subst hz
    unfold indNe
    rw [if_pos (rfl : (0:Fin 3) = 0), if_neg (by decide : ¬(1:Fin 3) = 0),
        if_neg (by decide : ¬(2:Fin 3) = 0), nzR_vals.1, nzR_vals.2.1, nzR_vals.2.2]
    norm_num
  · subst hz
    unfold indNe
    rw [if_neg (by decide : ¬(0:Fin 3) = 1), if_pos (rfl : (1:Fin 3) = 1),
        if_neg (by decide : ¬(2:Fin 3) = 1), nzR_vals.1, nzR_vals.2.1, nzR_vals.2.2]
    norm_num
  · subst hz
    unfold indNe
    rw [if_neg (by decide : ¬(0:Fin 3) = 2), if_neg (by decide : ¬(1:Fin 3) = 2),
        if_pos (rfl : (2:Fin 3) = 2), nzR_vals.1, nzR_vals.2.1, nzR_vals.2.2]
    norm_num

/-- The cross-zone degree function, named for the fiberwise rewrite. -/
def crossCount (z : Fin 3) : ℝ := 33 - nzR z

/-- **The discrete Einstein–Hilbert action proxy of the scene is its edge count: `359`.** -/
theorem eh_proxy_is_edge_count : discreteEHActionProxy Lr ρ1 = 359 := by
  unfold discreteEHActionProxy
  have hterm : ∀ i j : Fin 33,
      (if i ≠ j then (Lr i j) ^ 2 / (ρ1 i * ρ1 j) else 0)
        = (if zone i = zone j then (0:ℝ) else 1) := by
    intro i j
    unfold ρ1
    by_cases hij : i = j
    · rw [if_neg (not_not.mpr hij), hij, if_pos rfl]
    · rw [if_pos hij]
      by_cases hz : zone i = zone j
      · rw [if_pos hz]
        have hL : Lr i j = 0 := by unfold Lr; rw [if_neg hij, if_pos hz]
        rw [hL]; norm_num
      · rw [if_neg hz]
        have hL : Lr i j = -1 := by unfold Lr; rw [if_neg hij, if_neg hz]
        rw [hL]; norm_num
  have hsum : (∑ i : Fin 33, ∑ j : Fin 33,
      if i ≠ j then (Lr i j) ^ 2 / (ρ1 i * ρ1 j) else 0) = 718 := by
    rw [Finset.sum_congr rfl (fun i _ => Finset.sum_congr rfl (fun j _ => hterm i j))]
    have hin : ∀ i : Fin 33, (∑ j : Fin 33, if zone i = zone j then (0:ℝ) else 1)
        = crossCount (zone i) := by
      intro i
      have hflip : ∀ j : Fin 33, (if zone i = zone j then (0:ℝ) else 1)
          = (if zone j = zone i then (0:ℝ) else 1) := by
        intro j
        by_cases h : zone i = zone j
        · rw [if_pos h, if_pos h.symm]
        · rw [if_neg h, if_neg (fun hc => h hc.symm)]
      rw [Finset.sum_congr rfl (fun j _ => hflip j), sum_cross]
      rfl
    rw [Finset.sum_congr rfl (fun i _ => hin i), sum_zonefun crossCount]
    unfold crossCount
    rw [nzR_vals.1, nzR_vals.2.1, nzR_vals.2.2]
    norm_num
  rw [hsum]
  norm_num

/-- **a₂ at the scene**: `Tr(Δ²) = 16426 = 15708 + 2·359 = ζ_L(−2)`. -/
theorem a2_at_scene : spectralTracePower Lr ρ1 2 = 16426 := by
  rw [a2_is_eh_proxy Lr ρ1 ρ1_pos Lr_symm, diag_sq_at_scene, eh_proxy_is_edge_count]
  norm_num

/-- **Assembled: the first scene instantiation of the spectral-action ladder.** The volume proxy
is `2E`; the EH proxy is `E = 359` — the α_top numerator's own object; their combination is
`Tr L²`, split exactly as `allwalks + 2E`. -/
theorem scene_spectral_action :
    spectralTracePower Lr ρ1 1 = 718 ∧
    spectralTracePower Lr ρ1 2 = 16426 ∧
    diagonalSquareTerm Lr ρ1 = 15708 ∧
    discreteEHActionProxy Lr ρ1 = 359 ∧
    (15708 + 2 * 359 : ℝ) = 16426 :=
  ⟨a0_at_scene, a2_at_scene, diag_sq_at_scene, eh_proxy_is_edge_count, by norm_num⟩

end D0.Synthesis.SceneSpectralAction
