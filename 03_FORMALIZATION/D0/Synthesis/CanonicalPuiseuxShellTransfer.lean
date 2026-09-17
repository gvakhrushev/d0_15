import D0.Synthesis.AffineShellReadoutNoGo

/-!
# Canonical Puiseux shell transfer: the unique minimal quadratic shape

T40 proved a lower bound: no affine function of the shell radius can produce the owned
charged-lepton Puiseux row `(0, 1/4, 1/3)`. This module supplies the matching upper bound and
classifies it uniquely.

Normalize the affine shell metric `(1, 1+g, 1+2g)` by

`u(s) = (radius(s) - 1) / g`.

For every admissible torus parameter this sends `inner/core/outer` to `0/1/2`. On that intrinsic
coordinate, the unique quadratic polynomial matching the owned exponent row is

`P(u) = u/3 - u²/12`.

Its quadratic coefficient is exactly `-1/12`, so the transfer is strictly concave. Since T40
excludes degree at most one and this module constructs degree two, the minimal polynomial degree
of a shell-coordinate transfer realizing the Puiseux row is exactly two.

This is an interpolation/shape theorem, not yet the missing Green resolvent or the EFT/IR mass
map. It identifies the unique minimal transfer that those constructions must reproduce on the
three owned shell points.
-/

namespace D0.Synthesis.CanonicalPuiseuxShellTransfer

open D0.Geometry
open D0.Matter
open D0.Synthesis.MassSectorMetricUnderdetermination
open D0.Synthesis.AffineShellReadoutNoGo

/-- Intrinsic shell coordinate: unit inner radius is the origin and the positive shell gap is
the unit step. -/
def normalizedShellCoordinate (T : TorusParameter) (s : TorusShell) : ℚ :=
  (TorusShell.radius T s - 1) / shellGap T

@[simp] theorem normalizedShellCoordinate_inner (T : TorusParameter) :
    normalizedShellCoordinate T .innerD9 = 0 := by
  simp [normalizedShellCoordinate, torusShell_inner_unit]

@[simp] theorem normalizedShellCoordinate_core (T : TorusParameter) :
    normalizedShellCoordinate T .coreD11 = 1 := by
  have hg : shellGap T ≠ 0 := ne_of_gt (shellGap_pos T)
  rw [normalizedShellCoordinate, core_radius_eq_one_add_gap]
  field_simp [hg]
  ring

@[simp] theorem normalizedShellCoordinate_outer (T : TorusParameter) :
    normalizedShellCoordinate T .outerD13 = 2 := by
  have hg : shellGap T ≠ 0 := ne_of_gt (shellGap_pos T)
  rw [normalizedShellCoordinate, outer_radius_eq_one_add_two_gap]
  field_simp [hg]
  ring

/-- General quadratic shape in the normalized shell coordinate. -/
def quadraticShape (c0 c1 c2 u : ℚ) : ℚ :=
  c0 + c1 * u + c2 * u ^ 2

/-- Quadratic shell readout through the intrinsic normalized coordinate. -/
def normalizedQuadraticReadout (T : TorusParameter) (c0 c1 c2 : ℚ)
    (s : TorusShell) : ℚ :=
  quadraticShape c0 c1 c2 (normalizedShellCoordinate T s)

@[simp] theorem normalizedQuadraticReadout_inner
    (T : TorusParameter) (c0 c1 c2 : ℚ) :
    normalizedQuadraticReadout T c0 c1 c2 .innerD9 = c0 := by
  simp [normalizedQuadraticReadout, quadraticShape]

@[simp] theorem normalizedQuadraticReadout_core
    (T : TorusParameter) (c0 c1 c2 : ℚ) :
    normalizedQuadraticReadout T c0 c1 c2 .coreD11 = c0 + c1 + c2 := by
  simp [normalizedQuadraticReadout, quadraticShape]

@[simp] theorem normalizedQuadraticReadout_outer
    (T : TorusParameter) (c0 c1 c2 : ℚ) :
    normalizedQuadraticReadout T c0 c1 c2 .outerD13 = c0 + 2 * c1 + 4 * c2 := by
  simp [normalizedQuadraticReadout, quadraticShape]
  ring

/-- The canonical minimal nonlinear shape dictated by the owned Puiseux row. -/
def puiseuxQuadraticShape (u : ℚ) : ℚ :=
  (1 / 3 : ℚ) * u - (1 / 12 : ℚ) * u ^ 2

/-- Canonical shell-to-Puiseux transfer, independent of the free metric modulus after
normalization. -/
def canonicalPuiseuxShellReadout (T : TorusParameter) (s : TorusShell) : ℚ :=
  puiseuxQuadraticShape (normalizedShellCoordinate T s)

@[simp] theorem canonicalPuiseuxShellReadout_inner (T : TorusParameter) :
    canonicalPuiseuxShellReadout T .innerD9 = p_e := by
  norm_num [canonicalPuiseuxShellReadout, puiseuxQuadraticShape, p_e]

@[simp] theorem canonicalPuiseuxShellReadout_core (T : TorusParameter) :
    canonicalPuiseuxShellReadout T .coreD11 = p_mu := by
  norm_num [canonicalPuiseuxShellReadout, puiseuxQuadraticShape, p_mu]

@[simp] theorem canonicalPuiseuxShellReadout_outer (T : TorusParameter) :
    canonicalPuiseuxShellReadout T .outerD13 = p_tau := by
  norm_num [canonicalPuiseuxShellReadout, puiseuxQuadraticShape, p_tau]

/-- The owned exponent row has exact negative discrete curvature `-1/6`. -/
theorem puiseux_row_discrete_curvature :
    p_tau - 2 * p_mu + p_e = (-1 / 6 : ℚ) := by
  norm_num [p_e, p_mu, p_tau]

/-- **Coefficient uniqueness.** Any normalized quadratic matching the three owned exponent values
has exactly the coefficients `(0, 1/3, -1/12)`. -/
theorem puiseux_quadratic_coefficients_unique
    (c0 c1 c2 : ℚ)
    (h0 : quadraticShape c0 c1 c2 0 = p_e)
    (h1 : quadraticShape c0 c1 c2 1 = p_mu)
    (h2 : quadraticShape c0 c1 c2 2 = p_tau) :
    c0 = 0 ∧ c1 = 1 / 3 ∧ c2 = -1 / 12 := by
  norm_num [quadraticShape, p_e, p_mu, p_tau] at h0 h1 h2
  constructor
  · exact h0
  constructor <;> linarith

/-- Shell-level uniqueness is independent of the torus metric parameter because normalization
always sends the three shells to `0,1,2`. -/
theorem normalizedQuadraticReadout_coefficients_unique
    (T : TorusParameter) (c0 c1 c2 : ℚ)
    (h0 : normalizedQuadraticReadout T c0 c1 c2 .innerD9 = p_e)
    (h1 : normalizedQuadraticReadout T c0 c1 c2 .coreD11 = p_mu)
    (h2 : normalizedQuadraticReadout T c0 c1 c2 .outerD13 = p_tau) :
    c0 = 0 ∧ c1 = 1 / 3 ∧ c2 = -1 / 12 := by
  rw [normalizedQuadraticReadout_inner] at h0
  rw [normalizedQuadraticReadout_core] at h1
  rw [normalizedQuadraticReadout_outer] at h2
  exact puiseux_quadratic_coefficients_unique c0 c1 c2
    (by simpa [quadraticShape] using h0)
    (by simpa [quadraticShape] using h1)
    (by
      calc
        quadraticShape c0 c1 c2 2 = c0 + 2 * c1 + 4 * c2 := by
          simp [quadraticShape]
          ring
        _ = p_tau := h2)

/-- The canonical transfer is strictly concave: its quadratic coefficient is negative. -/
theorem puiseux_quadratic_curvature_negative :
    (-1 / 12 : ℚ) < 0 := by norm_num

/-- Predicate: the owned exponent row is reached by a quadratic in normalized shell coordinate. -/
def NormalizedQuadraticReachable : Prop :=
  ∃ (T : TorusParameter) (c0 c1 c2 : ℚ),
    normalizedQuadraticReadout T c0 c1 c2 .innerD9 = p_e ∧
    normalizedQuadraticReadout T c0 c1 c2 .coreD11 = p_mu ∧
    normalizedQuadraticReadout T c0 c1 c2 .outerD13 = p_tau

/-- Every admissible torus parameter supports the same canonical normalized quadratic transfer. -/
theorem puiseux_row_normalized_quadratic_reachable (T : TorusParameter) :
    ∃ c0 c1 c2 : ℚ,
      normalizedQuadraticReadout T c0 c1 c2 .innerD9 = p_e ∧
      normalizedQuadraticReadout T c0 c1 c2 .coreD11 = p_mu ∧
      normalizedQuadraticReadout T c0 c1 c2 .outerD13 = p_tau := by
  refine ⟨0, 1 / 3, -1 / 12, ?_, ?_, ?_⟩
  · norm_num [normalizedQuadraticReadout, quadraticShape, p_e]
  · norm_num [normalizedQuadraticReadout, quadraticShape, p_mu]
  · norm_num [normalizedQuadraticReadout, quadraticShape, p_tau]

/-- A concrete admissible parameter witnesses quadratic reachability. -/
theorem puiseux_row_quadratic_reachable :
    NormalizedQuadraticReachable := by
  obtain ⟨c0, c1, c2, h0, h1, h2⟩ :=
    puiseux_row_normalized_quadratic_reachable metricWitnessTwo
  exact ⟨metricWitnessTwo, c0, c1, c2, h0, h1, h2⟩

/-- **Minimal degree exactly two (within polynomial shell-coordinate transfers).** T40 excludes
all affine readouts, while the canonical normalized quadratic exists and is unique. -/
theorem puiseux_shell_transfer_minimal_degree_two :
    ¬ AffineReachable p_e p_mu p_tau
      ∧ NormalizedQuadraticReachable
      ∧ (∀ (T : TorusParameter) (c0 c1 c2 : ℚ),
          normalizedQuadraticReadout T c0 c1 c2 .innerD9 = p_e →
          normalizedQuadraticReadout T c0 c1 c2 .coreD11 = p_mu →
          normalizedQuadraticReadout T c0 c1 c2 .outerD13 = p_tau →
          c0 = 0 ∧ c1 = 1 / 3 ∧ c2 = -1 / 12) :=
  ⟨puiseux_row_not_affine_reachable, puiseux_row_quadratic_reachable,
    normalizedQuadraticReadout_coefficients_unique⟩

/-- Capstone: the normalized shell coordinate is metric-independent on the three owned shells,
and the unique minimal transfer is the concave quadratic `u/3-u²/12`. -/
theorem canonical_puiseux_shell_transfer :
    (∀ T : TorusParameter,
        normalizedShellCoordinate T .innerD9 = 0
        ∧ normalizedShellCoordinate T .coreD11 = 1
        ∧ normalizedShellCoordinate T .outerD13 = 2)
    ∧ (∀ T : TorusParameter,
        canonicalPuiseuxShellReadout T .innerD9 = p_e
        ∧ canonicalPuiseuxShellReadout T .coreD11 = p_mu
        ∧ canonicalPuiseuxShellReadout T .outerD13 = p_tau)
    ∧ p_tau - 2 * p_mu + p_e = (-1 / 6 : ℚ)
    ∧ (-1 / 12 : ℚ) < 0
    ∧ ¬ AffineReachable p_e p_mu p_tau
    ∧ NormalizedQuadraticReachable := by
  refine ⟨?_, ?_, puiseux_row_discrete_curvature,
    puiseux_quadratic_curvature_negative, puiseux_row_not_affine_reachable,
    puiseux_row_quadratic_reachable⟩
  · intro T
    exact ⟨normalizedShellCoordinate_inner T, normalizedShellCoordinate_core T,
      normalizedShellCoordinate_outer T⟩
  · intro T
    exact ⟨canonicalPuiseuxShellReadout_inner T, canonicalPuiseuxShellReadout_core T,
      canonicalPuiseuxShellReadout_outer T⟩

end D0.Synthesis.CanonicalPuiseuxShellTransfer
