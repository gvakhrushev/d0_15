# Finite native age-source transfer and ambient gain cotangent on the owned oldRIGHT stationary sector

22 October 2026. Mathematical continuation of the existing #334 source/Poisson owner. The full stationary fixed algebra, its Fredholm compatibility criterion, and the raw-terminal-CQ uniform-RIGHT solution were ALREADY proved in `A4D_ORIGINAL_OLDRIGHT_ARCHIVE_FREDHOLM_INFORMATION_AND_TWO_STAGE_GATE_2026_10_22.md`, §§3-4, Git blob `c2e897caa3416694c71bc6ddf1c3942f76e856ff`, present in pinned head `9239b31ec81092408ed1a5289f1412c83206f720`. They are consumed here, not claimed anew.

The new substitutions are (i) the complete ambient tensor-log cancellation for the entropy-GAIN convention, including arbitrary correlated joint input variations, and (ii) the exact finite AGE-clock conditional-to-input-gain boundary coboundary, centered adjoint transfer, and full source equality on the SAME actual finite native instrument (§6). The fixed-gap large-cap corollary retains the real invariant projector. No compulsory Book03 information convention or free preparation is selected.

## 1. Exact hypotheses and parent

Let DATA have dimension d and let the unchanged oldRIGHT spectator have dimension r. The original DATA channel Phi_y is CPTP, with a faithful stationary density rho_y and strict mixing on the trace-zero matrix space, as already assumed/proved on the parent native chart. Put Psi_y=Phi_y tensor id_R. No mixing of Psi on the entire trace-zero joint space is asserted.

Let F_y be the **complete actual finite stopped instrument channel** from DATA to the direct-sum fine-pointer plus conditional DATA output: F_y(X)=direct_sum_gamma L_gamma X L_gamma^dagger. Every abort, failed comparison and registered fine outcome is present, so sum_gamma L_gamma^dagger L_gamma=I. More general CPTP output channels obey the same tensor identities. Fixed support/smoothness is sufficient; the parent's separately justified amplitude C1 treatment can be used at allowed rank changes.

The genuine charge on this declared interface is spectator blind: C_y=A_y tensor I_R, with A_y=sum_gamma c_gamma L_gamma^dagger L_gamma for the actual full leaf ledger. Extra price terms independent of the joint input may be carried unchanged. Any genuine additional RIGHT-dependent charge, moving cut or heat dependence is kept separately rather than discarded.

Write ell=ln(phi), natural von Neumann entropy S, and define two **different existing** information conventions:

    P_gain(y,Omega)=Tr[(A_y tensor I)Omega]
                     -[S((F_y tensor id)Omega)-S(Omega)]/ell,
    P_CQ(y,Omega)=Tr[(A_y tensor I)Omega]
                     -S((F_y tensor id)Omega)/ell.

The stationary-input constraint is the same conditional admission as in the parent: Psi_y(Omega)=Omega and Tr Omega=1. We neither derive that physical constraint here nor replace a paid finite preparation by it.

## 2. Reused parent: complete fixed algebra and Fredholm compatibility

The following statements and their consequences are the existing oldRIGHT owner, §§3-4. The short proof is retained only to make this application self-contained. The exact stationary states are

    Fix(Psi) intersect states = {rho tensor omega: omega a RIGHT state}.

Proof: expand any stationary joint matrix in RIGHT matrix units, Omega=sum_ij X_ij tensor |i><j|. Each Phi(X_ij)=X_ij. Strict DATA mixing gives X_ij=a_ij rho, hence Omega=rho tensor omega. Positivity and trace give omega a state. The converse is immediate. This is a result on the entire joint matrix space, not a product ansatz.

The stationary and dual projections are

    Pi(X)=rho tensor Tr_D X,
    Pi*(M)=I_D tensor M_R,
    M_R=Tr_D[(rho tensor I_R)M].

All r^2 invariant observable modes I_D tensor B_R remain. Pi* is a conditional expectation onto this algebra. The correct centered Green operator is

    G_R=(I-Psi*+Pi*)^{-1}(I-Pi*)
       =sum_{n>=0}[(Phi*)^n-Pi_D*] tensor id_R,
    Pi_D*(A)=Tr(rho A) I_D.

Strict DATA mixing proves convergence. For any Hermitian score M,

    Y=G_R M,
    (I-Psi*)Y=M-Pi*M,
    Pi*Y=0.

Thus the full independent input equation with only trace normalization,

    M+(Psi*-I)Y+lambda I=0,

is solvable **if and only if** M_R is scalar. If M_R=m I_R, take lambda=-m and the unique centered Y above. A fixed nonuniform RIGHT marginal instead carries its true matrix Lagrange multiplier; it must not be silently treated as freely varied.

For d=16,r=128 this retains exactly r^2=16,384 invariant observable modes. The Hermitian joint space has (dr)^2=4,194,304 real dimensions; the range of I-Psi* has (d^2-1)r^2=4,177,920. These are algebraic dimension consequences, not a claimed multi-million-variable numerical replay.

## 3. The complete ambient gain cotangent factors: correlated variations included

Take any faithful omega and the actual stationary Omega=rho tensor omega. Let Gamma=F(rho). The full output is Gamma tensor omega, where the tensor is understood blockwise on the complete retained CQ output. On its support,

    log(Gamma tensor omega)=log Gamma tensor I + I tensor log omega,
    log(rho tensor omega)=log rho tensor I + I tensor log omega.

Since F* is unital on that output support, the complete ambient gain score is exactly

    M_gain,DR=M_gain,D tensor I_R,
    M_gain,D=A+[F*(log Gamma)-log rho]/ell.               (1)

The two log(omega) terms cancel before any tangent restriction. Therefore (1) pairs correctly with **every arbitrary Hermitian correlated joint perturbation** delta Omega, not only delta rho tensor omega or rho tensor delta omega. This is stronger than observing cancellation of S(omega) on product paths.

Its invariant projection is scalar:

    Pi*(M_gain,DR)=Tr(rho M_gain,D) I_DR.

Consequently the entire joint independent-input Euler equation closes with

    Y_DR=Y_D tensor I_R,
    (I-Phi*)Y_D=M_gain,D-Tr(rho M_gain,D)I_D,
    Tr(rho Y_D)=0,
    lambda=-Tr(rho M_gain,D).                            (2)

The formerly missing r^2-1 nonscalar RIGHT compatibility conditions vanish identically for the declared gain convention. No RIGHT state is frozen to make this happen. All faithful omega are flat stationary directions of this price; genuine RIGHT-dependent upstream charges may lift them.

## 4. Reused raw-CQ solution, with its ambient comparison to gain

The uniform-RIGHT solution and positive Hessian below are already owned; the ambient formula makes the contrast with the gain calculation explicit. For P_CQ, use the exact ambient Hermitian score (including the entropy trace derivative). The exact full score is

    M_CQ,DR=M_CQ,D tensor I_R + I_D tensor log(omega)/ell,
    M_CQ,D=A+[F*(log Gamma)+I_D]/ell.                    (3)

Thus free RIGHT variation is compatible if and only if log omega is scalar, i.e.

    omega=I_R/r.                                       (4)

This is the unique faithful stationary RIGHT state for this entropy convention. It is fixed by its own independent Euler equation, not posited as a preparation. At (4), the same centered lift uses Y_DR=Y_D tensor I_R with the DATA score M_CQ,D and

    lambda=-Tr(rho M_CQ,D)+(ln r)/ell.

The complete source-valued reduction is

    P_gain(y,rho_y tensor omega)=P_gain,D(y,rho_y),
    P_CQ(y,rho_y tensor I/r)=P_CQ,D(y,rho_y)-(ln r)/ell.  (5)

All field jets coincide with their DATA counterparts on these admitted sections. On the constrained RIGHT tangent at I/r, the raw-CQ second form is

    D^2_RIGHT P_CQ[delta omega,delta omega]
       =(r/ell)Tr[(delta omega)^2],                     (6)

strictly positive for any nonzero traceless Hermitian delta omega. Mixed field/RIGHT derivatives vanish. For the gain convention, the RIGHT factor is exactly flat to all orders. Ambient correlation Hessians need not vanish; they belong to the constrained Lagrange system and are not erased.

## 5. Full field source: the same parent Poisson reaction, no false factor 128

Along the stationary section and the declared spectator-blind ledger,

    d_y P = (partial_y P)_Omega
            +Tr_DR[Y_DR ((d_y Phi) tensor id)(rho tensor omega)]
          = (partial_y P_D)_rho+Tr_D[Y_D (d_y Phi)(rho)]. (7)

Every derivative of rho_y is retained through the same native DATA adjoint. There is no r multiplier in this normalized information price: Tr omega=1. An actual unnormalized Book heat or determinant may separately carry its genuine r-fold trace multiplicity and is unchanged by (7).

Thus the existing parent DATA first-source and Hessian formulas lift exactly to the full stationary DATA×oldRIGHT gain interface; for raw CQ they lift after (4), with only the explicit constant in (5). The new gain calculation satisfies the already-owned oldRIGHT compatibility criterion; the raw-CQ solution is consumed as a comparison.

## 6. Exact finite native age/oldRIGHT weld: conditional clock entropy versus true input gain

This section consumes the genuinely generated K-tick age instrument from `AGE_CLOCK_SOURCE.md`. It also applies to the complete fine K-tick output, with every fine entropy remainder retained. Let F_K be the actual retained-output channel, and its terminal-DATA marginal be Phi^K. With oldRIGHT included set Psi=Phi tensor id and F_K,DR=F_K tensor id. This is a finite existing execution, not a reset or an iid replacement.

For the same complete actual mean cost C(y,Omega), distinguish

    P_cond=C-[S(F_K,DR Omega)-S(Psi^K Omega)]/ell,
    P_gain=C-[S(F_K,DR Omega)-S(Omega)]/ell.

P_cond measures the retained record entropy conditional on terminal DATA×RIGHT. P_gain measures the actual whole gain relative to the initial DATA×RIGHT. Their exact off-section difference is

    P_gain-P_cond=[S(Omega)-S(Psi^K Omega)]/ell.          (8)

On every true stationary input Psi Omega=Omega these scalar values agree identically, including all total field jets along the stationary section. But their independent input scores are different. At a faithful stationary Omega,

    M_gain-M_cond=[(Psi*)^K-I]log(Omega)/ell
                =-(I-Psi*) B_K,
    B_K=(1/ell)sum_{j=0}^{K-1}(Psi*)^j log(Omega).       (9)

This follows directly by differentiating (8), using trace preservation to cancel identity terms; finite telescoping proves the last equality. In particular a normal derivative obtained by differentiating terminal conditional entropy cannot be used unchanged as the independent-input derivative of the true gain.

The entire difference lies in the range of I-Psi*, so it preserves the RIGHT invariant-algebra compatibility condition. The exact **centered** multiplier transfer is

    Y_gain=Y_cond-B_K+Pi*(B_K).                          (10)

For Omega=rho tensor omega the apparent RIGHT term in B_K is (K/ell) I tensor log(omega), which is removed by Pi*. Thus (10) has exactly the DATA correction tensor I_R, with ALL RIGHT modes present, not frozen.

The correction to the field derivative at **fixed independent Omega** is equally explicit. Put V=(d_y Psi)(Omega). Differentiating the finite actual power gives

    (d_y Psi^K)(Omega)=sum_{j=0}^{K-1}Psi^j(V),
    f_gain-f_cond=Tr[B_K V].                            (11)

Here stationary Psi^j(Omega)=Omega has been used only at the base. The true corrected fields therefore coincide:

    f_gain+Tr[Y_gain V]
      =f_cond+Tr[Y_cond V].                             (12)

The final extra pairing Tr[Pi*(B_K)V] vanishes because a derivative of the DATA trace-preserving channel has zero DATA partial trace. Equations (9)-(12) prove the whole source equality without discarding an independent preparation reaction. Function identity (8) also yields equality of all stationary-section Hessians wherever they exist; ambient Hessians retain the differentiated boundary defect.

**Fixed-gap large-cap control.** The centered transfer has the exact form

    B_K-Pi*B_K=(1/ell)sum_{j=0}^{K-1}[(Psi*)^j-Pi*]log(Omega).

On a fixed native chart with an actually proved operator estimate ||(Psi*)^j-Pi*||<=C eta^j, eta<1, put L_c=log(Omega)-Pi*log(Omega). Then

    ||B_K-Pi*B_K|| <= C ||L_c||/[ell(1-eta)],
    ||(B_K-Pi*B_K)-(1/ell)G_R log(Omega)||
       <= C eta^K ||L_c||/[ell(1-eta)].

Thus keeping the full invariant projector removes the otherwise spurious linear-in-K RIGHT piece. At the stationary product, L_c=[log(rho)-Tr(rho log(rho))I_D] tensor I_R exactly. This is fixed-gap control of the genuine transfer; no uniformity across physical mesh refinements or unpaid infinite preparation is asserted.

For the age channel specifically, the published age score is

    D_Omega{S(F_age,K Omega)-S(Psi^K Omega)}
      =-F_age,K*log(Gamma_age,K)+(Psi*)^Klog(Omega)

at stationarity. The true gain-information score must instead end in +log(Omega). In PRICE units this is exactly (9). The complete fine-record remainder may be added unchanged to both sides: it changes M_cond and Y_cond but not the universal correction B_K, so this weld does not assume that fine|age entropy or paid controller/clock charges vanish.

A separate finite diagnostic `check_age_spectator_poisson_weld.py` verifies 54 controls at caps 1,2,3,6 on the parent's noncommuting rational two-Kraus DATA2×RIGHT2 example. It enumerates all actual fixed-window Kraus words, groups them by trailing-blank age, retains the complete cap event, and uses the declared parent per-bit charge 1+bit. Full joint input Euler residuals are below 5e-15; corrected fixed-input plus Poisson field sources agree within 2.5e-10 and independently differentiated stationary curves within 6.9e-10. Keeping the unshifted conditional adjoint in the true gain price creates a nonzero source error about 0.5165236963. These are floating controls of the proved finite identities, not an original full128 replay or a physical Info selection.

## 7. Arbitrary correlations: the exact correction before stationary preparation

For an arbitrary joint input Omega with marginals rho,omega, no factorization is assumed. A local complete future channel F leaves omega invariant. Its total mutual-information loss obeys the exact entropy identity

    [S((F tensor id)Omega)-S(Omega)]-[S(F rho)-S(rho)]
       =I(D:R)_Omega-I(output:R)_(F tensor id)Omega.     (13)

Hence the gain price differs from the marginal DATA gain price by minus (13)/ell. Data processing makes this value nonnegative as an information loss, but does not provide a derivative sign. In particular the correlation-source term cannot be dropped before the input has actually reached the admitted product stationary section. This identity retains every measured pointer and conditional DATA mode in 'output'.

For a real L-round prefix, Omega_L=(Phi^L tensor id)Omega_0,

    Omega_L-rho tensor omega_0=[(Phi^L-Pi_D) tensor id]Omega_0. (14)

The convergence in (14) does not cancel the paid prefix ledger or its stored-record entropy. Those must remain in the existing finite adjoint recursion/full expanded history price. The theorem does not bound them by zero and makes no mesh-uniform estimate.

## 8. Why the ambient cotangent calculation is necessary

Equality of a price on product states is not enough to prove the factorization (1). Let a genuine extra joint term be B(Omega)=Tr[Omega (X_D tensor X_R)], with Tr(rho X_D)=0 and omega=I/r, Tr X_R=0. Its value on this stationary product section is zero, while its ambient score X_D tensor X_R is nonzero on correlated variations. In the old nonunital rational two-Kraus control, Phi*(X_D)=(24/25)X_D, so its exact extra joint Poisson response is 25 X_D tensor X_R. A DATA-only multiplier would miss it. The gain/CQ tensor-log calculation above rules this term out only under the explicitly stated true spectator ledger; it does not rule it out in an uncomputed full Book cut.

A simpler invariant obstruction is an extra real RIGHT charge I_D tensor Z_R with Z_R nonscalar. Its projected score is itself, so no centered Poisson response can absorb it. The genuine RIGHT Euler must be solved or its selected marginal constrained. Both controls preserve the entire invariant algebra.

## 9. Precise acceptance and exclusions

New exact parent substitution: the ambient gain cotangent satisfies the previously owned invariant-algebra compatibility criterion, and the actual finite age instrument has the exact conditional-to-input-gain normal/source transfer in §6. The fixed algebra, Fredholm criterion, raw-CQ uniform-RIGHT solution and its Hessian are reused original results, not new discoveries in this packet.

Still required: actual stationary-input physical admission or a paid finite prefix with its full ledger; the real Book03 choice of Info/cut/Hodge/clock; actual field writer; any non-spectator RIGHT-dependent costs/cuts; the original full42 physical root and uniform refinement. A pure entangled purification of faithful mixed rho is not a fixed point of Phi tensor id and is outside this stationary section. No result here equates these two physically different inputs, declares a free reset, or promotes GR_closed.

Sources consumed: `A4D_ORIGINAL_OLDRIGHT_ARCHIVE_FREDHOLM_INFORMATION_AND_TWO_STAGE_GATE_2026_10_22.md`, §§3-4, blob `c2e897caa3416694c71bc6ddf1c3942f76e856ff`; #334 pinned head 9239b31ec81092408ed1a5289f1412c83206f720; `A4D_COMPLETE_NATIVE_FIRST_MATCH_ENTROPIC_POISSON_PREPARATION_AND_HESSIAN_2026_10_22.md`, §§2–4,6–7; `A4D_NATIVE_STOPPED_QUANTUM_PRICE_AND_SOURCE_2026_10_22.md`, §§2–6; `A4D_NATIVE_COMPLETE_SOURCE_REDUCTION_2026_10_22.md`, §4. The new proofs above are finite tensor/operator calculations; the owned strict native mixing hypothesis is consumed, not independently re-proved.
