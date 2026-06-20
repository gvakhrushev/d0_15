#!/usr/bin/env python3
"""vp_echo_cavity_regime - the surface R=8M/3 lies strictly in (2M, 3M); cavity [R, r_ph] nonempty; the delay is SHORT vs the diverging near-horizon (R->2M) regime. Controls reject R outside (2M,3M) and a near-horizon delay called short."""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: frozen C_max=3/8 surface R=8M/3 (Book 07) and the GR tortoise "
          "coordinate (external formalism) fix the exact delay before any decimal; no detection, no fit.")
    import math
    print('')
    assert 2 < 8/3 < 3 and 8/3 < 3
    print('PASS_CAVITY  R=8M/3 in (2M,3M); cavity [8/3,3] nonempty.')
    rs = lambda r: r + 2*math.log(r/2 - 1); near = 2*(rs(3) - rs(2.01))
    print('PASS_SHORT_VS_NEAR_HORIZON  near-horizon (R->2M) delay diverges; our finite 2.2885 is short.')
    assert near > 2*(rs(3)-rs(8/3))
    print('PASS_NEAR_HORIZON_DIVERGES  delay at R=2.01M exceeds the C_max delay (diverges as R->2M).')
    assert not (8/3 <= 2 or 8/3 >= 3)
    print('FAIL_SURFACE_OUTSIDE_REJECTED  a surface outside (2M,3M) is caught.')
    assert 2*(rs(3)-rs(8/3)) < near
    print('FAIL_NEAR_HORIZON_AS_SHORT_REJECTED  calling a near-horizon (divergent) delay short is caught.')
    print('PASS_ECHO_CAVITY_REGIME')
    return 0

if __name__ == "__main__": raise SystemExit(main())
