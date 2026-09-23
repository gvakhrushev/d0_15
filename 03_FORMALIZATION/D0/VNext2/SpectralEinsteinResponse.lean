import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Legacy doubled graph-Laplacian response (`D0-SPECTRAL-EINSTEIN-001`)

This module proves a true but narrowly scoped linear-algebra statement.

For the quadratic matrix functional `S(L)=Tr(L^2)`, the gradient with respect to the
**matrix variable L** is `2L`. If `L` is a graph Laplacian, then `2L` is symmetric and
has zero row sums because `L` annihilates constants.

The historical API name `einsteinResponse` is retained for compatibility, but C1/A1 truth
repair fixes the interpretation:

* this theorem does **not** identify `2L` with the rank-2 variational response
  `dS_A2/dh` of the A1 edge action;
* `archiveDivergence` here is simply matrix row sum;
* row-sum zero of a graph Laplacian is not, by itself, the signed-current/Hodge divergence
  `B_-` and must not be called a discrete contracted Bianchi identity;
* no TT, diffeomorphism, or Einstein-tensor content follows from this module alone.

The load-bearing statements owned here are exactly:
`einsteinResponse L = 2 • L`, symmetry under a symmetric Laplacian hypothesis, and zero
row sums under the graph-Laplacian hypothesis.
-/

namespace D0.VNext2.SpectralEinsteinResponse

open Matrix BigOperators

variable {N : Type*} [Fintype N] [DecidableEq N]

/-- The corpus's discrete divergence: the row sums of a matrix. -/
def archiveDivergence (A : Matrix N N ℝ) : N → ℝ := fun i => ∑ j, A i j

/-- A graph-Laplacian predicate: symmetric with vanishing row sums (annihilates constants). -/
structure IsGraphLaplacian (L : Matrix N N ℝ) : Prop where
  symm : L.transpose = L
  rowsum_zero : ∀ i, ∑ j, L i j = 0

/-- Legacy-named doubled graph-Laplacian map. For `S(L)=Tr(L^2)`, `2L` is the matrix gradient with respect to `L`; no Einstein-tensor identification is asserted here. -/
def einsteinResponse (L : Matrix N N ℝ) : Matrix N N ℝ := (2 : ℝ) • L

/-- `G = 2 • L` is symmetric whenever `L` is. -/
theorem einstein_response_symmetric (L : Matrix N N ℝ) (hL : IsGraphLaplacian L) :
    (einsteinResponse L).transpose = einsteinResponse L := by
  unfold einsteinResponse
  rw [Matrix.transpose_smul, hL.symm]

/-- `G = 2 • L` has zero matrix row sums (`archiveDivergence G = 0`) whenever `L` is a graph Laplacian. -/
theorem einstein_response_divergence_free (L : Matrix N N ℝ) (hL : IsGraphLaplacian L) :
    archiveDivergence (einsteinResponse L) = 0 := by
  funext i
  unfold archiveDivergence einsteinResponse
  simp only [Matrix.smul_apply, smul_eq_mul, ← Finset.mul_sum, hL.rowsum_zero i, mul_zero]
  rfl

/-- The response is genuinely the doubled Laplacian entrywise. -/
theorem einstein_response_eq (L : Matrix N N ℝ) (i j : N) :
    einsteinResponse L i j = 2 * L i j := by
  simp [einsteinResponse]

/-- Both owned structural properties at once: the doubled Laplacian is symmetric and has zero matrix row sums. -/
theorem einstein_response_symmetric_and_conserved (L : Matrix N N ℝ) (hL : IsGraphLaplacian L) :
    (einsteinResponse L).transpose = einsteinResponse L ∧
      archiveDivergence (einsteinResponse L) = 0 :=
  ⟨einstein_response_symmetric L hL, einstein_response_divergence_free L hL⟩

end D0.VNext2.SpectralEinsteinResponse
