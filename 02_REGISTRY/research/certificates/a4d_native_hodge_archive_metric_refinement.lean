import D0.Geometry.ArchiveRefinementTower
import D0.Geometry.ArchiveLightProfinite
import Mathlib.Tactic

namespace D0.Research.NativeHodgeArchiveMetricRefinement
open D0
noncomputable section

def archiveZero (n : ℕ) : ArchivePoints n :=
  ⟨0, by simp [archiveTower, archiveModes, archiveFibers]⟩

def rawForget (n : ℕ) : ℕ → ℕ → ℕ
  | 0, x => x
  | k + 1, x => rawForget n k (x % (n + k + 2)^4)

def longProjection (n : ℕ) : (k : ℕ) → ArchivePoints (n + k) → ArchivePoints n
  | 0, x => x
  | k + 1, x => longProjection n k
      (archiveProjection (n + k)
        (cast (congrArg ArchivePoints (by omega : n + (k + 1) = (n + k) + 1)) x))

theorem actual_projection_val (n : ℕ) (x : ArchivePoints (n + 1)) :
    (archiveProjection n x).val = x.val % (n + 2)^4 := rfl

theorem rawForget_zero (n k : ℕ) : rawForget n k 0 = 0 := by
  induction k with
  | zero => rfl
  | succ k ih => simpa [rawForget] using ih

theorem longProjection_val (n k : ℕ) (x : ArchivePoints (n + k)) :
    (longProjection n k x).val = rawForget n k x.val := by
  induction k with
  | zero => rfl
  | succ k ih =>
      simp only [longProjection, rawForget]
      rw [ih]
      rfl

theorem rawForget_birth (n k j : ℕ) (hj : j < k) :
    rawForget n k ((n + j + 2)^4) = 0 := by
  induction k with
  | zero => omega
  | succ k ih =>
      rw [rawForget]
      by_cases he : j = k
      · subst j
        simp [rawForget_zero]
      · have hlt : j < k := by omega
        have hp : (n + j + 2)^4 < (n + k + 2)^4 :=
          Nat.pow_lt_pow_left (by omega) (by decide)
        rw [Nat.mod_eq_of_lt hp]
        exact ih hlt

def birthLabel (n k : ℕ) (j : Fin k) : ArchivePoints (n + k) :=
  ⟨(n + j.val + 2)^4, by
    change (n + j.val + 2)^4 < (n + k + 2)^4
    exact Nat.pow_lt_pow_left (by omega) (by decide)⟩

theorem birthLabel_injective (n k : ℕ) : Function.Injective (birthLabel n k) := by
  have hm : StrictMono (fun j : ℕ => (n + j + 2)^4) := by
    intro i j hij
    exact Nat.pow_lt_pow_left (by omega) (by decide)
  intro i j hij
  apply Fin.ext
  exact hm.injective (congrArg Fin.val hij)

theorem birthLabel_ne_zero (n k : ℕ) (j : Fin k) :
    birthLabel n k j ≠ archiveZero (n + k) := by
  intro he
  have hz := congrArg Fin.val he
  change (n + j.val + 2)^4 = 0 at hz
  have hp : 0 < (n + j.val + 2)^4 := by positivity
  omega

theorem longProjection_birth_zero (n k : ℕ) (j : Fin k) :
    longProjection n k (birthLabel n k j) = archiveZero n := by
  apply Fin.ext
  rw [longProjection_val]
  exact rawForget_birth n k j.val j.isLt

theorem longProjection_zero (n k : ℕ) :
    longProjection n k (archiveZero (n + k)) = archiveZero n := by
  apply Fin.ext
  rw [longProjection_val]
  exact rawForget_zero n k

def birthWitness (n k : ℕ) : Finset (ArchivePoints (n + k)) :=
  insert (archiveZero (n + k)) (Finset.univ.image (birthLabel n k))

theorem birthWitness_card (n k : ℕ) : (birthWitness n k).card = k + 1 := by
  have hn : archiveZero (n + k) ∉ Finset.univ.image (birthLabel n k) := by
    simp only [Finset.mem_image, Finset.mem_univ, true_and, not_exists]
    intro j
    exact birthLabel_ne_zero n k j
  rw [birthWitness, Finset.card_insert_of_notMem hn,
    Finset.card_image_of_injective _ (birthLabel_injective n k)]
  simp

theorem birthWitness_maps_zero (n k : ℕ) (x : ArchivePoints (n + k))
    (hx : x ∈ birthWitness n k) : longProjection n k x = archiveZero n := by
  simp only [birthWitness, Finset.mem_insert, Finset.mem_image,
    Finset.mem_univ, true_and] at hx
  rcases hx with he | ⟨j, he⟩
  · subst x
    exact longProjection_zero n k
  · rw [← he]
    exact longProjection_birth_zero n k j

theorem actual_long_zero_fiber_card_ge (n k : ℕ) :
    k + 1 ≤ (Finset.univ.filter
      (fun x : ArchivePoints (n + k) => longProjection n k x = archiveZero n)).card := by
  rw [← birthWitness_card n k]
  apply Finset.card_le_card
  intro x hx
  exact Finset.mem_filter.mpr ⟨Finset.mem_univ x, birthWitness_maps_zero n k x hx⟩

end
end D0.Research.NativeHodgeArchiveMetricRefinement

#check D0.Research.NativeHodgeArchiveMetricRefinement.actual_projection_val
#print axioms D0.Research.NativeHodgeArchiveMetricRefinement.actual_projection_val
#check D0.Research.NativeHodgeArchiveMetricRefinement.rawForget_zero
#print axioms D0.Research.NativeHodgeArchiveMetricRefinement.rawForget_zero
#check D0.Research.NativeHodgeArchiveMetricRefinement.longProjection_val
#print axioms D0.Research.NativeHodgeArchiveMetricRefinement.longProjection_val
#check D0.Research.NativeHodgeArchiveMetricRefinement.rawForget_birth
#print axioms D0.Research.NativeHodgeArchiveMetricRefinement.rawForget_birth
#check D0.Research.NativeHodgeArchiveMetricRefinement.birthLabel_injective
#print axioms D0.Research.NativeHodgeArchiveMetricRefinement.birthLabel_injective
#check D0.Research.NativeHodgeArchiveMetricRefinement.birthLabel_ne_zero
#print axioms D0.Research.NativeHodgeArchiveMetricRefinement.birthLabel_ne_zero
#check D0.Research.NativeHodgeArchiveMetricRefinement.longProjection_birth_zero
#print axioms D0.Research.NativeHodgeArchiveMetricRefinement.longProjection_birth_zero
#check D0.Research.NativeHodgeArchiveMetricRefinement.longProjection_zero
#print axioms D0.Research.NativeHodgeArchiveMetricRefinement.longProjection_zero
#check D0.Research.NativeHodgeArchiveMetricRefinement.birthWitness_card
#print axioms D0.Research.NativeHodgeArchiveMetricRefinement.birthWitness_card
#check D0.Research.NativeHodgeArchiveMetricRefinement.birthWitness_maps_zero
#print axioms D0.Research.NativeHodgeArchiveMetricRefinement.birthWitness_maps_zero
#check D0.Research.NativeHodgeArchiveMetricRefinement.actual_long_zero_fiber_card_ge
#print axioms D0.Research.NativeHodgeArchiveMetricRefinement.actual_long_zero_fiber_card_ge
#check D0.archive_record_kernel_projectively_compatible
#print axioms D0.archive_record_kernel_projectively_compatible
#check D0.archive_projection_surjective
#print axioms D0.archive_projection_surjective
#check D0.archiveFintypeDiagram_succ
#print axioms D0.archiveFintypeDiagram_succ
