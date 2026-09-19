import Mathlib.Algebra.Ring.Basic

namespace D0.Geometry

/-!
# D0.Geometry.PseudoinverseTwistAlgebra

Owner: `D0-ARCHIVE-PSEUDOINVERSE-TWIST-ALGEBRA-001`.

Generic purely algebraic theorem proving that any generalized inverse / projection pair
satisfying D⁺ D = 1 - P and an annihilation condition E P = 0 produces an exact
twisted commutator matching the target gradient G:

  D π - ρ D = G

where E = D π - π D - G and ρ = π + E D⁺.
-/

/-- **D0-ARCHIVE-PSEUDOINVERSE-TWIST-ALGEBRA-001 (Owner)**:
Exact algebraic identity for the pseudoinverse-derived twist in any (possibly noncommutative) ring:
Given operators D, D⁺, P, π, G, E, ρ satisfying:
  1. D⁺ D = 1 - P  (generalized inverse on the complement of P)
  2. E P = 0       (commutator residual annihilates the projection)
  3. E = D π - π D - G
  4. ρ = π + E D⁺
Then the twisted commutator strictly evaluates to G:
  D π - ρ D = G. -/
theorem pseudoinverse_twist_exact_identity {R : Type*} [Ring R]
    (D Dplus P pi G E rho : R)
    (h_pinv : Dplus * D = 1 - P)
    (h_annihilate : E * P = 0)
    (h_E : E = D * pi - pi * D - G)
    (h_rho : rho = pi + E * Dplus) :
    D * pi - rho * D = G := by
  have h_rho_D : rho * D = pi * D + E * (Dplus * D) := by
    rw [h_rho, add_mul, mul_assoc]
  rw [h_rho_D, h_pinv]
  have h_E_distrib : E * (1 - P) = E := by
    calc
      E * (1 - P) = E * 1 - E * P := mul_sub E 1 P
      _ = E - 0 := by rw [mul_one, h_annihilate]
      _ = E := sub_zero E
  rw [h_E_distrib]
  rw [sub_add_eq_sub_sub]
  rw [h_E]
  exact sub_sub_cancel (D * pi - pi * D) G

/-- Master owner theorem for the algebraic pseudoinverse twist lemma. -/
theorem archive_pseudoinverse_twist_algebra_owner {R : Type*} [Ring R]
    (D Dplus P pi G E rho : R)
    (h_pinv : Dplus * D = 1 - P)
    (h_annihilate : E * P = 0)
    (h_E : E = D * pi - pi * D - G)
    (h_rho : rho = pi + E * Dplus) :
    D * pi - rho * D = G :=
  pseudoinverse_twist_exact_identity D Dplus P pi G E rho h_pinv h_annihilate h_E h_rho

end D0.Geometry
