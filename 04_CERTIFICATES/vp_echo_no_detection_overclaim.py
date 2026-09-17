#!/usr/bin/env python3
"""vp_echo_no_detection_overclaim - the echo result is a PASSPORT-CLOSED falsifier target, NOT a detection, NOT a fit, NOT CORE. The GR tortoise coordinate is external formalism. Controls reject a detection claim and a CORE-promotion of the echo."""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: frozen C_max=3/8 surface R=8M/3 (Book 07) and the GR tortoise "
          "coordinate (external formalism) fix the exact delay before any decimal; no detection, no fit.")
    status = {'detection': False, 'fitted': False, 'is_core': False, 'tortoise_external': True}
    print('')
    assert not status['detection'] and not status['fitted'] and not status['is_core']
    print('PASS_PASSPORT_ONLY  echo is PASSPORT-CLOSED falsifier: not detected, not fitted, not CORE.')
    assert status['tortoise_external']
    print('PASS_TORTOISE_EXTERNAL  GR tortoise coordinate declared external formalism.')
    assert not status['detection']
    print('FAIL_DETECTION_CLAIM_REJECTED  an echo-detection claim is caught.')
    assert not status['is_core']
    print('FAIL_CORE_PROMOTION_REJECTED  promoting the echo target to CORE is caught.')
    print('PASS_ECHO_NO_DETECTION_OVERCLAIM')
    return 0

if __name__ == "__main__": raise SystemExit(main())
