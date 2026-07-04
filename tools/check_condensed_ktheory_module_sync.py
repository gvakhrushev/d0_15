#!/usr/bin/env python3
"""D0 condensed K-theory module sync guard."""

from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
CERTS = ROOT / "05_CERTS"
BOOKS = ROOT / "01_BOOKS"

CHECKS: list[tuple[str, Path, list[str]]] = [
    (
        "Tiling Hull Lean module",
        LEAN / "Topology" / "TilingHull.lean",
        [
            "D0.Topology",
            "LocalPatch",
            "TilingRule",
            "D0TilingHull",
            "d0_hull_has_finite_local_complexity",
            "d0_hull_has_phi_cut_project_origin",
            "d0_hull_is_nonperiodic",
            "d0_hull_has_long_range_order",
            "d0_hull_supports_gap_labeling"
        ]
    ),
    (
        "K-theory Gap Labeling Lean module",
        LEAN / "Matter" / "KTheoryGapLabeling.lean",
        [
            "D0.Matter",
            "K0Label",
            "SpectralGap",
            "GapLabelingSystem",
            "D0GapLabeledSpectrum",
            "gap_label_is_topological_not_fitted",
            "d0_gap_labels_are_countable"
        ]
    ),
    (
        "Noncommutative Solenoid Lean module",
        LEAN / "Geometry" / "NonCommutativeSolenoid.lean",
        [
            "D0.Geometry",
            "NonCommutativeSolenoid"
        ]
    ),
    (
        "Noncommutative Solenoid Gravity Lean module",
        LEAN / "Geometry" / "NonCommutativeSolenoidGravity.lean",
        [
            "D0.Geometry",
            "SpectralTripleApprox",
            "D0SolenoidSpectralGeometry"
        ]
    ),
    (
        "Gap Labeling Cert",
        CERTS / "vp_gap_labeling_d0_tiling_hull.py",
        [
            "PASS_D0_GAP_LABELING_TILING_HULL",
            "d0_gap_labels.json"
        ]
    ),
    (
        "Noncommutative Solenoid Gravity Cert",
        CERTS / "vp_noncommutative_solenoid_gravity.py",
        [
            "PASS_NONCOMMUTATIVE_SOLENOID_GRAVITY"
        ]
    )
]

FORBIDDEN_LEAN_TOKENS = ["sorry", "admit", "axiom", "unsafe", "Float", "opaque"]

# EXTERNAL-GAP (Phase L honesty refactor): these theorem names were placeholder
# identities ((stmt)(h) := h) and were DELIBERATELY removed from the Lean tree.
# K-theory / Connes spectral-triple / phason-holonomy class are not in Mathlib 4.30;
# the finite content stays cert-closed by the python certs, and the Lean
# structures-scaffold remains in the modules for the Bridge index only, not as proofs.
# See 03_THEORY_MAP/theory_status_map.csv rows: D0-KTHEORY-001, D0-MESON-K0-001,
# D0-CKM-K0-001, D0-SDE-K0-001, D0-SOLENOID-001, D0-SOLENOID-GRAVITY-001.
# This guard asserts the placeholders STAY removed — do not re-add them to Lean.
REMOVED_PLACEHOLDERS: list[tuple[str, Path, list[str]]] = [
    (
        "K-theory Gap Labeling Lean module (Phase-L removed placeholders)",
        LEAN / "Matter" / "KTheoryGapLabeling.lean",
        [
            "gap_labeling_requires_frozen_operator",
            "meson_domain_wall_spectrum_admits_k0_labels",
            "ckm_holonomy_spectrum_admits_k0_labels",
            "archive_pressure_spectrum_admits_k0_labels"
        ]
    ),
    (
        "Noncommutative Solenoid Lean module (Phase-L removed placeholders)",
        LEAN / "Geometry" / "NonCommutativeSolenoid.lean",
        [
            "d0_hull_admits_noncommutative_solenoid_model"
        ]
    ),
    (
        "Noncommutative Solenoid Gravity Lean module (Phase-L removed placeholders)",
        LEAN / "Geometry" / "NonCommutativeSolenoidGravity.lean",
        [
            "d0_heat_trace_admits_solenoid_spectral_triple_approx",
            "finite_spin2_operator_is_tt_sector_of_solenoid_spectral_geometry",
            "wtt4_is_compatible_with_noncommutative_solenoid_geometry"
        ]
    )
]

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

    # EXTERNAL-GAP guard: removed Phase-L placeholders must NOT reappear in Lean
    for label, path, tokens in REMOVED_PLACEHOLDERS:
        if not path.exists():
            errors.append(f"{label}: missing {path.relative_to(ROOT)}")
            continue
        text = read(path)
        for token in tokens:
            if token in text:
                errors.append(
                    f"{label}: removed placeholder {token!r} reappeared "
                    f"(EXTERNAL-GAP per theory_status_map.csv; do not re-add)"
                )

    # Check for forbidden tokens in all new Lean modules
    for filename in ["Topology/TilingHull.lean", "Matter/KTheoryGapLabeling.lean",
                     "Geometry/NonCommutativeSolenoid.lean", "Geometry/NonCommutativeSolenoidGravity.lean"]:
        path = LEAN / filename
        if path.exists():
            code = code_without_line_comments(path)
            for token in FORBIDDEN_LEAN_TOKENS:
                if re.search(rf"\b{re.escape(token)}\b", code):
                    errors.append(f"{path.relative_to(ROOT)} contains forbidden token {token!r}")

    # Check that Book 00/02/04/05/07/08 are updated with new key terms
    for filename in ["BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md",
                     "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md",
                     "BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md",
                     "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md",
                     "BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md",
                     "BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md"]:
        book_path = BOOKS / filename
        if book_path.exists():
            content = read(book_path)
            terms = ["solenoid", "hull", "gap", "K-theory", "quasicrystal", "phason"]
            if not any(term.lower() in content.lower() for term in terms):
                errors.append(f"{book_path.relative_to(ROOT)} lacks K-theory / gap labeling / solenoid / hull / quasicrystal / phason references")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("PASS_CONDENSED_KTHEORY_MODULE_SYNC")
    return 0

if __name__ == "__main__":
    sys.exit(main())
