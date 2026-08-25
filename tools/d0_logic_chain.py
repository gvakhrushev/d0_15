#!/usr/bin/env python3
"""d0_logic_chain.py — the derivation chain of the corpus, built from what actually depends on what.

The registry is a flat list: every claim names its module, its cert, its status. What it never
recorded is the ORDER OF DERIVATION — which claim stands on which. This tool builds that chain
from the one machine-truthful source available: the Lean `import` graph.

    claim --(registry)--> lean module --(imports)--> lean modules --(registry)--> claims

From that DAG it computes, per claim:

  genesis      the claim imports no other D0 module (it rests on Mathlib alone) — a block 0
  depth        longest derivation path from a genesis block to this claim
  carries      how many DISTINCT claims transitively rest on this one (load-bearing weight)
  rests_on     how many DISTINCT claims this one transitively rests on
  content_hash sha256 of the module's normalised source (comments and blank lines stripped:
               a docstring edit must NOT invalidate downstream blocks — only real content does)
  block_hash   sha256(content_hash + sorted parent block_hashes) — the prev-hash link

`block_hash` is the integrity property the corpus lacked: edit an upstream module's CONTENT and
every downstream block hash changes, so "this claim was verified against that version of its
foundation" becomes checkable instead of assumed. Re-run after any Lean edit and diff the chain
file to see exactly which downstream claims must be re-read.

Orphans are reported, not hidden: a claim with no Lean module has no block and cannot enter the
chain (it is a Python-certified or open row); a claim whose module exists but is imported by
nothing and imports nothing is an isolated block.

Outputs 03_THEORY_MAP/D0_LOGIC_CHAIN.json (machine) and returns the model for d0_value_model.py.
Exit 0 = ok, 1 = cycle detected (a derivation cycle is a real defect), 2 = IO/usage.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
LEAN_ROOT = ROOT / "09_LEAN_FORMALIZATION"
OUT = ROOT / "03_THEORY_MAP" / "D0_LOGIC_CHAIN.json"

IMPORT_RE = re.compile(r"^\s*import\s+(D0[\w.]*)", re.M)
BLOCK_COMMENT_RE = re.compile(r"/-.*?-/", re.S)
LINE_COMMENT_RE = re.compile(r"--.*")


def module_path(mod: str) -> Path:
    """`D0.Foo.Bar` -> 09_LEAN_FORMALIZATION/D0/Foo/Bar.lean"""
    return LEAN_ROOT / (mod.replace(".", "/") + ".lean")


def normalised_source(text: str) -> str:
    """Strip comments and blank lines: a docstring edit must not invalidate downstream hashes."""
    text = BLOCK_COMMENT_RE.sub("", text)
    text = LINE_COMMENT_RE.sub("", text)
    return "\n".join(ln.rstrip() for ln in text.splitlines() if ln.strip())


def load_registry() -> list[dict]:
    with REGISTRY.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def build() -> dict:
    rows = load_registry()

    # claim -> module (a row may name several modules; take every one it declares)
    claim_modules: dict[str, list[str]] = {}
    module_claims: dict[str, list[str]] = defaultdict(list)
    for r in rows:
        cid = (r.get("claim_id") or "").strip()
        if not cid:
            continue
        mods = [m.strip() for m in re.split(r"[;, ]+", r.get("lean_module") or "") if m.strip().startswith("D0")]
        claim_modules[cid] = mods
        for m in mods:
            module_claims[m].append(cid)

    # module -> imported D0 modules (only those that exist on disk)
    mod_of_path = {mp: mp.relative_to(LEAN_ROOT).with_suffix("").as_posix().replace("/", ".")
                   for mp in LEAN_ROOT.rglob("D0/**/*.lean")}
    module_imports: dict[str, list[str]] = {}
    module_source: dict[str, str] = {}
    for path, mod in mod_of_path.items():
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        module_source[mod] = normalised_source(text)
        module_imports[mod] = sorted({m for m in IMPORT_RE.findall(text) if m != mod})

    # claim DAG: claim A -> claim B when A's module (transitively at one hop) imports B's module
    # Claims sharing a module are SIBLINGS (same block), never ancestor/descendant of each other —
    # without this the DAG acquires spurious 2-cycles wherever two claims are co-hosted.
    parents: dict[str, set[str]] = defaultdict(set)
    children: dict[str, set[str]] = defaultdict(set)
    for cid, mods in claim_modules.items():
        own = set(mods)
        for m in mods:
            for imp in module_imports.get(m, []):
                for pcid in module_claims.get(imp, []):
                    if pcid != cid and not (own & set(claim_modules.get(pcid, []))):
                        parents[cid].add(pcid)
                        children[pcid].add(cid)

    chained = [c for c in claim_modules if claim_modules[c]]

    # topological order over the claim DAG
    indeg = {c: len(parents[c] & set(chained)) for c in chained}
    queue = deque(sorted(c for c in chained if indeg[c] == 0))
    topo: list[str] = []
    while queue:
        c = queue.popleft()
        topo.append(c)
        for ch in sorted(children[c]):
            if ch in indeg:
                indeg[ch] -= 1
                if indeg[ch] == 0:
                    queue.append(ch)
    cycle = len(topo) != len(chained)

    # depth + hashes in topological order
    depth: dict[str, int] = {}
    block_hash: dict[str, str] = {}
    content_hash: dict[str, str] = {}
    for c in topo:
        src = "\n".join(module_source.get(m, "") for m in claim_modules[c])
        content_hash[c] = hashlib.sha256(src.encode()).hexdigest()
        ps = sorted(p for p in parents[c] if p in block_hash)
        depth[c] = 0 if not ps else 1 + max(depth[p] for p in ps)
        seed = content_hash[c] + "".join(block_hash[p] for p in ps)
        block_hash[c] = hashlib.sha256(seed.encode()).hexdigest()

    # transitive weight: how many distinct claims rest on this one
    carries: dict[str, int] = {}
    for c in reversed(topo):
        acc: set[str] = set()
        for ch in children[c]:
            if ch in carries_set_cache:
                acc |= carries_set_cache[ch]
            if ch in chained:
                acc.add(ch)
        carries_set_cache[c] = acc
        carries[c] = len(acc)

    rests_on: dict[str, int] = {}
    for c in topo:
        acc: set[str] = set()
        for p in parents[c]:
            if p in rests_cache:
                acc |= rests_cache[p]
            if p in chained:
                acc.add(p)
        rests_cache[c] = acc
        rests_on[c] = len(acc)

    blocks = {}
    for c in chained:
        blocks[c] = {
            "claim_id": c,
            "modules": claim_modules[c],
            "genesis": not parents[c],
            "depth": depth.get(c, -1),
            "carries": carries.get(c, 0),
            "rests_on": rests_on.get(c, 0),
            "parents": sorted(parents[c]),
            "content_hash": content_hash.get(c, ""),
            "block_hash": block_hash.get(c, ""),
        }

    orphans = sorted(c for c in claim_modules if not claim_modules[c])
    return {
        "generated_from": ["09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv", "09_LEAN_FORMALIZATION/D0/**/*.lean"],
        "summary": {
            "claims_total": len(claim_modules),
            "claims_chained": len(chained),
            "claims_unchained": len(orphans),
            "genesis_blocks": sum(1 for b in blocks.values() if b["genesis"]),
            "max_depth": max((b["depth"] for b in blocks.values()), default=0),
            "cycle_detected": cycle,
        },
        "blocks": blocks,
        "unchained": orphans,
    }


carries_set_cache: dict[str, set[str]] = {}
rests_cache: dict[str, set[str]] = {}


def main() -> int:
    try:
        model = build()
    except OSError as exc:
        print(f"IO error: {exc}", file=sys.stderr)
        return 2
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(model, indent=2, sort_keys=True), encoding="utf-8")
    s = model["summary"]
    print(f"chain: {s['claims_chained']} chained / {s['claims_total']} claims, "
          f"{s['genesis_blocks']} genesis blocks, max depth {s['max_depth']}, "
          f"{s['claims_unchained']} unchained")
    if s["cycle_detected"]:
        print("CYCLE DETECTED in the derivation DAG — a claim transitively depends on itself.", file=sys.stderr)
        return 1
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
