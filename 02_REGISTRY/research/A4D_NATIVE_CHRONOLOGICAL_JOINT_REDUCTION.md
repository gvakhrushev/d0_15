# T1: pole-regular full-source reduction, exact minimum values and retained refinement

Repository: `gvakhrushev/d0_15`. Existing SOURCE #310; no new task or branch.
Input SOURCE: `353afa53bd52a6f24a485dde0ec59134d08cd970`.
Date: 14 October 2026. **Exact/analytic research; physical admission and GR remain open.**

This consumes [chronological stationary descent](A4D_NATIVE_CHRONOLOGICAL_STATIONARY_DESCENT.md),
not a new angle, symmetry or operator search. Its scalar residual formula divided by
`kappa=p^3 E2/s^(3/2)` away from the poles. The present continuation removes that
singular division for **all ten metric components**, retains the complete other
matter/heat equations, and gives a uniform residual-transfer estimate on bounded
regular charts. It also eliminates the entire internal feedback *minimum value*,
without selecting an angle, and transports its minimizing locus by the actual
archive pullback. The positive-Hodge radial owner then decides the complete
`H + local chronological feedback` candidate, rather than only one contribution.
None of these statements manufactures the missing physical preparation or a new
coupled action. The full-source identity below explicitly keeps every other term.

## 1. Exact input and the complete fields being varied

Use the actual first-grade observer of
[A4D_NATIVE_RECORD_METRIC_CHRONOLOGY.md](A4D_NATIVE_RECORD_METRIC_CHRONOLOGY.md):

    q has signature (+---), v=m^1, k=v^T q^-1 v>0,
    Q=-q+2vv^T/k, G=Q^-1, n=v/sqrt(k),
    W=mu Lambda*(G), mu=sqrt(abs(det q)), N(q,m)=m^T W(q,m)m.

All sixteen real exterior amplitudes remain. In the open domain where the first
and second recorded first grades are nonzero, the original endpoint-isometry
binding gives `Q_+=Q`, `m_+=U_n m`, and the next observer from that actual output.
The local chronological price is the already owned

    J(q,m)=-log det(I16-z P K^dagger(I16-P)K P),
    K=U_(n_+) U_n, P=I-C(n)C(n)^dagger, 0<z<1.             (1)

The final cut is the original P. Its full pencil is `A(c)^2 B(c)^2 C(c)`, not
`U_n^2` and not an eight-row replacement. This J does not depend on spatial links
or affine shifts; that does not remove them from the remaining action.

Write the **complete candidate** as `S=T+J`, where `T=H+R` contains the genuine
heat and every other action term. On many sites J means the ordinary sum of these
local prices, with its actual multiplicity. A nonlocal word involving spatial
transport instead of (1) is a different feedback map and is not classified here.
The geometry variables `Y=(q,D,b)` obey all existing spatial constraints
`D_e q_t D_e^T=q_s`. The matter domain is either the full regular chart or its
normalization `N(q,m)=N0>0`; arbitrary additional physical constraints must be
checked before using the directions below.

**Important:** W depends on m through its first grade. At fixed q,
`D_m N[xi]=2 m^T W xi + m^T D_m W[xi] m`. Treating the second term as zero would
be an incorrect normalization of the general matter tangent. The prior scalar
probe had fixed observer direction; the present general probes need this term.

## 2. A true same-owner frame lift with no angular denominator

Let F be any positive-determinant invertible real frame and set `T_F=Lambda*(F)`.
The original CAR creators, adjoints, observer, cuts, both state-selected record
steps and their solved next metric all transform under the **same** frame:

    q'=FqF^T, m'=(det F)^(-1/2) T_F m,
    Q'=FQF^T, n'=Fn,
    W'=(det F) T_F^(-T) W T_F^(-1),
    U'=T_F U T_F^-1, P'=T_F P T_F^-1,
    K'=T_F K T_F^-1, J(q',m')=J(q,m).                     (2)

Positive amplitude rescaling leaves Q,n and c unchanged. The half-density factor
is essential to `N(q',m')=N(q,m)`, including grade zero and all other grades.
Without it the norm is multiplied by det F. The full feedback transforms by
similarity because its genuine W-adjoint transforms with it. Thus the determinant,
not just a sampled eigenvalue or one scalar readout, is unchanged. No assertion
that the heat or the entire field action is frame-constant follows from (2).

For an arbitrary symmetric metric jet V choose

    A_q(V)=(1/2) V q^-1,
    rho_*(A)=sum_(i,j) A_ij C_i C_j^T,
    B_q(V)=rho_*(A_q(V))-(1/2)Tr(A_q(V)) I16.              (3)

Here `C_i` are the actual signed occupation-mask exterior creators. Their Euclidean
transposes in (3) implement the coordinate exterior representation; they are not
a replacement for the W-adjoint in (1). The curve `F(t)=exp(t A_q(V))` realizes
`q'(0)=V`, `m'(0)=B_q(V)m` and (2). In particular,

    D_q J[V]+D_m J[B_q(V)m]=0                             (4)

for every V, on the complete regular domain, including both angular poles. There
is no division by E2, sin(theta), j(c), a feedback Hessian or kappa. All ten packed
metric directions occur; off-diagonal coordinates retain their usual factor two.
The radial matter identity `D_m J[m]=0` also follows from positive homogeneity.
Equation (4) is a local algebraic frame identity for this actual J, **not** a new
physical diffeomorphism Ward theorem or a decision that a physical metric probe
is gauge.

For the spatial joint constraint, use

    dD_e=A_s D_e-D_e A_t,
    A_s=(1/2)V_s q_s^-1, A_t=(1/2)V_t q_t^-1.             (5)

This satisfies the full differentiated constraint for arbitrary endpoint V_s,V_t.
Any other allowed dD differs by a genuine six-component homogeneous Lorentz-link
tangent. Those directions are retained. Affine shifts can have any admitted jet;
they do not enter J. Thus the lift extends to a complete constraint tangent, not
an artificial metric-only source projection. Additional link equations, gauge
quotients and the physical transported readout still retain their own owners.

## 3. Full coupled-source identity, including the true moving normalization

First consider normalized fields. For an admitted geometric jet Ydot, with metric
part V, define

    tau(V)=-D_q N[V]/(2N),
    L0(Ydot)=(Ydot, tau(V)m),
    L(Ydot)=(Ydot, B_q(V)m),
    Theta(V)=B_q(V)m-tau(V)m.                             (6)

`L0` is the fixed-ray lift: its radial correction cancels the variation of W at
fixed m. `L` is the normalized frame lift (2). Both satisfy the normalization and
the same spatial constraints. Their difference is a **true matter tangent**:

    D_m N[Theta]=0,
    tau=D_m N[B_q(V)m]/(2N).                              (7)

These lifts exist in the full regular normalized chart. For a blank-only or
otherwise constrained physical preparation, L0 and Theta require their own
admission; preservation of the blank by L alone does not admit the other two.
This is not in general the W-orthogonal projection of Bm onto `m^perp`.
The term `m^T D_m W[Theta]m` is generally nonzero and is checked explicitly.
Since J is radially constant, (4) gives `dJ[L]=0` and
`dJ[L0]=-D_m J[Theta]`.

Let `E_m S` be the **full** matter covector, restricted to its actual normalization
tangent. Then for every geometric jet,

    dS[L0(Ydot)] = dT[L(Ydot)] - E_m S[Theta(V)].          (8)

Proof: subtract `L-L0=(0,Theta)` in `dS=dT+dJ` and use `dJ[L]=0`.
No equation for T is assumed, no contribution of R is dropped, and no source
is fitted. In particular,

    E_m S=0  ==>  dS[L0]=d(H+R)[L].                       (9)

This is the full reduced geometric covector of this coupled candidate after its
actual matter equations, not merely `D_q H` and not the feedback-only Euler gate.
The right side includes the real dependence of H and R on the moved matter,
observer, pairing, both endpoint metrics, links and shifts. Different geometric
lifts differ by matter terms which vanish at full matter stationarity. If
additional internal fields are present, their equations must also be retained.

For unnormalized matter, take `L0=(Ydot,0)` and `Theta=B_q(V)m`; (8)–(9) hold
without radial correction. For the transported physical metric
`B(D)qB(D)^T`, apply its **entire** differential after (8), retaining both dB(D)
terms. An identification with the designated ten-row physical source is not
supplied merely by having ten raw q coordinates.

## 4. Uniform error transfer, including approach to the poles

Use the Euclidean operator norm on four-dimensional matrices and the W-norm on
matter at the base point. On degree r the exterior generator is the restriction
of the sum of r tensor copies of A, so `||rho_r(A)|| <= r||A||`. Since r<=4 and
`|Tr A|<=4||A||`, (3) yields

    ||B_q(V)|| <= 3 ||q^-1|| ||V||.                       (10)

For unnormalized matter this implies

    ||B_q(V)m||_W <= C0 ||V||,
    C0=3 sqrt(cond W) ||q^-1|| ||m||_W.                  (11)

For normalized matter let `ell_m=D_m N/(2N)` be the genuine normalization
covector, with its W-dual norm. By (7), `Theta=(I-m ell_m) B_q(V)m`, whence

    ||Theta(V)||_W <= C_N ||V||,
    C_N=C0(1+||m||_W ||D_m N||_(W,dual)/(2N)).             (12)

Every derivative of the pairing is included in D_m N. A bounded regular chart
with positive lower bounds on N,k, controlled q,Q and amplitudes has a uniform
C_N; this follows from the explicit rational/square-root maps on that chart.
No assertion of such bounds for unclassified physical solutions is made. The
previous compact all-angle family has these controls, including both poles.

Taking the dual supremum in (8) gives the exact quantitative statement

    ||dS[L0]-d(H+R)[L]||_(metric,dual)
       <= C_N ||E_m S||_(W,dual).                        (13)

All ten metric components are controlled together. On a lattice with a uniform
C_N, summing gives the **same** estimate in the raw l1 sum, with no extra number
of sites. In particular `h^-2 sum_x ||E_m S_x|| -> 0` implies the corresponding
normalized raw metric discrepancy tends to zero. A volume average, mere weak
convergence, or an unscaled residual does not establish that premise. This is
not the separate original connection-response-decoupling theorem of #310.

The improvement over division by the scalar residual is real. In the full chart
at q=eta, start from the preceding raw blank family with
`c=(1-t^2)/(1+t^2), b=2t/(1+t^2)` and add the retained spatial two-form `m_6=1`.
This additional input is not asserted to be blank or physically admitted. For
the symmetric metric jet `V_02=V_20=1`, the exact calculation gives

    kappa=p b^2,
    lim_(t->0+) t * D_q c[V]/kappa = 1/2.                (14)

Thus the scalar quotient is genuinely unbounded near the pole in the complete
regular chart, while (11)–(13) stay bounded. The state, q, Q, norm and first-grade
regularity have finite nonzero limits. Equation (14) is an exact rational/golden
calculation, not a numerical ill-conditioning diagnostic.

## 5. Exact elimination of the complete feedback minimum value

There is a further variational consequence, distinct from choosing a critical
branch. Fix a nondegenerate q and a unit timelike initial n, a positive norm, z,
and the actual whole-blank apparatus orientation. Consider the complete regular
blank matter fibre of this local experiment. The prior all-angle family realizes
**every** `c in [-1,1]`, with both record steps regular. Transport (2) realizes the
same family at this q,n. The uniform rest bound scales with the declared density;
it is not claimed unchanged on unbounded metric families.

Let `j_*(z)=min_[-1,1] J(c;z)`. The full pencil is positive on this compact angle
interval, so the minimum exists. Every state of the whole fibre has an angle in
that interval, and the constructed family attains every angle. Consequently

    min_(whole regular blank fibre at q,n) J = j_*(z),   (15)

independently of q,n and the norm. No minimizing angle or operator is selected.
There may be several minimizing states, and other stationary branches can have
larger prices; the preceding unequal-critical-value result is not contradicted.

When the actual homogeneous Hodge heat H depends only on q,n,geometry and not
these internal scalar/two-form coordinates, partial minimization of the complete
specified `H + sum_x J_x` over this whole fibre is **exactly**

    S_min(Y,n)=H(Y,n)+|X| j_*(z).                        (16)

This is variational elimination, not a partial trace or removal of stored record
coordinates. At fixed site count the entire paired geometric contrast equals the
heat contrast. It is stronger than vanishing first derivatives at selected angles.
It does not minimize an unknown R, discard the remaining n equations, assert that
all mathematical preparations are physically admitted, or prove full-action roots.
A physical domain with a different allowed angle set must be independently tested.

## 6. Actual inherited records preserve this minimizing locus

Use the real adjacent archive projection of the existing engine,
`pi_n(y)=y mod (n+2)^4`, with its actual successive composites. Pull back all fields
and all sixteen amplitudes, allowing the positive factors required by the counting
isometry or by a declared weighted pairing:

    q_f(y)=q_c(pi_n y),  m_f(y)=b_y m_c(pi_n y), b_y>0.    (17)

Positive scaling preserves n,c, both local record operators and their regularity.
The solved next q and the whole recorded m therefore obey the same pointwise
pullback. This is ordinary inheritance of the *full* state, not a new initialization
or physical refinement trigger. The first actual fibres have sizes five or six;
counting isometry uses `b_y=1/sqrt(d_(pi_n y))`, not unweighted copying.

If every parent is a feedback minimizer, so is every child, without selecting a
new angle or erasing the parent. The complete determinant is retained with its
actual multiplicity:

    det_fine = product_x det_local(c_x)^(d_x),
    min J_fine = |X_fine| j_*(z).                        (18)

It is **not** equal to the coarse raw price. A fixed-level paired contrast cancels
the same minimum constant; cross-level absolute prices retain the new factors.
Equation (17) does not establish heat-operator naturality, a physical metric/link
refinement, or an allowed independent minimization when additional inherited
constraints couple the records. Those are precisely outside this feedback result.

## 7. Consequence for the complete Hodge-plus-local-record candidate

The [positive-Hodge radial owner](A4D_NATIVE_POSITIVE_HEAT_RADIAL_BALANCE.md)
already supplies the full spectral homogeneity for a finite, nonzero degree-raising
differential, positive graded W and the declared geometric dilation. Here the
same actual chronological preparation permits that normalized joint path:

    q(t)=e^(2t)q, m^r(t)=e^((r-2)t)m^r,
    W_r(t)=e^((4-2r)t)W_r, D_e fixed.                    (19)

It is (2) with F=e^t I. Both recorded endpoint metrics and every component of
both outputs follow it; the original cut, genuine adjoint and full chronology
remain covariant. J is exactly constant for every angle, not merely stationary.
Normalization stays fixed, and all spatial metric constraints are satisfied.

For the existing Hodge binding whose d is fixed on this path, the **complete**
heat square obeys `Delta(t)=e^-2t Lambda*(e^t I) Delta Lambda*(e^-t I)`.
Nilpotency of d is not required. Retain every eigenvalue lambda_i>=0 and every
zero mode. With fixed beta>0,

    d(H+sum_x J_x)/dt = 2 E_beta,
    E_beta=sum_i lambda_i exp(-beta lambda_i)
             /sum_i exp(-beta lambda_i) >0.             (20)

Thus the full stationary set of this **entire specified candidate class** is
empty whenever the path (19) is admitted and d is nonzero. Changing the critical
angle, taking the true internal minimum (16), or adding more passive local records
cannot repair it. This applies beyond the collinear or fixed-factor examples.
The spectral identity is consumed from its existing owner, not presented as a new
heat law. The checker includes a non-nilpotent raising fixture and retains its
zero modes explicitly.

For `S=H+J+R`, (20) is instead the necessary equation
`dR[(19)]=-2 E_beta`; the actual full geometric source remains (8)–(9). The equation
is a test of R derived from the same action, not a definition of an R selected to
cancel heat. A heat map whose d also changes outside the stated homogeneity class,
a nonlocal feedback word, a different admitted field coupling or forbidden radial
path is not excluded. There is no whole-core or physical GR no-go here.

## 8. Evidence, progress and the single remaining owner obligation

The adjacent checker executes the eight AST-pinned definitions of the actual CAR,
chronology and archive owners, not copied replacement gates. It checks all ten
metric jets and sixteen matter slots at both poles and nonrest/sheared regular
states, moving first-grade/pairing normalization, both actual gates, the complete
feedback similarity, all twenty endpoint metric lifts, the six retained link
slots, a genuinely divergent scalar-only quotient, actual archive composites,
full multiplicities, and graded heat homogeneity. The source/lift and minimum
proofs above are analytic; exact finite controls are not an infinity proof.

The immutable JSON receipt records the counts, negative controls, deterministic
check-name digest, exact declaration pins and hashes of this proof and checker.
Default execution and Python -O must replay unchanged; --write is explicit.
No new Lean compilation, whole import-closure audit or local full-repository guard
run is claimed. Current-head CI and separate CONTROL acceptance are still required.

This closes the local chronological-feedback **variational contribution** at the
level of full coupled-source reduction, uniform error transfer, complete internal
minimum values and retained record inheritance. It is not the original #310
terminal or the physical T0 gate. The next owner must supply the genuinely admitted
coupled preparation of H and R (or a distinct already owned nonlocal feedback map)
and their true variations. Its geometric covector is then explicitly (8), not an
unknown feedback compensator and not a new angle/symmetry/word search. All additional
Euler equations, physical source/Ward, full solutions, heat/metric refinement,
soundness/recovery, GR and independent #202/#317 remain open.
