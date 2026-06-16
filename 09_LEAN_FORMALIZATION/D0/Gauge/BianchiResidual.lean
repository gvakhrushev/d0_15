import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import D0.Gauge.NonAbelianDiscreteCurvature

namespace D0.Gauge

open D0.Algebra D0.Matter

noncomputable def spatialWedgeCommutator {n : Type} [Fintype n]
    (A K : Matrix n n ℝ) : Matrix n n ℝ :=
  spatialWedge A K

noncomputable def bianchiResidual {n : Type} [Fintype n]
    (D A : Matrix n n ℝ) : Matrix n n ℝ :=
  let K := discreteNonAbelianCurvature D A
  spatialCommutator D K + spatialWedgeCommutator A K

theorem residual_expands_by_definitions {n : Type} [Fintype n]
    (D A : Matrix n n ℝ) :
    bianchiResidual D A =
      let K := discreteNonAbelianCurvature D A
      spatialCommutator D K + spatialWedgeCommutator A K := by
  rfl

/-- The graph (graded-incidence) Bianchi residual `R = [D,K] + [A,K]` (with `K` the non-abelian
curvature) of two skew operators is itself a well-defined skew operator — the discrete replacement
for the exact continuum Bianchi identity. -/
theorem bianchiResidual_skew {n : Type} [Fintype n] [DecidableEq n]
    (D A : Matrix n n ℝ) (hD : isSkew D) (hA : isSkew A) :
    isSkew (bianchiResidual D A) := by
  have hK : isSkew (discreteNonAbelianCurvature D A) :=
    nonabelian_curvature_preserves_skew D A hD hA
  have h1 : isSkew (spatialCommutator D (discreteNonAbelianCurvature D A)) :=
    spatialCommutator_preserves_skew D _ hD hK
  have h2 : isSkew (spatialWedgeCommutator A (discreteNonAbelianCurvature D A)) :=
    spatialWedge_preserves_skew A _ hA hK
  exact skew_add h1 h2

/-- The graph Bianchi residual closes on skew operators: `[D,K]+[A,K]` stays skew
(instantiates the proved `bianchiResidual_skew`). -/
def exact_residual_graph_anomaly_boundary : Prop :=
  ∀ {n : Type} [Fintype n] [DecidableEq n] (D A : Matrix n n ℝ),
    isSkew D → isSkew A → isSkew (bianchiResidual D A)

theorem exact_residual_graph_anomaly_boundary_proof :
    exact_residual_graph_anomaly_boundary := by
  intro n _ _ D A hD hA
  exact bianchiResidual_skew D A hD hA

end D0.Gauge
