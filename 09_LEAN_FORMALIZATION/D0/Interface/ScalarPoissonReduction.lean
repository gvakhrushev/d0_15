import D0.Interface.ArchiveLaplacian
import D0.Geometry.ArchiveWeakField
import D0.Geometry.ArchiveBianchiIdentity

namespace D0

def ScalarSectorStationary (n : Nat) (φ : ArchivePotential n) (ρ : archivePhaseIndex n → ℝ) : Prop :=
  ∀ η : archivePhaseIndex n → ℝ, (∑ i : archivePhaseIndex n, η i = 0) →
    (∑ i : archivePhaseIndex n, (Matrix.mulVec (archiveCanonicalLaplacian n) φ i - ρ i) * η i) = 0

theorem scalar_stationarity_implies_constant_difference
  (n : Nat)
  (φ : ArchivePotential n)
  (ρ : archivePhaseIndex n → ℝ)
  (h_stat : ScalarSectorStationary n φ ρ)
  (j k : archivePhaseIndex n) :
  (Matrix.mulVec (archiveCanonicalLaplacian n) φ j - ρ j) =
  (Matrix.mulVec (archiveCanonicalLaplacian n) φ k - ρ k) := by
  let F := fun i => Matrix.mulVec (archiveCanonicalLaplacian n) φ i - ρ i
  have h_sum_j : (∑ i, if i = j then (1 : ℝ) else 0) = 1 := by
    rw [Finset.sum_eq_single j]
    · simp
    · intro i _ hne
      rw [if_neg hne]
    · intro h
      exact False.elim (h (Finset.mem_univ _))
  have h_sum_k : (∑ i, if i = k then (1 : ℝ) else 0) = 1 := by
    rw [Finset.sum_eq_single k]
    · simp
    · intro i _ hne
      rw [if_neg hne]
    · intro h
      exact False.elim (h (Finset.mem_univ _))
  have h_sum_zero : (∑ i, ((if i = j then (1 : ℝ) else 0) - (if i = k then (1 : ℝ) else 0))) = 0 := by
    rw [Finset.sum_sub_distrib, h_sum_j, h_sum_k, sub_self]
  have h_test := h_stat (fun i => (if i = j then 1 else 0) - (if i = k then 1 else 0)) h_sum_zero
  have h_expand : (∑ i, F i * ((if i = j then (1 : ℝ) else 0) - (if i = k then (1 : ℝ) else 0))) =
    (∑ i, F i * (if i = j then (1 : ℝ) else 0)) - (∑ i, F i * (if i = k then (1 : ℝ) else 0)) := by
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro i _
    ring
  have h_single_j : (∑ i, F i * (if i = j then (1 : ℝ) else 0)) = F j := by
    rw [Finset.sum_eq_single j]
    · simp
    · intro i _ hne
      rw [if_neg hne, mul_zero]
    · intro h
      exact False.elim (h (Finset.mem_univ _))
  have h_single_k : (∑ i, F i * (if i = k then (1 : ℝ) else 0)) = F k := by
    rw [Finset.sum_eq_single k]
    · simp
    · intro i _ hne
      rw [if_neg hne, mul_zero]
    · intro h
      exact False.elim (h (Finset.mem_univ _))
  rw [h_expand, h_single_j, h_single_k] at h_test
  linarith

lemma archiveCanonicalLaplacian_sum_zero (n : Nat) (φ : ArchivePotential n) :
  (∑ i : archivePhaseIndex n, (Matrix.mulVec (archiveCanonicalLaplacian n) φ) i) = 0 := by
  unfold Matrix.mulVec dotProduct
  rw [Finset.sum_comm]
  have h_eq : ∀ j : archivePhaseIndex n, (∑ i : archivePhaseIndex n, archiveCanonicalLaplacian n i j * φ j) =
    φ j * ∑ i : archivePhaseIndex n, archiveCanonicalLaplacian n i j := by
    intro j
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i _
    ring
  simp_rw [h_eq]
  have h_sym : ∀ j : archivePhaseIndex n, (∑ i : archivePhaseIndex n, archiveCanonicalLaplacian n i j) = 0 := by
    intro j
    have h_row := archiveCanonicalLaplacian_row_sum_zero n j
    have h_swap : (∑ i : archivePhaseIndex n, archiveCanonicalLaplacian n i j) = ∑ i : archivePhaseIndex n, archiveCanonicalLaplacian n j i := by
      apply Finset.sum_congr rfl
      intro i _
      exact archiveCanonicalLaplacian_symmetric n i j
    rw [h_swap, h_row]
  simp_rw [h_sym, mul_zero, Finset.sum_const_zero]

theorem scalar_stationarity_implies_archive_poisson
  (n : Nat)
  (φ : ArchivePotential n)
  (ρ : archivePhaseIndex n → ℝ)
  (h_stat : ScalarSectorStationary n φ ρ)
  (h_neutral : NeutralSource ρ) :
  ArchivePoissonEquation φ ρ := by
  unfold ArchivePoissonEquation
  ext j
  let F := fun i => Matrix.mulVec (archiveCanonicalLaplacian n) φ i - ρ i
  have h_const : ∀ i, F i = F j := fun i => scalar_stationarity_implies_constant_difference n φ ρ h_stat i j
  have h_sum_F : (∑ i, F i) = (archiveFibers n : ℝ) * F j := by
    have h_sum_const : (∑ i, F i) = (∑ i : archivePhaseIndex n, F j) := Finset.sum_congr rfl (fun i _ => h_const i)
    rw [h_sum_const, Finset.sum_const, nsmul_eq_mul]
    have h_card : (Finset.univ : Finset (archivePhaseIndex n)).card = archiveFibers n := Fintype.card_fin (archiveFibers n)
    rw [h_card]
  have h_sum_zero : (∑ i, F i) = 0 := by
    unfold F
    rw [Finset.sum_sub_distrib, archiveCanonicalLaplacian_sum_zero, h_neutral]
    ring
  have h_fibers : 0 < archiveFibers n := by
    unfold archiveFibers
    omega
  have h_fibers_real : (archiveFibers n : ℝ) ≠ 0 := by
    exact Nat.cast_ne_zero.mpr (ne_of_gt h_fibers)
  rw [h_sum_zero] at h_sum_F
  have h_Fj_zero : F j = 0 := by
    calc
      F j = (1 / (archiveFibers n : ℝ)) * ((archiveFibers n : ℝ) * F j) := by
        rw [← mul_assoc, one_div_mul_cancel h_fibers_real, one_mul]
      _ = (1 / (archiveFibers n : ℝ)) * 0 := by rw [← h_sum_F]
      _ = 0 := mul_zero _
  exact sub_eq_zero.mp h_Fj_zero

end D0
