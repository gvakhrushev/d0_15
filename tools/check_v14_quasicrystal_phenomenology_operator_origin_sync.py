#!/usr/bin/env python3
"""v14 D0-QUASI-002 phenomenology operator-origin synchronization guard."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"
DOCS = ROOT / "09_LEAN_FORMALIZATION" / "docs"
CERTS = ROOT / "05_CERTS"
RUNNER = ROOT / "tools" / "run_hard_theorem_closure.py"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def code_without_line_comments(path: Path) -> str:
    return "\n".join(line.split("--", 1)[0] for line in read(path).splitlines())


LEAN_CHECKS: list[tuple[str, Path, list[str]]] = [
    (
        "generation inflation owner",
        LEAN / "Physics" / "QuasiGenerationsInflation.lean",
        [
            "D0GenerationCarrier",
            "generation_carrier_is_three_inflation_classes",
            "generation_trace_layer_eq_three",
            "generation_inflation_transports_same_defect_type",
            "quasi_generation_inflation_orbit",
        ],
    ),
    (
        "archive phason dark matter owner",
        LEAN / "Physics" / "ArchivePhasonDarkMatter.lean",
        [
            "PhasonStrainField",
            "EMCouplingArchive",
            "GravityCouplingArchive",
            "archive_phason_strain_is_dark_to_em",
            "archive_phason_strain_can_source_metric_response",
            "archive_phason_strain_em_dark_metric_visible",
        ],
    ),
    (
        "window offset chirality owner",
        LEAN / "Physics" / "WindowOffsetChirality.lean",
        [
            "AcceptanceWindow",
            "Centered",
            "InversionSymmetric",
            "offset_window_breaks_parity_witness",
            "window_offset_forces_chiral_readout",
        ],
    ),
    (
        "phason flip inertia owner",
        LEAN / "Physics" / "PhasonFlipInertia.lean",
        [
            "MovingDefect",
            "PhasonFlipCount",
            "InertialCost",
            "NonzeroAcceleration",
            "phason_flip_drag_positive_cost",
        ],
    ),
    (
        "window fractional charge owner",
        LEAN / "Physics" / "WindowFractionalCharge.lean",
        [
            "ColorSector",
            "WindowWeight",
            "single_sector_weight_eq_one_third",
            "double_sector_weight_eq_two_thirds",
            "signed_window_charge_values",
            "fractional_charge_window_weights",
        ],
    ),
    (
        "quasicrystal phenomenology aggregator",
        LEAN / "Physics" / "QuasicrystalPhenomenology.lean",
        [
            "D0PhiCutProject",
            "d0PhiCutProject",
            "d0_phi_cut_project_matches_phase_unfolding",
            "QuasicrystalPhenomenologyOperatorOrigin",
            "quasicrystal_phenomenology_operator_origin",
        ],
    ),
]

TEXT_CHECKS: list[tuple[str, Path, list[str]]] = [
    (
        "Book 00 quasicrystal vacuum thesis",
        ROOT / "03_THEORY_MAP" / "BOOK_REFACTOR_AUDIT.md",
        [
            "D0 vacuum is the phi-quasicrystalline condensed/profinite support",
            "D0-QUASI-002",
            "Quasicrystal Phenomenology Operator Origin",
        ],
    ),
    (
        "Book 01 cut-and-project phase unfolding",
        BOOKS / "BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md",
        [
            "cut-and-project quasicrystal geometry",
            "D0PhiCutProject",
            "quasicrystal_phenomenology_operator_origin",
        ],
    ),
    (
        "Book 02 proof cell",
        BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md",
        [
            "D0-QUASI-002",
            "quasi_generation_inflation_orbit",
            "archive_phason_strain_em_dark_metric_visible",
            "fractional_charge_window_weights",
        ],
    ),
    (
        "Book 04 matter section",
        BOOKS / "BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md",
        [
            "Matter as phason/window defects of the φ-quasicrystal vacuum",
            "generations = inflation classes",
            "quark color/charge = window-sector weights",
            "chirality = acceptance-window offset",
        ],
    ),
    (
        "Book 06 inertia section",
        BOOKS / "BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md",
        [
            "Runtime transport through aperiodic support",
            "requires phason flips under acceleration",
            "inertia is the finite rewrite cost",
            "phason_flip_drag_positive_cost",
        ],
    ),
    (
        "Book 07 phason gravity section",
        BOOKS / "BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md",
        [
            "Gravity sees both phonon and phason strain energy",
            "sees only active visible window",
            "archive phason strain is a dark metric source",
        ],
    ),
    (
        "Book 08 dark branch split",
        BOOKS / "BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md",
        [
            "dark matter = localized archive phason strain",
            "dark energy = determinant-balance/archive expansion",
            "archive phason dark-matter module",
        ],
    ),
    (
        "D0.All imports",
        LEAN / "All.lean",
        [
            "import D0.Physics.QuasicrystalPhenomenology",
            "import D0.Physics.WindowFractionalCharge",
        ],
    ),
    (
        "FinalBridgeIndex checks",
        LEAN / "Bridge" / "FinalBridgeIndex.lean",
        [
            "D0.Physics.quasi_generation_inflation_orbit",
            "D0.Physics.archive_phason_strain_em_dark_metric_visible",
            "D0.Physics.quasicrystal_phenomenology_operator_origin",
        ],
    ),
    (
        "HardClosureTheoremIndex checks",
        LEAN / "TheoremLedger" / "HardClosureTheoremIndex.lean",
        [
            "D0.Physics.window_offset_forces_chiral_readout",
            "D0.Physics.phason_flip_drag_positive_cost",
            "D0.Physics.fractional_charge_window_weights",
            "D0.Physics.quasicrystal_phenomenology_operator_origin",
        ],
    ),
    (
        "Hard closure target rows",
        DOCS / "HARD_CLOSURE_TARGETS.csv",
        [
            "T_quasi_generation_inflation_orbit",
            "T_archive_phason_strain_em_dark_metric_visible",
            "T_quasicrystal_phenomenology_operator_origin",
        ],
    ),
    (
        "Claim map row",
        DOCS / "CLAIM_TO_LEAN_MAP.csv",
        [
            "D0-QUASICRYSTAL-PHENOMENOLOGY-OPERATOR-ORIGIN-001",
            "D0.Physics.QuasicrystalPhenomenology",
            "vp_quasicrystal_phenomenology_operator_origin.py",
        ],
    ),
    (
        "Runner integration",
        RUNNER,
        [
            "quasicrystal-phenomenology",
            "PASS_QUASICRYSTAL_PHENOMENOLOGY_OPERATOR_ORIGIN",
            "check_v14_quasicrystal_phenomenology_operator_origin_sync.py",
        ],
    ),
]

CERT_CHECKS: list[tuple[str, str]] = [
    ("vp_quasi_generation_inflation.py", "PASS_QUASI_GENERATION_INFLATION_ORBIT"),
    ("vp_archive_phason_dark_matter.py", "PASS_DARK_PHASON_STRAIN"),
    ("vp_window_offset_chirality.py", "PASS_CHIRAL_WINDOW_OFFSET"),
    ("vp_phason_flip_inertia.py", "PASS_INERTIA_PHASON_FLIP_DRAG"),
    ("vp_window_fractional_charge.py", "PASS_FRACTIONAL_CHARGE_WINDOW_WEIGHT"),
    ("vp_quasicrystal_phenomenology_operator_origin.py", "PASS_QUASICRYSTAL_PHENOMENOLOGY_OPERATOR_ORIGIN"),
]

FORBIDDEN = ["sorry", "admit", "axiom", "unsafe", "Float", "constant", "opaque"]


def check_tokens(errors: list[str], label: str, path: Path, tokens: list[str]) -> None:
    if not path.exists():
        errors.append(f"{label}: missing {path.relative_to(ROOT)}")
        return
    text = read(path)
    for token in tokens:
        if token not in text:
            errors.append(f"{label}: missing token {token!r}")


def main() -> int:
    errors: list[str] = []

    for label, path, tokens in LEAN_CHECKS:
        check_tokens(errors, label, path, tokens)
        if path.exists():
            code = code_without_line_comments(path)
            for token in FORBIDDEN:
                if re.search(rf"\b{re.escape(token)}\b", code):
                    errors.append(f"{label}: forbidden token {token!r}")

    for label, path, tokens in TEXT_CHECKS:
        check_tokens(errors, label, path, tokens)

    for filename, token in CERT_CHECKS:
        path = CERTS / filename
        if not path.exists():
            errors.append(f"certificate missing: {filename}")
        elif token not in read(path):
            errors.append(f"certificate {filename}: missing token {token!r}")

    if errors:
        print("FAIL_V14_QUASICRYSTAL_PHENOMENOLOGY_OPERATOR_ORIGIN_SYNC")
        for error in errors:
            print("  -", error)
        return 1

    print("PASS_V14_QUASICRYSTAL_PHENOMENOLOGY_OPERATOR_ORIGIN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
