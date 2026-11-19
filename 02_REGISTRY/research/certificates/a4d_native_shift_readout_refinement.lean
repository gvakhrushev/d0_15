import Mathlib.Algebra.Group.Defs

/-!
# Positive-ray readouts cannot be path-functorial and nontrivial

For an additive translation carrier, a readout that forgets the magnitude
(`f (2 • v) = f v`) cannot also compose by multiplication along concatenated
paths unless its values are the identity.  This is an abstract group theorem;
the adjacent exact certificate binds its hypotheses to the owned affine
shift law and the actual D0 CAR record operator.
-/

namespace D0.Research.AffineRayRefinement

variable {V G : Type*} [AddCommGroup V] [Group G]

/-- Scaling-blindness on the one positive rescaling needed for subdivision. -/
def DoubledRayInvariant (f : V → G) : Prop :=
  ∀ v, f (2 • v) = f v

/-- Assignment of a group element to a concatenated additive path. -/
def PathMultiplicative (f : V → G) : Prop :=
  ∀ v w, f (v + w) = f v * f w

/-- A positive-ray-invariant group-valued readout that respects path
concatenation must be trivial.  In particular, this applies to unitary
returns; no finite-dimensional assumption is needed for this elementary
subdivision obstruction. -/
theorem doubled_ray_path_multiplicative_trivial
    (f : V → G)
    (h_ray : DoubledRayInvariant f)
    (h_path : PathMultiplicative f) :
    ∀ v, f v = 1 := by
  intro v
  have hscale : (2 : ℕ) • v = v + v := two_nsmul v
  have h_idem : f v = f v * f v := by
    calc
      f v = f (2 • v) := (h_ray v).symm
      _ = f (v + v) := by rw [hscale]
      _ = f v * f v := h_path v v
  have h_cancel := congrArg (fun z : G => (f v)⁻¹ * z) h_idem
  simpa [mul_assoc] using h_cancel.symm

end D0.Research.AffineRayRefinement

#print axioms D0.Research.AffineRayRefinement.doubled_ray_path_multiplicative_trivial
#check D0.Research.AffineRayRefinement.doubled_ray_path_multiplicative_trivial
