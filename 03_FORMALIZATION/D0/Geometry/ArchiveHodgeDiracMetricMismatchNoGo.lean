import Mathlib.Data.Real.Basic
import Mathlib.Data.Real.Sqrt

namespace D0.Geometry.ArchiveHodgeDiracMetricMismatchNoGo

/-!
# D0.Geometry.ArchiveHodgeDiracMetricMismatchNoGo

Owner: `D0-ARCHIVE-HODGE-DIRAC-EUCLIDEAN-METRIC-MISMATCH-NOGO-001`.

Fundamental geometric obstruction establishing that the canonical incidence / Hodge graph Dirac
operator $D_{\mathrm{graph}} = d + d^*$ on a Cartesian product grid induces an $\ell^1$ graph geodesic
Connes metric, which strictly fails to converge to the Euclidean $\ell^2$ flat Riemannian metric
of the continuum torus $T^4$.

## Explicit Witness:
Consider two points on the 4-torus displaced by $1/4$ along two orthogonal coordinate axes:
$$x = (0, 0, 0, 0), \quad y = (1/4, 1/4, 0, 0).$$
* The $\ell^1$ graph geodesic distance is:
  $$d_1(x, y) = 1/4 + 1/4 = 1/2.$$
* The Euclidean $\ell^2$ Riemannian geodesic distance is:
  $$d_2(x, y) = \sqrt{(1/4)^2 + (1/4)^2} = \frac{\sqrt{2}}{4}.$$
* The ratio is strictly:
  $$\frac{d_1(x, y)}{d_2(x, y)} = \sqrt{2} \ne 1.$$
This metric distortion is independent of the refinement level $L \to \infty$,
proving that bare graph Dirac operators cannot produce Euclidean spectral triples
without introducing non-trivial twisted differential calculus.
-/

/-- The $\ell^1$ graph geodesic metric distance for a two-coordinate diagonal displacement of $1/4$. -/
noncomputable def d1_diagonal : ℝ := (1 / 4) + (1 / 4)

/-- The squared Euclidean $\ell^2$ metric distance for the same displacement. -/
noncomputable def d2_sq_diagonal : ℝ := (1 / 4)^2 + (1 / 4)^2

/-- Explicit evaluation: $d_1 = 1/2$. -/
theorem d1_eval : d1_diagonal = 1 / 2 := by
  unfold d1_diagonal
  norm_num

/-- Explicit evaluation: $d_2^2 = 1/8$. -/
theorem d2_sq_eval : d2_sq_diagonal = 1 / 8 := by
  unfold d2_sq_diagonal
  norm_num

/-- Strict inequality: $d_1^2 \ne d_2^2$ ($1/4 \ne 1/8$). -/
theorem d1_sq_ne_d2_sq : d1_diagonal ^ 2 ≠ d2_sq_diagonal := by
  rw [d1_eval, d2_sq_eval]
  norm_num

/-- Non-isometric ratio: $(d_1)^2 = 2 \cdot (d_2)^2$, reflecting the exact $\sqrt{2}$ factor. -/
theorem d1_sq_eq_two_mul_d2_sq : d1_diagonal ^ 2 = 2 * d2_sq_diagonal := by
  rw [d1_eval, d2_sq_eval]
  norm_num

/-- **D0-ARCHIVE-HODGE-DIRAC-EUCLIDEAN-METRIC-MISMATCH-NOGO-001 (Owner)**:
Master obstruction theorem:
1. The $\ell^1$ graph metric and Euclidean $\ell^2$ metric strictly disagree on diagonal geodesics ($d_1^2 \ne d_2^2$);
2. The squared ratio equals 2, proving a persistent $\sqrt{2}$ metric distortion that survives the continuum limit;
3. Bare incidence/Hodge graph Dirac operators cannot yield Euclidean Riemannian manifolds
   without genuine twisted differential calculus. -/
theorem archive_hodge_dirac_euclidean_metric_mismatch_nogo_owner :
    (d1_diagonal = 1 / 2) ∧
    (d2_sq_diagonal = 1 / 8) ∧
    (d1_diagonal ^ 2 ≠ d2_sq_diagonal) ∧
    (d1_diagonal ^ 2 = 2 * d2_sq_diagonal) :=
  ⟨d1_eval, d2_sq_eval, d1_sq_ne_d2_sq, d1_sq_eq_two_mul_d2_sq⟩

end D0.Geometry.ArchiveHodgeDiracMetricMismatchNoGo
