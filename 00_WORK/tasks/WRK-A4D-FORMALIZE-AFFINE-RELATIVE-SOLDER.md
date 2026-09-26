# WRK-A4D-FORMALIZE-AFFINE-RELATIVE-SOLDER

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-formalize-affine-relative-solder`
Primary artifact: `03_FORMALIZATION/D0/Geometry/A4DAffineRelativeSolderCompletion.lean`
Execution: `GitHub-first`

## Dependency gate

SATISFIED: research #184 is merged. This worker may start now.

## Why delegated

The selected relative-solder algebra is stable and bounded. Formalization prevents later agents from reopening the lambda selector or confusing this kinematic completion with the final physical quotient.

## Owned theorem packet

Formalize only merged #184 content:

- observer metric congruence under proper Lorentz transport;
- affine solder/link shift law;
- `ThetaHat^lambda = Theta - lambda b^T h_n`;
- exact transform with residual term proportional to `1-lambda`;
- uniqueness of `lambda=1` from a nonzero translation witness;
- homogeneous covariance at `lambda=1`;
- matched-edge diagonal invisibility of every functional factoring only through `ThetaHat`.

The finite L=2 statement that this erases 192 nongauge edge directions is research-certified; do not turn a Python rank into an axiom. Formalize it only if the concrete finite carrier/rank proof is genuinely closed in Lean.

## Non-claims

Do not call relative solder the final full-affine physical action. #185/#196 show extra joint-holonomy data are needed to recover nongauge edge information.

## GitHub execution contract

Run `python tools/task_dispatch.py WRK-A4D-FORMALIZE-AFFINE-RELATIVE-SOLDER`; open Draft PR; keep the module isolated; no `sorry`; update `D0.All` only when stable; self-retire before Ready; never self-merge.

## Chat handoff

Return PR, SHA, theorem names, build/guard results, and any exact rank statement deliberately left research-only.
