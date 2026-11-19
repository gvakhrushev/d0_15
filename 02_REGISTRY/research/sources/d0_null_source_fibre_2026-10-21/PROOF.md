# Exact null two-field source fibre, intrinsic realization, and the native readout test

21 October 2026. Existing scientific Draft PR #334 only.
Owner: EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.
Phase: conditional source descent / final composition.
Carrier: native-programme-v1; intended consumer: constitutive and the existing
same-execution readout/independent-input gate. Input head:
`5edac80c86c17014fc83e0aa608e192f43c1fdba`.

## 0. Result and change to the parent argument

The previous covariant two-field theorem identifies stationary equations.
It does not say whether the two scalar labels are determined by the metric
and its Einstein source, or whether a proposed extra scalar mode changes
that source. This continuation closes that precise nonlinear question on
the regular null rank-two sector, rather than constructing another spacetime.

**Proved here.** The complete local fibre over the SAME metric and source is
exactly the conformal/anticonformal pseudogroup of the two-dimensional scalar
target, with the uniquely compensating positive multiplier. There is also an
intrinsic necessary-and-sufficient local realization test using only the
source tensor: its kernel foliation and transverse conformal class. This
gives a constructive inverse without choosing scalar labels in advance.

An apparently dangerous complex characteristic pair integrates to an exact
family with UNCHANGED metric and stress. Its unquotiented scalar/multiplier
Cauchy data have a precise discontinuity example. This is not a gravitational
instability theorem. Conversely, calling that family physical gauge is also
unjustified: the original native volume gauge removes nonconstant target
conformal freedom at fixed native metric. Returning the general family to
that gauge requires a real, explicitly computed coordinate Jacobian/shift.

The remaining same-execution physical question is therefore sharper: do the
actual paid readout, preparation, cut, reference and clock identify this
mathematical fibre after that transport, or do they resolve it? Neither
answer is installed as a selector. No new action or Info law is selected.
`GR_closed=false`. No task/lifecycle/assembly acceptance is changed.

## 1. Precisely consumed equations and domains

Consume the existing proof in
`../d0_covariant_multiscalar_price_2026-10-21/PROOF.md`, its
`CROSSING_STREAMS.md` and `WEIGHTED_NULL_COROLLARY.md`, and the current
`../d0_causal_native_weighted_synthesis_2026-10-21/weighted_dynamics/WEIGHTED_WARD_AND_DUST.md`.
Their immutable blobs are in SOURCE_PINS.json. These owners, not this check,
supply the original all-field variation, finite Golden ratio and actual
PF-weight dictionary. Historical curvature/finite-lattice/Lean suites are
not rerun or claimed as freshly validated.

Work locally with smooth real fields, Lorentz signature (+---), a
nondegenerate coframe, the independently varied Lorentz connection, and
positive Lambda. Put

    Psi=psi_1+i psi_2,
    X=sum_A dpsi_A tensor dpsi_A,
    q=tr_g X,
    T=Lambda X.

The owned covariant representation in the FIXED sector q_*=0 is

    I_0 = integral vol_g [R(e,omega)-Lambda q].             (1)

Its full equations, after varying before imposing constraints, are

    omega=LC(e), G(g)=T, q=0,
    E_A:=div_g(Lambda grad_g psi_A)=0, A=1,2.              (2)

The regular source-fibre statements assume rank(dpsi)=2 on a sufficiently
small connected neighborhood, with connected local fibres. They concern
local germs or compatible transported domains, not arbitrary unchanged
outer collars. In (2), the trace gives R=0, but neither T nor its rank is zero.

The original fixed-volume continuum realization has

    Lambda vol_g=k0 mu0,
    k0=-lambda_minus(2^-20)>0.                            (3)

It remains a representation of the given price's stationary set, not a new
physical multiplier action. Its fixed-density/nonlocal and actual native
primitive/price boundaries are not discharged by (1).

## 2. Exact target-conformal invariance, including all equations

Let f be a locally holomorphic map on a neighborhood of Psi's image, with
f' nowhere zero there. Let D=|f'(Psi)|^2>0. Define

    Psi'=f(Psi), Lambda'=Lambda/D, g'=g, omega'=omega.     (4)

In real target coordinates Df^T Df=D I_2. Thus for arbitrary off-shell
fields, not merely a solution or a linearized variation,

    X'=D X, q'=D q, Lambda' X'=Lambda X,
    Lambda' q'=Lambda q.                                (5)

Equation (1) is EXACTLY invariant off shell. The metric source, including
its off-constraint trace term in the null action, is unchanged. The map is
locally invertible wherever f' is nonzero; inverse reparametrization
transports Euler equations. The same statements hold for anticonformal
maps, by composing with target complex conjugation.

A direct current check is useful because it retains the multiplier source.
Writing J^mu=Lambda grad^mu Psi and E=div J, one has

    J'^mu=J^mu/overline(f'),
    E'=E/overline(f')
        -Lambda overline(f'') q / overline(f')^2.         (6)

Here grad Psi dot grad overline(Psi)=q, with the SAME spacetime metric.
Consequently E'=0 whenever E=q=0. No scalar or connection equation is
removed; g, LC(e), and the entire right-hand side of Einstein's equation
stay exactly the same.

**Nonnull hostile control.** For a fixed nonzero q_* the off-shell matter
change under (4) is

    I_matter'-I_matter
       = integral vol_g Lambda q_* (D^-1-1).             (7)

Also q'=D q_* cannot equal the same q_* unless D=1 on the target image.
Thus the arbitrary conformal symmetry is specific to the zero sector. It
is not borrowed into timelike dust or a different kinetic constraint.

This is a standard type of target-conformal field reparametrization; no
claim of worldwide priority is made. The result consumed here is its
complete fibre characterization and application to the exact D0 source,
volume gauge and readout boundary.

## 3. Completeness: these are ALL local same-metric/same-source representations

**Theorem 1 (complete regular source fibre).** Suppose two positive-multiplier,
rank-two representations on the same coordinate neighborhood satisfy

    Lambda dpsi^T dpsi = Lambda_hat dpsi_hat^T dpsi_hat.   (8)

Then, after shrinking to a local product neighborhood, there is a unique
local target diffeomorphism f on psi's image such that

    psi_hat=f(psi),
    Df^T Df=(Lambda/Lambda_hat) I_2.                     (9)

It is conformal or anticonformal, and (4) gives the multiplier. Conversely,
every such map satisfies (8). This theorem is about equality of the entire
tensor, not its trace, determinant, norm, or selected contractions.

**Proof.** For any real tangent V,

    T(V,V)=Lambda sum_A (V psi_A)^2.

Positivity implies ker T=ker dpsi, and likewise for psi_hat. Thus their
rank-two kernel distributions agree. In submersion coordinates
(psi_1,psi_2,z_1,z_2), both components of psi_hat are independent of z.
They are therefore functions f(psi). Rank two makes Df invertible.
Substituting dpsi_hat=Df dpsi into (8) and using surjectivity of dpsi gives
(9) on the full two-dimensional target tangent space. Its conformal factor
is necessarily constant along the local fibres. The sign of det Df is
constant on a connected small domain. For positive orientation, (9) is
the Cauchy-Riemann system; for negative orientation compose with conjugation.
This proves both necessity and sufficiency. End of proof.

If both configurations already obey (2), the maps just classified preserve
all their equations by section 2. There are no additional hidden local
same-(g,T) branches on this regular positive rank-two chart. Rank drops,
zeros/sign changes of Lambda, nonlocal fibre topology and global monodromy
are not classified by this local statement.

## 4. Intrinsic source test and constructive reverse realization

**Theorem 2 (label-free local realization).** Let T be a smooth symmetric
covariant tensor on a smooth Lorentz four-manifold. Assume T is positive
semidefinite as a real bilinear form, has rank two, is g-traceless, and is
covariantly conserved. Then locally there exist Lambda>0 and two independent
real scalars satisfying T=Lambda sum_A dpsi_A^2, q=0 and E_A=0 if and only if:

(a) D=ker T is an integrable rank-two distribution;

(b) for every vector field V tangent to D, there is a scalar beta_V with

    Lie_V T = beta_V T.                                 (10)

Condition (b) says that the conformal class induced transversely to the
kernel leaves is independent of the point chosen on a leaf. It does not
say T itself is constant along a leaf.

**Necessity.** Exact scalar gradients give an integrable common kernel.
For V psi_A=0, Lie_V(dpsi_A)=d(V psi_A)=0, so
Lie_V T=(V log Lambda)T. Tracelessness and current conservation give the
stated trace and divergence conditions through (12) below.

**Sufficiency, with the actual reconstruction.** Frobenius gives local
coordinates (u^1,u^2,z^1,z^2) with D tangent to the z-fibres. The only nonzero
components are a positive-definite 2-by-2 block T_ab(u,z). From (10),

    partial_zj T_ab=beta_j T_ab.

Dividing by T_11>0 shows every ratio T_ab/T_11 is independent of z. Hence
T=c(u,z) h_ab(u) du^a du^b, with c>0 and h a smooth Riemannian two-metric.

Choose a local h-harmonic function p with dp nonzero. Such a choice follows
from a harmonic coordinate chart. On a simply connected smaller target
patch, harmonicity makes *_h dp closed, so set dr=*_h dp. Then

    dp wedge dr=|dp|_h^2 vol_h !=0,
    h=|dp|_h^-2 (dp^2+dr^2).                            (11)

Thus psi_1=p(u), psi_2=r(u), Lambda=c/|dp|_h^2 reconstruct T exactly.
This is the usual two-dimensional isothermal-coordinate construction,
not a claim that arbitrary transverse dimension is conformally flat.
For the harmonic-coordinate existence input see Liimatainen and Salo,
*n-harmonic coordinates and the regularity of conformal mappings*,
arXiv:1209.1285, Theorem 2.1, specialized to p=2. The subsequent inverse
construction and source application are the explicit calculations above.

The trace condition gives q=0. For any exact scalar gradients one has

    nabla^mu T_mu nu
       =sum_A E_A partial_nu psi_A +(Lambda/2)partial_nu q.  (12)

Conservation, q=0 and independence of the two gradients imply E_1=E_2=0.
This finishes the converse. End of proof.

**Metric-only corollary.** Set T=G(g). Conservation is automatic. A metric
belongs locally to this regular positive null two-field Einstein class
exactly when its Einstein tensor has the positivity/rank/trace conditions
and (a)-(b). The recovered LC connection solves the original independent
connection equation. The source representation is unique precisely up to
Theorem 1. This is an intrinsic characterization of THIS sector, not a
claim that every GR stress tensor has this form.

**Necessary hostile control.** In Minkowski coordinates (t,x,y,z), on |y|<1,
put T_00=T_11=1, T_01=T_10=y, with all other components zero. It is positive
rank two, traceless, divergence free, with integrable kernel span(d_y,d_z).
But Lie_(d_y) T has zero diagonal and a nonzero off-diagonal entry, so it
cannot be a scalar multiple of T. It has no representation of the form (8)
with two exact independent scalar labels and a common positive multiplier.
This is a tensor-level countercontrol, not an Einstein solution with flat g
and nonzero T. Dropping (b) would enlarge the claimed class incorrectly.

## 5. Apply the inverse and fibre to the already-owned non-VSI solution

Reuse the unchanged source-pinned witness, with b,d>0 and F=exp(db^2/2):

    g=bF db^2-(F/b)dx^2-b^2(dy^2+dz^2),
    psi_1=s=b^2/2, psi_2=x, Lambda=d/b^2,
    T=d db^2+(d/b^2)dx^2.                               (13)

The old curvature proof supplies G=T and R=0. Here the kernel leaves are
the (y,z) surfaces; their transverse tensor has no leaf dependence.
Theorem 2 reconstructs the two labels explicitly: for
h=d db^2+(d/b^2)dx^2, *_h(b db)=dx. Thus (11) returns exactly s=b^2/2 and x,
with factor Lambda=d/b^2. No new curvature ansatz or root search is used.

The full same-source family is therefore

    Psi_f=f(b^2/2+i x),
    Lambda_f=d/[b^2 |f'(b^2/2+i x)|^2],
    g_f=g.                                               (14)

Every equation, the entire stress tensor and both nonzero curvature
invariants of the inherited witness are unchanged. This integrates the
source fibre to ALL orders; it is not merely a zero Hessian direction.

## 6. Complex scalar characteristics: exact interpretation and full nonlinear control

At a point of (13), an orthonormal frame gives

    dpsi_1=a dt, dpsi_2=a dx, a=sqrt(b/F)>0.

For general positive amplitudes a,b_1, the frozen leading equations for
u=delta psi_1, v=delta psi_2 and l=delta log Lambda are

    u_tt-u_xx+a l_t=0,
    v_tt-v_xx-b_1 l_x=0,
    a u_t-b_1 v_x=0.                                    (15)

Keeping both gradient-integrability equations, set Z=(u_x,v_x,v_t,l).
Then Z_t=A Z_x, where

    A=[[0,b_1/a,0,0], [0,0,1,0],
       [0,1,0,b_1], [1/a,0,-b_1/a^2,0]],
    det(cI-A)=(c^2-1)(c^2+b_1^2/a^2).                  (16)

At (13) the speeds are +1,-1,+i,-i. The corresponding coordinate slopes
in (b,x) are +b,-b,+ib,-ib. For a=b_1=1 an explicit real growing solution is

    u=-(exp(kt)/k)cos(kx),
    v=-(exp(kt)/k)sin(kx), l=2exp(kt)cos(kx).              (17)

It satisfies the full scalar principal equations and norm constraint.
Crucially, DIRECT substitution gives

    delta T = l X + sum_A(dpsi_A tensor d(delta psi_A)
                         +d(delta psi_A) tensor dpsi_A)=0. (18)

An initial diagnostic conjecture that (17) forced a nonzero metric stress
was rejected by this exact check. Zero metric perturbation is compatible
with the coupled source, not an omission of the Einstein equations.
Equation (17) is the infinitesimal form of the holomorphic family (14).
No conclusion that a quotient by that family is strongly hyperbolic follows.
Even the rank-one real-root limit has a Jordan block in this reduction.

A general useful symbol control is

    det [[Lambda k_g^2 I_m, u],[u^T,0]]
       =-(Lambda k_g^2)^(m-1) sum_A u_A^2,
    u_A=grad psi_A dot k.                                (19)

For k=omega n+xi its extra quadratic has discriminant
-4(|u(n)|^2|u(xi)|^2-[u(n).u(xi)]^2). Complex roots in scalar labels must
therefore be checked against the complete stress and observational quotient,
not simply called gravitational modes.

### Exact nonlinear discontinuity for the unquotiented fields

This conclusion does not rely on a frozen-symbol extrapolation. Fix
s0<s1, 0<c<1/2, a spatial interval of length L, and k_n=2pi n/L. On the
whole slab s0<=s<=s1 define

    f_n(z)=z+(c/k_n)exp(k_n(z-s1)),
    D_n=|1+c exp(k_n(s-s1))exp(i k_n x)|^2.                (20)

Uniformly, (1-c)^2<=D_n<=(1+c)^2, so all transformed fields stay regular
and Lambda_n>0. These are exact solutions (14). Their metric, extrinsic
geometry and stress are IDENTICAL, not just close.

On the initial slice s=s0, every fixed finite-order spatial/time derivative
of the differences in psi and Lambda is bounded by a polynomial in k_n
times exp[-k_n(s1-s0)]. Thus their scalar Cauchy data and multiplier data
converge in every fixed finite Sobolev/C^m norm on compact subsets.
On the final slice,

    Lambda_n/Lambda = [1+2c cos(k_n x)+c^2]^-1.            (21)

Its mean over L is 1/(1-c^2), by the two convergent geometric Fourier
series. Cauchy-Schwarz therefore gives the n-independent bound

    ||Lambda_n/Lambda-1||_L2 >= sqrt(L)c^2/(1-c^2)>0.      (22)

This is exact failure of continuous dependence for the unquotiented
scalar/multiplier solution fields, in the fixed covariant chart and this
class of smooth solutions. It is NOT failure of continuous dependence of
g or T: those never changed. There is no proof here of well-posedness of
the source quotient, and no theorem of native D0 instability. The use of
an interval does not assume psi_2=x is a single-valued scalar on a circle;
only the perturbation has an integral number of periods. A small local
interval can be used to respect inherited bounded matter charts.

## 7. Native gauge: exact obstruction and the required transport

**Theorem 3 (fixed native metric fibre).** If two configurations are in the
SAME gauge (3), with the SAME g and mu0 and the SAME k0, then Lambda is fixed.
If they also have the same rank-two source, Theorem 1 gives Df^T Df=I_2.
Every local C^2 Euclidean isometry is rigid. Hence the whole fibre is only

    psi_hat=O psi+a, O in O(2), a constant vector.         (23)

For completeness, on the orientation-preserving branch f' is holomorphic
with |f'|=1. The Cauchy-Riemann equations force f' to be constant; the reverse
orientation case is conjugate. Thus a varying conformal target factor
CANNOT be called a same-fixed-native-metric gauge freedom.

The covariant family (14) does have original native representatives, but
the actual volume transport must be retained. On the witness its Jacobian is

    partial t_f/partial b
       =(d/k0) exp(db^2/2) / |f'(b^2/2+i x)|^2,
    (x,y,z) unchanged.                                  (24)

Take t_f as the integral of this positive expression in b from a fixed
b0. The full coordinate matrix is triangular apart from its first row,
so its determinant is exactly (24). The generally nonzero partial_x t_f
induces a metric shift and must not be dropped. In the new coordinates

    e_native=k0 b^2 |f'|^2/d,
    Lambda_f=d/[b^2 |f'|^2], e_native Lambda_f=k0.         (25)

This is a coordinate transport of the covariant geometry into the fixed
volume description, not a newly admitted physical clock operation. It need
not preserve an arbitrary original collar or the original physical time.
The covariant-chart discontinuity (22) is not automatically a statement
about solutions with the same native time/constraint data.

The inherited weighted-null corollary applies to EACH of these native
representatives. At R=q=0, with fixed positive PF density rho and common
constant price slopes and D_field B0=0,

    DS_rho=M tau integral [F_x(0,0)delta(eR)
                          +F_y(0,0)delta q].            (26)

All rho factors cancel before integration by parts. With the original
-F_y/F_x=k0, the full continuum field equations hold for the family in
its respective native gauge. This retains both independent scalar currents
and all coframe/connection rows. The genuine finite-lattice lift, paid
physical field writer, independent input price and clock transport do not
follow from (24)-(26).

## 8. A necessary-and-sufficient LOCAL readout descent criterion

Theorem 1 supplies a direct test, without a new physical selector.
For a supplied observable on this regular covariant solution space, local
descent to a function of (g,T) is equivalent to invariance under every
admissible local conformal/anticonformal target map (4). This is simply
constancy on the now completely classified fibres.

For a differentiable observable O, a necessary infinitesimal test is

    DO[delta g=0, delta Psi=h(Psi),
       delta Lambda=-2Lambda Re h'(Psi)]=0               (27)

for every holomorphic h on the actual target patch. With regular dependence,
this also gives invariance under connected local flows; reflection is a
separate discrete check. Near identity, the homotopy f_t=(1-t)id+t f has
nonzero derivative on a sufficiently small common patch, and its velocity
h_t=(f-id) composed with f_t^-1 is holomorphic, proving that implication.

For an actual native execution O must include the genuinely moved preparation,
oldRIGHT/reference, work, cuts, clock and its absolute valuation. The required
native direction includes (24)'s coordinate/cut/clock transport whenever one
claims covariant rather than fixed-volume identification. A terminal scalar
response r(x,y) at x=y=0 alone cannot test that full statement. Source
invariance is not an operational proof that independently prepared quantum
states or paid histories are indistinguishable.

Consequently there are two distinct valid consumers. A proved invariance of
one supplied full execution would permit the corresponding source quotient.
A nonzero response of that execution would instead require those fibre
variables and their full independent source equations to be retained.
No outcome is declared by choosing a convenient notion of Info.

This replaces an unspecified 'extra scalar' issue by the exact fibre (4),
the fixed-native restriction (23), and one concrete full-price/readout test
(27) with the actual volume/clock transport. It does not replace the existing
Book03 absolute normalization and same-history admission gates.

## 9. Reproduction, provenance and limits of the checks

Run `python check_source_fibre.py` and `python -O check_source_fibre.py`.
Both executions passed 87 exact groups and produced byte-identical JSON.
Checks use explicit exceptions rather than assertions; optimization does
not delete controls. No network access or external files are needed except
SymPy. The symbolic tensor, conformal/current, exact native Jacobian and
principal-symbol identities are checked independently of stored curvature
matrices. The complete fibre and intrinsic inverse are analytical proofs;
finite examples are not presented as proving their universal quantifiers.

The important diagnostic correction is retained in RESULT.json: nonzero
stress for the growing mode was an incorrect preliminary conjecture, not
a result. Exact calculation gives zero and leads to the nonlinear family.
No independent review, fresh full historical certificate/Lean build or
remote CI acceptance is claimed. This is author-checked research, published
without changing the parent scientific acceptance state.

Background only: the multiplier formulation is standard in the multifield
mimetic literature, e.g. Shen, Zheng, Li, arXiv:1909.01248, Eq. (15). Their
homogeneous, nonzero kinetic-sector perturbation analysis is not substituted
for the inhomogeneous rank-two NULL calculation here. Harmonic-coordinate
existence is used only as specified in section 4. All D0 normalization,
weight and field-source premises come from the pinned repository owners.
