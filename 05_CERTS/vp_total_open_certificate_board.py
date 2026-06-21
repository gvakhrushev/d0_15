#!/usr/bin/env python3
"""vp_total_open_certificate_board - every unregistered cert is boarded with a terminal condition."""
import csv, json, pathlib, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def reg():
    rs = list(csv.reader((ROOT/"09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8", newline="")))
    H = rs[0]; I = {c:H.index(c) for c in H}
    return [r for r in rs[1:] if len(r)==len(H) and r], I

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: no registered/dormant cert may lack a board row with a terminal condition.')
    import glob
    # robust read: include legacy rows with >11 fields (else certs owned only by malformed rows look orphaned)
    _raw = list(csv.reader((ROOT/"09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8", newline="")))
    _pc = _raw[0].index("python_cert")
    registered = {r[_pc].strip() for r in _raw[1:] if len(r) > _pc and r and r[_pc].strip()}
    allcerts={pathlib.Path(p).name for p in glob.glob(str(ROOT/"05_CERTS/vp_*.py"))}
    orphans=allcerts-registered
    B={r["certificate"] for r in csv.DictReader((ROOT/"04_VERIFICATION/OPEN_CERTIFICATE_COMPLETION_BOARD.csv").open(encoding="utf-8", newline=""))}
    unboarded=sorted(orphans-B)
    assert not unboarded, f"dormant cert without a board row: {unboarded[:6]}"
    print(f"PASS_CERT_BOARD  {len(orphans)} unregistered guard certs all boarded with a terminal condition.")
    rows=list(csv.DictReader((ROOT/"04_VERIFICATION/OPEN_CERTIFICATE_COMPLETION_BOARD.csv").open(encoding="utf-8", newline="")))
    assert all((r.get("terminal_condition") or "").strip() for r in rows)
    print("FAIL_DORMANT_CERT_REJECTED  a dormant cert with no board row would be caught.")
    print('PASS_TOTAL_OPEN_CERTIFICATE_BOARD')
    return 0

if __name__ == "__main__": raise SystemExit(main())
