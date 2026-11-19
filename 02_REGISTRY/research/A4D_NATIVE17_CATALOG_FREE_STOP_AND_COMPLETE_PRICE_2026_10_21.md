# D0: unknown-strength native Golden17 verification and complete stopped price

21 October 2026. Supporting continuation in existing Draft #334, EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, native-programme-v1 / constitutive. Phase: native realization. Input checkpoint 5f92d32ac405f956fc5e10c4f06649e2728881f5. No new task, detector, physical Book action, field-minimum assumption or GR closure.

Consume [the known-magnitude exact test](A4D_NATIVE17_OPTIMAL_STOPPED_ORIENTATION_AND_INFO_2026_10_21.md), its original Golden17 reversal/source owners, and [the primary nonvacuum source-recovery route](D0_GR_PRIMARY_POSITIVE_CASE.md). The changed premise is explicit: the previous optimal threshold requires the supplied magnitude xi. This continuation constructs ONE fixed controller valid for every unknown nonzero xi in the same native chart, then derives a finite-cap source with no field-dependent compiler selection. The original known-xi optimality remains valid in its narrower policy class; exact optimality is NOT asserted for the new universal rule.

## 1. Same original data, no magnitude catalogue

Let p=phi^-1 and c=p^4/98304. The ORIGINAL strict null chart P(xi)=exp(xi N2), N2^3=0, has one sensitive pair of actual Golden17 probabilities

    u=c(1+xi/sqrt(2))^2, v=c(1-xi/sqrt(2))^2.

Set X=+1,-1 on these outcomes and X=0 on all other FIFTEEN real outcomes. All outcomes remain recorded, charged and included in the actual clock. Exactly

    s=u+v=2c(1+xi^2/2), E X=2sqrt(2)c xi,
    eta=E[X | X!=0]=sqrt(2)xi/(1+xi^2/2).             (1)

The task supplies only an error tolerance 0<delta<1/2. It supplies no nonzero lower bound or prior on xi, no fixed horizon, and no additional quantum angles. At xi=0 a definitive finite sign is not promised. IID repetition retains the earlier owner's actual fresh-known-probe and reference/observer admission premises, not unknown-state copying.

## 2. An exact Golden code for all classical evidence scales

For integer j>=1, theta_j=p^j is an arithmetic evidence coefficient, NOT a parameter of a new quantum measurement. Let ell=bit_length(j), r=the count of ones after the leading one. Encode j as 0^(ell-1)1 followed by those remaining digits. Original Golden symbol probabilities 0:p, 1:p^2 give

    mu_j=p^(L_j), L_j=2ell+r <=3ell-1,
    sum_(j>=1) mu_j=1,
    sum_(j<2^L) mu_j=1-p^L.                           (2)

Proof: each length-ell block has prefix probability p^(ell+1); its suffix probabilities sum to one. Sum the geometric prefixes using 1-p=p^2. This is one explicit self-delimiting algorithm, not a theorem that Book03 uniquely chooses this integer code. No fair quantum coin or physical scale draw is required: mu allocates evidence error budgets.

For the FULL record define

    M_(j,n)^+ = product_(t<=n)(1+theta_j X_t)
              = (1+theta_j)^Nplus (1-theta_j)^Nminus,
    M_(j,n)^- = product_(t<=n)(1-theta_j X_t).           (3)

Under the nonpositive-sign null, M^+ is a nonnegative supermartingale since its next-factor conditional mean is 1+theta_j E[X_(n+1)|F_n]<=1. M^- has the opposite null. This validity extends to non-IID histories with the actual corresponding conditional sign bound; time bounds below concern the fixed IID original detector.

At informative count k=Nplus+Nminus activate exactly j with k p^j>=1. There are at most floor(log_phi k) such scales. Announce a sign and stop once ANY active scale satisfies

    mu_j M_(j,n)^± >= 1/delta.                        (4)

Newly activated scales use the already retained counts, not a reset. For rational delta decisions can be exact in Q(p); the checker uses delta=1/10 and Z[p] ordering. Rational tolerance is a task specification, not a rational physical random coin.

Ville's bound for each j is delta mu_j. Summing (2) proves

    P_(xi<=0)(ever announce +)<=delta,
    P_(xi>=0)(ever announce -)<=delta.                (5)

The finite active subset cannot increase these errors. At zero, any sign assertion has total probability at most 2delta; unresolved output is allowed. At every fixed nonzero xi, termination is almost sure with finite expected full trial count by the following bound. These are analytic all-time results, not finite-simulation extrapolations.

The same native17 stream can carry twelve one-sided certificates for its six marked pairs by allocating delta/12 to each assertion. Zero coordinates can remain unresolved; no automatic all-six completion is asserted.

## 3. Actual paid observation count, including all neutral failures

For eta>0 choose j=max(1,ceil(log(eta)/log(p))) IN THE PROOF ONLY. Then p eta<=theta_j<=eta. Its informative-step log drift is

    g(eta,theta)=((1+eta)/2)ln(1+theta)
                +((1-eta)/2)ln(1-theta),
    partial_theta g=(eta-theta)/(1-theta^2),
    g>=eta theta-theta^2/2>=kappa eta^2,
    kappa=p-p^2/2=(3p-1)/2>0.                         (6)

This scale activates at k0=ceil(1/theta). Its accumulated log capital is then at least -phi^3, using -ln(1-theta)<=theta/(1-theta), k0<=1/theta+1, theta<=p. A positive increment is at most ln(1+p)=ln(phi). For A_j=ln(1/(delta mu_j)), bounded-time Wald and the overshoot bound imply

    E K <= k0+[A_j+phi^3+ln(phi)]/g(eta,theta_j).      (7)

Finite expected hitting time is a consequence, not a premise: bound the stopped walk additionally by n, apply the pathwise upper overshoot, and pass monotonically to the limit in g E(tau∧n).

The original IID waiting intervals between informative outcomes have mean 1/s and are independent of their signs. Hence ALL native executions obey

    E T <= (1/s){ceil(1/theta_j)
          +[ln(1/delta)+L_j ln(phi)+phi^3+ln(phi)]/g}. (8)

Since j=O(1+ln(1/|xi|)) and L_j=O(1+ln(1+ln(1/|xi|))),

    E T = O((ln(1/delta)+1+ln(1+ln(1/|xi|)))/(c xi^2)). (9)

Thus one can remove the supplied curvature magnitude at only double-log overhead in this upper bound over the old xi^-2 observation scale. For xi=h^2 f it gives an h^-4 log log(1/h) upper bound for THIS detector, not a universal quantum lower bound. Controller arithmetic/read/write/bit complexity are not free. O(log k) active updates per informative mark is a finite algorithmic statement, not paid-gate optimality. Numeric values in the receipt are conservative upper bounds, not measured expected run counts.

## 4. Complete stopped entropy is NOT merely the information about one sign

Let q_xi be the actual complete 17-category one-run law, C(omega) a supplied fixed one-run charge and W_T any additional genuinely paid history-dependent controller/preparation/arithmetic/clock work. A deterministic copy of the tape to controller registers adds no independent pointer entropy, but costs work. For any deterministic field-independent stopping rule with finite mean, IID factorization and entropy chain rule give

    H_phi(Gamma_T | xi)=E_xi T H_phi(q_xi),
    E_xi sum_(n<=T) C(omega_n)=E_xi T E_(q_xi) C.

Thus under the declared FULL CLASSICAL POINTER-entropy contract,

    S_ptr(xi)=a(xi) E_xi T+E_xi W_T,
    a(xi)=E_(q_xi) C-H_phi(q_xi).                    (10)

No physical selection of Shannon as Book03 Info is inferred. For an equal prior on the fixed +/-xi alternatives and a symmetric policy, instead

    H_phi(Gamma_T)=E T H_phi(q_+)+I_phi(H;Gamma_T),
    Sbar_ptr=abar E T-I_phi(H;Gamma_T)+E W_T.          (11)

For the OLD known-xi threshold m, terminal sufficiency gives I=log_phi 2-h_phi(epsilon_m). With L=ln(u/v), d=(u-v)L, z=mL/2 and alpha=2abar ln(phi)/d, exactly

    Sbar_m-E W_(T_m)
      =[ln cosh(z)+(alpha-1)z tanh(z)]/ln(phi).        (12)

Actual rate abar and remaining work must be supplied, not chosen for Einstein. When W=0 the continuous relaxation has a positive optimum iff 0<alpha<1/2, satisfying sinh(2z)/(2z)=(1-alpha)/alpha. Alpha>=1/2 selects zero in this relaxation. Fractional thresholds are not native actions.

If the actual per-run cost is a fixed normalized prefix-code charge -log_phi(mu) plus nonnegative work, put qbar=(q_++q_-)/2 and chi=H_phi(qbar)-H_phi(q_+). By symmetry chi is the binary experiment's maximum mutual information over priors. Then

    abar=chi+D_phi(qbar||mu)+Wbar>=chi,
    I_phi(H;Gamma_T)<=chi E T.                       (13)

The second inequality is the sequential information chain rule with the posterior at each actual executed trial and predictable survival. Therefore for nonnegative additional W_T,

    Sbar_ptr >= E T[D_phi(qbar||mu)+Wbar]+E W_T>=0.   (14)

For m=1 the capacity bound is saturated: every neutral outcome leaves the posterior at one half. If immediate zero-price/no-gain inaction is admissible, it is an optimizer of this particular nonnegative code-redundancy objective. A nontrivial run needs a real task constraint or a different independently derived physical price. Required accuracy can exclude inaction. This is not a no-go for the original algebra-valued Book action.

## 5. New SAME-PROGRAMME finite-cap source interface

The old m_min(xi,delta) changes with the supplied magnitude. Rule (4) contains NO xi. For a fixed RAW-time cap N its complete stop/continue/abort leaf set is independent of fields: it is a deterministic function of labels alone. Every abort remains in the record. On the strict positive chart,

    P_y(gamma)=product_(t<=T_N(gamma)) q_y(omega_t),
    D ln P_y(gamma)=sum_(t<=T_N(gamma)) D ln q_y(omega_t).

For an actual supplied complete leaf price C_gamma(y), the full-pointer source is exactly

    D S_N = sum_gamma P_gamma D C_gamma
          +sum_gamma [C_gamma+log_phi(P_gamma)] D P_gamma. (15)

The extra derivative term cancels by COMPLETE normalization sum D P=0. Work, controller, preparation, clocks and their moving price/Info sources are not zeroed. Infinite-horizon derivatives require a separate tail estimate. This gives one source formula on a fixed programme across the unknown-field chart; it does not prove equality to the full Palatini/CAR covector or solve independent preparation/observer equations.

## Validation and boundary

The [companion checker](sources/d0_native17_exact_sequential_2026-10-21/check_native17_unknown_scale.py) actually ran in the author session: exact Z[p] Kraft/stopping comparisons, original native u/v and neutral mass, a rational absorbing finite-cap recursion at five unknown sign strengths, drift/time bounds and stopped entropy/code identities passed. The universal entropy identity has a separately labelled generic three-symbol test fixture, not a replacement for the native five failure probabilities. The all-time proof is analytic. No independent review, Lean build, CI run, compulsory task or physical Book source is claimed.

External method, not a D0 physical premise: Howard, Ramdas, McAuliffe and Sekhon, *Time-uniform, nonparametric, nonasymptotic confidence sequences*, Annals of Statistics 49 (2021), DOI 10.1214/20-AOS1991, arXiv:1810.08240; *Time-uniform Chernoff bounds via nonnegative supermartingales*, Probability Surveys 17 (2020), DOI 10.1214/18-PS321, arXiv:1808.03204. The native detector, phi code and actual admission/price scope are consumed from D0. The general supermartingale method is not claimed as a new discovery.

The physical one-source and field-writing/stationarity gates remain open. `GR_closed=false`.
