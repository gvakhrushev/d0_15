# CVFT v5 Refined Bounds and Baryon Scaffold Changelog

## A3 Theorem Statements Accepted

Refined log-det/rank, UV feedback-tail, boundary-channel rank and `U_eff`
contraction/pole discipline were integrated as theorem-ready proof cells.

## A3 Code/Markdown Cleanup

Canonical notes use `a=|z|rho(F)`, close code/math blocks, and avoid treating
`delta0^12` as convergence radius.

## B3 Scaffold Accepted

The baryon scaffold records the 27D triple carrier, rational S3 symmetrizer,
10D symmetric carrier and allowed `U_eff^B`/Feshbach-Schur pole equations.

## F3 Physical Claims Still Open

Spin labels, flavour labels, mass/width transfer, PDG sorting, GeV conversion
and QCD/EFT running are not closed.

## New Cert Stubs

- `vp_cvft_refined_logdet_rank_bound.py`
- `vp_cvft_uv_feedback_tail_bound_refined.py`
- `vp_cvft_boundary_channel_rank.py`
- `vp_cvft_ueff_pole_discipline.py`
- `vp_sde_exceptional_point_algebra.py`
- `vp_cvft_baryon_s3_scaffold.py`

## New Forbidden Shortcuts

`z/(1-z)` without `|z|rho(F)`, A/4 from rank, complex poles from bare `F`,
random non-Hermitian resonance matrices and PDG sorting before frozen poles.

## Remaining Proof Obligations

Lean owners are queued; external-data claims remain passports; F1/F2/F5/F6 need
their finite operators or manifests.

## Next Recommended Frontier

F7 boundary rank and F4 UV tail are the safest next Lean targets.
