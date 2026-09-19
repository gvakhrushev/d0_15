import Mathlib.Data.Fin.VecNotation
import Mathlib.Tactic
import D0.Algebra.CayleyDickson

/-!
# Concrete integer Cayley--Dickson tower: quaternions, octonions, sedenions

This module computes on the actual fourth Cayley--Dickson double constructed in
`D0.Algebra.CayleyDickson`.  It intentionally separates algebraic facts from
any later physical-generation interpretation.

The standard nested basis has coordinates

* 0..3   : common quaternion block A,
* 4..7   : block B,
* 8..11  : block C,
* 12..15 : block D.

Three natural eight-basis carriers A+B, A+C, A+D are multiplicatively closed
(up to the usual signed basis multiplication) and their pairwise basis
intersections are exactly A.  We also certify an explicit sedenion zero-divisor
pair and the loss of alternativity.

No S3 action on these three blocks is asserted here.
-/

namespace D0.Algebra.SedenionTower

open D0.Algebra.CayleyDickson

/-- Canonical basis of the first double. -/
def basisZC : Fin 2 → ZC :=
  ![(1, 0), (0, 1)]

/-- Canonical basis of the quaternion double. -/
def basisZH : Fin 4 → ZH :=
  ![(basisZC 0, 0),
    (basisZC 1, 0),
    (0, basisZC 0),
    (0, basisZC 1)]

/-- Canonical basis of the octonion double. -/
def basisZO : Fin 8 → ZO :=
  ![(basisZH 0, 0),
    (basisZH 1, 0),
    (basisZH 2, 0),
    (basisZH 3, 0),
    (0, basisZH 0),
    (0, basisZH 1),
    (0, basisZH 2),
    (0, basisZH 3)]

/-- Canonical basis of the sedenion double. -/
def basisZS : Fin 16 → ZS :=
  ![(basisZO 0, 0),
    (basisZO 1, 0),
    (basisZO 2, 0),
    (basisZO 3, 0),
    (basisZO 4, 0),
    (basisZO 5, 0),
    (basisZO 6, 0),
    (basisZO 7, 0),
    (0, basisZO 0),
    (0, basisZO 1),
    (0, basisZO 2),
    (0, basisZO 3),
    (0, basisZO 4),
    (0, basisZO 5),
    (0, basisZO 6),
    (0, basisZO 7)]

/-! ## Sanity checks across the tower -/

/-- Quaternion multiplication is associative on its four canonical basis units. -/
theorem quaternion_basis_associative :
    ∀ i j k : Fin 4,
      zhMul (zhMul (basisZH i) (basisZH j)) (basisZH k) =
        zhMul (basisZH i) (zhMul (basisZH j) (basisZH k)) := by
  native_decide

/-- Octonion multiplication is already non-associative. -/
theorem octonion_basis_nonassociative :
    zoMul (zoMul (basisZO 1) (basisZO 2)) (basisZO 4) ≠
      zoMul (basisZO 1) (zoMul (basisZO 2) (basisZO 4)) := by
  native_decide

/-! ## Explicit sedenion pathologies -/

def zeroDivisorX : ZS := basisZS 1 + basisZS 10
def zeroDivisorY : ZS := basisZS 4 - basisZS 15

theorem zeroDivisorX_ne_zero : zeroDivisorX ≠ 0 := by
  native_decide

theorem zeroDivisorY_ne_zero : zeroDivisorY ≠ 0 := by
  native_decide

/-- A literal zero-divisor witness in the fourth Cayley--Dickson double. -/
theorem explicit_sedenion_zero_divisor :
    zsMul zeroDivisorX zeroDivisorY = 0 := by
  native_decide

def nonAlternativeX : ZS := basisZS 1 + basisZS 10
def nonAlternativeY : ZS := basisZS 4

/-- Sedenions fail the left alternative law on an explicit pair. -/
theorem sedenion_not_left_alternative :
    zsMul (zsMul nonAlternativeX nonAlternativeX) nonAlternativeY ≠
      zsMul nonAlternativeX (zsMul nonAlternativeX nonAlternativeY) := by
  native_decide

/-! ## Three canonical eight-basis multiplicatively closed carriers -/

/-- Common quaternion basis block A = {0,1,2,3}. -/
def inHBlock (i : Fin 16) : Bool :=
  decide (i.val < 4)

/-- First eight-basis carrier A+B. -/
def inO1Block (i : Fin 16) : Bool :=
  decide (i.val < 8)

/-- Second eight-basis carrier A+C. -/
def inO2Block (i : Fin 16) : Bool :=
  decide (i.val < 4 ∨ (8 ≤ i.val ∧ i.val < 12))

/-- Third eight-basis carrier A+D. -/
def inO3Block (i : Fin 16) : Bool :=
  decide (i.val < 4 ∨ (12 ≤ i.val ∧ i.val < 16))

/-- Does `x` equal a signed canonical basis unit belonging to `block`? -/
def signedBasisIn (block : Fin 16 → Bool) (x : ZS) : Bool :=
  Finset.univ.any (fun k : Fin 16 =>
    block k && decide (x = basisZS k ∨ x = -basisZS k))

theorem O1_basis_closed :
    ∀ i j : Fin 16,
      inO1Block i = true → inO1Block j = true →
      signedBasisIn inO1Block (zsMul (basisZS i) (basisZS j)) = true := by
  native_decide

theorem O2_basis_closed :
    ∀ i j : Fin 16,
      inO2Block i = true → inO2Block j = true →
      signedBasisIn inO2Block (zsMul (basisZS i) (basisZS j)) = true := by
  native_decide

theorem O3_basis_closed :
    ∀ i j : Fin 16,
      inO3Block i = true → inO3Block j = true →
      signedBasisIn inO3Block (zsMul (basisZS i) (basisZS j)) = true := by
  native_decide

/-- Each of the three canonical blocks contains exactly eight basis units. -/
theorem canonical_block_cardinalities :
    (Finset.univ.filter (fun i : Fin 16 => inO1Block i = true)).card = 8 ∧
    (Finset.univ.filter (fun i : Fin 16 => inO2Block i = true)).card = 8 ∧
    (Finset.univ.filter (fun i : Fin 16 => inO3Block i = true)).card = 8 := by
  native_decide

/-- Pairwise basis intersections are exactly the common quaternion block A. -/
theorem canonical_block_pairwise_intersections :
    (∀ i : Fin 16,
      (inO1Block i = true ∧ inO2Block i = true) ↔ inHBlock i = true) ∧
    (∀ i : Fin 16,
      (inO1Block i = true ∧ inO3Block i = true) ↔ inHBlock i = true) ∧
    (∀ i : Fin 16,
      (inO2Block i = true ∧ inO3Block i = true) ↔ inHBlock i = true) := by
  native_decide

theorem quaternion_block_cardinality :
    (Finset.univ.filter (fun i : Fin 16 => inHBlock i = true)).card = 4 := by
  native_decide

/-- Capstone: a real sedenion carrier exists and contains three canonical
eight-basis multiplicatively closed blocks sharing exactly four basis units.
This theorem deliberately stops before asserting an S3 automorphism action or
a physical generation functor. -/
theorem sedenion_three_block_algebraic_core :
    zsMul zeroDivisorX zeroDivisorY = 0 ∧
    zeroDivisorX ≠ 0 ∧ zeroDivisorY ≠ 0 ∧
    (Finset.univ.filter (fun i : Fin 16 => inO1Block i = true)).card = 8 ∧
    (Finset.univ.filter (fun i : Fin 16 => inO2Block i = true)).card = 8 ∧
    (Finset.univ.filter (fun i : Fin 16 => inO3Block i = true)).card = 8 ∧
    (∀ i : Fin 16,
      (inO1Block i = true ∧ inO2Block i = true) ↔ inHBlock i = true) := by
  exact ⟨explicit_sedenion_zero_divisor,
    zeroDivisorX_ne_zero,
    zeroDivisorY_ne_zero,
    canonical_block_cardinalities.1,
    canonical_block_cardinalities.2.1,
    canonical_block_cardinalities.2.2,
    canonical_block_pairwise_intersections.1⟩

end D0.Algebra.SedenionTower
