import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2
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
`67531a343a0ae707ff0a3830c0e2c9cf2bbc8213`. This module now proves the
dimension-free vector midpoint estimate and Eq. (24)'s half-margin implication
for the same finite two-component history, identified through an isometric
Euclidean lift. It also retains the earlier, separate componentwise sufficient
condition.

It proves that the centered five-point transverse stencil annihilates the
displayed harmonic quadratic/cubic family, sends the radial quadratic to
four, and therefore reads the profile source as `-4 * coupling * energy`.
It also proves that the actual finite two-component midpoint update has
forward gradient exactly equal to its midpoint rate, so its norm is the
energy used by that readout. For a sampled exact history, it derives the
per-cell midpoint defect from a bound on the third derivative and composes
that estimate into a uniform second-order error bound at every mesh point,
both for scalar components and in the vector norm. The interval-local vector
CAR implication still assumes C³ regularity on the sampled interval, a vector
third-derivative bound, and a continuum norm envelope. The compactness
corollary below derives the latter two uniform bounds from a globally C³
profile and a pointwise strict chart margin; it does not derive smoothness or
the pointwise margin from the CAR generator or preparation. Its coefficient-
norm application derives that pointwise margin for cubic profiles on `[0,1]`
and carries an explicit nonzero initial matter rate; this finite-dimensional
subset is not selected by the original D0 generator. The cubic application
returns the same recursive record consumed by the exact stencil-source theorem;
the final composition pairs that source identity with the CAR-complement bound.
A stronger corollary also gives the exact Euclidean midpoint-refinement error
for that same record, without a component-count loss.

This is an exact finite algebraic and calculus application. It does not
formalize the original CAR construction, the 40 varied Cartan equations, or
all 16+24+2 Euler rows. Its C^3 estimate and complementary-amplitude criterion
are conditional on supplied analytic bounds; it does not select a physical
Book, clock, source, or execution.
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

/-- The same two real components represented in the Euclidean `L²` norm. -/
def twoComponentMatterEuclidean (v : Fin 2 → ℝ) : EuclideanSpace ℝ (Fin 2) :=
  (EuclideanSpace.equiv (Fin 2) ℝ).symm v

@[simp]
theorem twoComponentMatterEuclidean_apply (v : Fin 2 → ℝ) (i : Fin 2) :
    twoComponentMatterEuclidean v i = v i := by
  simp [twoComponentMatterEuclidean]

/-- The Euclidean lift preserves the squared norm used by the finite stencil. -/
theorem twoComponentMatterEuclidean_norm_sq (v : Fin 2 → ℝ) :
    ‖twoComponentMatterEuclidean v‖ ^ 2 = twoComponentMatterNormSq v := by
  rw [EuclideanSpace.real_norm_sq_eq]
  simp [twoComponentMatterEuclidean, twoComponentMatterNormSq]

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

/-- The radicand of the complementary amplitude in a two-component CAR record. -/
def twoComponentCARComplementRadicand (p : ℝ) (v : Fin 2 → ℝ) : ℝ :=
  1 - p - twoComponentMatterNormSq v

/-- The nonnegative square-root representative of the two-component CAR complement. -/
def twoComponentCARComplementAmplitude (p : ℝ) (v : Fin 2 → ℝ) : ℝ :=
  Real.sqrt (twoComponentCARComplementRadicand p v)

/-- A uniform component bound controls the squared two-component Euclidean norm. -/
theorem twoComponentMatterNormSq_le_two_mul_sq_of_abs_le
    (v : Fin 2 → ℝ) (B : ℝ) (hv : ∀ i : Fin 2, |v i| ≤ B) :
    twoComponentMatterNormSq v ≤ 2 * B ^ 2 := by
  unfold twoComponentMatterNormSq
  calc
    (∑ i : Fin 2, v i ^ 2) ≤ ∑ _i : Fin 2, B ^ 2 := by
      apply Finset.sum_le_sum
      intro i hi
      have habs := abs_le.mp (hv i)
      have hleft : 0 ≤ B - v i := by linarith
      have hright : 0 ≤ B + v i := by linarith
      nlinarith [mul_nonneg hleft hright]
    _ = 2 * B ^ 2 := by simp

/--
The existing componentwise midpoint estimate implies a conservative CAR
complement bound. If each continuum component is bounded by `A`, and each
component's accumulated history error is bounded by `B`, then the squared
two-component amplitude is at most `2 * (A + B)^2`. This is a componentwise
sufficient condition, not the vector-norm estimate in the source's Eq. (24).
-/
theorem sampledMatterMidpointCARComplement_positive_of_componentwiseSlack
    (ψ : ℝ → Fin 2 → ℝ) (x₀ h M duration A p : ℝ) (N : ℕ)
    (h_nonneg : 0 ≤ h) (M_nonneg : 0 ≤ M) (A_nonneg : 0 ≤ A)
    (h_duration : (N : ℝ) * h = duration)
    (hC3 : ∀ i : Fin 2, ContDiff ℝ 3 (fun t : ℝ => ψ t i))
    (hThird : ∀ t ∈ Set.Icc x₀ (x₀ + duration), ∀ i : Fin 2,
      |iteratedDeriv 3 (fun u : ℝ => ψ u i) t| ≤ M)
    (hEnvelope : ∀ t ∈ Set.Icc x₀ (x₀ + duration), ∀ i : Fin 2,
      |ψ t i| ≤ A)
    (hSlack : 2 * (A + duration * M * h ^ 2 / 24) ^ 2 < 1 - p) :
    ∀ n ≤ N,
      0 < twoComponentCARComplementAmplitude p
        (finiteMatterMidpointHistory h (sampledMatterMidpointRate ψ x₀ h)
          (sampledMatterExactValues ψ x₀ h 0) n) := by
  have hduration_nonneg : 0 ≤ duration := by
    rw [← h_duration]
    positivity
  have hErrorBound_nonneg : 0 ≤ duration * M * h ^ 2 / 24 := by
    positivity
  have hComponentBound_nonneg : 0 ≤ A + duration * M * h ^ 2 / 24 := by
    positivity
  have hHistoryError :=
    sampledMatterMidpointHistory_error_le_refinementBound
      ψ x₀ h M duration N h_nonneg M_nonneg h_duration hC3 hThird
  intro n hn
  have hnGrid : x₀ + (n : ℝ) * h ∈ Set.Icc x₀ (x₀ + duration) := by
    constructor
    · exact le_add_of_nonneg_right (mul_nonneg (Nat.cast_nonneg n) h_nonneg)
    · rw [← h_duration]
      have hn' : (n : ℝ) ≤ (N : ℝ) := Nat.cast_le.mpr hn
      nlinarith [mul_le_mul_of_nonneg_right hn' h_nonneg]
  have hHistoryComponent : ∀ i : Fin 2,
      |finiteMatterMidpointHistory h (sampledMatterMidpointRate ψ x₀ h)
          (sampledMatterExactValues ψ x₀ h 0) n i| ≤
        A + duration * M * h ^ 2 / 24 := by
    intro i
    have hApprox := hHistoryError n hn i
    have hExact := hEnvelope (x₀ + (n : ℝ) * h) hnGrid i
    calc
      |finiteMatterMidpointHistory h (sampledMatterMidpointRate ψ x₀ h)
          (sampledMatterExactValues ψ x₀ h 0) n i| =
        |(finiteMatterMidpointHistory h (sampledMatterMidpointRate ψ x₀ h)
            (sampledMatterExactValues ψ x₀ h 0) n i -
              sampledMatterExactValues ψ x₀ h n i) +
          sampledMatterExactValues ψ x₀ h n i| := by ring_nf
      _ ≤
        |finiteMatterMidpointHistory h (sampledMatterMidpointRate ψ x₀ h)
            (sampledMatterExactValues ψ x₀ h 0) n i -
              sampledMatterExactValues ψ x₀ h n i| +
          |sampledMatterExactValues ψ x₀ h n i| := abs_add_le _ _
      _ ≤ duration * M * h ^ 2 / 24 + A := add_le_add hApprox hExact
      _ = A + duration * M * h ^ 2 / 24 := by ring
  have hHistoryNorm := twoComponentMatterNormSq_le_two_mul_sq_of_abs_le
    (finiteMatterMidpointHistory h (sampledMatterMidpointRate ψ x₀ h)
      (sampledMatterExactValues ψ x₀ h 0) n)
    (A + duration * M * h ^ 2 / 24) hHistoryComponent
  have hRadicand :
      0 < twoComponentCARComplementRadicand p
        (finiteMatterMidpointHistory h (sampledMatterMidpointRate ψ x₀ h)
          (sampledMatterExactValues ψ x₀ h 0) n) := by
    unfold twoComponentCARComplementRadicand
    linarith
  exact Real.sqrt_pos.2 hRadicand

/-- The CAR complement amplitude defined by the norm of a real vector state. -/
def vectorCARComplementAmplitude {F : Type*} [NormedAddCommGroup F]
    (p : ℝ) (v : F) : ℝ := Real.sqrt (1 - p - ‖v‖ ^ 2)

/-
The vector-norm counterpart of the componentwise CAR result. It uses the
same complete finite-history recurrence and the dimension-free vector
midpoint estimate from `D0.Analysis`; no coordinate-count factor is added.
-/
theorem sampledVectorMidpointCARComplement_positive_of_vectorSlack_on_interval
    {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F] [CompleteSpace F]
    (ψ : ℝ → F) (x₀ h M duration A p : ℝ) (N : ℕ)
    (h_nonneg : 0 ≤ h) (M_nonneg : 0 ≤ M) (A_nonneg : 0 ≤ A)
    (h_duration : (N : ℝ) * h = duration)
    (hC3At : ∀ t ∈ Set.Icc x₀ (x₀ + duration), ContDiffAt ℝ 3 ψ t)
    (hThird : ∀ t ∈ Set.Icc x₀ (x₀ + duration),
      ‖iteratedDeriv 3 ψ t‖ ≤ M)
    (hEnvelope : ∀ t ∈ Set.Icc x₀ (x₀ + duration), ‖ψ t‖ ≤ A)
    (hSlack : (A + duration * M * h ^ 2 / 24) ^ 2 < 1 - p) :
    ∀ n ≤ N,
      0 < vectorCARComplementAmplitude p
        (D0.Analysis.finiteVectorMidpointHistory h
          (D0.Analysis.sampledVectorMidpointRate ψ x₀ h)
          (D0.Analysis.sampledVectorExactValues ψ x₀ h 0) n) := by
  have hDuration_nonneg : 0 ≤ duration := by
    rw [← h_duration]
    positivity
  have hErrorBound_nonneg : 0 ≤ duration * M * h ^ 2 / 24 := by positivity
  have hHistoryError := D0.Analysis.sampledVectorMidpointHistory_error_le_refinementBound_on_interval
    ψ x₀ h M duration N h_nonneg M_nonneg h_duration hC3At hThird
  intro n hn
  let state := D0.Analysis.finiteVectorMidpointHistory h
    (D0.Analysis.sampledVectorMidpointRate ψ x₀ h)
    (D0.Analysis.sampledVectorExactValues ψ x₀ h 0) n
  let exact := D0.Analysis.sampledVectorExactValues ψ x₀ h n
  have hnGrid : x₀ + (n : ℝ) * h ∈ Set.Icc x₀ (x₀ + duration) := by
    constructor
    · exact le_add_of_nonneg_right (mul_nonneg (Nat.cast_nonneg n) h_nonneg)
    · rw [← h_duration]
      have hn' : (n : ℝ) ≤ (N : ℝ) := Nat.cast_le.mpr hn
      nlinarith [mul_le_mul_of_nonneg_right hn' h_nonneg]
  have hExactNorm : ‖exact‖ ≤ A := by
    exact hEnvelope (x₀ + (n : ℝ) * h) hnGrid
  have hStateNorm : ‖state‖ ≤ A + duration * M * h ^ 2 / 24 := by
    have hErr := hHistoryError n hn
    calc
      ‖state‖ = ‖(state - exact) + exact‖ := by congr 1; abel
      _ ≤ ‖state - exact‖ + ‖exact‖ := norm_add_le _ _
      _ ≤ duration * M * h ^ 2 / 24 + A := add_le_add hErr hExactNorm
      _ = A + duration * M * h ^ 2 / 24 := by ring
  have hStateSq : ‖state‖ ^ 2 ≤ (A + duration * M * h ^ 2 / 24) ^ 2 :=
    (sq_le_sq₀ (norm_nonneg state) (by positivity)).2 hStateNorm
  have hRadicand : 0 < 1 - p - ‖state‖ ^ 2 := by
    linarith
  exact Real.sqrt_pos.2 hRadicand

/-- Global smoothness remains a compatibility wrapper for the local CAR proof. -/
theorem sampledVectorMidpointCARComplement_positive_of_vectorSlack
    {F : Type*} [NormedAddCommGroup F] [NormedSpace ℝ F] [CompleteSpace F]
    (ψ : ℝ → F) (x₀ h M duration A p : ℝ) (N : ℕ)
    (h_nonneg : 0 ≤ h) (M_nonneg : 0 ≤ M) (A_nonneg : 0 ≤ A)
    (h_duration : (N : ℝ) * h = duration)
    (hC3 : ContDiff ℝ 3 ψ)
    (hThird : ∀ t ∈ Set.Icc x₀ (x₀ + duration),
      ‖iteratedDeriv 3 ψ t‖ ≤ M)
    (hEnvelope : ∀ t ∈ Set.Icc x₀ (x₀ + duration), ‖ψ t‖ ≤ A)
    (hSlack : (A + duration * M * h ^ 2 / 24) ^ 2 < 1 - p) :
    ∀ n ≤ N,
      0 < vectorCARComplementAmplitude p
        (D0.Analysis.finiteVectorMidpointHistory h
          (D0.Analysis.sampledVectorMidpointRate ψ x₀ h)
          (D0.Analysis.sampledVectorExactValues ψ x₀ h 0) n) := by
  exact sampledVectorMidpointCARComplement_positive_of_vectorSlack_on_interval
    ψ x₀ h M duration A p N h_nonneg M_nonneg A_nonneg h_duration
    (fun t _ => hC3.contDiffAt (x := t)) hThird hEnvelope hSlack

/-- Coordinate projection commutes with the derivative at a locally smooth point. -/
private theorem euclideanMatter_deriv_apply_at
    (ψ : ℝ → EuclideanSpace ℝ (Fin 2)) (t : ℝ) (i : Fin 2)
    (hC3At : ContDiffAt ℝ 3 ψ t) :
    deriv ψ t i = deriv (fun s : ℝ => ψ s i) t := by
  let π : EuclideanSpace ℝ (Fin 2) →L[ℝ] ℝ := EuclideanSpace.proj i
  have hchain := fderiv_comp_deriv
    (l := π) (f := ψ) (x := t)
    (by fun_prop)
    (hC3At.differentiableAt (by norm_num))
  have hprojDerivative :
      fderiv ℝ π (ψ t) = π :=
    ContinuousLinearMap.fderiv (𝕜 := ℝ) (f := π) (x := ψ t)
  rw [hprojDerivative] at hchain
  simpa [π] using hchain.symm

/-- Global smoothness remains a compatibility wrapper for the local derivative lemma. -/
private theorem euclideanMatter_deriv_apply
    (ψ : ℝ → EuclideanSpace ℝ (Fin 2)) (hC3 : ContDiff ℝ 3 ψ)
    (t : ℝ) (i : Fin 2) :
    deriv ψ t i = deriv (fun s : ℝ => ψ s i) t := by
  exact euclideanMatter_deriv_apply_at ψ t i (hC3.contDiffAt (x := t))

/-- Sampling rates can be identified from local smoothness at that midpoint. -/
private theorem euclideanMatter_sampledRate_eq_at
    (ψ : ℝ → EuclideanSpace ℝ (Fin 2))
    (x₀ h : ℝ) (n : ℕ)
    (hC3At : ContDiffAt ℝ 3 ψ (x₀ + (n : ℝ) * h + h / 2)) :
    D0.Analysis.sampledVectorMidpointRate ψ x₀ h n =
      twoComponentMatterEuclidean (sampledMatterMidpointRate
        (fun t i => ψ t i) x₀ h n) := by
  ext i
  simp only [D0.Analysis.sampledVectorMidpointRate,
    twoComponentMatterEuclidean_apply, sampledMatterMidpointRate]
  exact euclideanMatter_deriv_apply_at ψ _ i hC3At

/-- Sampling the same Euclidean-valued source gives the existing component rates. -/
private theorem euclideanMatter_sampledRate_eq
    (ψ : ℝ → EuclideanSpace ℝ (Fin 2)) (hC3 : ContDiff ℝ 3 ψ)
    (x₀ h : ℝ) (n : ℕ) :
    D0.Analysis.sampledVectorMidpointRate ψ x₀ h n =
      twoComponentMatterEuclidean (sampledMatterMidpointRate
        (fun t i => ψ t i) x₀ h n) := by
  exact euclideanMatter_sampledRate_eq_at ψ x₀ h n
    (hC3.contDiffAt (x := x₀ + (n : ℝ) * h + h / 2))

/-- Exact samples in Euclidean space are the lift of the original two components. -/
private theorem euclideanMatter_sampledExact_eq
    (ψ : ℝ → EuclideanSpace ℝ (Fin 2)) (x₀ h : ℝ) (n : ℕ) :
    D0.Analysis.sampledVectorExactValues ψ x₀ h n =
      twoComponentMatterEuclidean (sampledMatterExactValues
        (fun t i => ψ t i) x₀ h n) := by
  ext i
  simp [D0.Analysis.sampledVectorExactValues, sampledMatterExactValues,
    twoComponentMatterEuclidean]

/-- The Euclidean and original two-component recurrences are the same history. -/
private theorem euclideanMatter_history_eq
    (ψ : ℝ → EuclideanSpace ℝ (Fin 2)) (hC3 : ContDiff ℝ 3 ψ)
    (x₀ h : ℝ) (n : ℕ) :
    D0.Analysis.finiteVectorMidpointHistory h
      (D0.Analysis.sampledVectorMidpointRate ψ x₀ h)
      (D0.Analysis.sampledVectorExactValues ψ x₀ h 0) n =
    twoComponentMatterEuclidean
      (finiteMatterMidpointHistory h
        (sampledMatterMidpointRate (fun t i => ψ t i) x₀ h)
        (sampledMatterExactValues (fun t i => ψ t i) x₀ h 0) n) := by
  induction n with
  | zero =>
      simp only [D0.Analysis.finiteVectorMidpointHistory,
        finiteMatterMidpointHistory]
      exact euclideanMatter_sampledExact_eq ψ x₀ h 0
  | succ n ih =>
      simp only [D0.Analysis.finiteVectorMidpointHistory,
        finiteMatterMidpointHistory]
      rw [ih]
      rw [euclideanMatter_sampledRate_eq ψ hC3 x₀ h n]
      ext i
      simp [twoComponentMatterEuclidean, finiteMatterMidpointStep]

/-- On a finite interval, local smoothness suffices for the same recurrence identity. -/
private theorem euclideanMatter_history_eq_on_interval
    (ψ : ℝ → EuclideanSpace ℝ (Fin 2)) (x₀ h duration : ℝ) (N : ℕ)
    (h_nonneg : 0 ≤ h) (h_duration : (N : ℝ) * h = duration)
    (hC3At : ∀ t ∈ Set.Icc x₀ (x₀ + duration), ContDiffAt ℝ 3 ψ t) :
    ∀ n ≤ N,
      D0.Analysis.finiteVectorMidpointHistory h
        (D0.Analysis.sampledVectorMidpointRate ψ x₀ h)
        (D0.Analysis.sampledVectorExactValues ψ x₀ h 0) n =
      twoComponentMatterEuclidean
        (finiteMatterMidpointHistory h
          (sampledMatterMidpointRate (fun t i => ψ t i) x₀ h)
          (sampledMatterExactValues (fun t i => ψ t i) x₀ h 0) n) := by
  intro n hn
  induction n with
  | zero =>
      simp only [D0.Analysis.finiteVectorMidpointHistory,
        finiteMatterMidpointHistory]
      exact euclideanMatter_sampledExact_eq ψ x₀ h 0
  | succ n ih =>
      have hnPrev : n ≤ N := Nat.le_trans (Nat.le_succ n) hn
      have hMid : x₀ + (n : ℝ) * h + h / 2 ∈ Set.Icc x₀ (x₀ + duration) := by
        constructor
        · dsimp
          linarith [mul_nonneg (Nat.cast_nonneg n) h_nonneg,
            div_nonneg h_nonneg (by norm_num : (0 : ℝ) ≤ 2)]
        · rw [← h_duration]
          have hnReal : (n : ℝ) + 1 ≤ (N : ℝ) := by exact_mod_cast hn
          nlinarith [mul_le_mul_of_nonneg_right hnReal h_nonneg]
      have hPrev := ih hnPrev
      simp only [D0.Analysis.finiteVectorMidpointHistory,
        finiteMatterMidpointHistory]
      rw [hPrev]
      rw [euclideanMatter_sampledRate_eq_at ψ x₀ h n (hC3At _ hMid)]
      ext i
      simp [twoComponentMatterEuclidean, finiteMatterMidpointStep]

/--
The vector-norm slack theorem applies to the very same two-component
chronological CAR record already used by the Brinkmann stencil. The Euclidean
lift preserves exact samples, midpoint rates, recurrence states, and the
complement radicand. Its vector derivative and envelope bounds remain supplied
hypotheses; this does not derive them from a CAR preparation or select them
physically.
-/
theorem sampledMatterMidpointCARComplement_positive_of_vectorSlack_on_interval
    (ψ : ℝ → EuclideanSpace ℝ (Fin 2)) (x₀ h M duration A p : ℝ) (N : ℕ)
    (h_nonneg : 0 ≤ h) (M_nonneg : 0 ≤ M) (A_nonneg : 0 ≤ A)
    (h_duration : (N : ℝ) * h = duration)
    (hC3At : ∀ t ∈ Set.Icc x₀ (x₀ + duration), ContDiffAt ℝ 3 ψ t)
    (hThird : ∀ t ∈ Set.Icc x₀ (x₀ + duration),
      ‖iteratedDeriv 3 ψ t‖ ≤ M)
    (hEnvelope : ∀ t ∈ Set.Icc x₀ (x₀ + duration), ‖ψ t‖ ≤ A)
    (hSlack : (A + duration * M * h ^ 2 / 24) ^ 2 < 1 - p) :
    ∀ n ≤ N,
      0 < twoComponentCARComplementAmplitude p
        (finiteMatterMidpointHistory h
          (sampledMatterMidpointRate (fun t i => ψ t i) x₀ h)
          (sampledMatterExactValues (fun t i => ψ t i) x₀ h 0) n) := by
  have hVector := sampledVectorMidpointCARComplement_positive_of_vectorSlack_on_interval
    ψ x₀ h M duration A p N h_nonneg M_nonneg A_nonneg h_duration
    hC3At hThird hEnvelope hSlack
  have hHistoryEq := euclideanMatter_history_eq_on_interval
    ψ x₀ h duration N h_nonneg h_duration hC3At
  intro n hn
  have hLiftPositive := hVector n hn
  rw [hHistoryEq n hn] at hLiftPositive
  simpa [vectorCARComplementAmplitude, twoComponentCARComplementAmplitude,
    twoComponentCARComplementRadicand, twoComponentMatterEuclidean_norm_sq] using
      hLiftPositive

/-- Global smoothness remains a compatibility wrapper for the local CAR proof. -/
theorem sampledMatterMidpointCARComplement_positive_of_vectorSlack
    (ψ : ℝ → EuclideanSpace ℝ (Fin 2)) (x₀ h M duration A p : ℝ) (N : ℕ)
    (h_nonneg : 0 ≤ h) (M_nonneg : 0 ≤ M) (A_nonneg : 0 ≤ A)
    (h_duration : (N : ℝ) * h = duration)
    (hC3 : ContDiff ℝ 3 ψ)
    (hThird : ∀ t ∈ Set.Icc x₀ (x₀ + duration),
      ‖iteratedDeriv 3 ψ t‖ ≤ M)
    (hEnvelope : ∀ t ∈ Set.Icc x₀ (x₀ + duration), ‖ψ t‖ ≤ A)
    (hSlack : (A + duration * M * h ^ 2 / 24) ^ 2 < 1 - p) :
    ∀ n ≤ N,
      0 < twoComponentCARComplementAmplitude p
        (finiteMatterMidpointHistory h
          (sampledMatterMidpointRate (fun t i => ψ t i) x₀ h)
          (sampledMatterExactValues (fun t i => ψ t i) x₀ h 0) n) := by
  exact sampledMatterMidpointCARComplement_positive_of_vectorSlack_on_interval
    ψ x₀ h M duration A p N h_nonneg M_nonneg A_nonneg h_duration
    (fun t _ => hC3.contDiffAt (x := t)) hThird hEnvelope hSlack

/--
The source's half-margin criterion implies the direct vector slack condition
for the same two-component midpoint history. Here `A` bounds the continuum
Euclidean norm and `δ = sqrt (1-p) - A`; the source preparation and these
analytic bounds are still premises rather than derived CAR data.
-/
theorem sampledMatterMidpointCARComplement_positive_of_vectorMargin_on_interval
    (ψ : ℝ → EuclideanSpace ℝ (Fin 2)) (x₀ h M duration A p : ℝ) (N : ℕ)
    (h_nonneg : 0 ≤ h) (M_nonneg : 0 ≤ M) (A_nonneg : 0 ≤ A)
    (h_duration : (N : ℝ) * h = duration)
    (hC3At : ∀ t ∈ Set.Icc x₀ (x₀ + duration), ContDiffAt ℝ 3 ψ t)
    (hThird : ∀ t ∈ Set.Icc x₀ (x₀ + duration),
      ‖iteratedDeriv 3 ψ t‖ ≤ M)
    (hEnvelope : ∀ t ∈ Set.Icc x₀ (x₀ + duration), ‖ψ t‖ ≤ A)
    (hMargin : 0 < Real.sqrt (1 - p) - A)
    (hRefinement : duration * M * h ^ 2 / 24 <
      (Real.sqrt (1 - p) - A) / 2) :
    ∀ n ≤ N,
      0 < twoComponentCARComplementAmplitude p
        (finiteMatterMidpointHistory h
          (sampledMatterMidpointRate (fun t i => ψ t i) x₀ h)
          (sampledMatterExactValues (fun t i => ψ t i) x₀ h 0) n) := by
  have hDuration_nonneg : 0 ≤ duration := by
    rw [← h_duration]
    positivity
  have hError_nonneg : 0 ≤ duration * M * h ^ 2 / 24 := by positivity
  have hRoot_pos : 0 < Real.sqrt (1 - p) := by linarith
  have hRadicand_pos : 0 < 1 - p := Real.sqrt_pos.mp hRoot_pos
  have hSum_lt : A + duration * M * h ^ 2 / 24 < Real.sqrt (1 - p) := by
    linarith
  have hSquare_lt :
      (A + duration * M * h ^ 2 / 24) ^ 2 < 1 - p := by
    have hsquares :=
      (sq_lt_sq₀ (by positivity : 0 ≤ A + duration * M * h ^ 2 / 24)
        (Real.sqrt_nonneg (1 - p))).2 hSum_lt
    rw [Real.sq_sqrt (le_of_lt hRadicand_pos)] at hsquares
    exact hsquares
  exact sampledMatterMidpointCARComplement_positive_of_vectorSlack_on_interval
    ψ x₀ h M duration A p N h_nonneg M_nonneg A_nonneg h_duration
    hC3At hThird hEnvelope hSquare_lt

/-- Global smoothness remains a compatibility wrapper for the local margin proof. -/
theorem sampledMatterMidpointCARComplement_positive_of_vectorMargin
    (ψ : ℝ → EuclideanSpace ℝ (Fin 2)) (x₀ h M duration A p : ℝ) (N : ℕ)
    (h_nonneg : 0 ≤ h) (M_nonneg : 0 ≤ M) (A_nonneg : 0 ≤ A)
    (h_duration : (N : ℝ) * h = duration)
    (hC3 : ContDiff ℝ 3 ψ)
    (hThird : ∀ t ∈ Set.Icc x₀ (x₀ + duration),
      ‖iteratedDeriv 3 ψ t‖ ≤ M)
    (hEnvelope : ∀ t ∈ Set.Icc x₀ (x₀ + duration), ‖ψ t‖ ≤ A)
    (hMargin : 0 < Real.sqrt (1 - p) - A)
    (hRefinement : duration * M * h ^ 2 / 24 <
      (Real.sqrt (1 - p) - A) / 2) :
    ∀ n ≤ N,
      0 < twoComponentCARComplementAmplitude p
        (finiteMatterMidpointHistory h
          (sampledMatterMidpointRate (fun t i => ψ t i) x₀ h)
          (sampledMatterExactValues (fun t i => ψ t i) x₀ h 0) n) := by
  exact sampledMatterMidpointCARComplement_positive_of_vectorMargin_on_interval
    ψ x₀ h M duration A p N h_nonneg M_nonneg A_nonneg h_duration
    (fun t _ => hC3.contDiffAt (x := t)) hThird hEnvelope hMargin hRefinement

/--
The source's fixed CAR slack survives every sufficiently fine uniform mesh.
The threshold is obtained from the explicit `duration * M * h^2 / 24` error
with `h = duration / N`; regularity, derivative, envelope and continuum-margin
hypotheses remain supplied data.
-/
theorem sampledMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes_on_interval
    (ψ : ℝ → EuclideanSpace ℝ (Fin 2)) (x₀ duration M A p : ℝ)
    (duration_pos : 0 < duration) (M_nonneg : 0 ≤ M) (A_nonneg : 0 ≤ A)
    (hC3At : ∀ t ∈ Set.Icc x₀ (x₀ + duration), ContDiffAt ℝ 3 ψ t)
    (hThird : ∀ t ∈ Set.Icc x₀ (x₀ + duration),
      ‖iteratedDeriv 3 ψ t‖ ≤ M)
    (hEnvelope : ∀ t ∈ Set.Icc x₀ (x₀ + duration), ‖ψ t‖ ≤ A)
    (hMargin : 0 < Real.sqrt (1 - p) - A) :
    ∃ N₀ : ℕ, 0 < N₀ ∧ ∀ N : ℕ, N₀ ≤ N →
      ∀ n ≤ N,
        0 < twoComponentCARComplementAmplitude p
          (finiteMatterMidpointHistory (duration / (N : ℝ))
            (sampledMatterMidpointRate (fun t i => ψ t i) x₀
              (duration / (N : ℝ)))
            (sampledMatterExactValues (fun t i => ψ t i) x₀
              (duration / (N : ℝ)) 0) n) := by
  let δ : ℝ := Real.sqrt (1 - p) - A
  let coefficient : ℝ := duration * M * duration ^ 2 / 24
  have hδ_pos : 0 < δ := hMargin
  have hCoefficient_nonneg : 0 ≤ coefficient := by positivity
  have hThreshold_nonneg : 0 ≤ 2 * coefficient / δ := by positivity
  obtain ⟨N₀, hThreshold_lt_N₀⟩ := exists_nat_gt (2 * coefficient / δ)
  have hThreshold_lt_N₀_real : 2 * coefficient / δ < (N₀ : ℝ) :=
    hThreshold_lt_N₀
  have hN₀_pos_real : 0 < (N₀ : ℝ) :=
    lt_of_le_of_lt hThreshold_nonneg hThreshold_lt_N₀_real
  have hN₀_pos : 0 < N₀ := by exact_mod_cast hN₀_pos_real
  refine ⟨N₀, hN₀_pos, ?_⟩
  intro N hN₀N n hn
  have hN_pos : 0 < N := lt_of_lt_of_le hN₀_pos hN₀N
  have hN_real_pos : 0 < (N : ℝ) := by exact_mod_cast hN_pos
  have hN_real_one_le : 1 ≤ (N : ℝ) := by
    exact_mod_cast (Nat.succ_le_of_lt hN_pos)
  have hN₀N_real : (N₀ : ℝ) ≤ (N : ℝ) := by exact_mod_cast hN₀N
  have hThreshold_lt_N : 2 * coefficient / δ < (N : ℝ) :=
    lt_of_lt_of_le hThreshold_lt_N₀_real hN₀N_real
  have hThreshold_mul : 2 * coefficient < (N : ℝ) * δ :=
    (div_lt_iff₀ hδ_pos).mp hThreshold_lt_N
  have hCoefficient_div_N_lt : coefficient / (N : ℝ) < δ / 2 := by
    apply (div_lt_iff₀ hN_real_pos).2
    nlinarith [hThreshold_mul]
  have hN_le_sq : (N : ℝ) ≤ (N : ℝ) ^ 2 := by
    calc
      (N : ℝ) = (N : ℝ) * 1 := by ring
      _ ≤ (N : ℝ) * (N : ℝ) :=
        mul_le_mul_of_nonneg_left hN_real_one_le (Nat.cast_nonneg N)
      _ = (N : ℝ) ^ 2 := by ring
  have hCoefficient_div_sq_le :
      coefficient / (N : ℝ) ^ 2 ≤ coefficient / (N : ℝ) := by
    rw [div_le_div_iff₀ (by positivity : 0 < (N : ℝ) ^ 2) hN_real_pos]
    exact mul_le_mul_of_nonneg_left hN_le_sq hCoefficient_nonneg
  let h : ℝ := duration / (N : ℝ)
  have hError_eq : duration * M * h ^ 2 / 24 = coefficient / (N : ℝ) ^ 2 := by
    dsimp [h, coefficient]
    field_simp [ne_of_gt hN_real_pos]
  have hRefinement : duration * M * h ^ 2 / 24 < δ / 2 := by
    rw [hError_eq]
    exact lt_of_le_of_lt hCoefficient_div_sq_le hCoefficient_div_N_lt
  have hDuration : (N : ℝ) * h = duration := by
    dsimp [h]
    field_simp [ne_of_gt hN_real_pos]
  have hResult := sampledMatterMidpointCARComplement_positive_of_vectorMargin_on_interval
    ψ x₀ h M duration A p N (le_of_lt (by dsimp [h]; positivity))
    M_nonneg A_nonneg hDuration hC3At hThird hEnvelope hMargin hRefinement
  simpa [h, δ] using hResult n hn

/-- Global smoothness remains a compatibility wrapper for the local mesh theorem. -/
theorem sampledMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes
    (ψ : ℝ → EuclideanSpace ℝ (Fin 2)) (x₀ duration M A p : ℝ)
    (duration_pos : 0 < duration) (M_nonneg : 0 ≤ M) (A_nonneg : 0 ≤ A)
    (hC3 : ContDiff ℝ 3 ψ)
    (hThird : ∀ t ∈ Set.Icc x₀ (x₀ + duration),
      ‖iteratedDeriv 3 ψ t‖ ≤ M)
    (hEnvelope : ∀ t ∈ Set.Icc x₀ (x₀ + duration), ‖ψ t‖ ≤ A)
    (hMargin : 0 < Real.sqrt (1 - p) - A) :
    ∃ N₀ : ℕ, 0 < N₀ ∧ ∀ N : ℕ, N₀ ≤ N →
      ∀ n ≤ N,
        0 < twoComponentCARComplementAmplitude p
          (finiteMatterMidpointHistory (duration / (N : ℝ))
            (sampledMatterMidpointRate (fun t i => ψ t i) x₀
              (duration / (N : ℝ)))
            (sampledMatterExactValues (fun t i => ψ t i) x₀
              (duration / (N : ℝ)) 0) n) := by
  exact sampledMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes_on_interval
    ψ x₀ duration M A p duration_pos M_nonneg A_nonneg
    (fun t _ => hC3.contDiffAt (x := t)) hThird hEnvelope hMargin

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


/--
On a compact time interval, a globally C³ matter profile whose value remains
strictly inside the pointwise CAR chart has a uniform amplitude margin and a
uniform third-derivative bound. Consequently the existing midpoint refinement
theorem supplies one natural-mesh threshold after which the same finite CAR
complement is positive at every sampled site. The smooth profile and its
pointwise strict chart inclusion remain hypotheses; compactness does not derive
physical preparation or source selection.
-/
theorem sampledMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes_of_pointwiseMargin
    (ψ : ℝ → EuclideanSpace ℝ (Fin 2)) (x₀ duration p : ℝ)
    (duration_pos : 0 < duration)
    (hC3 : ContDiff ℝ 3 ψ)
    (hPointwiseMargin :
      ∀ t ∈ Set.Icc x₀ (x₀ + duration),
        ‖ψ t‖ < Real.sqrt (1 - p)) :
    ∃ N₀ : ℕ, 0 < N₀ ∧ ∀ N : ℕ, N₀ ≤ N →
      ∀ n ≤ N,
        0 < twoComponentCARComplementAmplitude p
          (finiteMatterMidpointHistory (duration / (N : ℝ))
            (sampledMatterMidpointRate (fun t i => ψ t i) x₀
              (duration / (N : ℝ)))
            (sampledMatterExactValues (fun t i => ψ t i) x₀
              (duration / (N : ℝ)) 0) n) := by
  let interval : Set ℝ := Set.Icc x₀ (x₀ + duration)
  have hleft : x₀ ∈ interval := by
    simp [interval, le_add_of_nonneg_right duration_pos.le]
  have hinterval_nonempty : interval.Nonempty := ⟨x₀, hleft⟩
  have hprofile_norm_continuous : Continuous (fun t => ‖ψ t‖) :=
    hC3.continuous.norm
  obtain ⟨tA, htA, hAmax⟩ :=
    (isCompact_Icc (a := x₀) (b := x₀ + duration)).exists_isMaxOn
      hinterval_nonempty hprofile_norm_continuous.continuousOn
  let A : ℝ := ‖ψ tA‖
  have hA_nonneg : 0 ≤ A := by dsimp [A]; positivity
  have hEnvelope : ∀ t ∈ Set.Icc x₀ (x₀ + duration), ‖ψ t‖ ≤ A := by
    intro t ht
    exact hAmax (by simpa [interval] using ht)
  have hMargin : 0 < Real.sqrt (1 - p) - A := by
    dsimp [A]
    exact sub_pos.mpr (hPointwiseMargin tA (by simpa [interval] using htA))
  have hthird_norm_continuous :
      Continuous (fun t => ‖iteratedDeriv 3 ψ t‖) :=
    (hC3.continuous_iteratedDeriv' 3).norm
  obtain ⟨tM, htM, hMmax⟩ :=
    (isCompact_Icc (a := x₀) (b := x₀ + duration)).exists_isMaxOn
      hinterval_nonempty hthird_norm_continuous.continuousOn
  let M : ℝ := ‖iteratedDeriv 3 ψ tM‖
  have hM_nonneg : 0 ≤ M := by dsimp [M]; positivity
  have hThird : ∀ t ∈ Set.Icc x₀ (x₀ + duration),
      ‖iteratedDeriv 3 ψ t‖ ≤ M := by
    intro t ht
    exact hMmax (by simpa [interval] using ht)
  exact sampledMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes_on_interval
    ψ x₀ duration M A p duration_pos hM_nonneg hA_nonneg
    (fun t _ => hC3.contDiffAt (x := t)) hThird hEnvelope hMargin

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

/-- The Euclidean lift of the same cubic matter profile used by the finite source. -/
noncomputable def cubicMatterEuclideanProfile
    (c0 c1 c2 c3 : Fin 2 → ℝ) (t : ℝ) : EuclideanSpace ℝ (Fin 2) :=
  twoComponentMatterEuclidean c0 +
    t • twoComponentMatterEuclidean c1 +
    t ^ 2 • twoComponentMatterEuclidean c2 +
    t ^ 3 • twoComponentMatterEuclidean c3

@[simp]
theorem cubicMatterEuclideanProfile_apply
    (c0 c1 c2 c3 : Fin 2 → ℝ) (t : ℝ) (i : Fin 2) :
    cubicMatterEuclideanProfile c0 c1 c2 c3 t i =
      cubicMatterProfile c0 c1 c2 c3 t i := by
  simp [cubicMatterEuclideanProfile, cubicMatterProfile,
    twoComponentMatterEuclidean_apply]
  ring

/-- The coefficient norm controls this cubic profile on the unit time interval. -/
noncomputable def cubicMatterCoefficientNorm (c0 c1 c2 c3 : Fin 2 → ℝ) : ℝ :=
  ‖twoComponentMatterEuclidean c0‖ +
    ‖twoComponentMatterEuclidean c1‖ +
    ‖twoComponentMatterEuclidean c2‖ +
    ‖twoComponentMatterEuclidean c3‖

/-- The analytic derivative of the cubic profile is its declared midpoint rate. -/
theorem cubicMatterProfile_hasDerivAt
    (c0 c1 c2 c3 : Fin 2 → ℝ) (t : ℝ) (i : Fin 2) :
    HasDerivAt (fun s : ℝ => cubicMatterProfile c0 c1 c2 c3 s i)
      (cubicMatterMidpointRate c1 c2 c3 t i) t := by
  have hid : HasDerivAt (fun s : ℝ => s) 1 t := hasDerivAt_id t
  have h1 : HasDerivAt (fun s : ℝ => c1 i * s) (c1 i) t := by
    simpa using hid.const_mul (c1 i)
  have h2pow : HasDerivAt (fun s : ℝ => s ^ 2) (2 * t) t := by
    simpa using hid.pow 2
  have h2 : HasDerivAt (fun s : ℝ => c2 i * s ^ 2) (c2 i * (2 * t)) t := by
    simpa using h2pow.const_mul (c2 i)
  have h3pow : HasDerivAt (fun s : ℝ => s ^ 3) (3 * t ^ 2) t := by
    simpa using hid.pow 3
  have h3 : HasDerivAt (fun s : ℝ => c3 i * s ^ 3) (c3 i * (3 * t ^ 2)) t := by
    simpa using h3pow.const_mul (c3 i)
  have h0 : HasDerivAt (fun s : ℝ => c0 i) 0 t := hasDerivAt_const t (c0 i)
  have hsum := ((h0.add h1).add h2).add h3
  convert hsum using 1
  simp [cubicMatterMidpointRate]
  ring

/-- Sampling the Euclidean lift differentiates to the same cubic matter rate. -/
theorem cubicMatterEuclideanProfile_sampledRate_eq
    (c0 c1 c2 c3 : Fin 2 → ℝ) (h : ℝ) (n : ℕ) :
    sampledMatterMidpointRate
      (fun t i => cubicMatterEuclideanProfile c0 c1 c2 c3 t i) 0 h n =
        cubicMatterMidpointRate c1 c2 c3 (((n : ℝ) + 1 / 2) * h) := by
  funext i
  simp only [sampledMatterMidpointRate, cubicMatterEuclideanProfile_apply]
  have hMidpoint : 0 + (n : ℝ) * h + h / 2 = ((n : ℝ) + 1 / 2) * h := by ring
  rw [hMidpoint]
  exact (cubicMatterProfile_hasDerivAt c0 c1 c2 c3 _ i).deriv

/--
The Euclidean-lift midpoint history is exactly the recursively defined cubic
matter record used by the nonvacuum stencil source theorem.
-/
theorem cubicMatterMidpointSample_eq_sampledHistory
    (h : ℝ) (c0 c1 c2 c3 : Fin 2 → ℝ) (n : ℕ) :
    cubicMatterMidpointSample h c0 c1 c2 c3 n =
      finiteMatterMidpointHistory h
        (sampledMatterMidpointRate
          (fun t i => cubicMatterEuclideanProfile c0 c1 c2 c3 t i) 0 h)
        (sampledMatterExactValues
          (fun t i => cubicMatterEuclideanProfile c0 c1 c2 c3 t i) 0 h 0) n := by
  induction n with
  | zero =>
      funext i
      simp [cubicMatterMidpointSample, finiteMatterMidpointHistory,
        sampledMatterExactValues, cubicMatterEuclideanProfile_apply,
        cubicMatterProfile]
  | succ n ih =>
      have hRate := cubicMatterEuclideanProfile_sampledRate_eq c0 c1 c2 c3 h n
      simp only [cubicMatterMidpointSample, finiteMatterMidpointHistory]
      rw [ih, hRate]

/--
The Euclidean error of the same recursive cubic midpoint record is exactly
the signed cubic remainder applied to its coefficient vector. This connects
the coordinate identity to the normed source space used by the vector
refinement theorem without replacing the finite record by an independent
sample.
-/
theorem cubicMatterMidpointSample_euclideanError_eq_remainder
    (h : ℝ) (c0 c1 c2 c3 : Fin 2 → ℝ) (n : ℕ) :
    twoComponentMatterEuclidean (cubicMatterMidpointSample h c0 c1 c2 c3 n) -
      cubicMatterEuclideanProfile c0 c1 c2 c3 ((n : ℝ) * h) =
        -((n : ℝ) * h ^ 3 / 4) • twoComponentMatterEuclidean c3 := by
  ext i
  simp only [PiLp.sub_apply, PiLp.smul_apply, twoComponentMatterEuclidean_apply,
    cubicMatterEuclideanProfile_apply]
  rw [cubicMatterMidpointSample_error_eq]
  ring

/--
The same-record Euclidean cubic error obeys the dimension-free midpoint
refinement bound with its exact cubic coefficient. It follows from the signed
remainder identity and introduces no component-count factor.
-/
theorem cubicMatterMidpointSample_euclideanError_le_refinementBound
    (h : ℝ) (c0 c1 c2 c3 : Fin 2 → ℝ) (N n : ℕ) (duration : ℝ)
    (hn : n ≤ N) (h_nonneg : 0 ≤ h)
    (h_duration : (N : ℝ) * h = duration) :
    ‖twoComponentMatterEuclidean (cubicMatterMidpointSample h c0 c1 c2 c3 n) -
      cubicMatterEuclideanProfile c0 c1 c2 c3 ((n : ℝ) * h)‖ ≤
        duration * (6 * ‖twoComponentMatterEuclidean c3‖) * h ^ 2 / 24 := by
  rw [cubicMatterMidpointSample_euclideanError_eq_remainder]
  rw [norm_smul]
  simp only [Real.norm_eq_abs, abs_neg]
  have hAbs : |(n : ℝ) * h ^ 3 / 4| = (n : ℝ) * h ^ 3 / 4 :=
    abs_of_nonneg (by positivity)
  rw [hAbs]
  have hnCast : (n : ℝ) ≤ (N : ℝ) := Nat.cast_le.mpr hn
  have hnH : (n : ℝ) * h ≤ (N : ℝ) * h :=
    mul_le_mul_of_nonneg_right hnCast h_nonneg
  let q : ℝ := (n : ℝ) * h * h ^ 2 / 24
  let Q : ℝ := (N : ℝ) * h * h ^ 2 / 24
  have hq_nonneg : 0 ≤ q := by
    dsimp [q]
    positivity
  have hq_le_Q : q ≤ Q := by
    dsimp [q, Q]
    rw [div_le_div_iff_of_pos_right (by norm_num : (0 : ℝ) < 24)]
    nlinarith [mul_le_mul_of_nonneg_right hnH (sq_nonneg h)]
  calc
    ((n : ℝ) * h ^ 3 / 4) * ‖twoComponentMatterEuclidean c3‖ =
        q * (6 * ‖twoComponentMatterEuclidean c3‖) := by
          dsimp [q]
          ring
    _ ≤ Q * (6 * ‖twoComponentMatterEuclidean c3‖) :=
          mul_le_mul_of_nonneg_right hq_le_Q (by positivity)
    _ = duration * (6 * ‖twoComponentMatterEuclidean c3‖) * h ^ 2 / 24 := by
          dsimp [Q]
          rw [← h_duration]
          ring

theorem cubicMatterEuclideanProfile_norm_le_coefficientNorm
    (c0 c1 c2 c3 : Fin 2 → ℝ) (t : ℝ)
    (ht : t ∈ Set.Icc (0 : ℝ) 1) :
    ‖cubicMatterEuclideanProfile c0 c1 c2 c3 t‖ ≤
      cubicMatterCoefficientNorm c0 c1 c2 c3 := by
  rcases ht with ⟨ht0, htOne⟩
  have ht1 : ‖t‖ ≤ 1 := by
    simpa [Real.norm_eq_abs, abs_of_nonneg ht0] using htOne
  have hOneSubNonneg : 0 ≤ 1 - t := sub_nonneg.mpr htOne
  have hOneAddNonneg : 0 ≤ 1 + t := add_nonneg (by norm_num) ht0
  have ht2_nonneg : 0 ≤ t ^ 2 := sq_nonneg t
  have ht2_le : t ^ 2 ≤ 1 := by
    nlinarith [mul_nonneg hOneSubNonneg hOneAddNonneg]
  have ht2 : ‖t ^ 2‖ ≤ 1 := by
    simpa [Real.norm_eq_abs, abs_of_nonneg ht2_nonneg] using ht2_le
  have ht3_nonneg : 0 ≤ t ^ 3 := by positivity
  have ht3_le : t ^ 3 ≤ 1 := by
    have hFactorNonneg : 0 ≤ 1 + t + t ^ 2 := by positivity
    nlinarith [mul_nonneg hOneSubNonneg hFactorNonneg]
  have ht3 : ‖t ^ 3‖ ≤ 1 := by
    rw [Real.norm_eq_abs, abs_of_nonneg ht3_nonneg]
    exact ht3_le
  let v0 := twoComponentMatterEuclidean c0
  let v1 := twoComponentMatterEuclidean c1
  let v2 := twoComponentMatterEuclidean c2
  let v3 := twoComponentMatterEuclidean c3
  have h1 : ‖t • v1‖ ≤ ‖v1‖ := by
    calc
      ‖t • v1‖ = ‖t‖ * ‖v1‖ := norm_smul _ _
      _ ≤ 1 * ‖v1‖ := mul_le_mul_of_nonneg_right ht1 (norm_nonneg v1)
      _ = ‖v1‖ := by ring
  have h2 : ‖t ^ 2 • v2‖ ≤ ‖v2‖ := by
    calc
      ‖t ^ 2 • v2‖ = ‖t ^ 2‖ * ‖v2‖ := norm_smul _ _
      _ ≤ 1 * ‖v2‖ := mul_le_mul_of_nonneg_right ht2 (norm_nonneg v2)
      _ = ‖v2‖ := by ring
  have h3 : ‖t ^ 3 • v3‖ ≤ ‖v3‖ := by
    calc
      ‖t ^ 3 • v3‖ = ‖t ^ 3‖ * ‖v3‖ := norm_smul _ _
      _ ≤ 1 * ‖v3‖ := mul_le_mul_of_nonneg_right ht3 (norm_nonneg v3)
      _ = ‖v3‖ := by ring
  have h01 : ‖v0 + t • v1‖ ≤ ‖v0‖ + ‖v1‖ := by
    exact le_trans (norm_add_le _ _) (add_le_add le_rfl h1)
  have h012 : ‖v0 + t • v1 + t ^ 2 • v2‖ ≤
      (‖v0‖ + ‖v1‖) + ‖v2‖ := by
    exact le_trans (norm_add_le _ _) (add_le_add h01 h2)
  change ‖v0 + t • v1 + t ^ 2 • v2 + t ^ 3 • v3‖ ≤ _
  dsimp [cubicMatterCoefficientNorm, v0, v1, v2, v3]
  calc
    ‖v0 + t • v1 + t ^ 2 • v2 + t ^ 3 • v3‖ ≤
        ‖v0 + t • v1 + t ^ 2 • v2‖ + ‖t ^ 3 • v3‖ := norm_add_le _ _
    _ ≤ (‖v0‖ + ‖v1‖ + ‖v2‖) + ‖v3‖ := by
      exact add_le_add h012 h3

/--
Every cubic two-component profile with a small coefficient norm stays inside
the pointwise CAR chart on `[0,1]`. If its initial derivative is nonzero,
the compactness theorem therefore gives one positive-complement threshold for
the same midpoint history and a genuinely nonzero matter rate. This remains
conditional on the stated coefficient margin and CAR parameter; it selects no
physical preparation or execution.
-/
theorem sampledCubicMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes
    (c0 c1 c2 c3 : Fin 2 → ℝ) (p : ℝ)
    (hCoefficientMargin : cubicMatterCoefficientNorm c0 c1 c2 c3 <
      Real.sqrt (1 - p)) (hNonzeroRate : c1 ≠ 0) :
    cubicMatterMidpointRate c1 c2 c3 0 ≠ 0 ∧
      ∃ N₀ : ℕ, 0 < N₀ ∧ ∀ N : ℕ, N₀ ≤ N → ∀ n ≤ N,
        0 < twoComponentCARComplementAmplitude p
          (cubicMatterMidpointSample (1 / (N : ℝ)) c0 c1 c2 c3 n) := by
  let ψ : ℝ → EuclideanSpace ℝ (Fin 2) :=
    cubicMatterEuclideanProfile c0 c1 c2 c3
  have hC3 : ContDiff ℝ 3 ψ := by
    change ContDiff ℝ 3 (fun t =>
      twoComponentMatterEuclidean c0 +
        t • twoComponentMatterEuclidean c1 +
        t ^ 2 • twoComponentMatterEuclidean c2 +
        t ^ 3 • twoComponentMatterEuclidean c3)
    fun_prop
  have hPointwiseMargin : ∀ t ∈ Set.Icc (0 : ℝ) 1,
      ‖ψ t‖ < Real.sqrt (1 - p) := by
    intro t ht
    exact lt_of_le_of_lt
      (cubicMatterEuclideanProfile_norm_le_coefficientNorm c0 c1 c2 c3 t ht)
      hCoefficientMargin
  have hThreshold :=
    sampledMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes_of_pointwiseMargin
      ψ 0 1 p (by norm_num) hC3 (by simpa using hPointwiseMargin)
  have hInitialRate : cubicMatterMidpointRate c1 c2 c3 0 = c1 := by
    funext i
    simp [cubicMatterMidpointRate]
  constructor
  · rw [hInitialRate]
    exact hNonzeroRate
  · obtain ⟨N₀, hN₀, hPositive⟩ := hThreshold
    refine ⟨N₀, hN₀, ?_⟩
    intro N hN n hn
    rw [cubicMatterMidpointSample_eq_sampledHistory
      (1 / (N : ℝ)) c0 c1 c2 c3 n]
    exact hPositive N hN n hn

/--
The cubic matter realization has both a positive CAR complement and the exact
five-point stencil source on the same recursively constructed record at every
sufficiently fine mesh. This composes the source adapter with the CAR bound;
it does not assert physical admission or select the cubic profile.
-/
theorem nonvacuumCubicCARComplement_positive_with_sameRecordStencilSource
    (coupling p x y : ℝ) (a2 b2 a3 b3 : ℝ → ℝ)
    (c0 c1 c2 c3 : Fin 2 → ℝ)
    (hCoefficientMargin : cubicMatterCoefficientNorm c0 c1 c2 c3 <
      Real.sqrt (1 - p)) (hNonzeroRate : c1 ≠ 0) :
    cubicMatterMidpointRate c1 c2 c3 0 ≠ 0 ∧
      ∃ N₀ : ℕ, 0 < N₀ ∧ ∀ N : ℕ, N₀ ≤ N → ∀ n ≤ N,
        0 < twoComponentCARComplementAmplitude p
          (cubicMatterMidpointSample (1 / (N : ℝ)) c0 c1 c2 c3 n) ∧
        transverseFivePointLaplacian (1 / (N : ℝ))
          (fun x y => nonvacuumBrinkmannProfile coupling
            (twoComponentMatterNormSq
              (cubicMatterMidpointRate c1 c2 c3
                (((n : ℝ) + 1 / 2) * (1 / (N : ℝ)))))
            (a2 (((n : ℝ) + 1 / 2) * (1 / (N : ℝ))))
            (b2 (((n : ℝ) + 1 / 2) * (1 / (N : ℝ))))
            (a3 (((n : ℝ) + 1 / 2) * (1 / (N : ℝ))))
            (b3 (((n : ℝ) + 1 / 2) * (1 / (N : ℝ)))) x y) x y =
          -4 * coupling * twoComponentMatterNormSq
            (finiteMatterForwardGradient (1 / (N : ℝ))
              (cubicMatterMidpointSample (1 / (N : ℝ)) c0 c1 c2 c3 n)
              (cubicMatterMidpointSample (1 / (N : ℝ)) c0 c1 c2 c3 (n + 1))) := by
  obtain ⟨hInitialRate, N₀, hN₀, hCAR⟩ :=
    sampledCubicMatterMidpointCARComplement_positive_for_all_sufficiently_fine_meshes
      c0 c1 c2 c3 p hCoefficientMargin hNonzeroRate
  refine ⟨hInitialRate, N₀, hN₀, ?_⟩
  intro N hN n hn
  refine ⟨hCAR N hN n hn, ?_⟩
  have hNpos : 0 < N := lt_of_lt_of_le hN₀ hN
  have hNcast : (N : ℝ) ≠ 0 := by exact_mod_cast hNpos.ne'
  have hMesh : (1 / (N : ℝ)) ≠ 0 := div_ne_zero (by norm_num) hNcast
  exact nonvacuumCubicMidpointSource_matches_record
    (1 / (N : ℝ)) coupling x y a2 b2 a3 b3 c0 c1 c2 c3 n hMesh

/--
The cubic application also carries its dimension-free Euclidean refinement
error on the very same recursive record used by the CAR complement and exact
stencil source. This adds analytic recovery to that finite composition while
leaving physical admission and source selection open.
-/
theorem nonvacuumCubicCARComplement_positive_with_sameRecordStencilSource_and_refinement
    (coupling p x y : ℝ) (a2 b2 a3 b3 : ℝ → ℝ)
    (c0 c1 c2 c3 : Fin 2 → ℝ)
    (hCoefficientMargin : cubicMatterCoefficientNorm c0 c1 c2 c3 <
      Real.sqrt (1 - p)) (hNonzeroRate : c1 ≠ 0) :
    cubicMatterMidpointRate c1 c2 c3 0 ≠ 0 ∧
      ∃ N₀ : ℕ, 0 < N₀ ∧ ∀ N : ℕ, N₀ ≤ N → ∀ n ≤ N,
        0 < twoComponentCARComplementAmplitude p
          (cubicMatterMidpointSample (1 / (N : ℝ)) c0 c1 c2 c3 n) ∧
        transverseFivePointLaplacian (1 / (N : ℝ))
          (fun x y => nonvacuumBrinkmannProfile coupling
            (twoComponentMatterNormSq
              (cubicMatterMidpointRate c1 c2 c3
                (((n : ℝ) + 1 / 2) * (1 / (N : ℝ)))))
            (a2 (((n : ℝ) + 1 / 2) * (1 / (N : ℝ))))
            (b2 (((n : ℝ) + 1 / 2) * (1 / (N : ℝ))))
            (a3 (((n : ℝ) + 1 / 2) * (1 / (N : ℝ))))
            (b3 (((n : ℝ) + 1 / 2) * (1 / (N : ℝ)))) x y) x y =
          -4 * coupling * twoComponentMatterNormSq
            (finiteMatterForwardGradient (1 / (N : ℝ))
              (cubicMatterMidpointSample (1 / (N : ℝ)) c0 c1 c2 c3 n)
              (cubicMatterMidpointSample (1 / (N : ℝ)) c0 c1 c2 c3 (n + 1))) ∧
        ‖twoComponentMatterEuclidean
            (cubicMatterMidpointSample (1 / (N : ℝ)) c0 c1 c2 c3 n) -
          cubicMatterEuclideanProfile c0 c1 c2 c3
            ((n : ℝ) * (1 / (N : ℝ)))‖ ≤
          1 * (6 * ‖twoComponentMatterEuclidean c3‖) *
            (1 / (N : ℝ)) ^ 2 / 24 := by
  obtain ⟨hInitialRate, N₀, hN₀, hSameRecord⟩ :=
    nonvacuumCubicCARComplement_positive_with_sameRecordStencilSource
      coupling p x y a2 b2 a3 b3 c0 c1 c2 c3
      hCoefficientMargin hNonzeroRate
  refine ⟨hInitialRate, N₀, hN₀, ?_⟩
  intro N hN n hn
  obtain ⟨hCAR, hSource⟩ := hSameRecord N hN n hn
  have hNpos : 0 < N := lt_of_lt_of_le hN₀ hN
  have hNcast : (N : ℝ) ≠ 0 := by exact_mod_cast hNpos.ne'
  have hDuration : (N : ℝ) * (1 / (N : ℝ)) = 1 := by
    field_simp [hNcast]
  have hRefinement := cubicMatterMidpointSample_euclideanError_le_refinementBound
    (1 / (N : ℝ)) c0 c1 c2 c3 N n 1 hn (by positivity) hDuration
  exact ⟨hCAR, hSource, by simpa using hRefinement⟩

end D0.Geometry
