# A4D regular stationary sheets collapse to critical-value germs

Task: \`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE\`, Draft PR #310.  
Inputs: the exact envelope theorem in the stationary-sheet synthesis and the
source-image formulation in \`A4D_SOURCE_IMAGE_COLLAPSE.md\`.  
Status: exact finite-dimensional variational reduction; no task terminal.

## 1. Stationary components are not response classes

At fixed finite mesh, choose one genuine quotient/link coordinate chart and
write the finite action as

\[
\mathcal A_h(Q,a),\qquad
F_h(Q,a)=\partial_a\mathcal A_h(Q,a),\qquad
R_h(Q,a)=\partial_Q\mathcal A_h(Q,a).
\]

Let \(\mathcal C_\alpha(Q)\) be a connected component of the stationary fiber

\[
F_h(Q,a)=0
\]

which extends differentiably for all \(Q\) in one open metric neighborhood
\(U\).

For any differentiable path \(a(Q,s)\) inside that component,

\[
\partial_s\mathcal A_h(Q,a(Q,s))
=F_h(Q,a(Q,s))\cdot\partial_s a(Q,s)=0.
\]

Hence the action has one well-defined **critical-value germ**

\[
V_{\alpha,h}(Q)
:=\mathcal A_h(Q,a),\qquad a\in\mathcal C_\alpha(Q),
\tag{1}
\]

independent of the representative \(a\).

Differentiating (1) in \(Q\) and using \(F_h=0\) gives

\[
\boxed{
R_h(Q,a)=d_QV_{\alpha,h}(Q)
\quad\text{for every }a\in\mathcal C_\alpha(Q).
}
\tag{2}
\]

Thus every microscopic field in the same horizontally defined connected
stationary sheet has exactly the same metric response.  Connection
uniqueness, gauge identification, Fourier support and microscopic compactness
are irrelevant.

## 2. The regular response quotient

Define two regular stationary points to be equivalent when they belong to the
same horizontally defined connected component over \(U\).  Equation (2)
factors the entire metric-response map as

\[
\{\text{regular stationary connections}\}
\longrightarrow
\{\text{critical-value germs }V_{\alpha,h}\}
\overset{d_Q}{\longrightarrow}
\{\text{metric sources}\}.
\tag{3}
\]

A finer label inside one component is not response memory.

If two different components have the same critical-value germ, they are also
identified by every metric response observation.  Therefore the genuinely
minimal regular object is the germ \(V_{\alpha,h}\) itself, modulo an
irrelevant \(Q\)-independent constant if only derivatives are observed.

This is the variational form of the M1 reduction: classify critical-value
germs, not stationary representatives.

## 3. Exact relation to the source image

For a joint/source root

\[
E_K=0,\qquad E_Q=h^2\tau_h,
\]

equation (2) gives on a regular component

\[
\boxed{
h^2\tau_h=d_QV_{\alpha,h}(Q_h).
}
\tag{4}
\]

Hence the regular part of the feasible source image is

\[
\mathscr T_h^{\rm reg}(Q_h)
=
\left\{
h^{-2}d_QV_{\alpha,h}(Q_h):
\alpha\text{ a horizontal regular critical-value germ}
\right\}.
\tag{5}
\]

The #216 designated sheet contributes one such germ
\(V_{{\rm sm},h}\), with reconstructed derivative tending to
\(-G/2\).

Positive response closure on the regular domain is therefore equivalent to

\[
d_QV_{\alpha,h}(Q_h)
-
d_QV_{{\rm sm},h}(Q_h)
=o(h^2)
\tag{6}
\]

for all regular critical-value germs.  No statement about the number of
connections inside each component remains.

## 4. Why known microstructure families collapse immediately

Several previously separate-looking families are now one-line consequences
of (2).

* The flat #232/Y family is an exact connected stationary family with
  identically zero metric response.  Its connection multiplicity contributes
  no additional critical-value derivative.
* The exact constant-coframe quarter axes persist over a coframe neighborhood
  and have zero full solder/Gram Euler.  Their critical-value germs are
  locally constant, so their response is identically zero throughout that
  regular family.
* The full commuting Y-plane completion is already classified as a flat
  integrable geometry.  Its entire regular completion lies in the same flat
  response class.
* Conversely the flat #227 coupled-boost branch has nonzero metric response
  but fails to extend to the declared nonconstant warp: the exact shared-link
  current identity detects precisely the failure of a horizontal stationary
  germ.  Its flat connection-stationary existence is therefore not evidence
  for an additional regular curved source germ.

These examples are illustrations of (3), not separate assumptions of the
theorem.

## 5. What can still enlarge the source image

After (3), a new microscopic construction can matter only in one of two ways:

1. it defines a **different critical-value germ** \(V_{\alpha,h}\); or
2. it is singular/disconnected, so no common open-neighborhood stationary
   germ exists and the envelope reduction cannot be applied directly.

Thus the remaining response problem is not “all stationary microstructures”.
It is

\[
\boxed{
\text{classify or exclude singular/disconnected critical-value germs
that survive the smooth-source limit.}
}
\tag{7}
\]

A frozen joint kernel with a nonzero response moment is exactly a first-order
signal that horizontal continuation may fail.  It is not itself a new source
class.  This matches the owned deformation-map/Fredholm interpretation.

## 6. Connection with the new circle identity

The six continuous flat physical resonance circles are singular connection
directions, so (2) alone does not remove them.  The separate exact owner

\[
\texttt{A4D-IDENTITY-PHYSICAL-RESONANCE-CIRCLES-QUADRATIC-RESPONSE-NULL}
\]

now proves that their entire Hermitian quadratic source moment vanishes
anyway.  Therefore these continuous singular carriers do not enlarge the
quadratic flat source image before any nonlinear exactification question is
asked.

This leaves only singular carriers with a genuinely nonzero reduced response
cohomology as possible anomalies.

## 7. Finite-degree closure target

The matrix-link equations are exact degree at most four.  Consequently the
singular/disconnected source-image problem (7) is still the finite
degree-2/3/4 correlation problem of
\`A4D_FINITE_CURRENT_CORRELATION_MEMORY.md\`.

A final positive dual certificate can be phrased as:

\[
\boxed{
\text{every feasible singular quartic correlation has the same
critical-value derivative as }V_{{\rm sm},h},
}
\tag{8}
\]

up to the declared \(o(h^2)\) topology.

A negative terminal must produce one singular critical-value branch with an
independently fixed smooth source whose derivative stays separated from the
designated germ.

Verdict:

\[
\boxed{\texttt{REGULAR-STATIONARY-RESPONSE-QUOTIENT-IS-CRITICAL-VALUE-GERM}}
\]

and the parent task is reduced to singular/disconnected critical-value germs.

No new action, selector, gauge identification, spectral cutoff, BOOK/CORE
promotion or task-level terminal is claimed.
