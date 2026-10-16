import D0.Algebra.FibonacciAFTower
import D0.CondensedAnchor.DetectorSupportGoldenWeight
import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Tactic

/-! Positivity at every actual Fibonacci level forces the compatible trace
weights. No eigenvector or scale-ratio hypothesis is supplied. This is a
trace-state theorem, not a full GNS density or physical heat preparation. -/
namespace D0.Research.AFTracePreparation
open Filter
open scoped Topology
noncomputable section

theorem compatible_recurrence (x y : ℕ → ℝ)
    (hx : ∀ n, x n = x (n+1)+y (n+1))
    (hy : ∀ n, y n = x (n+1)) (n : ℕ) :
    x n = x (n+1)+x (n+2) := by
  simpa [hy] using hx n

theorem compatible_bounds (x y : ℕ → ℝ)
    (hxp : ∀ n, 0 ≤ x n) (hyp : ∀ n, 0 ≤ y n)
    (hx : ∀ n, x n = x (n+1)+y (n+1))
    (hn : x 0+y 0=1) : ∀ n, 0 ≤ x n ∧ x n ≤ 1 := by
  intro n
  refine ⟨hxp n, ?_⟩
  induction n with
  | zero => linarith [hyp 0]
  | succ n ih => linarith [hx n, hyp (n+1)]

def defect (p : ℝ) (x : ℕ → ℝ) (n : ℕ) := x (n+1)-p*x n

theorem defect_contracts_backwards (p : ℝ) (hp : p+p^2=1)
    (x : ℕ → ℝ) (hr : ∀ n, x n=x (n+1)+x (n+2)) (n : ℕ) :
    defect p x n = -p * defect p x (n+1) := by
  simp only [defect]
  have h := hr n
  have hp' : p^2=1-p := by linarith
  calc
    x (n+1)-p*x n = (1-p)*x (n+1)-p*x (n+2) := by rw [h]; ring
    _ = -p*(x (n+1+1)-p*x (n+1)) := by rw [← hp']; ring

theorem defect_after_k (p : ℝ) (hp : p+p^2=1)
    (x : ℕ → ℝ) (hr : ∀ n, x n=x (n+1)+x (n+2)) (n k : ℕ) :
    defect p x n = (-p)^k * defect p x (n+k) := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [ih, defect_contracts_backwards p hp x hr (n+k)]
    simp only [pow_succ, Nat.add_assoc]
    ring

theorem defect_bounded (p : ℝ) (hp0 : 0 ≤ p) (hp1 : p ≤ 1)
    (x : ℕ → ℝ) (hb : ∀ n, 0 ≤ x n ∧ x n ≤ 1) (n : ℕ) :
    |defect p x n| ≤ 1 := by
  rw [abs_le]
  have h0 := hb n
  have h1 := hb (n+1)
  dsimp [defect]
  constructor <;> nlinarith

theorem compatible_defect_zero (p : ℝ) (hp0 : 0 ≤ p) (hp1 : p < 1)
    (hp : p+p^2=1) (x : ℕ → ℝ)
    (hr : ∀ n, x n=x (n+1)+x (n+2))
    (hb : ∀ n, 0 ≤ x n ∧ x n ≤ 1) (n : ℕ) : defect p x n=0 := by
  have bound (k : ℕ) : |defect p x n| ≤ p^k := by
    calc
      |defect p x n| = |(-p)^k * defect p x (n+k)| := by rw [← defect_after_k p hp x hr n k]
      _ = p^k * |defect p x (n+k)| := by rw [abs_mul, abs_pow, abs_neg, abs_of_nonneg hp0]
      _ ≤ p^k := by
        have h := defect_bounded p hp0 (le_of_lt hp1) x hb (n+k)
        nlinarith [pow_nonneg hp0 k]
  have hz : |defect p x n| ≤ 0 :=
    ge_of_tendsto' (tendsto_pow_atTop_nhds_zero_of_lt_one hp0 hp1) bound
  exact abs_eq_zero.mp (le_antisymm hz (abs_nonneg _))

/-- Completeness: all nonnegative compatible normalized trace weights,
not just an assumed stationary/Perron eigenprofile. -/
theorem all_compatible_weights_forced (p : ℝ) (hp0 : 0 ≤ p) (hp1 : p < 1)
    (hp : p+p^2=1) (x y : ℕ → ℝ)
    (hxp : ∀ n, 0 ≤ x n) (hyp : ∀ n, 0 ≤ y n)
    (hx : ∀ n, x n=x (n+1)+y (n+1))
    (hy : ∀ n, y n=x (n+1)) (hn : x 0+y 0=1) :
    ∀ n, x n=p^(n+1) ∧ y n=p^(n+2) := by
  have hb := compatible_bounds x y hxp hyp hx hn
  have hr := compatible_recurrence x y hx hy
  have hd (n : ℕ) : x (n+1)=p*x n := by
    have h := compatible_defect_zero p hp0 hp1 hp x hr hb n
    exact sub_eq_zero.mp h
  have hzero : x 0=p := by
    have hn' : x 0+x 1=1 := by simpa [hy] using hn
    have hf : (1+p)*(x 0-p)=0 := by nlinarith [hd 0]
    have hnz : (1+p : ℝ) ≠ 0 := by positivity
    exact sub_eq_zero.mp ((mul_eq_zero.mp hf).resolve_left hnz)
  have form (n : ℕ) : x n=p^(n+1) := by
    induction n with
    | zero => simpa using hzero
    | succ n ih => rw [hd n, ih, pow_succ]; ring
  intro n
  exact ⟨form n, by rw [hy n]; simpa [Nat.add_assoc] using form (n+1)⟩

theorem compatible_trace_has_no_parameter
    (p : ℝ) (hp0 : 0 ≤ p) (hp1 : p < 1) (hp : p+p^2=1)
    {T : Type*} (x y : T → ℕ → ℝ)
    (hxp : ∀ t n, 0 ≤ x t n) (hyp : ∀ t n, 0 ≤ y t n)
    (hx : ∀ t n, x t n=x t (n+1)+y t (n+1))
    (hy : ∀ t n, y t n=x t (n+1)) (hn : ∀ t, x t 0+y t 0=1)
    (s t : T) (n : ℕ) : x s n=x t n ∧ y s n=y t n := by
  have hs := all_compatible_weights_forced p hp0 hp1 hp (x s) (y s)
    (hxp s) (hyp s) (hx s) (hy s) (hn s) n
  have ht := all_compatible_weights_forced p hp0 hp1 hp (x t) (y t)
    (hxp t) (hyp t) (hx t) (hy t) (hn t) n
  exact ⟨hs.1.trans ht.1.symm, hs.2.trans ht.2.symm⟩

/-- The actual owner counts give at least a factor two of product growth
at each refinement, used in the finite-horizon trace-state error bound. -/
theorem count_product_growth (a b : ℝ) (ha : b ≤ a) (hb : 0 ≤ b) :
    2*(a*b) ≤ (a+b)*a := by nlinarith

theorem finite_extreme_width (a b u v w : ℝ)
    (hd : u*w-v^2=1 ∨ u*w-v^2 = -1)
    (ha : a*u+b*v ≠ 0) (hb : a*v+b*w ≠ 0) :
    |u/(a*u+b*v)-v/(a*v+b*w)| =
      |b/((a*u+b*v)*(a*v+b*w))| := by
  have he : u/(a*u+b*v)-v/(a*v+b*w) =
      b*(u*w-v^2)/((a*u+b*v)*(a*v+b*w)) := by
    rw [div_sub_div _ _ ha hb]
    congr 1
    ring
  rw [he]
  rcases hd with hd | hd <;> rw [hd] <;> simp [neg_div]

theorem residual_coefficients (u v A B : ℝ)
    (hu : 0 < u) (hv : 0 < v) (hs : u+v=1)
    (hA : 0 < A) (hB : 0 < B) :
    0 < u*v ∧ 0 < (u-u*v*v)/A ∧ 0 < (v-u*v*u)/B ∧
      u*v+A*((u-u*v*v)/A)+B*((v-u*v*u)/B)=1 := by
  have hu1 : u < 1 := by linarith
  have hv1 : v < 1 := by linarith
  have hv2 : v*v < 1 := by nlinarith
  have hu2 : u*u < 1 := by nlinarith
  have ha : 0 < u-u*v*v := by nlinarith [mul_pos hu (sub_pos.mpr hv2)]
  have hb : 0 < v-u*v*u := by nlinarith [mul_pos hv (sub_pos.mpr hu2)]
  refine ⟨mul_pos hu hv, div_pos ha hA, div_pos hb hB, ?_⟩
  field_simp
  nlinarith [hs, mul_eq_mul_left_iff.mp (congrArg (fun z : ℝ => u*v*A*B*z) hs)]

theorem faithful_mixture_eigenvalues (lam r : ℝ)
    (hl : 1/2 ≤ lam) (hl1 : lam < 1) (hr : 0 < r) (hr1 : r < 1) :
    0 < (1-lam)*r ∧ (1-lam)*r < lam := by
  constructor
  · exact mul_pos (sub_pos.mpr hl1) hr
  · nlinarith [mul_pos (sub_pos.mpr hl1) (sub_pos.mpr hr1)]

theorem heat_price_derivative (beta lam : ℝ) (hl : lam ≠ 0) :
    HasDerivAt (fun s : ℝ => -Real.log s / beta) (-(1/lam)/beta) lam := by
  simpa [one_div] using (Real.hasDerivAt_log hl).neg.div_const beta

theorem heat_price_derivative_ne_zero (beta lam : ℝ)
    (hb : 0 < beta) (hl : 0 < lam) : -(1/lam)/beta ≠ 0 := by
  exact div_ne_zero (neg_ne_zero.mpr (one_div_ne_zero (ne_of_gt hl))) (ne_of_gt hb)

/-- The exact scalar price derivative along the full cyclic-state mixture.
The matrix interpretation is a separately proved state-interface statement. -/
theorem cyclic_mixture_price_derivative (beta lam : ℝ) (hl : lam ≠ 0) :
    HasDerivAt (fun s : ℝ => -Real.log (lam+(1-lam)*s)/beta)
      (-((1-lam)/lam)/beta) 0 := by
  have ha : HasDerivAt (fun s : ℝ => lam+(1-lam)*s) (1-lam) 0 := by
    simpa using (((hasDerivAt_id (0 : ℝ)).const_mul (1-lam)).const_add lam)
  have hn : lam+(1-lam)*(0 : ℝ) ≠ 0 := by simpa using hl
  simpa using (ha.log hn).neg.div_const beta

theorem cyclic_mixture_strict_descent (beta lam : ℝ)
    (hb : 0 < beta) (hl : 0 < lam) (hl1 : lam < 1) :
    -((1-lam)/lam)/beta < 0 := by
  exact div_neg_of_neg_of_pos (neg_neg_of_pos (div_pos (sub_pos.mpr hl1) hl)) hb

end
end D0.Research.AFTracePreparation

#check D0.Research.AFTracePreparation.compatible_recurrence
#check D0.Research.AFTracePreparation.compatible_bounds
#check D0.Research.AFTracePreparation.defect_contracts_backwards
#check D0.Research.AFTracePreparation.defect_after_k
#check D0.Research.AFTracePreparation.defect_bounded
#check D0.Research.AFTracePreparation.compatible_defect_zero
#check D0.Research.AFTracePreparation.all_compatible_weights_forced
#check D0.Research.AFTracePreparation.compatible_trace_has_no_parameter
#check D0.Research.AFTracePreparation.count_product_growth
#check D0.Research.AFTracePreparation.finite_extreme_width
#check D0.Research.AFTracePreparation.residual_coefficients
#check D0.Research.AFTracePreparation.faithful_mixture_eigenvalues
#check D0.Research.AFTracePreparation.heat_price_derivative
#check D0.Research.AFTracePreparation.heat_price_derivative_ne_zero
#check D0.Research.AFTracePreparation.cyclic_mixture_price_derivative
#check D0.Research.AFTracePreparation.cyclic_mixture_strict_descent
#print axioms D0.Research.AFTracePreparation.compatible_recurrence
#print axioms D0.Research.AFTracePreparation.compatible_bounds
#print axioms D0.Research.AFTracePreparation.defect_contracts_backwards
#print axioms D0.Research.AFTracePreparation.defect_after_k
#print axioms D0.Research.AFTracePreparation.defect_bounded
#print axioms D0.Research.AFTracePreparation.compatible_defect_zero
#print axioms D0.Research.AFTracePreparation.all_compatible_weights_forced
#print axioms D0.Research.AFTracePreparation.compatible_trace_has_no_parameter
#print axioms D0.Research.AFTracePreparation.count_product_growth
#print axioms D0.Research.AFTracePreparation.finite_extreme_width
#print axioms D0.Research.AFTracePreparation.residual_coefficients
#print axioms D0.Research.AFTracePreparation.faithful_mixture_eigenvalues
#print axioms D0.Research.AFTracePreparation.heat_price_derivative
#print axioms D0.Research.AFTracePreparation.heat_price_derivative_ne_zero
#print axioms D0.Research.AFTracePreparation.cyclic_mixture_price_derivative
#print axioms D0.Research.AFTracePreparation.cyclic_mixture_strict_descent
