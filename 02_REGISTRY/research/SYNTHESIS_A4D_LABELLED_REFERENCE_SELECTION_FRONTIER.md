# SYNTHESIS_A4D_LABELLED_REFERENCE_SELECTION_FRONTIER

## Status

DURABLE SYNTHESIS / POST-PR-114/#115/#116 FRONTIER.

## 1. What is now owned

The affine-sensitive matter seam is no longer blocked by representability,
row/vector typing, affine translation response, or conditional B/E comparison.

Lean owns:

- the nilpotent affine translation response \(T_b\) and affine semidirect lift;
- the exact full-affine origin covariance identity and the linear-only solder
  translation defect;
- the conditional transported-reference mismatch
  \[
  \kappa_q(A,e;x,r)=A_{x,r}(q_r(x+r))-v_r(e,x)
  \]
  for a supplied source reference field \(q\);
- flat, pure-shift, cancellation and nonidentity controls for the induced
  nilpotent matter response.

Research PR #114 additionally classifies the selection problem for \(q\).

## 2. PR #114 terminal

The strongest honest terminal is

\[
\texttt{SOLDER-REFERENCE-LEG-REQUIRES-NEW-GEOMETRIC-SELECTION-PRINCIPLE}.
\]

This is not a universal nonexistence theorem.

It states that the currently owned geometry plus the old mandatory controls do
not select a unique intrinsic source reference section.

Natural local candidate classes fail, one endpoint/node origin is too small,
and labelled path composition exposes a junction defect.

## 3. Exact junction boundary

For consecutive affine edges,

\[
\kappa_1+L_1\kappa_2
=
((A_1A_2)(q_2)-v_1)+L_1(q_1-v_2).
\]

Therefore compression to one endpoint-origin mismatch requires the extra
junction condition

\[
q_1=v_2.
\]

That condition is not generic and already fails at flat for mixed Role labels.
The labelled path parent remains the correct category.

## 4. Constructive nonselection

Conditional on one admissible seed \(q\), PR #114 constructs two independent
deformation directions:

\[
q\mapsto q+\lambda z_{\rm curl},
\]

and

\[
q\mapsto q+\mu z_{\rm harm}.
\]

Both preserve:

- flat normalization;
- exact pure-gauge cancellation;
- nonzero pure-shift visibility;
- pure-linear frame covariance.

But they change respectively:

- local curl/corner response;
- global harmonic/cycle response.

Hence

\[
q_{\lambda,\mu}
=
q+\lambda z_{\rm curl}+\mu z_{\rm harm}
\]

is an explicit conditional nonselection family.

Any future selector must explain why both deformations are inadmissible.

## 5. Full affine covariance is not selection

PR #115 Lean-owns:

- if both reference and solder legs transform as affine points, their mismatch
  transforms homogeneously by the target linear part;
- if the reference transforms affinely but the solder leg keeps only the
  current linear law, the residual node-translation defect is exactly the node
  shift.

This resolves the covariance boundary.

It does not choose \(q\).

## 6. Current heavy research

The active research task is

\`EXP-A4D-LABELLED-REFERENCE-SELECTION-PRINCIPLE\`.

It must introduce one independently motivated geometric selection principle,
not another convenient \(q\)-formula.

Mandatory tests:

1. flat \(q=e_r\);
2. exact pure-gauge \(\kappa=0\);
3. pure affine shift remains visible;
4. pure-linear frame covariance;
5. an explicit labelled junction/overlap law;
6. rejection of \(z_{\rm curl}\);
7. rejection of \(z_{\rm harm}\);
8. preservation of L=2 Nyquist, L=3 corner, curl and harmonic cycle data.

Principle classes to audit include:

- labelled junction/overlap cocycles;
- observer-positive variational selection using the already-owned \(h_n\);
- basepoint/path/spanning-tree gauge fixing;
- full affine-origin overlap structure;
- equivariant/orbitwise selection.

## 7. Current workers

Two theorem-ready workers are intentionally independent of the heavy selection
problem:

- \`WRK-A4D-REFERENCE-JUNCTION-COMPRESSION-BOUNDARY\`;
- \`WRK-A4D-REFERENCE-LOCAL-CANDIDATE-NOGO\`.

They formalize already-derived boundaries and must not choose the physical
selector.

## 8. Finite E remains blocked

\`EXP-A4D-FINITE-GRADED-COFRAME-DRESSING\` remains BLOCKED.

Neither PR #114 nor full affine covariance opens that gate.

The finite graded E dressing may start only after a usable labelled-edge
reference selector or an explicitly adopted equivalent geometric datum lands.

## 9. Firewalls

Do not reopen:

- affine representability;
- row/vector conversion;
- the nilpotent affine response;
- conditional \(\kappa_q\);
- endpoint-only path compression;
- \(A=A(e)\);
- \([H,T_b]\) as a selector;
- stress/Einstein;
- golden/AF refinement.

## 10. One current question

What geometric principle identifies the same Role-labelled edge reference
across junctions and transverse curl/harmonic sectors strongly enough to select
one \(q\), while preserving the exact flat, pure-gauge, pure-shift and frame
controls?
