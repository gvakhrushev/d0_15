# EXP-A4D-SELECTED-DIAGONAL-RANK-TRANSITION-CONTINUITY

## Class

EXPENSIVE / DEEP RESEARCH

## Parent

`CTRL-GRAVITY-DYNAMICS-CLOSURE`

## State

PLANNED

## Baseline

Start from fresh current `main` at
`31bdb4bac83e5222dc6fa480e5819ae6b3a81e0a` or newer.

Do not use old review heads #123–#129; their accepted results are already landed.

## Purpose

PR #128 established the pointwise classical-interface passport but also produced
an exact finite counterexample in which relation geometry remains well-defined,
raw solder remains nondegenerate, affine holonomy is trivial, and the background
depends smoothly on a parameter, while the selected sourced-diagonal readout and
mismatch ((\delta,\kappa)) jump at a rank transition.

Determine exactly when the landed relative A/e + sourced-diagonal construction
defines a continuous/stable selected readout under variation of background, and
when this is impossible. Do not re-prove pointwise existence: pressure-test
stability.

## Read first — completely

- `02_REGISTRY/research/MEMO_A4D_CLASSICAL_KINEMATIC_INTERFACE_PRESSURE.md`,
  especially §§10, 11, 12, 14;
- `02_REGISTRY/research/MEMO_A4D_RELATIVE_AE_COMPARISON_PRIMITIVE.md`;
- `02_REGISTRY/research/MEMO_A4D_DIAGONAL_JUNCTION_OVERLAP_LAW.md`;
- `03_FORMALIZATION/D0/Geometry/A4DRelativeAEComparisonSpan.lean`;
- `03_FORMALIZATION/D0/Geometry/A4DConditionalSourcedDiagonalTransport.lean`;
- `03_FORMALIZATION/D0/Geometry/A4DActiveSpanExtensionIndependence.lean`;
- `03_FORMALIZATION/D0/Geometry/A4DLabelledEndpointLocalityPassport.lean`.

## Frozen pointwise geometry

For a parameter family (t\mapsto(A_t,e_t)) at one site, use
[
\mathcal B_t:E_{\rm lab}\to V,\qquad
\mathcal S_t:E_{\rm lab}\to V,
]
[
K_t=\ker\mathcal B_t,\qquad
H_t=K_t^\perp,\qquad
U_t=\operatorname{im}\mathcal B_t,\qquad
M_t=\mathcal S_t(K_t).
]

The canonical correlated action and residual are
[
C_t=J_t^{\rm can}\mathcal B_t=\mathcal S_tP_{H_t},
\qquad
D_t=\mathcal S_tP_{K_t}=\mathcal S_t-C_t,
]
with Role residual (R_{t,r}=D_t\varepsilon_r).

Do not use arbitrary full-fibre extension freedom of (J): PR #127 already
proved that the sourced chain factors through the active-span restriction.

## Mandatory killing witness

The task cannot terminate without literal reproduction of the exact (L=3)
family. Let (j=x_A),
[
f=(1,-2,1),\qquad L_{x,r}=I,
]
[
b_{x,A}(t)=t f(j)e_A,\qquad b_{x,s}=0\ (s\ne A),
]
[
v_A(x)=e_A+f(j)e_B,\qquad v_s(x)=e_s\ (s\ne A).
]

The raw coframe is a determinant-one shear. The affine shift is the exact
periodic gradient of ((0,t,-t)e_A), so affine holonomy is trivial for every
(t). With
[
d_j=f(j)-f(j-1)=(0,-3,3),
]
[
\Delta b_A=t,d_j e_A,\qquad \Delta v_A=d_j e_B.
]
For every (t\ne0), (kappa_A(t;x)=0). At (t=0),
[
\kappa_A(0;x)=(f(j+1)-f(j))e_B=(-3,3,0)e_B,
]
in particular
[
\boxed{\kappa_A(0;0)=-3e_B},\qquad
\kappa_A(t;0)=0\quad\forall t\ne0.
]

Any proposed stability theorem must explain this witness or exclude it by an
explicit additional hypothesis.

## First theorem target: lost-direction criterion

Assume
[
\mathcal B_t\to\mathcal B_0,\qquad
\mathcal S_t\to\mathcal S_0,
]
and along a fixed-rank approach
[
P_{H_t}\to P_*.
]
Prove (H_0\subseteq\operatorname{im}P_*), define
[
\operatorname{im}P_*=H_0\oplus W_{\rm lost},
\qquad W_{\rm lost}\subseteq K_0,
]
and prove or correct
[
\boxed{\lim_{t\to0}C_t-C_0=\mathcal S_0P_{W_{\rm lost}}.}
]
Hence classify exactly when
[
C_t\to C_0\iff \mathcal S_0(W_{\rm lost})=0
]
along that approach.

This must be stated for arbitrary sequences/subsequences in finite dimension,
not only analytic one-parameter curves. Give the exact sequential criterion for
continuity at a point.

## Critical separation

Classify separately:

1. continuity of the relation (mathscr R_t);
2. continuity of active subspace (U_t);
3. continuity of projector (P_{H_t});
4. continuity of correlated action (C_t);
5. continuity of residual (D_t);
6. boundedness of normalized graph operator (J_t);
7. continuity of seed (a_t);
8. continuity of path source;
9. continuity of the affine solution space for (delta);
10. continuity of selected (delta_t);
11. continuity of final (kappa_t).

Do not silently identify any of these properties.

Preserve the control
[
\mathcal B_t\varepsilon_A=t^2e_A,\qquad
\mathcal S_t\varepsilon_A=te_B,
]
for which
[
J_t(e_A)=t^{-1}e_B
]
is unbounded while (C_t\to0). Boundedness of (J) is therefore not necessary
for continuity of downstream action.

## Strong local criterion

Audit the PR #128 claim that (M_0=0) is sufficient for continuity of (C_t,D_t)
at the point for every approaching sequence. If true, give an exact theorem and
record that it does not imply boundedness of (J_t). If false, construct an exact
counterexample and repair the criterion.

Determine also whether (M_0=0) is necessary for universal continuity, or whether
non-graph endpoints can still have continuous (C,D).

## Propagation through the sourced chain

Using landed #125/#127, propagate the continuity classification through
[
a_r=-\bar b_r-C_r,
]
[
S_{p,r}=P_pa_r(y')-a_r(y),
]
[
P_p\delta_r(y')-\delta_r(y)=S_{p,r},
]
and
[
\delta=a+h.
]

Separate continuity of the source, the parallel kernel subspace, the selected
(h), the selected (delta), and (kappa). Identify the earliest failure
stage exactly.

## PR #120 selection rule under pressure

Recover the existing selector literally from the repository: transported mean /
positive common fixed-space projection. Determine:

- when the projector onto the parallel/fixed kernel is continuous;
- what happens at a kernel-dimension jump;
- which spectral-gap / constant-rank hypotheses are sufficient;
- which are necessary;
- whether continuity depends on the observer metric;
- whether the result remains frame-covariant.

Do not replace the existing selector merely because another selector is more
continuous.

## Mandatory remediation audit

### A. Restrict admissible backgrounds

Find minimal additional hypotheses. Candidates include constant
(operatorname{rank}\mathcal B_t), annihilation of lost directions, constant
pair rank, spectral gap, and constant parallel-kernel dimension. Do not impose a
stronger restriction without a counterexample showing why it is needed.

### B. Change canonical representative

A different representative is admissible only if it preserves exact gauge
calibration, frame covariance, label symmetry, pure shift, Nyquist, the (L=3)
corner, and active-span extension independence. If continuous selection is
impossible under those constraints, prove the no-go.

### C. Quotient

Use the theorem-ready quotient condition
[
\mathcal S_y(\mathcal B_y^{-1}W_y)\subseteq W_y
]
for same-fibre quotient graphification, plus transport compatibility / loop
coinvariants for endpoint descent, including finite saturation (W^*).

The zero quotient is not a solution. Any quotient must preserve the claimed
observable distinctions, in particular the mandatory Nyquist/corner response.

### D. Weaken the output

Check whether a coarse continuous observable (q(\delta,\kappa)) exists even
when the full readout is discontinuous. If so, classify its kernel and what is
forgotten. Do not call it the full classical limit.

## Mandatory controls

Recheck:

- flat;
- constant pure shift;
- exact translation gauge;
- (L=3) exact-gauge rank drop;
- the mandatory discontinuity family above;
- (L=2) Nyquist;
- (L=3) corner/curl;
- constant harmonic coframe;
- duplicate increments;
- nontrivial linear holonomy;
- trivial affine holonomy;
- rank-zero and rank-one active spans.

The killing witness already has trivial affine holonomy, so endpoint descent or
flatness cannot be proposed as an automatic cure.

## Required classification matrix

The memo must explicitly classify at least:

- constant-rank graph family;
- rank drop with (M_0=0);
- rank drop with (M_0\ne0) but killed lost directions;
- rank drop with surviving lost direction;
- continuous (C), unbounded (J);
- continuous source, discontinuous selector;
- continuous (delta), discontinuous (kappa), if such a case exists;
- trivial versus nontrivial holonomy.

For every row identify the earliest stage where continuity fails.

## Acceptable terminals

Use the strongest result actually justified:

- `SELECTED-DIAGONAL-RANK-TRANSITION-CONTINUITY-CRITERION-CONSTRUCTED`
  only if a necessary/sufficient criterion is obtained for the stated class and
  propagated to selected ((\delta,\kappa));
- `SELECTED-DIAGONAL-RANK-TRANSITION-STABLE-SELECTION-OBSTRUCTED`
  if universal continuous selection preserving the mandatory controls is
  impossible, with an exact no-go and minimal assumptions;
- `SELECTED-DIAGONAL-RANK-TRANSITION-STRATA-CLASSIFIED`
  if several strata remain and are completely classified.

A terminal saying only “continuity may fail” is insufficient.

## Formalization handoff

This is research, not a Lean task. End with a small theorem-ready package for a
WORKER, preferably:

- lost-direction continuity theorem;
- all-sequence criterion;
- the (M=0) sufficient/universal theorem or its repair;
- source-continuity propagation;
- selector-kernel continuity criterion;
- exact periodic discontinuity witness.

The Lean worker should not need to repeat conceptual research.

## Firewalls

Do not:

- start finite graded dressing;
- declare rank 4 necessary for classicality;
- require an invertible full (J);
- replace labelled path carrier by endpoint quotient before checking holonomy;
- introduce continuum topology;
- make GR/QFT claims;
- build a stress tensor;
- touch time/golden/AF;
- hide discontinuity by choosing a new observable without an explicit forgetful map.

## GitHub-first flow

1. fresh current `main`;
2. lifecycle start;
3. Draft PR before research edits;
4. research only inside that PR;
5. one durable memo;
6. exact arithmetic/checker for mandatory finite witnesses;
7. hostile self-audit of all proposed implications;
8. self-retire before Ready;
9. `Lifecycle: REVIEW`;
10. do not self-merge.

## Exit condition

After this task it must be mathematically precise which additional conditions
turn the already-built pointwise relation/source interface into a stable selected
finite interface, or why no universal stable interface exists without new datum.
