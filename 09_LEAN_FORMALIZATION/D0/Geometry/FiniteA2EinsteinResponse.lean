import D0.Geometry.GradedBianchiClosure

namespace D0.Geometry

/-!
# Finite A2 response tensor — structure, Einstein closure, and the conserved-source probe

* A response tensor is a symmetric, divergence-balanced finite tensor `G : N → N → ℝ`
  (the discrete contracted-Bianchi class).
* The Einstein transform maps the class into itself.
* A **conserved source** `T` (zero row sums) couples to a response through
  `coupling G T = ∑ i ∑ j, G i j * T i j`.
* **Scalar decoupling theorem:** every constant (scalar-only) response couples to zero
  against every conserved source — scalar responses carry no information about them.
-/

variable {N : Type} [Fintype N] [DecidableEq N]

structure FiniteA2ResponseTensor (N : Type) [Fintype N] [DecidableEq N] [Nonempty N] where
  G : N → N → ℝ
  hsym : ∀ i j, G i j = G j i
  hdiv : IsDivergenceBalanced G

/-- The Einstein transform stays inside the response class. -/
noncomputable def responseEinstein {N : Type} [Fintype N] [DecidableEq N] [Nonempty N]
    (R : FiniteA2ResponseTensor N) : FiniteA2ResponseTensor N where
  G := einsteinTransform R.G
  hsym := einstein_symm R.hsym
  hdiv := einstein_balanced_of_balanced R.hdiv
/-- Coupling of a response with a source. -/
def coupling (S T : N → N → ℝ) : ℝ := ∑ i, ∑ j, S i j * T i j

/-- A conserved source (all row sums vanish). -/
def IsConservedSource (T : N → N → ℝ) : Prop := ∀ i, ∑ j, T i j = 0

/-- **Scalar decoupling.**  Every constant response couples to zero against every conserved
    source — scalar-only responses are blind to exactly the sources matter can deliver. -/
theorem scalar_coupling_of_conserved (κ : ℝ) (T : N → N → ℝ) (hcons : IsConservedSource T) :
    coupling (fun _ _ => κ) T = 0 := by
  classical
  unfold coupling
  have hstep : ∀ i : N, (∑ j, κ * T i j) = 0 := by
    intro i
    rw [← Finset.mul_sum, hcons i, mul_zero]
  rw [Finset.sum_congr rfl fun i _ => hstep i]
  simp

end D0.Geometry
