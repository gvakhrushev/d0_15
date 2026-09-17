import Mathlib.Data.Rat.Lemmas
import D0.Dynamics.ToralAutomorphism

namespace D0.Dynamics

/--
Book-facing record for active/archive branch accounting.  The formal core below
uses the integer matrix trace rather than analytic square roots.
-/
structure BranchPairTrace where
  activeContribution : Rat
  archiveContribution : Rat
  totalTrace : Int

/-- Full active/archive trace of the integer D0 time-transition matrix. -/
def ActiveArchiveTrace (n : Nat) : Int :=
  Matrix.trace (T ^ n)

theorem integer_trace_requires_full_time_matrix (n : Nat) :
    exists z : Int, z = Matrix.trace (T ^ n) := by
  exact Exists.intro (Matrix.trace (T ^ n)) rfl

theorem d0_integer_trace_layers :
    ActiveArchiveTrace 2 = 3 /\
    ActiveArchiveTrace 3 = -4 /\
    ActiveArchiveTrace 5 = -11 := by
  exact trace_evolution_unfolds_d0_geometry

/-- Generation-carrier trace layer. -/
def generationTrace : Int := ActiveArchiveTrace 2

/-- ABCD-capacity trace layer. -/
def abcdTrace : Int := -ActiveArchiveTrace 3

/-- Memory-torus trace layer. -/
def memoryTorusTrace : Int := -ActiveArchiveTrace 5

theorem generationTrace_eq_three :
    generationTrace = 3 := by
  native_decide

theorem abcdTrace_eq_four :
    abcdTrace = 4 := by
  native_decide

theorem memoryTorusTrace_eq_eleven :
    memoryTorusTrace = 11 := by
  native_decide

/-- Closure package for the integer Galois-pair balance layer. -/
structure GaloisConjugateBalanceClosure where
  integer_trace_layers :
    ActiveArchiveTrace 2 = 3 /\
    ActiveArchiveTrace 3 = -4 /\
    ActiveArchiveTrace 5 = -11
  generation_layer : generationTrace = 3
  abcd_layer : abcdTrace = 4
  memory_torus_layer : memoryTorusTrace = 11
  determinant_balance :
    forall n : Nat, Matrix.det (T ^ n) * Matrix.det (T ^ n) = 1

def galoisConjugateBalanceClosure :
    GaloisConjugateBalanceClosure where
  integer_trace_layers := d0_integer_trace_layers
  generation_layer := generationTrace_eq_three
  abcd_layer := abcdTrace_eq_four
  memory_torus_layer := memoryTorusTrace_eq_eleven
  determinant_balance := toral_volume_conservation_square

end D0.Dynamics
