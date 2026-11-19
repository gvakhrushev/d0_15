# Complete-archive compact Julia composition and refinement verification

Source snapshot: `0e4c9d6ca8b44574100338b04c27204cde7062dc`, existing scientific PR #334. Parent consumers: native_sector (actual composition and oldRIGHT preservation), constitutive (complete executed history cost), and gr_operational_realization (operational observability on refinement). This is a bounded composition of existing Julia and Golden17 owners, outside PR #386's foundation/transfer work.

The consumed original Julia instrument has C(U)=p Lambda(U), F(U)=sqrt(I-p² Lambda(U)^dagger Lambda(U)), p=(sqrt5-1)/2. The owner `A4D_OBSERVER_COMPLETE_CAR16_JULIA_CHOI_STAR_DENSITY_WELD_2026_10_20.md` §§5–6 states this native Golden version. On the observer's compact SO(3) subgroup, the complete CAR16 exterior operator V=Lambda(U) is unitary, so the TWO ACTUAL Kraus operators simplify exactly to

    K_G=p V,                 K_B=sqrt(p) I,
    g:=p²,                   g+p=1.

The failure branch is therefore a coherent identity on the actual input, including any entangled oldRIGHT/reference. This is a theorem about this specified instrument; the literal full128 L_k port instrument and a failed Bell programme teleportation are different instruments and do not inherit it.

## 1. Fixed horizon: all failure words contribute coherent signal

Apply this same instrument n times with distinct fresh flags and retain the entire chronological flag string s. Let k(s) be the number of G symbols. The branch Kraus operator is

    K_s=p^k p^((n-k)/2) V^k.

Thus its probability is w_s=g^k p^(n-k), independent of V, the input, every compact field parameter and the oldRIGHT state. The normalized joint data/reference output is (V^k tensor I_R) rho (V^k tensor I_R)^dagger. EACH branch preserves the entire oldRIGHT reduced density exactly. The complete flag law sums to 1; no all-success selection occurs. K has the exact binomial law Bin(n,g).

The whole n-step channel with its flag register is

    E_n(rho)=sum_s w_s |s><s| tensor V^k rho V^(-k).

For a smooth compact family V(y), all derivatives of w_s vanish; the first and higher field derivatives of each normalized output are the derivatives of the actual V(y)^k. This is not equality of complete clock histories with a single V^k gate: the n actual steps and full chronological tape remain in the execution.

For the original F/R Golden code, B has probability p and code length 1, G probability p² and code length 2. The complete raw tape has exact expected code length and Golden entropy

    E L(s)=H_phi(s)=n[p+2p²]=n(2-p).

They have zero compact-field derivative. Actual Book/HJR, controller, preparation, clock and physical work are separate; a field-dependent per-step price must be retained. If each actual step costs c_j(y), its source is D sum_j c_j(y), not zero merely because the flag probabilities are constant.

## 2. Exact original Golden17 overlap and Fisher after coherent accumulation

Use the original J23 compact subgroup V(theta)=Lambda(exp(theta J23)), followed by ONE final complete original Golden17 readout. A branch with k good flags supplies the original q17(k theta). Its final 1/4096 Bell factor (or a genuinely implemented fixed smaller rate) is paid once per complete block; this does not repeat the generally destructive Bell comparison for free.

The input/process/readout chain is constructive: prepare the common grade-one Choi state Omega4=vec(I4)/2 once. Compact accumulation gives chi_(P^k)=vec(P^k)/2 on the branch with k good flags. With u=vec(I4)/2, v_a=vec(G_a)/sqrt(2), the seven vectors u,v_a are orthonormal. The SAME fixed final effects E_(a,±)=kappa|u±v_a><u±v_a| yield the twelve marks. Complete with E_GGrest=24 kappa I−sum E_marks, E_GB=E_BG=gp/4096 I, E_BB=p²/4096 I, E_Bellfail=(4095/4096)I. All seventeen effects are positive and sum to I. The GG-rest eigenvalues are 12,22,24 times kappa. Thus no field-dependent programme for P^k is used in this final readout. Full derivation and exact certificate: fixed_readout.md and check_fixed_readout.py. This proves equality of the full seventeen-label law; a future test of postmeasurement quantum states would require the corresponding instrument extension. Preparation, fixed POVM and Julia realization retain their actual physical admission and prices.

Set kappa=p^4/(24*4096). On the original positive square-root chart m>|sin(t)/sqrt2|, m=(1+cos t)/2, the signed marks are

    q_±(t)=kappa (m ± sin(t)/sqrt2)^2.

All other 15 outcomes, including failure, are retained and are reversal even. For |t| in this chart,

    B(q(t),q(-t))=1-2 kappa sin²t,
    I_q(0)=4 kappa.

Here B is the full Bhattacharyya overlap and I is Fisher for parameter theta. The complete flag+final-output distributions Q_±(s,r)=w_s q_r(±k theta) have EXACT overlap

    B_n(theta)
      =1-2 kappa E[sin²(K theta)]
      =1-kappa[1-Re(p+g exp(2i theta))^n],

provided n|theta| stays within the same positive chart. Their exact flat Fisher is

    I_n(0)=4 kappa E[K²]
          =4 kappa [n²g²+ng(1-g)].

By comparison, n separately read out one-step Julia experiments supply only 4 kappa n g. The exact gain is 1+(n-1)g. This compares full recorded probability laws, with no unobserved success condition and no discarded failure records.

## 3. Refinement exponent: h^-2 instead of h^-4

For separated smooth compact hypotheses theta_h=±h²F, with 0<F_min<=F<=F_max, choose n_h=floor(c/h²) and 0<c F_max below the common positive chart boundary. Then

    (p+g exp(2i h²F))^n_h -> exp(2i gcF),
    B_nh(theta_h) -> 1-2 kappa sin²(gcF).

Choose c also so gcF lies in a compact subinterval of (0,pi). The limiting overlap is bounded strictly below 1 uniformly over the stated F interval. A finite, h-independent number M of independently prepared COMPLETE blocks achieves any fixed equal-prior Bayes error epsilon: the exact elementary bound Err_M<=B_n^M/2 gives M>=log(2epsilon)/log(B_n). Therefore the actual Julia-call count is M n_h=O(h^-2), with all flags and failures retained. The constant M can be large because the chosen Golden17/Bell readout is weak; no small laboratory cost is asserted.

In contrast, independently reading q17(theta_h) requires Omega(h^-4) records at fixed error: B_1=1-2 kappa h^4 F²+O(h^8) and Err_M >= [1-sqrt(1-B_1^(2M))]/2. Independent one-step Julia before each readout only adds the factor g and preserves that exponent. This is an operational query bound, not a derivation of gravitational action normalization from a query count.

If physically implemented final preparation contributes a fixed, field-independent success factor r>0 and a common theta-independent failure law, replace kappa by r*kappa. It changes the constant, not the exponent. If r=r_h vanishes with refinement, or programmes/reset costs grow, those actual factors enter the resource bound and cannot be ignored.

## 4. Finite-cap completion of an arbitrary ordered compact word

The fixed-n construction needs no adaptive feedback. A stronger optional controller theorem applies if the existing native controller may read fresh flags: for any ordered compact word V_m...V_1, repeat the current Julia letter until G, then advance. After m good flags every completed branch has Kraus scalar times EXACT V_m...V_1, regardless of failure positions. Its full negative-binomial attempt count satisfies E T=m/g. All outputs including oldRIGHT retain the exact state, chronological tape and clock.

Use a finite cap N and retain every cap-failure branch. Completion probability is

    Q_N=Pr[Bin(N,g)>=m],
    E[min(T,N)]=sum_(t=0)^(N-1) Pr[Bin(t,g)<m] <= m/g.

Both are independent of every compact field. Conditional on the explicit completed flag, the desired ordered channel and ALL its field derivatives are exact. The complete channel still includes the incomplete-prefix outcomes; none is discarded or assigned zero work. For N>=ceil((2m+8 log(1/delta))/g), the elementary Chernoff bound gives 1-Q_N<=delta. There is no infinite-time admission assumption.

This removes the exponential all-success penalty for a composed compact Julia word. It does not equate complete execution records or prices to a single direct instrument: the relevant accepted primitive-jet composition can consume the explicit completed-branch map, its field-independent success factor, and the separately retained work/clock terms.

## 5. Decisive hostile controls and exact scope

1. The result fails for a generic proper-Lorentz boost: Lambda(U)^dagger Lambda(U) is not I, so F(U) is not a scalar identity, branch probabilities move and each conditional branch can change the oldRIGHT Gram. The scalar-failure hypothesis must be checked on the SAME observer metric and fields. Observer changes that make a fixed coordinate rotation noncompact relative to that metric are not covered.
2. Postselecting only G^n unnecessarily has probability g^n. It is not the implemented complete-archive construction above.
3. The generally destructive Bell-effect failure is never treated as a harmless retry. Accumulation precedes one final Golden17 comparison.
4. A whole-field-dependent Choi programme that implements each Julia letter must actually be supplied if that is the available hardware realization. Existence of the Julia matrix is not proof G0 prepares that programme at bounded cost.
5. This supplies a concrete composition and verification resource theorem on an already specified compact instrument, with exact oldRIGHT preservation. It does not select the compulsory Einstein pretrace price, the noncompact boost sector, matter Ward or GR refinement roots.

Novel use in the parent: the prior direct-versus-sequential Julia success discrepancy does not imply an unavoidable exponential verification obstruction on the compact unitary sector. Complete retained failures are reusable coherent identity steps; their correct composition yields a positive, finite-cap, oldRIGHT-preserving programme and an h^-2 verification resource law. The missing physical map is now the admission and charged implementation of this specified compact Julia letter, not an invented perfect continuous oracle or another detector family.

## 6. The same exact weighted execution has a deterministic coherent limit without argmin

Let delta=h², V_h(y)=exp(delta X(y)), where X(y) is the skew-adjoint CAR16 generator of an admitted compact loop, and n_h=floor(tau/delta). Keep the complete flags. Its reduced data/reference channel is EXACTLY

    T_h=(p Id+g Ad_(exp(delta X)))^n_h
       =E[exp(K delta L_X)],       L_X(A)=[X,A].

There is no postulated minimizing path. The distribution and generator are those of the existing weighted instrument. K has the same native Bin(n_h,g) law, so its registered operational time obeys

    E(K delta)=g tau+O(delta),
    Var(K delta)=n_h g(1-g)delta² <=tau g(1-g)delta.

Taylor expand F(t)=exp(t L_X) around mu=n_h g delta. The first-order term cancels EXACTLY under expectation. Every F(t) is a unitary channel, so its diamond norm is 1 and ||F''(t)||_diamond<=||L_X||_diamond². Consequently

    ||T_h-Ad_(exp(g tau X))||_diamond
      <= (1/2)n_h g(1-g)delta² ||L_X||_diamond²
         +g delta ||L_X||_diamond
      =O(h²).

This holds with arbitrary reference entanglement. If X(y) is C² with bounded jets on the declared compact parameter chart, the SAME C² source estimate follows by differentiating F(t,y) before this time-Taylor expansion. Explicit sufficient bounds for ||D_y^j partial_t² F||, j=0,1,2 and t<=tau, putting M_j=sup||D_y^j L_X||, are

    C0=M0²,
    C1=2M0 M1+tau M0² M1,
    C2=2M1²+2M0 M2+4tau M0 M1²+M0²(tau M2+tau² M1²).

The mean-versus-tau floor term has the corresponding bounded first-time-derivative jet. These are finite operator estimates, not an interchange of an uncontrolled refinement limit.

The full retained-record Stinespring map is

    W_h psi=sum_s sqrt(w_s)|s> tensor exp(k(s)delta X)psi.

Let |a_h>=sum_s sqrt(w_s)|s>. Then

    ||W_h-|a_h> tensor exp(g tau X)||
      <=||X|| sqrt[n_h g(1-g)delta²+(n_h g delta-g tau)²]
      =O(h).

Thus the ORIGINAL chronological tape remains present while the data evolution asymptotically decouples from its variable delay. No history is erased and its entropy/code cost grows as n_h(2-p). This is a concrete conditional native continuation law from weighted coherent execution, without the still-unproved strict global prospective argmin premise.

**Source-normalization qualification.** An O(h²) channel error by itself is not negligible after an h^-2 source amplification. Use the exact success-count construction below if that normalization is required. Neither bound equates a channel generator to Einstein's full selected action.

## 7. Success-count time gives exponentially accurate complete-channel recovery

For m_h=floor(tau/h²), repeat until m_h successes with a finite cap N_h=ceil(2m_h/g), retaining all incomplete outputs. Here tau, m_h and N_h are fixed under the field variation y; X(y) and the observer Hilbert metric are identified on one fixed Hilbert fiber. EVERY completed branch is EXACTLY exp(m_h h² X). The failure probability epsilon_h obeys

    epsilon_h=Pr[Bin(N_h,g)<m_h]<=exp(-m_h/4).

On the actual grid time tau_h=m_h h², there is no O(h²) approximation in the completed branch. The unconditioned data channel differs from Ad_exp(tau_h X) in diamond norm by at most 2epsilon_h. More strongly, let A_h be the ENTIRE actual finite stopped flag law (including every failed cap prefix). The classical full-flag/data channel differs from A_h tensor Ad_exp(tau_h X) by at most 2epsilon_h: all completed blocks agree exactly, and the total probability of remaining blocks is epsilon_h. Complete retained coherent Stinespring error is at most 2sqrt(epsilon_h) against the same coherent flag amplitudes tensored with the target evolution; no flag is removed. The distinct epsilon_h and sqrt(epsilon_h) bounds must not be conflated.

Because every failed branch is a compact prefix exp(k h²X), 0<=k<m_h, and all branch probabilities are independent of y, bounded C² field jets give ||D_y^j(channel-target)||<=C_j epsilon_h, j<=2, for BOTH the data and full classical-flag/data channels. The coherent Stinespring jets are instead bounded by 2U_j sqrt(epsilon_h), where U_j uniformly bounds the j-th field jet of every prefix unitary; the classical channel estimate is 2V_j epsilon_h with the corresponding prefix-channel jet bound V_j. Thus any fixed polynomial source rescaling, INCLUDING h^-2, preserves convergence to zero. The finite cap and its failed records are real paid execution. For the unbounded stopping distribution (used only to upper-bound the finite cap),

    E T=m_h/g,
    E Golden raw-code length=E(T+m_h)=m_h(1/g+1).

The geometric success-count time tau_h is distinct from the actual variable attempt-clock time T h², which remains explicitly present in the archive and price. The finite cap costs no more expected attempts; its exact raw code is T+K and bounded stopping gives E(T+K)=(1+g)E T. This is a linear expected execution/coding budget in m_h, not an exponentially rare g^m_h postselection. Actual additional programme/preparation/clock work still enters its own selected price.

A finite controller that counts fresh G flags is an explicit implementation hypothesis. It can be tested against the existing stored-program/clock controllers; this theorem does not obtain a free controller from abstract matrix existence. Once admitted, it supplies the exact compact continuation and source composition rather than another assumed-optimality consequence.

## Independent hostile review

The source_equivalence reviewer independently checked the exact scalar-failure composition, finite-cap complete-law comparison, C² source estimates and the numerical/exact checker; all passed. The structural_synthesis reviewer independently supplied and exactly checked the fixed complete POVM used above. The latter construction has a supplied fresh rank-four Choi reference; it does not create an arbitrary oldRIGHT128 preparation. Scalar-failure preservation applies separately to any admitted supplied joint-reference state.
