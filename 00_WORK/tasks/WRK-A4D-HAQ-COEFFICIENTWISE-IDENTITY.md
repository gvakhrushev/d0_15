# WRK-A4D-HAQ-COEFFICIENTWISE-IDENTITY

Class: WORKER

State on registration: PLANNED

Parent: CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE

Repository: gvakhrushev/d0_15

Base: main

Branch: wrk/a4d-haq-coefficientwise-identity

Primary artifact: 02_REGISTRY/research/certificates/a4d_haq_coefficientwise_identity_check.py

Execution: GitHub-first

## Why delegated

Merged PR #270 already constructs the accepted metric-response symbol
`C(d)=H_AQ(d)`, checks that it is linear in `d`, and verifies the null identity
by exact symbolic simplification. This worker makes the algebra visible as an
explicit coefficient ledger: it certifies each coefficient of the cubic
polynomial `C(d) vec_sym(d d^T)` separately. That is a bounded, independently
reviewable exact certificate; it does not repeat the rank/kernel census.

## Runtime and dependency gate

Before starting, use current main, confirm this task is still PLANNED, and
search open PRs for this exact task ID. Pin merged owner #270 at merge commit
`7103412403e672ce7416bbfcc63028988f543494`. Use its accepted definition and
coordinate convention from:

- `02_REGISTRY/research/A4D_METRIC_NULL_HESSIAN_COMPLEX.md`
- `02_REGISTRY/research/certificates/a4d_metric_null_hessian_complex_check.py`

Do not use the archived FUGU bootstrap as an owner: it imports the missing
`a4d_fugu_p1p2_check.py`. Do not use the distinct J2 census symbol also named
`HAQ` as a substitute for the merged `C=H_AQ` owner.

## Objective

Set four algebraically independent variables
`d=(d_0,d_1,d_2,d_3)` and use the merged #270 symbol
`C(d): Sym^2(C^4) -> C^24`. Pin the ten-coordinate convention exactly as in
the owner:

`SYM = [(a,b) | 0 <= a <= b < 4]`, with the coordinate of `d d^T` at `(a,b)`
equal to `d_a d_b` (no extra `sqrt(2)` scaling on off-diagonal slots).

Produce a focused exact certificate and short memo that:

1. decomposes every entry as `C(d) = sum_{r=0}^3 d_r C_r` over the exact
   coefficient field of the accepted owner, proving that the constant and
   every degree-greater-than-one coefficient vanish;
2. expands `C(d) vec_sym(d d^T)` as a homogeneous cubic vector polynomial;
3. extracts every total-degree-three monomial in lexicographic exponent
   order (there are 20 in four variables) and certifies its full 24-vector
   coefficient is exactly zero, reporting all 480 scalar equalities;
4. substitutes `d_r = z_r^{-1}-1` and confirms the result is the zero Laurent
   polynomial, so the coefficient certificate implies
   `C(z) vec_sym(q_0(z)) = 0` identically on `(C^times)^4`;
5. records that at `z=(1,1,1,1)`, `d=q_0=0`; this identity alone makes no
   claim of a nonzero designated IR germ.

Use exact symbolic/rational arithmetic only. Keep the coefficient table
machine-readable in the certificate output or an adjacent JSON artifact, and
make the monomial order and vectorization order explicit.

## Terminal and stopping rule

Terminal:

`A4D-HAQ-LINEARITY-AND-Q0-IDENTITY-COEFFICIENTWISE-EXACT`

Pass only when the four coefficient matrices `C_r`, all 20 cubic coefficient
vectors, and the Laurent substitution check reproduce exactly from the merged
#270 owner. If the reconstructed FUGU `HAQ` cannot be identified term-for-term
with that owner, record the mismatch and stop; do not silently conflate two
symbols or repair the source by fitting orbit data.

## Scope fences

- Do not rerun the rank-9 or kernel-generator proof from #270.
- Do not substitute floating residuals, sampled torus points, SVD, or the
  archived unowned FUGU script for coefficient extraction.
- Do not transfer the identity to `C(conj(z))` or the physical
  `[A(z) | C(conj(z))]` operator.
- Do not infer `E_Q=0`, stress cancellation, nonlinear branch existence,
  uniqueness, gauge symmetry, or a physical/continuum claim.
- No Lean-owner, BOOK, claim, or action changes.

## GitHub execution contract

Start from current main; run
`python3 tools/task_lifecycle.py start WRK-A4D-HAQ-COEFFICIENTWISE-IDENTITY`
as the first task-branch change; open a Draft PR before certificate work; put
the checker and coefficient table in that PR; run the relevant repository
guards; refresh against current main; retire the task before marking the same
PR `Lifecycle: REVIEW`. Never self-merge.

## Chat handoff

Return the worker PR, exact coefficient-field result, the `C_r` and cubic
coefficient certificate summary, the Laurent substitution verdict, guard
results, and any source-symbol mismatch.
