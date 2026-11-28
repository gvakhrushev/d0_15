#!/usr/bin/env python3
"""Fixed-boundary A/4 capacity and a separate 0->3 terminal min-cut control."""

from __future__ import annotations
import json
from pathlib import Path
from cert_runtime import output_path
from datetime import datetime, timezone
from collections import defaultdict, deque
import math

def max_flow_min_cut(cap: dict, source: int, sink: int, n: int) -> tuple[float, float]:
    """Tiny Ford-Fulkerson / Edmonds-Karp for small deterministic graph. Returns (maxflow, mincut)."""
    if n <= 0 or source == sink or not (0 <= source < n and 0 <= sink < n):
        raise ValueError("source and sink must be distinct vertices in the network")
    # Residual reverse capacity must not overwrite an input edge in the opposite direction.
    residual = defaultdict(lambda: defaultdict(float))
    for (u, v), c in cap.items():
        if not (0 <= u < n and 0 <= v < n) or not math.isfinite(c) or c < 0:
            raise ValueError("capacities must be finite, nonnegative, and use valid vertices")
        residual[u][v] += c
    flow = 0.0
    while True:
        parent = [-1] * n
        q = deque([source])
        parent[source] = -2
        while q and parent[sink] == -1:
            u = q.popleft()
            for v in range(n):
                if parent[v] == -1 and residual[u][v] > 1e-12:
                    parent[v] = u
                    q.append(v)
        if parent[sink] == -1:
            break
        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, residual[u][v])
            v = u
        flow += path_flow
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] -= path_flow
            residual[v][u] += path_flow
            v = u
    # The final search exhausted the residual-reachable source side. Sum the
    # original directed capacities crossing this side, independently of flow.
    reachable = {v for v in range(n) if parent[v] != -1}
    cut = sum(c for (u, v), c in cap.items() if u in reachable and v not in reachable)
    return flow, float(cut)

def run_certificate() -> None:
    print("--- D0 FINITE FIXED-CUT CAPACITY AND 0->3 MIN-CUT CERTIFICATE ---")

    # Deterministic 4-vertex graph, A={0,1}, A^c={2,3}.
    # This particular partition has capacity 4 (two edges, capacity 2 each).
    n = 4
    cap = {
        (0,2): 2.0, (0,3): 0.0,
        (1,2): 0.0, (1,3): 2.0,
        (2,0): 0.0, (2,1): 0.0,
        (3,0): 0.0, (3,1): 0.0,
    }
    # Preserve the declared reverse zero-capacity edges.
    for (u,v),c in list(cap.items()):
        if (v,u) not in cap:
            cap[(v,u)] = 0.0

    mf, mc = max_flow_min_cut(cap, 0, 3, n)
    # The fixed A|A^c partition is a separate quantity from the 0->3 min-cut.
    A = {0,1}
    cut_val = sum(cap.get((i,j),0.0) for i in A for j in range(n) if j not in A)
    S = cut_val / 4.0

    if not math.isclose(mf, mc, rel_tol=1e-12, abs_tol=1e-12):
        raise AssertionError(f"terminal max-flow {mf} differs from independently computed min-cut {mc}")
    if mf != 0.0 or mc != 0.0:
        raise AssertionError(f"the original 0->3 network has max-flow and min-cut 0, got {mf}, {mc}")
    if cut_val != 4.0 or S != 1.0:
        raise AssertionError(f"fixed partition and its /4 value must be 4 and 1, got {cut_val}, {S}")
    if not cut_val > mc:
        raise AssertionError("the fixed A|A^c cut must be distinct from the 0->3 minimum")

    print("[1] Finite network + subsystem split A|A^c defined: PASS")
    print(f"[2] Fixed A|A^c cut capacity: {cut_val} (two capacity-2 edges)")
    print(f"[3] 0->3 max-flow and independently computed min-cut: {mf} == {mc}: PASS")
    print(f"[4] Declared S_EE = fixed cut / 4 = {S}; no physical entropy is computed")
    print("PASS_FINITE_FIXED_BOUNDARY_A4")
    print("PASS_MAXFLOW_MINCUT_WITNESS")

    # Distinct normalizations of this nonzero fixed cut give different values.
    S_half = cut_val / 2.0
    S_eighth = cut_val / 8.0
    if S_half == S:
        raise AssertionError(f"A/2 normalization {S_half} must differ from A/4 value {S}")
    if S_eighth == S:
        raise AssertionError(f"A/8 normalization {S_eighth} must differ from A/4 value {S}")
    print("[5] Negative controls:")
    print("    A/2 would give", S_half, "!= S : PASS")
    print("    A/8 would give", S_eighth, "!= S : PASS")
    print("PASS_A4_NEGATIVE_CONTROLS")
    print("Scope: fixed cut / 4 is a defined numerical capacity; it is not the 0->3 min-cut or a computed quantum entropy.")

    results = {
        "status": "PASS_FINITE_FIXED_BOUNDARY_A4",
        "min_cut": mc,
        "fixed_partition_cut": cut_val,
        "S_EE": S,
        "S_EE_scope": "fixed partition capacity / 4 by definition, not computed quantum entropy",
        "max_flow": mf,
        "substatuses": ["PASS_FINITE_FIXED_BOUNDARY_A4", "PASS_MAXFLOW_MINCUT_WITNESS", "PASS_A4_NEGATIVE_CONTROLS"],
        "negative_controls": ["A/2 differs from A/4", "A/8 differs from A/4", "fixed cut differs from terminal min-cut"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    out = output_path(__file__, Path(__file__).with_suffix(".results.json").name)
    out.write_text(json.dumps(results, indent=2))
    print(f"Results: {out.name}")

if __name__ == "__main__":
    run_certificate()
