import D0.Synthesis.EquivariantHyperchargeCarrier
import Mathlib.Tactic

/-!
# The equivariant normal form and the abelian archive

The corpus owns `dim Comm(Aut) = 12` twice over: as the isotype count `3²+1+1+1`
(`D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001`, "commutant = flavor-frame algebra
End(generation space) ⊕ ℂ³") and as the raw pair-orbit count "3 diag + 3 same-part + 6
cross-part" (`D0-RAW-SCENE-GRAPH-001`). This module gives the operator-level **normal form** —
elementary, swap-generated, no Schur machinery:

    `equivariant_normal_form`: every Aut-equivariant `M` satisfies
    `M u w = diagC (zone u)` if `u = w`, `offC (zone u)` if same zone `u ≠ w`,
    `crossC (zone u) (zone w)` otherwise —

i.e. determination by ≤ 12 structure constants (the `dim ≤ 12` direction; the equality and the
freeness of all 12 are owned at the count level, rows `D0-RAW-SCENE-GRAPH-001` /
`D0-RAW-COMMUTANT-WEDDERBURN-001` — cite, not re-mint).

Consequences proved here:

* `archive_scalar_action` — on the dark archive (all zone sums zero) an equivariant `M` acts as
  the **scalar** `diagC z − offC z` per zone. The archive part of the commutant is abelian —
  the `ℂ³` of the flavor-frame algebra, now with an explicit spectral formula.
* `archive_actions_commute` / `no_equivariant_archive_noncommutativity` — **any two equivariant
  operators commute on the archive** of the 33-scene.

**What this does and does NOT touch (post-skeptic 2026-08-02).** The Higgs condensation
blocker (`D0-HIGGS-FINITE-CONDENSATION-OWNER-001`, via `D0-HIGGS-PHASON-ORBIT-TRIVIAL-NOGO-001`)
is typed on a DIFFERENT carrier: a frozen idempotent `Q₀ ∈ M₂(ZMod 44)` with `[T, Q₀] ≠ 0`
against the 2×2 toral return — the campaign's own J2 typing note firewalls it: "NOT the 33-dim
scene". Moreover the GROUPE correction records the wall there as OWNERSHIP, not existence
(non-commuting idempotents abound on that carrier). This module therefore closes only the
*hypothetical 33-scene equivariant analogue* of a non-commuting archive action — a route the
Higgs campaign never named and whose carrier it explicitly excluded. No relocation of the
blocker's missing object is claimed. What IS new here: on the 33-scene, equivariant
non-commutativity exists only through the visible/cross structure constants — e.g. the
cross-indicator pair `M = [zone u = 0][zone w = 1]`, `N = [zone u = 1][zone w = 0]` has
`MN ≠ NM` (values 11 vs 0 on the zone-0 diagonal) while both are equivariant; this witness is
described, not formalized. The "only home" direction (a commutator annihilates every archive
component) uses an unformalized linearity step and is stated as a remark, not a theorem.

**Scope honesty.** No registry status changes; the Higgs PROOF-TARGET is untouched on its own
carrier. Same externality pattern as `EquivariantSeamNoGo` and `EquivariantHyperchargeCarrier`.
-/

namespace D0.Synthesis.EquivariantMatrixStructure

open D0.Synthesis.EquivariantSeamNoGo
open D0.Synthesis.EquivariantHyperchargeCarrier
open D0.Spectral.DarkArchiveStructure

/-- Zone representatives and second representatives. -/
def rep (z : Fin 3) : Fin 33 := if z = 0 then 0 else if z = 1 then 9 else 20
def rep2 (z : Fin 3) : Fin 33 := if z = 0 then 1 else if z = 1 then 10 else 21

theorem rep_zone : ∀ z, zone (rep z) = z := by decide
theorem rep2_zone : ∀ z, zone (rep2 z) = z := by decide
theorem rep_ne_rep2 : ∀ z, rep z ≠ rep2 z := by decide

/-- The twelve structure constants of an equivariant matrix. -/
def diagC (M : Fin 33 → Fin 33 → ℚ) (z : Fin 3) : ℚ := M (rep z) (rep z)
def offC (M : Fin 33 → Fin 33 → ℚ) (z : Fin 3) : ℚ := M (rep z) (rep2 z)
def crossC (M : Fin 33 → Fin 33 → ℚ) (z z' : Fin 3) : ℚ := M (rep z) (rep z')

/-- Diagonal entries are constant per zone: one swap. -/
theorem diag_constant (M : Fin 33 → Fin 33 → ℚ) (hM : Equivariant M) :
    ∀ u u' : Fin 33, zone u' = zone u → M u u = M u' u' := by
  intro u u' h
  have hs := hM u u' h.symm u u
  rw [Equiv.swap_apply_left] at hs
  exact hs.symm

/-- Same-zone off-diagonal entries are constant per zone: three swaps through a fresh vertex. -/
theorem samezone_offdiag_constant (M : Fin 33 → Fin 33 → ℚ) (hM : Equivariant M) :
    ∀ u w u' w' : Fin 33, u ≠ w → u' ≠ w' →
      zone u = zone w → zone u' = zone u → zone w' = zone u →
      M u w = M u' w' := by
  intro u w u' w' huw hu'w' hzw hzu' hzw'
  -- a fresh vertex t of the same zone, distinct from all four
  have hcard : ∀ z : Fin 3,
      9 ≤ (Finset.univ.filter (fun i : Fin 33 => zone i = z)).card := by decide
  set s := Finset.univ.filter (fun i : Fin 33 => zone i = zone u) with hs
  set T : Finset (Fin 33) := {u, w, u', w'} with hT
  have hTcard : T.card ≤ 4 := by
    have c1 := Finset.card_insert_le u ({w, u', w'} : Finset (Fin 33))
    have c2 := Finset.card_insert_le w ({u', w'} : Finset (Fin 33))
    have c3 := Finset.card_insert_le u' ({w'} : Finset (Fin 33))
    have c4 : ({w'} : Finset (Fin 33)).card = 1 := Finset.card_singleton _
    rw [hT]; omega
  have hnon : (s \ T).Nonempty := by
    rw [← Finset.card_pos]
    have h1 := Finset.le_card_sdiff T s
    have h2 := hcard (zone u)
    rw [← hs] at h2
    omega
  obtain ⟨t, ht⟩ := hnon
  rw [Finset.mem_sdiff, hs, Finset.mem_filter, hT] at ht
  obtain ⟨⟨-, htz⟩, htm⟩ := ht
  simp only [Finset.mem_insert, Finset.mem_singleton, not_or] at htm
  obtain ⟨htu, htw, htu', htw'⟩ := htm
  -- step A: (u, w) → (t, w) via swap u t
  have hA := hM u t htz.symm u w
  rw [Equiv.swap_apply_left,
    Equiv.swap_apply_of_ne_of_ne (Ne.symm huw) (fun h => htw h.symm)] at hA
  -- step B: (t, w) → (t, w') via swap w w'
  have hB := hM w w' (hzw.symm.trans hzw'.symm) t w
  rw [Equiv.swap_apply_left,
    Equiv.swap_apply_of_ne_of_ne htw htw'] at hB
  -- step C: (t, w') → (u', w') via swap t u'
  have hC := hM t u' (htz.trans hzu'.symm) t w'
  rw [Equiv.swap_apply_left,
    Equiv.swap_apply_of_ne_of_ne (fun h => htw' h.symm) (Ne.symm hu'w')] at hC
  -- chain: M u w = M t w = M t w' = M u' w'
  exact hA.symm.trans (hB.symm.trans hC.symm)

/-- **The normal form**: an equivariant matrix is determined by its twelve structure constants —
the Lean shape of `dim Comm(Aut) = 12 = 3 + 3 + 6` (pair-orbit count, `D0-RAW-SCENE-GRAPH-001`).
-/
theorem equivariant_normal_form (M : Fin 33 → Fin 33 → ℚ) (hM : Equivariant M)
    (u w : Fin 33) :
    M u w = if u = w then diagC M (zone u)
      else if zone u = zone w then offC M (zone u)
      else crossC M (zone u) (zone w) := by
  by_cases h1 : u = w
  · rw [if_pos h1, h1]
    exact diag_constant M hM w (rep (zone w)) (rep_zone (zone w)) |>.symm ▸
      (diag_constant M hM (rep (zone w)) w ((rep_zone (zone w)).symm ▸ rfl)).symm
  · rw [if_neg h1]
    by_cases h2 : zone u = zone w
    · rw [if_pos h2]
      exact samezone_offdiag_constant M hM u w (rep (zone u)) (rep2 (zone u))
        h1 (rep_ne_rep2 (zone u)) h2 (rep_zone (zone u)) (rep2_zone (zone u))
    · rw [if_neg h2]
      exact equivariant_cross_constant M hM u w (rep (zone u)) (rep (zone w))
        (rep_zone (zone u)).symm (rep_zone (zone w)).symm h2

/-- Weighted fiberwise collapse: a zone function against any vector sums by zone totals. -/
theorem sum_zone_weighted (g : Fin 3 → ℚ) (v : Fin 33 → ℚ) :
    (∑ w : Fin 33, g (zone w) * v w)
      = ∑ z : Fin 3, g z * (∑ w ∈ Finset.univ.filter (fun w => zone w = z), v w) := by
  rw [← Finset.sum_fiberwise Finset.univ zone (fun w => g (zone w) * v w)]
  refine Finset.sum_congr rfl (fun z _ => ?_)
  rw [Finset.mul_sum]
  exact Finset.sum_congr rfl (fun w hw => by rw [(Finset.mem_filter.mp hw).2])

/-- The zone-level tail of the per-summand decomposition, named so rewrites have a constant
head. -/
def gfun (M : Fin 33 → Fin 33 → ℚ) (zu z' : Fin 3) : ℚ :=
  if z' = zu then offC M zu else crossC M zu z'

theorem gfun_at_same (M : Fin 33 → Fin 33 → ℚ) (zu : Fin 3) :
    gfun M zu zu = offC M zu := by
  unfold gfun; rw [if_pos rfl]

theorem gfun_at_cross (M : Fin 33 → Fin 33 → ℚ) (zu z' : Fin 3) (h : z' ≠ zu) :
    gfun M zu z' = crossC M zu z' := by
  unfold gfun; rw [if_neg h]

/-- **The abelian archive**: on a zone-balanced (dark archive) vector an equivariant operator
acts as the scalar `diagC z − offC z` in each zone. -/
theorem archive_scalar_action (M : Fin 33 → Fin 33 → ℚ) (hM : Equivariant M)
    (v : Fin 33 → ℚ) (hv : ∀ z, zoneSum v z = 0) (u : Fin 33) :
    mulv M v u = (diagC M (zone u) - offC M (zone u)) * v u := by
  unfold mulv
  -- per-summand decomposition: a Kronecker part plus a zone-function part
  have hsplit : ∀ w : Fin 33, M u w * v w
      = (if w = u then (diagC M (zone u) - offC M (zone u)) * v w else 0)
        + gfun M (zone u) (zone w) * v w := by
    intro w
    rw [equivariant_normal_form M hM u w]
    by_cases h1 : u = w
    · subst h1
      rw [if_pos rfl, if_pos rfl, gfun_at_same]
      ring
    · rw [if_neg h1, if_neg (fun hc : w = u => h1 hc.symm)]
      by_cases h2 : zone u = zone w
      · rw [if_pos h2, ← h2, gfun_at_same]
        ring
      · rw [if_neg h2, gfun_at_cross M (zone u) (zone w) (fun hc : zone w = zone u => h2 hc.symm)]
        ring
  rw [Finset.sum_congr rfl (fun w _ => hsplit w), Finset.sum_add_distrib]
  rw [Finset.sum_ite_eq' Finset.univ u
    (fun w => (diagC M (zone u) - offC M (zone u)) * v w)]
  rw [if_pos (Finset.mem_univ u), sum_zone_weighted (gfun M (zone u)) v]
  have hz0 : ∀ z : Fin 3,
      (∑ w ∈ Finset.univ.filter (fun w => zone w = z), v w) = 0 := fun z => hv z
  rw [Fin.sum_univ_three, hz0 0, hz0 1, hz0 2]
  ring

/-- **Any two equivariant operators commute on the archive** — the archive block of the
commutant is abelian, with the commutation witnessed by the explicit scalars. -/
theorem archive_actions_commute (M N : Fin 33 → Fin 33 → ℚ)
    (hM : Equivariant M) (hN : Equivariant N)
    (v : Fin 33 → ℚ) (hv : ∀ z, zoneSum v z = 0) :
    mulv M (mulv N v) = mulv N (mulv M v) := by
  funext u
  have hNv : ∀ z, zoneSum (mulv N v) z = 0 := (no_equivariant_seam N hN).1 v hv
  have hMv : ∀ z, zoneSum (mulv M v) z = 0 := (no_equivariant_seam M hM).1 v hv
  rw [archive_scalar_action M hM _ hNv u, archive_scalar_action N hN v hv u,
      archive_scalar_action N hN _ hMv u, archive_scalar_action M hM v hv u]
  ring

/-- **No-go: no equivariant non-commuting archive pair on the 33-scene.** (The Higgs blocker's
own carrier is `M₂(ZMod 44)` — untouched; see the module docstring.) -/
theorem no_equivariant_archive_noncommutativity :
    ¬ ∃ M N : Fin 33 → Fin 33 → ℚ, Equivariant M ∧ Equivariant N ∧
      ∃ v u, (∀ z, zoneSum v z = 0) ∧ mulv M (mulv N v) u ≠ mulv N (mulv M v) u := by
  rintro ⟨M, N, hM, hN, v, u, hv, hne⟩
  exact hne (congrFun (archive_actions_commute M N hM hN v hv) u)

end D0.Synthesis.EquivariantMatrixStructure
