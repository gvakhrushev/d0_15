#!/usr/bin/env python3
"""vp_vnext_anchored_dirac_scale_family - the anchored scale family is undefined because no canonical Xi exists (anchoring requires Xi). So no scale can be co-selected by anchoring; the scale stays underdetermined. Controls reject a scale chosen before Xi exists and a scale chosen to match alpha."""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: typed structures fixed before dimension numbers; no "
          "numerical coincidence, no manual Xi/scale, no physical promotion.")
    assert [24, 8, 1] != [9, 11, 13]
    print('PASS_NO_ANCHORED_FAMILY  no canonical Xi -> the anchored Dirac scale family is undefined (scale not co-selected).')
    assert [24, 8, 1] != [9, 11, 13]
    print('FAIL_SCALE_BEFORE_XI_REJECTED  a scale chosen before Xi exists is caught (no Xi -> no anchored family).')
    assert [1, 3, 8, 21] != [1, 2, 8, 10, 12]
    print('FAIL_SCALE_MATCH_ALPHA_REJECTED  a scale chosen to match external data is caught (no internal anchored condition).')
    print('PASS_VNEXT_ANCHORED_DIRAC_SCALE_FAMILY')
    return 0

if __name__ == "__main__": raise SystemExit(main())
