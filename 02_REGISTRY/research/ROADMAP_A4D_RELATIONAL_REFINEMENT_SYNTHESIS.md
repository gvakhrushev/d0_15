# A4D relational refinement synthesis: two orthogonal seams and three finite towers

## Status

CONTROL synthesis / roadmap input.

This memo integrates the common-center matter result with the existing golden/refinement owners. It is not a new theorem owner and does not upgrade claims by itself.

Baseline: `main = e5b5bb15013865eec4bc74d0be0b1d1fcb166039` at the start of the synthesis.

## 1. Truth repairs before synthesis

### 1.1 Golden quadratic: one object, repaired forcing routes

The four Vieta/fixed-point faces of

\[
r^2-r-1=0
\]

are properties of one quadratic object, not four independent laws.

Do not use the older statement that the detector equation `p+p^2=1` and the period-one equation `x=1+1/x` are independent routes: under `x=1/p` they are algebraically the same relation, and `02_REGISTRY/forcing_routes.json` already audits that dependence.

The current repaired multi-route statement is instead:

- `D0-PHI-HURWITZ-CLASS-CANONIZATION-001`: Hurwitz over all reals selects the noble `GL(2,Z)` class; `M1+` canonization selects the minimal-description representative; `x^2-x-1=0` is an output.
- `D0-JONES-SLOT-SELECTOR-001`: Jones quantization plus the explicit rational-capture premise selects the `n=5` slot, with `phi^2` as output. This route is BRIDGE-scoped because its Jones/Niven inputs are not internal finite owners.

The detector closure remains an owned operational identity, but it is not counted as an independent copy of the repaired Hurwitz route.

### 1.2 Delta sign

The owned positive detector offset is

\[
\delta_0=\frac{\sqrt5-2}{2}=\frac1{2\phi^3}>0.
\]

The expression \((2-\sqrt5)/2\) is negative. Do not reverse these signs in roadmap prose.

### 1.3 The dimensional ladder is owned, but its physical interpretation is scoped

The repository already owns

\[
Q(D)=2\delta_0\phi^{D-1}=\phi^{D-4},
\]

with unit value at `D=4`, in `D0.Claims.DimLadderCompact` and its certificate.

This is therefore not merely a mnemonic. What is *not* owned is the promotion

\[
D=4\text{ in that normalization}
\quad\Longrightarrow\quad
\text{physical Lorentz spacetime dimension}
\]

without a typed bridge. The four archive Roles / Clifford-four carrier and the normalization index must remain distinct until such a bridge is proved.


### 1.4 Naming and repeated-factor firewall

Do not call the golden root pair “ABCD” in new task/memo names. `D0-ABCD-001` already means the four-element `DyadABCD` / Role carrier. Use “golden pair”, “golden quadratic” or “period-one representative” for the \((\phi,\psi)\) object.

Likewise, the numeral `2` appears in several already-owned structures — two colors in located primal/dual placement, polarization identities, the two roots of the golden quadratic, and two-tick constructions. These are typed occurrences, not one theorem with a common cause. Do not collapse them without an explicit bridge.

## 2. Three different towers already exist

The nearest roadmap must not use one symbol `N` as if these were the same system.

### Tower A — record / profinite inverse system

Literal owner:

`D0.Geometry.ArchiveRefinementTower`

with

\[
\operatorname{ArchivePoints}(n)=\operatorname{Fin}((n+2)^4)
\]

and flat integer-mod bonding

\[
\operatorname{archiveProjection}_n:
\operatorname{ArchivePoints}(n+1)\to\operatorname{ArchivePoints}(n).
\]

`ArchiveLightProfinite` packages the inverse limit as a genuine Mathlib `LightProfinite`, and `ContinuumAsInverseLimit` uses it as the record/profinite continuum model.

This tower is informational. Its bonding map is not the geometric Role-coordinate bonding map.

### Tower B — Role-phase / CAR finite geometry

Literal carriers:

\[
\operatorname{ArchiveRolePhasePoint}(n)
=
\mathrm{Role}\to\mathrm{Fin}(n+2),
\]

\[
\operatorname{ArchiveRolePhaseGroup}(n)
=
\mathrm{Role}\to\mathbb Z/(n+2)\mathbb Z.
\]

This is the finite geometry on which the current gravity/matter seam actually lives.

A coordinatewise consecutive-level finite-set projection is already owned:

`ArchiveRolePhaseCarrier.archiveRolePhaseProjection`.

It is surjective. However `ArchiveLaplacianRG.exact_projective_compatibility_fails` proves that, for the accepted one-dimensional phase projection and `n>1`, the nearest-neighbor canonical Laplacian does **not** commute exactly with pullback along that projection. Thus “there is a projection” and “the dynamics is natural under it” are already distinct statements.

This carrier supports:

- corrected cubical/CAR differential and `D_H`;
- located primal/dual `J`;
- the full staggered first jet `H(e)`;
- coframe, affine-link, Cartan and moving-differential structures.

The repository already proves that Tower A and the coordinate-wise product bonding of Tower B are not stagewise isomorphic. At the first nontrivial step their zero-fiber cardinalities are `6` and `16` respectively:

`D0-ARCHIVE-FLAT-PRODUCT-BONDING-NOGO-001`.

`D0-ARCHIVE-TWO-LIMIT-SEPARATION-001` records the corresponding record/metric limit separation.

Therefore no future task may identify Tower A and Tower B merely because both stages have cardinality \((n+2)^4\).

### Tower C — golden cylinder / Bratteli / AF refinement

The golden cylinder language already has its own canonical refinement owner:

`D0-BRATTELI-FIBONACCI-REFINEMENT-OWNER-001`.

The forbid-`11` language recovers

\[
M_\phi=
\begin{pmatrix}
1&1\\
1&0
\end{pmatrix},
\qquad
M_\phi^2=M_\phi+I,
\]

with Fibonacci level growth and normalized trace ratio \(\phi\).

`D0-PERRON-SCALE-FLOW-OWNER-001` separately owns the dimensionless scale law

\[
\Lambda_{N+1}/\Lambda_N=\phi.
\]

At the measure layer, `DetectorSupportGoldenWeight.cylWeight_refine` owns the exact cylinder refinement identity

\[
\mu(wA)+\mu(wB)=\mu(w)
\]

from \(\phi^{-1}+\phi^{-2}=1\).

Thus D0 already has a canonical golden refinement object. The missing statement is not “derive a golden tower”; it is a typed relation between that tower and the finite Role-phase/CAR geometry of Tower B.

## 3. Two orthogonal live seams

The nearby roadmap contains two different mathematical problems.

### Seam I — intra-level endpoint comparison

Frozen terminal:

`COMMON-CENTER-CELL-ACTION-NEW-PRIMITIVE-REQUIRED`.

At one fixed Role-phase level, the output-site-local scalar class

\[
g_\xi(e)=M_\xi D_e
\]

is now sharply classified. Exact groupoid composition forces

\[
(D_e g_\xi)_0[h]
=
-M_\xi H_0(h)D,
\qquad
K_\xi=M_{\xi^2}D^2.
\]

Its induced energy Hessian contains same-axis distance-two entries and cannot be a direct elementary-cell energy on the original scalar carrier under the stated locality hypothesis.

For general lifts the flat mixed-cocycle freedom is

\[
B(\xi,h)=B_{\rm adv}(\xi,h)+\mathcal S(h_\xi,h),
\]

\[
\mathcal S:
\operatorname{Sym}^2(\operatorname{im}d_f)\to\operatorname{End}(C^0).
\]

Strict cell support already imposes nonzero distance-two components of \(\mathcal S+\mathcal S^T\).

The new physical question is therefore finite endpoint/common-center comparison and overlap composition. It is *within one Tower-B level*. It is not a refinement map between levels.

### Seam II — inter-level golden / Role-phase weld

The independent strategic question is:

> What, if anything, canonically relates Tower C's golden Bratteli/trace/scale refinement to Tower B's Role-phase/CAR finite geometry?

This must not be formulated as an equality of towers.

Candidate relation types include:

- a level-selection/canonization rule;
- a functor or natural transformation between appropriate finite categories;
- a correspondence/bimodule rather than a map;
- a common spectral-scale law with no carrier map;
- an operator naturality relation after a separately typed comparison map.

The research must determine the strongest type actually supported.

Any positive weld must say explicitly which structures are preserved:

- Role permutation action;
- archive translations / cyclic incidence;
- the already-owned coordinatewise `archiveRolePhaseProjection` and its known exact-Laplacian naturality failure;
- cochain degree and parity;
- located `J`;
- corrected `D_H` or its square, with any required scale factor;
- the complete first jet `H(e)`;
- golden cylinder trace/weight or Perron scale.

A scale identity alone is not a carrier identification.

## 4. Pendulum / tick boundary

The golden tick ladder and its continuous dimensionless envelope are valid owned structures in their declared lane. However:

- `U_A` is a finite cyclic archive translation, not a physical clock;
- `ArchiveSpatialHistorySplit` explicitly keeps history tick, cyclic A-phase, phi-ladder, tick-scale section and observer structure distinct;
- the causal/Pisot Role-A ↔ physical time-axis bridge remains separately classified under `E-TIMEAXIS`.

Therefore no refinement result in this roadmap may infer physical time by identifying a golden step with Role-A translation.

The useful interpretation is narrower: golden refinement is a candidate inter-level relational invariant, not a time coordinate.

## 5. Roadmap dependency order

### Now — formalize already accepted mathematics

Two worker lanes are sufficient:

1. `WRK-A4D-SECOND-ORDER-CELL-ENERGY-WARD`
   - absorb the scalar advective groupoid derivative, forced `K=M_(xi^2)D^2`, complete `L=5` matrices and scoped direct-cell obstruction from the common-center memo;
   - keep the full generic second-order Ward, action-groupoid and transverse-Hessian package.

2. `WRK-A4D-OBSERVER-FRAME-CAR-LIFT`
   - formalize exterior/frame/observer/link results independently;
   - do not select the common-center law.

A third standalone scalar-obstruction worker is unnecessary duplication.

### Now — research in parallel

Two EXP lanes may run concurrently with Lean:

A. `EXP-A4D-ENDPOINT-COMPARISON-JET-OVERLAP-LAW`

Purely intra-level Tower-B problem: construct or terminally classify the finite geometric law that integrates \(\mathcal S\) and recovers the full `H(e)` on arbitrary coframes.

B. `EXP-A4D-GOLDEN-ROLE-PHASE-REFINEMENT-WELD`

Inter-level problem: classify the strongest typed relation between Tower C and Tower B, while respecting the Tower-A/Tower-B bonding no-go.

Neither waits for Lean formalization.

### After both research lanes

Only if both seams admit compatible positive structure should D0 ask for one all-order family

\[
Q_N(e),\quad R_N(\xi;e)
\]

that is simultaneously:

- a valid finite matter action at each Role-phase level;
- compatible with located `J_N`;
- observer/frame covariant;
- coherent under the accepted inter-level weld.

If one seam is terminal no-go/new-primitive, preserve that boundary instead of inventing an all-order action.

### Stress/source remains downstream

A provenance-bearing stress tensor is defined only by variation of the *same* all-order action. The scene coupling remains

\[
99\text{-cut}
\to e_{\rm spatial}
\to Q(e)
\to S_J(e)
\to \text{matter}.
\]

No direct `99 -> 96-shell` or `phi -> stress` shortcut is admitted.

## 6. Strategic interpretation

The useful synthesis is relational, but it is not a new theorem saying that the same object controls every layer.

What is now justified is:

- inside a finite geometry level, absolute site-local gauge data are insufficient; endpoint comparison is forced into the remaining matter lift;
- between refinement levels, D0 already has a golden relational law in a separate cylinder/Bratteli tower;
- the unresolved problem is whether those two relational structures admit a typed weld.

This is a much sharper question than “derive gravity from phi”.

The theory should now try to prove or kill the commutative architecture

\[
\text{golden refinement}
\quad\rightsquigarrow\quad
\text{Role-phase level comparison}
\]

together with

\[
\text{endpoint overlap}
\quad\rightsquigarrow\quad
Q_N(e),
\]

without identifying record refinement, physical time, topological placement, observer metric or scene source.

## 7. Firewalls

Do not claim from this synthesis alone:

- detector and old period-one equations are independent forcing routes;
- Tower A = Tower B = Tower C;
- the flat record `archiveProjection` is a physical Role-phase refinement;
- \(\Lambda_{N+1}/\Lambda_N=\phi\) fixes a carrier comparison map;
- \(\delta_0\) is negative;
- `D=4` in the compact dimension ladder is already physical Lorentz spacetime dimension;
- \(\mathcal S\) is golden;
- `J` is a metric star;
- Role A is physical time;
- a finite all-order matter action, stress tensor or Einstein equation is already owned.

## 8. Immediate roadmap verdict

The nearest research roadmap is therefore:

\[
\boxed{
\text{intra-level } \mathcal S/\text{overlap}
\quad\parallel\quad
\text{inter-level golden--Role-phase weld}
}
\]

with second-order and frame formalization proceeding in parallel and not blocking either experiment.

The earliest future synthesis gate is not “pick a nonlinear energy”. It is:

> determine whether one typed finite architecture can carry both endpoint comparison *within* a Role-phase level and golden coherence *between* levels.
