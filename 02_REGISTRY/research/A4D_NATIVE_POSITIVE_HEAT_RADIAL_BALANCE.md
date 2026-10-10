# Positive graded Hodge heat: compulsory balance on the full joint radial variation

Parent: existing #310, `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Input SOURCE: `eeab0de21ee704794e291434e6ae0b65fdb360d6`.
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

## 5. Checks, controls and effect on T0

Nineteen new propositions compile with standard logical axioms only. The
actual curved degree argument is rebuilt using kernel `decide` on the literal
CAR support. The separately printed old `dConn_raises_degree` retains its
one explicit `carCreateInt_degree_raise` native_decide leaf; it is not hidden
or used as the proof of the new rebuilt proposition. Three primary/prior
propositions and 71 transitive D0 source files are pinned. The checker passes
180 controls and rejects 18 false scope ledgers.

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
A mathematical choice of that response is insufficient. Full native
preparation, all ten source components, refinement and physical recovery are
still open; this result closes only the stated positive-Hodge radial branch.

Reproduce with `python3 02_REGISTRY/research/certificates/a4d_native_positive_heat_radial_balance_check.py`.
Use `--compile` to compile the two unchanged research dependencies and the
new capsule in an isolated temporary import directory, using the repository's
pinned Lean environment. The receipt contains actual propositions and
transitive axioms, source hashes and the exact compiler procedure. It
distinguishes the new compiled finite statements from the analytic graded,
spectral and uniform-in-L arguments above.
