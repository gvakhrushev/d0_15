#!/usr/bin/env python3
"""v14 global operator-geometry synchronization guard."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"


CHECKS: list[tuple[str, Path, list[str], list[str]]] = [
    (
        "Torus/Core13 geometry owner",
        LEAN / "Geometry" / "TorusCore13GeometryOrigin.lean",
        ["TorusParameter", "TorusShell", "radial_hopping_phase_drift_noncommute"],
        ["sorry", "admit", "axiom", "unsafe", "Float"],
    ),
    (
        "Generation selector owner",
        LEAN / "Matter" / "GenerationSelectorOrigin.lean",
        ["torus_geometry_forces_generation_selector_noncommute"],
        ["sorry", "admit", "axiom", "unsafe", "Float"],
    ),
    (
        "Generation overlap owner",
        LEAN / "Matter" / "GenerationOverlapResponseOrigin.lean",
        ["IsPermutationWitness", "IsUnistochasticOverlap", "torus_shell_noncommutativity_forces_nonpermutation_overlap_source"],
        ["sorry", "admit", "axiom", "unsafe", "Float"],
    ),
    (
        "CKM nontrivial flavour owner",
        LEAN / "Matter" / "CKMNontrivialFlavourAlgebra.lean",
        ["overlap_response_can_force_nonpermutation_transfer", "nontrivial_flavour_defect_positive_response"],
        ["sorry", "admit", "axiom", "unsafe", "Float"],
    ),
    (
        "Meson defect-transfer origin owner",
        LEAN / "Matter" / "MesonDefectTransferOrigin.lean",
        ["meson_support_projector_idempotent", "meson_positive_defect_transfer_admissible"],
        ["sorry", "admit", "axiom", "unsafe", "Float"],
    ),
    (
        "Baryon S3 owner",
        LEAN / "Matter" / "BaryonS3Symmetrizer.lean",
        ["BaryonTripleShellCarrier", "baryon_triple_shell_card_eq_27", "sorted_triple_card_eq_ten"],
        ["sorry", "admit", "axiom", "unsafe", "Float"],
    ),
    (
        "Higgs scalar projector owner",
        LEAN / "Matter" / "HiggsScalarProjectorConstructive.lean",
        [
            "FrozenSU2_X",
            "FrozenSU2_Z",
            "commutes_XZ_forces_scalar_matrix",
            "nonzero_gauge_idempotent_eq_identity",
            "rank1_scalar_projector_breaks_su2_gauge_compatibility",
            "minimal_positive_scalar_projector_rank_two",
            "higgs_yukawa_core_promotion_valid",
        ],
        ["sorry", "admit", "axiom", "unsafe", "Float"],
    ),
    (
        "Finite spin-2 wave operator owner",
        LEAN / "Geometry" / "FiniteSpin2WaveOperator.lean",
        ["PiTT4", "WTT4", "spin2_coupling_depends_only_on_tt_stress"],
        ["sorry", "admit", "axiom", "unsafe", "Float"],
    ),
    (
        "Born quadratic origin owner",
        LEAN / "Core" / "BornQuadraticOrigin.lean",
        ["parallelogram_response_is_quadratic_form", "quarter_turn_quadratic_forces_norm_square"],
        ["sorry", "admit", "axiom", "unsafe", "Float"],
    ),
    (
        "PDG passport certs",
        ROOT / "05_CERTS" / "vp_pdg_strict_passport.py",
        ["PASS_PDG_STRICT_PASSPORT"],
        [],
    ),
    (
        "Core13 passport cert",
        ROOT / "05_CERTS" / "vp_core13_shell_geometry_passport.py",
        ["PASS_CORE13_SHELL_GEOMETRY_PASSPORT"],
        [],
    ),
    (
        "PDG pinned dataset manifest",
        ROOT / "08_PASSPORTS" / "PDG" / "pdg_dataset_manifest.json",
        ["PINNED_EXTERNAL_PDG_DATASET", "7073c02222f08c19f5c40e422c5a54e9f9a75622b9e10b1b64096144e262d4b5"],
        ["DATA_PENDING", "null"],
    ),
    (
        "PDG pinned dataset file",
        ROOT / "08_PASSPORTS" / "PDG" / "data" / "mass_width_2025.mcd",
        ["MASSES, WIDTHS, AND MC ID NUMBERS FROM 2025 EDITION OF RPP"],
        [],
    ),
    (
        "Book 00 global chain",
        ROOT / "03_THEORY_MAP" / "BOOK_REFACTOR_AUDIT.md",
        ["Born quadratic response", "Torus/Core-13 shell geometry", "explicit TT projector", "operator first, passport second"],
        [],
    ),
    (
        "Book 01 Born 4.0",
        BOOKS / "BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md",
        ["Born 4.0", "D0.Core.BornQuadraticOrigin", "vp_born_quadratic_origin.py"],
        [],
    ),
    (
        "Book 02 proof spine",
        BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md",
        ["D0.Matter.CKMNontrivialFlavourAlgebra", "D0.Matter.MesonDefectTransferOrigin", "D0.Core.BornQuadraticOrigin"],
        [],
    ),
    (
        "Book 03 torus geometry",
        BOOKS / "BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md",
        ["K(9,11,13) Torus Shell Interpretation", "D=9", "D=11", "D=13", "phi^5"],
        [],
    ),
    (
        "Book 04 matter operators",
        BOOKS / "BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md",
        ["D0.Matter.CKMNontrivialFlavourAlgebra", "D0.Matter.MesonDefectTransferOrigin", "BaryonS3Symmetrizer", "HiggsScalarProjectorConstructive"],
        [],
    ),
    (
        "Book 05 verification rules",
        BOOKS / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md",
        ["operator first", "passport second", "no PDG tuning", "no geometry diagnostic as core source"],
        [],
    ),
    (
        "Book 06 constants and tick-gauge",
        BOOKS / "BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md",
        ["xi5 = phi^-5", "c_D0=1", "eta4 = diag(1,-1,-1,-1)"],
        [],
    ),
    (
        "Book 07 spin-2 operator",
        BOOKS / "BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md",
        ["D0.Geometry.FiniteSpin2WaveOperator", "PiTT4(h)", "WTT4"],
        [],
    ),
    (
        "Book 08 passport separation",
        BOOKS / "BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md",
        ["Core-13 particle-shell diagnostics", "cosmological survey", "PDG passport"],
        [],
    ),
]


CERTS = [
    ("05_CERTS/vp_torus_core13_geometry_origin.py", "PASS_TORUS_CORE13_GEOMETRY_ORIGIN"),
    ("05_CERTS/vp_generation_overlap_response_origin.py", "PASS_GENERATION_OVERLAP_RESPONSE_ORIGIN"),
    ("05_CERTS/vp_meson_positive_defect_transfer.py", "PASS_MESON_POSITIVE_DEFECT_TRANSFER"),
    ("05_CERTS/vp_baryon_s3_symmetrizer.py", "PASS_BARYON_S3_SYMMETRIZER"),
    ("05_CERTS/vp_finite_spin2_wave_operator.py", "PASS_FINITE_SPIN2_WAVE_OPERATOR_CONCRETE"),
    ("05_CERTS/vp_born_quadratic_origin.py", "PASS_BORN_QUADRATIC_ORIGIN"),
    ("05_CERTS/vp_core13_shell_geometry_passport.py", "PASS_CORE13_SHELL_GEOMETRY_PASSPORT"),
    ("05_CERTS/vp_pdg_strict_passport.py", "PASS_PDG_STRICT_PASSPORT"),
]


def main() -> int:
    errors: list[str] = []
    for label, path, required, forbidden in CHECKS:
        if not path.exists():
            errors.append(f"{label}: missing {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        for token in required:
            if token not in text:
                errors.append(f"{label}: missing token {token!r}")
        for token in forbidden:
            if token in text:
                errors.append(f"{label}: forbidden token {token!r}")

    for rel, token in CERTS:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"cert {rel}: missing")
            continue
        if token not in path.read_text(encoding="utf-8"):
            errors.append(f"cert {rel}: missing token {token}")

    if errors:
        print("FAIL_V14_GLOBAL_OPERATOR_GEOMETRY_SYNC")
        for error in errors:
            print("  -", error)
        return 1

    print("PASS_V14_GLOBAL_OPERATOR_GEOMETRY_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
