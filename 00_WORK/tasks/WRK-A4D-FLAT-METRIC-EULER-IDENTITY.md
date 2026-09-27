# WRK-A4D-FLAT-METRIC-EULER-IDENTITY

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`  
Research lane: joint-Palatini tangent-cone closure

Repository: `gvakhrushev/d0_15`  
Base: `main`  
Branch: `wrk/a4d-flat-metric-euler-identity`  
Primary artifact: `02_REGISTRY/research/A4D_FLAT_METRIC_EULER_IDENTITY.md`  
Execution: `GitHub-first`

## Why delegated

The open joint-Palatini work repeatedly uses the structural statement
`E_Q(Q,I) ≡ 0`: at identity links the naked-star curvature vanishes, so a
near-flat joint-critical germ should have its first nonzero connection
coefficient in the source-invisible joint kernel.  PR #231 explicitly records
that this direct nonlinear identity was not actually proved there.  Closing it
is a bounded exact finite-symbolic obligation over the already-owned star
formula, independent of the larger nonlinear germ classification, and is
therefore suitable for a WORKER.

## Objective

Build a direct exact owner for the flat-link metric Euler identity of the
accepted naked-star finite action.

Starting from the repository's actual finite star density/Euler definitions,
construct the metric/solder Euler map `E_Q` without replacing it by a
continuum Einstein equation or by rank arithmetic.  Prove or refute, component
by component, that for the full declared finite carrier

[
E_Q(Q,I)=0
]

identically in the admissible metric/solder variables `Q`.

The result must be strong enough to justify the tangent-cone use made by the
joint-Palatini lane: if `K(h)=I+h^m A+o(h^m)`, then the constant-in-connection
term in the metric Euler expansion is absent because the exact finite
`E_Q(Q,I)` vanishes, not because a sampled Hessian happened to have a null
row.

## Required gates

1. Locate and pin the exact merged owner definitions used for the naked-star
   density, identity-link configuration, metric/solder variables and Euler
   partial.  Record their merge SHAs in the memo.
2. Derive `E_Q` from the literal finite formula.  Do not infer the identity
   from `H_AQ`, Hessian symmetry, orbit ranks, or a continuum curvature
   slogan.
3. Prove/refute every independent metric/solder Euler component at `K=I`
   exactly.  Symbolic polynomial/rational identities are preferred; floating
   zero tests are forbidden.
4. Add a hostile non-flat control using an already-owned curved/nonidentity
   configuration for which the same evaluator produces a certified nonzero
   metric response.  This guards against an evaluator that is identically
   zero by construction.
5. State the precise consequence for the first connection valuation of a
   near-flat analytic/Puiseux joint germ.  Do not claim existence, uniqueness,
   smoothness, or Einstein response of that germ.
6. If the identity depends on a convention (polarized character, transpose,
   conjugate pairing, metric coordinate chart), make the convention explicit
   and prove the conversion to the direct physical Euler map.
7. Supply a self-contained exact certificate under
   `02_REGISTRY/research/certificates/a4d_flat_metric_euler_identity_check.py`.

## Terminals

Use

`J2-FLAT-LINK-METRIC-EULER-IDENTITY-CERTIFIED`

only if the literal direct finite Euler map is identically zero at identity
links on the complete declared carrier and the hostile non-flat control is
nonzero.

Use

`J2-FLAT-LINK-METRIC-EULER-IDENTITY-REFUTED`

only with an exact admissible counterexample/component from the literal owner
formula.

Otherwise remain Draft/BLOCKED and name the single missing convention or owner
definition.

## Scope fences

No nonlinear branch search, no joint-kernel census, no KKT decomposition, no
new action term, torsion constraint, Holst term, spectral filter, boundary
selector or `#202` edits.  No claim/release/BOOK promotion.  This task owns
only the direct flat-link metric Euler identity and its exact consequence for
the tangent cone.

## GitHub execution contract

Start from fresh current `main`; run
`python tools/task_lifecycle.py start WRK-A4D-FLAT-METRIC-EULER-IDENTITY` as
the first branch lifecycle change; open a Draft PR before substantive research
or code; keep the memo and exact certificate in that PR; run the relevant
repository guards; retire the task in the same PR before Ready; set
`Lifecycle: REVIEW`; never self-merge.

## Chat handoff

Return only the PR number/head, exact terminal or blocker, the direct owner
formula/convention used, whether every flat-link metric Euler component
vanishes, the hostile non-flat control, and validation commands.  Keep the full
derivation in GitHub.
