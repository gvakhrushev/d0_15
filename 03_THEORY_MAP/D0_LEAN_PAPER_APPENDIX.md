# D0 Lean Appendix — key machine-checked theorems

All build under `lake build D0.All` (Lean 4 + pinned Mathlib). Selected owners:

- `D0.Gravity.HorizonlessEchoDelay.horizonless_echo_delay_owner` — tau_echo/M = 2/3 + 4 log(3/2).
- `D0.Gravity.HorizonHumTransfer.horizon_hum_transfer_owner` — I_f = log phi, 0<I_f<1, 2 I_f = log(phi+1).
- `D0.Cosmology.PhasonContinuumEnvelope.phason_continuum_envelope_owner` — w_D0(s) restricts to w_N.
- `D0.Verification.TotalClosureBoundary.total_closure_boundary` — 10 lanes, each one terminal state.
- `D0.Verification.TotalExtensionPrimitiveMinimality.total_extension_primitive_independence` — 11 independent primitives.
- `D0.Verification.PresentCoreMaximality` — capstone conjunction of the present-core maximality no-gos.
