# SYNTHESIS_A4D_DIAGONAL_OVERLAP_FRONTIER

## Status

DURABLE SYNTHESIS / POST-PR-117/#118/#119 FRONTIER.

## 1. What is now owned

Lean owns the algebraic reference substrate through:

- nilpotent affine translation response and grading boundary;
- full-affine origin covariance boundary;
- conditional transported-reference mismatch \(\kappa_q\);
- exact two-link junction identity and endpoint-compression iff criterion;
- scoped no-go for the natural constant source/target/shift linear reference ansatz.

Research PR #117 then reduces the remaining selector freedom to one exact
Role-labelled diagonal overlap.

## 2. Overlap variables

At one source site \(y\), define

\[
\delta_r(y)=q_r(y)-v_r(e,y),
\]

and

\[
\Omega_{rs}(y)=q_r(y)-v_s(e,y).
\]

Then

\[
\Omega_{rs}=v_r-v_s+\delta_r.
\]

The conditional mismatch is

\[
\kappa_q(A,e;x,r)
=
A_{x,r}(v_r(e,x+r))-v_r(e,x)
+
L_{x,r}\delta_r(x+r).
\]

Thus selection of \(q\) is exactly selection of \(\delta\).

## 3. Twisted Role cocycle

The overlap satisfies the exact identity

\[
\Omega_{rs}+\Omega_{st}
=
\Omega_{rt}+\Omega_{ss}.
\]

The ordinary cocycle without \(\Omega_{ss}\) is too strong: it forces

\[
\delta_s=\Omega_{ss}=0,
\qquad q_s=v_s,
\]

which fails the generic exact translation-gauge control.

The off-diagonal overlap algebra therefore does not select the reference
section.  The genuine new datum is the diagonal

\[
\delta_r=\Omega_{rr}.
\]

## 4. PR #117 selector audit

The tested principles do not determine the diagonal:

- observer-positive local quadratic:
  exact pure gauge and pure shift require incompatible minima;
- background-only curl/harmonic penalties:
  do not change the minimizer;
- q-dependent transverse penalties:
  require choosing the missing overlap operator/target/weights;
- basepoint/path fixing:
  cannot propagate the required pure-gauge diagonal without a sourced law;
- spanning-tree fixing:
  becomes path-sensitive on curl/harmonic backgrounds unless the source is
  already path independent;
- full-affine origin covariance:
  repairs covariance but leaves every linearly covariant deformation;
- orbitwise/equivariant selection:
  preserves the known curl and harmonic deformations.

The exact rational A/B boost confirms that the failure is selection, not frame
covariance.

## 5. Exact hostile controls

A future diagonal law must reproduce:

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

For the PR #117 L=3 hostile gauge witness with B-shift cycle

\[
(3,3,-6)e_B,
\]

the required diagonal values are

\[
(15,-3,-12)e_B.
\]

They are nonconstant despite \(L=I\), so homogeneous basepoint propagation is
excluded.

### Pure affine shift

\[
\delta_r=0,\qquad \kappa=b.
\]

### Curl

The law must remove the \(z_{\rm curl}\) freedom.

### Harmonic

The law must remove the \(z_{\rm harm}\) freedom.

### Raw data

L=2 Nyquist, L=3 corner, plaquette curl, harmonic cycle and labelled holonomy
must remain visible.

## 6. Minimum new primitive

PR #117 terminal:

\[
\texttt{REFERENCE-SELECTION-REQUIRES-NEW-JUNCTION-OVERLAP-PRIMITIVE}.
\]

The next object is a Role-labelled overlap field

\[
\Omega_N(A,e,n;y;r,s)\in V_y
\]

with:

1. source-frame covariance;
2. solder-difference compatibility;
3. twisted Role cocycle;
4. a genuinely new diagonal law \(\delta_r=\Omega_{rr}\);
5. a sourced labelled path-transport equation.

The old geometry supplies the algebra around items 1–3 conditionally.  It does
not supply item 4.

## 7. Current heavy research

The active task is

\`EXP-A4D-DIAGONAL-JUNCTION-OVERLAP-LAW\`.

Highest-priority constructive route: derive a relative A/e defect which can
serve as the source of the diagonal transport equation without identifying
\(A=A(e)\).

Observer-positive minimality and basepoint/tree fixing are downstream tools
after the source law exists, not substitutes for it.

## 8. Current formalization

Two theorem-ready workers may run in parallel:

- \`WRK-A4D-ROLE-OVERLAP-TWISTED-COCYCLE\`;
- \`WRK-A4D-OBSERVER-QUADRATIC-REFERENCE-NOGO\`.

They must not invent the diagonal selector.

## 9. Finite E remains blocked

\`EXP-A4D-FINITE-GRADED-COFRAME-DRESSING\` remains BLOCKED.

The gate opens only after a usable diagonal overlap/source law lands, or after
the repository explicitly adopts the additional relative-A/e/basepoint/cycle
datum required by the next terminal.

## 10. One current question

What finite relative A/e law sources the Role-labelled diagonal overlap strongly
enough to reproduce exact pure gauge, preserve pure affine shift, and eliminate
both curl and harmonic reference freedoms while respecting labelled path
provenance?
