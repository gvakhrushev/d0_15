# Full correlations: covariant CAR current and the necessary interaction

Research continuation, 2026-10-13. Input SOURCE
`074b4223c0cae4aa5b1ad379dcd0a78930da1179`; existing #310 and CONTROL #322.
The previous turn was progress: it supplied exact collision/history evidence.
This packet retains the full objective and original #310/#202/#317 terminals.
No new action, selector, physical clock, refinement trigger or CORE claim is
installed. An explicit reading of existing CAR composites is constructed;
its physical admission and selection remain separate obligations.

There are three linked results. First, the previous tensor-marginal Pauli
reading fails the actual spatial covariance test. Second, preserving only
spectator/archive inner products cannot repair the entire current P1/top
endpoint chart, even with arbitrarily growing memory. Third, full native CAR
correlations supply a covariant causal current and an indefinitely timelike
golden component. In the actual homogeneous stored-operator class its full
heat derivative is strictly positive at fixed beta=log(2), uniformly in L.
This is a concrete source component, not a proof of native on-shell admission.

## 1. Owners and the covariance lost in a tensor marginal

Keep the exact full-sixteen Fock carrier, ACDB/ABCD sign conventions, golden
fullStep and apparatus4 tensor spectator4 change of coordinates in
[reference/memory preparation](A4D_NATIVE_REFERENCE_MEMORY_PREPARATION.md).
At fixed rest q=eta, observer n=e0 and top reference Omega, every proper
spatial rotation R acts in this apparatus as

    I_apparatus tensor (1 direct-sum R).

Consequently the system density obtained by tracing out the record and all
spectators is unchanged. This is true for every full state, not just the seed.
Any SO(3)-equivariant Role-vector reading depending only on
(q,n,Omega,system density) must have zero spatial part: the rotation stabilizer
fixes its arguments and fixes only the line spanned by n in the vector fibre.
Its normalized observer pairing is therefore precisely h(n). A general
symmetric positive vector pairing in this same class can only have one
temporal and one spatial scalar; cross terms and spatial shape vanish.

The old Pauli substitution j=(1,0,0,p^3) fails this test. A rotation exchanging
e1 and e3 keeps its system density fixed but moves its asserted spatial axis.
Its observer pairing must move the mixed temporal/spatial entry -1/2,
whereas the old reading leaves that entry in the e3 position. Physical time
reflection gives another exact control, but the proper spatial counterexample
already suffices. This is a complete stabilizer result for marginal-only
readings. Full spectator correlations, an explicitly retained spatial frame,
or other owned arguments lie outside it and are not excluded.

## 2. Passive archive preservation fails the complete fresh-top chart

Let M_j be the current W-normalized four apparatus rows with every spectator
coordinate retained. Allow any finite dimension d_j, any state-dependent
isometry V_j:C^d_j -> C^d_(j+1), and the entire endpoint frame intertwiner
class considered in the preceding proof:

    M_(j+1)=U_C M_j V_j*,
    U_C=diag(Rplus,Rminus),
    Rplus=[[a,-p],[p,a]], Rminus=[[a,-p],[-p,-a]],
    a>0, a^2=p, p>0, p+p^2=1, V_j* V_j=I.          (1)

This includes arbitrary O(4)/U(4) spectator mixing, enlarging the archive,
and arbitrary true W-normalized endpoint frames. It does not include
apparatus/spectator interactions that change the apparatus Gram. Such an
interaction is precisely what a positive continuation must derive.

The Gram S_j=M_j M_j* obeys S_(j+1)=U_C S_j U_C*, independently of V_j.
The actual self-conditioned chart B(q,m) requires in its distinguished
scalar column that row0=(x,0,...), row1,0=y>0 and row3,0=z>0. These conditions
come respectively from aligning P1(m) with n, normalizing its future first
grade, and freshly normalizing the current top grade. Thus

    h_j=Re[(S_j)_01 conjugate((S_j)_03)]=|x|^2 y z >=0, (2)

strictly if row0 is nonzero. No whole-blank condition is imposed on M_0.
An independently retained old top reference changes (2) and is not covered.

Put Q=Rplus^2. On even ticks Rminus^(2m)=I. If A is the initial upper
two-by-two Hermitian block and b its cross column to apparatus row3, then

    h_(2m)=Re[(Q^m A (Q^m)^T)_01 conjugate((Q^m b)_0)].

The frequencies are those of Q and Q cubed. Their exact annihilator is

    P(t)=(t^2-2p^3 t+1)(t^2-2(130p-81)t+1)
        =t^4+c1 t^3+c2 t^2+c1 t+1,
    c1=164-264p>0, c2=1366-2208p>0.                 (3)

Hence for every initial Hermitian A and complex b,

    h8+c1 h6+c2 h4+c1 h2+h0=0.                     (4)

One can obtain (3) by the triple tensor representation of Q: its eigenvalues
are exp(+/- i theta), with cos(theta)=p^3; the cube has cosine
4(p^3)^3-3p^3=130p-81. The checker instead verifies (4) symbolically for
arbitrary real and imaginary coefficients, so no irrational-angle premise
is required. Positivity follows from p<41/66 and p<683/1104; substituting
those numbers in t^2+t-1 gives 31/4356 and 1705/1218816.

At least one of h0,h2 is strictly positive on an admitted path. If row0
initially vanishes, the first row of Q=(2p-1,-2ap;2ap,2p-1) gives row0 at
tick2 as -2ap times the nonzero initial row1, followed by an isometry.
Thus row0 cannot vanish at both ticks. Equations (2)-(4) contradict existence
of the chart at ticks 0,2,4,6,8. The entire class (1) has no eight-tick path
satisfying (2). Several independent scalar archive slots with a different
current-field reading are outside this distinguished-scalar-line chart.
Adding heat/observable constraints cannot enlarge it. This does not exclude
genuine native interactions changing S_j, a retained orientation interface,
or other admitted readouts, and is not a global D0 NO-GO.

## 3. A current using the actual full CAR correlations

Let W>0 be the full exterior pairing induced by the retained observer u,
including any common positive site density. Write C(v) for the actual
exterior creator and A_G(v)=C(v)^dagger for its pairing adjoint. The actual
CAR give {C(v),A_G(w)}=G(v,w)I. For G(u,u)=1 and v perpendicular to u put

    beta_u=C(u)+A_G(u),
    gamma_v=C(v)-A_G(v), alpha_u(v)=beta_u gamma_v.    (5)

Here beta is selfadjoint, gamma is skew-adjoint, and they anticommute.
Consequently alpha is selfadjoint and

    alpha_u(v) alpha_u(w)+alpha_u(w) alpha_u(v)
       =2G(v,w)I.                                    (6)

Using two positive Euclidean fockGamma operators instead would give a
skew-adjoint product and a zero real quadratic reading. The sign in (5)
is therefore tested against the literal creation/annihilation matrices.
All sixteen components are retained.

For any nonzero full m, define b in the spatial complement by

    G(b,v)=<m,alpha_u(v)m>_W / <m,m>_W,
    J=u+b.                                           (7)

Equation (7) is basis independent. It is a reading of explicit owned CAR
composites, not the earlier two-by-two tensor marginal. For a unit spatial
v, (6) gives alpha(v)^2=I, so Cauchy--Schwarz bounds its normalized expectation
by one. Choosing v along b gives G(b,b)<=1. The physical Lorentz form ell
whose observer pairing is G satisfies

    ell(J,J)=1-G(b,b)>=0, ell(u,J)=1.

Thus J is future causal relative to the retained reference, and it is
timelike precisely when G(b,b)<1. Equality means m is an eigenvector of
alpha along b; it is not excluded on the whole state space.

Creators, their genuine adjoints and exterior frame lifts transform together.
Under any invertible coordinate frame E, with ell/G/u/m all transported,
alpha transforms by Lambda(E) conjugation and the expectation is invariant.
Therefore J transforms as a vector. This includes joint Lorentz covariance,
not merely one sampled rotation. Keeping the retained reference fixed while
transforming the matter alone is a different experiment.

The map requires its retained u. Its existence does not prove that M1 selects
it uniquely among all possible full-state readings, or grant its physical
operation admission. Neither an external axis nor an independently adjusted
coefficient is used in (5)-(7).

## 4. An all-time timelike component on the actual golden apparatus

Use the existing whole-blank isometry B with nonzero entries

    B_0,0=B_14,0=1/sqrt(2), B_3,1=B_13,1=1/sqrt(2),
    m0=B(x,y), x^2+y^2=1.                            (8)

Take the original rest fullStep U and retained u=e0. Its full cyclic space
is the eight occupation masks 0,1,2,3,12,13,14,15. On this space alpha_1
commutes with U^2; alpha_2 and alpha_3 have zero compressed expectation.
Direct CAR calculation gives, for every integer tick j>=0,

    J_(2j)=e0, J_(2j+1)=e0+2xy e1,
    ell(J_(2j+1),J_(2j+1))=(x^2-y^2)^2.             (9)

This is an all-time invariant-space proof, not extrapolation from finitely
many ticks. At the existing golden weights x=a,y=p the odd norm is p^6>0,
and the squared spatial current is 4p^3, the literal two-tick feedback
eigenvalue. The normalized observer form

    h_J=-eta+2(eta J)(eta J)^T/(J^T eta J)             (10)

is I at even ticks. At odd ticks its eigenvalues are
K,K^-1,1,1, where K=(1+2ap)/(1-2ap). Exact golden bounds give 60<K<80.
The full orbit is uniformly inside the timelike domain, although its old
P1/top-grade reading fails. This is a positive correlated-current sector;
it is not a solution of that old chart by reinterpretation.

Use the same normalized owned preparation curve

    u(t)=(1-t^2)/(1+t^2), v(t)=2t/(1+t^2),
    x(t)=a u(t)-p v(t), y(t)=p u(t)+a v(t).           (11)

It is timelike for every tick throughout |t|<=1/100. For example
x-y >=7719/80008>0, using 3/5<p<5/8 and 3/4<a<4/5.
Both x,y remain positive by the preceding preparation bounds. Equation (9)
then gives a uniform nonzero norm and a uniform pairing bound for this whole
interval. At t=0 put r=2xy; r=2ap and r'=4p^3>0.

## 5. Genuine first variation and the homogeneous native operator

In a fixed rest frame, r_i=<m,alpha_i m>/N, N=<m,m>, and

    delta r_i=2 Re<delta m,(alpha_i-r_i I)m>/N.        (12)

The denominator term is essential. On jointly moving fields there are also
the complete delta-W, delta-alpha and reference-frame terms. They follow by
differentiating (5)-(7), including A_G=W^-1 C* W; none is set to zero on a
physical metric variation. For ell/J the full derivative of (10) likewise
retains the numerator and delta(J^T ell J). Simultaneous frame motion is an
internal covariance identity, not a matter equation or a physical Ward theorem.

There is an exact binding to an already owned operator on a precise component.
At homogeneous F=eta, raw q=eta, identity links and zero translations, all
legs v_r=e_r are constant. Take the homogeneous observer n_J=J/sqrt(k),
pairing h_J and the actual stored d/ell from
[joint adjoint source](A4D_NATIVE_JOINT_ADJOINT_SOURCE.md). Its complete edge
criterion is satisfied for every t in (11). Thus ell=d^dagger and its full
Fourier square, on all sites and all sixteen grades, is

    Delta(k)=lambda_k I16, lambda_k=z(k)* h_J z(k),
    z_r(k)=L(exp(2pi i k_r/L)-1).                    (13)

No unrelated scalar Laplacian is substituted. This identifies operators on
this homogeneous component; it does not identify every Hodge binding with
the native scene D or derive the physical preparation selecting (7).

The full heat term is H=beta^-1 log(16 sum_k exp(-beta lambda_k)). On the odd
component let K=(1+r)/(1-r), K'>0. With
A=|z0-z1|^2 and B=|z0+z1|^2,

    lambda=(K/2)A+(1/(2K))B+|z2|^2+|z3|^2,
    H'=-(K'/2) E_beta[A-K^-2 B].                    (14)

Both transverse heat factors and the sixteenfold multiplicity cancel from
this derivative, not from the full price.

## 6. A fixed-beta source bound, uniform in every L>=2

At the golden point 60<K<80 and beta=log(2) lies between 1/2 and 1.
Let d(k)=min(k,L-k). The elementary sine bounds give

    16d(k)^2<=|z(k)|^2<=4pi^2 d(k)^2.

For the folded difference l=k0-k1 mod L the same bounds apply to A.
The heat is at least KA/2 and at least K^-1(|z0|^2+|z1|^2), hence

    beta lambda>=120d(l)^2+d(k0)^2/20.

On off-diagonal modes A>0, therefore

    sum_off A exp(-beta lambda)
      <=8pi^2 [sum_(d>=1) d^2 exp(-120d^2)]
                    [1+2sum_(n>=1) exp(-n^2/20)]
      <16896/2^30.                                  (15)

Indeed the Gaussian sum is bounded by its decreasing-function integral,
giving the second bracket <11. With t=exp(-120)<1/2 the first sum is
at most sum d^2 t^d=t(1+t)/(1-t)^3<12t. Use pi<4 and
exp(-120)<2^-30. These are bounds on the entire mode set, uniform in L.

The single diagonal mode k0=k1=1 has A=0,
64<=B<=16pi^2<256; lambda=B/(2K)<256/120<3.
Thus its negative contribution has magnitude at least

    K^-2 B exp(-beta lambda)>64/(80^2*27)=1/2700,     (16)

using exp(3)<27. All other diagonal contributions have the same sign; the
negative off-diagonal B terms may be discarded for an upper bound. Exact
rational comparison of (15)-(16) yields

    sum_(k0,k1)(A-K^-2B)exp(-beta lambda)<-1/3000.

Also lambda>=K^-1(|z0|^2+|z1|^2), so its two-coordinate partition is
less than [1+2sum_(n>=1) exp(-n^2/10)]^2<81.
Consequently the complete derivative satisfies

    H'(0)>K'/486000>0, for every L>=2 at beta=log(2). (17)

The deliberately loose constants avoid a mesh-dependent beta or a numerical
sign test. The bound applies in particular to every required L in 4N.
The all-L sine/Gaussian argument is analytic; exact rational steps and full
finite Fourier controls are separately checked. No normalization/readout
transfer or continuum physical source is inferred from (17).

## 7. Complete feedback and the remaining native source arrow

At every point of this homogeneous observer family, use the actual
U(h_J,n_J), P=I-N and its genuine full W-adjoint. For the literal two equal
current-observer ticks, the full sixteen-component fibre pencil is

    det(I-z F_2)=(1-4zp^3)^4.

On the complete periodic carrier the operation and cut act identically at
all L^4 sites. Therefore the full retained pencil is
`(1-4zp^3)^(4L^4)`, with 12L^4 zero-feedback directions retained.

Both complete pencils have zero derivative along (11). Combined with (17), the existing
heat-plus-feedback functional on this explicit static interface therefore
has strictly positive derivative along the actual full matter curve.
Its stationary set excludes that golden point if this curve is admitted
and all remaining price terms have zero derivative on the same curve.
A remaining term must supply the negative of (17) through its own equations;
no compensator or source is fitted.

These two equal ticks are a precisely specified feedback experiment. They
are not silently substituted for the earlier genuinely misaligned sequence
U_(n_next)U_(n_current) with its original retained cut. That chronology has a
separate nonconstant price and must enter the native preparation if used.

The next positive interaction must use full correlations and change the
apparatus Gram or explicitly retain the old orientation interface; passive
archive growth alone is insufficient by section 2. It must establish the
joint physical admission of its reading, heat/feedback and refinements, and
derive the complete source/Ward on genuine field variations. Quantitative
contrast, native stationarity, curved joint roots, soundness/recovery, GR and
the original fixed-source/raw-owner #310 terminal remain open.

## 8. The closed record engine does not feed this current source

This cross-owner continuation binds SOURCE baseline
`0a8e705a18b5dfc61307bd7b5e01f1436dbb9f16`, on top of the original
correlated-current input recorded at the head of this file.

Compare the actual full-CAR current in sections 3–6 with the already owned
[closed record engine](A4D_NATIVE_CLOSED_RECORD_ENGINE.md), rather than
identifying their seeds by name. In occupation-mask coordinates let

    S=span{e_0,e_1,e_14,e_15},   P_S be its orthogonal projector.

The engine seed is `e_1+e_15`. For each of its two literal state-selected
gates U_+ and U_-, the exact sixteen-column comparison with the native CAR
gate gives

    U_± S=S,   U_± S^perp=S^perp,
    P_S alpha_i P_S=0, i=1,2,3.                       (18)

Thus for every nonzero real m in S, not merely for sampled orbit states, the
section-3 full-current readout at q=eta is J(m)=e_0. Its observer pairing is
h_J=I. The engine's all-time seed orbit stays in S: the two gates preserve
that sector, its first two coordinates follow the `lowerStep` recursion in
the closed-engine Lean capsule, and the existing
`every_seed_tick_regular` theorem keeps the state-selected sign defined.
The distinct higher-grade records therefore evolve while this particular
current, its observer pairing, the section-6 current-defined heat and the
two-tick current feedback remain constant. For any differentiable matter
variation confined to S at fixed geometry, the pullback of those
current-mediated terms is zero. This says nothing about other native price
terms that may depend on the retained record directly.

The positive source in (17) belongs to a different state sector. The
whole-blank curve B(x(t),y(t)) has support in masks 0,14,3,13; at the golden
point its positive rescaling has coordinates m_0=m_14=a and m_3=m_13=p.
It is outside S and fails the closed engine's own collinear-domain guard
because m_3 is nonzero (its first-grade m_1 is also zero). The engine does
not accept this source-active state as an input. Conversely, replacing the
engine's state by the B curve is not one of its state-selected transitions.

This is an exact decoupling result for this pair of existing owners and this
current/heat readout: the positive source curve and the indefinitely
recording engine have not yet been composed into one dynamics. It does not
exclude another already-owned native interaction or source term, and it is
not a NO-GO for the D0 core. The next proof must either exhibit an already
owned, physically admitted operation that couples the retained engine
record into the current-active sector and derive its variation, or classify
this engine/current route as closed to that source. No interpolation,
mixing map or new physical selector is supplied here.

The checker pins the engine program, its exact checker, Lean capsule,
compiler output/results and proof, compares both signs on all sixteen
columns, tests both reducing blocks and all three compressed CAR currents,
and includes negative controls for falsely admitting the source state. The
all-time step is inherited only through the pinned existing Lean theorem;
the finite orbit rows are regression controls, not the all-time argument.

## 9. Evidence boundary

The accompanying exact checker retains literal CAR matrices, all components,
the complex eight-tick identity, full orbit invariant spaces, rotations and
joint nonrest frame covariance, true adjoints, genuine input derivatives and
complete Fourier multiplicities. Its named narrow Lean kernels retain their
actual propositions and transitive assumptions. Neither finite replay nor
generic algebraic kernels replace the all-time/all-L proofs above or the
missing physical admission, matter equations and refinement transfer.

Default replay is portable: it validates the immutable compiler output,
actual proposition/axiom requests, complete SOURCE closure and archived
object/runtime pin consistency without requiring the original machine's
temporary overlay directories. On that machine, `--runtime-check` also
hashes every actual object, the compiler binary and the preserved original
cache. The original compilation and both audits are recorded; portable
replay does not claim a new compiler execution on the CI runner.
