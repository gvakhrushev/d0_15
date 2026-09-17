import D0.Cosmology.CoreShapePassportBoundary
import Mathlib.Data.List.Basic

namespace D0.Cosmology

/--
The finite cosmology object that belongs to the D0 core: core parameters,
a finite archive/runtime window, and the internal entropy/S_DE transfer shape.
It deliberately contains no survey covariance, Hubble prior, BAO table, or
external likelihood value.
-/
structure InternalArchiveCosmologyObject where
  core : CoreParams
  finiteWindow : Fin 3 → ℝ
  entropyTransferShape : Fin 3 → ℝ

/-- The internal shape evaluation ignores empirical comparison parameters. -/
noncomputable def internalArchiveShapeEvaluated
    (O : InternalArchiveCosmologyObject) (_ep : EmpiricalParams) : Fin 3 → ℝ :=
  O.entropyTransferShape

/-- Core cosmology shape is invariant under changing survey/likelihood parameters. -/
theorem internal_archive_shape_independent_of_empirical_parameters
    (O : InternalArchiveCosmologyObject) (ep₁ ep₂ : EmpiricalParams) :
    internalArchiveShapeEvaluated O ep₁ = internalArchiveShapeEvaluated O ep₂ := by
  rfl

/--
A survey likelihood passport is downstream of the frozen internal object.  It may
record empirical parameters, external data and a likelihood value, but it must
compute that value from the frozen internal shape rather than mutating it.
-/
structure SurveyLikelihoodPassport where
  internalObject : InternalArchiveCosmologyObject
  empiricalParams : EmpiricalParams
  externalData : ExternalData
  reportedLikelihood : ℝ
  likelihoodIsExternal :
    reportedLikelihood =
      ExternalLikelihood
        (AmplitudeNormalization
          (RedshiftCalibration internalObject.entropyTransferShape empiricalParams)
          empiricalParams)
        externalData

/-- The internal shape carried by a passport is just the shape of its frozen object. -/
noncomputable def surveyPassportInternalShape (P : SurveyLikelihoodPassport) : Fin 3 → ℝ :=
  P.internalObject.entropyTransferShape

/-- A passport can compare a frozen internal shape; it cannot replace that shape. -/
theorem survey_passport_preserves_internal_archive_shape (P : SurveyLikelihoodPassport) :
    surveyPassportInternalShape P = P.internalObject.entropyTransferShape := by
  rfl

/-- The data-manifest layer is the minimal reproducibility witness for survey comparison. -/
def ExternalSurveyManifestComplete (manifest : List String) : Prop :=
  manifest ≠ []

/-- A survey comparison is advertised as reproducible only when the manifest is complete. -/
def SurveyComparisonReproducible (manifest : List String) : Prop :=
  ExternalSurveyManifestComplete manifest

/-- Without a manifest/data bundle, an empirical survey comparison is not reproducible. -/
theorem survey_comparison_requires_nonempty_manifest :
    ¬ SurveyComparisonReproducible [] := by
  unfold SurveyComparisonReproducible ExternalSurveyManifestComplete
  simp

/-- Survey likelihood passports do not promote to D0 core cosmology closure. -/
def CanPromoteSurveyPassportToCore (_P : SurveyLikelihoodPassport) : Prop :=
  False

/-- A survey likelihood can falsify a transfer, but it cannot become the core theorem. -/
theorem survey_likelihood_cannot_promote_to_core_cosmology
    (P : SurveyLikelihoodPassport) :
    ¬ CanPromoteSurveyPassportToCore P := by
  intro h
  exact h

/--
A compact witness object for the v14 cosmology split: a frozen archive cosmology
object plus the theorem that its internal shape is independent of empirical
comparison parameters.
-/
structure FrozenArchiveCosmology where
  object : InternalArchiveCosmologyObject
  shapeIndependent : ∀ ep₁ ep₂ : EmpiricalParams,
    internalArchiveShapeEvaluated object ep₁ = internalArchiveShapeEvaluated object ep₂

/-- Build a frozen archive-cosmology object from finite D0 data. -/
noncomputable def frozenArchiveCosmology
    (cp : CoreParams) (window transfer : Fin 3 → ℝ) : FrozenArchiveCosmology where
  object := { core := cp, finiteWindow := window, entropyTransferShape := transfer }
  shapeIndependent := by
    intro ep₁ ep₂
    exact internal_archive_shape_independent_of_empirical_parameters _ ep₁ ep₂

/-- The frozen cosmology object is core-shaped before any survey likelihood is read. -/
theorem frozen_archive_cosmology_core_shape_closed (F : FrozenArchiveCosmology)
    (ep₁ ep₂ : EmpiricalParams) :
    internalArchiveShapeEvaluated F.object ep₁ = internalArchiveShapeEvaluated F.object ep₂ :=
  F.shapeIndependent ep₁ ep₂

end D0.Cosmology
