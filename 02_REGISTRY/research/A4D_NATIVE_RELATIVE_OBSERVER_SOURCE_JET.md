# Exact source jet from a relative native CAR observer rotation

**Candidate-composition result, 14 October 2026.** This is the next test
after the pure-frame null result in
[`A4D_NATIVE_COFRAME_RECORD_FRAME_JET_BOUNDARY.md`](A4D_NATIVE_COFRAME_RECORD_FRAME_JET_BOUNDARY.md).
It uses the existing full-Fock `record(G,n)` operator inside the v3
four-return count instrument and differentiates the complete event-conditioned
cost. It establishes a nonzero source along one normalized relative observer
direction. It does not prove that the core admits this four-return
identification as its physical instrument.

## The actual D0 record family and one fixed variation

Work on the 16-dimensional full CAR/Fock carrier with `G=I_4` and the four
unit observers `n_r=e_r`. Set each instrument return to the actual native
operator
\[
U_r=\operatorname{record}(I_4,e_r),\quad r=0,1,2,3.
\]
They are real orthogonal, and the reference family includes noncommuting
pairs. Move only the first observer by the single normalized path
\[
n_0(t)=\cos(t)e_0+\sin(t)e_1,
\]
so \(\dot n_0(0)=e_1\); keep the other three returns fixed. The record
owner's actual `dU` formula gives the return tangent. This is not an
endpoint-fitted tangent and it obeys the unit-observer constraint.

Use the v3 golden count instrument with \(p=(\sqrt5-1)/2\), \(a=\sqrt p\),
four returns, trace preparation \(I_{16}/16\), three rounds, and the fixed
event \(1\le k\le2\). Its branches are
\[
\Phi_0(X)=\frac14\sum_r(pI+p^2U_r)X(pI+p^2U_r)^T,\qquad
\Phi_1(X)=\frac{p^3}{4}\sum_r(U_r-I)X(U_r-I)^T.
\]
The checker propagates both every count state and its actual first variation
through the full recursion. It also differentiates the event probability
and the return cost
\[
\Delta=\sum_r(U_r-I)^T(U_r-I),\qquad
S(t)=\operatorname{Tr}(\Delta(t)\rho_A(t)).
\]
Thus the answer includes the movement of the prepared density and the
normalization of the selected event. The reference returns do not commute;
the v3 commuting-reference derivative theorem is not invoked. This result
comes from direct finite matrix recursion.

## Exact outcome

In the exact coefficient field \(a^2=p\), \(p^2+p=1\), the event
probability, its derivative, the reference cost, and the full source jet are
\[
\begin{aligned}
Z_A&=-102ap+63a+\frac{255}{8}p-\frac{309}{16},\\
\dot Z_A&=\frac{221}{16}-\frac{179}{8}p,\\
S(0)&=\frac{9856ap-6084a+8044p-4990}
              {544ap-336a-170p+103},\\
\dot S(0)&=\frac{-17097116ap+10566598a+9221682p-5699312}
 {1233792ap-762528a+3019248p-1865985}.
\end{aligned}
\]
The exact positive-root brackets \(309/500<p<619/1000\) and
\(393/500<a<787/1000\) give \(Z_A>53661/250000>0\). Reducing the source
jet to the degree-four field \(a^4+a^2-1=0\) gives
\[
\dot S(0)=\frac{2Q(a)}{346943031568563},\quad
Q(a)=418298977134234a^3+47136853411765a^2
-266996949536729a-17948253838120.
\]
Termwise rational bounds on \(393/500<a<787/1000\) give
\[
Q(a)>\frac{260432886291208272219}{62500000}>0,
\]
so this candidate source jet is strictly positive, not merely numerically
nonzero. Freezing the prepared density or omitting the event-normalization
term produces a different result; both substitutions are rejected by the
certificate.

## Meaning and remaining proof

Together with the preceding pure-frame result, this locates a response in a
relative observer/matter direction for this specific native-record
composition: transporting the entire metric frame gives zero metric jet,
while rotating one observer relative to the other returns gives a positive
prepared-cost jet. This is the first nonzero full count-instrument response
computed from the D0 CAR record owner rather than from freely chosen unitary
generators.

It remains conditional on identifying these four basis-observer records as
the physical instrument returns. The calculation has not established the
admission of that identification, derived its source from an independently
owned D0 action, projected it onto the constrained ten-component metric
cotangent, matched it to \(\rho_0\) or the Einstein tensor, or proved its
Ward identity, refinement transfer, curved-root recovery, or GR. The next
critical test is whether the D0 joint coframe/link/matter constraints
actually admit this relative tangent and what its ten-component metric
projection is.

Reproduce with:

```sh
python3 02_REGISTRY/research/certificates/a4d_native_relative_observer_source_jet_check.py
```

The exact checker pins the CAR record owner and the submitted v3 source.
No Lean owner or physical lifecycle state is changed.
