# EXP-A4D-ENDPOINT-COMPARISON-JET-OVERLAP-LAW

## Class

EXPENSIVE

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

PLANNED

## Objective

Attack the now sharply isolated finite matter primitive left by the common-center groupoid research:

> construct, or terminally obstruct in a clearly stated geometric class, the endpoint/common-center comparison law whose flat second-order jet is
>
> [
> \mathcal S:\operatorname{Sym}^2(\operatorname{im}d_f)\to\operatorname{End}(C^0),
> ]
>
> and whose finite overlap-composition law extends the owned first-order Cartan matter generator to general coframe backgrounds.

This is a deep research task, not a Lean task.

Do not search for another abstract Hodge selector. The target is now an explicit geometric comparison/interpolation datum.

This EXP is **strictly intra-level**: work at one fixed `ArchiveRolePhaseGroup N` / `ArchiveCochain N` level. It does not derive or assume a refinement map between different `N`.


## Carrier / tower firewall

Read also:

`02_REGISTRY/research/ROADMAP_A4D_RELATIONAL_REFINEMENT_SYNTHESIS.md`.

Three different tower structures exist and must remain distinct:

1. **Record/profinite tower** — `ArchivePoints n = Fin ((n+2)^4)` with flat integer-mod `archiveProjection`.
2. **Role-phase/CAR geometry** — `ArchiveRolePhaseGroup N = Role -> ZMod (N+2)`; this is the carrier used by `J`, `H(e)`, `D_H`, coframes and the present task.
3. **Golden cylinder/Bratteli tower** — recovered `M_phi`, Fibonacci/AF refinement and Perron scale ratio `phi`.

This experiment lives entirely in **(2)**.

Do NOT:

- use the flat record `archiveProjection` as a bonding map for Role-phase cells;
- infer a golden `N -> N+1` law;
- assume the Bratteli level index and the Role-phase period index are the same type or physical quantity;
- use `phi` to choose the comparison jet `S`;
- identify any level step with physical time.

The repository already owns a bonding-fiber obstruction between (1) and the natural coordinate-product refinement underlying (2). The separate inter-level question (2) <-> (3) belongs to `EXP-A4D-GOLDEN-ROLE-PHASE-REFINEMENT-WELD`.

A positive result here is therefore a law `at fixed N`, not a tower naturality theorem.

## Mandatory frozen inputs

Read completely before doing any new construction:

- `02_REGISTRY/research/MEMO_A4D_COMMON_CENTER_MATTER_GROUPOID_ACTION.md`
- `02_REGISTRY/research/MEMO_A4D_SECOND_ORDER_CARTAN_CELL_ENERGY_INTEGRABILITY.md`
- `02_REGISTRY/research/MEMO_A4D_SOLDERED_CREATOR_OBSERVER_FRAME_LIFT.md`
- `02_REGISTRY/research/ROADMAP_A4D_RELATIONAL_REFINEMENT_SYNTHESIS.md`

Also inspect the literal owners from merged PRs #70, #74, #75 and #76.

Treat as frozen:

1. corrected cubical/CAR differential and `D_H`;
2. PR #70 affine links, path composition, flat translation gauge, curvature/torsion and path-word algebra;
3. PR #75 complete uncentered staggered first jet `H(e)`, including scalar neighbor, endpoint half-average, both corner paths, Nyquist and degree/parity controls;
4. PR #76 fixed located two-color `J`;
5. PR #74 scoped scalar two-sided inverse/locality no-go;
6. exterior/frame/observer lift from the durable frame memo;
7. generic second-order Ward identities and transverse Hessian freedom from the durable second-order memo.

Do not wait for active Lean workers. They formalize accepted mathematics and are not a research dependency.

## New frozen result from the common-center memo

The output-site-local scalar class

[
g_\xi(e)=M_\xi D_e
]

is now classified strongly enough to stop searching inside it.

Exact groupoid composition forces

[
(D_e g_\xi)_0[h]=-M_\xi H_0(h)D,
qquad
K_\xi=M_{\xi^2}D^2.
]

It has an exact pure-gauge finite cocycle, but its induced Hessian contains unavoidable same-axis distance-two entries and therefore cannot come from a direct elementary-cell energy on the original scalar carrier.

For unrestricted scalar lifts, every flat mixed-cocycle solution differs by

[
B(\xi,h)
=
B_{\rm adv}(\xi,h)
+
\mathcal S(h_\xi,h),
]

with `𝒮` symmetric in the two coframe inputs.

Strict direct-cell support already forces, on the delta witness,

[
(\mathcal S(h,h)+\mathcal S(h,h)^T)_{+1,-1}
=
-L^2/2,
]

[
(\mathcal S(h,h)+\mathcal S(h,h)^T)_{0,+2}
=
-L^2/4.
]

Therefore a nearest-neighbor matrix-output correction is insufficient. The missing law must compare endpoints across a two-edge patch / common-center overlap while still yielding a cell-supported final action, or else demonstrate why this is impossible in a precise class.

The pure-gauge graded benchmark reproduces every block of `H(d_f ξ)`, including Nyquist and the corner, but it fails to define the full first jet on arbitrary uncentered `e`. Constant harmonic strains, plaquette curl and a rational boost leave its potential domain.

These are starting facts, not targets to rediscover.

## Central research question

Can the owned affine/path/located/exterior geometry canonically produce endpoint-to-center comparison maps and an overlap law such that:

1. the flat first derivative is the complete owned `H(e)` on ALL uncentered coframe directions, not only `e=d_f ξ`;
2. the induced flat comparison jet is a geometrically derived `𝒮`, not a fitted Hessian correction;
3. the matter transformation obeys an exact finite background-dependent groupoid composition law;
4. the final direct or parent cell action is local in a precisely stated finite sense;
5. the fixed located `J` is retained;
6. observer/frame covariance works with transformed observer `n`;
7. the construction handles nonexact/harmonic and plaquette-curved coframes.

If yes, compute the resulting second jet and nonlinear energy boundary.

If no, prove a scoped no-go for the largest geometric comparison class actually exhausted.

## Research order

### A. Define the comparison carrier before coefficients

Identify the minimal typed objects that a common-center law needs.

Candidates may involve:

- oriented edge endpoints;
- half-edge or face-center comparison objects;
- affine pull links from PR #70;
- exterior lifts of the linear link part;
- raw solder/coframe data;
- cell orientation;
- fixed primal/dual placement.

Do not introduce a continuum midpoint or metric barycenter unless it is constructed from finite repository data.

Specify exactly what is compared to what.

### B. Endpoint-to-center factorization

Try to factor a matter comparison along an edge/cell schematically as

[
T_{x\leftarrow y}
=
C_{x\leftarrow c}\,C_{c\leftarrow y}
]

or the correctly typed finite analogue.

Determine:

- whether `c` is a genuine new finite object or only bookkeeping;
- how two cells sharing an edge compare their center data;
- how path reversal acts;
- how orientation enters;
- whether the factorization is unique.

The old fact that an endpoint map can be algebraically factorized in many ways is not enough. The rule must be geometric and compositional.

### C. Derive the overlap law

For adjacent cells / overlapping endpoint comparisons, formulate an exact finite compatibility condition.

This is the finite datum that should integrate `𝒮`.

The law must reduce to the owned node-translation groupoid on pure-gauge backgrounds, while allowing endpoint differences of the gauge parameter.

Do not assume ordinary background-independent representation composition.

### D. Compute the flat jet

Expand the geometric overlap law at flat background.

Derive, rather than prescribe,

[
\mathcal S(h_1,h_2).
]

Test immediately whether it satisfies the scalar delta constraints above.

Compute the complete `L=5` matrix output, including:

- `(+1,-1)`;
- `(0,+2)`;
- all diagonals;
- skew output if present.

Then test a non-delta field with `G^2\ne0`.

A construction that only fits diagonal entries is not sufficient.

### E. Recover the FULL PR #75 first jet

This is mandatory.

For arbitrary uncentered `e`, not only exact `d_f ξ`, derive:

[
DW|_0(e)=H(e).
]

Audit separately:

- scalar nearest-neighbor term;
- endpoint half-average;
- `U_s` path;
- `U_sU_r^{-1}` corner path;
- all Fock degrees;
- parity;
- simultaneous signed Role permutations;
- `L=2` Nyquist raw mode;
- `L=3` corner.

If only `H(d_f ξ)` is recovered, classify the result as pure-gauge only and do not call the cell action constructed.

### F. Harmonic and transverse controls

The construction must be defined on backgrounds outside `im d_f`.

At minimum test:

1. constant harmonic strain `e_A^A=t`;
2. one plaquette-curl excitation;
3. nonzero open affine torsion;
4. if applicable, nonzero linear curvature.

Determine whether comparison around a square depends on path.

If it does, decide whether curvature/torsion is legitimate action data or an obstruction to a common-center law.

### G. Observer/frame covariance

Use the exterior lift and

[
h_n=-\eta+2n^\flat\otimes n^\flat.
]

Test the exact rational A/B boost from the frame memo.

Transform BOTH the coframe/frame data and observer `n`.

The desired law must not use fixed counting `I` as the Lorentz metric.

`n=e_A` remains a reference gauge only.

Determine whether the comparison maps themselves transform covariantly, not merely the final quadratic form.

### H. Fixed located-J boundary

Do not move or metric-deform `J`.

Given the primal comparison action, derive the dual action through the fixed pairing where possible.

Track the shifted-anchor obstruction explicitly.

A positive result must explain how common-center comparison handles those anchors. A negative result must state whether the obstruction is algebraic, geometric, or only sitewise-local.

### I. Locality taxonomy

For every candidate clearly distinguish:

- locality of geometric input;
- elementary-cell support of the parent action;
- support of the effective eliminated kernel;
- path-word length;
- compressed matrix stencil;
- locality of inverses;
- finite circuit depth.

The common-center memo already proves that a uniformly bounded compressed support / circuit depth cannot hold for the constant isotropy flow. Do not demand an already impossible notion as the physical locality criterion.

A promising route is an inverse-free local parent whose eliminated effective kernel may be nonlocal. Test this explicitly rather than assuming it.

### J. Transverse modulus

The current research leaves a plaquette-curvature quadratic modulus invisible to pure-gauge Ward tests.

Determine whether the new overlap law:

- fixes it;
- relates it to curvature/torsion coefficients;
- or leaves a genuine constitutive parameter.

If a parameter survives all exact finite covariance/composition constraints, that is a valid terminal result.

Do not hide it by normalization.

## Required controls

Use exact symbolic/rational calculations whenever possible.

Mandatory finite controls:

- scalar `L=3,5,7`;
- `L=5` delta and non-delta full second jets;
- `L=2` Nyquist;
- `L=3` distinct-axis corner;
- full Fock degrees `0..4`;
- parity;
- nontrivial Role permutation;
- constant harmonic coframe;
- plaquette curl;
- rational Lorentz boost with moving observer;
- fixed located-J anchor comparison;
- flat limit;
- pure gauge;
- at least one transverse non-pure-gauge background.

Numerical floating-point agreement is not a proof.

## Hostile controls

Actively try to falsify every positive construction with:

- reversed orientation;
- alternate path through the same cell;
- adjacent-cell overlap;
- two different decompositions of the same affine path;
- period wraparound;
- nonzero torsion;
- nonzero curvature if the formula claims that scope;
- adding a constant gauge parameter;
- changing the potential representative on a pure-gauge orbit.

## Questions the terminal memo must answer

1. What is the exact finite comparison object?
2. What is the endpoint-to-center map?
3. What is the overlap/composition law?
4. Is the law canonical from current D0 owners or does it require a new primitive?
5. What `𝒮` does it induce?
6. Does `𝒮` satisfy the full scalar support constraints?
7. Does the construction recover `H(e)` for all uncentered `e`?
8. How are harmonic and curl backgrounds handled?
9. Does a local inverse-free parent exist even if the effective energy is nonlocal?
10. Does observer/frame covariance hold?
11. How is the fixed located `J` respected?
12. What locality notion actually holds?
13. Is the transverse plaquette modulus fixed?
14. Is there now an all-order provenance-bearing finite matter action?
15. If not, what is the single earliest remaining datum?
16. Which statements are genuinely fixed-`N`, and which would require the separate inter-level weld before they can be transported across levels?

## Terminal verdict

Return exactly one primary terminal, with scope made literal.

Preferred semantic forms:

### Positive

`ENDPOINT-COMPARISON-OVERLAP-LAW-CONSTRUCTED`

Use only if a finite geometric comparison/overlap law is actually constructed and it recovers the full owned first jet on general coframes.

If a local inverse-free parent action is additionally constructed, state that as a separate secondary result.

### Partial positive

`GEOMETRIC-COMPARISON-JET-CONSTRUCTED-FINITE-INTEGRATION-MISSING`

Use if `𝒮` is derived geometrically and satisfies the required jets, but no exact finite overlap integration is obtained.

### Scoped no-go

`COMMON-CENTER-ENDPOINT-COMPARISON-CLASS-NOGO`

Use only after clearly defining and exhausting the comparison class being ruled out.

### Remaining primitive

`ENDPOINT-OVERLAP-COMPARISON-NEW-PRIMITIVE-REQUIRED`

Use if current geometry still does not choose the comparison law. Name its minimal typed signature and its unavoidable degrees of freedom.

## Deliverable

Produce one durable theorem-ready memo suitable for `02_REGISTRY/research/`.

It must contain:

- exact repository baseline;
- frozen owners;
- construction or scoped no-go;
- formulas for the comparison jet;
- exact finite controls;
- locality statement;
- observer/frame and located-J boundaries;
- transverse-modulus status;
- one primary terminal;
- theorem-ready handoff;
- exactly one recommended next step.

Do NOT edit Lean, lifecycle files, manifest, claims, generated views or release metadata.

Do NOT create additional speculative tasks.

## Truth firewall

Do not promote any result to:

- Spin representation;
- physical causal time;
- unique nonlinear energy without proof;
- physical Lorentz stress before one same-action variation exists;
- stress conservation without the relevant EOM;
- Einstein equations;
- BOOK `F_N`;
- direct `99 → matter`;
- SM gauge derivation;
- metric reinterpretation of `J`;
- universal no-go beyond the class actually exhausted;
- any statement that the comparison jet `S` is selected by the golden refinement law.
