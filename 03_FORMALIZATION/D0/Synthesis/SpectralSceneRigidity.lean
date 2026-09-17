import D0.Synthesis.OperatorSceneReconstruction

/-!
# An operator-only recognition passport for the D0 graph

For an arbitrary finite simple adjacency matrix, the four readings
`|V| = 33`, `rank A ≤ 3`, `Tr(A²) = 718`, `Tr(A³) = 7722`
force the graph to be `K(9,11,13)` up to relabelling. Neither a partition,
a triangle, connectedness nor absence of isolated vertices is assumed.

The third moment supplies a triangle. Restriction to the nonisolated support
preserves both moments; rank-three recognition yields the three parts there.
The existing edge/triangle inverse theorem forces their sizes to be 9,11,13.
Those already use all 33 vertices, excluding any isolated remainder.
-/

namespace D0.Synthesis.SpectralSceneRigidity

open Matrix
open D0.Combinatorics.RankThreeRecognition
open D0.Synthesis.OperatorSceneReconstruction
open D0.Synthesis.SceneInvariantReconstruction
open scoped Classical

variable {V : Type*} [Fintype V]

theorem trace_cube_expansion (A : Matrix V V ℚ) :
    Matrix.trace (A * A * A) = ∑ x, ∑ y, ∑ z, A x y * A y z * A z x := by
  rw [Matrix.mul_assoc]
  simp only [Matrix.trace, Matrix.diag, Matrix.mul_apply, Finset.mul_sum, mul_assoc]

theorem triangle_of_nonzero_third_moment (A : Matrix V V ℚ) (hA : A.IsAdjMatrix)
    (h : Matrix.trace (A * A * A) ≠ 0) : ∃ t : Fin 3 → V, IsTriangle A t := by
  rw [trace_cube_expansion] at h
  obtain ⟨x, _, hx⟩ := Finset.exists_ne_zero_of_sum_ne_zero h
  obtain ⟨y, _, hy⟩ := Finset.exists_ne_zero_of_sum_ne_zero hx
  obtain ⟨z, _, hz⟩ := Finset.exists_ne_zero_of_sum_ne_zero hy
  have hxy : A x y = 1 := (hA.zero_or_one x y).resolve_left (by
    intro hh; simp [hh] at hz)
  have hyz : A y z = 1 := (hA.zero_or_one y z).resolve_left (by
    intro hh; simp [hh] at hz)
  have hzx : A z x = 1 := (hA.zero_or_one z x).resolve_left (by
    intro hh; simp [hh] at hz)
  have hyx : A y x = 1 := by rw [hA.symm.apply x y]; exact hxy
  have hzy : A z y = 1 := by rw [hA.symm.apply y z]; exact hyz
  have hxz : A x z = 1 := by rw [hA.symm.apply z x]; exact hzx
  refine ⟨![x,y,z], ?_⟩
  intro i j
  fin_cases i <;> fin_cases j <;>
    simp [hA.apply_diag, hxy, hyz, hzx, hyx, hzy, hxz]

/-- The third operator moment counts six oriented traversals per triangle. -/
theorem trace_cube_reads_triangles (A : Matrix V V ℚ) (z : V → Fin 3)
    (hz : ∀ x y, A x y = if z x = z y then 0 else 1) :
    Matrix.trace (A * A * A) =
      6 * ((fibreSize z 0 : ℚ) * fibreSize z 1 * fibreSize z 2) := by
  classical
  let p (i j : Fin 3) : ℚ := if i = j then 0 else 1
  have sum3 (f : Fin 3 → ℚ) : (∑ i, f i) = f 0 + f 1 + f 2 := by
    simp only [Fin.sum_univ_succ]
    change f 0 + (f 1 + (f 2 + 0)) = _
    ring
  have algebra (n : Fin 3 → ℚ) :
      (∑ i, n i * (∑ j, n j * (∑ k, n k * (p i j * p j k * p k i)))) =
        6 * (n 0 * n 1 * n 2) := by
    simp only [sum3,
      show p 0 0 = 0 from rfl, show p 0 1 = 1 from rfl, show p 0 2 = 1 from rfl,
      show p 1 0 = 1 from rfl, show p 1 1 = 0 from rfl, show p 1 2 = 1 from rfl,
      show p 2 0 = 1 from rfl, show p 2 1 = 1 from rfl, show p 2 2 = 0 from rfl,
      mul_zero, zero_mul, mul_one, add_zero, zero_add]
    ring
  rw [trace_cube_expansion]
  simp only [hz]
  change (∑ x, ∑ y, ∑ w, p (z x) (z y) * p (z y) (z w) * p (z w) (z x)) = _
  calc
    _ = ∑ x, ∑ y, ∑ k, (fibreSize z k : ℚ) *
        (p (z x) (z y) * p (z y) k * p k (z x)) := by
      apply Finset.sum_congr rfl; intro x _
      apply Finset.sum_congr rfl; intro y _
      exact sum_by_parts z (fun k => p (z x) (z y) * p (z y) k * p k (z x))
    _ = ∑ x, ∑ j, (fibreSize z j : ℚ) *
        (∑ k, (fibreSize z k : ℚ) * (p (z x) j * p j k * p k (z x))) := by
      apply Finset.sum_congr rfl; intro x _
      exact sum_by_parts z (fun j => ∑ k, (fibreSize z k : ℚ) *
        (p (z x) j * p j k * p k (z x)))
    _ = ∑ i, (fibreSize z i : ℚ) * (∑ j, (fibreSize z j : ℚ) *
        (∑ k, (fibreSize z k : ℚ) * (p i j * p j k * p k i))) :=
      sum_by_parts z (fun i => ∑ j, (fibreSize z j : ℚ) *
        (∑ k, (fibreSize z k : ℚ) * (p i j * p j k * p k i)))
    _ = _ := algebra (fun i => (fibreSize z i : ℚ))

def Active (A : Matrix V V ℚ) (x : V) : Prop := ∃ y, A x y = 1

omit [Fintype V] in
theorem inactive_row_zero (A : Matrix V V ℚ) (hA : A.IsAdjMatrix)
    {x : V} (hx : ¬ Active A x) (y : V) : A x y = 0 :=
  (hA.zero_or_one x y).resolve_right (fun h => hx ⟨y,h⟩)

theorem sum_supported (p : V → Prop) [DecidablePred p] (f : V → ℚ)
    (hf : ∀ x, ¬ p x → f x = 0) : (∑ x : {x // p x}, f x) = ∑ x, f x := by
  apply Fintype.sum_of_injective (fun x : {x // p x} => (x : V))
    Subtype.val_injective
  · intro x hx
    apply hf x
    simpa only [Subtype.range_coe_subtype, Set.mem_setOf_eq] using hx
  · intro x; rfl

theorem active_square_moment (A : Matrix V V ℚ) (hA : A.IsAdjMatrix) :
    let B := A.submatrix (fun x : {x // Active A x} => (x : V))
      (fun x : {x // Active A x} => (x : V))
    Matrix.trace (B * B) = Matrix.trace (A * A) := by
  classical
  dsimp only
  simp only [Matrix.trace, Matrix.diag, Matrix.mul_apply, Matrix.submatrix_apply]
  calc
    _ = ∑ x : {x // Active A x}, ∑ y : V, A x y * A y x := by
      apply Finset.sum_congr rfl; intro x _
      exact sum_supported (Active A) (fun y => A x y * A y x) (by
        intro y hy; dsimp only; rw [inactive_row_zero A hA hy]; simp)
    _ = _ := sum_supported (Active A) (fun x => ∑ y, A x y * A y x) (by
      intro x hx
      apply Finset.sum_eq_zero; intro y _
      rw [inactive_row_zero A hA hx]; simp)

theorem active_cube_moment (A : Matrix V V ℚ) (hA : A.IsAdjMatrix) :
    let B := A.submatrix (fun x : {x // Active A x} => (x : V))
      (fun x : {x // Active A x} => (x : V))
    Matrix.trace (B * B * B) = Matrix.trace (A * A * A) := by
  classical
  dsimp only
  simp only [trace_cube_expansion, Matrix.submatrix_apply]
  calc
    _ = ∑ x : {x // Active A x}, ∑ y : {y // Active A y},
        ∑ z : V, A x y * A y z * A z x := by
      apply Finset.sum_congr rfl; intro x _
      apply Finset.sum_congr rfl; intro y _
      exact sum_supported (Active A) (fun z => A x y * A y z * A z x) (by
        intro z hz; dsimp only; rw [inactive_row_zero A hA hz]; simp)
    _ = ∑ x : {x // Active A x}, ∑ y : V, ∑ z : V, A x y * A y z * A z x := by
      apply Finset.sum_congr rfl; intro x _
      exact sum_supported (Active A) (fun y => ∑ z, A x y * A y z * A z x) (by
        intro y hy
        apply Finset.sum_eq_zero; intro z _
        rw [inactive_row_zero A hA hy]; simp)
    _ = _ := sum_supported (Active A) (fun x => ∑ y, ∑ z, A x y * A y z * A z x) (by
      intro x hx
      apply Finset.sum_eq_zero; intro y _
      apply Finset.sum_eq_zero; intro z _
      rw [inactive_row_zero A hA hx]; simp)

theorem unordered_sizes_from_edge_triangle (a b c : ℕ)
    (ha : 0 < a) (hb : 0 < b) (hc : 0 < c)
    (hE : a*b + a*c + b*c = 359) (hT : a*b*c = 1287) :
    ({a, b, c} : Multiset ℕ) = {9, 11, 13} := by
  have key (x y z : ℕ) (hx : 0 < x) (hxy : x ≤ y) (hyz : y ≤ z)
      (he : x*y + x*z + y*z = 359) (ht : x*y*z = 1287) :
      x = 9 ∧ y = 11 ∧ z = 13 := by
    have h := reconstruct_from_edges_triangles x y z hx hxy hyz he ht
    simpa only [Prod.mk.injEq, and_assoc] using h
  rcases le_total a b with hab | hba
  · rcases le_total b c with hbc | hcb
    · obtain ⟨rfl,rfl,rfl⟩ := key a b c ha hab hbc hE hT; rfl
    · rcases le_total a c with hac | hca
      · obtain ⟨rfl,rfl,rfl⟩ := key a c b ha hac hcb (by nlinarith) (by nlinarith); decide
      · obtain ⟨rfl,rfl,rfl⟩ := key c a b hc hca hab (by nlinarith) (by nlinarith); decide
  · rcases le_total a c with hac | hca
    · obtain ⟨rfl,rfl,rfl⟩ := key b a c hb hba hac (by nlinarith) (by nlinarith); decide
    · rcases le_total b c with hbc | hcb
      · obtain ⟨rfl,rfl,rfl⟩ := key b c a hb hbc hca (by nlinarith) (by nlinarith); decide
      · obtain ⟨rfl,rfl,rfl⟩ := key c b a hc hcb hba (by nlinarith) (by nlinarith); decide

/-- The moments leave no room for an isolated component on a 33-vertex carrier. -/
theorem spectral_passport_no_isolates (A : Matrix V V ℚ) (hA : A.IsAdjMatrix)
    (hr : A.rank ≤ 3) (hV : Fintype.card V = 33)
    (h2 : Matrix.trace (A * A) = 718) (h3 : Matrix.trace (A * A * A) = 7722) :
    ∀ x, Active A x := by
  classical
  let W := {x // Active A x}
  let B : Matrix W W ℚ := A.submatrix Subtype.val Subtype.val
  have hb : B.IsAdjMatrix :=
    ⟨fun x y => hA.zero_or_one x y,
      by ext x y; exact hA.symm.apply x y,
      fun x => hA.apply_diag x⟩
  have hrb : B.rank ≤ 3 := (Matrix.rank_submatrix_le A _ _).trans hr
  have h2b : Matrix.trace (B * B) = 718 := (active_square_moment A hA).trans h2
  have h3b : Matrix.trace (B * B * B) = 7722 := (active_cube_moment A hA).trans h3
  obtain ⟨t, ht⟩ := triangle_of_nonzero_third_moment B hb (by rw [h3b]; norm_num)
  have hn : ∀ x : W, ∃ y : W, B x y = 1 := by
    intro x
    obtain ⟨y, hy⟩ := x.property
    exact ⟨⟨y, x, by rw [hA.symm.apply x y]; exact hy⟩, hy⟩
  obtain ⟨z, hs, hz⟩ := rank_three_recognizes_tripartite B hb hrb t ht hn
  have hm2 := trace_square_reads_edges B z hz
  have hm3 := trace_cube_reads_triangles B z hz
  rw [h2b] at hm2
  rw [h3b] at hm3
  have he : fibreSize z 0 * fibreSize z 1 + fibreSize z 0 * fibreSize z 2 +
      fibreSize z 1 * fibreSize z 2 = 359 := by
    have hq : (fibreSize z 0 : ℚ) * fibreSize z 1 + fibreSize z 0 * fibreSize z 2 +
      fibreSize z 1 * fibreSize z 2 = 359 := by linarith
    exact_mod_cast hq
  have ht' : fibreSize z 0 * fibreSize z 1 * fibreSize z 2 = 1287 := by
    have hq : (fibreSize z 0 : ℚ) * fibreSize z 1 * fibreSize z 2 = 1287 := by linarith
    exact_mod_cast hq
  have hm := unordered_sizes_from_edge_triangle _ _ _
    (part_sizes_positive z hs 0) (part_sizes_positive z hs 1)
    (part_sizes_positive z hs 2) he ht'
  have hsum := congrArg Multiset.sum hm
  have hw : Fintype.card W = 33 := by
    have hsz := part_sizes_sum z
    norm_num at hsum
    omega
  intro x
  by_contra hx
  have hlt := Fintype.card_subtype_lt hx
  change Fintype.card W < Fintype.card V at hlt
  omega

/-- Four operator readings recover the full scene among arbitrary finite simple graphs. -/
theorem spectral_passport_recovers_scene (A : Matrix V V ℚ) (hA : A.IsAdjMatrix)
    (hr : A.rank ≤ 3) (hV : Fintype.card V = 33)
    (h2 : Matrix.trace (A * A) = 718) (h3 : Matrix.trace (A * A * A) = 7722) :
    ∃ z : V → Fin 3, Function.Surjective z ∧
      (∀ x y, A x y = if z x = z y then 0 else 1) ∧
      ({fibreSize z 0, fibreSize z 1, fibreSize z 2} : Multiset ℕ) = {9, 11, 13} ∧
      (∀ x y, z x = z y ↔ A x = A y) := by
  obtain ⟨t, ht⟩ := triangle_of_nonzero_third_moment A hA (by rw [h3]; norm_num)
  exact operator_passport_recovers_scene A hA hr t ht
    (spectral_passport_no_isolates A hA hr hV h2 h3) hV h2

end D0.Synthesis.SpectralSceneRigidity
