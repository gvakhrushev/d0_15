# Native metric-only compactness and small-link UV resonance

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, existing Draft #310.
Frozen owner input: `af3658e09762860e1e38820fd8bc11de54403cff`.
CONTROL/main baseline: `fa2b04b9c8aae5a0b8470322d6091712ce56567a`.
Status: **closed small centered-gradient compactness theorem and constructive
curved transported-readout sequence, with explicit admission/refinement boundary**.
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

## 7. Verification and the single remaining consumer

The companion [exact checker](certificates/a4d_native_metric_compactness_check.py)
pins the proof, capsule, compiler output, toolchain and all transitive D0
inputs. It verifies the native finite Korn identity, nonlinear inverse,
proper link matrices, literal row-pull center, packed metric, nonzero
curvature, raw norm/product threshold, gauge control and actual refinement
defects. The stored [ledger](certificates/a4d_native_metric_compactness_certificate.json)
is compared in full; false scope extensions are rejected. The recorded
compiler receipt distinguishes the finite propositions from every analytic
continuum or phase-construction step above. The capsule prints 21 propositions
and 13 actual theorem types, with 36 transitive D0 source pins and only
standard axioms. The checker has 171 exact controls; 21 false scope ledgers
and three ledgers falsifying curvature, the raw/link product and the
cochain defect are rejected.

**Closed:** the metric-only loophole for the complete stated small centered-
gradient chart, its product-bounded transported extension, and the alleged
implication from O(h) links or bounded potentials to that extension. The
explicit countersequence proves that last implication false.

**Next single G0 consumer:** derive native admission, the history-to-action
law and commuting refinement on the full raw/transported joint carrier,
and decide whether the displayed resonant states are retained or excluded
by those independently owned laws. Any exclusion needs its own quantitative
raw or refinement consequence; a small-link assumption alone is insufficient.
If retained, prove the action/probe bounds and genuine joint equations,
with the same source and physical readout. This consumes rather than
repeats the supplied-parent classification. No new action, selector or
physical postulate is authorized by this result. All original #310/#202/#317
terminals and the 44 graph node statuses/dependencies remain unchanged.
