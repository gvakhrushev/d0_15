#!/usr/bin/env python3
"""D0 book K-theory and gap labeling sync guard."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "01_BOOKS"

REQUIRED_HEADERS: dict[str, list[str]] = {
    "BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md": [
        "## 00.4a D0 vacuum as condensed φ-quasicrystalline tiling hull",
        "## 00.9a Gap-label firewall"
    ],
    "BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md": [
        "## 01.4a Condensed φ-quasicrystalline support",
        "## 01.19a Cut-and-project reading of phase unfolding"
    ],
    "BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md": [
        "## 02.34 Master Evolution and φ-quasicrystal proof spine"
    ],
    "BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md": [
        "## 03.21a Gap labels do not create new action sections"
    ],
    "BOOK_04_SPECTRUM_MATTER_AND_FINITE_SELECTOR_THEORY.md": [
        "## 04.U Matter as defects and gap-labeled spectra of the φ-quasicrystal hull"
    ],
    "BOOK_05_VERIFICATION_STATUS_AND_CERTIFICATE_DISCIPLINE.md": [
        "## 05.10a Gap-label certificate discipline",
        "## 05.11a Risky prediction passport discipline"
    ],
    "BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md": [
        "## 06.30a Time evolution over the φ-quasicrystalline hull",
        "## 06.31a Gap-labeled RG bands"
    ],
    "BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY.md": [
        "## 07.6a Trace–Heat geometry over the D0 tiling hull",
        "## 07.47 Noncommutative solenoid gravity",
        "## 07.48 LIGO BBH mass-defect passport"
    ],
    "BOOK_08_COSMOLOGY_ARCHIVE_AND_SDE_TRANSFER.md": [
        "## 08.7a Dark matter as archive phason glass",
        "## 08.12.3 S_DE as gap-labeled phason-flip spectrum",
        "## 08.42 IceCube neutrino phason decoherence passport",
        "## 08.43 CMB phason-flip entropy spectrum passport",
        "## 08.44 Archive phason halo / lensing passport"
    ]
}

def main() -> int:
    errors = []
    for filename, headers in REQUIRED_HEADERS.items():
        path = BOOKS / filename
        if not path.exists():
            errors.append(f"Missing book: {filename}")
            continue
        content = path.read_text(encoding="utf-8")
        for header in headers:
            if header not in content:
                errors.append(f"Book {filename} is missing required section header: {header!r}")
                
    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        return 1
    
    print("PASS_BOOK_KTHEORY_GAPLABEL_SYNC")
    return 0

if __name__ == "__main__":
    sys.exit(main())
