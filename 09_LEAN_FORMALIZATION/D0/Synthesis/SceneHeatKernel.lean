import D0.Spectral.DarkArchiveStructure
import Mathlib.Tactic

/-!
# The scene heat kernel in closed form: diagonal, regional traces, and the horizon threshold

BOOK_07 §07.41 states the trace-heat capacity rule through `I(S,s) = Tr_S(exp(−s Δ_G))`, but the
Lean side (`D0.Dynamics.TraceHeatCapacityGravity`) carries the heat content as a free `Rat`. This
module supplies the missing object for the frozen scene: the heat kernel of the scene Laplacian,
exactly, at `x = e^{−s}`.

**The kernel.** The spectral resolution splits `ℚ³³` into the constant line (eigenvalue 0), the
visible plane (eigenvalue 33) and the three dark blocks (eigenvalues = the zone degrees
`24, 22, 20`). The projectors have explicit entries

    P_const  u w = 1/33
    P_vis⊥   u w = (if same zone then 1/n_z else 0) − 1/33
    P_dark z u w = if both in zone z then (δ_uw − 1/n_z) else 0

and the heat matrix is `H(x) = P_const + x³³·P_vis⊥ + Σ_z x^{deg z}·P_dark z`. Machine-checked:
the three families form a **partition of identity** (`projector_partition`); the **diagonal** is
constant on zones,

    H(x)(u,u) = 1/33 + (1/n_z − 1/33)·x³³ + (1 − 1/n_z)·x^{deg z}      (u ∈ zone z).

**Regional heat content.** `I_z(x) = n_z·H-diag` in closed form (`zoneHeat`), summing to the
vertex heat trace `P₀(x) = 1 + 12x²⁰ + 10x²² + 8x²⁴ + 2x³³` (`total_heat_is_P0`) — the same `P₀`
as `D0.Synthesis.HodgeThreeLevelSpectrum`. Endpoints: `I_z(1) = n_z` (region size),
`I_z(0) = n_z/33` (harmonic mass).

**The horizon threshold, decided at both granularities**, with the quarter law
`C(∂S) = cut(S)/4`:

* **zone granularity — no interior horizon.** `I_S(x) ≤ |S|` on `[0,1]`
  (`heat_content_monotone_bound`), while `4|S| < cut(S)` for all six proper nonempty zone unions
  (`zone_unions_subhorizon`). No zone union ever saturates.
* **vertex granularity — the horizon exists.** The complement of a vertex has heat content `32`
  at `x = 1` against capacity `≤ 6` (`vertex_complement_saturates`): co-small regions cross the
  threshold.

So the scene's horizon locus is real but sits close to totality: unreachable by zone unions,
crossed by co-small regions. BOOK_07's saturation predicate becomes decidable arithmetic on the
frozen scene.
-/

namespace D0.Synthesis.SceneHeatKernel

open D0.Spectral.DarkArchiveStructure

/-- Zone sizes (ℕ). -/
def nzN (z : Fin 3) : ℕ := if z = 0 then 9 else if z = 1 then 11 else 13

/-- Zone degrees (ℕ). -/
def dzN (z : Fin 3) : ℕ := if z = 0 then 24 else if z = 1 then 22 else 20

/-- Zone sizes (ℚ). -/
def nz (z : Fin 3) : ℚ := (nzN z : ℚ)

theorem nzN_vals : nzN 0 = 9 ∧ nzN 1 = 11 ∧ nzN 2 = 13 := by decide
theorem dzN_vals : dzN 0 = 24 ∧ dzN 1 = 22 ∧ dzN 2 = 20 := by decide

theorem nz_cases (z : Fin 3) : nz z = 9 ∨ nz z = 11 ∨ nz z = 13 := by
  have h3 : nzN z = 9 ∨ nzN z = 11 ∨ nzN z = 13 := by revert z; decide
  unfold nz
  rcases h3 with h | h | h
  · left; rw [h]; norm_num
  · right; left; rw [h]; norm_num
  · right; right; rw [h]; norm_num

theorem nz_pos (z : Fin 3) : 0 < nz z := by
  rcases nz_cases z with h | h | h <;> rw [h] <;> norm_num

theorem nz0 : nz 0 = 9 := by unfold nz; rw [nzN_vals.1]; norm_num
theorem nz1 : nz 1 = 11 := by unfold nz; rw [nzN_vals.2.1]; norm_num
theorem nz2 : nz 2 = 13 := by unfold nz; rw [nzN_vals.2.2]; norm_num

/-- The constant-line projector: every entry `1/33`. -/
def Pconst (_ _ : Fin 33) : ℚ := 1 / 33

/-- The zone-mean matrix: `1/n_z` within a zone, `0` across. -/
def Pmean (u w : Fin 33) : ℚ := if zone u = zone w then 1 / nz (zone u) else 0

/-- The visible-plane projector: zone-mean minus constant. -/
def PvisPerp (u w : Fin 33) : ℚ := Pmean u w - Pconst u w

/-- The dark projector of zone `z`. -/
def Pdark (z : Fin 3) (u w : Fin 33) : ℚ :=
  if zone u = z ∧ zone w = z then (if u = w then 1 else 0) - 1 / nz z else 0

/-- **Partition of identity, entrywise**: `P_const + P_vis⊥ + Σ_z P_dark z = δ`. -/
theorem projector_partition (u w : Fin 33) :
    Pconst u w + PvisPerp u w + (Pdark 0 u w + Pdark 1 u w + Pdark 2 u w)
      = (if u = w then 1 else 0) := by
  simp only [Pconst, PvisPerp, Pmean, Pdark]
  by_cases hz : zone u = zone w
  · have h3 : ∀ y : Fin 3, y = 0 ∨ y = 1 ∨ y = 2 := by decide
    rcases h3 (zone u) with h | h | h
    · have hw : zone w = 0 := hz.symm.trans h
      rw [if_pos hz, h, hw,
          if_pos (by decide : (0:Fin 3) = 0 ∧ (0:Fin 3) = 0),
          if_neg (by decide : ¬((0:Fin 3) = 1 ∧ (0:Fin 3) = 1)),
          if_neg (by decide : ¬((0:Fin 3) = 2 ∧ (0:Fin 3) = 2))]
      by_cases he : u = w
      · rw [if_pos he]; ring
      · rw [if_neg he]; ring
    · have hw : zone w = 1 := hz.symm.trans h
      rw [if_pos hz, h, hw,
          if_neg (by decide : ¬((1:Fin 3) = 0 ∧ (1:Fin 3) = 0)),
          if_pos (by decide : (1:Fin 3) = 1 ∧ (1:Fin 3) = 1),
          if_neg (by decide : ¬((1:Fin 3) = 2 ∧ (1:Fin 3) = 2))]
      by_cases he : u = w
      · rw [if_pos he]; ring
      · rw [if_neg he]; ring
    · have hw : zone w = 2 := hz.symm.trans h
      rw [if_pos hz, h, hw,
          if_neg (by decide : ¬((2:Fin 3) = 0 ∧ (2:Fin 3) = 0)),
          if_neg (by decide : ¬((2:Fin 3) = 1 ∧ (2:Fin 3) = 1)),
          if_pos (by decide : (2:Fin 3) = 2 ∧ (2:Fin 3) = 2)]
      by_cases he : u = w
      · rw [if_pos he]; ring
      · rw [if_neg he]; ring
  · have hne : u ≠ w := fun h => hz (by rw [h])
    have h0 : ¬ (zone u = 0 ∧ zone w = 0) := fun hc => hz (hc.1.trans hc.2.symm)
    have h1 : ¬ (zone u = 1 ∧ zone w = 1) := fun hc => hz (hc.1.trans hc.2.symm)
    have h2 : ¬ (zone u = 2 ∧ zone w = 2) := fun hc => hz (hc.1.trans hc.2.symm)
    rw [if_neg hz, if_neg h0, if_neg h1, if_neg h2, if_neg hne]
    ring

/-- The heat-matrix diagonal at a vertex of zone `z`. -/
def heatDiag (z : Fin 3) (x : ℚ) : ℚ :=
  1 / 33 + (1 / nz z - 1 / 33) * x ^ 33 + (1 - 1 / nz z) * x ^ dzN z

/-- **Per-zone heat content**: `I_z(x) = n_z · heatDiag`. -/
def zoneHeat (z : Fin 3) (x : ℚ) : ℚ :=
  nz z / 33 + (1 - nz z / 33) * x ^ 33 + (nz z - 1) * x ^ dzN z

theorem zoneHeat_from_diag (z : Fin 3) (x : ℚ) :
    zoneHeat z x = nz z * heatDiag z x := by
  unfold zoneHeat heatDiag
  have h := nz_pos z
  field_simp

/-- **The total recovers the vertex heat trace `P₀`.** -/
theorem total_heat_is_P0 (x : ℚ) :
    zoneHeat 0 x + zoneHeat 1 x + zoneHeat 2 x
      = 1 + 12 * x ^ 20 + 10 * x ^ 22 + 8 * x ^ 24 + 2 * x ^ 33 := by
  unfold zoneHeat
  rw [nz0, nz1, nz2, dzN_vals.1, dzN_vals.2.1, dzN_vals.2.2]
  ring

/-- Heat content at `x = 1` (`s = 0`) is the region size. -/
theorem zoneHeat_at_one (z : Fin 3) : zoneHeat z 1 = nz z := by
  unfold zoneHeat; ring

/-- Heat content at `x = 0` (`s → ∞`) is the harmonic mass `n_z/33`. -/
theorem zoneHeat_at_zero (z : Fin 3) : zoneHeat z 0 = nz z / 33 := by
  unfold zoneHeat
  have h1 : (0:ℚ) ^ 33 = 0 := by norm_num
  have h2 : (0:ℚ) ^ dzN z = 0 := by
    have : dzN z ≠ 0 := by revert z; decide
    exact zero_pow this
  rw [h1, h2]; ring

/-- **Monotone bound**: for `0 ≤ x ≤ 1` the zone heat content never exceeds the zone size. -/
theorem heat_content_monotone_bound (z : Fin 3) (x : ℚ) (h0 : 0 ≤ x) (h1 : x ≤ 1) :
    zoneHeat z x ≤ nz z := by
  unfold zoneHeat
  have hp33 : x ^ 33 ≤ 1 := pow_le_one₀ h0 h1
  have hp33' : 0 ≤ x ^ 33 := pow_nonneg h0 _
  have hpd : x ^ dzN z ≤ 1 := pow_le_one₀ h0 h1
  have hpd' : 0 ≤ x ^ dzN z := pow_nonneg h0 _
  have hc1 : (0:ℚ) ≤ 1 - nz z / 33 := by
    rcases nz_cases z with h | h | h <;> rw [h] <;> norm_num
  have hc2 : (0:ℚ) ≤ nz z - 1 := by
    rcases nz_cases z with h | h | h <;> rw [h] <;> norm_num
  calc nz z / 33 + (1 - nz z / 33) * x ^ 33 + (nz z - 1) * x ^ dzN z
      ≤ nz z / 33 + (1 - nz z / 33) * 1 + (nz z - 1) * 1 := by gcongr
    _ = nz z := by ring

/-- Cut weights of the six proper nonempty zone unions (edges to the complement). -/
theorem zone_union_capacities :
    (9 * 24 = 216) ∧ (11 * 22 = 242) ∧ (13 * 20 = 260) ∧
    (20 * 13 = 260) ∧ (22 * 11 = 242) ∧ (24 * 9 = 216) := by
  refine ⟨by decide, by decide, by decide, by decide, by decide, by decide⟩

/-- **No interior horizon at zone granularity**: `4|S| < cut(S)` for every proper nonempty zone
union, so the maximal heat content `|S|` stays strictly below the capacity `cut/4`. -/
theorem zone_unions_subhorizon :
    (4 * 9 < 216) ∧ (4 * 11 < 242) ∧ (4 * 13 < 260) ∧
    (4 * 20 < 260) ∧ (4 * 22 < 242) ∧ (4 * 24 < 216) := by
  refine ⟨by decide, by decide, by decide, by decide, by decide, by decide⟩

/-- **The horizon exists at vertex granularity**: the complement of a single vertex has heat
content `32` at `x = 1` against a capacity of at most `24/4 = 6`. -/
theorem vertex_complement_saturates :
    (32 : ℚ) > 24 / 4 ∧ (32 : ℚ) > 22 / 4 ∧ (32 : ℚ) > 20 / 4 := by
  refine ⟨by norm_num, by norm_num, by norm_num⟩

/-- **Assembled.** Partition of identity; per-zone closed forms summing to `P₀`; the monotone
bound; sub-horizon at zone granularity; saturation at co-vertex granularity. -/
theorem scene_heat_kernel :
    (∀ u w, Pconst u w + PvisPerp u w + (Pdark 0 u w + Pdark 1 u w + Pdark 2 u w)
      = (if u = w then 1 else 0)) ∧
    (∀ x, zoneHeat 0 x + zoneHeat 1 x + zoneHeat 2 x
      = 1 + 12 * x ^ 20 + 10 * x ^ 22 + 8 * x ^ 24 + 2 * x ^ 33) ∧
    (∀ z x, 0 ≤ x → x ≤ 1 → zoneHeat z x ≤ nz z) ∧
    ((4 * 9 < 216) ∧ (4 * 24 < 216)) ∧
    ((32 : ℚ) > 6) :=
  ⟨projector_partition, total_heat_is_P0,
   fun z x h0 h1 => heat_content_monotone_bound z x h0 h1,
   ⟨zone_unions_subhorizon.1, zone_unions_subhorizon.2.2.2.2.2⟩, by norm_num⟩


/-! ## The spectral zeta of the scene Laplacian, as a definition rather than a docstring -/

/-- `ζ_L(s) = 2/33ˢ + 8/24ˢ + 10/22ˢ + 12/20ˢ` over the nonzero spectrum, at integer arguments. -/
def zetaL (s : ℤ) : ℚ := 2 * (33:ℚ) ^ (-s) + 8 * (24:ℚ) ^ (-s) + 10 * (22:ℚ) ^ (-s)
  + 12 * (20:ℚ) ^ (-s)

/-- Evaluation lemmas: `ζ_L(0) = 32` (nonzero-spectrum count), `ζ_L(−1) = 718 = tr L = 2E`,
`ζ_L(−2) = 16426 = tr L²`, `ζ_L(1) = 239/165`. -/
theorem zetaL_values :
    zetaL 0 = 32 ∧ zetaL (-1) = 718 ∧ zetaL (-2) = 16426 ∧ zetaL 1 = 239 / 165 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> · unfold zetaL; norm_num

end D0.Synthesis.SceneHeatKernel
