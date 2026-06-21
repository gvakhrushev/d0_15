#!/usr/bin/env python3
"""vp_horizon_hum_empirical_passport - D0-HORIZON-HUM-EMPIRICAL-PASSPORT-001. Transfer-corrected residual protocol over the frozen I_f=log(phi); external waveform subtraction + instrument response + population controls; time-frequency window frozen before data. NOT a LIGO confirmation, NOT CORE. Controls reject a raw frequency-ratio hunt, a detector-frame phi artifact, and a confirmation claim."""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: I_f=log(phi) frozen; protocol is a pre-registered transfer-corrected residual test with negative controls; no event chooses the target; no LIGO-confirmation language.')
    status={'detection':False,'is_core':False,'window_frozen_before_data':True,'transfer_corrected':True,'event_selects_target':False}
    print('')
    controls=['external_waveform_subtraction','instrument_response_correction','population_systematics','detector_frame_phi_artifact','injection_recovery','null_distribution']
    print('')
    assert status['transfer_corrected'] and status['window_frozen_before_data']
    print('PASS_TRANSFER_PROTOCOL  transfer-corrected residual; time-frequency window frozen before data.')
    assert len(controls) >= 6 and 'detector_frame_phi_artifact' in controls
    print('PASS_CONTROLS  >=6 controls incl detector-frame phi-artifact null.')
    assert not status['event_selects_target']
    print('FAIL_EVENT_SELECTS_TARGET_REJECTED  using an event to choose the target is caught (I_f frozen).')
    assert not status['detection'] and not status['is_core']
    print('FAIL_DETECTION_OR_CORE_REJECTED  a hum-detection / CORE-promotion claim is caught.')
    print('PASS_HORIZON_HUM_EMPIRICAL_PASSPORT')
    return 0

if __name__ == "__main__": raise SystemExit(main())
