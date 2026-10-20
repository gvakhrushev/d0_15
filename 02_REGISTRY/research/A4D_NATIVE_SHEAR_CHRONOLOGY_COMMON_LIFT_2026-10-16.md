# An exact shear lift puts chronology and positive Hodge heat on the same carrier

Date: 2026-10-16. Result class: exact analytic cross-owner lift and a scoped
stationarity obstruction. This is not physical admission of the full D0 action,
not a no-go for additional native terms, and not GR closure.

## Result

The chronological-feedback test on the flat trace-free shear need not use the
empty matter field. The already-owned two-step chronology has an explicit
regular 16-component state with nonzero clock `k>0`. Its actual frame lift
puts that state, the Lorentz metric, and the observer-derived positive metric
on the same joint `(q,D,b,m)` path as the positive Hodge heat calculation.
On this lift the chronological price is exactly frame-invariant, while the
positive Hodge price has a strictly positive shear derivative. The flat
Einstein comparator is zero. Thus the named `H+J` candidate is not stationary
and cannot match the flat Einstein covector on this path.

This removes the prior `k=0` domain mismatch for the chronology row on this
specific shear. It does not establish that this `H+J` candidate is the complete
physical D0 action. Any additional term `R` in a full action must have its
own same-path derivative; stationarity would require

\[
  dR[V]=-2(E_1-E_2)<-1/10000.
\]

That is a derived test on an independently owned term, not a fitted source.

## Same-carrier construction

Let

\[
 p=(\sqrt5-1)/2,\qquad a=\sqrt p,\qquad
 \eta=\operatorname{diag}(1,-1,-1,-1).
\]

Choose `c=0, s=1` in the existing whole-blank chronology family. Before
normalization its only nonzero mask coordinates are

\[
 m_0=m_{14}=-a/p,\quad m_1=m_{15}=1,\quad
 m_3=m_{13}=1/p.
\]

The owner gives `N=4/p^2`; dividing by `2/p` yields the unit-norm state
with coordinates `m_0=m_{14}=-a/2`, `m_1=m_{15}=p/2`, and
`m_3=m_{13}=1/2`. In the mask convention of that owner, the first-grade
vector is `v_eta=(p/2)e_0`, so

\[
 k_\eta=v_\eta^T\eta^{-1}v_\eta=p^2/4>0.
\]

The actual first and second recorded first grades at this angle are

\[
 w=(0,-1,0,0),\qquad w_2=(-a,1-a,0,0).
\]

Both are nonzero; the source owner proves uniform regularity of both record
steps on the full angle interval. Thus this seed is in the chronology domain,
including the second gate.

Now set

\[
 S=\operatorname{diag}(2,1/2,1,1),\quad
 F_t=\operatorname{diag}(e^t,e^{-t},1,1),\quad G_t=F_tS,
\]

and use the owner's exterior frame action on all sixteen state coordinates:

\[
 q_t=G_t\eta G_t^T
   =\operatorname{diag}(4e^{2t},-e^{-2t}/4,-1,-1),\quad
 m_t=\Lambda^*(G_t)m_\eta.
\]

Since \(\det G_t=1\), this is exactly the owned half-density frame lift.
It preserves the complete pairing normalization. The first-grade vector is
\(v_t=(pe^t,0,0,0)\), and direct substitution gives

\[
 k_t=v_t^Tq_t^{-1}v_t=p^2/4,\quad
 n_t=v_t/\sqrt{k_t}=2e^t e_0,\quad
 Q_t=-q_t+2v_tv_t^T/k_t
   =\operatorname{diag}(4e^{2t},e^{-2t}/4,1,1).
\]

The joint spatial carrier has `D_e=I, b_e=0`, with the same `q_t` at
both ends of every edge. Hence the differentiated constraint holds with
\(\dot D=0\); the path is the same volume-preserving factor shear used by the
positive-Hodge source owner. At `t=0`,
\(Q_0^{-1}\dot Q_0=\operatorname{diag}(2,-2,0,0)\), so the tangent is
trace-free in the metric pairing.

## Source comparison

The chronology owner's exact frame covariance gives

\[
 J(q_t,m_t)=J(\eta,m_\eta),\qquad dJ/dt=0.
\]

This is the complete chronological determinant with its original retained cut,
all sixteen grades, both actual gate steps, and all feedback-null directions.
It is not an inference from one scalar readout or a replacement feedback word.

For the same `Q_t`, the positive-Hodge owner computes at `beta=log(2)`

\[
 \frac{dH}{dt}=2(E_1-E_2)>1/10000\qquad (L\ge2).
\]

Therefore \(d(H+J)/dt=2(E_1-E_2)>1/10000\). The metric and links are
spatially constant with identity links, so the finite flat Einstein covector
\(\rho_0\) vanishes in all ten packed slots on this same probe. Equality with
any fixed nonzero calibration would force this nonzero derivative to vanish,
which it does not.

## Scope and next use

The result closes only the source slot for the named chronological `J` on
this common frame-lift path: chronology contributes zero, not the required
negative heat response. It supersedes the `k=0` reason for omitting chronology
from this path, but it does not bind the separate AF preparation-price record
to the same physical action, nor show that any other `R` is absent. The next
full-action candidate must provide its actual same-carrier `R`, its admitted
matter/link variations, and its derivative on this fixed lift. The source may
not be supplied by choosing `R` to cancel the heat term.

Consumed owners:

- `A4D_NATIVE_CHRONOLOGICAL_JOINT_REDUCTION.md`, SOURCE commit
  `dfaf7c8df509d5abd83fa60a185ad530feadc9b5`, blob
  `c7819ef4a5a532b2c3c1da6c9b6c69bf22c049a3` (whole-blank family, frame
  covariance (2), full candidate `H+J`);
- `A4D_NATIVE_FACTOR_IMBALANCE_REMAINDER.md`, local input blob
  `1ba94020a5031162742b52ea7981784cb3fcf312`;
- `A4D_NATIVE_POSITIVE_HEAT_RADIAL_BALANCE.md`, local input blob
  `a4fa1a6332e3836757a901cc155762339cc52013`;
- `A4D_NATIVE_FINITE_PROBE_COMPLETION.md`, local input blob
  `90179067ece3dd4959a920029d1dad306a91c5d7`.

`certificates/a4d_native_shear_chronology_common_lift_check.py` checks the
exact 16-coordinate seed normalization, the full frame/lift identities, the
derived `(k,Q)`, and the trace-free tangent. All 18 checks, including the
empty-state and frozen-matter hostile controls, pass in ordinary and optimized
Python. The machine-readable output is
[`certificates/a4d_native_shear_chronology_common_lift_results.json`](certificates/a4d_native_shear_chronology_common_lift_results.json).
The checker consumes the two-owner all-angle regularity, chronological
frame-invariance and all-`L` heat bounds as stated analytic inputs; it does
not re-prove those results or physical admission.
