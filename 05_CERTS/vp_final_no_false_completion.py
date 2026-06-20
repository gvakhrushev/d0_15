#!/usr/bin/env python3
"""vp_final_no_false_completion - the campaign claims no physics derivation / no false completion.

NEGATION-AWARE scan of the books for forbidden completion overclaims: all physics derived, Standard Model
derived, measured alpha predicted, Planck n_s predicted, physical w_DE(z) derived, 246 GeV derived, LIGO
confirms D0, external theorem counted as CORE. Also asserts the release-readiness JSON records 0 physics
claims promoted to core and 0 external theorems imported as axiom. Reachable controls catch a planted
false-completion and allow an honest negated disclaimer.
"""
import csv
import json
import pathlib
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
BOOKS = ROOT / "01_BOOKS"
RR = ROOT / "04_VERIFICATION" / "D0_FINAL_RELEASE_READINESS.json"
FORBIDDEN = [
    "all physics derived", "all physics is derived", "standard model derived", "standard model is derived",
    "measured alpha predicted", "predict the measured alpha", "planck n_s predicted", "predict planck n_s",
    "physical w_de(z) derived", "derive physical w_de", "246 gev derived", "derive 246 gev",
    "ligo confirms d0", "ligo confirms the theory", "external theorem counted as core",
    "all geometry and time closed", "theory of everything complete",
]
NEG = ("no ", "not ", "never ", "without ", "n't ", "cannot ", "does not ", "do not ", "is not ",
       "are not ", "rejects ", "reject ", "no physics", "not a ", "must not ")


def affirmative_hits(prose):
    hits, low = [], prose.lower()
    for p in FORBIDDEN:
        for m in re.finditer(re.escape(p), low):
            ctx = low[max(0, m.start() - 40):m.start()]
            if not any(neg in ctx for neg in NEG):
                hits.append(p)
                break
    return hits


def main() -> int:
    print("=== vp_final_no_false_completion  no physics-derivation / no false-completion overclaim ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the campaign closes structure (CERT/NO-GO/PASSPORT), derives NO "
          "physics; the book prose carries no affirmative completion overclaim and the readiness JSON records "
          "0 physics-to-core and 0 axiom-imports. Scan is NEGATION-AWARE.")
    rr = json.load(RR.open(encoding="utf-8"))
    assert rr.get("physics_claims_promoted_to_core") == 0, "readiness must record 0 physics-to-core"
    assert rr.get("external_theorems_imported_as_axiom") == 0, "readiness must record 0 axiom-imports"
    print("PASS_READINESS_HONEST  release readiness records 0 physics-claims-to-core and 0 axiom-imports.")

    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in BOOKS.rglob("*.md"))
    hits = affirmative_hits(prose)
    assert not hits, f"affirmative false-completion overclaim(s) in books: {hits}"
    print("PASS_NO_OVERCLAIM  no affirmative physics-derivation / completion overclaim in the book prose.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    planted = "Result: all physics derived, measured alpha predicted, and 246 GeV derived; LIGO confirms D0."
    assert affirmative_hits(planted), "control: a planted false-completion must be caught"
    print("FAIL_FALSE_COMPLETION_CAUGHT  a planted 'all physics derived / alpha predicted' is caught.")
    honest = "D0 does not derive the measured alpha; Planck n_s is not predicted; no external theorem is counted as core."
    assert not affirmative_hits(honest), "control: an honest negated disclaimer must NOT be flagged"
    print("PASS_NEGATED_DISCLAIMER_ALLOWED  an honest negated disclaimer is NOT flagged.")

    print("PASS_FINAL_NO_FALSE_COMPLETION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
