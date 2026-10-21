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