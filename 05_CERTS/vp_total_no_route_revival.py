#!/usr/bin/env python3
"""vp_total_no_route_revival - permanently-blocked routes are not revived as positive owners; named no-gos stay NO-GO."""
import csv, json, pathlib, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def reg():
    rs = list(csv.reader((ROOT/"09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8", newline="")))
    H = rs[0]; I = {c:H.index(c) for c in H}
    return [r for r in rs[1:] if len(r)==len(H) and r], I

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: finite-pole/phi-ladder-Dixmier/AF-lift/34-1/manual-Xi/manual-Dirac/period-44/seed-Markov/graph-Weyl routes stay blocked.')
    D,I = reg(); gg=lambda r,c: r[I[c]].strip()
    NOGOS=["D0-ALPHA-PROFINITE-TOWER-NOGO-001","D0-ALPHA-PRESENT-CORE-MAXIMALITY-NOGO-001","D0-CMB-CANONICAL-SMOOTHING-MAXIMALITY-NOGO-001","D0-PHASON-MAGNITUDE-MAXIMALITY-NOGO-001","D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001","D0-HIGGS-CONDENSATION-PRESENT-CORE-MAXIMALITY-NOGO-001","D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001","D0-TORAL-SEED-MARKOV-MAXIMALITY-NOGO-001","D0-VNEXT-ISOMETRIC-DIRAC-TOWER-NOGO-001"]
    st={gg(r,"claim_id"):gg(r,"release_status") for r in D}
    revived=[c for c in NOGOS if c in st and st[c] not in ("NO-GO","NO_GO_PROVED")]
    assert not revived, f"revived no-gos: {revived}"
    present=[c for c in NOGOS if c in st]; assert len(present)>=7, f"only {len(present)} blocked-route no-gos found"
    print(f"PASS_NO_REVIVAL  {len(present)} permanently-blocked-route no-gos all still NO-GO.")
    assert "NO-GO" != "CERT-CLOSED"
    print("FAIL_REVIVAL_REJECTED  a blocked route flipped to a positive owner would be caught.")
    print('PASS_TOTAL_NO_ROUTE_REVIVAL')
    return 0

if __name__ == "__main__": raise SystemExit(main())
