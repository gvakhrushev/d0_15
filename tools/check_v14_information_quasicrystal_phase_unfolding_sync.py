#!/usr/bin/env python3
"""v14 information-quasicrystal phase-unfolding synchronization guard."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"
DOCS = ROOT / "09_LEAN_FORMALIZATION" / "docs"
RUNNER = ROOT / "tools" / "run_hard_theorem_closure.py"
CERT = ROOT / "05_CERTS" / "vp_information_quasicrystal_phase_unfolding.py"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def code_without_line_comments(path: Path) -> str:
    return "\n".join(line.split("--", 1)[0] for line in read(path).splitlines())


LEAN_CHECKS: list[tuple[str, Path, list[str]]] = [
    (
        "Hurwitz rigid phase owner",
        LEAN / "Geometry" / "HurwitzRigidPhaseGenerator.lean",
        [
            "NonPeriodicPhase",
            "sqrt_five_irrational",
            "phi_irrational",
            "alphaD0_irrational",
            "phi_phase_is_nonperiodic",
            "phi_continued_fraction_all_ones",
            "hurwitz_rigid_low_denominator_bound",
            "hurwitzRigidPhaseGeneratorClosure",
        ],
    ),
    (
        "Phase return branch count owner",
        LEAN / "Geometry" / "PhaseReturnBranchCount.lean",
        [
            "FiniteReturnModulusBranchCount",
            "finite_return_modulus_unfolds_branches",
            "terminal_return_branch_count",
            "electroweak_return_branch_count",
            "electroweak_return_depth_eq_35",
        ],
    ),
    (
        "Phase unfolding quasicrystal owner",
        LEAN / "Geometry" / "PhaseUnfoldingQuasicrystal.lean",
        [
            "StableLongRangeReturnStructure",
            "PeriodicLatticeLock",
            "QuasicrystalOrderNotPeriodicLattice",
            "ToralOrderedRuntime",
            "toral_runtime_supplies_quasicrystal_order",
            "quasicrystal_order_not_periodic_lattice",
            "phaseUnfoldingQuasicrystalClosure",
        ],
    ),
]

TEXT_CHECKS: list[tuple[str, Path, list[str]]] = [
    (
        "Book 00 information quasicrystal thesis",
        ROOT / "03_THEORY_MAP" / "BOOK_REFACTOR_AUDIT.md",
        [
            "D0 detector/vacuum support is a finite information quasicrystal",
            "finite information quasicrystal",
            "quasicrystal_order_not_periodic_lattice",
        ],
    ),
    (
        "Book 01 phase-unfolding master chain",
        BOOKS / "BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md",
        [
            "tick order",
            "irrational phi^-2 phase",
            "finite return modulus",
            "residue branches",
            "D0.Geometry.PhaseUnfoldingQuasicrystal",
        ],
    ),
    (
        "Book 06 toral runtime",
        BOOKS / "BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md",
        [
            "time operator supplies the non-periodic ordered runtime",
            "toral_runtime_supplies_quasicrystal_order",
        ],
    ),
    (
        "Book 07 Hurwitz promotion",
        BOOKS / "BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md",
        [
            "finite information-quasicrystal",
            "phi_phase_is_nonperiodic",
            "finite_return_modulus_unfolds_branches",
        ],
    ),
    (
        "Book 08 smooth macro-shadow",
        BOOKS / "BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md",
        [
            "smoothness is the coarse-grained shadow of a finite",
            "information quasicrystal",
            "q_T=44",
            "q_EW=710",
        ],
    ),
    (
        "D0.All imports",
        LEAN / "All.lean",
        [
            "import D0.Geometry.HurwitzRigidPhaseGenerator",
            "import D0.Geometry.PhaseReturnBranchCount",
            "import D0.Geometry.PhaseUnfoldingQuasicrystal",
        ],
    ),
    (
        "FinalBridgeIndex checks",
        LEAN / "Bridge" / "FinalBridgeIndex.lean",
        [
            "D0.Geometry.phi_phase_is_nonperiodic",
            "D0.Geometry.finite_return_modulus_unfolds_branches",
            "D0.Geometry.quasicrystal_order_not_periodic_lattice",
        ],
    ),
    (
        "HardClosureTheoremIndex checks",
        LEAN / "TheoremLedger" / "HardClosureTheoremIndex.lean",
        [
            "D0.Geometry.phi_phase_is_nonperiodic",
            "D0.Geometry.hurwitz_rigid_low_denominator_bound",
            "D0.Geometry.finite_return_modulus_unfolds_branches",
            "D0.Geometry.quasicrystal_order_not_periodic_lattice",
        ],
    ),
    (
        "Hard closure target rows",
        DOCS / "HARD_CLOSURE_TARGETS.csv",
        [
            "T_information_phi_phase_nonperiodic",
            "T_information_finite_return_modulus_unfolds_branches",
            "T_information_quasicrystal_order_not_periodic_lattice",
        ],
    ),
    (
        "Claim map row",
        DOCS / "CLAIM_TO_LEAN_MAP.csv",
        [
            "D0-INFORMATION-QUASICRYSTAL-PHASE-UNFOLDING-001",
            "D0.Geometry.HurwitzRigidPhaseGenerator;D0.Geometry.PhaseReturnBranchCount;D0.Geometry.PhaseUnfoldingQuasicrystal",
            "vp_information_quasicrystal_phase_unfolding.py",
        ],
    ),
    (
        "Hard closure runner integration",
        RUNNER,
        [
            "vp_information_quasicrystal_phase_unfolding.py",
            "PASS_INFORMATION_QUASICRYSTAL_PHASE_UNFOLDING",
            "check_v14_information_quasicrystal_phase_unfolding_sync.py",
        ],
    ),
]

FORBIDDEN = ["sorry", "admit", "axiom", "unsafe", "Float"]


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

    if not CERT.exists():
        errors.append("information-quasicrystal certificate is missing")
    elif "PASS_INFORMATION_QUASICRYSTAL_PHASE_UNFOLDING" not in read(CERT):
        errors.append("information-quasicrystal certificate missing PASS token")

    if errors:
        print("FAIL_V14_INFORMATION_QUASICRYSTAL_PHASE_UNFOLDING_SYNC")
        for error in errors:
            print("  -", error)
        return 1

    print("PASS_V14_INFORMATION_QUASICRYSTAL_PHASE_UNFOLDING_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
