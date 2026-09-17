import D0.Combinatorics.RankThreeRecognition
import D0.Synthesis.SceneInvariantReconstruction

/-!
# From an unpartitioned operator to the D0 scene

The inputs are an arbitrary finite simple adjacency matrix, a rank bound,
a triangle, absence of isolated vertices, the vertex count, and the second
operator moment. A complete tripartite partition is first *derived* from the
matrix; its sizes are then recovered from the counts by the existing D0
inverse theorem. The partition is intrinsic: two vertices lie in the same
part exactly when their adjacency rows coincide.

This is recognition of a supplied finite operator, not a derivation of rank
three or of the numerical passport from the primitive verification contract.
-/

namespace D0.Synthesis.OperatorSceneReconstruction

open Matrix
open D0.Combinatorics.RankThreeRecognition
open D0.Synthesis.SceneInvariantReconstruction

variable {V : Type*} [Fintype V]

/-- Actual cardinality of a recovered fibre, rather than an assigned mass. -/
def fibreSize (z : V → Fin 3) (i : Fin 3) : ℕ := Fintype.card {x // z x = i}

theorem sum_by_parts (z : V → Fin 3) (f : Fin 3 → ℚ) :
    (∑ x, f (z x)) = ∑ i, (fibreSize z i : ℚ) * f i := by
  rw [← Fintype.sum_fiberwise' z f]
  simp [fibreSize]

theorem part_sizes_sum (z : V → Fin 3) :
    fibreSize z 0 + fibreSize z 1 + fibreSize z 2 = Fintype.card V := by
  have h := sum_by_parts z (fun _ => 1)
  simp only [Finset.sum_const, Finset.card_univ, nsmul_eq_mul, mul_one,
    Fin.sum_univ_succ, Finset.univ_eq_empty, Finset.sum_empty, add_zero] at h
  have h' : ((fibreSize z 0 : ℚ) + fibreSize z 1 + fibreSize z 2) = Fintype.card V := by
    simpa only [add_assoc] using h.symm
  exact_mod_cast h'

theorem part_sizes_positive (z : V → Fin 3) (hz : Function.Surjective z)
    (i : Fin 3) : 0 < fibreSize z i := by
  obtain ⟨x, hx⟩ := hz i
  exact Fintype.card_pos_iff.mpr ⟨⟨x, hx⟩⟩

/-- The actual second moment reads twice the number of cross-part pairs. -/
theorem trace_square_reads_edges (A : Matrix V V ℚ) (z : V → Fin 3)
    (hz : ∀ x y, A x y = if z x = z y then 0 else 1) :
    Matrix.trace (A * A) = 2 *
      ((fibreSize z 0 : ℚ) * fibreSize z 1 + fibreSize z 0 * fibreSize z 2 +
        fibreSize z 1 * fibreSize z 2) := by
  classical
  have he (i j : Fin 3) :
      (if i = j then (0 : ℚ) else 1) * (if j = i then 0 else 1) =
        if i = j then 0 else 1 := by
    by_cases h : i = j
    · simp [h]
    · simp [h, Ne.symm h]
  have algebra (n : Fin 3 → ℚ) :
      (∑ i, n i * (∑ j, n j * (if i = j then 0 else 1))) =
        2 * (n 0 * n 1 + n 0 * n 2 + n 1 * n 2) := by
    simp only [Fin.sum_univ_succ]
    change n 0 * (n 0 * 0 + (n 1 * 1 + (n 2 * 1 + 0))) +
      (n 1 * (n 0 * 1 + (n 1 * 0 + (n 2 * 1 + 0))) +
      (n 2 * (n 0 * 1 + (n 1 * 1 + (n 2 * 0 + 0))) + 0)) = _
    ring
  calc
    Matrix.trace (A * A) = ∑ x, ∑ y, if z x = z y then (0 : ℚ) else 1 := by
      simp only [Matrix.trace, Matrix.diag, Matrix.mul_apply, hz, he]
    _ = ∑ x, ∑ j, (fibreSize z j : ℚ) * (if z x = j then 0 else 1) := by
      apply Finset.sum_congr rfl
      intro x _
      exact sum_by_parts z (fun j => if z x = j then (0 : ℚ) else 1)
    _ = ∑ i, (fibreSize z i : ℚ) *
        (∑ j, (fibreSize z j : ℚ) * (if i = j then 0 else 1)) :=
      sum_by_parts z (fun i => ∑ j, (fibreSize z j : ℚ) * (if i = j then 0 else 1))
    _ = _ := algebra (fun i => (fibreSize z i : ℚ))

/-- The old ordered arithmetic inverse theorem, now without chosen part labels. -/
theorem unordered_sizes_from_vertex_edge (a b c : ℕ)
    (ha : 0 < a) (hb : 0 < b) (hc : 0 < c)
    (hV : a + b + c = 33) (hE : a * b + a * c + b * c = 359) :
    ({a, b, c} : Multiset ℕ) = {9, 11, 13} := by
  have key (x y z : ℕ) (hx : 0 < x) (hxy : x ≤ y) (hyz : y ≤ z)
      (hv : x + y + z = 33) (he : x*y + x*z + y*z = 359) :
      x = 9 ∧ y = 11 ∧ z = 13 := by
    have h := reconstruct_from_vertices_edges x y z hx hxy hyz hv he
    simpa only [Prod.mk.injEq, and_assoc] using h
  rcases le_total a b with hab | hba
  · rcases le_total b c with hbc | hcb
    · obtain ⟨rfl, rfl, rfl⟩ := key a b c ha hab hbc hV hE
      rfl
    · rcases le_total a c with hac | hca
      · obtain ⟨rfl, rfl, rfl⟩ := key a c b ha hac hcb (by omega) (by nlinarith)
        decide
      · obtain ⟨rfl, rfl, rfl⟩ := key c a b hc hca hab (by omega) (by nlinarith)
        decide
  · rcases le_total a c with hac | hca
    · obtain ⟨rfl, rfl, rfl⟩ := key b a c hb hba hac (by omega) (by nlinarith)
      decide
    · rcases le_total b c with hbc | hcb
      · obtain ⟨rfl, rfl, rfl⟩ := key b c a hb hbc hca (by omega) (by nlinarith)
        decide
      · obtain ⟨rfl, rfl, rfl⟩ := key c b a hc hcb hba (by omega) (by nlinarith)
        decide

omit [Fintype V] in
/-- Equal adjacency rows are the intrinsic parts of any complete tripartite graph. -/
theorem same_part_iff_same_row (A : Matrix V V ℚ) (z : V → Fin 3)
    (hz : ∀ x y, A x y = if z x = z y then 0 else 1) (x y : V) :
    z x = z y ↔ A x = A y := by
  constructor
  · intro h
    funext v
    simp only [hz, h]
  · intro h
    have hxy := congrFun h y
    rw [hz x y, hz y y] at hxy
    by_contra hne
    simp [hne] at hxy

/-- An arbitrary unpartitioned graph with this operator passport is `K(9,11,13)`
up to vertex and part relabelling. The output contains the full adjacency law. -/
theorem operator_passport_recovers_scene (A : Matrix V V ℚ) (hA : A.IsAdjMatrix)
    (hr : A.rank ≤ 3) (t : Fin 3 → V) (ht : IsTriangle A t)
    (hn : ∀ x, ∃ y, A x y = 1) (hV : Fintype.card V = 33)
    (hM : Matrix.trace (A * A) = 718) :
    ∃ z : V → Fin 3, Function.Surjective z ∧
      (∀ x y, A x y = if z x = z y then 0 else 1) ∧
      ({fibreSize z 0, fibreSize z 1, fibreSize z 2} : Multiset ℕ) = {9, 11, 13} ∧
      (∀ x y, z x = z y ↔ A x = A y) := by
  obtain ⟨z, hs, hz⟩ := rank_three_recognizes_tripartite A hA hr t ht hn
  refine ⟨z, hs, hz, ?_, same_part_iff_same_row A z hz⟩
  have hv := part_sizes_sum z
  rw [hV] at hv
  have hm := trace_square_reads_edges A z hz
  rw [hM] at hm
  have he : fibreSize z 0 * fibreSize z 1 + fibreSize z 0 * fibreSize z 2 +
      fibreSize z 1 * fibreSize z 2 = 359 := by
    have hq : (fibreSize z 0 : ℚ) * fibreSize z 1 + fibreSize z 0 * fibreSize z 2 +
        fibreSize z 1 * fibreSize z 2 = 359 := by linarith
    exact_mod_cast hq
  exact unordered_sizes_from_vertex_edge _ _ _
    (part_sizes_positive z hs 0) (part_sizes_positive z hs 1)
    (part_sizes_positive z hs 2) hv he

end D0.Synthesis.OperatorSceneReconstruction
