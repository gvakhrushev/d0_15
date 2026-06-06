import Mathlib.Data.Real.Basic
import D0.Geometry.ArchiveRefinementTower

namespace D0

abbrev archivePhaseIndex (n : Nat) := Fin (archiveFibers n)

def cyclicDistance (N : Nat) (i j : Fin N) : Nat :=
  min ((i.val + N - j.val) % N) ((j.val + N - i.val) % N)

noncomputable def archivePhaseDistance (n : Nat)
  (i j : archivePhaseIndex n) : ℝ :=
  (cyclicDistance (archiveFibers n) i j : ℝ) / archiveFibers n

theorem archivePhaseDistance_nonnegative (n : Nat) (i j : archivePhaseIndex n) :
  0 ≤ archivePhaseDistance n i j := by
  unfold archivePhaseDistance
  apply div_nonneg
  · exact Nat.cast_nonneg _
  · exact Nat.cast_nonneg _

theorem cyclicDistance_symmetric (N : Nat) (i j : Fin N) :
  cyclicDistance N i j = cyclicDistance N j i := by
  unfold cyclicDistance
  exact min_comm _ _

theorem archivePhaseDistance_symmetric (n : Nat) (i j : archivePhaseIndex n) :
  archivePhaseDistance n i j = archivePhaseDistance n j i := by
  unfold archivePhaseDistance
  rw [cyclicDistance_symmetric]

theorem cyclicDistance_zero_iff (N : Nat) (hN : 0 < N) (i j : Fin N) :
  cyclicDistance N i j = 0 ↔ i = j := by
  constructor
  · intro h
    unfold cyclicDistance at h
    have hmin := min_eq_zero.mp h
    apply Fin.ext
    rcases lt_trichotomy i.val j.val with h1 | h1 | h1
    · -- i.val < j.val
      cases hmin with
      | inl ha =>
        have h_lt : i.val + N - j.val < N := by omega
        rw [Nat.mod_eq_of_lt h_lt] at ha
        omega
      | inr hb =>
        have h_eq : j.val + N - i.val = (j.val - i.val) + N * 1 := by omega
        rw [h_eq] at hb
        have h_mod := Nat.add_mul_mod_self_left (j.val - i.val) N 1
        rw [h_mod] at hb
        have h_lt2 : j.val - i.val < N := by omega
        rw [Nat.mod_eq_of_lt h_lt2] at hb
        omega
    · -- i.val = j.val
      exact h1
    · -- i.val > j.val
      cases hmin with
      | inl ha =>
        have h_eq : i.val + N - j.val = (i.val - j.val) + N * 1 := by omega
        rw [h_eq] at ha
        have h_mod := Nat.add_mul_mod_self_left (i.val - j.val) N 1
        rw [h_mod] at ha
        have h_lt2 : i.val - j.val < N := by omega
        rw [Nat.mod_eq_of_lt h_lt2] at ha
        omega
      | inr hb =>
        have h_lt : j.val + N - i.val < N := by omega
        rw [Nat.mod_eq_of_lt h_lt] at hb
        omega
  · intro h
    subst h
    unfold cyclicDistance
    have h_sub : i.val + N - i.val = N := by omega
    have h1 : (i.val + N - i.val) % N = 0 := by
      rw [h_sub]
      exact Nat.mod_self N
    rw [h1]
    simp

theorem archivePhaseDistance_zero_iff (n : Nat) (i j : archivePhaseIndex n) :
  archivePhaseDistance n i j = 0 ↔ i = j := by
  unfold archivePhaseDistance
  have hF : 0 < archiveFibers n := by
    unfold archiveFibers
    omega
  rw [div_eq_zero_iff]
  have hF_real : (archiveFibers n : ℝ) ≠ 0 := by
    exact Nat.cast_ne_zero.mpr (ne_of_gt hF)
  simp [hF_real]
  exact cyclicDistance_zero_iff (archiveFibers n) hF i j

end D0
