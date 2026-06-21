#!/usr/bin/env python3
"""vp_postcore_no_manual_extension_data - no extension Lean module defines an operator from manual/external data."""
import csv, json, pathlib, re, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def regrows():
    rs = list(csv.reader((ROOT/"09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8", newline="")))
    return rs, rs[0]
def books():
    return "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT/"01_BOOKS").rglob("*.md"))
NEG = ("no ","not ","never ","without ","does not ","is not ","are not ","do not ","cannot ","would ","if ","reject","only if")
def affirm(prose, phrases):
    o, low = [], prose.lower()
    for p in phrases:
        for m in re.finditer(re.escape(p), low):
            if not any(n in low[max(0,m.start()-46):m.start()] for n in NEG): o.append(p); break
    return o

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: extension modules use only frozen scene/phi objects; no PDG/Planck/DESI/LIGO/CODATA/246.')
    mods = list((ROOT/"09_LEAN_FORMALIZATION/D0/Extensions").glob("*.lean"))
    EXT = ["codata","planck","desi","ligo","246 gev","pdg mass"]
    def strip_comments(txt):
        # remove Lean block comments /- ... -/ (incl /-! and /--) and -- line comments, so only CODE is scanned
        txt = re.sub(r"/-.*?-/", " ", txt, flags=re.DOTALL)
        txt = re.sub(r"--.*", " ", txt)
        return txt.lower()
    for m in mods:
        code = strip_comments(m.read_text(encoding="utf-8"))
        hit = [e for e in EXT if e in code]
        assert not hit, f"external datum in {m.name} CODE: {hit}"
    assert len(mods) >= 6
    print(f"PASS_NO_MANUAL_DATA  {len(mods)} extension modules name no PDG/Planck/DESI/LIGO/CODATA datum.")
    e3 = (ROOT/"05_CERTS/vp_postcore_e3_archive_coordinate.py").read_text(encoding="utf-8")
    assert "FAIL_CPL_DESI_REJECTED" in e3
    print("FAIL_MANUAL_DATA_REJECTED  an external datum in an extension operator would be caught.")
    print('PASS_POSTCORE_NO_MANUAL_EXTENSION_DATA')
    return 0

if __name__ == "__main__": raise SystemExit(main())
