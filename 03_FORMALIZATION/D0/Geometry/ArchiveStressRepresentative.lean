import D0.Geometry.ArchiveVariationSpace
import D0.Geometry.ArchiveVariationDual
import D0.Geometry.ArchiveBianchiIdentity

namespace D0

def VariationEquivalent {n : Nat}
  (A B : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ) : Prop :=
  ∀ δ : AdmissibleLaplacianVariation n,
    variationPairing A δ = variationPairing B δ

noncomputable def canonicalStressRepresentative {n : Nat}
  (A : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ) :
  Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ :=
  symPart A

theorem raw_gradient_equivalent_to_canonical_stress (n : Nat) :
  VariationEquivalent (archiveCurvatureGradient n)
    (canonicalStressRepresentative (archiveCurvatureGradient n)) := by
  unfold VariationEquivalent canonicalStressRepresentative
  intro δ
  rw [pairing_depends_only_on_symmetric_part]

theorem canonical_stress_symmetric (n : Nat) :
  MatrixSymmetric (canonicalStressRepresentative (archiveCurvatureGradient n)) := by
  unfold canonicalStressRepresentative symPart MatrixSymmetric
  intro i j
  ring

def NO_GO_CANONICAL_STRESS_CONSERVATION_PROJECTION (n : Nat) : Prop :=
  ∃ A : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ,
    archiveDivergence (symPart A) ≠ 0

theorem canonical_stress_conservation_no_go (n : Nat) :
  NO_GO_CANONICAL_STRESS_CONSERVATION_PROJECTION n := by
  unfold NO_GO_CANONICAL_STRESS_CONSERVATION_PROJECTION
  have hn : 0 < archiveFibers n := by
    unfold archiveFibers
    omega
  let A : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ :=
    fun i j => if i.val = 0 ∧ j.val = 0 then 1 else 0
  use A
  intro h
  have h0 : archiveDivergence (symPart A) ⟨0, hn⟩ = 0 := congr_fun h ⟨0, hn⟩
  have hsum : (∑ j : archivePhaseIndex n, symPart A ⟨0, hn⟩ j) = 1 := by
    have h_term : ∀ j : archivePhaseIndex n,
      symPart A ⟨0, hn⟩ j = if j.val = 0 then 1 else 0 := by
      intro j
      unfold symPart A
      dsimp [A]
      simp
    simp_rw [h_term]
    rw [Finset.sum_eq_single (⟨0, hn⟩ : archivePhaseIndex n)]
    · simp
    · intro j _hj h_ne
      have hj_val : j.val ≠ 0 := fun hc => h_ne (Fin.ext hc)
      simp [hj_val]
    · intro h_mem
      exact False.elim (h_mem (Finset.mem_univ _))
  unfold archiveDivergence at h0
  rw [hsum] at h0
  norm_num at h0

end D0
