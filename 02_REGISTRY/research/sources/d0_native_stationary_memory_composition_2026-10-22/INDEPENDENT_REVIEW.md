# Independent review: native stationary age-memory source and Poisson transfer

22 October 2026. Review of `AGE_CLOCK_SOURCE.md`, `SPECTATOR_POISSON.md`, and the associated finite checkers within the existing #334 native-programme/constitutive owner. Scope: exact finite matrix/entropy identities, their conditional native application, and numerical/exact-rational diagnostics. No physical Book03 selection, full42 stationary root, or uniform GR refinement is certified.

## 1. Ownership check: reuse the oldRIGHT theorem rather than rediscover it

An integration-time owner audit located an already existing result:

`A4D_ORIGINAL_OLDRIGHT_ARCHIVE_FREDHOLM_INFORMATION_AND_TWO_STAGE_GATE_2026_10_22.md`, Git blob `c2e897caa3416694c71bc6ddf1c3942f76e856ff`, already present in frozen PR#334 head `9239b31ec81092408ed1a5289f1412c83206f720`.

Its §§3-4 already prove the complete stationary DATA×oldRIGHT fixed algebra, the projector Pi*, the Fredholm condition that the projected RIGHT score be scalar, the uniform-RIGHT solution for raw terminal CQ entropy, and the positive RIGHT Hessian. These are **existing prerequisites**, not new results of the current packet. `SPECTATOR_POISSON.md` was revised accordingly. The earlier DATA-only Poisson warning is therefore not treated as the current unresolved fixed-algebra theorem.

The genuinely new composition reviewed here is:

1. Ambient tensor-log cancellation for the **entropy-gain** score, including arbitrary correlated input variations, through the existing Fredholm criterion.
2. The actual finite native **age instrument**, its clock-DATA entropy and spectral source, without reset or an iid premise.
3. The finite conditional-clock-entropy versus true-input-gain boundary defect and exact centered Poisson/field-source transfer on that **same** native instrument.
4. A controlled native spectral cancellation and finite-cap estimate, with a reproducible exact rational sign bound.

## 2. Actual no-reset age instrument: approved

Assume the frozen original instrument has complete CPTP sum Phi, true positive blank operator B=I-t Delta with 0<B<I, the owned stationary DATA state rho=Delta^-1/Z, and Phi(rho)=rho. The nonblank CP map is A=Phi-Ad_B, containing all original nonblank Kraus branches.

For the actual fixed K-tick history, grouping words by the number of trailing blanks gives

    L_n=Ad_B^n A Phi^(K-n-1), 0<=n<K,
    L_K=Ad_B^K,
    sum_n L_n=Phi^K.

The last identity is a noncommutative telescope; no commutation of CP maps is assumed. The coarse output blocks on the stationary section are exactly

    X_n=(t/Z)(I+B)B^(2n), n<K,
    X_K=rho B^(2K),
    sum_n X_n=rho.

These are real reduced blocks of the full retained finite history. Calling this a last-age readout does not erase any fine history from the actual ledger. The coarse scalar is not the full fine-archive information source.

## 3. Entropy, spectral heat and finite cap: approved with stated interpretation

Because rho and B are functions of the same positive Delta, the joint clock-DATA entropy satisfies

    S(Gamma_K)-S(rho)=Tr rho (I-B^(2K)) g(B^2),
    g(s)=-log(1-s)-s log(s)/(1-s).

This is conditional entropy of age given terminal DATA, retaining the conditional quantum states. It is generally different from Shannon entropy of the age marginal. The full fine archive has the exact additional conditional entropy H(fine|age,DATA); its nonnegative value does not imply any sign or smallness of its derivative.

The positive countable spectral representation

    H_n=beta^-1[-log((I+B)/2)-2n log B]

has trace Z_age=Z/(2t) and its normalized Gibbs blocks equal X_n exactly. It is generated mathematically by the actual arrival state and blank survival. It is **not** thereby the physical Book03 Hodge operator or a proved paid energy term.

There is also an exact finite representation of the real capped record. Retain the n<K blocks and use

    H_tail=beta^-1[-2K log B+log(2(I-B))].

Its Boltzmann block is B^(2K)/[2(I-B)], the same partition remains Z/(2t), and the normalized tail equals the real X_K. H_tail is nonnegative precisely when B^(2K)<=2(I-B). This is verified on the stated original chart at K=4096; it is not asserted at arbitrary small caps. The finite operator still uses nonalgebraic logarithmic functional calculus, and its physical admission is separate.

Normalized state entropy does not acquire a multiplicity r from oldRIGHT. An unnormalized heat trace tensored with I_R does acquire its actual r factor. A Gibbs state of H tensor I_R has uniform RIGHT I_R/r; an arbitrary spectator state contributes its actual entropy rather than automatically log r. This distinction is retained.

## 4. Required correction found during review: input gain versus terminal conditional entropy

The initial age preparation formula differentiated

    S(F_K sigma)-S(Phi^K sigma),

whereas true information gain uses S(F_K sigma)-S(sigma). Values and total field jets agree on the stationary section; independent preparation cotangents do not. This distinction was reported and corrected explicitly in `AGE_CLOCK_SOURCE.md` (13a,b), then composed with the oldRIGHT projector in `SPECTATOR_POISSON.md`, §6.

For price Cost-Info/ell, ell=log(phi), Psi=Phi tensor id_R, and a faithful stationary joint input Omega, define

    B_K=ell^-1 sum_(j=0)^(K-1) (Psi*)^j log Omega.

The exact full ambient score defect is

    M_gain-M_cond=((Psi*)^K-I)log Omega/ell
                 =-(I-Psi*) B_K.

The correct full centered multiplier and direct field source obey

    Y_gain=Y_cond-B_K+Pi*B_K,
    f_gain-f_cond=Tr[B_K (D Psi)Omega].

Consequently

    f_gain+Tr[Y_gain(D Psi)Omega]
      =f_cond+Tr[Y_cond(D Psi)Omega].

The final Pi* pairing vanishes by DATA trace preservation. This proves equality of complete stationary sources while retaining all independent input rows. A fixed-gap bound controls B_K-Pi*B_K uniformly in K and gives geometric convergence to the existing centered Green response; this is not a mesh-uniform gap claim.

This transfer remains exact if the true full fine conditional entropy or genuine paid ledgers are retained on both sides. Such terms change the common score and adjoint; they are not set to zero by the universal boundary correction.

## 5. Independent finite normal/source replay

`check_age_spectator_poisson_weld.py` performs 54 checks on the **previously owned rational two-Kraus noncommuting fixture**, DATA2×RIGHT2, at caps1,2,3,6. It is not an original full128 replay. The declared parent per-label cost is 1+bit; no external compensating charge is introduced.

The checker enumerates the real fixed-window Kraus words and groups their output by trailing-blank age, including the unresolved allblank event. It uses a faithful nontracial RIGHT state and tests full joint ambient input derivatives, projected Euler rows, the adjoint shift, fixed-input source correction and independent differentiation of the actual stationary curve.

- Full joint operator Euler residuals are below 5e-15.
- Corrected source equality errors are below 2.5e-10.
- Independently differentiated stationary curves agree within 6.9e-10.
- Deliberately retaining the unshifted conditional adjoint in the true gain source gives a nonzero error approximately 0.5165236963.

These are floating diagnostics of proved finite identities. They do not establish the original native field writer, the full42 source or physical Info selection.

## 6. Structural native spectral cancellation: analytical proof reviewed

The audit consumes the original pinned CAR16 two-band spectral values and jets at the named (r,nu)=(1/9,3/5) fixture:

    mu=141489/10240000, h=69399/5030720,
    mu_r=-328779/204800000, h_r=-20040939/9885993640,
    mu_v=mu_r-mu h_r/h, D_v h=0,
    lambda_+-=mu+-sqrt(mu(mu-h)), t=3-sqrt(5).

No new original full128 matrix replay is claimed. On this section,

    S(Gamma_age)=log(Z/(2t))+Tr rho F(t Delta),
    F(x)=1-x/2-x^2/24+x^3/24+47x^4/960+... .

The exact coefficient formula and the all-k bound |a_k|<=1 for k>=2 were checked algebraically. The upper bound uses the geometric positive sum <=1-2^-k; the lower bound exceeds -2/k. Thus the full Taylor remainder and its derivative are bounded by convergent geometric sums, not by a finite coefficient census.

At fixed h and positive mu_v, the native two-band moments satisfy

    M_k=Tr rho Delta^k=(h/2)(lambda_+^(k-1)+lambda_-^(k-1)),
    0<=D_v M_k<=h mu_v (k-1)^2 lambda_max^(k-2).

The moment inequality follows by differentiating the two roots and using (a^m-b^m)/(a-b)<=m a^(m-1) for a>=b>0. Summing the entire differentiated k>=4 tail gives the exact bound in `AGE_CLOCK_SOURCE.md` (15b).

`check_age_clock_rational_bound.py` persists a fully reproducible **29-check Fraction replay**. All asserted inequalities use rational arithmetic, including rigorously bracketed square roots of the native rational radicand and of 5. Floating numbers in its JSON are display previews only.

The replay proves t lambda_max<q=.012, h<.0138, and 0<mu_v<.00044. It verifies that the quadratic negative source dominates the entire later tail and obtains

    D_v S(Gamma_age)<0,
    |D_v S(Gamma_age)|<1.7483801195266405e-7<1.8e-7.

It also verifies both named native directions' band-weight and blank-probability derivative bounds. At cap4096 the exact rational tail comparisons give

    entropy tail <=6.920815741862039e-36 <7e-36,
    source tail  <=5.877514538871135e-34 <6e-34,

and ensure positivity of the finite spectral tail block. These are bounds on the **named local age-entropy source**, not on an uncomputed full42 normalized residual or arbitrary physical refinements.

The roughly9000-fold numerical reduction compares the two explicitly stated candidate entropy/thermal+feedback expressions on one native one-port-null tangent. It is not a demonstrated cancellation of the compulsory full physical price. Other actual tangent sources remain nonzero, and fine-history information, native costs, clock and work reactions remain mandatory.

## 7. Final acceptance and limitations

APPROVED as scoped mathematics: the real finite age channel; clock-DATA entropy and its functional derivative; finite/countable spectral representation; corrected independent input-gain cotangent; exact same-instrument boundary/Poisson/field-source weld; ambient gain tensor cancellation using the **existing** oldRIGHT Fredholm owner; fixed-chart analytic source and cap bounds.

CONSUMED, NOT NEW: stationary joint factorization, Pi*, general Fredholm compatibility, raw terminal-CQ uniform RIGHT solution and its Hessian, original primitive DATA preparation and spectral fixture values.

OPEN: compulsory Book03 Delta_N(V)/Info/cut/clock selection; actual paid finite preparation with its complete retained archive; any real non-spectator RIGHT interaction or charge; native field-writer admission; full42 physical stationarity and source-normalized uniform refinement. A pure original Choi+coherent-prefix input cannot be replaced by a mixed stationary product at zero cost. The original owner already proves that its reference correlations persist in the retained archive.

No physical closure or promotion follows merely from the passing checkers. The contribution is a new explicit normal/source composition on an actual finite native record, with every remaining physical term identified rather than fitted away.
