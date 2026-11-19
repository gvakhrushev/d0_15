import D0.CondensedAnchor.DetectorSupportGoldenWeight
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Tactic

/-!
The pathwise information increment forced by the joint Book III equations
`weight = phi ^ (-action)`, `action = codeCost - information`, instantiated
with the actual branch probability and the owned golden prefix-code cost.

This is a conditional bridge: the Lean result proves the exact consequence
once that owner binding is made. It does not prove that every D0 sector uses
this record instrument or that the physical field/action map is admitted.
-/

open Real
open scoped goldenRatio

namespace D0.Research.NativeBranchInformationCocycle

noncomputable def pathInfo (q : List Bool → ℝ) (w : List Bool) : ℝ :=
  Real.log (q w / D0.CondensedAnchor.cylWeight w) / Real.log φ

noncomputable def pathAction (q : List Bool → ℝ) (w : List Bool) : ℝ :=
  -Real.log (q w) / Real.log φ

def codeCost (w : List Bool) : ℝ := D0.CondensedAnchor.weightExp w

theorem goldenReference_pos (w : List Bool) :
    0 < D0.CondensedAnchor.cylWeight w := by
  induction w with
  | nil => norm_num [D0.CondensedAnchor.cylWeight]
  | cons b w ih => cases b <;> simp [D0.CondensedAnchor.cylWeight] <;> positivity

theorem log_phi_pos : 0 < Real.log φ := Real.log_pos Real.one_lt_goldenRatio

/-- The actual owned direct/return code cost is the surprisal of its golden
reference cylinder. -/
theorem codeCost_eq_reference_surprisal (w : List Bool) :
    codeCost w =
      -Real.log (D0.CondensedAnchor.cylWeight w) / Real.log φ := by
  rw [D0.CondensedAnchor.cylWeight_eq_pow]
  simp only [codeCost, Real.log_pow, Real.log_inv]
  have hlog : Real.log φ ≠ 0 := ne_of_gt log_phi_pos
  simp [hlog]

/-- With `q` the measured probability of this complete recorded history, the
Book III pathwise information is uniquely the log likelihood ratio to the
owned golden reference. -/
theorem code_minus_pathInfo_eq_pathAction
    (q : List Bool → ℝ) (w : List Bool) (hq : 0 < q w) :
    codeCost w - pathInfo q w = pathAction q w := by
  rw [codeCost_eq_reference_surprisal]
  unfold pathInfo pathAction
  rw [Real.log_div (ne_of_gt hq) (ne_of_gt (goldenReference_pos w))]
  have hlog : Real.log φ ≠ 0 := ne_of_gt log_phi_pos
  field_simp [hlog]
  ring

/-- No second pathwise information assignment can satisfy the same owned
code-cost and measured-probability action equations on positive-probability
histories. -/
theorem pathInfo_unique
    (q : List Bool → ℝ) (w : List Bool) (hq : 0 < q w) (I : ℝ)
    (hI : codeCost w - I = pathAction q w) :
    I = pathInfo q w := by
  have h := code_minus_pathInfo_eq_pathAction q w hq
  linarith

noncomputable def likelihood (q : List Bool → ℝ) (w : List Bool) : ℝ :=
  q w / D0.CondensedAnchor.cylWeight w

def PrefixProbability (q : List Bool → ℝ) : Prop :=
  ∀ w, q (w.concat true) + q (w.concat false) = q w

noncomputable def localInfo (q : List Bool → ℝ) (w : List Bool) (b : Bool) : ℝ :=
  Real.log (likelihood q (w.concat b) / likelihood q w) / Real.log φ

/-- The total likelihood information changes by the conditional likelihood
ratio at each recorded branch. -/
theorem pathInfo_increment_eq_localInfo
    (q : List Bool → ℝ) (w : List Bool) (b : Bool)
    (hq : 0 < q w) (hqc : 0 < q (w.concat b)) :
    pathInfo q (w.concat b) - pathInfo q w = localInfo q w b := by
  unfold pathInfo localInfo likelihood
  have hchild :
      0 < q (w.concat b) / D0.CondensedAnchor.cylWeight (w.concat b) :=
    div_pos hqc (goldenReference_pos (w.concat b))
  have hparent :
      0 < q w / D0.CondensedAnchor.cylWeight w :=
    div_pos hq (goldenReference_pos w)
  rw [Real.log_div (ne_of_gt hchild) (ne_of_gt hparent)]
  field_simp [ne_of_gt log_phi_pos]

/-- Nonnegative measured history probabilities give a nonnegative likelihood
density on the owned golden cylinders. -/
theorem likelihood_nonneg
    (q : List Bool → ℝ) (w : List Bool) (hq : 0 ≤ q w) :
    0 ≤ likelihood q w := by
  unfold likelihood
  exact div_nonneg hq (le_of_lt (goldenReference_pos w))

/-- If the measured histories form a complete probability tree, their
likelihood density satisfies the martingale refinement identity under the
golden cylinder law. This is the exact all-history conservation equation. -/
theorem likelihood_refines
    (q : List Bool → ℝ) (hq : PrefixProbability q) (w : List Bool) :
    D0.CondensedAnchor.cylWeight (w.concat true) *
        likelihood q (w.concat true) +
      D0.CondensedAnchor.cylWeight (w.concat false) *
        likelihood q (w.concat false) =
      D0.CondensedAnchor.cylWeight w * likelihood q w := by
  unfold likelihood
  calc
    D0.CondensedAnchor.cylWeight (w.concat true) *
        (q (w.concat true) / D0.CondensedAnchor.cylWeight (w.concat true)) +
      D0.CondensedAnchor.cylWeight (w.concat false) *
        (q (w.concat false) / D0.CondensedAnchor.cylWeight (w.concat false)) =
        q (w.concat true) + q (w.concat false) := by
          rw [mul_div_cancel₀ (q (w.concat true))
                (ne_of_gt (goldenReference_pos (w.concat true))),
              mul_div_cancel₀ (q (w.concat false))
                (ne_of_gt (goldenReference_pos (w.concat false)))]
    _ = q w := hq w
    _ = D0.CondensedAnchor.cylWeight w *
        (q w / D0.CondensedAnchor.cylWeight w) := by
          rw [mul_div_cancel₀ (q w) (ne_of_gt (goldenReference_pos w))]

noncomputable def movingPathInfo (mu : ℝ) (q : ℝ → ℝ) (t : ℝ) : ℝ :=
  Real.log (q t / mu) / Real.log φ

/-- The joint source includes every variation of the measured probability,
including both state preparation and the recorded return operators. -/
theorem movingPathInfo_hasDerivAt
    (mu dq : ℝ) (q : ℝ → ℝ) (t : ℝ)
    (hmu : 0 < mu) (hq : 0 < q t) (hderiv : HasDerivAt q dq t) :
    HasDerivAt (movingPathInfo mu q) ((dq / q t) / Real.log φ) t := by
  have hratio : HasDerivAt (fun s => q s / mu) (dq / mu) t := hderiv.div_const mu
  have hlog := hratio.log (ne_of_gt (div_pos hq hmu))
  have hscale := hlog.div_const (Real.log φ)
  convert hscale using 1
  field_simp [ne_of_gt hmu, ne_of_gt hq, ne_of_gt log_phi_pos]

#check codeCost_eq_reference_surprisal
#check code_minus_pathInfo_eq_pathAction
#check pathInfo_unique
#check pathInfo_increment_eq_localInfo
#check likelihood_nonneg
#check likelihood_refines
#check movingPathInfo_hasDerivAt

#print axioms codeCost_eq_reference_surprisal
#print axioms code_minus_pathInfo_eq_pathAction
#print axioms pathInfo_unique
#print axioms pathInfo_increment_eq_localInfo
#print axioms likelihood_nonneg
#print axioms likelihood_refines
#print axioms movingPathInfo_hasDerivAt

end D0.Research.NativeBranchInformationCocycle
