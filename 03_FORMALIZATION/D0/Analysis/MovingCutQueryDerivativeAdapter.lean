import D0.Analysis.MovingProjectorVariableParameters
import D0.Geometry.MovingCutQueryCancellation

/-!
Derivative adapter for the #334 §7cu rank-one control. This is a finite matrix
calculation; it neither admits these curves as physical operations nor selects
the complete native source. The owner and all physical obligations remain open.
-/

namespace D0.Analysis.MovingCutQueryDerivativeAdapter

open Filter D0.Algebra.MovingProjectorTransport
open scoped Topology Matrix.Norms.Frobenius
noncomputable section

abbrev M2 := Matrix (Fin 2) (Fin 2) ℂ

/-- The existing orthogonal-projector curve with the source's exact velocity. -/
def movingP (t : ℝ) : M2 := exampleProjector ((4 / 5 : ℝ) * t)

/-- A reflection on the same rank-one orbit; it is unitary at every time. -/
def movingU (t : ℝ) : M2 := (2 : ℝ) • exampleProjector ((1 / 2 : ℝ) + t) - 1

def P0 : M2 := exampleProjectorBase
def U0 : M2 := exampleReflection
def dP : M2 := !![(0 : ℂ), 4 / 5; 4 / 5, 0]
def dU : M2 := !![-(32 / 25 : ℂ), 24 / 25; 24 / 25, 32 / 25]

theorem movingP_zero : movingP 0 = P0 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [movingP, P0, exampleProjector, exampleProjectorBase,
      exampleProjectorVelocity, exampleProjectorOther, Complex.real_smul]

theorem movingU_zero : movingU 0 = U0 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [movingU, U0, exampleProjector, exampleProjectorBase,
      exampleProjectorVelocity, exampleProjectorOther, exampleReflection,
      Complex.real_smul, Matrix.one_apply]

theorem movingP_idempotent (t : ℝ) : movingP t * movingP t = movingP t :=
  exampleProjector_idempotent _

theorem movingP_selfadjoint (t : ℝ) : star (movingP t) = movingP t :=
  exampleProjector_selfadjoint _

theorem movingU_isometry (t : ℝ) : star (movingU t) * movingU t = 1 := by
  have hi := exampleProjector_idempotent ((1 / 2 : ℝ) + t)
  have hs := exampleProjector_selfadjoint ((1 / 2 : ℝ) + t)
  simp only [movingU, two_smul, star_sub, star_add, star_one, hs]
  noncomm_ring [hi]

theorem movingP_derivative : HasDerivAt movingP dP 0 := by
  have harg : HasDerivAt (fun t : ℝ => (4 / 5 : ℝ) * t) (4 / 5) 0 := by
    simpa using (hasDerivAt_id' (0 : ℝ)).const_mul (4 / 5 : ℝ)
  have hf : HasDerivAt exampleProjector exampleProjectorVelocity
      ((fun t : ℝ => (4 / 5 : ℝ) * t) 0) := by
    simpa using exampleProjector_hasDerivAt
  have h := hf.scomp (0 : ℝ) harg
  have hm : (4 / 5 : ℝ) • exampleProjectorVelocity = dP := by
    ext i j
    fin_cases i <;> fin_cases j <;>
      norm_num [exampleProjectorVelocity, dP, Complex.real_smul]
  simpa [movingP, hm] using h

theorem movingU_derivative : HasDerivAt movingU dU 0 := by
  have ha : HasDerivAt (fun t : ℝ => (1 / 2 : ℝ) + t) 1 0 := by
    simpa using (hasDerivAt_id' (0 : ℝ)).const_add (1 / 2 : ℝ)
  have hs : HasDerivAt (fun t : ℝ => ((1 / 2 : ℝ) + t)^2) 1 0 := by
    simpa using ha.pow 2
  have hd : HasDerivAt (fun t : ℝ => 1 + ((1 / 2 : ℝ) + t)^2) 1 0 := by
    exact (hasDerivAt_const_add_iff (1 : ℝ)).2 hs
  have hi : HasDerivAt (fun t : ℝ => (1 + ((1 / 2 : ℝ) + t)^2)⁻¹)
      (-(16 / 25 : ℝ)) 0 := by
    have h := hd.inv (by norm_num)
    norm_num at h ⊢
    exact h
  have hn : HasDerivAt
      (fun t : ℝ => exampleProjectorBase + ((1 / 2 : ℝ) + t) • exampleProjectorVelocity +
        ((1 / 2 : ℝ) + t)^2 • exampleProjectorOther)
      (exampleProjectorVelocity + exampleProjectorOther) 0 := by
    have h0 := hasDerivAt_const (0 : ℝ) exampleProjectorBase
    have h1 := ha.smul_const exampleProjectorVelocity
    have h2 := hs.smul_const exampleProjectorOther
    simpa using (h0.add h1).add h2
  have h := (hi.smul hn).const_smul (2 : ℝ)
  have h := h.sub (hasDerivAt_const (0 : ℝ) (1 : M2))
  convert h using 1
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [dU, exampleProjectorBase, exampleProjectorVelocity,
      exampleProjectorOther, Complex.real_smul]

def feedback (P U : ℝ → M2) (t : ℝ) : ℝ :=
  -Real.log ((1 - ((1 / 4 : ℝ) : ℂ) •
    (star (cut (P t) (U t)) * cut (P t) (U t))).det.re)

def feedbackSource (vP vU : M2) : ℝ :=
  let C := cut P0 U0
  let R := (1 - ((1 / 4 : ℝ) : ℂ) • (star C * C))⁻¹
  (1 / 4 : ℝ) * (2 * (Matrix.trace (R * star C *
    ((1 - P0) * (vU - comm (generator P0 vP) U0) * P0))).re)

theorem feedback_resolvent :
    (1 - ((1 / 4 : ℝ) : ℂ) • (star (cut P0 U0) * cut P0 U0))⁻¹ =
      !![(25 / 21 : ℂ), 0; 0, 1] := by
  apply Matrix.inv_eq_left_inv
  ext i j
  fin_cases i <;> fin_cases j <;>
    norm_num [cut, P0, U0, exampleProjectorBase, exampleReflection,
      Matrix.star_apply, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_apply]
  simp only [map_ofNat]
  norm_num

theorem feedback_chart :
    (1 - ((1 / 4 : ℝ) : ℂ) • (star (cut P0 U0) * cut P0 U0)).det ∈
      Complex.slitPlane := by
  rw [Matrix.det_fin_two]
  norm_num [cut, P0, U0, exampleProjectorBase, exampleReflection,
    Matrix.star_apply, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_apply,
    Complex.mem_slitPlane_iff]
  simp only [map_ofNat]
  norm_num

theorem feedbackSource_values :
    feedbackSource 0 dU = 16 / 35 ∧
    feedbackSource dP 0 = -(16 / 35) ∧
    feedbackSource dP dU = 0 := by
  unfold feedbackSource
  dsimp only
  rw [feedback_resolvent]
  constructor
  · norm_num [cut, D0.Algebra.MovingProjectorTransport.comm, generator, P0, U0, dU, exampleProjectorBase,
      exampleReflection, Matrix.trace, Matrix.star_apply, Matrix.mul_apply,
      Matrix.vecMul, dotProduct, Fin.sum_univ_two, Matrix.one_apply]
    simp only [map_ofNat]
    norm_num
  constructor
  · norm_num [cut, D0.Algebra.MovingProjectorTransport.comm, generator, P0, U0, dP, exampleProjectorBase,
      exampleReflection, Matrix.trace, Matrix.star_apply, Matrix.mul_apply,
      Matrix.vecMul, dotProduct, Fin.sum_univ_two, Matrix.one_apply]
    simp only [map_ofNat]
    norm_num
  · norm_num [cut, D0.Algebra.MovingProjectorTransport.comm, generator, P0, U0, dP, dU, exampleProjectorBase,
      exampleReflection, Matrix.trace, Matrix.star_apply, Matrix.mul_apply,
      Matrix.vecMul, dotProduct, Fin.sum_univ_two, Matrix.one_apply]

/-- The relative analytic source agrees with the existing rational consumer. -/
theorem feedbackSource_matches_rational_control :
    feedbackSource 0 dU =
      (D0.Geometry.MovingCutQueryCancellation.source (3 / 5) (4 / 5) (1 / 4)
        (D0.Geometry.MovingCutQueryCancellation.queryVelocity (3 / 5) (4 / 5)) 0 : ℝ) ∧
    feedbackSource dP 0 =
      (D0.Geometry.MovingCutQueryCancellation.source (3 / 5) (4 / 5) (1 / 4) 0
        (D0.Geometry.MovingCutQueryCancellation.cutVelocity (4 / 5)) : ℝ) ∧
    feedbackSource dP dU =
      (D0.Geometry.MovingCutQueryCancellation.source (3 / 5) (4 / 5) (1 / 4)
        (D0.Geometry.MovingCutQueryCancellation.queryVelocity (3 / 5) (4 / 5))
        (D0.Geometry.MovingCutQueryCancellation.cutVelocity (4 / 5)) : ℝ) := by
  have h := D0.Geometry.MovingCutQueryCancellation.rational_query_cut_source_control
  have hq : (D0.Geometry.MovingCutQueryCancellation.source (3 / 5) (4 / 5) (1 / 4)
      (D0.Geometry.MovingCutQueryCancellation.queryVelocity (3 / 5) (4 / 5)) 0 : ℝ) = 16 / 35 := by
    simpa using congrArg (fun x : ℚ => (x : ℝ)) h.2.1
  have hc : (D0.Geometry.MovingCutQueryCancellation.source (3 / 5) (4 / 5) (1 / 4) 0
      (D0.Geometry.MovingCutQueryCancellation.cutVelocity (4 / 5)) : ℝ) = -(16 / 35) := by
    simpa using congrArg (fun x : ℚ => (x : ℝ)) h.2.2.1
  have hj : (D0.Geometry.MovingCutQueryCancellation.source (3 / 5) (4 / 5) (1 / 4)
      (D0.Geometry.MovingCutQueryCancellation.queryVelocity (3 / 5) (4 / 5))
      (D0.Geometry.MovingCutQueryCancellation.cutVelocity (4 / 5)) : ℝ) = 0 := by
    simpa using congrArg (fun x : ℚ => (x : ℝ)) h.2.2.2
  rw [hq, hc, hj]
  exact feedbackSource_values

theorem feedback_derivative_at_control
    {P U : ℝ → M2} {vP vU : M2}
    (hP0 : P 0 = P0) (hU0 : U 0 = U0)
    (hP : HasDerivAt P vP 0) (hU : HasDerivAt U vU 0)
    (hIdem : ∀ᶠ t in 𝓝 (0 : ℝ), P t * P t = P t)
    (hSelf : ∀ᶠ t in 𝓝 (0 : ℝ), star (P t) = P t) :
    HasDerivAt (feedback P U) (feedbackSource vP vU) 0 := by
  have hz : HasDerivAt (fun _ : ℝ => (1 / 4 : ℝ)) 0 0 :=
    hasDerivAt_const 0 (1 / 4 : ℝ)
  have hSlit : (1 - (((fun _ : ℝ => (1 / 4 : ℝ)) 0 : ℝ) : ℂ) •
      (star (cut (P 0) (U 0)) * cut (P 0) (U 0))).det ∈ Complex.slitPlane := by
    simpa [hP0, hU0] using feedback_chart
  have h := D0.Analysis.MovingProjectorBookPrice.hasDerivAt_variable_feedback_logdet
    hz hP hU hIdem hSelf hSlit
  change HasDerivAt (fun t => feedback P U t) (feedbackSource vP vU) 0
  simpa [feedback, feedbackSource, hP0, hU0] using h

/-- Actual derivatives on the three smooth QUERY/cut curves, in the original
finite chart. No physical admission or other part of the complete price is
asserted. -/
theorem query_cut_feedback_derivatives :
    HasDerivAt (feedback (fun _ => P0) movingU) (16 / 35) 0 ∧
    HasDerivAt (feedback movingP (fun _ => U0)) (-(16 / 35)) 0 ∧
    HasDerivAt (feedback movingP movingU) 0 0 := by
  have hp : HasDerivAt (fun _ : ℝ => P0) 0 0 := hasDerivAt_const 0 P0
  have hu : HasDerivAt (fun _ : ℝ => U0) 0 0 := hasDerivAt_const 0 U0
  have hpi : P0 * P0 = P0 := by
    simpa [movingP_zero] using movingP_idempotent 0
  have hps : star P0 = P0 := by
    simpa [movingP_zero] using movingP_selfadjoint 0
  have hpi0 : ∀ᶠ _t in 𝓝 (0 : ℝ), P0 * P0 = P0 := Filter.Eventually.of_forall (fun _ => hpi)
  have hps0 : ∀ᶠ _t in 𝓝 (0 : ℝ), star P0 = P0 := Filter.Eventually.of_forall (fun _ => hps)
  have hpi1 : ∀ᶠ t in 𝓝 (0 : ℝ), movingP t * movingP t = movingP t :=
    Filter.Eventually.of_forall movingP_idempotent
  have hps1 : ∀ᶠ t in 𝓝 (0 : ℝ), star (movingP t) = movingP t :=
    Filter.Eventually.of_forall movingP_selfadjoint
  have hq := feedback_derivative_at_control rfl movingU_zero hp movingU_derivative hpi0 hps0
  have hc := feedback_derivative_at_control movingP_zero rfl movingP_derivative hu hpi1 hps1
  have hj := feedback_derivative_at_control movingP_zero movingU_zero movingP_derivative
    movingU_derivative hpi1 hps1
  have hlinks := feedbackSource_matches_rational_control
  have hr := D0.Geometry.MovingCutQueryCancellation.rational_query_cut_source_control
  have qvalue : feedbackSource 0 dU = (16 / 35 : ℝ) := by
    rw [hlinks.1]
    simpa using congrArg (fun x : ℚ => (x : ℝ)) hr.2.1
  have cvalue : feedbackSource dP 0 = -(16 / 35 : ℝ) := by
    rw [hlinks.2.1]
    simpa using congrArg (fun x : ℚ => (x : ℝ)) hr.2.2.1
  have jvalue : feedbackSource dP dU = 0 := by
    rw [hlinks.2.2]
    simpa using congrArg (fun x : ℚ => (x : ℝ)) hr.2.2.2
  rw [qvalue] at hq
  rw [cvalue] at hc
  rw [jvalue] at hj
  exact ⟨hq, hc, hj⟩

end
end D0.Analysis.MovingCutQueryDerivativeAdapter
