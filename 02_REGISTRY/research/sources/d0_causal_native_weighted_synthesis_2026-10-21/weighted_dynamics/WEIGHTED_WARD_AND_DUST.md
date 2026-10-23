# Actual PF weights: exact weighted Ward reduction, dust realization, and the original metric

21 October 2026. Bounded continuation of existing research owner #334.
Input repository: `gvakhrushev/d0_15`, commit
`086fab99d8aaed7f712e9a3d2858c516b61901fc`.
This note changes the missing weight input of the existing density-rigidity
application. It does not introduce another action, measure, density dressing,
paid operation or physical metric readout. The exact finite normal form is
consumed; the continuum Ward application is identified separately.

## 1. Precise new consumer and conclusions

The actual independently implemented cap-one CQ programme has the supplied
complete field-dependent price

    S_h = B0 + M sum_z rho_z F(tau fhat_z/rho_z,
                              tau qhat_z/rho_z),
    M>0, tau>0, rho_z>0.                                      (1)

The positive rho_z are the actual fixed PF/trace-count weights. They are not
Born probabilities to be chosen. The old continuum density-rigidity proof
used F(tau eR,-tau q) with a constant outer measure and did not establish its
Ward identity for (1). The supplied universal stationary normal form DOES
already apply exactly to (1), including its inverse-PF nonlinear vertices.

Here are the new consequences for the continuum version with those actual
weights retained as an arbitrary prescribed smooth positive function rho:

* The correct weighted full-field Ward identity is
  d(F-x F_x)+y F_y dlog(rho)=0, not d(F-x F_x)=0.
* Together with the genuine local coframe-scale equation, it gives
  d[rho y/F_x]=0. Under the already-owned stationary coframe map this is
  exactly d(q_tilde)=0. The two original operands need not be constant.
* The full reduced equations are ordinary Einstein equations with an
  undensitized gradient source and its genuine scalar-current equations.
  One timelike scalar gives irrotational positive dust, with the exact
  prescribed mass-coordinate law in (17) below.
* Every local positive irrotational Einstein-dust geometry has a reduced
  representative for EVERY prescribed smooth positive rho, on a small
  common operand chart. A time-dependent spatial Jacobian constructs it;
  its induced shift is retained explicitly.
* The original operational metric is its determined conformal image.
  Its torsion and extra metric terms are explicit, generally nonzero, and
  cannot be removed by calling the transformation a physical gauge choice.
  In the null sector the map is identity, for arbitrary rho.
* At every such background, the full coupled fixed-collar Jacobi kernel
  equals that of the affine Palatini action with the ACTUAL spatially
  varying material slope frozen at that background. This does not replace
  that slope by the constant J2 slope or identify off-shell Hessians.

The finite action (1) has no automatically available continuum Lie/Ward
identity. Section 9 gives its exact remaining substitution, rather than
silently promoting this continuum theorem to a finite-lattice proof.

## 2. Actual price, sign convention and density types

Use the exact F from
`sources/d0_primary_normal_source_recovery_2026-10-21/constitutive/CONSTITUTIVE_COMPOSITION.md`:

    F(x,y)=-alpha beta [h_phi(r(x,-y))-h_phi(r(0,0))].

Thus the source orientation sigma=-1 is INSIDE F. In this note y is the
positive signed contraction tau q/rho, not the negative raw detector
operand used in the earlier fixed-measure paper. At the origin

    a=F_x(0,0)<0, b=F_y(0,0)>0, b/a=lambda_minus,
    K(0)=0, K'(0)=b>0.                                     (2)

The actual alpha, beta, detector probability and finite Golden ratio are
unchanged. The proof only needs the owned analytic common chart with
F_x!=0, F_y!=0 and the regular stationary section. Shrink it so that the
positive scale and K' remain positive. Every assertion involving infinitely
many points requires all their operands to remain inside that one chart.

Let e^a be a nondegenerate oriented coframe, omega an INDEPENDENT Lorentz
connection, g its metric, e=sqrt(|det g|), and psi_1,psi_2 the two original
real material components. In signature (+---), put

    f=e R(e,omega),
    q=sum_A g^(mu nu) partial_mu psi_A partial_nu psi_A,
    x=tau f/rho, y=tau q/rho,
    S_rho=B0+M integral rho(xcoord) F(x,y) d^4xcoord.         (3)

Here f is a weight-one Palatini density and q is an UNdensitized scalar.
The notation xcoord distinguishes coordinates from the query operand x.
rho is a fixed, possibly inhomogeneous, external coefficient in this
specified coordinate chart. It is not varied or relabelled during field
variations. There is no additional sqrt(|g|) in the material query.

For the field equations considered here, the actual fixed-cost interface
makes D_field B0=0 and keeps M,tau,alpha,beta fixed. Independent upstream
variables retain their own source equations and are not declared stationary
by this assumption. Variations are taken in ALL genuine coframe,
connection and scalar directions before any ansatz. They have compact
support or compatible fixed collar data.

For reference, the complete local chain rule before those quantities are
held fixed is

    d[rho F(x,y)]
       =tau F_x df + tau F_y dq
        +(F-xF_x-yF_y)drho
        +rho(xF_x+yF_y)dlog(tau).                            (4)

Dependence of operational fields on an actually moving rho belongs inside
df,dq as well. This formula is not an equation of motion for the discrete
PF multiplicities.

## 3. Exact weighted Ward identity and the missing invariant

Take any compactly supported vector field xi, and vary e^a,omega by their
Lie derivatives as forms and psi_A by their scalar Lie derivatives.
These are admissible variations of the original independent fields;
neither the fixed coordinate measure nor rho is varied. This uses a
particular field variation, not a diffeomorphism symmetry of (3).

The DIFFERENT density types give

    delta_xi x=xi.dx+x div(xi)+x xi.dlog(rho),
    delta_xi y=xi.dy+y xi.dlog(rho).

After one integration by parts, with P=F-xF_x,

    delta_xi S_rho
       =M integral xi^mu [rho partial_mu P
                           +y F_y partial_mu rho] d^4xcoord.

Consequently every full stationary field obeys

    dP+y F_y dlog(rho)=0.                                  (5)

The local coframe variation e^a -> exp(t/2)e^a, at fixed independent
connection and scalar fields, sends x->exp(t)x, y->exp(-t)y. It gives

    x F_x-y F_y=0.                                         (6)

Consume the owned trace branch, reflected into the convention (2), as
x=chi(y). Define

    m(y)=F_x(chi(y),y), n(y)=F_y(chi(y),y),
    u(y)=m(y)/a>0, Y(y)=y/u(y).

The existing radial nondegeneracy gives a locally invertible Y(y), with
Y(0)=0 and Y'(0)=1. Equation (6) says chi m=y n. Hence

    d_y P=n-chi m'=n(1-y m'/m).

Substitute in (5), use n!=0, and retain the external weight:

    (1-y m'/m)dy+y dlog(rho)=0,
    d[rho y/m(y)]=0.                                      (7)

The second identity is valid THROUGH y=0; no division by y was used.
On a connected chart it has one constant value. In particular a solution
whose y vanishes at one point has y identically zero. The incorrect
unweighted conclusion dy=0 does not follow when rho varies.

## 4. Consume the SAME stationary normal form, with all weights intact

The supplied universal auxiliary section is

    P=F_x(s,(P/a)t), s=(t/a)F_y(s,(P/a)t),
    U(t)=P(t)/a>0,
    K(t)=F(s(t),U(t)t)-P(t)s(t).                            (8)

Its inverse auxiliary Hessian is the owned regular block; no field
Hessian is inverted. On a full stationary solution s=x, U=u(y), t=Y(y).
The only coframe change is the SAME already-derived one:

    e_tilde^a=sqrt(U)e^a, g_tilde=U g,
    f_tilde=U f, q_tilde=q/U.

Thus t=tau q_tilde/rho. The complete reduced action is

    S_eff=B0+M tau a integral e_tilde R(e_tilde,omega)
                  +M integral rho K(tau q_tilde/rho).        (9)

This is stationary equivalence through the auxiliary extension and its
two reductions, not an off-shell physical-only equality. Constraints and
collars are transported through this map. Independent internal sources
would also be transported if they were varied.

Equation (7) now has the immediate interpretation

    rho y/m=(tau/a)q_tilde,
    d q_tilde=0.                                           (10)

For later use, the envelope derivative of (8) is exactly

    K'(t)=U(t)F_y(s(t),U(t)t)>0.                            (11)

## 5. Every reduced field equation; independent rigidity proof

Varying (9) in the independent Lorentz connection gives the torsion-free
connection of e_tilde. The ten metric equations and both material equations
are then

    a e_tilde G_mu nu(g_tilde)
       +K'(t) sum_A partial_mu psi_A partial_nu psi_A=0,     (12)
    partial_mu[K'(t) g_tilde^(mu nu) partial_nu psi_A]=0.   (13)

The other six coframe equations follow from internal Lorentz invariance
and the connection equations, as in the original full-field owner. Thus
these are all 16+24+2 continuum rows, not equations restricted to an ansatz.
No canonical-scalar pressure term has appeared: the material measure
was not densitized.

There are two short independent checks of (10):

1. The Palatini density in (9) has zero integrated Lie variation for
   compact xi, while delta_xi q_tilde=xi.dq_tilde. Therefore the EXACT
   off-shell identity is

       DS_eff[L_xi Phi]
          =M tau integral xi^mu K'(t) partial_mu q_tilde.   (14)

   Full stationarity and K'!=0 imply (10), for arbitrary prescribed rho.

2. Divide (12) by a e_tilde. The scalar equations say that the currents
   [K'(t)/e_tilde] partial^mu psi_A are covariantly conserved. The divergence
   of their quadratic source is therefore

       [K'(t)/(2e_tilde)] partial_nu q_tilde.

   Contracted Bianchi gives the same result. Derivatives of K'(t), including
   ALL derivatives coming from rho, are included in the scalar current and
   cancel in this calculation; they are not set to zero.

More generally, (14) proves this rigidity for any continuum action
A integral eR + integral L(xcoord,q) with constant nonzero A, independent
connection, undensitized q and L_q!=0. The present weighted CQ application
is its exact specified instance, not a change to a covariant e P(q) action.

## 6. Exact positive dust class for ANY prescribed positive rho

Set the second scalar constant and let q_tilde=q0>0. Define

    T=psi_1/sqrt(q0), v_mu=partial_mu T,
    varrho=-q0 K'(tau q0/rho)/(a e_tilde)>0.                (15)

Then v has unit norm in g_tilde. Equation (12) is precisely

    G_mu nu(g_tilde)=varrho v_mu v_nu.                      (16)

Because v=dT and its norm is constant, v is geodesic. Equation (13) is
equivalent to covariant dust conservation. The exact coordinate condition is

    e_tilde varrho = H_rho(xcoord),
    H_rho(xcoord)=-[q0/a]K'(tau q0/rho(xcoord))>0.           (17)

This includes the full nonlinear inverse-PF response. No uniform coefficient
has been substituted for K'(tau q0/rho).

### Converse construction without a frozen comoving shift

Start with ANY smooth local positive irrotational Einstein-dust solution
(g_d,varrho_d,T), with dT unit timelike, before caustics. Choose a regular
proper-time/comoving source chart (T,X^1,X^2,X^3). Its mass volume is

    varrho_d vol_(g_d)=C(X)dT dX^1 dX^2 dX^3, C(X)>0,

where conservation gives independence of T. Fix the TARGET coefficient
rho(T,x^1,x^2,x^3)>0 as given. It is never adjusted. On a relatively compact
target box choose q0>0 small enough that tau q0/rho lies in the common
master chart. Define the target H_rho by (17).

Preserve T,x^2,x^3 and define X^1=X^1(T,x) implicitly by

    integral_(X0^1)^(X^1) C(s,x^2,x^3)ds
       = integral_(x0^1)^(x^1) H_rho(T,s,x^2,x^3)ds.         (18)

After shrinking the box both sides are well defined; positivity gives

    partial_(x^1)X^1=H_rho/C(X)>0.

This is a smooth local spacetime diffeomorphism phi preserving T. Its
spatial Jacobian, and hence its full spacetime Jacobian, is H_rho/C. Put

    g_tilde=phi^*g_d, varrho=phi^*varrho_d,
    psi_1=sqrt(q0)T, psi_2=constant,
    omega=LC(g_tilde).

Then e_tilde varrho=H_rho EXACTLY. Norm, Einstein equations and conservation
pull back tensorially; (17) turns conservation into exactly (13). Thus every
full reduced equation holds. The stationary inverse (8) then produces a
full original weighted-CQ continuum stationary field.

Time dependence of X^1 MUST be retained in phi^*g_d. For example, if the
source metric is dT^2-gamma_ij dX^i dX^j, its pullback contains

    dX^1=X^1_T dT+sum_j X^1_(x^j)dx^j.

This generally gives nonzero mixed dT dx terms and changes the coordinate
components of the dust velocity. Although v=dT still has unit norm, its
contravariant spatial components need not vanish. Nothing in this proof
keeps the target metric in zero-shift/comoving form.

For an explicit check, take the flat dust FLRW geometry

    g_d=dT^2-T^(4/3)(dX^2+dY^2+dZ^2),
    varrho_d=4/(3T^2), C=4/3.

For a target rho depending on T alone, (18) is X=k(T)x with
k=3H_rho/4. The exact target metric is

    dT^2-T^(4/3)[(k dx+k' x dT)^2+dy^2+dz^2].             (19)

It has g_tilde^(TT)=1 and g_tilde^(xT)=-k'x/k. Its scalar equation reads
partial_T K' + partial_x[-K'(k'/k)x]=0, since K' is proportional to k.
Deleting the induced shift would instead leave partial_T K', generally
nonzero. This is a decisive check against the incorrect frozen-shift move.

The construction is local, respects only correspondingly transported
collars, and is not a claim that arbitrary coordinate changes are physical
symmetries of the given CQ execution. For two independently varying scalar
components, (10),(12),(13) hold with their summed contraction, but the source
need not be rank-one dust; no arbitrary two-fluid classification is claimed.

### Null class in the ORIGINAL metric

For a supplied local positive irrotational null-dust geometry
G=varrho_d dT tensor dT with nonzero null dT and conserved varrho_d dT,
choose psi_1=cT, psi_2 constant, and coordinates with

    e varrho_d=-(b/a)c^2>0.

The positive mass-volume coordinate construction can preserve T. Now
q_tilde=0, t=0, U(0)=1 and K'(0)=b, for EVERY prescribed rho. Thus x=y=0
and the ORIGINAL operational metric itself realizes this entire local
null-dust class, not only the Brinkmann/VSI subfamily. This extends the
existing continuum null construction through the actual PF weights;
finite-lattice realization of these arbitrary geometries is still separate.

## 7. Exact original-metric relation and a real obstruction

Let g denote the ORIGINAL operational metric in (3). At a weighted solution,

    g_tilde=U(t)g, t=tau q0/rho, l=log U(t),
    omega=LC(e_tilde),
    D_omega e^a=-one_half dl wedge e^a.                    (20)

Thus the independent original connection is generally not the torsion-free
connection of the original coframe. More precisely, define the affine
connection from the ORIGINAL coframe and the SAME independent omega by

    Gamma^lambda_(mu nu)(e,omega)
       =e_a^lambda[partial_mu e^a_nu+omega^a_(b mu)e^b_nu].

The torsion-free affine connection of g_tilde is then exactly

    Gamma_tilde^lambda_(mu nu)
       =Gamma^lambda_(mu nu)(e,omega)
          +one_half delta^lambda_nu partial_mu l.

Their difference is the projective one-form dl/2 times the identity. Its
exterior derivative is zero, so these TWO affine curvature tensors (and
their Ricci contractions) agree. This does NOT compare LC(g) to LC(g_tilde):
LC(g) is generally different from Gamma(e,omega). In particular the original
Palatini metric equation is equivalent to (12).

In terms of the torsion-free Levi-Civita derivatives of the ORIGINAL g,
the exact conformal Einstein identity gives

    G_mu nu(g)
      =-[F_y/(e F_x)] sum_A partial_mu psi_A partial_nu psi_A
        +nabla_mu nabla_nu l -one_half l_mu l_nu
        -g_mu nu Box_g l -one_quarter g_mu nu (dl)^2_g.     (21)

Every F derivative here is evaluated at the original on-shell pair
(chi(y),y), with y=U(t)t. Formula (11) and e_tilde=U^2 e verify the matter
coefficient directly. These derivative terms are determined by the actual
rho and the original price; no new scalar is introduced.

For the actual cap-one sign convention, the owned detector derivatives imply
F_xx(0)>0 and F_xy(0)<0. Hence the exact section derivative is

    U'(0)=[F_xy(0)+(b/a)F_xx(0)]/a>0.                     (22)

After shrinking the chart U is strictly monotone. Consequently, on any
nonnull constant-q_tilde branch, requiring the original connection also
to be torsion-free for the original coframe forces d rho=0. Arbitrarily
varying PF weights therefore obstruct that particular original-metric
torsion-free GR identification away from null. This is a precise remaining
interface condition, not an obstruction to the weighted stationary solutions
just constructed.

The dependence on rho is not made physically gauge by the stationary
coordinate change. The correct transport of an original observable O(e)
is O(U^(-1/2)e_tilde), including its rho dependence. Only an independently
established native readout identifying g_tilde as the physical metric would
allow the reduced Einstein geometry itself to be called the physical GR
geometry. On null fields U=1, so this distinction disappears exactly.

## 8. Full coupled Jacobi kernel: exact frozen-slope reduction

At a full reduced solution q_tilde=q0, define the actual spatial coefficient

    k_rho(xcoord)=K'(tau q0/rho(xcoord)).

Let S_aff have the same Palatini term as (9), and material term
M tau integral k_rho q_tilde, plus any field-independent constant. It has
the SAME first differential as S_eff at that background, in every original
reduced field direction. Its coefficients are held fixed in this comparison.
The full Hessian difference is exactly

    (H_eff-H_aff)[v,w]
      =M tau^2 integral [K''(tau q0/rho)/rho]
                          delta_v q_tilde delta_w q_tilde. (23)

Differentiate the off-shell identity (14) at the stationary background.
For a full Jacobi vector v, H_eff[v,w]=0 for every ambient test w. The
additional DS_eff[L_xi v] term vanishes at stationarity, and dq_tilde=0
kills the coefficient derivative. Thus

    d(delta_v q_tilde)=0.

With compact support or a fixed collar on a connected chart,
delta_v q_tilde=0. Equation (23) then proves H_aff[v,w]=0 for all w.
Conversely S_aff obeys the SAME Lie identity with coefficient k_rho!=0,
so every full fixed-collar Jacobi vector of S_aff also has delta q_tilde=0
and belongs to ker H_eff. Therefore

    ker H_eff = ker H_aff                                  (24)

on that full coupled variation space. This is not a claim about a scalar
propagator at frozen metric, equality of off-shell Hessians, their inertia,
or equality of different caps' kernels. Different actual weights and caps
can change k_rho(xcoord). The auxiliary stationary map transports these
coupled kernels to the original variables; the physical observable map
must be transported as in section 7.

## 9. Exact finite-source substitution and the remaining discrete Ward step

No continuum coordinate variation was needed for the EXISTING exact finite
normal form. It remains, with every actual PF factor,

    S_eff,h=B0+M tau a sum_z f_tilde,z
                  +M sum_z rho_z K(tau q_tilde,z/rho_z).

Its complete finite field source is exactly

    D S_eff,h=M tau [a D sum_z f_tilde,z
             +sum_z K'(tau q_tilde,z/rho_z) Dq_tilde,z].    (25)

The independent-link equation is precisely the common Palatini link
equation, since the original q has no independent-link dependence. Every
material equation is the adjoint of the ACTUAL original forward difference
with its actual coefficient K', and all coframe rows retain it. Thus at any
finite configuration with q_tilde,z=q0, the nonlinear source equals the
full affine weighted source with k_z=K'(tau q0/rho_z), without any continuum
assumption. A full root of that affine source having those q-values is an
exact nonlinear root. This is a concrete finite consumer, not a source on
an ansatz with missing variations.

What has NOT been established is that every finite root satisfies constant
q, or that every continuum dust geometry has an exact finite representative.
A finite star with fixed forward differences has no automatically exact
compact-Lie variation or continuum contracted Bianchi identity. Therefore
neither (10) nor (24) is imported onto it without a discrete identity.

This structural substitution is now carried out in
[`CONTINUUM_TO_FINITE_WARD.md`](CONTINUUM_TO_FINITE_WARD.md). It computes the
material product/inverse-chain defect and the geometric defect of the literal
six-face Palatini source, then verifies the complete pullback identity with
all 16 coframe, 24 proper-link and 2 scalar rows. It assumes no discrete
diffeomorphism symmetry. The canonical numerical outputs are
[`DISCRETE_MATERIAL_RESULT.json`](DISCRETE_MATERIAL_RESULT.json) and
[`FULL_WARD_RESULT.json`](FULL_WARD_RESULT.json); input and result hashes,
runtime and replay status are in [`WARD_SOURCE_PINS.json`](WARD_SOURCE_PINS.json).

The continuation also proves a conditional smooth-field estimate. On
uniformly C4 sampled fields with bounded inverse coframes, controlled link
logs, complete collars and uniformly C1 actual price slope, both Ward defects
are O(h). Therefore existing full finite stationary roots satisfying these
regularity and gain bounds obey `q_h=q_*+O(h)` when the compatible collar
fixes the constant mode. The checker grids themselves remain diagnostics,
not stationary roots; no physical native family or its regularity is
constructed or selected here.

For an admitted finite tangent `L_(xi,h)`, keep the gravity and
scalar-chain defects defined by

    D sum_z f_z[L_(xi,h)] = E_geom,h[xi],
    Dq_z[L_(xi,h)] = xi_z.D_h q_z+E_mat,h,z[xi].

In (26), k_z denotes K'(tau q_tilde,z/rho_z) at the actual finite stationary
point; the specialized q0 formula above applies only if q_tilde,z=q0 has
independently been established. At that point (25) gives the EXACT identity

    sum_z k_z xi_z.D_h q_z
       =-a E_geom,h[xi]-sum_z k_z E_mat,h,z[xi].             (26)

The finite identity and conditional smooth-regime norm bound now instantiate
(25)-(26) on the original carrier. No finite defect is set to zero. What
remains is to establish that the physically admitted execution has the stated
regularity, nonzero gain and collar, and to transport its full Book03,
preparation and clock source into this same root equation. This is the
remaining physical source step, not a new search over geometries or an
invented removal of PF weights.

All exact continuum statements above are local and conditional on the
declared continuum density dictionary. For arbitrary positive finite weights
a common off-null chart still requires tau |q0|/rho_min within the actual
master radius. The smooth-regime estimate does not establish regularity of
native physical roots, original metric/readout transport, moving-query
admission, compulsory Book valuation or genuine upstream stationarity. These
remain their respective real obligations. GR_closed=false.

## 10. Consumed sources and verification scope

All paths below are relative to the pinned repository's `02_REGISTRY/research/`:

* `sources/d0_native_density_rigidity_2026-10-21/PROOF.md`, especially
  sections 3-5 and 9: original Ward argument and its explicit weight boundary.
* `sources/d0_primary_normal_source_recovery_2026-10-21/constitutive/CONSTITUTIVE_COMPOSITION.md`:
  exact actual weighted price, universal K, coefficient signs and finite scope.
* `sources/d0_same_execution_spatial_source_2026-10-21/geometry/SAME_EXECUTION_LOCAL_HOMOGENEITY_AND_WEIGHT_SOURCE.md`:
  literal original coframe/difference dictionary and independent-site scaling.
* `sources/d0_same_execution_spatial_source_2026-10-21/weights/ONE_STAGE_COMPLETE_SPATIAL_WEIGHT_THEOREM.md`:
  actual multiplicities, original weights and paid fixed-field interface.
* `A4D_COMPLETE_PRICE_NONVACUUM_STATIONARY_NORMAL_FORM_2026_10_21.md`:
  stationary auxiliary equivalence, full source and Hessian transport.
* `A4D_CONDITIONAL_NON_NULL_BIANCHI_COMPLETE_PRICE_2026_10_21.md`:
  continuum Palatini convention, full independent field equations and collars.
* `weighted_dynamics/CONTINUUM_TO_FINITE_WARD.md`: exact finite all-42 source
  identity and its conditional smooth-regime refinement estimate.
* `weighted_dynamics/DISCRETE_MATERIAL_RESULT.json`,
  `weighted_dynamics/FULL_WARD_RESULT.json`, and
  `weighted_dynamics/WARD_SOURCE_PINS.json`: numerical outputs and replay
  provenance for the material and full-star finite checkers.

`SOURCE_PINS.json` records original bytes. The accompanying narrow checker
checks the weighted invariant with the actual nonlinear native master law,
the sign in (22), and the time-dependent mass-coordinate current with its
required shift. Its arithmetic is an authored diagnostic, not a replacement
for the analytical argument or a replay of the original finite native source.
