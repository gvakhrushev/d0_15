#!/usr/bin/env python3
"""vp_frontier_dag_partition - Tier-0 frontier measurement integrity (frontier_dag.json).

Verifies that the generated frontier DAG + partition (tools/build_frontier_dag.py) is an
exact, well-formed measurement of the open frontier in CLAIM_TO_LEAN_MAP.csv:
every frontier claim lands in exactly ONE partition bucket (sole-gate / joint / external /
independent), every edge endpoint exists, every primitive is connected, and every no-go
flag is a declared kind. Measurement integrity only - closes no claim, promotes nothing.
"""
import csv
import json
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
DAG = ROOT / "03_THEORY_MAP" / "frontier_dag.json"
MD = ROOT / "03_THEORY_MAP" / "FRONTIER_PARTITION.md"
REGISTRY = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"

sys.path.insert(0, str(ROOT / "tools"))
from d0_status_model import canonical_release  # noqa: E402

NOGO_KINDS = {"wall", "witness_pair", "unclassified"}


def load_registry() -> dict[str, dict[str, str]]:
    with open(REGISTRY, encoding="utf-8") as fh:
        return {r["claim_id"]: r for r in csv.DictReader(fh) if r.get("claim_id")}


def recompute_frontier(registry: dict[str, dict[str, str]]) -> set[str]:
    out = set()
    for cid, r in registry.items():
        rel = canonical_release(r.get("release_status", ""))
        lean = r.get("lean_status", "")
        if lean == "DEPRECATED" or rel == "DEPRECATED":
            continue
        if lean == "OPEN" or rel == "PROOF-TARGET":
            out.add(cid)
    return out


def violations(payload: dict, registry: dict[str, dict[str, str]]) -> list[str]:
    """independent re-derivation of the well-formedness conditions; returns violation list."""
    out = []
    part = payload["partition"]
    frontier = recompute_frontier(registry)

    # 1. coverage: every recomputed frontier claim has a requirements entry
    reqs = part["requirements"]
    missing = frontier - set(reqs)
    if missing:
        out.append(f"frontier claims missing from partition.requirements: {sorted(missing)[:5]}")
    phantom = set(reqs) - frontier
    if phantom:
        out.append(f"partition.requirements rows that are not frontier claims: {sorted(phantom)[:5]}")

    # 2. exact partition: sole ∪ joint ∪ external ∪ independent is disjoint and covers frontier
    sole = {c for v in part["per_primitive"].values() for c in v["transitive_sole_gate"]}
    joint = set(part["joint_fronts"])
    external = set(part["external_gated"])
    independent = set(part["independent_residual"])
    buckets = [("sole", sole), ("joint", joint), ("external", external), ("independent", independent)]
    for i, (na, a) in enumerate(buckets):
        for nb, b in buckets[i + 1:]:
            inter = a & b
            if inter:
                out.append(f"buckets overlap ({na} ∩ {nb}): {sorted(inter)[:5]}")
    union = sole | joint | external | independent
    if union != frontier:
        out.append(f"bucket union != frontier (missing {sorted(frontier - union)[:5]}, "
                   f"extra {sorted(union - frontier)[:5]})")

    # 3. edges: endpoints must be registry claims or PRIM-* nodes; gates src must be PRIM-*
    node_ids = {n["id"] for n in payload["nodes"]}
    for e in payload["edges"]:
        for end in (e["src"], e["dst"]):
            if not (end in registry or end.startswith("PRIM-")):
                out.append(f"edge endpoint outside registry/primitives: {e['src']} -> {e['dst']}")
                break
        if e["type"] == "gates" and not e["src"].startswith("PRIM-"):
            out.append(f"gates edge with non-primitive src: {e['src']} -> {e['dst']}")
        if end in node_ids:
            pass  # nodes list is a view; edge endpoints validated against registry above

    # 4. every primitive node has at least one incident edge
    prims = {n["id"] for n in payload["nodes"] if n["kind"] == "primitive"}
    touched = {e["src"] for e in payload["edges"]} | {e["dst"] for e in payload["edges"]}
    isolated = prims - touched
    if isolated:
        out.append(f"isolated primitive nodes (no incident edge): {sorted(isolated)[:5]}")

    # 5. no-go flags carry a declared kind
    for c, v in payload["nogo_flags"].items():
        if v.get("kind") not in NOGO_KINDS:
            out.append(f"no-go {c} carries undeclared kind: {v.get('kind')!r}")

    # 6. counts block is honest
    cnt = payload["counts"]
    checks = {
        "frontier_claims": len(frontier),
        "joint_front_claims": len(joint),
        "external_gated": len(external),
        "independent_residual": len(independent),
        "gate_edges": sum(1 for e in payload["edges"] if e["type"] == "gates"),
    }
    for key, expect in checks.items():
        if cnt.get(key) != expect:
            out.append(f"counts.{key}={cnt.get(key)} but recomputation gives {expect}")
    return out


def main() -> int:
    print("=== vp_frontier_dag_partition  Tier-0 frontier measurement integrity ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the partition must be exact (disjoint buckets covering "
          "every OPEN/PROOF-TARGET registry row), every edge endpoint must exist in the registry "
          "or be a PRIM-* node, every primitive must be connected, every no-go flag declared; "
          "the counts block must match independent recomputation.")

    payload = json.loads(DAG.read_text(encoding="utf-8"))
    registry = load_registry()

    # positive controls
    v = violations(payload, registry)
    assert not v, "frontier DAG integrity violations: " + " | ".join(v[:6])
    print(f"PASS_PARTITION_EXACT  {payload['counts']['frontier_claims']} frontier claims in "
          f"disjoint buckets (sole+joint+external+independent), 0 violations.")

    md = MD.read_text(encoding="utf-8")
    for key, label in [("joint_front_claims", "JOINT"), ("independent_residual", "INDEPENDENT")]:
        assert f"**{payload['counts'][key]}**" in md, f"MD headline for {label} != json counts.{key}"
    print("PASS_MD_MATCHES_JSON  FRONTIER_PARTITION.md headline numbers match frontier_dag.json.")

    prims_reg = {p for p, r in payload["partition"]["per_primitive"].items()}
    assert len(prims_reg) == payload["counts"]["primitives"], "primitive count drift"
    print(f"PASS_PRIMITIVES_CONNECTED  {len(prims_reg)} primitives, none isolated.")

    # negative controls: planted flaws must be caught by the same checker
    import copy
    m1 = copy.deepcopy(payload)
    m1["edges"].append({"src": "D0-PHANTOM-CLAIM-999", "dst": "D0-SCENE-001", "type": "blocks",
                        "provenance": "planted"})
    assert violations(m1, registry), "control: a phantom edge endpoint must be detected"
    print("FAIL_PHANTOM_EDGE_REJECTED  an edge to a claim absent from the registry is caught.")

    m2 = copy.deepcopy(payload)
    if m2["partition"]["independent_residual"]:
        dropped = m2["partition"]["independent_residual"].pop()
        del m2["partition"]["requirements"][dropped]
        assert violations(m2, registry), "control: a frontier claim dropped from the partition must be detected"
        print("FAIL_DROPPED_CLAIM_REJECTED  removing a frontier claim from the partition is caught.")

    m3 = copy.deepcopy(payload)
    for c, v3 in m3["nogo_flags"].items():
        v3["kind"] = "definitely-a-wall-trust-me"
        break
    assert violations(m3, registry), "control: an undeclared no-go kind must be detected"
    print("FAIL_UNDECLARED_NOGO_KIND_REJECTED  a no-go flag outside {wall,witness_pair,unclassified} is caught.")

    m4 = copy.deepcopy(payload)
    m4["counts"]["independent_residual"] += 1
    assert violations(m4, registry), "control: an inflated counts block must be detected"
    print("FAIL_INFLATED_COUNTS_REJECTED  a counts block that disagrees with recomputation is caught.")

    print("PASS_FRONTIER_DAG_PARTITION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
