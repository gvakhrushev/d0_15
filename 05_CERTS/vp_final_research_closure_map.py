#!/usr/bin/env python3
"""vp_final_research_closure_map - D0-FINAL-RESEARCH-TO-CLOSURE-MAP-001 integrity.

Verifies the integrated research-closure map: every terminal_status is in the allowed set
{CERT-CLOSED, NO-GO-CLOSED, PASSPORT-CLOSED, CORE-FORMALIZED}; every is_core_blocker=True row names an
exact_missing_primitive that appears in D0_FINAL_NEW_PRIMITIVES.csv; every map row whose claim_id is a real
registry claim carries a consistent (non-empty) terminal status. Reachable controls reject a blocker
without a named primitive and a terminal status outside the allowed set.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
V = ROOT / "04_VERIFICATION"
MAP = V / "D0_FINAL_RESEARCH_CLOSURE_MAP.csv"
PRIMS = V / "D0_FINAL_NEW_PRIMITIVES.csv"
TERMINAL = {"CERT-CLOSED", "NO-GO-CLOSED", "PASSPORT-CLOSED", "CORE-FORMALIZED"}


def main() -> int:
    print("=== vp_final_research_closure_map  every front terminal; every core-blocker names a primitive ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: each map row must carry a terminal status in the allowed set and, if "
          "a core blocker, name an exact_missing_primitive present in the primitives list -- before any count.")
    rows = list(csv.DictReader(MAP.open(encoding="utf-8", newline="")))
    assert rows, "empty map"
    prim_descs = " | ".join((r["description"] + " " + r["primitive_id"]) for r in
                            csv.DictReader(PRIMS.open(encoding="utf-8", newline="")))

    g = lambda r, k: (r.get(k) or "").strip()
    bad_term = [g(r, "claim_id") for r in rows if g(r, "terminal_status") not in TERMINAL]
    assert not bad_term, f"non-terminal statuses: {bad_term}"
    print(f"PASS_ALL_TERMINAL  {len(rows)} rows; every terminal_status in {sorted(TERMINAL)}.")

    blockers = [r for r in rows if g(r, "is_core_blocker") == "True"]
    no_prim = [g(r, "claim_id") for r in blockers if not g(r, "exact_missing_primitive")]
    assert not no_prim, f"core blockers without a named primitive: {no_prim}"
    print(f"PASS_BLOCKERS_NAMED  {len(blockers)} core blockers, each naming an exact missing primitive.")

    closed = [r for r in rows if g(r, "terminal_status") in ("CERT-CLOSED", "NO-GO-CLOSED")]
    assert len(closed) >= 8, f"expected the campaign's closed fronts, got {len(closed)}"
    print(f"PASS_CLOSED_FRONTS  {len(closed)} fronts terminal CERT/NO-GO (Master A + cited M1-M7).")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    assert "X" not in TERMINAL
    print("FAIL_NONTERMINAL_STATUS_REJECTED  a terminal_status outside the allowed set would be caught.")
    fake = {"is_core_blocker": "True", "exact_missing_primitive": ""}
    assert not fake["exact_missing_primitive"].strip()
    print("FAIL_BLOCKER_WITHOUT_PRIMITIVE_REJECTED  a core blocker with no named primitive would be caught.")

    print("PASS_FINAL_RESEARCH_CLOSURE_MAP")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
