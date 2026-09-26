# EXP-A4D-RESOLVED-CURVED-STATIONARY-CLOSURE

Class: `EXPENSIVE`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `exp/a4d-resolved-curved-stationary-closure`
Primary artifact: `02_REGISTRY/research/MEMO_A4D_RESOLVED_CURVED_STATIONARY_CLOSURE.md`
Execution: `GitHub-first`

## Why delegated

This is the lower-wall OTO/F4 problem. PR #201 already fixed the flat Einstein seed, so the remaining load-bearing question is nonlinear: does the selected finite action possess a nondegenerate curved stationary configuration? Current execution PR #202 has reduced the numerical search to a parabolic E(2) little-group carrier and a 14-equation transverse exactification problem. This is strong-research work, not routine formalization.

## Runtime / collision gate

Before starting, search GitHub for an open PR carrying this exact task id. PR #202 is the current execution as of the registration refresh. If it is still open, CONTINUE #202; do not fork a second execution. Do not edit #201 terminal artifacts, the J2 bridge memo, or the Palatini target-span memo.

## Current repository-owned inputs

Merged inputs include #184, #185, #188, #189, #193, #196, #199, #200 and #201.

Use these exact boundaries:

- #201 terminal: naked `S_star` has pure finite Einstein flat Hessian, `K_star,metric=(1/4)K_E_eta`, and `j^2_flat Q(R)=0`.
- #201 corrected H1: DO NOT infer `EL_b => R=0`. Solve/integrate the residual channel as `R=R_*(C,...)` after its own Euler equation.
- #196: joint residuals are quotient-complete on declared generic curved L=2 controls, but this is not a global nonlinear theorem.
- #199/#200: solder Euler alone does not force flatness; canonical flat checkerboard physical nulls are nonlinearly obstructed.

Current #202 checkpoint to reproduce before extending:

- four legal residual channels `I_eta_adj, I_eta_opp, I_n_adj, I_n_opp`;
- exact response matrix rank 4 / kernel 0 on the declared sample;
- five exact homogeneous word controls have no nondegenerate full stationary point;
- numerical E(2) little-group candidates pass literal single-site/single-edge Euler tests at machine precision;
- the enlarged E(2) pattern has now exactified to the family `e2=(0,0,j,0,0,j,g,d,0,d,-g,0)`; witness `(j,g,d)=(2,0,1)` has exact declared star residual zero and `curv²=32`;
- the classical 8+6 check confirms the current star-family stationarity, but the cheap `b≡0` four-channel filter is dormant (`C≠0`, `R=0`), so active `R=R_*(C)≠0` remains open;
- independently, the rank-two seam has a canonical fixed-rank affine quotient coordinate `Psi_2(M,t)=t∧(Λ²M)`, with `Psi_r(M,t)=Psi_r(M,t')` iff `t-t'∈im M`; this is diagnostic/resolution data, not a new action channel.

Numerical evidence is not a theorem.

## Objective

Either:

1. promote the exact enlarged parabolic star-family to one all-site nondegenerate configuration with nonzero curvature and full Euler zero for the selected **active four-channel** action, including `R=R_*(C)≠0`; or
2. prove a precisely scoped exact no-go for that active residual/channel completion.

Separately record whether any nontrivial stationary member/continuation accumulates at the **flat physical quotient**. This flat-accumulation question is cross-wall input to #216 and is logically independent of existence of a finite-amplitude curved vacuum.

L=2 may discover the witness. A broad finite-carrier terminal requires an L=3 hostile control.

## Required method

Prefer exact rational/algebraic elimination, rational reconstruction, Jacobian rank certification and symmetry reduction. Numerical optimization is a scout only. For the current exact family, first solve/activate the matched residual section `R=R_*(C)≠0`; do not restart blind multivariable Gröbner/resultant chains. For the cross-wall diagnostic, test flat convergence in quotient-invariant holonomy/compound data rather than curvature alone. Checkpoint every exact subsystem/rank/factorization before moving on.

## Forbidden shortcuts

No Holst channel, no phi coefficient, no new unowned invariant, no forcing `R=0`, no 7x7 coefficient grid, no continuum Einstein claim, no treating machine-precision roots as exact.

## GitHub execution contract

Start from current `main`; run `python tools/task_dispatch.py EXP-A4D-RESOLVED-CURVED-STATIONARY-CLOSURE`; use the existing open execution if present; checkpoint durable results in the primary memo/certificates; keep exact/structural/numerical/open statuses separate; refresh against main before Ready; self-retire only when terminal; never self-merge.

## Chat handoff

Return the PR number, final SHA, exact witness/no-go, curvature/nondegeneracy data, validation commands, L=3 status, and the single smallest remaining blocker.
