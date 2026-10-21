# Book03 global weighted-scene equilibrium and a noncircular report-to-conductance source test

22 October 2026. Existing Draft PR #334, task EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE. New finite-dimensional theorem for the **already defined** 33-vertex K(9,11,13) weighted-scene heat-plus-full-history-feedback scalar; and a conditional operational interface test consuming the existing paid N1 reporter. No new physical action, freely chosen Info, free native weighted edges, controller, or GR-closure claim. GR_closed=false.

## 1. Exact global spectrum on the original three-zone equitable family

The prior owned [native shared scene price source](A4D_NATIVE_SHARED_SCENE_PRICE_SOURCE.md) defines all 359 genuine positive cross-zone conductances, original degrees, normalized transport T=D_d^{-1}A, normalized heat Delta=I-T, and all 718 history rows with the TRUE full return F_H=J(I-T²)C. It proves the exact full-history determinant identity

det(I_718-z F_H)=det(I_33-z(I-T²)),

retaining its nontrivial 718-dimensional complement, moving degree/archival pairing and all multiplicities. In this note no weighted scene is presumed physically admitted by D0's original binary passport.

Specialize only the **mathematical** conductance family with one positive value x on 9–11 edges (99 edges), y on 9–13 edges (117 edges), and u on 11–13 edges (143 edges). The normalized T annihilates the whole 30-dimensional within-zone balanced space. Its quotient on zone constants is the actual stochastic matrix

T_q =
[ [0,11x/(11x+13y),13y/(11x+13y)],
  [9x/(9x+13u),0,13u/(9x+13u)],
  [9y/(9y+11u),11u/(9y+11u),0] ].

The top eigenvalue is 1; trace is 0 and determinant is

kappa(x,y,u)=2574 x y u / [(11u+9y)(13u+9x)(11x+13y)].

The remaining two eigenvalues solve l²+l+kappa=0. Since this positive-undirected weighted graph's T is similar to a real symmetric matrix, kappa<=1/4. The complete normalized spectrum is 0 (multiplicity 30), 1, and -1/2 ± sqrt(1/4-kappa). Consequently the **full** prescribed Book03 scalar, not a selected column or assigned external source, equals exactly

B_beta,z(x,y,u)=Phi_beta,z(kappa(x,y,u)),

Phi_beta,z(k)=beta^-1 log Z_beta(k)-30 log(1-z)-log Q_z(k),

Z_beta(k)=1+30 exp(-beta)
           +2 exp(-3 beta/2) cosh(beta sqrt(1/4-k)),

Q_z(k)=(1-z)(1-2k z)+k² z²,

with the continuous analytic value at k=1/4. Here beta>0 and 0<z<1. The heat factor 30 and feedback factor 30 are genuine spectral multiplicities. The equality holds at **every positive equitable weight triple**, not only at the canonical first jet. It does not claim that arbitrary non-equitable 359-edge weights have only this invariant.

## 2. Global sharp balance and a natural information-geometric coordinate

The elementary three-factor AM–GM inequality yields

(11x+13y)(9x+13u)(9y+11u)
 >=8 sqrt[(11x)(13y)(9x)(13u)(9y)(11u)]
 =8*9*11*13*x*y*u.

Thus 0<kappa<=1/4, with equality precisely when

11x=13y, 9x=13u, 9y=11u,

or equivalently **x:y:u=13:11:9**, up to an arbitrary positive common scale. At the canonical original binary scene x=y=u=1, kappa_0=39/160 and the exact derivatives are

kappa_x=91/2816, kappa_y=13/6400, kappa_u=-1209/35200.

An intrinsic coordinate for the quotient by common scaling is

t=log(11x/(13y)), s=log(9y/(11u)).

Using a+b=2 sqrt(ab) cosh[log(a/b)/2] in all three denominators gives the exact, global identity

   kappa(t,s)=1 / [4 cosh(t/2) cosh(s/2) cosh((t+s)/2)].

The balance is t=s=0. The only κ-critical point in the positive (t,s)-plane is the balance: differentiating log κ, its directional derivative along any nonzero ray (t,s)=r(a,b), r>0, is

-(1/2)[a tanh(ra/2)+b tanh(rb/2)
                  +(a+b) tanh(r(a+b)/2)]<0.

Every summand is nonnegative and at least one is positive. Thus all κ<1/4 level curves are smooth; away from the balance, a one-dimensional tangent is isospectral, and the independent overall scale is another exactly price-neutral coordinate.

The exact Hessian at balance is

D²_(t,s) kappa = [[-1/8,-1/16],[-1/16,-1/8]],

with eigenvalues -3/16 and -1/16. The full mathematical scene price therefore has two shape directions and one common-scale zero direction. The other non-equitable edge directions are NOT eliminated by this coordinate chart.

## 3. Fixed original Golden calibration: strict global monotonicity

Retain the actual original HJR/Golden calibration, not a tuned heat/feedback cancellation:

p=phi^-1, beta=2p², z=2^-20.

For k in (0,1/4], put delta=sqrt(1/4-k). Differentiating the complete scalar gives

Phi'(k) = -exp(-3beta/2)*sinh(beta delta)/(delta Z_beta(k))
          + 2z[1-(1+k)z]/Q_z(k),

where sinh(beta delta)/delta is beta at delta=0. This analytic expression includes all 30 zero transport eigenvalues in Z and Q.

Because p>3/5, 7/10<beta<1. For 0<=delta<1/2, sinh(beta delta)/delta>=beta, exp(-3beta/2)>exp(-2)>1/8, and 0<Z_beta(k)<=33 (all 33 heat eigenvalues correspond to nonnegative Delta). Therefore the positive magnitude of the thermal negative derivative exceeds 7/2640.

Both nontrivial feedback eigenvalues lie in [0,1], giving Q_z(k)>=(1-z)²>1/4, and the positive feedback derivative is <2z/Q_z<8z=1/131072. Consequently the following GLOBAL inequality has a strict rational proof:

   Phi'(k)<-[7/2640-8*2^-20]
          =-57179/21626880<0.

The weighted equitable scene price is strictly decreasing with κ. Its **unique global minimum modulo scale** is exactly the balanced ray x:y:u=13:11:9. At canonical x=y=u=1, kappa=39/160; integrating the strict bound from 39/160 to 1/4 yields

   B(1,1,1)-B(13,11,9)>57179/3460300800>0.

This is an actual nonzero absolute price contrast within the SAME specified 33-vertex master and same beta,z, not a CQ-reporter comparison or a change of heat. Its high-precision numerical check is approximately 9.72556182199559e-5; that decimal is not used in the proof.

At balance, Dkappa=0, so all **three equitable** derivatives of the master vanish. Moreover, the complete 359-edge gradient vanishes at the same balanced matrix: B is invariant under every permutation inside a zone; its gradient entries are equal on each of the three edge orbits. Each equitable derivative is the sum over its corresponding orbit, hence their three vanishing sums force every individual edge gradient to vanish. This is a complete **first-order** mathematical statement on the 359-dimensional positive-weight extension; no full359 Hessian minimum is claimed. Along the two equitable shape directions, however, the Hessian is exactly Phi'(1/4) D²κ, with eigenvalues -3 Phi'(1/4)/16 and -Phi'(1/4)/16, both positive. The common-scale Hessian is zero.

Therefore ANY differentiable field-to-weight map landing at this balanced scene has zero first scene source by the chain rule. The bare weighted scene's own minimum cannot be used to transmit a nonzero Einstein/CAR covector.

## 4. A noncircular proposed source carrier using genuine Born reports

The earlier [derived-scene source transmission](A4D_BOOK03_DERIVED_SCENE_J2_SOURCE_TRANSMISSION_2026_10_21.md) used the mathematical prescription x(Y)=1+J_2(Y)-J_2(Y*). That reproduces the target covector, but asks an upstream writer to compute the target action itself. Here is a **weaker, directly measurable candidate interface**, not a declaration of its compulsory physical role.

Consume the actual paid finite N1 moment/report construction from
[A4D_NATIVE_GOLDEN_REPORT_TO_BOOK_FEEDBACK_ALL42_2026_10_21.md](A4D_NATIVE_GOLDEN_REPORT_TO_BOOK_FEEDBACK_ALL42_2026_10_21.md).
Let c_i be its TRUE positive integer multiplicities of separate literal local report copies, W=sum_i c_i>0, and r_i(Y) each actual configured binary report probability. On the common-null Einstein--CAR section they all have the same r0 in (0,1/2). The owned counted-CQ scalar, on its field-independent-bank-cost chart, obeys

S_CQ(Y)=B_m-gamma_m sum_i c_i h_phi(r_i(Y)), gamma_m>0,

D S_CQ|_null=-gamma_m W h_phi'(r0) D R,
R(Y):=(sum_i c_i r_i(Y))/W,
h_phi'(r0)=log_phi[(1-r0)/r0]>0.

A uniform lottery among the W **literal already counted copies**, using paid fair H bits, a fixed Boolean comparator and finite capped independent retries, has selection success probability alpha>0 independent of Y. Conditional on the known selector success, it uses index i with probability c_i/W. Retain the full index, aborts, every unused bank row, clock and work. The **unconditional** joint law has

P(I=i,click)=alpha c_i r_i/W,
P(I=i,no-click)=alpha c_i(1-r_i)/W,
P(early abort)=1-alpha.

Thus the complete measured law determines the absolute marginal P(click)=alpha R(Y); no postselected physical price or erased index is presumed. The input/output ROW states and the own Book03 Info of that sampler remain different uncomputed ledgers.

As a possible *derived* positive scene parameter, define only the numerical ratio

    x_report(Y)=P(click)/(alpha r0)=R(Y)/r0,
    y=u=1.

It is an **operational measurement statistic**, not an existing D0 rule converting a measured event frequency into a physical conductance. At the common-null section x_report=1 and its complete 42-field first jet satisfies the exact sourced identity

D_Y B(x_report,1,1)
   =-[Phi'(39/160)*(91/2816)]
      /[gamma_m W r0 h_phi'(r0)] *D_Y S_CQ,

whose prefactor is strictly positive by §3. No coefficient is fitted; it is determined by the fixed scene, original Golden report, real multiplicities/readiness and the selected ratio. The identity is **first source on the common-null section**. Off that section the individual h_phi'(r_i) differ and a single R is not generally sufficient for full CQ source or Hessian; no nonlinear all42 action equivalence is asserted.

This removes the need to encode J_2 itself in a candidate conductor: the finite binary report law supplies the needed scalar FIRST JET. But native admission still must convert that complete statistic into the actual moving degrees/edges of Book03 Delta_N and F_N, and pay every independent preparation, controller, clock, work and Info derivative. Merely defining x_report does NOT prove that conversion, and original **binary passport** scene is rigid under these continuous weighted variations. In particular no new graph weight is installed in native D0 by this note.

## 5. Decisive native-selection trilemma

The established exact alternatives are now:

1. Under the **original binary 33-vertex passport** of DenseOperatorSceneRigidity, the native normalized heat/return scene price is constant on all allowed passport scenes; it has zero geometry source. This is consumed from the prior [shared scene owner](A4D_NATIVE_SHARED_SCENE_PRICE_SOURCE.md), §8, not proved anew here.
2. Under freely **optimizable positive weighted** cross-zone edges, the natural three-parameter equitable subfamily has a global master minimum at 13:11:9 and the full359 gradient zero there. Its first field source therefore vanishes at that minimum. The canonical scene 1:1:1 is NOT that optimum.
3. A **source-carrying generated/reaction-constrained weighted scene**, for example one with a truly native map like the measured statistic in §4, can have the correct *mathematical* 42 first-source jet at the canonical scene. Its independent normal-conductance Euler row is nonzero and must not be freely varied unless an actual source or constraint reaction is derived.

This is a strong reason **not** to pursue unconstrained scene-conductance minimization as a complete GR selection law. A more promising native route may retain the rigid binary scene and generate the field dependence in a paid **device feedback factor**, as in the separately owned actual Golden reflection bridge; the latter still faces coherent uncomputation/complete-memory and independent-controller source gates. None of the three mathematical routes is yet selected by the physical D0 controller or complete compulsory Book03 valuation.

The mathematical theorems above are global in the stated equitable positive graph class, and the 359 first-jet statement concerns its balanced point. They do not assert a globally minimizing point over all arbitrary 359 independently weighted edges, nor a physically selected Book03 action. Original 42-field full-price/admission/refinement and raw216 remain open: GR_closed=false.

## 6. Reproducibility

Companion bounded standalone diagnostic \`check_book03_balanced_scene.py\` checks the exact fractions (39/160, 1/4 and canonical three derivative coefficients), positive rational weight controls, the hyperbolic two-shape-coordinate identity, the complete 33×33 normalized matrix spectrum and both actual master traces, the 359 edge-source components at the balanced configuration, the price gap, and the positive two-shape Hessian. The algebraic proof of the global derivative inequality and all-size 359-edge statement is in §§1–3; finite floating checks do not replace it.

A verified local replay with NumPy gave 359 original edges, exact rational lower gap 57179/3460300800, numerical gap 9.725561821971596e-5, maximum complete balanced first-edge derivative 1.34e-19 and full closed-form spectral price discrepancy below 4.5e-16. No old root, physics, full128, Lean or raw216 suites were rerun.

## 7. Stronger: a 31-dimensional isospectral stationary manifold in the **full 359-edge** space

The balanced 13:11:9 **equitable ray** is merely a slice of a larger exact family. Write the zone sizes as n=(9,11,13), and the three balanced edge factors as w^0_(9,11)=13, w^0_(9,13)=11, w^0_(11,13)=9. For each of all 33 vertices independently choose s_i>0, imposing only the **three** constraints

    sum_{i in zone a} s_i=n_a   (a=9,11,13).

Give EVERY cross-zone edge i∈a,j∈b its genuine positive weight

    w_ij = w^0_ab s_i s_j.

There are 33−3=30 independently variable vertex factors. A separate common positive scaling of every edge supplies a 31st independent parameter. These are truly different positive conductance arrays: under the fixed zone-sum constraints, ratios of edges sharing a target recover each source vertex factor, so the parameter-to-weight map is injective.

**Exact spectrum.** Every vertex i in zone a has the actual degree d_i=s_i d^0_a, with d^0=(286,234,198). Consequently the full 33×33 stochastic operator has entries

    T_ij = w^0_ab s_j / d^0_a    (i∈a,j∈b,a≠b).

Let J embed zone constants into all vertices, and let Z take the s-weighted mean in each zone: (Z f)_a=(1/n_a)sum_{i∈a}s_i f_i. Then ZJ=I_3 and

    T=J T_0 Z,     T_0=(ones_3 ones_3^T−I_3)/2.

It follows that the full transport spectrum is EXACTLY {1,−1/2,−1/2,0^30} for **all** these independently varying 30 parameters. The true 718-history Sylvester feedback and full 33-vertex heat price therefore have exactly the same value Phi(1/4) everywhere on this family. This is not a relabeling of the unweighted scene: individual vertex degrees and conductances genuinely change.

**The stronger, all-edge stationary statement.** Constancy along this 30-manifold alone would not guarantee vanishing of the 359-dimensional ambient gradient; we check every edge direction analytically. Let m(t)=exp[-beta(1−t)]/Z−2z t/[1−z(1−t²)] be the exact scalar from the original complete weighted-scene derivative, and let M=m(T). Define the two idempotents P_zone=JZ and P_1=J[ones_3 ones_3^T/3]Z. Since T has eigenvalues 1,−1/2,0 with projectors P_1, P_zone−P_1 and I−P_zone,

    M=m(0)I+[m(−1/2)−m(0)]P_zone
                 +[m(1)−m(−1/2)]P_1.

Put c=[m(1)−m(−1/2)]/3. For i∈a,j∈b,a≠b, the displayed spectral decomposition gives the **actual complete matrix entries**

    M_ji=c*s_i/n_a,    M_ij=c*s_j/n_b,
    (TM)_ii=c*s_i/n_a, (TM)_jj=c*s_j/n_b.

Substitute these into the existing all-edge source formula (native shared-scene owner, equation (5)):

    omega_ij=M_ji/d_i+M_ij/d_j
                   −(TM)_ii/d_i−(TM)_jj/d_j = 0.

Every cancellation is exact for every one of the **359** independent cross-zone edge jets, any beta>0 and 0<z<1. The moving degree, history pairing and full feedback are already inside M and this formula. Thus the 30 vertex-redistribution parameters, plus scale, describe an exact **31-dimensional full-gradient stationary manifold**, not merely a family of equal values on which transverse Euler rows could remain nonzero.

Differentiating the identically zero full gradient along this smooth injective family shows that **the full 359×359 Hessian has at least 31 independent kernel vectors at every member of the family**. We make no positive-definiteness or global-minimum claim in the remaining 328 directions; the original section 3 proves global minimality only within the *three-parameter equitable* subfamily. This explicit degeneracy is a further obstruction to asserting unique apparatus preparation or isolated physical selection from the weighted-scene scalar alone.

A separate narrow checker \`check_book03_vertex_balance.py\` verifies three non-equitable rational factor arrays. It evaluates all 359 analytic edge cancellations in exact rational arithmetic and independently recomputes the true 33×33 normalized spectrum, complete master scalar and complete per-edge source to floating accuracy. All three trials pass, with maximum full359 numerical first-source norm below 2.4e−19. The general conclusion is the projector proof above, not an extrapolation from those three controls.

The original D0 **binary** 33-vertex passport still does not admit these weights without an explicit paid native extension. No new scene preparation, Book03 Info law or GR selection is derived. GR_closed=false.


## 8. A genuine 296-dimensional positive second-variation block at the balanced scene

The 31-dimensional kernel does NOT exhaust the actual transverse response. There is a directly proved 296-dimensional independent subspace with **strictly positive** Book03 second variation, at the original beta=2p², z=2^-20.

For each pair of zones a,b, choose zero-sum vectors f on a and g on b and vary all their cross-edges by the symmetric matrix E=f g^T+g f^T. Linear combinations span

    (9−1)(11−1)+(9−1)(13−1)+(11−1)(13−1)
    =80+96+120=296

independent real edge directions. Each E has zero row-degree sum, hence D_d is EXACTLY fixed on the straight positive-weight curve A(t)=A0+tE. Put V=D_d^-1 E. At the balanced rank-three graph, T0 V=V T0=0. Consequently the trace-exp and full-feedback factors can be differentiated explicitly on the 30-dimensional null zone-balanced subspace, yielding, for every nonzero such E,

    D² B[A0](E,E)
       =[ beta exp(-beta)/Z_beta(1/4) − 2z/(1-z)] Tr(V²),

    Tr(V²)=sum_(i,j) E_ij²/(d_i d_j)>0.

This is the existing exact weighted-scene Hessian mechanism evaluated at the NEW balanced full359-stationary manifold, not an assumed positive metric or an added stabilizing action. Because 7/10<beta<1, exp(-beta)>1/3 and Z_beta(1/4)<=33,

    beta exp(-beta)/Z_beta(1/4)>7/990,

while 2z/(1-z)<4z=1/262144. Therefore the bracket is STRICTLY positive with a fixed elementary lower bound. The previously identified 31 null tangent directions and these 296 positive directions are distinct; the two equitable shape directions also have strictly positive Hessian. The sign of the **remaining 30-dimensional transverse star block**, and therefore full359 local minimality, is not claimed by this analytic argument.

A literal zero-sum edge-square fixture (f=e0−e1 on the 9-zone, g=e9−e10 on the 11-zone, actual degrees 286 and 234) has Tr(V²)=8/(286*234) and analytical second response approximately 2.7247680179231694e-6. Re-evaluating the complete 33×33 original master on the exact positive curves at step 1/4 yields 2.7247684641906744e-6; their difference has the expected even-order finite-difference truncation and is not used as proof.

The entire ambient carrier is **359 edges**, with one 31-dimensional proven Hessian kernel and a separate 296-dimensional strictly positive test subspace. The remaining 32-dimensional complement (two known positive equitable shapes and 30 star directions) requires its own full mixed-sign analysis before a global full-edge minimum is asserted. Physical native binary/weighted admission, complete memory selection, and GR remain open.
