import D0.Geometry.ArchiveCARRelations

namespace D0.Geometry

open D0

/-!
# Occupancy masks for archive cochains

The mask is one exactly when every occupied Fock direction is allowed.  It
records support only: it does not select a refinement or a physical readout.
-/

/-- Mask a Fock component when an occupied role is not allowed. -/
noncomputable def archiveOccupancyMask (state : ArchiveFockState)
    (allowed : Role → Bool) : ℝ := by
  classical
  exact if ∀ s : Role, state s = true → allowed s = true then 1 else 0

/-- Only the values of `allowed` at occupied roles can affect the mask. -/
theorem archiveOccupancyMask_congr (state : ArchiveFockState)
    (allowed allowed' : Role → Bool)
    (h : ∀ s : Role, state s = true → allowed s = allowed' s) :
    archiveOccupancyMask state allowed = archiveOccupancyMask state allowed' := by
  classical
  have hequiv : (∀ s : Role, state s = true → allowed s = true) ↔
      (∀ s : Role, state s = true → allowed' s = true) := by
    constructor
    · intro ha s hs
      rw [← h s hs]
      exact ha s hs
    · intro ha s hs
      rw [h s hs]
      exact ha s hs
  by_cases ha : ∀ s : Role, state s = true → allowed s = true
  · have ha' := hequiv.mp ha
    simp only [archiveOccupancyMask, if_pos ha, if_pos ha']
  · have ha' : ¬ (∀ s : Role, state s = true → allowed' s = true) :=
      fun h' => ha (hequiv.mpr h')
    simp only [archiveOccupancyMask, if_neg ha, if_neg ha']

/-- A nonzero creation entry adds precisely its new role to the mask.  The
CAR coefficient and its Jordan-Wigner sign remain unchanged. -/
theorem archiveOccupancyMask_carCreate (r : Role) (bra ket : ArchiveFockState)
    (allowed : Role → Bool) (hc : carCreate r bra ket ≠ 0) :
    archiveOccupancyMask bra allowed =
      (if allowed r = true then 1 else 0) * archiveOccupancyMask ket allowed := by
  classical
  obtain ⟨hbra, hket, hother⟩ := carCreate_support r bra ket hc
  have hequiv : (∀ s : Role, bra s = true → allowed s = true) ↔
      (allowed r = true ∧ ∀ s : Role, ket s = true → allowed s = true) := by
    constructor
    · intro ha
      refine ⟨ha r hbra, ?_⟩
      intro s hs
      have hsr : s ≠ r := by
        intro heq
        subst s
        rw [hket] at hs
        cases hs
      apply ha s
      rw [hother s hsr]
      exact hs
    · rintro ⟨hr, hk⟩ s hs
      by_cases hsr : s = r
      · subst s
        exact hr
      · apply hk s
        rw [← hother s hsr]
        exact hs
  by_cases hr : allowed r = true
  · by_cases hk : ∀ s : Role, ket s = true → allowed s = true
    · have hb := hequiv.mpr ⟨hr, hk⟩
      simp only [archiveOccupancyMask, if_pos hb, if_pos hr, if_pos hk, one_mul]
    · have hb : ¬ (∀ s : Role, bra s = true → allowed s = true) :=
        fun h => hk (hequiv.mp h).2
      simp only [archiveOccupancyMask, if_neg hb, if_pos hr, if_neg hk, one_mul]
  · have hb : ¬ (∀ s : Role, bra s = true → allowed s = true) :=
      fun h => hr (hequiv.mp h).1
    simp only [archiveOccupancyMask, if_neg hb, if_neg hr, zero_mul]

end D0.Geometry
