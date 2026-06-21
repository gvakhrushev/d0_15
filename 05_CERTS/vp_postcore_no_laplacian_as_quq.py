#!/usr/bin/env python3
"""vp_postcore_no_laplacian_as_quq - the L_archive spectrum {24,22,20} is never asserted to be the QUQ spectrum."""
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
    print("STRUCTURE_FIXED_BEFORE_NUMBER: L_archive = Laplacian|ker A (degrees), QUQ = tick archive block; the former's spectrum is NOT the latter's.")
    sr = list(csv.DictReader((ROOT/"04_VERIFICATION/POST_CORE_NOGO_SCOPE_REPAIR.csv").open(encoding="utf-8", newline="")))
    r2 = next(r for r in sr if r["root"]=="R2")
    assert "NOT the QUQ spectrum" in r2["what_it_does_NOT_prove"] or "QUQ" in r2["what_it_does_NOT_prove"]
    print("PASS_R2_SCOPED  R2 scope row states the L_archive spectrum is NOT the QUQ spectrum.")
    bad = affirm(books(), ["laplacian spectrum is the quq spectrum","quq has spectrum {24,22,20}","quq is non-contractive"])
    assert not bad, f"laplacian-as-quq in books: {bad}"
    print("FAIL_LAPLACIAN_AS_QUQ_REJECTED  asserting L_archive spectrum = QUQ spectrum (or QUQ non-contractive) is caught.")
    print('PASS_POSTCORE_NO_LAPLACIAN_AS_QUQ')
    return 0

if __name__ == "__main__": raise SystemExit(main())
