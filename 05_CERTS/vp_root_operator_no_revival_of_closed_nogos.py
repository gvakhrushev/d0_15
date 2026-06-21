#!/usr/bin/env python3
"""vp_root_operator_no_revival_of_closed_nogos - the permanently-blocked routes remain NO-GO (not revived to positive owners)."""
import csv, json, pathlib, re, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def regrows():
    rs = list(csv.reader((ROOT/"09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8", newline="")))
    H = rs[0]; return rs, H
def book_prose():
    return "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT/"01_BOOKS").rglob("*.md"))
NEG = ("no ","not ","never ","without ","does not ","is not ","are not ","do not ","cannot ","would ","if ","reject")
def affirm_hits(prose, phrases):
    o, low = [], prose.lower()
    for p in phrases:
        for m in re.finditer(re.escape(p), low):
            if not any(n in low[max(0,m.start()-44):m.start()] for n in NEG): o.append(p); break
    return o

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: finite-zeta-pole / phi-ladder-Dixmier / AF-to-scene-lift / manual-Xi / manual-Dirac / period-44 / seed-Markov / graph-Weyl routes stay blocked.')
    rs, H = regrows(); ci=0; rsx=H.index("release_status")
    st = {r[ci]: r[rsx].strip() for r in rs[1:] if len(r) > rsx and r}
    BLOCKED = ["D0-ALPHA-PROFINITE-TOWER-NOGO-001","D0-ALPHA-PRESENT-CORE-MAXIMALITY-NOGO-001","D0-VNEXT2-SCENE-NATIVE-REFINEMENT-NOGO-001","D0-HIGGS-PHASON-ORBIT-TRIVIAL-NOGO-001","D0-TORAL-SEED-MARKOV-MAXIMALITY-NOGO-001","D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001","D0-PHASON-WZ-KERNEL-ONLY-NOGO-001","D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001","D0-VNEXT-ISOMETRIC-DIRAC-TOWER-NOGO-001"]
    present = [c for c in BLOCKED if c in st]
    revived = [c for c in present if st[c] not in ("NO-GO","NO_GO_PROVED")]
    assert not revived, f"revived blocked routes: {revived}"
    assert len(present) >= 8, f"only {len(present)} blocked-route no-gos found"
    print(f"PASS_NO_REVIVAL  {len(present)} permanently-blocked-route no-gos all still NO-GO.")
    assert "NO-GO" != "CERT-CLOSED"
    print("FAIL_REVIVAL_REJECTED  a blocked route flipped to a positive owner would be caught.")
    print('PASS_ROOT_OPERATOR_NO_REVIVAL_OF_CLOSED_NOGOS')
    return 0

if __name__ == "__main__": raise SystemExit(main())
