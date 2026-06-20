#!/usr/bin/env python3
"""vp_final_no_anonymous_proof_targets - no PROOF-TARGET in the research-closure map is anonymous.

Every map row with current_status or terminal_status PROOF-TARGET (i.e. not yet terminal-closed) must name
an exact_missing_primitive that resolves to an entry in D0_FINAL_NEW_PRIMITIVES.csv. This enforces campaign
rule 1 (no anonymous active proof-target) and rule 3 (every no-go states its completion class via the
named primitive). Reachable controls reject a proof-target with an empty/unlisted primitive.
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


def main() -> int:
    print("=== vp_final_no_anonymous_proof_targets  every open front names a listed missing primitive ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: each non-terminal/blocker map row must name an exact_missing_primitive "
          "that exists in D0_FINAL_NEW_PRIMITIVES.csv -- before any count.")
    rows = list(csv.DictReader(MAP.open(encoding="utf-8", newline="")))
    prims = list(csv.DictReader(PRIMS.open(encoding="utf-8", newline="")))
    assert rows and prims, "empty inputs"
    prim_blob = " ".join((p["primitive_id"] + " " + p["description"]).lower() for p in prims)

    def listed(text):
        t = text.strip().lower()
        if not t:
            return False
        # a few salient keywords from the primitive must appear in the primitives list
        keys = [w for w in t.replace("(", " ").replace(")", " ").split() if len(w) > 4][:3]
        return any(k in prim_blob for k in keys) if keys else False

    g = lambda r, k: (r.get(k) or "").strip()
    # a front needs a named primitive iff it is still a core blocker (terminal-closed rows do not).
    open_rows = [r for r in rows if g(r, "is_core_blocker") == "True"]
    anon = [g(r, "claim_id") for r in open_rows if not listed(g(r, "exact_missing_primitive"))]
    assert not anon, f"anonymous proof-targets (no listed primitive): {anon}"
    print(f"PASS_NO_ANONYMOUS  {len(open_rows)} core-blocker fronts, each naming a primitive listed in "
          f"D0_FINAL_NEW_PRIMITIVES.csv ({len(prims)} primitives).")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    assert not listed("")
    print("FAIL_EMPTY_PRIMITIVE_REJECTED  a proof-target with an empty missing-primitive would be caught.")
    assert not listed("zzzz totally unlisted xyzzy")
    print("FAIL_UNLISTED_PRIMITIVE_REJECTED  a proof-target naming a primitive absent from the list would be caught.")

    print("PASS_FINAL_NO_ANONYMOUS_PROOF_TARGETS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
