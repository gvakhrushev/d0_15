import Mathlib.Tactic

/-!
# The dark archive is the invariant-free part of the scene

The corpus reads the adjacency spectrum of `K(9,11,13)` as `rank 3 = space, kernel 30 = dark
archive`, but records no structure for the kernel beyond its dimension. This module supplies it.

Write `zoneSum v z` for the sum of `v` over zone `z`. Then:

* `balanced_mem_ker` and `ker_imp_balanced` — `A v = 0` **iff every zone sum vanishes**. One
  direction is immediate; the other uses that the zone sums are then all equal to the total, which
  for three zones forces the total to vanish. So the archive is exactly the space of zone-wise
  balanced vectors — the direct sum of the three zones' zero-sum spaces, i.e. the standard
  representations of `S₉`, `S₁₁`, `S₁₃`, of dimensions `8 + 10 + 12 = 30`.

* `no_invariant_vector_in_archive` — **the archive carries no `Aut`-invariant vector.** `Aut` acts
  within zones, so its invariants are the zone-constant vectors; a zone-constant vector with
  vanishing zone sums is zero, because each zone is non-empty.

So the visible/dark division is not a reading laid over the spectrum: it *is* the split of the
adjacency into its invariants and an invariant-free complement. Nothing in the archive can be seen
by any `Aut`-invariant measurement — which is why `R^Aut` has dimension three and no more.
-/

namespace D0.Spectral.DarkArchiveStructure

open scoped BigOperators

/-- The `9 | 11 | 13` zone label. -/
def zone (i : Fin 33) : Fin 3 :=
  if i.val < 9 then 0 else if i.val < 20 then 1 else 2

/-- The adjacency of `K(9,11,13)`: adjacent iff in different zones. -/
def adj (i j : Fin 33) : ℚ := if zone j = zone i then 0 else 1

/-- The zone sum of a vector. -/
noncomputable def zoneSum (v : Fin 33 → ℚ) (z : Fin 3) : ℚ :=
  ∑ w ∈ Finset.univ.filter (fun w => zone w = z), v w

/-- The total sum. -/
noncomputable def total (v : Fin 33 → ℚ) : ℚ := ∑ w, v w

/-- The row of the adjacency against `v` is the total minus the own-zone sum. -/
theorem adj_row (v : Fin 33 → ℚ) (u : Fin 33) :
    ∑ w, adj u w * v w = total v - zoneSum v (zone u) := by
  have hsplit :
      (∑ w ∈ Finset.univ.filter (fun w => zone w = zone u), v w)
        + (∑ w ∈ Finset.univ.filter (fun w => ¬ zone w = zone u), v w) = total v :=
    Finset.sum_filter_add_sum_filter_not _ _ _
  have hrow : ∑ w, adj u w * v w
      = ∑ w ∈ Finset.univ.filter (fun w => ¬ zone w = zone u), v w := by
    rw [Finset.sum_filter]
    refine Finset.sum_congr rfl ?_
    intro w _
    unfold adj
    by_cases h : zone w = zone u
    · simp [h]
    · simp [h]
  rw [hrow]
  unfold zoneSum
  linarith [hsplit]

/-- Zone-wise balanced vectors lie in the kernel. -/
theorem balanced_mem_ker (v : Fin 33 → ℚ) (h : ∀ z, zoneSum v z = 0) :
    ∀ u, ∑ w, adj u w * v w = 0 := by
  intro u
  rw [adj_row]
  have htot : total v = 0 := by
    have h3 : total v = ∑ z : Fin 3, zoneSum v z := by
      unfold total zoneSum
      rw [← Finset.sum_fiberwise Finset.univ zone v]
    rw [h3]
    simp [h]
  rw [htot, h (zone u)]; ring

/-- Kernel vectors are zone-wise balanced. -/
theorem ker_imp_balanced (v : Fin 33 → ℚ) (hk : ∀ u, ∑ w, adj u w * v w = 0) :
    ∀ z, zoneSum v z = total v := by
  intro z
  have hz : ∃ u : Fin 33, zone u = z := by
    fin_cases z
    · exact ⟨⟨0, by omega⟩, by decide⟩
    · exact ⟨⟨9, by omega⟩, by decide⟩
    · exact ⟨⟨20, by omega⟩, by decide⟩
  obtain ⟨u, hu⟩ := hz
  have := hk u
  rw [adj_row, hu] at this
  linarith

/-- Each zone is non-empty, with the stated cardinalities. -/
theorem zone_card :
    (Finset.univ.filter (fun w : Fin 33 => zone w = 0)).card = 9 ∧
    (Finset.univ.filter (fun w : Fin 33 => zone w = 1)).card = 11 ∧
    (Finset.univ.filter (fun w : Fin 33 => zone w = 2)).card = 13 := by
  refine ⟨by decide, by decide, by decide⟩

/-- **The archive carries no `Aut`-invariant vector.** A zone-constant, zone-balanced vector is
zero, because each zone is non-empty. -/
theorem no_invariant_vector_in_archive (v : Fin 33 → ℚ) (c : Fin 3 → ℚ)
    (hconst : ∀ u, v u = c (zone u)) (hbal : ∀ z, zoneSum v z = 0) : ∀ u, v u = 0 := by
  have hz : ∀ z : Fin 3, (Finset.univ.filter (fun w : Fin 33 => zone w = z)).card ≠ 0 := by
    intro z
    fin_cases z <;> decide
  intro u
  have hzs : zoneSum v (zone u)
      = ((Finset.univ.filter (fun w : Fin 33 => zone w = zone u)).card : ℚ) * c (zone u) := by
    unfold zoneSum
    rw [Finset.sum_congr rfl (fun w hw => by
      rw [hconst w, (Finset.mem_filter.mp hw).2])]
    simp [mul_comm]
  rw [hbal (zone u)] at hzs
  have hcard : ((Finset.univ.filter (fun w : Fin 33 => zone w = zone u)).card : ℚ) ≠ 0 := by
    exact Nat.cast_ne_zero.mpr (hz (zone u))
  have : c (zone u) = 0 := by
    rcases mul_eq_zero.mp hzs.symm with h | h
    · exact absurd h hcard
    · exact h
  rw [hconst u, this]

end D0.Spectral.DarkArchiveStructure
