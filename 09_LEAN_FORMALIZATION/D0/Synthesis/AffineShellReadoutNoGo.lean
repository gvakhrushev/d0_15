import D0.Synthesis.MassSectorMetricUnderdetermination
import D0.Matter.LeptonGreenPuiseuxOwner

/-!
# Affine shell readout is equally spaced: the mass transfer must be nonlinear

T38 proved that the residual shell metric is one positive modulus `g`, with radii `(1,1+g,1+2g)`.
The remaining physical content is the *transfer* from a shell radius to a mass-sector observable.
This module rules out the simplest possible transfer — an affine (linear) readout
`m(s) = α + β · radius(s)` — as a source of the observed hierarchy, and does so without importing
any PDG number.

Key facts, all independent of the free modulus `g` and of the affine coefficients `α, β`:

* an affine readout of the three shells is always **equally spaced**
  (`(m_core − m_inner) = (m_outer − m_core)`), i.e. its discrete second difference vanishes;
* equivalently the normalized invariant `(m_outer − m_inner)/(m_core − m_inner) = 2` whenever the
  readout is non-constant;
* therefore any target triple whose spacing is unequal is **not** affine-reachable for any
  `(g, α, β)`.

Concrete internal instance: the owned charged-lepton Puiseux exponent row `(0, 1/4, 1/3)` is not
equally spaced (`1/4 ≠ 1/12`), hence it is not an affine shell readout. The transfer that produces
the generation ladder is genuinely nonlinear — consistent with the Green-function / Puiseux route,
not with a linear shell map.
-/

namespace D0.Synthesis.AffineShellReadoutNoGo

open D0.Geometry
open D0.Matter
open D0.Synthesis.MassSectorMetricUnderdetermination

/-- Affine (linear) readout of a shell radius into a mass-sector observable. -/
def affineReadout (T : TorusParameter) (α β : ℚ) (s : TorusShell) : ℚ :=
  α + β * TorusShell.radius T s

@[simp] theorem affineReadout_inner (T : TorusParameter) (α β : ℚ) :
    affineReadout T α β .innerD9 = α + β := by
  simp [affineReadout, torusShell_inner_unit]

@[simp] theorem affineReadout_core (T : TorusParameter) (α β : ℚ) :
    affineReadout T α β .coreD11 = α + β * (1 + shellGap T) := by
  simp [affineReadout, core_radius_eq_one_add_gap]

@[simp] theorem affineReadout_outer (T : TorusParameter) (α β : ℚ) :
    affineReadout T α β .outerD13 = α + β * (1 + 2 * shellGap T) := by
  simp [affineReadout, outer_radius_eq_one_add_two_gap]

/-- Both adjacent readout gaps equal `β · g`: the affine readout is equally spaced,
for every torus parameter and every pair of coefficients. -/
theorem affineReadout_equally_spaced (T : TorusParameter) (α β : ℚ) :
    affineReadout T α β .coreD11 - affineReadout T α β .innerD9
      = affineReadout T α β .outerD13 - affineReadout T α β .coreD11 := by
  simp only [affineReadout_inner, affineReadout_core, affineReadout_outer]
  ring

/-- The discrete second difference of an affine shell readout is identically zero. -/
theorem affineReadout_second_difference_zero (T : TorusParameter) (α β : ℚ) :
    (affineReadout T α β .outerD13 - affineReadout T α β .coreD11)
      - (affineReadout T α β .coreD11 - affineReadout T α β .innerD9) = 0 := by
  have := affineReadout_equally_spaced T α β
  linarith

/-- Each adjacent readout gap is exactly `β · g`. -/
theorem affineReadout_gap (T : TorusParameter) (α β : ℚ) :
    affineReadout T α β .coreD11 - affineReadout T α β .innerD9 = β * shellGap T := by
  simp only [affineReadout_inner, affineReadout_core]
  ring

/-- **Gap-independent normalized invariant.** For any affine readout the total span is exactly
twice the first gap, independent of the free modulus `g` and of `α, β`. When the readout is
non-constant (`β ≠ 0`, so the first gap is nonzero) this is the ratio invariant `= 2`. -/
theorem affineReadout_normalized_ratio (T : TorusParameter) (α β : ℚ) :
    (affineReadout T α β .outerD13 - affineReadout T α β .innerD9)
      = 2 * (affineReadout T α β .coreD11 - affineReadout T α β .innerD9) := by
  simp only [affineReadout_inner, affineReadout_core, affineReadout_outer]
  ring

/-- Any triple realized by an affine shell readout is equally spaced. -/
theorem affineReadout_target_equally_spaced
    (T : TorusParameter) (α β m0 m1 m2 : ℚ)
    (h0 : affineReadout T α β .innerD9 = m0)
    (h1 : affineReadout T α β .coreD11 = m1)
    (h2 : affineReadout T α β .outerD13 = m2) :
    m1 - m0 = m2 - m1 := by
  have h := affineReadout_equally_spaced T α β
  rw [h0, h1, h2] at h
  exact h

/-- Predicate: a target triple is realized by some affine shell readout. -/
def AffineReachable (m0 m1 m2 : ℚ) : Prop :=
  ∃ (T : TorusParameter) (α β : ℚ),
    affineReadout T α β .innerD9 = m0 ∧
    affineReadout T α β .coreD11 = m1 ∧
    affineReadout T α β .outerD13 = m2

/-- **Affine readout no-go.** Any unequally spaced target spectrum is unreachable by every affine
shell readout, for every admissible torus parameter. The mass transfer must therefore be
nonlinear in the shell radius. -/
theorem unequal_spacing_not_affine_reachable (m0 m1 m2 : ℚ)
    (h : m1 - m0 ≠ m2 - m1) :
    ¬ AffineReachable m0 m1 m2 := by
  rintro ⟨T, α, β, h0, h1, h2⟩
  exact h (affineReadout_target_equally_spaced T α β m0 m1 m2 h0 h1 h2)

/-- The owned charged-lepton Puiseux exponent row `(0, 1/4, 1/3)` is not equally spaced. -/
theorem puiseux_row_not_equally_spaced :
    (p_mu - p_e) ≠ (p_tau - p_mu) := by
  norm_num [p_e, p_mu, p_tau]

/-- **Concrete instance without PDG input.** The owned Puiseux exponent ladder `(0,1/4,1/3)` is
not an affine shell readout; the exponent transfer is genuinely nonlinear in the shell radius. -/
theorem puiseux_row_not_affine_reachable :
    ¬ AffineReachable p_e p_mu p_tau :=
  unequal_spacing_not_affine_reachable p_e p_mu p_tau puiseux_row_not_equally_spaced

/-- Capstone: affine shell readout has a gap-independent equal-spacing invariant, so the physical
mass/exponent transfer must be nonlinear; the owned Puiseux row is an explicit witness. -/
theorem affine_shell_readout_boundary :
    (∀ (T : TorusParameter) (α β : ℚ),
        affineReadout T α β .coreD11 - affineReadout T α β .innerD9
          = affineReadout T α β .outerD13 - affineReadout T α β .coreD11)
    ∧ (∀ (T : TorusParameter) (α β : ℚ),
        (affineReadout T α β .outerD13 - affineReadout T α β .innerD9)
          = 2 * (affineReadout T α β .coreD11 - affineReadout T α β .innerD9))
    ∧ (∀ m0 m1 m2 : ℚ, m1 - m0 ≠ m2 - m1 → ¬ AffineReachable m0 m1 m2)
    ∧ ¬ AffineReachable p_e p_mu p_tau :=
  ⟨affineReadout_equally_spaced, affineReadout_normalized_ratio,
    unequal_spacing_not_affine_reachable, puiseux_row_not_affine_reachable⟩

end D0.Synthesis.AffineShellReadoutNoGo
