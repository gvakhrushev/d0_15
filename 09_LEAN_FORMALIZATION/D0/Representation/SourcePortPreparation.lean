import D0.Integration.V15.RawZone
import D0.Representation.OrderMemoryReadout
import Mathlib.LinearAlgebra.Matrix.Kronecker

/-!
# Source-derived ports and information-preserving preparation

The maximum-degree spectral projector fixes a declared, source-internal frame.
This is NOT a proof that M1 uniquely prefers maximum over minimum degree.
No arbitrary vector is needed: compression to the existing active plane gives
one port; its complement recovers the earlier (0,1,2) direction.

The coupled matrix below is an explicit representation. Its physical availability
is not implied by its membership in a matrix algebra. Likewise preparation by
projection is selective; its complementary branch cannot be silently discarded.
-/

namespace D0.Representation.SourcePortPreparation

open Matrix
open D0.Integration.V15.RawZone (DW comm Gq Pact P0)
open D0.Representation.OrderMemoryReadout (spin)

abbrev M3 := Matrix (Fin 3) (Fin 3) ℚ
abbrev V3 := Fin 3 → ℚ

def D : M3 := DW.map (fun z : ℤ => (z : ℚ))
def K : M3 := comm.map (fun z : ℤ => (z : ℚ))

/-- Spectral projector for degree 24, the largest of the source's 24,22,20. -/
def degreePort : M3 := (1/8 : ℚ) • ((D - 22 • (1 : M3)) * (D - 20 • (1 : M3)))

def compressed : M3 := Pact * degreePort * Pact
def signalPort : M3 := (710/567 : ℚ) • compressed
def inputPort : M3 := Pact - signalPort
def reversal : M3 := 1 - 2 • signalPort

theorem degreePort_from_spectrum : degreePort = !![1,0,0;0,0,0;0,0,0] := by native_decide
theorem compression_normalization : compressed.trace = 567/710 := by native_decide
theorem port_projectors :
    signalPort * signalPort = signalPort ∧ inputPort * inputPort = inputPort ∧
    signalPort * inputPort = 0 ∧ inputPort * signalPort = 0 ∧
    signalPort + inputPort = Pact := by native_decide

theorem port_metric :
    signalPort.transpose * Gq = Gq * signalPort ∧
    inputPort.transpose * Gq = Gq * inputPort := by native_decide

theorem port_ranks : signalPort.trace = 1 ∧ inputPort.trace = 1 := by native_decide

theorem inputPort_explicit :
    inputPort = !![0,0,0;0,11/63,26/63;0,22/63,52/63] := by native_decide

theorem signalPort_explicit : signalPort =
    !![567/710,143/355,-143/710;
       117/355,3718/22365,-1859/22365;
       -99/710,-1573/22365,1573/44730] := by native_decide

/-- The previously used vector q is recovered as a port direction. -/
def q : V3 := ![0,1,2]
def r : V3 := K.mulVec q
def frame : Matrix (Fin 3) (Fin 2) ℚ := !![0,126;1,52;2,-22]

theorem inputPort_recovers_q (v : V3) :
    inputPort.mulVec v = ((11*v 1 + 26*v 2)/63) • q := by
  rw [inputPort_explicit]
  ext i
  fin_cases i <;> simp [Matrix.mulVec, dotProduct, Fin.sum_univ_succ, q] <;> ring

theorem frame_from_source :
    r = ![126,52,-22] ∧ inputPort.mulVec q = q ∧ signalPort.mulVec q = 0 ∧
    inputPort.mulVec r = 0 ∧ signalPort.mulVec r = r := by native_decide

theorem frame_metric : frame.transpose * Gq * frame = !![63,0;0,178920] := by
  native_decide

theorem reversal_involution : reversal * reversal = 1 := by native_decide
theorem reversal_metric : reversal.transpose * Gq * reversal = Gq := by native_decide
theorem reversal_reverses_generator : reversal * K * reversal = -K := by native_decide
theorem reversal_preserves_neutral : reversal * P0 = P0 ∧ P0 * reversal = P0 := by
  native_decide

/-! Actual local operator on scene x Q8 coordinates, rather than a named port bit. -/
abbrev M12 := Matrix (Fin 3 × Fin 4) (Fin 3 × Fin 4) ℚ
def coupled : M12 :=
  Matrix.kronecker (1 - signalPort) (1 : Matrix (Fin 4) (Fin 4) ℚ) +
  Matrix.kronecker signalPort (spin 2)
def jointMetric : M12 := Matrix.kronecker Gq (1 : Matrix (Fin 4) (Fin 4) ℚ)

/-- Symmetric source projector times skew memory generator: a valid metric-skew
interaction, unlike a tensor of two skew operators. Its availability is a bridge. -/
def interactionGenerator : M12 := Matrix.kronecker signalPort (spin 2)

theorem interaction_generator_skew :
    interactionGenerator.transpose * jointMetric = -(jointMetric * interactionGenerator) := by
  simp only [interactionGenerator, signalPort_explicit]
  native_decide

theorem interaction_generator_square :
    interactionGenerator * interactionGenerator =
      -Matrix.kronecker signalPort (1 : Matrix (Fin 4) (Fin 4) ℚ) := by
  simp only [interactionGenerator, signalPort_explicit]
  native_decide

/-- Exact quarter-turn polynomial. No fitted interaction strength enters this
dimensionless algebraic construction; no physical time calibration is asserted. -/
theorem local_gate_from_generator :
    coupled = 1 + interactionGenerator + interactionGenerator * interactionGenerator := by
  rw [interaction_generator_square]
  simp only [coupled, interactionGenerator, signalPort_explicit]
  native_decide

theorem coupled_preserves_metric : coupled.transpose * jointMetric * coupled = jointMetric := by
  simp only [coupled, signalPort_explicit]
  native_decide
theorem coupled_square :
    coupled * coupled = Matrix.kronecker reversal (1 : Matrix (Fin 4) (Fin 4) ℚ) := by
  simp only [coupled, reversal, signalPort_explicit]
  native_decide
theorem coupled_fourth : coupled ^ 4 = 1 := by
  have hs := coupled_square
  calc coupled ^ 4 = (coupled * coupled) * (coupled * coupled) := by noncomm_ring
       _ = Matrix.kronecker (reversal * reversal)
         ((1 : Matrix (Fin 4) (Fin 4) ℚ) * 1) := by
           rw [hs]
           exact (Matrix.mul_kronecker_mul reversal reversal
             (1 : Matrix (Fin 4) (Fin 4) ℚ) 1).symm
       _ = 1 := by rw [reversal_involution]; simp

/-- A two-by-two minor of the operator realignment; nonzero detects interaction. -/
def interactionMinor (M : M12) : ℚ :=
  M (0,0) (0,0) * M (1,0) (1,1) - M (0,0) (0,1) * M (1,0) (1,0)

theorem coupled_interaction_witness : interactionMinor coupled = 5657/8946 := by
  simp only [interactionMinor, coupled, signalPort_explicit]
  native_decide

theorem independent_actions_zero_minor (A : M3) (B : Matrix (Fin 4) (Fin 4) ℚ) :
    interactionMinor (Matrix.kronecker A B) = 0 := by
  simp [interactionMinor, Matrix.kronecker, Matrix.kroneckerMap]
  ring

/-- Even arbitrary independent scene/memory operators cannot implement this gate. -/
theorem coupled_not_independent (A : M3) (B : Matrix (Fin 4) (Fin 4) ℚ) :
    coupled ≠ Matrix.kronecker A B := by
  intro h
  have hz := independent_actions_zero_minor A B
  rw [← h, coupled_interaction_witness] at hz
  norm_num at hz

/-! Preparation keeps both the selected and complementary response. -/
theorem preparation_conservation :
    inputPort.transpose * Gq * inputPort +
      (1-inputPort).transpose * Gq * (1-inputPort) = Gq := by native_decide

theorem prepare_is_not_injective : ¬ Function.Injective inputPort.mulVec := by
  intro h
  have he : inputPort.mulVec ![1,0,0] = inputPort.mulVec 0 := by native_decide
  have hh := congrArg (fun v : V3 => v 0) (h he)
  norm_num at hh

/-- Keeping both branches permits exact recovery of every input. -/
theorem prepare_with_archive_recovers (v : V3) :
    inputPort.mulVec v + (1-inputPort).mulVec v = v := by
  rw [← Matrix.add_mulVec]
  simp

end D0.Representation.SourcePortPreparation
