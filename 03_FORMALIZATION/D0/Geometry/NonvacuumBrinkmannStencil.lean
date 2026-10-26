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
`63c36b18af67fc1f113f9e33deb13cf43ddf4556`, in
`02_REGISTRY/research/A4D_EXACT_NONVACUUM_GR_MIDPOINT_C2_RECOVERY_2026_10_20.md`,
§§7.1–7.2. The corresponding unmerged scientific-owner source is pinned at
PR #334 commit `fe5cf335da04cac14e50407b03f98b96be17dc52`, same path, blob
`67531a343a0ae707ff0a3830c0e2c9cf2bbc8213`. That version gives the explicit
CAR-slack threshold in Eq. (24); this module formalizes only the componentwise
midpoint defect and finite-stencil source identities, not the slack conclusion.

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

/--
For a two-component function `ψ`, the nonvacuum Brinkmann source is the norm
of the derivative values used by that same chronological midpoint update.
This is an algebraic source/update identity and assumes no regularity of `ψ`;
the smooth-field refinement estimate is proved separately under its C^3 and
third-derivative-bound hypotheses.
-/
theorem sampledMatterMidpointProfile_source_eq_derivativeNorm
    (h coupling x₀ : ℝ) (ψ : ℝ → Fin 2 → ℝ)
    (a2 b2 a3 b3 : ℕ → ℝ) (n : ℕ) (x y : ℝ) (hh : h ≠ 0) :
    transverseFivePointLaplacian h
      (fun x y => finiteTimeNonvacuumBrinkmannProfile
        coupling (sampledMatterMidpointRate ψ x₀ h) a2 b2 a3 b3 n x y) x y =
      -4 * coupling * twoComponentMatterNormSq
        (sampledMatterMidpointRate ψ x₀ h n) := by
  rw [finiteTimeNonvacuumProfile_source_eq_midpointHistoryNorm
    h coupling (sampledMatterMidpointRate ψ x₀ h)
    (sampledMatterExactValues ψ x₀ h 0) a2 b2 a3 b3 n x y hh]
  rw [twoComponentMatterNormSq_midpointHistoryGradient_eq_rate
    h (sampledMatterMidpointRate ψ x₀ h)
    (sampledMatterExactValues ψ x₀ h 0) n hh]

/-- The half-step readout assigned to coframe site `j` in the source carrier. -/
def nonvacuumCoframeReadoutTime (x₀ h : ℝ) (j : ℕ) : ℝ :=
  x₀ + (j : ℝ) * h - h / 2

/-- Sample a continuum profile coefficient at the next coframe readout. -/
def sampleNonvacuumCoefficientAtNextSite
    (a : ℝ → ℝ) (x₀ h : ℝ) (n : ℕ) : ℝ :=
  a (nonvacuumCoframeReadoutTime x₀ h (n + 1))

/-- The fixed continuum Brinkmann profile built from its original fields. -/
def fixedNonvacuumBrinkmannProfileFromFields
    (coupling : ℝ) (ψ : ℝ → Fin 2 → ℝ)
    (a2 b2 a3 b3 : ℝ → ℝ) (u x y : ℝ) : ℝ :=
  nonvacuumBrinkmannProfile coupling
    (twoComponentMatterNormSq (fun i => deriv (fun t : ℝ => ψ t i) u))
    (a2 u) (b2 u) (a3 u) (b3 u) x y

/-- The midpoint of cell `n` is the declared readout at site `n + 1`. -/
theorem sampledMatterMidpointTime_eq_nextCoframeReadout
    (x₀ h : ℝ) (n : ℕ) :
    x₀ + (n : ℝ) * h + h / 2 =
      nonvacuumCoframeReadoutTime x₀ h (n + 1) := by
  simp only [nonvacuumCoframeReadoutTime, Nat.cast_add, Nat.cast_one]
  ring

/-- The sampled midpoint derivative is evaluated at that same next site. -/
theorem sampledMatterMidpointRate_eq_nextCoframeReadout
    (ψ : ℝ → Fin 2 → ℝ) (x₀ h : ℝ) (n : ℕ) :
    sampledMatterMidpointRate ψ x₀ h n =
      fun i => deriv (fun t : ℝ => ψ t i)
        (nonvacuumCoframeReadoutTime x₀ h (n + 1)) := by
  funext i
  simp only [sampledMatterMidpointRate]
  rw [sampledMatterMidpointTime_eq_nextCoframeReadout]

/--
The finite profile at step `n` is the fixed continuum profile evaluated at
the declared coframe readout `τ_(n+1)`, with all four harmonic coefficients
sampled at that same time.
-/
theorem sampledNonvacuumBrinkmannProfile_eq_fixedReadout
    (x₀ h coupling : ℝ) (ψ : ℝ → Fin 2 → ℝ)
    (a2 b2 a3 b3 : ℝ → ℝ) (n : ℕ) (x y : ℝ) :
    finiteTimeNonvacuumBrinkmannProfile coupling
      (sampledMatterMidpointRate ψ x₀ h)
      (sampleNonvacuumCoefficientAtNextSite a2 x₀ h)
      (sampleNonvacuumCoefficientAtNextSite b2 x₀ h)
      (sampleNonvacuumCoefficientAtNextSite a3 x₀ h)
      (sampleNonvacuumCoefficientAtNextSite b3 x₀ h) n x y =
    fixedNonvacuumBrinkmannProfileFromFields coupling ψ a2 b2 a3 b3
      (nonvacuumCoframeReadoutTime x₀ h (n + 1)) x y := by
  change nonvacuumBrinkmannProfile coupling
      (twoComponentMatterNormSq (sampledMatterMidpointRate ψ x₀ h n))
      (a2 (nonvacuumCoframeReadoutTime x₀ h (n + 1)))
      (b2 (nonvacuumCoframeReadoutTime x₀ h (n + 1)))
      (a3 (nonvacuumCoframeReadoutTime x₀ h (n + 1)))
      (b3 (nonvacuumCoframeReadoutTime x₀ h (n + 1))) x y =
    nonvacuumBrinkmannProfile coupling
      (twoComponentMatterNormSq
        (fun i => deriv (fun t : ℝ => ψ t i)
          (nonvacuumCoframeReadoutTime x₀ h (n + 1))))
      (a2 (nonvacuumCoframeReadoutTime x₀ h (n + 1)))
      (b2 (nonvacuumCoframeReadoutTime x₀ h (n + 1)))
      (a3 (nonvacuumCoframeReadoutTime x₀ h (n + 1)))
      (b3 (nonvacuumCoframeReadoutTime x₀ h (n + 1))) x y
  rw [sampledMatterMidpointRate_eq_nextCoframeReadout]

/--
At every nonzero mesh width, the fixed continuum profile sampled on the
half-step coframe readout has exactly the source of the same midpoint matter
increment. This is the algebraic site/source map only; smoothness, normalized
CAR admissibility and the full Euler system remain separate obligations.
-/
theorem sampledFixedNonvacuumBrinkmannProfile_source_eq_siteMatter
    (x₀ h coupling : ℝ) (ψ : ℝ → Fin 2 → ℝ)
    (a2 b2 a3 b3 : ℝ → ℝ) (n : ℕ) (x y : ℝ) (hh : h ≠ 0) :
    transverseFivePointLaplacian h
      (fun x y => fixedNonvacuumBrinkmannProfileFromFields coupling ψ a2 b2 a3 b3
        (nonvacuumCoframeReadoutTime x₀ h (n + 1)) x y) x y =
      -4 * coupling * twoComponentMatterNormSq
        (fun i => deriv (fun t : ℝ => ψ t i)
          (nonvacuumCoframeReadoutTime x₀ h (n + 1))) := by
  have hprofile :
      (fun x y => fixedNonvacuumBrinkmannProfileFromFields coupling ψ a2 b2 a3 b3
        (nonvacuumCoframeReadoutTime x₀ h (n + 1)) x y) =
      (fun x y => finiteTimeNonvacuumBrinkmannProfile coupling
        (sampledMatterMidpointRate ψ x₀ h)
        (sampleNonvacuumCoefficientAtNextSite a2 x₀ h)
        (sampleNonvacuumCoefficientAtNextSite b2 x₀ h)
        (sampleNonvacuumCoefficientAtNextSite a3 x₀ h)
        (sampleNonvacuumCoefficientAtNextSite b3 x₀ h) n x y) := by
    funext x y
    exact (sampledNonvacuumBrinkmannProfile_eq_fixedReadout
      x₀ h coupling ψ a2 b2 a3 b3 n x y).symm
  calc
    transverseFivePointLaplacian h
        (fun x y => fixedNonvacuumBrinkmannProfileFromFields coupling ψ a2 b2 a3 b3
          (nonvacuumCoframeReadoutTime x₀ h (n + 1)) x y) x y =
      transverseFivePointLaplacian h
        (fun x y => finiteTimeNonvacuumBrinkmannProfile coupling
          (sampledMatterMidpointRate ψ x₀ h)
          (sampleNonvacuumCoefficientAtNextSite a2 x₀ h)
          (sampleNonvacuumCoefficientAtNextSite b2 x₀ h)
          (sampleNonvacuumCoefficientAtNextSite a3 x₀ h)
          (sampleNonvacuumCoefficientAtNextSite b3 x₀ h) n x y) x y := by
            rw [hprofile]
    _ = -4 * coupling * twoComponentMatterNormSq
        (sampledMatterMidpointRate ψ x₀ h n) :=
          sampledMatterMidpointProfile_source_eq_derivativeNorm h coupling x₀ ψ
            (sampleNonvacuumCoefficientAtNextSite a2 x₀ h)
            (sampleNonvacuumCoefficientAtNextSite b2 x₀ h)
            (sampleNonvacuumCoefficientAtNextSite a3 x₀ h)
            (sampleNonvacuumCoefficientAtNextSite b3 x₀ h) n x y hh
    _ = -4 * coupling * twoComponentMatterNormSq
        (fun i => deriv (fun t : ℝ => ψ t i)
          (nonvacuumCoframeReadoutTime x₀ h (n + 1))) := by
            rw [sampledMatterMidpointRate_eq_nextCoframeReadout]

end


/-- A two-component cubic matter profile, represented by its coefficients. -/
def cubicMatterProfile
    (c0 c1 c2 c3 : Fin 2 → ℝ) (t : ℝ) : Fin 2 → ℝ :=
  fun i => c0 i + c1 i * t + c2 i * t ^ 2 + c3 i * t ^ 3

/-- The exact derivative of the two-component cubic matter profile. -/
def cubicMatterMidpointRate
    (c1 c2 c3 : Fin 2 → ℝ) (t : ℝ) : Fin 2 → ℝ :=
  fun i => c1 i + 2 * c2 i * t + 3 * c3 i * t ^ 2

/--
The actual chronological record obtained by integrating the cubic rate with
one midpoint increment per interval.
-/
noncomputable def cubicMatterMidpointSample (h : ℝ) (c0 c1 c2 c3 : Fin 2 → ℝ) :
    ℕ → Fin 2 → ℝ
  | 0 => c0
  | n + 1 =>
      finiteMatterMidpointStep h
        (cubicMatterMidpointRate c1 c2 c3 (((n : ℝ) + 1 / 2) * h))
        (cubicMatterMidpointSample h c0 c1 c2 c3 n)

/--
For a cubic matter profile, the accumulated midpoint increments have an exact
closed form. The only error is the cubic coefficient times n*h^3/4.
-/
theorem cubicMatterMidpointSample_eq_profile_sub_cubic_error
    (h : ℝ) (c0 c1 c2 c3 : Fin 2 → ℝ) (n : ℕ) (i : Fin 2) :
    cubicMatterMidpointSample h c0 c1 c2 c3 n i =
      cubicMatterProfile c0 c1 c2 c3 ((n : ℝ) * h) i -
        c3 i * (n : ℝ) * h ^ 3 / 4 := by
  induction n with
  | zero =>
      simp [cubicMatterMidpointSample, cubicMatterProfile]
  | succ n ih =>
      simp [cubicMatterMidpointSample, finiteMatterMidpointStep,
        cubicMatterMidpointRate, cubicMatterProfile, ih]
      ring

/--
The accumulated midpoint record differs from the sampled cubic profile by the
explicit signed cubic remainder.
-/
theorem cubicMatterMidpointSample_error_eq
    (h : ℝ) (c0 c1 c2 c3 : Fin 2 → ℝ) (n : ℕ) (i : Fin 2) :
    cubicMatterMidpointSample h c0 c1 c2 c3 n i -
      cubicMatterProfile c0 c1 c2 c3 ((n : ℝ) * h) i =
        -(c3 i * (n : ℝ) * h ^ 3 / 4) := by
  rw [cubicMatterMidpointSample_eq_profile_sub_cubic_error]
  ring

/-- The cubic midpoint error is exactly its third-derivative midpoint bound. -/
theorem cubicMatterMidpointSample_error_bound
    (h : ℝ) (c0 c1 c2 c3 : Fin 2 → ℝ) (n : ℕ) (i : Fin 2)
    (M : ℝ) (hM : ∀ i, |6 * c3 i| ≤ M) :
    |cubicMatterMidpointSample h c0 c1 c2 c3 n i -
      cubicMatterProfile c0 c1 c2 c3 ((n : ℝ) * h) i| ≤
        ((n : ℝ) * |h|) * M * |h| ^ 2 / 24 := by
  have hExact :
      |cubicMatterMidpointSample h c0 c1 c2 c3 n i -
        cubicMatterProfile c0 c1 c2 c3 ((n : ℝ) * h) i| =
        ((n : ℝ) * |h|) * |6 * c3 i| * |h| ^ 2 / 24 := by
    rw [cubicMatterMidpointSample_error_eq]
    rw [abs_neg]
    simp only [abs_div, abs_mul,
      abs_of_nonneg (show (0 : ℝ) ≤ (n : ℝ) from Nat.cast_nonneg n), abs_pow,
      abs_of_pos (by norm_num : (0 : ℝ) < 4),
      abs_of_nonneg (by norm_num : (0 : ℝ) ≤ 6)]
    ring_nf
  rw [hExact]
  have hfactor : 0 ≤ ((n : ℝ) * |h|) * |h| ^ 2 / 24 := by
    positivity
  have hmul := mul_le_mul_of_nonneg_left (hM i) hfactor
  nlinarith [hmul]

/--
The time-midpoint source generated by a cubic matter rate equals the norm of
the forward difference of the same recursively constructed matter record.
-/
theorem nonvacuumCubicMidpointSource_matches_record
    (h coupling x y : ℝ) (a2 b2 a3 b3 : ℝ → ℝ)
    (c0 c1 c2 c3 : Fin 2 → ℝ) (n : ℕ) (hh : h ≠ 0) :
    transverseFivePointLaplacian h
      (fun x y => nonvacuumBrinkmannProfile coupling
        (twoComponentMatterNormSq
          (cubicMatterMidpointRate c1 c2 c3 (((n : ℝ) + 1 / 2) * h)))
        (a2 (((n : ℝ) + 1 / 2) * h))
        (b2 (((n : ℝ) + 1 / 2) * h))
        (a3 (((n : ℝ) + 1 / 2) * h))
        (b3 (((n : ℝ) + 1 / 2) * h)) x y) x y =
      -4 * coupling * twoComponentMatterNormSq
        (finiteMatterForwardGradient h
          (cubicMatterMidpointSample h c0 c1 c2 c3 n)
          (cubicMatterMidpointSample h c0 c1 c2 c3 (n + 1))) := by
  have hsource :=
    nonvacuumProfile_source_eq_finiteMidpointMatterNorm h coupling
      (a2 (((n : ℝ) + 1 / 2) * h))
      (b2 (((n : ℝ) + 1 / 2) * h))
      (a3 (((n : ℝ) + 1 / 2) * h))
      (b3 (((n : ℝ) + 1 / 2) * h)) x y
      (cubicMatterMidpointRate c1 c2 c3 (((n : ℝ) + 1 / 2) * h))
      (cubicMatterMidpointSample h c0 c1 c2 c3 n) hh
  simpa [cubicMatterMidpointSample, finiteMatterMidpointStep] using hsource

end D0.Geometry
