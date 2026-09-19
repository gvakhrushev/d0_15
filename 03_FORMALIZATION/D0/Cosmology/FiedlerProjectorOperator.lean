import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Tactic
import D0.Cosmology.CLightconePercolationOwner

/-!
# D0.Cosmology.FiedlerProjectorOperator

Theoretical owner: `D0-FIEDLER-PROJECTOR-OPERATOR-001`.

Concrete finite operator realization of the Hodge-Fiedler spectral projector $\Pi_F$
on the rational 33-vertex scene $K(9,11,13)$.

In the graph Laplacian $L$ of $K(9,11,13)$:
- $V = \mathrm{Fin}\ 33$, partitioned into three parts of sizes $9, 11, 13$.
- Part 0 (size 9): indices $[0, 9)$, degree 24
- Part 1 (size 11): indices $[9, 20)$, degree 22
- Part 2 (size 13): indices $[20, 33)$, degree 20
- The Fiedler eigenvalue is $\lambda_2 = 20$, with multiplicity 12.
- The Fiedler eigenspace is precisely the zero-sum subspace supported on Part 2 (size 13).

Therefore, on $V_{13}$, the canonical orthogonal projector is:
$$\Pi_F = I_{13} - \frac{1}{13} J_{13}$$
and zero on all other vertices. Entrywise:
$$(\Pi_F)_{ij} = \begin{cases}
12/13, & i = j \in V_{13} \\
-1/13, & i \neq j,\ i,j \in V_{13} \\
0, & \text{otherwise}.
\end{cases}$$

Key verified properties:
1. Symmetry: $\Pi_F^T = \Pi_F$
2. Idempotence: $\Pi_F^2 = \Pi_F$
3. Eigenspace relation: $L \Pi_F = 20 \Pi_F$
4. Trace / Rank: $\mathrm{Tr}(\Pi_F) = 12 = \mathrm{mult}(\lambda_2)$
-/

namespace D0.Cosmology.FiedlerProjectorOperator

open D0.Cosmology

/-- Combinatorial Laplacian of $K(9,11,13)$ on `Fin 33 × Fin 33` over $\mathbb{Q}$. -/
def Lq : Matrix (Fin 33) (Fin 33) ℚ := Lap

/-- Predicate selecting vertices belonging to Part 2 (the unique part of size 13,
degree 20, indices 20 through 32). -/
def inPart13 (i : Fin 33) : Bool :=
  20 ≤ i.val

/-- The exact rational Hodge-Fiedler spectral projector $\Pi_F$ on `Matrix (Fin 33) (Fin 33) ℚ`. -/
def PiF : Matrix (Fin 33) (Fin 33) ℚ :=
  Matrix.of (fun i j =>
    if inPart13 i && inPart13 j then
      if i = j then 12 / 13 else -1 / 13
    else 0)

/-- $\Pi_F$ is symmetric (self-adjoint). -/
theorem PiF_transpose : PiF.transpose = PiF := by
  ext i j
  simp only [PiF, Matrix.transpose_apply, Matrix.of_apply]
  by_cases h : inPart13 i && inPart13 j
  · have h' : inPart13 j && inPart13 i := by
      rw [Bool.and_comm]; exact h
    simp [h, h']
    by_cases heq : j = i
    · simp [heq]
    · have heq' : ¬ (i = j) := fun h_ij => heq h_ij.symm
      simp [heq, heq']
  · have h' : ¬ (inPart13 j && inPart13 i) := by
      rw [Bool.and_comm]; exact h
    simp [h, h']

/-- Entrywise identity for $\Pi_F * \Pi_F = \Pi_F$. -/
theorem PiF_mul_self_entry : ∀ i j : Fin 33, (PiF * PiF) i j = PiF i j := by
  native_decide +revert

/-- $\Pi_F$ is idempotent: $\Pi_F^2 = \Pi_F$. -/
theorem PiF_mul_self : PiF * PiF = PiF := by
  ext i j
  exact PiF_mul_self_entry i j

/-- Entrywise identity for $L_q \Pi_F = 20 \Pi_F$. -/
theorem Lq_mul_PiF_entry : ∀ i j : Fin 33, (Lq * PiF) i j = ((20 : ℚ) • PiF) i j := by
  native_decide +revert

/-- $\Pi_F$ projects onto the Fiedler eigenspace of eigenvalue 20: $L \Pi_F = 20 \Pi_F$. -/
theorem Lq_mul_PiF : Lq * PiF = (20 : ℚ) • PiF := by
  ext i j
  exact Lq_mul_PiF_entry i j

/-- The trace of $\Pi_F$ is 12, matching the multiplicity of the Fiedler eigenvalue $\lambda_2 = 20$. -/
theorem PiF_trace : Matrix.trace PiF = 12 := by
  native_decide

/-- Comprehensive owner theorem for `D0-FIEDLER-PROJECTOR-OPERATOR-001`. -/
theorem fiedler_projector_operator_owner :
    PiF.transpose = PiF ∧
    PiF * PiF = PiF ∧
    Lq * PiF = (20 : ℚ) • PiF ∧
    Matrix.trace PiF = 12 := by
  refine ⟨PiF_transpose, PiF_mul_self, Lq_mul_PiF, PiF_trace⟩

end D0.Cosmology.FiedlerProjectorOperator
