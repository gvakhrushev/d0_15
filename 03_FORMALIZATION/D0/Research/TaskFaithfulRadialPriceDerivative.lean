import D0.Analysis.ReturnPriceLogScaleDerivative
import D0.Analysis.GramMatrixOrder

/-!
# Task-faithful return price: one radial scalar corner

Source: #334 owner commit `fd35893d77e4aa5f819bafa0c6428c8e7a8f1812`,
`02_REGISTRY/research/sources/d0_task_faithful_source_2026-10-28/PROOF_RU.md`,
blob `c99e90a8c8e96bae70e700fa88d1c2d824a1831b`, §4 and §5.

One positive, differentiable scalar corner changes while the retained history
and the other scalar corners stay fixed. This is a chain-rule application of
the fixed-history log-scale theorem. In particular it does not infer that an
arbitrary reporter variation is radial, or that any such family is physically
admitted. Preparation, independent heat, clock and work remain separate.
-/

noncomputable section

namespace D0.Research

open Filter D0.Analysis D0.Analysis.ReturnPriceLogScaleDerivative
open scoped ComplexOrder Topology

/-- A differentiable positive scalar amplitude changes the price with the
gain of the same PSD reference. The reference may be singular or zero. -/
theorem regularizedReturnPrice_hasDerivAt_scalarCorner
    {n : Type*} [Fintype n] [DecidableEq n]
    (S : Matrix n n ℂ) (hS : S.PosSemidef) (a x : ℝ) (ha : 0 < a)
    (c : ℝ → ℝ) (dc : ℝ) (hc : 0 < c x) (hc' : HasDerivAt c dc x) :
    HasDerivAt (fun y => regularizedReturnPrice a (((c y ^ 2 : ℝ) : ℂ) • S))
      (-(2 * dc / c x) * regularizedReturnGain a (((c x ^ 2 : ℝ) : ℂ) • S)) x := by
  have hlog := (hc'.log (ne_of_gt hc)).const_mul 2
  have houter := regularizedReturnPrice_hasDerivAt_logScale S hS a
    (2 * Real.log (c x)) ha
  have h := houter.comp x hlog
  have hpos : ∀ᶠ y in 𝓝 x, 0 < c y :=
    hc'.continuousAt.eventually (eventually_gt_nhds hc)
  have heq : (fun y => regularizedReturnPrice a (((c y ^ 2 : ℝ) : ℂ) • S)) =ᶠ[𝓝 x]
      (fun y => regularizedReturnPrice a ((Real.exp (2 * Real.log (c y)) : ℂ) • S)) := by
    filter_upwards [hpos] with y hy
    have hexp : Real.exp (2 * Real.log (c y)) = c y ^ 2 := by
      rw [show 2 * Real.log (c y) = Real.log (c y) + Real.log (c y) by ring,
        Real.exp_add, Real.exp_log hy]
      ring
    rw [hexp]
  have h' := h.congr_of_eventuallyEq heq
  have hexp : Real.exp (2 * Real.log (c x)) = c x ^ 2 := by
    rw [show 2 * Real.log (c x) = Real.log (c x) + Real.log (c x) by ring,
      Real.exp_add, Real.exp_log hc]
    ring
  rw [hexp] at h'
  convert h' using 1 <;> ring

/-- Concrete retained-history consumer: `S` is the same scaled Gram matrix
used in `taskReturnProduct_price_bound`. `other` is the fixed product of the
other scalar corners. No inverse of the history is assumed. -/
theorem taskReturnGramPrice_hasDerivAt_scalarCorner
    {V X : Type*} [NormedAddCommGroup V] [InnerProductSpace ℂ V] [FiniteDimensional ℂ V]
    [NormedAddCommGroup X] [InnerProductSpace ℂ X] [FiniteDimensional ℂ X]
    {n : Type*} [Fintype n] [DecidableEq n]
    (K : V →L[ℂ] X) (b : OrthonormalBasis n ℂ V)
    (z other x : ℝ) (hz : 0 ≤ z) (hzOne : z < 1)
    (c : ℝ → ℝ) (dc : ℝ) (hc : 0 < c x) (hc' : HasDerivAt c dc x) :
    let S : Matrix n n ℂ := ((z * other ^ 2 : ℝ) : ℂ) • gramMatrix K.toLinearMap b
    HasDerivAt (fun y => regularizedReturnPrice (1 - z) (((c y ^ 2 : ℝ) : ℂ) • S))
      (-(2 * dc / c x) * regularizedReturnGain (1 - z) (((c x ^ 2 : ℝ) : ℂ) • S)) x := by
  let S : Matrix n n ℂ := ((z * other ^ 2 : ℝ) : ℂ) • gramMatrix K.toLinearMap b
  have hS : S.PosSemidef :=
    (gramMatrix_posSemidef K.toLinearMap b).smul
      (Complex.zero_le_real.mpr (mul_nonneg hz (sq_nonneg other)))
  exact regularizedReturnPrice_hasDerivAt_scalarCorner S hS (1 - z) x
    (sub_pos.mpr hzOne) c dc hc hc'

end D0.Research
