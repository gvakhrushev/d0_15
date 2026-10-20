# Full preparation fiber: a correlation-preserving price direction

Research parent: existing #310. Input SOURCE
`a235dbbc05631335498cda376671af6c2772dc41`. Date: 2026-10-13.
The original fixed-source/raw-owner terminal remains open.

The [Jones transport](A4D_NATIVE_JONES_RECORD_TRANSPORT.md) supplies an actual
full matrix transition and a compatible conditional corner. This continuation
tests the remaining **full preparation**, rather than constructing another gate.
It classifies the entire coordinate-conjugation-invariant protected-ground
state interface. It has two real parameters. Fixing both native marginals and
the entire Jones joint table leaves a direction on which the actual heat price
strictly decreases. Motion of a tuple preserving the proved Jones/golden
relations cannot cancel it. The full preparation law must exclude this
direction or couple it to an independently owned changing price term.

A second complete result tests lossless refinement of the full density:
**every** reversible quantum channel across one Fibonacci GNS step has a
positive rank deficit. A faithful finite Gibbs state cannot be its output.
Restricted-family channels and unnormalized heat extensions remain possible
and are constructed below. These are statements about declared interfaces,
not an impossibility theorem for the entire native core.

## 1. Exact state class and all of its parameters

Use the actual level `B=A_(n+7)=M_X(C) (+) M_Y(C)`, n>=0, with
`tau=w_X Tr_X+w_Y Tr_Y`, `u=w_X X`, `v=w_Y Y`, `u+v=1`.
Here `X,Y>=2`. On the **full** GNS space of dimension `X^2+Y^2` take the
existing orthogonal decomposition

\[
 \mathcal H=\operatorname{span}(\Omega,\eta)
       \oplus\mathfrak{sl}_X\oplus\mathfrak{sl}_Y,
 \quad \Omega=\sqrt u\,e_X+\sqrt v\,e_Y,
 \quad \eta=\sqrt v\,e_X-\sqrt u\,e_Y,
\]

where `e_X=vec(I_X)/sqrt(X)` and similarly for Y. Denote the four projections
by `P_Omega,P_eta,P_X,P_Y` and `N_X=X^2-1`, `N_Y=Y^2-1`.

The class requires: a faithful density on the full GNS space; both native
left and right marginals equal tau; invariance under every internal coordinate
conjugation `x -> U_X x U_X* (+) U_Y x U_Y*`; and Omega is a simple largest
eigenvector. This is the previously used protected-zero Gibbs interface with
its actual covariance made exhaustive. It is not declared to be all physical
preparations.

Invariance of the density at fixed data is stronger than mere equivariance
of an assignment depending on moving frames. The latter may have additional
components permitted by the frame stabilizer. Exhaustiveness below is for
the explicitly invariant class, not for every equivariant preparation map.

Every member, and only a member, is

\[
 \sigma_{\lambda,\mu}=\lambda P_\Omega+\mu P_\eta
                 +\alpha P_X+\gamma P_Y,
\]
\[
 \alpha=\frac{(1-\lambda)u-\mu v}{N_X},\qquad
 \gamma=\frac{(1-\lambda)v-\mu u}{N_Y},                 \tag{1}
\]

in the open polygon

\[
 \lambda,\mu,\alpha,\gamma>0,\qquad
 \lambda>\mu,\quad\lambda>\alpha,\quad\lambda>\gamma.   \tag{2}
\]

Proof of exhaustiveness. Diagonal unitary phases give distinct characters on
the off-diagonal matrix units. An operator commuting with all these
conjugations is scalar on each such character line. Permutation conjugations
make the scalars equal. A two-coordinate Hadamard conjugation sends a diagonal
difference to the symmetric off-diagonal pair, forcing the same scalar on
the traceless diagonal part. Thus each complex traceless block is irreducible;
its only commuting endomorphisms are scalar. The two independent unitary
groups prohibit intertwiners between these blocks or with the invariant
two-dimensional scalar space. The remaining block is an arbitrary Hermitian
2-by-2 matrix. Requiring Omega to be an eigenvector makes it diagonal in
`(Omega,eta)`. The two marginal equations are precisely

\[
 \lambda u+\mu v+N_X\alpha=u,\qquad
 \lambda v+\mu u+N_Y\gamma=v.                           \tag{3}
\]

They give (1), and their sum gives trace one. Left and right marginals agree
for every listed projection. Positivity and the simple largest eigenvalue are
exactly (2). This proves both directions and retains every traceless mode.
Distinct lambda or mu give distinct densities. The two parameters are not
coordinate gauge; in particular lambda is a spectral invariant.

The class is nonempty at every actual n. The previously owned family is the
line `mu=(1-lambda)uv`, with `1/2<=lambda<1`. Its normalized residual has
strictly positive eigenvalues summing to one with multiplicities, so each is
less than one. At `lambda=p>1/2` the inequalities (2) are strict. No new
numerical constant is needed for this interior base.

## 2. Full Jones table fixed, full price changes

The current Jones cut has ranks `r_X,r_Y=pathCount(n+1)` and trace `c=p^6`.
Set

\[
 f_X=\frac{r_X(X-r_X)}{N_X}>0,\quad
 f_Y=\frac{r_Y(Y-r_Y)}{N_Y}>0,\quad
 K=uf_X+vf_Y>0,\quad J=vf_X+uf_Y>0.
\]

The joint mismatch `L_e(I-R_e)` annihilates both central vectors. Its traces
on `P_X,P_Y` are `r_X(X-r_X),r_Y(Y-r_Y)`. Therefore the full joint table has
the same form as the previous packet, with

\[
 c-t=(1-\lambda)K-\mu J.                                \tag{4}
\]

At **every** point of (2), the line

\[
 \lambda(s)=\lambda+s,\qquad
 \mu(s)=\mu-\frac KJ s                                 \tag{5}
\]

stays in (2) for sufficiently small positive and negative s. It preserves
both marginals and every entry `(t,c-t,c-t,1-2c+t)` exactly. Thus fixing the
complete Jones joint table leaves an open one-dimensional fiber. This t is a
full-GNS joint readout; physical admission was not supplied by the previous
packet and is not supplied here.

Fix beta>0. Conditional on the **existing Gibbs identification**, the unique
positive heat with kernel `C Omega` is

\[
 \Delta=\beta^{-1}(\log\lambda\,I-\log\sigma),\qquad
 B_{heat}=-\beta^{-1}\log\lambda.
\]

Consequently

\[
 \left.\frac{d B_{heat}}{ds}\right|_0
           =-\frac1{\beta\lambda}<0.                    \tag{6}
\]

This is not an unfixed scalar shift: ground energy zero and its simple vector
are retained. It changes the full spectrum and the actual ordinary partition
trace. The earlier formula `B(t)` remains true on its explicitly declared
one-parameter line; (4)-(6) prove it is not reconstruction from t on this
complete invariant interface. The classification, not a parameter census,
proves that no further covariance condition already stated removes (5).

## 3. Necessary full-price stationarity test

The primary action is BOOK_03 section 03.25:

\[
 \mathcal B=\beta^{-1}\log\operatorname{Tr}e^{-\beta\Delta}
               -\log\det(I-zF).                        \tag{7}
\]

For differentiable finite matrices and fixed beta,z, on the real determinant
domain, its differential is

\[
 d\mathcal B=-\operatorname{Tr}(\sigma_{Gibbs}\,d\Delta)
       +z\operatorname{Tr}((I-zF)^{-1}dF).               \tag{8}
\]

The exponential derivative follows by integrating its first variation and
cycling the trace; it does not require commuting Delta and dDelta. For a
moving normalized simple eigenvector Omega, differentiating its eigenvalue
equation gives `d lambda=Tr(P_Omega d sigma)`. Thus the first term can also
be written `-d lambda/(beta lambda)` in the protected Gibbs interface. Delta
and sigma are then two coordinates of the same accepted interface, not
independently adjustable variables.

For the whole class of tuples preserving the proved golden/Jones relations,
the complete feedback is `F=kappa P`, with `kappa=p^2` or `4p^3` and constant
rank k at a fixed finite level. On `1-z kappa>0`, its price is
`-k log(1-z kappa)`. Hence its
derivative is zero even if the exact Jones frames move. Constant rank alone
would not suffice: the fixed relative overlap and golden coefficients are
essential. The same zero conclusion holds for any differentiable feedback
price depending only on t along (5). No replacement of the older fullStep,
scene or composite price by this particular cut is made.

Therefore the stated full two-term Jones preparation has **no stationary
point anywhere in (2) with t fixed**. If the actual native constraint admits
(5), every other actually owned coupled price contribution must have derivative
`+1/(beta lambda)` on it. If there is no such contribution, the constraint
must exclude this direction. This is a necessary equation to test, not a
definition of native admission and not permission to introduce a compensator.

The carrier condition `D q_t D*=q_s` alone has zero derivative on (5) when
q,D are held fixed, because it contains neither full state parameter. Its
differentiated geometric tangent does not determine which sigma variations
are admitted by a missing joint preparation map. No ten-component metric
source, Ward identity or native stationary state follows from (6)-(8).

## 4. All lossless quantum refinements have a rank deficit

Here a reversible channel means a completely positive trace-preserving
linear map `Phi:M_d -> M_D` with a completely positive trace-preserving
recovery `Psi` satisfying `Psi Phi=id` on **all** density matrices. This is
an explicit full-quantum-information requirement, stronger than preservation
of an operational readout or a chosen state family.

Every such channel has the form

\[
 \Phi(\rho)=\sum_{i=1}^{k}\ell_i V_i\rho V_i^*,\quad
 \ell_i>0,\ \sum_i\ell_i=1,\quad V_i^*V_j=\delta_{ij}I_d.
                                                               \tag{9}
\]

Finite proof. Take Kraus operators K_i,L_j for Phi,Psi. A Kraus operator of
the identity channel is scalar I: its action on any pure vector must stay
on the same line, and testing basis vectors and their pairwise sums makes
the scalar independent of the line. Thus `L_j K_i=alpha_ji I`. Trace
preservation of Psi gives
`K_i* K_m=sum_j conjugate(alpha_ji) alpha_jm I`. Diagonalize this positive
scalar Gram matrix by a unitary change of Kraus coordinates. Nonzero new
Kraus operators are `sqrt(ell_i)V_i` with orthogonal ranges; trace
preservation of Phi gives the sum of ell_i. Kraus existence in finite
dimension follows directly by diagonalizing the positive Choi matrix and
reshaping its eigenvectors. No assumption of a chosen environment state is
made. Conversely (9) has a trace-preserving CP recovery, adding any fixed
density on the unused range outcome. This proves the full class.

For actual consecutive Fibonacci GNS spaces, with `(A,B)=pathCount(n)`,

\[
 d=A^2+B^2,\quad D=(A+B)^2+A^2,\quad
 2d<D<3d,\quad r=D-2d=B(2A-B)>0.                         \tag{10}
\]

Thus k<=2 and **every** channel output has rank at most 2d. At least r fine
modes have zero weight. No output is faithful, even from a faithful input;
in particular no finite-temperature full-carrier Gibbs density is an output.
The rank bound is sharp in the unrestricted matrix-channel class: choose two
orthogonal isometries with equal weights and any faithful coarse density.
This sharpness construction is not a physically supplied fresh environment.

Since `B<=A<=2B`,

\[
 5r-D=2(A-B)(3B-A)\ge0,\qquad r/D\ge1/5.               \tag{11}
\]

The dimensions start 2,5,13 and satisfy `d_(n+2)=3d_(n+1)-d_n`.
Their adjacent gcd is one and `d_n d_(n+2)-d_(n+1)^2=1`.
The ratio tends to phi^2, so `r/D -> 1-2p^2=p^3`.
This applies also to the Jones composite: inner conjugation does not change
these dimensions.

For any faithful fine target sigma and any output rho of a reversible channel,
testing a kernel projection of rho gives the quantitative bound

\[
 \tfrac12\|\sigma-\rho\|_1
 \ge\sum_{i=1}^{r}\lambda_i^\uparrow(\sigma)
 \ge r\lambda_{min}(\sigma).                           \tag{12}
\]

Indeed a traceless Hermitian difference has positive part trace equal to half
its trace norm; pairing with any projection is bounded above by that trace.
The trace of sigma on a rank-r projection is at least its r smallest eigenvalues.
For `sigma=e^(-beta Delta)/Z`, `0<=Delta<=Emax I`, beta>0, `Z<=D`, hence

\[
 \tfrac12\|\sigma-\rho\|_1\ge\tfrac15e^{-\beta Emax}.  \tag{13}
\]

The rank bound is sharp; (12)'s spectral-tail distance is not claimed attainable
for every arbitrary target by a channel in (9). A uniformly bounded beta Emax
therefore leaves a uniform full-state error. Allowing growing heat or changing
the readout is a distinct interface, not a contradiction of (13).

## 5. Constructive alternatives keep the scope exact

**Restricted states.** For the already owned one-parameter states
`sigma_(n,lambda)=lambda P_Omega_n+(1-lambda)R_n`, the map

\[
 \Phi_n(X)=\operatorname{Tr}(P_{\Omega_n}X)P_{\Omega_{n+1}}
       +\operatorname{Tr}((I-P_{\Omega_n})X)R_{n+1}       \tag{14}
\]

is CP and trace preserving. It maps the entire family to the next family with
the same lambda, preserving both required native marginals and the protected
vector. The reverse formula recovers every state in this family. Thus exact
compatible faithful restricted families exist at every actual level n>=2 where
the owned residual is defined (including all Jones carriers), with lambda
still arbitrary. It erases coherences and all distinctions inside Omega's
complement, so it does not recover arbitrary input states. Physical execution
as a closed process would have to retain and price that discarded information.
Equation (14) is not claimed to preserve the Jones joint table across levels.

**Unnormalized heat.** Let V be the actual conjugated-inclusion GNS isometry,
P=VV*, Q=I-P. If the inherited subspace reduces the heat, every positive
ground-zero heat extension with exact unnormalized Gibbs compression has

\[
 e^{-\beta\Delta_f}=V e^{-\beta\Delta_c}V^*+D_Q,
 \quad 0<D_Q\le I_Q,\quad
 Z_f=Z_c+\operatorname{Tr}D_Q.                          \tag{15}
\]

Conversely every such positive D_Q gives a finite heat by the Hermitian
logarithm. Strict `D_Q<I_Q` retains a simple inherited zero mode. Normalized
compression is `(Z_c/Z_f)sigma_c`, and the full heat price grows by
`beta^-1 log(1+Tr(D_Q)/Z_c)>0`. No fine mode was removed or renormalized away.
Fine left/right native marginals impose, for every fine observable y, the
additional exact affine equations

\[
 \operatorname{Tr}(D_Q L_y)=(Z_c+\operatorname{Tr}D_Q)\tau_f(y)
       -\operatorname{Tr}(V e^{-\beta\Delta_c}V^* L_y),   \tag{16}
\]

and the corresponding right equations. They are not automatic. Equations
(15)-(16) expose the remaining new-mode preparation, rather than asserting
it uniquely selected. No all-native refinement no-go follows from (9).

## 6. Actual owners and next exact obligation

`D0.Foundation.M1Forced` contains uniqueness as a field, and
`D0.Foundation.selector_M1Forced` consumes an already proved strict minimum.
`D0.Foundation.M1ClassAdmissibility.non_singleton_class_not_M1Forced` explicitly
allows non-singleton catalogue-independent classes. Neither supplies the
missing preparation constraint. `D0.Complexity.LyapunovNavigable` likewise
receives `solution_forced`. `D0.CompatibleOperatorFamily` receives the
whole family and its naturality equation before lifting it to the limit.
These actual source propositions were inspected and hash pinned; they are not
additional compiler-resolved declarations in this packet. Their interfaces
must not be read as selection of lambda, mu, Delta or a physical clock.

This packet does not add an action or change these owners. It classifies the
complete stated invariant preparation interface, proves the exact surviving
price direction (5), and tests all reversible full-state channels. Finite exact
controls bind the scalar spectra, actual block marginal matrices, fixed joint
tables, Kraus recovery witnesses and retained new-mode rank. The research Lean
capsule formalizes its named scalar kernels, not the complete complex group
classification, the full Kraus theorem, or physical admission. Those have the
separate analytic/certificate scope just specified.

The next proof must construct the **joint native preparation constraint** and
evaluate it on `(delta lambda,delta mu)=(1,-K/J)`, with all actual metric/link,
matter, feedback and heat arguments retained. If it admits this vector, an
existing coupled term must supply the compensating derivative in section 3;
if it excludes it, derive that exclusion from its owner. Fixing t, asserting
M1 uniqueness, using a full-state reversible channel, or rotating a fixed
Jones tuple does not answer this test. Source/Ward, quantitative contrast,
native stationarity, curved roots, soundness/recovery and GR remain open;
#310, #202, #317 and all parent contracts remain intact.
