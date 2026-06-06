#!/usr/bin/env python3
"""v14 gravity closure synchronization guard."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"
DOCS = ROOT / "09_LEAN_FORMALIZATION" / "docs"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def code_without_line_comments(path: Path) -> str:
    return "\n".join(line.split("--", 1)[0] for line in read(path).splitlines())


LEAN_CHECKS: list[tuple[str, Path, list[str]]] = [
    (
        "Entropic archive interface owner",
        LEAN / "Gravity" / "EntropicArchiveInterface.lean",
        [
            "FiniteArchiveGraph",
            "BoundaryCutWeight",
            "BoundaryCapacity",
            "boundary_capacity_nonnegative",
            "GraphLaplacian",
            "graph_laplacian_symmetric",
            "ArchiveFlux",
            "conserved_flux_no_creation",
            "EntropicBoundaryTension",
            "entropic_tension_energy_nonnegative",
            "entropic_archive_interface_closure",
        ],
    ),
    (
        "Macro Einstein interface owner",
        LEAN / "Gravity" / "MacroEinsteinInterface.lean",
        [
            "SpectralA2EHBridgeWitness",
            "spectral_a2_eh_bridge_closed",
            "FiniteGravityInterfaceWitness",
            "finite_gravity_witness_forces_macro_constraints",
            "finite_gravity_macro_constraints_closed",
            "macro_tension_yields_einstein_hilbert_interface",
            "macro_tension_einstein_hilbert_interface_closed",
            "finite_gravity_witness_yields_einstein_hilbert_interface",
        ],
    ),
    (
        "Finite spin-2 wave operator owner",
        LEAN / "Geometry" / "FiniteSpin2WaveOperator.lean",
        [
            "Role4",
            "eta4",
            "k4",
            "u4",
            "PiTT4",
            "WTT4",
            "spin2_coupling_depends_only_on_tt_stress",
            "finite_spin2_supplies_tt_macro_carrier",
        ],
    ),
    (
        "Higher-curvature finite cut owner",
        LEAN / "Geometry" / "HigherCurvatureSuppression.lean",
        [
            "higher_curvature_suppression_by_floor",
            "higher_curvature_terms_below_finite_readout_cut",
        ],
    ),
]


TEXT_CHECKS: list[tuple[str, Path, list[str]]] = [
    (
        "Book 00 gravity chain",
        ROOT / "03_THEORY_MAP" / "BOOK_REFACTOR_AUDIT.md",
        [
            "finite archive flow",
            "entropic boundary tension",
            "explicit TT projector and finite spin-2 wave operator",
            "Einstein-Hilbert macro interface",
        ],
    ),
    (
        "Book 02 gravity proof spine",
        BOOKS / "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md",
        [
            "Entropic archive gravity interface",
            "Finite spin-2 wave operator",
            "Higher-curvature finite cut",
            "Spectral A2 / EH bridge",
            "Macro Einstein interface",
        ],
    ),
    (
        "Book 05 gravity verification rule",
        BOOKS / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md",
        [
            "Gravity closure requires:",
            "finite graph/entropy cert",
            "explicit Pi_TT and W_TT",
            "higher-curvature cut",
            "spectral A2/EH bridge",
            "no continuum constants imported as core",
        ],
    ),
    (
        "Book 06 gravity runtime boundary",
        BOOKS / "BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md",
        [
            "c_D0 = 1 tick gauge",
            "eta4 terminal signature",
            "delta0 finite readout cut",
            "heat trace scale is internal, not SI time",
        ],
    ),
    (
        "Book 07 fourteen-step gravity chain",
        BOOKS / "BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md",
        [
            "07.1 Archive variation and finite stress",
            "07.2 Graph Laplacian and heat trace",
            "07.3 Boundary capacity as finite holographic area",
            "07.4 Entropic surface tension",
            "07.5 Conservation of archive flux",
            "07.6 Symmetric stress representative",
            "07.7 Terminal 4-role Lorentz/tick carrier",
            "07.8 Explicit TT projector Pi_TT",
            "07.9 Finite wave operator W_TT",
            "07.10 Gauge/trace ghost annihilation",
            "07.11 TT stress coupling",
            "07.12 Higher-curvature finite cut",
            "07.13 Spectral A2 / Einstein-Hilbert bridge",
            "07.14 Macro Einstein interface theorem",
        ],
    ),
    (
        "Book 08 archive entropy citation",
        BOOKS / "BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md",
        [
            "Cosmological acceleration/entropy flow uses archive entropy layer",
            "D0.Gravity.EntropicArchiveInterface",
            "not import continuum GR as primitive",
        ],
    ),
    (
        "FinalBridgeIndex gravity checks",
        LEAN / "Bridge" / "FinalBridgeIndex.lean",
        [
            "D0.Gravity.boundary_capacity_nonnegative",
            "D0.Gravity.finite_gravity_macro_constraints_closed",
            "D0.Gravity.finite_gravity_witness_yields_einstein_hilbert_interface",
        ],
    ),
    (
        "HardClosureTheoremIndex gravity checks",
        LEAN / "TheoremLedger" / "HardClosureTheoremIndex.lean",
        [
            "D0.Gravity.boundary_capacity_nonnegative",
            "D0.Geometry.finite_spin2_supplies_tt_macro_carrier",
            "D0.Geometry.HigherCurvatureSuppression.higher_curvature_terms_below_finite_readout_cut",
            "D0.Gravity.finite_gravity_witness_yields_einstein_hilbert_interface",
        ],
    ),
    (
        "Claim map gravity rows",
        DOCS / "CLAIM_TO_LEAN_MAP.csv",
        [
            "D0-GRAVITY-ENTROPIC-ARCHIVE-001",
            "D0-GRAVITY-MACRO-EINSTEIN-INTERFACE-001",
            "vp_entropic_archive_gravity.py",
            "vp_macro_einstein_interface.py",
        ],
    ),
]


CERT_CHECKS = [
    ("05_CERTS/vp_entropic_archive_gravity.py", "PASS_ENTROPIC_ARCHIVE_GRAVITY"),
    ("05_CERTS/vp_finite_spin2_wave_operator.py", "PASS_FINITE_SPIN2_WAVE_OPERATOR_CONCRETE"),
    ("05_CERTS/vp_macro_einstein_interface.py", "PASS_MACRO_EINSTEIN_INTERFACE"),
]


FORBIDDEN = ["sorry", "admit", "axiom", "unsafe", "Float"]


def main() -> int:
    errors: list[str] = []

    for label, path, tokens in LEAN_CHECKS:
        if not path.exists():
            errors.append(f"{label}: missing {path.relative_to(ROOT)}")
            continue
        text = read(path)
        code = code_without_line_comments(path)
        for token in tokens:
            if token not in text:
                errors.append(f"{label}: missing token {token!r}")
        for token in FORBIDDEN:
            if re.search(rf"\b{re.escape(token)}\b", code):
                errors.append(f"{label}: forbidden token {token!r}")

    for label, path, tokens in TEXT_CHECKS:
        if not path.exists():
            errors.append(f"{label}: missing {path.relative_to(ROOT)}")
            continue
        text = read(path)
        for token in tokens:
            if token not in text:
                errors.append(f"{label}: missing token {token!r}")

    for rel, token in CERT_CHECKS:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"cert {rel}: missing")
            continue
        if token not in read(path):
            errors.append(f"cert {rel}: missing token {token}")

    if errors:
        print("FAIL_V14_GRAVITY_CLOSURE_SYNC")
        for error in errors:
            print("  -", error)
        return 1

    print("PASS_V14_GRAVITY_CLOSURE_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
