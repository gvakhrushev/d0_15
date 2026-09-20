#!/usr/bin/env python3
"""vp_verified_closure_protocol - D0-VERIFIED-CLOSURE-PROTOCOL-001.

Enforces that the verify-then-build closure protocol document exists and carries every mandatory
section: the 7 phases (0-6), the verify-then-build rule, the scout verdict vocabulary, the Lean
integration recurring-fixes section, the negation-aware no-overclaim discipline, the negative-control
rule, and the closure report template. Also verifies CP1 control plane alignment: active-work source
is 00_WORK/manifest.json, scope excludes pure CONTROL tasks, real gate commands are listed, and no
stale hardcoded status-normalization mappings are present. Reachable controls: a protocol text
missing a required marker or reintroducing stale status mappings is rejected.
"""
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC = ROOT / "02_REGISTRY/frontier" / "verification_protocol.md"

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
    "00_WORK/manifest.json",
    "EXPENSIVE", "WORKER", "CONTROL",
    "validate_repo.py",
    "generate_lean_views.py --check",
    "validate_work.py --self-test",
    "validate_work.py",
    "render_work_status.py --check",
]

FORBIDDEN_STALE_MAPPINGS = [
    "PROOF-TARGET registry rows use lean_status = OPEN",
    "passport rows use PYTHON_CERTIFIED",
]


def required_missing(text: str) -> list[str]:
    return [m for m in REQUIRED if m not in text]


def forbidden_present(text: str) -> list[str]:
    return [m for m in FORBIDDEN_STALE_MAPPINGS if m in text]


def validate_protocol_text(text: str) -> None:
    miss = required_missing(text)
    assert not miss, f"protocol document is missing required sections/markers: {miss}"

    stale = forbidden_present(text)
    assert not stale, f"protocol document contains forbidden stale status mappings: {stale}"

    assert "MANDATORY" in text and "grounded verification scout" in text, "verify-then-build rule must be explicit"
    assert "does not claim DESI confirms D0" in text or "no SM table imported as proof" in text, \
        "the no-overclaim discipline must cite a concrete honest (negated) example"
    assert "00_WORK/README.md" in text, "protocol must note that CONTROL tasks are governed by 00_WORK/README.md"
    assert "CP1 does not normalize" in text, "protocol must explicitly note that CP1 does not normalize statuses"


def main() -> int:
    print("=== vp_verified_closure_protocol  verify-then-build protocol is codified and complete ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the protocol is fixed first -- 7 phases, the verify-then-build "
          "rule, the scout verdict vocabulary, the Lean recurring fixes, the negation-aware no-overclaim "
          "discipline, the negative-control rule, and the report template -- before any closure attempt.")

    assert DOC.exists(), "verification_protocol.md is missing"
    text = DOC.read_text(encoding="utf-8")

    validate_protocol_text(text)
    print(f"PASS_PROTOCOL_COMPLETE  all {len(REQUIRED)} mandatory markers present "
          "(7 phases, verify-then-build rule, 5 scout verdicts, Lean fixes, no-overclaim discipline, "
          "negative-control rule, report template, 00_WORK/manifest.json alignment, real gate commands).")
    print("PASS_VERIFY_THEN_BUILD_MANDATORY  the no-Lean-before-scout rule is present and marked MANDATORY.")
    print("PASS_NO_OVERCLAIM_NEGATION_AWARE  the negation-aware no-overclaim discipline + honest example present.")
    print("PASS_NO_STALE_STATUS_MAPPINGS  hardcoded PROOF-TARGET->OPEN and PASSPORT->PYTHON_CERTIFIED absent.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    # Control 1: missing required section
    planted_missing = text.replace("Phase 4 — negative controls", "Phase 4 — (removed)")
    assert required_missing(planted_missing), "control 1: a protocol text missing a required section must be rejected"
    print("FAIL_PROTOCOL_SECTION_MISSING_REJECTED  a protocol text with a required section removed is caught (reachable).")

    # Control 2: regression control catching return of old status mapping
    planted_stale = text + "\nPROOF-TARGET registry rows use lean_status = OPEN; passport rows use PYTHON_CERTIFIED.\n"
    assert forbidden_present(planted_stale), "control 2: reintroducing stale status mappings must be rejected"
    stale_rejected = False
    try:
        validate_protocol_text(planted_stale)
    except AssertionError:
        stale_rejected = True
    assert stale_rejected, "control 2: validation failed to reject stale status mapping"
    print("FAIL_STALE_STATUS_MAPPING_REJECTED  reintroduction of stale status mapping is caught (reachable).")

    print("PASS_VERIFIED_CLOSURE_PROTOCOL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
