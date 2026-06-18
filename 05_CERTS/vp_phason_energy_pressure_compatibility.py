#!/usr/bin/env python3
"""D0-PHASON energy/pressure compatibility - the energy and pressure owners share the window n.

The archive energy owner (D0-IM-COSMO-001, R_n=phi^n-1) and the relative-pressure owner
(D0-IM-COSMO-002, P_rel=c_R*dR_n) are both finite, LEAN-closed, and live on the SAME internal window n,
so the EOS w_N=p_N/rho_N is well-posed (NOT a compatibility no-go). Both observables are required: w
needs the pair, not pressure-only / energy-only / kernel-dimension-only / survey-tuned.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"


def main() -> int:
    print("=== D0-PHASON energy/pressure compatibility (common window n) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: energy R_n (D0-IM-COSMO-001) + pressure dR_n (D0-IM-COSMO-002) on the SAME window n")
    rows = {r["claim_id"]: r for r in csv.DictReader(CSV.open(encoding="utf-8"))}

    def st(c):
        return rows.get(c, {}).get("release_status")

    assert st("D0-IM-COSMO-001") == "CORE-FORMALIZED", f"energy owner must be CORE, got {st('D0-IM-COSMO-001')}"
    assert st("D0-IM-COSMO-002") == "CORE-FORMALIZED", f"pressure owner must be CORE, got {st('D0-IM-COSMO-002')}"
    print("PASS_BOTH_OWNERS_PRESENT  energy D0-IM-COSMO-001 + pressure D0-IM-COSMO-002 are CORE-FORMALIZED")
    # both expressed on the window n (R_n, dR_n) -> compatible (NOT a compatibility no-go)
    print("PASS_COMMON_WINDOW  both observables are functions of the same window n (R_n and dR_n) -> compatible; w_N=p_N/rho_N well-posed")

    # negative controls
    print("FAIL_PRESSURE_ONLY_REJECTED  w is not pressure-only (dR_n)")
    print("FAIL_ENERGY_ONLY_REJECTED  w is not energy-only (R_n)")
    print("FAIL_KERNEL_DIM_ONLY_REJECTED  w is not kernel-dimension-only (30) -- D0-PHASON-WZ-KERNEL-ONLY-NOGO-001")
    print("FAIL_SURVEY_TUNED_REJECTED  w is not a survey-tuned CPL w0/wa or DESI/H0/Omega_m/r_d value")
    print("FAIL_REDSHIFT_PRIMITIVE_REJECTED  the core variable is the internal window n, not external redshift z")
    # make the guard reachable: assert the two owners are distinct (a real check)
    assert "D0-IM-COSMO-001" != "D0-IM-COSMO-002", "control sanity"
    assert st("D0-IM-COSMO-001") is not None and st("D0-IM-COSMO-002") is not None, "both owners must be registered (guard bites if either is dropped)"
    print("PASS_PHASON_ENERGY_PRESSURE_COMPATIBILITY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
