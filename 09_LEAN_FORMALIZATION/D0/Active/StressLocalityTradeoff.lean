import D0.Geometry.ArchiveCanonicalLaplacian
import D0.Geometry.ArchiveVariationSpace
import D0.Geometry.ArchiveVariationDual
import D0.Geometry.ArchiveBianchiIdentity
import D0.Frozen.ConservedStressProjection

namespace D0

def StrictPhaseLocal {n : Nat} (M : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ) : Prop :=
  ∀ i j, ¬ (i = j ∨ archiveAdjacent n i j) → M i j = 0

def NO_GO_CONSTRAINED_STRESS_LOCALITY (n : Nat) : Prop :=
  ∃ G : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ,
    (∃ i : archivePhaseIndex n, (∑ k, symPart G i k) ≠ 0) ∧
    ¬ StrictPhaseLocal (conservedStressProjection G)

def ConstrainedStressLocalityDivergenceFreeNoGo (n : Nat) : Prop :=
  ∃ G : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ,
    archiveDivergence G = 0 ∧
    StrictPhaseLocal G ∧
    ¬ StrictPhaseLocal (conservedStressProjection G)

-- Concrete divergence-free local witness at n = 2 (archiveFibers 2 = 4, so Z/4Z):
-- G[0,0] = 1, G[0,1] = -1, all other entries zero.
theorem NO_GO_CONSTRAINED_STRESS_LOCALITY_DIVERGENCE_FREE :
  ConstrainedStressLocalityDivergenceFreeNoGo 2 := by
  let i0 : archivePhaseIndex 2 := ⟨0, by decide⟩
  let i1 : archivePhaseIndex 2 := ⟨1, by decide⟩
  let i2 : archivePhaseIndex 2 := ⟨2, by decide⟩
  let G : Matrix (archivePhaseIndex 2) (archivePhaseIndex 2) ℝ :=
    fun i j => if i = i0 ∧ j = i0 then 1 else if i = i0 ∧ j = i1 then -1 else 0
  use G
  have h_v_i0 : ∑ k : archivePhaseIndex 2, symPart G i0 k = 1 / 2 := by
    unfold symPart G
    simp only [i0, i1]
    change (∑ x : Fin 4,
      ((if x = (0 : Fin 4) then (1 : ℝ) else if x = (1 : Fin 4) then -1 else 0) +
        (if x = (0 : Fin 4) then (1 : ℝ) else 0)) / 2) = 1 / 2
    rw [Fin.sum_univ_four]
    norm_num [Fin.ext_iff]
  have h_v_i2 : ∑ k : archivePhaseIndex 2, symPart G i2 k = 0 := by
    unfold symPart G
    simp only [i0, i1, i2]
    norm_num [Fin.sum_univ_four]
  constructor
  · funext i
    unfold archiveDivergence
    by_cases hi : i = i0
    · subst i
      simp only [G, i0, i1]
      change (∑ x : Fin 4,
        if x = (0 : Fin 4) then (1 : ℝ) else if x = (1 : Fin 4) then -1 else 0) = 0
      rw [Fin.sum_univ_four]
      norm_num [Fin.ext_iff]
    · have h_row_zero : ∀ j : archivePhaseIndex 2, G i j = 0 := by
        intro j
        simp [G, hi]
      simp [h_row_zero]
  constructor
  · intro i j h_not
    by_cases h00 : i = i0 ∧ j = i0
    · exfalso
      apply h_not
      left
      rw [h00.1, h00.2]
    · by_cases h01 : i = i0 ∧ j = i1
      · exfalso
        apply h_not
        right
        rw [h01.1, h01.2]
        unfold archiveAdjacent cyclicDistance archiveFibers
        norm_num
      · simp [G, h00, h01]
  · intro h_local
    have h_not_adj : ¬ (i0 = i2 ∨ archiveAdjacent 2 i0 i2) := by
      intro hc
      cases hc with
      | inl h => exact absurd h (by decide)
      | inr h =>
        unfold archiveAdjacent cyclicDistance archiveFibers at h
        simp only [show i0.val = 0 from rfl, show i2.val = 2 from rfl] at h
        norm_num at h
    have h_zero := h_local i0 i2 h_not_adj
    have h_T_val : conservedStressProjection G i0 i2 = -1 / 8 := by
      show symPart G i0 i2 -
        (1 / (archiveFibers 2 : ℝ)) *
          ((∑ k : archivePhaseIndex 2, symPart G i0 k) +
           (∑ k : archivePhaseIndex 2, symPart G i2 k)) = -1 / 8
      have h_S_i0_i2 : symPart G i0 i2 = 0 := by
        unfold symPart G
        simp only [i0, i1, i2]
        norm_num
      have hfib : (archiveFibers 2 : ℝ) = 4 := by unfold archiveFibers; norm_num
      rw [h_S_i0_i2, h_v_i0, h_v_i2, hfib]
      norm_num
    rw [h_T_val] at h_zero
    norm_num at h_zero

-- Concrete witness at n = 2 (archiveFibers 2 = 4, so Fin 4)
-- G with a single nonzero entry G[0,0] = 1 → symPart G = G
-- v 0 = 1, v 2 = 0 → T[0,2] = -1/4 ≠ 0 but 0 and 2 are not adjacent in Z/4Z
theorem constrained_stress_locality_tradeoff :
  NO_GO_CONSTRAINED_STRESS_LOCALITY 2 := by
  let i0 : archivePhaseIndex 2 := ⟨0, by decide⟩
  let i2 : archivePhaseIndex 2 := ⟨2, by decide⟩
  let G : Matrix (archivePhaseIndex 2) (archivePhaseIndex 2) ℝ :=
    fun i j => if i = i0 ∧ j = i0 then 1 else 0
  use G
  -- Compute v i0 = 1 and v i2 = 0 using the Fin 4 sum expansion
  have h_S_eq : symPart G = G := by
    funext i j
    unfold symPart G
    by_cases h1 : i = i0 ∧ j = i0
    · simp [h1]
    · have h2 : ¬ (j = i0 ∧ i = i0) := fun h => h1 ⟨h.2, h.1⟩
      simp [h1, h2]
  have h_v_i0 : ∑ k : archivePhaseIndex 2, symPart G i0 k = 1 := by
    rw [h_S_eq]
    simp only [G, i0]
    norm_num
  have h_v_i2 : ∑ k : archivePhaseIndex 2, symPart G i2 k = 0 := by
    rw [h_S_eq]
    simp only [G, i2]
    norm_num
  constructor
  · -- v i0 = 1 ≠ 0
    exact ⟨i0, by rw [h_v_i0]; exact one_ne_zero⟩
  · -- StrictPhaseLocal fails: T i0 i2 ≠ 0 but i0, i2 not adjacent
    intro h_local
    have h_not_adj : ¬ (i0 = i2 ∨ archiveAdjacent 2 i0 i2) := by
      intro hc
      cases hc with
      | inl h => exact absurd h (by decide)
      | inr h =>
        unfold archiveAdjacent cyclicDistance archiveFibers at h
        -- substitute concrete values: i0.val = 0, i2.val = 2, N = 4
        simp only [show i0.val = 0 from rfl, show i2.val = 2 from rfl] at h
        norm_num at h
    have h_zero := h_local i0 i2 h_not_adj
    -- T i0 i2 = symPart G i0 i2 - (1/4)*(v i0 + v i2) = 0 - (1/4)*(1+0) = -1/4
    have h_T_val : conservedStressProjection G i0 i2 = -1 / 4 := by
      show symPart G i0 i2 -
        (1 / (archiveFibers 2 : ℝ)) *
          ((∑ k : archivePhaseIndex 2, symPart G i0 k) +
           (∑ k : archivePhaseIndex 2, symPart G i2 k)) = -1 / 4
      have h_S_i0_i2 : symPart G i0 i2 = 0 := by
        rw [h_S_eq]
        simp only [G]
        have h_ne : i2 ≠ i0 := by decide
        simp [h_ne]
      have hfib : (archiveFibers 2 : ℝ) = 4 := by unfold archiveFibers; norm_num
      rw [h_S_i0_i2, h_v_i0, h_v_i2, hfib]
      norm_num
    rw [h_T_val] at h_zero
    norm_num at h_zero

end D0
