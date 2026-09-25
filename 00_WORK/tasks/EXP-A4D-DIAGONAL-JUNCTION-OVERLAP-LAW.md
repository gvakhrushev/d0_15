# EXP-A4D-DIAGONAL-JUNCTION-OVERLAP-LAW

## Class

EXPENSIVE / DEEP RESEARCH

## Parent

\`CTRL-GRAVITY-DYNAMICS-CLOSURE\`

## State

PLANNED

## Baseline

Start from fresh current \`main\` after merged PR #117 or newer.

## Read first

Read completely:

1. \`02_REGISTRY/research/MEMO_A4D_LABELLED_REFERENCE_SELECTION_PRINCIPLE.md\`;
2. \`02_REGISTRY/research/MEMO_A4D_SOLDER_REFERENCE_LEG_SECTION.md\`;
3. \`03_FORMALIZATION/D0/Geometry/A4DReferenceJunctionCompressionBoundary.lean\`;
4. \`03_FORMALIZATION/D0/Geometry/A4DReferenceLocalCandidateNoGo.lean\`;
5. \`03_FORMALIZATION/D0/Geometry/A4DTransportedReferenceMismatch.lean\`;
6. \`03_FORMALIZATION/D0/Geometry/A4DAffineOriginSolderBoundary.lean\`;
7. \`03_FORMALIZATION/D0/Geometry/A4DLabelledPathHolonomyDescent.lean\`;
8. the observer/frame substrate from PR #103.

## Frozen result

For a source reference section \(q\),

\[
\delta_r(y)=q_r(y)-v_r(e,y),
\]

and

\[
\Omega_{rs}(y)=q_r(y)-v_s(e,y)
              =v_r(e,y)-v_s(e,y)+\delta_r(y).
\]

The conditional mismatch is

\[
\kappa_q(A,e;x,r)
=
\tau_r(A,e;x)+L_{x,r}\delta_r(x+r),
\]

where

\[
\tau_r(A,e;x)=A_{x,r}(v_r(e,x+r))-v_r(e,x).
\]

PR #117 proves that the old normalization/covariance/path principles do not
select the diagonal \(\delta_r=\Omega_{rr}\).

The minimal unresolved object is therefore a **Role-labelled overlap primitive**
whose diagonal supplies the selector.

## Objective

Derive, construct, or terminally classify one finite overlap law

\[
\Omega_N(A,e,n;y;r,s)\in V_y
\]

together with a diagonal law

\[
\delta_r(y)=\Omega_{rr}(y)
\]

and a sourced labelled path-transport equation strong enough to remove both
known nonselection directions.

Do not merely rename \(q\) or \(\delta\).

## Mandatory structural laws

A viable overlap package must satisfy:

### 1. Source-frame covariance

\[
\Omega(A^g,e^g,n^g;y;r,s)
=
g_y\,\Omega(A,e,n;y;r,s).
\]

Use only the already-owned observer/frame transformation law.

### 2. Solder-difference compatibility

For fixed \(r\),

\[
\Omega_{rs}-\Omega_{rt}=v_t-v_s.
\]

This must make

\[
q_r=v_s+\Omega_{rs}
\]

independent of the chosen outgoing label \(s\).

### 3. Twisted Role cocycle

\[
\Omega_{rs}+\Omega_{st}
=
\Omega_{rt}+\Omega_{ss}.
\]

Do not replace this by the ordinary cocycle: PR #117 shows the ordinary law
forces \(\delta=0\) and fails generic exact pure gauge.

### 4. Diagonal law

The genuinely new part is a finite rule fixing

\[
\delta_r=\Omega_{rr}.
\]

It must be derived from an explicit geometric principle or declared as the
earliest new primitive.  Do not hide it inside notation.

### 5. Sourced path transport

Derive an equation of the form

\[
\delta(y')-\mathcal P_{y\to y'}\delta(y)
=
S_N(A,e,n;\text{labelled edge/path data}),
\]

or an exact groupoid equivalent.

The source term must be explicit and compatible with append/reverse.

A spanning tree or basepoint is downstream of this source law, not a
replacement for it.

## Mandatory acceptance controls

### Flat

\[
\delta_r=0.
\]

### Exact translation gauge

For \(y=x+r\),

\[
\delta_r(y)
=
v_r(e,x)-b_{x,r}-v_r(e,y).
\]

This must reproduce \(\kappa=0\) exactly.

### Pure affine shift

At \(e=0,L=I,b\ne0\),

\[
\delta_r=0,\qquad \kappa=b.
\]

### Curl

The law must reject

\[
\delta\mapsto\delta+\lambda z_{\rm curl}
\]

unless \(\lambda=0\).

### Harmonic

The law must reject

\[
\delta\mapsto\delta+\mu z_{\rm harm}
\]

unless \(\mu=0\).

### Labelled junction

For an \(r\to s\) junction use the actual transported overlap

\[
J_{rs}=L_r\Omega_{rs}.
\]

No endpoint-only quotient.

### Raw finite controls

Keep visible:

- L=2 Nyquist;
- L=3 off-diagonal corner;
- one plaquette curl witness;
- one harmonic cycle;
- one nontrivial labelled holonomy witness.

## Mandatory principle classes to audit

### A. Relative A/e defect law

Test whether a tensor built from the already-owned affine Cartan link and raw
solder legs can source \(\delta\) without identifying \(A=A(e)\).

This is the highest-priority constructive route.

### B. Junction cocycle with diagonal source

Test whether the twisted Role cocycle can be promoted from a tautology to a
sourced law whose diagonal is fixed by local B/E relative data.

### C. Observer-positive solution after source law

Once a source law is known, use the owned \(h_n\) only to resolve any remaining
kernel/global integration freedom.

Do not use positivity to invent the source itself.

### D. Basepoint/tree integration after source law

If the source is closed but not exact, classify exactly which basepoint/tree/
cycle datum is required.

Do not hide harmonic choices.

### E. Full-affine option

If affine-point solder/origin structure is needed, keep the PR #115 translation
defect explicit.

Covariance alone is not selection.

## Exact hostile controls

At minimum include:

- the PR #117 L=3 pure-gauge shift cycle \((3,3,-6)e_B\), whose required
  diagonal overlap is \((15,-3,-12)e_B\);
- the L=2 Nyquist witness with raw parallel defect \(4\);
- the L=3 off-diagonal curl witness;
- the constant harmonic coframe witness;
- a nonzero pure affine shift;
- the exact rational A/B boost.

## Nonselection firewall

Every proposed law must be tested explicitly against both

\[
z_{\rm curl},\qquad z_{\rm harm}.
\]

If either survives, the selector is incomplete.

## Finite-E firewall

Do not start \`EXP-A4D-FINITE-GRADED-COFRAME-DRESSING\`.

That gate remains closed until a usable diagonal overlap/source law lands or the
repo explicitly adopts the additional geometric datum required by the
terminal.

## Other firewalls

Do not:

- reopen affine representability;
- reopen row/vector typing;
- identify \(A=A(e)\);
- impose ordinary endpoint compression;
- use \([H,T_b]\) as the selector;
- introduce golden/AF data;
- start stress/Einstein/time;
- select a second jet.

## Preferred terminals

Positive:

- \`DIAGONAL-JUNCTION-OVERLAP-LAW-CONSTRUCTED\`;
- \`SOURCED-OVERLAP-TRANSPORT-CONSTRUCTED\`;
- \`RELATIVE-AE-OVERLAP-SELECTOR-CONSTRUCTED\`.

Scoped:

- \`DIAGONAL-OVERLAP-REQUIRES-NEW-RELATIVE-AE-DEFECT\`;
- \`OVERLAP-TRANSPORT-REQUIRES-BASEPOINT-CYCLE-DATUM\`;
- \`OWNED-GEOMETRY-DOES-NOT-FIX-DIAGONAL-OVERLAP\`.

Use only the strongest statement actually derived.

## Deliverable

One durable theorem-ready memo containing:

1. exact overlap type contract;
2. source-frame law;
3. solder-difference law;
4. twisted cocycle;
5. diagonal/source law attempted;
6. sourced path-transport equation;
7. flat/pure-gauge/pure-shift controls;
8. curl and harmonic rejection tests;
9. L=2/L=3 controls;
10. observer/basepoint use only after the source law;
11. exact terminal;
12. theorem-ready handoff;
13. exactly one next step.

No Lean source.

## GitHub-first flow

Fresh branch from current main → lifecycle start → Draft PR immediately →
research only in PR → durable memo → self-retire → \`Lifecycle: REVIEW\` →
Ready → do not self-merge.

## Exit condition

A Role-labelled diagonal overlap law and sourced path-transport equation select
the reference section while rejecting both curl and harmonic nonselection
directions, or the earliest additional relative-A/e/basepoint/cycle primitive
needed to do so is terminally identified without starting finite E dressing.
