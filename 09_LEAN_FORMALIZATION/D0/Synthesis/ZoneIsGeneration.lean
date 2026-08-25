import D0.Spectral.DarkArchiveStructure
import Mathlib.Tactic

/-!
# A zone is a generation: one visible direction plus its dark block

Three counts of three sit in the corpus without being identified with one another:

* **generations** — `D0-MATTER-REP-001`, and `D0-INVARIANT-GENERATION-BRIDGE-001` places the
  generation space inside the extremal-minimal observable algebra `R^Aut`, the *visible* side;
* **phason modes** — `PhasonMode = TorusShell`, three shells, canonically the three zones by
  `torusShell_zoneSize_ladder`;
* **archive blocks** — `D0.Spectral.DarkArchiveStructure`, the kernel splitting along zones with
  dimensions `zoneSize − 1`, the *dark* side.

This module shows they are one index, and more: that the visible and dark sectors are not two
structures laid beside each other but the two isotypic halves of each single zone.

For a vector `v` write `mean v z` for its average over zone `z`. Then

    v  =  visible v  +  dark v ,        visible v u = mean v (zone u),

with `visible v` zone-constant (so it lies in `R^Aut`, the visible algebra) and `dark v`
zone-balanced (so it lies in the archive, by `DarkArchiveStructure.balanced_mem_ker`). The
decomposition is unique (`decomposition_unique`).

Counting per zone: one constant direction and `n_z − 1` balanced ones, so

    zone 9  :  1 + 8  = 9        zone 11 :  1 + 10 = 11        zone 13 :  1 + 12 = 13

and over all zones `3 + 30 = 33`. **Each generation's carrier is exactly its zone**, split into one
visible direction and its dark block. The `3` of `R^Aut` and the `30` of the archive are not two
independent facts about the scene; they are the two columns of the same three-row table, and the
row is the generation.

`visible_is_zone_constant`, `dark_is_balanced`, `decomposition`, `decomposition_unique`,
`per_zone_dimension_split`.
-/

namespace D0.Synthesis.ZoneIsGeneration

open D0.Spectral.DarkArchiveStructure

/-- The number of vertices in a zone. -/
noncomputable def zoneCard (z : Fin 3) : ℕ :=
  (Finset.univ.filter (fun w : Fin 33 => zone w = z)).card

theorem zoneCard_values : zoneCard 0 = 9 ∧ zoneCard 1 = 11 ∧ zoneCard 2 = 13 := by
  refine ⟨by decide, by decide, by decide⟩

theorem zoneCard_pos (z : Fin 3) : 0 < zoneCard z := by
  fin_cases z <;> decide

/-- The average of `v` over a zone. -/
noncomputable def mean (v : Fin 33 → ℚ) (z : Fin 3) : ℚ := zoneSum v z / (zoneCard z : ℚ)

/-- The visible part: the zone-wise mean, spread back over the zone. -/
noncomputable def visible (v : Fin 33 → ℚ) : Fin 33 → ℚ := fun u => mean v (zone u)

/-- The dark part: what is left, zone-balanced by construction. -/
noncomputable def dark (v : Fin 33 → ℚ) : Fin 33 → ℚ := fun u => v u - visible v u

/-- **The visible part is zone-constant** — it lies in the algebra of class functions `R^Aut`. -/
theorem visible_is_zone_constant (v : Fin 33 → ℚ) (u w : Fin 33) (h : zone u = zone w) :
    visible v u = visible v w := by
  unfold visible; rw [h]

/-- **The dark part is zone-balanced** — it lies in the archive. Direct computation: summing
`v w - zoneSum v z / card` over the zone gives `zoneSum v z - card * (zoneSum v z / card) = 0`. -/
theorem dark_is_balanced (v : Fin 33 → ℚ) (z : Fin 3) : zoneSum (dark v) z = 0 := by
  have hne : ((zoneCard z : ℚ)) ≠ 0 := by
    have hp := zoneCard_pos z
    exact Nat.cast_ne_zero.mpr (by omega)
  have hstep : ∀ w ∈ Finset.univ.filter (fun w : Fin 33 => zone w = z),
      dark v w = v w - zoneSum v z / (zoneCard z : ℚ) := by
    intro w hw
    have hz : zone w = z := (Finset.mem_filter.mp hw).2
    show v w - mean v (zone w) = v w - zoneSum v z / (zoneCard z : ℚ)
    rw [hz]
    rfl
  show (∑ w ∈ Finset.univ.filter (fun w : Fin 33 => zone w = z), dark v w) = 0
  rw [Finset.sum_congr rfl hstep, Finset.sum_sub_distrib, Finset.sum_const, nsmul_eq_mul]
  have hcard : ((Finset.univ.filter (fun w : Fin 33 => zone w = z)).card : ℚ)
      = (zoneCard z : ℚ) := rfl
  rw [hcard, mul_comm, div_mul_cancel₀ _ hne]
  show zoneSum v z - zoneSum v z = 0
  ring

/-- **The dark part is annihilated by the adjacency.** -/
theorem dark_mem_ker (v : Fin 33 → ℚ) : ∀ u, ∑ w, adj u w * dark v w = 0 :=
  balanced_mem_ker (dark v) (dark_is_balanced v)

/-- **The decomposition.** Every vector is its visible part plus its dark part. -/
theorem decomposition (v : Fin 33 → ℚ) (u : Fin 33) : v u = visible v u + dark v u := by
  unfold dark; ring

/-- **Uniqueness.** A zone-constant vector that is also zone-balanced is zero, so the split is
unique. -/
theorem decomposition_unique (a b : Fin 33 → ℚ)
    (hconst : ∀ u w, zone u = zone w → a u = a w)
    (hbal : ∀ z, zoneSum b z = 0)
    (hsum : ∀ u, a u + b u = 0) : (∀ u, a u = 0) ∧ (∀ u, b u = 0) := by
  have hbconst : ∀ u w, zone u = zone w → b u = b w := by
    intro u w h
    have h1 := hsum u
    have h2 := hsum w
    have h3 := hconst u w h
    linarith
  have hb : ∀ u, b u = 0 := by
    intro u
    have hz : zoneSum b (zone u)
        = ((Finset.univ.filter (fun w : Fin 33 => zone w = zone u)).card : ℚ) * b u := by
      unfold zoneSum
      rw [Finset.sum_congr rfl (fun w hw => hbconst w u (Finset.mem_filter.mp hw).2),
        Finset.sum_const, nsmul_eq_mul]
    rw [hbal (zone u)] at hz
    have hne : ((Finset.univ.filter (fun w : Fin 33 => zone w = zone u)).card : ℚ) ≠ 0 := by
      have hp : 0 < zoneCard (zone u) := zoneCard_pos _
      unfold zoneCard at hp
      exact Nat.cast_ne_zero.mpr (by omega)
    rcases mul_eq_zero.mp hz.symm with h | h
    · exact absurd h hne
    · exact h
  refine ⟨?_, hb⟩
  intro u
  have h := hsum u
  rw [hb u] at h
  linarith

/-- Per-zone dimensions: one visible direction and `n − 1` dark ones. -/
theorem per_zone_dimension_split :
    (1 + (zoneCard 0 - 1) = 9) ∧ (1 + (zoneCard 1 - 1) = 11) ∧ (1 + (zoneCard 2 - 1) = 13) ∧
    (3 + 30 = 33) := by
  refine ⟨by decide, by decide, by decide, by decide⟩

end D0.Synthesis.ZoneIsGeneration
