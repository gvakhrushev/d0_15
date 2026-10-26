import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
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
energy used by that readout.

This is an exact finite algebraic application. It does not formalize the
original CAR construction, the 40 varied Cartan equations, all 16+24+2
Euler rows, refinement error bounds, or selection of a physical Book,
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
