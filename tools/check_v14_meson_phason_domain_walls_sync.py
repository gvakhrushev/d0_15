#!/usr/bin/env python3
"""v14 QUASI-007 meson phason domain-wall sync guard."""

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
        "Meson phason domain-wall Lean owner",
        LEAN / "Matter" / "MesonPhasonDomainWalls.lean",
        [
            "MesonPhasonDomainWall",
            "sourceIx",
            "targetIx",
            "meson_phason_domain_wall_boundary_nonzero",
            "meson_phason_domain_wall_card_eq_six",
            "MesonDomainWallCarrier",
            "meson_domain_wall_generation_carrier_card_eq_eighteen",
            "meson_domain_wall_transfer_uses_lifted_defect",
            "meson_phason_domain_wall_closure",
            "MesonDefectTransferOriginClosure",
        ],
    ),
    (
        "Meson phason domain-wall cert",
        CERTS / "vp_phason_domain_wall_mesons.py",
        [
            "PASS_PHASON_DOMAIN_WALL_MESONS_K0_LABELS",
            "oriented walls = 3*2 = 6",
            "wall x generation carrier = 6*3 = 18",
            "no direct mass fixture",
        ],
    ),
    (
        "Hard theorem targets",
        DOCS / "HARD_CLOSURE_TARGETS.csv",
        [
            "T_meson_phason_domain_wall_card_eq_six",
            "T_meson_domain_wall_generation_carrier_card_eq_eighteen",
            "T_meson_domain_wall_transfer_uses_lifted_defect",
            "T_meson_phason_domain_wall_closure",
            "D0.Matter.MesonPhasonDomainWalls",
        ],
    ),
    (
        "Claim map row",
        DOCS / "CLAIM_TO_LEAN_MAP.csv",
        [
            "D0-QUASI007-MESON-PHASON-DOMAIN-WALLS-001",
            "D0.Matter.MesonPhasonDomainWalls",
            "vp_phason_domain_wall_mesons.py",
        ],
    ),
    (
        "Runner integration",
        RUNNER,
        ["meson-phason-domain-walls", "PASS_PHASON_DOMAIN_WALL_MESONS_K0_LABELS"],
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

    lean_path = LEAN / "Matter" / "MesonPhasonDomainWalls.lean"
    if lean_path.exists():
        code = code_without_line_comments(lean_path)
        for token in FORBIDDEN_LEAN_TOKENS:
            if re.search(rf"\b{re.escape(token)}\b", code):
                errors.append(f"{lean_path.relative_to(ROOT)} contains forbidden token {token!r}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("PASS_MESON_PHASON_DOMAIN_WALLS_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
