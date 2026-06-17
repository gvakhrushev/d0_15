#!/usr/bin/env python3
"""v14 QUASI-009 CKM phason-holonomy sync guard."""

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
        "CKM phason holonomy Lean owner",
        LEAN / "Matter" / "CKMPhasonHolonomy.lean",
        [
            "TorusShellPhasonConnectionCurvature",
            "torus_shell_noncommutator_is_phason_connection_curvature",
            "phasonHolonomyAmplitude",
            "phasonHolonomyResponse",
            "phason_parallel_transport_around_shells_is_unitary",
            "phason_holonomy_response_has_multisupport_row",
            "phason_holonomy_response_not_permutation",
            "ckm_cp_phase_is_chiral_phason_bundle_twist",
            "ckm_matrix_is_phason_holonomy_on_torus_core13",
            "CKMPhasonHolonomyClosure",
        ],
    ),
    (
        "CKM phason holonomy cert",
        CERTS / "vp_ckm_phason_holonomy_k0.py",
        [
            "PASS_CKM_PHASON_HOLONOMY_K0",
            "[A_radial,D_phase](0,1)=(a-1)/2 != 0",
            "3/5-4/5 transport",
            "no PDG CKM entries",
        ],
    ),
    (
        "Hard theorem targets",
        DOCS / "HARD_CLOSURE_TARGETS.csv",
        [
            "T_ckm_torus_shell_noncommutator_phason_curvature",
            "T_ckm_phason_parallel_transport_unitary",
            "T_ckm_matrix_phason_holonomy_core13",
            "T_ckm_cp_phase_chiral_phason_twist",
            "D0.Matter.CKMPhasonHolonomy",
        ],
    ),
    (
        "Claim map row",
        DOCS / "CLAIM_TO_LEAN_MAP.csv",
        [
            "D0-QUASI009-CKM-PHASON-HOLONOMY-001",
            # lean_module column for QUASI009 was intentionally blanked
            # (Lean = EXTERNAL-GAP, placeholder theorem removed), so the
            # D0.Matter.CKMPhasonHolonomy pin no longer belongs in this row.
            "vp_ckm_phason_holonomy_k0.py",
        ],
    ),
    (
        "Runner integration",
        RUNNER,
        ["ckm-phason-holonomy", "PASS_CKM_PHASON_HOLONOMY_K0"],
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

    lean_path = LEAN / "Matter" / "CKMPhasonHolonomy.lean"
    if lean_path.exists():
        code = code_without_line_comments(lean_path)
        for token in FORBIDDEN_LEAN_TOKENS:
            if re.search(rf"\b{re.escape(token)}\b", code):
                errors.append(f"{lean_path.relative_to(ROOT)} contains forbidden token {token!r}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("PASS_CKM_PHASON_HOLONOMY_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
