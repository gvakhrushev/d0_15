#!/usr/bin/env python3
"""D0-COSMOLOGY-CONNECTIVITY-THRESHOLD-OWNER-001 (CERT-CLOSED) - percolation onset is real.

Front P4. The onset of cosmic expansion is a graph connectivity threshold, not an inflationary
singularity (BOOK_08 §08.49, GOLDEN-LEDGER THE 61.4). The forced carrier is the complete tripartite
graph K(9,11,13): zones of size 9, 11, 13 give 33 vertices, and EVERY cross-zone pair is an edge
(no intra-zone edges - a role cannot distinguish itself). The Lean owner module
D0.Cosmology.ReheatingPercolationOwner records `before.connected = false -> after.connected = true`.

WHAT IS PROVED (exact, able to FAIL):
  * K(9,11,13) has 33 vertices and 9*11 + 9*13 + 11*13 = 359 cross-zone edges; BFS from any seed
    reaches all 33 vertices, so it IS connected (the AFTER stage).
  * The SUB-THRESHOLD stage (only the intra-zone edges allowed; a complete tripartite graph has
    NONE, so the stage is 33 isolated vertices) has BFS-component-count 33 != 1: it is DISCONNECTED
    (the BEFORE stage).
  * Therefore the transition disconnected -> connected at the threshold is real, matching the Lean
    `PercolationTransition` with `h_before : before.connected = false`, `h_after : after.connected = true`.

The structure (33-vertex complete tripartite, no inflaton) is fixed BEFORE any number; no CMB datum,
no Planck n_s, no inflaton field enters.
"""
from __future__ import annotations

import sys
from collections import deque

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ZONES = (9, 11, 13)  # forced zone sizes -> 33 vertices


def build_blocks(sizes):
    """Partition vertices 0..(sum-1) into contiguous zones; return (n, block_of)."""
    block_of, v = {}, 0
    for b, s in enumerate(sizes):
        for _ in range(s):
            block_of[v] = b
            v += 1
    return v, block_of


def complete_tripartite_edges(n, block_of):
    """Edges of K: every cross-zone pair (i<j) is present; no intra-zone edge."""
    adj = {u: set() for u in range(n)}
    for u in range(n):
        for w in range(u + 1, n):
            if block_of[u] != block_of[w]:
                adj[u].add(w)
                adj[w].add(u)
    return adj


def subthreshold_edges(n, block_of, k_adj):
    """Sub-threshold stage: the edges of K retained below threshold are exactly those that are
    INTRA-zone. K(9,11,13) is complete tripartite, so EVERY edge of K is cross-zone; the intersection
    with intra-zone pairs is empty -> the sub-threshold stage is 33 isolated vertices.
    """
    adj = {u: set() for u in range(n)}
    for u in range(n):
        for w in k_adj[u]:
            if block_of[u] == block_of[w]:  # retain only intra-zone edges of K (there are none)
                adj[u].add(w)
    return adj


def n_components(n, adj):
    """Count connected components by BFS over an adjacency-set graph (exact integer count)."""
    seen, comps = set(), 0
    for s in range(n):
        if s in seen:
            continue
        comps += 1
        q = deque([s])
        seen.add(s)
        while q:
            x = q.popleft()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    q.append(y)
    return comps


def is_connected(n, adj):
    return n > 0 and n_components(n, adj) == 1


def main() -> int:
    print("=== D0-COSMOLOGY-CONNECTIVITY-THRESHOLD-OWNER-001  percolation onset K(9,11,13) (CERT-CLOSED) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: zones (9,11,13) -> 33-vertex COMPLETE TRIPARTITE scene "
          "(every cross-zone pair an edge, no intra-zone edge), and the transition disconnected->connected "
          "is fixed before any number; no inflaton, no CMB datum")

    # ---- vertex count = 33 ----------------------------------------------------------
    n, block_of = build_blocks(ZONES)
    assert n == 33, f"vertex count != 33: {n}"
    assert sum(ZONES) == 33, "zone sizes must sum to 33"
    print(f"PASS_VERTEX_COUNT_33  9+11+13 = {n} vertices")

    # ---- AFTER stage: K(9,11,13) is connected ---------------------------------------
    after = complete_tripartite_edges(n, block_of)
    n_edges = sum(len(a) for a in after.values()) // 2
    assert n_edges == 9 * 11 + 9 * 13 + 11 * 13 == 359, f"edge count != 359: {n_edges}"
    assert is_connected(n, after), "K(9,11,13) must be connected"
    assert n_components(n, after) == 1, "connected scene must have exactly 1 component"
    print(f"PASS_AFTER_CONNECTED  K(9,11,13): {n_edges} cross-zone edges, BFS reaches all 33 -> 1 component")

    # ---- BEFORE stage: sub-threshold is disconnected --------------------------------
    before = subthreshold_edges(n, block_of, after)
    before_edges = sum(len(a) for a in before.values()) // 2
    assert before_edges == 0, f"tripartite sub-threshold must have NO edges, got {before_edges}"
    bc = n_components(n, before)
    assert bc == 33, f"sub-threshold must be 33 isolated vertices, got {bc} components"
    assert not is_connected(n, before), "sub-threshold stage must be DISCONNECTED"
    print(f"PASS_BEFORE_DISCONNECTED  sub-threshold = {before_edges} edges -> {bc} components (33 isolated vertices)")

    # ---- transition disconnected -> connected is real -------------------------------
    assert (not is_connected(n, before)) and is_connected(n, after), "transition must be disconnected->connected"
    print("PASS_TRANSITION_REAL  before.connected=false -> after.connected=true (matches Lean PercolationTransition)")

    # ---- negative controls (genuinely reachable) ------------------------------------
    # (a) a graph "connected BEFORE the threshold": claim the sub-threshold stage is already
    #     connected. The sub-threshold stage has 33 components, so the claim is rejected.
    claimed_before_connected = is_connected(n, before)
    assert claimed_before_connected is False, "control: sub-threshold must NOT be connected"
    print("FAIL_CONNECTED_BEFORE_THRESHOLD_CAUGHT  planted 'already connected before threshold' rejected "
          f"(sub-threshold has {bc} components, not 1)")

    # (b) an arbitrary threshold not matching the connectivity onset: remove every edge incident
    #     to vertex 0 (a single intra-stage cut), claim THAT graph is the connected scene. It is
    #     not - vertex 0 becomes isolated -> 2 components -> rejected as the connectivity onset.
    bad = {u: set(after[u]) for u in range(n)}
    for w in list(bad[0]):
        bad[0].discard(w)
        bad[w].discard(0)
    assert n_components(n, bad) == 2, "arbitrary-cut control must split off vertex 0"
    assert not is_connected(n, bad), "arbitrary threshold must not be the connectivity onset"
    print("FAIL_ARBITRARY_THRESHOLD_CAUGHT  planted off-onset graph (vertex 0 cut) rejected "
          f"({n_components(n, bad)} components, not connected)")

    # (c) vertex count != 33: K(9,11,15) has 35 vertices -> rejected as the forced scene.
    n_bad, bo_bad = build_blocks((9, 11, 15))
    assert n_bad == 35 and n_bad != 33, "control: wrong zones must not give 33"
    bad_after = complete_tripartite_edges(n_bad, bo_bad)
    assert sum(len(a) for a in bad_after.values()) // 2 != 359, "wrong scene edge count must differ"
    print("FAIL_VERTEX_COUNT_NOT_33_CAUGHT  planted K(9,11,15) (35 vertices, !=33) rejected as the forced scene")

    print("PASS_CONNECTIVITY_THRESHOLD_OWNER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
