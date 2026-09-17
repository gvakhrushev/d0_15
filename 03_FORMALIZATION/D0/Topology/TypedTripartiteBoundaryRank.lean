import D0.SelfReading.TypedIncidenceCarriers
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Tactic

/-!
# D0-TYPED-TRIPARTITE-BOUNDARY-RANK-001

An explicit rational chain complex for the canonical finite scene
`K(9,11,13)`:

```
C₂ --∂₂--> C₁ --∂₁--> C₀.
```

The carrier types are the canonical finite representatives
`Fin 9`, `Fin 11`, `Fin 13`; the incidence carriers are exactly the generic
typed `TripartiteEdge` and `TripartiteTriangle` types.  The module proves:

* `∂₁∂₂ = 0`;
* `rank ∂₁ = 32`;
* `rank ∂₂ = 327`.

The lower bound for `rank ∂₂` uses an explicit `327×327` minor indexed by the
non-tree edges of a fixed spanning tree.  An explicit inverse-on-vectors proves
that minor surjective.  The upper bound then follows from
`rank ∂₁ + rank ∂₂ ≤ |C₁|`.
-/

namespace D0.Topology.TypedTripartiteBoundaryRank

open scoped BigOperators
open Matrix
open D0.SelfReading.TypedIncidenceCarriers

abbrev A := Fin 9
abbrev B := Fin 11
abbrev C := Fin 13

abbrev Vertex := A ⊕ (B ⊕ C)
abbrev Edge := TripartiteEdge A B C
abbrev Triangle := TripartiteTriangle A B C

instance : DecidableEq Vertex := inferInstance
instance : DecidableEq Edge := inferInstance
instance : DecidableEq Triangle := inferInstance

/-- Oriented vertex-edge boundary, with every edge oriented in increasing
zone order. -/
def boundary1 : Matrix Vertex Edge ℚ
  | Sum.inl a, Sum.inl (a', _) => if a = a' then -1 else 0
  | Sum.inl a, Sum.inr (Sum.inl (a', _)) => if a = a' then -1 else 0
  | Sum.inl _, Sum.inr (Sum.inr _) => 0
  | Sum.inr (Sum.inl b), Sum.inl (_, b') => if b = b' then 1 else 0
  | Sum.inr (Sum.inl _), Sum.inr (Sum.inl _) => 0
  | Sum.inr (Sum.inl b), Sum.inr (Sum.inr (b', _)) =>
      if b = b' then -1 else 0
  | Sum.inr (Sum.inr _), Sum.inl _ => 0
  | Sum.inr (Sum.inr c), Sum.inr (Sum.inl (_, c')) =>
      if c = c' then 1 else 0
  | Sum.inr (Sum.inr c), Sum.inr (Sum.inr (_, c')) =>
      if c = c' then 1 else 0

/-- Oriented edge-triangle boundary:
`∂[a,b,c] = [b,c] - [a,c] + [a,b]`. -/
def boundary2 : Matrix Edge Triangle ℚ
  | Sum.inl (a, b), (a', b', _) =>
      if a = a' ∧ b = b' then 1 else 0
  | Sum.inr (Sum.inl (a, c)), (a', _, c') =>
      if a = a' ∧ c = c' then -1 else 0
  | Sum.inr (Sum.inr (b, c)), (_, b', c') =>
      if b = b' ∧ c = c' then 1 else 0

/-! ## Boundary squared zero -/

private lemma sum_prod_indicator_pair
    {α β : Type} [Fintype α] [Fintype β]
    [DecidableEq α] [DecidableEq β]
    (a a' : α) (b' : β) (u v : ℚ) :
    (∑ p : α × β,
      (if a = p.1 then u else 0) *
        (if p.1 = a' ∧ p.2 = b' then v else 0)) =
      if a = a' then u * v else 0 := by
  by_cases h : a = a'
  · subst a'
    rw [Fintype.sum_prod_type]
    calc
      (∑ x : α, ∑ y : β,
        (if a = x then u else 0) *
          (if x = a ∧ y = b' then v else 0)) =
        ∑ x : α, if a = x then u * v else 0 := by
          apply Fintype.sum_congr
          intro x
          by_cases hx : a = x
          · subst x
            simp only [if_true, true_and, mul_ite, mul_zero]
            simpa using congrArg (fun z : ℚ => u * z)
              (Fintype.sum_ite_eq' b' (fun _ : β => v))
          · simp [hx]
      _ = u * v := Fintype.sum_ite_eq a (fun _ : α => u * v)
      _ = if a = a then u * v else 0 := by simp
  · simp only [h, if_false]
    apply Finset.sum_eq_zero
    intro p _
    by_cases ha : a = p.1
    · by_cases hp : p.1 = a' ∧ p.2 = b'
      · exact (h (ha.trans hp.1)).elim
      · simp [hp]
    · simp [ha]

private lemma sum_prod_indicator_pair_snd
    {α β : Type} [Fintype α] [Fintype β]
    [DecidableEq α] [DecidableEq β]
    (b b' : β) (a' : α) (u v : ℚ) :
    (∑ p : α × β,
      (if b = p.2 then u else 0) *
        (if p.1 = a' ∧ p.2 = b' then v else 0)) =
      if b = b' then u * v else 0 := by
  rw [Fintype.sum_prod_type]
  by_cases h : b = b'
  · subst b'
    calc
      (∑ x : α, ∑ y : β,
        (if b = y then u else 0) *
          (if x = a' ∧ y = b then v else 0)) =
        ∑ x : α, if x = a' then u * v else 0 := by
          apply Fintype.sum_congr
          intro x
          by_cases hx : x = a'
          · subst x
            simp only [if_true, true_and, mul_ite, mul_zero]
            simpa using congrArg (fun z : ℚ => u * z)
              (Fintype.sum_ite_eq b (fun _ : β => v))
          · simp [hx]
      _ = u * v := Fintype.sum_ite_eq' a' (fun _ : α => u * v)
      _ = if b = b then u * v else 0 := by simp
  · simp only [h, if_false]
    apply Fintype.sum_eq_zero
    intro x
    apply Fintype.sum_eq_zero
    intro y
    by_cases hb : b = y
    · by_cases hp : x = a' ∧ y = b'
      · exact (h (hb.trans hp.2)).elim
      · simp [hp]
    · simp [hb]

/-- The oriented typed incidence maps form a chain complex. -/
theorem boundary_squared_zero : boundary1 * boundary2 = 0 := by
  ext v t
  rcases t with ⟨a', b', c'⟩
  rcases v with a | v
  · simp only [Matrix.mul_apply, boundary1, boundary2,
      Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
      add_zero, zero_add, Matrix.zero_apply]
    rw [sum_prod_indicator_pair a a' b' (-1) 1]
    rw [sum_prod_indicator_pair a a' c' (-1) (-1)]
    by_cases h : a = a' <;> simp [h]
  · rcases v with b | c
    · simp only [Matrix.mul_apply, boundary1, boundary2,
        Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
        add_zero, zero_add, Matrix.zero_apply]
      rw [sum_prod_indicator_pair_snd b b' a' 1 1]
      rw [sum_prod_indicator_pair b b' c' (-1) 1]
      by_cases h : b = b' <;> simp [h]
    · simp only [Matrix.mul_apply, boundary1, boundary2,
        Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
        add_zero, zero_add, Matrix.zero_apply]
      rw [sum_prod_indicator_pair_snd c c' a' 1 (-1)]
      rw [sum_prod_indicator_pair_snd c c' b' 1 1]
      by_cases h : c = c' <;> simp [h]

/-! ## Rank of `∂₁` -/

private def ones : Vertex → ℚ := fun _ => 1

private lemma sum_ite_one
    {α : Type} [Fintype α] [DecidableEq α] (a : α) :
    (∑ x : α, if x = a then (1 : ℚ) else 0) = 1 := by
  simpa using Fintype.sum_ite_eq' a (fun _ : α => (1 : ℚ))

private lemma sum_ite_neg_one
    {α : Type} [Fintype α] [DecidableEq α] (a : α) :
    (∑ x : α, if x = a then (-1 : ℚ) else 0) = -1 := by
  simpa using Fintype.sum_ite_eq' a (fun _ : α => (-1 : ℚ))

private lemma boundary1_transpose_ones :
    boundary1.transpose.mulVec ones = 0 := by
  funext e
  rcases e with e | e
  · rcases e with ⟨a, b⟩
    simp only [Matrix.mulVec, dotProduct, transpose_apply, boundary1,
      ones, Fintype.sum_sum_type, mul_one, Finset.sum_const_zero,
      add_zero, zero_add]
    rw [sum_ite_neg_one, sum_ite_one]
    norm_num
  · rcases e with e | e
    · rcases e with ⟨a, c⟩
      simp only [Matrix.mulVec, dotProduct, transpose_apply, boundary1,
        ones, Fintype.sum_sum_type, mul_one, Finset.sum_const_zero,
        add_zero, zero_add]
      rw [sum_ite_neg_one, sum_ite_one]
      norm_num
    · rcases e with ⟨b, c⟩
      simp only [Matrix.mulVec, dotProduct, transpose_apply, boundary1,
        ones, Fintype.sum_sum_type, mul_one, Finset.sum_const_zero,
        add_zero, zero_add]
      rw [sum_ite_neg_one, sum_ite_one]
      norm_num

private lemma ones_ne_zero : ones ≠ 0 := by
  intro h
  have hx := congrFun h (Sum.inl (0 : A))
  norm_num [ones] at hx

private lemma boundary1_rank_le_32 : boundary1.rank ≤ 32 := by
  have hmem : ones ∈ LinearMap.ker boundary1.transpose.mulVecLin := by
    rw [LinearMap.mem_ker]
    exact boundary1_transpose_ones
  have hker : LinearMap.ker boundary1.transpose.mulVecLin ≠ ⊥ := by
    intro hbot
    have hmem' := hmem
    rw [hbot] at hmem'
    have hz : ones = 0 := by simpa using hmem'
    exact ones_ne_zero hz
  have hkerpos :
      1 ≤ Module.finrank ℚ
        (LinearMap.ker boundary1.transpose.mulVecLin) :=
    Submodule.one_le_finrank_iff.mpr hker
  have hrn :=
    LinearMap.finrank_range_add_finrank_ker
      boundary1.transpose.mulVecLin
  have hsum :
      boundary1.transpose.rank +
        Module.finrank ℚ
          (LinearMap.ker boundary1.transpose.mulVecLin) = 33 := by
    rw [Matrix.rank]
    calc
      Module.finrank ℚ
          (LinearMap.range boundary1.transpose.mulVecLin) +
          Module.finrank ℚ
            (LinearMap.ker boundary1.transpose.mulVecLin) =
          Module.finrank ℚ (Vertex → ℚ) := hrn
      _ = Fintype.card Vertex :=
        Module.finrank_fintype_fun_eq_card ℚ
      _ = 33 := by decide
  have htrans :
      boundary1.transpose.rank = boundary1.rank :=
    Matrix.rank_transpose boundary1
  omega

abbrev Tree := Fin 8 ⊕ (B ⊕ C)

instance : DecidableEq Tree := inferInstance
instance : Fintype Tree := inferInstance

private def tA (a : Fin 8) : Tree := Sum.inl a
private def tB (b : B) : Tree := Sum.inr (Sum.inl b)
private def tC (c : C) : Tree := Sum.inr (Sum.inr c)

private def nonRootVertex : Tree → Vertex
  | Sum.inl a => Sum.inl a.succ
  | Sum.inr (Sum.inl b) => Sum.inr (Sum.inl b)
  | Sum.inr (Sum.inr c) => Sum.inr (Sum.inr c)

private def treeEdge : Tree → Edge
  | Sum.inl a => Sum.inl (a.succ, 0)
  | Sum.inr (Sum.inl b) => Sum.inl (0, b)
  | Sum.inr (Sum.inr c) => Sum.inr (Sum.inl (0, c))

private def treeMinor : Matrix Tree Tree ℚ
  | Sum.inl a, Sum.inl a' => if a = a' then -1 else 0
  | Sum.inl _, _ => 0
  | Sum.inr (Sum.inl b), Sum.inl _ => if b = 0 then 1 else 0
  | Sum.inr (Sum.inl b), Sum.inr (Sum.inl b') =>
      if b = b' then 1 else 0
  | Sum.inr (Sum.inl _), Sum.inr (Sum.inr _) => 0
  | Sum.inr (Sum.inr c), Sum.inr (Sum.inr c') =>
      if c = c' then 1 else 0
  | Sum.inr (Sum.inr _), _ => 0

private lemma sum_indicator_one
    {α : Type} [Fintype α] [DecidableEq α]
    (f : α → ℚ) (a : α) :
    (∑ x : α, (if a = x then (1 : ℚ) else 0) * f x) =
      f a := by
  simp_rw [ite_mul, one_mul, zero_mul]
  exact Fintype.sum_ite_eq a f

private lemma sum_indicator_neg
    {α : Type} [Fintype α] [DecidableEq α]
    (f : α → ℚ) (a : α) :
    (∑ x : α, (if a = x then (-1 : ℚ) else 0) * f x) =
      -f a := by
  simp_rw [ite_mul, neg_one_mul, zero_mul]
  rw [Fintype.sum_ite_eq]

private lemma treeMinor_mulVec_A
    (x : Tree → ℚ) (a : Fin 8) :
    treeMinor.mulVec x (tA a) = -x (tA a) := by
  simp only [Matrix.mulVec, dotProduct, treeMinor, tA,
    Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
    add_zero, zero_add]
  exact sum_indicator_neg (fun a => x (Sum.inl a)) a

private lemma treeMinor_mulVec_B
    (x : Tree → ℚ) (b : B) :
    treeMinor.mulVec x (tB b) =
      x (tB b) +
        (if b = 0 then ∑ a : Fin 8, x (tA a) else 0) := by
  simp only [Matrix.mulVec, dotProduct, treeMinor, tA, tB,
    Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
    add_zero, zero_add]
  rw [sum_indicator_one]
  by_cases hb : b = 0
  · subst b
    simp
    ring
  · simp [hb]

private lemma treeMinor_mulVec_C
    (x : Tree → ℚ) (c : C) :
    treeMinor.mulVec x (tC c) = x (tC c) := by
  simp only [Matrix.mulVec, dotProduct, treeMinor, tC,
    Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
    add_zero, zero_add]
  exact sum_indicator_one
    (fun c => x (Sum.inr (Sum.inr c))) c

private def treeInverseVec (y : Tree → ℚ) : Tree → ℚ
  | Sum.inl a => -y (tA a)
  | Sum.inr (Sum.inl b) =>
      y (tB b) +
        (if b = 0 then ∑ a : Fin 8, y (tA a) else 0)
  | Sum.inr (Sum.inr c) => y (tC c)

private lemma treeInverseVec_right (y : Tree → ℚ) :
    treeMinor.mulVec (treeInverseVec y) = y := by
  funext r
  rcases r with a | r
  · change treeMinor.mulVec (treeInverseVec y) (tA a) = y (tA a)
    rw [treeMinor_mulVec_A]
    change -(-y (tA a)) = y (tA a)
    ring
  · rcases r with b | c
    · change treeMinor.mulVec (treeInverseVec y) (tB b) = y (tB b)
      rw [treeMinor_mulVec_B]
      change
        (y (tB b) +
          (if b = 0 then ∑ a : Fin 8, y (tA a) else 0)) +
          (if b = 0 then ∑ a : Fin 8, -y (tA a) else 0) =
          y (tB b)
      by_cases hb : b = 0
      · simp [hb]
      · simp [hb]
    · change treeMinor.mulVec (treeInverseVec y) (tC c) = y (tC c)
      rw [treeMinor_mulVec_C]
      rfl

private lemma treeMinor_surjective :
    Function.Surjective treeMinor.mulVec := by
  intro y
  exact ⟨treeInverseVec y, treeInverseVec_right y⟩

private lemma treeMinor_rank_full :
    treeMinor.rank = Fintype.card Tree := by
  rw [Matrix.rank]
  rw [LinearMap.range_eq_top.mpr treeMinor_surjective]
  simp

private lemma treeMinor_eq_submatrix :
    treeMinor =
      boundary1.submatrix nonRootVertex treeEdge := by
  ext i j
  rcases i with a | i
  · rcases j with a' | j
    · simp [treeMinor, boundary1, nonRootVertex, treeEdge]
    · rcases j with b | c
      · simp [treeMinor, boundary1, nonRootVertex, treeEdge]
      · simp [treeMinor, boundary1, nonRootVertex, treeEdge]
  · rcases i with b | c
    · rcases j with a | j
      · simp [treeMinor, boundary1, nonRootVertex, treeEdge]
      · rcases j with b' | c'
        · simp [treeMinor, boundary1, nonRootVertex, treeEdge]
        · simp [treeMinor, boundary1, nonRootVertex, treeEdge]
    · rcases j with a | j
      · simp [treeMinor, boundary1, nonRootVertex, treeEdge]
      · rcases j with b | c'
        · simp [treeMinor, boundary1, nonRootVertex, treeEdge]
        · simp [treeMinor, boundary1, nonRootVertex, treeEdge]

private theorem tree_card : Fintype.card Tree = 32 := by decide

private lemma boundary1_rank_ge_32 : 32 ≤ boundary1.rank := by
  have hminor : treeMinor.rank = 32 := by
    rw [treeMinor_rank_full, tree_card]
  calc
    32 = treeMinor.rank := hminor.symm
    _ = (boundary1.submatrix nonRootVertex treeEdge).rank := by
      rw [← treeMinor_eq_submatrix]
    _ ≤ boundary1.rank :=
      Matrix.rank_submatrix_le boundary1 nonRootVertex treeEdge

/-- The connected complete-tripartite incidence matrix has rank `33-1=32`. -/
theorem boundary1_rank : boundary1.rank = 32 :=
  le_antisymm boundary1_rank_le_32 boundary1_rank_ge_32

/-! ## Rank of `∂₂` -/

abbrev NonTree :=
  (Fin 8 × B) ⊕
    ((A × Fin 12) ⊕
      (B ⊕ (Fin 10 × Fin 12)))

instance : DecidableEq NonTree := inferInstance
instance : Fintype NonTree := inferInstance

private def ntAB (a : Fin 8) (b : B) : NonTree :=
  Sum.inl (a, b)

private def ntAC (a : A) (c : Fin 12) : NonTree :=
  Sum.inr (Sum.inl (a, c))

private def ntBC0 (b : B) : NonTree :=
  Sum.inr (Sum.inr (Sum.inl b))

private def ntBCP (b : Fin 10) (c : Fin 12) : NonTree :=
  Sum.inr (Sum.inr (Sum.inr (b, c)))

private def nonTreeEdge : NonTree → Edge
  | Sum.inl (a, b) => Sum.inl (a.succ, b)
  | Sum.inr (Sum.inl (a, c)) =>
      Sum.inr (Sum.inl (a, c.succ))
  | Sum.inr (Sum.inr (Sum.inl b)) =>
      Sum.inr (Sum.inr (b, 0))
  | Sum.inr (Sum.inr (Sum.inr (b, c))) =>
      Sum.inr (Sum.inr (b.succ, c.succ))

private def selectedTriangle : NonTree → Triangle
  | Sum.inl (a, b) => (a.succ, b, 0)
  | Sum.inr (Sum.inl (a, c)) => (a, 0, c.succ)
  | Sum.inr (Sum.inr (Sum.inl b)) => (0, b, 0)
  | Sum.inr (Sum.inr (Sum.inr (b, c))) =>
      (0, b.succ, c.succ)

/-- The explicit non-tree-edge/selected-triangle minor of `∂₂`. -/
def boundary2Minor : Matrix NonTree NonTree ℚ
  | Sum.inl (a, b), Sum.inl (a', b') =>
      if a = a' ∧ b = b' then 1 else 0
  | Sum.inl (a, b), Sum.inr (Sum.inl (a', _)) =>
      if a.succ = a' ∧ b = 0 then 1 else 0
  | Sum.inl _, Sum.inr (Sum.inr _) => 0
  | Sum.inr (Sum.inl (a, c)),
      Sum.inr (Sum.inl (a', c')) =>
      if a = a' ∧ c = c' then -1 else 0
  | Sum.inr (Sum.inl _), Sum.inl _ => 0
  | Sum.inr (Sum.inl (a, c)),
      Sum.inr (Sum.inr (Sum.inr (_, c'))) =>
      if a = 0 ∧ c = c' then -1 else 0
  | Sum.inr (Sum.inl _),
      Sum.inr (Sum.inr (Sum.inl _)) => 0
  | Sum.inr (Sum.inr (Sum.inl b)), Sum.inl (_, b') =>
      if b = b' then 1 else 0
  | Sum.inr (Sum.inr (Sum.inl b)),
      Sum.inr (Sum.inr (Sum.inl b')) =>
      if b = b' then 1 else 0
  | Sum.inr (Sum.inr (Sum.inl _)),
      Sum.inr (Sum.inl _) => 0
  | Sum.inr (Sum.inr (Sum.inl _)),
      Sum.inr (Sum.inr (Sum.inr _)) => 0
  | Sum.inr (Sum.inr (Sum.inr (b, c))),
      Sum.inr (Sum.inr (Sum.inr (b', c'))) =>
      if b = b' ∧ c = c' then 1 else 0
  | Sum.inr (Sum.inr (Sum.inr _)), _ => 0

private lemma boundary2Minor_eq_submatrix :
    boundary2Minor =
      boundary2.submatrix nonTreeEdge selectedTriangle := by
  ext i j
  rcases i with i | i
  · rcases i with ⟨a, b⟩
    rcases j with j | j
    · rcases j with ⟨a', b'⟩
      simp [boundary2Minor, boundary2, nonTreeEdge, selectedTriangle]
    · rcases j with j | j
      · rcases j with ⟨a', c'⟩
        simp [boundary2Minor, boundary2, nonTreeEdge, selectedTriangle]
      · rcases j with b' | j
        · simp [boundary2Minor, boundary2, nonTreeEdge, selectedTriangle]
        · rcases j with ⟨b', c'⟩
          simp [boundary2Minor, boundary2, nonTreeEdge, selectedTriangle]
  · rcases i with i | i
    · rcases i with ⟨a, c⟩
      rcases j with j | j
      · rcases j with ⟨a', b'⟩
        simp [boundary2Minor, boundary2, nonTreeEdge, selectedTriangle]
      · rcases j with j | j
        · rcases j with ⟨a', c'⟩
          simp [boundary2Minor, boundary2, nonTreeEdge, selectedTriangle]
        · rcases j with b | j
          · simp [boundary2Minor, boundary2, nonTreeEdge, selectedTriangle]
          · rcases j with ⟨b, c'⟩
            simp [boundary2Minor, boundary2, nonTreeEdge, selectedTriangle]
    · rcases i with b | i
      · rcases j with j | j
        · rcases j with ⟨a', b'⟩
          simp [boundary2Minor, boundary2, nonTreeEdge, selectedTriangle]
        · rcases j with j | j
          · rcases j with ⟨a', c'⟩
            simp [boundary2Minor, boundary2, nonTreeEdge, selectedTriangle]
            intro _
            exact (Fin.succ_ne_zero c') ∘ Eq.symm
          · rcases j with b' | j
            · simp [boundary2Minor, boundary2, nonTreeEdge, selectedTriangle]
            · rcases j with ⟨b', c'⟩
              simp [boundary2Minor, boundary2, nonTreeEdge, selectedTriangle]
              intro _
              exact (Fin.succ_ne_zero c') ∘ Eq.symm
      · rcases i with ⟨b, c⟩
        rcases j with j | j
        · rcases j with ⟨a', b'⟩
          simp [boundary2Minor, boundary2, nonTreeEdge, selectedTriangle]
        · rcases j with j | j
          · rcases j with ⟨a', c'⟩
            simp [boundary2Minor, boundary2, nonTreeEdge, selectedTriangle]
          · rcases j with b' | j
            · simp [boundary2Minor, boundary2, nonTreeEdge, selectedTriangle]
            · rcases j with ⟨b', c'⟩
              simp [boundary2Minor, boundary2, nonTreeEdge, selectedTriangle]

private lemma sum_prod_ite_pair
    {α β : Type} [Fintype α] [Fintype β]
    [DecidableEq α] [DecidableEq β]
    (f : α × β → ℚ) (a : α) (b : β) :
    (∑ p : α × β,
      if a = p.1 ∧ b = p.2 then f p else 0) =
      f (a, b) := by
  rw [Fintype.sum_prod_type]
  calc
    (∑ x : α, ∑ y : β,
      if a = x ∧ b = y then f (x, y) else 0) =
        ∑ x : α, if a = x then f (x, b) else 0 := by
      apply Fintype.sum_congr
      intro x
      by_cases hx : a = x
      · subst x
        simpa using
          Fintype.sum_ite_eq b (fun y : β => f (a, y))
      · simp [hx]
    _ = f (a, b) := by
      simpa using
        Fintype.sum_ite_eq a (fun x : α => f (x, b))

private lemma sum_prod_ite_snd
    {α β : Type} [Fintype α] [Fintype β] [DecidableEq β]
    (f : α × β → ℚ) (b : β) :
    (∑ p : α × β, if b = p.2 then f p else 0) =
      ∑ a : α, f (a, b) := by
  rw [Fintype.sum_prod_type]
  apply Fintype.sum_congr
  intro a
  simpa using
    Fintype.sum_ite_eq b (fun y : β => f (a, y))

private lemma sum_prod_ite_fst
    {α β : Type} [Fintype α] [Fintype β] [DecidableEq α]
    (f : α × β → ℚ) (a : α) :
    (∑ p : α × β, if a = p.1 then f p else 0) =
      ∑ b : β, f (a, b) := by
  rw [Fintype.sum_prod_type]
  calc
    (∑ x : α, ∑ y : β,
      if a = x then f (x, y) else 0) =
        ∑ x : α,
          if a = x then (∑ y : β, f (x, y)) else 0 := by
      apply Fintype.sum_congr
      intro x
      by_cases hx : a = x <;> simp [hx]
    _ = ∑ b : β, f (a, b) := by
      simpa using
        Fintype.sum_ite_eq a
          (fun x : α => ∑ y : β, f (x, y))

private lemma sum_indicator_pair_one
    {α β : Type} [Fintype α] [Fintype β]
    [DecidableEq α] [DecidableEq β]
    (f : α × β → ℚ) (a : α) (b : β) :
    (∑ p : α × β,
      (if a = p.1 ∧ b = p.2 then (1 : ℚ) else 0) * f p) =
      f (a, b) := by
  simp_rw [ite_mul, one_mul, zero_mul]
  exact sum_prod_ite_pair f a b

private lemma sum_indicator_pair_neg
    {α β : Type} [Fintype α] [Fintype β]
    [DecidableEq α] [DecidableEq β]
    (f : α × β → ℚ) (a : α) (b : β) :
    (∑ p : α × β,
      (if a = p.1 ∧ b = p.2 then (-1 : ℚ) else 0) * f p) =
      -f (a, b) := by
  simp_rw [ite_mul, neg_one_mul, zero_mul]
  rw [sum_prod_ite_pair]

private lemma sum_indicator_snd_one
    {α β : Type} [Fintype α] [Fintype β] [DecidableEq β]
    (f : α × β → ℚ) (b : β) :
    (∑ p : α × β,
      (if b = p.2 then (1 : ℚ) else 0) * f p) =
      ∑ a : α, f (a, b) := by
  simp_rw [ite_mul, one_mul, zero_mul]
  exact sum_prod_ite_snd f b

private lemma sum_indicator_snd_neg
    {α β : Type} [Fintype α] [Fintype β] [DecidableEq β]
    (f : α × β → ℚ) (b : β) :
    (∑ p : α × β,
      (if b = p.2 then (-1 : ℚ) else 0) * f p) =
      -∑ a : α, f (a, b) := by
  simp_rw [ite_mul, neg_one_mul, zero_mul]
  rw [sum_prod_ite_snd, Finset.sum_neg_distrib]

private lemma sum_indicator_fst_one
    {α β : Type} [Fintype α] [Fintype β] [DecidableEq α]
    (f : α × β → ℚ) (a : α) :
    (∑ p : α × β,
      (if a = p.1 then (1 : ℚ) else 0) * f p) =
      ∑ b : β, f (a, b) := by
  simp_rw [ite_mul, one_mul, zero_mul]
  exact sum_prod_ite_fst f a

private lemma boundary2Minor_mulVec_BCP
    (x : NonTree → ℚ) (b : Fin 10) (c : Fin 12) :
    boundary2Minor.mulVec x (ntBCP b c) =
      x (ntBCP b c) := by
  simp only [Matrix.mulVec, dotProduct, ntBCP,
    boundary2Minor, Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
    add_zero, zero_add]
  exact sum_indicator_pair_one
    (fun p => x (Sum.inr (Sum.inr (Sum.inr p)))) b c

private lemma boundary2Minor_mulVec_AC
    (x : NonTree → ℚ) (a : A) (c : Fin 12) :
    boundary2Minor.mulVec x (ntAC a c) =
      -x (ntAC a c) -
        (if a = 0 then
          ∑ b : Fin 10, x (ntBCP b c)
        else 0) := by
  simp only [Matrix.mulVec, dotProduct, ntAC, ntBCP,
    boundary2Minor, Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
    add_zero, zero_add]
  rw [sum_indicator_pair_neg]
  by_cases ha : a = 0
  · subst a
    simp only [if_true, true_and]
    rw [sum_indicator_snd_neg]
    ring
  · simp [ha]

private lemma boundary2Minor_mulVec_AB
    (x : NonTree → ℚ) (a : Fin 8) (b : B) :
    boundary2Minor.mulVec x (ntAB a b) =
      x (ntAB a b) +
        (if b = 0 then
          ∑ c : Fin 12, x (ntAC a.succ c)
        else 0) := by
  simp only [Matrix.mulVec, dotProduct, ntAB, ntAC,
    boundary2Minor, Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
    add_zero, zero_add]
  rw [sum_indicator_pair_one]
  by_cases hb : b = 0
  · subst b
    simp only [if_true]
    convert congrArg
      (fun z : ℚ => x (Sum.inl (a, 0)) + z)
      (sum_indicator_fst_one
        (fun p => x (Sum.inr (Sum.inl p))) a.succ) using 1 <;> simp
  · simp [hb]

private lemma boundary2Minor_mulVec_BC0
    (x : NonTree → ℚ) (b : B) :
    boundary2Minor.mulVec x (ntBC0 b) =
      x (ntBC0 b) +
        ∑ a : Fin 8, x (ntAB a b) := by
  simp only [Matrix.mulVec, dotProduct, ntAB, ntBC0,
    boundary2Minor, Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
    add_zero, zero_add]
  rw [sum_indicator_snd_one]
  have hsingle :
      (∑ x₁ : B,
        (if b = x₁ then (1 : ℚ) else 0) *
          x (Sum.inr (Sum.inr (Sum.inl x₁)))) =
        x (Sum.inr (Sum.inr (Sum.inl b))) := by
    simp_rw [ite_mul, one_mul, zero_mul]
    exact Fintype.sum_ite_eq b
      (fun x₁ : B => x (Sum.inr (Sum.inr (Sum.inl x₁))))
  rw [hsingle]
  ring

private def boundary2MinorInverseVec
    (y : NonTree → ℚ) : NonTree → ℚ
  | Sum.inr (Sum.inr (Sum.inr (b, c))) =>
      y (ntBCP b c)
  | Sum.inr (Sum.inl (a, c)) =>
      -y (ntAC a c) -
        (if a = 0 then
          ∑ b : Fin 10, y (ntBCP b c)
        else 0)
  | Sum.inl (a, b) =>
      y (ntAB a b) +
        (if b = 0 then
          ∑ c : Fin 12, y (ntAC a.succ c)
        else 0)
  | Sum.inr (Sum.inr (Sum.inl b)) =>
      y (ntBC0 b) -
        ∑ a : Fin 8,
          (y (ntAB a b) +
            (if b = 0 then
              ∑ c : Fin 12, y (ntAC a.succ c)
            else 0))

private lemma boundary2MinorInverseVec_right
    (y : NonTree → ℚ) :
    boundary2Minor.mulVec (boundary2MinorInverseVec y) = y := by
  funext r
  rcases r with r | r
  · rcases r with ⟨a, b⟩
    change
      boundary2Minor.mulVec (boundary2MinorInverseVec y)
        (ntAB a b) = y (ntAB a b)
    rw [boundary2Minor_mulVec_AB]
    change
      (y (ntAB a b) +
        (if b = 0 then
          ∑ c : Fin 12, y (ntAC a.succ c)
        else 0)) +
        (if b = 0 then
          ∑ c : Fin 12,
            (-y (ntAC a.succ c) -
              (if a.succ = 0 then
                ∑ b : Fin 10, y (ntBCP b c)
              else 0))
        else 0) = y (ntAB a b)
    have hsucc : a.succ ≠ (0 : A) := Fin.succ_ne_zero a
    by_cases hb : b = 0
    · simp [hb, hsucc]
    · simp [hb]
  · rcases r with r | r
    · rcases r with ⟨a, c⟩
      change
        boundary2Minor.mulVec (boundary2MinorInverseVec y)
          (ntAC a c) = y (ntAC a c)
      rw [boundary2Minor_mulVec_AC]
      change
        -(-y (ntAC a c) -
            (if a = 0 then
              ∑ b : Fin 10, y (ntBCP b c)
            else 0)) -
          (if a = 0 then
            ∑ b : Fin 10, y (ntBCP b c)
          else 0) = y (ntAC a c)
      ring
    · rcases r with b | r
      · change
          boundary2Minor.mulVec (boundary2MinorInverseVec y)
            (ntBC0 b) = y (ntBC0 b)
        rw [boundary2Minor_mulVec_BC0]
        change
          (y (ntBC0 b) -
            ∑ a : Fin 8,
              (y (ntAB a b) +
                (if b = 0 then
                  ∑ c : Fin 12, y (ntAC a.succ c)
                else 0))) +
            ∑ a : Fin 8,
              (y (ntAB a b) +
                (if b = 0 then
                  ∑ c : Fin 12, y (ntAC a.succ c)
                else 0)) = y (ntBC0 b)
        ring
      · rcases r with ⟨b, c⟩
        change
          boundary2Minor.mulVec (boundary2MinorInverseVec y)
            (ntBCP b c) = y (ntBCP b c)
        rw [boundary2Minor_mulVec_BCP]
        rfl

private lemma boundary2Minor_surjective :
    Function.Surjective boundary2Minor.mulVec := by
  intro y
  exact
    ⟨boundary2MinorInverseVec y,
      boundary2MinorInverseVec_right y⟩

private theorem nonTree_card : Fintype.card NonTree = 327 := by
  norm_num [NonTree]

/-- The explicit `327×327` minor is full-rank. -/
theorem boundary2_minor_rank : boundary2Minor.rank = 327 := by
  calc
    boundary2Minor.rank = Fintype.card NonTree := by
      rw [Matrix.rank]
      rw [LinearMap.range_eq_top.mpr boundary2Minor_surjective]
      simp
    _ = 327 := nonTree_card

private lemma boundary2_rank_ge_327 : 327 ≤ boundary2.rank := by
  calc
    327 = boundary2Minor.rank := boundary2_minor_rank.symm
    _ = (boundary2.submatrix nonTreeEdge selectedTriangle).rank := by
      rw [← boundary2Minor_eq_submatrix]
    _ ≤ boundary2.rank :=
      Matrix.rank_submatrix_le boundary2 nonTreeEdge selectedTriangle

private lemma edge_card : Fintype.card Edge = 359 := by
  rw [tripartite_edge_cardinality]
  norm_num

private lemma boundary2_rank_le_327 : boundary2.rank ≤ 327 := by
  have h :=
    Matrix.rank_add_rank_le_card_of_mul_eq_zero
      boundary_squared_zero
  rw [boundary1_rank, edge_card] at h
  omega

/-- Every graph cycle is a rational combination of triangle boundaries:
`rank ∂₂ = 327`. -/
theorem boundary2_rank : boundary2.rank = 327 :=
  le_antisymm boundary2_rank_le_327 boundary2_rank_ge_327

/-- Rank bundle for the explicit typed tripartite chain complex. -/
theorem typed_tripartite_boundary_rank :
    boundary1 * boundary2 = 0 ∧
    boundary1.rank = 32 ∧
    boundary2.rank = 327 :=
  ⟨boundary_squared_zero, boundary1_rank, boundary2_rank⟩

end D0.Topology.TypedTripartiteBoundaryRank
