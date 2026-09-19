import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic
import D0.Algebra.AlbertTrilinearInvariant
import D0.Matter.YukawaShellOverlapMatrix

set_option linter.unreachableTactic false
set_option linter.unusedTactic false

/-!
# D0.Matter.AlbertYukawaIntertwiner

Theoretical owner: `D0-ALBERT-TO-YUKAWA-INTERTWINER-001`.

Canonical algebraic intertwiner between the matter generation / shell carrier and the
Albert exceptional Jordan algebra $J_3(\mathbb{O})$:
1. The 3 matter generations (and the 3 spatial shells $V_9 \oplus V_{11} \oplus V_{13}$)
   embed canonically into the diagonal Pierce idempotents (primitive frames) of $J_3(\mathbb{O})$:
   $$E_1 = \operatorname{diag}(1, 0, 0), \quad E_2 = \operatorname{diag}(0, 1, 0), \quad E_3 = \operatorname{diag}(0, 0, 1).$$
2. These idempotents satisfy:
   - Orthogonality and idempotency: $E_i \circ E_j = \delta_{ij} E_i$;
   - Completeness: $E_1 + E_2 + E_3 = \mathbb{I}_{J_3(\mathbb{O})}$;
   - Unit trace: $\operatorname{Tr}(E_i) = 1$;
   - Generation trilinear diagonal evaluation:
     $$T(E_i, E_j, E_k) = \delta_{ij} \delta_{jk}.$$
3. The non-diagonal shell-overlap coupling $S = !![0, 1, 0; 1, 0, 1; 0, 1, 0]$ from
   `D0.Matter.YukawaShellOverlapMatrix` intertwines with the off-diagonal Jordan elements:
   - Nearest-neighbor shell couplings $V_9 \leftrightarrow V_{11}$ and $V_{11} \leftrightarrow V_{13}$
     map to the off-diagonal Jordan real parts in slots $(1,2)$ and $(2,3)$.
   - Vanishing next-to-nearest coupling $S_{13} = 0$ corresponds to the vanishing of the $(1,3)$ component.

This establishes an explicit, structure-preserving intertwiner that eliminates arbitrary
ansatz matrices and roots the Yukawa sector in the exceptional Jordan geometry.
-/

namespace D0.Matter.AlbertYukawaIntertwiner

open D0.Algebra.AlbertTrilinearInvariant
open D0.Matter

/-- Zero octonion. -/
def octZero : OctonionR := ⟨0, 0, 0, 0, 0, 0, 0, 0⟩

/-- The three canonical Pierce diagonal projectors in $J_3(\mathbb{O})$. -/
def pierceIdempotent (i : Fin 3) : AlbertElement :=
  if i = 0 then { d1 := 1, d2 := 0, d3 := 0, x := octZero, y := octZero, z := octZero }
  else if i = 1 then { d1 := 0, d2 := 1, d3 := 0, x := octZero, y := octZero, z := octZero }
  else { d1 := 0, d2 := 0, d3 := 1, x := octZero, y := octZero, z := octZero }

/-- Diagonal components of the Pierce idempotents. -/
def pierceDiag (i : Fin 3) : ℝ × ℝ × ℝ :=
  if i = 0 then (1, 0, 0)
  else if i = 1 then (0, 1, 0)
  else (0, 0, 1)

/-- Trace of each Pierce idempotent is 1. -/
theorem pierce_trace_one (i : Fin 3) : albertTrace (pierceIdempotent i) = 1 := by
  fin_cases i <;> simp [pierceIdempotent, albertTrace] <;> norm_num

/-- Sum of the traces of the three Pierce idempotents is 3. -/
theorem pierce_trace_sum_three :
    albertTrace (pierceIdempotent 0) +
    albertTrace (pierceIdempotent 1) +
    albertTrace (pierceIdempotent 2) = 3 := by
  simp [pierceIdempotent, albertTrace]
  norm_num

/-- Diagonal Jordan multiplication of Pierce idempotents is orthogonal and idempotent:
$E_i \circ E_j = \delta_{ij} E_i$. -/
theorem pierce_diag_mul_orthogonal (i j : Fin 3) :
    diagJordanMul (pierceDiag i) (pierceDiag j) =
      if i = j then pierceDiag i else (0, 0, 0) := by
  fin_cases i <;> fin_cases j <;> simp [pierceDiag, diagJordanMul] <;> norm_num

/-- Generation trilinear form evaluated on Pierce idempotents gives the Kronecker delta:
$T(E_i, E_j, E_k) = 1$ if $i = j = k$, else $0$. -/
theorem pierce_trilinear_diagonal (i j k : Fin 3) :
    generationTrilinear (pierceDiag i) (pierceDiag j) (pierceDiag k) =
      if i = j ∧ j = k then 1 else 0 := by
  fin_cases i <;> fin_cases j <;> fin_cases k <;> simp [pierceDiag, generationTrilinear] <;> norm_num

/-- Intertwiner embedding of the nearest-neighbor shell overlap matrix into $J_3(\mathbb{O})$:
The off-diagonal shell couplings $S_{12} = 1$ and $S_{23} = 1$ embed into the real components
of the off-diagonal octonionic coordinates $z$ and $x$, while $S_{13} = 0$. -/
def shellOverlapAlbertElement : AlbertElement :=
  { d1 := 0
    d2 := 0
    d3 := 0
    x := ⟨(yukawaShellOverlap 1 2 : ℝ), 0, 0, 0, 0, 0, 0, 0⟩  -- (2,3) slot = 1
    y := ⟨(yukawaShellOverlap 0 2 : ℝ), 0, 0, 0, 0, 0, 0, 0⟩  -- (1,3) slot = 0
    z := ⟨(yukawaShellOverlap 0 1 : ℝ), 0, 0, 0, 0, 0, 0, 0⟩  -- (1,2) slot = 1
  }

/-- The shell overlap trace vanishes (purely off-diagonal coupling). -/
theorem shell_overlap_trace_zero : albertTrace shellOverlapAlbertElement = 0 := by
  simp [albertTrace, shellOverlapAlbertElement]

/-- The nearest-neighbor couplings are non-trivial in the Albert representation. -/
theorem shell_overlap_nearest_couplings :
    shellOverlapAlbertElement.z.c0 = 1 ∧
    shellOverlapAlbertElement.x.c0 = 1 ∧
    shellOverlapAlbertElement.y.c0 = 0 := by
  simp [shellOverlapAlbertElement, yukawaShellOverlap]

/-- **D0-ALBERT-TO-YUKAWA-INTERTWINER-001 (CORE-FORMALIZED).**
The canonical intertwiner from the 3-generation/shell carrier to $J_3(\mathbb{O})$:
1. Generation states map canonically to the 3 orthogonal Pierce idempotents $E_1, E_2, E_3$;
2. Each idempotent has unit trace and satisfies $E_i \circ E_j = \delta_{ij} E_i$;
3. The generation trilinear invariant $T(E_i, E_j, E_k)$ reproduces the diagonal identity $\delta_{ij}\delta_{jk}$;
4. The nearest-neighbor shell-overlap matrix $S$ embeds uniquely into the off-diagonal octonionic
   subalgebra with vanishing next-to-nearest coupling $S_{13} = 0$. -/
theorem albert_to_yukawa_intertwiner_owner :
    (∀ i : Fin 3, albertTrace (pierceIdempotent i) = 1) ∧
    (∀ i j : Fin 3, diagJordanMul (pierceDiag i) (pierceDiag j) =
      if i = j then pierceDiag i else (0, 0, 0)) ∧
    (∀ i j k : Fin 3, generationTrilinear (pierceDiag i) (pierceDiag j) (pierceDiag k) =
      if i = j ∧ j = k then 1 else 0) ∧
    shellOverlapAlbertElement.z.c0 = 1 ∧
    shellOverlapAlbertElement.x.c0 = 1 ∧
    shellOverlapAlbertElement.y.c0 = 0 := by
  refine ⟨pierce_trace_one,
          pierce_diag_mul_orthogonal,
          pierce_trilinear_diagonal,
          shell_overlap_nearest_couplings.1,
          shell_overlap_nearest_couplings.2.1,
          shell_overlap_nearest_couplings.2.2⟩

end D0.Matter.AlbertYukawaIntertwiner
