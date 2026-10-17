import D0.Geometry.ArchiveRefinementTower
import D0.Geometry.ArchiveLightProfinite
import D0.CondensedAnchor.DetectorSupportGoldenWeight
import Mathlib.Tactic

/-!
The literal BOOK_02 / GOLDEN 21.4 scalar compatibility rule, on the actual
archive diagram. This classifies that rule; it does not select the physically
admitted observable algebra or substitute it for the full price carrier.
The Hodge metric-collapse and scalar-subalgebra arguments in the companion
memo are analytic, not asserted to be formalized by these declarations.
-/

namespace D0.Research.NativeStrictObservableDescent
open D0
noncomputable section

def toBase : (n : ℕ) → ArchivePoints n → ArchivePoints 0
  | 0, x => x
  | n + 1, x => toBase n (archiveProjection n x)

def Compatible {α : Type*} (F : (n : ℕ) → ArchivePoints n → α) : Prop :=
  ∀ n x, F (n + 1) x = F n (archiveProjection n x)

def fromBase {α : Type*} (f : ArchivePoints 0 → α) :
    (n : ℕ) → ArchivePoints n → α := fun n x => f (toBase n x)

theorem toBase_surjective (n : ℕ) : Function.Surjective (toBase n) := by
  induction n with
  | zero => exact Function.surjective_id
  | succ n ih =>
      exact ih.comp (archive_projection_surjective n)

theorem fromBase_compatible {α : Type*} (f : ArchivePoints 0 → α) :
    Compatible (fromBase f) := by
  intro n x
  rfl

theorem compatible_factors_through_base {α : Type*}
    (F : (n : ℕ) → ArchivePoints n → α) (hF : Compatible F)
    (n : ℕ) (x : ArchivePoints n) : F n x = F 0 (toBase n x) := by
  induction n with
  | zero => rfl
  | succ n ih => exact (hF n x).trans (ih (archiveProjection n x))

theorem compatible_iff_base_pullback {α : Type*}
    (F : (n : ℕ) → ArchivePoints n → α) :
    Compatible F ↔ ∃ f : ArchivePoints 0 → α, F = fromBase f := by
  constructor
  · intro hF
    refine ⟨F 0, ?_⟩
    funext n x
    exact compatible_factors_through_base F hF n x
  · rintro ⟨f, rfl⟩
    exact fromBase_compatible f

theorem compatible_same_base_ext {α : Type*}
    (F G : (n : ℕ) → ArchivePoints n → α)
    (hF : Compatible F) (hG : Compatible G) (h0 : F 0 = G 0) : F = G := by
  funext n x
  rw [compatible_factors_through_base F hF,
    compatible_factors_through_base G hG, h0]

theorem compatible_ext_of_equal_at_any_level {α : Type*}
    (F G : (n : ℕ) → ArchivePoints n → α)
    (hF : Compatible F) (hG : Compatible G)
    (n : ℕ) (hn : F n = G n) : F = G := by
  apply compatible_same_base_ext F G hF hG
  funext y
  obtain ⟨x, hx⟩ := toBase_surjective n y
  have h := congrFun hn x
  rw [compatible_factors_through_base F hF n x,
    compatible_factors_through_base G hG n x, hx] at h
  exact h

theorem fromBase_injective {α : Type*} :
    Function.Injective (@fromBase α) := by
  intro f g hfg
  have h := congrArg (fun F => F 0) hfg
  exact h

def familyEquivBase (α : Type*) :
    {F : (n : ℕ) → ArchivePoints n → α // Compatible F} ≃
      (ArchivePoints 0 → α) where
  toFun F := F.1 0
  invFun f := ⟨fromBase f, fromBase_compatible f⟩
  left_inv F := by
    apply Subtype.ext
    funext n x
    exact (compatible_factors_through_base F.1 F.2 n x).symm
  right_inv _ := rfl

theorem same_base_fiber_indistinguishable {α : Type*}
    (F : (n : ℕ) → ArchivePoints n → α) (hF : Compatible F)
    (n : ℕ) (x y : ArchivePoints n) (hxy : toBase n x = toBase n y) :
    F n x = F n y := by
  rw [compatible_factors_through_base F hF n x,
    compatible_factors_through_base F hF n y, hxy]

theorem base_has_sixteen_points : Fintype.card (ArchivePoints 0) = 16 := by
  norm_num [ArchivePoints, archiveTower, archiveModes, archiveFibers]

theorem compatible_boolean_family_count :
    Fintype.card (ArchivePoints 0 → Bool) = 65536 := by
  rw [Fintype.card_fun, Fintype.card_bool, base_has_sixteen_points]
  norm_num

def zeroAt (n : ℕ) : ArchivePoints n :=
  ⟨0, by simp [archiveTower, archiveModes, archiveFibers]⟩

def birthOne : ArchivePoints 1 := ⟨16, by decide⟩

theorem first_birth_and_zero_same_actual_parent :
    archiveProjection 0 birthOne = archiveProjection 0 (zeroAt 1) := by
  apply Fin.ext
  norm_num [archiveProjection, birthOne, zeroAt,
    archiveTower, archiveModes, archiveFibers]

def freshTest : ArchivePoints 1 → Bool := fun x => decide (x.val = 16)

theorem fresh_test_distinguishes_actual_birth :
    freshTest birthOne = true ∧ freshTest (zeroAt 1) = false := by
  norm_num [freshTest, birthOne, zeroAt]

theorem fresh_test_has_no_base_pullback :
    ¬ ∃ f : ArchivePoints 0 → Bool,
      freshTest = fun x => f (archiveProjection 0 x) := by
  rintro ⟨f, hf⟩
  have hb := congrFun hf birthOne
  have hz := congrFun hf (zeroAt 1)
  rw [first_birth_and_zero_same_actual_parent] at hb
  have h := hb.trans hz.symm
  norm_num [freshTest, birthOne, zeroAt] at h

theorem fresh_test_has_no_strict_family :
    ¬ ∃ F : (n : ℕ) → ArchivePoints n → Bool,
      Compatible F ∧ F 1 = freshTest := by
  rintro ⟨F, hF, h1⟩
  apply fresh_test_has_no_base_pullback
  refine ⟨F 0, ?_⟩
  funext x
  rw [← h1]
  exact hF 0 x

def freshTail : (k : ℕ) → ArchivePoints (k + 1) → Bool
  | 0, x => freshTest x
  | k + 1, x => freshTail k (archiveProjection (k + 1) x)

theorem fresh_tail_persists_from_its_birth (k : ℕ)
    (x : ArchivePoints (k + 1 + 1)) :
    freshTail (k + 1) x = freshTail k (archiveProjection (k + 1) x) := rfl

theorem fresh_tail_starts_with_new_test : freshTail 0 = freshTest := rfl

-- The two actual inverse-limit records below agree at the base and differ
-- at level one. No new projection or history-reset rule is installed.
def birthThread : (n : ℕ) → ArchivePoints n
  | 0 => zeroAt 0
  | n + 1 => ⟨16, by
      change 16 < (n + 1 + 2)^4
      have hp : 2^4 < (n + 1 + 2)^4 :=
        Nat.pow_lt_pow_left (by omega) (by decide)
      norm_num at hp ⊢
      exact hp⟩

theorem birthThread_coherent (n : ℕ) :
    archiveProjection n (birthThread (n + 1)) = birthThread n := by
  apply Fin.ext
  cases n with
  | zero => norm_num [birthThread, zeroAt, archiveProjection,
      archiveTower, archiveModes, archiveFibers]
  | succ n =>
      change 16 % (n + 1 + 2)^4 = 16
      apply Nat.mod_eq_of_lt
      have hp : 2^4 < (n + 1 + 2)^4 :=
        Nat.pow_lt_pow_left (by omega) (by decide)
      norm_num at hp
      exact hp

theorem zeroThread_coherent (n : ℕ) :
    archiveProjection n (zeroAt (n + 1)) = zeroAt n := by
  apply Fin.ext
  simp [archiveProjection, zeroAt]

def actualBirthRecord : InverseLimit archiveProfiniteSystem :=
  ⟨birthThread, birthThread_coherent⟩

def actualZeroRecord : InverseLimit archiveProfiniteSystem :=
  ⟨zeroAt, zeroThread_coherent⟩

theorem two_actual_records_same_base_distinct :
    actualBirthRecord.1 0 = actualZeroRecord.1 0 ∧
      actualBirthRecord ≠ actualZeroRecord := by
  constructor
  · rfl
  · intro h
    have he := congrArg (fun w : InverseLimit archiveProfiniteSystem =>
      (w.1 1).val) h
    norm_num [actualBirthRecord, actualZeroRecord, birthThread, zeroAt] at he

theorem all_strict_readings_miss_actual_record_difference {α : Type*}
    (F : (n : ℕ) → ArchivePoints n → α) (hF : Compatible F) (n : ℕ) :
    F n (actualBirthRecord.1 n) = F n (actualZeroRecord.1 n) := by
  have hEval (w : InverseLimit archiveProfiniteSystem) :
      ∀ k, F k (w.1 k) = F 0 (w.1 0) := by
    intro k
    induction k with
    | zero => rfl
    | succ k ih =>
        have hw : archiveProjection k (w.1 (k + 1)) = w.1 k := w.2 k
        rw [hF, hw]
        exact ih
  rw [hEval actualBirthRecord n, hEval actualZeroRecord n]
  rfl

end
end D0.Research.NativeStrictObservableDescent

#check D0.Research.NativeStrictObservableDescent.toBase_surjective
#print axioms D0.Research.NativeStrictObservableDescent.toBase_surjective

#check D0.Research.NativeStrictObservableDescent.fromBase_compatible
#print axioms D0.Research.NativeStrictObservableDescent.fromBase_compatible

#check D0.Research.NativeStrictObservableDescent.compatible_factors_through_base
#print axioms D0.Research.NativeStrictObservableDescent.compatible_factors_through_base

#check D0.Research.NativeStrictObservableDescent.compatible_iff_base_pullback
#print axioms D0.Research.NativeStrictObservableDescent.compatible_iff_base_pullback

#check D0.Research.NativeStrictObservableDescent.compatible_same_base_ext
#print axioms D0.Research.NativeStrictObservableDescent.compatible_same_base_ext

#check D0.Research.NativeStrictObservableDescent.fromBase_injective
#print axioms D0.Research.NativeStrictObservableDescent.fromBase_injective

#check D0.Research.NativeStrictObservableDescent.same_base_fiber_indistinguishable
#print axioms D0.Research.NativeStrictObservableDescent.same_base_fiber_indistinguishable

#check D0.Research.NativeStrictObservableDescent.base_has_sixteen_points
#print axioms D0.Research.NativeStrictObservableDescent.base_has_sixteen_points

#check D0.Research.NativeStrictObservableDescent.compatible_boolean_family_count
#print axioms D0.Research.NativeStrictObservableDescent.compatible_boolean_family_count

#check D0.Research.NativeStrictObservableDescent.first_birth_and_zero_same_actual_parent
#print axioms D0.Research.NativeStrictObservableDescent.first_birth_and_zero_same_actual_parent

#check D0.Research.NativeStrictObservableDescent.fresh_test_distinguishes_actual_birth
#print axioms D0.Research.NativeStrictObservableDescent.fresh_test_distinguishes_actual_birth

#check D0.Research.NativeStrictObservableDescent.fresh_test_has_no_base_pullback
#print axioms D0.Research.NativeStrictObservableDescent.fresh_test_has_no_base_pullback

#check D0.Research.NativeStrictObservableDescent.fresh_test_has_no_strict_family
#print axioms D0.Research.NativeStrictObservableDescent.fresh_test_has_no_strict_family

#check D0.Research.NativeStrictObservableDescent.birthThread_coherent
#print axioms D0.Research.NativeStrictObservableDescent.birthThread_coherent

#check D0.Research.NativeStrictObservableDescent.zeroThread_coherent
#print axioms D0.Research.NativeStrictObservableDescent.zeroThread_coherent

#check D0.Research.NativeStrictObservableDescent.two_actual_records_same_base_distinct
#print axioms D0.Research.NativeStrictObservableDescent.two_actual_records_same_base_distinct

#check D0.Research.NativeStrictObservableDescent.all_strict_readings_miss_actual_record_difference
#print axioms D0.Research.NativeStrictObservableDescent.all_strict_readings_miss_actual_record_difference

#check D0.archive_projection_surjective
#print axioms D0.archive_projection_surjective

#check D0.archiveFintypeDiagram_succ
#print axioms D0.archiveFintypeDiagram_succ

#check D0.CondensedAnchor.readout_factors_through_finite_level
#print axioms D0.CondensedAnchor.readout_factors_through_finite_level

#check D0.Research.NativeStrictObservableDescent.compatible_ext_of_equal_at_any_level
#print axioms D0.Research.NativeStrictObservableDescent.compatible_ext_of_equal_at_any_level
#check D0.Research.NativeStrictObservableDescent.fresh_tail_persists_from_its_birth
#print axioms D0.Research.NativeStrictObservableDescent.fresh_tail_persists_from_its_birth
#check D0.Research.NativeStrictObservableDescent.fresh_tail_starts_with_new_test
#print axioms D0.Research.NativeStrictObservableDescent.fresh_tail_starts_with_new_test
