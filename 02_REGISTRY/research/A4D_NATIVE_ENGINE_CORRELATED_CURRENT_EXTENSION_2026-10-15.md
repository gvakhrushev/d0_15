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

The existing conditional endpoint-isometry update in
[`A4D_NATIVE_RECORD_METRIC_CHRONOLOGY.md`](A4D_NATIVE_RECORD_METRIC_CHRONOLOGY.md)
does not repair this mismatch on the present engine orbit. Its input first
grade alternates between \((2p-1)e_0\) and \(a(4p-3)e_0\), both nonzero.
Consequently its owned positive pairing
\(Q=-q+2vv^T/(v^Tq^{-1}v)\) is exactly \(I_4\), and the solved output update
\(q_+=-Q+2ww^T/(w^TQ^{-1}w)\) is also exactly \(\eta\), since the engine
output first grade remains a nonzero multiple of \(e_0\). The actual engine
output induces the same positive pairing \(Q_+=I_4\). The actual engine gate
is orthogonal for the full exterior pairing \(C_*(I_4)\), so the conditional
endpoint-isometry hypothesis is satisfied at each of 128 replayed ticks.
Feeding this already-owned updater to this orbit therefore leaves the
Lorentz metric fixed and the fixed-\(q\) operator mismatch intact. This closes
only that named conditional update as a rescue; it does not establish its
physical admission or exclude other metric-changing owners.

## A direct current-rest coframe change also leaves the executor domain

There is a natural next attempt: use the existing full exterior frame lift to
put the active current at rest, then run the unchanged axis executor in that
frame. For the amplitude family, the initial current is
\(J_s=e_0-2s^2(1+2s^2)^{-1}e_1\). The Lorentz boost

\[
\Lambda_s=\begin{pmatrix}\gamma_s&b_s\\b_s&\gamma_s\end{pmatrix}
\oplus I_2,\qquad
\gamma_s=\frac{1+2s^2}{\sqrt{1+4s^2}},\quad
b_s=\frac{2s^2}{\sqrt{1+4s^2}},
\]

satisfies \(\Lambda_s\eta\Lambda_s^T=\eta\) and sends \(J_s\) to
\(\sqrt{1+4s^2}(1+2s^2)^{-1}e_0\). The existing exterior lift
\(\wedge\Lambda_s\) sends the CAR current to this rest direction. However,
on the grade-one native component \((2p-1)e_0\), it creates the forbidden
executor coordinate

\[
(\wedge\Lambda_s m_s)_2=
\frac{2s^2(2p-1)}{\sqrt{1+4s^2}}.
\]

Because \(2p-1=\sqrt5-2\ne0\), this coordinate is nonzero for every
\(s\ne0\), so the transformed state violates the actual six-zero executor
guard at mask 2. At \(s=0\), the boost is the identity and the guard survives,
but the spatial current and the heat-amplitude response vanish. The exact
checker verifies the full current rest alignment, Lorentz identity, forbidden
coordinate, stored \(s=1\) witness, and the zero-amplitude hostile control,
binding the existing CAR and exterior-frame sources. This explicit boost
witness is then strengthened below to every common linear GL frame lift; it
leaves nonlinear preparations, genuine interactions and a larger admitted
executor domain open.

The obstruction is independent of the chosen rest boost or a following
spatial rotation. Let \(L\) be any Lorentz change of orthonormal frame that
puts \(J_s=e_0+r_s e_1\) at rest, with \(r_s\ne0\). If the transformed
native first grade still obeyed the executor guard, then \(Le_0=d e_0\).
Lorentz normalization gives \(d^2=1\), and orthogonality forces the time
component of \(Le_1\) to vanish. Since \(Le_1\) is a unit spacelike vector,
its spatial part has squared Euclidean norm one. Thus the spatial part of
\(LJ_s=d e_0+r_sLe_1\) has squared norm \(r_s^2>0\), contradicting rest
alignment. So every metric-preserving Lorentz frame that aligns this current
necessarily violates the engine's first-grade support guard.

The existing full-CAR owner proves that the current transforms as a vector under a common
invertible frame change when the metric, observer reference and matter are all
transported ([source, section 3](A4D_NATIVE_CORRELATED_CURRENT_TRANSITION.md#3-a-current-using-the-actual-full-car-correlations)). This gives a stronger result for the proposed current-rest repair. On the active family the native first grade is
\((2p-1)e_0\), while \(J_s=e_0+r_s e_1\) with \(r_s\ne0\). A common
\(E\in GL(4)\) that keeps the unchanged executor guard must send the first
grade into \(\mathbb R e_0\); putting the current at rest also requires
\(EJ_s\in\mathbb R e_0\). Since the two input vectors are independent and
\(E\) is invertible, their images cannot both lie on that one-dimensional
axis. In coordinates, those two requirements force both the first and second
columns of \(E\) to be multiples of \(e_0\), hence \(\det E=0\). The new
abstract Lean theorem and exact symbolic control certify this implication for
every nonzero \(r_s\), not only for Lorentz boosts. It closes all common linear
GL frame/coframe lifts that preserve the executor's existing guard while
rest-aligning this current. Nonlinear state preparations, interaction-level
metric changes, and changes to the executor itself remain outside the result
and require their own owner.

## Census of existing metric, heat, and recording owners

Two metric/heat candidate owners now replay inside the same exact packet. The
record-metric chronology owner derives a next metric only under
full endpoint-pairing isometry. Its certificate leaves physical admission
open, and the conditional update gives \(q_+=\eta\) on all 128 tested engine
steps. The independent soldered-heat owner proves ten homogeneous heat
components and the full raw-solder/metric tangent, but its source explicitly
contains no on-shell equation, leaves the bootstrap heat identification open,
and supplies no state-to-state metric transition. Their exact checkers pass:
469 chronology controls with 18 mutations, and 405 soldered-heat controls with
16 mutations. These results classify the two inspected candidates; they do
not prove that no other owner exists in the repository. Within these owners,
the existing record interaction must still be coupled to the metric/current
transition.

That recording interaction already has a separate owner: the Fibonacci AF
construction builds its full regular-representation price with three AF
inclusions (four levels including the input), and its exact replay passes
21,396 controls with 11 mathematical mutations. Its own certificate leaves
physical preparation/refinement admission and the metric/link source/Ward/GR
open; the owner says the AF tower is not yet welded to the Role-phase
physical mesh and supplies no independently admitted \((q,D,b,m)\) binding.
This does not show that a bridge is impossible. It makes the next target
specific: construct and verify that bridge to the joint geometric state, the
active CAR current and the accepted executor step, or prove a scoped
obstruction for this declared AF representation class. These three metric,
heat and AF owners do not establish that composite physical transition.

The separate full-CAR record binding realizes the literal golden record gate
on all sixteen exterior components, with its complete two-return price; its
checker passes 169 exact controls and 15 mathematical mutations. The owner
also gives explicit fixed-\(q\) inputs whose gate outputs lose timelike grade
one or the top-grade orientation, so the unrestricted update does not preserve
that domain. But the active executor has a sharper positive match: at
\(q=\eta\), for either sign of its collinear first grade and either sign of
the top-grade volume, the full CAR gate matrix is exactly the executor's
\(U_{\pm}\). On the stored active orbit the top grade is absent at tick 0,
appears at tick 1, and this operator identity holds on all 128 tested later
steps. Yet none of those 128 states lies in the full-CAR owner's fresh-blank
plane. The exact checker records all three facts. Thus the operator is already
shared on this orbit, but those states are not fresh-blank inputs. The owner
replays alone did not identify a preparation bridge. The next section now
supplies an exact first-level AF-to-CAR map and shows the canonical AF trace
seed produce a timelike/top-grade CAR component after one record. Its
all-level physical admission, joint metric transition and source remain open.
The active fixed-carrier orbit and this growing-carrier construction are
different state sequences.

## First AF-to-Lorentz-to-CAR bridge

The first nontrivial Fibonacci algebra is

\[
 A_1=M_2(\mathbb C)\oplus\mathbb C,
 \qquad \iota_1(X,y)=(\operatorname{diag}(X,y),X)
       \in M_3(\mathbb C)\oplus M_2(\mathbb C).
\]

Its Hermitian part has a canonical four-real-dimensional carrier. Write
\[
 H(t,x,y,z)=\begin{pmatrix}t+z&x-iy\\x+iy&t-z\end{pmatrix}.
\]
Then \(\det H=t^2-x^2-y^2-z^2\), and the positive semidefinite cone is
\(t\ge\sqrt{x^2+y^2+z^2}\). The identity is the future unit vector; the
traceless Pauli matrices span its three-dimensional negative space, with
orientation fixed by their cyclic commutator. Thus the Lorentz form, its
future cone and an orientation arise from the actual \(M_2\) block's
algebraic structure. This is a carrier construction, not yet a spacetime
field or a physical interpretation of the scalar block.

For \(A\in SL(2,\mathbb C)\), congruence \(X\mapsto AXA^*\) preserves the
determinant and positive cone. The actual AF inclusion intertwines it with
\((Z,W)\mapsto((A\oplus1)Z(A\oplus1)^*,AWA^*)\): the old scalar \(y\) is
retained as the added diagonal entry, while the old \(X\) is copied into the
second block. The limitation is exact: a noncompact boost does not preserve
the canonical AF trace. For
\(A=\begin{psmallmatrix}5/3&4/3\\4/3&5/3\end{psmallmatrix}\),
\(\det A=1\), but \(\operatorname{Tr}(A I A^*)-\operatorname{Tr}(I)=64/9\).
So this is a Lorentzian carrier transport compatible with refinement, not a
trace-preserving physical symmetry or an admitted metric update.

The same first AF level gives a positive exact overlap with the full CAR
owner. Its actual three-inclusion recording frame at base level 1 has a
20-dimensional \(\mathbb C^4\otimes\mathcal H_1\) range inside the
89-dimensional \(\mathcal H_4\). The \(M_2\)-GNS summand supplies a canonical
16-dimensional reducing sector. If \(\chi\) is the normalized Pauli basis,
\(T\) the existing four-coordinate change of basis, and \(\mathcal B\) the
owned full-exterior frame, the map
\[
 \Psi=V_{1,M_2}(T\otimes\chi)\mathcal B^*
\]
is isometric and intertwines, exactly, the AF and CAR record gate, price cut
and fresh-blank projection. The remaining scalar \(M_1\) block is a separate
four-dimensional channel; together these two sectors exhaust all 20 frame
directions. The other 69 directions of \(\mathcal H_4\) remain in the owner's
identity complement, with no cut or blank directions discarded.

This correspondence also acts on the actual normalized GNS vector of the
full canonical AF trace, without conditioning away the scalar sector. At
level 1,
\[
 \tau_1(X,y)=p^2\operatorname{Tr}X+p^3y,\qquad
 e_2=\operatorname{vec}(I_2)/\sqrt2,\quad
 \Omega_1=\sqrt2p\,e_2\;\oplus\;ap,
 \quad 2p^2+p^3=1.
\]
Its AF inclusion is in the fresh-blank plane. The CAR reducing component of
that seed is \(p(|\varnothing\rangle+|123\rangle)\), with squared norm
\(2p^2\); the orthogonal scalar channel of squared norm \(p^3\) is retained.
After one actual AF recording application, the CAR component is
\[
 ap(|\varnothing\rangle+|123\rangle)
 +p^2(|0\rangle-|0123\rangle).
\]
It therefore has a nonzero timelike first-grade component and nonzero
top-grade orientation, generated from the full AF trace seed by the existing
record operator. The certificate does not turn AF depth into physical time,
or close the subsequent joint metric/link/matter transition. It identifies a
finite first-stage construction for the seed/preparation arrow that the
active fixed-carrier executor orbit did not provide.

The same owned identity can be iterated without resetting or dropping the
old state. At record depth \(k\), let \(x_k\in\mathcal H_{1+3k}\) be the
full AF vector and compose the canonical three-level inclusion \(J_k\) with
the owned recording operator \(W_k\):
\[
 x_{k+1}=W_kJ_kx_k=aJ_kx_k+p e_k,
 \qquad e_k=V_{3,k}x_k\perp J_k\mathcal H_{1+3k},
 \qquad \|e_k\|=\|x_k\|.
\]
Because \(a^2=p\), \(p+p^2=1\), and the new-detail direction is orthogonal
to the complete prior carrier, every step preserves total norm and adds a
nonzero record of squared norm \(p^2\). Later inclusions retain earlier
records, and the newly added detail is orthogonal to all of them. After \(k\)
steps the orthogonal components have squared weights
\[
 \underbrace{p^k}_{\text{retained base carrier}},\qquad
 \underbrace{p^2,p^3,\ldots,p^{k+1}}_{\text{successive recorded details}},
 \qquad p^k+\sum_{j=2}^{k+1}p^j=1.
\]
The certificate executes two steps on the entire level-1 canonical trace
vector, including both its \(M_2\) and scalar sectors: at level 7 the weights
are exactly \(p^2,p^3,p^2\), with the second detail orthogonal to the full
first-step state. The carrier dimensions along this sequence are
\(\dim\mathcal H_1=5\), \(\dim\mathcal H_4=89\), and
\(\dim\mathcal H_7=1597\). This is an exact growing-resolution, retained-
memory process built from the existing refinement and record owners. It
provides a candidate operational tick because every step changes the state
in a new orthogonal direction; it does not identify that tick with physical
proper time or those Hilbert dimensions with spatial volume.

## The current heat does not descend to the metric/link fiber

The attached strategy's next test asks whether the additional heat block can
be an owner-derived function \(F(q,D)\) on the metric carrier constraint.
On the present sector take \(q_s=q_t=\eta\) and \(D=I_4\). Then
\(Dq_tD^T=q_s\) holds identically, the homogeneous auxiliary field is
\(b=0\), and the matter family \(m_s\) varies only in masks 13 and 14.
After one actual engine step its observer parameter
is

\[
K(s)=\frac{1+r(s)}{1-r(s)}=1+4s^2,
\qquad K'(1)=8.
\]

The existing current-defined heat therefore has a nonzero vertical
derivative at fixed \((q,D)\): the all-\(L\) estimate above gives
\(H'(1)>0\) for every \(L\ge2\). A function \(F(q,D)\) has zero derivative
along this fixed-\((q,D)\) matter tangent, so it cannot represent this
current heat on a real neighborhood of the active state. The finite
coefficient engine also accepts \(s=1\) and \(s=2\), with post-step
parameters \(K=5\) and \(K=17\), respectively; this finite pair confirms
the same fiber has distinct current-observer data, while the derivative
claim uses the stated real-state extension. Thus the metric carrier equation
alone does not supply the required preparation function. To make the heat a
function of \((q,D)\), an existing preparation owner must constrain matter
along this fiber. No such constraint is derived here. This is a no-go only
for the current heat on this open family with the stated carrier constraint;
it does not rule out another coupled heat block or a separately proved
matter-preparation law.

This vertical variation is present in the currently owned carrier, rather
than added for the counterexample: the joint-field quotient and constrained-
price source retain all affine/matter directions alongside the metric/link
constraint. They do not give a preparation equation that relates these
matter coordinates to \((q,D)\). Their exact source capsules and ledgers are
pinned by the checker. The nonzero heat jet therefore identifies the precise
missing arrow: a preparation owner must restrict the matter fiber before
this heat can descend to a metric/link function.

## Conditional test of the proposed three-term price

The supplied strategy text proposes
\(S_{\mathrm{coupled}}=S_{\mathrm{scene}}+S_{\mathrm{feedback}}+
S_{\mathrm{heat}}\). The repository currently proves these pieces in
separate owners and does not identify them as one common admitted action. If
that additive identity is assumed at shared fixed \(\beta=\log 2\) and
fugacity \(z\), with the scene remaining in its owned binary passport class,
then the same fixed-\((q,D,b)\) matter tangent has:

* zero scene-price derivative, by the exact constant-price theorem for every
  binary scene satisfying the owned dense passport;
* zero current two-tick feedback derivative, because its existing pencil is
  \((1-4zp^3)^4\), independent of \(s\);
* strictly positive current-heat derivative, \(H'(1)>0\), for every
  \(L\ge2\).

Thus those three terms alone have \(dS_{\mathrm{coupled}}/ds>0\) and cannot
be stationary on this allowed matter direction. Any stationary completion
must either derive a preparation constraint excluding this direction or add
an independently owned coupled term whose derivative cancels it. The second
option is not present in the supplied three-term identity. Since the
repository has not yet proved that the three separate readouts form one
common \(S_{\mathrm{coupled}}\), this sum result is explicitly conditional;
it is not promoted to a native on-shell obstruction. The exact checker replays
the shared-scene (2894 controls), constrained-price (528 controls) and
joint-field-quotient (41 controls, 51 D0 pins) certificates before recording
this conditional derivative split.

The next load-bearing question is whether an already-owned metric/link
transition can make this nonzero heat readout and the executor's actual state
transition part of one admitted action. The fixed-metric direct match is now
ruled out on the entire active-amplitude family. Any continuation has to use
an existing metric-changing owner and its genuine tangent, then differentiate
the complete price there. A fitted metric map, heat term or source would evade
the obstruction rather than solve it.

The Lean capsule
[`a4d_native_engine_correlated_current_extension.lean`](certificates/a4d_native_engine_correlated_current_extension.lean)
proves generic gate/minor and heat-sign arithmetic kernels, plus the abstract
no-two-axis-collapse theorem for an invertible common frame, with standard
axioms only. The exact cross-owner checker reports its source SHAs, source Git
blobs, 2084 exact controls and 61 owner-source pins. These include the
AF/Lorentz/CAR first-stage bridge, conditional three-term price split, and metric-update replay,
Lorentz and general-GL current-rest guard obstructions, the fixed-\((q,D)\) heat-fiber jet,
null-sector/domain and off-axis metric controls, the exact \(L=4\) mode
polynomial, the current-step mismatch, and a 128-step regression in
[`a4d_native_engine_correlated_current_extension_results.json`](certificates/a4d_native_engine_correlated_current_extension_results.json).
