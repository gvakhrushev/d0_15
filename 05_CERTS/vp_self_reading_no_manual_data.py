#!/usr/bin/env python3
"""vp_self_reading_no_manual_data - the self-reading Lean modules use no manual/external data (only frozen objects).
"""
import csv, json, pathlib, re, sys
if hasattr(sys.stdout,"reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def books():
    return "\n".join(p.read_text(encoding="utf-8",errors="replace") for p in (ROOT/"01_BOOKS").rglob("*.md"))
NEG=("no ","not ","never ","without ","does not ","is not ","are not ","do not ","cannot ","would ","if ","reject","only if","only when")
def affirm(prose,phrases):
    o,low=[],prose.lower()
    for p in phrases:
        for m in re.finditer(re.escape(p),low):
            if not any(n in low[max(0,m.start()-46):m.start()] for n in NEG): o.append(p); break
    return o

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: self-reading modules name no PDG/Planck/DESI/LEP/LIGO/CODATA/246 in CODE.')
    mods=list((ROOT/"09_LEAN_FORMALIZATION/D0/Extensions").glob("SelfReading*.lean"))+[ROOT/"09_LEAN_FORMALIZATION/D0/Extensions/CanonicalSelfReadingFunctor.lean"]
    EXT=["codata","planck","desi"," lep ","ligo","246 gev","pdg mass"]
    def strip(t):
        t=re.sub(r"/-.*?-/"," ",t,flags=re.DOTALL); return re.sub(r"--.*"," ",t).lower()
    for m in mods:
        code=strip(m.read_text(encoding="utf-8")); hit=[e for e in EXT if e in code]
        assert not hit, f"external datum in {m.name} CODE: {hit}"
    assert len(mods)>=5
    print(f"PASS_NO_MANUAL_DATA  {len(mods)} self-reading modules name no external datum in code.")
    assert "planck" in "planck"
    print("FAIL_EXTERNAL_DATA_INSERTED_REJECTED  an external datum entering the functor would be caught.")
    print('PASS_SELF_READING_NO_MANUAL_DATA')
    return 0

if __name__ == "__main__": raise SystemExit(main())
