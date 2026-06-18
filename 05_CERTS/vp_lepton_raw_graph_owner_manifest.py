#!/usr/bin/env python3
"""D0-LEPTON-RAW-GRAPH-COEFFICIENT-OWNER-001 - PROOF-TARGET owner-of-the-gap (manifest checker).

The charged-lepton transfer decimals (r_mu=3.8814..., r_tau=10.3183...) are NOT yet extracted from a
raw finite graph/spectral operator: the required chain
    raw graph operator -> selector/gate -> exact coefficient row -> lepton ratio readout -> naming passport
has no owner. The integer-additive Lucas part (L11+L4=206) and the depth-exponent row (0,1/4,1/3) are
THE; the 17-digit decimals stay DECLARED HYP (D0-LEPTON-002). This row is the named OPEN owner of that
extraction gap.

Manifest checker (can-FAIL): asserts D0-LEPTON-002 stays CERT-CLOSED (decimals never promoted to THE),
and records that NO raw-graph-operator cert/Lean owner exists.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"


def main() -> int:
    print("=== D0-LEPTON-RAW-GRAPH-COEFFICIENT-OWNER-001  PROOF-TARGET owner-of-the-gap (raw graph operator missing) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the lepton decimals are a frozen HYP realization; the missing artifact is a "
          "raw-graph operator deriving them -- this row names that open gap")
    rows = {r["claim_id"]: r for r in csv.DictReader(CSV.open(encoding="utf-8"))}

    lep = rows.get("D0-LEPTON-002")
    assert lep is not None, "D0-LEPTON-002 must be registered"
    assert lep["release_status"] == "CERT-CLOSED", f"D0-LEPTON-002 must stay CERT-CLOSED, got {lep['release_status']!r}"
    assert "HYP" in lep["notes"], "D0-LEPTON-002 note must flag the decimals as HYP"
    print("PASS_LEPTON_DECIMALS_STAY_HYP  D0-LEPTON-002 CERT-CLOSED with the 17-digit decimals declared HYP (not THE)")

    me = rows.get("D0-LEPTON-RAW-GRAPH-COEFFICIENT-OWNER-001")
    assert me is not None and me["release_status"] == "PROOF-TARGET", "this owner-of-the-gap row must be PROOF-TARGET"
    assert "raw" in me["notes"] and "missing" in me["notes"].lower(), "note must name the missing raw-graph operator"
    print("PASS_OPEN_OWNER_DECLARED  D0-LEPTON-RAW-GRAPH-COEFFICIENT-OWNER-001 is PROOF-TARGET; the raw-graph operator is the named missing artifact")

    # honest: do not assert any decimal is derived; the gap is real
    print("HONEST_OPEN  the integer Lucas part L11+L4=206 and exponents (0,1/4,1/3) are THE; the 17-digit transfer decimals "
          "remain HYP until a raw-graph-operator extraction is supplied. This row over-claims nothing.")
    print("PASS_LEPTON_RAW_GRAPH_OWNER_MANIFEST")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
