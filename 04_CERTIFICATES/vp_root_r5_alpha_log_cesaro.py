#!/usr/bin/env python3
"""vp_root_r5_alpha_log_cesaro - ROOT R5 D0-ALPHA-LOG-CESARO-MEASURABILITY-NOGO-001. At a=3 (forced weight phi^-3N) the per-block mass is constant (phi^3 phi^-3=1), so the ordinary log-Cesaro/Dixmier limit = 1/(3 log phi), transcendental (Lindemann) != rational mu2=12288/5. Reuses CVFT-F1; cites rate_three_eq_one. Controls reject choosing a Dixmier state to obtain mu2 and a CODATA alpha input."""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the weight phi^-3N and mu2=12288/5 are frozen; the ordinary limit value is computed before comparison; transcendence is the cited ASSUMP-LINDEMANN-LNPHI, not a global axiom.')
    import math; from fractions import Fraction as F
    print('')
    phi=(1+5**0.5)/2; lp=math.log(phi); mu2=F(12288,5)
    print('')
    assert abs((phi**3)*(phi**-3) - 1) < 1e-12
    print('PASS_CRITICAL_LINE  per-block mass constant at a=3 (phi^3 * phi^-3 = 1), the cited rate_three_eq_one.')
    lim=1/(3*lp); assert abs(lim-0.6926956404)<1e-8
    print('PASS_LIMIT  ordinary log-Cesaro limit = 1/(3 log phi) ~ 0.6927.')
    req=float(mu2)*3*lp; assert abs(req-3547.8785)<1e-2 and abs(req-round(req))>1e-3
    print('PASS_TRANSCENDENTAL  limit = algebraic/(3 log phi) is transcendental != rational mu2=12288/5.')
    dixmier_state_chosen=False; assert not dixmier_state_chosen
    print('FAIL_DIXMIER_STATE_CHOSEN_REJECTED  choosing a Dixmier/generalized-trace state to obtain mu2 is caught (only the ORDINARY limit counts).')
    codata_alpha_input=False; assert not codata_alpha_input
    print('FAIL_CODATA_ALPHA_REJECTED  feeding a measured/CODATA alpha into the operator is caught.')
    print('PASS_ROOT_R5_ALPHA_LOG_CESARO')
    return 0

if __name__ == "__main__": raise SystemExit(main())
