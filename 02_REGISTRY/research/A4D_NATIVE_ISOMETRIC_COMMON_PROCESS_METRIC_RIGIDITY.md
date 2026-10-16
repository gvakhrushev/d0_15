# Fixed-branch native updates preserve the complete record metric

2026-10-16. Cross-owner consequence for the adaptive AF engine and the
coherent price-preserving refinement. This is a scoped rigidity theorem,
not a no-go for every internal-geometric model and not an Einstein equation.

Inputs at the checked head `dfaf7c8df509d5abd83fa60a185ad530feadc9b5`:

| owner | exact input |
|---|---|
| Adaptive full-carrier update | `sources/d0_native_adaptive_engine_2026-10-16/adaptive_engine.py`, SHA-256 `1eaf0ed625c78d2779da83cf85e65bf1c1e797a3719da3b786c46cd16733b402` |
| Coherent completion and refinement | `A4D_COHERENT_COMPILATION_COST_DESCENT.md`, SHA-256 `72826a840aac882d1a93acaf0e1eba5c7e7c57cd5bfc770aff26c5824375f43c` |
| Full AF transition controls | `certificates/a4d_native_adaptive_engine_synthesis_check.py` |
| Full comparison/price controls | `certificates/a4d_coherent_compilation_cost_descent_check.py` |

## The finite-horizon theorem

Let `X` parameterize a smooth family of complete comparison isometries
`J_X` on the retained carrier. Let the actual engine selector be the sign
of its first-grade coordinate, and let the two owned branches be the full
carrier unitaries `W_+` and `W_-`. Fix `X_0` and a finite number `n` of
updates. Suppose the selected first-grade coordinate is nonzero at each of
the first `n` states on the orbit of `X_0`.

On each fixed branch the state update is linear and continuous. The finitely
many strict sign inequalities therefore remain unchanged on some open
neighborhood `U` of `X_0`. For every `X` in `U`, the same word
`s_1,...,s_n` is selected, so the common update is one fixed unitary

\[
W^{(n)}=W_{s_n}\cdots W_{s_1},\qquad
J_X^{(n)}=W^{(n)}J_X.
\]

It follows exactly, for every pair `X,Y` in `U`, that

\[
(J_Y^{(n)})^*J_X^{(n)}=J_Y^*J_X.
\tag{1}
\]

Thus every complete comparison effect and log-determinant price built from
these overlaps is unchanged, for every common fugacity in its domain. If
`P_X=J_XJ_X^*`, then `P_X^(n)=W^(n) P_X (W^(n))^*`. Consequently the
projector metric

\[
q_{\mu\nu}(X)=c\,\operatorname{Re}\operatorname{Tr}
  (\partial_\mu P_X\,\partial_\nu P_X)
\]
is also unchanged. This includes its full Hessian and all mixed parameter
directions; the conclusion is not limited to the value at one state.

The argument permits a different selected sign at every tick. It only
requires that, for each finite horizon and each base point, the finite word
stay strict on a neighborhood. It makes no uniform-in-`n` claim and says
nothing at a selector zero, where the engine branch is undefined.

## Refinement does not add resolution under the owned comparison

The coherent compiler's completed comparison isometry is

\[
J_{\mathrm{comp},X}=I(J_X\otimes v),\qquad I^*I=1,
\]
with a fixed auxiliary blank `v` and fixed code embedding `I`. Its owner
proves `J_comp,Y^* J_comp,X = J_Y^* J_X` for all compared preparations,
including their derivatives. The AF level shift adds the field-independent
code cost `k`; its derivative and metric Hessian are zero. Composing this
refinement with a finite fixed-branch engine word preserves (1) whenever
that engine word is intertwined by the same isometric code map on the
compared family. This intertwining is a condition on a common process, not a
claim that the current owners have admitted it at every AF level.

Under that common-process/intertwining hypothesis, the unitary update and
coherent isometric refinement can change the full state and retain additional
history coordinates, but cannot increase distinguishability or expand the
metric defined by that same complete comparison. Whether the actual moving
AF process satisfies this cross-level hypothesis remains open. This
identifies a specific limit of the route: archive growth and a larger carrier
do not by themselves produce geometric refinement.

## What this does and does not decide

This theorem applies only when the same branch word acts on every state in
the complete comparison family and when the same price/metric readout is
used. A field-dependent frame update `W(F(X))`, a changed comparator,
partial observation, or a non-isometric record transition could change the
readout. Each would need its own admitted owner and its complete derivative;
terms such as (W^*dW) cannot be dropped. The theorem neither supplies such
an update nor rules out every possible one.

The exact finite AF gate identities and the coherent refinement identity
are covered by the two cited controls. Their analytic proofs are the fixed
unitary cancellation and (7) of the coherent-compilation owner. No new
certificate, selector, action, primitive admission, Lean declaration or
physical claim is introduced. The #310 common moving-field update, its ten
transverse equations, full native source, exact roots and refinement-uniform
GR terminal remain open.
