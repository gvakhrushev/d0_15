#!/usr/bin/env python3
"""D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001 (owner manifest) - indirect route is PROOF-TARGET.

The direct raw-graph->decimal route is retired by no-go (D0-BARE-GRAPH-DECIMAL-NOGO-001). The indirect
route (finite Green function over the shell torus -> ramification/Puiseux branch indices -> exact
coefficient row) is the only admissible positive route, and its operator+extraction are NOT yet built.
This manifest verifies the honest open state with the exact missing artifacts named.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"


def main() -> int:
    print("=== D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001  owner manifest (PROOF-TARGET, exact missing artifact) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: direct route no-go'd; the indirect Green/Puiseux route is the only admissible "
          "positive route and its operator+extraction are the named gap")
    rows = {r["claim_id"]: r for r in csv.DictReader(CSV.open(encoding="utf-8"))}

    def st(c):
        return rows.get(c, {}).get("release_status")

    assert st("D0-BARE-GRAPH-DECIMAL-NOGO-001") in ("NO-GO", "NO_GO_PROVED"), "the direct route must stay no-go'd"
    print("PASS_DIRECT_ROUTE_BLOCKED  D0-BARE-GRAPH-DECIMAL-NOGO-001 = NO-GO (direct raw-graph->decimal forbidden)")
    assert st("D0-LEPTON-002") == "CERT-CLOSED" and "HYP" in rows["D0-LEPTON-002"]["notes"], "lepton decimals must stay HYP"
    print("PASS_DECIMALS_STAY_HYP  D0-LEPTON-002 CERT-CLOSED with decimals HYP (never THE)")

    me = rows.get("D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001")
    assert me is not None and me["release_status"] == "PROOF-TARGET", "the indirect owner must be PROOF-TARGET"
    note = me["notes"].lower()
    for tok in ("green function", "puiseux", "missing"):
        assert tok in note, f"note must name the missing-artifact token {tok!r}"
    print("PASS_OWNER_PROOF_TARGET  D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001 = PROOF-TARGET; missing = finite Green function "
          "over the shell torus + Puiseux/ramification extraction theorem + branch-index uniqueness + EFT/IR matching functor")
    print("PASS_LEPTON_INDIRECT_COEFFICIENT_OWNER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
