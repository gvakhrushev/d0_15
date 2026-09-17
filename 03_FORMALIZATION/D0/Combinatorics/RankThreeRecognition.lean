import Mathlib.Combinatorics.SimpleGraph.AdjMatrix
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Tactic

/-!
# Recovering three graph parts from the adjacency operator

A finite simple adjacency matrix of rank at most three containing a triangle
determines every entry from its three triangle columns. The diagonal and the
zero-one condition force each vertex to have either zero or two triangle
neighbours. In the absence of isolated vertices, the missing neighbour defines
three nonempty parts, and adjacency is exactly inequality of these parts.

No partition, completeness, number of vertices, or part sizes are inputs.
This is a kernel-checked special case of the classical rank/clique recognition
theorem (Akbari, Cameron, Khosrovshahi, "Ranks and signatures of adjacency
matrices", Corollary 8). Rank and triangle existence remain explicit hypotheses.
-/

namespace D0.Combinatorics.RankThreeRecognition

open Matrix

variable {V : Type*} [Fintype V]

/-- A triangle is supplied by its three vertices, without zone labels on `V`. -/
def IsTriangle (A : Matrix V V ℚ) (t : Fin 3 → V) : Prop :=
  ∀ i j, A (t i) (t j) = if i = j then 0 else 1

/-- Rank at most three kills every four-by-four minor, including mixed minors. -/
theorem four_minor_zero (A : Matrix V V ℚ) (hr : A.rank ≤ 3)
    (r c : Fin 4 → V) : (A.submatrix r c).det = 0 := by
  by_contra h
  have hu := Matrix.rank_of_isUnit (A.submatrix r c)
    ((Matrix.isUnit_iff_isUnit_det _).mpr (isUnit_iff_ne_zero.mpr h))
  have hl := Matrix.rank_submatrix_le A r c
  simp only [Fintype.card_fin] at hu
  omega

/-- The exact determinant identity for a triangle with one extra row and column. -/
theorem triangle_border_det (a b c d e f z : ℚ) :
    (!![0, 1, 1, d; 1, 0, 1, e; 1, 1, 0, f; a, b, c, z]).det =
      2 * z - ((-a + b + c) * d + (a - b + c) * e + (a + b - c) * f) := by
  rw [Matrix.det_succ_row_zero]
  simp only [Fin.sum_univ_succ, Matrix.det_fin_three, Matrix.submatrix_apply]
  change
    1 * 0 * (0 * 0 * z - 0 * f * c - 1 * 1 * z + 1 * f * b + e * 1 * c - e * 0 * b) +
      ((-1) * 1 * (1 * 0 * z - 1 * f * c - 1 * 1 * z + 1 * f * a + e * 1 * c - e * 0 * a) +
      (1 * 1 * (1 * 1 * z - 1 * f * b - 0 * 1 * z + 0 * f * a + e * 1 * b - e * 1 * a) +
      ((-1) * d * (1 * 1 * c - 1 * 0 * b - 0 * 1 * c + 0 * 0 * a + 1 * 1 * b - 1 * 1 * a) + 0))) = _
  ring

/-- A triangle is a complete sampling set for a rank-three adjacency operator. -/
theorem triangle_columns_determine_entry (A : Matrix V V ℚ)
    (hr : A.rank ≤ 3) (t : Fin 3 → V) (ht : IsTriangle A t) (x y : V) :
    2 * A x y =
      (-A x (t 0) + A x (t 1) + A x (t 2)) * A (t 0) y +
      (A x (t 0) - A x (t 1) + A x (t 2)) * A (t 1) y +
      (A x (t 0) + A x (t 1) - A x (t 2)) * A (t 2) y := by
  have hz := four_minor_zero A hr ![t 0, t 1, t 2, x] ![t 0, t 1, t 2, y]
  change ∀ i j, A (t i) (t j) = if i = j then 0 else 1 at ht
  have hm : A.submatrix ![t 0, t 1, t 2, x] ![t 0, t 1, t 2, y] =
      !![0, 1, 1, A (t 0) y;
         1, 0, 1, A (t 1) y;
         1, 1, 0, A (t 2) y;
         A x (t 0), A x (t 1), A x (t 2), A x y] := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [Matrix.submatrix, ht]
  rw [hm, triangle_border_det] at hz
  linarith

/-- Zero triangle profile is equivalent to an isolated vertex. -/
theorem zero_profile_iff_isolated (A : Matrix V V ℚ)
    (hr : A.rank ≤ 3) (t : Fin 3 → V) (ht : IsTriangle A t) (x : V) :
    (∀ i, A x (t i) = 0) ↔ ∀ y, A x y = 0 := by
  constructor
  · intro hx y
    have h := triangle_columns_determine_entry A hr t ht x y
    simp only [hx, neg_zero, add_zero, sub_zero, zero_mul] at h
    linarith
  · intro hx i
    exact hx (t i)

/-- Every nonisolated vertex has one and only one missing triangle neighbour. -/
theorem vertex_profile (A : Matrix V V ℚ) (hA : A.IsAdjMatrix)
    (hr : A.rank ≤ 3) (t : Fin 3 → V) (ht : IsTriangle A t)
    (hn : ∀ x, ∃ y, A x y = 1) (x : V) :
    ∃ i : Fin 3, ∀ j, A x (t j) = if i = j then 0 else 1 := by
  have hd := triangle_columns_determine_entry A hr t ht x x
  rw [hA.apply_diag] at hd
  rw [hA.symm.apply x (t 0), hA.symm.apply x (t 1),
    hA.symm.apply x (t 2)] at hd
  rcases hA.zero_or_one x (t 0) with h0 | h0 <;>
    rcases hA.zero_or_one x (t 1) with h1 | h1 <;>
    rcases hA.zero_or_one x (t 2) with h2 | h2
  · obtain ⟨y, hy⟩ := hn x
    have hz := (zero_profile_iff_isolated A hr t ht x).mp
      (by intro i; fin_cases i <;> assumption) y
    linarith
  · norm_num [h0, h1, h2] at hd
  · norm_num [h0, h1, h2] at hd
  · exact ⟨0, by intro j; fin_cases j <;> simp [h0, h1, h2]⟩
  · norm_num [h0, h1, h2] at hd
  · exact ⟨1, by intro j; fin_cases j <;> simp [h0, h1, h2]⟩
  · exact ⟨2, by intro j; fin_cases j <;> simp [h0, h1, h2]⟩
  · norm_num [h0, h1, h2] at hd

/-- The part of a vertex is read directly from its adjacency to the anchor triangle. -/
def recoveredPart (A : Matrix V V ℚ) (t : Fin 3 → V) (x : V) : Fin 3 :=
  if A x (t 0) = 0 then 0 else if A x (t 1) = 0 then 1 else 2

omit [Fintype V] in
theorem recoveredPart_of_profile (A : Matrix V V ℚ) (t : Fin 3 → V)
    (x : V) (i : Fin 3)
    (hi : ∀ j, A x (t j) = if i = j then 0 else 1) :
    recoveredPart A t x = i := by
  fin_cases i <;> simp [recoveredPart, hi]

theorem recoveredPart_profile (A : Matrix V V ℚ) (hA : A.IsAdjMatrix)
    (hr : A.rank ≤ 3) (t : Fin 3 → V) (ht : IsTriangle A t)
    (hn : ∀ x, ∃ y, A x y = 1) (x : V) (j : Fin 3) :
    A x (t j) = if recoveredPart A t x = j then 0 else 1 := by
  obtain ⟨i, hi⟩ := vertex_profile A hA hr t ht hn x
  rw [recoveredPart_of_profile A t x i hi]
  exact hi j

omit [Fintype V] in
theorem recoveredPart_anchor (A : Matrix V V ℚ) (t : Fin 3 → V)
    (ht : IsTriangle A t) (i : Fin 3) : recoveredPart A t (t i) = i :=
  recoveredPart_of_profile A t (t i) i (ht i)

/-- The graph is complete tripartite on the recovered, necessarily nonempty fibres. -/
theorem adjacency_recovered (A : Matrix V V ℚ) (hA : A.IsAdjMatrix)
    (hr : A.rank ≤ 3) (t : Fin 3 → V) (ht : IsTriangle A t)
    (hn : ∀ x, ∃ y, A x y = 1) (x y : V) :
    A x y = if recoveredPart A t x = recoveredPart A t y then 0 else 1 := by
  have h := triangle_columns_determine_entry A hr t ht x y
  rw [hA.symm.apply y (t 0), hA.symm.apply y (t 1),
    hA.symm.apply y (t 2)] at h
  simp only [recoveredPart_profile A hA hr t ht hn] at h
  generalize recoveredPart A t x = i at *
  generalize recoveredPart A t y = j at *
  fin_cases i <;> fin_cases j <;> norm_num [Fin.ext_iff] at h ⊢ <;> linarith

/-- Recognition from operator data, with no input partition. -/
theorem rank_three_recognizes_tripartite (A : Matrix V V ℚ) (hA : A.IsAdjMatrix)
    (hr : A.rank ≤ 3) (t : Fin 3 → V) (ht : IsTriangle A t)
    (hn : ∀ x, ∃ y, A x y = 1) :
    ∃ z : V → Fin 3, Function.Surjective z ∧
      ∀ x y, A x y = if z x = z y then 0 else 1 := by
  refine ⟨recoveredPart A t, ?_, adjacency_recovered A hA hr t ht hn⟩
  intro i
  exact ⟨t i, recoveredPart_anchor A t ht i⟩

end D0.Combinatorics.RankThreeRecognition
