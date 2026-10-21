# Exact correction-class closure from the existing two-scalar solution space

21 October 2026. Supporting continuation inside the existing research owner
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, PR #334.
Input repository snapshot: `5edac80c86c17014fc83e0aa608e192f43c1fdba`.

## 0. Exact target and result

The previous two-field packet explicitly left open the Euler source of a
higher-curvature correction on its new non-VSI witness. Nonzero curvature
invariants alone do not settle that question. This packet computes that
source and combines it with the ALREADY owned positive dust solution class.
It does not introduce a new physical action or start another root search.

Let `S0` be the same configured continuum price whose full stationary fields
include the source-owned crossing-stream solution and its positive
irrotational-dust sector, in their correct native volume coordinates.
Consider a possible **remaining metric source** with local functional

    Delta S = integral vol_g [ f(R) + beta Ric_mn Ric^mn + gamma GB ].       (0.1)

Here beta and gamma are constants, all original matter fields and their
source normalization are held, and variations have compact support or the
original appropriately transported collar. `GB` is the four-dimensional
metric Euler density. In a first-order extension, its harmless replacement
must be the actual topological Euler form, not an assumed torsion identity.
The scalar function is single-valued on a connected branch near R=0.

**The strongest proved application.** Assume f is C1 at R=0 and C3 on
its punctured curvature interval. Requiring the SAME crossing-stream solution
and the anisotropic representatives of the SAME two-scalar stationary class
to survive (0.1), with their SAME scalar fields and multiplier normalization,
forces

    beta=0,  f(R)=0 throughout the sampled connected curvature interval. (0.2)

Only gamma GB remains as a metric boundary term. When both signs of the
original small kinetic sector are included, the test covers BOTH signs of R.
When only the timelike/positive-dust sector is included, it proves f=0 on
the sampled negative-R side; no positive-side conclusion is then implied.
There is no analyticity assumption, flat C2 assumption, bounded f'' at zero,
finite-algebraic-log assumption, or unproved stationary-elimination assumption
in this strongest result.

The crossing transverse row first forces beta=0 and f(0)=f'(0)=0. An exact
anisotropic representative then has the independent source difference

    E^f_11/g_11 - E^f_22/g_22
       = -4 A(2v+A) f''(R)/(3 v^3(v+A)^3),  v,A>0.                     (0.3)

Its coefficient is strictly nonzero for both causal sectors. Thus f''=0
on each sampled side; the actual C1 matching at R=0 and crossing conditions
force each affine remainder to be zero.

The earlier isotropic-dust calculation is retained below as a sharp control:
it alone leaves the two powers (-R)^((7 +/- sqrt(73))/12). A finite
Puiseux-log price excludes those powers, but such structure is not automatic
after arbitrary stationary input elimination. Equation (0.3) removes that
loophole without invoking that price-class premise. In a genuinely
independent-Lorentz scalar correction, the connection equation supplies a
separate, even shorter f''=0 test on varying-curvature timelike dust.

All constant-coefficient, parity-even quadratic METRIC corrections are
therefore removed modulo the Euler boundary term. The full scalar f(R)
class is also removed on the stated sampled domain, not merely a finite
Taylor truncation. The new anisotropic metrics are explicit members of the
already owned continuum representation, not new native finite-lattice roots.

This is a source-uniqueness result in the explicitly specified correction
class, **not a proof that the full native Book price belongs to that class**.
The original Book admission, independent inputs, physical refinement and
raw216 obligations are not discharged. `GR_closed=false`.

## 1. Source convention and the original crossing-stream witness

Use signature (+---) and

    R^a_bcd = partial_c Gamma^a_db - partial_d Gamma^a_cb
              + Gamma^a_ck Gamma^k_db - Gamma^a_dk Gamma^k_cb,
    Ric_bd = R^a_bad,
    delta Delta S = integral vol_g E_mn delta g^mn.

The existing witness in coordinates (b,xi,y,z), for b,d>0, is

    W(b)=exp(d b^2/2),
    g=diag(b W,-W/b,-b^2,-b^2),
    psi1=b^2/2, psi2=xi, Lambda=d/b^2.

It has Ric=diag(d,d/b^2,0,0), R=0, and q=sum_A |dpsi_A|_g^2=0.
Its native volume coordinate satisfies d tau/db=(d/k0)W, giving
`e_native Lambda=k0`, with k0 the original finite Golden coefficient,
not a coefficient fitted here. Covariant tensor tests may be carried out
in b coordinates and then transported; no fixed-volume functional is
silently treated as invariant before that transport.

For Q=Ric_mn Ric^mn the full inverse-metric Euler tensor is

    E^Q_mn = 2 R_manb Ric^ab + Box Ric_mn - nabla_m nabla_n R
             + (g_mn/2)(Box R-Q).                                      (1.1)

It follows by variation of integral vol_g Q. At the witness the scalar
R and all of its derivatives vanish, but the tensor derivatives do not.
Direct calculation on ALL sixteen matrix entries gives

    E^Q_bb   = d(db^2-2)/(b^3 W),
    E^Q_xixi = d(3db^2+2)/(b^5 W),
    E^Q_yy   = E^Q_zz = -d(db^2+2)/(b^2 W^2),
    E^Q_mn   = 0 for m != n.                                            (1.2)

In particular E^Q_yy is strictly negative everywhere on the patch.
The checker also verifies the full divergence is zero and the trace is
zero. These checks supplement, rather than replace, the direct variation.

A separate calculation varies a transverse scale factor
`a_y -> a_y exp(epsilon h(b))` in the curvature-square ACTION DENSITY,
without using (1.1). After integrating the coefficients of h',h'' by
parts, its first-order Euler coefficient is

    -2d(db^2+2)/(b^2 W)
       = 2 vol_g E^Q_yy/b^2.                                           (1.3)

This is an independent algebraic derivation of the decisive row, not an
independent-agent review and not an ansatz replacement for the full tensor.

For the scalar correction, on the same R=0 background,

    E^f_mn = f'(0) Ric_mn - f(0)g_mn/2.                                 (1.4)

Define the transverse ratio

    A(b)=E^Q_yy/g_yy=d(db^2+2)exp(-db^2)/b^4.

Its derivative is exactly

    A'(b)=-2d exp(-db^2)[d^2 b^4+3db^2+4]/b^5 < 0.                       (1.5)

If (0.1) has zero full source on this witness, its yy row requires
`-f(0)/2+beta A(b)=0` on an open b interval. Since f(0), beta are constants
and A is strictly monotone, beta=0 and f(0)=0. The bb row, with Ric_bb=d>0,
then gives f'(0)=0. Thus neither a cosmological term nor an unannounced
change of the gravitational coefficient can cancel this test at fixed
matter source.

This is stronger than testing one numerical point. It uses one existing
solution on its open coordinate patch, without assuming a field minimum.

## 2. The dust consumer and its native-volume map

Use a simple member of the already owned positive irrotational-dust class:

    ds^2=dt^2-t^(4/3)(dx^2+dy^2+dz^2),
    psi1=epsilon t, psi2=0,
    q_star=epsilon^2, Lambda=4/(3 epsilon^2 t^2), t,epsilon>0.              (2.1)

Direct computation gives

    R=-4/(3t^2),
    G=diag(4/(3t^2),0,0,0)=Lambda sum_A dpsi_A tensor dpsi_A,
    partial_t(t^2 Lambda epsilon)=0.                                   (2.2)

Choose epsilon sufficiently small that the same regular two-density price
has its trace branch at `Y_star=-eta^2 epsilon^2`, and let k_star>0 be the
ratio supplied by that branch. This is the existing local branch condition,
not a new choice of gravitational coupling. The coordinate change

    tau=[4/(3 epsilon^2 k_star)] t                                     (2.3)

gives `e_native=3 epsilon^2 k_star t^2/4`, hence

    e_native Lambda=k_star,
    eta^2 e_native R=k_star Y_star,
    g^(tau tau) partial_tau psi1=[4/(3 epsilon^2 k_star)] epsilon.

The last current is constant. The independent connection is Levi-Civita.
These identities place (2.1) inside the original configured full stationary
class through its previously proved reverse map. They do not claim a new
native finite-lattice realization. The test requires local dust patches
sampling a curvature interval (-r0,0), with accumulation at flat curvature
when the flat-regularity or Puiseux-germ conclusion is used. A single compact
interval bounded away from zero does not suffice for that extra conclusion.

## 3. Solve the ENTIRE scalar-correction equation

For a metric correction integral vol_g f(R),

    E^f_mn=f'(R)Ric_mn-f(R)g_mn/2
            +(g_mn Box-nabla_m nabla_n)f'(R).                            (3.1)

At (2.1), its 00 component is exactly

    2 E^f_00 = 6R^2 f''(R)-R f'(R)-f(R).                                (3.2)

Thus full source preservation implies the Euler equation
`6R^2 f''-R f'-f=0`. Write r=-R>0 and F(r)=f(-r). Its characteristic
polynomial is

    P(m)=6m^2-7m-1,
    m_plus=(7+sqrt(73))/12, m_minus=(7-sqrt(73))/12.                       (3.3)

The general solution on the connected negative-R interval is a linear combination of the two powers in (3.3).
This is not just a necessary time-row test with spatial rows ignored.
For f(R)=(-R)^m direct substitution in the full tensor gives

    E^f_00=P(m)r^m/2,
    E^f_ii=t^(4/3)(m-1)P(m)r^m/2,
    E^f_mn=0, m!=n.                                                      (3.4)

Both roots really annul every metric source component there. In particular,
`(-R)^m_plus` is a genuine C1, non-C2, invisible metric correction on this
negative-curvature dust branch, with a compatible C1 zero-side extension
at R=0. Calling all C1 corrections excluded would be false.

But m_minus<0, while 1<m_plus<2. A C2 extension to R=0 forces both
coefficients to vanish: the minus branch is unbounded; the second derivative
of the plus branch diverges. Real analyticity gives the same result and
continues the zero function to the connected analytic curvature interval.
No claim of a new general f(R)-reconstruction mechanism is made; the result
here is its exact application to the repository's same-price witnesses and
its combination with the transverse tensor source (1.2).

## 4. Finite algebraic-log prices: rank birth does not require C2

A useful replacement for C2 regularity is the following explicit class.
A convergent finite-ramification Puiseux-log germ has the form

    F(r)=sum_{j>=j0} r^(j/N) P_j(log r), N a positive integer,            (4.1)

with a finite common bound on the polynomial degrees and convergent
coefficient series on a punctured interval. The nonzero germ has a least
exponent j/N and then a highest nonzero log power at that exponent; there
is no unspecified flat remainder.

**Lemma.** The only such germ solving `6r^2 F''-rF'-F=0` is zero.

Proof. Write the operator as `6D^2-7D-1`, D=r d/dr. On
`r^a P(log r)` its highest log coefficient is multiplied by
`6a^2-7a-1`. For a rational exponent a=j/N this number cannot vanish,
because the discriminant 73 is not a rational square. The leading term
of a nonzero germ therefore cannot solve the equation. Equivalently,
the exact two possible powers (3.3) are irrational. End proof.

This covers the relevant **fixed finite algebraic matrix calculations**
when their actual reduced field graph is algebraic in r: eigenvalues are
algebraic branches; after finite ramification each is `r^a A(r^(1/N))`.
The logarithm is `a log r+log A`; finite traces, fixed powers, inverse
matrices on their true chart, log determinants and terms `lambda log lambda`
have expansions of type (4.1). Finite code averages with algebraic
probabilities do too. Zero eigenvalues and their usual entropy births are
included; a spectral lower bound or automatic C2 upgrade is unnecessary.
The use of rational Puiseux exponents is the standard local algebraic
branch property, not a property of golden-ratio number mysticism.

**This membership must be checked on the actual full source graph.** It
is not a universal theorem about everything called Book03 Info. Infinite
horizon/mesh limits, arbitrary exponentiation of logarithmic gains,
nonalgebraic field maps, and stationary elimination of independent inputs
are not automatically covered. Fixed finite algebraic causal generation
is covered; an arbitrary stationary solution map is not.

The following exact hostile control makes the last boundary unavoidable:

    U(r,u)=u[log u-alpha log r-1], r,u>0,
    U_u=log u-alpha log r=0  =>  u=r^alpha,
    U_reduced=-r^alpha.                                                   (4.2)

The two-variable expression is algebraic-log. An irrational algebraic alpha
can give an irrational reduced power. Thus one cannot invoke (4.1) after
eliminating an independent preparation merely because the unreduced finite
ledger contained only algebraic operations and logarithms. This is a test
of a proposed reduction, not a new native action or chosen compensation.

## 5. Anisotropic source subtraction closes the entire scalar class

The isotropic calculation has a genuine fractional-power blind direction.
The original regular-price correspondence covers ALL local positive-multiplier
solutions in a chosen small kinetic sector, not only the isotropic member.
Use the following explicit representatives. Let v,A,epsilon>0 and
sigma in {+1,-1}, and define

    a1(v)=v(v+A)^(-1/3),  a2(v)=a3(v)=(v+A)^(2/3),
    V(v)=v(v+A),  rho(v)=4/[3V(v)],
    g_sigma=diag(sigma,-sigma a1^2,-a2^2,-a3^2),
    psi1=epsilon v, psi2=0, Lambda=rho/epsilon^2.                         (5.1)

Both metrics have Lorentz signature (+---). At sigma=+1 coordinate v is
time and this is anisotropic pressureless dust. At sigma=-1 coordinate 1
is time and v is space; this is the spacelike-scalar sector of the SAME
constrained-scalar model. It is NOT called ordinary physical dust, and
no claim of empirical or native microscopic admission is made for it.

### All original continuum rows and the volume gauge

The checker constructs the complete Einstein tensor afresh and verifies

    G_mn=diag(rho,0,0,0)=Lambda dpsi1_m dpsi1_n,
    q_star=sigma epsilon^2,
    R=-sigma rho,
    partial_v(V Lambda sigma epsilon)=0.                                (5.2)

Every other current component and the second scalar equation vanish.
The connection is Levi-Civita. Let k_sigma>0 be the ratio of the original
regular price at its trace root with Y_star=-eta^2 sigma epsilon^2.
Such small roots of BOTH signs exist when F_x(0,0) is nonzero and the
original positive ratio is continuous: apply the implicit-function theorem
to T=xF_x-YF_Y, with T_x(0,0)=F_x(0,0). No ratio is fitted to this metric.

The actual positive volume-gauge coordinate is simply

    tau=c v,  c=4/(3 epsilon^2 k_sigma),
    e_native=V/c,
    e_native Lambda=k_sigma,
    eta^2 e_native R=k_sigma Y_star,
    g^(tau tau) partial_tau psi1=sigma c epsilon.                         (5.3)

Thus all metric/coframe, independent connection and both scalar equations
of the source-owned fixed-measure continuum price hold. The same original
query branch and supplied source ratio are used. The two signs use their
respective allowed kinetic sectors, not an unauthorized variation of a
fixed-sector constraint in a single covariant action. Local scalar shifts
can keep amplitudes in an admitted open scalar chart on each local patch;
no global infinite-volume CAR state is claimed.

For a fixed A>0, rho decreases continuously from infinity to zero on v>0.
The local representatives therefore sample any subinterval of the positive
or negative scalar-curvature axis allowed by the correction's domain.
The matching-at-zero conclusion uses a family of such patches approaching
R=0, not a single compact patch bounded away from zero. No uniform native
refinement, physical clock or same-fixed-boundary realization is inferred.

### Full source difference, without a symmetry-restricted variation

For an arbitrary differentiable scalar u(v), the full covariant Hessian
obeys

    (nabla_1 nabla_1 u)/g_11 = sigma (a1'/a1)u',
    (nabla_2 nabla_2 u)/g_22 = sigma (a2'/a2)u'.

Here a1'/a1-a2'/a2=A/[v(v+A)] is strictly positive. Since
Ric_11/g_11=Ric_22/g_22=R/2 on (5.1), the isotropic terms in the full
metric Euler tensor (3.1) cancel in their difference. Taking u=f'(R) gives

    E^f_11/g_11-E^f_22/g_22
      =-sigma A/[v(v+A)] (d/dv)f'(R)
      =-4A(2v+A)/[3v^3(v+A)^3] f''(R).                                 (5.4)

This is a subtraction of two independent ambient source components after
the full variation. It does not assume variations restricted to the metric
ansatz. The checker verifies the full Einstein tensor and this identity
with symbolic u(v), F(v) for BOTH sigma signs. The source coefficient is
strictly negative on every patch. Setting A=0 is an exact hostile control:
the row then disappears, recovering why isotropic dust alone failed.

Full source preservation now gives f''=0 on each sampled open curvature
interval. Therefore f=a_sigma R+b_sigma there. Combining with the already
forced crossing values f(0)=f'(0)=0 and C1 matching at zero yields a_sigma=
b_sigma=0. This proves (0.2). If only sigma=+1 is part of the chosen physical
interpretation, the proof stops at the negative-R conclusion; the positive
side is not obtained by an unjustified analytic continuation.

This upgrade supersedes the need for section 4's Puiseux-log membership in
the strongest correction test. Section 4 remains a valid finite-price
application and a necessary warning about arbitrary upstream elimination.

## 6. Separate original independent-connection scalar test

Suppose the scalar correction is genuinely first order,
`integral epsilon_abcd e^a wedge e^b wedge R^cd` with coefficient f'(R)
in its connection variation. At a torsion-free original connection,
its own Lorentz equation reads

    d f'(R) wedge e^a wedge e^b=0 for every internal pair.                (6.1)

For a nondegenerate four-coframe, the wedge map in (6.1) is injective on
one-forms: for each nonzero component choose two different remaining
basis legs. Hence d f'(R)=0. On (2.1), dR/dt=8/(3t^3) is nowhere zero,
so f''(R)=0 on its entire sampled interval. Thus f=aR+b there. A C1 match
to the crossing point, with f(0)=f'(0)=0, gives f=0.

This argument retains the original independent Lorentz rows. It must NOT
be used for a metric-only effective f(R) functional after a different
connection has been eliminated: that different problem has the genuine
fractional solutions (3.3) on ISOTROPIC dust alone. Likewise a proposed correction to the first-order
curvature-square tensor may have additional torsion-source rows. The metric
pullback test in sections 1-3 is necessary for the same full field root,
not a proof that arbitrary independent-connection rows have disappeared.

## 7. Exact quadratic closure and a boundary that prevents overclaiming

In four-dimensional metric geometry,

    Riem^2=GB+4 Ric^2-R^2.

Therefore aR^2+bRic^2+cRiem^2 has metric source
`(a-c)E^(R^2)+(b+4c)E^Q`. The crossing transverse row sets b+4c=0.
The dust row `E^(R^2)_00=8/t^4` sets a-c=0. Only c GB remains.
Thus the complete parity-even curvature-quadratic ambiguity is closed in
this metric source class, including the old R^2 blind spot of the VSI route.
The checker additionally verifies `E^Q=E^(R^2)/3` on the dust metric;
using the dust example alone would not separate the two quadratic terms.

Even preservation of the ENTIRE two-scalar stationary class does not
identify an arbitrary higher-curvature price. For every one of those
solutions,

    G_mn=Lambda sum_(A=1)^2 dpsi_A_m dpsi_A_n

has rank at most two. Hence the genuine scalar polynomial

    D(g)=det(G^mu_nu)

vanishes. The nontrivial correction

    Delta S_hidden=integral vol_g D(g)^2                                (7.1)

has zero first variation on EVERY such solution: D=0 identically, and
`delta(vol_g D^2)=delta(vol_g)D^2+2 vol_g D delta D=0` before integration
by parts. It is not an identically trivial action. For nonzero constant
curvature K, G^mu_nu=-3K delta^mu_nu and D^2=6561 K^8. Under constant
metric scaling g->exp(2s)g its density scales as exp(-12s), so its Euler
source is nonzero there. The checker verifies a rank-two determinant
fixture, the squared-ideal derivative, and this nonzero scaling control;
the all-solution rank argument is analytical.

This precise countercontrol prevents upgrading the proved f(R)+quadratic
result to uniqueness among ALL local metric actions. It is not inserted
into the native D0 price. It explains why the existing physical scale/order
or source-descent theorem still has independent work to do.

For comparison, `[R C_abcd C^abcd]^2` already evades the crossing and
ISOTROPIC-dust witnesses alone. It is NOT asserted invisible on the added
anisotropic metrics. Both controls are kept distinct in the checker.

## 8. Substitution into the existing closure architecture

The consumed parent gap is the **unclassified source-order/correction
ambiguity** in the old VSI/Lovelock route, specifically the explicitly open
higher-curvature source on the new rank-two witness. The result replaces:

    'R^2 and Ricci^2 may be invisible on the known wave family'

by the exact decision:

    'They cannot preserve the source-owned crossing and anisotropic scalar
     sectors with the same matter source; the entire C1-at-flat f(R) class
     is removed on the corresponding sampled domains.'

No premise is discharged for arbitrary nonlocal Book actions, torsion,
field-dependent coefficients, additional matter/clock/preparation sources,
or for a correction deliberately built from the original equations.
The native finite compiler has not been lifted to this new continuum
witness by this calculation. There is no claim of a uniform raw216 limit,
physical minimum, off-shell equality with CQ, or unconditional GR closure.

The Book gate inspected at the input SHA still leaves its branch gain and
absolute source unselected on one complete physical execution. We do not
replace them with Shannon information to assert progress. The new test is a
usable source discriminator once that execution or its exact residual is
supplied; it can reject the specified correction classes without a new
geometric census or a fitted counterterm.

## 9. Reproduction, provenance and verification scope

Run from this directory:

    python3 -B check_price_source_rigidity.py > actual.json
    python3 -O -B check_price_source_rigidity.py > optimized.json
    cmp actual.json optimized.json

The script constructs the full connection, curvature, tensor Laplacian and
Euler tensors directly. It also varies the transverse action independently.
Its checks are exact symbolic identities with positive symbolic b,d,t;
there are no fitted tolerances or numerical finite differences. All checks
remain active under -O. The symbolic proof of the full function class is
in sections 3-6, not an inference from a finite exponent scan.

No independent human/agent review, fresh Lean build, repository-wide CI or
physical acceptance is claimed. The ordinary and optimized replay outputs
and local hashes are recorded separately. The first draft's numeric literal
inversion was corrected to exact SymPy rationals; the final checker rejects
floating metric inputs. No failed run is relabelled as passing.

Consumed repository owners (read at the input SHA):

* `sources/d0_covariant_multiscalar_price_2026-10-21/CROSSING_STREAMS.md`:
  the original two-field metric, currents and volume-gauge map.
* `sources/d0_covariant_multiscalar_price_2026-10-21/REVIEW_ADDENDUM.md`:
  the regular-price positive-multiplier representation and sector conditions.
* `A4D_FINITE_SOURCE_AND_COVARIANT_TWO_FIELD_SYNTHESIS_2026_10_21.md`:
  the full composition and its missing native-lattice application.
* `A4D_NATIVE_BOOK03_CLOSURE_GATE_2026_10_21.md` and
  `A4D_NEXT_COMMON_MAP_CONSTRUCTION_GATE_2026_10_21.md`:
  current physical source and input boundaries, kept open.

Standard variational background is checked against primary scholarly sources:

1. R. Svarc, A. Pravdova, D. Miskovsky, *The Newman-Penrose formalism in
   quadratic gravity*, arXiv:2209.15089, section 1.1 (quadratic action,
   Euler/Bach source and four-dimensional reduction):
   https://arxiv.org/html/2209.15089
2. T. P. Sotiriou, V. Faraoni, *f(R) theories of gravity*,
   arXiv:0805.1726, sections II.1-II.2 (metric versus Palatini variation):
   https://arxiv.org/html/0805.1726
3. C. J. Chapman et al., *Non-dimensional Newton-Puiseux Expansions*,
   arXiv:2111.05762 (background on rational-exponent expansions):
   https://arxiv.org/abs/2111.05762

The full crossing Euler tensor, exact anisotropic source difference on both
kinetic sectors, proof of the combined correction-class closure, finite-log
application and explicit upstream-elimination control are provided here.
Their publication does not assert priority for general quadratic gravity,
dust cosmology, the Cauchy-Euler method or Newton-Puiseux theory.
