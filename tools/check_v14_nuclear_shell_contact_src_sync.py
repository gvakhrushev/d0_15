#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def require(label: str, text: str, tokens: list[str], errors: list[str]) -> None:
    for token in tokens:
        if token not in text:
            errors.append(f"{label}: missing token {token!r}")


def main() -> int:
    errors: list[str] = []
    require(
        "Lean SRC owner",
        read("09_LEAN_FORMALIZATION/D0/Matter/NuclearShellContactSRC.lean"),
        [
            "NuclearOrbital",
            "ShellOccupancy",
            "sameShellContact",
            "same_shell_contact_index_zero_for_unmatched_valence_protons",
            "same_shell_contact_turns_on_for_matched_valence_pn",
            "mass_number_alone_cannot_determine_src_contact",
            "neutron_excess_alone_cannot_determine_src_contact",
            "nuclear_shell_contact_src_closure",
        ],
        errors,
    )
    require(
        "Book 04 SRC section",
        read("01_BOOKS/BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md"),
        [
            "04.V Nuclear shell-contact SRC operator",
            "Shell Contact Index",
            "Ca48/Ca40",
            "Fe54/Ca48",
            "same-shell proton-neutron overlap",
        ],
        errors,
    )
    require(
        "Book 05 SRC no-go",
        read("01_BOOKS/BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md"),
        [
            "A-only SRC scalar failure",
            "N/Z-only SRC scalar failure",
            "density-only SRC scalar failure",
        ],
        errors,
    )
    require(
        "Book 08 SRC passport boundary",
        read("01_BOOKS/BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md"),
        [
            "Nuclear shell-contact SRC passport boundary",
            "SKIP_NATURE2026_SOURCE_DATA_REQUIRED",
        ],
        errors,
    )
    cert = subprocess.run(
        [sys.executable, str(ROOT / "05_CERTS/vp_nuclear_shell_contact_src.py"), "--mode", "synthetic"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if cert.returncode != 0:
        errors.append(f"SRC synthetic cert failed:\n{cert.stdout}\n{cert.stderr}")
    elif "PASS_NUCLEAR_SHELL_CONTACT_SRC_SYNTHETIC" not in cert.stdout:
        errors.append("SRC synthetic cert missing PASS_NUCLEAR_SHELL_CONTACT_SRC_SYNTHETIC")

    if errors:
        print("FAIL_V14_NUCLEAR_SHELL_CONTACT_SRC_SYNC")
        for error in errors:
            print("  -", error)
        return 1
    print("PASS_V14_NUCLEAR_SHELL_CONTACT_SRC_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
