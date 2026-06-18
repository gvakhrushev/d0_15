#!/usr/bin/env python3
"""D0 critical-collapse DSS echo-lattice bridge — INTERPRETIVE cross-reference to an external GR result.

This is a one-directional BRIDGE (CORE_BRIDGE_SPLIT), NOT a data passport: it CITES the external
analytic result arXiv:2601.14358 (PRL 2026, analytic large-D discretely self-similar
Einstein-massless-Klein-Gordon solutions) and records how D0's echo-lattice / terminal-archive-boundary
picture reads it. It does NOT fetch, hash-pin, or independently re-derive the paper; it claims no D0
numeric prediction and confronts no measurement.

(Earlier this cert printed `arXiv source pinned: hash=<sha256 of a self-typed "(simulated fetch)"
string>` for three artifacts -- fabricated provenance, since each hash depended on nothing real. Those
fake-pinning lines are removed; the external result is CITED, not pinned. The one real check kept is
that the local manifest exists and cites the same arXiv id.)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "08_PASSPORTS" / "CriticalCollapseDSS" / "dss_prl2026_manifest.json"

ARXIV_ID = "2601.14358"
DOI = "10.1103/qgl5-5l3t"
NOTEBOOK = "NNNLOLargeD.nb"
EXPECTED_TITLE = "Analytic discrete self-similar solutions of Einstein-Klein-Gordon at large D"

# external claims, as STATED by the cited paper (cited, not independently verified here)
CITED_CLAIMS = [
    "closed analytic infinite family of DSS solutions",
    "Einstein-massless-Klein-Gordon system",
    "large-D expansion",
    "self-similar horizon (SSH) as null surface",
    "spacetime-crystal interpretation (lattice vector timelike / spacelike / lightlike)",
    "NLO consistency / convexity / SSH constraints filter periodic functions",
    "echoing period Delta appears; not all LO functions survive NLO",
]
# D0-side interpretive readings (the bridge content; no numeric prediction)
D0_READINGS = [
    "echo lattice at critical threshold -> finite log-time recurrence (D0)",
    "SSH = capacity-null boundary (D0 terminal archive boundary)",
    "NLO admissibility = no-go filter on illegal critical readout modes",
]


def run_certificate() -> int:
    print("--- D0 CRITICAL-COLLAPSE DSS ECHO-LATTICE BRIDGE (interpretive cross-reference, not a data passport) ---")
    print(f"CITES (not fetched/pinned): arXiv:{ARXIV_ID}  DOI:{DOI}  notebook:{NOTEBOOK}")
    print(f"  title: {EXPECTED_TITLE}")

    # ---- the one real can-FAIL check: the local manifest must exist AND cite this arXiv id ----
    assert MANIFEST.exists(), f"DSS manifest missing: {MANIFEST}"
    mtext = MANIFEST.read_text(encoding="utf-8")
    assert ARXIV_ID in mtext, f"manifest must cite the bridged source arXiv:{ARXIV_ID}"
    print(f"PASS_MANIFEST_CITES_SOURCE  dss_prl2026_manifest.json present and cites arXiv:{ARXIV_ID} "
          "(a wrong/absent manifest FAILs this assert)")

    print("[external, CITED -- the paper's stated claims, not independently re-derived here]:")
    for c in CITED_CLAIMS:
        print(f"  - {c}")
    print("[D0 reading -- interpretive bridge, no numeric prediction]:")
    for d in D0_READINGS:
        print(f"  - {d}")
    print("  D0-GRAV-DSS-001/002/003/004 bridges recorded.")

    print("SKIP_DSS_NOTEBOOK_REPRODUCTION_TOOL_REQUIRED  notebook repro needs a local Wolfram engine; "
          "the GR content stays externally owned, CITED not re-derived")

    results = {
        "status": "BRIDGE_RECORDED_CRITICAL_COLLAPSE_DSS_ECHO_LATTICE",
        "external_owner": {"arxiv": ARXIV_ID, "doi": DOI, "title": EXPECTED_TITLE, "notebook": NOTEBOOK,
                           "provenance": "CITED, not fetched/hash-pinned"},
        "cited_claims": CITED_CLAIMS,
        "d0_readings": D0_READINGS,
        "notebook_repro": "SKIP_DSS_NOTEBOOK_REPRODUCTION_TOOL_REQUIRED",
    }
    (Path(__file__).with_suffix(".results.json")).write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("PASS_CRITICAL_COLLAPSE_DSS_ECHO_LATTICE_BRIDGE")  # the interpretive bridge is recorded honestly
    return 0


if __name__ == "__main__":
    raise SystemExit(run_certificate())
