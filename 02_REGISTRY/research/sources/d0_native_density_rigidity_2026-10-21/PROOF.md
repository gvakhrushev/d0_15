# Full fixed-measure price: density rigidity and a common all-cap stationary set

21 October 2026. Read-only derived contribution inside existing PR #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, `native-programme-v1`.
Inputs are pinned in `SOURCE_PINS.json`. This proof is a NEW consequence of
those inputs; it does not repeat or replace their exact Bianchi solution.

## 1. Statement, scope and genuine new consequence

The existing explicit-dynamics packet exhibits one nonnull Bianchi I family
common to every fixed finite cap. The existing all-order radial theorem
provides a common trace branch and an invertible material coordinate.
Together with a compactly supported variation of the FULL original fields,
they imply more:

> **Density-rigidity / full stationary-set theorem.** In the exact
> fixed-coordinate-measure continuum model below, on a connected chart
> `|x|<1/4`, `|y|<2^-12`, EVERY smooth full coframe/independent-Lorentz-
> connection/two-real-scalar stationary configuration has spacetime-constant
> `x,y`, with `x=tau(y)`. Consequently the FULL field stationary sets of ALL
> the admitted fixed finite-cap valuations are identical on that chart.
> This is not merely one shared ansatz or equality of sources on a null
> solution family.

At each such stationary field, the FULL coupled Jacobi solution spaces are
also identical for perturbations vanishing on a fixed collar. This does not
equate the off-shell Hessians or their signs (Section 8).

All actual internal parameters are fixed, spatially constant, and satisfy
exactly the previous unit-price interface. The theorem does not solve their
independent equations or identify the continuum dictionary with the finite
native lattice. It does not prove diffeomorphism covariance of this action:
the fixed measure is essential to the new constraint. No native physical
admission, absolute Book valuation or GR closure is inferred.

## 2. Exactly the same continuum action and domain

Use the oriented nondegenerate coframe, independent Lorentz spin connection
and two real scalar components of the original Bianchi theorem. Write

    e = sqrt(|det g|) > 0,
    q = sum_A g^{mu nu} partial_mu psi_A partial_nu psi_A, A=1,2,
    x = eta^2 e R(e,omega),   y = -eta^2 q,
    S_N = integral F_N(x,y) d^4x,
    F_N(x,y) = V_N(r(x,y)).

The Palatini curvature convention and the literal Golden detector r are
exactly those in `A4D_CONDITIONAL_NON_NULL_BIANCHI_COMPLETE_PRICE...`,
equations (2)-(6). In particular the material query is UNdensitized and has
no independent spin-connection source. Eta>0 is constant. The outer price is

    V_N(r)=alpha [kappa-beta h_phi(r)] E_N(beta r),
    E_N(t)=sum_(j=0)^(N-1) t^j,
    alpha>0, 0<beta<=1, kappa>53,  N a fixed finite positive integer.

Different caps may use different spatially constant parameters satisfying
these assumptions. Additive field-independent baseline terms do not alter
any field equation and are omitted from F_N for the argument below. One must
not include an arbitrary externally varying baseline in the pressure P
while pretending it transforms with the fields.

All variations are compactly supported inside the coordinate cylinder, or
vanish on the same fixed collar. The field variables are varied BEFORE any
ansatz or connection elimination. Assume enough smoothness for the Euler
equations, their integration by parts and the induced coordinate variations.
The prescribed price functions are analytic on the common operand domain

    D = { |x|<1/4, |y|<epsilon }, epsilon=2^-12.

The prior radial theorem proves on D that z<r<2z, z=2^-20, that V_N'(r) is
nonzero for every admitted fixed cap, and that the only root of

    T(x,y)=x r_x-y r_y=0

in D is x=tau(y). It also proves the bounds consumed in Section 5 below.
These are owned analytical inequalities, not inferences from numerical caps.
The probability bound is proved on the FULL rectangle in the radial
owner's Section 3.3, before dividing by V_N'. One may verify it directly:
put p=phi^(-1), E=p^2(1+x), b=p+p^2y,
ell(E)=4E(1-E), B=4b^2(1-b^2), and A=ell+(1-ell)B.
The exact bounds 3/8<p^2<2/5 and 3/5<p<5/8 imply
1/4<E<1/2 and 1/2<b<2/3 throughout D. Hence 3/4<ell,B,A<1,
and

    1 < 3/2-z < r/z=A+B-zAB < 2.

Thus the nonvanishing-price premise used to extract the trace branch does
not depend on having already restricted to that branch.

## 3. A missing on-shell identity from a legitimate full field variation

Let xi be any compactly supported vector field in this SAME fixed coordinate
chart. Vary e^a, omega^{ab} as their Lie derivatives as differential forms and
psi_A as scalar Lie derivatives. These are particular admissible variations
among the independent continuum field variations. The coordinate measure
`d^4x` is held fixed: this is NOT an assertion that S_N has a diffeomorphism
symmetry and is NOT a free change of physical coordinates.

The geometric quantity eR is a density of weight one under this induced
field variation, while q is a scalar. Thus, exactly,

    delta_xi x = xi^mu partial_mu x + x partial_mu xi^mu,
    delta_xi y = xi^mu partial_mu y.

There is no explicit coordinate dependence in F_N. Hence

    delta_xi S_N
       = integral [xi^mu partial_mu F_N + x F_(N,x) div xi] d^4x
       = integral [x F_(N,x)-F_N] div xi d^4x
       = integral xi^mu partial_mu P_N d^4x,
    P_N = F_N-x F_(N,x).                                      (1)

At a FULL stationary field this variation vanishes for every xi. Therefore

    partial_mu P_N = 0.                                       (2)

This is a necessary consequence of all the existing field equations on the
fixed measure, not a new equation obtained by varying an external density.
One may equivalently introduce the fixed reference volume form as a
background and read (2) as its on-shell source identity, but no new varied
field or paid operation is needed for the direct proof above.

A volume-preserving variation div xi=0 would not reveal (2); restricting to
that set before varying would discard the decisive permitted directions.
Likewise, using a moving volume measure or densitizing the material changes
(1), so this theorem cannot be transferred to those actions by notation.

## 4. The radial equation and exact pressure derivative

For any compactly supported real t(x), the existing independent coframe
scale e^a -> exp(t/2)e^a at fixed omega and psi sends

    x -> exp(t)x,   y -> exp(-t)y.

Full stationarity therefore gives x F_x-y F_y=0 pointwise. Since V_N' is
nonzero on D, this is precisely T=0, so x=tau(y).

Along that branch define the original quantities

    a_N = V_N'(r0) r_x(0,0) != 0,
    M_N(y) = V_N'(r(tau(y),y)) r_x(tau(y),y),
    Q_N(y) = V_N'(r(tau(y),y)) r_y(tau(y),y),
    u_N(y)=M_N(y)/a_N,       Y_N(y)=y/u_N(y).

The radial identity is tau M_N=y Q_N, valid analytically through y=0.
Differentiating the actual pressure along this branch gives

    P_N'(y)=Q_N(y)-tau(y) M_N'(y)
           =Q_N(y) [1-y M_N'(y)/M_N(y)]                       (3)
           =a_N u_N(y) [r_y/r_x](tau(y),y)
                    [1-y d_y log|M_N(y)|].

The same expression follows by the previously derived normal form:

    P_N(y)=V_N(r0)+K_N(Y_N(y)),
    K_N'(Y_N(y))=[V_N'(rbar)]^2 r_x r_y/a_N,
    P_N'=K_N'(Y_N) Y_N'.                                    (4)

In particular P_N'(0)=V_N'(r0) r_y(0,0), not zero. The old difference
between a null VALUE of q and a nonzero material VARIATION is preserved.

## 5. A cap-uniform nondegeneracy estimate, with the true gain retained

The exact radial owner proves on |y|<=epsilon:

    15/16 < u_N < 16/15,
    |d_y log|M_N|| < 202,
    123/128 < r_x/A < 133/128,
    11 < r_y/A < 37,

where A(y)>0 is the owned quadratic coefficient. Since 202epsilon<1/16,

    15/16 < 1-y M_N'/M_N < 17/16,
    1408/133 < r_y/r_x < 4736/123.

Substitution in (3) proves the useful uniform bound

    2475/266 < P_N'(y)/a_N < 80512/1845,
    in particular 9 < P_N'(y)/a_N < 44.                    (5)

The sign of a_N is negative for cap one and positive for caps >=2. Thus
P_N is strictly monotone in either case, with no vanishing normalized
pressure derivative. Actual |a_N| is NOT bounded below uniformly across
arbitrary readiness parameters, and is not silently divided away from a
physical source/error estimate.

Now (2), x=tau(y), and (5) imply

    partial_mu y = 0,   partial_mu x = 0.                   (6)

On a connected domain each is a single constant. This proves the rigidity
claim without assuming homogeneity, a Bianchi metric, null matter, a fixed
lapse, or field variations preserving x and y.

## 6. Identical FULL stationary sets for every admitted fixed cap

Let a field in D be stationary for one cap N. By (6), r=r_* is constant.
For EVERY ambient compactly supported independent field variation,

    delta S_N=V_N'(r_*) integral delta r d^4x,
    delta S_M=V_M'(r_*) integral delta r d^4x.

Both multipliers are nonzero constants. Therefore

    delta S_M = [V_M'(r_*)/V_N'(r_*)] delta S_N = 0          (7)

for every other admitted finite cap M. The same argument in reverse proves

    Crit_D S_N = Crit_D S_M  for all N,M.                   (8)

This uses the original fields and the same fixed boundary task; no cap-
dependent coframe map is needed for the equality. It permits different
constant alpha,beta,kappa satisfying the same premises. It does not compare
an optimized/nonsmooth cap envelope, infinite-cap execution, or varying
internal parameters; no clock selection is inferred.

A convenient intrinsic characterization of this common set is:

1. x=x_*, y=y_* are spacetime constant and x_*=tau(y_*);
2. the independent connection is the torsion-free Levi-Civita spin
   connection of the ORIGINAL coframe;
3. all ten metric and both scalar equations hold:

       r_x e G_(mu nu)
          -r_y sum_A partial_mu psi_A partial_nu psi_A = 0,  (9)
       partial_mu(g^(mu nu) partial_nu psi_A)=0.             (10)

Here r_x,r_y are evaluated at the SAME constant (x_*,y_*). The six remaining
coframe rows follow from internal Lorentz invariance together with the 24
connection equations, exactly as in the owned full Bianchi proof. Conversely
(9)-(10) with the same constant density dictionary and torsion-free
connection imply every full coframe/connection/scalar Euler equation for
every cap, because their first variations have precisely (7)'s form.

Equation (8) says nothing about equality of Hessians or minima. The second
variation retains V_N''(r_*) integral(delta r)^2 as well as V_N' delta^2r;
the already-owned opposite radial signs between cap one and higher caps
remain unchanged. The native source-preserving field-minimum exclusion is
also unchanged.

## 7. Positive geometric content and the actual matter interpretation

The owned exact Bianchi I solution has x_*,y_* nonzero and constant and
satisfies (9)-(10), with nonzero Ricci and Weyl. It is consequently a
nonempty explicit member of this entire common stationary set, with no new
root computation. The known null primary sector x_*=y_*=0 is retained; q=0
does not force the scalar fields or their null gradients to vanish.

For ONE real timelike scalar (the other component constant), q=q_*>0,
let u_mu=partial_mu psi/sqrt(q_*). Then u_mu u^mu=1 and (9) is exactly

    G_(mu nu)=rho u_mu u_nu,
    rho=(r_y/r_x) q_*/e >0.                                (11)

The two remaining dust identities follow, rather than being added:

    u^mu nabla_mu u_nu=(1/(2q_*)) partial_nu q=0,
    nabla_mu(rho u^mu)=0.                                  (12)

The second uses (10) and spacetime-constant r_y/r_x,q_*. This is a derived
irrotational pressureless Einstein source in the specified fixed-volume
chart. It is NOT the canonical densitized massless-scalar stress: (9) has
no `-g_mu nu q/2` term. For two independently varying real components the
source is their sum and need not be rank one or pressureless dust.

A further local constructive corollary is available. Suppose a smooth
Einstein irrotational dust solution has rho>0 and a local unit velocity
potential tau with u=d tau; assume a regular flow box without caustics.
Choose proper-time/comoving coordinates (tau,X^i). Conservation gives
`e rho=C(X)>0`, independent of tau. A time-independent spatial relabeling
with prescribed positive Jacobian makes `e rho=k` any chosen positive
constant locally. Explicitly, on a coordinate box set

    Xnew^1=(1/k) integral_(x0^1)^(X^1) C(s,X^2,X^3) ds,
    Xnew^2=X^2,  Xnew^3=X^3.

Its spatial Jacobian is C/k>0, so it is a local diffeomorphism and the new
volume satisfies e_new rho=k. It is time independent and therefore
preserves the proper-time/comoving choice. Pick any
small y_*<0 in the owned interval, put

    q_*=-y_*/eta^2,  k=-tau_branch(y_*)/eta^2>0,
    psi=sqrt(q_*) tau, other scalar constant.

In these chosen fixed-volume coordinates x=eta^2 eR=-eta^2 e rho
=tau_branch(y_*), y=y_*, and the trace identity gives
`r_x k=r_y q_*`. Equation (9) is exactly the supplied Einstein dust
system, while (10) follows from `partial_mu(e rho u^mu)=0` and e rho=k.
Thus every such local irrotational positive-dust geometry has a
representative in the common stationary set. This is a conditional
continuum construction in specified mass coordinates, not a proof that
all coordinates represent equivalent physical D0 executions. No new dust
field or new action was inserted. The elementary coordinate argument is
included to make this corollary reviewable, not to claim historical priority
for dust spacetimes or their mass coordinates.

The null analogue is also exact and compact. Suppose a smooth local
irrotational null-dust solution has

    G=varrho dT tensor dT,  g^(-1)(dT,dT)=0, dT!=0, varrho>0,
    nabla_mu(varrho partial^mu T)=0.

Choose c!=0, let L0=r_y(0,0)/r_x(0,0)>0, and choose local coordinates
with `e varrho=L0 c^2`. Such coordinates exist: the positive volume form
`varrho vol_g` has a positive coordinate density, and the same one-coordinate
integration normalizes it; one may keep T as one coordinate since dT!=0.
With psi=cT and the other scalar constant, x=y=0, the metric equation
becomes exactly G=varrho dT tensor dT, and the undensitized scalar equation
follows from conservation and constant e varrho. Thus the same all-cap
stationary class contains representatives of arbitrary such local null-dust
geometries, with no Brinkmann/VSI restriction. A vacuum Ricci-flat metric
with both scalars constant is the already-familiar zero-source corollary.

These are local existence/representation statements in explicitly selected
fixed-volume coordinates. They do not make arbitrary coordinate transforms
symmetries of the original nonlinear price and do not cover vortical dust,
caustics, zeros of the matter density, or a generic canonical scalar source.

## 8. Identical FULL coupled Jacobi kernels with a fixed collar

Let Phi be any common stationary field, and let H_N=D^2S_N|_Phi be the
full Hessian in the original independent fields. A Jacobi perturbation v
means H_N[v,w]=0 for EVERY compactly supported ambient test variation w.
The perturbation need not be the tangent of an integrable solution family.

The off-shell induced-field identity is

    DS_N(Phi)[L_xi Phi]=integral xi^mu partial_mu P_N(Phi).

Differentiate this identity in direction v. The additional term from the
field dependence of L_xi Phi is DS_N(Phi)[L_xi v], which vanishes at the
stationary background. The Hessian-kernel condition kills
H_N[v,L_xi Phi]. Since xi is arbitrary, d(delta_v P_N)=0 follows for
every full Jacobi perturbation, without an integrability assumption.

Likewise the off-shell independent coframe-scale identity is

    DS_N(Phi)[R_t Phi]=integral t V_N'(r) T(x,y).

Its linearization at a stationary background has no DS_N term and T=0.
The same Hessian-kernel condition therefore gives delta_v T=0. The owned
nonzero T_x on the trace branch implies
delta_v x=tau'(y_*) delta_v y. Substitution into delta_v P_N and the
nonzero constant P_N'(y_*) then gives

    d(delta y)=0,  d(delta x)=0,                            (13)

because P_N'(y_*)!=0. For perturbations of compact support, or with fixed
collar values on a connected domain, the constants must be zero:

    delta y=delta x=0.                                     (14)

In particular delta_v r=0 pointwise. The full bilinear Hessian at the
constant-response background is

    H_N[v,w]=V_N'(r_*) integral delta^2 r[v,w]
             +V_N''(r_*) integral delta_v r delta_w r.

For the given Jacobi perturbation v, the second term vanishes for every w.
Consequently H_M[v,w]=[V_M'(r_*)/V_N'(r_*)]H_N[v,w]=0. Reversing the
argument proves the exact equality, on the SAME fixed-collar variation
space,

    ker H_N = ker H_M  for every admitted finite cap N,M.  (15)

This is equality of the full coupled linearized solution spaces about each
common background. It is not equality of the off-shell Hessian operators,
quadratic forms, minima, or finite perturbations. With no fixed collar the
constant density-changing modes need not vanish, so (15) is not asserted
for that larger variation space. The actual nonzero multipliers in (15)
remain those of the configured prices.

Neither (14) nor (15) says that a scalar disturbance itself vanishes:
delta y includes the metric perturbation and both scalar components.
Consequently the previous fixed-reduced-metric material propagator cannot,
by itself, be the general full coupled propagator. Its explicit limitation
was correct; (13)-(15) identify the missing constraint and show that it
removes the cap-dependent density-product Hessian term on every full
Jacobi solution.

## 9. Relation to the actual finite cap-one PF composition

The theorem above is confined to the stated constant-parameter continuum
dictionary. The distinct finite-lattice application can nevertheless use a
simple exact formula, without claiming continuum coordinate variations.

Let the actually implemented cap-one local price be F(x,y), with
F(0)=0, a=F_x(0), b=F_y(0), and its owned local stationary material normal
form K. Let the actual trace-copy multiplicities be m_i=C rho_i and
operands x_i=epsilon_i f_i, y_i=sigma epsilon_i q_i, where
`epsilon_i=eta_h^2/rho_i`. On its specified scalar-coded field chart the
fixed ± two-query basis is exact for every E,b, so the local formula is
an exact full-neighborhood identity of the configured price. It is not an
all-order identity for arbitrary extra off-diagonal feedback variations.

Applying the owned stationary normal form to the independent ledgers gives

    S_eff=B+a_h sum_i f_i + C sum_i rho_i K(sigma epsilon_i q_i),
    a_h=C eta_h^2 a !=0.

In normalized form,

    (S_eff-B)/a_h = sum_i(f_i+lambda q_i)+sum_i R_i(q_i),
    lambda=sigma b/a,
    R_i(q)=[K(sigma epsilon_i q)-b sigma epsilon_i q]/(a epsilon_i).

If |K''/a|<=C_K on the actual common operand interval, then exactly

    |R_i(q)|<=C_K epsilon_i q^2/2,
    |R_i'(q)|<=C_K epsilon_i |q|,
    |R_i''(q)|<=C_K epsilon_i.

The full first derivative is sum_i R_i' Dq_i; its Hessian is
sum_i[R_i'' Dq_i tensor Dq_i +R_i' D^2q_i]. These retain the actual
field jet norms, lattice size/averaging convention and epsilon_max.
The reduced proper-link equation is EXACTLY that of the common weighted
Palatini term because the specified q_i does not depend on independent
links. This does not identify the transformed coframe with an unchanged
physical readout, prove uniform inverse bounds, or supply native admission.

With spatially varying rho_i or internal parameters, this finite normal
form need not obey the continuum identity (1). The constant-density theorem
must not silently be imported onto an inhomogeneous ledger or a finite
lattice, which has no automatically admitted compact Diff variation.

## 10. What is closed and what remains open

Closed inside the declared continuum model: the need to assume constant
queries in applying the full-source cap transfer. Constancy is now derived
from the full independent field equations, on the actual common small
branch. The all-cap statement is equality of entire local stationary sets.
At each common background their full coupled Jacobi kernels also agree on
the same fixed-collar perturbation space, despite different Hessians and
radial stability signs.
The nonnull existence result is broadened from the Bianchi family to local
irrotational dust representatives under the stated regularity assumptions.

Still open: the actual native continuum dictionary, finite-lattice lift,
complete Book selection/absolute price, field-writing admission, independent
preparation/clock/reference equations, metric-only Diff descent, uniform
refinement and generic GR/raw216. The fixed external measure produces a
constraint rather than supplying the missing off-shell diffeomorphism
symmetry. Changing that measure changes the model.

The checker verifies the new exact symbolic identities and rational
nondegeneracy bounds, including hostile density-weight and Hessian controls.
It does not replay the old all40, Bianchi, compiler or Lean suites and does
not replace the analytical proof of (1)-(15).
