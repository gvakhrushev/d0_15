# A4D regular stationary sheets collapse to critical-value germs

Task: \`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE\`, Draft PR #310.  
Inputs: the exact envelope theorem in the stationary-sheet synthesis and the
source-image formulation in \`A4D_SOURCE_IMAGE_COLLAPSE.md\`.  
Status: conditional envelope theorem within each horizontal stationary
component; distinct regular germs and singular roots remain in the full
source-image problem. No task terminal.

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

which extends differentiably for all \(Q\) in one open neighborhood
\(U\) of the **full finite metric-coordinate space**, with fibers joined
by differentiable stationary paths. A family defined only at fixed Q or
only over constant coframes does not meet this full-metric hypothesis.

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

The #216 smooth comparator has reconstructed response tending to
\(-G/2\). Its connection residual is super-algebraically small; this does
not by itself make it an exact stationary germ. Identifying it, up to the
required error, with a derivative \(d_QV_{{\rm sm},h}\) requires a
separate exact-stationary-germ and response-comparison theorem. The
H-NORMAL-RESCUE contract is one sufficient route, explicitly OPEN in that
owner; it is not asserted to be the only possible route.

Positive response closure on the regular domain is therefore equivalent to

\[
d_QV_{\alpha,h}(Q_h)
-
E_Q(Q_h,K_h^{\rm sm})
=o_{\mathrm{owner},1}(h^2)
\tag{6}
\]

for every admissible regular-germ sequence whose source is the exact
sampling of one fixed smooth tau. Equation (2) does not compare different
germs. If an exact designated germ is supplied with sufficiently small
response error, it may replace the comparator in (6); its existence is not
a conclusion of the envelope theorem.

## 4. Scope of the known response-null controls

The flat #232/Y family has identically zero full metric response by its
literal Euler certificate. The same is true of the constant-coframe quarter
axes on their declared constant-coframe parameter domain. These facts do
not prove that either family extends over an open neighborhood of all
finite metric coordinates. Equation (2), when used only on a restricted
parameter domain, identifies only the response tested along that domain.

The commuting Y-plane completion is separately classified as flat
integrable geometry. The flat #227 coupled-boost branch has nonzero metric
response and fails its proposed extension to the declared nonconstant warp
by the exact shared-link current identity. Failure of that one extension
neither excludes other regular critical-value germs nor classifies all
singular stationary roots on a varying background.

These scoped results remain valid independently of the envelope theorem.
No assertion that all regular branches have equal response follows.

## 5. Both distinct regular germs and singular roots remain

After (3), a microscopic construction can still enlarge the source image
by defining a **different regular critical-value germ**, or by producing a
stationary root without the horizontal continuation required in Section 1.
Disconnected regular components can each possess such a germ; disconnected
is not synonymous with singular.

The full response question remains

\[
\boxed{
\text{control all distinct regular germs and all remaining singular roots
that realize the prescribed fixed smooth source.}
}
\tag{7}
\]

The envelope theorem removes labels *inside* an eligible component. It
does not remove that component from the comparison with the designated
response, and it supplies no bound between different components.

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

This excludes these particular quadratic flat carriers. Distinct regular
germs, nonlinear completions and other singular roots are still subject to
the full fixed-source test in (7).

## 7. What the local degree theorem does and does not imply

The matrix-link equations have degree at most four and a bounded local
stencil. On a varying coframe their coefficients depend on position. The
corrected `A4D_FINITE_CURRENT_CORRELATION_MEMORY.md` therefore retains
coefficient-weighted correlations or pointwise moment fields; it does not
provide a fixed-size globally exact realizability quotient.

A positive result must compare the actual response of **all** admissible
fixed-source roots, including distinct regular germs and singular roots,
with the smooth comparator in the original owner norm. A negative result
may come from either a distinct regular germ or a singular root, but must
produce an admissible refining sequence with one background and one smooth
source fixed before the links. A singular witness is not required.

Verdict:

\[
\boxed{\texttt{REGULAR-STATIONARY-RESPONSE-QUOTIENT-IS-CRITICAL-VALUE-GERM}}
\]

This is a conditional within-component quotient. It neither identifies
all regular germs with the designated comparator nor reduces the parent
task to singular/disconnected germs. The full attempt and its failed
arrows are recorded in
[A4D_SOURCE_IMAGE_END_TO_END_ATTEMPT.md](A4D_SOURCE_IMAGE_END_TO_END_ATTEMPT.md).

No new action, selector, gauge identification, spectral cutoff, BOOK/CORE
promotion or task-level terminal is claimed.
