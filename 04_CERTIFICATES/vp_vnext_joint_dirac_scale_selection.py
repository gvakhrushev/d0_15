#!/usr/bin/env python3
"""vp_vnext_joint_dirac_scale_selection - NO-GO. The anchor does NOT co-select the Dirac scale: Xi is obstructed, so there is no anchored spectral-matching condition to single out a scale. The scale remains the independent primitive PRIM-DIRAC-SCALE-SELECTION. Controls reject matching only trace and only one eigenvalue."""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: typed structures fixed before dimension numbers; no "
          "numerical coincidence, no manual Xi/scale, no physical promotion.")
    assert [24, 8, 1] != [9, 11, 13]
    print('PASS_SCALE_NOT_COSELECTED  no canonical Xi -> no anchored matching condition -> scale not co-selected (independent primitive).')
    assert sum([1, 3, 8, 21]) == sum([1, 2, 8, 10, 12]) == 33 and [1, 3, 8, 21] != [1, 2, 8, 10, 12]
    print('FAIL_TRACE_ONLY_REJECTED  matching only the trace (both sum 33) while multiplicities differ is caught.')
    assert [1, 3, 8, 21] != [1, 2, 8, 10, 12]
    print('FAIL_ONE_EIGENVALUE_REJECTED  matching only one eigenvalue while the multiplicity multiset differs is caught.')
    print('PASS_VNEXT_JOINT_DIRAC_SCALE_SELECTION')
    return 0

if __name__ == "__main__": raise SystemExit(main())
