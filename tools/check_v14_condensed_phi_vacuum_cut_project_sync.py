#!/usr/bin/env python3
"""v14 condensed phi-vacuum cut-project sync guard."""

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
        "Condensed phi-vacuum Lean owner",
        LEAN / "Condensed" / "CondensedPhiVacuum.lean",
        [
            "PhiVacuumStage",
            "CondensedPhiVacuum",
            "CutProjectQuasicrystal",
            "condensed_phi_vacuum_support_closed",
            "cut_project_quasicrystal_matches_phase_unfolding",
            "condensedPhiVacuumCutProjectClosure",
        ],
    ),
    (
        "Physics cut-project bridge",
        LEAN / "Physics" / "QuasicrystalPhenomenology.lean",
        [
            "D0.Condensed.CondensedPhiVacuum",
            "d0_phi_cut_project_matches_condensed_phi_vacuum",
        ],
    ),
    (
        "Condensed phi-vacuum cert",
        CERTS / "vp_condensed_phi_vacuum_cut_project.py",
        [
            "PASS_CONDENSED_PHI_VACUUM_CUT_PROJECT",
            "q_T=44",
            "q_EW=710",
            "condensed support and cut-project values agree",
        ],
    ),
    (
        "Hard theorem targets",
        DOCS / "HARD_CLOSURE_TARGETS.csv",
        [
            "T_condensed_phi_vacuum_support_closed",
            "T_cut_project_quasicrystal_matches_phase_unfolding",
            "T_physics_cut_project_matches_condensed_phi_vacuum",
        ],
    ),
    (
        "Claim map row",
        DOCS / "CLAIM_TO_LEAN_MAP.csv",
        [
            "D0-CONDENSED-PHI-VACUUM-CUT-PROJECT-001",
            "D0.Condensed.CondensedPhiVacuum",
            "vp_condensed_phi_vacuum_cut_project.py",
        ],
    ),
    (
        "Runner integration",
        RUNNER,
        ["condensed-phi-vacuum", "PASS_CONDENSED_PHI_VACUUM_CUT_PROJECT"],
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

    for lean_path in [
        LEAN / "Condensed" / "CondensedPhiVacuum.lean",
        LEAN / "Physics" / "QuasicrystalPhenomenology.lean",
    ]:
        if lean_path.exists():
            code = code_without_line_comments(lean_path)
            for token in FORBIDDEN_LEAN_TOKENS:
                if re.search(rf"\b{re.escape(token)}\b", code):
                    errors.append(f"{lean_path.relative_to(ROOT)} contains forbidden token {token!r}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("PASS_CONDENSED_PHI_VACUUM_CUT_PROJECT_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
