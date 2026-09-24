# EXP-A4D-PATH-GROUPOID-CROSSED-MATTER-LIFT

## Class

EXPENSIVE / DEEP RESEARCH

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

PLANNED

## Start gate

SATISFIED on current `main` after merged PR #101 and PR #102.

Read completely:

- `02_REGISTRY/research/MEMO_A4D_CROSSED_CONSTITUTIVE_REPRESENTATION.md`;
- `02_REGISTRY/research/MEMO_A4D_PATH_RESOLVED_MATTER_WORD_ACTION.md`;
- `03_FORMALIZATION/D0/Geometry/ArchivePathWordAlgebra.lean`;
- the PR #70 affine Cartan/path owners;
- the landed PR #102 crossed path-algebra boundary modules;
- the located primal/dual `J` owners needed only for the final duality check.

The parallel `WRK-A4D-CROSSED-DERIVATION-INTEGRABILITY` may proceed independently.
Do not wait for it. Treat any unmerged observer/frame worker result as noncanonical until it lands.

## Frozen boundary

PR #101 constructs the compressed finite algebra

```text
A_N = (Fun(X_N, E_deg)) ⋊ X_N
```

and an exact pure-gauge crossed subpackage, but leaves the full raw-background affine-sensitive
matter lift missing.

PR #102 Lean-owns:

- scalar vertical word mixing;
- full staggered first-jet support through path words of length at most two;
- quadratic endpoint-dressing second-jet nonselection.

The new research hypothesis to test is:

> generic harmonic/curl background data should live first on a free path/groupoid representation,
> and descent to the endpoint/group-compressed algebra should occur only under an explicit
> integrability/holonomy condition.

Do not assume this conclusion; derive or refute it.

## Objective

Construct or terminally classify one **path-resolved crossed matter lift**

```text
Pi_{A,e,n}(p)
```

for free PR #70 path words `p`, with elementary link letters

```text
ell_N(A,e,n; x,r)
```

that reproduce the landed first jet and retain relative affine holonomy instead of quotienting
all paths with the same endpoints.

The primary result must separate:

1. existence on the free path/path-groupoid parent;
2. composition/reversal;
3. descent to the finite endpoint crossed product;
4. failure of descent caused by cycle or plaquette holonomy.

## Mandatory attack

### A. Type the parent literally

Use the existing PR #70 free path/path-expression types. Do not invent an abstract category if the
repository already has the needed source/target, append and reverse operations.

Keep distinct:

- affine connection `A`;
- raw coframe `e`;
- observer `n`;
- archive path word `p`;
- background/groupoid arrow.

No silent `A=A(e)`.

### B. Elementary link seed

Construct or classify a local link letter

```text
ell_N(A,e,n;x,r)
```

in an appropriate path-expression/CAR target.

Required limits:

- flat zero-shift limit gives the landed linear/Lorentz exterior link;
- on `e=d_f phi`, agree with the exact pure-gauge conjugated letter from PR #101;
- infinitesimal derivative reproduces the complete landed first jet, including the scalar
  `U_r U_t` / `U_r^{-1}U_t` word mixing and CAR corner terms;
- retain harmonic, curl, Nyquist and L=3 corner backgrounds rather than projecting them away.

A fiber-only `16x16` affine representation is a hostile control, not an acceptable solution.

### C. Free-path composition

Derive exact append and reverse laws for `Pi(p)`.

Determine whether the natural target is:

- units of a free path-expression algebra;
- an inverse-free local parent;
- a larger typed CAR/path algebra;
- or a path-groupoid representation with local coefficient operators.

State precisely which structure is actually constructed.

### D. Holonomy and descent

For two free paths with the same endpoints, compute the relative matter transport.

Test separately:

- a contractible plaquette curl witness;
- a nonzero cycle/harmonic witness;
- exact/pure-gauge background.

Derive the exact criterion for factorization through the endpoint/group-compressed algebra.

The existing theorem

`pathEval_factors_pairGroupoid_iff_trivial_holonomy`

is a key model: reuse its logic rather than restating it informally.

### E. Compressed crossed-product boundary

Explain exactly how the PR #101 compressed algebra is recovered when descent holds.

If the new integrability worker lands during this research, reconcile the scalar quotient theorem
with the path-holonomy criterion. If it does not land, keep that comparison theorem-ready only.

### F. Observer/frame and located-J

Only after the path law exists:

- check moving-observer/frame covariance using canonical landed owners only;
- define the dual transport through fixed located `J_N` by the forced contragredient formula;
- verify that path resolution does not erase the shifted dual anchors.

Do not make the whole task depend on an unmerged observer worker.

### G. Constitutive seed

Do **not** invent a new second-order selector.

Only if the path lift is constructed, test whether the independently owned

```text
W_flux(e) = I + H(e)
```

can be transported consistently on the same free-path/background groupoid.

Crossed dressing nonselection from PR #101 remains a truth firewall.

## Hostile controls

At minimum include exact controls for:

- `L=3` plaquette curl;
- `L=5` nonzero cycle/harmonic period;
- one exact pure-gauge field;
- one Nyquist case at `L=2`;
- one length-two CAR corner;
- two same-endpoint paths with different affine holonomy;
- one case where free-path transport descends;
- one case where endpoint quotient provably loses information;
- the 16-state and 32-state homogeneous affine fiber lifts as controls, not automatic solutions.

Use exact symbolic/rational arithmetic.

## Allowed terminal forms

Examples:

- `PATH-GROUPOID-CROSSED-MATTER-LIFT-CONSTRUCTED-DESCENT-CLASSIFIED`;
- `PATH-GROUPOID-LIFT-CONSTRUCTED-CONSTITUTIVE-COMPATIBILITY-MISSING`;
- `PATH-GROUPOID-LIFT-REQUIRES-NEW-AFFINE-PATH-RESPONSE-PRIMITIVE`;
- `FREE-PATH-PARENT-SUFFICIENT-ENDPOINT-DESCENT-SCOPED-NOGO`.

Use only the strongest wording actually proved.

## Downstream firewall

Do not promote:

- stress tensor;
- Einstein equations;
- physical time;
- golden/phi matching;
- a universal second jet;
- `A=e` or `A=A(e)`;
- endpoint-only transport on a background with nontrivial holonomy.

## Deliverable

One durable theorem-ready memo in `02_REGISTRY/research/` containing:

- literal free-path carrier/target;
- elementary link law;
- append/reverse law;
- exact first-jet comparison;
- plaquette and cycle holonomy controls;
- descent theorem or scoped obstruction;
- compressed crossed-product recovery;
- optional observer/J compatibility;
- constitutive compatibility result only if actually derived;
- terminal verdict;
- theorem-ready handoff;
- exactly one recommended next step.

No Lean source.

## GitHub-first flow

1. fresh branch from current `main`;
2. `python tools/task_lifecycle.py start EXP-A4D-PATH-GROUPOID-CROSSED-MATTER-LIFT`;
3. immediately open Draft PR before research edits;
4. research and durable memo only inside that PR;
5. before Ready self-retire the task;
6. set `Lifecycle: REVIEW`;
7. Ready for review;
8. do not self-merge.

## Exit condition

A free-path/path-groupoid matter lift is either explicitly constructed with an exact endpoint
descent criterion, or the earliest additional affine path-response primitive needed for such a
construction is terminally identified, without hiding harmonic/curl holonomy in an endpoint
quotient.
