import Mathlib.Tactic

/-!
# The 30 within-zone adjacent transpositions have the zones as their orbits

`D0.Claims.InvariantGenerationBridge` records a gap, verbatim (`InvariantGenerationBridge.lean:42`):

> "the 30 swaps generate `Aut(K(9,11,13)) = S₉ × S₁₁ × S₁₃` (adjacent transpositions generate each
> `Sₙ` — **standard, cited not formalized**); what the theorem USES is only the computable fact
> that their orbit closure has the zones as orbits"

This module proves exactly the fact the theorem uses, and proves it rather than citing it.

The generators are the adjacent transpositions `(i, i+1)` whose two indices lie in the same zone of
`Fin 33` under the `9 | 11 | 13` split. Write `i ↝ j` for reachability in the graph these pairs
form. Then

* `reach_imp_sameZone` — reachability never crosses a zone: every generator fixes the zone label,
  so the label is a reachability invariant (this is the half that makes the zones *separate*
  orbits rather than one big one);
* `sameZone_imp_reach` — inside a zone every pair is reachable, since a zone is an interval and
  consecutive members are joined by a generator;
* `reach_iff_sameZone` — hence the orbits of the generated group are precisely the three zones.

Nothing here evaluates `Equiv.Perm (Fin 33)` as a `Fintype`, matching the source module's stated
constraint. The full group-theoretic statement (`⟨generators⟩ = S₉ × S₁₃ × S₁₃`) is not claimed;
`InvariantGenerationBridge` says the orbit fact is what it consumes, and that is what is supplied.
-/

namespace D0.Foundation.ZoneConnectivity

/-- The `9 | 11 | 13` zone label, as in `D0.Claims.Signature31Split.zone31`. -/
def zone (i : Fin 33) : Fin 3 :=
  if i.val < 9 then 0 else if i.val < 20 then 1 else 2

/-- The generator relation: `i` and `i+1` are joined when they share a zone. These are exactly the
`8 + 10 + 12 = 30` within-zone adjacent transpositions. -/
def Gen (i j : Fin 33) : Prop :=
  (j.val = i.val + 1 ∧ zone i = zone j) ∨ (i.val = j.val + 1 ∧ zone i = zone j)

/-- Reachability in the generator graph — the orbit relation of the generated group. -/
def Reach : Fin 33 → Fin 33 → Prop := Relation.ReflTransGen Gen

theorem gen_symm {i j : Fin 33} (h : Gen i j) : Gen j i := by
  rcases h with ⟨hv, hz⟩ | ⟨hv, hz⟩
  · exact Or.inr ⟨hv, hz.symm⟩
  · exact Or.inl ⟨hv, hz.symm⟩

theorem gen_sameZone {i j : Fin 33} (h : Gen i j) : zone i = zone j := by
  rcases h with ⟨_, hz⟩ | ⟨_, hz⟩ <;> exact hz

/-- **Reachability never leaves a zone.** -/
theorem reach_imp_sameZone {i j : Fin 33} (h : Reach i j) : zone i = zone j := by
  induction h with
  | refl => rfl
  | tail _ hstep ih => exact ih.trans (gen_sameZone hstep)

/-- Reachability is symmetric, the generator relation being symmetric. -/
theorem reach_symm {i j : Fin 33} (h : Reach i j) : Reach j i := by
  induction h with
  | refl => exact Relation.ReflTransGen.refl
  | tail _ hstep ih => exact (Relation.ReflTransGen.single (gen_symm hstep)).trans ih

/-- The zone label is constant on each of the three index intervals. -/
theorem zone_eq_of_val_lt_nine {i j : Fin 33} (hi : i.val < 9) (hj : j.val < 9) :
    zone i = zone j := by simp [zone, hi, hj]

/-- Stepping up by one inside a zone is a generator step. -/
theorem reach_succ (i : Fin 33) (h : i.val + 1 < 33)
    (hz : zone i = zone ⟨i.val + 1, h⟩) : Reach i ⟨i.val + 1, h⟩ :=
  Relation.ReflTransGen.single (Or.inl ⟨rfl, hz⟩)

/-- **Inside a zone, everything is reachable from everything.** Proved by walking up from the
smaller index; each step stays inside the zone because a zone is an interval. -/
theorem sameZone_imp_reach : ∀ i j : Fin 33, zone i = zone j → Reach i j := by
  have key : ∀ d : ℕ, ∀ i j : Fin 33, j.val = i.val + d → zone i = zone j → Reach i j := by
    intro d
    induction d with
    | zero =>
      intro i j hij _
      have : i = j := Fin.ext (by omega)
      exact this ▸ Relation.ReflTransGen.refl
    | succ d ih =>
      intro i j hij hz
      have hlt : i.val + 1 < 33 := by omega
      set m : Fin 33 := ⟨i.val + 1, hlt⟩ with hm
      have hzm : zone i = zone m := by
        -- the zone label is monotone in the index and agrees at the two ends
        have h1 : zone i ≤ zone m := by
          simp only [zone, hm]; split_ifs <;> simp_all <;> omega
        have h2 : zone m ≤ zone j := by
          simp only [zone, hm]; split_ifs <;> simp_all <;> omega
        exact le_antisymm h1 (hz ▸ h2)
      have hmj : zone m = zone j := by rw [← hzm]; exact hz
      exact (reach_succ i hlt hzm).trans (ih m j (by simp [hm]; omega) hmj)
  intro i j hz
  rcases le_total i.val j.val with h | h
  · exact key (j.val - i.val) i j (by omega) hz
  · exact reach_symm (key (i.val - j.val) j i (by omega) hz.symm)

/-- **The orbits are exactly the zones.** -/
theorem reach_iff_sameZone (i j : Fin 33) : Reach i j ↔ zone i = zone j :=
  ⟨reach_imp_sameZone, sameZone_imp_reach i j⟩

end D0.Foundation.ZoneConnectivity
