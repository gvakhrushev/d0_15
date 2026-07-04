import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# Finite spectral-action Einstein-tensor response (`D0-SPECTRAL-EINSTEIN-001`)

The rank-2 variational response of the quadratic spectral action `S(L) = Tr(L^2)` (the `a2` / EH proxy at
flat measure) is `G = dS/dh = 2 L`. This file proves the two structural properties the ledger flagged as
missing — that `G` is simultaneously **symmetric** and **divergence-free** — for an arbitrary graph
Laplacian, on the single `Matrix N N ℝ` carrier (no `Fin 4` spin-2 carrier is needed for the existence of
`G`; the two-polarization TT linkage is the separate `D0-HODGE-LINKS-001`).

* `archiveDivergence A i = ∑ j, A i j` (the corpus's discrete divergence, row sums).
* A **graph Laplacian** `L` is symmetric with vanishing row sums (`L` annihilates the constant vector).
* Hence `G = 2 • L` is symmetric (`einstein_response_symmetric`) and divergence-free
  (`einstein_response_divergence_free`) — the discrete contracted-Bianchi conservation of the variational
  response.

The mis-scoped conservation NO-GO only exhibited *some* symmetric matrix with nonzero divergence; it never
blocked the canonical response `2L`. Conservation is FORCED by the Laplacian structure, not automatic.
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

/-- The finite Einstein-tensor response of `S(L) = Tr(L^2)` is `G = 2 • L`. -/
def einsteinResponse (L : Matrix N N ℝ) : Matrix N N ℝ := (2 : ℝ) • L

/-- `G = 2 • L` is symmetric whenever `L` is. -/
theorem einstein_response_symmetric (L : Matrix N N ℝ) (hL : IsGraphLaplacian L) :
    (einsteinResponse L).transpose = einsteinResponse L := by
  unfold einsteinResponse
  rw [Matrix.transpose_smul, hL.symm]

/-- `G = 2 • L` is divergence-free (`archiveDivergence G = 0`) whenever `L` is a graph Laplacian. -/
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

/-- Both structural properties at once: the variational response exists, is symmetric AND
divergence-free — the object the ledger flagged as missing. -/
theorem einstein_response_symmetric_and_conserved (L : Matrix N N ℝ) (hL : IsGraphLaplacian L) :
    (einsteinResponse L).transpose = einsteinResponse L ∧
      archiveDivergence (einsteinResponse L) = 0 :=
  ⟨einstein_response_symmetric L hL, einstein_response_divergence_free L hL⟩

end D0.VNext2.SpectralEinsteinResponse
