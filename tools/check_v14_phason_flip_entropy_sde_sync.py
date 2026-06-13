#!/usr/bin/env python3
"""v14 QUASI-008 phason-flip entropy / S_DE sync guard."""

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
        "Phason flip entropy Lean owner",
        LEAN / "Cosmology" / "PhasonFlipEntropy.lean",
        [
            "PhasonFlipEntropy",
            "ArchivePressureFromPhasonFlips",
            "phasonFlipTransferMatrix",
            "SDEPolynomial",
            "phason_flip_entropy_nonnegative",
            "archive_pressure_is_phason_flip_entropy_osmosis",
            "phason_flip_transfer_matrix_has_sde_polynomial",
            "sde_roots_are_phason_flip_relaxation_modes",
            "PhasonFlipEntropySDEClosure",
        ],
    ),
    (
        "Phason flip entropy cert",
        CERTS / "vp_phason_flip_entropy_sde.py",
        [
            "PASS_PHASON_FLIP_ENTROPY_SDE_GAP_LABELS",
            "160 lambda^2 - 480 lambda + 359",
            "no BAO/DESI data",
            "no fitted S_DE parameter",
        ],
    ),
    (
        "Hard theorem targets",
        DOCS / "HARD_CLOSURE_TARGETS.csv",
        [
            "T_phason_flip_entropy_nonnegative",
            "T_archive_pressure_phason_flip_entropy_osmosis",
            "T_phason_flip_transfer_sde_polynomial",
            "T_sde_roots_phason_flip_relaxation_modes",
            "D0.Cosmology.PhasonFlipEntropy",
        ],
    ),
    (
        "Claim map row",
        DOCS / "CLAIM_TO_LEAN_MAP.csv",
        [
            "D0-QUASI008-PHASON-FLIP-ENTROPY-SDE-001",
            "D0.Cosmology.PhasonFlipEntropy",
            "vp_phason_flip_entropy_sde.py",
        ],
    ),
    (
        "Runner integration",
        RUNNER,
        ["phason-flip-entropy-sde", "PASS_PHASON_FLIP_ENTROPY_SDE_GAP_LABELS"],
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

    lean_path = LEAN / "Cosmology" / "PhasonFlipEntropy.lean"
    if lean_path.exists():
        code = code_without_line_comments(lean_path)
        for token in FORBIDDEN_LEAN_TOKENS:
            if re.search(rf"\b{re.escape(token)}\b", code):
                errors.append(f"{lean_path.relative_to(ROOT)} contains forbidden token {token!r}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("PASS_PHASON_FLIP_ENTROPY_SDE_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
