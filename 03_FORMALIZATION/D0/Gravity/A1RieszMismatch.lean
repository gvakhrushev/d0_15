import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.FiniteDimensional.Basic
import Mathlib.Tactic
import D0.Geometry.SignlessSignedCommonCarrier

/-!
# D0.Gravity.A1RieszMismatch

The exact algebraic A-CAP residue on the literal unsigned common carrier.

`BPlusLin` is imported from `D0.Geometry.SignlessSignedCommonCarrier`; this
file deliberately does not introduce another endpoint operator or another
scene.  `R (a,b,c)` is the bare block-scalar inverse-metric map on the three
edge blocks.  Its restriction to `ker BPlusLin` is the bare-metric mismatch.

This is a bare-metric non-closure theorem only.  It is not a theorem about
physical leakage of the compensator-reduced A1 Hessian, memory cost, capacity
saturation, generation maximality, or Bianchi conservation.  In particular,
`BPlus` remains distinct from the signed Hodge/current operator `BMinus`.
-/

namespace D0.Gravity.A1RieszMismatch

open BigOperators Matrix
open D0.Geometry.SceneCochainComplex
open D0.Geometry.SceneSourceStratification
open D0.Geometry.SignlessSignedCommonCarrier

abbrev EdgeCochain := D0.Geometry.SignlessSignedCommonCarrier.EdgeCochain
abbrev VertexCochain := D0.Geometry.SignlessSignedCommonCarrier.VertexCochain
abbrev V9 := D0.Geometry.SignlessSignedCommonCarrier.V9
abbrev V11 := D0.Geometry.SignlessSignedCommonCarrier.V11
abbrev V13 := D0.Geometry.SignlessSignedCommonCarrier.V13

abbrev KPlus : Submodule ℚ EdgeCochain := LinearMap.ker BPlusLin

/-! ## Balanced zone standard spaces -/

/-- The coordinate sum functional on a finite rational zone. -/
def zoneSumMap (n : ℕ) : (Fin n → ℚ) →ₗ[ℚ] ℚ where
  toFun f := ∑ i, f i
  map_add' f g := Finset.sum_add_distrib
  map_smul' r f := by
    change (∑ i, r * f i) = r * (∑ i, f i)
    rw [Finset.mul_sum]

/-- The balanced (zero-sum) standard space of a zone of size `n`. -/
def Balanced (n : ℕ) : Submodule ℚ (Fin n → ℚ) :=
  LinearMap.ker (zoneSumMap n)

abbrev Balanced9 := Balanced 9
abbrev Balanced11 := Balanced 11
abbrev Balanced13 := Balanced 13

theorem balanced_sum {n : ℕ} (f : Balanced n) :
    (∑ i, f.1 i) = 0 := by
  exact LinearMap.mem_ker.mp f.2

private theorem zoneSumMap_surjective {n : ℕ} (hn : 0 < n) :
    Function.Surjective (zoneSumMap n) := by
  intro q
  refine ⟨fun _ => q / (n : ℚ), ?_⟩
  dsimp [zoneSumMap]
  rw [Finset.sum_const, Finset.card_fin]
  simp only [nsmul_eq_mul]
  field_simp

theorem balanced_finrank {n : ℕ} (hn : 0 < n) :
    Module.finrank ℚ (Balanced n) = n - 1 := by
  have hrange : LinearMap.range (zoneSumMap n) = ⊤ := by
    rw [LinearMap.range_eq_top]
    exact zoneSumMap_surjective hn
  have hrange_dim : Module.finrank ℚ (LinearMap.range (zoneSumMap n)) = 1 := by
    rw [hrange, finrank_top]
    simp
  have h := LinearMap.finrank_range_add_finrank_ker (zoneSumMap n)
  have hdom : Module.finrank ℚ (Fin n → ℚ) = n := by
    rw [Module.finrank_fintype_fun_eq_card]
    simp
  change Module.finrank ℚ (LinearMap.ker (zoneSumMap n)) = n - 1
  rw [hrange_dim, hdom] at h
  omega

theorem balanced9_finrank : Module.finrank ℚ Balanced9 = 8 := by
  simpa using balanced_finrank (n := 9) (by norm_num)

theorem balanced11_finrank : Module.finrank ℚ Balanced11 = 10 := by
  simpa using balanced_finrank (n := 11) (by norm_num)

theorem balanced13_finrank : Module.finrank ℚ Balanced13 = 12 := by
  simpa using balanced_finrank (n := 13) (by norm_num)

/-! ## Bare block-scalar Riesz map and explicit standard embeddings -/

/-- The block-scalar inverse-metric map `R_(a,b,c)`. -/
def R (a b c : ℚ) : EdgeCochain →ₗ[ℚ] EdgeCochain where
  toFun X e :=
    match e with
    | Sum.inl _ => a * X e
    | Sum.inr (Sum.inl _) => b * X e
    | Sum.inr (Sum.inr _) => c * X e
  map_add' X Y := by
    funext e
    rcases e with e | e | e <;> simp <;> ring
  map_smul' r X := by
    funext e
    rcases e with e | e | e <;> simp [smul_eq_mul] <;> ring

@[simp] theorem R_ab (a b c : ℚ) (X : EdgeCochain) (i : V9) (j : V11) :
    R a b c X (Sum.inl (i, j)) = a * X (Sum.inl (i, j)) := rfl

@[simp] theorem R_ac (a b c : ℚ) (X : EdgeCochain) (i : V9) (k : V13) :
    R a b c X (Sum.inr (Sum.inl (i, k))) =
      b * X (Sum.inr (Sum.inl (i, k))) := rfl

@[simp] theorem R_bc (a b c : ℚ) (X : EdgeCochain) (j : V11) (k : V13) :
    R a b c X (Sum.inr (Sum.inr (j, k))) =
      c * X (Sum.inr (Sum.inr (j, k))) := rfl

theorem R_apply (a b c : ℚ) (X : EdgeCochain) (e : SceneEdge) :
    R a b c X e =
      match e with
      | Sum.inl _ => a * X e
      | Sum.inr (Sum.inl _) => b * X e
      | Sum.inr (Sum.inr _) => c * X e := rfl

/-- The bare-metric mismatch before restriction to `KPlus`. -/
def mismatch (a b c : ℚ) : EdgeCochain →ₗ[ℚ] VertexCochain :=
  BPlusLin.comp (R a b c)

/-- The A-CAP mismatch restricted to the literal unsigned kernel. -/
def mismatchOnK (a b c : ℚ) : KPlus →ₗ[ℚ] VertexCochain :=
  (mismatch a b c).comp KPlus.subtype

def lift9 (f : Balanced9) : VertexCochain := fun v =>
  match v with
  | Sum.inl i => f.1 i
  | Sum.inr _ => 0

def lift11 (f : Balanced11) : VertexCochain := fun v =>
  match v with
  | Sum.inl _ => 0
  | Sum.inr (Sum.inl j) => f.1 j
  | Sum.inr (Sum.inr _) => 0

def lift13 (f : Balanced13) : VertexCochain := fun v =>
  match v with
  | Sum.inl _ => 0
  | Sum.inr (Sum.inl _) => 0
  | Sum.inr (Sum.inr k) => f.1 k

/-- Standard `A₉` edge embedding into the unsigned kernel. -/
def A9 : Balanced9 →ₗ[ℚ] EdgeCochain where
  toFun f e :=
    match e with
    | Sum.inl (i, _) => 13 * f.1 i
    | Sum.inr (Sum.inl (i, _)) => -(11 : ℚ) * f.1 i
    | Sum.inr (Sum.inr _) => 0
  map_add' f g := by
    funext e
    rcases e with e | e | e <;> simp <;> ring
  map_smul' r f := by
    funext e
    rcases e with e | e | e <;> simp [smul_eq_mul] <;> ring

@[simp] theorem A9_ab (f : Balanced9) (i : V9) (j : V11) :
    A9 f (Sum.inl (i, j)) = 13 * f.1 i := rfl

@[simp] theorem A9_ac (f : Balanced9) (i : V9) (k : V13) :
    A9 f (Sum.inr (Sum.inl (i, k))) = -(11 : ℚ) * f.1 i := rfl

@[simp] theorem A9_bc (f : Balanced9) (j : V11) (k : V13) :
    A9 f (Sum.inr (Sum.inr (j, k))) = 0 := rfl

/-- Standard `A₁₁` edge embedding into the unsigned kernel. -/
def A11 : Balanced11 →ₗ[ℚ] EdgeCochain where
  toFun f e :=
    match e with
    | Sum.inl (_, j) => 13 * f.1 j
    | Sum.inr (Sum.inl _) => 0
    | Sum.inr (Sum.inr (j, _)) => -(9 : ℚ) * f.1 j
  map_add' f g := by
    funext e
    rcases e with e | e | e <;> simp <;> ring
  map_smul' r f := by
    funext e
    rcases e with e | e | e <;> simp [smul_eq_mul] <;> ring

@[simp] theorem A11_ab (f : Balanced11) (i : V9) (j : V11) :
    A11 f (Sum.inl (i, j)) = 13 * f.1 j := rfl

@[simp] theorem A11_ac (f : Balanced11) (i : V9) (k : V13) :
    A11 f (Sum.inr (Sum.inl (i, k))) = 0 := rfl

@[simp] theorem A11_bc (f : Balanced11) (j : V11) (k : V13) :
    A11 f (Sum.inr (Sum.inr (j, k))) = -(9 : ℚ) * f.1 j := rfl

/-- Standard `A₁₃` edge embedding into the unsigned kernel. -/
def A13 : Balanced13 →ₗ[ℚ] EdgeCochain where
  toFun f e :=
    match e with
    | Sum.inl _ => 0
    | Sum.inr (Sum.inl (_, k)) => 11 * f.1 k
    | Sum.inr (Sum.inr (_, k)) => -(9 : ℚ) * f.1 k
  map_add' f g := by
    funext e
    rcases e with e | e | e <;> simp <;> ring
  map_smul' r f := by
    funext e
    rcases e with e | e | e <;> simp [smul_eq_mul] <;> ring

@[simp] theorem A13_ab (f : Balanced13) (i : V9) (j : V11) :
    A13 f (Sum.inl (i, j)) = 0 := rfl

@[simp] theorem A13_ac (f : Balanced13) (i : V9) (k : V13) :
    A13 f (Sum.inr (Sum.inl (i, k))) = 11 * f.1 k := rfl

@[simp] theorem A13_bc (f : Balanced13) (j : V11) (k : V13) :
    A13 f (Sum.inr (Sum.inr (j, k))) = -(9 : ℚ) * f.1 k := rfl

@[simp] theorem lift9_apply (f : Balanced9) (i : V9) :
    lift9 f (Sum.inl i) = f.1 i := rfl

@[simp] theorem lift9_apply_B (f : Balanced9) (j : V11) :
    lift9 f (Sum.inr (Sum.inl j)) = 0 := rfl

@[simp] theorem lift9_apply_C (f : Balanced9) (k : V13) :
    lift9 f (Sum.inr (Sum.inr k)) = 0 := rfl

@[simp] theorem lift11_apply_A (f : Balanced11) (i : V9) :
    lift11 f (Sum.inl i) = 0 := rfl

@[simp] theorem lift11_apply (f : Balanced11) (j : V11) :
    lift11 f (Sum.inr (Sum.inl j)) = f.1 j := rfl

@[simp] theorem lift11_apply_C (f : Balanced11) (k : V13) :
    lift11 f (Sum.inr (Sum.inr k)) = 0 := rfl

@[simp] theorem lift13_apply_A (f : Balanced13) (i : V9) :
    lift13 f (Sum.inl i) = 0 := rfl

@[simp] theorem lift13_apply_B (f : Balanced13) (j : V11) :
    lift13 f (Sum.inr (Sum.inl j)) = 0 := rfl

@[simp] theorem lift13_apply (f : Balanced13) (k : V13) :
    lift13 f (Sum.inr (Sum.inr k)) = f.1 k := rfl

theorem A9_mem_KPlus (f : Balanced9) : A9 f ∈ KPlus := by
  have h13 : (∑ x : V9, 13 * f.1 x) = 0 := by
    rw [← Finset.mul_sum, balanced_sum f, mul_zero]
  have h11 : (∑ x : V9, -(11 : ℚ) * f.1 x) = 0 := by
    rw [← Finset.mul_sum, balanced_sum f, mul_zero]
  have h11pos : (∑ x : V9, 11 * f.1 x) = 0 := by
    rw [← Finset.mul_sum, balanced_sum f, mul_zero]
  apply LinearMap.mem_ker.mpr
  rw [BPlusLin_apply]
  funext v
  rcases v with i | j | k
  · simp only [BPlus, A9_ab, A9_ac, A9_bc]
    simp [Finset.sum_const, Finset.card_fin, nsmul_eq_mul]
    ring
  · simp only [BPlus, A9_ab, A9_ac, A9_bc]
    simp [h13]
  · simp only [BPlus, A9_ab, A9_ac, A9_bc]
    simp [h11pos]

theorem A11_mem_KPlus (f : Balanced11) : A11 f ∈ KPlus := by
  have h13 : (∑ x : V11, 13 * f.1 x) = 0 := by
    rw [← Finset.mul_sum, balanced_sum f, mul_zero]
  have h9 : (∑ x : V11, -(9 : ℚ) * f.1 x) = 0 := by
    rw [← Finset.mul_sum, balanced_sum f, mul_zero]
  have h9pos : (∑ x : V11, 9 * f.1 x) = 0 := by
    rw [← Finset.mul_sum, balanced_sum f, mul_zero]
  apply LinearMap.mem_ker.mpr
  rw [BPlusLin_apply]
  funext v
  rcases v with i | j | k
  · simp only [BPlus, A11_ab, A11_ac, A11_bc]
    simp [h13]
  · simp only [BPlus, A11_ab, A11_ac, A11_bc]
    simp [Finset.sum_const, Finset.card_fin, nsmul_eq_mul]
    ring
  · simp only [BPlus, A11_ab, A11_ac, A11_bc]
    simp [h9pos]

theorem A13_mem_KPlus (f : Balanced13) : A13 f ∈ KPlus := by
  have h11 : (∑ x : V13, 11 * f.1 x) = 0 := by
    rw [← Finset.mul_sum, balanced_sum f, mul_zero]
  have h9 : (∑ x : V13, -(9 : ℚ) * f.1 x) = 0 := by
    rw [← Finset.mul_sum, balanced_sum f, mul_zero]
  have h9pos : (∑ x : V13, 9 * f.1 x) = 0 := by
    rw [← Finset.mul_sum, balanced_sum f, mul_zero]
  apply LinearMap.mem_ker.mpr
  rw [BPlusLin_apply]
  funext v
  rcases v with i | j | k
  · simp only [BPlus, A13_ab, A13_ac, A13_bc]
    simp [h11]
  · simp only [BPlus, A13_ab, A13_ac, A13_bc]
    simp [h9pos]
  · simp only [BPlus, A13_ab, A13_ac, A13_bc]
    simp [Finset.sum_const, Finset.card_fin, nsmul_eq_mul]
    ring

theorem A9_injective : Function.Injective A9 := by
  intro f g h
  apply Subtype.ext
  funext i
  have hi := congrFun h (Sum.inl (i, (0 : V11)))
  change 13 * f.1 i = 13 * g.1 i at hi
  linarith

theorem A11_injective : Function.Injective A11 := by
  intro f g h
  apply Subtype.ext
  funext j
  have hj := congrFun h (Sum.inl ((0 : V9), j))
  change 13 * f.1 j = 13 * g.1 j at hj
  linarith

theorem A13_injective : Function.Injective A13 := by
  intro f g h
  apply Subtype.ext
  funext k
  have hk := congrFun h (Sum.inr (Sum.inl ((0 : V9), k)))
  change 11 * f.1 k = 11 * g.1 k at hk
  linarith

theorem A9_range_finrank :
    Module.finrank ℚ (LinearMap.range A9) = 8 := by
  rw [LinearMap.finrank_range_of_inj A9_injective]
  exact balanced9_finrank

theorem A11_range_finrank :
    Module.finrank ℚ (LinearMap.range A11) = 10 := by
  rw [LinearMap.finrank_range_of_inj A11_injective]
  exact balanced11_finrank

theorem A13_range_finrank :
    Module.finrank ℚ (LinearMap.range A13) = 12 := by
  rw [LinearMap.finrank_range_of_inj A13_injective]
  exact balanced13_finrank

/-! ## Exact standard-sector residues -/

theorem mismatch_A9 (a b c : ℚ) (f : Balanced9) :
    mismatch a b c (A9 f) = 143 * (a - b) • lift9 f := by
  have h13 : (∑ x : V9, 13 * f.1 x) = 0 := by
    rw [← Finset.mul_sum, balanced_sum f, mul_zero]
  have h11 : (∑ x : V9, -(11 : ℚ) * f.1 x) = 0 := by
    rw [← Finset.mul_sum, balanced_sum f, mul_zero]
  have h13a : (∑ x : V9, a * (13 * f.1 x)) = 0 := by
    calc
      _ = a * (∑ x : V9, 13 * f.1 x) := by
        symm
        rw [Finset.mul_sum]
      _ = 0 := by rw [h13]; simp
  have h11b : (∑ x : V9, b * (-(11 : ℚ) * f.1 x)) = 0 := by
    calc
      _ = b * (∑ x : V9, -(11 : ℚ) * f.1 x) := by
        symm
        rw [Finset.mul_sum]
      _ = 0 := by rw [h11]; simp
  rw [mismatch, LinearMap.comp_apply, BPlusLin_apply]
  funext v
  rcases v with i | j | k
  · simp only [BPlus, R_ab, R_ac, R_bc, A9_ab, A9_ac, A9_bc,
      lift9_apply, lift9_apply_B, lift9_apply_C, Pi.smul_apply, smul_eq_mul]
    simp [Finset.sum_const, Finset.card_fin, nsmul_eq_mul]
    ring
  · simp only [BPlus, R_ab, R_ac, R_bc, A9_ab, A9_ac, A9_bc,
      lift9_apply, lift9_apply_B, lift9_apply_C, Pi.smul_apply, smul_eq_mul]
    rw [h13a]
    simp
  · simp only [BPlus, R_ab, R_ac, R_bc, A9_ab, A9_ac, A9_bc,
      lift9_apply, lift9_apply_B, lift9_apply_C, Pi.smul_apply, smul_eq_mul]
    rw [h11b]
    simp

theorem mismatch_A11 (a b c : ℚ) (f : Balanced11) :
    mismatch a b c (A11 f) = 117 * (a - c) • lift11 f := by
  have h13 : (∑ x : V11, 13 * f.1 x) = 0 := by
    rw [← Finset.mul_sum, balanced_sum f, mul_zero]
  have h9 : (∑ x : V11, -(9 : ℚ) * f.1 x) = 0 := by
    rw [← Finset.mul_sum, balanced_sum f, mul_zero]
  have h13a : (∑ x : V11, a * (13 * f.1 x)) = 0 := by
    calc
      _ = a * (∑ x : V11, 13 * f.1 x) := by
        symm
        rw [Finset.mul_sum]
      _ = 0 := by rw [h13]; simp
  have h9c : (∑ x : V11, c * (-(9 : ℚ) * f.1 x)) = 0 := by
    calc
      _ = c * (∑ x : V11, -(9 : ℚ) * f.1 x) := by
        symm
        rw [Finset.mul_sum]
      _ = 0 := by rw [h9]; simp
  rw [mismatch, LinearMap.comp_apply, BPlusLin_apply]
  funext v
  rcases v with i | j | k
  · simp only [BPlus, R_ab, R_ac, R_bc, A11_ab, A11_ac, A11_bc,
      lift11_apply_A, lift11_apply, lift11_apply_C, Pi.smul_apply, smul_eq_mul]
    rw [h13a]
    simp
  · simp only [BPlus, R_ab, R_ac, R_bc, A11_ab, A11_ac, A11_bc,
      lift11_apply_A, lift11_apply, lift11_apply_C, Pi.smul_apply, smul_eq_mul]
    simp [Finset.sum_const, Finset.card_fin, nsmul_eq_mul]
    ring
  · simp only [BPlus, R_ab, R_ac, R_bc, A11_ab, A11_ac, A11_bc,
      lift11_apply_A, lift11_apply, lift11_apply_C, Pi.smul_apply, smul_eq_mul]
    rw [h9c]
    simp

theorem mismatch_A13 (a b c : ℚ) (f : Balanced13) :
    mismatch a b c (A13 f) = 99 * (b - c) • lift13 f := by
  have h11 : (∑ x : V13, 11 * f.1 x) = 0 := by
    rw [← Finset.mul_sum, balanced_sum f, mul_zero]
  have h9 : (∑ x : V13, -(9 : ℚ) * f.1 x) = 0 := by
    rw [← Finset.mul_sum, balanced_sum f, mul_zero]
  have h11b : (∑ x : V13, b * (11 * f.1 x)) = 0 := by
    calc
      _ = b * (∑ x : V13, 11 * f.1 x) := by
        symm
        rw [Finset.mul_sum]
      _ = 0 := by rw [h11]; simp
  have h9c : (∑ x : V13, c * (-(9 : ℚ) * f.1 x)) = 0 := by
    calc
      _ = c * (∑ x : V13, -(9 : ℚ) * f.1 x) := by
        symm
        rw [Finset.mul_sum]
      _ = 0 := by rw [h9]; simp
  rw [mismatch, LinearMap.comp_apply, BPlusLin_apply]
  funext v
  rcases v with i | j | k
  · simp only [BPlus, R_ab, R_ac, R_bc, A13_ab, A13_ac, A13_bc,
      lift13_apply_A, lift13_apply_B, lift13_apply, Pi.smul_apply, smul_eq_mul]
    rw [h11b]
    simp
  · simp only [BPlus, R_ab, R_ac, R_bc, A13_ab, A13_ac, A13_bc,
      lift13_apply_A, lift13_apply_B, lift13_apply, Pi.smul_apply, smul_eq_mul]
    rw [h9c]
    simp
  · simp only [BPlus, R_ab, R_ac, R_bc, A13_ab, A13_ac, A13_bc,
      lift13_apply_A, lift13_apply_B, lift13_apply, Pi.smul_apply, smul_eq_mul]
    simp [Finset.sum_const, Finset.card_fin, nsmul_eq_mul]
    ring

/-! The following are the minimum image/finrank corollaries for the three
standard sectors.  They do not assert the full conditional rank stratification
of the mismatch on all of `KPlus`. -/

def mismatchA9 (a b c : ℚ) : Balanced9 →ₗ[ℚ] VertexCochain :=
  (mismatch a b c).comp A9

def mismatchA11 (a b c : ℚ) : Balanced11 →ₗ[ℚ] VertexCochain :=
  (mismatch a b c).comp A11

def mismatchA13 (a b c : ℚ) : Balanced13 →ₗ[ℚ] VertexCochain :=
  (mismatch a b c).comp A13

theorem mismatchA9_injective_of_ne {a b c : ℚ} (h : a ≠ b) :
    Function.Injective (mismatchA9 a b c) := by
  intro f g hfg
  apply Subtype.ext
  funext i
  change mismatch a b c (A9 f) = mismatch a b c (A9 g) at hfg
  rw [mismatch_A9, mismatch_A9] at hfg
  have hi := congrFun hfg (Sum.inl i)
  simp [lift9, Pi.smul_apply] at hi
  exact hi.resolve_right (sub_ne_zero.mpr h)

theorem mismatchA11_injective_of_ne {a b c : ℚ} (h : a ≠ c) :
    Function.Injective (mismatchA11 a b c) := by
  intro f g hfg
  apply Subtype.ext
  funext j
  change mismatch a b c (A11 f) = mismatch a b c (A11 g) at hfg
  rw [mismatch_A11, mismatch_A11] at hfg
  have hj := congrFun hfg (Sum.inr (Sum.inl j))
  simp [lift11, Pi.smul_apply] at hj
  exact hj.resolve_right (sub_ne_zero.mpr h)

theorem mismatchA13_injective_of_ne {a b c : ℚ} (h : b ≠ c) :
    Function.Injective (mismatchA13 a b c) := by
  intro f g hfg
  apply Subtype.ext
  funext k
  change mismatch a b c (A13 f) = mismatch a b c (A13 g) at hfg
  rw [mismatch_A13, mismatch_A13] at hfg
  have hk := congrFun hfg (Sum.inr (Sum.inr k))
  simp [lift13, Pi.smul_apply] at hk
  exact hk.resolve_right (sub_ne_zero.mpr h)

theorem mismatchA9_range_finrank_of_ne {a b c : ℚ} (h : a ≠ b) :
    Module.finrank ℚ (LinearMap.range (mismatchA9 a b c)) = 8 := by
  rw [LinearMap.finrank_range_of_inj (mismatchA9_injective_of_ne h)]
  exact balanced9_finrank

theorem mismatchA11_range_finrank_of_ne {a b c : ℚ} (h : a ≠ c) :
    Module.finrank ℚ (LinearMap.range (mismatchA11 a b c)) = 10 := by
  rw [LinearMap.finrank_range_of_inj (mismatchA11_injective_of_ne h)]
  exact balanced11_finrank

theorem mismatchA13_range_finrank_of_ne {a b c : ℚ} (h : b ≠ c) :
    Module.finrank ℚ (LinearMap.range (mismatchA13 a b c)) = 12 := by
  rw [LinearMap.finrank_range_of_inj (mismatchA13_injective_of_ne h)]
  exact balanced13_finrank

/-! ## Tensor-sector annihilation -/

theorem mismatch_zero_on_SceneTensorBlock
    (a b c : ℚ) (z : EdgeCochain) (hz : z ∈ SceneTensorBlock) :
    mismatch a b c z = 0 := by
  rw [mismatch, LinearMap.comp_apply, BPlusLin_apply]
  funext v
  rcases v with i | j | k
  · simp only [BPlus, R_ab, R_ac, R_bc]
    have hAB : (∑ x : V11, a * z (Sum.inl (i, x))) =
        a * sceneABRowMarginal z i := by
      symm
      simp only [sceneABRowMarginal]
      rw [Finset.mul_sum]
    have hAC : (∑ x : V13, b * z (Sum.inr (Sum.inl (i, x)))) =
        b * sceneACRowMarginal z i := by
      symm
      simp only [sceneACRowMarginal]
      rw [Finset.mul_sum]
    rw [hAB, hAC]
    rw [hz.1 i, hz.2.2.1 i]
    simp
  · simp only [BPlus, R_ab, R_ac, R_bc]
    have hAB : (∑ x : V9, a * z (Sum.inl (x, j))) =
        a * sceneABColumnMarginal z j := by
      symm
      simp only [sceneABColumnMarginal]
      rw [Finset.mul_sum]
    have hBC : (∑ x : V13, c * z (Sum.inr (Sum.inr (j, x)))) =
        c * sceneBCRowMarginal z j := by
      symm
      simp only [sceneBCRowMarginal]
      rw [Finset.mul_sum]
    rw [hAB, hBC]
    rw [hz.2.1 j, hz.2.2.2.2.1 j]
    simp
  · simp only [BPlus, R_ab, R_ac, R_bc]
    have hAC : (∑ x : V9, b * z (Sum.inr (Sum.inl (x, k)))) =
        b * sceneACColumnMarginal z k := by
      symm
      simp only [sceneACColumnMarginal]
      rw [Finset.mul_sum]
    have hBC : (∑ x : V11, c * z (Sum.inr (Sum.inr (x, k)))) =
        c * sceneBCColumnMarginal z k := by
      symm
      simp only [sceneBCColumnMarginal]
      rw [Finset.mul_sum]
    rw [hAC, hBC]
    rw [hz.2.2.2.1 k, hz.2.2.2.2.2 k]
    simp

/-! ## Uniformity criterion and positive-weight corollary -/

def balanced9Witness : Balanced9 :=
  ⟨fun i => if i = 0 then 1 else if i = 1 then -1 else 0, by
    apply LinearMap.mem_ker.mpr
    norm_num [zoneSumMap, Fin.sum_univ_succ] <;> simp⟩

def balanced11Witness : Balanced11 :=
  ⟨fun i => if i = 0 then 1 else if i = 1 then -1 else 0, by
    apply LinearMap.mem_ker.mpr
    norm_num [zoneSumMap, Fin.sum_univ_succ] <;> simp⟩

def balanced13Witness : Balanced13 :=
  ⟨fun i => if i = 0 then 1 else if i = 1 then -1 else 0, by
    apply LinearMap.mem_ker.mpr
    norm_num [zoneSumMap, Fin.sum_univ_succ] <;> simp⟩

theorem mismatchOnK_zero_iff (a b c : ℚ) :
    (∀ X : KPlus, mismatchOnK a b c X = 0) ↔ a = b ∧ b = c := by
  constructor
  · intro h
    have h9 := h ⟨A9 balanced9Witness, A9_mem_KPlus balanced9Witness⟩
    have h11 := h ⟨A11 balanced11Witness, A11_mem_KPlus balanced11Witness⟩
    have h9' : mismatch a b c (A9 balanced9Witness) = 0 := h9
    have h11' : mismatch a b c (A11 balanced11Witness) = 0 := h11
    rw [mismatch_A9] at h9'
    rw [mismatch_A11] at h11'
    have h9v := congrFun h9' (Sum.inl (0 : V9))
    have h11v := congrFun h11' (Sum.inr (Sum.inl (0 : V11)))
    simp [lift9, lift11] at h9v h11v
    have hab0 : a - b = 0 := h9v.resolve_right (by
      norm_num [balanced9Witness])
    have hac0 : a - c = 0 := h11v.resolve_right (by
      norm_num [balanced11Witness])
    constructor <;> linarith
  · rintro ⟨hab, hbc⟩ X
    have hac : a = c := hab.trans hbc
    have hR : R a b c (X : EdgeCochain) = a • (X : EdgeCochain) := by
      funext e
      rcases e with e | e | e <;> simp [R, hab, hbc, hac]
    change BPlusLin (R a b c (X : EdgeCochain)) = 0
    rw [hR, map_smul]
    rw [LinearMap.mem_ker.mp X.property]
    simp

theorem mismatch_zero_on_K_iff_uniform (a b c : ℚ) :
    (∀ X : KPlus, mismatchOnK a b c X = 0) ↔ a = b ∧ b = c :=
  mismatchOnK_zero_iff a b c

/-- Positive block weights and their blockwise inverse metric. -/
def WInverse (x y z : ℚ) : EdgeCochain →ₗ[ℚ] EdgeCochain :=
  R x⁻¹ y⁻¹ z⁻¹

theorem positive_weight_mismatch_zero_iff
    (x y z : ℚ) (hx : 0 < x) (hy : 0 < y) (hz : 0 < z) :
    (∀ X : KPlus, BPlusLin (WInverse x y z (X : EdgeCochain)) = 0) ↔
      x = y ∧ y = z := by
  rw [show (∀ X : KPlus,
      BPlusLin (WInverse x y z (X : EdgeCochain)) = 0) ↔
      (∀ X : KPlus, mismatchOnK x⁻¹ y⁻¹ z⁻¹ X = 0) by
        rfl]
  rw [mismatchOnK_zero_iff]
  constructor
  · rintro ⟨hxy, hyz⟩
    constructor
    · exact (inv_inj.mp hxy)
    · exact (inv_inj.mp hyz)
  · rintro ⟨hxy, hyz⟩
    constructor
    · simpa using congrArg (fun q : ℚ => q⁻¹) hxy
    · simpa using congrArg (fun q : ℚ => q⁻¹) hyz

end D0.Gravity.A1RieszMismatch
