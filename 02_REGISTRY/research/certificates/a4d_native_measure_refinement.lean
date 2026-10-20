import D0.Geometry.ArchiveLaplacianRG
import D0.Geometry.ArchiveRolePhaseProductCarrier
import D0.Probability.FiniteArchiveMeasure
import Mathlib.Data.Countable.Basic
import Mathlib.LinearAlgebra.Pi

/-! Research boundary for positive states on the actual Role point tower.
The probability/weak-limit theorems are proved analytically in the companion
note. No physical measure, refinement rule or new action is selected here. -/

namespace D0.Research.NativeMeasureRefinement
open scoped BigOperators
noncomputable section

local instance archiveFibersNeZero (n : ℕ) : NeZero (archiveFibers n) :=
  ⟨by simp [archiveFibers]⟩

def cap (L j : ℕ) : ℕ := if j < L then j else 0

theorem cap_lt (L j : ℕ) (hL : 0 < L) : cap L j < L := by
  unfold cap
  split_ifs <;> omega

theorem cap_comp (L M j : ℕ) (hL : 0 < L) (hLM : L ≤ M) :
    cap L (cap M j) = cap L j := by
  unfold cap
  split_ifs <;> omega

def doublingCollapse (x : ℝ) : ℝ := if x < 1/2 then 2*x else 0

theorem doubled_coordinate_readout (L j : ℕ) (hL : 0 < L) :
    (cap L j : ℝ)/(L:ℝ) = doublingCollapse ((j:ℝ)/(2*(L:ℝ))) := by
  have hLR : 0 < (L:ℝ) := by exact_mod_cast hL
  have h2 : 0 < 2*(L:ℝ) := by positivity
  have hh : (1/2:ℝ)*(2*(L:ℝ)) = (L:ℝ) := by ring
  have hc : (j:ℝ)/(2*(L:ℝ)) < 1/2 ↔ j < L := by
    rw [div_lt_iff₀ h2, hh]
    norm_cast
  by_cases hj : j < L
  · simp only [cap, if_pos hj, doublingCollapse, if_pos (hc.mpr hj)]
    field_simp
  · have hn : ¬ (j:ℝ)/(2*(L:ℝ)) < 1/2 := fun h => hj (hc.mp h)
    simp only [cap, if_neg hj, doublingCollapse, if_neg hn, Nat.cast_zero, zero_div]

theorem smooth_peak_recurrence_bound (n : ℕ) :
    (2*(n:ℝ)+1)^2*((n:ℝ)+2) ≤ 4*((n:ℝ)+1)^3 := by
  nlinarith [show (0:ℝ) ≤ (n:ℝ) from Nat.cast_nonneg n]

theorem actual_projection_cap (n : ℕ) (x : archivePhaseIndex (n+1)) :
    (archiveRGPhaseProjection n x).val = cap (n+2) x.val := by
  change x.val % (n+2) = _
  by_cases h : x.val < n+2
  · simp [cap, h, Nat.mod_eq_of_lt h]
  · have hx := x.isLt
    change x.val < n+1+2 at hx
    have he : x.val = n+2 := by omega
    simp [cap, he]

def PhaseHistory :=
  {x : (n : ℕ) → archivePhaseIndex n //
    ∀ n, archiveRGPhaseProjection n (x (n+1)) = x n}

theorem history_step (x : PhaseHistory) (n : ℕ) :
    (x.1 n).val = cap (n+2) (x.1 (n+1)).val := by
  rw [← x.2 n, actual_projection_cap]

theorem history_composite (x : PhaseHistory) (n m : ℕ) (hnm : n ≤ m) :
    (x.1 n).val = cap (n+2) (x.1 m).val := by
  induction m, hnm using Nat.le_induction with
  | base =>
      have hlt : (x.1 n).val < n+2 := (x.1 n).isLt
      simp [cap, hlt]
  | succ m hnm ih =>
      calc
        (x.1 n).val = cap (n+2) (x.1 m).val := ih
        _ = cap (n+2) (cap (m+2) (x.1 (m+1)).val) := by rw [history_step x m]
        _ = cap (n+2) (x.1 (m+1)).val := cap_comp _ _ _ (by omega) (by omega)

theorem history_nonzero_persists (x : PhaseHistory) (n m : ℕ)
    (hnm : n ≤ m) (hn : (x.1 n).val ≠ 0) : (x.1 m).val = (x.1 n).val := by
  have h := history_composite x n m hnm
  by_cases hm : (x.1 m).val < n+2
  · simpa [cap, hm] using h.symm
  · simp only [cap, if_neg hm] at h
    exact False.elim (hn h)

/-- The countability argument in the published archive-record proof is now
bound to the actual phase owner. Zero codes the all-zero history. -/
theorem every_history_has_birth_code (x : PhaseHistory) :
    ∃ k : ℕ, ∀ n, (x.1 n).val = cap (n+2) k := by
  by_cases h : ∀ n, (x.1 n).val = 0
  · exact ⟨0, fun n => by simp [h n, cap]⟩
  · push Not at h
    obtain ⟨n, hn⟩ := h
    refine ⟨(x.1 n).val, fun m => ?_⟩
    by_cases hm : m ≤ n
    · exact history_composite x m n hm
    · have hval := history_nonzero_persists x n m (by omega) hn
      have hlt : (x.1 n).val < m+2 := by
        rw [← hval]
        exact (x.1 m).isLt
      simp [cap, hlt, hval]

def historyOfCode (k : ℕ) : PhaseHistory :=
  ⟨fun n => ⟨cap (n+2) k, cap_lt _ _ (by omega)⟩, by
    intro n
    apply Fin.ext
    rw [actual_projection_cap]
    exact cap_comp _ _ _ (by omega) (by omega)⟩

theorem historyOfCode_injective : Function.Injective historyOfCode := by
  intro k j h
  have he := congrArg (fun x : PhaseHistory => (x.1 (k+j)).val) h
  have hk : k < k+j+2 := by omega
  have hj : j < k+j+2 := by omega
  simpa [historyOfCode, cap, hk, hj] using he

theorem historyOfCode_surjective : Function.Surjective historyOfCode := by
  intro x
  obtain ⟨k,hk⟩ := every_history_has_birth_code x
  refine ⟨k, ?_⟩
  apply Subtype.ext
  funext n
  apply Fin.ext
  exact (hk n).symm

def phaseHistoryEquiv : ℕ ≃ PhaseHistory :=
  Equiv.ofBijective historyOfCode ⟨historyOfCode_injective,historyOfCode_surjective⟩

theorem phase_histories_countable : Countable PhaseHistory :=
  Countable.of_equiv ℕ phaseHistoryEquiv

open D0.Geometry.ArchiveRolePhaseProductCarrier

def RoleHistory :=
  {x : (n : ℕ) → ArchiveRolePhasePoint n //
    ∀ n r, archiveRGPhaseProjection n (x (n+1) r) = x n r}

def roleHistoryEquiv : RoleHistory ≃ (Role → PhaseHistory) where
  toFun x r := ⟨fun n => x.1 n r, fun n => x.2 n r⟩
  invFun f := ⟨fun n r => (f r).1 n, fun n r => (f r).2 n⟩
  left_inv _ := rfl
  right_inv _ := rfl

theorem actual_role_histories_countable : Countable RoleHistory := by
  letI : Countable PhaseHistory := phase_histories_countable
  exact Countable.of_equiv (Role → PhaseHistory) roleHistoryEquiv.symm

variable {I J : Type*} [Fintype I] [DecidableEq I] [Fintype J]

def pointTest (i : I) : I → ℝ := fun j => if j=i then 1 else 0

theorem linear_state_has_weights (s : (I → ℝ) →ₗ[ℝ] ℝ) (f : I → ℝ) :
    s f = ∑ i, s (pointTest i) * f i := by
  have hf : f = ∑ i, f i • pointTest i := by
    funext j
    simp [pointTest, Finset.sum_apply]
  calc
    s f = s (∑ i, f i • pointTest i) := congrArg s hf
    _ = ∑ i, s (pointTest i) * f i := by
      rw [map_sum]
      simp [smul_eq_mul, mul_comm]

omit [Fintype I] in
theorem positive_state_weights_nonnegative (s : (I → ℝ) →ₗ[ℝ] ℝ)
    (hp : ∀ f, (∀ i, 0 ≤ f i) → 0 ≤ s f) (i : I) : 0 ≤ s (pointTest i) := by
  apply hp
  intro j
  unfold pointTest
  split_ifs <;> norm_num

theorem normalized_state_weights_sum_one (s : (I → ℝ) →ₗ[ℝ] ℝ)
    (hn : s (fun _ => 1)=1) : ∑ i, s (pointTest i) = 1 := by
  simpa [hn] using (linear_state_has_weights s (fun _ => 1)).symm

def pushWeights (p : J → I) (w : J → ℝ) (i : I) : ℝ :=
  ∑ j, if p j=i then w j else 0

theorem pushWeights_duality (p : J → I) (w : J → ℝ) (f : I → ℝ) :
    (∑ i, pushWeights p w i * f i) = ∑ j, w j * f (p j) := by
  simp only [pushWeights, Finset.sum_mul]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro j _
  simp [ite_mul]

theorem pushWeights_mass (p : J → I) (w : J → ℝ) :
    (∑ i, pushWeights p w i) = ∑ j, w j := by
  simpa using pushWeights_duality p w (fun _ => 1)

omit [Fintype I] in
theorem pushWeights_nonnegative (p : J → I) (w : J → ℝ)
    (hw : ∀ j, 0 ≤ w j) (i : I) : 0 ≤ pushWeights p w i := by
  unfold pushWeights
  apply Finset.sum_nonneg
  intro j _
  split_ifs <;> simp [hw]

theorem state_compatibility_iff_weights (p : J → I) (w : J → ℝ) (v : I → ℝ) :
    (∀ f : I → ℝ, (∑ j, w j * f (p j)) = ∑ i, v i * f i) ↔
      pushWeights p w = v := by
  constructor
  · intro h
    funext i
    have hi := h (pointTest i)
    rw [← pushWeights_duality] at hi
    simpa [pointTest, mul_ite] using hi
  · intro h f
    rw [← pushWeights_duality, h]

theorem quadratic_pullback_isometry_iff (p : J → I) (w : J → ℝ) (v : I → ℝ) :
    (∀ f : I → ℝ, (∑ j, w j * (f (p j))^2) = ∑ i, v i * (f i)^2) ↔
      pushWeights p w = v := by
  constructor
  · intro h
    funext i
    have hi := h (pointTest i)
    have hs : (fun x => (pointTest i x)^2) = pointTest i := by
      funext x
      simp [pointTest]
    change (∑ j, w j * ((fun x => (pointTest i x)^2) (p j))) = _ at hi
    rw [hs] at hi
    rw [← pushWeights_duality] at hi
    simpa [pointTest, mul_ite] using hi
  · intro h f
    exact (state_compatibility_iff_weights p w v).mpr h (fun i => (f i)^2)

theorem actual_scalar_mass_compatibility (n : ℕ)
    (w : archivePhaseIndex (n+1) → ℝ) (v : archivePhaseIndex n → ℝ) :
    (∀ f : archivePhaseIndex n → ℝ,
      (∑ j, w j * (f (archiveRGPhaseProjection n j))^2) = ∑ i, v i * (f i)^2) ↔
      pushWeights (archiveRGPhaseProjection n) w = v :=
  quadratic_pullback_isometry_iff _ _ _

theorem actual_uniform_zero_push (n : ℕ) :
    pushWeights (archiveRGPhaseProjection n)
      (fun _ => (1:ℝ)/(n+3)) 0 = 2/(n+3) := by
  unfold pushWeights
  change (∑ j : Fin (n+3), if archiveRGPhaseProjection n j=0 then (1:ℝ)/(n+3) else 0) = _
  rw [Fin.sum_univ_castSucc]
  have hold (j : Fin (n+2)) : archiveRGPhaseProjection n j.castSucc=j := by
    apply Fin.ext
    exact Nat.mod_eq_of_lt j.isLt
  have hlast : archiveRGPhaseProjection n (Fin.last (n+2))=0 := by
    apply Fin.ext
    simp [archiveRGPhaseProjection, archiveFibers]
  simp_rw [hold]
  simp only [hlast, if_true]
  change (∑ j : Fin (n+2), if j=0 then (1:ℝ)/(n+3) else 0) + 1/(n+3) = 2/(n+3)
  simp only [Finset.sum_ite_eq', Finset.mem_univ, if_true]
  ring

theorem actual_uniform_zero_defect (n : ℕ) :
    pushWeights (archiveRGPhaseProjection n)
      (fun _ => (1:ℝ)/(n+3)) 0 - 1/(n+2) =
        (n+1)/((n+2)*(n+3)) := by
  rw [actual_uniform_zero_push]
  have h2 : (n:ℝ)+2 ≠ 0 := by positivity
  have h3 : (n:ℝ)+3 ≠ 0 := by positivity
  field_simp
  ring

theorem actual_uniform_zero_defect_positive (n : ℕ) :
    0 < pushWeights (archiveRGPhaseProjection n)
      (fun _ => (1:ℝ)/(n+3)) 0 - 1/(n+2) := by
  rw [actual_uniform_zero_defect]
  positivity

theorem literal_eight_atom_stage_is_constant (n m : ℕ) :
    archiveStageMeasure n = archiveStageMeasure m := rfl

theorem literal_eight_atom_stage_cardinality (n : ℕ) :
    (archiveStageMeasure n).atomCount = 8 := rfl

#print axioms cap_comp
#print axioms doubled_coordinate_readout
#print axioms smooth_peak_recurrence_bound
#print axioms actual_projection_cap
#print axioms history_composite
#print axioms history_nonzero_persists
#print axioms every_history_has_birth_code
#print axioms historyOfCode_injective
#print axioms historyOfCode_surjective
#print axioms phase_histories_countable
#print axioms actual_role_histories_countable
#print axioms linear_state_has_weights
#print axioms positive_state_weights_nonnegative
#print axioms normalized_state_weights_sum_one
#print axioms pushWeights_duality
#print axioms pushWeights_mass
#print axioms pushWeights_nonnegative
#print axioms state_compatibility_iff_weights
#print axioms quadratic_pullback_isometry_iff
#print axioms actual_scalar_mass_compatibility
#print axioms actual_uniform_zero_push
#print axioms actual_uniform_zero_defect
#print axioms actual_uniform_zero_defect_positive
#print axioms literal_eight_atom_stage_is_constant
#print axioms literal_eight_atom_stage_cardinality
#check D0.archiveRGPhaseProjection
#check D0.Geometry.ArchiveRolePhaseProductCarrier.archive_role_phase_product_carrier_owner
#check D0.archiveStageMeasure
#check D0.Research.NativeMeasureRefinement.actual_role_histories_countable
#check D0.Research.NativeMeasureRefinement.actual_scalar_mass_compatibility

end
end D0.Research.NativeMeasureRefinement
