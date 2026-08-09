#!/usr/bin/env python3
"""check_dependency_resolution.py — how much of the corpus's dependency structure is actually known.

## The gap this measures

The attack queue is ordered by LOAD — how many claims presuppose a given one. Load is computed from
conceptual edges, and those come from two sources of very different quality:

* **evidence-backed per-claim edges** (`03_THEORY_MAP/D0_PRESUPPOSITION_EDGES.json`), each carrying a
  quoted reason — these attribute load to a specific claim;
* **section-level co-citation**, the fallback — every claim owning a section inherits the *same*
  dependents, so co-owners share one load that belongs to the section, not to any of them.

A fragile joint whose load is shared is not a target: it is an unresolved sector wearing several
names. Four claims tied at the top of the queue can be one thing, and the queue cannot tell you
which of the four to attack.

Two refinements were tried and rejected, both recorded so they are not retried blindly:

1. **proximity** — attributing to each claim the ids near its own mentions. Rejected: proximity is
   symmetric, so it emits edges both ways, dense claim listings become near-cliques, the citation
   graph collapses to one strongly-connected component and every load degenerates to the same
   number. A dependency edge needs an asymmetric signal.
2. **dependency language** — mining "owned by X", "reuses X", "upstream X" and similar. Measured
   across all books: **34 marked citations in total.** The prose does not carry per-claim dependency
   at scale; it carries section-level co-citation. So this cannot resolve the gap either.

The conclusion is about the corpus, not the parser: **dependency is not an authored field.** Until it
is, load stays attributed only where evidence edges exist. This guard reports the coverage so the
gap is a tracked number instead of a silent one, and so that adding evidence edges shows up as
progress.

Exit 0 always (report-only by default); `--min-coverage P` fails below P percent for CI use.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCH = ROOT / "03_THEORY_MAP" / "D0_ARCHITECTURE.json"
EDGES = ROOT / "03_THEORY_MAP" / "D0_PRESUPPOSITION_EDGES.json"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min-coverage", type=float, default=None,
                    help="fail if fragile-joint attribution falls below this percentage")
    args = ap.parse_args()

    if not ARCH.exists():
        print("run tools/d0_architecture.py first", file=sys.stderr)
        return 2
    arch = json.loads(ARCH.read_text(encoding="utf-8"))
    rows = arch["rows"]
    n_edges = 0
    if EDGES.exists():
        n_edges = len(json.loads(EDGES.read_text(encoding="utf-8")).get("edges", []))

    frag = [r for r in rows if r["kind"] == "FRAGILE-JOINT"]
    pill = [r for r in rows if r["kind"] == "PILLAR"]
    attributed = [r for r in frag if r["resolution"] == "claim"]
    shared = [r for r in frag if r["resolution"] == "section"]
    cov = 100.0 * len(attributed) / len(frag) if frag else 100.0

    print(f"evidence-backed per-claim edges : {n_edges}")
    print(f"fragile joints                  : {len(frag)}")
    print(f"  load attributed to the claim  : {len(attributed)}  ({cov:.0f}%)")
    print(f"  load still shared with section: {len(shared)}")
    print(f"pillars (load-bearing, m>=2)    : {len(pill)}")

    if shared:
        by_cluster: dict[str, list[str]] = {}
        for r in shared:
            by_cluster.setdefault(r["cluster"] or "(none)", []).append(r["claim_id"])
        worst = sorted(by_cluster.items(), key=lambda kv: -len(kv[1]))[:5]
        print("\nlargest unresolved sectors (one shared load, several names):")
        for sec, members in worst:
            print(f"  {len(members)}x  {sec}")
            for m in members[:4]:
                print(f"        {m}")

    print("\nTo raise coverage, add evidence-backed edges to "
          "03_THEORY_MAP/D0_PRESUPPOSITION_EDGES.json — each with a quoted reason. Proximity and "
          "dependency-language mining were both tried and rejected; see this module's docstring.")

    if args.min_coverage is not None and cov < args.min_coverage:
        print(f"\nFAIL: attribution coverage {cov:.0f}% < required {args.min_coverage:.0f}%",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
