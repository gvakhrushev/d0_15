#!/usr/bin/env python3
"""D0-PHASON w(z) passport boundary - redshift/CPL is downstream packaging, never the core definition.

The internal w_N (and any future w_D0(u)) is defined from finite archive pressure-energy on the window n
BEFORE any redshift; the u->z / CPL reading is passport-only. This guard fails if a book lets
DESI/BAO/H0/Omega_m/r_d enter the core definition or promotes the survey comparison to CORE.
"""
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
FORBIDDEN = [
    "DESI confirms D0",
    "kernel proves w(z)",
    "w0 wa are core",
    "w0/wa are core",
    "redshift is the core variable",
    "CPL parameters define the phason",
]


def main() -> int:
    print("=== D0-PHASON w(z) passport boundary ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: w_N/w_D0(u) defined from internal window-n pressure-energy BEFORE z/CPL; redshift is passport-only")
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT / "01_BOOKS").rglob("*.md"))
    hits = [f for f in FORBIDDEN if f in prose]
    assert not hits, f"forbidden passport-boundary violation(s): {hits}"
    print(f"PASS_PASSPORT_BOUNDARY  none of the {len(FORBIDDEN)} core-definition violations appear in the books (z/CPL stay passport)")
    assert any(f in "x DESI confirms D0 x" for f in FORBIDDEN), "control: detector reachable"
    print("FAIL_PLANTED_BOUNDARY_VIOLATION_CAUGHT  the detector is reachable")
    print("PASS_PHASON_WZ_PASSPORT_BOUNDARY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
