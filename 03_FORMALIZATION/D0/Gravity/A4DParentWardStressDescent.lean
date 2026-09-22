import Mathlib.Tactic
import D0.Geometry.A4DCoframeParentConstraint
import D0.Gravity.A4DLinearizedMetricResponse

namespace D0.Gravity

open D0
open D0.Geometry

noncomputable section

/-!
# Conditional parent-Ward stress descent

The parent Ward identity, the auxiliary equations of motion, and the coframe equation
are explicit hypotheses.  The only owned dynamical ingredient reused here is the finite
adjoint identity for symmetricRoleGradient.

No connection, physical Hodge law, local Lorentz gauge, nonlinear Einstein equation,
Nyquist stress, or continuum Diff covariance is asserted.
-/

/-- Name used by the parent descent theorem for the already-owned centered divergence. -/
abbrev centeredRoleDivergence (N : ℕ) (Lambda : LocalSymRoleField N) :
    LocalRoleVector N :=
  divergenceVector N Lambda

/-- Parent Ward + auxiliary EOM + coframe EOM force the metric multiplier to annihilate
all constrained metric gauge variations. -/
theorem metricMultiplier_pairing_zero_of_parentWard
    {E : Type*}
    (N : ℕ)
    (df : LocalRoleVector N → E)
    (readout : E → LocalSymRoleField N)
    (coframeEuler : E → ℝ)
    (auxiliaryWardTerm : LocalRoleVector N → ℝ)
    (Lambda : LocalSymRoleField N)
    (hconstraint :
      ∀ xi, readout (df xi) = symmetricRoleGradient N xi)
    (hparentWard :
      ∀ xi,
        coframeEuler (df xi) +
            auxiliaryWardTerm xi +
            tensorInnerProduct N Lambda (readout (df xi)) = 0)
    (hauxiliaryEOM : ∀ xi, auxiliaryWardTerm xi = 0)
    (hcoframeEOM : ∀ xi, coframeEuler (df xi) = 0)
    (xi : LocalRoleVector N) :
    tensorInnerProduct N Lambda (symmetricRoleGradient N xi) = 0 := by
  have hw := hparentWard xi
  rw [hauxiliaryEOM xi, hcoframeEOM xi, hconstraint xi] at hw
  simpa using hw

/-- Coordinate probe on the finite site/Role vector carrier. -/
def roleVectorProbe (N : ℕ)
    (x0 : ArchiveRolePhaseGroup N) (b0 : Role) :
    LocalRoleVector N :=
  fun x b => if x = x0 ∧ b = b0 then 1 else 0

/-- The finite pairing with a coordinate probe reads exactly one vector component. -/
theorem roleVectorInnerProduct_probe (N : ℕ)
    (x0 : ArchiveRolePhaseGroup N) (b0 : Role)
    (v : LocalRoleVector N) :
    roleVectorInnerProduct N (roleVectorProbe N x0 b0) v =
      v x0 b0 := by
  classical
  unfold roleVectorInnerProduct scalarInnerProduct roleVectorProbe
  rw [Finset.sum_eq_single b0]
  · rw [Finset.sum_eq_single x0]
    · simp
    · intro x hx hne
      simp [hne]
    · simp
  · intro b hb hne
    apply Finset.sum_eq_zero
    intro x hx
    simp [hne]
  · simp

/-- Vanishing metric pairing against every symmetricRoleGradient implies exact
centered Role divergence zero, by the owned adjoint theorem. -/
theorem centeredRoleDivergence_zero_of_metric_pairing
    (N : ℕ) (Lambda : LocalSymRoleField N)
    (hmetric :
      ∀ xi : LocalRoleVector N,
        tensorInnerProduct N Lambda (symmetricRoleGradient N xi) = 0) :
    centeredRoleDivergence N Lambda = 0 := by
  funext x b
  let probe := roleVectorProbe N x b
  have hpair :
      tensorInnerProduct N (symmetricRoleGradient N probe) Lambda = 0 := by
    calc
      tensorInnerProduct N (symmetricRoleGradient N probe) Lambda =
          tensorInnerProduct N Lambda (symmetricRoleGradient N probe) :=
        tensorInnerProduct_symm N _ _
      _ = 0 := hmetric probe
  have hadj := symmetricRoleGradient_adjoint N probe Lambda
  have hinner :
      roleVectorInnerProduct N probe (divergenceVector N Lambda) = 0 := by
    rw [hpair] at hadj
    linarith
  dsimp [probe] at hinner
  rw [roleVectorInnerProduct_probe N x b (divergenceVector N Lambda)] at hinner
  exact hinner

/-- Final conditional descent capstone. -/
theorem centeredRoleDivergence_zero_of_parentWard
    {E : Type*}
    (N : ℕ)
    (df : LocalRoleVector N → E)
    (readout : E → LocalSymRoleField N)
    (coframeEuler : E → ℝ)
    (auxiliaryWardTerm : LocalRoleVector N → ℝ)
    (Lambda : LocalSymRoleField N)
    (hconstraint :
      ∀ xi, readout (df xi) = symmetricRoleGradient N xi)
    (hparentWard :
      ∀ xi,
        coframeEuler (df xi) +
            auxiliaryWardTerm xi +
            tensorInnerProduct N Lambda (readout (df xi)) = 0)
    (hauxiliaryEOM : ∀ xi, auxiliaryWardTerm xi = 0)
    (hcoframeEOM : ∀ xi, coframeEuler (df xi) = 0) :
    centeredRoleDivergence N Lambda = 0 := by
  apply centeredRoleDivergence_zero_of_metric_pairing N Lambda
  intro xi
  exact metricMultiplier_pairing_zero_of_parentWard
    N df readout coframeEuler auxiliaryWardTerm Lambda
    hconstraint hparentWard hauxiliaryEOM hcoframeEOM xi

end

end D0.Gravity
