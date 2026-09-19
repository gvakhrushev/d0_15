import Mathlib.Tactic

/-!
# Cayley--Dickson doubling over an explicit involutive base

This file provides the algebraic carrier missing from the old three-label
"Sedenions" placeholder.  It deliberately uses explicit multiplication and
conjugation functions instead of pretending that a three-element index type is
itself a sedenion algebra.

For an additive group `R`, a multiplication `mulR` and a conjugation
`conjR`, the Cayley--Dickson double is the pair `R × R` with convention

  (a,b) * (c,d) = (a*c - conj(d)*b, d*a + b*conj(c))
  conj(a,b)      = (conj(a), -b).

Iterating from the integers gives concrete carriers of ranks 2,4,8,16 as
nested integer pairs.  No associativity is assumed at the generic level.
-/

namespace D0.Algebra.CayleyDickson

/-- One Cayley--Dickson doubling step. -/
abbrev CD (R : Type*) := R × R

/-- Cayley--Dickson conjugation induced by a base conjugation. -/
def conjCD {R : Type*} [Neg R] (conjR : R → R) (x : CD R) : CD R :=
  (conjR x.1, -x.2)

/-- Cayley--Dickson multiplication, in the convention used throughout this file. -/
def mulCD {R : Type*} [AddGroup R]
    (mulR : R → R → R) (conjR : R → R)
    (x y : CD R) : CD R :=
  (mulR x.1 y.1 - mulR (conjR y.2) x.2,
   mulR y.2 x.1 + mulR x.2 (conjR y.1))

/-- The canonical left copy of the base carrier in its double. -/
def embedLeft {R : Type*} [Zero R] (x : R) : CD R := (x, 0)

/-- Integer conjugation is trivial. -/
def zConj (x : ℤ) : ℤ := x

/-- Integer multiplication as the base Cayley--Dickson product. -/
def zMul (x y : ℤ) : ℤ := x * y

/-- Gaussian-integer-shaped first double. -/
abbrev ZC := CD ℤ

def zcConj : ZC → ZC := conjCD zConj
def zcMul : ZC → ZC → ZC := mulCD zMul zConj

/-- Quaternion carrier as the second double. -/
abbrev ZH := CD ZC

def zhConj : ZH → ZH := conjCD zcConj
def zhMul : ZH → ZH → ZH := mulCD zcMul zcConj

/-- Octonion carrier as the third double. -/
abbrev ZO := CD ZH

def zoConj : ZO → ZO := conjCD zhConj
def zoMul : ZO → ZO → ZO := mulCD zhMul zhConj

/-- Sedenion carrier as the fourth double. -/
abbrev ZS := CD ZO

def zsConj : ZS → ZS := conjCD zoConj
def zsMul : ZS → ZS → ZS := mulCD zoMul zoConj

@[simp] theorem zcConj_zero : zcConj (0 : ZC) = 0 := by
  rfl

@[simp] theorem zhConj_zero : zhConj (0 : ZH) = 0 := by
  rfl

@[simp] theorem zoConj_zero : zoConj (0 : ZO) = 0 := by
  rfl

@[simp] theorem zsConj_zero : zsConj (0 : ZS) = 0 := by
  rfl

@[simp] theorem zcMul_zero_left (x : ZC) : zcMul 0 x = 0 := by
  rcases x with ⟨a,b⟩
  simp [zcMul, mulCD, zMul, zConj]

@[simp] theorem zcMul_zero_right (x : ZC) : zcMul x 0 = 0 := by
  rcases x with ⟨a,b⟩
  simp [zcMul, mulCD, zMul, zConj]

@[simp] theorem zhMul_zero_left (x : ZH) : zhMul 0 x = 0 := by
  rcases x with ⟨a,b⟩
  simp [zhMul, mulCD]

@[simp] theorem zhMul_zero_right (x : ZH) : zhMul x 0 = 0 := by
  rcases x with ⟨a,b⟩
  simp [zhMul, mulCD]

@[simp] theorem zoMul_zero_left (x : ZO) : zoMul 0 x = 0 := by
  rcases x with ⟨a,b⟩
  simp [zoMul, mulCD]

@[simp] theorem zoMul_zero_right (x : ZO) : zoMul x 0 = 0 := by
  rcases x with ⟨a,b⟩
  simp [zoMul, mulCD]

@[simp] theorem zsMul_zero_left (x : ZS) : zsMul 0 x = 0 := by
  rcases x with ⟨a,b⟩
  simp [zsMul, mulCD]

@[simp] theorem zsMul_zero_right (x : ZS) : zsMul x 0 = 0 := by
  rcases x with ⟨a,b⟩
  simp [zsMul, mulCD]

@[simp] theorem zcConj_involutive (x : ZC) : zcConj (zcConj x) = x := by
  rcases x with ⟨a,b⟩
  simp [zcConj, conjCD, zConj]

@[simp] theorem zhConj_involutive (x : ZH) : zhConj (zhConj x) = x := by
  rcases x with ⟨a,b⟩
  simp [zhConj, conjCD]

@[simp] theorem zoConj_involutive (x : ZO) : zoConj (zoConj x) = x := by
  rcases x with ⟨a,b⟩
  simp [zoConj, conjCD]

@[simp] theorem zsConj_involutive (x : ZS) : zsConj (zsConj x) = x := by
  rcases x with ⟨a,b⟩
  simp [zsConj, conjCD]

/-- Concrete left embeddings along the tower. -/
def hToO (x : ZH) : ZO := (x, 0)
def oToS (x : ZO) : ZS := (x, 0)

theorem hToO_mul (x y : ZH) :
    zoMul (hToO x) (hToO y) = hToO (zhMul x y) := by
  simp [hToO, zoMul, mulCD]

theorem oToS_mul (x y : ZO) :
    zsMul (oToS x) (oToS y) = oToS (zoMul x y) := by
  simp [oToS, zsMul, mulCD]

/-- The construction is genuinely iterated doubling, not a dimension constant. -/
theorem tower_shape :
    ZC = (ℤ × ℤ) ∧
    ZH = ((ℤ × ℤ) × (ℤ × ℤ)) ∧
    ZO = (((ℤ × ℤ) × (ℤ × ℤ)) × ((ℤ × ℤ) × (ℤ × ℤ))) := by
  exact ⟨rfl, rfl, rfl⟩

end D0.Algebra.CayleyDickson
