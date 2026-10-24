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

The general observed-matrix theorem takes an operator family `X_r` and keeps
the hypothesis that each operator equals the owned raising query for the
corresponding principal-frame column and a linear equivalence `M_r`. The
companion constructor `principalFrameJuliaQueryFamily` supplies that family
directly, so its matrix, coframe, and metric corollaries need no external
operator-representation premise. On the source's null chart, a composed
readout also recovers the selected role's endpoint map from its complete
query using the existing Eq. (28) inverse and its canonical witness.

This is finite matrix/query composition only. The module does not derive the
raising-query representation hypothesis for an arbitrary externally supplied
family, constrain `M_r` to the source's proper-Lorentz endpoint family, or
prove smoothness of the full inverse and `D R D Φ = I`. The null-chart result
retains symmetric nondegenerate endpoint forms, their isometry, a normalized
covector, and one selected nonzero null shift. Physical observer/clock recovery, the
all-jet and variational pullback (31), native price/source selection, and
physical execution remain open.
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

/-- The vector read from the complete vacuum response of one role query. -/
def principalFrameObservedQueryVector
    (X : Role → ArchiveJuliaQueryOperator) (r : Role) : RoleSpace :=
  (principalFrameObservedQueryColumnMatrix X).mulVec
    (Pi.single r (1 : ℝ))

/-- The concrete finite-carrier query family whose shifts are the columns of
the source's principal-frame matrix and whose role maps are `M`. -/
def principalFrameJuliaQueryFamily
    (F L : Matrix Role Role ℝ)
    (M : Role → RoleSpace ≃ₗ[ℝ] RoleSpace) :
    Role → ArchiveJuliaQueryOperator :=
  fun r => archiveJuliaCARRaisingQuery
    ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ))) (M r)

/-- The constructed family uses the repository-owned CAR creator matrices;
the existing full-carrier identity relates each query to the exterior model. -/
theorem principalFrameJuliaQueryFamily_eq_model
    (F L : Matrix Role Role ℝ)
    (M : Role → RoleSpace ≃ₗ[ℝ] RoleSpace) (r : Role) :
    principalFrameJuliaQueryFamily F L M r = archiveJuliaRaisingQuery
      ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ))) (M r) := by
  exact archiveJuliaCARRaisingQuery_eq_model
    ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ))) (M r)

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

/-- At every role the observed vector is exactly the corresponding source
column whenever the operator has the declared raising-query representation. -/
theorem principalFrameObservedQueryVector_eq
    (F L : Matrix Role Role ℝ)
    (M : Role → RoleSpace ≃ₗ[ℝ] RoleSpace)
    (X : Role → ArchiveJuliaQueryOperator)
    (hQuery : ∀ r, X r = archiveJuliaRaisingQuery
      ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ))) (M r))
    (r : Role) :
    principalFrameObservedQueryVector X r =
      (principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ)) := by
  unfold principalFrameObservedQueryVector
  rw [principalFrameObservedQueryColumnMatrix_eq F L M X hQuery]

/-- The concrete query family realizes the full Eq. (30a) column matrix with
no external operator-representation premise. -/
theorem principalFrameJuliaQueryFamily_columnMatrix
    (F L : Matrix Role Role ℝ)
    (M : Role → RoleSpace ≃ₗ[ℝ] RoleSpace) :
    principalFrameObservedQueryColumnMatrix
      (principalFrameJuliaQueryFamily F L M) =
        principalFrameColumnMatrix F L := by
  exact principalFrameObservedQueryColumnMatrix_eq F L M
    (principalFrameJuliaQueryFamily F L M)
    (principalFrameJuliaQueryFamily_eq_model F L M)

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

/-- The observed null-chart decoder for each complete role query. The vector
input is read from that same operator family, so the decoder does not receive
an independent coframe column. -/
def principalFrameObservedNullQueryFrameReadout
    (Pₓ Pᵧ : Role → ArchiveRoleBilinear)
    (X : Role → ArchiveJuliaQueryOperator)
    (α : Role → Module.Dual ℝ RoleSpace) :
    Role → RoleSpace → RoleSpace :=
  fun r => archiveJuliaQueryNullRecoveredFrame
    (Pₓ r) (Pᵧ r) (principalFrameObservedQueryVector X r) (X r) (α r)
      (archiveJuliaQueryNullCanonicalWitness
        (Pₓ r) (principalFrameObservedQueryVector X r) (X r) (α r))

/-- A complete finite-carrier query recovers the selected endpoint map on the
source's null chart. The theorem applies to any chosen role and does not
require the other three shifts to be null. It retains the endpoint-form
assumptions from Eq. (28); the canonical witness removes the separate
normalization and branch inputs. -/
theorem principalFrameJuliaQueryFamily_null_link_recovery
    (F L : Matrix Role Role ℝ)
    (M : Role → RoleSpace ≃ₗ[ℝ] RoleSpace)
    (Pₓ Pᵧ : Role → ArchiveRoleBilinear)
    (α : Role → Module.Dual ℝ RoleSpace)
    (r : Role)
    (hSymm : ∀ x y, Pₓ r x y = Pₓ r y x)
    (hNondegenerate : ∀ x, (∀ y, Pₓ r x y = 0) → x = 0)
    (hIso : ∀ x y, Pₓ r ((M r) x) ((M r) y) = Pᵧ r x y)
    (hα : α r
      ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ))) = 1)
    (hu : (principalFrameColumnMatrix F L).mulVec
      (Pi.single r (1 : ℝ)) ≠ 0)
    (hNull : Pₓ r
      ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ)))
      ((principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ))) = 0) :
    principalFrameObservedNullQueryFrameReadout Pₓ Pᵧ
      (principalFrameJuliaQueryFamily F L M) α r = M r := by
  let X := principalFrameJuliaQueryFamily F L M
  let u := (principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ))
  have hColumn : principalFrameObservedQueryVector X r = u := by
    exact principalFrameObservedQueryVector_eq F L M X
      (principalFrameJuliaQueryFamily_eq_model F L M) r
  have hX : X r = archiveJuliaRaisingQuery
      (principalFrameObservedQueryVector X r) (M r) := by
    calc
      X r = archiveJuliaRaisingQuery u (M r) := by
        simpa [X, u] using principalFrameJuliaQueryFamily_eq_model F L M r
      _ = archiveJuliaRaisingQuery
          (principalFrameObservedQueryVector X r) (M r) := by rw [hColumn]
  have hαu : α r (principalFrameObservedQueryVector X r) = 1 := by
    simpa [hColumn, u] using hα
  have hu' : principalFrameObservedQueryVector X r ≠ 0 := by
    simpa [hColumn, u] using hu
  have hNull' : Pₓ r (principalFrameObservedQueryVector X r)
      (principalFrameObservedQueryVector X r) = 0 := by
    simpa [hColumn, u] using hNull
  simpa [principalFrameObservedNullQueryFrameReadout, X] using
    archiveJuliaQueryNullRecoveredFrame_eq_of_null
      (Pₓ r) (Pᵧ r) (principalFrameObservedQueryVector X r) (M r)
      (α r) (X r) hX hαu hSymm hNondegenerate hIso hu' hNull'

/-- Coframe recovery specializes to the constructed family directly. -/
theorem principalFrameJuliaQueryFamily_coframeRecovery
    (F e Λ : Matrix Role Role ℝ)
    (M : Role → RoleSpace ≃ₗ[ℝ] RoleSpace)
    (hFe : F * e = 1) (hΛ : IsRoleLorentz Λ) :
    (principalFrameInverseCoframeReadout
      (principalFrameObservedQueryColumnMatrix
        (principalFrameJuliaQueryFamily F Λ.transpose M)))⁻¹ =
      Λ.transpose * e := by
  exact principalFrameObservedQueryCoframeRecovery F e Λ M
    (principalFrameJuliaQueryFamily F Λ.transpose M)
    (principalFrameJuliaQueryFamily_eq_model F Λ.transpose M) hFe hΛ

/-- Metric invariance for the constructed query family, reusing the same
principal-frame Lorentz map as the coframe readout. -/
theorem principalFrameJuliaQueryFamily_metric_invariant
    (F e Λ : Matrix Role Role ℝ)
    (M : Role → RoleSpace ≃ₗ[ℝ] RoleSpace)
    (hFe : F * e = 1) (hΛ : IsRoleLorentz Λ) :
    ((principalFrameInverseCoframeReadout
      (principalFrameObservedQueryColumnMatrix
        (principalFrameJuliaQueryFamily F Λ.transpose M)))⁻¹).transpose *
        roleLorentzMetric *
      (principalFrameInverseCoframeReadout
        (principalFrameObservedQueryColumnMatrix
          (principalFrameJuliaQueryFamily F Λ.transpose M)))⁻¹ =
        e.transpose * roleLorentzMetric * e := by
  rw [principalFrameJuliaQueryFamily_coframeRecovery F e Λ M hFe hΛ]
  exact principalFrame_metric_invariant_of_roleLorentz e Λ hΛ

end
end D0.Geometry
