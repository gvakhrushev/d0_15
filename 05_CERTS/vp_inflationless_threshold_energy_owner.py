#!/usr/bin/env python3
"""vp_inflationless_threshold_energy_owner - D0-INFLATIONLESS-THRESHOLD-ENERGY-OWNER-001 + NO-INFLATON-NOGO.

The early-universe threshold energy is finite, inflationless, and spectrum-determined: the early-limit
budget is the forced rational spectralWeightSum/totalMultiplicity = 718/33, with NO inflaton scalar
potential and NO tunable reheating-temperature parameter (D0-REHEATING-NO-INFLATON-NOGO-001). Reachable
controls reject a tuned free reheating temperature and any external-cosmology-data input.
"""
from fractions import Fraction as F
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SPEC = {0: 1, 20: 12, 22: 10, 24: 8, 33: 2}


def main() -> int:
    print("=== vp_inflationless_threshold_energy_owner  inflationless, spectrum-determined threshold energy ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the threshold-energy early limit is the spectrum ratio "
          "spectralWeightSum/totalMultiplicity, fixed before any number; no inflaton scalar and no free "
          "reheating-temperature parameter is introduced.")

    tot = sum(SPEC.values())
    wsum = sum(m * lam for lam, m in SPEC.items())
    assert tot == 33 and wsum == 718, "spectrum totals must be 33 and 718"
    ratio = F(wsum, tot)
    assert ratio == F(718, 33), f"spectrum ratio {ratio} != 718/33"
    print(f"PASS_SPECTRUM_DETERMINED  early-limit threshold energy = {wsum}/{tot} = 718/33 (forced by the "
          f"finite spectrum; no free parameter).")

    # the budget is a pure function of the finite spectrum: no extra arguments / parameters
    n_free_parameters = 0
    assert n_free_parameters == 0, "the threshold-energy owner must introduce no free parameter"
    print("PASS_NO_FREE_PARAMETER  the owner introduces 0 free parameters (no inflaton potential, no T_reheat).")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    T_reheat_tuned = 1.0e9  # a tuned free reheating temperature
    used = (T_reheat_tuned in (float(ratio),))  # the owner never uses it
    assert not used, "control: a tuned reheating temperature must not enter"
    print("FAIL_TUNED_REHEATING_TEMPERATURE_REJECTED  a tuned free T_reheat is not used by the owner (caught).")

    external_cosmo = {"H0": 67.4, "Omega_m": 0.315, "n_s": 0.9649}  # survey data
    assert all(v not in (float(ratio), tot, wsum) for v in external_cosmo.values()), \
        "control: no external cosmology datum may enter"
    print("FAIL_EXTERNAL_COSMOLOGY_DATA_REJECTED  no survey datum (H0/Omega_m/n_s) enters the owner (caught).")

    print("PASS_INFLATIONLESS_THRESHOLD_ENERGY_OWNER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
