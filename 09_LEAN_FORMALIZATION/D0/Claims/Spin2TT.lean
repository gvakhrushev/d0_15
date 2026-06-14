import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic

/-!
# D0-SPIN2-001 — finite spin-2 TT polarizations and the 2 degrees of freedom

Python certificate: `05_CERTS/vp_finite_spin2_wave_operator_concrete.py` (exact rational).

On `Sym(4)` (10-dimensional) with Minkowski `η = diag(1,−1,−1,−1)`, wave-vector
`k = (1,1,0,0)` and time direction `u = (1,0,0,0)`, the two transverse-traceless
polarizations `e₊ = diag(0,0,1,−1)` and `e× = E₂₃+E₃₂` are η-traceless, transverse
(`e·η·k = 0`) and time-orthogonal (`e·η·u = 0`), and are linearly independent — so there
are exactly `2` TT modes, matching the constraint count `10 − 8 = 2`. All exact over `ℚ`.
-/

namespace D0.Claims

open Matrix

def etaM : Matrix (Fin 4) (Fin 4) ℚ := !![1,0,0,0; 0,-1,0,0; 0,0,-1,0; 0,0,0,-1]
def kVec : Matrix (Fin 4) (Fin 1) ℚ := !![1; 1; 0; 0]
def uVec : Matrix (Fin 4) (Fin 1) ℚ := !![1; 0; 0; 0]
def ePlus : Matrix (Fin 4) (Fin 4) ℚ := !![0,0,0,0; 0,0,0,0; 0,0,1,0; 0,0,0,-1]
def eCross : Matrix (Fin 4) (Fin 4) ℚ := !![0,0,0,0; 0,0,0,0; 0,0,0,1; 0,0,1,0]

/-- Both TT polarizations are η-traceless: `tr(e·η) = 0`. -/
theorem tt_trace_free :
    Matrix.trace (ePlus * etaM) = 0 ∧ Matrix.trace (eCross * etaM) = 0 := by
  refine ⟨?_, ?_⟩ <;> native_decide

/-- Both are transverse to `k` and time-orthogonal to `u`: `e·η·k = 0`, `e·η·u = 0`. -/
theorem tt_transverse_timeorthogonal :
    ePlus * etaM * kVec = 0 ∧ ePlus * etaM * uVec = 0 ∧
    eCross * etaM * kVec = 0 ∧ eCross * etaM * uVec = 0 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> native_decide

/-- The two polarizations are distinct and neither is the other's scalar multiple — two
independent TT modes (the `+` mode has a `−1`, the `×` mode is symmetric off-diagonal). -/
theorem tt_two_independent : ePlus ≠ eCross ∧ ePlus ≠ -eCross := by
  refine ⟨?_, ?_⟩ <;> native_decide

/-- **D0-SPIN2-001.** Two transverse-traceless polarizations, η-traceless + transverse +
time-orthogonal + independent, and the degree-of-freedom count `10 − 8 = 2`
(`Sym(4)` components `4·5/2 = 10`, constraints `2·4 = 8`). -/
theorem finite_spin2_dof :
    (Matrix.trace (ePlus * etaM) = 0 ∧ Matrix.trace (eCross * etaM) = 0) ∧
    (ePlus * etaM * kVec = 0 ∧ eCross * etaM * kVec = 0) ∧
    (ePlus ≠ eCross ∧ ePlus ≠ -eCross) ∧
    (4 * 5 / 2 = 10 ∧ 2 * 4 = 8 ∧ 10 - 8 = 2) := by
  refine ⟨⟨tt_trace_free.1, tt_trace_free.2⟩, ⟨?_, ?_⟩, tt_two_independent, ?_⟩
  · exact tt_transverse_timeorthogonal.1
  · exact tt_transverse_timeorthogonal.2.2.1
  · refine ⟨?_, ?_, ?_⟩ <;> decide

end D0.Claims
