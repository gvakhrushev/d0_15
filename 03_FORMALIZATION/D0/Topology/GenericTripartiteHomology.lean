import D0.SelfReading.TypedIncidenceCarriers
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Tactic

/-!
# D0-GENERIC-TRIPARTITE-HOMOLOGY-001 — generic boundary ranks for K(p+1,q+1,r+1)

For the canonical finite zones `Fin (p+1)`, `Fin (q+1)`, and `Fin (r+1)`,
this module constructs the rational simplicial boundary maps and proves

* `rank ∂₁ = p+q+r+2`;
* `rank ∂₂ = pq+pr+qr+p+q+r+1`;
* `range ∂₂ = ker ∂₁`;
* `(β₀,β₁,β₂) = (1,0,pqr)` and `χ = 1+pqr`.

The result is rational and chain-level.  It does not assert integral
torsion-freeness, an explicit basis of `H₂`, or a wedge-of-spheres homotopy
classification.
-/

namespace D0.Topology.GenericTripartiteHomology

open scoped BigOperators
open Matrix
open D0.SelfReading.TypedIncidenceCarriers

abbrev GenericVertex (p q r : ℕ) :=
  Fin (p + 1) ⊕ (Fin (q + 1) ⊕ Fin (r + 1))

abbrev GenericEdge (p q r : ℕ) :=
  TripartiteEdge (Fin (p + 1)) (Fin (q + 1)) (Fin (r + 1))

abbrev GenericTriangle (p q r : ℕ) :=
  TripartiteTriangle (Fin (p + 1)) (Fin (q + 1)) (Fin (r + 1))

abbrev TreeIndex (p q r : ℕ) :=
  Fin p ⊕ (Fin (q + 1) ⊕ Fin (r + 1))

abbrev NonTreeIndex (p q r : ℕ) :=
  (Fin p × Fin (q + 1)) ⊕
    ((Fin (p + 1) × Fin r) ⊕
      (Fin (q + 1) ⊕ (Fin q × Fin r)))

/-- Rank of the connected vertex-edge boundary. -/
def vertexBoundaryRank (p q r : ℕ) : ℕ := p + q + r + 2

/-- Dimension of the graph cycle space / rank of the triangle boundary. -/
def cycleRank (p q r : ℕ) : ℕ :=
  p * q + p * r + q * r + p + q + r + 1

section

variable {p q r : ℕ}

local notation "A" => Fin (p + 1)
local notation "B" => Fin (q + 1)
local notation "C" => Fin (r + 1)
local notation "Vertex" => GenericVertex p q r
local notation "Edge" => GenericEdge p q r
local notation "Triangle" => GenericTriangle p q r
local notation "Tree" => TreeIndex p q r
local notation "NonTree" => NonTreeIndex p q r
local notation "vRank" => vertexBoundaryRank p q r
local notation "cycleDim" => cycleRank p q r

instance : DecidableEq Vertex := inferInstance
instance : DecidableEq Edge := inferInstance
instance : DecidableEq Triangle := inferInstance
instance : DecidableEq Tree := inferInstance
instance : Fintype Tree := inferInstance
instance : DecidableEq NonTree := inferInstance
instance : Fintype NonTree := inferInstance

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

local notation "d₁" => boundary1 (p := p) (q := q) (r := r)
local notation "d₂" => boundary2 (p := p) (q := q) (r := r)

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
theorem boundary_squared_zero : d₁ * d₂ = 0 := by
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

local notation "ONE" => ones (p := p) (q := q) (r := r)

private lemma sum_ite_one
    {α : Type} [Fintype α] [DecidableEq α] (a : α) :
    (∑ x : α, if x = a then (1 : ℚ) else 0) = 1 := by
  simpa using Fintype.sum_ite_eq' a (fun _ : α => (1 : ℚ))

private lemma sum_ite_neg_one
    {α : Type} [Fintype α] [DecidableEq α] (a : α) :
    (∑ x : α, if x = a then (-1 : ℚ) else 0) = -1 := by
  simpa using Fintype.sum_ite_eq' a (fun _ : α => (-1 : ℚ))

private lemma boundary1_transpose_ones :
    (d₁).transpose.mulVec ONE = 0 := by
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

private lemma ones_ne_zero : ONE ≠ 0 := by
  intro h
  have hx := congrFun h (Sum.inl (0 : A))
  norm_num [ones] at hx

private lemma boundary1_rank_le : (d₁).rank ≤ vRank := by
  have hmem : ONE ∈ LinearMap.ker (d₁).transpose.mulVecLin := by
    rw [LinearMap.mem_ker]
    exact boundary1_transpose_ones (p := p) (q := q) (r := r)
  have hker : LinearMap.ker (d₁).transpose.mulVecLin ≠ ⊥ := by
    intro hbot
    have hmem' := hmem
    rw [hbot] at hmem'
    have hz : ONE = 0 := by simpa using hmem'
    exact ones_ne_zero (p := p) (q := q) (r := r) hz
  have hkerpos :
      1 ≤ Module.finrank ℚ
        (LinearMap.ker (d₁).transpose.mulVecLin) :=
    Submodule.one_le_finrank_iff.mpr hker
  have hrn :=
    LinearMap.finrank_range_add_finrank_ker
      (d₁).transpose.mulVecLin
  have hsum :
      (d₁).transpose.rank +
        Module.finrank ℚ
          (LinearMap.ker (d₁).transpose.mulVecLin) = p + q + r + 3 := by
    rw [Matrix.rank]
    calc
      Module.finrank ℚ
          (LinearMap.range (d₁).transpose.mulVecLin) +
          Module.finrank ℚ
            (LinearMap.ker (d₁).transpose.mulVecLin) =
          Module.finrank ℚ (Vertex → ℚ) := hrn
      _ = Fintype.card Vertex :=
        Module.finrank_fintype_fun_eq_card ℚ
      _ = p + q + r + 3 := by
        simp [GenericVertex]
        omega
  have htrans :
      (d₁).transpose.rank = (d₁).rank :=
    Matrix.rank_transpose d₁
  rw [htrans] at hsum
  simp [vertexBoundaryRank] at hsum ⊢
  omega

private def tA (a : Fin p) : Tree := Sum.inl a
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
    (x : Tree → ℚ) (a : Fin p) :
    treeMinor.mulVec x (tA a) = -x (tA a) := by
  simp only [Matrix.mulVec, dotProduct, treeMinor, tA,
    Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
    add_zero, zero_add]
  exact sum_indicator_neg (fun a => x (Sum.inl a)) a

private lemma treeMinor_mulVec_B
    (x : Tree → ℚ) (b : B) :
    treeMinor.mulVec x (tB b) =
      x (tB b) +
        (if b = 0 then ∑ a : Fin p, x (tA a) else 0) := by
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
        (if b = 0 then ∑ a : Fin p, y (tA a) else 0)
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
          (if b = 0 then ∑ a : Fin p, y (tA a) else 0)) +
          (if b = 0 then ∑ a : Fin p, -y (tA a) else 0) =
          y (tB b)
      by_cases hb : b = 0
      · simp [hb]
      · simp [hb]
    · change treeMinor.mulVec (treeInverseVec y) (tC c) = y (tC c)
      rw [treeMinor_mulVec_C]
      rfl

private lemma treeMinor_surjective :
    Function.Surjective
      (treeMinor (p := p) (q := q) (r := r)).mulVec := by
  intro y
  exact ⟨treeInverseVec y, treeInverseVec_right y⟩

private lemma treeMinor_rank_full :
    (treeMinor (p := p) (q := q) (r := r)).rank = Fintype.card Tree := by
  rw [Matrix.rank]
  rw [LinearMap.range_eq_top.mpr (treeMinor_surjective (p := p) (q := q) (r := r))]
  simp

private lemma treeMinor_eq_submatrix :
    treeMinor (p := p) (q := q) (r := r) =
      (d₁).submatrix
        (nonRootVertex (p := p) (q := q) (r := r))
        (treeEdge (p := p) (q := q) (r := r)) := by
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

private theorem tree_card : Fintype.card Tree = vRank := by
  simp [TreeIndex, vertexBoundaryRank]
  omega

private lemma boundary1_rank_ge : vRank ≤ (d₁).rank := by
  have hminor :
      (treeMinor (p := p) (q := q) (r := r)).rank = vRank := by
    rw [treeMinor_rank_full (p := p) (q := q) (r := r),
      tree_card (p := p) (q := q) (r := r)]
  calc
    vRank = (treeMinor (p := p) (q := q) (r := r)).rank := hminor.symm
    _ = ((d₁).submatrix
          (nonRootVertex (p := p) (q := q) (r := r))
          (treeEdge (p := p) (q := q) (r := r))).rank := by
      rw [← treeMinor_eq_submatrix (p := p) (q := q) (r := r)]
    _ ≤ (d₁).rank :=
      Matrix.rank_submatrix_le d₁
        (nonRootVertex (p := p) (q := q) (r := r))
        (treeEdge (p := p) (q := q) (r := r))

/-- The connected complete-tripartite incidence matrix has rank
`p+q+r+2`, one below its vertex count. -/
theorem boundary1_rank : (d₁).rank = vRank :=
  le_antisymm (boundary1_rank_le (p := p) (q := q) (r := r))
    (boundary1_rank_ge (p := p) (q := q) (r := r))

/-! ## Rank of `∂₂` -/

private def ntAB (a : Fin p) (b : B) : NonTree :=
  Sum.inl (a, b)

private def ntAC (a : A) (c : Fin r) : NonTree :=
  Sum.inr (Sum.inl (a, c))

private def ntBC0 (b : B) : NonTree :=
  Sum.inr (Sum.inr (Sum.inl b))

private def ntBCP (b : Fin q) (c : Fin r) : NonTree :=
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
    boundary2Minor (p := p) (q := q) (r := r) =
      (d₂).submatrix
        (nonTreeEdge (p := p) (q := q) (r := r))
        (selectedTriangle (p := p) (q := q) (r := r)) := by
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
    (x : NonTree → ℚ) (b : Fin q) (c : Fin r) :
    boundary2Minor.mulVec x (ntBCP b c) =
      x (ntBCP b c) := by
  simp only [Matrix.mulVec, dotProduct, ntBCP,
    boundary2Minor, Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
    add_zero, zero_add]
  exact sum_indicator_pair_one
    (fun p => x (Sum.inr (Sum.inr (Sum.inr p)))) b c

private lemma boundary2Minor_mulVec_AC
    (x : NonTree → ℚ) (a : A) (c : Fin r) :
    boundary2Minor.mulVec x (ntAC a c) =
      -x (ntAC a c) -
        (if a = 0 then
          ∑ b : Fin q, x (ntBCP b c)
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
    (x : NonTree → ℚ) (a : Fin p) (b : B) :
    boundary2Minor.mulVec x (ntAB a b) =
      x (ntAB a b) +
        (if b = 0 then
          ∑ c : Fin r, x (ntAC a.succ c)
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
        ∑ a : Fin p, x (ntAB a b) := by
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
          ∑ b : Fin q, y (ntBCP b c)
        else 0)
  | Sum.inl (a, b) =>
      y (ntAB a b) +
        (if b = 0 then
          ∑ c : Fin r, y (ntAC a.succ c)
        else 0)
  | Sum.inr (Sum.inr (Sum.inl b)) =>
      y (ntBC0 b) -
        ∑ a : Fin p,
          (y (ntAB a b) +
            (if b = 0 then
              ∑ c : Fin r, y (ntAC a.succ c)
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
          ∑ c : Fin r, y (ntAC a.succ c)
        else 0)) +
        (if b = 0 then
          ∑ c : Fin r,
            (-y (ntAC a.succ c) -
              (if a.succ = 0 then
                ∑ b : Fin q, y (ntBCP b c)
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
              ∑ b : Fin q, y (ntBCP b c)
            else 0)) -
          (if a = 0 then
            ∑ b : Fin q, y (ntBCP b c)
          else 0) = y (ntAC a c)
      ring
    · rcases r with b | r
      · change
          boundary2Minor.mulVec (boundary2MinorInverseVec y)
            (ntBC0 b) = y (ntBC0 b)
        rw [boundary2Minor_mulVec_BC0]
        change
          (y (ntBC0 b) -
            ∑ a : Fin p,
              (y (ntAB a b) +
                (if b = 0 then
                  ∑ c : Fin r, y (ntAC a.succ c)
                else 0))) +
            ∑ a : Fin p,
              (y (ntAB a b) +
                (if b = 0 then
                  ∑ c : Fin r, y (ntAC a.succ c)
                else 0)) = y (ntBC0 b)
        ring
      · rcases r with ⟨b, c⟩
        change
          boundary2Minor.mulVec (boundary2MinorInverseVec y)
            (ntBCP b c) = y (ntBCP b c)
        rw [boundary2Minor_mulVec_BCP]
        rfl

private lemma boundary2Minor_surjective :
    Function.Surjective
      (boundary2Minor (p := p) (q := q) (r := r)).mulVec := by
  intro y
  exact
    ⟨boundary2MinorInverseVec y,
      boundary2MinorInverseVec_right y⟩

private theorem nonTree_card : Fintype.card NonTree = cycleDim := by
  simp [NonTreeIndex, cycleRank]
  ring

/-- The explicit square minor of size
`pq+pr+qr+p+q+r+1` is full-rank. -/
theorem boundary2_minor_rank :
    (boundary2Minor (p := p) (q := q) (r := r)).rank = cycleDim := by
  calc
    (boundary2Minor (p := p) (q := q) (r := r)).rank =
        Fintype.card NonTree := by
      rw [Matrix.rank]
      rw [LinearMap.range_eq_top.mpr
        (boundary2Minor_surjective (p := p) (q := q) (r := r))]
      simp
    _ = cycleDim := nonTree_card (p := p) (q := q) (r := r)

private lemma boundary2_rank_ge : cycleDim ≤ (d₂).rank := by
  calc
    cycleDim = (boundary2Minor (p := p) (q := q) (r := r)).rank :=
      (boundary2_minor_rank (p := p) (q := q) (r := r)).symm
    _ = ((d₂).submatrix
          (nonTreeEdge (p := p) (q := q) (r := r))
          (selectedTriangle (p := p) (q := q) (r := r))).rank := by
      rw [← boundary2Minor_eq_submatrix (p := p) (q := q) (r := r)]
    _ ≤ (d₂).rank :=
      Matrix.rank_submatrix_le d₂
        (nonTreeEdge (p := p) (q := q) (r := r))
        (selectedTriangle (p := p) (q := q) (r := r))

private lemma edge_card : Fintype.card Edge = vRank + cycleDim := by
  rw [tripartite_edge_cardinality]
  simp [GenericEdge, vertexBoundaryRank, cycleRank]
  ring

private lemma boundary2_rank_le : (d₂).rank ≤ cycleDim := by
  have h :=
    Matrix.rank_add_rank_le_card_of_mul_eq_zero
      (boundary_squared_zero (p := p) (q := q) (r := r))
  rw [boundary1_rank (p := p) (q := q) (r := r),
    edge_card (p := p) (q := q) (r := r)] at h
  omega

/-- Every graph cycle is a rational combination of triangle boundaries:
`rank ∂₂ = pq+pr+qr+p+q+r+1`. -/
theorem boundary2_rank : (d₂).rank = cycleDim :=
  le_antisymm (boundary2_rank_le (p := p) (q := q) (r := r))
    (boundary2_rank_ge (p := p) (q := q) (r := r))

/-- Rank bundle for the explicit typed tripartite chain complex. -/
theorem generic_tripartite_boundary_rank :
    d₁ * d₂ = 0 ∧
    (d₁).rank = vRank ∧
    (d₂).rank = cycleDim :=
  ⟨boundary_squared_zero (p := p) (q := q) (r := r),
    boundary1_rank (p := p) (q := q) (r := r),
    boundary2_rank (p := p) (q := q) (r := r)⟩

/-! ## Exactness and generic rational homology -/

/-- Face-cardinality formulas for the generic complete-tripartite clique complex. -/
theorem generic_face_cardinalities :
    Fintype.card Vertex = p + q + r + 3 ∧
    Fintype.card Edge = vRank + cycleDim ∧
    Fintype.card Triangle = (p + 1) * (q + 1) * (r + 1) := by
  constructor
  · simp [GenericVertex]
    omega
  constructor
  · exact edge_card (p := p) (q := q) (r := r)
  · simp [GenericTriangle, TripartiteTriangle]
    ring

/-- Every rational 1-cycle is generated by triangle boundaries. -/
theorem boundary_exact :
    LinearMap.range (d₂).mulVecLin = LinearMap.ker (d₁).mulVecLin := by
  have hle :
      LinearMap.range (d₂).mulVecLin ≤ LinearMap.ker (d₁).mulVecLin := by
    rw [LinearMap.range_le_ker_iff]
    rw [← Matrix.mulVecLin_mul,
      boundary_squared_zero (p := p) (q := q) (r := r)]
    exact Matrix.mulVecLin_zero
  have hrange2 :
      Module.finrank ℚ (LinearMap.range (d₂).mulVecLin) = cycleDim := by
    simpa [Matrix.rank] using boundary2_rank (p := p) (q := q) (r := r)
  have hrange1 :
      Module.finrank ℚ (LinearMap.range (d₁).mulVecLin) = vRank := by
    simpa [Matrix.rank] using boundary1_rank (p := p) (q := q) (r := r)
  have hrankNullity := LinearMap.finrank_range_add_finrank_ker (d₁).mulVecLin
  have hdomain : Module.finrank ℚ (Edge → ℚ) = vRank + cycleDim := by
    rw [Module.finrank_fintype_fun_eq_card,
      edge_card (p := p) (q := q) (r := r)]
  have hker1 : Module.finrank ℚ (LinearMap.ker (d₁).mulVecLin) = cycleDim := by
    omega
  exact Submodule.eq_of_le_of_finrank_le hle (by omega)

/-- Top cycles have dimension `p*q*r`. -/
theorem boundary2_kernel_finrank :
    Module.finrank ℚ (LinearMap.ker (d₂).mulVecLin) = p * q * r := by
  have hrange2 :
      Module.finrank ℚ (LinearMap.range (d₂).mulVecLin) = cycleDim := by
    simpa [Matrix.rank] using boundary2_rank (p := p) (q := q) (r := r)
  have hrankNullity := LinearMap.finrank_range_add_finrank_ker (d₂).mulVecLin
  have hdomain :
      Module.finrank ℚ (Triangle → ℚ) = (p + 1) * (q + 1) * (r + 1) := by
    rw [Module.finrank_fintype_fun_eq_card]
    simp [GenericTriangle, TripartiteTriangle]
    ring
  have hsplit :
      (p + 1) * (q + 1) * (r + 1) = cycleDim + p * q * r := by
    simp [cycleRank]
    ring
  omega

/-- Connectedness gives a one-dimensional degree-zero quotient. -/
theorem boundary1_cokernel_finrank :
    Module.finrank ℚ ((Vertex → ℚ) ⧸ LinearMap.range (d₁).mulVecLin) = 1 := by
  have hrange1 :
      Module.finrank ℚ (LinearMap.range (d₁).mulVecLin) = vRank := by
    simpa [Matrix.rank] using boundary1_rank (p := p) (q := q) (r := r)
  have hquot := Submodule.finrank_quotient_add_finrank
    (LinearMap.range (d₁).mulVecLin)
  have hdomain : Module.finrank ℚ (Vertex → ℚ) = vRank + 1 := by
    rw [Module.finrank_fintype_fun_eq_card]
    simp [GenericVertex, vertexBoundaryRank]
    omega
  omega

/-- Boundaries viewed as a subspace of rational 1-cycles. -/
noncomputable def firstHomologyBoundaries :
    Submodule ℚ (LinearMap.ker (d₁).mulVecLin) :=
  (LinearMap.range (d₂).mulVecLin).comap (LinearMap.ker (d₁).mulVecLin).subtype

/-- Exactness makes the boundary subspace equal to all 1-cycles. -/
theorem first_homology_boundaries_top :
    firstHomologyBoundaries (p := p) (q := q) (r := r) = ⊤ := by
  unfold firstHomologyBoundaries
  rw [boundary_exact (p := p) (q := q) (r := r)]
  ext x
  simp

/-- Actual rational first homology. -/
noncomputable abbrev FirstHomology :=
  (LinearMap.ker (d₁).mulVecLin) ⧸ firstHomologyBoundaries (p := p) (q := q) (r := r)

/-- The generic complete-tripartite clique complex has no rational H1. -/
theorem first_homology_finrank : Module.finrank ℚ (FirstHomology (p := p) (q := q) (r := r)) = 0 := by
  unfold FirstHomology
  rw [first_homology_boundaries_top (p := p) (q := q) (r := r)]
  have hquot := Submodule.finrank_quotient_add_finrank
    (⊤ : Submodule ℚ (LinearMap.ker (d₁).mulVecLin))
  have htop :
      Module.finrank ℚ (↥(⊤ : Submodule ℚ (LinearMap.ker (d₁).mulVecLin))) =
        Module.finrank ℚ (LinearMap.ker (d₁).mulVecLin) := by simp
  omega

/-- **Generic rational homology theorem.** -/
theorem rational_homology_rank_vector :
    (Module.finrank ℚ ((Vertex → ℚ) ⧸ LinearMap.range (d₁).mulVecLin),
      Module.finrank ℚ (FirstHomology (p := p) (q := q) (r := r)),
      Module.finrank ℚ (LinearMap.ker (d₂).mulVecLin)) = (1, 0, p * q * r) := by
  rw [boundary1_cokernel_finrank (p := p) (q := q) (r := r),
    first_homology_finrank (p := p) (q := q) (r := r),
    boundary2_kernel_finrank (p := p) (q := q) (r := r)]

/-- Euler characteristic is `1+p*q*r`. -/
def eulerCharacteristic : ℤ :=
  (Fintype.card Vertex : ℤ) - (Fintype.card Edge : ℤ) + (Fintype.card Triangle : ℤ)

theorem euler_characteristic_formula :
    eulerCharacteristic (p := p) (q := q) (r := r) = 1 + p * q * r := by
  unfold eulerCharacteristic
  have hfaces := generic_face_cardinalities (p := p) (q := q) (r := r)
  rw [hfaces.1, hfaces.2.1, hfaces.2.2]
  simp [vertexBoundaryRank, cycleRank]
  ring

/-- Source-scene specialization: `(p,q,r)=(8,10,12)` gives `β₂=960`. -/
theorem scene_top_homology_finrank :
    Module.finrank ℚ
      (LinearMap.ker (boundary2 (p := 8) (q := 10) (r := 12)).mulVecLin) = 960 := by
  simpa using boundary2_kernel_finrank (p := 8) (q := 10) (r := 12)

end

end D0.Topology.GenericTripartiteHomology
