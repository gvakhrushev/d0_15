# Native metric-only compactness and small-link UV resonance

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, existing Draft #310.
Frozen owner input: `af3658e09762860e1e38820fd8bc11de54403cff`.
CONTROL/main baseline: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.
Status: **closed small centered-gradient compactness theorem and constructive
curved transported-readout sequence, with a complete stated frozen-coframe
weak-metric-refinement boundary**.
No physical action or gate is selected. G0, positive GR and global closure remain OPEN.

This consumes the metric-only exception in
[dynamical ownership, §6.6](A4D_NATIVE_DYNAMICAL_OWNERSHIP.md#66-every-smooth-strongly-coframe-convergent-flat-orbit-limit-is-flat).
It does not repeat the Fourier rank census. Small native centered gradients
admit a mesh-independent nonlinear inverse estimate. That estimate supplies
the previously unproved coframe compactness from metric convergence alone.
Small transported links without a raw-field bound do not satisfy the same
conclusion: an explicit bounded native potential and O(h) proper Lorentz links
produce a smooth, genuinely curved transported metric limit.

The distinction is material. The constructed metric is the owned transported
readout, not the raw metric of the full joint quotient. The latter diverges
and retains the ultraviolet information. Its coordinate-time component
1+2zeta/h even changes sign; a smooth causal chart for that raw reading
is not supplied. No complete native admission,
physical dynamics, source, Ward identity or coframe refinement of this
sequence has been proved. A curved kinematic limit is not a GR solution.

## 1. Exact owners and conventions

Use the actual periodic `ArchiveRolePhaseGroup N`, L=N+2, h=1/L, with
the required subsequence L in 4N. Fix the order A,B,C,D and the owned
signature eta=diag(1,-1,-1,-1). Role is the dyad product; this explicit order
is a reindexing of its four named values, not an inferred signature datum.
All norms below use ordinary positive Frobenius squares and normalized
h^4 counting on the carrier. Every packed off-diagonal metric slot has weight
two. The Lorentz form is used inside the metric product, not as an energy norm.

| Object | Primary supported owner | Exact input/output used here |
|---|---|---|
| Native potential and raw gradient | `A4DCoframeParentConstraint.forwardGaugeCoframe`, `ArchiveCubicalDifferential.forwardDifference_apply` | e_ra=L(xi^a(x+r)-xi^a(x)) |
| Literal center | `A4DSolderMetricCompletion.centeredCoframeMatrix` | C(e)_ra=(e_ra(x)+e_ra(x-r))/2 |
| Centered derivative | `A4DSymRoleCentralDifference` | D_r=L(U_r-U_r^-1)/2; commutation and skew adjointness |
| Raw/centered metric | `A4DRawSolderFrameAction.rawSolderMatrix`, `A4DSolderMetricCompletion.solderMetric_expand` | F=eta+e; q=(eta+C(e)) eta (eta+C(e))^T |
| Transported center | `A4DRawSolderFrameAction.transportedSolderCenter` | ThetaHat_ra=(F_ra(x)+(F(x-r)R(x-r,r))_ra)/2 |
| Genuine local frame action | `A4DRawSolderFrameAction.transportedSolderCenter_covariance` | F'=F Lambda; R'=Lambda_remote^-1 R Lambda_local |
| Full physical information | [joint quotient](A4D_NATIVE_JOINT_FIELD_QUOTIENT.md) | Raw Gram, dressed links and matter, with constrained variations retained |
| Frozen cochain lift | [native cochain refinement](A4D_NATIVE_COCHAIN_REFINEMENT.md) | Actual B0/B1, composition and degree normalization; not geometric resampling |

The [capsule](certificates/a4d_native_metric_compactness.lean) imports these
actual owners. It proves the finite native identities and inequalities for
every N. Its four-by-four matrix propositions are exact calculations; the
analytic reindexing, even-carrier parity construction and continuum arguments
below are not described as compiled Lean theorems.

## 2. All-size native Korn identity and nonlinear inverse

Write A=C(dForward xi)=D xi and Theta=eta+A. The metric is exactly

    q(A)=eta+A+A^T+A eta A^T.

For any commuting skew-adjoint real differences on the finite carrier,
summation by parts twice gives

    sum_(x,r,a) (D_r xi^a)(D_a xi^r)
      = sum_x (sum_r D_r xi^r)^2.

Expanding the positive Frobenius square yields the exact identity

    ||A+A^T||_h^2 = 2 ||A||_h^2 + 2 ||div_D xi||_h^2.       (1)

The capsule proves both this identity and its binding to the literal native
center. Constants and every Nyquist readout-null potential remain in the
domain. Nothing is declared gauge to obtain (1).

Let A=D xi and B=D psi, with pointwise ||A||_F,||B||_F<=1/4. Set Delta=A-B.
The quadratic metric difference is

    q(A)-q(B)=Delta+Delta^T+E,
    E=A eta Delta^T+Delta eta B^T.

Finite Cauchy-Schwarz gives ||X eta Y^T||_F^2<=||X||_F^2 ||Y||_F^2,
because each signature entry has square one. Thus

    ||E||_h^2 <= 2(1/16+1/16)||Delta||_h^2 = ||Delta||_h^2/4.

Apply ||X+Y||^2<=2||X||^2+2||Y||^2 and (1):

    2||Delta||_h^2 <= 2||q(A)-q(B)||_h^2 + ||Delta||_h^2/2,
    ||A-B||_h^2 <= (4/3)||q(A)-q(B)||_h^2.                  (2)

This is a genuine nonlinear, all-size inverse estimate on the stated native
gradient chart, with no h-loss. It is not an inverse of the joint metric–
connection–matter Euler operator, and it does not apply to arbitrary coframes.

## 3. Metric-only compactness and smooth flatness of the entire small chart

**Theorem.** Let L tend to infinity through 4N, and let A_h=D_h xi_h satisfy
||A_h(x)||_F<=1/4. Suppose the literal q_h=q(A_h), reconstructed as constants
on the standard h-cubes of the unit four-torus, converges strongly in L2 to
a smooth metric g. Then every coframe subsequence has an L2-convergent
subsequence, and g has vanishing Levi-Civita curvature. No coframe
convergence, bound on the raw e_h, or derivative bound on xi_h is assumed.

**Compactness.** Every lattice translate T_k A_h is another native gradient
in the same chart. Equation (2) applies to A_h and T_k A_h. For any real torus
translation z, write z/h=k+alpha with alpha in [0,1)^4. The exact squared L2
translation norm of a piecewise-constant field is the sum of the 16 lattice
translation norms at k+v, v in {0,1}^4, with weights
prod_r alpha_r^(v_r)(1-alpha_r)^(1-v_r). The weights are the volumes of
the corresponding overlaps of h-cubes and do not depend on the field.
Consequently

    ||T_z Theta_h-Theta_h||_2^2
      <= (4/3)||T_z q_h-q_h||_2^2.                          (3)

Since q_h tends to g strongly, the right-hand side is bounded by
(4/3)(2||q_h-g||_2+||T_z g-g||_2)^2. This tends uniformly to zero as z tends
to zero and h tends to zero. The finitely many larger-h fields separately
have L2-continuous translations.

For completeness the compactness step needs no unverified external theorem.
Let E_K u average u on K^4 fixed cubes of side ell=1/K. The variance identity
and the change of variables y=x+z give

    ||u-E_K u||_2^2
      = sum_Q (1/(2|Q|)) int_Q int_Q |u(x)-u(y)|^2 dx dy
      <= 8 sup_(|z|_infty<=ell) ||T_z u-u||_2^2.             (4)

The factors are (2ell)^4/(2ell^4)=8. All E_K Theta_h belong to a bounded
finite-dimensional space. Choose a convergent subsequence successively for
K=1,2,..., and take the diagonal. Equation (4) makes it L2-Cauchy.
Thus Theta_h tends strongly along that subsequence to Theta. The pointwise
chart bound passes to the limit, so sigma_min(Theta)>=3/4; the metric product
converges strongly in L2 because the coframes are uniformly bounded. Therefore
g=Theta eta Theta^T, with a nondegenerate Lorentz signature.

**Closedness.** The actual commuting centered differences imply
D_i Theta_h,ja=D_j Theta_h,ia. Test this identity against a sampled smooth
periodic function and use the owned skew-adjointness. Centered differences
of that test converge uniformly to its derivatives. Passing to the strong
L2 limit proves partial_i Theta_ja=partial_j Theta_ia distributionally.

**Regularity from the smooth metric.** Passing (3) to the limit gives
||T_z Theta-Theta||_2<=sqrt(4/3)||T_z g-g||_2. Difference quotients of Theta
are uniformly L2-bounded since g is smooth. A weakly convergent subsequence
of those quotients, tested by changing variables against a smooth function,
is the distributional derivative; hence Theta belongs to H1. The elementary
weak subsequence construction can be made by diagonal convergence of scalar
products on a countable dense family and the L2 bound.

H1 and the uniform bound permit the product rule for g=Theta eta Theta^T
(mollify locally and pass the products in L1). Closedness and this rule give

    2(partial_i Theta_j) eta Theta_l^T
      = partial_i g_jl+partial_j g_il-partial_l g_ij,
    partial_i Theta_j=Gamma^k_ij(g) Theta_k.                 (5)

Uniform invertibility justifies the second identity almost everywhere.
Its right-hand side is bounded, so Theta belongs locally to W1,infty.
Differentiating (5) weakly bootstraps Theta to W2,infty, and then to arbitrary
regularity since g is smooth. Thus it has a smooth representative. Commuting
two ordinary derivatives in (5) yields Riem(g)^k_lij Theta_k=0. Since Theta
is invertible, Riem(g)=0. This also completes the analytic regularity step
left outside the compiled finite estimate.

The class is nonempty: small smooth periodic potentials sampled on the grid
produce smooth nondegenerate flat limits. A small conformal coframe
Theta=(1+cos(2pi x_A)/10)eta instead satisfies the same pointwise size bound
and has a curved metric, but its columns are not closed and it is not in the
native centered-gradient image. A constant large proper boost has exactly
the flat metric eta while leaving the small chart. These controls prevent
using metric smallness to assert a chart hypothesis or extending the theorem
to the entire joint carrier.

## 4. The precise raw-field condition for transported links

Let F_h=eta+e_h, and let Theta_I be its literal untransported center. The
actual transported owner gives, row by row,

    (Theta_R-Theta_I)_r(x)
      = (1/2) F_r(x-r)(R(x-r,r)-I).

For delta_h=sup_(x,r)||R(x,r)-I||_op, translating each row is norm preserving,
so

    ||Theta_R-Theta_I||_h <= (delta_h/2)||F_h||_h.            (6)

Suppose Theta_I is in the chart of §3, delta_h||F_h||_h tends to zero, and
the transported metric tends strongly in L2 to smooth g. Equation (6) makes
the two coframes L2-close. Their bounded L2 norms make the metrics L1-close.
The untransported metric is uniformly bounded, so its L1 convergence to
bounded smooth g upgrades to L2 convergence. Section 3 now forces g to be
flat. Thus (6) closes the transported extension **under the stated product
condition**. Links O(h) and a uniform raw bound suffice. Links O(h) alone,
or a uniform primitive-potential bound alone, do not imply that condition.

## 5. Bounded native potential, proper small links and a curved metric limit

For every even L define zeta_h(x)=(-1)^(x_A+x_B+x_C+x_D), using integer
representatives. Evenness makes wrapping preserve the sign flip under every
plus or minus unit translation. In particular zeta^2=1 and zeta(x±r)=-zeta(x).
Let v=(1,1,0,0)^T and w=(1,1,1,1)^T. Then v^T eta v=v^T eta w=0. Set

    xi_h^a(x)=-(1/2)zeta_h(x)v_a,
    e_h=dForward xi_h=(zeta_h/h)w v^T,
    F_h=eta+(zeta_h/h)w v^T.                                (7)

The capsule binds (7) to the actual native gradient, given the phase flips.
It also proves that its centered gradient is exactly zero at every site.
The potential is uniformly bounded. Rank-one determinant expansion gives
det F_h=det eta(1+(zeta/h)v^T eta w)=-1; the same identity is compiled.
Normalized raw norm satisfies ||F_h||_h^2=4+8/h^2. These are real native
component fields, not archive coding of a chosen scalar action.

Take the smooth periodic profile f(t)=(2+cos(2pi t))/32, with t=h x_A.
It obeys 1/32<=f<=3/32. Set R_A=R_B=I. Let R_C be the A,D Lorentz boost
with rational Cayley half-parameter -hf, and R_D the A,C boost with parameter
+hf. A boost on a time/space plane has diagonal c=(1+s^2)/(1-s^2), off-diagonal
b=2s/(1-s^2), and identity elsewhere. The capsule proves both Lorentz matrix
identities. The two-by-two determinant is one and c>0 for |s|<1, so the links
are in the proper future component. Here h<=1/4 ensures every denominator
is positive. Their norms differ from identity by O(h), and log(R)/h stays
uniformly bounded and smooth. Affine shifts and matter may be set to zero.

The active boost plane excludes the row of the corresponding link: the
eta part of its incoming row is unchanged. Since f depends only on A,
the profile at the incoming C,D endpoint equals f at the local site.
The literal transported center, proved as a four-by-four identity, is

    a_h=f/(1-h^2 f^2),       b_h=-h f^2/(1-h^2 f^2),
    ThetaHat_h = [ 1  0     0          0;
                   0 -1     0          0;
                zeta b_h 0 -1      zeta a_h;
                zeta b_h 0 -zeta a_h   -1 ].               (8)

Its determinant is -(1+a_h^2), everywhere nonzero. Its exact Gram is

    qHat_h = [1 0 zeta b_h zeta b_h;
              0 -1 0 0;
              zeta b_h 0 -1-f^2/(1-h^2 f^2) b_h^2;
              zeta b_h 0 b_h^2 -1-f^2/(1-h^2 f^2)].         (9)

All 16 entries of (8), all ten packed entries and their weights in (9), raw
and centered determinants, signs and denominators are checked exactly.
In particular qHat_h tends uniformly, including the sampling error O(h), to

    g=diag(1,-1,-1-f(t)^2,-1-f(t)^2).                       (10)

ThetaHat_h converges weakly to eta but not strongly: opposite grid-cell
pairs cancel zeta against every smooth test, while
lim ||ThetaHat_h-eta||_2^2=2 int_0^1 f(t)^2 dt=9/1024.
Despite its small pointwise coframe perturbation, (8) is not a centered
gradient when the links are nontrivial; the hypothesis of (1) fails.

This is a genuinely curved metric. With the convention
R^rho_sigma mu nu=partial_mu Gamma^rho_nu sigma-partial_nu Gamma^rho_mu sigma
+Gamma^rho_mu lambda Gamma^lambda_nu sigma-Gamma^rho_nu lambda Gamma^lambda_mu sigma,
put a(t)=sqrt(1+f(t)^2). Direct Christoffel calculation gives
Ric_AA=-2a''/a and G_BB=-2a''/a-(a'/a)^2. At t=0,
f=3/32, f'=0, f''=-pi^2/8, so both equal 24pi^2/1033, nonzero.
The certificate evaluates the complete ten Einstein components and the
curvature tensor from that convention at the indicated jet. Metric (10)
is therefore not a vacuum Einstein solution; no native source is fitted.

The construction violates the product condition exactly. The maximum link
operator norm delta_h is 2h f_max/(1-h f_max). Hence

    lim (delta_h ||F_h||_h)^2=32 f_max^2=9/32,               (11)

not zero. With e=0 the same two links leave the centered metric exactly eta;
the curved reading comes from their interaction with the raw Nyquist field.
The raw Gram F_h eta F_h^T depends on zeta at order 1/h and is Lorentz gauge
invariant. Consequently the UV field is not removable by a genuine local
Lorentz frame change. The active boost generators do not commute: a C,D
plaquette is nonidentity even for constant nonzero f. Response-null at one
background does not mean gauge or null on this background.

This gives a nonempty native *kinematic* realization of a curved transported
reading. The [complete joint quotient](A4D_NATIVE_JOINT_FIELD_QUOTIENT.md)
retains the raw metric and dressed links, with constraint D q_target D^T=q_source.
When one replaces the raw coordinate q by qHat, the owned transformation
qHat=B q B^T and its inverse constraint must still be imposed. This example
does not show a smooth full raw quotient, a uniformly regular change of
those coordinates, or the native action/probe estimates. Zero matter solves
only the supplied homogeneous mixed-parent field equations; it does not
certify the independently owned geometric equations. No physical root or
source-subtracted stationarity is inferred from (7)–(11).

## 6. Exact link bonding, and the separate native coframe-refinement defect

There is an exponential companion to avoid mistaking the rational link
bonding defect for a necessary obstruction. Use R_C=exp(-2hf K_AD),
R_D=exp(2hf K_AC), with K the unit boost generators. Equation (8) then uses
a_h=sinh(2hf)/(2h), b_h=(1-cosh(2hf))/(2h); its Gram has the same smooth
limit (10) and O(h) error. At the doubled even carrier, each coarse C,D edge
is exactly the product of its two fine edges, since f is constant along
these edges. A,B links are identity. Exp(uK)exp(uK)=exp(2uK) proves this
identity; expanded path words follow by associativity. This statement uses
geometric edge subdivision. It does not identify that subdivision with the
frozen archive lift. The rational Cayley companion has a generally nonzero
O(h^3) two-edge defect, checked separately.

Even exact link bonding does not provide coframe or potential bonding.
Under geometric vertex decimation x->2x, xi_(2L)(2x)=-v/2 is constant,
whereas xi_L(x)=-zeta_L(x)v/2. Their normalized squared discrepancy is
exactly one for every even L. A,B components both contribute.

Under the *actual* adjacent frozen B0, an even Nyquist phase at size L is
copied at the first L vertices and takes value one on the appended vertex.
The collapsed edge joins equal phases; the plus-flip law fails there. At
size L+1 its scaled centered phase derivative has magnitude L+1 at the two
seam vertices and zero elsewhere. In four dimensions take the tensor phase
and the same two-component potential. Its normalized squared centered-
gradient norm is exactly 4(L+1) (eight component/row contributions times
the one-dimensional phase derivative variance and the factor 1/4).

Compose the frozen lifts to K=2L as in the owned refinement theorem. Each
one-dimensional phase is old parity on i<L and constant one on i>=L;
their product is the lifted four-dimensional phase. For L>=4 even, its
centered phase derivative has magnitude K at the two parity/tail interfaces
and vanishes elsewhere. The normalized squared centered-gradient norm
of the lifted potential is exactly 4K=8L, rather than zero for the freshly
constructed even-carrier Nyquist potential. The degree-aware B1 scaling
is consistent with dForward of that lifted potential, so it cannot repair
this centered-readout discrepancy by dropping the normalization. The finite
certificate checks the actual adjacent and composed matrices, including all
wrap and collapsed edges. These are state/readout defects, not a claim that
the entire sequence violates a separately supplied physical refinement rule.

Thus a smooth resampling map, bonded connection words, a bounded primitive
potential and a per-level raw gradient are four distinct facts. The existing
native interlevel arrow must determine which of them is physically admitted.
Neither a new coframe lift nor an unproved removal of the raw UV sector is
introduced here. O(h) metric corrections are allowed by the new positive
criterion but do not close #310's original fixed-source/raw-owner task.

### 6.1 Complete frozen-coframe refinement class and its metric boundary

This consumes the actual composed maps in
[native cochain refinement, §5](A4D_NATIVE_COCHAIN_REFINEMENT.md#5-one-step-estimates-and-composed-fixed-torus-failure).
The precisely stated candidate diagram is the coordinatewise frozen map,
its actual composition, the degree-one normalization K/L and fixed-torus
placement x/K. All sixteen raw entries and internal columns are retained.
The earlier [centered-lift boundary](A4D_NATIVE_CENTERED_METRIC_LIFT.md#the-owned-graded-one-form-lift-is-a-different-candidate)
already gives zero/eta limits in measure for exact iterates from one fixed
coarse field; that theorem is reused. The new consumer below covers changing,
arbitrarily large coarse fields, role-dependent transported links, complete
Lorentz gauge and composed weak metric probes with vanishing metric errors.
For **every** coarse coframe e_L, with no size or gradient-image restriction,

    (P1_(K<-L)e_L)_ra(x)=(K/L)1_[x_r<L]e_L(c_L(x))_ra,
    c_L(j)=j if j<L, and 0 otherwise.                      (12)

This is B1 in direction r and B0 in the other directions. The existing
all-grade tensor composition proof gives (12) for every K>=L; a single
modulo map would be different. The capsule's `frozenNativeCoframe` uses
these coordinates through the actual point/group equivalence, and
`frozen_native_tail_zero` binds its zero rows to `rawSolderMatrix`.
The tensor-composition assembly remains the consumed analytic proof,
not a newly supported physical-state owner.

Two interpretations of the linear map have different immediate failures.
Applied homogeneously to the whole F, it makes every row zero wherever
all x_r>=L. Its raw determinant is zero, already at the all-L point of an
adjacent step. Thus even a constant nondegenerate coarse raw field is sent
outside the full nondegenerate carrier. Links, shifts, matter and Lorentz
frames cannot repair a zero raw determinant.

Applied instead to the existing perturbation e=F-eta, it gives F_fine=eta+P1 e.
This affine proposal also fails to preserve the **whole** nondegenerate
kinematic carrier: at K=2L take coarse F=eta/2, e=-eta/2. On the prefix cube
x_r<L every row factor is two, so fine F=0, although coarse det F=-1/16.
For any K>L the same witness is e=-(L/K)eta, coarse F=(1-L/K)eta.
The doubling matrix statement is compiled as
`affine_frozen_doubling_degeneracy`. These are input-state preservation
facts, not purported on-shell counterexamples. A derived admissible subset
could exclude those coarse states, but the linear chain theorem does not
supply that subset or a full joint transition.

For the affine perturbation proposal let
B_(L,K)={x:L+1<=x_r<K for all four r}. Its exact size is (K-L-1)^4 for
K>=L+1. At x and every actual incoming neighbor x-r, (12) is zero in every
row, so the raw field is eta there. Let arbitrary comparison links R_(L,K)
have delta_(L,K)=sup_(x,r,a,b)|(R_(L,K)(x,r)-I)_ab|. The actual center yields

    H_ra=(ThetaHat-eta)_ra
        =eta_rr(R_(L,K)(x-r,r)_ra-I_ra)/2,
    |H_ra|<=delta/2,
    |(qHat-eta)_ra|<=delta+delta^2,
    ||qHat-eta||_F<=4(delta+delta^2) on B_(L,K).             (13)

Proof: qHat-eta=H+H^T+H eta H^T; the quadratic entry has four terms,
each bounded by delta^2/4. The native center identity, entry bound and full
Gram expansion/bound are compiled. This retains all 24 Lorentz link
directions; it even holds for arbitrary linear matrices. Proper O(1/K)
comparison links suffice. Their small chart is an explicit hypothesis,
not something derived from physical equations. Affine shifts and every
matter grade are retained and do not enter this particular metric owner.

**Complete weak-metric class.** Let metrics qHat_K of native kinematic states
converge against all smooth periodic metric tests to smooth nondegenerate g.
For each fixed integer rho>=2, K=rho L, L in 4N, form a comparison raw
field eta+P1 e_L and some comparison links with delta_(L,K)->0. Its metric
owner is defined even without raw invertibility; calling it a full native
state additionally requires that independent admission check. Require only

    K^-4 sum_x chi(x/K)[qHat_K-qHat_(L,K)^comparison]_ra->0  (14)

for every fixed smooth chi supported compactly in T_rho=(1/rho,1)^4 and
each metric slot. Include any recording/reconstruction errors used to assert
(14). An unbounded set of fixed rho suffices. No raw or coframe closeness,
uniform inverse-B bound, exact field equation or fitted source is assumed.

For large L every tested point lies in B_(L,K). By (13), the comparison
pairing tends to eta_ra integral chi. Metric convergence and (14) imply
integral chi(g_ra-eta_ra)=0. Hence smooth g=eta on T_rho. The union over
unbounded rho covers all points with positive coordinates; continuity extends
the equality across coordinate subtori. Therefore **g=eta everywhere and
its Levi-Civita curvature vanishes**. This is an analytic all-size theorem
for every coarse coframe and comparison link in the declared class.
One rho=2 gives only g=eta on T_2, not global flatness: a smooth metric
perturbation supported in the first temporal quarter can be curved elsewhere.
Adjacent errors do not establish the required composed intervals.

For the homogeneous raw-F interpretation, both raw field and transported
center are zero on B_(L,K), for any links. One such weak interval forces
g=0 on an open set, contradicting nondegeneracy. Its finite raw-state
failure already occurs earlier.

The metric conclusion survives the **complete** owned local Lorentz action:
transform the whole raw solder and incoming links together. The actual center
then obeys ThetaHat'=ThetaHat Lambda and qHat'=qHat. This owner-bound
invariance is compiled for arbitrary site frames. A coframe-only change is
not that gauge action. Reconstructing another fine state after a frame change
requires its own transition law. No affine-origin or coordinate gauge is
provided or removed here; the complete raw Gram, dressed links, shifts and
exterior matter remain in the joint quotient.

**Existing curved resonance at one doubled interval.** Use the §5 fine
links at K=2L for the comparison of (12). Their boost planes exclude the
incoming row, so its metric is exactly eta on B_(L,2L). The actual resonance
has CC and DD differences both -f(x_A/K)^2/(1-K^-2 f(x_A/K)^2). Since
f>=1/32 and the denominator lies in (0,1],

    ||qHat_(2L)^resonance-qHat_(L,2L)^comparison||_h^2
       >=2((L-1)/(2L))^4/32^4,
    liminf ||difference||_h^2>=1/8388608>0.                (15)

Here the comparison really is a nonempty full **kinematic** raw/link state:
its raw field is eta+K zeta(c_L(x)) w_mask v^T, with
(w_mask)_r=1_[x_r<L]. Its determinant is
-1-K zeta(c_L(x))((w_mask)_A-(w_mask)_B), never zero for K>=4.
The fine links are proper; affine shifts and every matter component may
be retained independently. All sixteen masks are exactly checked.
Neither member is asserted to solve the unowned physical Euler equations.

The scalar gap inequality is compiled. Arbitrary comparison links with
delta_(L,2L)->0 change the bulk norm by a quantity tending to zero, by (13),
so the same liminf remains. Normalized L2 metric correctors tending to zero
cannot remove it, by the triangle inequality. No raw-corrector bound is
inferred from a small metric corrector.

Choose any fixed smooth nonnegative nonzero chi with support inside
(5/8,7/8)^4. Its support lies in B_(L,2L) for L>=4. Testing the sum of CC
and DD differences gives the limit

    -2 integral chi(y) f(y_A)^2 dy
       <=-(1/512) integral chi<0.                         (16)

Thus the resonance fails even one doubled weak interval (14). Arbitrary
small comparison links, complete Lorentz gauge and vanishing weak recording
or metric errors preserve this defect. The exponential companion has the
same metric limit and conclusion. Without small comparison links a proper
constant boost gives a nonflat transported bulk metric; that hypothesis
cannot be discarded.

**Decision at this full specified interface:** frozen one-form refinement,
fixed-torus placement, small comparison links and composed weak metric
compatibility exclude the displayed curved resonance; all unbounded fixed
ratios exclude every smooth curved metric limit. This is an exhaustive
boundary of the stated diagram/readout class, not an added admission gate
or a whole-core NO-GO. An independently owned field-dependent reconstruction,
another diagram/readout or non-small comparison links requires its own law.
No replacement transition, action, source or postulate is introduced.

Equations (14)--(16) concern **metric readout**. They neither follow from
nor replace the calibrated O(h) source-subtracted **action** contrast on a
different observable. A claimed factorization needs proof. Full physical
admission into D0, own dynamics and #310's fixed-source/raw terminal remain
open. The next preparation/composition law must explicitly address this
state-domain and metric-refinement boundary.

### 6.2 Full Lorentz-orbit obstruction and complete affine raw intertwiners

Section 6.1 tests the refinement domain and its metric limit. There is a
separate obstruction even on an arbitrarily small **proper gauge orbit of
the flat state**. No curved root, equation, source or admitted physical
selector is assumed in this test. The candidate is still the existing
composed frozen one-form block, interpreted as refinement of e=F-eta.
The required covariance is preservation of the actual raw-solder Lorentz
orbits. It is necessary for a full-state transition on the existing joint
quotient; a different weaker physical reading has its own proof obligation.

Write p(x)=c_L(x), rho=K/L and d_r(x)=rho*1_[x_r<L]. The literal owner gives

```text
F_f(x)=eta+diag(d(x))*(F_L(p(x))-eta).                   (17)
```

This full sixteen-entry binding is compiled as
`frozen_native_pointwise_affine_binding`. Occupancy is an external row
weight; internal frame columns are all retained.

**An exact nonempty gauge test.** Let Lambda(u) be the constant proper
rotation of the internal B,C plane, fixing A,D, with its spatial block

```text
[ c(u)  s(u) ],   c(u)=(1-u^2)/(1+u^2),
[-s(u)  c(u) ],   s(u)=2u/(1+u^2).
```

The coarse states F_L=eta and F_L=eta Lambda(u), with identity links,
zero shifts and zero sixteen-component matter, are related by the owned
full raw/link/matter node frame action. The constant conjugation leaves
identity links unchanged. Both raw and transported coarse Gram metrics are
exactly eta, and their raw determinants are -1. The rotation has determinant
one and future component one; it is connected to identity for every small u.
This is a full kinematic gauge test, not an assertion of a native physical root.

The two active rows of (17) have the exact form

```text
F_BB=-1+d_B*(1-c),    F_BC=-d_B*s,
F_CB=d_C*s,           F_CC=-1+d_C*(1-c).
```

Direct multiplication, with no expansion or smallness approximation, gives

```text
(F_f eta F_f^T)_BC=(d_C-d_B)*s.                         (18)
```

At a fine point with x_B<L and x_C>=L this is -rho*s, whereas the
refinement of F_L=eta has raw Gram eta. Such points exist already at
K=L+1. Therefore the two refined fields cannot be related by **any** fine
Lorentz frame: raw Gram is invariant under the entire owned frame action.
No choice of fine links, shifts or matter can erase this raw invariant.
This is stronger than failure of the guessed pulled-back frame law.

These are nondegenerate full fine states for sufficiently small nonzero u.
The four B,C occupancy sectors have raw determinants respectively

```text
-1,    -1+rho*(1-c),    -1+rho*(1-c),
-[1+2*rho*(rho-1)*(1-c)].                               (19)
```

For any fixed rho>1, (2*rho-1)*u^2<1 suffices. All remaining rows are
unchanged. Thus excluding singular states or requiring a small neighborhood
of flatness does not remove (18). A gauge-saturated admitted neighborhood
containing the flat state cannot use (17) as a full quotient transition.
Gauge fixing before applying (17), or admitting only one representative,
would require an independently owned preparation and transition law.

**Entire first-jet class, including nonlinear completions.** For any raw
Lorentz tangent A, put S=eta*A; the Lorentz equation gives S^T=-S.
Conversely every antisymmetric S is obtained from A=eta*S and has a proper
Lorentz one-parameter curve. At the flat raw field, the metric derivative
of eta+t*H is H+H^T. A proposed row-weighted first derivative H=diag(d)*S
therefore gives the complete gauge metric jet

```text
(delta q)_ra=(d_r-d_a)*S_ra.                           (20)
```

It vanishes for **all six** independent internal Lorentz directions iff
all four d_r are equal. Necessity follows by the elementary antisymmetric
matrix in each pair; equality of the row weights is sufficient by
antisymmetry. This all-size equivalence and the genuine raw Gram derivative
are compiled. In every partial prefix mask of (17) the row weights are
unequal. For the B,C rotation at a B-only mask, (18) has genuine derivative
-2*rho at u=0.

Consequently no differentiable full-state refinement with flat raw output
eta and **this same full coframe first derivative on the stated gauge
curve** can preserve the coarse Lorentz orbit. This includes nonlocal,
link-dependent or nonlinear completions with an o(u) raw correction at
that fine point. The scalar raw Gram derivative is still -2*rho; a curve
inside one fine Lorentz orbit has identically zero metric derivative.
`nonzero_metric_jet_not_orbit_constant` checks the local derivative argument;
no zero totalized derivative is substituted for a genuine derivative.
A correction of order u, a different first jet, raw reconstruction or a
new gauge law is outside this class and must have its own native owner.

**The discrepancy survives composed metric observations.** For K=rho L
with fixed integer rho>=2, the two partial occupancy regions each occupy
fraction (L/K)*(1-L/K). Equation (18) gives the exact raw packed-norm bound

```text
K^-4 sum_x ||q_f^rot(x)-q_f^flat(x)||_F^2
  >= 4*(rho-1)*s(u)^2.                                (21)
```

The factor two for the symmetric BC slot is retained. All fine states are
nondegenerate under (19). For identity fine links, the literal transported
center equals the same constant masked raw field away from the B,C prefix
boundaries. Restricting to 1<=x_B<L, L+1<=x_C<K and the reversed region
preserves both actual incoming active rows. The other two coordinates are
unrestricted. Their exact total cardinality is
2*(L-1)*(K-L-1)*K^2, giving the transported lower bound

```text
4*rho^2*((L-1)*(K-L-1)/K^2)*s(u)^2
  -> 4*(rho-1)*s(u)^2 > 0.                             (22)
```

For rho=2,u=1/16 the limit lower bound is 4096/66049. This is a
**refinement covariance** discrepancy between two gauge-equivalent coarse
flat states, not curvature of a physical fine solution. On each fixed-ratio
family the raw fields are bounded, so arbitrary proper comparison links
with sup|R-I|->0 change the transported metric by o(1). Vanishing normalized
L2 metric recording/correction errors cannot remove (22). A fixed smooth
nonnegative probe supported inside x_B in (0,1/rho), x_C in (1/rho,1)
also has BC pairing limit -rho*s(u)*integral(chi), which is nonzero. One
adjacent step can have a small volume norm even though it already fails the
exact orbit law; composed fixed ratios cannot be inferred from that error.

**Complete affine alternative, with no selected replacement lift.** Fix a
finite coarse-to-fine vertex map p. Consider *all* real affine maps from
all coarse raw matrix entries to fine raw entries, independent of links,
shifts and matter. Require covariance under every independent proper
coarse Lorentz node frame, with fine frame Lambda(p(x)). The whole class is

```text
T(F)(x)=C_x*F(p(x)),                                  (23)
```

with arbitrary real 4x4 C_x. Here is a complete proof. Expand an affine map
into its bias and linear coefficients for each input site and row. Affine
identities valid on the open product of nondegenerate raw matrices extend
to all entries. For y!=p(x), varying only the frame at y forces every input
covector coefficient to be fixed by all proper Lorentz matrices, hence zero.
For y=p(x), each output-row/input-row coefficient is a 4x4 commutant of the
standard Lorentz representation, hence a scalar multiple of identity. The
bias is also a fixed row covector and is zero. These scalars form C_x.
Conversely (23) is covariant under every node frame.

No unproved representation theorem is needed for those two finite facts.
The three proper spatial half-turns have distinct sign characters on A,B,C,D,
so a commuting matrix is diagonal. The three proper rational boosts in AB,
AC,AD force its four diagonal values to agree. A row fixed by the half-turns
has only its A entry left, and any one of those boosts kills that entry.
Thus this finite set is already sufficient; scalar matrices and zero rows
satisfy the entire group requirement. Exact controls certify commutant
rank 15, fixed-row rank 4, and the 16-dimensional full raw intertwiner space.
This is an analytic universal proof, not a numerical-rank extrapolation.

The class (23) preserves **every** nondegenerate coarse raw field iff each
C_x is invertible. Requiring the fixed raw reference eta to map to eta
forces C_x=I, hence the unique affine map in this precisely stated class is
raw B0 pullback. For a composed family the full law is
C_(K,M)(x)=C_(K,L)(x)*C_(L,M)(p_(K,L)(x)); reference preservation fixes all
these factors to identity. Raw B0 pullback, however, is not the exact
scale-corrected one-form chain block. Already at the newly added point of
an adjacent cycle, the forward difference of B0 f is zero while B0 of the
coarse forward difference can be nonzero. Exact controls retain this
counterexample and the true B1 chain identity. Formula (23) is a
classification, **not a replacement arrow introduced into D0**.

The result closes the complete fixed-background frozen row-jet orbit class
and the complete affine connection-independent intertwiner class. It does
not exhaust nonlinear maps with a different first jet, covariant link
reconstruction, a different diagram/readout, constraints with an owned
gauge preparation, or all native dynamics. Lorentz naturality alone does
not select an action, source, Ward identity, independent physical gate,
curved solution, action-contrast transfer, soundness or recovery. G0/GR and
all original parent terminals remain open. The single next owned
history/preparation/composition law must now account for this gauge-orbit
failure as well as the earlier state-domain and weak-metric boundary.

### 6.3 Exact admission boundary without a flat-state or open-domain premise

The previous flat orbit is an explicit nondegenerate test, but it leaves a
logical question: could a sparse, nonlinear or isolated physical root class
avoid that orbit and make the **same literal transition (17)** descend to
the full raw Lorentz quotient? The answer is no for **every nonempty
nondegenerate full-state class closed under the owned proper frame action**.
No equation, source, weak metric limit, link smallness, differentiability,
flat state or open admission neighborhood is needed for this statement.
This resolves admission for this specified raw transition, rather than
constructing or excluding the other native transitions.

At every strict refinement K>L, take a fine point with x_B=0, x_C=L and
x_A=x_D=0. It is an actual fine phase point, even for K=L+1. The B row
weight in (17) is rho=K/L>0 and the C row weight is zero. The other row
weights are irrelevant. For an **arbitrary** coarse raw matrix F at p(x),
not the flat representative, the exact fine raw Gram component is

```text
q_f(F)_BC = rho F_BC,
q_f(F Lambda)_BC-q_f(F)_BC = rho [(F Lambda)_BC-F_BC].   (24)
```

Indeed the inactive C row is the fixed eta row, so its metric pairing
selects the C column of the active B row. This is compiled as
`frozen_partial_metric_reads_any_raw_row`; the strict-refinement point
exists at every native size by `native_partial_mask_exists`. The already
compiled full sixteen-entry binding to (17) remains the consumed owner.
The actual `rawFullSolderFrameAction_matrix` acts on the entire raw matrix
F by right multiplication, including its background, rather than acting
only on its perturbation coordinates.

Here is a finite complete test of (24). Write w_a=F_Ba. Use the two B,C
rotations with sine +s and -s, the A,C boost, and the C,D rotation with
sine s. For any 0<t<1 put

```text
c=(1-t^2)/(1+t^2),  s=2t/(1+t^2),
ch=(1+t^2)/(1-t^2), sh=2t/(1-t^2).
```

All four matrices are connected proper Lorentz matrices: their Lorentz
identity, determinant one and future component hold along the continuous
curves from t=0. Constancy of (F Lambda)_BC for these four frames gives
exactly the four independent equations

```text
 s w_B+(c-1)w_C=0,       -s w_B+(c-1)w_C=0,
sh w_A+(ch-1)w_C=0,     (c-1)w_C-s w_D=0.              (25)
```

Adding and subtracting the first two equations forces w_C=w_B=0, since
c-1 and s are nonzero. The last two then force w_A=w_D=0, since sh and
s are nonzero. Thus the entire B row is zero and det(F)=0. Conversely a
zero B row passes this single-component test, which is why the actual
nondegeneracy hypothesis is retained. No finite-rank extrapolation or
generic/open-set argument is used: the four displayed equations prove the
implication for **every** real F.

The fixed t=1/16 instance is compiled as
`four_proper_frames_force_raw_row_zero` and
`nondegenerate_raw_orbit_has_frozen_metric_defect`. Its constants are
c=255/257, s=32/257, ch=257/255 and sh=32/255. The checker also verifies the
symbolic determinant and all proper-group properties, and supplies exact
nonzero-row controls when any one frame is omitted. The argument works
for arbitrarily small nonzero t; it is not dependent on that finite test
radius or on the conditioning of F.

**Full admission theorem.** Let X be any stated full-state carrier, with
arbitrary links, affine shifts, all matter grades, constraints and other
data. At the chosen coarse point let raw:X→Mat(4,R) be its actual raw
solder. Let A⊆X satisfy the following three hypotheses, without inserting
any stationarity conclusion into its definition:

1. A is closed under the owned proper full-state frame changes, whose raw
   binding is raw(act_Lambda x)=raw(x)Lambda.
2. Every x∈A has det(raw(x))!=0.
3. A proposed full refinement has precisely the literal raw block (17),
   and sends gauge-related admitted coarse states into one fine raw
   Lorentz orbit.

Then **A is empty**. If x∈A existed, gauge closure admits all four frames
above. Fine orbit descent requires equality of their fine raw Gram BC
entries, by the owned raw Gram invariant. Equations (24)--(25) imply a
zero coarse B row, contradicting hypothesis 2. The generic full-state
statement is compiled as `frozen_gauge_saturated_admission_empty`, with
raw binding, gauge closure, nondegeneracy and the necessary fine metric
invariance printed explicitly as premises. The primary raw frame owner
supplies the binding when this theorem is applied to the existing joint
carrier; the preparation/admission of a physical X remains independent.

This excludes restricting (17) to an isolated or nonlinear on-shell subset
as a repair **when that subset must respect the complete owned gauge**.
It does not assume that any particular state is a physical root. If some
gauge representative instead has a singular fine output, refinement
already fails its state-domain requirement; if all outputs are valid,
their raw Gram defect rules out every fine Lorentz frame. Arbitrary fine
links, shifts and matter cannot alter this raw invariant. The nonempty
all-mask coarse/fine flat controls in §6.2 are retained, so the conclusion
is not obtained from a vacuous comparison fiber.

Selecting one raw representative before applying (17) changes hypothesis
1 and needs its own derived gauge preparation/reconstruction. A different
raw law changes hypothesis 3. Homogeneous full-raw B1 prolongation avoids
the fixed affine bias but has a zero C row at the same fine point, hence
never preserves a nondegenerate full raw state. Together these statements
exhaust the two **explicitly stated** full-raw and fixed-reference
perturbation interpretations of this composed frozen block. They do not
exhaust the entire native core, other diagrams/readouts, link-dependent
reconstructions or nonlinear raw laws with a different first jet.

**Next consumer:** an owned history/preparation/composition law must
therefore supply a different full gauge-compatible transition, or derive
the gauge preparation that changes this admission problem. It cannot
repair the literal block solely by restricting to a gauge-closed set of
solutions, changing fine links or removing nongauge response-null modes.
No replacement action, lift, selector or physical postulate is installed.
G0, own source/Ward, action-contrast transfer, curved joint roots,
soundness/recovery, positive GR, global closure and the original parent
terminals remain open.


## 7. Verification and the single remaining consumer

The companion [exact checker](certificates/a4d_native_metric_compactness_check.py)
pins the proof, capsule, compiler output, toolchain and all transitive D0
inputs. It verifies the native finite Korn identity, nonlinear inverse,
proper link matrices, literal row-pull center, packed metric, nonzero
curvature, raw norm/product threshold, gauge control and actual refinement
defects. The stored [ledger](certificates/a4d_native_metric_compactness_certificate.json)
is compared in full; false scope extensions are rejected. The recorded
compiler receipt distinguishes the finite propositions from every analytic
continuum or phase-construction step above. The capsule prints 45 propositions
and 37 actual theorem types, with 36 transitive D0 source pins and only
standard axioms. The extended checker has 593 exact controls, including
all composed graded rows, full-carrier preservation failures, the flat bulk,
complete Lorentz gauge and nonempty resonant comparison. Forty-one false
scope ledgers and thirteen falsified exact-result ledgers must be rejected.
The all-ratio and fixed-smooth-test limit arguments are analytic, not
compiled continuum theorems. The full affine intertwiner classification
is analytic; the exact proper group witnesses force its full commutant and
fixed-vector claims. The new proper gauge curve and its nonzero metric jet
have genuine compiled derivatives, including the local nonconstancy test.

**Closed:** the metric-only loophole for the complete stated small centered-
gradient chart, its product-bounded transported extension, and the alleged
implication from O(h) links or bounded potentials to that extension. The
explicit countersequence proves that last implication false.
Section 6.1 adds the full frozen-coframe state-domain and weak-metric
boundary. Its curved-resonance gap persists under complete Lorentz gauge,
arbitrary small comparison links and vanishing metric correctors.
Section 6.2 additionally excludes every differentiable completion retaining
the frozen row first jet on the flat gauge orbit, and completely classifies
the specified affine raw intertwiners. Fine Lorentz frames and links cannot
remove the raw Gram defect. Section 6.3 completes admission for the literal
fixed-reference raw block: every nonempty nondegenerate gauge-closed
full-state class fails its quotient law, including isolated or nonlinear
solution classes. The hypothesis is the full raw quotient, not an unproved
weak physical readout or selected preparation.

**Next single G0 consumer:** derive native admission, the history-to-action
law and commuting refinement on the full raw/transported joint carrier,
and decide whether the displayed resonant states are retained or excluded
by those independently owned laws. The full frozen one-form/small-link
weak-metric class is now excluded quantitatively; it must not be reused as
the unproved physical arrow. Any other exclusion or retained preparation
needs its own quantitative law; a small-link assumption alone is insufficient.
If retained, prove the action/probe bounds and genuine joint equations,
with the same source and physical readout. This consumes rather than
repeats the supplied-parent classification. No new action, selector or
physical postulate is authorized by this result. All original #310/#202/#317
terminals and the 44 graph node statuses/dependencies remain unchanged.
