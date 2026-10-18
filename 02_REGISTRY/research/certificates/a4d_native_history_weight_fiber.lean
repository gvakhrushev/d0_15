import D0.CondensedAnchor.DetectorSupportGoldenWeight
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Tactic

/-!
Exact classification of positive finite-cylinder assignments on the owned
golden tree. This is an interface theorem only: it classifies every
positive/root-normalized/refinement-compatible assignment, but does not
construct an infinite-path measure or claim that any particular assignment
or its field dependence is physically admitted by D0.
-/

open Real
open scoped goldenRatio

namespace D0.Research.NativeHistoryWeightFiber

abbrev History := List Bool

noncomputable def goldenP : ℝ := φ⁻¹

theorem goldenP_pos : 0 < goldenP := by
  unfold goldenP
  positivity

theorem goldenP_closure : goldenP + goldenP ^ 2 = 1 := by
  simpa [goldenP] using D0.CondensedAnchor.inv_gold_closure

theorem goldenCylinder_pos (w : History) : 0 < D0.CondensedAnchor.cylWeight w := by
  induction w with
  | nil => norm_num [D0.CondensedAnchor.cylWeight]
  | cons b w ih =>
      cases b <;> simp [D0.CondensedAnchor.cylWeight] <;> positivity

theorem goldenCylinder_concat_direct (w : History) :
    D0.CondensedAnchor.cylWeight (w.concat true) =
      φ⁻¹ * D0.CondensedAnchor.cylWeight w := by
  induction w with
  | nil => simp [D0.CondensedAnchor.cylWeight]
  | cons b tail ih =>
      simp only [List.concat_cons, D0.CondensedAnchor.cylWeight]
      rw [ih]
      ring

theorem goldenCylinder_concat_return (w : History) :
    D0.CondensedAnchor.cylWeight (w.concat false) =
      (φ⁻¹) ^ 2 * D0.CondensedAnchor.cylWeight w := by
  induction w with
  | nil => simp [D0.CondensedAnchor.cylWeight]
  | cons b tail ih =>
      simp only [List.concat_cons, D0.CondensedAnchor.cylWeight]
      rw [ih]
      ring

/-- Positive normalized cylinder weights on every finite history, consistent
under the two chronological one-step refinements. -/
structure PositiveHistoryLaw where
  value : History → ℝ
  root : value [] = 1
  positive : ∀ w, 0 < value w
  refinement : ∀ w, value (w.concat true) + value (w.concat false) = value w

theorem positiveHistoryLaw_ext {q₁ q₂ : PositiveHistoryLaw}
    (h : q₁.value = q₂.value) : q₁ = q₂ := by
  cases q₁ with
  | mk value₁ root₁ positive₁ refinement₁ =>
    cases q₂ with
    | mk value₂ root₂ positive₂ refinement₂ =>
      simp_all

/-- Positive densities over the owned golden cylinder weights, satisfying
the corresponding one-step likelihood martingale identity. -/
structure PositiveGoldenLikelihood where
  value : History → ℝ
  root : value [] = 1
  positive : ∀ w, 0 < value w
  martingale : ∀ w,
    D0.CondensedAnchor.cylWeight (w.concat true) * value (w.concat true) +
      D0.CondensedAnchor.cylWeight (w.concat false) * value (w.concat false) =
        D0.CondensedAnchor.cylWeight w * value w

theorem positiveGoldenLikelihood_ext {L₁ L₂ : PositiveGoldenLikelihood}
    (h : L₁.value = L₂.value) : L₁ = L₂ := by
  cases L₁ with
  | mk value₁ root₁ positive₁ martingale₁ =>
    cases L₂ with
    | mk value₂ root₂ positive₂ martingale₂ =>
      simp_all

/-- Every complete positive history law has its unique density over the
already-owned golden cylinder measure. -/
noncomputable def lawToLikelihood (q : PositiveHistoryLaw) : PositiveGoldenLikelihood where
  value w := q.value w / D0.CondensedAnchor.cylWeight w
  root := by
    rw [q.root]
    simp [D0.CondensedAnchor.cylWeight]
  positive w := div_pos (q.positive w) (goldenCylinder_pos w)
  martingale w := by
    calc
      D0.CondensedAnchor.cylWeight (w.concat true) *
          (q.value (w.concat true) / D0.CondensedAnchor.cylWeight (w.concat true)) +
        D0.CondensedAnchor.cylWeight (w.concat false) *
          (q.value (w.concat false) / D0.CondensedAnchor.cylWeight (w.concat false)) =
          q.value (w.concat true) + q.value (w.concat false) := by
            rw [mul_div_cancel₀ _ (ne_of_gt (goldenCylinder_pos (w.concat true))),
                mul_div_cancel₀ _ (ne_of_gt (goldenCylinder_pos (w.concat false)))]
      _ = q.value w := q.refinement w
      _ = D0.CondensedAnchor.cylWeight w *
          (q.value w / D0.CondensedAnchor.cylWeight w) := by
            rw [mul_div_cancel₀ _ (ne_of_gt (goldenCylinder_pos w))]

/-- Multiplying a positive golden martingale density by the owned cylinder
measure reconstructs a complete probability law. -/
noncomputable def likelihoodToLaw (L : PositiveGoldenLikelihood) : PositiveHistoryLaw where
  value w := D0.CondensedAnchor.cylWeight w * L.value w
  root := by
    simp [D0.CondensedAnchor.cylWeight, L.root]
  positive w := mul_pos (goldenCylinder_pos w) (L.positive w)
  refinement w := by
    simpa using L.martingale w

theorem law_roundtrip (q : PositiveHistoryLaw) :
    likelihoodToLaw (lawToLikelihood q) = q := by
  cases q with
  | mk value root positive hRefinement =>
      apply positiveHistoryLaw_ext
      funext w
      dsimp [likelihoodToLaw, lawToLikelihood]
      exact mul_div_cancel₀ _ (ne_of_gt (goldenCylinder_pos w))

theorem likelihood_roundtrip (L : PositiveGoldenLikelihood) :
    lawToLikelihood (likelihoodToLaw L) = L := by
  cases L with
  | mk value root positive martingale =>
      apply positiveGoldenLikelihood_ext
      funext w
      dsimp [lawToLikelihood, likelihoodToLaw]
      field_simp [ne_of_gt (goldenCylinder_pos w)]

/-- The literal golden splitter law, when it is bound to measured conditional
history probabilities at every chronological extension. -/
def GoldenStepBinding (q : PositiveHistoryLaw) : Prop :=
  ∀ w, q.value (w.concat true) = goldenP * q.value w ∧
    q.value (w.concat false) = goldenP ^ 2 * q.value w

/-- If the primitive `p,p²` branches are the measured probabilities of the
same complete history tree, its complete law is uniquely the owned cylinder
measure. -/
theorem goldenStepBinding_forces_cylinder_law
    (q : PositiveHistoryLaw) (hstep : GoldenStepBinding q) :
    q.value = D0.CondensedAnchor.cylWeight := by
  funext w
  induction w using List.reverseRecOn with
  | nil => simpa [D0.CondensedAnchor.cylWeight] using q.root
  | append_singleton pre last ih =>
      rw [← List.concat_eq_append]
      cases last with
      | true =>
          calc
            q.value (pre.concat true) = goldenP * q.value pre := (hstep pre).1
            _ = φ⁻¹ * D0.CondensedAnchor.cylWeight pre := by rw [ih]; simp [goldenP]
            _ = D0.CondensedAnchor.cylWeight (pre.concat true) :=
              (goldenCylinder_concat_direct pre).symm
      | false =>
          calc
            q.value (pre.concat false) = goldenP ^ 2 * q.value pre := (hstep pre).2
            _ = (φ⁻¹) ^ 2 * D0.CondensedAnchor.cylWeight pre := by rw [ih]; simp [goldenP]
            _ = D0.CondensedAnchor.cylWeight (pre.concat false) :=
              (goldenCylinder_concat_return pre).symm

/-- Under that measured-split binding, the density over the golden cylinders
is identically one. This is the exact condition that removes the martingale
freedom at the branch-law layer. -/
theorem goldenStepBinding_forces_unit_density
    (q : PositiveHistoryLaw) (hstep : GoldenStepBinding q) (w : History) :
    q.value w / D0.CondensedAnchor.cylWeight w = 1 := by
  rw [goldenStepBinding_forces_cylinder_law q hstep]
  exact div_self (ne_of_gt (goldenCylinder_pos w))

/-- The entire complete positive branch-law fiber is exactly the positive
likelihood-martingale fiber over the golden cylinders. -/
theorem finite_cylinder_law_equiv_golden_likelihood :
    Function.Bijective (lawToLikelihood) := by
  constructor
  · intro q₁ q₂ h
    apply positiveHistoryLaw_ext
    funext w
    have hw := congrFun (congrArg PositiveGoldenLikelihood.value h) w
    dsimp [lawToLikelihood] at hw
    have hμ : D0.CondensedAnchor.cylWeight w ≠ 0 :=
      ne_of_gt (goldenCylinder_pos w)
    have hm := congrArg (fun x : ℝ => x * D0.CondensedAnchor.cylWeight w) hw
    simpa [div_mul_cancel₀, hμ] using hm
  · intro L
    exact ⟨likelihoodToLaw L, likelihood_roundtrip L⟩

/-- One family on the finite-cylinder interface. At every history it shifts
probability between the direct and return extension while preserving total
mass. The parameter is a diagnostic coordinate; no native D0 map to it is
asserted here. -/
noncomputable def perturbedFirstMass (t : ℝ) : Bool → ℝ
  | true => goldenP + t * goldenP ^ 2
  | false => goldenP ^ 2 * (1 - t)

noncomputable def perturbedHistoryLaw (t : ℝ) : History → ℝ
  | [] => 1
  | b :: tail => perturbedFirstMass t b * perturbedHistoryLaw t tail

theorem perturbedFirstMass_pos (t : ℝ)
    (htlow : -1 / goldenP < t) (hthigh : t < 1) (b : Bool) :
    0 < perturbedFirstMass t b := by
  cases b with
  | true =>
      have hp := goldenP_pos
      have hmul : -1 < t * goldenP := (div_lt_iff₀ hp).mp htlow
      have hfactor : 0 < 1 + t * goldenP := by linarith
      unfold perturbedFirstMass
      nlinarith
  | false =>
      have hp := goldenP_pos
      unfold perturbedFirstMass
      exact mul_pos (pow_pos hp 2) (by linarith)

theorem perturbedHistoryLaw_root (t : ℝ) : perturbedHistoryLaw t [] = 1 := rfl

theorem perturbedHistoryLaw_positive (t : ℝ)
    (htlow : -1 / goldenP < t) (hthigh : t < 1) (w : History) :
    0 < perturbedHistoryLaw t w := by
  induction w with
  | nil => norm_num [perturbedHistoryLaw]
  | cons b tail ih =>
      exact mul_pos (perturbedFirstMass_pos t htlow hthigh b) ih

theorem perturbedHistoryLaw_step_direct (t : ℝ) (w : History) :
    perturbedHistoryLaw t (w.concat true) =
      (goldenP + t * goldenP ^ 2) * perturbedHistoryLaw t w := by
  induction w with
  | nil => simp [perturbedHistoryLaw, perturbedFirstMass]
  | cons b tail ih =>
      simp only [List.concat_cons, perturbedHistoryLaw]
      calc
        perturbedFirstMass t b * perturbedHistoryLaw t (tail.concat true) =
            perturbedFirstMass t b *
              ((goldenP + t * goldenP ^ 2) * perturbedHistoryLaw t tail) := by rw [ih]
        _ = (goldenP + t * goldenP ^ 2) *
            (perturbedFirstMass t b * perturbedHistoryLaw t tail) := by ring

theorem perturbedHistoryLaw_step_return (t : ℝ) (w : History) :
    perturbedHistoryLaw t (w.concat false) =
      (goldenP ^ 2 * (1 - t)) * perturbedHistoryLaw t w := by
  induction w with
  | nil => simp [perturbedHistoryLaw, perturbedFirstMass]
  | cons b tail ih =>
      simp only [List.concat_cons, perturbedHistoryLaw]
      calc
        perturbedFirstMass t b * perturbedHistoryLaw t (tail.concat false) =
            perturbedFirstMass t b *
              ((goldenP ^ 2 * (1 - t)) * perturbedHistoryLaw t tail) := by rw [ih]
        _ = (goldenP ^ 2 * (1 - t)) *
            (perturbedFirstMass t b * perturbedHistoryLaw t tail) := by ring

theorem perturbedHistoryLaw_refines (t : ℝ) (w : History) :
    perturbedHistoryLaw t (w.concat true) +
      perturbedHistoryLaw t (w.concat false) = perturbedHistoryLaw t w := by
  induction w with
  | nil =>
      have htrue : ([] : History).concat true = [true] := rfl
      have hfalse : ([] : History).concat false = [false] := rfl
      rw [htrue, hfalse]
      simp only [perturbedHistoryLaw, mul_one]
      unfold perturbedFirstMass
      nlinarith [goldenP_closure]
  | cons b tail ih =>
      change perturbedFirstMass t b * perturbedHistoryLaw t (tail.concat true) +
        perturbedFirstMass t b * perturbedHistoryLaw t (tail.concat false) =
          perturbedFirstMass t b * perturbedHistoryLaw t tail
      rw [← mul_add, ih]

theorem perturbed_root_true_branch (t : ℝ) :
    perturbedHistoryLaw t [true] = goldenP + t * goldenP ^ 2 := by
  simp [perturbedHistoryLaw, perturbedFirstMass]

theorem perturbed_branch_binding_forces_zero
    (t : ℝ) (hstep : perturbedHistoryLaw t [true] =
      goldenP * perturbedHistoryLaw t []) : t = 0 := by
  have hvalue := perturbed_root_true_branch t
  rw [hvalue] at hstep
  dsimp [perturbedHistoryLaw] at hstep
  have hzero : t * goldenP ^ 2 = 0 := by nlinarith [hstep]
  rcases mul_eq_zero.mp hzero with ht | hp
  · exact ht
  · exact False.elim ((ne_of_gt (pow_pos goldenP_pos 2)) hp)

noncomputable def perturbedLaw (t : ℝ) (htlow : -1 / goldenP < t) (hthigh : t < 1) :
    PositiveHistoryLaw where
  value := perturbedHistoryLaw t
  root := perturbedHistoryLaw_root t
  positive := perturbedHistoryLaw_positive t htlow hthigh
  refinement := perturbedHistoryLaw_refines t

theorem perturbedLaw_ne_golden_of_ne_zero
    (t : ℝ) (htlow : -1 / goldenP < t) (hthigh : t < 1) (hne : t ≠ 0) :
    (perturbedLaw t htlow hthigh).value ≠ D0.CondensedAnchor.cylWeight := by
  intro h
  have hfirst : perturbedHistoryLaw t [true] = D0.CondensedAnchor.cylWeight [true] := by
    simpa [perturbedLaw] using congrFun h [true]
  rw [perturbed_root_true_branch] at hfirst
  have hgolden : D0.CondensedAnchor.cylWeight [true] = goldenP := by
    simp [D0.CondensedAnchor.cylWeight, goldenP]
  rw [hgolden] at hfirst
  have hzero : t * goldenP ^ 2 = 0 := by nlinarith [hfirst]
  rcases mul_eq_zero.mp hzero with ht | hp
  · exact hne ht
  · exact (ne_of_gt (pow_pos goldenP_pos 2)) hp

theorem perturbedLaw_zero_is_golden
    (htlow : -1 / goldenP < 0) (hthigh : 0 < 1) :
    (perturbedLaw 0 htlow hthigh).value = D0.CondensedAnchor.cylWeight := by
  funext w
  induction w with
  | nil => simp [perturbedLaw, perturbedHistoryLaw, D0.CondensedAnchor.cylWeight]
  | cons b tail ih =>
      change perturbedHistoryLaw 0 (b :: tail) = D0.CondensedAnchor.cylWeight (b :: tail)
      change perturbedHistoryLaw 0 tail = D0.CondensedAnchor.cylWeight tail at ih
      cases b with
      | true =>
          have hm : perturbedFirstMass 0 true = φ⁻¹ := by
            simp [perturbedFirstMass, goldenP]
          calc
            perturbedHistoryLaw 0 (true :: tail) =
                perturbedFirstMass 0 true * perturbedHistoryLaw 0 tail := rfl
            _ = φ⁻¹ * D0.CondensedAnchor.cylWeight tail := by rw [hm, ih]
            _ = D0.CondensedAnchor.cylWeight (true :: tail) := by
              simp [D0.CondensedAnchor.cylWeight]
      | false =>
          have hm : perturbedFirstMass 0 false = (φ⁻¹) ^ 2 := by
            simp [perturbedFirstMass, goldenP]
          calc
            perturbedHistoryLaw 0 (false :: tail) =
                perturbedFirstMass 0 false * perturbedHistoryLaw 0 tail := rfl
            _ = (φ⁻¹) ^ 2 * D0.CondensedAnchor.cylWeight tail := by rw [hm, ih]
            _ = D0.CondensedAnchor.cylWeight (false :: tail) := by
              simp [D0.CondensedAnchor.cylWeight]

noncomputable def trueBranchInformation (t : ℝ) : ℝ :=
  Real.log (1 + t * goldenP) / Real.log φ

noncomputable def falseBranchInformation (t : ℝ) : ℝ :=
  Real.log (1 - t) / Real.log φ

theorem trueBranchInformation_at_zero : trueBranchInformation 0 = 0 := by
  simp [trueBranchInformation]

theorem falseBranchInformation_at_zero : falseBranchInformation 0 = 0 := by
  simp [falseBranchInformation]

theorem trueBranch_density (t : ℝ) :
    perturbedHistoryLaw t [true] / D0.CondensedAnchor.cylWeight [true] =
      1 + t * goldenP := by
  rw [perturbed_root_true_branch]
  simp [D0.CondensedAnchor.cylWeight, goldenP]
  field_simp [ne_of_gt (goldenCylinder_pos [true])]

theorem falseBranch_density (t : ℝ) :
    perturbedHistoryLaw t [false] / D0.CondensedAnchor.cylWeight [false] =
      1 - t := by
  simp [perturbedHistoryLaw, perturbedFirstMass,
    D0.CondensedAnchor.cylWeight, goldenP]
  field_simp [ne_of_gt (goldenCylinder_pos [false])]

theorem trueBranchInformation_source :
    HasDerivAt trueBranchInformation (goldenP / Real.log φ) 0 := by
  have hlinear : HasDerivAt (fun t : ℝ => 1 + t * goldenP) goldenP 0 := by
    simpa using ((hasDerivAt_id 0).mul_const goldenP).const_add 1
  have hlog := hlinear.log (by norm_num)
  have hscaled := hlog.div_const (Real.log φ)
  simpa [trueBranchInformation] using hscaled

theorem trueBranchInformation_is_density (t : ℝ) :
    trueBranchInformation t =
      Real.log (perturbedHistoryLaw t [true] /
        D0.CondensedAnchor.cylWeight [true]) / Real.log φ := by
  rw [trueBranch_density]
  rfl

theorem falseBranchInformation_is_density (t : ℝ) :
    falseBranchInformation t =
      Real.log (perturbedHistoryLaw t [false] /
        D0.CondensedAnchor.cylWeight [false]) / Real.log φ := by
  rw [falseBranch_density]
  rfl

theorem falseBranchInformation_source :
    HasDerivAt falseBranchInformation (-(1 / Real.log φ)) 0 := by
  have hlinear : HasDerivAt (fun t : ℝ => 1 - t) (-1) 0 := by
    simpa using (hasDerivAt_id 0).const_sub 1
  have hlog := hlinear.log (by norm_num)
  have hscaled := hlog.div_const (Real.log φ)
  convert hscaled using 1
  ring

#check finite_cylinder_law_equiv_golden_likelihood
#check law_roundtrip
#check likelihood_roundtrip
#check perturbedLaw_zero_is_golden
#check perturbedLaw_ne_golden_of_ne_zero
#check perturbedHistoryLaw_step_direct
#check perturbedHistoryLaw_step_return
#check goldenStepBinding_forces_cylinder_law
#check goldenStepBinding_forces_unit_density
#check trueBranchInformation_is_density
#check falseBranchInformation_is_density
#check trueBranchInformation_source
#check falseBranchInformation_source

#print axioms finite_cylinder_law_equiv_golden_likelihood
#print axioms law_roundtrip
#print axioms likelihood_roundtrip
#print axioms goldenStepBinding_forces_cylinder_law
#print axioms goldenStepBinding_forces_unit_density
#print axioms perturbedHistoryLaw_refines
#print axioms perturbedHistoryLaw_step_direct
#print axioms perturbedHistoryLaw_step_return
#print axioms perturbedLaw_ne_golden_of_ne_zero
#print axioms trueBranchInformation_is_density
#print axioms falseBranchInformation_is_density
#print axioms trueBranchInformation_source
#print axioms falseBranchInformation_source

end D0.Research.NativeHistoryWeightFiber
