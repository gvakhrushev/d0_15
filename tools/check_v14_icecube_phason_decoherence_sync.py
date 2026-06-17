#!/usr/bin/env python3
"""v14 QUASI-005 IceCube neutrino phason-decoherence sync guard."""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "09_LEAN_FORMALIZATION" / "D0"
BOOKS = ROOT / "01_BOOKS"
DOCS = ROOT / "09_LEAN_FORMALIZATION" / "docs"
CERTS = ROOT / "05_CERTS"
PASSPORT = ROOT / "08_PASSPORTS" / "IceCube"
RUNNER = ROOT / "tools" / "run_hard_theorem_closure.py"

CHECKS: list[tuple[str, Path, list[str]]] = [
    (
        "Neutrino phason Lean owner",
        LEAN / "Matter" / "NeutrinoPhasonWaves.lean",
        [
            "NeutralPhasonWave",
            "neutrino_neutral_leakage_is_bulk_phason_wave",
            "neutral_phason_wave_has_no_em_coupling",
            "delta0_over_four_is_phason_birefringence_seed",
            "hurwitz_gap_scattering_kernel_admissible",
            "phason_wave_decoherence_kernel_positive",
        ],
    ),
    (
        "IceCube passport Lean owner",
        LEAN / "Passport" / "IceCubePhasonDecoherence.lean",
        [
            "IceCubeManifest",
            "IceCubeManifestComplete",
            "icecube_decoherence_passport_requires_external_manifest",
            "empty_icecube_manifest_cannot_run",
            "icecube_passport_uses_frozen_phason_kernel",
        ],
    ),
    (
        "IceCube passport cert",
        CERTS / "vp_neutrino_phason_decoherence_passport.py",
        [
            "SKIP_NEUTRINO_PHASON_DECOHERENCE_EXTERNAL_DATA_REQUIRED",
            "PASS_ICECUBE_PHASON_DECOHERENCE_PASSPORT",
            "manifest_only",
            "icecube_hese",
            "icecube_tracks",
        ],
    ),
    (
        "IceCube manifest",
        PASSPORT / "icecube_manifest.json",
        ["dataset_name", "source_url_or_local_path", "sha256", "energy_field"],
    ),
    (
        "Book 04 neutrino line",
        BOOKS / "BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md",
        ["Neutrino is interpreted as neutral bulk phason wave", "neutral_phason_wave_has_no_em_coupling"],
    ),
    (
        "Book 05 passport rule",
        BOOKS / "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md",
        ["IceCube comparison is EMPIRICAL-PASSPORT", "cannot select or tune the D0 neutrino kernel"],
    ),
    (
        "Book 08 falsification hook",
        BOOKS / "BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md",
        ["High-energy neutrino decoherence is a falsification hook", "neutrino phason-decoherence passport"],
    ),
    (
        "Hard theorem targets",
        DOCS / "HARD_CLOSURE_TARGETS.csv",
        ["T_icecube_neutrino_bulk_phason_wave", "T_icecube_passport_requires_external_manifest"],
    ),
    (
        "Claim map row",
        DOCS / "CLAIM_TO_LEAN_MAP.csv",
        ["D0-ICECUBE-001", "D0.Passport.IceCubePhasonDecoherence", "vp_neutrino_phason_decoherence_passport.py"],
    ),
    (
        "Runner integration",
        RUNNER,
        ["icecube-phason-decoherence", "SKIP_NEUTRINO_PHASON_DECOHERENCE_EXTERNAL_DATA_REQUIRED"],
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
        LEAN / "Matter" / "NeutrinoPhasonWaves.lean",
        LEAN / "Passport" / "IceCubePhasonDecoherence.lean",
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
    print("PASS_ICECUBE_PHASON_DECOHERENCE_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
