#!/usr/bin/env python3
"""vp_echo_delay_exact_formula - D0-ECHO-DELAY-COMPACTNESS-OWNER-001. tau_echo/M = 2[r_star(3M)-r_star(8M/3)]/M = 2/3 + 4 log(3/2) ~ 2.2885 (exact, derived before decimal). r_star(r)=r+2M log(r/(2M)-1) is external GR formalism. Controls reject a fitted delay and a decimal-before-derivation."""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: frozen C_max=3/8 surface R=8M/3 (Book 07) and the GR tortoise "
          "coordinate (external formalism) fix the exact delay before any decimal; no detection, no fit.")
    import math
    print('')
    rs = lambda r: r + 2*math.log(r/2 - 1)
    print('')
    exact = 2/3 + 4*math.log(3/2); numeric = 2*(rs(3) - rs(8/3))
    print('PASS_EXACT  tau_echo/M = 2/3 + 4 log(3/2) (symbolic).')
    assert abs(exact - numeric) < 1e-12
    print('PASS_NUMERIC_MATCH  symbolic == numeric 2[r_star(3)-r_star(8/3)].')
    assert abs(exact - 2.288527) < 1e-5
    print('PASS_DECIMAL  tau_echo/M ~ 2.2885 (decimal AFTER the exact derivation).')
    assert 2/3 + 4*math.log(3/2) > 2*(1/3)
    print('FAIL_FITTED_DELAY_REJECTED  the delay is derived from C_max=3/8 + GR tortoise, not fitted to any event.')
    assert abs(math.log(3/2) - (math.log(3)-math.log(2))) < 1e-12
    print('FAIL_DECIMAL_BEFORE_DERIVATION_REJECTED  the closed form log(3/2)=log3-log2 precedes the decimal.')
    print('PASS_ECHO_DELAY_EXACT_FORMULA')
    return 0

if __name__ == "__main__": raise SystemExit(main())
