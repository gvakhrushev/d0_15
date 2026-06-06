#!/usr/bin/env python3
"""v14 no-go stress-test suite sync guard."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
DOCS = ROOT / "09_LEAN_FORMALIZATION" / "docs"
CERTS = ROOT / "05_CERTS"
RUNNER = ROOT / "tools" / "run_hard_theorem_closure.py"

CHECKS: list[tuple[str, Path, list[str]]] = [
    (
        "No-go stress Lean owner",
        LEAN / "NoGo" / "StressTestSuite.lean",
        [
            "no_go_rank_one_higgs_scalar_projector",
            "no_go_isolated_phason_generation_carrier",
            "no_go_isolated_phason_baryon_s3_sector",
            "no_go_euclidean_signature_export",
            "NoGoStressTestSuite",
            "no_go_stress_test_suite_closed",
        ],
    ),
    (
        "No-go stress cert",
        CERTS / "vp_no_go_stress_test_suite.py",
        [
            "PASS_NO_GO_STRESS_TEST_SUITE",
            "Rank-1 Higgs/scalar projector obstruction",
            "Isolated phason cannot close generation/baryon carriers",
            "Euclidean signature export negative control",
        ],
    ),
    (
        "Hard theorem targets",
        DOCS / "HARD_CLOSURE_TARGETS.csv",
        [
            "T_no_go_rank_one_higgs_scalar_projector",
            "T_no_go_isolated_phason_generation_carrier",
            "T_no_go_euclidean_signature_export",
            "T_no_go_stress_test_suite_closed",
        ],
    ),
    (
        "Claim map row",
        DOCS / "CLAIM_TO_LEAN_MAP.csv",
        [
            "D0-NO-GO-STRESS-SUITE-001",
            "D0.NoGo.StressTestSuite",
            "vp_no_go_stress_test_suite.py",
        ],
    ),
    (
        "Runner integration",
        RUNNER,
        ["no-go-stress-suite", "PASS_NO_GO_STRESS_TEST_SUITE"],
    ),
]

FORBIDDEN_LEAN_TOKENS = ["sorry", "admit", "axiom", "unsafe", "Float", "opaque"]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def code_without_line_comments(path: Path) -> str:
    return "\n".join(line.split("--", 1)[0] for line in read(path).splitlines())


def main() -> int:
    errors: list[str] = []
    for label, path, tokens in CHECKS:
        if not path.exists():
            errors.append(f"{label}: missing {path.relative_to(ROOT)}")
            continue
        text = read(path)
        for token in tokens:
            if token not in text:
                errors.append(f"{label}: missing token {token!r}")

    lean_path = LEAN / "NoGo" / "StressTestSuite.lean"
    if lean_path.exists():
        code = code_without_line_comments(lean_path)
        for token in FORBIDDEN_LEAN_TOKENS:
            if re.search(rf"\b{re.escape(token)}\b", code):
                errors.append(f"{lean_path.relative_to(ROOT)} contains forbidden token {token!r}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("PASS_NO_GO_STRESS_TEST_SUITE_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
