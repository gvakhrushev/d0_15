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

/-- The active spectral gap formed from the first three elementary-symmetric
invariants of a tripartite size vector. -/
def tripartiteGap (a b c : ℚ) : ℚ :=
  tripartiteV a b c * tripartiteE a b c - 9 * tripartiteT a b c

@[simp] theorem tripartiteGap_formula (a b c : ℚ) :
    tripartiteGap a b c =
      (a + b + c) * (a * b + a * c + b * c) - 9 * (a * b * c) := by
  rfl

/-- The tripartite gap is a weighted sum of squared pairwise differences. -/
theorem tripartiteGap_sos (a b c : ℚ) :
    tripartiteGap a b c =
      a * (b - c) ^ 2 + b * (c - a) ^ 2 + c * (a - b) ^ 2 := by
  simp only [tripartiteGap, tripartiteV, tripartiteE, tripartiteT]
  ring

/-- Positive zone sizes make the tripartite gap nonnegative. -/
theorem tripartiteGap_nonneg (a b c : ℚ)
    (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) : 0 ≤ tripartiteGap a b c := by
  rw [tripartiteGap_sos]
  have h1 : 0 ≤ a * (b - c) ^ 2 := mul_nonneg ha.le (sq_nonneg _)
  have h2 : 0 ≤ b * (c - a) ^ 2 := mul_nonneg hb.le (sq_nonneg _)
  have h3 : 0 ≤ c * (a - b) ^ 2 := mul_nonneg hc.le (sq_nonneg _)
  linarith

/-- For positive sizes, the tripartite gap vanishes exactly when all sizes are equal. -/
theorem tripartiteGap_eq_zero_iff (a b c : ℚ)
    (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) :
    tripartiteGap a b c = 0 ↔ (a = b ∧ b = c) := by
  constructor
  · intro h
    rw [tripartiteGap_sos] at h
    have h1 : 0 ≤ a * (b - c) ^ 2 := mul_nonneg ha.le (sq_nonneg _)
    have h2 : 0 ≤ b * (c - a) ^ 2 := mul_nonneg hb.le (sq_nonneg _)
    have h3 : 0 ≤ c * (a - b) ^ 2 := mul_nonneg hc.le (sq_nonneg _)
    have e1 : a * (b - c) ^ 2 = 0 := by linarith
    have e3 : c * (a - b) ^ 2 = 0 := by linarith
    have hab : a = b := by
      have hsq : (a - b) ^ 2 = 0 := by
        rcases mul_eq_zero.mp e3 with hzero | hzero
        · exact absurd hzero hc.ne'
        · exact hzero
      have hdiff := (pow_eq_zero_iff (n := 2) (by norm_num)).mp hsq
      linarith
    have hbc : b = c := by
      have hsq : (b - c) ^ 2 = 0 := by
        rcases mul_eq_zero.mp e1 with hzero | hzero
        · exact absurd hzero ha.ne'
        · exact hzero
      have hdiff := (pow_eq_zero_iff (n := 2) (by norm_num)).mp hsq
      linarith
    exact ⟨hab, hbc⟩
  · rintro ⟨hab, hbc⟩
    subst hab
    subst hbc
    simp only [tripartiteGap, tripartiteV, tripartiteE, tripartiteT]
    ring

end D0.Combinatorics.TripartiteVieta
