import D0.Synthesis.SpectralSceneRigidity
import D0.Claims.Signature31Split
import Mathlib.Combinatorics.SimpleGraph.Extremal.Turan

/-!
# Recognition from dimension, rank and quadratic moment alone

The cubic moment in the four-reading passport is redundant. On 33 vertices,
359 edges exceed the triangle-free bound. Rank at most three then recovers a
complete tripartite nonisolated support. A support of at most 32 vertices can
have at most floor(32²/3) = 341 such edges, so there are no isolates. The existing
vertex/edge inverse theorem determines the parts. Consequently the cubic moment
7722 is an output, not an input.
-/

namespace D0.Synthesis.DenseOperatorSceneRigidity

open Matrix
open D0.Combinatorics.RankThreeRecognition
open D0.Synthesis.OperatorSceneReconstruction
open D0.Synthesis.SpectralSceneRigidity
open scoped Classical

variable {V : Type*} [Fintype V]

theorem dense_passport_triangle (A : Matrix V V ℚ) (hA : A.IsAdjMatrix)
    (hV : Fintype.card V = 33) (h2 : Matrix.trace (A * A) = 718) :
    ∃ t : Fin 3 → V, IsTriangle A t := by
  classical
  let G := hA.toGraph
  have hGA : G.adjMatrix ℚ = A := by
    ext x y
    change (if A x y = 1 then 1 else 0) = A x y
    rcases hA.zero_or_one x y with h | h <;> simp [h]
  have hedges : G.edgeFinset.card = 359 := by
    have htrace : Matrix.trace (A * A) = (2 * G.edgeFinset.card : ℕ) := by
      conv_lhs => rw [← hGA]
      simp only [Matrix.trace, Matrix.diag, G.adjMatrix_mul_self_apply_self]
      rw [← Nat.cast_sum, G.sum_degrees_eq_twice_card_edges]
    rw [h2] at htrace
    exact_mod_cast (show (G.edgeFinset.card : ℚ) = 359 by push_cast at htrace; linarith)
  have hnot : ¬ G.CliqueFree 3 := by
    intro h
    have hb := h.card_edgeFinset_le (r := 2)
    rw [hV, hedges] at hb
    norm_num at hb
  let e := SimpleGraph.topEmbeddingOfNotCliqueFree hnot
  refine ⟨e, ?_⟩
  intro i j
  by_cases hij : i = j
  · subst j; simp [hA.apply_diag]
  · rw [if_neg hij]
    exact e.map_rel_iff.mpr (by simpa using hij)

theorem dense_passport_no_isolates (A : Matrix V V ℚ) (hA : A.IsAdjMatrix)
    (hr : A.rank ≤ 3) (hV : Fintype.card V = 33)
    (h2 : Matrix.trace (A * A) = 718) : ∀ x, Active A x := by
  classical
  obtain ⟨t, ht⟩ := dense_passport_triangle A hA hV h2
  let W := {x // Active A x}
  let B : Matrix W W ℚ := A.submatrix Subtype.val Subtype.val
  have hb : B.IsAdjMatrix :=
    ⟨fun x y => hA.zero_or_one x y,
      by ext x y; exact hA.symm.apply x y,
      fun x => hA.apply_diag x⟩
  have hrb : B.rank ≤ 3 := (Matrix.rank_submatrix_le A _ _).trans hr
  have h2b : Matrix.trace (B * B) = 718 := (active_square_moment A hA).trans h2
  have hta (i : Fin 3) : Active A (t i) := by
    change ∀ i j, A (t i) (t j) = if i = j then 0 else 1 at ht
    fin_cases i
    · exact ⟨t 1, by simpa using ht 0 1⟩
    · exact ⟨t 0, by simpa using ht 1 0⟩
    · exact ⟨t 0, by simpa using ht 2 0⟩
  let tb : Fin 3 → W := fun i => ⟨t i, hta i⟩
  have htb : IsTriangle B tb := ht
  have hn : ∀ x : W, ∃ y : W, B x y = 1 := by
    intro x
    obtain ⟨y, hy⟩ := x.property
    exact ⟨⟨y, x, by rw [hA.symm.apply x y]; exact hy⟩, hy⟩
  obtain ⟨z, _, hz⟩ := rank_three_recognizes_tripartite B hb hrb tb htb hn
  have hm := trace_square_reads_edges B z hz
  rw [h2b] at hm
  have he : fibreSize z 0 * fibreSize z 1 + fibreSize z 0 * fibreSize z 2 +
      fibreSize z 1 * fibreSize z 2 = 359 := by
    exact_mod_cast (show (fibreSize z 0 : ℚ) * fibreSize z 1 +
      fibreSize z 0 * fibreSize z 2 + fibreSize z 1 * fibreSize z 2 = 359 by linarith)
  intro x
  by_contra hx
  have hlt := Fintype.card_subtype_lt hx
  change Fintype.card W < Fintype.card V at hlt
  have hsz := part_sizes_sum z
  have hsum : fibreSize z 0 + fibreSize z 1 + fibreSize z 2 ≤ 32 := by omega
  have sqbound := Nat.mul_self_le_mul_self hsum
  have ab := sq_nonneg ((fibreSize z 0 : ℤ) - fibreSize z 1)
  have ac := sq_nonneg ((fibreSize z 0 : ℤ) - fibreSize z 2)
  have bc := sq_nonneg ((fibreSize z 1 : ℤ) - fibreSize z 2)
  zify at he sqbound
  nlinarith

/-- The scene and cubic moment follow from only three operator readings. -/
theorem dense_operator_recovers_scene (A : Matrix V V ℚ) (hA : A.IsAdjMatrix)
    (hr : A.rank ≤ 3) (hV : Fintype.card V = 33)
    (h2 : Matrix.trace (A * A) = 718) :
    ∃ z : V → Fin 3, Function.Surjective z ∧
      (∀ x y, A x y = if z x = z y then 0 else 1) ∧
      ({fibreSize z 0, fibreSize z 1, fibreSize z 2} : Multiset ℕ) = {9, 11, 13} ∧
      (∀ x y, z x = z y ↔ A x = A y) ∧
      Matrix.trace (A * A * A) = 7722 := by
  obtain ⟨t, ht⟩ := dense_passport_triangle A hA hV h2
  obtain ⟨z, hs, hz, hm, hi⟩ := operator_passport_recovers_scene A hA hr t ht
    (dense_passport_no_isolates A hA hr hV h2) hV h2
  refine ⟨z, hs, hz, hm, hi, ?_⟩
  have hp := congrArg Multiset.prod hm
  norm_num at hp
  rw [trace_cube_reads_triangles A z hz]
  have hpq : (fibreSize z 0 : ℚ) * fibreSize z 1 * fibreSize z 2 = 1287 := by
    exact_mod_cast (show fibreSize z 0 * fibreSize z 1 * fibreSize z 2 = 1287 by
      simpa only [mul_assoc] using hp)
  rw [hpq]
  norm_num

/-- A concrete graph isomorphism, not just a list of recovered cardinalities. -/
noncomputable def recoveredGraphIso (A : Matrix V V ℚ) (hA : A.IsAdjMatrix)
    (z : V → Fin 3) (hz : ∀ x y, A x y = if z x = z y then 0 else 1) :
    hA.toGraph ≃g SimpleGraph.completeMultipartiteGraph (fun i => Fin (fibreSize z i)) := by
  classical
  let e : V ≃ Σ i : Fin 3, Fin (fibreSize z i) :=
    (Equiv.sigmaFiberEquiv z).symm.trans
      (Equiv.sigmaCongrRight (fun i => Fintype.equivFin {x // z x = i}))
  refine { e with map_rel_iff' := ?_ }
  intro x y
  change z x ≠ z y ↔ A x y = 1
  rw [hz]
  by_cases h : z x = z y <;> simp [h]

/-- The concrete D0 adjacency satisfies the input passport in the Lean kernel. -/
theorem scene_passport_inhabited :
    D0.Claims.Adj31.IsAdjMatrix ∧ D0.Claims.Adj31.rank ≤ 3 ∧
      Fintype.card (Fin 33) = 33 ∧
      Matrix.trace (D0.Claims.Adj31 * D0.Claims.Adj31) = 718 := by
  have ha : D0.Claims.Adj31.IsAdjMatrix := by
    refine ⟨?_, ?_, ?_⟩
    · intro x y; unfold D0.Claims.Adj31; dsimp only [Matrix.of_apply]
      split <;> simp
    · ext x y
      simp only [D0.Claims.Adj31, Matrix.transpose_apply, Matrix.of_apply]
      by_cases h : D0.Claims.zone31 x = D0.Claims.zone31 y
      · simp [h]
      · simp [h, Ne.symm h]
    · intro x; simp [D0.Claims.Adj31]
  refine ⟨ha, D0.Claims.adj31_rank_le_three, Fintype.card_fin _, ?_⟩
  have hs : ∀ i : Fin 3, fibreSize D0.Claims.zone31 i = ![9,11,13] i := by decide
  rw [trace_square_reads_edges D0.Claims.Adj31 D0.Claims.zone31 (fun _ _ => rfl)]
  rw [hs 0, hs 1, hs 2]
  change 2 * ((9 : ℚ) * 11 + 9 * 13 + 11 * 13) = 718
  norm_num

end D0.Synthesis.DenseOperatorSceneRigidity
