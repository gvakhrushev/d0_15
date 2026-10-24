import D0.Geometry.ArchiveJuliaRaisingOperatorReadout
import D0.Geometry.A4DRawSolderFrameAction

/-!
# Julia observation to principal-frame coframe recovery

This composes the finite-carrier vacuum readout (26) with the principal-frame
matrix identities (30a) from the published #334 source at commit
`fe5cf335da04cac14e50407b03f98b96be17dc52`, path
`02_REGISTRY/research/A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md`,
blob `1c8d59e5533b443d9a015dc4512cfbc160ae7e62`, §§8.4–8.5. The downstream
consumer is §5.1 of
`02_REGISTRY/research/A4D_EXACT_AF_RADIAL_COFRAME_EQUIVALENCE_NONLINEAR_SPIN2_2026_10_18.md`,
blob `734e21ae6bc04ff3446ad15858936d417fdd2e55`.

The observed matrix is assembled from four separate full-query vacuum
responses. Each query keeps its linear-equivalence argument `M_r` explicit;
the owned vacuum-readout theorem proves that response recovers its input
vector, independently of `M_r`. Under the stated inverse-coframe and
`IsRoleLorentz` hypotheses, the same observed matrix recovers `L e` and its
Lorentz metric equals that of `e`.

This is finite matrix/query composition only. The module does not constrain
`M_r` to the source's proper-Lorentz endpoint family, recover a physical
observer or clock, prove all-jet smoothness or the variational pullback (31),
or select a native price/source or physical execution.
-/

namespace D0.Geometry

open D0

noncomputable section

/-- Existing finite-carrier full-query operator type. -/
abbrev ArchiveJuliaQueryOperator :=
  (ArchiveFockState → ℝ) →ₗ[ℝ] (ArchiveFockState → ℝ)

/-- Matrix whose `r`-th column is read from the vacuum response of the actual
finite-carrier query operator family. -/
def principalFrameObservedQueryColumnMatrix
    (X : Role → ArchiveJuliaQueryOperator) : Matrix Role Role ℝ :=
  fun i r => archiveJuliaVacuumVectorReadout
    (X r (Pi.single fockVacuumState (1 : ℝ))) i

/-- Eq. (26) reads back each whole query vector, so the assembled observed
matrix is exactly the principal-frame column matrix in (30a), assuming the
actual operators have the stated raising-query form. -/
theorem principalFrameObservedQueryColumnMatrix_eq
    (F L : Matrix Role Role ℝ)
    (M : Role → RoleSpace ≃ₗ[ℝ] RoleSpace)
    (X : Role → ArchiveJuliaQueryOperator)
    (hQuery : ∀ r, X r = archiveJuliaRaisingQuery
      ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ))) (M r)) :
    principalFrameObservedQueryColumnMatrix X = principalFrameColumnMatrix F L := by
  ext i r
  rw [principalFrameObservedQueryColumnMatrix, hQuery r]
  simp [
    archiveJuliaVacuumVectorReadout_query]

/-- The full query-derived matrix recovers the transported coframe under the
same Lorentz convention already used by the solder-frame module. -/
theorem principalFrameObservedQueryCoframeRecovery
    (F e Λ : Matrix Role Role ℝ)
    (M : Role → RoleSpace ≃ₗ[ℝ] RoleSpace)
    (X : Role → ArchiveJuliaQueryOperator)
    (hQuery : ∀ r, X r = archiveJuliaRaisingQuery
      ((principalFrameColumnMatrix F Λ.transpose).mulVec
        (Pi.single r (1 : ℝ))) (M r))
    (hFe : F * e = 1) (hΛ : IsRoleLorentz Λ) :
    (principalFrameInverseCoframeReadout
      (principalFrameObservedQueryColumnMatrix X))⁻¹ =
        Λ.transpose * e := by
  rw [principalFrameObservedQueryColumnMatrix_eq F Λ.transpose M X hQuery]
  exact principalFrame_coframe_recovery_of_roleLorentz F e Λ hFe hΛ

/-- The metric reconstructed from all four query-derived coframe columns is
unchanged by the principal-frame Lorentz transport. -/
theorem principalFrameObservedQueryMetric_invariant
    (F e Λ : Matrix Role Role ℝ)
    (M : Role → RoleSpace ≃ₗ[ℝ] RoleSpace)
    (X : Role → ArchiveJuliaQueryOperator)
    (hQuery : ∀ r, X r = archiveJuliaRaisingQuery
      ((principalFrameColumnMatrix F Λ.transpose).mulVec
        (Pi.single r (1 : ℝ))) (M r))
    (hFe : F * e = 1) (hΛ : IsRoleLorentz Λ) :
    ((principalFrameInverseCoframeReadout
      (principalFrameObservedQueryColumnMatrix X))⁻¹).transpose *
        roleLorentzMetric *
      (principalFrameInverseCoframeReadout
        (principalFrameObservedQueryColumnMatrix X))⁻¹ =
          e.transpose * roleLorentzMetric * e := by
  rw [principalFrameObservedQueryCoframeRecovery F e Λ M X hQuery hFe hΛ]
  exact principalFrame_metric_invariant_of_roleLorentz e Λ hΛ

end
end D0.Geometry
