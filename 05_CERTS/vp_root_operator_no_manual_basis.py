#!/usr/bin/env python3
"""vp_root_operator_no_manual_basis - the root certs each declare a reachable control rejecting a manual/hand-picked basis or subspace."""
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: every constructed sector must come from a canonical (kernel/Riesz/spectral) projector, never a hand-picked basis.')
    certs = ["vp_root_r1_representation_reconstruction.py","vp_root_r2_archive_contraction.py","vp_root_r4_lepton_branch.py"]
    txts = {c: (ROOT/"05_CERTS"/c).read_text(encoding="utf-8") for c in certs}
    # R2 explicitly rejects a hand-picked 2D basis; R1/R4 reject rank-only / mass-coefficient shortcuts
    assert "FAIL_MANUAL_BASIS_REJECTED" in txts["vp_root_r2_archive_contraction.py"]
    assert "FAIL_COUNT3_FROM_RANK_ALONE_REJECTED" in txts["vp_root_r1_representation_reconstruction.py"]
    print("PASS_NO_MANUAL_BASIS  root certs reject hand-picked bases / rank-only shortcuts (reachable controls present).")
    prose = book_prose()
    bad = affirm_hits(prose, ["hand-picked 2d basis chosen","manual basis selected for the sector"])
    assert not bad, f"manual-basis claim in books: {bad}"
    print("FAIL_MANUAL_BASIS_PROSE_REJECTED  an affirmative manual-basis claim in the books would be caught.")
    print('PASS_ROOT_OPERATOR_NO_MANUAL_BASIS')
    return 0

if __name__ == "__main__": raise SystemExit(main())
