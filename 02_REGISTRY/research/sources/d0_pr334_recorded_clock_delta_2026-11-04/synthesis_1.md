## Matched-source synthesis: one stationary programme section, the original input cut, and global Einstein rigidity

4 November 2026. Existing Draft #334; native realization / final composition. Inputs: §7ee H8–H22 / Proof II, §7ei EI6–EI12, §7ex EX1–EX9, and A4D_GOLDEN_DISCRETE_BLOWUP_CONDENSED_GR_2026_10_20.md. Working input read: 89dcb2c8 (4 November 2026). This note proves a stronger source-class substitution on the specified matched native family. It does not establish the entire A–D physical contract.

### 1. The exact monotone reparametrization supplied by the original determinant

Retain the actual chronological old map C_<, its current-interface OUTPUT Gram A=C_< C_<* >=0 with Tr A>0, and the physical initial cut. If C_< is rectangular, retain H1r's absolute dimension constant. No inverse of A is used. Put d=1-z>0 and let eta>0 be the actual paid retention coefficient.

For every programme branch theta and duplicate block j use ALL independent variables

    Z_theta,j=(E_theta,j, omega_theta,j, Psi_theta,j),
    E_theta,j=e_theta,j/sqrt(sigma_theta,j).

Initially the same coordinate measure m is fixed in every copy. Every j carries the SAME finite action, boundary data, material normalization and local field chart; different I_j require separate decoded components. H18 and pointwise degree -2 give the EXACT finite identity

    I_theta,j(e_theta,j,omega_theta,j,Psi_theta,j)=I_h(Z_theta,j).

This includes spatially variable sigma. In particular dE_theta contains the actual term -E_theta dsigma_theta/(2 sigma_theta). The positive slope is not frozen before differentiation.

Evaluate on the OFF-SHELL matched section Z_theta,j=Z, for every regular Z; no Einstein equation is imposed. The ideal original corners of H5 then satisfy

    c=c0-2g I_h(Z)>0,  t=c^M,  C=t I,
    J_red(Z)=F_A(I_h(Z)),
    F_A(u)=-nu Tr log[d I+eta(c0-2g u)^(2M) A]+constant_dim.

Define B=eta t^2 A(d I+eta t^2 A)^(-1), w=nu Tr B>0. Direct differentiation gives

    F'_A(u)=Gamma=4g M w/c >0.

Thus, on the regular collar, F_A is strictly increasing and

    Gamma^(-1) dJ_red=dI_h

EXACTLY, even off shell. The nonlinear logarithm, all old eigenvalues and the absolute dimension constant were retained. J_red need not be homogeneous under any physical scale. This is division of the true covector by its derived gain; it is NOT differentiation of J/Gamma, addition of a counterterm, or a free rescaling of the relative matter source.

### 2. Independent branches survive: a full source factorization, not a diagonal-only calculation

At the same matched point let

    pi_theta=nu Tr(Pi_theta B)/w,  pi_theta>=0, sum pi_theta=1.

For ALL independent current field and slope directions, H8/H19 give

    DJ_current/Gamma
      = DI_h(Z)[ (1/M) sum_j,theta pi_theta dZ_theta,j ].       (R1)

PVM-basis variations have dC=[K,C]=0 at this point. If m is independently variable, instead use E_theta,j=e_theta,j/sqrt(m_theta,j sigma_theta,j) and the unit-coordinate-measure version of I_h. Pointwise degree -2 gives the same exact identity, now including Dm. This is a coordinate change, not permission to delete a measure equation. Old Gram variations retain their separate term below.

Define a local field chart by the explicit mean

    Phi({Z_theta,j},A,Pi)=(1/M) sum_j,theta pi_theta Z_theta,j,

extending pi smoothly by the actual positive resolvent weights on the regular finite chart. Averaging here uses one LOCAL LINEAR coordinate chart for each proper-Lorentz link, not averages of group matrices. At the matched section,

    dPhi=(1/M) sum_j,theta pi_theta dZ_theta,j,

because every weight-derivative term is Z d(sum pi)=0. This is the decisive difference from inserting sigma_eff(Y) into the common-raw-field action away from its zero-density locus. No ell d(sigma_eff) term was omitted: each sigma derivative is already in dZ_theta, and every d pi term cancels by equality of the branch fields, not by an equation of motion.

Consequently (R1) is the full covector identity

    DJ_current/Gamma = DI_h(Z) composed with dPhi.             (R2)

The simultaneous lift v -> (v for every theta,j) is a right inverse of dPhi of norm one in the existing independent-copy maximum norm. The complementary projector v_theta,j -> v_theta,j-dPhi(v) has norm at most two. Zero-weight branches cause no inverse-weight singularity. All their independent controls remain; their leading source is zero. Thus in these legitimate local coordinates the relative branch fields have an internal stationary section at the diagonal for EVERY off-shell physical Z. For an explicit complementary chart choose one reference copy L and r_i=Z_i-Z_L. At matching, dPhi=dZ_L+sum_(i!=L) a_i dr_i, a_i=pi_theta/M. The inverse is dZ_L=dPhi-sum a_i dr_i and dZ_i=dZ_L+dr_i; no division by a weight occurs. The chart differential and inverse have bounds 2 and 3 in the material product-max norm. The inverse-function theorem gives a finite local chart, but its radius need not be uniform in M. Raw coframe norms retain the actual sqrt(sigma), or sqrt(m sigma), chart constants. Their individual raw field rows are generally NONZERO; (R2) retains them and assigns their common component to the physical field row. This is not imposing equality of branch variations.

For a coordinate-invariant metric statement, first consume the owned independent-link equation and Lorentz gauge/source map, without deleting their rows. Each branch then has physical variables (g_hat_theta,j,Psi_theta,j). Near their common value define Phi by the weighted mean of these metric/scalar components, rather than by averaging unrelated Lorentz frames. The same cancellation and right-inverse proof apply. A convex neighbourhood of one nondegenerate Lorentz metric remains in its regular signature chart. No physical meaning is assigned to a mean of distant unrelated branch geometries.

This supplies the source equalizer on the MATCHED stationary subobject: every allowed positive slope/PVM/history choice gives the SAME normalized reduced physical source. It does not assert that the entire unrestricted history object is that subobject.

### 2a. Prepared CODE: the same source with the original physical input rank

The preceding retained-full-code determinant is not necessary for this matched construction. Consume the PREPARED-code alternative explicitly distinguished after H17: birth CODE as genuine new WORK, pay its known forward preparation and backward unpreparation, and keep the original physical input rank r. Its controlled body has table

    T=diag(t_theta),  t_theta=product_j c_theta,j,
    c(v_f,v_b)=<v_b,T v_f>.

At matched branches/copies T=tI, t=c^M>0, and at the proposed preparation section v_f=v_b=v,

    c(v,v)=t,  q_theta=<v,Pi_theta v> >=0,  sum q_theta=1.

These are the actually prepared Born weights, not chosen history weights and not independent resampling at each call. For independent changes of BOTH normalized preparation vectors, every branch field and the programme basis, the exact differential is

    dc=sum_theta q_theta dt_theta
        +t[<dv_b,v>+<v,dv_f>]
        +t sum_theta <v,dPi_theta v>.

The last sum vanishes. Each of the two overlap terms is separately purely imaginary. Therefore the original feedback differential, which uses Re(dc/t), has zero source on EACH independent CODE-only preparation leg at this section. The legs were not identified before differentiation. Equivalently the full mixed coefficient <v_b,Pi_theta v_f> has value q_theta; its summed differential multiplies the scalar t and has zero real part. No arbitrary other WORK preparation is thereby declared neutral.

Use the physical input Gram A_in=C_<* C_< on rank r. The actual reduced determinant is

    J_red=-nu Tr_r log[d I_r+eta t^2 A_in]=F_A(I_h(Z)),
    Gamma=4g M w/c>0.

Independent field/slope rows now obey (R1)--(R2) with pi_theta replaced by q_theta. A field-dependent matched preparation v(Y) introduces no dq term at equal branch fields: sum dq=0. The same mean/readout and norm-one simultaneous lift apply; the original physical input cut does not grow with the new CODE. Every CODE dimension still belongs to the complete clock and heat trace.

This version also avoids defining the physical mean by posterior price weights: q is the separately specified Born law of the actual fresh preparation. Phi is finite postprocessing of these weights and the already owned branch field-name/decoded-data chart. Its derivative is not selected by solving Einstein equations or by defining a coordinate equal to the price. If a consumer instead requires a different registered field decoder on off-diagonal branch histories, its equality to this Phi is a separate readout transport; coincidence of their central metrics alone does not establish equality of their full source maps.

For actually compiled bodies the all-column/table errors and independent-leg imbalance remain in the source budget. CODE-only feedback stationarity does not by itself imply exact heat stationarity. Apply §7ex only if these PARTICULAR transported preparation generators satisfy its all-column joint-effect commutant premise. Otherwise retain the complete enlarged-prefix heat estimate relative to the actual positive Gamma, as in §7ei and §3 below. This prepared-code route gives the stronger same-fixed-input source construction without claiming an unproved whole-heat symmetry.

### 3. Whole H+J, old rows, and the actual stationary preparation section

For the actual complete execution write q_h=D(H+J)/Gamma_h in the owner's physical source norm. Gamma_h includes the true native field-step factor if the comparison is a Born-preparation displacement; the simple Gamma in §1 uses the direct field chart. Do not erase the sampler step, compiler denominator or dimension-dependent lift constant.

The remaining old-matrix term is exactly

    D_A J=-nu eta Tr[D^(-1) C(DA)C].

At C=tI, H22a bounds it after division by Gamma. The real prefix constant is suppressed only by the actual current concentration. Full heat, nonlinear reporter errors, all-column compiler errors and programme-product errors keep their existing estimates. In particular M g E_ref ->0 is still needed for the palette comparison; full heat is treated after the actual finite prefix is known. No price term is subtracted.

With those owned errors denoted e_h, the actual application is

    q_h = DI_h composed with dPhi_h + e_h,
    ||rightlift_h|| ||e_h||_* ->0.                              (R3)

This is a kappa source statement, not a claim that the ideal relative-branch section solves every finite native equation exactly.

§7ex adds an EXACT off-shell substitution for the independently varied preparation legs of its actual reader. For its four joint all-column effects P_(sigma,q), B_l=K_l B with K_l in their common commutant. At K_f=K_b the relative K=K_b* K_f is I. EX7 proves equality under K -> K*, including the entire growing heat and the actual cut. EX8 therefore kills each independent leg row. An arbitrary field-dependent matched choice K_f(Y)=K_b(Y)=K0(Y) adds no envelope term: both independent Euler rows vanish. Equal all-column effect representatives differ by precisely this commutant; at matched legs their completed endpoint depends only on B*P_nu B, not the chosen bank frame. With the same paid layout, the prefix conjugacy/ST3 owner supplies the corresponding clock statement. Native comparison errors retain EX9's real tau Gamma denominator.

This removes the bank-frame part of the source descent, not all changes of the joint effects. It also does NOT identify the marked-reader price with the unmarked §7ee price. See §6.

### 4. Explicit local-diffeomorphism lift, including a variable Jacobian

Let phi:U->V be an orientation-preserving local diffeomorphism, J=Dphi and j=det J>0. Write F=m sigma for one source/material chart and

    e_hat=sqrt(F/det e) e.

For any prescribed positive target F'(x), define the actual raw-data transformation

    e'(x)=sqrt(F'(x)/(j(x) F(phi(x)))) e(phi(x)) J(x),
    omega'=phi*omega,   Psi'=Psi composed with phi.             (R4)

Taking determinants proves EXACTLY

    e_hat'(x)=e_hat(phi(x)) J(x),  g_hat'=phi*g_hat.             (R5)

With the same fixed background F in all charts, its positive factor is a genuine cocycle: r_phi(x) r_psi(phi(x))=r_(psi composed with phi)(x). Hence T_phi T_psi=T_(psi composed with phi), with the usual contravariant pullback order. Constant physical rescaling commutes with this transformation. This is an actual composition identity of the raw field-name maps, not merely covariance of one selected solution. A finite native composition test includes these same composite data maps and their comparison words in the paid catalogue.

In particular m=1 and sigma=1 can both remain fixed: e'=j^(-1/2) phi*e. No new measure writer is needed. For arbitrary fixed F one uses F'=F in (R4); thus a spatially varying calibration can be compensated by the already owned material-frame map rather than treated as a preferred physical tensor.

Before connection elimination, the two original contractions f and q are coordinate scalars under an ordinary coframe/connection/scalar pullback; their pointwise coframe degree is -2. Hence the CONTINUUM first-order density obeys

    F'(x) ell(e',omega',Psi')
      = j(x) F(phi(x)) ell(e,omega,Psi)(phi(x)).                (R6)

This is a change-of-variables identity for the original curvature and scalar contractions, before identifying their field equation as Einstein. There is no derivative of the coframe in this first-order density. Connection pullback and all independent connection variations remain.

The finite lattice stencil is not asserted exactly Diff-natural. Instead, (R4) is an effective data map on the existing full-field writer: include Y, its pulled-back data, and the finite comparison endpoints in one regular finite catalogue before choosing reference bounds/attenuation/compiler precision. Every word, helper and clock is paid. The existing geometric source-convergence estimate supplies the discretization error of (R6); the complete-price estimate (R3) supplies the native errors. On physical compactly supported variations v, one gets

    |(T_phi* q_h')(v)-q_h(v)|
      <= [||DT_phi|| E_h' + E_h + E_geom,h(phi)] ||v||.          (R7)

Use the actual physical right-lift/chart constants in each E. After their vanishing limit, (R7) gives restriction/local-diffeomorphism naturality of the reduced source on this SAME declared source family. Condensed support alone is not used as its proof. The standard extension from effective data to a larger smooth chart uses the already owned continuous material-source limit; an arbitrary noncomputable native word is not claimed.

For the matched palette apply (R4) branchwise to its actual sigma_theta. All branch physical metrics still agree, so the posterior-weight derivatives again cancel. On the physical section the result is independent of every pi_theta, even when those weights change under the finite operation. This is why the argument is valid there and is not valid for the common-raw-field posterior substitution of §7ee.C.

### 5. Golden source cocycle, Ward, and what absolute prices need not satisfy

The already executed EI9 map e->p e, p=phi^(-1), is the constant-scale counterpart of (R4). It gives

    g_hat -> rho g_hat,  I_h -> rho I_h,  rho=phi^2,
    T_rho* DI_h = rho DI_h.                                  (R8)

On the matched source class, (R2)--(R3) therefore give the limiting identity

    T_rho* [Gamma_rho^(-1) D S_red,rho]
        = rho [Gamma^(-1) D S_red]                            (R9)

on physical interior variations. Finite errors are exactly of EI12's form, with the new actual gains and lifts. At the ideal determinant level this follows from F'_A=Gamma, although F_A(rho I) is generally not rho F_A(I). The old complete heat anchor and return logarithm are retained.

Thus the native equations can be classified through this operationally normalized SOURCE CLASS. No exact scale law for the raw dimensionless Book number is needed. The multiplier is the SAME positive global scalar for the gravitational, connection and matter rows. A field-dependent local rescaling of individual equation components is not authorized. At fixed entire field a global Gamma[I,A] is constant in spacetime, but its dependence on the domain/history can spoil locality of the raw source. Dividing by the DERIVED Gamma removes that dependence; positivity and the true physical normalization remain load-bearing.

The reduced normalized one-form is closed because (R2) restricts to dI, not because every rescaled Euler form is automatically closed. In general d(Gamma^(-1)dS)=-Gamma^(-2)dGamma wedge dS need not vanish. Here dS_current=F'_A(I)dI at fixed old data, and the retained extra sources in (R3) vanish in the specified topology.

The Diff identity (R6)--(R7) gives Noether's identity after legitimate internal/link elimination. With physical matter still present its precise form is 2 nabla_a E_g^(ab)=sum_A E_Psi_A nabla^b Psi_A; the TOTAL metric source is not asserted conserved off shell without the scalar equations. For the gravitational component, or the matter-zero restriction, the right side is zero. Equivalently, source-level naturality of the CLOSED metric one-form alpha gives L_X alpha=0; Cartan's formula makes alpha(L_xi g) constant on a connected chart. Its flat value is zero by the Golden law, so compactly supported xi give the gravitational off-shell Ward identity. Mere naturality of a tensor without this variational/closedness input would not suffice.

For the gravitational component (matter zero, or with the SAME actual matter source separated), (R9) has covariant tensor weight zero. The owned smooth flat material-source limit supplies the differentiability premise. The Golden blow-up theorem then applies to this descended normalized source. The full gravitational-plus-matter equation is unchanged by its nonzero common multiplier, and the existing sourced witness fixes the same coupling ratio. This is a genuine strengthening of the ACTION-level sufficient route: use monotone action reparametrization plus source descent, not homogeneous raw price.

### 6. Exact boundary of the marked-reader and endpoint-coboundary application

The actual §7ex reader is the priced word G_R^(-1) B* S M_q K B. Its §7ew scalar corner is

    c_read,theta=k_theta c_old,theta
                   -(sqrt(p)-p)(1-beta_theta) K_theta,
    k_theta=sqrt(p)-(sqrt(p)-p) beta_theta,
    K_theta=4 lambda r0_theta chi_theta.

Thus matching the geometric branch actions alone gives baseline

    b_theta=k_theta c0-(sqrt(p)-p)(1-beta_theta)K_theta.

These b_theta need not be equal. Relative commutant stationarity in §7ex does not change them: beta/chi and comparator-changing profile motions are outside that fibre. Consequently one cannot directly insert C=(c0-2g I)^M I for the marked reader with an unconstrained palette. For ONE common profile, the affine change of corner preserves the same monotone-source mechanism with its actual positive derivative; independent profile rows still retain their full equations. For a palette, source matching requires the actual matched full corner/profile and its remaining Euler rows, not merely matching geometric densities. This is the precise whole-source interface still needed to extend (R9) to that larger reader class.

Absolute price equality across representations is unnecessary if their FULL normalized interior covectors agree under the real history map. However a HISTORY ENDPOINT coboundary is not automatically a spacetime boundary term. If

    S' composed with T - S = F_out(R_out(Y))-F_in(R_in(Y)),

the terminal archive can encode the entire bulk field. The exact required condition is

    D[F_out composed with R_out-F_in composed with R_in]
          [physical rightlift(v)]=0

for every compactly supported physical v, or a bound which vanishes after the actual gain and right-lift normalization. If an internally stationary section depends on Y, include its true adjoint in this derivative. A local spacetime boundary-jet functional with fixed boundary data satisfies this criterion; an arbitrary function of a complete terminal record does not.

Accordingly this sufficient source route no longer needs: absolute-price equality/homogeneity for the matched source family; the false need to freeze positive slopes or independent relative branch rows; and, by §7ex on its own actual word, the all-column effect-preserving preparation-frame ambiguity. The unchanged obligation is a SAME complete-price/admitted-domain map covering the remaining profile/record/clock/scene directions. No GR_closed or exact finite whole-source solution is asserted here.


### 7. Complete-history weights can transport this source without a separate Cost/Info split

The following consumes the owned prospective P1–P4b and weighted-intertwining owners. It is a second sufficient input to the same full covector consumer, not an installed Gibbs law.

#### C1. Owned inputs and the strengthened observation

Use `A4D_PROSPECTIVE_BOOK_FINITE_FUTURE_LAW_Q8_VERIFICATION_2026_10_20.md`,
P1–P4b, on its declared state space INCLUDING the complete retained prefix,
programme, preparation and clock. The theorem explicitly assumes the actual
scalar prices, terminal task and proportional-weight sampling rule.
Use `repository_puzzle/weights/EXACT_DOOB_BINDING_CRITERION.md` for the
stationary alternative, and `FOUNDATIONAL_WEIGHT_BRIDGES.md` for its actual
weighted primitive/response interface. All paths below have positive support.

Let H_N consist of the complete length-N histories from ONE fixed initial
state and ONE physical experiment. With the SAME specified terminal weight χ_N,

    μ_N(γ) = χ_N(γ) φ^(−S_N(γ)) / Z_N.

P2 immediately gives, for arbitrary complete endings γ and δ,

    S_N(γ) − S_N(δ)
      = −log_φ[μ_N(γ)/μ_N(δ)] + log_φ[χ_N(γ)/χ_N(δ)].       (1)

The endings need not be equal, have equal memory, or erase their records.
The common normalizer cancels because they are alternatives in ONE law.
If an additional actual attempt factor a_N is outside S, replace χ_N by
a_N χ_N and retain its full source. Do not count the prefix price twice.

If two additive prices S and S~ give the SAME μ_N with the SAME χ_N for every
N, division yields

    S~_N(γ) − S_N(γ) = b_N,
    s~(γ→γe) − s(γ→γe) = b_(N+1) − b_N.                    (2)

Thus complete finite-horizon laws remove the arbitrary ending potential left
by a single stationary Doob kernel. The remaining ambiguity is one number per
horizon. This does not assume a finite Markov quotient of retained histories.

#### C2. Exact application to a complete finite comparison covector

Suppose every actual ± word in the §7eo comparison recipe is an alternative
of that ONE law at its common paid horizon N. If a proved native weighted-law
identity establishes

    μ_N(γ) ∝ χ_N(γ) φ^(−κ B_N(γ)),                         (3)

on these alternatives, then (1) gives

    S_N(γ_+) − S_N(γ_−) = κ[B_N(γ_+) − B_N(γ_−)].          (4)

Consequently the ENTIRE declared linear finite-difference covector transports
coordinate by coordinate, with the original Jacobian, right lift, norm and
actual gain. No knowledge of separate Cost and Info is needed. No equality of
arbitrary nonlinear chords follows. Equation (3) is the required native
application, NOT a definition or a Gibbs selector being installed here.

If (4) has actual coordinate error δ_α, its dual-source error is bounded by
the existing basis-map constant times

    max_α |δ_α| / (2 |t_α| Γ_h).

Endpoint probability/price precision, compiler error, common-clock expansion
and every original source component must satisfy this same true-gain budget.

#### C3. What complete means for this application

* Separate experiments μ_N^y leave b_N(y); ordinary preparation/scene sources
  contain db_N. To apply (4) to those rows, their ± choices must be actual
  alternatives of ONE retained programme experiment, or their normalizer
  source must be measured/derived separately.
* Different-duration comparisons retain b_N−b_M. A general growing-history
  carrier permits arbitrary horizon dependence. The owned 2/3 clock inversion
  fixes one PER-TICK constant only after its stationary edge-local hypothesis
  and its actual common attempt/acceptance map have been supplied. It does not
  fix arbitrary b_N from one ratio. A genuine joint stopping law over the
  required horizons, with known attempts, can instead fix all their ratios.
* This scalar law is not automatically the Born law of the algebra-valued
  Book amplitude. For a single orthogonally retained branch with memory vector
  m_γ, the response is φ^(−2S_γ)||m_γ||². Its relative reconstruction has the
  factor 1/2 and the derivative of ||m_γ||². Coherent grouped histories retain
  their full Gram cross terms and phases. P2 cannot replace those by a scalar
  sum. `BOOK_SOURCE_BINDING.md` already owns the exact distinction.
* Retaining a random programme label changes the actual carrier and complete
  heat trace. Conditioning on a favourable programme branch would not meet
  (3). The weighted interpretation must retain all programme, failure, abort,
  record and clock branches with the true generated input and reference.

#### C4. The single native map still to instantiate

The owned positive sufficient map is the primitive weighted intertwining in
`FOUNDATIONAL_WEIGHT_BRIDGES.md` §2: intertwine the actual complete native
continuation transfer and terminal effect with the Book transfer. Concatenation
then proves every finite cylinder/suffix law, including moving preparation and
the full response-defect term of its §1. For a many-word compiler, it is a
fibrewise SUM of actual complete weights, not one implementation word's weight.

No inspected owner instantiates this map for the §7eo programme instrument
and its full growing-clock H+J. K913 supplies a conditional scalar law; the
native detector supplies a Born response; neither identifies them on its own.
The reduction (1)–(4) nevertheless changes the target: for the equal-duration
finite-source task, absolute C/I/W reconstruction and its horizon constant are
unnecessary once this FULL weighted-law identity is proved. Clock and external
preparation rows retain exactly the qualifications in §3.


### 8. Integration check and exact remaining consumer

Independent bounded review checked the full differential at matching, the local submersion including zero weights, the original input-cut distinction and the genuine measure term. The calculation is an application of H18–H20 and the already paid preparation/clock owners; no new numerical certificate or replay of unchanged geometric suites is needed.

The scientific change is an off-shell internally stationary programme section and a source-level route to global rigidity, with a prepared-CODE implementation that keeps the original physical input rank. This does not derive the physical continuation law or assert that the actual retained reader belongs to that section. Its surviving record/calibration normals, a genuinely admitted shared scalar controller, other WORK/scene inputs and variable-duration comparisons remain equations or explicit native transports. Neither the weighted-cylinder identity nor computational realizability is itself a proof that the kernel selects this family. The exact nonvacuum recovery and existing finite-source centres remain the consumers at their established scope. GR_closed=false; no assembly acceptance, public claim, task retirement or raw216 promotion.
