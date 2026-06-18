#!/usr/bin/env python3
"""D0-LEPTON-INDIRECT missing-artifacts manifest - the exact gaps, while the owner is not closed.

If D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001 is not CERT-CLOSED, this manifest verifies that the exact
missing artifacts are named in its registry note: a finite Green function over the shell torus, a
Puiseux extraction theorem, a branch-index uniqueness certificate, and the EFT/IR matching functor.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
ARTIFACTS = ["green function", "puiseux", "branch-index uniqueness", "matching functor"]


def main() -> int:
    print("=== D0-LEPTON-INDIRECT missing-artifacts manifest ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: while the indirect owner is open, the exact missing artifacts must be named")
    rows = {r["claim_id"]: r for r in csv.DictReader(CSV.open(encoding="utf-8"))}
    me = rows.get("D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001")
    assert me is not None, "the indirect coefficient owner must be registered"
    if me["release_status"] == "CERT-CLOSED":
        print("OWNER_CLOSED  the indirect owner is CERT-CLOSED -- missing-artifacts manifest is vacuously satisfied")
    else:
        assert me["release_status"] == "PROOF-TARGET", f"owner must be PROOF-TARGET or CERT-CLOSED, got {me['release_status']}"
        note = me["notes"].lower()
        miss = [a for a in ARTIFACTS if a not in note]
        assert not miss, f"the owner note must name the exact missing artifacts; absent: {miss}"
        print("PASS_MISSING_ARTIFACTS_NAMED  finite Green function over shell torus + Puiseux extraction theorem + "
              "branch-index uniqueness certificate + EFT/IR matching functor are all named in the owner note")
    print("PASS_LEPTON_INDIRECT_MISSING_ARTIFACTS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
