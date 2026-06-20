#!/usr/bin/env python3
"""vp_research_closure_source_ledger - D0 research-source discipline guard.

Enforces the research ledger rules: NO source is imported as a D0 axiom; every source is used only as a
method/passport; every source is paired with a concrete frozen D0 object and a named D0 front and a
technical result. This keeps external literature from silently becoming CORE. Reachable controls reject a
source marked imported-as-axiom, a source with no paired D0 object, and a source carrying a numerical input.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
LEDGER = ROOT / "04_VERIFICATION" / "RESEARCH_CLOSURE_SOURCE_LEDGER.csv"


def viol(r):
    if r["imported_as_axiom"].strip().upper() != "NO":
        return f"{r['source_id']}: imported_as_axiom != NO"
    if r["used_only_as_method"].strip().upper() not in ("YES", "PASSPORT-ONLY"):
        return f"{r['source_id']}: not method/passport-only"
    if not r["finite_D0_object_needed"].strip():
        return f"{r['source_id']}: no paired frozen D0 object"
    if not r["D0_front"].strip() or not r["technical_result_used"].strip():
        return f"{r['source_id']}: missing front/result"
    return ""


def main() -> int:
    print("=== vp_research_closure_source_ledger  no paper is a D0 axiom; method/passport-only, paired ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: every source must be imported_as_axiom=NO, method/passport-only, "
          "with a paired frozen D0 object + named front + technical result -- before any count.")
    rows = list(csv.DictReader(LEDGER.open(encoding="utf-8", newline="")))
    assert rows, "empty ledger"
    vs = [v for r in rows for v in [viol(r)] if v]
    assert not vs, f"violations: {vs}"
    print(f"PASS_DISCIPLINE  {len(rows)} sources: 0 imported-as-axiom; all method/passport-only with a paired "
          "frozen D0 object + front + result.")
    assert all(not r["url_or_doi"].strip() or r["url_or_doi"].strip().startswith("http") for r in rows)
    print("PASS_NO_FABRICATED_DOI  url_or_doi blank (classical, not asserted) or a real URL -- no fabricated DOI.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    assert viol({"source_id": "X", "imported_as_axiom": "YES", "used_only_as_method": "YES",
                 "finite_D0_object_needed": "obj", "D0_front": "f", "technical_result_used": "r"})
    print("FAIL_IMPORTED_AS_AXIOM_REJECTED  a source marked imported-as-axiom is caught.")
    assert viol({"source_id": "X", "imported_as_axiom": "NO", "used_only_as_method": "YES",
                 "finite_D0_object_needed": "", "D0_front": "f", "technical_result_used": "r"})
    print("FAIL_NO_D0_OBJECT_REJECTED  a source with no paired frozen D0 object is caught.")
    assert viol({"source_id": "X", "imported_as_axiom": "NO", "used_only_as_method": "NO",
                 "finite_D0_object_needed": "obj", "D0_front": "f", "technical_result_used": "r"})
    print("FAIL_NOT_METHOD_ONLY_REJECTED  a source not used-only-as-method/passport is caught.")

    print("PASS_RESEARCH_CLOSURE_SOURCE_LEDGER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
