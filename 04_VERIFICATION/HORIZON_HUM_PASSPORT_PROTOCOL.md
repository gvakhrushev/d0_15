# D0 Horizon-Hum Falsifier Passport — Protocol

**Pre-registered transfer-corrected residual test. Not a raw frequency hunt. Not a detection. Not CORE.**

## Frozen internal target
- Horizon information rate `I_f = log φ ≈ 0.4812` (golden return/Lyapunov rate; `2 I_f = log(φ+1)`).
- Lean owner `D0-HORIZON-HUM-TRANSFER-OBSERVABLE-OWNER-001` (`D0.Gravity.HorizonHumTransfer`).

## Protocol (no event chooses the target)
- Build an instrument-response-corrected, **external-waveform-subtracted** residual; compare its log-spacing
  statistic to `I_f` in a time-frequency window **frozen before data**.
- Propagate population/systematic uncertainties; apply look-elsewhere/trials correction.

## Controls (see HORIZON_HUM_NEGATIVE_CONTROL_MATRIX.csv)
- detector-frame `φ`-artifact null, external waveform subtraction, instrument response, population systematics,
  injection-recovery, null (time-slid) distribution.

## PASS / FAIL
- FAIL (disfavored): no `I_f` residual excess after transfer correction + controls.
- PASS (not excluded): a calibrated, trials-corrected residual consistent with `log φ` survives every control.
- Neither promotes any quantity to CORE; no LIGO-confirmation language.
