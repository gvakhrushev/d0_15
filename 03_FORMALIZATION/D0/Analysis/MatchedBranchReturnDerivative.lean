import D0.Analysis.MatrixDeterminantDerivative
import D0.Algebra.MovingProjectorCalculus
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Star

/-!
# Matched finite branch returns

Matrix-calculus component of the matched-source synthesis in #334, commit
`b42db3deb`, source blob `886cac666344703940ebb699a304be2f86fb75bb`, §2.
Independent branch amplitudes and moving matrix components are kept until the
local completeness relation cancels the latter at the matched point. This
finite calculus does not assert physical admission, complete price selection,
or any GR source application.
-/

noncomputable section
namespace D0.Analysis.MatchedBranchReturn

open Filter
open scoped BigOperators Topology Matrix.Norms.Frobenius

variable {ι θ : Type*} [Fintype ι] [DecidableEq ι]

/-- Sum of independently varying amplitudes and matrix components. -/
def branchReturn (s : Finset θ) (amp : θ → ℝ → ℝ)
    (proj : θ → ℝ → Matrix ι ι ℂ) (y : ℝ) : Matrix ι ι ℂ :=
  ∑ i ∈ s, amp i y • proj i y

/-- Local completeness differentiates to zero. At a matched base all actual
component variations cancel; each amplitude direction remains independent. -/
theorem branchReturn_hasDerivAt_matched
    (s : Finset θ) (amp : θ → ℝ → ℝ) (proj : θ → ℝ → Matrix ι ι ℂ)
    (damp : θ → ℝ) (dproj : θ → Matrix ι ι ℂ) (p t : ℝ)
    (hamp : ∀ i ∈ s, HasDerivAt (amp i) (damp i) p)
    (hproj : ∀ i ∈ s, HasDerivAt (proj i) (dproj i) p)
    (hmatch : ∀ i ∈ s, amp i p = t)
    (hcomplete : ∀ᶠ y in 𝓝 p, ∑ i ∈ s, proj i y = 1) :
    branchReturn s amp proj p = t • (1 : Matrix ι ι ℂ) ∧
    HasDerivAt (branchReturn s amp proj)
      (∑ i ∈ s, damp i • proj i p) p := by
  have hsum : HasDerivAt (fun y => ∑ i ∈ s, proj i y) (∑ i ∈ s, dproj i) p :=
    HasDerivAt.fun_sum hproj
  have hzero : (∑ i ∈ s, dproj i) = 0 := by
    have he : (fun y => ∑ i ∈ s, proj i y) =ᶠ[𝓝 p] (fun _ => (1 : Matrix ι ι ℂ)) := hcomplete
    exact (hsum.congr_of_eventuallyEq he.symm).unique (hasDerivAt_const p _)
  constructor
  · have heval : (∑ i ∈ s, proj i p) = 1 := hcomplete.self_of_nhds
    unfold branchReturn
    calc
      _ = ∑ i ∈ s, t • proj i p := by
        apply Finset.sum_congr rfl
        intro i hi
        rw [hmatch i hi]
      _ = t • (∑ i ∈ s, proj i p) := by rw [Finset.smul_sum]
      _ = _ := by rw [heval]
  · have h : HasDerivAt (branchReturn s amp proj)
        (∑ i ∈ s, (amp i p • dproj i + damp i • proj i p)) p := by
      exact HasDerivAt.fun_sum fun i hi => (hamp i hi).smul (hproj i hi)
    have heq : (∑ i ∈ s, (amp i p • dproj i + damp i • proj i p)) =
        ∑ i ∈ s, damp i • proj i p := by
      rw [Finset.sum_add_distrib]
      have hc : (∑ i ∈ s, amp i p • dproj i) = 0 := by
        calc
          _ = ∑ i ∈ s, t • dproj i := by
            apply Finset.sum_congr rfl
            intro i hi
            rw [hmatch i hi]
          _ = t • (∑ i ∈ s, dproj i) := by rw [Finset.smul_sum]
          _ = 0 := by rw [hzero, smul_zero]
      rw [hc, zero_add]
    rwa [heq] at h


/-- On the positive determinant chart the actual finite return price has
its full derivative with independently varied branch amplitudes. -/
theorem branchReturn_price_hasDerivAt_matched
    (s : Finset θ) (amp : θ → ℝ → ℝ) (proj : θ → ℝ → Matrix ι ι ℂ)
    (damp : θ → ℝ) (dproj : θ → Matrix ι ι ℂ) (p t d eta nu : ℝ)
    (A : Matrix ι ι ℂ)
    (hamp : ∀ i ∈ s, HasDerivAt (amp i) (damp i) p)
    (hproj : ∀ i ∈ s, HasDerivAt (proj i) (dproj i) p)
    (hmatch : ∀ i ∈ s, amp i p = t)
    (hcomplete : ∀ᶠ y in 𝓝 p, ∑ i ∈ s, proj i y = 1)
    (hpositive : ∀ᶠ y in 𝓝 p, ∃ q : ℝ, 0 < q ∧
      ((d • (1 : Matrix ι ι ℂ) + eta •
        (branchReturn s amp proj y * A * star (branchReturn s amp proj y))).det) = (q : ℂ)) :
    let C := branchReturn s amp proj p
    let V := ∑ i ∈ s, damp i • proj i p
    let D := d • (1 : Matrix ι ι ℂ) + eta • (C * A * star C)
    HasDerivAt (fun y => -nu * Real.log
      ((d • (1 : Matrix ι ι ℂ) + eta •
        (branchReturn s amp proj y * A * star (branchReturn s amp proj y))).det.re))
      (-nu * ((D⁻¹ * (eta • (V * A * star C + C * A * star V))).trace).re) p := by
  let C := branchReturn s amp proj
  let V := ∑ i ∈ s, damp i • proj i p
  let D : ℝ → Matrix ι ι ℂ := fun y => d • (1 : Matrix ι ι ℂ) + eta • (C y * A * star (C y))
  have hC : HasDerivAt C V p := (branchReturn_hasDerivAt_matched s amp proj damp dproj p t
    hamp hproj hmatch hcomplete).2
  have hD : HasDerivAt D (eta • (V * A * star (C p) + C p * A * star V)) p := by
    have h := (hasDerivAt_const p (d • (1 : Matrix ι ι ℂ))).add
      (((hC.mul_const A).mul hC.star).const_smul eta)
    simpa only [zero_add] using h
  obtain ⟨q, hq, hqeq⟩ := hpositive.self_of_nhds
  have hSlit : (D p).det ∈ Complex.slitPlane := by
    change (d • (1 : Matrix ι ι ℂ) + eta •
      (branchReturn s amp proj p * A * star (branchReturn s amp proj p))).det ∈ Complex.slitPlane
    rw [hqeq]
    exact Complex.ofReal_mem_slitPlane.mpr hq
  have hLog := D0.Analysis.hasDerivAt_matrix_clogdet D _ p hD hSlit
  have hReal := (Complex.reCLM.hasFDerivAt.comp_hasDerivAt p hLog).const_mul (-nu)
  have heq : (fun y => -nu * Real.log ((D y).det.re)) =ᶠ[𝓝 p]
      (fun y => -nu * (Complex.log ((D y).det)).re) := by
    filter_upwards [hpositive] with y hy
    obtain ⟨r, hr, hre⟩ := hy
    rw [hre]
    simp [Complex.log_re, Real.norm_eq_abs, abs_of_pos hr]
  exact hReal.congr_of_eventuallyEq heq


/-- Independent branch velocities enter the complete trace source as a sum,
without commuting the history matrix with the branch projectors. -/
theorem branch_trace_velocity_sum
    (s : Finset θ) (v : θ → ℝ) (P : θ → Matrix ι ι ℂ)
    (R A C : Matrix ι ι ℂ) (eta : ℝ) :
    let V := ∑ i ∈ s, v i • P i
    ((R * (eta • (V * A * star C + C * A * star V))).trace).re =
      eta * ∑ i ∈ s, v i * ((R * (P i * A * star C + C * A * star (P i))).trace).re := by
  dsimp
  simp only [star_sum, star_smul, star_trivial, Finset.sum_mul, Finset.mul_sum, mul_add,
    smul_mul_assoc, mul_smul_comm, Matrix.trace_smul, Matrix.trace_sum,
    Matrix.trace_add, Complex.re_sum, Complex.add_re, Complex.smul_re, smul_eq_mul]
  simp only [Finset.sum_add_distrib]


/-- The differentiated original return price, resolved into independent
branch coefficients. The two noncommuting trace terms are both retained. -/
theorem branchReturn_price_hasDerivAt_independent_branches
    (s : Finset θ) (amp : θ → ℝ → ℝ) (proj : θ → ℝ → Matrix ι ι ℂ)
    (damp : θ → ℝ) (dproj : θ → Matrix ι ι ℂ) (p t d eta nu : ℝ)
    (A : Matrix ι ι ℂ)
    (hamp : ∀ i ∈ s, HasDerivAt (amp i) (damp i) p)
    (hproj : ∀ i ∈ s, HasDerivAt (proj i) (dproj i) p)
    (hmatch : ∀ i ∈ s, amp i p = t)
    (hcomplete : ∀ᶠ y in 𝓝 p, ∑ i ∈ s, proj i y = 1)
    (hpositive : ∀ᶠ y in 𝓝 p, ∃ q : ℝ, 0 < q ∧
      ((d • (1 : Matrix ι ι ℂ) + eta •
        (branchReturn s amp proj y * A * star (branchReturn s amp proj y))).det) = (q : ℂ)) :
    let C := branchReturn s amp proj p
    let D := d • (1 : Matrix ι ι ℂ) + eta • (C * A * star C)
    HasDerivAt (fun y => -nu * Real.log
      ((d • (1 : Matrix ι ι ℂ) + eta •
        (branchReturn s amp proj y * A * star (branchReturn s amp proj y))).det.re))
      (-nu * eta * ∑ i ∈ s, damp i *
        ((D⁻¹ * (proj i p * A * star C + C * A * star (proj i p))).trace).re) p := by
  have h := branchReturn_price_hasDerivAt_matched s amp proj damp dproj p t d eta nu A
    hamp hproj hmatch hcomplete hpositive
  have heq := branch_trace_velocity_sum s damp (fun i => proj i p)
    ((d • (1 : Matrix ι ι ℂ) + eta •
      (branchReturn s amp proj p * A * star (branchReturn s amp proj p)))⁻¹)
    A (branchReturn s amp proj p) eta
  apply h.congr_deriv
  rw [heq]
  ring

end D0.Analysis.MatchedBranchReturn
end
