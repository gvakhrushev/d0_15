#!/usr/bin/env python3
"""v14 master finite-evolution theorem sync guard."""

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
        "Master evolution Lean owner",
        LEAN / "Dynamics" / "MasterEvolutionTheorem.lean",
        [
            "T_squared_plus_T_minus_identity_eq_zero",
            "det_T_pow_square_eq_one",
            "lucas_heat_moment_bridge",
            "detector_is_fixed_under_ladder",
            "d0_phi_quasicrystal_vacuum_support",
            "D0MasterEvolutionClosure",
            "master_evolution_theorem",
        ],
    ),
    (
        "Master evolution cert",
        CERTS / "vp_master_evolution_theorem.py",
        [
            "PASS_MASTER_EVOLUTION_THEOREM",
            "T^2 + T - I = 0",
            "Tr(T^n)=(-1)^n L_n",
            "det(T^n)^2=1",
            "detector fixed",
        ],
    ),
    (
        "Hard theorem targets",
        DOCS / "HARD_CLOSURE_TARGETS.csv",
        [
            "T_master_evolution_theorem",
            "D0.Dynamics.MasterEvolutionTheorem",
            "Dynamics.master_evolution_theorem",
        ],
    ),
    (
        "Claim map row",
        DOCS / "CLAIM_TO_LEAN_MAP.csv",
        [
            "D0-MASTER-EVOLUTION-001",
            "D0.Dynamics.MasterEvolutionTheorem",
            "vp_master_evolution_theorem.py",
        ],
    ),
    (
        "Runner integration",
        RUNNER,
        ["master-evolution", "PASS_MASTER_EVOLUTION_THEOREM"],
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

    lean_path = LEAN / "Dynamics" / "MasterEvolutionTheorem.lean"
    if lean_path.exists():
        code = code_without_line_comments(lean_path)
        for token in FORBIDDEN_LEAN_TOKENS:
            if re.search(rf"\b{re.escape(token)}\b", code):
                errors.append(f"{lean_path.relative_to(ROOT)} contains forbidden token {token!r}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("PASS_MASTER_EVOLUTION_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
