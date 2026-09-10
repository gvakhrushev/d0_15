import D0.Cosmology.SelfUnfoldingObservableRelations
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic

/-!
# Conditional redshift-drift / expansion / archive-response coupling

This bridge records the consequence of combining two explicit physical assumptions with the
already-owned internal archive relation:

1. constant-rate interpolation `dot z = rho * log(phi) * (1+z)`;
2. the standard FLRW redshift-drift identity `dot z = (1+z) H0 - H(z)`.

Eliminating the drift gives `H(z)/(1+z) = H0-rho*log(phi)`.  Therefore radial BAO must have the
one-normalisation shape `D_H/r_d = C/(1+z)`.  If the internal dynamic archive share is additionally
represented by a measured dark response, the same elimination gives
`D_H/r_d = C * (1-darkResponse)`.

Neither FLRW nor the measured-dark-response representation is promoted to CORE here.  The module
also proves the sharp reopening condition: a nonconstant observed `H(z)/(1+z)` forces a nonconstant
rate function.  Such a function is additional outcome-affecting information, not a new value of the
same scalar `rho`.
-/

namespace D0.Bridge.RedshiftExpansionArchiveCoupling

open D0

/-- Continuous constant-rate interpolation of the one-tick D0 comparison law. -/
noncomputable def constantRateDrift (rho z : ℝ) : ℝ :=
  rho * Real.log phi * (1 + z)

/-- Standard FLRW redshift-drift expression, retained as an explicit bridge term. -/
def flrwDrift (H0 : ℝ) (H : ℝ → ℝ) (z : ℝ) : ℝ :=
  (1 + z) * H0 - H z

end D0.Bridge.RedshiftExpansionArchiveCoupling

namespace D0.Bridge.BridgeAssumption

open D0.Bridge.RedshiftExpansionArchiveCoupling

/-- A physical application must supply equality of the two independently defined drift readouts. -/
structure ConstantRateFLRWRepresentation where
  rho : ℝ
  H0 : ℝ
  H : ℝ → ℝ
  sameDrift : ∀ z, constantRateDrift rho z = flrwDrift H0 H z

end D0.Bridge.BridgeAssumption

namespace D0.Bridge.RedshiftExpansionArchiveCoupling

open D0
open D0.Bridge.BridgeAssumption

/-- Eliminating redshift drift fixes the complete expansion shape up to one constant. -/
theorem expansion_shape_after_eliminating_drift
    (R : ConstantRateFLRWRepresentation) (z : ℝ) :
    R.H z = (1 + z) * (R.H0 - R.rho * Real.log phi) := by
  have h := R.sameDrift z
  unfold constantRateDrift flrwDrift at h
  linarith

/-- The normalized expansion rate is constant at all physical redshifts `z ≠ -1`. -/
theorem normalized_expansion_constant
    (R : ConstantRateFLRWRepresentation) (z : ℝ) (hz : 1 + z ≠ 0) :
    R.H z / (1 + z) = R.H0 - R.rho * Real.log phi := by
  rw [expansion_shape_after_eliminating_drift]
  field_simp [hz]

/-- Radial-BAO shape after the nuisance normalization `C=c/[r_d(H0-rho log phi)]` is collected. -/
noncomputable def radialBAOShape (C z : ℝ) : ℝ :=
  C / (1 + z)

/-- Continuum candidate obtained from the internally proved relation
`dynamicArchiveShare = zD0/(1+zD0)`.  Calling it a measured dark fraction requires a separate
representation below. -/
noncomputable def archiveResponseCandidate (z : ℝ) : ℝ :=
  z / (1 + z)

/-- The radial expansion observable and the archive candidate have no independent shape knob. -/
theorem radial_bao_archive_candidate_coupling
    (C z : ℝ) (hz : 1 + z ≠ 0) :
    radialBAOShape C z = C * (1 - archiveResponseCandidate z) := by
  unfold radialBAOShape archiveResponseCandidate
  field_simp [hz]
  ring

end D0.Bridge.RedshiftExpansionArchiveCoupling

namespace D0.Bridge.BridgeAssumption

open D0.Bridge.RedshiftExpansionArchiveCoupling

/-- External application datum: a concrete independently measured response must represent the
archive candidate.  No global inhabitant is asserted. -/
structure MeasuredDarkResponseRepresentation where
  response : ℝ → ℝ
  representsArchive : ∀ z, response z = archiveResponseCandidate z

end D0.Bridge.BridgeAssumption

namespace D0.Bridge.RedshiftExpansionArchiveCoupling

open D0.Bridge.BridgeAssumption

/-- Conditional three-way observable relation after eliminating the shared refinement variable. -/
theorem represented_dark_response_coupling
    (D : MeasuredDarkResponseRepresentation) (C z : ℝ) (hz : 1 + z ≠ 0) :
    radialBAOShape C z = C * (1 - D.response z) := by
  rw [D.representsArchive]
  exact radial_bao_archive_candidate_coupling C z hz

/-- Variable-rate rescue of the same FLRW bridge. -/
structure VariableRateFLRWRepresentation where
  rho : ℝ → ℝ
  H0 : ℝ
  H : ℝ → ℝ
  shape : ∀ z, H z = (1 + z) * (H0 - rho z * Real.log phi)

/-- **Structural reopening theorem.** If two normalized expansion measurements differ, the rate
function must carry different values at those redshifts.  A single scalar `rho` cannot absorb the
failure. -/
theorem unequal_normalized_expansion_forces_rate_variation
    (R : VariableRateFLRWRepresentation) (z1 z2 : ℝ)
    (hz1 : 1 + z1 ≠ 0) (hz2 : 1 + z2 ≠ 0)
    (hne : R.H z1 / (1 + z1) ≠ R.H z2 / (1 + z2)) :
    R.rho z1 ≠ R.rho z2 := by
  intro hrho
  apply hne
  rw [R.shape z1, R.shape z2]
  field_simp [hz1, hz2]
  rw [hrho]
  ring

/-- Capstone of the conditional bridge and its exact variable-rate reopening condition. -/
theorem redshift_expansion_archive_coupling
    (R : ConstantRateFLRWRepresentation)
    (D : MeasuredDarkResponseRepresentation) :
    (∀ z : ℝ, 1 + z ≠ 0 →
      R.H z / (1 + z) = R.H0 - R.rho * Real.log phi) ∧
    (∀ C z : ℝ, 1 + z ≠ 0 →
      radialBAOShape C z = C * (1 - D.response z)) :=
  ⟨normalized_expansion_constant R,
    fun C z hz => represented_dark_response_coupling D C z hz⟩

end D0.Bridge.RedshiftExpansionArchiveCoupling
