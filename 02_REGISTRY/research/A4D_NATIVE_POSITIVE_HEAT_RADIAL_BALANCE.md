# Positive graded Hodge heat: radial balance and the complete flat shape source

Parent: existing #310, `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Initial capsule input: `eeab0de21ee704794e291434e6ae0b65fdb360d6`.
Flat-shape continuation input: `2d3a678ef308735c9c6fbcc3c5af94e45c0ba23c`.
Main: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`. Date: 2026-10-10.

**Result.** The positive graded Hodge binding left outside the earlier Lorentz
heat obstruction has a compulsory, strictly positive thermal response under
an admitted common metric dilation. It is twice its full Gibbs mean energy.
This is a coupled metric variation, not an independently varied hidden block.
If the other terms have zero response along that same variation, the complete
price has no stationary point in this stated class. A genuine coupling must
instead produce the explicitly computed opposite radial response. Neither
this condition nor a chosen compensator is installed as a native law.

At the actual flat counting Hodge operator, a uniform positive lower bound
also gives a failed O(h) flat-probe contrast for the literal, unrescaled
bootstrap and a scale-constant remainder. This is a conditional binding test:
physical admission, normalization and the readout to a physical flat metric
must be established before using it against a proposed native realization.

This does not construct the complete native preparation. It does not exclude
all positive pairings, all couplings, nonzero matter, scale-dependent beta/z,
or all GR realizations. It does not infer a pure-trace source from one radial
contraction. All original #310/#202/#317 and G0–G4 terminals stay OPEN.

## 1. Consumed operators and the precise full class

The [weighted-operator construction](A4D_NATIVE_WEIGHTED_DIRAC_BOUNDARY.md)
builds the documented operator on the actual full D0 cochains:

\[
 \delta_W=W^{-1}d^T W,\qquad \mathcal D_W=d+\delta_W.
\]

Here W is supplied, invertible, symmetric and, in this result, **positive**.
Its physical selection is not a conclusion of the old Boolean Hodge owner.
The identity weight is bound to the actual counting `hodgeCarDirac`.
`ArchiveCovariantCubicalDifferential.dConn_raises_degree` proves that the
actual coefficient-link differential raises form degree by one, also for
curved links. It does not require the square to vanish. The old all-16-grade
carrier, all sites and coefficient fibres are retained.

Consider the whole following class, not one chosen spectrum:

* E is a finite graded real space, d raises degree by one and d is nonzero;
* W is a positive degree-preserving pairing;
* a real admitted joint preparation path realizes q(t)=exp(2t)q, fixed
  dressed links, and W(t)|E^k=exp((4-2k)t)W|E^k;
* d is unchanged on this path; beta is fixed and positive;
* the complete remaining price R(t), including feedback, pairing terms not
  already in W, affine/matter effects and any other retained contribution,
  is differentiated along **the same actual path**.

The W scaling is the already tested geometric compound law:
W_Q^k=sqrt(abs(det Q)) times the k-th compound of Q^{-1}. At positive Q,
this law supplies a positive pairing and has exactly the displayed scaling.
Other independently owned positive pairings may satisfy it. Positivity alone
does not imply this scaling law; a Lorentz compound pairing is not positive.
No constitutive uniqueness or physical admission of these W(Q) is asserted.
An extra constraint forbidding the radial path lies outside the class and
requires its own physical probe/recovery analysis.

The same variation is present in the existing joint constraint chart:

\[
 Dq_tD^T=q_s,\quad (V_s,V_t,\dot D)=(2q_s,2q_t,0),
 \quad DV_tD^T+\dot Dq_tD^T+Dq_t\dot D^T=V_s.       \tag{1}
\]

Both endpoint metrics vary. The link coordinates and all other allowed
variations remain in the domain. One nonzero admitted directional derivative
suffices to exclude full stationarity; it does not discard link equations or
compute all ten components of the source. For the existing transported
readout B(D)qB(D)^T, D is fixed, so that readout scales by exp(2t) as well.
The path has no missing delta-B term.

## 2. Exact homogeneity without a flatness assumption

Let J_t act on degree k as exp(kt). The grade relations give

\[
 \delta_{W(t)}=e^{-2t}\delta_W,\qquad
 \mathcal D_{W(t)}=e^{-t}J_t\mathcal D_WJ_t^{-1},\qquad
 \Delta(t):=\mathcal D_{W(t)}^2
       =e^{-2t}J_t\Delta(0)J_t^{-1}.                 \tag{2}
\]

Indeed the weight ratio between two consecutive degrees is exp(-2t),
J_t d J_t^{-1}=exp(t)d, and the adjoint has the opposite degree.
Squaring a similarity proves the last equality. **No d squared equals zero
premise is used.** Thus the same spectral scaling holds for the actual
curved coefficient differential when the stated pairing and path apply.

Positive W makes D_W self-adjoint in a positive inner product, hence its
square has eigenvalues lambda_i>=0, with all multiplicities. At least one
is positive: d and its adjoint have different degrees, so d nonzero implies
D_W nonzero, and a nonzero finite self-adjoint operator has a nonzero square.
Equation (2) gives every eigenvalue exp(-2t)lambda_i, including every zero
mode. No archive mode or determinant is deleted.

The finite grade/spectral argument is analytic. The capsule compiles the
square-similarity algebra without nilpotency, the actual graded-link owner,
and the previously constructed actual untwisted square identity. It does not
claim a formal spectral theorem for every moving geometric W(Q).

## 3. The actual bootstrap derivative and the necessary compensator

Use the existing BOOK_03 / composed-feedback price, not a spectral-action
replacement:

\[
 H(t)=\beta^{-1}\log\sum_i e^{-\beta e^{-2t}\lambda_i},
 \qquad \mathcal B(t)=H(t)+R(t).
\]

Its genuine derivative is

\[
 H'(0)=2E_\beta,\qquad
 E_\beta={\sum_i\lambda_i e^{-\beta\lambda_i}
                  \over\sum_i e^{-\beta\lambda_i}}>0,
 \qquad \mathcal B'(0)=2E_\beta+R'(0).                \tag{3}
\]

The numerator is a sum of nonnegative terms with a positive term; the
partition is positive. The existing `genuine_thermal_source` is consumed
literally, with a new actual `HasDerivAt` of each radial spectral curve.
The finite Hilbert trace is the algebraic operator trace in a complete basis;
a change of positive pairing does not insert an extra factor W into that trace.
Adding any finite number of retained zero modes enlarges the denominator
but preserves the strict sign. Positivity is essential: a signed spectrum
can have a negative or cancelling mean and belongs to a different case.

Consequently full stationarity requires

\[
                    R'(0)=-2E_\beta.                \tag{4}
\]

If R'(0)=0 throughout a described prepared class, its full stationary set
is empty. This applies whenever a real native map is proved to stay in the
fixed-compression golden first-variation class of
[A4D_NATIVE_CONSTRAINED_PRICE_SOURCE.md](A4D_NATIVE_CONSTRAINED_PRICE_SOURCE.md)
and **all other** radial contributions also vanish. The golden zero is not
silently extended to arbitrary feedback maps. A remainder supplied to cancel
(3) is not a construction of a native law or a source. A nonzero overall
calibration or fixed-level nonzero normalization does not turn this derivative
into zero.

This computes a nonzero radial/trace contraction, not a pure-trace covector.
Off-diagonal and traceless components may be nonzero. Equality with rho0,
physical matter/source subtraction, Ward identities and actual on-shell
solutions remain separate obligations. In a sourced gate its own source
variation is part of R'(0); it cannot be silently set to zero.

## 4. Quantitative flat contrast of the literal bootstrap

This section additionally fixes the actual full counting Hodge/CAR operator
at the flat base and the same full scalar representation used in
[A4D_NATIVE_HODGE_CONNES_METRIC.md](A4D_NATIVE_HODGE_CONNES_METRIC.md).
All 16 Fock copies remain. The difference square has eigenvalues

\[
 \lambda_k=4L^2\sum_{r=1}^4\sin^2(\pi k_r/L),
 \quad k\in(\mathbb Z/L)^4,\quad L\ge2,               \tag{5}
\]

each with multiplicity 16. This follows by applying each actual periodic
shift to its character; the actual square identity is the input, not a
different graph or a counting kernel. The native index and physical mesh
are identified here only as this owner's L=N+2 and the proposed probe h=1/L.

For q(s)=s q_0, s in [1/2,2], the trace spectrum is lambda_k/s. With
j=min(k,L-k), concavity of sine on [0,pi/2] and sin(x)<=x give
16j^2 <= 4L^2 sin^2(pi k/L). In particular the mode (1,0,0,0) lies
between 16 and 4pi^2. There are at most two one-dimensional indices per j.
Thus

\[
 Z_L(s)\le16\left({1+e^{-8\beta}\over1-e^{-8\beta}}\right)^4,
\]

using j^2>=j and the geometric series. Keeping just the indicated positive
mode in the numerator of dH/ds gives the all-L bound

\[
 {dH_L\over ds}={1\over s^2}
 {16\sum_k\lambda_k e^{-\beta\lambda_k/s}\over Z_L(s)}
 \ge c_\beta:=4e^{-8\pi^2\beta}
       \left({1-e^{-8\beta}\over1+e^{-8\beta}}\right)^4>0. \tag{6}
\]

For 0<epsilon<=1/2 the native half contrast is therefore at least
c_beta epsilon when R is constant along this probe. If a proposed realization
reads the physical constant metric (1+-epsilon)g_0 with flat physical links
and zero source, the physical Palatini half contrast is exactly zero.
For one fixed a!=0, the literal bootstrap then obeys

\[
 |a^{-1}\Delta\mathcal B_h-\Delta I_h|
       \ge {c_\beta\over|a|}\,h^{1/3},              \tag{7}
\]

which cannot be O(h). An O(h) error of recording/preparation subtracts only
O(h) from this lower bound. No claim of native physical admission of that
flat probe is made. With a nonconstant R, (3) alone is a pointwise first-jet
statement; (7) cannot be asserted without an appropriate uniform secant bound.

**Normalization fence.** The literal price in this section is B_h itself.
If a native owner instead supplies I_h^N=nu_h B_h, (7) carries |nu_h|.
A varying nu_h, beta_h, z_h, physical volume constraint or different transition
requires its own analysis. Neither h^2 B_h nor a compensating counterterm is
installed. Fixed-level emptiness when R'=0 persists for every nu_h!=0, but
that does not exclude nearby corrected roots, singular limits or recovery in
other prepared classes. The all-L spectral estimate is analytic, not a
fully compiled continuum result.

## 5. All ten flat heat coefficients and a nonzero traceless response

The preceding radial contraction alone cannot classify the source as pure
trace. Here the same existing geometric Hodge binding admits the complete
calculation at every constant **positive** Q. Q is the pairing metric in
this section; a Lorentzian native readout and physical admission are not
inferred from positivity. The original constrained Lorentz carrier and its
24 independent link directions are unchanged.

On the full periodic exterior carrier write

\[
 z_r(k)=L(e^{2\pi i k_r/L}-1),\qquad
 C_{rs}(k)=\operatorname{Re}(\overline{z_r(k)}z_s(k)).
\]

Complexifying the real Fourier decomposition retains every conjugate mode
and all sixteen grades. For constant Q the common volume factor in W_Q
cancels in W_Q^{-1}d^*W_Q. The weighted creator adjoints obey
\(\{c_r^\dagger,(c_s^\dagger)^{*_{W_Q}}\}=(Q^{-1})_{rs}I\),
while two creators or two adjoints anticommute. Thus the **actual full**
Dirac square has symbol

\[
 \Delta_Q(k)=\lambda_Q(k)I_{16},\qquad
 \lambda_Q(k)=z(k)^*Q^{-1}z(k).                         \tag{8}
\]

This is a scalar symbol on the full Fock space, not a degree-zero filter.
For a real symmetric metric variation V,
\(\delta Q^{-1}=-Q^{-1}VQ^{-1}\). Differentiating the actual finite heat
price therefore gives its entire covector on the constant-metric subspace

\[
 dH_Q[V]=\operatorname{tr}(A_QV),\qquad
 A_Q=Q^{-1}\left(\sum_k w_k C(k)\right)Q^{-1},\qquad
 w_k={e^{-\beta\lambda_Q(k)}\over\sum_\ell e^{-\beta\lambda_Q(\ell)}}.
                                                               \tag{9}
\]

The sixteenfold multiplicity cancels from this normalized derivative,
not from the retained trace. Formula (9) follows from the genuine finite
thermal derivative already owned by the capsule. Its Fourier/metric
binding here is an analytic argument; the full assertion is not a new
kernel-formalized theorem. Packed independent components are A_rr on the
diagonal and **2 A_rs** for r<s.
These are ten spatially uniform metric variations. The complete local
q,D,b,m source, all connection equations and matter equations are not
computed by this restriction.

For diagonal Q=diag(q_0,q_1,q_2,q_3), put

\[
 E_r={\sum_{j=0}^{L-1}(4L^2\sin^2(\pi j/L)/q_r)
                e^{-\beta 4L^2\sin^2(\pi j/L)/q_r}
                \over\sum_{j=0}^{L-1}e^{-\beta 4L^2\sin^2(\pi j/L)/q_r}}.
\]

The product Fourier weights and the oddness of the sine term give all ten
coefficients explicitly:

\[
 (A_Q)_{rr}=E_r/q_r,\qquad
 (A_Q)_{rs}=E_rE_s/(4L^2)\quad(r\ne s).                \tag{10}
\]

The off-diagonal terms are present for the actual forward differences;
freezing them to zero would not give the finite operator derivative.
They are O(L^{-2}) for fixed positive diagonal Q and beta, whereas the
following traceless diagonal response stays separated from zero.

Take Q_0=diag(4,1/4,1,1), V=diag(4,-1/4,0,0), beta=log(2).
This is test data, not a selected native temperature. Then

\[
 \operatorname{tr}(Q_0^{-1}V)=0,\qquad dH_{Q_0}[V]=E_0-E_1.
                                                               \tag{11}
\]

V is the tangent of the exactly volume-preserving curve
Q(t)=diag(4 exp(t),exp(-t)/4,1,1). Applying the same Q(t) at both ends of
every identity link obeys the full joint constraint with delta D=0.
Hence this is a genuine constrained traceless tangent in this stated
binding; it does not freeze one endpoint. Its coordinate trace is not zero:
metric trace, not the sum of coordinate entries, is the relevant condition.

There is an all-L lower bound, not an extrapolation from small lattices.
For j=min(k,L-k), the one-axis eigenvalue lambda^0_j satisfies
16j^2 <= lambda^0_j <= 4pi^2 j^2. For q_0=4, its partition is at most
17/15, and the j=1 term gives
E_0 >= 60/(17*2^16), using pi^2<16. For q_1=1/4, the partition is at
least one and, with r=2^-64,

\[
 E_1\le512\sum_{j\ge1}j^2r^j
       ={512r(1+r)\over(1-r)^3}.
\]

The geometric-series identity and exact rational comparison imply

\[
                 E_0-E_1>1/20000 \quad\text{for every }L\ge2.   \tag{12}
\]

All zero modes remain in the denominators. Consequently this heat source
is **not pure trace**, even in the refining limit. For an actual complete
price whose other terms have zero derivative on this same volume-preserving
path, it excludes stationarity. Other coupled terms may have a compensating
traceless derivative; no general coupled no-go is inferred.

For the linear paired probe Q_0+-epsilon V, the two determinants are both
1-epsilon^2. Any same-state volume-only price term cancels exactly between
the two endpoints. These endpoints are an equal-volume pair, not two points
of the fixed-det=1 fibre; the volume-preserving curve above is the separate
fixed-volume first-jet test.

For |t|<=1/4 on the linear pencil Q_0+tV, the first q lies in [3,5] and
the inverse second q in [16/5,16/3]. The same bounds give

\[
 {d\over dt}H(Q_0+tV)
 ={E_0(t)\over1+t}-{E_1(t)\over1-t}
 \ge {28\over15\,2^{22}}
       -{1024r_{48}(1+r_{48})\over(1-r_{48})^3}
 >1/2500000,\quad r_{48}=2^{-48}.                      \tag{13}
\]

Indeed the first spectral scale is at least 3j^2, its j=1 value is less
than 22, and its partition is at most 9/7. The second spectral scale is
at least 48j^2 and at most 384j^2; at most two modes occur per j, and
1/(1-t)<=4/3. These estimates prove (13) uniformly in L.

Thus the literal heat half contrast is at least epsilon/2500000. Adding
any volume-only term does not change it. If an independently admitted
native readout realizes this prepared pair as the corresponding constant
flat physical metric probe, its zero-source Palatini contrast is zero.
With epsilon=h^(1/3), one fixed nonzero calibration then leaves an
h^(1/3) gap, which O(h) recording errors cannot remove. This comparison
has exactly the physical-admission and native-normalization fences of
Section 4; a direct Lorentz realization of Q is not claimed. A varying
normalization multiplies the bound. No conclusion about all native F,
all coupled prices, corrected roots or Lorentzian GR follows.

**Every fixed positive temperature.** The preceding shape test is not
restricted to one numerical beta. For any fixed beta>0 set
c=beta/log(2)>0 and

\[
 Q_c=\operatorname{diag}(4c,c/4,c^{-1},c^{-1}),\qquad
 V_c=\operatorname{diag}(4c,-c/4,0,0).
\]

Then det Q_c=1, tr(Q_c^{-1}V_c)=0, and both linear endpoints have
determinant 1-epsilon^2. The first two one-axis eigenvalues on this pencil
are exactly 1/c times their values above, so their Boltzmann weights at
beta=c log(2) are unchanged. The other two axis partitions cancel from
these two energy means by the same product factorization. Consequently
dH_beta(Q_c)[V_c]>1/(20000c), and the heat half contrast is at least
epsilon/(2500000c) for every L>=2 and 0<epsilon<=1/4. The exact
volume-preserving curve replaces the first two diagonal entries by
4c exp(t) and c exp(-t)/4. Beta is fixed throughout each variation;
no temperature variation or temperature law is used. This is a statement
for every fixed beta on the stated full positive-metric family, with its
test metric depending on beta. It neither assumes all these metrics are
native-admitted nor supplies a uniform result for beta_h or a joint
temperature-metric constraint.

The exact checker binds (8) to all sixteen actual CAR grades for both a
mixed positive metric and Q_0, then computes all ten packed coefficients
from every Fourier mode for L=2 and L=4. It checks (11), both distinct
volume statements, the temperature-rescaling algebra, and the rational
constants in (12)-(13). The all-L
inequalities are proved above, not by the two finite checks.

## 6. Checks, controls and effect on T0

The capsule contains twenty-three propositions with standard logical axioms only.
The four added shape statements prove the genuine first derivative of each
pencil mode a/(1+t)+b/(1-t)+c and of the existing full finite heat price;
the full Fourier/metric binding and uniform estimates remain analytic. The
actual curved degree argument is rebuilt using kernel `decide` on the literal
CAR support. The separately printed old `dConn_raises_degree` retains its
one explicit `carCreateInt_degree_raise` native_decide leaf; it is not hidden
or used as the proof of the new rebuilt proposition. Three primary/prior
propositions and 71 transitive D0 source files are pinned. The checker passes
319 controls and rejects 22 false scope ledgers.

The exact checker retains every degree and site in the L=2 D0 stencil,
non-diagonal positive compound weights, and curved coefficient links with
d squared nonzero. It checks the full similarity and weighted-adjoint
relations, both endpoint metrics in (1), the literal L=2/L=4 spectra and
rational thermal moments at beta=log(2), including added zero modes.

A separate finite control uses the same existing bootstrap on four graded
coordinates: d has only d[1,0]=1, their degrees are (0,1,0,1), and the actual
positive Dirac square has full spectrum (0,0,1,1). It is scaled by exp(-2t)
with beta=log(2). The complete orthogonal operation is the two-dimensional
Cayley block plus the identity on the other two coordinates, with the rank-one
readout onto coordinate zero. These matrices are expressed in the moving
W(t)-orthonormal frame: in the fixed graded basis the operation is
W(t)^(-1/2) U W(t)^(1/2), and its adjoint is taken with W(t). The readout
commutes with these diagonal weights; the feedback price is unchanged.
Its feedback has z=1/2 and parameter
u(t)=1/3-(205/324)t. Its thermal derivative is 2/3 and its feedback derivative
is -2/3. This cancels one radial derivative. It is **not** an admitted D0
preparation or a full joint stationary solution; it prevents promotion of
(3) to a no-go for every coupled price. The zero differential, indefinite
pairing, varying temperature/normalization and missing radial admission
are independent scope controls. No compensator is selected for the theory.

The consequence for the single T0/T1 packet is concrete: a preparation using
this positive graded heat cannot close its gate using only the already
vanishing golden feedback contribution. It must derive the genuine remainder
response in (4), or prove a different allowed scaling/normalization/readout.
A mathematical choice of that response is insufficient. Section 5 also computes
all ten heat coefficients at constant positive metrics and excludes a pure-trace
reading of that contribution. The full native preparation, coupled source,
refinement and physical recovery remain open; neither this computation nor
the radial test closes the complete D0 law.

Reproduce with `python3 02_REGISTRY/research/certificates/a4d_native_positive_heat_radial_balance_check.py`.
Use `--compile` to compile the two unchanged research dependencies and the
new capsule in an isolated temporary import directory, using the repository's
pinned Lean environment. The receipt contains actual propositions and
transitive axioms, source hashes and the exact compiler procedure. It
distinguishes the new compiled finite statements from the analytic graded,
spectral and uniform-in-L arguments above.
