# Finite scalar-reporter recovery: complete code–information source and a universal first jet

20 October 2026. Existing scientific PR #334, `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, `native-programme-v1`. Phase: native realization. Scientific input fixed at `d333307d031123aedf7a49b35a12ce5f7c17fc04`; main was subsequently observed at `6c6b3ce0c3d658e27f49fe71975ad30923c2baee`. Research-positive conditional construction, not physical Book03 selection or GR closure.

## 0. The parent substitution and what actually changes

The [causal source synthesis](A4D_CAUSAL_BOOK_SOURCE_TO_EXACT_GR_SYNTHESIS_2026_10_20.md) and its [CAR geometric proof](sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/proof.md), §§4–7, already construct a complete unitary query with real scalar clean-input compression `i* U(y) i = t(y) I`. On the primary common-null family `Sigma`, `t=0`, and its full ambient first derivative is the known geometric source. Its original Golden port reporter has the correct known Cost derivative, but retained query work, information and causal preparation still require attention.

**New substitution:** two recorded attempts to restore the fresh reversible query workspace suffice to make the *entire output amplitude and its first field derivative*, not only the observed port effect, factor through the single scalar `t`, with the logical input and arbitrary oldRIGHT unchanged to first order. The actual complete eight-leaf 0/10 code, its pointer Shannon information and its coherent-record entropy now have explicit first sources. Every outcome, including unfinished recovery, remains in the instrument. There is no imposed success postselection, no independent copy, and no infinite runtime in the finite theorem.

The result is a prospective modification of that already constructed scalar reporter. It does **not** remove the residual of the distinct original energy-counting full128 programme calculated in [same-representative paid source](A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md). Its price has not been subtracted, redefined or silently replaced. Choosing this reporter as compulsory Book03 execution is still a separate admission/valuation premise.

### Exact interface

An isometric clean embedding `i: H -> W tensor H` is fixed. Its projector is `P=i i*`, `Q=I-P`. The executed unitary `U(y)` and its inverse are available on the same fresh reversible work; on an open real chart

    i* U i = t I,       t real,       |t|<1.                 (1)

The query may be non-Hermitian. The actual existing scalarization supplies (1) on the entire padded site-times-CAR input, not only one input vector. Fixed arbitrary oldRIGHT is tensored with identity. Every blank/nonblank test below is a coherent two-subspace `P/Q` registration, retaining its flag; it is NOT a measurement of each work address.

Admission/payment of `U`, `U*`, the clean-subspace test, controlled branching, and their fresh prepared work must be supplied. The inverses may act on fresh computational work but **not on a separately registered protected old history**. That distinction has an explicit hostile control in §7.

## 1. Exact operator recovery, without knowing the unknown data

Set `s=sqrt(1-t^2)` and define the isometries

    J_+ = (U i - t i)/s,       J_- = (U* i - t i)/s.

Then `i*J_+=i*J_-=0`, `J_+*J_+=J_-*J_-=I` and, exactly,

    U* J_+ = s i - t J_-,
    U J_-  = s i - t J_+.                                  (2)

For example, substitute `J_+` and use `U*U=I`, followed by `U*i=t i+sJ_-`. No assumption `U=U*`, no inverse on a kernel, and no input preparation is used.

Use the **existing** Golden reflection/comparison, `p=phi^-1`, `p+p^2=1`, with complete port maps

    A_0=p^2 i+p U i,       A_1=p sqrt(p)(i-U i).

In the two orthogonal isometric components these are

    A_b=a_b i + beta_b s J_+,
    a_0=p^2+pt,      beta_0=p,
    a_1=p sqrt(p)(1-t), beta_1=-p sqrt(p).                  (3)

Record port `b`, then record the `P/Q` test. A clean outcome ends the run. On a nonclean outcome apply `U*`, record another `P/Q` test, and stop if clean. If still nonclean apply `U`, record a third `P/Q` test, then stop in either case. A remaining nonclean output is explicitly flagged **unresolved**, not discarded.

With a cap of `N` recovery queries, alternately `U*,U,...`, the actual completed amplitudes are

    K_(b,0)=a_b i,
    K_(b,k)=beta_b (1-t^2)(-t)^(k-1) i,  1<=k<=N,          (4)

and the unresolved map is `beta_b s(-t)^N J_(parity)`. Hence its effect is scalar as well. The complete probabilities, for EVERY normalized logical/source/reference preparation, are

    q_(b,0)=a_b^2,
    q_(b,k)=beta_b^2 (1-t^2)^2 t^(2k-2),
    q_(b,?)=beta_b^2 (1-t^2)t^(2N).                        (5)

Their sum is one and

    P(unresolved)=p(1-t^2)t^(2N).                           (6)

Every intermediate conditional map is a scalar multiple of an isometry (`i`, `J_+`, `J_-`, or their orthogonal linear combination in (3)). It therefore preserves the oldRIGHT Gram after normalization, including a supplied `M*M=I128/128`. This is stronger than preservation only after averaging outcomes. The logical data are restored exactly on each completed clean record; no assertion of logical restoration is made on the explicitly unresolved branch.

## 2. The decisive two-attempt theorem: restore the FIRST JET, not only the state

One recovery attempt is enough to restore the state exactly at `t=0`, since its unresolved amplitude is proportional to `t`. It is **not** enough to remove the first derivative of unknown work: the latter still contains `J_-(y)` and the actual source input. An argument based only on the zero probability of the unresolved outcome would miss this coherent first derivative.

Two recovery attempts change that amplitude to `O(t^2)`. Let `V_2(y)` be the complete recorded output isometry, including all eight coarse leaves and all output work. At a point `y0 in Sigma` with `t(y0)=0`, identify clean work with its original fixed blank. Then

    V_2(y0) = |r_0> tensor i,
    D V_2(y0)[v] = |r_1> tensor i * D t(y0)[v].            (7)

No omitted remainder occurs in these two equations. On the resolved records the scalar coefficient vector is (in `b=0` then `b=1` order)

    r_0 = (p^2, p, 0, 0 ; p sqrt(p), -p sqrt(p), 0, 0),
    r_1 = (p, 0, -p, 0 ; -p sqrt(p), 0, p sqrt(p), 0),    (8)

where the entries are clean / first recovery / second recovery / unresolved. They satisfy `||r_0||=1`, `<r_0,r_1>=0` and `||r_1||^2=2p`.

Proof: differentiate (4); the unresolved `t^2 J` and its differential vanish at `t=0`. The derivative of `J(y)` is not frozen; it is multiplied by `t^2`. The same proof works with all independent coframe, proper-link, material, observer and preparation jets admitted by (1).

**Universal source consequence.** Every fixed differentiable functional of this *complete final apparatus record*, or every fixed Hermitian record price, has first source `kappa dt` at Sigma. The coefficient is determined by its actual valuation on the two fixed vectors (8), not by hidden data occupation or a chosen coframe component. Its normalized logical-input/oldRIGHT preparation source is zero. Any remaining explicit field, preparation or initial-record dependence of that valuation is separate and must still be differentiated.

This is a first-jet theorem, not erasure of every future field distinction: the original logical/field state is retained. It is also not equality of the two-recovery and unrecovered historical executions. We compare prospective programmes before execution, never rewrite an already registered tape.

For a cap N, the unresolved amplitude is `O(t^N)` and the corresponding complete amplitude jets through order N-1 have only scalar logical coefficients. No global inverse on the geometric field or new field equation is invoked.

## 3. Full actual 0/10 code: no free clock or work-output flag

Encode **each actual binary recorded decision** by the original direct0/return10 code, with lengths one and two, not only the outer port. Use bit zero for clean/success and one for nonclean/failure. A completed tree word consists of the port bit, the initial work-test bit, then every actually executed recovery-test bit. The actual leaf lengths are

    L_(b,0)=2+b,
    L_(b,k)=2+b+2k,           1<=k<=N,
    L_(b,?)=3+b+2N.                                    (9)

This is a finite prefix-free complete binary tree. Its original Golden reference masses are exactly `mu_omega=p^L_omega`, and

    sum_omega mu_omega=1,       sum_omega q_omega=1.      (10)

No new Kraft normalization or fitted branch reference is chosen. On a resolved leaf the retained work is blank. A full final work-address record on the unresolved leaves can be added; any bounded finite cost of that extra record is `O(t^(2N))`, and its entropy is `O(t^(2N) log|t|)` on a fixed finite carrier. It changes none of the following first sources. Protected older records remain separate and unchanged.

Directly summing EVERY actual coded leaf gives

    C_code,N(t)
      = 2+2p+2p^3(1-t)-p(1+t^2)t^(2N).                  (11)

Therefore

    C_code,N(0)=6p,
    D C_code,N|_Sigma = -2p^3 dt.                       (12)

All extra clean/retry flags have an even total cost in t. The number of actual inverse/forward recovery queries has expectation

    E N_recovery = p(1-t^(2N)).                         (13)

It is bounded by p, independently of the cap. At N=2 it is `p(1-t^4)`: the extra recovery work has **zero first and second t derivative** if the two directions are equally charged fixed words. For different fixed charges `c_-`, `c_+`, the exact recovery cost at cap two is

    p(1-t^2)(c_-+t^2 c_+),                             (14)

whose first derivative still vanishes at t=0. Fixed charges for the initial query, Golden gates, clean tests, and initial records retain their positive values; their first sources are zero only under that fixed-price hypothesis. If their actual costs have explicit field-dependent excesses, those derivatives remain in the parent residual. Nothing derives constant primitive costs from ActionProtocol's lower bound.

The uncapped expected recovery count equals p exactly for every |t|<1, but that infinite-runtime version is not needed: cap two already proves the complete first-source theorem, with at most three query calls in a run (one initial U and at most U*,U).

## 4. The full information term DOES NOT kill this signed source

### Literal pointer information and its positive whole-code KL

Let `H_phi(q)=-sum q log_phi q` be the information of the actual complete final classical code record in the specified pointer algebra. All eight leaves are included at N=2, including their zero probabilities on Sigma. The common normalization and code give the exact identity

    C_code,N - H_phi(q) = D_phi(q || mu) >= 0.             (15)

This is the actual Golden code/record identity; it is not an assertion that Book03 necessarily selects pointer Shannon Info.

At t=0 the nonzero probabilities are `p^4,p^2,p^3,p^3`. Only the two direct-clean leaves have nonzero first derivatives: `+2p^3,-2p^3`. The new retry probabilities are even and start at t^2 or higher; `t^2 log t^2` has zero first derivative. Thus, exactly,

    H_phi(q(0))=4-2p,
    D H_phi(q)|_Sigma=+2p^3 dt,
    [C_code,N-H_phi(q)](0)=4p^3,
    D[C_code,N-H_phi(q)]|_Sigma = -4p^3 dt != 0.         (16)

The complete pointer Info therefore **doubles** the known nonzero port-cost first coefficient; it does not invent a competing tensor, erase the mark, or require an information floor. The additional recorded recovery is precisely what makes this statement about the whole apparatus, not one discarded-work marginal.

No automatic C2 claim is made for (15): the second-recovery probability is proportional to t^2, so pointer entropy has the familiar logarithmic second-derivative issue. The all40 consumer needs the C1 source, which is what (16) proves.

### Coherent information algebra, separately scoped

If all branch registrations are implemented coherently and the full apparatus record is retained without external dephasing, the resolved output factors into a scalar tape state times the original logical state. Only the unresolved branch can entangle the new record with the source. For its total probability `delta_N=p(1-t^2)t^(2N)`, the largest eigenvalue of the full record marginal is at least `1-delta_N`. On the finite record carrier,

    S_record <= h_2(delta_N)+delta_N log(d_record-1).      (17)

Consequently `S_record=O(t^(2N) log|t|)` and `D S_record|_Sigma=0`. For cap two the actual entropy is `O(t^4 log|t|)`; this is a new instrument with a higher-order rank birth, not an upgrade of the previous unmodified flag entropy theorem. The complete coherent candidate therefore has

    D[C_code,N-S_record/log(phi)]|_Sigma=-2p^3 dt.        (18)

The two information algebras are not the same physical model. Both are computed, and both give a nonzero constant multiple of the **same** source dt, with no logical-input preparation residual. Which algebra is Book03 Info remains a physical binding question.

## 5. Exact use of the existing geometric and matter results

The owned full-carrier scalar reporter has

    t_h = -(8 sigma_c / D_h) sum_(z,r<s) a_(nu,rs),
    t_h|_Sigma=0,
    dt_h|_Sigma=-(8 sigma_c nu^2 h^2/D_h) d sum_z fhat_z.

Here `sigma_c` is the owned fixed Golden contraction, not the material amplitude used in the earlier paid-source residual. These are original CAR/Lorentz operator identities, including the whole ambient sixteen coframe and twenty-four link variations.

Applying (12), (16) and (18), and the already supplied number `M_h=D_h/16` of sequential reports, gives respectively

    d C_complete_code,h|_Sigma
      = p^3 sigma_c nu^2 h^2 d sum_z fhat_z,
    d(C_complete_code,h-H_pointer/ell)|_Sigma
      = 2p^3 sigma_c nu^2 h^2 d sum_z fhat_z,             (19)
    d(C_complete_code,h-S_coherent/ell)|_Sigma
      = p^3 sigma_c nu^2 h^2 d sum_z fhat_z,
    ell=log(phi).

The first is precisely the previous reporting coefficient with its actual clean/recovery record now paid. All intermediate-state constraints can use the existing causal adjoint elimination, not be independently freely re-prepared. OldRIGHT/source state is retained at every prefix as specified in §1. Sequential reports retain previous completed histories as untouched references.

For any already supplied scalar source amplitude with jet `dt=a_h dF+b_h dQ`, the same theorem multiplies both slots by one constant. Applying the same coding/information convention to both genuinely supplied slots therefore preserves their ratio. **This does not derive `b_h/a_h=lambda_-(2^-20)` or authorize choosing such an amplitude by fitting to Einstein.** The matter operand and its actual relative coefficient still need their native source/admission map. The existing all40+2 theorem is consumed when those maps and the remainder are proved, not before.

### Why this is progress beyond the previous material residual

The old material-positive `n p epsilon Delta` port instrument is not altered and its exact parity obstruction remains. The new result applies to the other existing CAR source reporter. It proves a way for its known nonzero geometric signal to survive **actual completion of the recorded execution and explicit information accounting**, without a spurious data/preparation force from leftover reversible work.

Thus one need not require a unique microscopic entropy formula before applying the geometric theorem: two precisely stated record-information choices already have the same equation-level source class on this completed programme. A full physical conclusion still requires the actual absolute price of its query/controller and the identity of its retained information algebra. Not every unspecified extra term is a function of this report, and arbitrary field-dependent work cannot be dropped.

## 6. Remaining physical gate, now stated without a fabricated counterterm

Let `W_actual` collect only the genuinely remaining costs/gains not included in the literal code and chosen recorded information above: elementary query construction, field-dependent price excess, initial work/observer/preparation, raw common amplitude normalizer, protected past and whatever Book03 additionally charges. It is determined by the admitted process, not selected to cancel the answer.

The new contribution reduces the same-programme comparison to

    dS_full|_Sigma = kappa dt + dW_actual|_Sigma,          (20)

where kappa is now explicitly nonzero for either actual candidate information algebra above. Within the fixed-price query interface, the added restoration clocks and every explicit code flag are already accounted for and contribute no independent first source. To consume the all40+matter theorem, the **actual** remaining term and matter coefficient must meet its existing interface, or a controlled equation transport must be proved.

This is a conditional positive source compiler and a concrete replacement of the reporter's work/information/preparation placeholder. It is not a proof of global prospective D_min optimality, compulsory operation admission, complete Book03 valuation, or physical GR. Source equivalence implies stationarity under its hypotheses, not a global minimum. `GR_closed=false` and raw216 remains separate.

## 7. Reproduction and hostile controls

`check_clean_scalar_source.py` checks the complete probabilities and Golden Kraft identity exactly in Q(sqrt(5))[t] at caps 1,2,3,5. A non-Hermitian block unitary with different left/right work frames verifies (2) and two-step amplitude cleanup without an involution assumption. No eigenvalue-floor entropy approximation is used in the exact first-source proof.

The numerical positive control uses the actual null basis, all16 original CAR creators/exterior grades, the inverse-leg bilinear and the same nonzero null-plaquette coefficients as the preceding representative `(-.00122444268454558,-.00062444268454558)`. A genuine opposite-null link variation generates its source. An actual 256-Pauli coherent scalarization and complete 32-dimensional Julia query form an8192-dimensional work/query space, not a scalar angle put into a test after the fact. All final amplitudes, including nonclean outputs, are propagated through U,U*,U. The logical CAR16 tensor an untouched spectator8 provides a128-column oldRIGHT Gram control; it is NOT a reproduction of the full physical site's selected reference128 preparation.

Numerical results (author replay, not interval acceptance):

    dt/dtheta = .00383152252539747,
    d C_code = -.00180899954682623,
    d H_pointer,phi = +.00180899954793645,
    d(C_code-H_pointer,phi) = -.00361799909476268.

The complete amplitude-jet error is about `1.31e-11`; maximum complete-record probability error `1.12e-16`; all128 conditional Gram error below `8.7e-19`. One recovery has a nonzero unresolved first-amplitude norm about `.0120486`; two remove it as predicted. These controls concern a real local CAR source operand. The whole-family/all40 application is the analytical composition with the already-owned source theorem, not a claim that this local replay re-solved the full lattice.

**Protected-history hostile control:** copying a fine work-address outcome into a separately protected record before reversing U destroys the required coherent interface. A two-dimensional entangled example has recovered logical/reference fidelity1/2 rather than1. The theorem therefore cannot be used to erase an already registered full128 tape or assume uncharged reversible access to arbitrary old records. This is an explicit admission boundary, not an omitted failure branch.

General inverse-query/measurement recovery is related to established quantum rewinding/repeat-until-success methods (Marriott–Watrous, `arXiv:cs/0506068`; Paetznick–Svore, `arXiv:1311.1074`). The result claimed here is the exact D0-Golden finite first-jet completion, its literal whole-code Cost–Info source, protected-history boundary, and consumption of the existing geometric reporter—not invention of those general methods.

Evidence is the mathematical derivation above, exact algebra, numerical full-work control and author receipt. The script hash and environment are saved in `receipt.json`. Independent scientific acceptance and Lean formalization are not claimed. No shared registry, BOOK, claim, workflow or lifecycle is promoted.
