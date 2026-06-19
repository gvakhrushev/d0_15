#!/usr/bin/env python3
"""vp_verified_closure_protocol - D0-VERIFIED-CLOSURE-PROTOCOL-001.

Enforces that the verify-then-build closure protocol document exists and carries every mandatory
section: the 7 phases (0-6), the verify-then-build rule, the scout verdict vocabulary, the Lean
integration recurring-fixes section, the negation-aware no-overclaim discipline, the negative-control
rule, and the closure report template. Reachable control: a protocol text missing a required marker is
rejected.
"""
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC = ROOT / "04_VERIFICATION" / "VERIFIED_CLOSURE_PROTOCOL.md"

REQUIRED = [
    "Phase 0 — identify owner and exact blocker",
    "Phase 1 — grounded verification scout",
    "Phase 2 — honest scope decision",
    "Phase 3 — Lean / cert implementation",
    "Phase 4 — negative controls",
    "Phase 5 — book / registry integration",
    "Phase 6 — full gate and final report",
    "No high-load proof-target may receive Lean code before a grounded verification scout",
    "CERT-CLOSABLE", "NO-GO-CLOSABLE", "PARTIAL-CLOSABLE", "NOT-CLOSABLE", "DUPLICATE-ALREADY-OWNED",
    "Lean integration recurring fixes",
    "noncomputable", "div_lt_iff₀", "sub-namespace",
    "negation-aware",
    "STRUCTURE_FIXED_BEFORE_NUMBER",
    "Closure report template",
]


def required_missing(text):
    return [m for m in REQUIRED if m not in text]


def main() -> int:
    print("=== vp_verified_closure_protocol  verify-then-build protocol is codified and complete ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the protocol is fixed first -- 7 phases, the verify-then-build "
          "rule, the scout verdict vocabulary, the Lean recurring fixes, the negation-aware no-overclaim "
          "discipline, the negative-control rule, and the report template -- before any closure attempt.")

    assert DOC.exists(), "VERIFIED_CLOSURE_PROTOCOL.md is missing"
    text = DOC.read_text(encoding="utf-8")

    miss = required_missing(text)
    assert not miss, f"protocol document is missing required sections/markers: {miss}"
    print(f"PASS_PROTOCOL_COMPLETE  all {len(REQUIRED)} mandatory markers present "
          "(7 phases, verify-then-build rule, 5 scout verdicts, Lean fixes, no-overclaim discipline, "
          "negative-control rule, report template).")

    # the verify-then-build rule is mandatory and explicit
    assert "MANDATORY" in text and "grounded verification scout" in text, "verify-then-build rule must be explicit"
    print("PASS_VERIFY_THEN_BUILD_MANDATORY  the no-Lean-before-scout rule is present and marked MANDATORY.")

    # the no-overclaim discipline names the negation-aware requirement and a concrete honest example
    assert "does not claim DESI confirms D0" in text or "no SM table imported as proof" in text, \
        "the no-overclaim discipline must cite a concrete honest (negated) example"
    print("PASS_NO_OVERCLAIM_NEGATION_AWARE  the negation-aware no-overclaim discipline + honest example present.")

    # ===================== REACHABLE NEGATIVE CONTROL =====================
    planted = text.replace("Phase 4 — negative controls", "Phase 4 — (removed)")
    assert required_missing(planted), "control: a protocol text missing a required section must be rejected"
    print("FAIL_PROTOCOL_SECTION_MISSING_REJECTED  a protocol text with a required section removed is caught (reachable).")

    print("PASS_VERIFIED_CLOSURE_PROTOCOL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
