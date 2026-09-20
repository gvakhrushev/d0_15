import Mathlib.Data.Fin.VecNotation
import Mathlib.Tactic
import D0.Algebra.SedenionTower

/-!
# Brown S3 automorphisms on the scalar-extended sedenion basis

This module formalizes the first positive layer left open by the sedenion
integrity audit.  The signed canonical-basis route over the integer carrier is
too small, but the classical Brown order-three automorphism uses coefficients
in Q(sqrt(3)) and mixes each pair e_i, e_(i+8).

We model Q(sqrt(3)) exactly by coordinate pairs (a,b), denoting a+b*sqrt(3),
with multiplication (a,b)(c,d)=(ac+3bd, ad+bc).  The sedenion multiplication
table is tied back to D0.Algebra.SedenionTower by an exhaustive theorem.

The three octonion subalgebras used in the Gresnigt--Gourlay--Varma
construction are also the literature triple, not the older three carriers
containing {e0,e1,e2,e3}.  Their common quaternion basis is
{e0,e4,e8,e12}.

Scope: this file proves exact basis-level multiplicativity and the S3
presentation for the scalar-extended action.  It does not yet construct the
complex Clifford left-action, minimal left ideals, or the final typed map to
the D0 generation carrier.
-/

namespace D0.Algebra.SedenionBrownS3

open D0.Algebra.CayleyDickson
open D0.Algebra.SedenionTower

/-- Exact coordinate model for Q(sqrt(3)): (a,b) means a+b*sqrt(3). -/
abbrev Q3 := ℚ × ℚ

def q3Mul (x y : Q3) : Q3 :=
  (x.1 * y.1 + 3 * x.2 * y.2, x.1 * y.2 + x.2 * y.1)

def q3Rat (q : ℚ) : Q3 := (q, 0)
def q3Sqrt3 : Q3 := (0, 1)
def q3MHalf : Q3 := (-1 / 2, 0)
def q3PSqrt3Half : Q3 := (0, 1 / 2)
def q3MSqrt3Half : Q3 := (0, -1 / 2)

theorem q3_sqrt3_sq :
    q3Mul q3Sqrt3 q3Sqrt3 = q3Rat 3 := by
  norm_num [q3Mul, q3Sqrt3, q3Rat]

/-- XOR index table for the repository Cayley--Dickson convention. -/
def mulIndex : Fin 16 → Fin 16 → Fin 16 :=
  ![
    ![0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    ![1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14],
    ![2, 3, 0, 1, 6, 7, 4, 5, 10, 11, 8, 9, 14, 15, 12, 13],
    ![3, 2, 1, 0, 7, 6, 5, 4, 11, 10, 9, 8, 15, 14, 13, 12],
    ![4, 5, 6, 7, 0, 1, 2, 3, 12, 13, 14, 15, 8, 9, 10, 11],
    ![5, 4, 7, 6, 1, 0, 3, 2, 13, 12, 15, 14, 9, 8, 11, 10],
    ![6, 7, 4, 5, 2, 3, 0, 1, 14, 15, 12, 13, 10, 11, 8, 9],
    ![7, 6, 5, 4, 3, 2, 1, 0, 15, 14, 13, 12, 11, 10, 9, 8],
    ![8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7],
    ![9, 8, 11, 10, 13, 12, 15, 14, 1, 0, 3, 2, 5, 4, 7, 6],
    ![10, 11, 8, 9, 14, 15, 12, 13, 2, 3, 0, 1, 6, 7, 4, 5],
    ![11, 10, 9, 8, 15, 14, 13, 12, 3, 2, 1, 0, 7, 6, 5, 4],
    ![12, 13, 14, 15, 8, 9, 10, 11, 4, 5, 6, 7, 0, 1, 2, 3],
    ![13, 12, 15, 14, 9, 8, 11, 10, 5, 4, 7, 6, 1, 0, 3, 2],
    ![14, 15, 12, 13, 10, 11, 8, 9, 6, 7, 4, 5, 2, 3, 0, 1],
    ![15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
  ]

/-- Sign bit for the same table: true means a minus sign. -/
def mulNeg : Fin 16 → Fin 16 → Bool :=
  ![
    ![false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false],
    ![false, true, false, true, false, true, true, false, false, true, true, false, true, false, false, true],
    ![false, true, true, false, false, false, true, true, false, false, true, true, true, true, false, false],
    ![false, false, true, true, false, true, false, true, false, true, false, true, true, false, true, false],
    ![false, true, true, true, true, false, false, false, false, false, false, false, true, true, true, true],
    ![false, false, true, false, true, true, true, false, false, true, false, true, false, true, false, true],
    ![false, false, false, true, true, false, true, true, false, true, true, false, false, true, true, false],
    ![false, true, false, false, true, true, false, true, false, false, true, true, false, false, true, true],
    ![false, true, true, true, true, true, true, true, true, false, false, false, false, false, false, false],
    ![false, false, true, false, true, false, false, true, true, true, true, false, true, false, false, true],
    ![false, false, false, true, true, true, false, false, true, false, true, true, true, true, false, false],
    ![false, true, false, false, true, false, true, false, true, true, false, true, true, false, true, false],
    ![false, false, false, false, false, true, true, true, true, false, false, false, true, true, true, true],
    ![false, true, false, true, false, false, false, true, true, true, false, true, false, true, false, true],
    ![false, true, true, false, false, true, false, false, true, true, true, false, false, true, true, false],
    ![false, false, true, true, false, false, true, false, true, false, true, true, false, false, true, true]
  ]

/-- Signed basis product reconstructed from the finite table. -/
def tableProductZS (i j : Fin 16) : ZS :=
  if mulNeg i j then -basisZS (mulIndex i j) else basisZS (mulIndex i j)

/-- The finite table above is not a parallel convention: it is exactly the
multiplication already implemented by the concrete repository sedenions. -/
theorem table_agrees_with_repository :
    ∀ i j : Fin 16,
      zsMul (basisZS i) (basisZS j) = tableProductZS i j := by
  native_decide

/-- Coordinate vector on the 16 canonical sedenion basis units. -/
abbrev SVec := Array Q3

instance : CoeFun SVec (fun _ => Fin 16 → Q3) where
  coe v := fun i => v[i.1]!

def basisVec (i : Fin 16) : SVec := Id.run do
  let mut a := (List.replicate 16 ((0 : ℚ), (0 : ℚ))).toArray
  a := a.set! i.1 (1, 0)
  return a

def vecMul (x y : SVec) : SVec := Id.run do
  let mut a := (List.replicate 16 ((0 : ℚ), (0 : ℚ))).toArray
  for i in [:16] do
    let xi := x[i]!
    if xi != (0, 0) then
      for j in [:16] do
        let yj := y[j]!
        if yj != (0, 0) then
          let fi : Fin 16 := ⟨i % 16, by omega⟩
          let fj : Fin 16 := ⟨j % 16, by omega⟩
          let k := (mulIndex fi fj).1
          let p := q3Mul xi yj
          let neg := mulNeg fi fj
          let term := if neg = true then (-p.1, -p.2) else p
          let curr := a[k]!
          a := a.set! k (curr.1 + term.1, curr.2 + term.2)
  return a

/-- Brown order-three automorphism, in exact Q(sqrt(3)) coordinates. -/
def psi (x : SVec) : SVec := Id.run do
  let mut a := (List.replicate 16 ((0 : ℚ), (0 : ℚ))).toArray
  a := a.set! 0 x[0]!
  a := a.set! 8 x[8]!
  for i in [1:8] do
    let x_i := x[i]!
    let x_i8 := x[i+8]!
    let p1 := q3Mul q3MHalf x_i
    let p2 := q3Mul q3PSqrt3Half x_i8
    a := a.set! i (p1.1 + p2.1, p1.2 + p2.2)
    let q1 := q3Mul q3MSqrt3Half x_i
    let q2 := q3Mul q3MHalf x_i8
    a := a.set! (i+8) (q1.1 + q2.1, q1.2 + q2.2)
  return a

/-- Brown order-two automorphism epsilon(a+b e8)=a-b e8. -/
def epsilon (x : SVec) : SVec := Id.run do
  let mut a := (List.replicate 16 ((0 : ℚ), (0 : ℚ))).toArray
  for i in [:8] do
    a := a.set! i x[i]!
  for i in [8:16] do
    let v := x[i]!
    a := a.set! i (-v.1, -v.2)
  return a

/-- Exact multiplicativity of the order-three action on all 256 canonical
basis products.  Since both operations are Q(sqrt(3))-linear/bilinear, this is
the finite structure-constant certificate for the scalar-extended algebra. -/
theorem psi_basis_multiplicative :
    ∀ i j : Fin 16,
      psi (vecMul (basisVec i) (basisVec j)) =
        vecMul (psi (basisVec i)) (psi (basisVec j)) := by
  native_decide

theorem epsilon_basis_multiplicative :
    ∀ i j : Fin 16,
      epsilon (vecMul (basisVec i) (basisVec j)) =
        vecMul (epsilon (basisVec i)) (epsilon (basisVec j)) := by
  native_decide

theorem psi_order_three_on_basis :
    ∀ i : Fin 16,
      psi (psi (psi (basisVec i))) = basisVec i := by
  native_decide

theorem epsilon_order_two_on_basis :
    ∀ i : Fin 16,
      epsilon (epsilon (basisVec i)) = basisVec i := by
  native_decide

theorem brown_s3_relation_on_basis :
    ∀ i : Fin 16,
      epsilon (psi (basisVec i)) =
        psi (psi (epsilon (basisVec i))) := by
  native_decide

/-- The Brown generator is genuinely outside the signed-monomial class. -/
theorem psi_nonmonomial_witness :
    psi (basisVec 1) 1 = q3MHalf ∧
    psi (basisVec 1) 9 = q3MSqrt3Half ∧
    q3MHalf ≠ 0 ∧ q3MSqrt3Half ≠ 0 := by
  native_decide

/-! ## The octonion triple actually used in the literature construction -/

def inLitO1 : Fin 16 → Bool :=
  ![true, true, false, false, true, true, false, false,
    true, true, false, false, true, true, false, false]

def inLitO2 : Fin 16 → Bool :=
  ![true, false, true, false, true, false, true, false,
    true, false, true, false, true, false, true, false]

def inLitO3 : Fin 16 → Bool :=
  ![true, false, false, true, true, false, false, true,
    true, false, false, true, true, false, false, true]

def inLitCommonH : Fin 16 → Bool :=
  ![true, false, false, false, true, false, false, false,
    true, false, false, false, true, false, false, false]

theorem literature_blocks_closed :
    (∀ i j : Fin 16,
      inLitO1 i = true → inLitO1 j = true →
      inLitO1 (mulIndex i j) = true) ∧
    (∀ i j : Fin 16,
      inLitO2 i = true → inLitO2 j = true →
      inLitO2 (mulIndex i j) = true) ∧
    (∀ i j : Fin 16,
      inLitO3 i = true → inLitO3 j = true →
      inLitO3 (mulIndex i j) = true) := by
  native_decide

theorem literature_block_cardinalities :
    (Finset.univ.filter (fun i : Fin 16 => inLitO1 i = true)).card = 8 ∧
    (Finset.univ.filter (fun i : Fin 16 => inLitO2 i = true)).card = 8 ∧
    (Finset.univ.filter (fun i : Fin 16 => inLitO3 i = true)).card = 8 := by
  native_decide

theorem literature_common_quaternion :
    (∀ i : Fin 16,
      (inLitO1 i = true ∧ inLitO2 i = true ∧ inLitO3 i = true) ↔
        inLitCommonH i = true) ∧
    (Finset.univ.filter (fun i : Fin 16 => inLitCommonH i = true)).card = 4 := by
  native_decide

def SupportedIn (block : Fin 16 → Bool) (x : SVec) : Prop :=
  ∀ k : Fin 16, block k = false → x k = 0

instance (block : Fin 16 → Bool) (x : SVec) : Decidable (SupportedIn block x) :=
  Fintype.decidableForallFintype

theorem brown_s3_stabilizes_literature_blocks :
    (∀ i : Fin 16, inLitO1 i = true →
      SupportedIn inLitO1 (psi (basisVec i)) ∧
      SupportedIn inLitO1 (epsilon (basisVec i))) ∧
    (∀ i : Fin 16, inLitO2 i = true →
      SupportedIn inLitO2 (psi (basisVec i)) ∧
      SupportedIn inLitO2 (epsilon (basisVec i))) ∧
    (∀ i : Fin 16, inLitO3 i = true →
      SupportedIn inLitO3 (psi (basisVec i)) ∧
      SupportedIn inLitO3 (epsilon (basisVec i))) := by
  native_decide

/-- **D0-SEDENION-BROWN-S3-SCALAR-EXTENSION-001.**
Exact positive closure of the scalar-extension automorphism layer: the
repository multiplication table admits the Brown S3 generators over
Q(sqrt(3)); the generators satisfy the S3 presentation on the canonical basis
and stabilize the three literature octonion subalgebras with common quaternion
{e0,e4,e8,e12}. -/
theorem sedenion_brown_s3_scalar_extension_core :
    (∀ i j : Fin 16,
      psi (vecMul (basisVec i) (basisVec j)) =
        vecMul (psi (basisVec i)) (psi (basisVec j))) ∧
    (∀ i : Fin 16, psi (psi (psi (basisVec i))) = basisVec i) ∧
    (∀ i : Fin 16,
      epsilon (psi (basisVec i)) = psi (psi (epsilon (basisVec i)))) := by
  exact ⟨psi_basis_multiplicative,
    psi_order_three_on_basis,
    brown_s3_relation_on_basis⟩

end D0.Algebra.SedenionBrownS3
