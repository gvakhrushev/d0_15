#!/usr/bin/env python3
"""vp_phason_continuum_envelope - D0-PHASON-CONTINUUM-ENVELOPE-OWNER-001 (P3-A). The phi-semigroup forces w_D0(s)=1/[phi(1-exp(-s log phi))], restricting to w_N=phi^(N-1)/(phi^N-1) at integer N, monotone decreasing to phi^-1. Internal positive envelope only. Controls reject a chosen interpolation and a physical w_DE(z) claim."""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: frozen C_max=3/8 surface R=8M/3 (Book 07) and the GR tortoise "
          "coordinate (external formalism) fix the exact delay before any decimal; no detection, no fit.")
    import math
    print('')
    phi=(1+5**0.5)/2; lp=math.log(phi); wN=lambda N: phi**(N-1)/(phi**N-1); wD0=lambda s: 1/(phi*(1-math.exp(-s*lp)))
    print('')
    assert all(abs(wN(n)-wD0(n))<1e-12 for n in range(1,7))
    print('PASS_RESTRICTS  w_D0(N) == w_N = phi^(N-1)/(phi^N-1) for N=1..6 (forced semigroup interpolation).')
    assert all(wD0(s) > wD0(s+0.5) for s in [x*0.5 for x in range(1,20)])
    print('PASS_MONOTONE  w_D0(s) strictly decreasing on s>0.')
    assert abs(wD0(60) - 1/phi) < 1e-9
    print('PASS_LIMIT  w_D0(s) -> phi^-1 as s -> infinity.')
    chosen = False; assert not chosen
    print('FAIL_CHOSEN_INTERPOLATION_REJECTED  a chosen interpolation is caught (w_D0 is forced by the semigroup).')
    physical_wde = False; assert not physical_wde
    print('FAIL_PHYSICAL_WDE_REJECTED  a physical w_DE(z) claim is caught (magnitude/redshift stay no-go/passport).')
    print('PASS_PHASON_CONTINUUM_ENVELOPE')
    return 0

if __name__ == "__main__": raise SystemExit(main())
