#!/usr/bin/env python3
"""v14 Torus/Core13 geometry integration guard."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"


checks: list[tuple[str, Path, list[str]]] = [
    (
        "TorusCore13 Lean owner",
        LEAN / "Geometry" / "TorusCore13GeometryOrigin.lean",
        [
            "structure TorusParameter",
            "def inner",
            "def core",
            "def outer",
            "def minor",
            "def major",
            "def radialAdjacency",
            "def phaseDrift",
            "theorem radial_hopping_phase_drift_commutator_01",
            "theorem radial_hopping_phase_drift_noncommute",
        ],
    ),
    (
        "Generation selector torus bridge",
        LEAN / "Matter" / "GenerationSelectorOrigin.lean",
        [
            "import D0.Geometry.TorusCore13GeometryOrigin",
            "theorem torus_geometry_forces_generation_selector_noncommute",
        ],
    ),
    (
        "Generation overlap torus source",
        LEAN / "Matter" / "GenerationOverlapResponseOrigin.lean",
        [
            "theorem torus_shell_noncommutativity_forces_nonpermutation_overlap_source",
        ],
    ),
    (
        "Baryon shell carrier",
        LEAN / "Matter" / "BaryonS3Symmetrizer.lean",
        [
            "BaryonTripleShellCarrier",
            "baryon_triple_shell_card_eq_27",
        ],
    ),
    (
        "Book 00 torus architecture",
        ROOT / "03_THEORY_MAP" / "BOOK_REFACTOR_AUDIT.md",
        [
            "D0 memory torus and Core-13 geometry",
            "TorusCore13GeometryOrigin",
            "radial_hopping_phase_drift_noncommute",
            "PDG Core-13 remains a passport diagnostic",
        ],
    ),
    (
        "Book 01 Born relation",
        BOOKS / "BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md",
        [
            "Torus Shell Overlap And Born Readout",
            "phase-blind quadratic response",
        ],
    ),
    (
        "Book 02 proof spine",
        BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md",
        [
            "Torus-Core13 Geometry Origin",
            "D0.Geometry.TorusCore13GeometryOrigin",
            "torus_geometry_forces_generation_selector_noncommute",
        ],
    ),
    (
        "Book 03 torus shell interpretation",
        BOOKS / "BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md",
        [
            "K(9,11,13) Torus Shell Interpretation",
            "D=9",
            "D=11",
            "D=13",
            "phi^5",
        ],
    ),
    (
        "Book 04 matter integration",
        BOOKS / "BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md",
        [
            "torus_geometry_forces_generation_selector_noncommute",
            "torus_shell_noncommutativity_forces_nonpermutation_overlap_source",
            "BaryonTripleShellCarrier",
            "Torus shell radius is not a Higgs VEV",
        ],
    ),
    (
        "Book 05 passport rule",
        BOOKS / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md",
        [
            "PDG Strict Passport Protocol",
            "Torus geometry is core; PDG shell alignment is passport",
            "geometry diagnostic",
            "may not tune a core operator",
        ],
    ),
    (
        "Book 06 torus invariant",
        BOOKS / "BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md",
        [
            "Phi^5 Torus Invariant",
            "xi5 = phi^-5",
            "no SI",
            "length scale",
        ],
    ),
    (
        "Book 07 spin2 separation",
        BOOKS / "BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md",
        [
            "D0 memory torus is a separate internal shell geometry",
            "does not replace the terminal four-role TT",
            "projector",
        ],
    ),
    (
        "Book 08 passport pointer",
        BOOKS / "BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md",
        [
            "Core-13 Passport Boundary",
            # Books are publication-clean: prose pins de-pathified in §08.43.
            # Old repo-paths "08_PASSPORTS/PDG" and "vp_core13_shell_geometry_passport.py"
            # now read as clean concepts; lockstep the guard to the current prose.
            "the PDG passport",
            "the Core-13 shell-geometry passport",
        ],
    ),
    (
        "Torus cert",
        ROOT / "05_CERTS" / "vp_torus_core13_geometry_origin.py",
        ["PASS_TORUS_CORE13_GEOMETRY_ORIGIN"],
    ),
    (
        "Core13 passport cert",
        ROOT / "05_CERTS" / "vp_core13_shell_geometry_passport.py",
        ["PASS_CORE13_SHELL_GEOMETRY_PASSPORT", "SKIP_CORE13_SHELL_GEOMETRY_PASSPORT_DATA_MISSING"],
    ),
    (
        "PDG protocol",
        ROOT / "08_PASSPORTS" / "PDG" / "core13_geometry_protocol.json",
        ["Core-13 Shell Geometry Passport"],
    ),
]

errors: list[str] = []
for label, path, required in checks:
    if not path.exists():
        errors.append(f"{label}: missing file {path.relative_to(ROOT)}")
        continue
    text = path.read_text(encoding="utf-8")
    for token in required:
        if token not in text:
            errors.append(f"{label}: missing token {token!r}")

for rel in [
    "09_LEAN_FORMALIZATION/D0/All.lean",
    "09_LEAN_FORMALIZATION/D0/TheoremLedger/HardClosureTheoremIndex.lean",
    "09_LEAN_FORMALIZATION/D0/Bridge/FinalBridgeIndex.lean",
]:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    if "import D0.Geometry.TorusCore13GeometryOrigin" not in text:
        errors.append(f"{rel}: missing TorusCore13GeometryOrigin import")
    if not rel.endswith("All.lean"):
        for token in [
            "D0.Geometry.radial_hopping_phase_drift_noncommute",
            "D0.Matter.torus_geometry_forces_generation_selector_noncommute",
        ]:
            if token not in text:
                errors.append(f"{rel}: missing token {token}")

if errors:
    print("FAIL_V14_TORUS_CORE13_SYNC")
    for error in errors:
        print("  -", error)
    sys.exit(1)

print("PASS_V14_TORUS_CORE13_SYNC")
