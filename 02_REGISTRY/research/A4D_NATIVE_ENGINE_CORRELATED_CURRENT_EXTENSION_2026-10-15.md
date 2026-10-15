# A current-active invariant sector of the closed record engine

Research continuation, 2026-10-15. This note binds the existing closed-record
executor to the existing full-CAR current readout on an alternative exact
initial state. It is a scoped cross-owner construction; it adds no physical
selector, admission rule or CORE claim.

## Exact state and current

Keep the engine's existing golden coefficients (a,p>0),

\[
a^2=p,\qquad p+p^2=1,
\]

and define the state in occupation-mask order by

\[
m_0=-2ap,\qquad m_1=2p-1,\qquad m_{13}=m_{14}=1,
\]

with all other twelve components zero. This is a valid exact `State` of the
existing executor and satisfies its actual six-zero guard
`m2=m3=m4=m5=m8=m9=0`. Its lower pair is the engine's already proved band
state (A=(-2ap,2p-1)), so the executor sign is defined and its lower pair
alternates between the existing A and B states for all ticks.

The correlated-current owner's literal full-CAR readout has the following
symbolically checked form on either lower band, for arbitrary real values of
the four retained coordinates (m_{12},m_{13},m_{14},m_{15}):

\[
J=e_0+\frac{2\omega}{N}e_1,\qquad
\omega=m_{12}m_{15}-m_{13}m_{14},\qquad
N=1+m_{12}^2+m_{13}^2+m_{14}^2+m_{15}^2.
\]

For the displayed state, (omega=-1) and (N=3), hence

\[
J_0=e_0-\tfrac23e_1.
\]

This current comes from the existing full CAR matrices, not a newly chosen
bilinear. The exact checker verifies all four current components as symbolic
identities on both A and B, then compares the literal current implementation
against the formula on the first nine states of the actual engine orbit.

## All-time extension

Let (u=(m_{12},m_{13})) and (v=(m_{14},m_{15})). The engine's actual
degree-two/three gate applies to both pairs the same matrix

\[
H_\sigma=\begin{pmatrix}a&-\sigma p\\-\sigma p&-a\end{pmatrix},
\qquad \sigma=\operatorname{sign}(m_1)\in\{-1,1\}.
\]

The identities above give (H_\sigma^T H_\sigma=I) and
\(\det H_\sigma=-a^2-p^2=-1\). Thus each pair norm stays one and
\(\omega_{n+1}=-\omega_n\). Since the exact A/B lower pair also has norm
one, the full state norm is always (N=3). Consequently the current is

\[
J_n=e_0+(-1)^{n+1}\tfrac23e_1,
\qquad \eta(J_n,J_n)=\tfrac59>0
\]

for every tick. This is an invariant-sector proof: the six guarded
coordinates and the other four unused high coordinates remain zero, the
existing A/B lemma keeps the executor sign defined, and the generic Lean
kernel proves the high-pair norm and minor identities for either gate sign.
The exact executable regression additionally checks 128 transitions.

More generally, replacing both initial high amplitudes by the same nonzero
coefficient (s) gives

\[
\omega_n=(-1)^{n+1}s^2,\quad N=1+2s^2,\quad
1-\left(\frac{2s^2}{1+2s^2}\right)^2
=\frac{1+4s^2}{(1+2s^2)^2}>0.
\]

The executable uses the existing exact (\mathbb Z[a]) coefficient type;
the main witness (s=1) and the regression witness (s=2) lie in that type.
The displayed real-amplitude formula is the algebraic extension of the same
block identities, not a claim that arbitrary real values are encoded as
finite engine coefficients.

The current's existing observer-pairing chart parameter
\(K=(1+r)/(1-r)\), (r=J_1/J_0\), alternates from (K=1/5) to (K=5) at
unit amplitude. Under the real-amplitude perturbation at the odd tick,
\(K(s)=1+4s^2\), so (K'(1)=8\). This pins a concrete entry point for the
existing heat functional, whose response on this sector is derived below.

## Exact boundary and next proof

For the odd-tick amplitude curve, \(K(s)=1+4s^2\) and \(K'(1)=8\). The
existing heat formula gives \(H'(1)=-4\,\mathbb E[A-B/25]\). This sign is
positive for every periodic size \(L\ge2\), including every required
\(L\in4\mathbb N\).

At \(K=5\), write
\(\lambda=5A/2+B/10=12A/5+(A+B)/10\), and let
\(d(k)=\min(k,L-k)\), \(l=k_0-k_1\pmod L\). The existing sine estimates
give \(16d(k)^2\le |z(k)|^2<64d(k)^2\). For off-diagonal modes
\(d(l)\ge1\), \(A-B/25\le A<64d(l)^2\), while

\[
\lambda\ge(192/5)d(l)^2+(16/5)(d(k_0)^2+d(k_1)^2).
\]

Since \(d^2\le2^{d^2}\), the factor
\(d(l)^2 2^{-(192/5)d(l)^2}\) is at most \(2^{-37}\). Also
\(\sum_k 2^{-(16/5)d(k)^2}\le1+2\sum_{n\ge1}2^{-3n}=9/7\). Therefore
all positive off-diagonal contributions total less than
\(64(9/7)^2 2^{-37}<2^{-30}\).

The diagonal mode \((k_0,k_1)=(1,1)\) is strictly negative: there
\(B=4|z(1)|^2\ge64\), and \(\lambda=B/10<128/5<26\), so its magnitude
exceeds \((64/25)2^{-26}=1/(25\cdot2^{20})>2^{-30}\). Other diagonal
modes are nonpositive, and negative off-diagonal modes only lower the sum.
The full weighted numerator is negative, proving \(H'(1)>0\) for every
\(L\ge2\). Separately, the checker expands all 16 modes at \(L=4\) into an
exact polynomial in \(x=2^{-1/5}\) and certifies its sign with rational
bounds; the uniform estimate is analytic and does not extrapolate those 16
terms.

On the same observer interface, the already-owned two-equal-current-tick
feedback pencil is \((1-4zp^3)^4\), independent of \(s\). Its logarithmic
feedback-price derivative is therefore zero, so the combined
current-observer heat-plus-feedback derivative remains strictly positive at
every \(L\ge2\) if all other terms are held fixed. This is a statement about
that named readout functional; the transition comparison below shows it is
not the executor's own one-step operator on any nonzero member of this
amplitude family.

This state is not on the original whole-blank seed orbit. That orbit has
\(\omega=0\) and stays current-null because the same gates only change the
minor's sign; the positive-current state starts with a nonzero retained
correlation. Therefore the result establishes an active-current invariant
sector inside the executor's accepted state domain, not a mechanism selecting
that initial correlation from the whole blank.

The two owners still do not define one common physical observer transition:
the executor gate uses the state-selected axis
\(\operatorname{sign}(m_1)e_0\), while the CAR readout above has a tilted
timelike direction. This can be tested directly on the displayed witness:
apply the existing current-owner operator \(U(h_J,n_J)\) and compare it with
the executor's actual \(U_{+e_0}\) output. Across the real-amplitude family,
the exact mask-13 residual is
\((U(h_J,n_J)m(s)-U_{+e_0}m(s))_{13}=-4as^3\). Since \(a>0\), literal
common-step identification within this family forces \(s=0\), where the
spatial current also vanishes. This is a route-specific NO-GO for matching
these two transitions at fixed \(q=\eta\). It does not exclude another
state family, an already-owned metric-changing operation, or a larger
admitted class. Physical admission of this initial sector and transfer of
its heat, price, metric variation or source/Ward identity remain open.

The next load-bearing question is whether an already-owned metric/link
transition can make this nonzero heat readout and the executor's actual state
transition part of one admitted action. The fixed-metric direct match is now
ruled out on the entire active-amplitude family. Any continuation has to use
an existing metric-changing owner and its genuine tangent, then differentiate
the complete price there. A fitted metric map, heat term or source would evade
the obstruction rather than solve it.

The Lean capsule
[`a4d_native_engine_correlated_current_extension.lean`](certificates/a4d_native_engine_correlated_current_extension.lean)
proves generic gate/minor and heat-sign arithmetic kernels with standard
axioms only. The exact cross-owner checker reports its source SHAs, source Git
blobs, 845 exact controls, hostile null-sector/domain controls, the exact
L=4 mode polynomial, the current-step mismatch, and a 128-step regression in
[`a4d_native_engine_correlated_current_extension_results.json`](certificates/a4d_native_engine_correlated_current_extension_results.json).
