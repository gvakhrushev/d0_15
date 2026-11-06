import D0.Geometry.ArchiveGradedCochainRefinement
import D0.Geometry.ArchiveHodgeCARDirac
import Mathlib.Algebra.BigOperators.Ring.Finset

namespace D0.Geometry

open D0
open scoped BigOperators
noncomputable section

/-- Multiplicity of a coarse coordinate for a given occupation. -/
def archiveGramCoordinateWeight (occupied : Bool) (a : ZMod (archiveFibers N)) : ℝ :=
  if occupied then 1 else if a = 0 then 2 else 1

/-- Counting Gram weight at a literal group/Fock basis element. -/
def archiveGradedGramWeight (N : ℕ) (x : ArchiveRolePhaseGroup N)
    (S : ArchiveFockState) : ℝ :=
  archiveCochainScaleRatio (N + 1) ^ (2 * fockDegree S) *
    ∏ r : Role, archiveGramCoordinateWeight (S r) (x r)

/-- The single-coordinate occupation mask on the fine phase cycle. -/
def archiveFinEdgeMask (N : ℕ) (occupied : Bool) (i : archivePhaseIndex (N + 1)) : ℝ :=
  if occupied then (if i.val < N + 2 then 1 else 0) else 1

/-- One-dimensional weighted fiber count: vertices duplicate zero, whereas
occupied edges discard the collapsed fine edge. -/
theorem archive_fin_weighted_fiber (N : ℕ) (occupied : Bool) (j : archivePhaseIndex N) :
    (∑ i : archivePhaseIndex (N + 1), archiveFinEdgeMask N occupied i *
      (if archiveRGPhaseProjection N i = j then 1 else 0)) =
        (if occupied then 1 else if j = 0 then 2 else 1) := by
  classical
  have hlast : archiveRGPhaseProjection N (Fin.last (N + 2)) = 0 := by
    apply Fin.ext
    simp [archiveRGPhaseProjection, archiveFibers]
  have hcast : ∀ k : archivePhaseIndex N,
      archiveRGPhaseProjection N k.castSucc = k := by
    intro k
    apply Fin.ext
    exact Nat.mod_eq_of_lt k.isLt
  change (∑ i : Fin ((N + 2) + 1), archiveFinEdgeMask N occupied i *
      (if archiveRGPhaseProjection N i = j then 1 else 0)) = _
  rw [Fin.sum_univ_castSucc]
  have hsum : (∑ k : Fin (N + 2), archiveFinEdgeMask N occupied k.castSucc *
      (if archiveRGPhaseProjection N k.castSucc = j then 1 else 0)) = 1 := by
    calc
      _ = ∑ k : Fin (N + 2), (if k = j then (1 : ℝ) else 0) := by
        apply Finset.sum_congr rfl
        intro k hk
        calc
          _ = archiveFinEdgeMask N occupied k.castSucc *
              (if k = j then 1 else 0) :=
            congrArg (fun a => archiveFinEdgeMask N occupied k.castSucc *
              (if a = j then 1 else 0)) (hcast k)
          _ = _ := by simp [archiveFinEdgeMask, k.isLt]
      _ = 1 := by simp
  rw [hsum, hlast]
  cases occupied <;> by_cases hj : j = 0 <;>
    simp [archiveFinEdgeMask, eq_comm, hj] <;> norm_num

/-- The real occupancy mask is the product of its four 0/1 edge factors. -/
theorem archive_occupancy_mask_product (S : ArchiveFockState) (allowed : Role → Bool) :
    archiveOccupancyMask S allowed =
      ∏ r : Role, (if S r = true then (if allowed r = true then (1 : ℝ) else 0) else 1) := by
  classical
  by_cases h : ∀ r : Role, S r = true → allowed r = true
  · simp only [archiveOccupancyMask, if_pos h]
    symm
    apply Finset.prod_eq_one
    intro r hr
    by_cases hs : S r = true
    · simp [hs, h r hs]
    · simp [hs]
  · simp only [archiveOccupancyMask, if_neg h]
    push Not at h
    obtain ⟨r, hr, ha⟩ := h
    apply (Finset.prod_eq_zero (Finset.mem_univ r) ?_).symm
    simp [hr, ha]

/-- The fine mask and a coarse-site indicator factor across roles. -/
theorem archive_fine_fiber_factor (N : ℕ) (S : ArchiveFockState)
    (x : ArchiveRolePhaseGroup N)
    (z : D0.ArchiveRolePhasePoint (N + 1)) :
    archiveOccupancyMask S (archiveRefinementAllowed N
        (archiveRolePhasePointGroupEquiv (N + 1) z)) *
      (if archiveRoleGroupProjection N (archiveRolePhasePointGroupEquiv (N + 1) z) = x
        then 1 else 0) =
      ∏ r : Role, archiveFinEdgeMask N (S r) (z r) *
        (if archiveRGPhaseProjection N (z r) = (finZModEquiv N).symm (x r)
          then 1 else 0) := by
  classical
  let y := archiveRolePhasePointGroupEquiv (N + 1) z
  have hi (r : Role) : archiveFineRoleIndex N r y = z r := by
    simp [y, archiveFineRoleIndex, archiveRolePhasePointGroupEquiv]
  have hp (r : Role) : (finZModEquiv N).symm (archiveRoleGroupProjection N y r) =
      archiveRGPhaseProjection N (z r) := by
    rw [archive_group_projection_role_index, hi]
  have he : archiveRoleGroupProjection N y = x ↔
      ∀ r : Role, archiveRGPhaseProjection N (z r) = (finZModEquiv N).symm (x r) := by
    constructor
    · intro h r
      rw [← hp r, h]
    · intro h
      funext r
      apply (finZModEquiv N).symm.injective
      exact (hp r).trans (h r)
  have hind : (if archiveRoleGroupProjection N y = x then (1 : ℝ) else 0) =
      ∏ r : Role, (if archiveRGPhaseProjection N (z r) = (finZModEquiv N).symm (x r)
        then (1 : ℝ) else 0) := by
    by_cases h : archiveRoleGroupProjection N y = x
    · rw [if_pos h]
      symm
      apply Finset.prod_eq_one
      intro r hr
      simp [(he.mp h) r]
    · rw [if_neg h]
      have hn : ¬ ∀ r : Role, archiveRGPhaseProjection N (z r) =
          (finZModEquiv N).symm (x r) := fun h' => h (he.mpr h')
      push Not at hn
      obtain ⟨r, hr⟩ := hn
      exact (Finset.prod_eq_zero (Finset.mem_univ r) (by simp [hr])).symm
  have hmask : archiveOccupancyMask S (archiveRefinementAllowed N y) =
      ∏ r : Role, archiveFinEdgeMask N (S r) (z r) := by
    rw [archive_occupancy_mask_product]
    apply Finset.prod_congr rfl
    intro r hr
    simp [archiveFinEdgeMask, archiveRefinementAllowed, hi]
  change archiveOccupancyMask S (archiveRefinementAllowed N y) *
    (if archiveRoleGroupProjection N y = x then 1 else 0) = _
  rw [hmask, hind, ← Finset.prod_mul_distrib]

/-- Weighted cardinality of each fiber of the actual group projection. -/
theorem archive_group_weighted_fiber (N : ℕ) (S : ArchiveFockState)
    (x : ArchiveRolePhaseGroup N) :
    (∑ y : ArchiveRolePhaseGroup (N + 1),
      archiveOccupancyMask S (archiveRefinementAllowed N y) *
        (if archiveRoleGroupProjection N y = x then 1 else 0)) =
      ∏ r : Role, archiveGramCoordinateWeight (S r) (x r) := by
  classical
  calc
    _ = ∑ z : D0.ArchiveRolePhasePoint (N + 1),
        archiveOccupancyMask S (archiveRefinementAllowed N
          (archiveRolePhasePointGroupEquiv (N + 1) z)) *
        (if archiveRoleGroupProjection N (archiveRolePhasePointGroupEquiv (N + 1) z) = x
          then 1 else 0) := by
            symm
            exact (archiveRolePhasePointGroupEquiv (N + 1)).sum_comp
              (fun y : ArchiveRolePhaseGroup (N + 1) =>
                archiveOccupancyMask S (archiveRefinementAllowed N y) *
                  (if archiveRoleGroupProjection N y = x then (1 : ℝ) else 0))
    _ = ∑ z : D0.ArchiveRolePhasePoint (N + 1), ∏ r : Role,
        archiveFinEdgeMask N (S r) (z r) *
          (if archiveRGPhaseProjection N (z r) = (finZModEquiv N).symm (x r)
            then 1 else 0) := by
              apply Finset.sum_congr rfl
              intro z hz
              exact archive_fine_fiber_factor N S x z
    _ = ∏ r : Role, ∑ i : archivePhaseIndex (N + 1),
        archiveFinEdgeMask N (S r) i *
          (if archiveRGPhaseProjection N i = (finZModEquiv N).symm (x r)
            then 1 else 0) := by
              simpa only [Fintype.piFinset_univ] using
                (Finset.sum_prod_piFinset (s := Finset.univ)
                  (g := fun r i => archiveFinEdgeMask N (S r) i *
                    (if archiveRGPhaseProjection N i = (finZModEquiv N).symm (x r)
                      then (1 : ℝ) else 0)))
    _ = _ := by
      apply Finset.prod_congr rfl
      intro r hr
      rw [archive_fin_weighted_fiber]
      simp [archiveGramCoordinateWeight, finZModEquiv, ZMod.finEquiv]

/-- The occupancy indicator is idempotent, as a real-valued 0/1 mask. -/
theorem archive_occupancy_mask_sq (S : ArchiveFockState) (allowed : Role → Bool) :
    archiveOccupancyMask S allowed * archiveOccupancyMask S allowed =
      archiveOccupancyMask S allowed := by
  classical
  unfold archiveOccupancyMask
  split <;> norm_num

/-- The actual pullback factors into a scale, an idempotent mask and the
literal role-group projection on the full cochain carrier. -/
theorem archive_pullback_pair_pointwise (N : ℕ) (ψ φ : ArchiveCochain N)
    (y : ArchiveRolePhaseGroup (N + 1)) (S : ArchiveFockState) :
    archiveGradedCochainPullback N ψ (y, S) *
        archiveGradedCochainPullback N φ (y, S) =
      (archiveCochainScaleRatio (N + 1) ^ (2 * fockDegree S) *
        archiveOccupancyMask S (archiveRefinementAllowed N y)) *
          (ψ (archiveRoleGroupProjection N y, S) *
            φ (archiveRoleGroupProjection N y, S)) := by
  simp only [archiveGradedCochainPullback]
  have hm := archive_occupancy_mask_sq S (archiveRefinementAllowed N y)
  rw [mul_comm 2, pow_mul, pow_two]
  calc
    _ = ((archiveCochainScaleRatio (N + 1) ^ fockDegree S *
      archiveCochainScaleRatio (N + 1) ^ fockDegree S) *
        (archiveOccupancyMask S (archiveRefinementAllowed N y) *
         archiveOccupancyMask S (archiveRefinementAllowed N y))) *
          (ψ (archiveRoleGroupProjection N y, S) * φ (archiveRoleGroupProjection N y, S)) := by ring
    _ = _ := by rw [hm]

/-- Gram pairing expressed as a weighted sum over the fine carrier. -/
theorem archive_graded_pairing_fine (N : ℕ) (ψ φ : ArchiveCochain N) :
    cochainPairing (N + 1) (archiveGradedCochainPullback N ψ)
      (archiveGradedCochainPullback N φ) =
    ∑ y : ArchiveRolePhaseGroup (N + 1), ∑ S : ArchiveFockState,
      (archiveCochainScaleRatio (N + 1) ^ (2 * fockDegree S) *
        archiveOccupancyMask S (archiveRefinementAllowed N y)) *
          (ψ (archiveRoleGroupProjection N y, S) *
            φ (archiveRoleGroupProjection N y, S)) := by
  unfold cochainPairing
  apply Finset.sum_congr rfl
  intro y hy
  apply Finset.sum_congr rfl
  intro S hS
  exact archive_pullback_pair_pointwise N ψ φ y S

/-- Weighted pushforward along the actual projection, for every coarse
observable. The weight is computed from all four role fibers. -/
theorem archive_group_weighted_pushforward (N : ℕ) (S : ArchiveFockState)
    (g : ArchiveRolePhaseGroup N → ℝ) :
    (∑ y : ArchiveRolePhaseGroup (N + 1),
      archiveOccupancyMask S (archiveRefinementAllowed N y) *
        g (archiveRoleGroupProjection N y)) =
    ∑ x : ArchiveRolePhaseGroup N,
      (∏ r : Role, archiveGramCoordinateWeight (S r) (x r)) * g x := by
  classical
  calc
    _ = ∑ y : ArchiveRolePhaseGroup (N + 1),
        archiveOccupancyMask S (archiveRefinementAllowed N y) *
          (∑ x : ArchiveRolePhaseGroup N,
            if archiveRoleGroupProjection N y = x then g x else 0) := by
              apply Finset.sum_congr rfl
              intro y hy
              simp
    _ = ∑ y : ArchiveRolePhaseGroup (N + 1), ∑ x : ArchiveRolePhaseGroup N,
        (archiveOccupancyMask S (archiveRefinementAllowed N y) *
          (if archiveRoleGroupProjection N y = x then 1 else 0)) * g x := by
            apply Finset.sum_congr rfl
            intro y hy
            rw [Finset.mul_sum]
            apply Finset.sum_congr rfl
            intro x hx
            by_cases h : archiveRoleGroupProjection N y = x <;> simp [h]
    _ = ∑ x : ArchiveRolePhaseGroup N, ∑ y : ArchiveRolePhaseGroup (N + 1),
        (archiveOccupancyMask S (archiveRefinementAllowed N y) *
          (if archiveRoleGroupProjection N y = x then 1 else 0)) * g x := by
            rw [Finset.sum_comm]
    _ = _ := by
      apply Finset.sum_congr rfl
      intro x hx
      rw [← Finset.sum_mul, archive_group_weighted_fiber]

/-- Exact diagonal counting Gram form of the degree-scaled pullback on the
full site × Fock carrier, with no normalization of its constituent sectors. -/
theorem archive_graded_cochain_gram (N : ℕ) (ψ φ : ArchiveCochain N) :
    cochainPairing (N + 1) (archiveGradedCochainPullback N ψ)
      (archiveGradedCochainPullback N φ) =
    ∑ x : ArchiveRolePhaseGroup N, ∑ S : ArchiveFockState,
      archiveGradedGramWeight N x S * (ψ (x, S) * φ (x, S)) := by
  classical
  rw [archive_graded_pairing_fine, Finset.sum_comm]
  conv_rhs => rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro S hS
  calc
    _ = archiveCochainScaleRatio (N + 1) ^ (2 * fockDegree S) *
      (∑ y : ArchiveRolePhaseGroup (N + 1),
        archiveOccupancyMask S (archiveRefinementAllowed N y) *
          (ψ (archiveRoleGroupProjection N y, S) *
            φ (archiveRoleGroupProjection N y, S))) := by
              rw [Finset.mul_sum]
              apply Finset.sum_congr rfl
              intro y hy
              ring
    _ = archiveCochainScaleRatio (N + 1) ^ (2 * fockDegree S) *
      (∑ x : ArchiveRolePhaseGroup N,
        (∏ r : Role, archiveGramCoordinateWeight (S r) (x r)) *
          (ψ (x, S) * φ (x, S))) := by
            exact congrArg
              (fun a : ℝ => archiveCochainScaleRatio (N + 1) ^ (2 * fockDegree S) * a)
              (archive_group_weighted_pushforward N S (fun x => ψ (x, S) * φ (x, S)))
    _ = _ := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro x hx
      simp only [archiveGradedGramWeight]
      ring

end
end D0.Geometry
