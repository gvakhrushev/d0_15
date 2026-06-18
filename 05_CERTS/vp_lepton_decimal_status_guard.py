#!/usr/bin/env python3
"""D0-LEPTON decimal-status guard - the direct decimal route stays no-go and the decimals stay HYP.

Checks: D0-BARE-GRAPH-DECIMAL-NOGO-001 is active (NO-GO); D0-LEPTON-002 is CERT-CLOSED with the decimals
HYP; no book promotes the 17-digit lepton decimals to CORE/THE or claims PDG validation.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
FORBIDDEN = [
    "charged-lepton decimals are CORE",
    "lepton decimals are THE",
    "PDG validates lepton coefficients",
    "17-digit lepton row is CORE",
]


def main() -> int:
    print("=== D0-LEPTON decimal-status guard ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: direct raw-graph decimal route stays no-go; the 17-digit decimals stay HYP/BRIDGE")
    rows = {r["claim_id"]: r for r in csv.DictReader(CSV.open(encoding="utf-8"))}

    def st(c):
        return rows.get(c, {}).get("release_status")

    assert st("D0-BARE-GRAPH-DECIMAL-NOGO-001") in ("NO-GO", "NO_GO_PROVED"), "the direct-decimal no-go must stay active"
    print("PASS_DIRECT_NOGO_ACTIVE  D0-BARE-GRAPH-DECIMAL-NOGO-001 = NO-GO (direct raw-graph->decimal forbidden)")
    lep = rows.get("D0-LEPTON-002")
    assert lep is not None and lep["release_status"] == "CERT-CLOSED" and "HYP" in lep["notes"], "decimals must stay HYP under CERT-CLOSED"
    print("PASS_DECIMALS_HYP  D0-LEPTON-002 = CERT-CLOSED with the 17-digit decimals declared HYP (never THE)")
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT / "01_BOOKS").rglob("*.md"))
    hits = [f for f in FORBIDDEN if f in prose]
    assert not hits, f"forbidden lepton-decimal promotion(s): {hits}"
    print("PASS_NO_DECIMAL_PROMOTION  no 'lepton decimals are CORE/THE' / 'PDG validates lepton coefficients' in the books")
    assert any(f in "x charged-lepton decimals are CORE x" for f in FORBIDDEN), "control: detector reachable"
    print("FAIL_PLANTED_DECIMAL_PROMOTION_CAUGHT  the detector is reachable")
    print("PASS_LEPTON_DECIMAL_STATUS_GUARD")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
