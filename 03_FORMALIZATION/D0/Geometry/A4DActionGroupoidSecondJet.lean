import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic
import Mathlib.Tactic.Module

set_option linter.unusedSimpArgs false

/-!
# Action-groupoid second jet

Assume a background-dependent family whose moved generator is `G + t Dg` and whose
finite composition, through the quadratic jet, is additive in the translation
parameters. The cross term is then

`K = G² + Dg`,

and two such cross terms with a common value obey

`(D_e g_ζ)[h_ξ] - (D_e g_ξ)[h_ζ] + [G_ζ, G_ξ] = 0`.

`Dg` is not constructed. The nonlocal energy-engineered formula is not a
candidate matter lift and is not formalized.
-/

namespace D0.Geometry

open Matrix

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- Left factor at background moved by parameter `t`. -/
def groupoidMoved (G Dg K : Matrix ι ι ℚ) (s t : ℚ) : Matrix ι ι ℚ :=
  1 + s • G + (s * t) • Dg + (s ^ 2 / 2) • K

/-- Right factor at the original background. -/
def groupoidBase (G K : Matrix ι ι ℚ) (t : ℚ) : Matrix ι ι ℚ :=
  1 + t • G + (t ^ 2 / 2) • K

/-- Additive jet `R(s+t)` with the same `G` and `K`. -/
def groupoidSum (G K : Matrix ι ι ℚ) (s t : ℚ) : Matrix ι ι ℚ :=
  1 + (s + t) • G + ((s + t) ^ 2 / 2) • K

private lemma isolate_cross_entry (x a e b c : ℚ)
    (h : ∀ s t : ℚ,
      s * t * x + s * t ^ 2 * a + s * t ^ 3 * e + s ^ 2 * t * b + s ^ 2 * t ^ 2 * c = 0) :
    x = 0 := by
  have h11 := h 1 1
  have h21 := h 2 1
  have h12 := h 1 2
  have h22 := h 2 2
  have h13 := h 1 3
  linear_combination (5 : ℚ) * h11 - h21 - (2 : ℚ) * h12 + (1 / 4) * h22 + (1 / 3) * h13

theorem groupoidProduct_expansion (G Dg K : Matrix ι ι ℚ) (s t : ℚ) :
    groupoidMoved G Dg K s t * groupoidBase G K t =
      groupoidSum G K s t + (s * t) • (G * G + Dg - K) +
        (s * t ^ 2) • ((1 / 2 : ℚ) • (G * K) + Dg * G) +
        (s * t ^ 3) • ((1 / 2 : ℚ) • (Dg * K)) +
        (s ^ 2 * t) • ((1 / 2 : ℚ) • (K * G)) +
        (s ^ 2 * t ^ 2) • ((1 / 4 : ℚ) • (K * K)) := by
  simp only [groupoidMoved, groupoidBase, groupoidSum, add_mul, mul_add, one_mul, mul_one,
    smul_mul_assoc, mul_smul_comm, smul_smul, smul_add, add_smul, sub_eq_add_neg, mul_assoc]
  module

/-- Under the explicit additive composition hypothesis, `K = G² + (D_e g)[h]`. -/
theorem actionGroupoid_secondJet (G Dg K : Matrix ι ι ℚ)
    (hcomp : ∀ s t : ℚ, groupoidMoved G Dg K s t * groupoidBase G K t = groupoidSum G K s t) :
    K = G * G + Dg := by
  have hdiff : ∀ s t : ℚ,
      (s * t) • (G * G + Dg - K) +
        (s * t ^ 2) • ((1 / 2 : ℚ) • (G * K) + Dg * G) +
        (s * t ^ 3) • ((1 / 2 : ℚ) • (Dg * K)) +
        (s ^ 2 * t) • ((1 / 2 : ℚ) • (K * G)) +
        (s ^ 2 * t ^ 2) • ((1 / 4 : ℚ) • (K * K)) = 0 := by
    intro s t
    let R : Matrix ι ι ℚ :=
      (s * t) • (G * G + Dg - K) +
        (s * t ^ 2) • ((1 / 2 : ℚ) • (G * K) + Dg * G) +
        (s * t ^ 3) • ((1 / 2 : ℚ) • (Dg * K)) +
        (s ^ 2 * t) • ((1 / 2 : ℚ) • (K * G)) +
        (s ^ 2 * t ^ 2) • ((1 / 4 : ℚ) • (K * K))
    have hexp := groupoidProduct_expansion G Dg K s t
    rw [hcomp s t] at hexp
    have hgoal : groupoidSum G K s t = groupoidSum G K s t + R := by
      simpa [R, add_assoc, add_left_comm, add_comm] using hexp
    have hsub := congrArg (fun M : Matrix ι ι ℚ => M - groupoidSum G K s t) hgoal
    simpa [R, add_sub_cancel_left, sub_self] using hsub.symm
  let X := G * G + Dg - K
  let A := (1 / 2 : ℚ) • (G * K) + Dg * G
  let E := (1 / 2 : ℚ) • (Dg * K)
  let B := (1 / 2 : ℚ) • (K * G)
  let C := (1 / 4 : ℚ) • (K * K)
  have hX : X = 0 := by
    ext i j
    refine isolate_cross_entry (X i j) (A i j) (E i j) (B i j) (C i j) ?_
    intro s t
    have h0 := congr_fun (congr_fun (hdiff s t) i) j
    simp only [X, A, E, B, C, Matrix.add_apply, Matrix.smul_apply] at h0
    exact h0
  exact (sub_eq_zero.mp hX).symm

/-- The mixed cocycle is the equality of the two cross terms. -/
theorem actionGroupoid_mixedCocycle
    (Gξ Gζ Dξζ Dζξ : Matrix ι ι ℚ)
    (h : Gξ * Gζ + Dξζ = Gζ * Gξ + Dζξ) :
    Dζξ - Dξζ + (Gζ * Gξ - Gξ * Gζ) = 0 := by
  have hsub : Gξ * Gζ + Dξζ - (Gζ * Gξ + Dζξ) = 0 := sub_eq_zero.mpr h
  have hrewrite :
      Dζξ - Dξζ + (Gζ * Gξ - Gξ * Gζ) =
        -(Gξ * Gζ + Dξζ - (Gζ * Gξ + Dζξ)) := by
    abel
  rw [hrewrite, hsub, neg_zero]

end D0.Geometry
