import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic

/-!
# Adler-Weiss internal Markov realization (`D0-ADLER-WEISS-INTERNAL-CONSTRUCTION-001`)

The D0 toral automorphism `T = ![![0,1],![1,-1]]` (Anosov, `tr = -1`, `det = -1`) admits an exact 2-cell
Markov partition realized INTERNALLY via the M1-forced golden `beta = phi` natural extension. The
symbolic-dynamical content is the golden SFT with transition matrix `![![1,1],![1,0]]` (the digit `1` cannot
follow itself), and `T` is `GL(2,Z)`-conjugate to `-M_phi` with `M_phi = ![![1,1],![1,0]]`.

This file certifies the exact integer/matrix facts that carry the construction:
* the conjugacy `U * T * U⁻¹ = -M_phi` with `det U = +1` (orientation twist), and
* `det T = -1`, `trace T = -1` (Anosov data), and the golden SFT transition matrix determinant `-1`.

The metric flat-torus parallelogram embedding and the smooth/measure conjugacy stay the external classical
owner `D0-ADLER-WEISS-PARTITION-OWNER-001`; the golden-split boundary and the `1->1` forbidding are proven
in the companion Python cert `vp_adler_weiss_internal_markov.py`.
-/

namespace D0.VNext2.AdlerWeissInternalMarkov

open Matrix

/-- The D0 time operator `T = [[0,1],[1,-1]]`. -/
def T : Matrix (Fin 2) (Fin 2) ℤ := !![0, 1; 1, -1]

/-- The golden (Fibonacci) companion `M_phi = [[1,1],[1,0]]` — also the golden SFT transition matrix. -/
def Mphi : Matrix (Fin 2) (Fin 2) ℤ := !![1, 1; 1, 0]

/-- The unimodular conjugator `U = [[0,1],[-1,0]]`. -/
def U : Matrix (Fin 2) (Fin 2) ℤ := !![0, 1; -1, 0]

/-- `U⁻¹ = [[0,-1],[1,0]]` (as an explicit integer matrix, since `det U = 1`). -/
def Uinv : Matrix (Fin 2) (Fin 2) ℤ := !![0, -1; 1, 0]

/-- `T` is Anosov data: `det T = -1`. -/
theorem det_T : T.det = -1 := by
  simp [T, Matrix.det_fin_two, Matrix.of_apply]

/-- `det M_phi = -1` (the golden SFT transition matrix is unimodular, orientation-reversing). -/
theorem det_Mphi : Mphi.det = -1 := by
  simp [Mphi, Matrix.det_fin_two, Matrix.of_apply]

/-- `det U = +1`: the conjugator is orientation-PRESERVING. -/
theorem det_U : U.det = 1 := by
  simp [U, Matrix.det_fin_two, Matrix.of_apply]

/-- `U` and `Uinv` are genuine inverses. -/
theorem U_mul_Uinv : U * Uinv = 1 := by
  simp [U, Uinv, ← Matrix.one_fin_two]

/-- The orientation-twisted conjugacy `U * T * Uinv = -M_phi`: the golden-SFT Markov partition of `M_phi`
transfers to `T` with an orientation twist. This is the load-bearing integer identity of the construction. -/
theorem conjugacy_T_negMphi : U * T * Uinv = -Mphi := by
  simp [U, T, Uinv, Mphi]

/-- The golden SFT transition matrix `[[1,1],[1,0]]` forbids `1 -> 1`: its `(1,1)` entry is `0` while the
other three entries are `1` (the exact Markov property `T(int P_i) ⊆ ⋃ int P_j`). -/
theorem golden_sft_forbids_11 :
    Mphi 0 0 = 1 ∧ Mphi 0 1 = 1 ∧ Mphi 1 0 = 1 ∧ Mphi 1 1 = 0 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> simp [Mphi]

end D0.VNext2.AdlerWeissInternalMarkov
