#!/usr/bin/env python3
"""build_frontier_dag.py - Tier-0 frontier measurement: blocker->blocked dependency DAG + partition.

Reads the canonical registry (CLAIM_TO_LEAN_MAP.csv) plus the 04_VERIFICATION blocker
atlases and no-go atlases, builds a typed directed graph

    primitive -[gates]-> claim        (claim names the primitive as its missing input)
    claim     -[blocks]-> claim       (depends_on / prose "awaits" conventions)

and computes, per PRIM-* primitive, the transitive set of frontier claims that become
provable-conditional-on-that-primitive, the joint (multi-primitive) fronts, and the
independent residual. Emits:

    03_THEORY_MAP/frontier_dag.json
    03_THEORY_MAP/FRONTIER_PARTITION.md

Measurement only: no registry statuses are read-modified, no claim is promoted or demoted.
Ambiguous prose references are queued for human review, never silently counted as blocks.
Verified by 05_CERTS/vp_frontier_dag_partition.py (can-fail cert).
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from d0_status_model import canonical_release  # noqa: E402
from sync_theory_status_map import read_csv, split_values  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
VERIF = ROOT / "04_VERIFICATION"
THEORY_DIR = ROOT / "03_THEORY_MAP"
OUT_JSON = THEORY_DIR / "frontier_dag.json"
OUT_MD = THEORY_DIR / "FRONTIER_PARTITION.md"

PRIM_RE = re.compile(r"PRIM-[A-Z0-9]+(?:-[A-Z0-9]+)*")
CLAIM_RE = re.compile(r"D0-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}|CVFT-F\d+")
NOGO_ATLASES = ["D0_FINAL_NO_GO_ATLAS.md", "VNEXT2_SCENE_NATIVE_NO_GO_ATLAS.md", "TOTAL_NO_GO_ATLAS.md"]
PRIMITIVES_CSV = VERIF / "TOTAL_EXTENSION_PRIMITIVES.csv"

# prose conventions in registry notes (registry agent's verified list)
BLOCKED_BY_MARKERS = ("awaits", "await ", "blocked by", "stays proof-target", "stay proof-target",
                      "gap narrowed from", "pending ", "requires ", "needs ")
DEPENDS_ON_MARKERS = ("owned by", "proved by", "closed by", "cert by", "backed by")
# structural rule exceptions: a frontier row citing a NO-GO with these markers is NOT obstructed by it
NOGO_REF_EXCEPTIONS = ("supersede", "replaced", "replaces", "retired", "deprecat", "revives", "reopen")
# a frontier row whose own MISSING-artifact clause names an external leg is external-gated
# (G2 quarantine candidate); the corpus writes the marker in several forms:
#   "EXACT-MISSING:", "MISSING (exact):", "MISSING ARTIFACT (named, exact):", "EXACT MISSING ARTIFACT:"
EXACT_MISSING_RE = re.compile(
    r"(?:EXACT[- ]MISSING(?:\s+ARTIFACTS?)?|MISSING(?:\s+ARTIFACTS?)?\s*\([^)]*exact[^)]*\)|MISSING\s*\(exact\))\s*:?"
    r"([^|]{0,240})", re.IGNORECASE | re.DOTALL)
EXTERNAL_RE = re.compile(r"\bexternal\b|\bpassport\b", re.IGNORECASE)

# no-go "proved:" phrasing -> wall vs witness-pair
WALL_RE = re.compile(r"^\s*(every|all|no |none|any)\b", re.IGNORECASE)
WITNESS_RE = re.compile(r"(two|three|>=\s*2)\s+(admissible|companions?|refinement|famil)|give (distinct|inequivalent)|maps? agree .* but differ", re.IGNORECASE)


def load_registry() -> dict[str, dict[str, str]]:
    rows = read_csv(REGISTRY)
    return {r["claim_id"]: r for r in rows if r.get("claim_id")}


def is_frontier(row: dict[str, str]) -> bool:
    rel = canonical_release(row.get("release_status", ""))
    lean = row.get("lean_status", "")
    if lean == "DEPRECATED" or rel == "DEPRECATED":
        return False
    return lean == "OPEN" or rel == "PROOF-TARGET"


def is_nogo(row: dict[str, str]) -> bool:
    rel = canonical_release(row.get("release_status", ""))
    return rel.startswith("NO-GO") or rel == "NO_GO_PROVED"


def extract_registry_edges(registry: dict[str, dict[str, str]]):
    """notes-field extraction: claim->primitive gates + claim->claim edges.

    Two edge rules:
      prose rule      - convention markers near the mention (awaits/owned by/...)
      structural rule - a FRONTIER row citing a NO-GO row is obstructed by it
                        (status-based, no prose guessing; supersede/retire refs excepted)
    Anything else goes to the review queue, never silently into blocks.
    """
    gates, blocks, review = [], [], []
    external_gated: dict[str, str] = {}
    for cid, row in sorted(registry.items()):
        notes = row.get("notes", "")
        low = notes.lower()
        for prim in sorted(set(PRIM_RE.findall(notes))):
            gates.append({"src": prim, "dst": cid, "type": "gates", "provenance": "registry:notes"})
        if is_frontier(row):
            m = EXACT_MISSING_RE.search(notes)
            if m and EXTERNAL_RE.search(m.group(1)):
                external_gated[cid] = m.group(1).strip()[:160]
            elif "-PASSPORT-" in cid:
                # observational passports are external by construction (data, not math)
                external_gated[cid] = "observational passport: closes only against external data"
        for ref in sorted(set(CLAIM_RE.findall(notes))):
            if ref == cid or ref not in registry:
                continue
            # classify by nearest convention marker in a +-90 char window around the mention
            idx = low.find(ref.lower())
            window = low[max(0, idx - 90): idx + len(ref) + 90]
            if any(m in window for m in BLOCKED_BY_MARKERS):
                blocks.append({"src": ref, "dst": cid, "type": "blocks", "provenance": "registry:notes"})
            elif any(m in window for m in DEPENDS_ON_MARKERS):
                blocks.append({"src": ref, "dst": cid, "type": "depends_on", "provenance": "registry:notes"})
            elif (is_frontier(row) and is_nogo(registry[ref])
                  and not any(m in window for m in NOGO_REF_EXCEPTIONS)):
                blocks.append({"src": ref, "dst": cid, "type": "blocks",
                               "provenance": "registry:nogo-ref-rule"})
            else:
                review.append({"src": ref, "dst": cid, "context": window.strip()[:160]})
    return gates, blocks, review, external_gated


def load_atlas_edges():
    """structured depends_on / exact_missing_primitive columns across *BLOCKERS*.csv."""
    gates, blocks, meta = [], [], []
    for path in sorted(VERIF.glob("*BLOCKERS*.csv")):
        rows = read_csv(path)
        src_name = f"atlas:{path.name}"
        for r in rows:
            # F-01 guard: ROOT_OPERATOR_COMPLETION_BLOCKERS.csv has no claim_id column; its
            # 'blocker' field is FREE TEXT — accept only well-formed claim ids as node sources
            cid = r.get("claim_id") or r.get("blocker") or ""
            if not cid or not CLAIM_RE.fullmatch(cid.strip()):
                continue
            cid = cid.strip()
            for prim in sorted(set(PRIM_RE.findall(" ".join(r.values())))):
                gates.append({"src": prim, "dst": cid, "type": "gates", "provenance": src_name})
            for dep in split_values(r.get("depends_on", "")):
                for dep_id in CLAIM_RE.findall(dep):
                    if dep_id != cid:
                        blocks.append({"src": dep_id, "dst": cid, "type": "blocks", "provenance": src_name})
            meta.append({"claim": cid, "atlas": path.name, "status": r.get("status", "")})

    # completion boards: structured primitive -> downstream-claim edges
    root_board = VERIF / "ROOT_OPERATOR_COMPLETION_BOARD.csv"
    if root_board.exists():
        for r in read_csv(root_board):
            prims = PRIM_RE.findall(r.get("exact missing primitive", ""))
            downstream = CLAIM_RE.findall(r.get("downstream claims unlocked", ""))
            for prim in prims:
                for c in downstream:
                    gates.append({"src": prim, "dst": c, "type": "gates",
                                  "provenance": "atlas:ROOT_OPERATOR_COMPLETION_BOARD.csv"})
    lane_board = VERIF / "TOTAL_CLOSURE_BOARD.csv"
    if lane_board.exists():
        for r in read_csv(lane_board):
            prims = PRIM_RE.findall(r.get("minimum_new_primitive", ""))
            owners = CLAIM_RE.findall(r.get("owner(s)", ""))
            for prim in prims:
                for c in owners:
                    gates.append({"src": prim, "dst": c, "type": "gates",
                                  "provenance": "atlas:TOTAL_CLOSURE_BOARD.csv"})
    return gates, blocks, meta


def load_primitive_catalog() -> dict[str, dict[str, str]]:
    catalog = {}
    if PRIMITIVES_CSV.exists():
        for r in read_csv(PRIMITIVES_CSV):
            pid = r.get("primitive_id", "")
            if pid:
                catalog[pid] = {
                    "completion_class": r.get("admissible_completion_class", ""),
                    "lane": r.get("lane", ""),
                    "mathematical_type": r.get("mathematical_type", ""),
                }
    return catalog


def parse_nogo_flags():
    """per no-go claim: wall | witness_pair | unclassified from the 'proved:' phrasing,
    plus gate edges primitive -> no-go claim from the 'completion class:' lines
    (some NO-GO registry rows have empty notes; the atlas is their only primitive source)."""
    flags, gate_edges = {}, []
    for name in NOGO_ATLASES:
        path = VERIF / name
        if not path.exists():
            continue
        current = None
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("## "):
                m = CLAIM_RE.search(line)
                current = m.group(0) if m else None
            elif current and "completion class:" in line.lower():
                for prim in sorted(set(PRIM_RE.findall(line))):
                    gate_edges.append({"src": prim, "dst": current, "type": "gates",
                                       "provenance": f"nogo-atlas:{name}"})
            elif current and line.strip().lower().startswith("- proved:"):
                proved = line.split(":", 1)[1].strip()
                if WITNESS_RE.search(proved):
                    kind = "witness_pair"
                elif WALL_RE.search(proved):
                    kind = "wall"
                else:
                    kind = "unclassified"
                # first atlas wins; conflicts recorded rather than overwritten
                if current in flags and flags[current]["kind"] != kind:
                    flags[current]["conflict"] = f"{flags[current]['atlas']}={flags[current]['kind']} vs {name}={kind}"
                else:
                    flags[current] = {"kind": kind, "proved": proved, "atlas": name}
    return flags, gate_edges


def dedupe(edges: list[dict]) -> list[dict]:
    seen, out = set(), []
    for e in edges:
        key = (e["src"], e["dst"], e["type"])
        if key not in seen:
            seen.add(key)
            out.append(e)
    return out


def transitive_requirements(frontier: set[str], gates: list[dict], blocks: list[dict],
                            unresolved: set[str]) -> dict[str, frozenset]:
    """fixpoint: R(X) = direct primitives of X  ∪  R(Y) for every unresolved Y with Y-blocks->X."""
    direct = defaultdict(set)
    for e in gates:
        direct[e["dst"]].add(e["src"])
    preds = defaultdict(set)
    for e in blocks:
        if e["type"] == "blocks" and e["src"] in unresolved:
            preds[e["dst"]].add(e["src"])
    req = {c: set(direct[c]) for c in frontier}
    changed = True
    while changed:
        changed = False
        for c in frontier:
            for p in preds[c]:
                extra = req.get(p, direct[p]) - req[c]
                if extra:
                    req[c] |= extra
                    changed = True
    return {c: frozenset(v) for c, v in req.items()}


def main() -> int:
    registry = load_registry()
    frontier = {c for c, r in registry.items() if is_frontier(r)}
    nogos = {c for c, r in registry.items() if is_nogo(r)}

    r_gates, r_blocks, review, external_gated = extract_registry_edges(registry)
    a_gates, a_blocks, atlas_meta = load_atlas_edges()
    catalog = load_primitive_catalog()
    nogo_flags, nogo_gates = parse_nogo_flags()
    a_gates = a_gates + nogo_gates

    # keep only edges whose claim endpoints exist in the canonical registry
    def known(e):
        ok_dst = e["dst"] in registry or e["dst"].startswith("PRIM-")
        ok_src = e["src"] in registry or e["src"].startswith("PRIM-")
        return ok_src and ok_dst
    dropped = [e for e in a_gates + a_blocks if not known(e)]
    a_gates = [e for e in a_gates if known(e)]
    a_blocks = [e for e in a_blocks if known(e)]

    gates = dedupe(r_gates + a_gates)
    blocks = dedupe(r_blocks + a_blocks)

    # desync report: gate edges present in exactly one source
    rg = {(e["src"], e["dst"]) for e in r_gates}
    ag = {(e["src"], e["dst"]) for e in a_gates}
    desyncs = (
        [{"edge": f"{s} -> {d}", "issue": "in atlas, absent from registry notes"} for s, d in sorted(ag - rg)]
        + [{"edge": f"{s} -> {d}", "issue": "in registry notes, absent from all atlases"} for s, d in sorted(rg - ag)]
        + [{"edge": f"{e['src']} -> {e['dst']}", "issue": f"atlas endpoint not in registry ({e['provenance']})"} for e in dropped]
        # registry-internal: lean says OPEN while release carries a positive closure status
        + [{"edge": c, "issue": f"lean_status=OPEN but release_status={canonical_release(r.get('release_status',''))} (status inflation candidate)"}
           for c, r in sorted(registry.items())
           if r.get("lean_status") == "OPEN"
           and canonical_release(r.get("release_status", "")) in ("CERT-CLOSED", "CORE-FORMALIZED")]
    )

    # primitives propagate through frontier claims AND through no-gos: a no-go blocking a
    # frontier claim names (as its admissible completion class) exactly the object whose
    # absence keeps that claim open — regardless of the wall/witness-pair trust distinction
    unresolved = frontier | nogos
    reqs = transitive_requirements(frontier, gates, blocks, unresolved)

    primitives = sorted({e["src"] for e in gates if e["src"].startswith("PRIM-")})
    per_prim = {
        p: {
            "direct": sorted(c for c in frontier if any(e["src"] == p and e["dst"] == c for e in gates)),
            "transitive_sole_gate": sorted(c for c in frontier if reqs[c] == frozenset({p})),
        }
        for p in primitives
    }
    joint = sorted(c for c in frontier if len(reqs[c]) >= 2)
    external = sorted(c for c in frontier if not reqs[c] and c in external_gated)
    independent = sorted(c for c in frontier if not reqs[c] and c not in external_gated)

    nodes = (
        [{"id": c, "kind": "claim", "frontier": c in frontier, "nogo": c in nogos,
          "lean_status": registry[c].get("lean_status", ""),
          "release_status": canonical_release(registry[c].get("release_status", "")),
          **({"nogo_kind": nogo_flags[c]["kind"], "nogo_proved": nogo_flags[c]["proved"]} if c in nogo_flags else {})}
         for c in sorted(frontier | nogos | {e["src"] for e in blocks} | {e["dst"] for e in blocks + gates})
         if c in registry]
        + [{"id": p, "kind": "primitive", **catalog.get(p, {})} for p in primitives]
    )

    THEORY_DIR.mkdir(exist_ok=True)
    payload = {
        "generated_by": "tools/build_frontier_dag.py",
        "sources": {"registry": str(REGISTRY.relative_to(ROOT)), "registry_rows": len(registry),
                    "atlas_files": sorted(p.name for p in VERIF.glob("*BLOCKERS*.csv")),
                    "nogo_atlases": NOGO_ATLASES},
        "counts": {"frontier_claims": len(frontier), "nogo_claims": len(nogos),
                   "primitives": len(primitives), "gate_edges": len(gates),
                   "block_edges": len(blocks), "review_queue": len(review),
                   "desyncs": len(desyncs),
                   "joint_front_claims": len(joint), "external_gated": len(external),
                   "independent_residual": len(independent)},
        "nodes": nodes,
        "edges": sorted(gates + blocks, key=lambda e: (e["src"], e["dst"], e["type"])),
        "partition": {"per_primitive": per_prim, "joint_fronts": joint,
                      "external_gated": {c: external_gated[c] for c in external},
                      "independent_residual": independent,
                      "requirements": {c: sorted(reqs[c]) for c in sorted(frontier)}},
        "nogo_flags": {c: v for c, v in sorted(nogo_flags.items())},
        "desyncs": desyncs,
        "review_queue": review,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    # ---- human-readable partition ----
    sole = {p: v["transitive_sole_gate"] for p, v in per_prim.items()}
    dominating = sorted(sole.items(), key=lambda kv: -len(kv[1]))
    lines = [
        "# Frontier Partition (generated by tools/build_frontier_dag.py — measurement, not closure)",
        "",
        f"Frontier claims (OPEN / PROOF-TARGET): **{len(frontier)}**  ·  primitives named: **{len(primitives)}**",
        f"Gate edges: {len(gates)}  ·  block edges: {len(blocks)}  ·  desyncs: {len(desyncs)}  ·  review queue: {len(review)}",
        "",
        "## Headline",
        "",
        f"- claims gated by exactly ONE primitive: **{sum(len(v) for v in sole.values())}**",
        f"- claims on JOINT fronts (>=2 primitives): **{len(joint)}**",
        f"- EXTERNAL-gated (own EXACT-MISSING names an external leg/passport): **{len(external)}**",
        f"- INDEPENDENT residual (no primitive, no external marker): **{len(independent)}**",
        "",
        "## Per-primitive collapse sets (transitive, sole-gate)",
        "",
        "| primitive | lane | sole-gate claims | direct mentions | completion class |",
        "|---|---|--:|--:|---|",
    ]
    for p, cs in dominating:
        cat = catalog.get(p, {})
        lines.append(f"| `{p}` | {cat.get('lane','')} | {len(cs)} | {len(per_prim[p]['direct'])} | {cat.get('completion_class','')[:80]} |")
    lines += ["", "## Joint fronts (claim -> required primitives)", ""]
    for c in joint:
        lines.append(f"- `{c}` <- {', '.join(f'`{p}`' for p in sorted(reqs[c]))}")
    lines += ["", "## External-gated (frontier claims whose own EXACT-MISSING names an external leg — G2 quarantine candidates)", ""]
    for c in external:
        lines.append(f"- `{c}`: {external_gated[c]}")
    lines += ["", "## Independent residual (frontier claims naming NO primitive and NO external marker)", ""]
    for c in independent:
        row = registry[c]
        lines.append(f"- `{c}` ({row.get('lean_status','')}/{canonical_release(row.get('release_status',''))})")
    lines += ["", "## No-go wall-vs-witness flags", ""]
    for c, v in sorted(nogo_flags.items()):
        mark = {"wall": "WALL", "witness_pair": "WITNESS-PAIR (hiding-place risk)", "unclassified": "UNCLASSIFIED"}[v["kind"]]
        lines.append(f"- `{c}`: **{mark}** — proved: {v['proved'][:110]}")
    lines += ["", "## Desyncs (registry vs atlases)", ""]
    lines += [f"- {d['edge']}: {d['issue']}" for d in desyncs] or ["- none"]
    lines += ["", f"## Review queue ({len(review)} ambiguous prose references — NOT counted as blocks)", ""]
    lines += [f"- `{r['src']}` ~ `{r['dst']}`: …{r['context']}…" for r in review[:60]]
    if len(review) > 60:
        lines.append(f"- … and {len(review) - 60} more (see frontier_dag.json)")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"frontier={len(frontier)} primitives={len(primitives)} gate_edges={len(gates)} "
          f"block_edges={len(blocks)} sole={sum(len(v) for v in sole.values())} joint={len(joint)} "
          f"external={len(external)} independent={len(independent)} desyncs={len(desyncs)} review={len(review)}")
    print(f"wrote {OUT_JSON.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
