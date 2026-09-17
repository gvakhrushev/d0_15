import D0.Matter.GaugeCurvatureOrigin
import D0.Matter.VectorOperatorOrigin
import D0.Geometry.EdgeStiffnessOrigin

namespace D0.Bridge

def gauge_curvature_origin_closed : Prop :=
  D0.Matter.gauge_curvature_origin_closed

theorem gauge_curvature_origin_closed_proof : gauge_curvature_origin_closed := by
  exact D0.Matter.gauge_curvature_origin_closed_proof

def vector_operator_origin_closed : Prop :=
  D0.Matter.vector_operator_origin_closed

theorem vector_operator_origin_closed_proof : vector_operator_origin_closed := by
  exact D0.Matter.vector_operator_origin_closed_proof

def edge_stiffness_origin_closed : Prop :=
  D0.Geometry.edge_stiffness_origin_closed

theorem edge_stiffness_origin_closed_proof : edge_stiffness_origin_closed := by
  exact D0.Geometry.edge_stiffness_origin_closed_proof

def nonabelian_completion_boundary : Prop :=
  D0.Matter.nonabelian_completion_boundary

theorem nonabelian_completion_boundary_proof : nonabelian_completion_boundary := by
  exact D0.Matter.nonabelian_completion_boundary_proof

#check gauge_curvature_origin_closed
#check vector_operator_origin_closed
#check edge_stiffness_origin_closed
#check nonabelian_completion_boundary

end D0.Bridge
