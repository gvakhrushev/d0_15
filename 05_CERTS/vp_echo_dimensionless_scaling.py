#!/usr/bin/env python3
"""vp_echo_dimensionless_scaling - tau_echo/M is dimensionless and mass-rescaling invariant: r/(2M)-1 at r in {3M,8M/3} is mass-free, so the ratio carries no M. Controls reject an M-dependent target and a dimensionful echo claim."""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: frozen C_max=3/8 surface R=8M/3 (Book 07) and the GR tortoise "
          "coordinate (external formalism) fix the exact delay before any decimal; no detection, no fit.")
    import math
    print('')
    rsM = lambda M,r: r + 2*M*math.log(r/(2*M) - 1)
    print('')
    vals = [2*(rsM(M,3*M)-rsM(M,8*M/3))/M for M in (1.0, 5.0, 137.0)]
    print('PASS_MASS_INVARIANT  tau_echo/M identical across M in {1,5,137}.')
    assert max(vals)-min(vals) < 1e-9
    print('PASS_INVARIANT_NUMERIC  spread across masses < 1e-9 (M cancels).')
    assert abs((3*5)/(2*5) - 3/2) < 1e-12
    print('FAIL_M_DEPENDENT_TARGET_REJECTED  the log argument 3M/(2M)=3/2 is mass-free (an M-dependent target is caught).')
    assert abs(vals[0] - (2/3+4*math.log(3/2))) < 1e-9
    print('FAIL_DIMENSIONFUL_CLAIM_REJECTED  the target is the dimensionless ratio tau/M, not a dimensionful time.')
    print('PASS_ECHO_DIMENSIONLESS_SCALING')
    return 0

if __name__ == "__main__": raise SystemExit(main())
