import D0.Representation.CompatibleInvolutionClassification
import D0.Representation.OrientationOperatorTransport
import D0.Representation.OrientationZoneDescentNoGo
import D0.Representation.VerifierSwapGradingNoGo
import D0.Synthesis.IntrinsicDegreeFibreFrame

/-!
# Generation grading present-core maximality

This capstone terminalizes the neutral-current grading lane at the exact
CORE / BRIDGE boundary.

What is machine-owned:

* every rational involution compatible with the intrinsic degree operator
  is one of eight diagonal sign patterns;
* scalar patterns give the scalar branch, while every non-scalar compatible
  involution gives nc = 8;
* direct scene parity is scalar and gives nc = 12;
* the canonical RawZone 2+1 involution fails degree compatibility;
* the verifier line-swap has the desired abstract 2+1 eigensign split but
  also fails degree compatibility;
* the owned pointwise Omega8 orientation is nontrivial upstairs but its
  ordinary descent to the three-zone quotient is the identity, hence nc = 12;
* once a Fourier-sector -> degree-fibre transport is supplied, every transport
  gives an actual compatible non-scalar grading and nc = 8.

Therefore the present core does not leave a search over grading matrices or
sector permutations.  The residual is exactly representation provenance:
a semantic transport saying that terminal Fourier orientation sectors act as
the grading on the intrinsic generation fibres.  This module classifies that
residual; it does not postulate the missing provenance map as CORE.
-/

namespace D0.Representation.GenerationGradingPresentCoreMaximality

open D0.Representation.CompatibleInvolutionClassification
open D0.Representation.OrientationOperatorTransport
open D0.Representation.OrientationZoneDescentNoGo
open D0.Representation.VerifierSwapGradingNoGo
open D0.Synthesis.IntrinsicDegreeFibreFrame
open D0.SelfReading.TypedCapacityRawScene

/-- Exhaustive present-core boundary for the neutral-current grading lane. -/
theorem generation_grading_present_core_maximality :
    (∀ X : CompatibleInvolutionClassification.M3,
      CompatibleInvolution X →
        X = (1 : CompatibleInvolutionClassification.M3) ∨
        X = -(1 : CompatibleInvolutionClassification.M3) ∨
        ncReadout X = 8) ∧
    ncReadout sceneParityGrading = 12 ∧
    (zoneCurrentGrading * intrinsicDegreeOp ≠
      intrinsicDegreeOp * zoneCurrentGrading) ∧
    (¬ CompatibleInvolution verifierSwapMatrix) ∧
    (∀ (τ : Fin 3 → Fin 3),
      (∀ x : TypedVertex,
        typedZone (flipTyped x) = τ (typedZone x)) →
      τ = id) ∧
    ncReadout directZoneOrientation = 12 ∧
    (∀ σ : OrientationTransport,
      CompatibleInvolution (transportedGrading σ) ∧
      NonScalar (transportedGrading σ) ∧
      ncReadout (transportedGrading σ) = 8) := by
  refine ⟨compatible_involution_scalar_or_nc8,
    scene_parity_nc_is_twelve,
    zoneCurrentGrading_not_degree_compatible,
    verifierSwapMatrix_not_compatible,
    induced_zone_action_eq_id,
    direct_zone_orientation_nc_twelve,
    ?_⟩
  intro σ
  exact ⟨transportedGrading_compatible σ,
    transportedGrading_nonscalar σ,
    transportedGrading_nc_eight σ⟩

end D0.Representation.GenerationGradingPresentCoreMaximality
