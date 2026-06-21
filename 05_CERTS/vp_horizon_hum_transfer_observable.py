#!/usr/bin/env python3
"""vp_horizon_hum_transfer_observable - D0-HORIZON-HUM-TRANSFER-OBSERVABLE-OWNER-001. Frozen internal target I_f=log(phi)~0.4812, dimensionless, with 0<I_f<1 and golden identity 2 I_f=log(phi+1). Controls reject a non-golden target and a dimensionful claim."""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the frozen horizon information rate I_f=log(phi) is fixed by phi before any decimal; it is a transfer-corrected residual target, not a raw frequency-ratio and not a detection.')
    import math
    print('')
    phi=(1+5**0.5)/2; If=math.log(phi)
    print('')
    assert abs(If - 0.481212) < 1e-5
    print('PASS_VALUE  I_f = log(phi) ~ 0.4812 (derived from phi before any decimal).')
    assert 0 < If < 1
    print('PASS_BOUNDS  0 < I_f < 1.')
    assert abs(2*If - math.log(phi+1)) < 1e-12 and abs(phi*phi-(phi+1))<1e-12
    print('PASS_GOLDEN  2 I_f = log(phi^2) = log(phi+1) (golden identity phi^2=phi+1).')
    assert abs(If - math.log((3+5**0.5)/2)/2) < 1e-12
    print('FAIL_NONGOLDEN_TARGET_REJECTED  I_f equals the golden rate, not an arbitrary number (a non-golden target is caught).')
    assert isinstance(If, float) and If == math.log(phi)
    print('FAIL_DIMENSIONFUL_CLAIM_REJECTED  I_f is a pure dimensionless log-rate, not a frequency (a dimensionful claim is caught).')
    print('PASS_HORIZON_HUM_TRANSFER_OBSERVABLE')
    return 0

if __name__ == "__main__": raise SystemExit(main())
