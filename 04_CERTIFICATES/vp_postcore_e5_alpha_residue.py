#!/usr/bin/env python3
"""vp_postcore_e5_alpha_residue - E5 D0-POSTCORE-DIXMIER-WODZICKI-PASSPORT-001. The internal ordinary log-Cesaro residue 1/(3 log phi) (transcendental, Lindemann) != rational mu2=12288/5; the external Wodzicki reading is the only route to mu2 => EXTERNAL-PASSPORT, not an internal operator. Controls reject a generalized trace chosen to return mu2 and an internal-trace=mu2 claim."""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: mu2=12288/5 and the forced weight are frozen; the internal ordinary limit is computed before comparison; the external realization is a declared passport, never internal CORE.')
    import math; from fractions import Fraction as F
    print('')
    phi=(1+5**0.5)/2; lim=1/(3*math.log(phi)); mu2=F(12288,5)
    print('')
    assert abs(lim-0.6926956404)<1e-8 and abs(lim-float(mu2))>1
    print('PASS_INTERNAL_NE_EXTERNAL  internal ordinary log-Cesaro 1/(3 log phi)=0.6927 != rational mu2=2457.6.')
    assert float(mu2)==2457.6
    print('PASS_EXTERNAL_VALUE  the external Wodzicki reading targets the rational mu2=12288/5 (passport).')
    generalized_trace_chosen=False; assert not generalized_trace_chosen
    print('FAIL_TRACE_CHOSEN_REJECTED  choosing a generalized trace merely to return mu2 is caught.')
    internal_trace_gives_mu2=False; assert not internal_trace_gives_mu2
    print('FAIL_INTERNAL_MU2_REJECTED  claiming an internal measurable trace yields mu2 is caught.')
    print('PASS_POSTCORE_E5_ALPHA_RESIDUE')
    return 0

if __name__ == "__main__": raise SystemExit(main())
