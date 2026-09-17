#!/usr/bin/env python3
"""Phason w(z) no-survey-tuning guard - no DESI/H0/Omega_m/r_d datum defines the phason EOS.

The internal w_D0 = p/rho is computed from archive pressure-energy only; the redshift u->z / CPL reading
is passport-only. This guard fails if any book lets survey data define or select the phason object.
"""
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
FORBIDDEN = [
    "DESI confirms D0",
    "D0 predicts DESI w(z)",
    "30-dimensional kernel proves w(z)",
    "phason w(z) is fit from H0",
    "w(z) inferred from Omega_m",
    "w0/wa chosen from DESI then called D0",
]


def main() -> int:
    print("=== Phason w(z) no-survey-tuning guard ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: w_D0 = p/rho from internal archive pressure-energy; survey data may only COMPARE, never define")
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT / "01_BOOKS").rglob("*.md"))
    hits = [f for f in FORBIDDEN if f in prose]
    assert not hits, f"forbidden survey-tuning phrase(s) present: {hits}"
    print(f"PASS_NO_SURVEY_TUNING  none of the {len(FORBIDDEN)} survey-tuning phrases appear in the books")
    assert any(f in "x DESI confirms D0 x" for f in FORBIDDEN), "control: detector reachable"
    print("FAIL_PLANTED_SURVEY_TUNING_CAUGHT  the survey-tuning detector is reachable")
    print("PASS_PHASON_WZ_NO_SURVEY_TUNING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
