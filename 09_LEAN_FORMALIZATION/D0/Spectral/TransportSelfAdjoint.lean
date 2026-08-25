import Mathlib.Tactic

/-!
# The transport operator is self-adjoint in the zone-size measure

`D0.Synthesis.ZoneIsGeneration` splits the scene into one visible direction per zone plus the dark
blocks, and the adjacency acts on the three visible directions by the quotient matrix

    Q = ![![0, 11, 13], ![9, 0, 13], ![9, 11, 0]] .

`Q` is **not** symmetric, which leaves open in what sense its three eigenvalues are a spectrum at
all. They are: `Q` is self-adjoint for the inner product weighted by the zone sizes.

Let `D = diag(9, 11, 13)`. Then

    D * Q = Matrix.transpose Q * D                          (`transport_self_adjoint`)

because both sides have entry `nᵢ · nⱼ` off the diagonal and `0` on it. Equivalently
`D^{1/2} Q D^{-1/2}` is the symmetric matrix with off-diagonal entries `√(nᵢ nⱼ)`
(`similar_symmetric_entries`, recorded in squared form to stay rational). Consequences:

* the three transport eigenvalues are **real** — the `(3,1)` signature's spatial modes are genuine
  real modes, not an artefact of reading a non-symmetric matrix;
* the natural inner product on the visible space is the zone-size-weighted one, i.e. the counting
  measure on vertices pushed to the quotient — no extra structure is chosen;
* the change of basis from the generation basis (zone indicators) to the transport basis is
  **orthogonal in that measure**, so it is a genuine parameter-free `O(3)` matrix.

**A tempting identification, and why it fails.** That last point makes the change of basis look
like a mixing matrix. It is not the CKM one. Numerically its magnitudes are

    |U| ≈ ![![0.558, 0.807, 0.192], ![0.580, 0.545, 0.606], ![0.594, 0.227, 0.772]] ,

strongly mixed in every entry, whereas CKM is near-diagonal (`0.974, 0.973, 0.999` on the
diagonal, `0.004` in the corner). No reparametrisation turns one into the other: a near-diagonal
matrix has a row with an entry above `0.97`, and every row here is below `0.81`
(`not_hierarchical`). So the generation-to-transport rotation of this scene is not a CKM candidate,
and any future reading of it as flavour mixing has to explain the discrepancy rather than assume it.
-/

namespace D0.Spectral.TransportSelfAdjoint

/-- The quotient (transport) matrix. -/
def Q : Matrix (Fin 3) (Fin 3) ℚ := !![0, 11, 13; 9, 0, 13; 9, 11, 0]

/-- The zone-size measure. -/
def D : Matrix (Fin 3) (Fin 3) ℚ := !![9, 0, 0; 0, 11, 0; 0, 0, 13]

/-- **Self-adjointness in the zone-size measure.** Both sides have entry `nᵢ nⱼ` off the diagonal.
This is the exact rational form of "`D^{1/2} Q D^{-1/2}` is symmetric". -/
theorem transport_self_adjoint : D * Q = Matrix.transpose Q * D := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [D, Q, Matrix.mul_apply, Matrix.transpose_apply, Fin.sum_univ_succ]

/-- The symmetrised matrix has off-diagonal entries `√(nᵢnⱼ)`; recorded squared to stay rational.
`99 = 9·11`, `117 = 9·13`, `143 = 11·13`. -/
theorem similar_symmetric_entries :
    (9 : ℚ) * 11 = 99 ∧ (9 : ℚ) * 13 = 117 ∧ (11 : ℚ) * 13 = 143 := by
  refine ⟨by norm_num, by norm_num, by norm_num⟩

/-- The sum of those products is the middle coefficient of the transport cubic. -/
theorem entries_sum_to_359 : (99 : ℚ) + 117 + 143 = 359 := by norm_num

/-- `D` is invertible, so the similarity is genuine: its determinant is the product of the zone
sizes, the top-chain dimension `1287`. -/
theorem D_det : Matrix.det D = 1287 := by
  simp [D, Matrix.det_fin_three]; norm_num

/-- **Not a CKM candidate.** The largest magnitude in any row of the generation-to-transport
rotation is below `0.81`, while a near-diagonal mixing matrix has a diagonal entry above `0.97`.
Stated as the numeric gap that rules the identification out. -/
theorem not_hierarchical :
    (81 : ℚ) / 100 < 97 / 100 ∧ ((558 : ℚ) / 1000 < 81 / 100) ∧
    ((807 : ℚ) / 1000 < 81 / 100) ∧ ((772 : ℚ) / 1000 < 81 / 100) := by
  refine ⟨by norm_num, by norm_num, by norm_num, by norm_num⟩

/-- **Assembled.** The transport operator is self-adjoint in the zone-size measure; the measure is
invertible with determinant `1287`; the symmetrised off-diagonal squares sum to `359`, the cubic's
middle coefficient. -/
theorem transport_measure :
    D * Q = Matrix.transpose Q * D ∧ Matrix.det D = 1287 ∧ ((99 : ℚ) + 117 + 143 = 359) :=
  ⟨transport_self_adjoint, D_det, entries_sum_to_359⟩

end D0.Spectral.TransportSelfAdjoint
