import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import D0.Analysis.MidpointQuadrature
import Mathlib.Tactic

namespace D0.Geometry

open scoped BigOperators

noncomputable section

/-!
# Exact nonvacuum Brinkmann stencil and midpoint source

This module formalizes the exact algebraic fragment in the positive
nonvacuum recovery case, source-pinned at main commit
`8b94198c8dfbdf5983ad0b350b058fb30bb68a54`, blob
`63c36b18af67fc1f113f9e33deb13cf43ddf4556`, §§7.1–7.2.

It proves that the centered five-point transverse stencil annihilates the
displayed harmonic quadratic/cubic family, sends the radial quadratic to
four, and therefore reads the profile source as `-4 * coupling * energy`.
It also proves that the actual finite two-component midpoint update has
forward gradient exactly equal to its midpoint rate, so its norm is the
energy used by that readout. For a sampled exact history, it derives the
per-cell midpoint defect from a bound on the third derivative and composes
that estimate into a uniform second-order error bound at every mesh point.

This is an exact finite algebraic and calculus application. It does not
formalize the original CAR construction, the 40 varied Cartan equations, or
all 16+24+2 Euler rows. The C^3 estimate is conditional on a supplied bound
for the same sampled component functions; it does not select a physical Book,
clock, source, or execution.
-/

/-- The centered five-point transverse Laplacian with nonzero mesh width. -/
def transverseFivePointLaplacian (h : ℝ) (f : ℝ → ℝ → ℝ) (x y : ℝ) : ℝ :=
  (f (x + h) y + f (x - h) y + f x (y + h) + f x (y - h) - 4 * f x y) / h ^ 2

/-- The quadratic and cubic harmonic profile used in the positive example. -/
def harmonicBrinkmannCubic
    (a2 b2 a3 b3 x y : ℝ) : ℝ :=
  a2 * (x ^ 2 - y ^ 2) + 2 * b2 * x * y +
    a3 * (x ^ 3 - 3 * x * y ^ 2) + b3 * (3 * x ^ 2 * y - y ^ 3)

/-- The exact sourced Brinkmann profile on the finite transverse stencil. -/
def nonvacuumBrinkmannProfile
    (coupling energy a2 b2 a3 b3 x y : ℝ) : ℝ :=
  -(coupling * energy) * (x ^ 2 + y ^ 2) +
    harmonicBrinkmannCubic a2 b2 a3 b3 x y

/-- Every displayed harmonic quadratic/cubic is annihilated at every `h ≠ 0`. -/
theorem transverseFivePoint_harmonicBrinkmannCubic_eq_zero
    (h a2 b2 a3 b3 x y : ℝ) (hh : h ≠ 0) :
    transverseFivePointLaplacian h
      (fun x y => harmonicBrinkmannCubic a2 b2 a3 b3 x y) x y = 0 := by
  unfold transverseFivePointLaplacian harmonicBrinkmannCubic
  field_simp [hh]
  ring

/-- The centered five-point transverse Laplacian of the radial quadratic is four. -/
theorem transverseFivePoint_radialQuadratic_eq_four
    (h x y : ℝ) (hh : h ≠ 0) :
    transverseFivePointLaplacian h (fun x y => x ^ 2 + y ^ 2) x y = 4 := by
  unfold transverseFivePointLaplacian
  field_simp [hh]
  ring

/-- The sourced profile has the exact finite source at every nonzero mesh size. -/
theorem transverseFivePoint_nonvacuumBrinkmannProfile_eq_source
    (h coupling energy a2 b2 a3 b3 x y : ℝ) (hh : h ≠ 0) :
    transverseFivePointLaplacian h
      (fun x y => nonvacuumBrinkmannProfile coupling energy a2 b2 a3 b3 x y) x y =
        -4 * coupling * energy := by
  unfold transverseFivePointLaplacian nonvacuumBrinkmannProfile
    harmonicBrinkmannCubic
  field_simp [hh]
  ring

/-- One midpoint finite update of the original two real matter components. -/
def finiteMatterMidpointStep
    (h : ℝ) (rate base : Fin 2 → ℝ) : Fin 2 → ℝ :=
  fun i => base i + h * rate i

/-- The forward difference of the finite two-component matter record. -/
def finiteMatterForwardGradient
    (h : ℝ) (base next : Fin 2 → ℝ) : Fin 2 → ℝ :=
  fun i => (next i - base i) / h

/-- The squared Euclidean norm of the original two real matter components. -/
def twoComponentMatterNormSq (v : Fin 2 → ℝ) : ℝ :=
  ∑ i : Fin 2, v i ^ 2

/-- The forward gradient of the actual midpoint update is its midpoint rate. -/
theorem finiteMatterForwardGradient_midpointStep
    (h : ℝ) (rate base : Fin 2 → ℝ) (i : Fin 2) (hh : h ≠ 0) :
    finiteMatterForwardGradient h base (finiteMatterMidpointStep h rate base) i =
      rate i := by
  unfold finiteMatterForwardGradient finiteMatterMidpointStep
  field_simp [hh]
  ring

/-- The finite midpoint record's squared gradient norm equals its rate energy. -/
theorem twoComponentMatterNormSq_midpointGradient_eq_rate
    (h : ℝ) (rate base : Fin 2 → ℝ) (hh : h ≠ 0) :
    twoComponentMatterNormSq
      (finiteMatterForwardGradient h base (finiteMatterMidpointStep h rate base)) =
        twoComponentMatterNormSq rate := by
  unfold twoComponentMatterNormSq
  apply Finset.sum_congr rfl
  intro i hi
  rw [finiteMatterForwardGradient_midpointStep h rate base i hh]

/--
The stencil source is exactly the energy of the same finite midpoint matter
record; no independent energy variable is installed.
-/
theorem nonvacuumProfile_source_eq_finiteMidpointMatterNorm
    (h coupling a2 b2 a3 b3 x y : ℝ) (rate base : Fin 2 → ℝ)
    (hh : h ≠ 0) :
    transverseFivePointLaplacian h
      (fun x y => nonvacuumBrinkmannProfile coupling
        (twoComponentMatterNormSq rate) a2 b2 a3 b3 x y) x y =
      -4 * coupling * twoComponentMatterNormSq
        (finiteMatterForwardGradient h base (finiteMatterMidpointStep h rate base)) := by
  rw [transverseFivePoint_nonvacuumBrinkmannProfile_eq_source
    h coupling (twoComponentMatterNormSq rate) a2 b2 a3 b3 x y hh]
  rw [twoComponentMatterNormSq_midpointGradient_eq_rate h rate base hh]

/-- A chronological finite matter record driven by a two-component rate at each step. -/
def finiteMatterMidpointHistory
    (h : ℝ) (rate : ℕ → Fin 2 → ℝ) (base : Fin 2 → ℝ) :
    ℕ → Fin 2 → ℝ
  | 0 => base
  | n + 1 => finiteMatterMidpointStep h (rate n)
      (finiteMatterMidpointHistory h rate base n)

/-- Each adjacent pair in the history is the specified midpoint update. -/
theorem finiteMatterMidpointHistory_next
    (h : ℝ) (rate : ℕ → Fin 2 → ℝ) (base : Fin 2 → ℝ)
    (n : ℕ) (i : Fin 2) :
    finiteMatterMidpointHistory h rate base (n + 1) i =
      finiteMatterMidpointHistory h rate base n i + h * rate n i := by
  rfl

/-- The chronological endpoint is the initial record plus its accumulated rates. -/
theorem finiteMatterMidpointHistory_eq_base_add_rateSum
    (h : ℝ) (rate : ℕ → Fin 2 → ℝ) (base : Fin 2 → ℝ)
    (n : ℕ) (i : Fin 2) :
    finiteMatterMidpointHistory h rate base n i =
      base i + h * (∑ k ∈ Finset.range n, rate k i) := by
  induction n with
  | zero => simp [finiteMatterMidpointHistory]
  | succ n ih =>
      rw [finiteMatterMidpointHistory_next, Finset.sum_range_succ, ih]
      ring

/-- The actual forward difference of every history step recovers its rate. -/
theorem finiteMatterForwardGradient_midpointHistory
    (h : ℝ) (rate : ℕ → Fin 2 → ℝ) (base : Fin 2 → ℝ)
    (n : ℕ) (i : Fin 2) (hh : h ≠ 0) :
    finiteMatterForwardGradient h
      (finiteMatterMidpointHistory h rate base n)
      (finiteMatterMidpointHistory h rate base (n + 1)) i = rate n i := by
  change finiteMatterForwardGradient h
    (finiteMatterMidpointHistory h rate base n)
    (finiteMatterMidpointStep h (rate n)
      (finiteMatterMidpointHistory h rate base n)) i = rate n i
  exact finiteMatterForwardGradient_midpointStep h (rate n)
    (finiteMatterMidpointHistory h rate base n) i hh

/-- The squared gradient norm of one chronological step is its rate energy. -/
theorem twoComponentMatterNormSq_midpointHistoryGradient_eq_rate
    (h : ℝ) (rate : ℕ → Fin 2 → ℝ) (base : Fin 2 → ℝ)
    (n : ℕ) (hh : h ≠ 0) :
    twoComponentMatterNormSq
      (finiteMatterForwardGradient h
        (finiteMatterMidpointHistory h rate base n)
        (finiteMatterMidpointHistory h rate base (n + 1))) =
      twoComponentMatterNormSq (rate n) := by
  unfold twoComponentMatterNormSq
  apply Finset.sum_congr rfl
  intro i hi
  rw [finiteMatterForwardGradient_midpointHistory h rate base n i hh]

/-- The complete finite-history gradient energy equals the sum of its rate energies. -/
theorem twoComponentMatterHistorySquaredGradientSum_eq_rateEnergySum
    (h : ℝ) (rate : ℕ → Fin 2 → ℝ) (base : Fin 2 → ℝ)
    (n : ℕ) (hh : h ≠ 0) :
    (∑ k ∈ Finset.range n,
      twoComponentMatterNormSq
        (finiteMatterForwardGradient h
          (finiteMatterMidpointHistory h rate base k)
          (finiteMatterMidpointHistory h rate base (k + 1)))) =
    ∑ k ∈ Finset.range n, twoComponentMatterNormSq (rate k) := by
  apply Finset.sum_congr rfl
  intro k hk
  exact twoComponentMatterNormSq_midpointHistoryGradient_eq_rate
    h rate base k hh

/--
The local midpoint quadrature defect in one real component: sampled increment
minus the exact increment between adjacent values.
-/
def finiteMatterMidpointLocalDefect
    (h : ℝ) (rate exact : ℕ → Fin 2 → ℝ) (n : ℕ) (i : Fin 2) : ℝ :=
  h * rate n i - (exact (n + 1) i - exact n i)

/-- Exact samples of a two-component matter history on the refining time grid. -/
def sampledMatterExactValues
    (ψ : ℝ → Fin 2 → ℝ) (x₀ h : ℝ) : ℕ → Fin 2 → ℝ :=
  fun n i => ψ (x₀ + (n : ℝ) * h) i

/-- The midpoint derivative rate of the same exact component history. -/
def sampledMatterMidpointRate
    (ψ : ℝ → Fin 2 → ℝ) (x₀ h : ℝ) : ℕ → Fin 2 → ℝ :=
  fun n i => deriv (fun t : ℝ => ψ t i) (x₀ + (n : ℝ) * h + h / 2)

/--
The actual sample/rate pair has local defect `M*h^3/24` when the same
component function is C^3 and its third derivative is bounded by `M` across
the full sampled interval.
-/
theorem sampledMatterMidpointLocalDefect_abs_le
    (ψ : ℝ → Fin 2 → ℝ) (x₀ h M duration : ℝ) (N k : ℕ) (i : Fin 2)
    (h_nonneg : 0 ≤ h) (h_duration : (N : ℝ) * h = duration) (hk : k < N)
    (hC3 : ∀ j : Fin 2, ContDiff ℝ 3 (fun t : ℝ => ψ t j))
    (hThird : ∀ t ∈ Set.Icc x₀ (x₀ + duration), ∀ j : Fin 2,
      |iteratedDeriv 3 (fun u : ℝ => ψ u j) t| ≤ M) :
    |finiteMatterMidpointLocalDefect h (sampledMatterMidpointRate ψ x₀ h)
      (sampledMatterExactValues ψ x₀ h) k i| ≤ M * h ^ 3 / 24 := by
  let xₖ : ℝ := x₀ + (k : ℝ) * h
  have hkN : (k : ℝ) + 1 ≤ (N : ℝ) := by
    exact_mod_cast Nat.succ_le_of_lt hk
  have hStart : x₀ ≤ xₖ := by
    dsimp [xₖ]
    exact le_add_of_nonneg_right (mul_nonneg (Nat.cast_nonneg k) h_nonneg)
  have hEnd : xₖ + h ≤ x₀ + duration := by
    dsimp [xₖ]
    rw [← h_duration]
    nlinarith [mul_le_mul_of_nonneg_right hkN h_nonneg]
  have hCell : ∀ y ∈ Set.Icc xₖ (xₖ + h), y ∈ Set.Icc x₀ (x₀ + duration) := by
    intro y hy
    exact ⟨le_trans hStart hy.1, le_trans hy.2 hEnd⟩
  have hNextSite : x₀ + ((k : ℝ) + 1) * h = xₖ + h := by
    dsimp [xₖ]
    ring
  have hScalar := D0.Analysis.midpointQuadrature_error_abs_le_of_thirdDerivative_bound
    (fun t : ℝ => ψ t i) xₖ h M h_nonneg (hC3 i)
    (fun y hy => hThird y (hCell y hy) i)
  simpa [finiteMatterMidpointLocalDefect, sampledMatterMidpointRate,
    sampledMatterExactValues, xₖ, hNextSite] using hScalar

/--
The accumulated finite-history error is exactly the sum of its local
midpoint increment defects. No smoothness or error estimate is assumed.
-/
theorem finiteMatterMidpointHistory_error_eq_localDefectSum
    (h : ℝ) (rate exact : ℕ → Fin 2 → ℝ) (n : ℕ) (i : Fin 2) :
    finiteMatterMidpointHistory h rate (exact 0) n i - exact n i =
      ∑ k ∈ Finset.range n, finiteMatterMidpointLocalDefect h rate exact k i := by
  induction n with
  | zero => simp [finiteMatterMidpointHistory]
  | succ n ih =>
      calc
        finiteMatterMidpointHistory h rate (exact 0) (n + 1) i - exact (n + 1) i =
            (finiteMatterMidpointHistory h rate (exact 0) n i - exact n i) +
              finiteMatterMidpointLocalDefect h rate exact n i := by
                rw [finiteMatterMidpointHistory_next]
                simp [finiteMatterMidpointLocalDefect]
                ring
        _ = (∑ k ∈ Finset.range n,
              finiteMatterMidpointLocalDefect h rate exact k i) +
              finiteMatterMidpointLocalDefect h rate exact n i := by rw [ih]
        _ = ∑ k ∈ Finset.range (n + 1),
              finiteMatterMidpointLocalDefect h rate exact k i := by
                rw [Finset.sum_range_succ]

/-- The absolute accumulated error is bounded by the sum of absolute local defects. -/
theorem finiteMatterMidpointHistory_error_abs_le_localDefectSum
    (h : ℝ) (rate exact : ℕ → Fin 2 → ℝ) (n : ℕ) (i : Fin 2) :
    |finiteMatterMidpointHistory h rate (exact 0) n i - exact n i| ≤
      ∑ k ∈ Finset.range n, |finiteMatterMidpointLocalDefect h rate exact k i| := by
  rw [finiteMatterMidpointHistory_error_eq_localDefectSum]
  exact Finset.abs_sum_le_sum_abs _ _

/--
If every step has defect at most `C`, the error after `n` steps is at most
`n * C`. This is the discrete composition step in the midpoint refinement
estimate; the local calculus estimate remains a separate premise.
-/
theorem finiteMatterMidpointHistory_error_abs_le_localDefectBound
    (h C : ℝ) (rate exact : ℕ → Fin 2 → ℝ) (n : ℕ) (i : Fin 2)
    (hLocal : ∀ k ∈ Finset.range n,
      |finiteMatterMidpointLocalDefect h rate exact k i| ≤ C) :
    |finiteMatterMidpointHistory h rate (exact 0) n i - exact n i| ≤
      (n : ℝ) * C := by
  calc
    |finiteMatterMidpointHistory h rate (exact 0) n i - exact n i|
        ≤ ∑ k ∈ Finset.range n,
            |finiteMatterMidpointLocalDefect h rate exact k i| :=
          finiteMatterMidpointHistory_error_abs_le_localDefectSum h rate exact n i
    _ ≤ ∑ _k ∈ Finset.range n, C := by
          apply Finset.sum_le_sum
          intro k hk
          exact hLocal k hk
    _ = (n : ℝ) * C := by simp

/--
The standard `|I| * M * h^2 / 24` global rate follows from the per-cell
`M * h^3 / 24` midpoint defect bound, uniformly at every grid point and for
both real matter components. This theorem composes a supplied local estimate;
the sampled C^3 specialization below derives that estimate from the same
component functions.
-/
theorem finiteMatterMidpointHistory_error_le_refinementBound
    (h M duration : ℝ) (rate exact : ℕ → Fin 2 → ℝ) (N : ℕ)
    (h_nonneg : 0 ≤ h) (M_nonneg : 0 ≤ M)
    (h_duration : (N : ℝ) * h = duration)
    (hLocal : ∀ k < N, ∀ i : Fin 2,
      |finiteMatterMidpointLocalDefect h rate exact k i| ≤ M * h ^ 3 / 24) :
    ∀ n ≤ N, ∀ i : Fin 2,
      |finiteMatterMidpointHistory h rate (exact 0) n i - exact n i| ≤
        duration * M * h ^ 2 / 24 := by
  intro n hn i
  have hPrefix : ∀ k ∈ Finset.range n,
      |finiteMatterMidpointLocalDefect h rate exact k i| ≤ M * h ^ 3 / 24 := by
    intro k hk
    exact hLocal k (Finset.mem_range.mp hk |>.trans_le hn) i
  have hCount := finiteMatterMidpointHistory_error_abs_le_localDefectBound
    h (M * h ^ 3 / 24) rate exact n i hPrefix
  have hCell_nonneg : 0 ≤ M * h ^ 3 / 24 := by positivity
  calc
    |finiteMatterMidpointHistory h rate (exact 0) n i - exact n i|
        ≤ (n : ℝ) * (M * h ^ 3 / 24) := hCount
    _ ≤ (N : ℝ) * (M * h ^ 3 / 24) := by
          exact mul_le_mul_of_nonneg_right (Nat.cast_le.mpr hn) hCell_nonneg
    _ = duration * M * h ^ 2 / 24 := by
          rw [← h_duration]
          ring

/--
The sampled two-component midpoint history converges uniformly at each node
with the classical `duration * M * h^2 / 24` bound under a common C^3 source
and a third-derivative bound over the whole interval.
-/
theorem sampledMatterMidpointHistory_error_le_refinementBound
    (ψ : ℝ → Fin 2 → ℝ) (x₀ h M duration : ℝ) (N : ℕ)
    (h_nonneg : 0 ≤ h) (M_nonneg : 0 ≤ M)
    (h_duration : (N : ℝ) * h = duration)
    (hC3 : ∀ i : Fin 2, ContDiff ℝ 3 (fun t : ℝ => ψ t i))
    (hThird : ∀ t ∈ Set.Icc x₀ (x₀ + duration), ∀ i : Fin 2,
      |iteratedDeriv 3 (fun u : ℝ => ψ u i) t| ≤ M) :
    ∀ n ≤ N, ∀ i : Fin 2,
      |finiteMatterMidpointHistory h (sampledMatterMidpointRate ψ x₀ h)
          (sampledMatterExactValues ψ x₀ h 0) n i -
        sampledMatterExactValues ψ x₀ h n i| ≤ duration * M * h ^ 2 / 24 := by
  apply finiteMatterMidpointHistory_error_le_refinementBound
    h M duration (sampledMatterMidpointRate ψ x₀ h)
    (sampledMatterExactValues ψ x₀ h) N h_nonneg M_nonneg h_duration
  intro k hk i
  exact sampledMatterMidpointLocalDefect_abs_le ψ x₀ h M duration N k i
    h_nonneg h_duration hk hC3 hThird

/-- The time-indexed Brinkmann profile uses the rate of that same history step. -/
def finiteTimeNonvacuumBrinkmannProfile
    (coupling : ℝ) (rate : ℕ → Fin 2 → ℝ)
    (a2 b2 a3 b3 : ℕ → ℝ) (n : ℕ) (x y : ℝ) : ℝ :=
  nonvacuumBrinkmannProfile coupling (twoComponentMatterNormSq (rate n))
    (a2 n) (b2 n) (a3 n) (b3 n) x y

/--
At every chronological site and every nonzero mesh width, the exact
Brinkmann stencil source is the energy of the adjacent two-component history
values. The geometry and matter term therefore share the same rate input.
-/
theorem finiteTimeNonvacuumProfile_source_eq_midpointHistoryNorm
    (h coupling : ℝ) (rate : ℕ → Fin 2 → ℝ) (base : Fin 2 → ℝ)
    (a2 b2 a3 b3 : ℕ → ℝ) (n : ℕ) (x y : ℝ) (hh : h ≠ 0) :
    transverseFivePointLaplacian h
      (fun x y => finiteTimeNonvacuumBrinkmannProfile
        coupling rate a2 b2 a3 b3 n x y) x y =
      -4 * coupling * twoComponentMatterNormSq
        (finiteMatterForwardGradient h
          (finiteMatterMidpointHistory h rate base n)
          (finiteMatterMidpointHistory h rate base (n + 1))) := by
  dsimp [finiteTimeNonvacuumBrinkmannProfile]
  rw [transverseFivePoint_nonvacuumBrinkmannProfile_eq_source
    h coupling (twoComponentMatterNormSq (rate n))
    (a2 n) (b2 n) (a3 n) (b3 n) x y hh]
  rw [twoComponentMatterNormSq_midpointHistoryGradient_eq_rate
    h rate base n hh]

end

end D0.Geometry
