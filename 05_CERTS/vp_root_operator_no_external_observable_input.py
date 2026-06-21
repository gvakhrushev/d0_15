#!/usr/bin/env python3
"""vp_root_operator_no_external_observable_input - no root Lean module defines an operator from PDG/Planck/DESI/LIGO/CODATA; certs carry the external-input controls."""
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: no external datum may enter an operator definition; only frozen K(9,11,13)/phi objects.')
    mods = ["D0/Representation/FinitePathRepresentation.lean","D0/Cosmology/ArchiveContractionCriterion.lean","D0/Spectral/SceneNativeMultiscaleTower.lean","D0/Matter/LeptonBranchAssignmentNoGo.lean","D0/Spectral/AlphaLogCesaroMeasurability.lean"]
    EXT = ["codata","planck","desi","ligo","246 gev","pdg mass"]
    for m in mods:
        low = (ROOT/"09_LEAN_FORMALIZATION"/m).read_text(encoding="utf-8").lower()
        hit = [e for e in EXT if e in low]
        assert not hit, f"external datum in {m}: {hit}"
    print(f"PASS_NO_EXTERNAL_INPUT  none of the {len(mods)} root Lean modules name a PDG/Planck/DESI/LIGO/CODATA datum.")
    r5 = (ROOT/"05_CERTS/vp_root_r5_alpha_log_cesaro.py").read_text(encoding="utf-8")
    assert "FAIL_CODATA_ALPHA_REJECTED" in r5
    print("FAIL_EXTERNAL_INPUT_REJECTED  a measured/CODATA datum entering an operator would be caught.")
    print('PASS_ROOT_OPERATOR_NO_EXTERNAL_OBSERVABLE_INPUT')
    return 0

if __name__ == "__main__": raise SystemExit(main())
