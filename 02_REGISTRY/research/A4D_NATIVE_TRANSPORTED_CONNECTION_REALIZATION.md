# Native connection readout and transported coframe realization

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Input: `fc12fc7800eff1a0fb74d73c9d920128cbc9450f`.
Status: **complete finite transported-center fiber classification and
constructive smooth kinematic preparation; native dynamics remain OPEN**.

This advances the state/variation map in the native realization plan. It
uses existing affine links and the existing transported solder center.
It installs no action, source, equation, refinement arrow, gauge quotient
or physical selection principle. Composing the transported center with
the Gram map is an explicitly analyzed readout, not a proof that an
existing native action uses it. The previous ordinary center and its
refinement obstructions retain their scopes.

## 1. Owners, orientation and the actual map

All source versions and transitive Lean imports are pinned by the
companion certificate and compilation receipt.

| Actual owner | Data and theorem used | Boundary retained |
|---|---|---|
| `ArchiveChainConnection.lean` | A stored link pulls a vector at x+r to x; independent oriented slots and ordered path composition. | Opposite slots are not identified at period two. |
| `ArchiveChainCurvature.lean` | A=U(x,r)U(x+r,s), B=U(x,s)U(x+s,r), P=AB^-1, F=A-B=(P-I)B. | Ordinary node gauge covariance is not a centered-Cartan/diffeomorphism law. |
| `ArchiveAffineCartanConnection.lean` | Affine pairs (U,b), product (UV,b+Uc), open and based torsion. | Translation shifts are independent data; no constitutive solder relation is assumed. |
| `ArchiveAffineExteriorLink.lean` | Lorentz matrix condition on the linear part, with arbitrary affine shift. | The CAR readout sees only the linear part, not a matter action. |
| `A4DRawSolderFrameAction.lean` | Raw F=eta+e, transported center and its finite local frame covariance. | Ordinary backward centering equals this readout only at R=I. |
| `A4DObserverPositiveExterior.lean` | Lorentz invertibility and `lorentzVectorEquiv`. | That equivalence acts by U^-1; the present constructor uses its inverse. |

Let eta=diag(1,-1,-1,-1). For every matrix U with U eta U^T=eta
and every vector b, define the native affine link

    nativeLink(U,b) = ((lorentzVectorEquiv U).symm, b).

Its actual matrix in `archiveRoleBasis` is exactly U. Thus the linear
readout onto Lorentz matrix links is surjective. Matrix coordinates
determine a linear map in a basis, so its full fibers are precisely
the arbitrary affine shifts b. Their invisibility to this readout
does not make them physical gauge. The capsule verifies the matrix,
inverse, Lorentz-subtype, four-factor holonomy and open-torsion bindings.

The existing raw-row transported center is

\[
 T_R(F)_r(x)=\tfrac12\{F_r(x)+F_r(x-r)R(x-r,r)\}.                 \tag{1}
\]

Use R=U, not U^-1: the stored vector pull from x to x-r induces a
covector row pull from x-r to x. With raw right frames F'=F Lambda,
the corresponding native vector frame is Lambda^-1, so

\[
 R'(x,r)=\Lambda_x^{-1}R(x,r)\Lambda_{x+r},\quad
 T_{R'}(F')=T_R(F)\Lambda,\quad
 g=T_R(F)\eta T_R(F)^T.                                      \tag{2}
\]

The first two identities reuse the compiled owner theorem; Lorentz
Gram invariance proves the last readout independent of that frame.
This matrix-level bridge does not fill the missing centered-Cartan
connection law identified by `A4D_CARTAN_CHAIN_CONNECTION_REALIZATION.md`.

## 2. Complete finite range, kernel and nonlinear metric fibers

Fix one direction and one periodic line of length L>=2. Allow arbitrary
invertible links R_j, not only Lorentz links. Rows f_j,t_j have dimension
d (d=4 in D0). Indices below are modulo L. The exact equation is

\[
 (A_Rf)_j=(f_j+f_{j-1}R_{j-1})/2=t_j.                         \tag{3}
\]

Set W=R_0 R_1 ... R_(L-1), Q_0=I and
Q_k=R_(-k) ... R_(-1) for 1<=k<=L-1. Successive substitution into
the j=0 equation gives

\[
 f_0G=B(t),\qquad G=I-(-1)^LW,\qquad
 B(t)=2\sum_{k=0}^{L-1}(-1)^k t_{-k}Q_k.                     \tag{4}
\]

Consequently (3) is solvable **iff B(t) is in the row range of G**,
equivalently B(t)v=0 for every column v in ker G. Choose any such f_0,
then set f_j=2t_j-f_(j-1)R_(j-1) for j=1,...,L-1. Equation (4)
is exactly the remaining wrap equation; it is sufficient as well as
necessary. Every other solution has initial row f_0+n_0 with n_0G=0,
and n_j=(-1)^j n_0R_0...R_(j-1). Thus

\[
 \dim\ker A_R=\dim\ker G,\quad
 \operatorname{rank}A_R=dL-\dim\ker G,\quad
 \det A_R=2^{-dL}\det G.                                    \tag{5}
\]

Eliminating rows 1,...,L-1 in the block matrix 2A_R leaves identity
pivots and Schur complement G^T when row vectors are stacked as
columns, proving the determinant. Dimension follows from the explicit
kernel isomorphism. The criterion supplies the actual compatibility
equation and reconstruction, not only a rank count.

The Lean capsule proves the generic version for any real module:
iteration u_(j+1)=b_j-T_j u_j has homogeneous part
(-1)^L T_(L-1)...T_0, periodic solutions exist iff the zero-initial
forcing is in the defect-map range, and every inhabited fiber is a
translate of its kernel. Substituting T_j(f)=fR_j, b_j=2t_(j+1)
gives (3)--(4); the actual row equation is separately bound to (1).
The all-size determinant and finite-dimensional dimension arguments
are analytical, not claimed as compiled Lean results.

On the full four-torus the raw rows are independent: there are 4L^3
lines and 16L^4 scalar unknowns. Sum the kernel dimensions in (5)
over all lines. Under (2), W becomes Lambda_0^-1 W Lambda_0 and
B becomes B Lambda_0; admissibility and dimensions are unchanged.
Norm bounds refer to the stated Euclidean frame, not an uncontrolled
noncompact Lorentz gauge.

At R=I the old odd/even classification is recovered: invertible
for odd L, and a four-dimensional alternating raw kernel per line
for even L. This kernel need not survive transported connections.
A commuting nonzero boost and nontrivial spatial rotation has no
eigenvalue 1, so an even cycle with that holonomy is invertible.
A pure boost leaves two kernel directions. Exact rational controls
include these cases and noncommuting products.

For a prescribed nondegenerate Lorentz Gram Q, choose any representative
T_0 with T_0 eta T_0^T=Q. Every possible transported center has the
form T=T_0 Lambda, Lambda eta Lambda^T=eta. For fixed R, the **complete
nonlinear metric-fiber criterion** is: there exists such a field Lambda
for which each row line satisfies (4). Reconstruct F, retain its full
raw kernel, and put e=F-eta. This neither asserts every singular-center
metric fiber inhabited nor treats the kernel as gauge. If every G is
invertible, all target centers are attainable; an additional requirement
of raw-solder nondegeneracy is separate, and is satisfied by Section 5.

## 3. Quantitative range bound and the even-grid obstruction

Use the maximum Euclidean row norm. Suppose every oriented segment
product of length at most L has norm <=C_0, with C_0>=1, and the row
range map u->uG has a right inverse of norm <=kappa on its range.
Equation (4) gives ||B||<=2LC_0||t||. Choosing a least-norm initial
solution and then applying the recursion gives

\[
 \|f\|_\infty\le 2LC_0(1+C_0\kappa)\|t\|_\infty.              \tag{6}
\]

This is a right inverse on the admissible target subspace. Kappa is
a singular-value bound for the matrix range, not merely an eigenvalue
gap; it is not inferred uniformly for arbitrary holonomy.

Even invertible, uniformly controlled G does not provide a uniformly
bounded full centering inverse in the smooth near-identity link class.
Let L be even, h=1/L and ||R_j-I||<=Ch. For a fixed unit row w set
f_j=(-1)^j w. Direct substitution gives

\[
 (A_R f)_j=(-1)^j w(I-R_{j-1})/2,\qquad
 \|A_R f\|_\infty\le Ch/2,\quad\|f\|_\infty=1.                \tag{7}
\]

If A_R is injective, ||A_R^-1||>=2/(Ch). If it is singular, this
bounds the smallest singular value including zero; it does **not**
by itself bound the least positive singular value or quotient inverse.
These alternatives remain separate. This is the coframe readout,
not the joint physical Euler operator or a genuine gauge quotient.

## 4. Exact flat joint metric/link differential

One further finite distinction matters for the simultaneous variation map.
At the actual flat point F=eta, R=I, differentiate the metric readout:

\[
 \delta g_{rs}=(A_r\delta F_{rs})+(A_s\delta F_{sr})
 +\tfrac12\{\eta_{rr}K_r(x-r)_{rs}+
                   \eta_{ss}K_s(x-s)_{sr}\},                 \tag{7a}
\]

where K_r eta+eta K_r^T=0 and A_r is the ordinary row average.
Each diagonal K_r entry is zero. Link variations therefore leave all
four diagonal equations unchanged. Conversely a link in direction r
with its single internal generator (r,s), at x-r, can set precisely
the off-diagonal metric component (r,s) at x. Hence all six
off-diagonal metric fields are independently in the joint image.
The diagonal equations have exactly the old one-direction Nyquist
cokernels on even grids.

The **metric-only** differential on all 16 raw plus 24 link variables
therefore has rank 10L^4-4L^3 at even L, and rank 10L^4 at odd L.
Its kernels have dimensions 30L^4+4L^3 and 30L^4, respectively.
But prescribing the metric **and** all link variations is a different
map. Its block form is [[D_F,D_R],[0,I]], so after subtracting D_R
times the second output it has rank 24L^4+rank D_F. Reusing the
previous complete flat coframe-rank theorem gives

\[
 \operatorname{rank}D(F,R\mapsto(g,R))=
 \begin{cases}
 34L^4-4L^3-6L^2,&L\ \text{even},\\
 34L^4,&L\ \text{odd}.
 \end{cases}                                                \tag{7b}
\]

In the even case the cokernel dimension remains 4L^3+6L^2, and
the kernel dimension is 6L^4+4L^3+6L^2. Thus the freedom to vary
links improves metric-only reachability but does not make arbitrary
independently prescribed finite metric/link targets feasible. At L=2
the three exact ranks are 104 (raw metric), 128 (joint variables,
metric-only output), and 488 (metric plus links output). The checker
assembles all three real-space matrices and computes exact rational
ranks. None of these kernels is declared physical gauge.

## 5. Smooth native coframes, links and all variations

Work on the unit periodic four-torus, L in 4N, h=1/L. Specify before
preparation a smooth periodic invertible row solder Theta(y), with
the chosen orientation/time orientation, and any smooth eta-skew
connection one-form omega_r(y). These are kinematic input data, not
a source or an on-shell gate. Constants come from fixed C^(k+2)
bounds on the data and an inverse bound for Theta.

For Z eta+eta Z^T=0 and ||Z|| small, define

\[
 C(Z)=(I-Z/2)^{-1}(I+Z/2).
\]

The identity (I+D)eta(I+D)^T=(I-D)eta(I-D)^T for D=Z/2
proves C(Z) Lorentz. The inverse identity C(-Z)=C(Z)^-1 and
continuity along tZ put it in the identity component. The inverse
series gives, also in any fixed parameter derivatives,

\[
 C(h\omega)=I+h\omega+\tfrac12h^2\omega^2+O(h^3)
            =\exp(h\omega)+O(h^3).                           \tag{8}
\]

Define actual native data, without inverting A_R:

\[
 R_h(x,r)=C(h\omega_r(hx)),\qquad
 F_{h,r}(x)=\Theta_r(hx+\tfrac h2 e_r)
                      C(-\tfrac h2\omega_r(hx)),\quad e_h=F_h-\eta.       \tag{9}
\]

The links lift through `nativeLink`; affine shifts can initially be
zero. Evaluate the literal center (1), not an independently replaced
target. Its current term is
Theta_r+(h/2)partial_r Theta_r-(h/2)Theta_r omega_r+O(h^2).
Since C(-h omega/2)C(h omega)=I+(h/2)omega+O(h^2), its previous
transported term is
Theta_r-(h/2)partial_r Theta_r+(h/2)Theta_r omega_r+O(h^2).
The first-order defects cancel:

\[
 T_{R_h}(F_h)=\Theta(hx)+O_{C^k}(h^2),\qquad
 Q_h=T_{R_h}(F_h)\eta T_{R_h}(F_h)^T
       =g(hx)+O_{C^k}(h^2).                                 \tag{10}
\]

C^k refers to the smooth interpolating formula with hx replaced by
y. Taylor's integral remainder and
||(I-Z/2)^-1||<=1/(1-||Z||/2) supply uniform constants.
F_h-Theta=O(h); the prescribed inverse bound then gives uniform raw
and centered invertibility, Lorentz signature and orientation for
sufficiently small h. No frequency filter or stationary sheet is used.

For each smooth symmetric V, use the exact smooth straight Gram
pencil Theta_s from `A4D_NATIVE_CENTERED_METRIC_LIFT.md`:
Theta_s eta Theta_s^T=g+sV. Independently take any 24 smooth
eta-skew components W_r and set omega_s=omega+sW. Apply (9).
Uniform parameter differentiation of the same estimates gives

\[
 \partial_s Q_h|_0=V+O_{C^k}(h^2),\quad
 h^{-1}\partial_s R_h|_0=W+O_{C^k}(h).                        \tag{11}
\]

This includes all ten symmetric components with the full Frobenius
pairing (off-diagonal packed dual weight 2), and six independent
generators in each of four link directions. The finite differential
is exactly

\[
 D C_Z[B]=(I-Z/2)^{-1}B(I-Z/2)^{-1}.                          \tag{12}
\]

It is injective and takes the six-dimensional eta-skew space onto
the Lorentz tangent space. Right trivialization by R^-1 is an
invertible coordinate change, so no physical connection row is lost.
The midpoint cancellation holds for these coupled raw/link variations.

Their finite differential is also explicit before taking any limit.
For simultaneous raw and link increments H,K, the actual center is the
quadratic polynomial

\[
 T_{R+tK}(F+tH)=T_R(F)+t\{T_R(H)+M(F,K)\}+t^2M(H,K),\quad
 M(F,K)_r(x)=F_r(x-r)K(x-r,r)/2.                             \tag{12a}
\]

This identity compiles against the literal definition. In particular
discarding the mixed term M(F,K) would use the wrong native variation
map. Link variations must additionally lie in the Lorentz tangent;
(12) constructs all such directions.

The affine translation channel can also be prepared explicitly.
Set E=eta Theta^T and b_h(x,r)=h E_r(hx), where E_r is column r;
then E^T eta E=g. This is a stated integrated-one-form preparation,
not a constitutive equation on all native shifts. Multiplication
of the actual two ordered affine paths gives

\[
 h^{-2}F^{open}_{rs}
   =\partial_r\omega_s-\partial_s\omega_r+[\omega_r,\omega_s]+O(h),
\]
\[
 h^{-2}T^{open}_{rs}
   =\partial_r E_s-\partial_s E_r+\omega_rE_s-\omega_sE_r+O(h).          \tag{13}
\]

Based torsion differs from open torsion by (I-P)b_B=O(h^3), as
required by its existing owner; they are not exactly interchangeable.

## 6. Entry into the probe domain, not native stationarity

Choose omega as the Levi-Civita spin connection of E. The published
finite-probe theorem (same input SHA, explicit certificate prerequisite)
gives O(h^2) in all 24 physical connection Euler rows at
(E(hx),exp(h omega)). Equation (8) changes each link by O(h^3);
(10) changes the physical coframe eta T^T by O(h^2). The finite
local Euler stencil has a mesh-independent sup-norm Lipschitz constant
on this bounded nondegenerate coframe family and near-identity links.
All 24 residuals therefore remain O(h^2) on the **actual corrected
readout**. Principal logs are O(h) and eta-skew; constants are
uniform on the smooth pencil.

Thus native geometric states constructively map into the auxiliary
physical preparation domain with Q_h=g+O(h^2). Its uniform
smooth-family action theorem preserves the physical observable
estimate O(h/epsilon+epsilon^2) at epsilon=h^(1/3). This evaluates
the existing physical naked-star observable on (9). No native action
value is identified with it. The contrast of a different native
action, record/refinement errors and source-subtracted stationarity
still require independent proofs.

The states are not shown to solve native field gates, sourced
physical metric equations or joint matter equations. An O(h^2)
connection residual proves neither native soundness nor recovery.
Arbitrary affine shifts and retained raw null directions cannot
be removed as gauge to manufacture those conclusions. No physical
refinement arrow is selected, and ordinary finite gauge covariance
does not prove the required centered-Cartan/Ward law.

There is also a precise obstruction for a proposed immediate use of this
map. Take the **existing standalone free flux gate**, with the actual
links present as unconstrained spectators; its action is still the
literal §fluxEnergy(e,psi)§ and has no link dependence. The preceding
compiled flux classification gives every pair (e,0) as an exact full
free-field/coframe root, with action and all native first variations
zero. The extra spectator-link variation is zero as well.

Use (9) with Theta=s(y_0)eta,
s=1+cos(2 pi y_0)/10, and its Levi-Civita omega. Every resulting
(e_h,0,R_h) is therefore a genuine root of **that stated levelwise
gate**, and its transported metric tends to the same curved conformal
metric. The already pinned full-curvature calculation gives

\[
 I(g)=-3\int_0^1(s')^2\,dy_0=-3\pi^2/50.
\]

For the straight metric pencil g_t=(1+t)g, scale Theta by sqrt(1+t).
Its Levi-Civita spin connection is unchanged. Formula (9) is linear
in Theta, so the actual readout is exactly Q_h(t)=(1+t)Q_h(0).
At epsilon=h^(1/3), the published physical action estimate and smooth
metric correction imply the physical half-contrast

\[
 \Delta I_h=-\frac{3\pi^2}{50}h^{1/3}+O(h),
 \qquad \Delta I_h^N=0.                                    \tag{14}
\]

For every fixed nonzero calibration, this gap cannot be O(h);
allowed O(h) record/refinement errors cannot cancel its leading term.
Thus adding only the transported readout and unconstrained links does
not repair the standalone flux action. This is a nonempty on-shell
counterexample **for the explicitly stated spectator-link levelwise
class**. Additional native connection equations, matter couplings and
interlevel constraints are outside it. The construction is not asserted
to satisfy them, and no complete-core obstruction follows.

## 7. The specified refinement obstructions survive transport

The previous native scalar-refinement obstruction also survives this
transported readout under the physical near-identity preparation bound.
Test **the same specified componentwise scalar pullback on the full raw
solder F**, without installing it as a physical transition. Let A_I F
denote its ordinary row center, assume ||R_h-I||_infinity<=Ch and
||F_h||_(normalized L2)<=B. Translation preserves each row's counting
norm, so directly from (1),

\[
 \|T_{R_h}F_h-A_I F_h\|_2\le (Ch/2)B,\qquad
 \|Q_h^R-Q_h^0\|_1\le(Ch+C^2h^2/4)B^2.                    \tag{15}
\]

The second estimate uses the previous **global** L2 contraction
||A_I F||_2<=||F||_2 and the Gram product inequality, not a false
pointwise Frobenius contraction. Therefore the transported and ordinary
metric readouts have the same L1 limit. Under the previous exact
composed scalar pullback, the complete smooth nondegenerate limit class
is still constant Lorentz metrics. The bounded-raw approximate extension
with vanishing composed L2 errors retains its bound
dist_L1(g,G_L)<=(2B+rho_L)rho_L after taking the fine-level limit.
Neither raw bounds nor composed consistency is inferred from an
Einstein-contrast estimate.

The same conclusion for the exact scalar arrow needs no uniform B if
only convergence in measure is used: at each fixed coarse level the
previous bulk argument makes F and every backward row equal to one
fixed finite matrix on a set whose measure tends to one; R_h->I
uniformly makes (1) converge there to that matrix. Constant raw fields,
R=I and zero flux fields realize every constant Lorentz metric. This
proves necessity and nonempty sufficiency within the stated class,
without controlling concentrated energy.

For the separate exact graded one-form lift, the full raw solder and
its backward rows vanish on that same bulk, giving Q_h^R=0 there even
with transported links. If that lift is applied to the perturbation,
the raw solder is eta on the bulk; near-identity links then give
Q_h^R->eta in measure. These retain the previous zero/eta limit
classes, either owned normalization and the absence of an L1 or
concentration claim. Alternative physical arrows, macroscopic links
and general approximate graded diagrams remain outside this result.

## 8. Verification and next load-bearing obligation

The capsule compiles 18 new propositions and two existing owner
propositions with standard axioms only. Five printed types expose
the Lorentz-subtype premise and actual recurrence range/kernel
conditions. The analytical results (4)--(13) remain separate.
The certificate independently assembles the entire block operator
on each finite test cycle, checks determinant/rank, actual fibers
and noncommuting order, all ten metric and 24 connection directions,
smooth cancellation, ordered curvature/torsion coefficients and
hostile scope ledgers. There are 162 grouped exact controls and 50
transitive D0 source pins. It uses no numerical SVD for exact rank.
Thirteen false ledgers are rejected: inverse orientation, unrestricted
fiber feasibility, uniform inverse, omitted variation directions,
action/stationarity/refinement promotion, discarded invisible kernel,
centered-Cartan Ward, global GR, the spectator-gate scope and the
specified refinement limit class and false finite joint surjectivity.
The consumed physical certificate was also replayed unchanged for all
24x64 connection coefficients and ten packed metric responses.

The next load-bearing obligation is an existing native action and
its independently derived on-shell equations that actually use
such a geometric readout, with quantitative action/source/refinement
transfer. Kinematic surjectivity does not select that action. The
original #310 fixed-source/raw-owner, #202 full-affine stationary
and #317 complex-stratification terminals, positive GR and global
closure remain OPEN.
