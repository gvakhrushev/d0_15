# Joint adjoint class, realizable metric variations and the full bootstrap covector

Research continuation, 2026-10-13. Input SOURCE
`9f2028bdf6b5ff708e5b46e4476e3fb4a305b34f`. Existing #310 and CONTROL #322;
original #310/#202/#317 and G0–G4 remain open. No action, selector, physical
postulate, or replacement of a supported operator is installed.

The previous curved packet kept the observer and internal links fixed. This
packet exhausts the same stored operator with arbitrary unit observers and
Lorentz links. Full exterior adjointness forces both observer-pairing and
leg transport. The resulting local metric image is explicitly characterized
and every metric direction in it has an exact nonlinear realization. Some
full joint solutions of the linearized equations nevertheless fail a
second-order holonomy test: a formal linearized solution is not automatically
a velocity of an admitted curve.

A separate calculation gives the complete tangent and joint covector of the
existing heat/feedback functional on its actual positive-pairing, projector,
unitary interface. It retains the Gram derivative and distinguishes a change
of physical data from a simultaneous basis change. Its pullback to the native
geometric/recording preparation still requires that preparation's own map.

## 1. Owners and precise class

On the complete finite carrier `(Z/LZ)^4 x exterior(Role)`, L=N+2>=2,
retain all sixteen exterior components in degrees 0 through 4. At each site
let F be an invertible raw solder, eta=diag(1,-1,-1,-1), and

    v_r = eta F_r^T,   q=F eta F^T,
    n^T eta n=1,       h_n=-eta+2 eta n n^T eta.

The observer form h_n is positive definite and det h_n=1. For example,
`h_n^-1=-eta+2 n n^T`; the determinant follows from the rank-one determinant
formula and n^T eta n=1. The full site pairing G_n is the induced exterior
Gram, with counting weight between sites. No independent site-volume factor
or arbitrary additional graded Gram is included in this first class.

For edge x->y=x+r, A_xy is the linear part of the actual affine pull link,
`A^T eta A=eta`. Its exterior lift E=Lambda(A) pulls y to x. Translations
remain available in the carrier but do not enter this operator. The legs,
forward differential d, stored lower operator ell and D=d+ell are exactly
`archiveSolderedForwardDifferential`, `archiveSolderedCodifferential` and
`archiveSolderedDirac` in `ArchiveAffineExteriorLink.lean`. The positive
observer form and creation/contraction pairing are owned by
`A4DObserverPositiveExterior.lean`.

Creation is C(v), contraction is i_(h v), and C(v)^dagger=i_(h v). Thus

    d=L sum_r C(v_r)(T_r-I),
    ell=L sum_r i_(h v_r)(T_r^-1-I),                     (1)

where T_r is the actual edge pull followed by the forward site shift.
No nilpotency of this variable-coefficient d is assumed. The ACDB exterior
basis and ABCD CAR basis are related by the explicit sign conjugation proved
in the preceding packet; all tests use that conversion.

BOOK_03 sections 03.1.1–03.1.2 specify a scene spectral triple and Delta=D^2
for its selected D. Section 03.25 specifies the bootstrap functional of
Delta and feedback. Neither statement identifies the scene D with (1).
The frozen weighted-Hodge construction is also a different family. In
particular, the actual proposition `archive_weighted_hodge_dirac_owner`
contains cardinalities and a Boolean degree-preservation flag, not a general
adjoint theorem. This packet consumes defining terms and real propositions,
not their stronger prose descriptions.

## 2. Complete edge adjoint criterion, including the GL exception

Because G is grade orthogonal, d raises degree by one and ell lowers it by
one. Therefore D=D^dagger iff ell=d^dagger. The diagonal coefficient already
has the correct local adjoint. At L>=2, predecessors in different directions
are distinct, including L=2, so the off-diagonal condition is independently

    E_xy^dagger i_(h_x v_x) = i_(h_y v_y) E_xy^-1,
    E_xy^dagger=G_y^-1 E_xy^T G_x.                       (2)

Here v_x and v_y are the legs for this edge's role, not the entire frame.
Equivalently, the full operator defect is

    d^dagger-ell=L sum_r(T_r^dagger i_(h v_r)
                               -i_(h v_r)T_r^-1).       (3)

Define on the four-dimensional vector fibre

    T=h_y^-1 A^T h_x A,  b=h_y v_y,  c=A^T h_x v_x.

Exterior functoriality and contraction transport turn (2) into

    i_b = Lambda(T) i_c.                                (4)

Degree one of (4) gives b=c, since Lambda(T) acts as the identity on scalars.
Degree two says T fixes ker b pointwise: contraction by nonzero b maps
Lambda^2 onto ker b. T is positive and selfadjoint for h_y. The orthogonal
complement of ker b is the line spanned by v_y. Consequently the complete
class for arbitrary invertible A is

    c=b,
    T=I+(kappa-1) P_vy^(h_y),    kappa>0.                (5)

Conversely, all outputs of contraction lie in the exterior algebra of
ker b. Equation (5) therefore proves (4) in every degree, not just in the
tested low-degree blocks. There are no additional hidden exterior conditions.

For Lorentz A, det T=(det A)^2 det h_x/det h_y=1, so kappa=1. Thus the exact
classification in the class of section 1 is

    D=D^dagger  iff  A_xy^T h_x A_xy=h_y
                      and A_xy v_r(y)=v_r(x)
                      on every edge.                   (6)

The first equality is equivalent to `A_xy n_y=+n_x` or `A_xy n_y=-n_x`.
Only the observer line is fixed by the positive form. Choosing a time-cone
component and working near the identity gives the plus sign. Lorentz links
and unit observers alone do not imply (6): identity links with adjacent
observers e0 and (5/4,3/4,0,0) already violate it. In the actual code,
parallel leg is an explicit `hpar` hypothesis, not an unconditional theorem.

## 3. Why general linear links do not repair the same metric carrier

The exception in (5) is real. At h_x=h_y=I, take

    v_x=e_r, v_y=lambda e_r,
    A=I+(lambda-1)E_rr,  lambda>0.

Then c=b and T=I+(lambda^2-1)E_rr, so (2) holds for every exterior component.
For lambda!=1, A is not Lorentz. More generally, given any nonzero v_x,v_y,
put beta=||v_y||/||v_x|| and choose orthogonal R mapping the direction of v_y
to that of v_x. Then

    A=R[I+(beta-1)P_vy]

satisfies A^T v_x=v_y and (5). Near the reference legs R can be chosen smoothly
near the identity. Independent choices on every edge make the stored operator
selfadjoint for arbitrary nearby raw F with n=e0. Thus discarding non-Lorentz
links without checking the metric carrier would falsely restrict this class.

The same canonical quotient, however, uses the actual dressed coordinate link

    mathsfD_xy=F_x A_xy F_y^-1,    q_x=F_x eta F_x^T.

Its exact defect is

    mathsfD_xy q_y mathsfD_xy^T-q_x
       =F_x(A_xy eta A_xy^T-eta)F_x^T.                   (7)

Invertibility makes the carrier equation equivalent to A being Lorentz.
Hence the general-linear escape cannot preserve this same dressed-link
carrier. Introducing a different coordinate link independently would change
the interface and require its own native owner. Equations (5)–(7) classify
this distinction completely; they are not a NO-GO for the whole D0 core or
for every possible positive graded pairing.

## 4. All 24 link directions and the exact local metric image

Linearize (6) at F=eta, n=e0 and A=I. Write E=dot F, u=dot n with u_0=0,
and B_r=dot A_r in so(1,3). There are 16+3+4*6=43 variables per Fourier mode.
Let kappa_r=1-exp(2 pi i k_r/L). The full linear equations are

    B_r e0=kappa_r u,
    B_r e_r=kappa_r eta E_r^T.                          (8)

All six Lorentz components on each of four links are retained. The metric
jet is H=E+E^T. Eliminating E,u,B_r gives precisely

    H_rr=0                 if k_r!=0,
    H_0i=0                 if k_0!=0 and k_i!=0,
    H_ij arbitrary         for 1<=i<j<=3.                (9)

No other restrictions occur. To see this directly, the diagonal of a
Lorentz Lie-algebra element vanishes. For r=0, its boost column gives
kappa_0(E_0i+u_i)=0. For r=i, the time component gives
kappa_i(E_i0-u_i)=0; the two remaining spatial components can be supplied
by the link's rotation entries. These equations prove both necessity and
surjectivity in (9).

Let b=1_(k_0!=0) and s be the number of nonzero spatial coordinates of k.
The complete ranks are

| Quantity | Dimension |
|---|---:|
| Unknown variables | 43 |
| Linear constraint rank | 18+4b+2s |
| Linearized solution space | 25-4b-2s |
| Metric image | 10-b-s-bs |
| Kernel of metric map on linearized solutions | 15-3b-s+bs |

Complex Fourier dimensions combine with their conjugates to give the real
lattice dimensions. Summing all modes gives

    constraints: 28L^4-10L^3,
    linearized solutions: 15L^4+10L^3,
    metric image: 3L^4+10L^3-3L^2,
    metric kernel: 12L^4+3L^2.                          (10)

At L=4 these are 6528,4480,1360,3120, out of 11008 unknowns. The free local
Lorentz-frame tangent has dimension 6L^4 and lies in the metric kernel;
other kernel directions are not declared gauge. These are dimensions of
linearized equations. Section 6 proves why they cannot all be called
manifold dimensions or dimensions of actual velocities.

For a generic mode with every k_r nonzero, (9) contains only H12,H13,H23.
Even granting the ordinary coordinate-gauge comparison
H_rs=k_r xi_s+k_s xi_r adds only four directions, with zero intersection:
vanishing diagonal entries force every xi_r=0. The combined image therefore
has dimension seven, not ten. Its three independent annihilators are

    I_i(H)=H_0i-(k_0/(2k_i))H_ii-(k_i/(2k_0))H_00,
    i=1,2,3.                                           (11)

This is a comparison with the standard smooth coordinate-gauge symbol,
not a claim that coordinate diffeomorphisms are native admitted operations.
At k=(1,1,1,1), H=diag(0,1,-1,0) fails (11). Thus the missing metric directions
cannot all be dismissed as four coordinate-gauge choices.

## 5. Every metric direction in (9) has an exact nonlinear realization

This statement is stronger than a numerical rank. On the finite torus let
P_r average along coordinate r. A real H in (9) obeys

    P_r H_rr=H_rr,
    (I-P_0)(I-P_i)H_0i=0.

Set A_i=P_i H_0i and B_i=(I-P_i)P_0 H_0i, so H_0i=A_i+B_i. The former is
independent of coordinate i and the latter of coordinate 0. With n=e0 choose

    v_0=(1+epsilon H_00/2)e0-epsilon sum_i B_i e_i,
    v_i=epsilon A_i e0+(1-epsilon H_ii/2) w_i,
    w_i=normalize(e_i-(epsilon/2) sum_(j!=i, j>0) H_ij e_j).  (12)

The time leg is independent of time. Each spatial leg's time component and
spatial length are independent of its own coordinate. Put A_x0=I. On spatial
edges choose A_xi=diag(1,R_xy), where R_xy sends w_i(y) to w_i(x). For nearby
unit vectors a,b an explicit smooth proper rotation is

    K=b a^T-a b^T,    R=I+K+K^2/(1+a^T b).

It is well-defined near the reference e_i, preserves lengths, and Ra=b.
All these links are Lorentz, preserve the rest observer, and obey (6).
Reconstruct F_r=(eta v_r)^T. For sufficiently small epsilon, F is invertible
and dot q=dot(F eta F^T)=H, including every off-diagonal factor. This proves
exact local realizability of the entire metric image (9), while allowing
the links and raw frame to carry their necessary coupled variations.

No interlevel transition or on-shell equation is imposed by (12). The
previous uniformly curved warp belongs to this nonempty class.

## 6. A genuine nonintegrable joint linearized solution

Metric-image realizability does not imply that every independently prescribed
joint jet in (8) is integrable. Consider the homogeneous jet with

    dot n=0, dot v_0=e1, dot v_i=0 (i>0),
    dot A_x0=J12 at every temporal edge,
    dot A_xi=0 (i>0),

where J12 is a nonzero spatial rotation generator with J12 e1!=0. It solves
(8): the temporal generator fixes e0, and all leg/observer differences vanish.
Suppose a C1 exact family realizes this jet. A local observer-frame choice
puts n=e0 throughout without changing these first derivatives. Temporal
holonomy H(epsilon), acting on the spatial part w0 of v0, must then satisfy

    (H(epsilon)-I) w0(epsilon)=0,
    H(epsilon)=I+epsilon L J12+o(epsilon),
    w0(epsilon)=epsilon e1+o(epsilon).

Division by epsilon^2 would give L J12 e1=0, a contradiction. Unknown second
jets cannot repair this product of first jets. Each summand of this jet is
separately integrable: use v0=e0+epsilon e1 with every link I, or keep v0=e0
and use temporal links exp(epsilon J12). Their sum is not integrable. Thus
the actual velocity cone is not closed under addition, and the exact solution
set is not a C1 embedded manifold at the aligned reference v0=n. The certificate checks the
nonzero coefficient and a finite exact rotation witness. No first-order
rank calculation is used as a physical admission theorem.

## 7. What selfadjointness uniquely completes, and what it does not

For any supplied positive, grade-orthogonal G and fixed degree-raising d,
the complete class D=d+ell with ell lowering exactly one degree satisfies

    D=D^dagger  iff  ell=d^dagger=G^-1 d* G.             (13)

This follows by comparing adjacent grade blocks. It is a uniqueness theorem
for an explicitly specified class. Spectral-triple selfadjointness alone
leaves the full family

    D=d+d^dagger+K,  K=K^dagger,
    K_(j+1,j)=K_(j,j+1)=0.

Even an odd-grading requirement still admits jumps by three degrees. The
stored operator in (1) is in the adjacent-grade class, so (6) is its complete
compatibility test. Replacing its lower part outside (6) is a different
operator; no such replacement is silently installed here.

## 8. Complete admissible matrix tangent for heat and feedback

Now specify a separate general finite interface on the same full carrier:
G>0, d supplied, D=d+d^dagger, Pi^2=Pi=Pi^dagger, U^dagger U=I. Fix beta>0
and 0<z<1. The existing bootstrap functional is

    B=beta^-1 log Tr exp(-beta D^2)-log det(I-z F),
    F=Pi U^dagger(I-Pi)U Pi.                            (14)

This section computes (14) exactly. Its identification with the native
bootstrap preparation is still a separate hypothesis. Positive G and these
constraints give 0<=F<=I, so I-zF is positive and the log determinant is real.
No prescribed rank step is replaced by a continuous variation of rank.

Use dagger for the G-adjoint. For a tangent put

    K=G^-1 dot G,
    Z=dot d+[K,d]/2,
    X=dot Pi+[K,Pi]/2,
    A=U^-1(dot U+[K,U]/2).

The full differentiated constraints are equivalent to

    K^dagger=K,
    X^dagger=X,  Pi X+X Pi=X,
    A^dagger=-A.                                       (15)

Z is arbitrary in the general matrix interface, not in an independently
constrained native field family. These conditions are also sufficient for
actual curves. Set C0=(I-Pi)X Pi, S=C0-C0^dagger and T_t=exp(-tK/2). Then

    G_t=T_t^{-*} G T_t^-1,
    Pi_t=T_t exp(tS) Pi exp(-tS) T_t^-1,
    U_t=T_t U exp(tA) T_t^-1,
    d_t=T_t(d+tZ)T_t^-1.                               (16)

They obey the exact constraints and give the stated derivatives. If the
family additionally requires a grade-orthogonal G and a degree-raising d,
restrict K to degree zero and Z to degree +1. Native solder/link constraints
are additional and cannot be inferred from the smooth matrix manifold;
section 6 gives a concrete reason not to do so.

## 9. Joint covector, the Gram contribution and internal Ward

Define

    rho=exp(-beta D^2)/Tr exp(-beta D^2),
    Y=rho D,
    N=U^-1(I-Pi)U,
    R=z(I-zF)^-1,   R_P=Pi R Pi,
    C=N R_P+R_P N-U R_P U^-1,
    J=[R_P,N].

The exact first variation of (14) in coordinates (15) is

    dot B=-4 Re Tr(Y Z)+Tr(C X)+Tr(J A).                 (17)

It follows from the finite trace exponential derivative, the determinant
logarithmic derivative and cyclic trace. No commutation of an arbitrary
variation with D is assumed. In the original coordinates the same formula is

    dot B=-4 Re Tr(Y dot d)+Tr(C_G G^-1 dot G)
          +Tr(C dot Pi)+Tr(J U^-1 dot U),
    C_G=-2[Y,d^dagger]=2[Y,d].                          (18)

Here C_G is G-Hermitian and traceless because [Y,D]=0. Indeed

    dot(d^dagger)=G^-1 dot d* G+[d^dagger,G^-1 dot G].    (19)

The last term is necessary. Orthonormalizing the moving pairing transfers
it into Z; it does not remove changes of actual geometric data.

For feedback, the exact unitary constraint gives U^dagger=U^-1, so its
independent G-slot disappears after respecting the constraint. Dependence
through the native maps Pi(G),U(G) remains. Full cancellation in the moving
coordinates is the algebraic identity

    [Pi,C]+U J U^-1-J=0.                               (20)

In (17), the feedback traces are real because C,X are G-Hermitian and J,A
are G-skew-Hermitian. In complex raw coordinates, the separate feedback
terms in (18) need not be real individually; their sum is real by (20).

It can also be verified directly using F=Pi N Pi, Pi R_P=R_P=R_P Pi and
[F,R_P]=0. Thus every simultaneous basis change

    dot G=-V*G-GV,
    dot d=[V,d], dot Pi=[V,Pi], dot U=[V,U]

gives dot D=[V,D], dot F=[V,F] and dot B=0. This is an internal frame Ward
identity. A physical stress-divergence or diffeomorphism Ward equation
requires its own native field and source maps.

A full-sixteen-component exact control prevents confusing Gram-data with
basis motion. Let d=C(e0) on the exterior carrier and let G be induced by
h=diag(g,1,1,1), g>0. Then d^dagger=g C(e0)^T and

    D^2=g I16,
    B_heat=beta^-1 log(16)-g,
    dB_heat/dg=-1.                                     (21)

With the simultaneous basis-transformed d_g=g^-1/2 C(e0), the same Gram
instead gives D_g^2=I16 and zero heat derivative. This control uses a general
positive graded Gram, not a new observer-induced physical law.

The current `feedback_variation_universal_source` proposition is a Boolean
wrapper, not this derivative theorem. Equations (17)–(20) have the explicit
research proof and matrix tests here; formal claims are limited to the named
kernels in the accompanying Lean receipt.

## 10. The next required arrow

The complete Lorentz/observer stored-operator class now has a sharp answer:
its true metric directions are (9), with exact realizations (12), and the
missing directions include three that survive the coordinate-gauge comparison.
Neither affine-shift nor unconstrained matter spectators can enlarge this
metric image without changing the actual operator dependence. They may impose
further constraints. General-linear links alone restore the operator image
but violate the same metric-compatible dressed carrier.

The positive matrix interface supplies a full, explicitly integrable tangent
and a joint heat/feedback/Gram covector. It does not select the native map

    (q, mathsfD, b, m and admitted observer data) -> (d,G,Pi,U).

That map must come from the existing native preparation and refinement, and
its pullback must be evaluated on actual curves. If it uses the stored
Lorentz/observer operator, it must account for the restricted metric image.
If it uses another existing positive graded pairing or operator, its precise
owner and its full compatible domain are required. The operator-first
Connes readout, the raw Gram q and transported-center readout cannot be
interchanged without a proof.

The four-level golden record and its exact delta normalization remain inputs;
there is no new role/word census or independent Gibbs-preparation requirement.
Source/Ward in native fields, quantitative contrast, stationarity, joint curved
solutions, refinement, soundness/recovery and positive GR remain open. The
classification here neither retires #310 nor replaces its fixed-source/raw
terminal by a result for another observable.

## 11. Evidence

Run `python3 02_REGISTRY/research/certificates/a4d_native_joint_adjoint_source_check.py`.
The immutable ledger pins this proof, primary definitions, exact program,
negative controls and genuine narrow Lean compilation. The complete exterior
classification, nonlinear realizability, holonomy exclusion and finite
functional differential have the analytical scope proved above. Finite matrix
witnesses support those proofs; they do not replace their universal statements.
General nonorthonormal rational covector controls use normalized
`(I+D^2)^-1` solely as a positive commuting surrogate for algebraic cyclic-trace
kernels; they do not check a Gibbs matrix exponential. The full-sixteen family
(21) instead has the exact Gibbs weight I16/16 and checks its actual logarithmic
heat derivative.
The receipt names precisely which kernels are compiled and exposes consumed
owner propositions. No supported CORE/claim/book is changed and no D0.All or
physical closure is asserted.
