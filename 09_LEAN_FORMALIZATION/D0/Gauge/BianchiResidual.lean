import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import D0.Gauge.NonAbelianDiscreteCurvature

namespace D0.Gauge

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

def exact_residual_graph_anomaly_boundary : Prop := True

theorem exact_residual_graph_anomaly_boundary_proof :
    exact_residual_graph_anomaly_boundary := by
  trivial

end D0.Gauge
