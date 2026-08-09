import D0.Spectral.DarkArchiveStructure
import Mathlib.Tactic

/-!
# No equivariant seam: the α-front Feshbach coupling must break the scene's symmetry

The flagship α route (`D0-ALPHA-FESHBACH-DIXMIER-OWNER-001`) works with the Feshbach–Schur
effective operator `W_eff(z) = A − B (D − zI)⁻¹ C` over the **active (rank 3) / archive (dim 30)**
split, and its honesty boundary declares the seam normalisation — the `2¹¹` active–archive
pairing — to be the *external* Dixmier extraction (`ASSUMP-DIXMIER-TRACE`). External is a scope
declaration. This module upgrades it to a necessity:

> **every operator on the scene that is equivariant under the same-zone swaps is block-diagonal
> across the active/archive split — its coupling blocks `B, C` vanish identically.**

Concretely: if `M` commutes with every same-zone transposition, then `M` maps zone-balanced
vectors to zone-balanced vectors (`archive_invariant`) and zone-constant vectors to zone-constant
vectors (`visible_invariant`). The split is the invariant/invariant-free split
(`D0.Spectral.DarkArchiveStructure`), so an equivariant `M` has `P_vis M P_arch = 0` and
`P_arch M P_vis = 0`; its `W_eff(z)` is `z`-independent and the residue functional of a constant
operator vanishes.

**Consequence for the α front.** A non-trivial Feshbach seam across this split cannot be produced
by any equivariant operator — not by the adjacency, the Laplacian, the normalised Laplacian, nor
any polynomial or equivariant combination of scene operators. Whatever realises the `2¹¹`
active–archive pairing necessarily carries symmetry-breaking data. The corpus's "EXTERNAL
Dixmier/Wodzicki extraction" is thereby not a modelling choice but a theorem: within the
equivariant class there is nothing to extract, so the finite-pole-sum machinery of
`D0-ALPHA-FESHBACH-RESIDUE-FINITE-SUM-001` must have its couplings imported from outside the
scene's symmetry — exactly what `ASSUMP-DIXMIER-TRACE` registers.

This is the operator-level face of the commutant count `12 = 3² + 1 + 1 + 1` (R1 leg of
`D0-P-M1-SATURATION-001`): the count says equivariant operators are a `3×3` visible block plus
three archive scalars; here the block-diagonality is proved directly from swap equivariance, with
no representation theory, so the α-front consequence is available at certificate grade.

**Hypothesis honesty.** Equivariance is assumed under every same-zone transposition. These lie in
`Aut = S₉ × S₁₁ × S₁₃` and generate it, so the hypothesis class is exactly the `Aut`-equivariant
operators. Nothing else is assumed of `M`: no symmetry, no normality, no integrality.
-/

namespace D0.Synthesis.EquivariantSeamNoGo

open D0.Spectral.DarkArchiveStructure

/-- Matrix–vector action, written out. -/
def mulv (M : Fin 33 → Fin 33 → ℚ) (v : Fin 33 → ℚ) : Fin 33 → ℚ :=
  fun u => ∑ w, M u w * v w

/-- Equivariance under every same-zone transposition — exactly `Aut`-equivariance, since these
transpositions generate `S₉ × S₁₁ × S₁₃`. -/
def Equivariant (M : Fin 33 → Fin 33 → ℚ) : Prop :=
  ∀ a b : Fin 33, zone a = zone b →
    ∀ u w, M (Equiv.swap a b u) (Equiv.swap a b w) = M u w

/-- A same-zone swap preserves the zone label. -/
theorem zone_swap (a b : Fin 33) (h : zone a = zone b) (u : Fin 33) :
    zone (Equiv.swap a b u) = zone u := by
  rcases eq_or_ne u a with rfl | hua
  · rw [Equiv.swap_apply_left]; exact h.symm
  · rcases eq_or_ne u b with rfl | hub
    · rw [Equiv.swap_apply_right]; exact h
    · rw [Equiv.swap_apply_of_ne_of_ne hua hub]

/-- A zone-constant vector is fixed by every same-zone swap. -/
theorem zoneConstant_swap_fixed (v : Fin 33 → ℚ)
    (hv : ∀ u w, zone u = zone w → v u = v w)
    (a b : Fin 33) (h : zone a = zone b) (u : Fin 33) :
    v (Equiv.swap a b u) = v u :=
  hv _ _ (zone_swap a b h u)

/-- A vector fixed by every same-zone swap is zone-constant: swap the two points themselves. -/
theorem swap_fixed_zoneConstant (v : Fin 33 → ℚ)
    (hfix : ∀ a b : Fin 33, zone a = zone b → ∀ u, v (Equiv.swap a b u) = v u)
    (u w : Fin 33) (huw : zone u = zone w) : v u = v w := by
  have h := hfix u w huw u
  rw [Equiv.swap_apply_left] at h
  exact h.symm

/-- Zone row sums of a matrix, in whole-universe form. -/
def rowSum (M : Fin 33 → Fin 33 → ℚ) (z : Fin 3) (w : Fin 33) : ℚ :=
  ∑ u, (if zone u = z then M u w else 0)

/-- **Equivariance makes each zone row sum a swap-fixed function of the column.** -/
theorem rowSum_swap_fixed (M : Fin 33 → Fin 33 → ℚ) (hM : Equivariant M) (z : Fin 3)
    (a b : Fin 33) (h : zone a = zone b) (w : Fin 33) :
    rowSum M z (Equiv.swap a b w) = rowSum M z w := by
  unfold rowSum
  calc ∑ u, (if zone u = z then M u (Equiv.swap a b w) else 0)
      = ∑ u, (if zone (Equiv.swap a b u) = z then
          M (Equiv.swap a b u) (Equiv.swap a b w) else 0) :=
        (Equiv.sum_comp (Equiv.swap a b)
          (fun u => if zone u = z then M u (Equiv.swap a b w) else 0)).symm
    _ = ∑ u, (if zone u = z then M u w else 0) := by
        refine Finset.sum_congr rfl fun u _ => ?_
        rw [zone_swap a b h u, hM a b h u w]

/-- Hence zone-constant in the column. -/
theorem rowSum_zoneConstant (M : Fin 33 → Fin 33 → ℚ) (hM : Equivariant M) (z : Fin 3)
    (w w' : Fin 33) (hww : zone w = zone w') : rowSum M z w = rowSum M z w' :=
  swap_fixed_zoneConstant (rowSum M z)
    (fun a b h u => rowSum_swap_fixed M hM z a b h u) w w' hww

/-- Zone representatives. -/
def rep (z : Fin 3) : Fin 33 :=
  if z = 0 then ⟨0, by omega⟩ else if z = 1 then ⟨9, by omega⟩ else ⟨20, by omega⟩

theorem zone_rep (z : Fin 3) : zone (rep z) = z := by
  fin_cases z <;> decide

/-- A sum against a zone-constant weight collapses to the three zone sums. -/
theorem weight_collapse (f v : Fin 33 → ℚ)
    (hf : ∀ u w, zone u = zone w → f u = f w) :
    (∑ w, f w * v w) = ∑ z : Fin 3, f (rep z) * zoneSum v z := by
  have hfib : (∑ w, f w * v w)
      = ∑ z : Fin 3, ∑ w ∈ Finset.univ.filter (fun w : Fin 33 => zone w = z),
          f w * v w := by
    rw [← Finset.sum_fiberwise Finset.univ zone (fun w => f w * v w)]
  rw [hfib]
  refine Finset.sum_congr rfl fun z _ => ?_
  unfold zoneSum
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl fun w hw => ?_
  have hz : zone w = z := (Finset.mem_filter.mp hw).2
  rw [hf w (rep z) (by rw [hz, zone_rep])]

/-- **The archive is invariant.** An equivariant `M` maps zone-balanced vectors to zone-balanced
vectors: the coupling out of the archive vanishes. -/
theorem archive_invariant (M : Fin 33 → Fin 33 → ℚ) (hM : Equivariant M)
    (v : Fin 33 → ℚ) (hv : ∀ z, zoneSum v z = 0) (z : Fin 3) :
    zoneSum (mulv M v) z = 0 := by
  have step1 : zoneSum (mulv M v) z = ∑ w, (rowSum M z w) * v w := by
    unfold zoneSum mulv rowSum
    rw [Finset.sum_filter]
    have hpush : (∑ u, (if zone u = z then (∑ w, M u w * v w) else 0))
        = ∑ u, ∑ w, (if zone u = z then M u w * v w else 0) := by
      refine Finset.sum_congr rfl fun u _ => ?_
      by_cases h : zone u = z
      · simp [h]
      · simp [h]
    rw [hpush, Finset.sum_comm]
    refine Finset.sum_congr rfl fun w _ => ?_
    rw [Finset.sum_mul]
    refine Finset.sum_congr rfl fun u _ => ?_
    by_cases h : zone u = z
    · simp [h]
    · simp [h]
  rw [step1, weight_collapse (rowSum M z) v (rowSum_zoneConstant M hM z)]
  simp [hv]

/-- **The visible block is invariant.** An equivariant `M` maps zone-constant vectors to
zone-constant vectors: the coupling into the archive vanishes. -/
theorem visible_invariant (M : Fin 33 → Fin 33 → ℚ) (hM : Equivariant M)
    (v : Fin 33 → ℚ) (hv : ∀ u w, zone u = zone w → v u = v w) :
    ∀ u w, zone u = zone w → mulv M v u = mulv M v w := by
  intro u w huw
  refine swap_fixed_zoneConstant (mulv M v) ?_ u w huw
  intro a b h u'
  unfold mulv
  calc ∑ w', M (Equiv.swap a b u') w' * v w'
      = ∑ w', M (Equiv.swap a b u') (Equiv.swap a b w') * v (Equiv.swap a b w') :=
        (Equiv.sum_comp (Equiv.swap a b)
          (fun w' => M (Equiv.swap a b u') w' * v w')).symm
    _ = ∑ w', M u' w' * v w' := by
        refine Finset.sum_congr rfl fun w' _ => ?_
        rw [hM a b h u' w', zoneConstant_swap_fixed v hv a b h w']

/-- **The no-seam theorem.** Every `Aut`-equivariant operator is block-diagonal across the
active/archive split: balanced stays balanced and zone-constant stays zone-constant. Its Feshbach
coupling blocks vanish, its `W_eff(z)` is `z`-independent, and its seam residue is zero. Any
non-trivial active–archive pairing must therefore break the scene's own symmetry. -/
theorem no_equivariant_seam (M : Fin 33 → Fin 33 → ℚ) (hM : Equivariant M) :
    (∀ v, (∀ z, zoneSum v z = 0) → ∀ z, zoneSum (mulv M v) z = 0) ∧
    (∀ v, (∀ u w, zone u = zone w → v u = v w) →
      ∀ u w, zone u = zone w → mulv M v u = mulv M v w) :=
  ⟨fun v hv z => archive_invariant M hM v hv z,
   fun v hv => visible_invariant M hM v hv⟩

end D0.Synthesis.EquivariantSeamNoGo
