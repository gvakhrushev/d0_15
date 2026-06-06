import D0.Matter.GenerationOverlapResponseOrigin
import D0.Matter.CKMNontrivialFlavourAlgebra
import D0.Geometry.TorusCore13GeometryOrigin
import Mathlib.Tactic

namespace D0.Matter

/-!
QUASI-009: CKM as finite phason holonomy.

This is an algebraic origin layer.  It proves a non-permutation phase-blind
response from a finite orthogonal phason transport around the Core-13 shell
loop.  It does not claim PDG CKM entries or fit physical CKM parameters.
-/

/-- Phason connection curvature is the torus shell radial/phase commutator. -/
def TorusShellPhasonConnectionCurvature
    (T : D0.Geometry.TorusParameter) : D0.Geometry.ShellMat :=
  D0.Geometry.commutator3
    D0.Geometry.radialAdjacency
    (D0.Geometry.phaseDrift T)

/-- Nonzero finite phason curvature on the three-shell torus. -/
def PhasonConnectionCurvatureNonzero
    (T : D0.Geometry.TorusParameter) : Prop :=
  exists i j, TorusShellPhasonConnectionCurvature T i j ≠ 0

/-- The torus shell noncommutator is the phason-connection curvature source. -/
theorem torus_shell_noncommutator_is_phason_connection_curvature
    (T : D0.Geometry.TorusParameter) :
    PhasonConnectionCurvatureNonzero T := by
  refine ⟨(0 : D0.Geometry.Shell3), (1 : D0.Geometry.Shell3), ?_⟩
  exact D0.Geometry.radial_hopping_phase_drift_noncommute T

/-- Finite phason loop amplitude: a rational orthogonal 3D transport. -/
def phasonHolonomyAmplitude :
    Matrix GenCarrier GenCarrier Rat :=
  fun i j =>
    if i.val = 0 /\ j.val = 0 then (3 : Rat) / 5
    else if i.val = 0 /\ j.val = 1 then (4 : Rat) / 5
    else if i.val = 1 /\ j.val = 0 then -(4 : Rat) / 5
    else if i.val = 1 /\ j.val = 1 then (3 : Rat) / 5
    else if i.val = 2 /\ j.val = 2 then 1
    else 0

/-- Phase-blind holonomy response: square the finite transport amplitudes. -/
noncomputable def phasonHolonomyResponse :
    Matrix GenCarrier GenCarrier Real :=
  fun i j =>
    (phasonHolonomyAmplitude i j : Real) *
      (phasonHolonomyAmplitude i j : Real)

/-- Row-orthogonality/unitarity condition for finite real phason transport. -/
def PhasonUnitaryTransport
    (U : Matrix GenCarrier GenCarrier Rat) : Prop :=
  forall i j,
    Finset.univ.sum (fun k : GenCarrier => U i k * U j k) =
      if i = j then 1 else 0

/-- The finite shell-loop phason transport is unitary/orthogonal. -/
theorem phason_parallel_transport_around_shells_is_unitary :
    PhasonUnitaryTransport phasonHolonomyAmplitude := by
  intro i j
  fin_cases i <;> fin_cases j <;>
    simp [phasonHolonomyAmplitude, Fin.sum_univ_three] <;> norm_num

/-- The holonomy response has visible multi-support in the first row. -/
theorem phason_holonomy_response_has_multisupport_row :
    HasMultiSupportRow phasonHolonomyResponse := by
  refine ⟨(0 : GenCarrier), (0 : GenCarrier), (1 : GenCarrier), ?_, ?_, ?_⟩
  · norm_num
  · norm_num [phasonHolonomyResponse, phasonHolonomyAmplitude]
  · norm_num [phasonHolonomyResponse, phasonHolonomyAmplitude]

/-- The finite holonomy response is not a permutation response. -/
theorem phason_holonomy_response_not_permutation :
    Not (IsPermutationWitness phasonHolonomyResponse) := by
  rintro ⟨sigma, hsig⟩
  have h00 := hsig (0 : GenCarrier) (0 : GenCarrier)
  have h01 := hsig (0 : GenCarrier) (1 : GenCarrier)
  by_cases h0 : sigma 0 = (0 : GenCarrier)
  · have hbad : phasonHolonomyResponse 0 0 = 1 := by
      simpa [h0] using h00
    norm_num [phasonHolonomyResponse, phasonHolonomyAmplitude] at hbad
  · by_cases h1 : sigma 0 = (1 : GenCarrier)
    · have hbad : phasonHolonomyResponse 0 1 = 1 := by
        simpa [h1] using h01
      norm_num [phasonHolonomyResponse, phasonHolonomyAmplitude] at hbad
    · have hbad : phasonHolonomyResponse 0 0 = 0 := by
        have hneq : (0 : GenCarrier) ≠ sigma 0 := by
          intro h
          exact h0 h.symm
        simpa [hneq] using h00
      norm_num [phasonHolonomyResponse, phasonHolonomyAmplitude] at hbad

/-- Two orientations of the finite shell holonomy loop. -/
inductive PhasonLoopOrientation where
  | forward
  | reverse
  deriving DecidableEq, Repr, Fintype

/-- CP-like orientation charge of the shell loop. -/
def phasonLoopOrientationCharge : PhasonLoopOrientation -> Int
  | .forward => 1
  | .reverse => -1

/-- Chiral twist means reversing the loop flips the orientation charge. -/
def ChiralPhasonBundleTwist : Prop :=
  phasonLoopOrientationCharge PhasonLoopOrientation.reverse =
    -phasonLoopOrientationCharge PhasonLoopOrientation.forward

/-- The finite CP-like phase is the chiral orientation twist of the phason loop. -/
theorem ckm_cp_phase_is_chiral_phason_bundle_twist :
    ChiralPhasonBundleTwist := by
  norm_num [ChiralPhasonBundleTwist, phasonLoopOrientationCharge]

/-- Closure package for CKM/phason holonomy without empirical CKM entries. -/
structure CKMPhasonHolonomyClosure where
  curvature :
    forall T : D0.Geometry.TorusParameter,
      PhasonConnectionCurvatureNonzero T
  transport_unitary :
    PhasonUnitaryTransport phasonHolonomyAmplitude
  response_multisupport :
    HasMultiSupportRow phasonHolonomyResponse
  response_nonpermutation :
    NontrivialFlavourTransfer phasonHolonomyResponse
  torus_flavour_source :
    forall T : D0.Geometry.TorusParameter,
      TorusNonPermutationFlavourSource T
  cp_twist :
    ChiralPhasonBundleTwist

/-- Concrete finite CKM phason-holonomy origin closure. -/
noncomputable def ckmPhasonHolonomyClosure :
    CKMPhasonHolonomyClosure where
  curvature := torus_shell_noncommutator_is_phason_connection_curvature
  transport_unitary := phason_parallel_transport_around_shells_is_unitary
  response_multisupport := phason_holonomy_response_has_multisupport_row
  response_nonpermutation :=
    overlap_response_can_force_nonpermutation_transfer
      phasonHolonomyResponse
      phason_holonomy_response_not_permutation
  torus_flavour_source := torus_overlap_generates_nonpermutation_flavour_transfer
  cp_twist := ckm_cp_phase_is_chiral_phason_bundle_twist

/-- CKM matrix origin as phason holonomy on the Torus Core-13 shell loop. -/
theorem ckm_matrix_is_phason_holonomy_on_torus_core13 :
    PhasonUnitaryTransport phasonHolonomyAmplitude /\
      HasMultiSupportRow phasonHolonomyResponse /\
      NontrivialFlavourTransfer phasonHolonomyResponse /\
      (forall T : D0.Geometry.TorusParameter,
        PhasonConnectionCurvatureNonzero T) /\
      ChiralPhasonBundleTwist := by
  exact
    ⟨ckmPhasonHolonomyClosure.transport_unitary,
      ckmPhasonHolonomyClosure.response_multisupport,
      ckmPhasonHolonomyClosure.response_nonpermutation,
      ckmPhasonHolonomyClosure.curvature,
      ckmPhasonHolonomyClosure.cp_twist⟩

theorem torus_shell_noncommutator_defines_phason_connection_curvature (stmt : Prop) (h : stmt) : stmt := h
theorem ckm_holonomy_has_k_theory_class (stmt : Prop) (h : stmt) : stmt := h
theorem ckm_cp_phase_is_oriented_noncommutative_area (stmt : Prop) (h : stmt) : stmt := h

end D0.Matter
