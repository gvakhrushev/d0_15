import D0.Gauge.AnomalySums
import Mathlib.Tactic

/-!
# D0-SM-ANOMALY-CANCELLATION-OWNER-001 / hypercharge graph-flow (Lean)

Python certificates: `05_CERTS/vp_sm_anomaly_cancellation_owner.py`,
`05_CERTS/vp_hypercharge_graph_flow_owner.py`, `05_CERTS/vp_sm_hypercharge_minimal_denominator.py`.

Front P1 construction. The carrier is the complete tripartite graph `K(9,11,13)` (zones 9, 11, 13;
33 vertices). The one-generation hypercharge row `Y = (1/6, −2/3, 1/3, −1/2, 1, 0)` (left-handed Weyl
convention) is **anomaly-free**: the gravitational·U(1), U(1)³, SU(2)²·U(1) and SU(3)²·U(1) sums all
vanish — reused here as the proven `D0.Gauge.AnomalySums` theorems (`D0-GAUGE-MATTER-002`, CORE).

HONESTY BOUNDARY. What is owned here (CERT-CLOSED, consolidating the existing CORE anomaly proof): the
row is anomaly-free on the `K(9,11,13)` carrier. What stays PROOF-TARGET: deriving the hypercharge row
itself as a normalized divergence-free edge-current (`D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001`) and forcing
the minimal denominator `6` from the Kirchhoff flow solution space (`D0-SM-HYPERCHARGE-MINIMAL-DENOMINATOR-001`)
— here only the edge-current/divergence-free SCAFFOLD is given. No SM charge table is imported as a
proof of origin; the anomaly-free property is a genuine arithmetic fact about the row.
-/

namespace D0.Matter

open D0

/-- The complete tripartite carrier `K(9,11,13)` (zones 9, 11, 13). -/
structure TripartiteGraph where
  n9 : Nat
  n11 : Nat
  n13 : Nat
  h9 : n9 = 9
  h11 : n11 = 11
  h13 : n13 = 13

/-- The scene graph. -/
def sceneGraph : TripartiteGraph := ⟨9, 11, 13, rfl, rfl, rfl⟩

/-- Total vertex count `9 + 11 + 13 = 33`. -/
theorem scene_vertex_count : sceneGraph.n9 + sceneGraph.n11 + sceneGraph.n13 = 33 := by decide

/-- An oriented edge-current on the scene (scaffold for the graph-flow derivation): the Kirchhoff
divergence-free condition and the zone-normalized projection are recorded as the obligations that the
hypercharge-from-flow owner must discharge (`D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001`, PROOF-TARGET). -/
structure EdgeCurrent where
  /-- Kirchhoff conservation: the signed current sums to zero at every vertex. -/
  divergenceFree : Prop
  /-- The zone-normalized projection onto the 3-zone hypercharge row is well-defined. -/
  zoneProjectionDefined : Prop

/-- **D0-SM-ANOMALY-CANCELLATION-OWNER-001.** On the `K(9,11,13)` carrier (33 vertices) the
one-generation hypercharge row is anomaly-free: all four anomaly sums vanish (reusing the proven
`D0.Gauge.AnomalySums`). -/
theorem sm_anomaly_cancellation_owner :
    (sceneGraph.n9 + sceneGraph.n11 + sceneGraph.n13 = 33)
      ∧ gravU1Sum = 0
      ∧ cubicU1Sum = 0
      ∧ su2su2u1Sum = 0
      ∧ su3su3u1Sum = 0 :=
  ⟨scene_vertex_count, grav_U1_anomaly_sum, U1_cubic_anomaly_sum,
   SU2_SU2_U1_anomaly_sum, SU3_SU3_U1_anomaly_sum⟩

end D0.Matter
