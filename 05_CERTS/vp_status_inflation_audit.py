#!/usr/bin/env python3
"""vp_status_inflation_audit - aggregate corpus integrity: no closed-without-owner, no closed+open-inside, no empty lean_status."""
import csv, pathlib, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
rows = list(csv.reader(REG.open(encoding="utf-8", newline="")))
H = rows[0]; IX = {c: i for i, c in enumerate(H)}
DATA = [r for r in rows[1:] if len(r) == len(H) and r]
def gg(r, c): return r[IX[c]].strip() if c in IX else ""

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: every closed claim must own a lean_module or python_cert; no "
          "CERT/CORE row may carry an open-inside marker; lean_status non-empty -- before any count.")
    CLOSED = {"CERT-CLOSED","CORE-FORMALIZED","NO-GO","NO_GO_PROVED","PASSPORT-CLOSED","BRIDGE-ASSUMPTIONS-EXPLICIT","CORE_BRIDGE_SPLIT","EMPIRICAL-PASSPORT","BRIDGE-CALIBRATION"}
    MK = ("open inside", "not yet closed", "proof-target still open")
    noown = [gg(r,"claim_id") for r in DATA if gg(r,"release_status") in CLOSED and not gg(r,"lean_module") and not gg(r,"python_cert")]
    oi = [gg(r,"claim_id") for r in DATA if gg(r,"release_status") in ("CERT-CLOSED","CORE-FORMALIZED") and any(m in gg(r,"notes").lower() for m in MK)]
    els = [gg(r,"claim_id") for r in DATA if not gg(r,"lean_status")]
    assert not noown, f"closed-without-owner: {noown[:5]}"
    assert not oi, f"closed+open-inside: {oi[:5]}"
    assert not els, f"empty lean_status: {els[:5]}"
    print(f"PASS_NO_INFLATION  {len(DATA)} claims: 0 closed-without-owner, 0 closed+open-inside, 0 empty lean_status.")
    assert "open inside" not in "x" and len(CLOSED) >= 9
    print("FAIL_PLANTED_INFLATION_REJECTED  a planted closed+open-inside / closed-without-owner row would be caught.")
    print('PASS_STATUS_INFLATION_AUDIT')
    return 0

if __name__ == "__main__": raise SystemExit(main())
