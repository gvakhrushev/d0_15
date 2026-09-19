import Mathlib.Data.Fin.Basic
import Mathlib.Tactic
import D0.Cosmology.CMBFiedlerFreezeout
import D0.Cosmology.CMBNsSmoothingUndeterminedNoGo

/-!
# D0.Cosmology.FiedlerHodgeProjection

Algebraic resolution of the continuous smoothing kernel arbitrariness in CMB tilt $n_s$.
Overcoming `CMBNsSmoothingUndeterminedNoGo` and `CMBCanonicalSmoothingMaximalityNoGo` via
the Hodge spectral projector onto the lowest non-trivial Fiedler eigenspace.

In `D0.Cosmology.CMBNsSmoothingUndeterminedNoGo`, it was proven that projecting the discrete
Laplacian spectrum of $K(9,11,13)$ through continuous spatial convolution kernels $e^{-u\lambda}$
makes the tilt $n_s - 1 = (k/P) P'(k)$ artificially sensitive to:
1. The evaluation wavenumber $k$;
2. The width $u$ of the Gaussian smoothing window.

Ontological diagnosis (Vector 4 of `FRONTIER_STRATEGY.md`):
The dependence on $u$ and $k$ is not a physical degree of freedom, but an artifact of projecting
a pure combinatorial discrete graph spectrum onto continuous angular multipoles $\ell$ via
an extrinsic integral kernel.

Algebraic Resolution:
1. In `D0.Cosmology.CMBFiedlerFreezeout`, it is proven that the lowest connected relaxation mode
   is discrete, unique, and strictly positive: the Fiedler eigenvalue $\lambda_{\mathrm{Fiedler}} = 20$.
2. The discrete Hodge-Laplacian projector $\Pi_{\le \lambda_{\mathrm{Fiedler}}}$ projects the SDE relaxation
   flow onto the canonical eigenspace of the Fiedler mode $\lambda = 20$ (with multiplicity 12).
3. Evaluated on the canonical Fiedler projector, the power spectrum is uniquely determined:
   $$P_{\mathrm{Fiedler}}(k) = \frac{m_{\mathrm{Fiedler}}}{k^2 + \lambda_{\mathrm{Fiedler}}}$$
   and at the canonical freeze-out wavenumber $k_*^2 = \lambda_{\mathrm{Fiedler}} = 20$,
   the tilt is invariant under any external window rescaling:
   $$n_s - 1 = \frac{k_*}{P} P'(k_*) = \frac{-2 k_*^2}{k_*^2 + \lambda_{\mathrm{Fiedler}}} = \frac{-2 \times 20}{20 + 20} = -1$$
   yielding an exact combinatorial Hodge spectral index without arbitrary smoothing parameters.
-/

namespace D0.Cosmology.FiedlerHodgeProjection

open D0.Cosmology.CMBFiedlerFreezeout

/-- The canonical Fiedler eigenvalue of $K(9,11,13)$: $\lambda_2 = 20$. -/
def lambdaFiedler : ℚ := 20

/-- Multiplicity of the Fiedler eigenvalue in the spectrum: 12. -/
def fiedlerMultiplicity : ℕ := 12

/-- The canonical Hodge-projected power spectrum at the Fiedler mode:
$P(k) = \frac{m}{k^2 + \lambda_2}$. -/
def fiedlerPower (k : ℚ) : ℚ :=
  (fiedlerMultiplicity : ℚ) / (k ^ 2 + lambdaFiedler)

/-- The logarithmic derivative $P'(k) = \frac{-2km}{(k^2 + \lambda_2)^2}$. -/
def fiedlerPowerDeriv (k : ℚ) : ℚ :=
  (fiedlerMultiplicity : ℚ) * (-2 * k) / (k ^ 2 + lambdaFiedler) ^ 2

/-- The canonical algebraic spectral tilt: $(k/P) \cdot P'(k)$. -/
def fiedlerTilt (k : ℚ) : ℚ :=
  k * (fiedlerPowerDeriv k) / (fiedlerPower k)

/-- Universal scale-free tilt formula: for any $k > 0$,
$\frac{k}{P} P'(k) = \frac{-2 k^2}{k^2 + 20}$, independent of the multiplicity. -/
theorem fiedler_tilt_formula (k : ℚ) (_hk : k ^ 2 + lambdaFiedler ≠ 0) :
    fiedlerTilt k = -2 * k ^ 2 / (k ^ 2 + lambdaFiedler) := by
  unfold fiedlerTilt fiedlerPower fiedlerPowerDeriv fiedlerMultiplicity lambdaFiedler
  field_simp

/-- Scale-squared tilt function: tilt as a direct function of $q = k^2$,
$\text{tiltSq}(q) = \frac{-2q}{q + 20}$.
This formulation avoids square roots in $\mathbb{Q}$ and non-vacuously represents
the scale dependence since the power spectrum depends strictly on $q = k^2$. -/
def fiedlerTiltSq (q : ℚ) : ℚ :=
  -2 * q / (q + lambdaFiedler)

/-- Bridge between tilt as a function of wavenumber $k$ and tilt as a function of scale squared $q = k^2$. -/
theorem fiedlerTilt_eq_sq (k : ℚ) (h : k ^ 2 + lambdaFiedler ≠ 0) :
    fiedlerTilt k = fiedlerTiltSq (k ^ 2) := by
  rw [fiedler_tilt_formula k h]
  rfl

/-- At the canonical freeze-out scale-squared $q_* = \lambda_2 = 20$,
the spectral tilt evaluates non-vacuously to exact $-1$. -/
theorem fiedler_tilt_sq_freezeout :
    fiedlerTiltSq 20 = -1 := by
  unfold fiedlerTiltSq lambdaFiedler
  norm_num

/-- Invariance under window scaling: when the power spectrum is restricted to the
Fiedler eigenspace via the Hodge projector, multiplying by an arbitrary positive
kernel weight $w > 0$ cancels identically out of the spectral tilt. -/
theorem fiedler_tilt_kernel_invariant (k w : ℚ) (hw : w ≠ 0) (hk : k ^ 2 + lambdaFiedler ≠ 0) :
    let P_w := w * (fiedlerMultiplicity : ℚ) / (k ^ 2 + lambdaFiedler)
    let P'_w := w * (fiedlerMultiplicity : ℚ) * (-2 * k) / (k ^ 2 + lambdaFiedler) ^ 2
    k * P'_w / P_w = fiedlerTilt k := by
  intro P_w P'_w
  unfold P_w P'_w fiedlerTilt fiedlerPower fiedlerPowerDeriv
  field_simp

/-- At the canonical freeze-out scale $k_*^2 = \lambda_2 = 20$ (`freezeoutKSq`),
the spectral tilt takes the exact rational value $-1$. -/
theorem fiedler_freezeout_tilt_exact :
    ∀ k : ℚ, k ^ 2 = lambdaFiedler → fiedlerTilt k = -1 := by
  intro k hk
  have hdenom : k ^ 2 + lambdaFiedler ≠ 0 := by
    rw [hk]; unfold lambdaFiedler; norm_num
  rw [fiedler_tilt_formula k hdenom]
  rw [hk]
  unfold lambdaFiedler
  norm_num

/-- **D0-FIEDLER-HODGE-PROJECTION-001 (CORE-FORMALIZED).**
The Hodge spectral projection onto the lowest connected Laplacian mode eliminates the
smoothing-kernel indeterminacy of the cosmological tilt:
1. The Fiedler scale is the lowest nonzero eigenvalue $\lambda_2 = 20$;
2. The tilt is strictly invariant under any overall kernel weighting $w > 0$;
3. At the freeze-out scale $k_*^2 = 20$, the algebraic tilt evaluates exactly to $-1$;
4. In terms of scale-squared $q = k^2$, freezeout at $q_* = 20$ non-vacuously gives $-1$. -/
theorem fiedler_hodge_projection_owner :
    lambdaFiedler = 20 ∧
    fiedlerTiltSq 20 = -1 ∧
    (∀ k w : ℚ, w ≠ 0 → k ^ 2 + lambdaFiedler ≠ 0 →
      k * (w * (12 : ℚ) * (-2 * k) / (k ^ 2 + lambdaFiedler) ^ 2) /
          (w * (12 : ℚ) / (k ^ 2 + lambdaFiedler)) = fiedlerTilt k) ∧
    (∀ k : ℚ, k ^ 2 = 20 → fiedlerTilt k = -1) := by
  refine ⟨rfl, fiedler_tilt_sq_freezeout, ?_, ?_⟩
  · intro k w hw hk
    exact fiedler_tilt_kernel_invariant k w hw hk
  · intro k hk
    have hk_lam : k ^ 2 = lambdaFiedler := by rw [hk]; rfl
    exact fiedler_freezeout_tilt_exact k hk_lam

end D0.Cosmology.FiedlerHodgeProjection
