import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import D0.Core.Phi
import D0.Foundation.M1Predicate

/-!
# D0.Algebra.FibonacciPerronTraceCanonicity

Theoretical owner: `D0-FIBONACCI-PERRON-PROFILE-CANONICITY-001`.

Formalization of the exact canonicity of the positive normalized Perron eigenvector
and eigenvalue of the Fibonacci incidence matrix:
$$M_\varphi = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}.$$

The Perron eigen-equations for positive eigenvector $(x, y) \in \mathbb{R}^2$
and positive eigenvalue $r \in \mathbb{R}$:
$$\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix} = r \begin{pmatrix} x \\ y \end{pmatrix}$$
expand to:
1. $x + y = r x$
2. $x = r y$
with normalization:
3. $x + y = 1$

From (2), $x = r y$. Substituting into (1) gives $(r + 1) y = r^2 y$.
Since $y > 0$, dividing by $y$ yields:
$$r^2 - r - 1 = 0.$$
Factoring over $\mathbb{R}$:
$$r^2 - r - 1 = (r - \varphi)(r + \varphi - 1).$$
For any $r > 0$, since $\varphi = (1 + \sqrt{5})/2 > 1$, the factor $r + \varphi - 1 > 0$.
Hence $r = \varphi$ uniquely!

Then from $x + y = 1$ and $x + y = \varphi x$:
$$\varphi x = 1 \implies x = \varphi^{-1}.$$
And $x = \varphi y \implies y = \varphi^{-1} x = \varphi^{-2}$.

Finally, $(x, y) = (\varphi^{-1}, \varphi^{-2})$ is the unique witness satisfying
the canonical positive normalized Perron condition, yielding an exact `M1Forced` theorem.
-/

namespace D0.Algebra.FibonacciPerronTraceCanonicity

open D0
open D0.Foundation

/-- A positive normalized eigenvector profile for the Fibonacci incidence matrix $M_\varphi$. -/
structure PositivePerronProfile where
  x : ℝ
  y : ℝ
  r : ℝ
  x_pos : 0 < x
  y_pos : 0 < y
  r_pos : 0 < r
  eig₁ : x + y = r * x
  eig₂ : x = r * y
  normalized : x + y = 1

/-- $\varphi > 1$. -/
theorem phi_gt_one : 1 < phi := by
  have h5 : (1 : ℝ) < 5 := by norm_num
  have hsqrt : 1 < Real.sqrt 5 := by
    calc 1 = Real.sqrt 1 := by rw [Real.sqrt_one]
    _ < Real.sqrt 5 := Real.sqrt_lt_sqrt (by norm_num) h5
  unfold phi
  linarith

/-- $\varphi > 0$. -/
theorem phi_pos : 0 < phi := by
  have := phi_gt_one
  linarith

/-- The polynomial factorization $r^2 - r - 1 = (r - \varphi)(r + \varphi - 1)$ holds identically on $\mathbb{R}$. -/
theorem poly_factorization (r : ℝ) :
    r ^ 2 - r - 1 = (r - phi) * (r + phi - 1) := by
  have hphi := phi_sq
  calc r ^ 2 - r - 1 = r ^ 2 - r - (phi ^ 2 - phi) := by linarith
  _ = (r - phi) * (r + phi - 1) := by ring

/-- **Theorem: The positive Perron eigenvalue is uniquely forced to be $\varphi$.** -/
theorem positive_perron_eigenvalue_unique (p : PositivePerronProfile) :
    p.r = phi := by
  have h_subst : p.x + p.y = p.r * (p.r * p.y) := by
    calc p.x + p.y = p.r * p.x := p.eig₁
    _ = p.r * (p.r * p.y) := by rw [p.eig₂]
  have h_lin : p.x + p.y = (p.r + 1) * p.y := by
    calc p.x + p.y = (p.r * p.y) + p.y := by rw [p.eig₂]
    _ = (p.r + 1) * p.y := by ring
  -- So (r^2 - r - 1) * y = 0
  have h_eq : (p.r ^ 2 - p.r - 1) * p.y = 0 := by
    calc (p.r ^ 2 - p.r - 1) * p.y = p.r * (p.r * p.y) - (p.r + 1) * p.y := by ring
    _ = (p.x + p.y) - (p.x + p.y) := by rw [← h_subst, ← h_lin]
    _ = 0 := sub_self _
  have h_root : p.r ^ 2 - p.r - 1 = 0 := by
    cases mul_eq_zero.mp h_eq with
    | inl h => exact h
    | inr hy => linarith [p.y_pos]
  rw [poly_factorization p.r] at h_root
  cases mul_eq_zero.mp h_root with
  | inl h_minus =>
    linarith
  | inr h_plus =>
    have h_phi_gt := phi_gt_one
    have : 0 < p.r + phi - 1 := by linarith [p.r_pos]
    linarith

/-- **Theorem: The normalized Perron profile is uniquely $(x, y) = (\varphi^{-1}, \varphi^{-2})$.** -/
theorem normalized_perron_profile_unique (p : PositivePerronProfile) :
    p.x = phi⁻¹ ∧ p.y = phi⁻¹ ^ 2 := by
  have hr : p.r = phi := positive_perron_eigenvalue_unique p
  have hphi_pos : 0 < phi := phi_pos
  have hphi_ne : phi ≠ 0 := ne_of_gt hphi_pos
  -- From normalized: x + y = 1 and eig1: x + y = r * x = phi * x
  have h_phix : phi * p.x = 1 := by
    calc phi * p.x = p.r * p.x := by rw [hr]
    _ = p.x + p.y := p.eig₁.symm
    _ = 1 := p.normalized
  have hx : p.x = phi⁻¹ := by
    calc p.x = (phi * p.x) / phi := by field_simp
    _ = 1 / phi := by rw [h_phix]
    _ = phi⁻¹ := by rw [one_div]
  -- From eig2: x = r * y = phi * y, so y = x / phi = phi⁻¹ / phi = phi⁻²
  have hy : p.y = phi⁻¹ ^ 2 := by
    have h_phi_y : phi * p.y = p.x := by
      calc phi * p.y = p.r * p.y := by rw [hr]
      _ = p.x := p.eig₂.symm
    calc p.y = (phi * p.y) / phi := by field_simp
    _ = p.x / phi := by rw [h_phi_y]
    _ = phi⁻¹ / phi := by rw [hx]
    _ = phi⁻¹ ^ 2 := by
      rw [div_eq_mul_inv, mul_comm, sq]
  exact ⟨hx, hy⟩

/-- Predicate for canonical normalized positive Perron profile on a pair $(x, y) \in \mathbb{R}^2$. -/
def CanonicalPerronProfile (pair : ℝ × ℝ) : Prop :=
  ∃ r : ℝ,
    0 < pair.1 ∧
    0 < pair.2 ∧
    0 < r ∧
    pair.1 + pair.2 = r * pair.1 ∧
    pair.1 = r * pair.2 ∧
    pair.1 + pair.2 = 1

/-- Existence of the canonical Perron profile at $(\varphi^{-1}, \varphi^{-2})$. -/
theorem canonical_perron_profile_exists :
    CanonicalPerronProfile (phi⁻¹, phi⁻¹ ^ 2) := by
  use phi
  have hphi_gt := phi_gt_one
  have hphi_pos := phi_pos
  have hphi_ne : phi ≠ 0 := ne_of_gt hphi_pos
  have h_inv_sq : phi⁻¹ ^ 2 = phi⁻¹ * phi⁻¹ := sq phi⁻¹
  refine ⟨by positivity, by positivity, hphi_pos, ?_, ?_, ?_⟩
  · -- phi⁻¹ + phi⁻¹^2 = phi * phi⁻¹
    calc (phi⁻¹, phi⁻¹ ^ 2).1 + (phi⁻¹, phi⁻¹ ^ 2).2 = phi⁻¹ + phi⁻¹ ^ 2 := rfl
    _ = 1 := phi_inv_satisfies_primitive
    _ = phi * phi⁻¹ := by field_simp
    _ = phi * (phi⁻¹, phi⁻¹ ^ 2).1 := rfl
  · -- phi⁻¹ = phi * phi⁻¹^2
    calc (phi⁻¹, phi⁻¹ ^ 2).1 = phi⁻¹ := rfl
    _ = phi * (phi⁻¹ * phi⁻¹) := by
      have h_assoc : phi * (phi⁻¹ * phi⁻¹) = (phi * phi⁻¹) * phi⁻¹ := by ring
      rw [h_assoc]
      field_simp
    _ = phi * phi⁻¹ ^ 2 := by rw [← sq]
    _ = phi * (phi⁻¹, phi⁻¹ ^ 2).2 := rfl
  · -- phi⁻¹ + phi⁻¹^2 = 1
    calc (phi⁻¹, phi⁻¹ ^ 2).1 + (phi⁻¹, phi⁻¹ ^ 2).2 = phi⁻¹ + phi⁻¹ ^ 2 := rfl
    _ = 1 := phi_inv_satisfies_primitive

/-- **Theorem: The Perron profile is M1-forced to $(\varphi^{-1}, \varphi^{-2})$.** -/
theorem perron_profile_m1_forced :
    M1Forced CanonicalPerronProfile (phi⁻¹, phi⁻¹ ^ 2) where
  forced := canonical_perron_profile_exists
  unique := by
    rintro ⟨x, y⟩ ⟨r, hx_pos, hy_pos, hr_pos, heig1, heig2, hnorm⟩
    let p : PositivePerronProfile := {
      x := x
      y := y
      r := r
      x_pos := hx_pos
      y_pos := hy_pos
      r_pos := hr_pos
      eig₁ := heig1
      eig₂ := heig2
      normalized := hnorm
    }
    have h_unique := normalized_perron_profile_unique p
    exact Prod.ext h_unique.1 h_unique.2

/-- Summary owner for `D0-FIBONACCI-PERRON-PROFILE-CANONICITY-001`. -/
theorem fibonacci_perron_profile_canonicity_owner :
    (∀ p : PositivePerronProfile, p.r = phi) ∧
    (∀ p : PositivePerronProfile, p.x = phi⁻¹ ∧ p.y = phi⁻¹ ^ 2) ∧
    M1Forced CanonicalPerronProfile (phi⁻¹, phi⁻¹ ^ 2) :=
  ⟨positive_perron_eigenvalue_unique,
   normalized_perron_profile_unique,
   perron_profile_m1_forced⟩

end D0.Algebra.FibonacciPerronTraceCanonicity
