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

This is the lower-wall OTO/F4 problem. PR #201 already fixed the flat Einstein seed, so the remaining load-bearing question is nonlinear: does the selected finite action possess a nondegenerate curved stationary configuration? Existing PR #202 evidence narrowed a candidate to a parabolic E(2) sheet, but its old full-stationarity reading used an inconsistent Cayley differential. The local continuation corrects that audit and then tests only controlled deformations that can change both the missing Euler equations and residual blindness. This is strong-research work, not routine formalization.

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
- the enlarged E(2) matrix family is `e2=(0,0,j,0,0,j,g,d,0,d,-g,0)`; its action/curvature evaluations remain exact, but the historical full-stationarity interpretation used a mismatched Cayley generator for the stored role matrices;
- the corrected exact full-link audit uses the matrix-defined subgroup `span{M2,M3,-J23}` and complement `{K1,N2,N3}`; its full-star Euler zero-set on this sheet is only the flat origin, so no curved full-stationary member survives;
- matched/arbitrary affine `b` remains structurally residual-blind on this parabolic sheet (`R=0`), so stop trying to activate `R_*(C)` here; only controlled deformations that can change both missing Euler equations and residual rank are live;
- independently, the rank-two seam has a canonical fixed-rank affine quotient coordinate `Psi_2(M,t)=t∧(Λ²M)`, with `Psi_r(M,t)=Psi_r(M,t')` iff `t-t'∈im M`; this is diagnostic/resolution data, not a new action channel.

Numerical evidence is not a theorem.

## Objective

The first local correction now gives a scoped exact no-go on the matrix-defined homogeneous parabolic sheet: its full-star Euler zero-set is only the flat origin, and matched-b four-channel residuals are blind there. Continue by testing the smallest controlled deformations that can repair the true missing Euler equations and activate the existing residual simultaneously. Reject any deformation that fails either rank gate before solving.

Separately preserve the cross-wall result: no nontrivial zero-source stationary germ on this sheet accumulates at its flat locus. This is input to #216, not a theorem about other charts or the full physical quotient.

L=2 may discover the witness. A broad finite-carrier terminal requires an L=3 hostile control.

## Required method

Use exact rational directional derivatives and symmetry reduction. The current homogeneous parabolic sheet is killed and its `R` channel is identically dormant; do not try to activate it. For each controlled deformation, first compute the missing-Euler Jacobian and the same directions' first variation of `det(I-P)`, `adj(I-P)`, or `R`. Reject it unless both obstruction gates can change. Only then run a small exact/rational reconstruction. Do not restart blind Gröbner/resultant chains. Checkpoint each exact subsystem and rank before moving on.

## Current durable checkpoint (2026-09-26)

The exact first-order gate is owned by
`a4d_resolved_curved_stationary_e2_controlled_normal_gate_check.py`.
The null-line dilation `K1` fails: its four-role Euler Jacobian has rank 4
and augmented rank 5, while all tested adjugate first variations vanish.
Among the twelve role-local `{K1,N2,N3}` directions, only `N2` on role 2
and `N3` on role 3 activate `adj(I-P)` on the four curved faces. The full
eight-equation missing-Euler Jacobian has rank 8, augmented rank 8; a
residual-active linearized correction needs at least seven directions.
This is not a finite stationary witness. Exact nonlinear reconstruction of
the full Euler system with active residual remains open; L=3 has not started
because no exact L=2 witness has been reconstructed.

## Checkpoint (2026-09-27)

The fixed-`eta` seven-amplitude necessary subsystem has no open-chart
solution except the obstructed origin
(`a4d_resolved_curved_stationary_e2_support7_main_branch_check.py`).

At the same frozen homogeneous link, with one absolute solder copied at
every site,
`a4d_resolved_curved_stationary_e2_support7_joint_linear_gate_check.py`
shows two further exact facts. The joint linearization in the seven
amplitudes plus 16 solder entries is consistent of rank 19, and every
solution has zero amplitudes, hence zero first adjugate variation. On the
full solder-critical kernel, `(E_{role2,N3}+E_{role3,N2})/64=(z0-z2)(z1-z2)`
divides `det theta`, so every link-stationary critical solder is degenerate.
All six faces have `det(I-P)=adj(I-P)=0` while four curvature bivectors are
nonzero, so the owned channels vanish for every translation and do not
repair this link. This is not a finite no-go for deformations of the seven
amplitudes away from the link, and it is not an active-residual witness.
L=3 remains unopened.

## Forbidden shortcuts

No Holst channel, no phi coefficient, no new unowned invariant, no forcing `R=0`, no 7x7 coefficient grid, no continuum Einstein claim, no treating machine-precision roots as exact.

## GitHub execution contract

Start from current `main`; run `python tools/task_dispatch.py EXP-A4D-RESOLVED-CURVED-STATIONARY-CLOSURE`; use the existing open execution if present; checkpoint durable results in the primary memo/certificates; keep exact/structural/numerical/open statuses separate; refresh against main before Ready; self-retire only when terminal; never self-merge.

## Chat handoff

Return the PR number, final SHA, exact witness/no-go, curvature/nondegeneracy data, validation commands, L=3 status, and the single smallest remaining blocker.
