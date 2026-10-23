# Joint kinematic lift of the relative CAR observer source

**Exact conditional continuation, 14 October 2026.** This checks the next
arrow after the positive relative-observer jet: whether that observer tangent
can occur in the existing native 16-component (q,D,b,m) kinematic carrier.
It can. The lift is an actual whole-blank coframe orbit with the prescribed
spatial constraint and fixed positive pairing. Pulling the already-certified
v3 cost along this orbit gives a nonzero trace-free joint shear response.

This is a kinematic-admission result for the tangent. The v3 trace preparation
and cost are not thereby admitted as D0 physical matter/action. No native
ten-component metric source is selected, and no GR conclusion follows.

## The joint lift

At the reference point take `q=eta=diag(1,-1,-1,-1)`, `m0=e0+Omega` in the
literal mask coordinates, `D_e=I`, `b_e=0`, and `G=I`. For `i=1,2,3`, let
`F_i(t)` be the proper Euclidean rotation in the `(0,i)` plane with

\[
F_i(0)=I,\quad \dot F_i(0)e_0=e_i,\quad
q_i(t)=F_i(t)\eta F_i(t)^T,\quad
m_i(t)=\Lambda^*(F_i(t))m_0.
\]

The first-grade vector is `v_i(t)=F_i(t)e0`. Directly,

\[
v_i^Tq_i^{-1}v_i=1,\qquad
Q_i=-q_i+2v_iv_i^T=I,\qquad G_i=I.
\]

Thus the relative record tangent is exactly `dot n0=ei` at fixed `G`,
while the other three instrument returns remain the reference
`record(I,e_j)`. The spatial carrier is homogeneous, so
`D_e q_t D_e^T=q_s` continues to hold with `D_e=I`. The actual blank
projector and matter vector are transported by the same exterior frame
representation. The shear jet is

\[
V_i=\dot q_i(0)=2(e_0e_i^T+e_ie_0^T),\qquad
\operatorname{tr}(\eta^{-1}V_i)=0.
\]

This is a non-gauge metric/matter tangent in the declared kinematic field
chart. The proof does not add an equation identifying it with the v3 cost's
physical variation.

## Candidate cost response on the lifted directions

One exact full-Fock, four-return count recursion gives the source derivative
for `dot n0=e1`. Exact cyclic conjugacy of the three native spatial returns,
the full CAR action, trace preparation, and cost carries it to `e2` and `e3`.
In the coefficient field `a^4+a^2-1=0` the common derivative is

\[
\dot S=\frac{2Q(a)}{346943031568563}>0,
\]

with strict positivity already certified in
[`A4D_NATIVE_RELATIVE_OBSERVER_SOURCE_JET.md`](A4D_NATIVE_RELATIVE_OBSERVER_SOURCE_JET.md).
trace-free joint shears. The homogeneous metric is flat, so its geometric
`rho0` comparator is zero on these probes. These are three directional
contractions; they do not assign the source to the metric-only part of the
joint covector.
joint covector.

This does **not** establish a full ten-component comparison. A single
candidate instrument readout does not define the other seven independent
metric projections, and its trace preparation (I_{16}/16) has not been
identified with the native matter state (m). Other terms of an actual
action, including the matter and heat equations, could change the total
source. The computed mismatch is confined to the named candidate cost on
these three joint probes.

## Evidence and remaining G0 arrow

The exact checker consumes the earlier full-CAR chronology owner and the
positive relative-source receipt. It tests all three spatial shears, the
full sixteen matter jets, normalization and (Q)-preservation, the whole-
blank covariance, the identity-link spatial constraint, and the direct
record-operator jets. Its result is
[`a4d_native_relative_observer_joint_lift_results.json`](certificates/a4d_native_relative_observer_joint_lift_results.json).

The next missing datum is now sharply located: a core-owned map from the
complete native field state and its preparation to the v3 instrument's
four-return density/cost, including the remaining metric and matter
variations. Without that map, this positive shear response is a conditional
kinematic pullback, not the native stress. The native action, Ward identity,
refinement transfer, curved roots, soundness/recovery, G0, and the original
#310 terminal remain open.

Reproduce with:

```sh
python3 02_REGISTRY/research/certificates/a4d_native_relative_observer_joint_lift_check.py
```
