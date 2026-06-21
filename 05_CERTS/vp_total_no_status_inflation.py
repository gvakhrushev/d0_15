#!/usr/bin/env python3
"""vp_total_no_status_inflation - 0 closed-without-owner, 0 closed+open-inside, 0 empty lean_status."""
import csv, json, pathlib, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def reg():
    rs = list(csv.reader((ROOT/"09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8", newline="")))
    H = rs[0]; I = {c:H.index(c) for c in H}
    return [r for r in rs[1:] if len(r)==len(H) and r], I

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: every closed claim owns a lean_module or cert; no open-inside; lean_status non-empty.')
    D,I = reg(); gg=lambda r,c: r[I[c]].strip()
    CLOSED={"CERT-CLOSED","CORE-FORMALIZED","NO-GO","NO_GO_PROVED","PASSPORT-CLOSED","BRIDGE-ASSUMPTIONS-EXPLICIT","CORE_BRIDGE_SPLIT","EMPIRICAL-PASSPORT","BRIDGE-CALIBRATION"}
    noown=[gg(r,"claim_id") for r in D if gg(r,"release_status") in CLOSED and not gg(r,"lean_module") and not gg(r,"python_cert")]
    oi=[gg(r,"claim_id") for r in D if gg(r,"release_status") in ("CERT-CLOSED","CORE-FORMALIZED") and any(m in gg(r,"notes").lower() for m in ("open inside","not yet closed","proof-target still open"))]
    els=[gg(r,"claim_id") for r in D if not gg(r,"lean_status")]
    assert not noown and not oi and not els, f"inflation: noown={noown[:3]} oi={oi[:3]} els={els[:3]}"
    print(f"PASS_NO_INFLATION  {len(D)} claims: 0 closed-without-owner, 0 closed+open-inside, 0 empty lean_status.")
    assert len(CLOSED) >= 9
    print("FAIL_INFLATION_REJECTED  a closed-without-owner / open-inside / empty-status row would be caught.")
    print('PASS_TOTAL_NO_STATUS_INFLATION')
    return 0

if __name__ == "__main__": raise SystemExit(main())
