import Mathlib.Tactic
import D0.Geometry.ArchiveExteriorFrameLift
import D0.Geometry.A4DObserverPositiveExterior

/-!
Review scope: this module owns only the canonical background-independent local quadratic obstruction.

# Scoped observer-positive local quadratic reference no-go

Review note: this module is a scoped no-go for the canonical background-independent
observer-positive local quadratic only. It does not claim a universal obstruction
against nonlinear / sourced / path / junction selectors.

Lean-owns theorem-ready handoff F/G from
`MEMO_A4D_LABELLED_REFERENCE_SELECTION_PRINCIPLE.md` (PR #117 research):

the canonical background-independent local quadratic

\[
E_{\alpha,\beta}(\delta)
=
\alpha\|b+\delta\|^2
+
\beta\|\delta\|^2,
\qquad
\alpha,\beta\ge0
\]

has an exact pure-gauge versus pure-shift incompatibility on the hostile
Role-space ray. Exact pure-gauge forces \(\beta=0\); the same coefficients then
erase pure-shift visibility (\(\kappa_*=0\)).

This is a **candidate-class** no-go only. It does not choose a physical overlap
law, does not invent curl/harmonic penalties, and does not start finite E
dressing. `EXP-A4D-FINITE-GRADED-COFRAME-DRESSING` stays BLOCKED.
-/

namespace D0.Geometry

open D0

local instance observerQuadraticRoleLinearOrder : LinearOrder Role :=
  LinearOrder.lift' roleCode roleCode_injective

set_option linter.unusedSimpArgs false

noncomputable section

/-! ## 0. Scalar hostile-ray energy -/

/-- Canonical scalar energy on the hostile ray \(\delta = t\,b\) at the rest
observer (memo §8.1): \(E_{\alpha,\beta}(t)=\alpha(1+t)^2+\beta t^2\). -/
def observerQuadraticRayEnergy (α β t : ℝ) : ℝ :=
  α * (1 + t) ^ 2 + β * t ^ 2

/-- Unique candidate minimizer coordinate \(t_*=-\alpha/(\alpha+\beta)\). -/
def observerQuadraticRayMinimizer (α β : ℝ) : ℝ :=
  -α / (α + β)

/-- Pure-shift / transported-reference mismatch coefficient on the ray:
\(\kappa_*=b+\delta_*=\bigl(\beta/(\alpha+\beta)\bigr)b\). -/
def observerQuadraticRayKappaCoeff (α β : ℝ) : ℝ :=
  β / (α + β)

/-- Role-space overlap minimizer \(\delta_*=t_*\cdot b\). -/
def observerQuadraticDeltaStar (α β : ℝ) (b : RoleSpace) : RoleSpace :=
  observerQuadraticRayMinimizer α β • b

/-- Role-space mismatch at the minimizer \(\kappa_*=b+\delta_*\). -/
def observerQuadraticKappaStar (α β : ℝ) (b : RoleSpace) : RoleSpace :=
  observerQuadraticRayKappaCoeff α β • b

/-! ## 1. Exact quadratic completion -/

theorem observerQuadraticRayEnergy_completion (α β t : ℝ) (hsum : α + β ≠ 0) :
    observerQuadraticRayEnergy α β t =
      (α + β) * (t + α / (α + β)) ^ 2 + (α * β) / (α + β) := by
  unfold observerQuadraticRayEnergy
  field_simp [hsum]
  ring

/-! ## 2. Unique minimizer -/

theorem observerQuadraticRayMinimizer_eq (α β : ℝ) :
    observerQuadraticRayMinimizer α β = -α / (α + β) :=
  rfl

theorem observerQuadraticRayKappaCoeff_eq (α β : ℝ) :
    observerQuadraticRayKappaCoeff α β = β / (α + β) :=
  rfl

private theorem ray_min_shift_cancel (α β : ℝ) (hsum : α + β ≠ 0) :
    observerQuadraticRayMinimizer α β + α / (α + β) = 0 := by
  simp only [observerQuadraticRayMinimizer]
  field_simp [hsum]
  ring

theorem observerQuadraticRayEnergy_eq_min_plus_gap (α β t : ℝ) (hsum : α + β ≠ 0) :
    observerQuadraticRayEnergy α β t =
      observerQuadraticRayEnergy α β (observerQuadraticRayMinimizer α β) +
        (α + β) * (t - observerQuadraticRayMinimizer α β) ^ 2 := by
  have hcomp := observerQuadraticRayEnergy_completion α β t hsum
  have hmin :=
    observerQuadraticRayEnergy_completion α β (observerQuadraticRayMinimizer α β) hsum
  have hvanish := ray_min_shift_cancel α β hsum
  -- Rewrite both sides via the completion formula.
  calc
    observerQuadraticRayEnergy α β t
        = (α + β) * (t + α / (α + β)) ^ 2 + (α * β) / (α + β) := hcomp
    _ = (α + β) * (t - observerQuadraticRayMinimizer α β) ^ 2 + (α * β) / (α + β) := by
          have : t + α / (α + β) = t - observerQuadraticRayMinimizer α β := by
            simp only [observerQuadraticRayMinimizer]
            ring
          simp [this]
    _ = observerQuadraticRayEnergy α β (observerQuadraticRayMinimizer α β) +
          (α + β) * (t - observerQuadraticRayMinimizer α β) ^ 2 := by
          have : observerQuadraticRayEnergy α β (observerQuadraticRayMinimizer α β) =
              (α * β) / (α + β) := by
            simp [hmin, hvanish]
          rw [this]
          ring

theorem observerQuadraticRayEnergy_ge_min (α β t : ℝ) (hsum : 0 < α + β) :
    observerQuadraticRayEnergy α β (observerQuadraticRayMinimizer α β) ≤
      observerQuadraticRayEnergy α β t := by
  have hne : α + β ≠ 0 := ne_of_gt hsum
  rw [observerQuadraticRayEnergy_eq_min_plus_gap α β t hne]
  exact le_add_of_nonneg_right (mul_nonneg (le_of_lt hsum) (sq_nonneg _))

theorem observerQuadraticRayMinimizer_unique (α β t : ℝ) (hsum : 0 < α + β)
    (hle : observerQuadraticRayEnergy α β t ≤
      observerQuadraticRayEnergy α β (observerQuadraticRayMinimizer α β)) :
    t = observerQuadraticRayMinimizer α β := by
  have hne : α + β ≠ 0 := ne_of_gt hsum
  have hgap := observerQuadraticRayEnergy_eq_min_plus_gap α β t hne
  have hle' : observerQuadraticRayEnergy α β t ≤
      observerQuadraticRayEnergy α β (observerQuadraticRayMinimizer α β) := hle
  have hgap0 :
      (α + β) * (t - observerQuadraticRayMinimizer α β) ^ 2 = 0 := by
    nlinarith [hgap, hle', sq_nonneg (t - observerQuadraticRayMinimizer α β),
      le_of_lt hsum]
  have hsq : (t - observerQuadraticRayMinimizer α β) ^ 2 = 0 := by
    exact (mul_eq_zero.mp hgap0).resolve_left (ne_of_gt hsum)
  have hsub : t - observerQuadraticRayMinimizer α β = 0 := by
    exact (sq_eq_zero_iff).mp hsq
  exact sub_eq_zero.mp hsub

theorem observerQuadraticDeltaStar_eq (α β : ℝ) (b : RoleSpace) :
    observerQuadraticDeltaStar α β b = (-α / (α + β)) • b :=
  rfl

theorem observerQuadraticKappaStar_eq (α β : ℝ) (b : RoleSpace) :
    observerQuadraticKappaStar α β b = (β / (α + β)) • b :=
  rfl

theorem observerQuadraticKappaStar_eq_b_add_delta (α β : ℝ) (b : RoleSpace)
    (hsum : α + β ≠ 0) :
    observerQuadraticKappaStar α β b =
      b + observerQuadraticDeltaStar α β b := by
  ext r
  simp only [observerQuadraticKappaStar, observerQuadraticDeltaStar,
    observerQuadraticRayKappaCoeff, observerQuadraticRayMinimizer,
    Pi.add_apply, Pi.smul_apply, smul_eq_mul]
  field_simp [hsum]
  ring

/-! ## 3. Exact pure-gauge ⇒ β = 0 -/

private theorem smul_eq_neg_coeff {c : ℝ} {b : RoleSpace} (hb : b ≠ 0)
    (h : c • b = -b) : c = -1 := by
  have : c • b = (-1 : ℝ) • b := by simpa [neg_one_smul] using h
  exact smul_left_injective ℝ hb this

theorem observerQuadratic_exact_pureGauge_forces_beta_zero
    (α β : ℝ) (_hα : 0 ≤ α) (_hβ : 0 ≤ β) (hsum : 0 < α + β)
    (b : RoleSpace) (hb : b ≠ 0)
    (hδ : observerQuadraticDeltaStar α β b = -b) :
    β = 0 := by
  have hne : α + β ≠ 0 := ne_of_gt hsum
  have hc : -α / (α + β) = -1 :=
    smul_eq_neg_coeff hb (by simpa [observerQuadraticDeltaStar_eq] using hδ)
  have hmul : -α = -(α + β) := by
    have := congrArg (fun x : ℝ => x * (α + β)) hc
    field_simp [hne] at this
    exact this
  linarith

/-! ## 4. Pure-shift failure at gauge endpoint -/

theorem observerQuadraticRayMinimizer_pureGauge_endpoint (α : ℝ) (hα : 0 < α) :
    observerQuadraticRayMinimizer α 0 = -1 := by
  simp [observerQuadraticRayMinimizer, hα.ne']

theorem observerQuadratic_pureShift_failure_at_gauge_endpoint
    (α : ℝ) (hα : 0 < α) (b : RoleSpace) :
    observerQuadraticDeltaStar α 0 b = -b ∧
      observerQuadraticKappaStar α 0 b = 0 := by
  constructor
  · simp [observerQuadraticDeltaStar, observerQuadraticRayMinimizer_pureGauge_endpoint α hα,
      neg_one_smul]
  · simp [observerQuadraticKappaStar, observerQuadraticRayKappaCoeff]

/-! ## 5. Converse endpoint α = 0 -/

theorem observerQuadratic_converse_pureShift_endpoint
    (β : ℝ) (hβ : 0 < β) (b : RoleSpace) :
    observerQuadraticDeltaStar 0 β b = 0 ∧
      observerQuadraticKappaStar 0 β b = b := by
  constructor
  · simp [observerQuadraticDeltaStar, observerQuadraticRayMinimizer]
  · simp [observerQuadraticKappaStar, observerQuadraticRayKappaCoeff, hβ.ne', one_smul]

/-! ## 6. Positive interpolation boundary -/

theorem observerQuadratic_positive_interpolation_boundary
    (α β : ℝ) (hα : 0 < α) (hβ : 0 < β) (b : RoleSpace) (hb : b ≠ 0) :
    observerQuadraticDeltaStar α β b ≠ -b ∧
      observerQuadraticDeltaStar α β b ≠ 0 := by
  have hsum : 0 < α + β := add_pos hα hβ
  have hne : α + β ≠ 0 := ne_of_gt hsum
  constructor
  · intro hδ
    exact hβ.ne'
      (observerQuadratic_exact_pureGauge_forces_beta_zero α β hα.le hβ.le hsum b hb hδ)
  · intro hδ
    have hc : -α / (α + β) = 0 :=
      smul_left_injective ℝ hb (by
        simpa [observerQuadraticDeltaStar_eq, zero_smul] using hδ)
    have hmul : -α = 0 := by
      have := congrArg (fun x : ℝ => x * (α + β)) hc
      field_simp [hne] at this
      linarith [this]
    have hα0 : α = 0 := by linarith [hmul]
    exact hα.ne' hα0

/-! ## 7. Scoped no-go -/

/-- No background-independent nonnegative pair \((\alpha,\beta)\) with \(\alpha+\beta>0\)
makes the canonical local quadratic select both exact pure-gauge
(\(\delta_*=-b\)) and pure-shift visibility (\(\kappa_*=b\)).

Scoped to this quadratic class only — not a no-go for nonlinear or sourced
overlap functionals. -/
theorem observerQuadraticReference_no_go
    (α β : ℝ) (hα : 0 ≤ α) (hβ : 0 ≤ β) (hsum : 0 < α + β)
    (b : RoleSpace) (hb : b ≠ 0)
    (hgauge : observerQuadraticDeltaStar α β b = -b)
    (hshift : observerQuadraticKappaStar α β b = b) :
    False := by
  have hβ0 :=
    observerQuadratic_exact_pureGauge_forces_beta_zero α β hα hβ hsum b hb hgauge
  subst hβ0
  have hαpos : 0 < α := by simpa using hsum
  have hκ := (observerQuadratic_pureShift_failure_at_gauge_endpoint α hαpos b).2
  have : (b : RoleSpace) = 0 := by simpa [hκ] using hshift.symm
  exact hb this

/-! ## Optional rest-observer bridge -/

def roleCountingNormSq (v : RoleSpace) : ℝ :=
  ∑ r : Role, (v r) ^ 2

theorem roleCountingNormSq_eq_restObserver (v : RoleSpace) :
    roleCountingNormSq v =
      ∑ r : Role, ∑ s : Role,
        v r * observerMetric restObserver r s * v s := by
  simp only [roleCountingNormSq, observerMetric_restObserver]
  simp [pow_two]

private theorem roleCountingNormSq_smul (c : ℝ) (b : RoleSpace) :
    roleCountingNormSq (c • b) = c ^ 2 * roleCountingNormSq b := by
  simp only [roleCountingNormSq, Pi.smul_apply, smul_eq_mul, mul_pow, Finset.mul_sum]

theorem observerQuadraticRay_restObserver_restriction
    (α β t : ℝ) (b : RoleSpace) (hb : roleCountingNormSq b = 1) :
    α * roleCountingNormSq (b + t • b) + β * roleCountingNormSq (t • b) =
      observerQuadraticRayEnergy α β t := by
  have h1 : b + t • b = (1 + t) • b := by rw [add_smul, one_smul]
  simp only [observerQuadraticRayEnergy, h1, roleCountingNormSq_smul, hb, mul_one]

#print axioms observerQuadraticRayEnergy_completion
#print axioms observerQuadraticRayMinimizer_unique
#print axioms observerQuadratic_exact_pureGauge_forces_beta_zero
#print axioms observerQuadratic_pureShift_failure_at_gauge_endpoint
#print axioms observerQuadratic_converse_pureShift_endpoint
#print axioms observerQuadratic_positive_interpolation_boundary
#print axioms observerQuadraticReference_no_go
#print axioms observerQuadraticRay_restObserver_restriction

end

end D0.Geometry
