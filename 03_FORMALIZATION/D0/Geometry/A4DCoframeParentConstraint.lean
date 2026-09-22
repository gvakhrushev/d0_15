import Mathlib.Tactic
import D0.Geometry.ArchiveCubicalDifferential
import D0.Geometry.A4DRolePairMetricCarrier

namespace D0.Geometry

open D0

noncomputable section

/-!
# A4D coframe parent constraint

Finite theorem-ready algebra for the parent constraint m = R(e) + n.

The concrete readout uses the already-owned forward difference and backward averaging.
The generic transport theorem is intentionally only a carrier-compatibility statement.
No nonlinear connection, Hodge constitutive law, Lorentz gauge, continuum covariance,
or Einstein equation is asserted.
-/

/-- Pre-centered coframe perturbations: direction r and frame component a at each site. -/
abbrev LocalCoframeField (N : ℕ) :=
  ArchiveRolePhaseGroup N → Role → Role → ℝ

/-- The frozen centered metric readout R(e)_{ab} = A_a e_a^b + A_b e_b^a. -/
def coframeMetricReadout (N : ℕ) (e : LocalCoframeField N) :
    LocalSymRoleField N :=
  fun x =>
    { toMatrix := fun a b =>
        backwardAverage N a (fun y => e y a b) x +
          backwardAverage N b (fun y => e y b a) x
      symmetric := by
        intro a b
        ring }

/-- Forward coframe gauge strain d_f xi. -/
def forwardGaugeCoframe (N : ℕ) (xi : LocalRoleVector N) :
    LocalCoframeField N :=
  fun x r a => forwardDifference N r (fun y => xi y a) x

/-- The concrete staggered readout exactly reconstructs the existing centered metric gauge. -/
theorem coframeMetricReadout_forwardGauge (N : ℕ) (xi : LocalRoleVector N) :
    coframeMetricReadout N (forwardGaugeCoframe N xi) =
      symmetricRoleGradient N xi := by
  funext x
  apply SymRoleTensor.ext
  funext a b
  change
    backwardAverage N a
        (forwardDifference N a (fun y => xi y b)) x +
      backwardAverage N b
        (forwardDifference N b (fun y => xi y a)) x =
      centeredDifference N a (fun y => xi y b) x +
        centeredDifference N b (fun y => xi y a) x
  have ha := congrFun
    (centeredDifference_eq_average_forward N a (fun y => xi y b)) x
  have hb := congrFun
    (centeredDifference_eq_average_forward N b (fun y => xi y a)) x
  rw [← ha, ← hb]

/-- Pointwise parent constraint, with the Nyquist/auxiliary residue kept explicit. -/
def CoframeParentConstraint (N : ℕ)
    (m : LocalSymRoleField N) (e : LocalCoframeField N)
    (n : LocalSymRoleField N) : Prop :=
  ∀ x a b,
    (m x).toMatrix a b =
      (coframeMetricReadout N e x).toMatrix a b + (n x).toMatrix a b

/-- Generic transport consequence of differentiating m = R(e) + n.

Hypotheses are exactly the pieces used:
delta m = K xi, delta e = d_f xi + T, delta n = 0,
the linearized parent constraint, and R(d_f xi) = K xi.
-/
theorem parentConstraint_transport_in_readout_kernel
    {E M X : Type*}
    [AddCommGroup E] [Module ℝ E]
    [AddCommGroup M] [Module ℝ M]
    [AddCommGroup X] [Module ℝ X]
    (R : E →ₗ[ℝ] M) (df : X →ₗ[ℝ] E) (K : X →ₗ[ℝ] M)
    (xi : X) (deltaM : M) (deltaE T : E) (deltaN : M)
    (hparent : deltaM = R deltaE + deltaN)
    (hmetric : deltaM = K xi)
    (hcoframe : deltaE = df xi + T)
    (hresidue : deltaN = 0)
    (hreadout : R (df xi) = K xi) :
    R T = 0 := by
  have h : K xi = K xi + R T := by
    calc
      K xi = deltaM := hmetric.symm
      _ = R deltaE + deltaN := hparent
      _ = R (df xi + T) + 0 := by rw [hcoframe, hresidue]
      _ = R (df xi) + R T := by simp
      _ = K xi + R T := by rw [hreadout]
  have hzero : K xi + 0 = K xi + R T := by
    simpa using h
  exact (add_left_cancel hzero).symm

/-! ## Exact odd one-role control: L = 5 -/

/-- Five-site scalar one-role sector used as the exact odd-cycle control. -/
abbrev OddCycle5Field := Fin 5 → ℝ

/-- Cyclic predecessor on five sites. -/
def oddCycle5Prev (i : Fin 5) : Fin 5 := i - 1

/-- One-role centered readout A = (I + U^{-1}) / 2 on L = 5. -/
def oddCycle5Readout (f : OddCycle5Field) : OddCycle5Field :=
  fun i => (f i + f (oddCycle5Prev i)) / 2

/-- Exact odd-cycle kernel control: the L = 5 centering readout has trivial kernel. -/
theorem oddCycle5Readout_kernel_zero (f : OddCycle5Field)
    (h : oddCycle5Readout f = 0) :
    f = 0 := by
  have hstep : ∀ i : Fin 5, f i + f (i - 1) = 0 := by
    intro i
    have hi := congrFun h i
    simp [oddCycle5Readout, oddCycle5Prev] at hi
    linarith
  have h0 := hstep 0
  have h1 := hstep 1
  have h2 := hstep 2
  have h3 := hstep 3
  have h4 := hstep 4
  have z0 : (0 : Fin 5) - 1 = 4 := by decide
  have z1 : (1 : Fin 5) - 1 = 0 := by decide
  have z2 : (2 : Fin 5) - 1 = 1 := by decide
  have z3 : (3 : Fin 5) - 1 = 2 := by decide
  have z4 : (4 : Fin 5) - 1 = 3 := by decide
  rw [z0] at h0
  rw [z1] at h1
  rw [z2] at h2
  rw [z3] at h3
  rw [z4] at h4
  have f0 : f 0 = 0 := by linarith
  have f1 : f 1 = 0 := by linarith
  have f2 : f 2 = 0 := by linarith
  have f3 : f 3 = 0 := by linarith
  have f4 : f 4 = 0 := by linarith
  funext i
  fin_cases i <;> simp [f0, f1, f2, f3, f4]

/-- Capstone for the exact odd one-role restriction: readout-trivial transport vanishes. -/
theorem odd_one_role_transport_zero (T : OddCycle5Field)
    (hT : oddCycle5Readout T = 0) :
    T = 0 :=
  oddCycle5Readout_kernel_zero T hT

end

end D0.Geometry
