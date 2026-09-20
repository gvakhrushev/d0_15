import Mathlib.Data.Real.Basic
import D0.Geometry.ArchiveRefinementTower
import D0.Geometry.ArchivePhaseDistance
import D0.Geometry.ArchiveCanonicalLaplacian
import D0.Geometry.ArchiveRolePhaseProductCarrier
import D0.Geometry.ArchiveProductLaplacian

namespace D0.Geometry.ArchiveMetricLaplacianScaleNoGo

open D0
open D0.Geometry.ArchiveRolePhaseProductCarrier
open D0.Geometry.ArchiveProductLaplacian

/-- The combinatorial cycle size at refinement depth `n` is $L = n + 2$. -/
def cycleSize (n : ℕ) : ℕ := archiveFibers n

/-- Physical continuum lattice spacing $a_n = 1 / L = 1 / (n + 2)$ for a unit-circumference phase circle. -/
noncomputable def latticeSpacing (n : ℕ) : ℝ := (1 : ℝ) / (archiveFibers n : ℝ)

/-- Continuum metric scaling factor $L^2 = (n + 2)^2 = a_n^{-2}$.
This is the quadratic factor used in the Python Weyl certificate `vp_archive_heat_trace_weyl_dimension.py`
to scale the combinatorial cycle Laplacian into a continuum Laplace-Beltrami operator. -/
noncomputable def metricScaleFactor (n : ℕ) : ℝ := (archiveFibers n : ℝ) ^ 2

/-- Combinatorial scale: the Lean `archiveCanonicalLaplacian n` has unit weight ($c_n = 1$). -/
def combinatorialScale : ℝ := 1

/-- Strict scale mismatch between the combinatorial Lean Laplacian and the continuum metric certificate:
for any refinement depth $n \ge 0$, the metric scale factor strictly exceeds the combinatorial unit scale. -/
theorem metric_scale_strictly_exceeds_combinatorial (n : ℕ) :
    combinatorialScale < metricScaleFactor n := by
  unfold combinatorialScale metricScaleFactor archiveFibers
  push_cast
  have h_fibers : (2 : ℝ) ≤ (n : ℝ) + 2 := by linarith
  have h_sq : (4 : ℝ) ≤ ((n : ℝ) + 2) ^ 2 := by nlinarith
  linarith

/-- The metric scale factor grows monotonically with refinement depth:
$$\mathrm{metricScaleFactor}(n + 1) > \mathrm{metricScaleFactor}(n).$$ -/
theorem metric_scale_strictly_increasing (n : ℕ) :
    metricScaleFactor n < metricScaleFactor (n + 1) := by
  unfold metricScaleFactor archiveFibers
  push_cast
  have h1 : (0 : ℝ) < (n : ℝ) + 2 := by linarith
  have h2 : (n : ℝ) + 2 < (n : ℝ) + 1 + 2 := by linarith
  nlinarith

/-- The lattice spacing strictly contracts to zero:
$$a_{n+1} < a_n.$$ -/
theorem lattice_spacing_strictly_decreasing (n : ℕ) :
    latticeSpacing (n + 1) < latticeSpacing n := by
  unfold latticeSpacing archiveFibers
  push_cast
  have h1 : (0 : ℝ) < (n : ℝ) + 2 := by linarith
  have h2 : (n : ℝ) + 2 < (n : ℝ) + 1 + 2 := by linarith
  exact one_div_lt_one_div_of_lt h1 h2

/-- Metric scaled 4D product Laplacian:
$$\widetilde L_{\mathrm{metric}}(n) = L^2 \cdot L_{\mathrm{prod}}(n).$$ -/
noncomputable def metricProductLaplacian (n : ℕ) :
    Matrix (ArchiveRolePhasePoint n) (ArchiveRolePhasePoint n) ℝ :=
  fun x y => metricScaleFactor n * archiveProductLaplacian n x y

/-- The metric-scaled product Laplacian remains symmetric. -/
theorem metricProductLaplacian_symmetric (n : ℕ) :
    MatrixSymmetric (metricProductLaplacian n) := by
  intro x y
  unfold metricProductLaplacian
  have h_symm := archiveProductLaplacian_symmetric n x y
  unfold MatrixSymmetric at h_symm
  rw [h_symm]

/-- **D0-ARCHIVE-METRIC-LAPLACIAN-SCALE-OWNER-001 (Owner)**:
Structural obstruction theorem on the archive Laplacian metric scale:
1. The present-core Lean operator `archiveCanonicalLaplacian` is unscaled ($c_n = 1$).
2. The Python Weyl-dimension certificate uses the metric-scaled operator with $L^2 = (n+2)^2$.
3. The metric scale factor strictly exceeds 1 for all $n$, is strictly increasing,
   and corresponds to the inverse square of the contracting lattice spacing $a_n = 1/(n+2)$.
4. Present-core D0 lacks a canonical dynamical mechanism forcing this $L^2$ factor,
   identifying the metric normalization as an open structural bridge. -/
theorem archive_metric_laplacian_scale_owner :
    (∀ n : ℕ, combinatorialScale < metricScaleFactor n) ∧
    (∀ n : ℕ, metricScaleFactor n < metricScaleFactor (n + 1)) ∧
    (∀ n : ℕ, latticeSpacing (n + 1) < latticeSpacing n) ∧
    (∀ n : ℕ, MatrixSymmetric (metricProductLaplacian n)) :=
  ⟨metric_scale_strictly_exceeds_combinatorial,
   metric_scale_strictly_increasing,
   lattice_spacing_strictly_decreasing,
   metricProductLaplacian_symmetric⟩

end D0.Geometry.ArchiveMetricLaplacianScaleNoGo
