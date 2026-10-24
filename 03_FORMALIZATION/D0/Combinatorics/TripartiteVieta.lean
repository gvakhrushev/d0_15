import Mathlib.Tactic

/-!
# Generic Vieta rigidity for tripartite zone sizes

This file owns the rational elementary-symmetric data and the root-multiset
argument independently of any particular graph or spectral application.
Concrete modules can recover these three invariants from their own operators
and then reuse the same unordered reconstruction theorem.
-/

namespace D0.Combinatorics.TripartiteVieta

open Polynomial

/-- Vertex elementary-symmetric invariant of three rational zone sizes. -/
def tripartiteV (a b c : ℚ) : ℚ := a + b + c

@[simp] theorem tripartiteV_formula (a b c : ℚ) :
    tripartiteV a b c = a + b + c := rfl

/-- Edge elementary-symmetric invariant of three rational zone sizes. -/
def tripartiteE (a b c : ℚ) : ℚ := a * b + a * c + b * c

@[simp] theorem tripartiteE_formula (a b c : ℚ) :
    tripartiteE a b c = a * b + a * c + b * c := rfl

/-- Triangle elementary-symmetric invariant of three rational zone sizes. -/
def tripartiteT (a b c : ℚ) : ℚ := a * b * c

@[simp] theorem tripartiteT_formula (a b c : ℚ) :
    tripartiteT a b c = a * b * c := rfl

/-- The monic cubic whose roots, with multiplicity, are the three zone sizes. -/
noncomputable def zoneRootPolynomial (a b c : ℚ) : Polynomial ℚ :=
  (X - Polynomial.C a) * (X - Polynomial.C b) * (X - Polynomial.C c)

/-- Vieta expansion of the zone-root polynomial. -/
theorem zoneRootPolynomial_vieta (a b c : ℚ) :
    zoneRootPolynomial a b c =
      X ^ 3 - Polynomial.C (tripartiteV a b c) * X ^ 2 +
        Polynomial.C (tripartiteE a b c) * X -
          Polynomial.C (tripartiteT a b c) := by
  simp [zoneRootPolynomial, tripartiteV, tripartiteE, tripartiteT]
  ring

/-- Equal elementary-symmetric invariants give equal root polynomials. -/
theorem zoneRootPolynomial_eq_of_VET_eq
    {a b c a' b' c' : ℚ}
    (hV : tripartiteV a b c = tripartiteV a' b' c')
    (hE : tripartiteE a b c = tripartiteE a' b' c')
    (hT : tripartiteT a b c = tripartiteT a' b' c') :
    zoneRootPolynomial a b c = zoneRootPolynomial a' b' c' := by
  rw [zoneRootPolynomial_vieta, zoneRootPolynomial_vieta, hV, hE, hT]

/-- The polynomial records the full root multiset, including repeated sizes. -/
theorem zoneRootPolynomial_roots (a b c : ℚ) :
    (zoneRootPolynomial a b c).roots = ({a, b, c} : Multiset ℚ) := by
  rw [zoneRootPolynomial,
    Polynomial.roots_mul
      (mul_ne_zero
        (mul_ne_zero (Polynomial.X_sub_C_ne_zero a)
          (Polynomial.X_sub_C_ne_zero b))
        (Polynomial.X_sub_C_ne_zero c)),
    Polynomial.roots_mul
      (mul_ne_zero (Polynomial.X_sub_C_ne_zero a)
        (Polynomial.X_sub_C_ne_zero b)),
    Polynomial.roots_X_sub_C, Polynomial.roots_X_sub_C,
    Polynomial.roots_X_sub_C]
  rfl

/-- Equal rational Vieta data determine the unordered triple. -/
theorem unordered_triple_eq_of_VET_eq
    {a b c a' b' c' : ℚ}
    (hV : tripartiteV a b c = tripartiteV a' b' c')
    (hE : tripartiteE a b c = tripartiteE a' b' c')
    (hT : tripartiteT a b c = tripartiteT a' b' c') :
    ({a, b, c} : Multiset ℚ) = ({a', b', c'} : Multiset ℚ) := by
  rw [← zoneRootPolynomial_roots a b c,
    ← zoneRootPolynomial_roots a' b' c']
  exact congrArg Polynomial.roots
    (zoneRootPolynomial_eq_of_VET_eq hV hE hT)

/-- Natural-number specialization of unordered Vieta rigidity. -/
theorem unordered_nat_triple_eq_of_VET_eq
    {a b c a' b' c' : ℕ}
    (hV : tripartiteV a b c = tripartiteV a' b' c')
    (hE : tripartiteE a b c = tripartiteE a' b' c')
    (hT : tripartiteT a b c = tripartiteT a' b' c') :
    ({a, b, c} : Multiset ℕ) = ({a', b', c'} : Multiset ℕ) := by
  apply Multiset.map_injective
    (Nat.cast_injective : Function.Injective (fun n : ℕ => (n : ℚ)))
  simpa using unordered_triple_eq_of_VET_eq hV hE hT

end D0.Combinatorics.TripartiteVieta
