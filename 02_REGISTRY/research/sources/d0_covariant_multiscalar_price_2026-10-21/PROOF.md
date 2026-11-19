# The full native continuum stationary set has a covariant two-scalar representation

21 October 2026. Bounded composition within existing scientific PR #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`,
`Assembly-Slot: constitutive`, `Assembly-Carrier: native-programme-v1`.
Input snapshot: `80d3b1bac1bb9a974f365dbc4c48d3ada539d3a2`.

## 1. New parent substitution and exact scope

The owned [density-rigidity theorem](../d0_native_density_rigidity_2026-10-21/PROOF.md)
already proves that every full stationary field of the specified fixed-measure
continuum price has constant query densities, and that every finite cap has
the same stationary set. Its converse construction covers one real scalar
and irrotational dust. The result below identifies the **entire two-real-scalar
stationary set**, including nonparallel gradients, with a volume-gauge slice
of a generally covariant Einstein/constrained-scalar system. It also maps
the complete fixed-sector Jacobi equations in both directions.

No new physical constraint is imposed on the native price: the constant
kinetic constraint used below is already a consequence of its full equations.
The multiplier action is a representation of those solutions, not a proposed
replacement for the actual paid price. In particular this theorem does not
make the original off-shell action Diff-natural, identify an absolute Book
value, admit a finite native field writer, or solve independent upstream
equations. `GR_closed=false`.

## 2. Owned continuum input, without changing its measure or matter

Work on an oriented connected local four-dimensional chart with fixed positive
coordinate volume `mu0=d^4z`, nondegenerate coframe, independent Lorentz spin
connection, and two real scalar fields `psi_1,psi_2`. Set

    e = vol_g/mu0 = sqrt(|det g|) > 0,
    K_(mu nu) = sum_(A=1)^2 partial_mu psi_A partial_nu psi_A,
    q = g^(mu nu) K_(mu nu),
    x = eta^2 e R(e,omega),       y = -eta^2 q,
    S_N = integral V_N(r(x,y)) mu0.

Here `eta>0` is fixed, `r` is the original Golden two-query detector, and

    V_N(r)=alpha[kappa-beta h_phi(r)] sum_(j=0)^(N-1)(beta r)^j,
    alpha>0, 0<beta<=1, kappa>53, 1<=N<infinity.

All these internal parameters are fixed and spatially constant. The actual
domain is `|x|<1/4`, `|y|<2^-12`; the owned estimates hold on the closed
`y` interval as well. Smooth fields and compactly supported
variations, or the original fixed collar, are retained. Different caps may
use different constant parameters obeying those same hypotheses.

The consumed owner proves, before any ansatz, that every stationary field has

    x=x_*=tau(y_*),       y=y_* constant,
    x_* r_x(x_*,y_*) = y_* r_y(x_*,y_*),
    r_x>0, r_y>0, V_N'(r_*) != 0,       r_*=r(x_*,y_*).

It also proves the exact full stationary equations

    omega = omega_LC(e),
    e r_x G_(mu nu) = r_y K_(mu nu),
    partial_mu(g^(mu nu) partial_nu psi_A)=0, A=1,2.       (1)

All sixteen coframe and twenty-four connection rows are represented: after
the independent connection equation the ten metric rows and local Lorentz
identity give all sixteen coframe rows. The material has no independent spin
connection source. These facts are consumed from the original variational
proof, not inferred by restricting the action before variation.

For a fixed sector label `y_*`, define

    q_* = -y_*/eta^2,
    k_* = r_y(x_*,y_*)/r_x(x_*,y_*) > 0,
    a_N = eta^2 V_N'(r_*) r_x(x_*,y_*) != 0.              (2)

The radial identity says `x_*=k_* y_*`. At `y_*=0` the ratio in (2) is used
directly; no division by `y_*` or `q_*` is made. The exact finite-fugacity
value is `k_0=-lambda_minus(2^-20)=23.416406751884...`, consumed from the
owned coefficient identity. The factor `a_N` is retained: its sign and
magnitude need not be cap independent or uniformly bounded away from zero.
The continuum operand here is `y=-eta^2 q`. A finite compiler using
`y_phys=+eta^2 q` and the original `sigma=-1` dictionary has
`y=-y_phys`; its material first derivative has the opposite sign.
The equality is `k_0=-lambda_minus`, not an equality of those two raw
operand derivatives.

## 3. Covariant multiplier equations derived before fixing a gauge

For this one fixed sector consider the auxiliary first-order functional

    I_*[e,omega,psi, Lambda]
      = integral vol_g [R(e,omega) - Lambda(q-q_*)].       (3)

`Lambda` is a genuine scalar in this representation, while `q_*` is a fixed
sector parameter. It is **not varied**. Varying `q_*` would add a false global
equation `integral Lambda vol_g=0` on the positive branch.

Vary the independent coframe, connection, both scalars and multiplier BEFORE
imposing any constraint or gauge. The resulting equations are

    omega=omega_LC(e),
    G_(mu nu)-Lambda K_(mu nu)
        +(Lambda/2)(q-q_*) g_(mu nu)=0,
    nabla_mu(Lambda partial^mu psi_A)=0, A=1,2,
    q=q_*.                                               (4)

The metric formula follows from `delta vol_g=-(1/2)vol_g g_(mu nu)
delta g^(mu nu)` and `delta q=K_(mu nu) delta g^(mu nu)` with scalar fields
held. Its constrained form is therefore

    G=Lambda K,      div_g(Lambda grad psi_A)=0, q=q_*.    (5)

The Einstein-Hilbert coefficient in (3) is one, rather than one-half. This
fixes the multiplier normalization in (5); no factor of two is absorbed
silently. The independent Lorentz-connection equation is ordinary Palatini
with a constant nonzero coefficient, hence torsion free on a nondegenerate
coframe. Local internal Lorentz covariance accounts for the remaining six
coframe components after that equation is imposed.

Constrained scalar and multifield mimetic multiplier formulations are known
theories. For the timelike sector `q_*>0`, field rescaling puts the constraint
in the usual unit form, with the positive field-space metric. For comparison
see Shen, Zheng and Li, *Two-field mimetic gravity revisited and Hamiltonian
analysis*, JCAP 12 (2019) 026, [arXiv:1909.01248, Eq. (15)](https://arxiv.org/html/1909.01248v4),
and Mansoori et al., *Multifield mimetic gravity*, Phys. Rev. D 105 (2022)
023529, [arXiv:2108.11666, Section 2.1](https://arxiv.org/html/2108.11666v3).
The contribution here is the specific native-price/volume-gauge theorem,
including its `q_*=0` sector, not the invention of that theory or an imported
stability conclusion. The proof of (3)-(5) is direct and uses no external
Hamiltonian theorem.

## 4. Forward map: every native stationary field is a covariant solution

For a native solution in sector `y_*`, set

    Lambda = k_*/e.                                     (6)

This is a positive function in the given chart. Declare it to be the scalar
field of the covariant representation; the relation (6) is the volume-gauge
condition in that chart, not a scalar transformation law for `1/e`.
Equations (1) imply `G=Lambda K`, `q=q_*`, and

    nabla_mu(Lambda partial^mu psi_A)
      = (1/e) partial_mu(e Lambda g^(mu nu)partial_nu psi_A)
      = (k_*/e) partial_mu(g^(mu nu)partial_nu psi_A)=0.    (7)

Thus all of (4) hold. The gauge is intrinsically

    Lambda vol_g = k_* mu0.                              (8)

This step applies to both independent real scalar fields; their gradients
need not be parallel, timelike, nonzero, or separately of constant norm.
Only their total `q` has the already-proved constant value. In particular
`q_*=0` does not imply rank-one null dust: timelike and spacelike scalar
kinetic terms can cancel in the total Lorentz contraction.

## 5. Converse: every positive-multiplier solution has a native representative

Let a smooth local solution of (4) with the fixed `q_*` have `Lambda>0` and a
nondegenerate coframe. The volume form `Lambda vol_g` is positive. On an
oriented coordinate box `z=(z^0,z^1,z^2,z^3)`, write its density as
`f(z)=e(z)Lambda(z)>0`. Define new coordinates by

    Z^0 = (1/k_*) integral_(z0^0)^(z^0) f(s,z^1,z^2,z^3) ds,
    Z^i = z^i, i=1,2,3.                                 (9)

The full Jacobian matrix is triangular apart from its first row and has
`det(DZ/Dz)=f/k_*>0`. The inverse function theorem makes (9) a local
diffeomorphism. In these coordinates

    e_new Lambda = e Lambda / det(DZ/Dz)=k_*.              (10)

This changes coordinates of a covariant solution; it does not rescale its
metric or modify its physical scalar fields. Equivalently, pull the solution
back to a chart with the originally prescribed `mu0` satisfying (8).
No timelike clock potential or flow-box hypothesis is necessary for this
local positive-volume construction.

Take the trace of the full Einstein equation in four dimensions:

    -R = Lambda q_*.

Together with (10), this yields exactly

    y=-eta^2 q_*=y_*,
    x=eta^2 e R=-eta^2 e Lambda q_*=k_* y_*=tau(y_*).      (11)

The case `q_*=0` gives `R=x=0` without dividing by it. The scalar equations
in (4) reduce via (10) to the two original equations (1). The metric and
connection equations reduce to (1) with the exact ratio (2).
The entire original native Euler system therefore vanishes for **every**
finite cap in the owner's class. This is a genuine reverse implication;
an arbitrary already-chosen solution ansatz is not needed.

The statement is local. A prescribed boundary or collar need not admit the
normalization (9) while remaining fixed. A boundary-preserving volume gauge
has extra volume/boundary compatibility conditions, and no global topology,
global time foliation, extension through `Lambda=0`, or caustic theorem is
asserted. When a given gauge slice and collar are already fixed, Section 7
states the exact linearized result there.

## 6. What covariance and the residual gauge now mean

At fixed `y_*`, any two representations satisfying (8) differ, within the
same local covariant diffeomorphism orbit, by a diffeomorphism preserving
`mu0` (and by ordinary coframe Lorentz transformations). Conversely such
volume-preserving maps preserve (8) and the native equations. Infinitesimally
the residual coordinate transformations obey `div_mu0 xi=0`.

Consequently, the local native solution classes modulo volume-preserving
coordinate transformations are equivalent to the local positive-`Lambda`
solution classes of (3) modulo arbitrary orientation-preserving coordinate
transformations. Here 'equivalent' refers to the displayed forward map,
local gauge existence and exact residual transformations. It makes no
additional identification of microscopic executions or observables.

There is also an explicit conserved current for each original scalar,

    J_A^mu=Lambda partial^mu psi_A,      div_g J_A=0,

and an exact off-shell differential identity after the torsion-free reduction,

    nabla^mu(Lambda K_(mu nu))
      = sum_A [div_g(Lambda grad psi_A)] partial_nu psi_A
          +(Lambda/2) partial_nu q.                      (12)

Thus the two scalar equations and constant `q` make the full rank-one or
rank-two matter tensor conserved. This is the required same-equation
compatibility, with no assumption that each field separately supplies a
conserved dust stress.

This closes the **on-shell local covariance and two-scalar interpretation**
of this configured continuum stationary set. It does NOT close the physical
metric-only/off-shell Diff-natural premise in the Golden-blow-up/Lovelock
route. The original price contains the external measure away from its
stationary set; (3) introduces matter and a multiplier; the physical complete
Book action and its clocks/preparations have not been transported to (3).
The off-shell Ward identity of (3) must not be relabelled as an off-shell Ward
identity of the actual native complete Price.

## 7. Exact transfer of the full fixed-sector Jacobi equations

At a common native solution in this gauge, the density-rigidity owner proves
for every full Jacobi perturbation `v` with compact support or the original
fixed collar

    delta_v x=delta_v y=0.                               (13)

Associate the multiplier perturbation

    delta_v Lambda=-(Lambda/e) delta_v e.                 (14)

Then `delta(e Lambda)=0` and `delta q=0`, exactly the linearized gauge and
fixed-sector multiplier equation. Since (13) kills the variations of
`V_N'(r)r_x` and `V_N'(r)r_y` as spacetime functions, the linearized native
coframe, connection and scalar Euler covectors, written as densities with
the common coordinate volume before stripping nonzero row factors, equal
`a_N` times their counterparts from the variation of (3), with (14), on
these perturbations. In particular the scalar Euler density is twice the
coordinate divergence; (4)'s displayed covariant divergence has already
divided out `2e`. No derivatives of a varying
coefficient remain. Since `a_N!=0`, every full native Jacobi field maps to
a full covariant Jacobi field in the fixed volume gauge.

Conversely, take a full Jacobi perturbation of (4) about this solution,
at fixed `q_*`, satisfying the linearized gauge `delta(e Lambda)=0`.
The multiplier equation gives `delta q=0`. The linearized trace equation
`delta R=-q_* delta Lambda-Lambda delta q` then gives

    delta(eR)=-q_* delta(e Lambda)-e Lambda delta q=0.     (15)

Thus `delta x=delta y=0`, and the same nonzero row multiplier proves the
native Jacobi equations. This is a bijection of the stated full coupled
linearized solution spaces, including the independent connection. It is
valid at `q_*=0`; it does not require division by the curvature or kinetic
constraint. Restrict both sides to the same collar/support conditions.

This does not identify off-shell Hessians, their signs, symplectic forms,
energies, or a selected stability notion. Nor does local nonlinear gauge
existence promise a gauge change supported inside an arbitrary fixed collar.
Density-changing constant modes without that collar must be treated with
the sector labels allowed to move; this fixed-sector statement does not
discard them.

## 8. Why the multiplier is derived here, not a fitted source cancellation

The implication uses an already forced constraint `q=q_*`, an already
forced source ratio `k_*`, and the already solved independent connection
equations. It does not cancel a nonzero tangent residual by freely selecting
a multiplier. Given native fields, (6) fixes `Lambda` uniquely. Given a
covariant solution, (9)-(11) prove the reverse native equations.

One must not substitute (6) in (3) before varying and thereby discard the
multiplier equation. The resulting fixed-gauge expression

    integral [eR-k_*(q-q_*)] mu0

does not itself retain the constraint `q=q_*`; its field equations at most
force a locally constant `q`, whose value need not satisfy the native
radial relation with the chosen `k_*`. The correct theorem is about all the
equations obtained **before** gauge restriction.

Nor is there an absolute-price equality. On a common solution the native
integrand is `V_N(r_*)` whereas (3)'s integrand in gauge is `-k_* q_*`.
They need not agree, and the full off-shell native nonlinear terms have
not disappeared. The complete first/second source, field-writing image,
upstream stationarity, physical admission, finite-lattice lift and universal
refinement still require their actual parent transports.

## 9. Bounded verification and downstream use

`check_covariant_multiscalar.py` verifies source pins, the exact original
finite-`z` coefficient, the full first-source normalization, multiplier and
gauge linearization, an explicit nonconstant positive four-dimensional
volume normalization, and negative controls for dropping the constraint,
wrong multiplier normalization and confusing total-null with rank-one
matter. The coordinate existence and full solution/Jacobi equivalences are
proved analytically above; a finite symbolic calculation is not their proof.

The separate `CROSSING_STREAMS.md` / `examples_crossing_streams.py` constructs
a rank-two, non-VSI geometric example as a consumer of this theorem. The
unchanged historical all40, compiler, density-rigidity and Lean suites need
not be repeated. The positive theorem removes a missing **continuum model
interpretation and reverse-realization** step; none of the still missing
native physical admission/absolute-price gates is promoted.
