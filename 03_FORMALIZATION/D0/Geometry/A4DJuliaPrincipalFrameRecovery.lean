import D0.Geometry.ArchiveJuliaRaisingOperatorReadout
import D0.Geometry.A4DRawSolderFrameAction
import Mathlib.Analysis.Calculus.FDeriv.Linear
import Mathlib.Analysis.Calculus.FDeriv.Mul
import Mathlib.Analysis.Matrix.Normed

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
operator-representation premise. A composed readout also recovers the selected
role's endpoint map from its complete query. The existing Eq. (28) inverse is
now composed on its full open chart, with the observed projected covector and
positive branch explicit; the null specialization derives those conditions
from nondegeneracy and the canonical witness.

This is finite matrix/query composition only. The module does not derive the
raising-query representation hypothesis for an arbitrary externally supplied
family, constrain `M_r` to the source's proper-Lorentz endpoint family, or
prove smoothness of the full inverse and `D R D Φ = I`. For the canonical
query family with a fixed Lorentz link map, it now proves the coframe block of
the readout derivative in all 16 matrix directions; the link directions are
still held fixed. The open-chart result retains symmetric endpoint forms,
their isometry, a normalized covector, a
nonzero projected metric covector, and the positive square-root branch. The
null specialization additionally retains nondegeneracy and one selected
nonzero null shift. The separate
`A4DJuliaNonNullGammaRecovery` module formalizes the Eq. (27) algebraic inverse
for nonzero Lorentz norm, conditional on explicit endpoint Clifford
conjugation and frame-covariance identities. Their derivation for the source's
proper-Lorentz endpoint package remains open, as do physical observer/clock
recovery, the all-jet and variational pullback (31), native price/source
selection, and physical execution.
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

/-- The Eq. (28) open-chart decoder for each complete role query. The retained
`Null` name marks its original use on the null locus; the decoder also applies
when the projected metric covector and positive-branch conditions hold away
from that locus. The vector is read from the same operator family. -/
def principalFrameObservedNullQueryFrameReadout
    (Pₓ Pᵧ : Role → ArchiveRoleBilinear)
    (X : Role → ArchiveJuliaQueryOperator)
    (α : Role → Module.Dual ℝ RoleSpace) :
    Role → RoleSpace → RoleSpace :=
  fun r => archiveJuliaQueryNullRecoveredFrame
    (Pₓ r) (Pᵧ r) (principalFrameObservedQueryVector X r) (X r) (α r)
      (archiveJuliaQueryNullCanonicalWitness
        (Pₓ r) (principalFrameObservedQueryVector X r) (X r) (α r))

/-- Generic Eq. (28) application for a complete query family. The caller
supplies the two actual maps used by the application: the query is the native
raising operator at `u` with endpoint map `M`, and the full vacuum readout is
that same `u`. This separates the reusable decoder from the principal-frame
matrix constructor below. -/
theorem principalFrameObservedQuery_open_chart_link_recovery
    (M : RoleSpace ≃ₗ[ℝ] RoleSpace)
    (Pₓ Pᵧ : Role → ArchiveRoleBilinear)
    (X : Role → ArchiveJuliaQueryOperator)
    (u : RoleSpace)
    (α : Role → Module.Dual ℝ RoleSpace)
    (r : Role)
    (hQuery : X r = archiveJuliaRaisingQuery u M)
    (hColumn : principalFrameObservedQueryVector X r = u)
    (hα : α r u = 1)
    (hSymm : ∀ x y, Pₓ r x y = Pₓ r y x)
    (hIso : ∀ x y, Pₓ r (M x) (M y) = Pᵧ r x y)
    (hCovector : archiveJuliaQueryNullMetricCovector (Pₓ r)
      (principalFrameObservedQueryVector X r) (X r) (α r) ≠ 0)
    (hBranch : 0 < 1 +
      Pₓ r (principalFrameObservedQueryVector X r)
        (principalFrameObservedQueryVector X r) *
        α r (M (archiveJuliaQueryNullCanonicalWitness (Pₓ r)
          (principalFrameObservedQueryVector X r) (X r) (α r)))) :
    principalFrameObservedNullQueryFrameReadout Pₓ Pᵧ X α r = M := by
  let v := principalFrameObservedQueryVector X r
  have hQuery' : X r = archiveJuliaRaisingQuery v M := by
    calc
      X r = archiveJuliaRaisingQuery u M := hQuery
      _ = archiveJuliaRaisingQuery v M := by
        dsimp [v]
        rw [← hColumn]
  have hα' : α r v = 1 := by
    dsimp [v]
    rw [hColumn]
    exact hα
  let z := archiveJuliaQueryNullCanonicalWitness (Pₓ r) v (X r) (α r)
  have hWitness : archiveJuliaQueryNullMetricCovector (Pₓ r) v (X r)
      (α r) z = 1 := by
    have h := archiveJuliaNullEuclideanWitness_normalized
      (archiveJuliaQueryNullMetricCovector (Pₓ r) v (X r) (α r)) hCovector
    simpa [z, archiveJuliaQueryNullCanonicalWitness] using h
  have hBranch' : 0 < 1 + (Pₓ r v v) * α r (M z) := by
    simpa [z, archiveJuliaQueryNullCanonicalWitness] using hBranch
  simpa [principalFrameObservedNullQueryFrameReadout, z, v] using
    (archiveJuliaQueryNullRecoveredFrame_eq
      (Pₓ r) (Pᵧ r) v z M (α r) (X r) hQuery' hα' hSymm hIso
      hWitness hBranch')

/-- Query-derived endpoint recovery on the full Eq. (28) open chart. The shift
need not be null: the actual projected metric covector must be nonzero and the
square-root branch must remain positive. The canonical witness supplies the
normalization from that same observed covector. -/
theorem principalFrameJuliaQueryFamily_open_chart_link_recovery
    (F L : Matrix Role Role ℝ)
    (M : Role → RoleSpace ≃ₗ[ℝ] RoleSpace)
    (Pₓ Pᵧ : Role → ArchiveRoleBilinear)
    (α : Role → Module.Dual ℝ RoleSpace)
    (r : Role)
    (hSymm : ∀ x y, Pₓ r x y = Pₓ r y x)
    (hIso : ∀ x y, Pₓ r ((M r) x) ((M r) y) = Pᵧ r x y)
    (hα : α r ((principalFrameColumnMatrix F L).mulVec
      (Pi.single r (1 : ℝ))) = 1)
    (hCovector : archiveJuliaQueryNullMetricCovector (Pₓ r)
      (principalFrameObservedQueryVector
        (principalFrameJuliaQueryFamily F L M) r)
      (principalFrameJuliaQueryFamily F L M r) (α r) ≠ 0)
    (hBranch : 0 < 1 +
      Pₓ r
        (principalFrameObservedQueryVector
          (principalFrameJuliaQueryFamily F L M) r)
        (principalFrameObservedQueryVector
          (principalFrameJuliaQueryFamily F L M) r) *
        α r ((M r) (archiveJuliaQueryNullCanonicalWitness (Pₓ r)
          (principalFrameObservedQueryVector
            (principalFrameJuliaQueryFamily F L M) r)
          (principalFrameJuliaQueryFamily F L M r) (α r)))) :
    principalFrameObservedNullQueryFrameReadout Pₓ Pᵧ
      (principalFrameJuliaQueryFamily F L M) α r = M r := by
  let X := principalFrameJuliaQueryFamily F L M
  let u := (principalFrameColumnMatrix F L).mulVec (Pi.single r (1 : ℝ))
  have hColumn : principalFrameObservedQueryVector X r = u := by
    exact principalFrameObservedQueryVector_eq F L M X
      (principalFrameJuliaQueryFamily_eq_model F L M) r
  have hQuery : X r = archiveJuliaRaisingQuery
      u (M r) := by
    simpa [X, u] using principalFrameJuliaQueryFamily_eq_model F L M r
  exact principalFrameObservedQuery_open_chart_link_recovery
    (M r) Pₓ Pᵧ X u α r hQuery hColumn hα hSymm hIso hCovector hBranch

/-- Null-chart specialization of the full Eq. (28) open-chart recovery. A
complete finite-carrier query recovers the selected endpoint map for any
chosen role; nullness sets the square-root branch to its positive value. -/
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
  have hQuery : X r = archiveJuliaRaisingQuery u (M r) := by
    simpa [X, u] using principalFrameJuliaQueryFamily_eq_model F L M r
  have hBlock : archiveJuliaQueryNullBlock (X r) (α r) =
      archiveJuliaNullBlock u (M r) (α r) := by
    rw [hQuery]
    exact archiveJuliaQueryNullBlock_readout u (M r) (α r) hα
  have hObserved : archiveJuliaQueryNullMetricCovector (Pₓ r)
      (principalFrameObservedQueryVector X r) (X r) (α r) =
        (Pₓ r u).comp (archiveJuliaNullBlock u (M r) (α r)) := by
    simp [archiveJuliaQueryNullMetricCovector, hColumn, hBlock]
  have hCovector : archiveJuliaQueryNullMetricCovector (Pₓ r)
      (principalFrameObservedQueryVector X r) (X r) (α r) ≠ 0 := by
    rw [hObserved]
    exact archiveJuliaNullBlock_covector_ne_zero (Pₓ r) u (M r) (α r)
      hNondegenerate hu hNull
  have hBranch : 0 < 1 +
      (Pₓ r (principalFrameObservedQueryVector X r)
        (principalFrameObservedQueryVector X r)) * α r ((M r)
          (archiveJuliaQueryNullCanonicalWitness (Pₓ r)
            (principalFrameObservedQueryVector X r) (X r) (α r))) := by
    rw [hColumn, hNull]
    norm_num
  exact principalFrameJuliaQueryFamily_open_chart_link_recovery
    F L M Pₓ Pᵧ α r hSymm hIso hα hCovector hBranch

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

section JuliaPrincipalFrameCoframeDerivative

local notation "RoleMat" => Matrix Role Role ℝ

local instance : NormedAddCommGroup RoleMat := Matrix.normedAddCommGroup
local instance : NormedSpace ℝ RoleMat := Matrix.normedSpace
local instance : NormedRing RoleMat := Matrix.frobeniusNormedRing
local instance : NormedAlgebra ℝ RoleMat := Matrix.frobeniusNormedAlgebra

/-- The actual Julia query-family inverse-coframe readout is Fréchet
differentiable in every one of the 16 coframe-matrix directions when its
Lorentz link map is held fixed. Its derivative is the right transport by the
inverse link. This is the coframe block only; it does not assert link jets,
smoothness of the joint inverse, or the full `D R D Φ = I` identity. -/
theorem principalFrameJuliaQueryFamily_inverseCoframeReadout_hasFDerivAt
    (F Λ : RoleMat)
    (M : Role → RoleSpace ≃ₗ[ℝ] RoleSpace)
    (hΛ : IsRoleLorentz Λ) :
    HasFDerivAt
      (fun Z : RoleMat => principalFrameInverseCoframeReadout
        (principalFrameObservedQueryColumnMatrix
          (principalFrameJuliaQueryFamily Z Λ.transpose M)))
      ((ContinuousLinearMap.mul ℝ RoleMat).flip ((Λ.transpose)⁻¹)) F := by
  have hLorentz : Λ * roleLorentzMetric * Λ.transpose = roleLorentzMetric := by
    simpa [IsRoleLorentz] using hΛ
  have hreadout :
      (fun Z : RoleMat => principalFrameInverseCoframeReadout
        (principalFrameObservedQueryColumnMatrix
          (principalFrameJuliaQueryFamily Z Λ.transpose M))) =
        fun Z : RoleMat => Z * (Λ.transpose)⁻¹ := by
    funext Z
    rw [principalFrameJuliaQueryFamily_columnMatrix]
    exact principalFrame_inverse_coframe_readout Z Λ.transpose hLorentz
  rw [hreadout]
  exact (((ContinuousLinearMap.mul ℝ RoleMat).flip ((Λ.transpose)⁻¹)).hasFDerivAt
    (x := F))

end JuliaPrincipalFrameCoframeDerivative

end
end D0.Geometry
