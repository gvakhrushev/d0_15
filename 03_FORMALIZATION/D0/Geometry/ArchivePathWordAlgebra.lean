import Mathlib.Algebra.Algebra.Basic
import Mathlib.Algebra.Algebra.Equiv
import Mathlib.Algebra.BigOperators.Pi
import Mathlib.Algebra.Ring.MinimalAxioms
import Mathlib.Data.Fintype.EquivFin
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.LinearAlgebra.FreeModule.Finite.Matrix
import Mathlib.Tactic
import D0.Geometry.ArchiveFiniteCartanLieClosureNoGo

/-!
# Scalar crossed product and syntactic path words

For a finite additive group `X`, the monomials `M_f U^a` multiply by

`(M_f U^a)(M_g U^b) = M_{f · (U^a g)} U^{a+b}`.

Evaluating them on `K^X` is an algebra equivalence with `End_K(K^X)`, of
dimension `n^2`. That associative envelope is not the Lie closure of dimension
`n(n-1)`.

Separately, `ChainPath` is the universal path type on a directed graph. It is
not a finite type when the graph has a loop, and it is not quotiented by
endpoints. Endpoint evaluation is valid exactly when every loop holonomy is
trivial.

`PathExprCost` records term count and maximum word length. A product of
radius-one letters can have arbitrarily large word length, so factorized
locality is not a uniform bound on compressed support. Bracket depth adds word
lengths, so a fixed word length is not preserved.
-/

namespace D0.Geometry

open D0

variable {K X : Type*} [Field K] [AddCommGroup X] [Fintype X] [DecidableEq X]

def shiftOp (a : X) : (X → K) →ₗ[K] (X → K) where
  toFun f z := f (z + a)
  map_add' f g := by ext z; simp [Pi.add_apply]
  map_smul' c f := by ext z; simp

def mulOp (f : X → K) : (X → K) →ₗ[K] (X → K) where
  toFun g z := f z * g z
  map_add' g h := by ext z; simp [mul_add]
  map_smul' c g := by ext z; simp [mul_left_comm, mul_assoc]

theorem shiftOp_add (a b : X) :
    (shiftOp (a + b)).comp (LinearMap.id : (X → K) →ₗ[K] (X → K)) =
      (shiftOp a).comp (shiftOp b) := by
  ext f z
  simp [shiftOp, add_assoc]

theorem shift_mul_commute (a : X) (g : X → K) :
    (shiftOp a).comp (mulOp g) = (mulOp (shiftOp a g)).comp (shiftOp a) := by
  ext f z
  simp [shiftOp, mulOp]

def monomial (f : X → K) (a : X) : (X → K) →ₗ[K] (X → K) :=
  (mulOp f).comp (shiftOp a)

theorem monomial_apply (f : X → K) (a z : X) (g : X → K) :
    monomial f a g z = f z * g (z + a) := rfl

theorem crossed_monomial_mul (f g : X → K) (a b : X) :
    (monomial f a).comp (monomial g b) =
      monomial (fun z => f z * g (z + a)) (a + b) := by
  ext h z
  simp [monomial, mulOp, shiftOp, add_assoc, mul_assoc]

theorem matrixUnit_eq_delta_shift (x y : X) :
    matrixUnit (K := K) x y = monomial (Pi.single x (1 : K)) (y - x) := by
  apply LinearMap.ext
  intro f
  funext z
  by_cases hz : z = x
  · subst z
    simp [matrixUnit_apply, monomial_apply, Pi.single_apply, sub_eq_add_neg]
  · simp [matrixUnit_apply, monomial_apply, Pi.single_apply, hz]

/-- Coefficients of `∑_a M_{f_a} U^a`. Multiplication is the crossed product,
not the pointwise product of functions. -/
@[ext] structure ScalarCrossed (K X : Type*) where
  coeff : X → X → K

namespace ScalarCrossed

variable {K X : Type*} [Field K] [AddCommGroup X] [Fintype X] [DecidableEq X]

instance : Zero (ScalarCrossed K X) := ⟨⟨0⟩⟩

@[simp] theorem coeff_zero (a z : X) : (0 : ScalarCrossed K X).coeff a z = 0 := rfl

instance : Add (ScalarCrossed K X) := ⟨fun c d => ⟨c.coeff + d.coeff⟩⟩

instance : Neg (ScalarCrossed K X) := ⟨fun c => ⟨-c.coeff⟩⟩

instance : SMul K (ScalarCrossed K X) := ⟨fun t c => ⟨t • c.coeff⟩⟩

instance : Mul (ScalarCrossed K X) :=
  ⟨fun c d => ⟨fun a z => ∑ b : X, c.coeff b z * d.coeff (a - b) (z + b)⟩⟩

instance : One (ScalarCrossed K X) := ⟨⟨fun a _ => if a = 0 then 1 else 0⟩⟩

@[simp] theorem coeff_add (c d : ScalarCrossed K X) :
    (c + d).coeff = c.coeff + d.coeff := rfl

@[simp] theorem coeff_neg (c : ScalarCrossed K X) : (-c).coeff = -c.coeff := rfl

@[simp] theorem coeff_smul (t : K) (c : ScalarCrossed K X) :
    (t • c).coeff = t • c.coeff := rfl

theorem mul_coeff (c d : ScalarCrossed K X) (a z : X) :
    (c * d).coeff a z = ∑ b : X, c.coeff b z * d.coeff (a - b) (z + b) := rfl

theorem one_coeff (a z : X) :
    (1 : ScalarCrossed K X).coeff a z = if a = 0 then 1 else 0 := rfl

theorem one_mul (c : ScalarCrossed K X) : (1 : ScalarCrossed K X) * c = c := by
  ext a z
  rw [mul_coeff]
  rw [Fintype.sum_eq_single (0 : X)]
  · simp [one_coeff, sub_zero, add_zero]
  · intro b hb
    simp [one_coeff, hb]

theorem mul_one (c : ScalarCrossed K X) : c * (1 : ScalarCrossed K X) = c := by
  ext a z
  rw [mul_coeff]
  rw [Fintype.sum_eq_single a]
  · simp [one_coeff, sub_self]
  · intro b hb
    have hne : a - b ≠ 0 := by
      intro h
      exact hb (eq_of_sub_eq_zero h).symm
    simp [one_coeff, hne]

theorem crossed_mul_assoc (c d e : ScalarCrossed K X) : c * d * e = c * (d * e) := by
  ext a z
  simp only [mul_coeff, Finset.sum_mul, Finset.mul_sum, mul_assoc]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl ?_
  intro b _
  simpa only [mul_assoc] using (Fintype.sum_equiv (Equiv.addRight b)
    (fun u => c.coeff b z * d.coeff u (z + b) *
      e.coeff ((a - b) - u) ((z + b) + u))
    (fun t => c.coeff b z * d.coeff (t - b) (z + b) * e.coeff (a - t) (z + t))
    (by
      intro u
      simp [add_sub_cancel_right, sub_sub, add_assoc, add_left_comm, add_comm])).symm

theorem crossed_mul_add (c d e : ScalarCrossed K X) : c * (d + e) = c * d + c * e := by
  ext a z
  simp only [mul_coeff, coeff_add, Pi.add_apply, mul_add, Finset.sum_add_distrib]

theorem crossed_add_mul (c d e : ScalarCrossed K X) : (c + d) * e = c * e + d * e := by
  ext a z
  simp only [mul_coeff, coeff_add, Pi.add_apply, add_mul, Finset.sum_add_distrib]

instance : Ring (ScalarCrossed K X) :=
  Ring.ofMinimalAxioms
    (fun c d e => by ext a z; simp [coeff_add, Pi.add_apply, add_assoc])
    (fun c => by ext a z; simp [coeff_zero, coeff_add, Pi.zero_apply, Pi.add_apply])
    (fun c => by
      ext a z
      simp [coeff_neg, coeff_add, coeff_zero, Pi.neg_apply, Pi.add_apply, Pi.zero_apply,
        neg_add_cancel])
    crossed_mul_assoc one_mul mul_one crossed_mul_add crossed_add_mul

instance : Module K (ScalarCrossed K X) where
  one_smul c := by ext a z; simp [coeff_smul, Pi.smul_apply]
  mul_smul r s c := by ext a z; simp [coeff_smul, Pi.smul_apply]; ring
  smul_zero r := by ext a z; simp [coeff_smul, coeff_zero, Pi.smul_apply]
  smul_add r c d := by ext a z; simp [coeff_smul, coeff_add, Pi.smul_apply, Pi.add_apply]; ring
  add_smul r s c := by ext a z; simp [coeff_smul, Pi.smul_apply]; ring
  zero_smul c := by ext a z; simp [coeff_smul, coeff_zero, Pi.smul_apply]

theorem smul_mul (r : K) (c d : ScalarCrossed K X) : r • c * d = r • (c * d) := by
  ext a z
  simp only [mul_coeff, coeff_smul, Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro b _
  ring

theorem mul_smul_comm (r : K) (c d : ScalarCrossed K X) : c * r • d = r • (c * d) := by
  ext a z
  simp only [mul_coeff, coeff_smul, Pi.smul_apply, smul_eq_mul, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro b _
  ring

instance : Algebra K (ScalarCrossed K X) := Algebra.ofModule smul_mul mul_smul_comm

def crossedToEnd (c : ScalarCrossed K X) : Module.End K (X → K) :=
  ∑ a : X, monomial (c.coeff a) a

theorem monomial_add (f g : X → K) (a : X) :
    monomial (f + g) a = monomial f a + monomial g a := by
  apply LinearMap.ext
  intro h
  funext z
  simp [monomial_apply, add_mul]

theorem monomial_smul (t : K) (f : X → K) (a : X) :
    monomial (t • f) a = t • monomial f a := by
  apply LinearMap.ext
  intro h
  funext z
  simp [monomial_apply, Pi.smul_apply, smul_eq_mul]
  ring

theorem crossedToEnd_apply (c : ScalarCrossed K X) (f : X → K) (z : X) :
    crossedToEnd c f z = ∑ a : X, c.coeff a z * f (z + a) := by
  rw [crossedToEnd, LinearMap.sum_apply, Finset.sum_apply]
  simp_rw [monomial_apply]

def endToCrossed (A : Module.End K (X → K)) : ScalarCrossed K X :=
  ⟨fun a z => A (Pi.single (z + a) (1 : K)) z⟩

theorem endToCrossed_crossedToEnd (c : ScalarCrossed K X) :
    endToCrossed (crossedToEnd c) = c := by
  ext a z
  dsimp [endToCrossed]
  rw [crossedToEnd_apply]
  rw [Fintype.sum_eq_single a]
  · rw [Pi.single_eq_same]
    simp
  · intro b hb
    have hne : z + b ≠ z + a := fun h => hb (add_left_cancel h)
    rw [Pi.single_eq_of_ne hne]
    simp

theorem crossedToEnd_endToCrossed (A : Module.End K (X → K)) :
    crossedToEnd (endToCrossed A) = A := by
  apply LinearMap.ext
  intro g
  funext z
  rw [crossedToEnd_apply, endToCrossed]
  have hg : g = ∑ y : X, g y • Pi.single y (1 : K) := pi_eq_sum_univ' g
  have hR : A g z = ∑ y : X, g y * A (Pi.single y (1 : K)) z := by
    calc
      A g z = A (∑ y : X, g y • Pi.single y (1 : K)) z :=
        congrArg (fun v : X → K => A v z) hg
      _ = (∑ y : X, A (g y • Pi.single y (1 : K))) z := by rw [map_sum]
      _ = ∑ y : X, g y * A (Pi.single y (1 : K)) z := by
        rw [Finset.sum_apply]
        apply Finset.sum_congr rfl
        intro y _
        simp [LinearMap.map_smul, Pi.smul_apply, smul_eq_mul]
  rw [hR]
  refine Fintype.sum_equiv (Equiv.addLeft z)
      (fun a => A (Pi.single (z + a) (1 : K)) z * g (z + a))
      (fun y => g y * A (Pi.single y (1 : K)) z) ?_
  intro a
  simp [mul_comm]

theorem crossedToEnd_one : crossedToEnd (1 : ScalarCrossed K X) = 1 := by
  apply LinearMap.ext
  intro f
  funext z
  rw [crossedToEnd_apply, Module.End.one_apply]
  rw [Fintype.sum_eq_single (0 : X)]
  · simp [one_coeff]
  · intro a ha
    simp [one_coeff, ha]

theorem crossedToEnd_mul (c d : ScalarCrossed K X) :
    crossedToEnd (c * d) = crossedToEnd c * crossedToEnd d := by
  apply LinearMap.ext
  intro f
  funext z
  rw [Module.End.mul_apply, crossedToEnd_apply]
  simp_rw [crossedToEnd_apply, mul_coeff, Finset.sum_mul, Finset.mul_sum, mul_assoc]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl ?_
  intro b _
  simpa [mul_assoc] using
    (Fintype.sum_equiv (Equiv.addRight b)
      (fun u => c.coeff b z * d.coeff u (z + b) * f ((z + b) + u))
      (fun t => c.coeff b z * d.coeff (t - b) (z + b) * f (z + t))
      (by
        intro u
        simp [add_sub_cancel_right, add_assoc, add_left_comm, add_comm])).symm

def coeffLinear : ScalarCrossed K X ≃ₗ[K] (X → X → K) where
  toFun c := c.coeff
  invFun φ := ⟨φ⟩
  map_add' _ _ := rfl
  map_smul' _ _ := rfl
  left_inv _ := rfl
  right_inv _ := rfl

noncomputable def crossedLinear : ScalarCrossed K X ≃ₗ[K] Module.End K (X → K) where
  toFun := crossedToEnd
  invFun := endToCrossed
  map_add' c d := by
    simp [crossedToEnd, coeff_add, monomial_add, Finset.sum_add_distrib]
  map_smul' t c := by
    simp [crossedToEnd, coeff_smul, monomial_smul, Finset.smul_sum]
  left_inv := endToCrossed_crossedToEnd
  right_inv := crossedToEnd_endToCrossed

/-- Evaluation `K^X ⋊ X ≃ End_K(K^X)`. -/
noncomputable def crossedEval : ScalarCrossed K X ≃ₐ[K] Module.End K (X → K) :=
  AlgEquiv.ofLinearEquiv crossedLinear crossedToEnd_one crossedToEnd_mul

theorem crossed_finrank :
    Module.finrank K (ScalarCrossed K X) = Fintype.card X * Fintype.card X := by
  rw [LinearEquiv.finrank_eq (coeffLinear (K := K) (X := X)), Module.finrank_pi_fintype]
  simp [Module.finrank_fintype_fun_eq_card, Finset.sum_const, Finset.card_univ, smul_eq_mul]

/-- The associative envelope has dimension `n^2`, while the scalar Lie closure has
dimension `n(n-1)`. -/
theorem crossed_finrank_ne_lie_closure (hX : 0 < Fintype.card X) :
    Module.finrank K (ScalarCrossed K X) ≠
      Module.finrank K (LinearMap.ker (evalConst (K := K) (X := X))) := by
  rw [crossed_finrank, finrank_annihilatesConstants]
  intro h
  have hn := Nat.eq_of_mul_eq_mul_left hX h
  omega

end ScalarCrossed

/-! ## Syntactic path words

`ChainPath` is the free path type of a directed graph. A loop makes it infinite,
so it is not a `Fintype`. Paths are not quotiented by their endpoints: that
quotient is valid exactly when every loop holonomy is trivial.
-/

universe u

inductive ChainPath {X : Type u} (E : X → X → Prop) : X → X → Type u
  | nil {x : X} : ChainPath E x x
  | cons {x y z : X} : E x y → ChainPath E y z → ChainPath E x z

namespace ChainPath

variable {X : Type u} {E : X → X → Prop}

def pathAppend : ∀ {x y z : X}, ChainPath E x y → ChainPath E y z → ChainPath E x z
  | _, _, _, nil, q => q
  | _, _, _, cons h p, q => cons h (pathAppend p q)

def pathReverse (revE : ∀ {x y : X}, E x y → E y x) :
    ∀ {x y : X}, ChainPath E x y → ChainPath E y x
  | _, _, nil => nil
  | _, _, cons h p => pathAppend (pathReverse revE p) (cons (revE h) nil)

variable {K V : Type*} [Field K] [AddCommGroup V] [Module K V]

/-- Pull transport: later edges act first, matching `pathTransport`. -/
def pathEval (link : ∀ {x y : X}, E x y → V ≃ₗ[K] V) :
    ∀ {x y : X}, ChainPath E x y → V ≃ₗ[K] V
  | _, _, nil => LinearEquiv.refl K V
  | _, _, cons h p => (pathEval link p).trans (link h)

theorem pathEval_append (link : ∀ {x y : X}, E x y → V ≃ₗ[K] V) :
    ∀ {x y z : X} (p : ChainPath E x y) (q : ChainPath E y z),
      pathEval link (pathAppend p q) = (pathEval link q).trans (pathEval link p)
  | _, _, _, nil, q => by simp [pathAppend, pathEval]
  | _, _, _, cons h p, q => by
      rw [pathAppend, pathEval, pathEval_append link p q]
      conv_rhs => rw [pathEval]
      exact LinearEquiv.trans_assoc _ _ _

theorem pathEval_reverse (link : ∀ {x y : X}, E x y → V ≃ₗ[K] V)
    (revE : ∀ {x y : X}, E x y → E y x)
    (hrev : ∀ {x y : X} (e : E x y), link (revE e) = (link e).symm)
    {x y : X} (p : ChainPath E x y) :
    pathEval link (pathReverse revE p) = (pathEval link p).symm := by
  induction p with
  | nil => simp [pathReverse, pathEval]
  | cons h p ih =>
      rw [pathReverse, pathEval_append, ih]
      simp only [pathEval, LinearEquiv.refl_trans, hrev h, LinearEquiv.trans_symm]

/-- Endpoint evaluation is well-defined if and only if every loop is trivial.
A nontrivial loop holonomy therefore blocks an endpoint-only quotient. -/
theorem pathEval_factors_pairGroupoid_iff_trivial_holonomy
    (link : ∀ {x y : X}, E x y → V ≃ₗ[K] V)
    (revE : ∀ {x y : X}, E x y → E y x)
    (hrev : ∀ {x y : X} (e : E x y), link (revE e) = (link e).symm) :
    (∀ x y (p q : ChainPath E x y), pathEval link p = pathEval link q) ↔
      ∀ x (p : ChainPath E x x), pathEval link p = LinearEquiv.refl K V := by
  constructor
  · intro h x p
    simpa [pathEval] using h x x p (nil : ChainPath E x x)
  · intro h x y p q
    have hloop := h x (pathAppend p (pathReverse revE q))
    rw [pathEval_append, pathEval_reverse link revE hrev] at hloop
    have htrans := congrArg (fun f => (pathEval link q).trans f) hloop
    simpa [LinearEquiv.trans_symm_cancel_left, LinearEquiv.trans_refl] using htrans

def pathLength : ∀ {x y : X}, ChainPath E x y → ℕ
  | _, _, nil => 0
  | _, _, cons _ p => pathLength p + 1

def loopWord {x : X} (h : E x x) : ℕ → ChainPath E x x
  | 0 => nil
  | n + 1 => cons h (loopWord h n)

theorem loopWord_length {x : X} (h : E x x) (n : ℕ) :
    pathLength (loopWord h n) = n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [loopWord, pathLength, ih]

theorem loopWord_injective {x : X} (h : E x x) : Function.Injective (loopWord h) := by
  intro m n hEq
  have := congrArg pathLength hEq
  simpa [loopWord_length] using this

theorem chainPath_loop_infinite {x : X} (h : E x x) : Infinite (ChainPath E x x) :=
  Infinite.of_injective (loopWord h) (loopWord_injective h)

end ChainPath

/-! ## Locality resources

`PathExprCost` counts terms and the longest word. Multiplying and bracketing add
word lengths, so a fixed word length is not preserved by bracket depth.

Factorized-local ≠ uniformly bounded compressed support: a product of radius-one
letters can have arbitrarily large word length.
-/

inductive PathExpr (α : Type*)
  | word : List α → PathExpr α
  | add : PathExpr α → PathExpr α → PathExpr α
  | mul : PathExpr α → PathExpr α → PathExpr α
  | bracket : PathExpr α → PathExpr α → PathExpr α
  | rev : PathExpr α → PathExpr α

structure PathExprCost where
  terms : ℕ
  maxWordLength : ℕ

structure LocalCircuitCost where
  gates : ℕ
  maxGateRadius : ℕ

def pathExprCost {α : Type*} : PathExpr α → PathExprCost
  | .word w => ⟨1, w.length⟩
  | .add a b =>
      let ca := pathExprCost a
      let cb := pathExprCost b
      ⟨ca.terms + cb.terms, max ca.maxWordLength cb.maxWordLength⟩
  | .mul a b =>
      let ca := pathExprCost a
      let cb := pathExprCost b
      ⟨ca.terms * cb.terms, ca.maxWordLength + cb.maxWordLength⟩
  | .bracket a b =>
      let ca := pathExprCost a
      let cb := pathExprCost b
      ⟨2 * ca.terms * cb.terms, ca.maxWordLength + cb.maxWordLength⟩
  | .rev a => pathExprCost a

theorem cost_add {α : Type*} (a b : PathExpr α) :
    (pathExprCost (.add a b)).terms = (pathExprCost a).terms + (pathExprCost b).terms ∧
      (pathExprCost (.add a b)).maxWordLength =
        max (pathExprCost a).maxWordLength (pathExprCost b).maxWordLength := by
  simp [pathExprCost]

theorem cost_mul {α : Type*} (a b : PathExpr α) :
    (pathExprCost (.mul a b)).terms = (pathExprCost a).terms * (pathExprCost b).terms ∧
      (pathExprCost (.mul a b)).maxWordLength =
        (pathExprCost a).maxWordLength + (pathExprCost b).maxWordLength := by
  simp [pathExprCost]

theorem cost_bracket {α : Type*} (a b : PathExpr α) :
    (pathExprCost (.bracket a b)).terms =
        2 * (pathExprCost a).terms * (pathExprCost b).terms ∧
      (pathExprCost (.bracket a b)).maxWordLength =
        (pathExprCost a).maxWordLength + (pathExprCost b).maxWordLength := by
  simp [pathExprCost]

theorem cost_reverse {α : Type*} (a : PathExpr α) :
    pathExprCost (.rev a) = pathExprCost a := rfl

theorem bracket_depth_not_length_preserving {α : Type*} (a b : List α)
    (ha : 0 < a.length) (hb : 0 < b.length) :
    (pathExprCost (.word a)).maxWordLength <
      (pathExprCost (.bracket (.word a) (.word b))).maxWordLength := by
  simp [pathExprCost]
  omega

/-- Factorized-local ≠ uniformly bounded compressed support. -/
theorem factorized_local_not_uniform_support (n : ℕ) :
    ∃ c : LocalCircuitCost, c.maxGateRadius = 1 ∧ c.gates = n :=
  ⟨⟨n, 1⟩, rfl, rfl⟩

end D0.Geometry
