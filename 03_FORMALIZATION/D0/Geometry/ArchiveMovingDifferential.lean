import Mathlib.Tactic

/-!
# Moving graded differential

For linear equivalences `Q_k` on each degree slot,
`d'_k = Q_{k+1} ∘ d_k ∘ Q_k⁻¹`.

`LinearEquiv.trans` applies its left argument first, matching the chain-connection
owner. Transformation by `Q` and then by `R` is therefore transformation by
`Q.trans R`.

The infinitesimal law is the formal first-order identity
`(I + G₁) d (I - G₀) = d + (G₁ d - d G₀) - G₁ d G₀`.
No analytic exponential and no physical background action are used.
Nilpotency is not assumed.
-/

namespace D0.Geometry

variable {K V0 V1 V2 : Type*} [CommRing K]
variable [AddCommGroup V0] [Module K V0]
variable [AddCommGroup V1] [Module K V1]
variable [AddCommGroup V2] [Module K V2]

/-- `d' = Q_{k+1} ∘ d ∘ Q_k⁻¹`. -/
def movingDifferential (Q : V0 ≃ₗ[K] V0) (R : V1 ≃ₗ[K] V1)
    (d : V0 →ₗ[K] V1) : V0 →ₗ[K] V1 :=
  R.toLinearMap.comp (d.comp Q.symm.toLinearMap)

@[simp] theorem movingDifferential_apply
    (Q : V0 ≃ₗ[K] V0) (R : V1 ≃ₗ[K] V1) (d : V0 →ₗ[K] V1) (v : V0) :
    movingDifferential Q R d v = R (d (Q.symm v)) := rfl

/-- Applying the `Q`-transformation and then the `R`-transformation is the
transformation by `Q.trans R`. -/
theorem movingDifferential_comp
    (Q0 R0 : V0 ≃ₗ[K] V0) (Q1 R1 : V1 ≃ₗ[K] V1) (d : V0 →ₗ[K] V1) :
    movingDifferential (Q0.trans R0) (Q1.trans R1) d =
      movingDifferential R0 R1 (movingDifferential Q0 Q1 d) := by
  ext v
  simp [movingDifferential, LinearEquiv.trans_apply]

/-- Curvature conjugates: `d'_{k+1} ∘ d'_k = Q_{k+2} ∘ (d_{k+1} ∘ d_k) ∘ Q_k⁻¹`. -/
theorem movingDifferential_curvature
    (Q0 : V0 ≃ₗ[K] V0) (Q1 : V1 ≃ₗ[K] V1) (Q2 : V2 ≃ₗ[K] V2)
    (d0 : V0 →ₗ[K] V1) (d1 : V1 →ₗ[K] V2) :
    (movingDifferential Q1 Q2 d1).comp (movingDifferential Q0 Q1 d0) =
      Q2.toLinearMap.comp ((d1.comp d0).comp Q0.symm.toLinearMap) := by
  ext v
  simp [movingDifferential]

/-- A square that already vanishes stays zero after moving the slots.
A nonzero square is conjugated, not erased. -/
theorem movingDifferential_preserves_sq_zero
    (Q0 : V0 ≃ₗ[K] V0) (Q1 : V1 ≃ₗ[K] V1) (Q2 : V2 ≃ₗ[K] V2)
    (d0 : V0 →ₗ[K] V1) (d1 : V1 →ₗ[K] V2)
    (h : d1.comp d0 = 0) :
    (movingDifferential Q1 Q2 d1).comp (movingDifferential Q0 Q1 d0) = 0 := by
  rw [movingDifferential_curvature, h]
  ext v
  simp

/-- Formal first-order variation `δd = G₁ d - d G₀`. -/
def movingDifferentialVariation (G0 : V0 →ₗ[K] V0) (G1 : V1 →ₗ[K] V1)
    (d : V0 →ₗ[K] V1) : V0 →ₗ[K] V1 :=
  G1.comp d - d.comp G0

@[simp] theorem movingDifferentialVariation_apply
    (G0 : V0 →ₗ[K] V0) (G1 : V1 →ₗ[K] V1) (d : V0 →ₗ[K] V1) (v : V0) :
    movingDifferentialVariation G0 G1 d v = G1 (d v) - d (G0 v) := by
  simp [movingDifferentialVariation]

/-- `(I + G₁) d (I - G₀) = d + δd - G₁ d G₀`, with `I - G₀` the formal
first-order inverse of `I + G₀`. The quadratic remainder is kept explicit. -/
theorem movingDifferential_infinitesimal
    (G0 : V0 →ₗ[K] V0) (G1 : V1 →ₗ[K] V1) (d : V0 →ₗ[K] V1) :
    ((LinearMap.id : V1 →ₗ[K] V1) + G1).comp
        (d.comp ((LinearMap.id : V0 →ₗ[K] V0) - G0)) =
      d + movingDifferentialVariation G0 G1 d - (G1.comp d).comp G0 := by
  ext v
  simp [movingDifferentialVariation, sub_eq_add_neg, add_assoc, add_left_comm, add_comm]

end D0.Geometry
