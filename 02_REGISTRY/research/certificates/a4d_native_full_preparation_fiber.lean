import D0.Representation.GoldenCoherentMemory
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Tactic

/-! Scalar research kernel for the complete two-parameter invariant density
class described in the accompanying analytic proof. These identities do not
formalize the representation-theoretic classification, native admission,
Kraus-channel classification, or a physical stationary preparation. All modes,
normalizations and denominator hypotheses are explicit. -/
namespace D0.Research.FullPreparationFiber
noncomputable section

/-- Eigenvalue on a full traceless matrix sector. -/
def coefficient (u v lam mu N : ℝ) : ℝ := ((1-lam)*u-mu*v)/N

def mismatch (u v fx fy lam mu : ℝ) : ℝ :=
  (1-lam)*(u*fx+v*fy)-mu*(v*fx+u*fy)

def heat (beta lam : ℝ) : ℝ := -Real.log lam/beta

/-- These are precisely the two marginal equations in the invariant scalar
class, without postulating a particular residual eigenvalue. -/
theorem marginal_equations_iff (u v lam mu NX NY A B : ℝ)
    (hNX : NX≠0) (hNY : NY≠0) :
    (lam*u+mu*v+NX*A=u ∧ lam*v+mu*u+NY*B=v) ↔
    (A=coefficient u v lam mu NX ∧ B=coefficient v u lam mu NY) := by
  simp only [coefficient,eq_div_iff hNX,eq_div_iff hNY]
  constructor <;> rintro ⟨h1,h2⟩ <;> constructor <;> nlinarith

theorem full_normalization (u v lam mu NX NY : ℝ)
    (huv : u+v=1) (hNX : NX≠0) (hNY : NY≠0) :
    lam+mu+NX*coefficient u v lam mu NX+
      NY*coefficient v u lam mu NY=1 := by
  dsimp [coefficient]
  field_simp
  linear_combination (1-lam-mu)*huv

theorem positive_coefficient_iff (u v lam mu N : ℝ) (hN : 0<N) :
    0<coefficient u v lam mu N ↔ mu*v<(1-lam)*u := by
  simp only [coefficient,lt_div_iff₀ hN,zero_mul]
  constructor <;> intro h <;> linarith

theorem protected_domination_iff (u v lam mu N : ℝ) (hN : 0<N) :
    coefficient u v lam mu N<lam ↔ (1-lam)*u-mu*v<lam*N := by
  exact div_lt_iff₀ hN

theorem mismatch_expansion (u v fx fy lam mu : ℝ) :
    ((1-lam)*u-mu*v)*fx+((1-lam)*v-mu*u)*fy=
      mismatch u v fx fy lam mu := by
  dsimp [mismatch]
  ring

/-- The minus sign in the second coordinate is essential. -/
theorem fixed_mismatch_path (u v fx fy lam mu s : ℝ)
    (hJ : v*fx+u*fy≠0) :
    mismatch u v fx fy (lam+s) (mu-(u*fx+v*fy)/(v*fx+u*fy)*s)=
      mismatch u v fx fy lam mu := by
  dsimp [mismatch]
  have hc := div_mul_cancel₀ (u*fx+v*fy) hJ
  linear_combination s*hc

theorem wrong_sign_mismatch_defect (u v fx fy lam mu s : ℝ)
    (hJ : v*fx+u*fy≠0) :
    mismatch u v fx fy (lam+s) (mu+(u*fx+v*fy)/(v*fx+u*fy)*s)-
      mismatch u v fx fy lam mu = -2*(u*fx+v*fy)*s := by
  dsimp [mismatch]
  have hc := div_mul_cancel₀ (u*fx+v*fy) hJ
  linear_combination -s*hc

theorem mismatch_coefficients_positive (u v fx fy : ℝ)
    (hu : 0<u) (hv : 0<v) (hx : 0<fx) (hy : 0<fy) :
    0<u*fx+v*fy ∧ 0<v*fx+u*fy := by
  constructor <;> positivity

/-- The owned positive heat price strictly decreases along the lambda
coordinate, including a path on which mismatch is held fixed. -/
theorem heat_hasDerivAt (beta lam : ℝ) (hlam : 0<lam) :
    HasDerivAt (fun s : ℝ => heat beta (lam+s)) (-1/(beta*lam)) 0 := by
  have h : HasDerivAt (fun s : ℝ => lam+s) 1 0 := by
    simpa using (hasDerivAt_const (0 : ℝ) lam).add (hasDerivAt_id (0 : ℝ))
  have hlog := h.log (by simpa using ne_of_gt hlam)
  convert hlog.neg.div_const beta using 1
  simp
  ring

theorem heat_derivative_negative (beta lam : ℝ) (hb : 0<beta) (hlam : 0<lam) :
    -1/(beta*lam)<0 := div_neg_of_neg_of_pos (by norm_num) (mul_pos hb hlam)

theorem finite_heat_descent (beta lam s : ℝ)
    (hb : 0<beta) (hlam : 0<lam) (hs : 0<s) :
    heat beta (lam+s)<heat beta lam := by
  apply div_lt_div_of_pos_right _ hb
  apply neg_lt_neg
  exact Real.log_lt_log hlam (by linarith)

/-- All four joint sectors are retained, including the double complement. -/
theorem full_joint_sector_count (D r : ℕ) (hr : r≤D) :
    r^2+r*(D-r)+(D-r)*r+(D-r)^2=D^2 := by
  have hs : r+(D-r)=D := by omega
  calc
    _ = (r+(D-r))^2 := by ring
    _ = _ := by rw [hs]

theorem mismatch_sector_nonempty (D r : ℕ) (hr : 0<r) (hD : r<D) :
    0<r*(D-r) := Nat.mul_pos hr (Nat.sub_pos_of_lt hD)

theorem invariant_sector_count (A B : ℕ) (hA : 0<A) (hB : 0<B) :
    1+1+(A^2-1)+(B^2-1)=A^2+B^2 := by
  have ha : 1≤A^2 := by nlinarith
  have hb : 1≤B^2 := by nlinarith
  omega

/-- The full new space exceeds twice the old one by this exact residual. -/
theorem refinement_residual (A B : ℝ) :
    ((A+B)^2+A^2)-2*(A^2+B^2)=B*(2*A-B) := by ring

theorem refinement_dimension_bounds (A B : ℝ) (hB : 0<B) (hBA : B≤A) :
    2*(A^2+B^2)<(A+B)^2+A^2 ∧
    (A+B)^2+A^2<3*(A^2+B^2) := by
  have hBB : 0<B^2 := sq_pos_of_pos hB
  have hprod : 0<B*(2*A-B) := mul_pos hB (by linarith)
  constructor <;> nlinarith [sq_nonneg (A-B)]

theorem residual_fifth_identity (A B : ℝ) :
    5*(((A+B)^2+A^2)-2*(A^2+B^2))-((A+B)^2+A^2)=
      2*(A-B)*(3*B-A) := by ring

theorem retained_residual_fraction (A B : ℝ)
    (hB : 0<B) (hBA : B≤A) (hAB : A≤2*B) :
    (1:ℝ)/5 ≤ (((A+B)^2+A^2)-2*(A^2+B^2))/((A+B)^2+A^2) ∧
    (((A+B)^2+A^2)-2*(A^2+B^2))/((A+B)^2+A^2)<(1:ℝ)/3 := by
  have hD : 0<(A+B)^2+A^2 := by nlinarith [sq_nonneg A,sq_pos_of_pos hB]
  have hprod : 0≤(A-B)*(3*B-A) := mul_nonneg (by linarith) (by linarith)
  have hbound := refinement_dimension_bounds A B hB hBA
  constructor
  · rw [le_div_iff₀ hD]
    nlinarith [residual_fifth_identity A B]
  · rw [div_lt_iff₀ hD]
    nlinarith [hbound.2]

end
end D0.Research.FullPreparationFiber

#print axioms D0.Research.FullPreparationFiber.marginal_equations_iff
#print axioms D0.Research.FullPreparationFiber.full_normalization
#print axioms D0.Research.FullPreparationFiber.positive_coefficient_iff
#print axioms D0.Research.FullPreparationFiber.protected_domination_iff
#print axioms D0.Research.FullPreparationFiber.mismatch_expansion
#print axioms D0.Research.FullPreparationFiber.fixed_mismatch_path
#print axioms D0.Research.FullPreparationFiber.wrong_sign_mismatch_defect
#print axioms D0.Research.FullPreparationFiber.mismatch_coefficients_positive
#print axioms D0.Research.FullPreparationFiber.heat_hasDerivAt
#print axioms D0.Research.FullPreparationFiber.heat_derivative_negative
#print axioms D0.Research.FullPreparationFiber.finite_heat_descent
#print axioms D0.Research.FullPreparationFiber.full_joint_sector_count
#print axioms D0.Research.FullPreparationFiber.mismatch_sector_nonempty
#print axioms D0.Research.FullPreparationFiber.invariant_sector_count
#print axioms D0.Research.FullPreparationFiber.refinement_residual
#print axioms D0.Research.FullPreparationFiber.refinement_dimension_bounds
#print axioms D0.Research.FullPreparationFiber.residual_fifth_identity
#print axioms D0.Research.FullPreparationFiber.retained_residual_fraction
#print axioms D0.Representation.GoldenCoherentMemory.fullStep_orthogonal
