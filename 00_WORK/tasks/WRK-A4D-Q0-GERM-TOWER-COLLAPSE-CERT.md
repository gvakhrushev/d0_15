# WRK-A4D-Q0-GERM-TOWER-COLLAPSE-CERT
Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-q0-germ-tower-collapse-cert`
Primary artifact: `02_REGISTRY/research/certificates/a4d_q0_germ_tower_collapse_check.py`
Execution: `GitHub-first`

Class: `WORKER`
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`
State on registration: `PLANNED`
Affected claims: `D0-A4D-SECOND-ORDER-ENERGY-COVARIANCE-001`

## Why delegated

Main separately owns the exact coefficient decomposition of the mixed block,
the moving metric-null line, the physical same-carrier/cross-character split,
and the fixed-link second harmonic. What is still missing is one cheap,
auditable owner for the algebraic collapse of the full harmonic expression.
Without it, new executors can waste time re-running the closed germ front or
confuse a frozen-source residual with the moving section.

## Dependency gate

Consume current main only. In particular use the merged exact coefficient
owner for `C(d)=sum_r d_r K_r`, merged #290 for the physical
same-carrier/cross-character distinction, and merged #296 only as the
fixed-link harmonic reference.

Do **not** consume open #260 as an input theorem. This worker is independent
of the N0 nonlinear connection-amplitude germ.

## Objective

With `q0(x)=vec_sym(xx^T)` and
`M_k=sum_r x_r^k K_r q0(x)`:

1. prove coefficientwise in exact arithmetic that
   `M_1=sum_r x_r K_r q0(x)=0`;
2. for `d_n,r=(1+x_r)^n-1`, certify the exact binomial identity
   `F_n=sum_r d_n,r K_r q0(x)=sum_{k>=2} binom(n,k) M_k`;
3. certify that the first nonzero homogeneous piece for every `n>=2` is
   `binom(n,2) M_2`, with `deg M_2=4` and next possible degree 5;
4. certify
   `sum_{n>=2} binom(n,2) s^(n-1)=s/(1-s)^3`;
5. on the exact orbit-5/7 physical carriers, evaluate the left-cokernel
   pairing/image test for the homogeneous pieces needed to compare with the
   supplied synthesis. If a general all-`k` theorem follows from the exact
   carrier algebra, prove it; otherwise report the maximal exact range and
   leave the stronger statement explicitly open;
6. add hostile controls showing that substituting the frozen/cross-character
   source reproduces its nonzero residual and is not the same object as the
   moving-germ tower.

## Required checks

- Use exact rational / Gaussian-rational / symbolic arithmetic only.
- Reconstruct coefficient data from repository owners; do not paste a
  floating matrix from chat.
- No SVD, tolerance rank, finite-difference derivative, or numerical fit.
- The certificate must be deterministic and fast enough for ordinary guards.
- Run `python3 tools/validate_repo.py`, `python3 tools/validate_work.py`,
  `python3 tools/lint_claim_strength.py`, and the certificate itself before
  REVIEW.

## Scope guard

This task does not prove stationary-sheet stress, a nonlinear Einstein
equation, a general continuum theorem, or the odd N0 resonance. It must not
modify #260/#275/#202, BOOK text, ClaimMap, or release statuses.

The historical `8/5` residual remains a frozen/cross-character diagnostic;
do not relabel it as a germ stress.

## Exit condition

A deterministic exact certificate and short research note establish the
harmonic-tower algebra stated above, with the physical-cokernel scope stated
at exactly the strength actually proved. The task is retired in the same PR
before Ready.

## GitHub execution contract

Start from fresh current `main`; run
`python3 tools/task_lifecycle.py start WRK-A4D-Q0-GERM-TOWER-COLLAPSE-CERT`
as the first branch change; open a Draft PR before substantive work; retire
the task in the same PR before setting `Lifecycle: REVIEW`. Never
self-merge.

## Chat handoff

Return the PR, exact terminal, certificate command, homogeneous identities,
orbit-5/7 physical verdict, and any remaining all-`k` gap. Do not paste a
large symbolic dump into chat.
