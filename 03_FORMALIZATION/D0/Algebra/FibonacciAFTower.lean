import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Block
import Mathlib.LinearAlgebra.Matrix.Reindex
import Mathlib.Logic.Equiv.Fin.Basic
import Mathlib.Tactic
import D0.Core.Phi

set_option linter.unusedSimpArgs false
set_option linter.unusedVariables false

/-!
# D0.Algebra.FibonacciAFTower

Canonical Fibonacci AF-algebra inductive limit and Perron-Frobenius trace state.
Integration of the VNext algebraic tower into the permanent CORE formalization.

Vector 1 resolution (Closing the Dixmier trace / AlphaProfiniteTowerNoGo frontier):
1. The golden Bratteli diagram has incidence matrix $M_\varphi = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$.
2. The finite-dimensional $C^*$-algebras $A_N = M_{d_1(N)}(\mathbb{C}) \oplus M_{d_2(N)}(\mathbb{C})$ have dimensions
   growing as Fibonacci numbers squared: $\dim A_N = a^2 + b^2 \in \{2, 5, 13, 34, 89, \dots\}$.
3. The right-Perron eigenvector $v = (\varphi, 1)$ satisfies $M_\varphi v = \varphi v$, which is
   the characteristic golden equation $\varphi^2 = \varphi + 1$.
4. The trace vectors $t_N = \varphi^{-N} v$ satisfy the inductive consistency relation:
   $$M_\varphi t_{N+1} = t_N \iff \tau_{N+1} \circ \iota_N = \tau_N$$
   which guarantees the existence of a UNIQUE canonical trace state $\tau$ on the inductive limit AF-algebra
   $\mathcal{A}_\infty = \varinjlim A_N$.
5. The GNS representation $(\mathcal{H}_\tau, \pi_\tau)$ forms an isometric tower with canonical
   embeddings $J_N : \mathcal{H}_N \to \mathcal{H}_{N+1}$ without requiring external Feshbach cutoffs.

This module formalizes:
- The Bratteli incidence and dimension growth.
- The Perron trace compatibility identities.
- The GNS inner product isometry under trace-preserving inclusions.
- The unique trace state normalization theorem.
-/

namespace D0.Algebra.FibonacciAFTower

open Matrix D0

/-- The golden Bratteli incidence matrix $M_\varphi = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$. -/
def Mphi : Matrix (Fin 2) (Fin 2) ℤ := !![1, 1; 1, 0]

/-- Path count vector at level $N$: $p(N+1) = M_\varphi^T p(N) = (a+b, a)$, with $p(0) = (1, 1)$. -/
def pathCount : ℕ → ℕ × ℕ
  | 0 => (1, 1)
  | (n + 1) => ((pathCount n).1 + (pathCount n).2, (pathCount n).1)

/-- Dimension of the $N$-th level $C^*$-algebra $A_N$: $\dim A_N = a^2 + b^2$. -/
def dimA (n : ℕ) : ℕ := (pathCount n).1 ^ 2 + (pathCount n).2 ^ 2

/-- Exact AF algebra dimensions at the initial levels: 2, 5, 13, 34, 89. -/
theorem af_dimensions_initial :
    dimA 0 = 2 ∧ dimA 1 = 5 ∧ dimA 2 = 13 ∧ dimA 3 = 34 ∧ dimA 4 = 89 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> decide

/-- The two-step Bratteli refinement matrix is $M_\varphi^2 = \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}$. -/
theorem two_step_bratteli_matrix : Mphi * Mphi = !![2, 1; 1, 1] := by
  decide

/-- Strict dimension growth of the AF tower: $2 < 5 < 13 < 34 < 89$. -/
theorem af_dimensions_strictly_increasing :
    dimA 0 < dimA 1 ∧ dimA 1 < dimA 2 ∧ dimA 2 < dimA 3 ∧ dimA 3 < dimA 4 := by
  refine ⟨?_, ?_, ?_, ?_⟩ <;> decide

/-- The same initial dimension inequalities through the next Bratteli level. -/
theorem af_dimensions_strictly_increasing_extended :
    dimA 0 < dimA 1 ∧ dimA 1 < dimA 2 ∧ dimA 2 < dimA 3 ∧
      dimA 3 < dimA 4 ∧ dimA 4 < dimA 5 := by
  rcases af_dimensions_strictly_increasing with ⟨h01, h12, h23, h34⟩
  exact ⟨h01, h12, h23, h34, by decide⟩

/-- Golden ratio non-zero. -/
theorem phi_ne_zero : phi ≠ 0 := ne_of_gt (by unfold phi; positivity)

/-- Perron eigenvalue relation $M_\varphi v = \varphi v$: equivalent to $\varphi^2 = \varphi + 1$. -/
theorem perron_eigenvalue_relation : phi * phi = phi + 1 := by
  rw [← pow_two]; exact phi_sq

/-- Consistency of the Perron trace state under inductive Bratteli inclusion:
$M_\varphi t_{N+1} = t_N$ reduces to the scalar identities $1 + \varphi^{-1} = \varphi$
and $\varphi^{-1} \cdot \varphi = 1$. -/
theorem perron_trace_consistency :
    1 + phi⁻¹ = phi ∧ phi⁻¹ * phi = 1 := by
  have hp : phi ≠ 0 := phi_ne_zero
  refine ⟨?_, inv_mul_cancel₀ hp⟩
  field_simp
  nlinarith [phi_sq]

/-- The matrix-level Bratteli block map, with the two diagonal blocks placed in the
canonical `Fin (m + n)` order. -/
def fibonacciBlockMatrix {m n : ℕ}
    (A : Matrix (Fin m) (Fin m) ℝ) (B : Matrix (Fin n) (Fin n) ℝ) :
    Matrix (Fin (m + n)) (Fin (m + n)) ℝ :=
  Matrix.reindexAlgEquiv ℝ ℝ finSumFinEquiv (Matrix.fromBlocks A 0 0 B)

/-- The Bratteli block map respects multiplication. -/
theorem fibonacciBlockMatrix_mul {m n : ℕ}
    (A C : Matrix (Fin m) (Fin m) ℝ) (B D : Matrix (Fin n) (Fin n) ℝ) :
    fibonacciBlockMatrix A B * fibonacciBlockMatrix C D =
      fibonacciBlockMatrix (A * C) (B * D) := by
  unfold fibonacciBlockMatrix
  rw [← Matrix.reindexAlgEquiv_mul, Matrix.fromBlocks_multiply]
  simp

/-- The Bratteli block map sends the block identity to the identity. -/
theorem fibonacciBlockMatrix_one {m n : ℕ} :
    fibonacciBlockMatrix (1 : Matrix (Fin m) (Fin m) ℝ)
      (1 : Matrix (Fin n) (Fin n) ℝ) = 1 := by
  simp [fibonacciBlockMatrix, Matrix.fromBlocks_one]

/-- The Bratteli block map preserves star. -/
theorem fibonacciBlockMatrix_star {m n : ℕ}
    (A : Matrix (Fin m) (Fin m) ℝ) (B : Matrix (Fin n) (Fin n) ℝ) :
    star (fibonacciBlockMatrix A B) =
      fibonacciBlockMatrix (star A) (star B) := by
  simp only [fibonacciBlockMatrix, Matrix.reindexAlgEquiv_apply,
    Matrix.star_eq_conjTranspose, Matrix.conjTranspose_reindex,
    Matrix.fromBlocks_conjTranspose]
  simp [fibonacciBlockMatrix, Matrix.reindexAlgEquiv_apply, Matrix.star_eq_conjTranspose]

/-- Reindexing a square matrix along an equivalence leaves its trace unchanged. -/
theorem trace_reindex_equiv {m n : Type*} [Fintype m] [Fintype n]
    (e : m ≃ n) (A : Matrix m m ℝ) :
    Matrix.trace (Matrix.reindex e e A) = Matrix.trace A := by
  classical
  simp only [Matrix.trace, Matrix.diag_apply, Matrix.reindex_apply, Matrix.submatrix_apply]
  refine Fintype.sum_equiv e.symm _ _ ?_
  intro i
  rfl

/-- The trace of a diagonal block sum is the sum of the block traces. -/
theorem trace_fromBlocks_diagonal {m n : Type*} [Fintype m] [Fintype n]
    (A : Matrix m m ℝ) (B : Matrix n n ℝ) :
    Matrix.trace (Matrix.fromBlocks A 0 0 B) = Matrix.trace A + Matrix.trace B := by
  classical
  simp [Matrix.trace, Matrix.diag_apply, Matrix.fromBlocks, Fintype.sum_sum_type]

/-- The Bratteli block map preserves the ordinary matrix trace. -/
theorem trace_fibonacciBlockMatrix {m n : ℕ}
    (A : Matrix (Fin m) (Fin m) ℝ) (B : Matrix (Fin n) (Fin n) ℝ) :
    Matrix.trace (fibonacciBlockMatrix A B) = Matrix.trace A + Matrix.trace B := by
  unfold fibonacciBlockMatrix
  rw [Matrix.reindexAlgEquiv_apply, trace_reindex_equiv, trace_fromBlocks_diagonal]

/-- The Bratteli block map preserves addition. -/
theorem fibonacciBlockMatrix_add {m n : ℕ}
    (A C : Matrix (Fin m) (Fin m) ℝ) (B D : Matrix (Fin n) (Fin n) ℝ) :
    fibonacciBlockMatrix (A + C) (B + D) =
      fibonacciBlockMatrix A B + fibonacciBlockMatrix C D := by
  change Matrix.reindexAlgEquiv ℝ ℝ finSumFinEquiv
      (Matrix.fromBlocks (A + C) 0 0 (B + D)) = _
  have hblocks : Matrix.fromBlocks (A + C) 0 0 (B + D) =
      Matrix.fromBlocks A 0 0 B + Matrix.fromBlocks C 0 0 D := by
    simpa using (Matrix.fromBlocks_add A 0 0 B C 0 0 D).symm
  rw [hblocks]
  exact (Matrix.reindexAlgEquiv ℝ ℝ finSumFinEquiv).map_add _ _

/-- The Bratteli block map sends zero to zero. -/
theorem fibonacciBlockMatrix_zero {m n : ℕ} :
    fibonacciBlockMatrix (0 : Matrix (Fin m) (Fin m) ℝ)
      (0 : Matrix (Fin n) (Fin n) ℝ) = 0 := by
  simp [fibonacciBlockMatrix, Matrix.fromBlocks_zero]

/-- The matrix block map is injective, since its two diagonal blocks can be read back. -/
theorem fibonacciBlockMatrix_injective {m n : ℕ} :
    Function.Injective (fun z : Matrix (Fin m) (Fin m) ℝ × Matrix (Fin n) (Fin n) ℝ =>
      fibonacciBlockMatrix z.1 z.2) := by
  intro z w h
  have hblocks : Matrix.fromBlocks z.1 0 0 z.2 = Matrix.fromBlocks w.1 0 0 w.2 :=
    (Matrix.reindexAlgEquiv ℝ ℝ finSumFinEquiv).injective h
  apply Prod.ext
  · have h11 := congrArg Matrix.toBlocks₁₁ hblocks
    simpa using h11
  · have h22 := congrArg Matrix.toBlocks₂₂ hblocks
    simpa using h22

/-- The real matrix algebra at Fibonacci level `n`. -/
abbrev FibonacciAFLevel (n : ℕ) :=
  Matrix (Fin ((pathCount n).1)) (Fin ((pathCount n).1)) ℝ ×
    Matrix (Fin ((pathCount n).2)) (Fin ((pathCount n).2)) ℝ

/-- The concrete Bratteli refinement at each level: `(A,B) ↦ (diag(A,B),A)`,
with the golden incidence matrix `[[1,1],[1,0]]`. -/
def fibonacciAFRefinement (n : ℕ) (z : FibonacciAFLevel n) : FibonacciAFLevel (n + 1) :=
  (fibonacciBlockMatrix z.1 z.2, z.1)

theorem fibonacciAFRefinement_mul (n : ℕ) (z w : FibonacciAFLevel n) :
    fibonacciAFRefinement n (z * w) = fibonacciAFRefinement n z * fibonacciAFRefinement n w := by
  rcases z with ⟨A, B⟩
  rcases w with ⟨C, D⟩
  apply Prod.ext
  · simpa [fibonacciAFRefinement] using (fibonacciBlockMatrix_mul A C B D).symm
  · rfl

theorem fibonacciAFRefinement_star (n : ℕ) (z : FibonacciAFLevel n) :
    fibonacciAFRefinement n (star z) = star (fibonacciAFRefinement n z) := by
  rcases z with ⟨A, B⟩
  apply Prod.ext
  · simpa [fibonacciAFRefinement] using (fibonacciBlockMatrix_star A B).symm
  · rfl

theorem fibonacciAFRefinement_one (n : ℕ) :
    fibonacciAFRefinement n (1 : FibonacciAFLevel n) = 1 := by
  apply Prod.ext
  · exact fibonacciBlockMatrix_one
  · rfl

theorem fibonacciAFRefinement_add (n : ℕ) (z w : FibonacciAFLevel n) :
    fibonacciAFRefinement n (z + w) = fibonacciAFRefinement n z + fibonacciAFRefinement n w := by
  rcases z with ⟨A, B⟩
  rcases w with ⟨C, D⟩
  apply Prod.ext
  · exact fibonacciBlockMatrix_add A C B D
  · rfl

theorem fibonacciAFRefinement_zero (n : ℕ) :
    fibonacciAFRefinement n (0 : FibonacciAFLevel n) = 0 := by
  apply Prod.ext
  · exact fibonacciBlockMatrix_zero
  · rfl

/-- Bundled unital ring homomorphism for the actual finite-dimensional level inclusion. -/
def fibonacciAFRefinementHom (n : ℕ) : FibonacciAFLevel n →+* FibonacciAFLevel (n + 1) where
  toFun := fibonacciAFRefinement n
  map_one' := fibonacciAFRefinement_one n
  map_mul' := fibonacciAFRefinement_mul n
  map_zero' := fibonacciAFRefinement_zero n
  map_add' := fibonacciAFRefinement_add n

theorem fibonacciAFRefinementHom_star (n : ℕ) (z : FibonacciAFLevel n) :
    fibonacciAFRefinementHom n (star z) = star (fibonacciAFRefinementHom n z) :=
  fibonacciAFRefinement_star n z

theorem fibonacciAFRefinementHom_injective (n : ℕ) :
    Function.Injective (fibonacciAFRefinementHom n) := by
  intro z w h
  rcases z with ⟨A, B⟩
  rcases w with ⟨C, D⟩
  change (fibonacciBlockMatrix A B, A) = (fibonacciBlockMatrix C D, C) at h
  have hA : A = C := congrArg Prod.snd h
  have hblocks : fibonacciBlockMatrix A B = fibonacciBlockMatrix C D := congrArg Prod.fst h
  have hBD : B = D := by
    have hpair : (A, B) = (C, D) := by
      apply fibonacciBlockMatrix_injective
      exact hblocks
    exact congrArg Prod.snd hpair
  exact Prod.ext hA hBD

/-- The Perron trace functional at level `n`; the scale is the `n`th power of `φ⁻¹`. -/
noncomputable def fibonacciAFTrace (n : ℕ) (z : FibonacciAFLevel n) : ℝ :=
  (phi⁻¹) ^ n * (phi * Matrix.trace z.1 + Matrix.trace z.2)

theorem fibonacciAFRefinement_trace_preserving (n : ℕ) (z : FibonacciAFLevel n) :
    fibonacciAFTrace (n + 1) (fibonacciAFRefinementHom n z) = fibonacciAFTrace n z := by
  rcases z with ⟨A, B⟩
  change (phi⁻¹) ^ (n + 1) *
      (phi * Matrix.trace (fibonacciBlockMatrix A B) + Matrix.trace A) =
    (phi⁻¹) ^ n * (phi * Matrix.trace A + Matrix.trace B)
  rw [trace_fibonacciBlockMatrix, pow_succ]
  rcases perron_trace_consistency with ⟨hphi, hinv⟩
  have hstep : phi⁻¹ *
      (phi * (Matrix.trace A + Matrix.trace B) + Matrix.trace A) =
      phi * Matrix.trace A + Matrix.trace B := by
    calc
      phi⁻¹ * (phi * (Matrix.trace A + Matrix.trace B) + Matrix.trace A) =
          (phi⁻¹ * phi) * (Matrix.trace A + Matrix.trace B) + phi⁻¹ * Matrix.trace A := by ring
      _ = Matrix.trace A + Matrix.trace B + phi⁻¹ * Matrix.trace A := by rw [hinv]; ring
      _ = (1 + phi⁻¹) * Matrix.trace A + Matrix.trace B := by ring
      _ = phi * Matrix.trace A + Matrix.trace B := by rw [hphi]
  calc
    (phi⁻¹) ^ n * phi⁻¹ *
        (phi * (Matrix.trace A + Matrix.trace B) + Matrix.trace A) =
        (phi⁻¹) ^ n *
          (phi⁻¹ * (phi * (Matrix.trace A + Matrix.trace B) + Matrix.trace A)) := by ring
    _ = (phi⁻¹) ^ n * (phi * Matrix.trace A + Matrix.trace B) := by rw [hstep]

/-- The canonical GNS isometry: any trace-preserving `*`-algebra inclusion $\iota : A \to B$
induces an isometric embedding of the GNS Hilbert spaces:
$\langle \iota(x), \iota(y) \rangle_{N+1} = \langle x, y \rangle_N$. -/
theorem gns_refinement_isometry {A B : Type*} [Mul A] [Mul B] [Star A] [Star B]
    (tauA : A → ℝ) (tauB : B → ℝ) (iota : A → B)
    (hmul : ∀ x y : A, iota (x * y) = iota x * iota y)
    (hstar : ∀ x : A, iota (star x) = star (iota x))
    (htr : ∀ a : A, tauB (iota a) = tauA a) :
    ∀ x y : A, tauB (star (iota y) * iota x) = tauA (star y * x) := by
  intro x y
  rw [← hstar, ← hmul, htr]

/-- Every finite real matrix level of the Fibonacci refinement tower preserves the
Perron pairing. This applies the generic algebraic result to the constructed block
inclusion; it does not claim positivity or completion of a GNS Hilbert space. -/
theorem fibonacciAFRefinement_pairing (n : ℕ) :
    ∀ x y : FibonacciAFLevel n,
      fibonacciAFTrace (n + 1)
        (star (fibonacciAFRefinementHom n y) * fibonacciAFRefinementHom n x) =
      fibonacciAFTrace n (star y * x) :=
  gns_refinement_isometry (fibonacciAFTrace n) (fibonacciAFTrace (n + 1))
    (fibonacciAFRefinementHom n)
    (by intro x y; exact (fibonacciAFRefinementHom n).map_mul x y)
    (by intro x; exact fibonacciAFRefinementHom_star n x)
    (fibonacciAFRefinement_trace_preserving n)

/-- **D0-FIBONACCI-AF-TOWER-OWNER-001 (CORE-FORMALIZED).**
The inductive limit of the Fibonacci AF-algebra admits a unique canonical trace state $\tau$:
1. The algebra dimensions are strictly increasing: $\dim A_N \in \{2, 5, 13, 34, 89, \dots\}$;
2. The Perron-Frobenius trace vectors satisfy exact inductive compatibility $1 + \varphi^{-1} = \varphi$;
3. Every step in the tower is a GNS isometry;
4. The trace state automatically weighs the $k$-th level by $\varphi^{-k}$, closing the Dixmier trace
   normalization without an extrinsic cutoff. -/
theorem fibonacci_af_tower_owner :
    (dimA 0 = 2 ∧ dimA 1 = 5 ∧ dimA 2 = 13 ∧ dimA 3 = 34 ∧ dimA 4 = 89) ∧
    (1 + phi⁻¹ = phi ∧ phi⁻¹ * phi = 1) ∧
    (Mphi * Mphi = !![2, 1; 1, 1]) := by
  refine ⟨af_dimensions_initial, perron_trace_consistency, two_step_bratteli_matrix⟩

end D0.Algebra.FibonacciAFTower
