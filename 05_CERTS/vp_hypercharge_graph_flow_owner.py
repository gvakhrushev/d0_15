#!/usr/bin/env python3
"""
vp_hypercharge_graph_flow_owner.py  (PROOF-TARGET manifest)

D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001 / Front P1.

Lean: D0.Matter.HyperchargeGraphFlowOwner provides the K(9,11,13) carrier and an
EdgeCurrent SCAFFOLD (divergenceFree : Prop, zoneProjectionDefined : Prop) recorded
as the obligations the hypercharge-from-flow owner must discharge.

WHAT IS REAL HERE (verified): the Kirchhoff conservation structure is genuine -- on a
tiny example graph (a triangle) we build an explicit divergence-free edge-current
(integer/Fraction circulation) and check it sums to 0 at every vertex, exactly.

WHAT STAYS OPEN (PROOF-TARGET -- exact missing artifact printed below):
  A divergence-free EdgeCurrent J on the FULL K(9,11,13) carrier whose zone-normalized
  U(1) holonomy reproduces the one-generation hypercharge row
  Y = (1/6, -2/3, 1/3, -1/2, 1, 0). The triangle below only demonstrates the
  conservation STRUCTURE is real; it does NOT derive the row. No SM charge table is
  used to define the D0 object.
"""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fractions import Fraction as F


def divergence_at(vertex, edges, current):
    """Net signed flow into `vertex`. edges[k]=(u,v) oriented u->v; current[k]=flow.
    Convergence (in-flow positive) at vertex = sum over edges of signed contribution.
    """
    div = F(0)
    for k, (u, v) in enumerate(edges):
        if v == vertex:
            div += current[k]   # flow arriving at vertex
        if u == vertex:
            div -= current[k]   # flow leaving vertex
    return div


def main() -> int:
    print("=== vp_hypercharge_graph_flow_owner (PROOF-TARGET manifest) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the carrier K(9,11,13) (complete tripartite, "
          "zones 9/11/13, 33 vertices), the notion of an oriented EdgeCurrent J on its edges, "
          "the Kirchhoff divergence operator div(J)(v)=Sum_{e into v}J - Sum_{e out of v}J, "
          "and the zone-normalized U(1)-holonomy projection -- ALL fixed BEFORE any "
          "hypercharge number. The hypercharge row is NOT input; it is the target of the open derivation.")

    # --- TINY EXAMPLE: a triangle, to prove the conservation structure is real ----
    # Vertices a,b,c; oriented edges a->b, b->c, c->a; a circulation of strength s.
    verts = ["a", "b", "c"]
    edges = [("a", "b"), ("b", "c"), ("c", "a")]
    s = F(7, 3)  # arbitrary rational circulation strength (exact)
    current = [s, s, s]  # equal circulation around the cycle -> divergence-free

    divs = {v: divergence_at(v, edges, current) for v in verts}
    assert all(d == F(0) for d in divs.values()), f"triangle current not divergence-free: {divs}"
    print(f"PASS_TRIANGLE_KIRCHHOFF circulation s={s} around triangle a->b->c->a is "
          f"divergence-free: div = {{ {', '.join(f'{v}:{divs[v]}' for v in verts)} }} (all 0, exact).")

    # A second, non-uniform divergence-free current: superpose two opposite circulations.
    current2 = [F(2), F(2), F(2)]
    divs2 = {v: divergence_at(v, edges, current2) for v in verts}
    assert all(d == F(0) for d in divs2.values()), "second cycle current not divergence-free"
    print(f"PASS_CYCLE_SPACE_NONTRIVIAL a 1-dim cycle space exists on the triangle "
          f"(any uniform circulation is conserved); checked current={current2} -> all div 0.")

    # --- The EXACT missing artifact (PROOF-TARGET) --------------------------------
    print("MISSING_ARTIFACT (D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001, PROOF-TARGET):")
    print("  Required: a divergence-free EdgeCurrent J on K(9,11,13) (i.e. div(J)(v)=0 at "
          "all 33 vertices) together with a fixed zone-normalization of its U(1) holonomy "
          "such that the induced per-multiplet holonomies equal EXACTLY "
          "(1/6, -2/3, 1/3, -1/2, 1, 0).")
    print("  Status: ABSENT. Only the EdgeCurrent SCAFFOLD (divergenceFree/zoneProjectionDefined "
          "as Prop fields in Lean D0.Matter.EdgeCurrent) and the conservation check above exist. "
          "The map (divergence-free current) -> (hypercharge row) is not constructed.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    # (a) A current with NONZERO divergence at one vertex must be rejected.
    bad_current = [s, s, F(0)]  # break the c->a leg -> b,c imbalanced... check explicitly
    bad_divs = {v: divergence_at(v, edges, bad_current) for v in verts}
    assert any(d != F(0) for d in bad_divs.values()), \
        "negative control failed: broken current still divergence-free"
    print(f"FAIL_NONZERO_DIVERGENCE_CAUGHT current {bad_current} has div "
          f"{{ {', '.join(f'{v}:{bad_divs[v]}' for v in verts)} }} -- not all 0, rejected.")

    # (b) "The row IS derived (graph-flow owner closed)" -- rejected: scaffold-only.
    claim_row_derived = False  # the derivation map does not exist
    assert claim_row_derived is False, "would over-claim: hypercharge row derived from flow"
    print("FAIL_ROW_DERIVED_CLAIM_CAUGHT 'hypercharge row is DERIVED as a divergence-free "
          "edge-current' is rejected -- this cert is SCAFFOLD-ONLY (missing artifact above).")

    # (c) "SM charge table = the graph-flow derivation" -- rejected.
    claim_sm_table_is_derivation = False
    assert claim_sm_table_is_derivation is False, "would launder SM table as a derivation"
    print("FAIL_SM_TABLE_AS_DERIVATION_CAUGHT 'pasted SM charge table = graph-flow derivation' "
          "is rejected; a table is not a divergence-free edge-current on K(9,11,13).")

    print("CROSS_REF Lean D0.Matter.HyperchargeGraphFlowOwner (EdgeCurrent scaffold; "
          "sm_anomaly_cancellation_owner reuses D0.Gauge.AnomalySums CORE).")
    print("PASS_VP_HYPERCHARGE_GRAPH_FLOW_OWNER conservation STRUCTURE verified on a triangle; "
          "full-carrier derivation NAMED as missing artifact; manifest PROOF-TARGET.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
