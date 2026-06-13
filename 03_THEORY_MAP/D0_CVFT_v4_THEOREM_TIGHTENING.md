# D0 CVFT v4 Theorem Tightening

## Accepted A2 Theorem Targets

Boundary-local rank, refined log-det/rank control, UV feedback-tail control,
`U_eff` pole discipline and effective S_DE exceptional-point algebra are
accepted as theorem targets.

## Required Corrections to A2 Formulas

All log-det and tail bounds use `a=|z|rho(F)<1`, not `z` alone.  The determinant
formula is logarithmic and uses the analytic branch connected to `z=0`.
`delta0^12` is a readout threshold, not a convergence radius.

## Accepted B2 Sector Operator Designs

F1 coefficient-origin, F2 greybody leakage, F3 hadron poles, F5 neutrino
decoherence and F6 gauge-boundary leakage are retained as operator designs or
proof obligations. None is promoted to physical closure.

## Frontier Status Classification

The canonical registry is `D0_CVFT_FRONTIER_OPERATOR_TARGETS.csv`.

## Book Proof-Cell Wording

Books 02/04/07/08 use `F_N` only as feedback-return, `R_N` only as positive
readout, `U_eff` for complex poles and `P_fb` for pressure.

## Book 05 Admissibility Inserts

Forbidden shortcuts include `z/(1-z)` log-det without `|z|rho(F)`, `delta0^12`
as radius, rank bound as `A/4`, complex poles from bare positive `F`, DESI pass
from S_DE EP algebra and PDG baryon sorting before frozen poles.

## Cert/Lean Readiness Matrix

| target | cert | Lean |
|---|---|---|
| log-det rank | `vp_cvft_refined_logdet_rank_bound.py` | queued |
| UV tail | `vp_cvft_uv_feedback_tail_bound_refined.py` | queued |
| boundary channel rank | `vp_cvft_boundary_channel_rank.py` | queued |
| U_eff pole | `vp_cvft_ueff_pole_discipline.py` | queued |
| S_DE EP | `vp_sde_exceptional_point_algebra.py` | queued |
| baryon S3 scaffold | `vp_cvft_baryon_s3_scaffold.py` | queued |

## Remaining Obligations

Exact F1 sector construction, F2 observable transfer, F3 spin/flavour transfer,
F5 external manifest, F6 lower bound and F7 Lean proof remain open.
