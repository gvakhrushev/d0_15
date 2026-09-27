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

The supplied synthesis and merged #296 use the same informal symbol for two
different harmonic objects. This worker must remove that ambiguity once and
make future executors consume a typed distinction rather than re-running the
germ calculation.

## Dependency gate

Consume current main only: the exact `K_r` coefficient owner, merged #290
for the physical same-carrier/cross-character split, and merged #296 for the
analytic Gram-lift coefficient. Do not consume open #260 as an input theorem.

## Objective

Define two distinct objects.

Bare harmonic operator:
```text
B_n(x) := C(d(z^n)) q0(x)
```

Full #296 Gram-lift coefficient:
```text
G_n(x) :=
  2 * binom(1/2,n) * sigma(x)^(n-1) * B_n(x),
sigma(x) := x^T eta x.
```

With `M_k=sum_r x_r^k K_r q0(x)`, certify in exact arithmetic:

1. `M_1=sum_r x_r K_r q0(x)=0`;
2. `B_n=sum_{k>=2} binom(n,k) M_k`;
3. for every fixed `n>=2`,
   `B_n=binom(n,2)M_2+O(||x||^5)`, with `deg M_2=4`;
4. `sum_{n>=2} binom(n,2)s^(n-1)=s/(1-s)^3`;
5. after restoring the #296 prefactor,
   `G_n=O(h^(2n+2))` for generic `x=O(h)`, reconciling the h^4 bare
   operator with the existing #296 fixed-harmonic scaling;
6. on exact orbit-5/7 physical carriers, determine the maximal exact
   left-cokernel/image statement justified for the required `M_k`; do not
   extrapolate a sampled low-k check into an all-k theorem;
7. hostile controls must reproduce the frozen/cross-character nonzero
   residual while keeping same-carrier moving transport distinct.

## Required checks

Use exact rational / Gaussian-rational / symbolic arithmetic only. Reconstruct
coefficient data from repository owners. No SVD, tolerance ranks,
finite-difference derivatives, or numerical fitting. The certificate must be
fast enough for ordinary guards.

Run the certificate plus:

```text
python3 tools/validate_repo.py
python3 tools/validate_work.py
python3 tools/lint_claim_strength.py
```

before REVIEW.

## Scope guard

This task does not prove stationary-sheet stress, nonlinear Einstein,
continuum convergence, or any N0 odd correction. It must not edit
#260/#275/#202, BOOK, ClaimMap, or release statuses.

The historical `8/5` residual remains a frozen/cross-character diagnostic.

## Exit condition

A deterministic certificate and short note establish the typed
`B_n`/full-`G_n` distinction, the exact harmonic algebra, the #296 scaling
reconciliation, and only the physical-cokernel strength actually proved. The
task retires in the same PR before Ready.

## GitHub execution contract

Start from fresh current `main`; run
`python3 tools/task_lifecycle.py start WRK-A4D-Q0-GERM-TOWER-COLLAPSE-CERT`
as the first branch change; open a Draft PR before substantive work; retire
the task in the same PR before setting `Lifecycle: REVIEW`. Never
self-merge.

## Chat handoff

Return the PR, terminal, certificate command, exact `B_n` and `G_n`
identities, orbit-5/7 verdict, and any remaining all-k gap.
