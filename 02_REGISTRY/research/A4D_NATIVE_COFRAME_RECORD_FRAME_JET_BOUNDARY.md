# Native CAR record: pure coframe-frame jets are source-blind

**Exact carrier-level result, 14 October 2026.** This tests one concrete
candidate composition of the D0 full-Fock `record(G,n)` owner with the
four-return moving-preparation interface. It isolates a metric/coframe
variation from a relative matter/observer variation. It does not declare
this composition physically admitted by the core.

## Exact result

Let `record(G,n)` be the existing 16-dimensional CAR/Fock record operator.
At the positive reference pairing `G=I_4`, take the four orthonormal
observer directions `n_r=e_r`, `r=0,...,3`. The returns `U_r=record(I,e_r)`
are real orthogonal; the four reference returns are not all commuting.

For any symmetric metric tangent `V`, move the whole orthonormal frame with
the metric:

\[
G(t)=I+tV+O(t^2),\qquad n_r(t)=e_r-\tfrac t2Ve_r+O(t^2).
\]

This is realized by the frame lift `A(t)=I-tV/2+O(t^2)`, with
`G(t)=A(t)^{-T}A(t)^{-1}` and `n_r(t)=A(t)e_r`. The Fock pairing is
`S(t)=ext(G(t))`; its derivative is `dS`. To compare instruments in one
fixed Hilbert space, use the frame isometry `E(t)=ext(A(t))` and
\[
\widehat U_r(t)=E(t)^{-1}U_r(t)E(t).
\]
Since `dE=-dS/2` at the reference, its actual first variation is
\[
\delta\widehat U_r
 =\delta U_r+\tfrac12(dS\,U_r-U_r\,dS)=0
\]
for every one of the ten independent symmetric directions and all four
returns. The checker verifies the defining CAR record jet, the moving
pairing isometry identity, and all 40 fixed-frame zero jets over the exact
golden coefficient field.

Consequently, any finite-count preparation whose only metric dependence is
through these fixed-frame returns has zero first-order metric response:
each channel, the event probability, the normalized prepared state, and
the return-derived cost are stationary along this pure coframe-frame
subspace. This conclusion does not use the commuting-base theorem from v3;
the reference returns here fail that hypothesis, and the result follows
directly because their fixed-frame jets vanish.

## What the result says about the open bridge

This is a useful obstruction for the most natural covariant identification:
the existing record operator transported together with its own metric frame
does not by itself produce a metric source. A nonzero source must see a
relative degree of freedom, such as a matter/observer tangent relative to
the coframe, a link variation not removed by the same frame transport, or
another independently owned coupling. Such directions are not silently
discarded: with `G=I`, `n=e_0`, and normalized relative tangent `delta n=e_1`,
the native record operator has a nonzero fixed-pairing jet.

The result does **not** establish that the relative tangent is physically
admitted, derive its action or Ward identity, or show that its source has the
Einstein tensor's trace-free component. It also does not map the full
`LocalCoframeField`/link/matter carrier into a closed instrument law, solve a
curved native root, or close G0/#310/GR. The next proof obligation is now
sharper: derive the D0-owned relative matter/link response and its constraint
projection; the pure common-frame metric sector is already classified as
null for this candidate map.

## Reproduction

```sh
python3 02_REGISTRY/research/certificates/a4d_native_coframe_record_frame_jet_check.py
```

The adjacent receipt pins the actual record and chronology inputs. No Lean
owner, physical action, or core lifecycle state is changed.
