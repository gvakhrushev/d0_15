# Actual full128 normalization, the true complementary Book source, and the primary test

21 October 2026. Existing Draft #334; task EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, constitutive/native-programme-v1. Input scientific snapshot: `5edac80c86c17014fc83e0aa608e192f43c1fdba`. Research calculation and correction of the author's recent normalization notes. `GR_closed=false`.

## 1. Result, consumer and correction

The preceding authored source-identifiability notes inferred too much from a scalar ambiguity in an UNNORMALIZED amplitude sum. Their determinant formula for a separately postulated `F_a=a F_0` is algebraically correct, but that scaling was not derived for the actual complementary Book operator. The original owner specifies

    A=i* U i,  F=i* U*(I-ii*) U i=I-A*A.

Scaling an amplitude does not scale this F. The older graph-ratio lemma determines scalar weight jets, not all physical source jets. An absolute scalar anchor is not necessary for a source invariant under scalar multiplication. Nor is it sufficient without the actual memory operators, active cut, heat map, preparation and their derivatives.

This calculation completes the normalization-to-source application on the specified original full128 instrument. It gives an exact finite, noncommuting operator normalizer, its chronological reconstruction, a root-free formula for the normalized complementary source, and all retained failure terms for an actual output attenuation. It then tests the unchanged HJR source on the already-owned primary nonvacuum family. The result is NOT a new GR closure: the primary preparation residual remains nonzero. A normalization convention cannot repair it.

The elementary isometry/polar identities below are standard finite linear algebra, not claimed as new general quantum-channel theory. The contribution is their explicit application to the existing D0 operators and correction of the prior proposed closure route. Stinespring context: Kretschmann, Schlingemann, Werner, arXiv:quant-ph/0605009. No theorem about continuity or physical admission is borrowed from that paper.

## 2. The actual retained execution has a fixed operator normalization

Let H be the original finite DATA space, and retain all oldRIGHT factors. One real round has 128 Kraus operators K_b,j, b=0,1 and j=0,...,63. With p=phi^-1, a=sqrt(p), the literal Walsh/Julia/Golden construction gives

    K_0,j=delta_j0 I-2p^2 N_j* A_native,
    K_1,j=-2ap N_j* A_native,
    sum_(b,j) K_b,j* K_b,j=I,
    B=K_0,0=I-2p^2 A_native^2=I-alpha Delta,
    E_1=sum_j K_1,j* K_1,j=4p^3 A_native^2=2p alpha Delta.

The original reporting charges are c_b=1+b. Every j and both ports remain.
For n fixed fresh rounds, K_omega is the chronological product and

    V_n=sum_omega |omega> tensor K_omega,
    V_n*V_n=I,    D_y(V_n*V_n)=0.                         (1)

The second equality includes all Kraus/defect/link derivatives. For a normalized preparation C with any retained oldRIGHT, Tr(C* V_n* V_n C)=1. Its total normalized-record log norm is zero, including preparation derivatives. It is NOT the heat trace Tr B^(2n), a selected blank probability, or the HJR action.

If an unnormalized vector is a(y)V_n C, normalizing it removes a. If it is asserted to be the same complete isometry before normalization, positivity of a and (1) force a=1. A free positive a cannot simultaneously be an arbitrary convention and an extra physical source of this unchanged execution.

## 3. The real cost mark gives a calculable OPERATOR, not a single scalar

For a supplied analytical cost mark t>=0 define

    C_omega=sum_{steps} c_b,
    W_n,t=sum_omega exp(-t C_omega/2)|omega> tensor K_omega,
    N_n,t=W_n,t* W_n,t.

This need not be an isometry. For the repeated original round,

    N_0,t=I,
    Phi_t*(X)=sum_(b,j) exp[-t(1+b)] K_b,j* X K_b,j,
    N_n,t=Phi_t*(N_(n-1),t).                             (2)

The recurrence is a sum over every actual history, not a successful-subensemble model. Its field derivative is computed by the full product rule:

    DN_n=sum w_b [DK* N_(n-1) K + K* DN_(n-1) K
                            +K* N_(n-1) DK],             (3)

for fixed charges and t. Moving t or real charges add their own Dw_b terms.
At t=0, N_n,0=I and DN_n,0=0. Also

    -partial_t N_n,t|_0 = sum_omega C_omega K_omega* K_omega
      =sum_(j=0)^(n-1) (Phi*)^j(I+E_1).                 (4)

This is the actual unconditioned reporting-cost effect. In particular

    N_1,t=e^-t [I+(e^-t-1)E_1].                          (5)

Whenever E_1 is nonscalar, no single input-independent scalar normalizes this marked map on every preparation. Since n<=C_omega<=2n,

    e^(-2nt) I <= N_n,t <= e^(-nt) I.                    (6)

Thus the finite inverse is well defined without a probability floor. No estimate uniform in increasing n or refinement is claimed.
For rho, the scalar success norm is s_t(rho)=Tr(rho N_n,t), with
Ds_t=Tr(rho DN_n,t)+Tr(N_n,t D rho). Neither term may be dropped.

## 4. Exact normalized Book determinant and its full source

Let i:H->E be the SAME specified active embedding in the retained output space. For any injective amplitude map W:H->E put

    N=W*W>0,  A=i*W,  G=A*A,
    Vhat=W N^-1/2,  Ahat=A N^-1/2,
    Fhat=I-Ahat* Ahat.

This defines a normalized isometry mathematically. It does not assert that the original hardware executes Vhat. With the actual spectator oldRIGHT multiplicity r_R=128 and fixed 0<z<1, Sylvester's determinant identity gives

    Q=(1-z)N+zG,
    Jhat=-r_R logdet Q+r_R logdet N.                     (7)

Indeed (1-z)I+z Ahat* Ahat=N^-1/2 Q N^-1/2. No commutation is used. For an arbitrary first variation,

    DJhat=r_R Tr[N^-1 DN
       -Q^-1{(1-z)DN+z DG+(G-N)Dz}],
    DG=(DA)* A+A* DA.                                   (8)

This is the complete complementary-feedback source on this specified normalized map. For fixed z it retains BOTH normalizer and active-corner jets. Moving i contributes to DA=(Di)*W+i*DW; no fixed-cut conclusion applies when those terms are absent from the model.

### A root-free geometric form and exact normalization invariance

Define the projector onto the range of the actual amplitude map:

    Pi_W=W N^-1 W*,
    Jhat=-r_R logdet[(1-z)I+z i*Pi_W i].                 (9)

The equality follows because Ahat*Ahat and Ahat Ahat* have the same determinant polynomial. For fixed i,

    DPi_W=(I-Pi_W) DW N^-1 W*
                 +W N^-1(DW)*(I-Pi_W).                 (10)

Consequently only the change of the output subspace relative to the actual active cut contributes. Any change DW=W X is annihilated. More strongly, for every invertible, possibly field-dependent input-coordinate change L(y),

    Pi_(WL)=Pi_W,    Jhat(WL)=Jhat(W),
    D Jhat(WL)=D Jhat(W).                               (11)

The formula follows by inserting (L*NL)^-1=L^-1 N^-1 L^-*; it includes DL, not a frozen reparametrization. In particular a common positive factor cancels EXACTLY in (7)-(8): Q and N both scale by a^2. This is a statement about this normalized feedback trace, not invariance of Rayleigh matter under an unaccompanied change of physical input.

For the existing unmarked execution, W=V_n, N=I and (7) reduces to the original complement. None of (7)-(11) identifies the separate Book geometry partition with this normalized map or fixes the physical active cut.

## 5. A real attenuation retains failures and is a different execution

Post-filtering a retained history with weight exp(-t C_omega/2) can be dilated on a fresh flag while retaining EVERY original history:

    V_filter psi=sum_omega |omega> tensor
       [exp(-t C_omega/2)|success>
        +sqrt(1-exp(-t C_omega))|failure>] K_omega psi.    (12)

The full map is isometric. Failure amplitudes are still labelled by omega. Replacing them by one compressed sqrt(I-N) may reproduce a Gram matrix, but not their preserved histories; we do not erase them. The additional controlled flag operation and any flag reporting require their actual native implementation and price.

For a cut containing the original input and the success flag only, the corner is A_t=i*W_n,t. The TRUE complement is

    F_filter=I-A_t*A_t.                                 (13)

For a scalar physical attenuation a, it is I-a^2 A*A, NOT a(I-A*A). It differs from the normalized Fhat in section 4 because it represents a different isometry with failures, rather than a scalar normalization convention.

On a prepared state rho, success and failure probabilities are

    p_(omega,s)=q_omega exp(-t C_omega),
    p_(omega,f)=q_omega[1-exp(-t C_omega)].

The original query cost is still sum q_omega C_omega. It decomposes as
s E(C|success)+(1-s)E(C|failure); the first conditional term alone is not the all-launch price. If the original history and added flag are classically reported, their COMPLETE entropy is exactly

    H_phi(omega,flag)=H_phi(omega)
                    +sum q_omega h_phi(exp(-t C_omega)). (14)

This does not select Shannon as Book Info. If the flag remains coherent, its different quantum cut must be used. Keeping both flag sectors restores the original oldRIGHT marginal. Conditioning on success generally changes it.

### Constructive sequential normalized kernel

The normalized map in section 4 also has an exact finite chronological factorization. With k rounds remaining define

    Khat_b,j^(k)=exp[-t(1+b)/2]
                  N_(k-1),t^1/2 K_b,j N_k,t^-1/2.       (15)

Equation (2) gives sum Khat* Khat=I at each step. The full word telescopes to
exp(-t C_omega/2)K_omega N_n,t^-1/2. To reproduce the conditioned marked state from the original rho using this trace-preserving map one must instead input

    rho_t=N_n,t^1/2 rho N_n,t^1/2 / Tr(rho N_n,t).        (16)

The equality follows by direct substitution. These new positive operators and the changed preparation have not been shown to be native paid gates. For purification C, the new right Gram is C*N_n,t C/Tr(C*N_n,t C), generally different from C*C. Thus (15) is an explicit normalized mathematical kernel, not a free same-initial-state replacement or oldRIGHT-preserving actuator.

## 6. Correction of the earlier port-marker table

For the original nonblank pair K_0=pL, K_1=sqrt(p)L, the ORIGINAL charge gap is 1 and the tilted target has q_t(1)/q_t(0)=e^-t/p. Absolute weights on normalized branch states therefore require

    Delta I_abs,amp=3/2-t/(2 ln phi),
    Delta I_abs,prob=2-t/ln phi.

Those two formulas were correct. But an EXTRA multiplier applied to the UNMARKED original Kraus pair to PRODUCE this target needs ratio e^-t/2, hence

    Delta I_extra,unmarked-to-marked=1-t/(2 ln phi).      (17)

The earlier Delta I_extra=1 is correct only when preserving the record already supplied as the base, in particular when that base has already been marked. At t=ln phi, the unmarked-to-marked gain is 1/2, not 1. Claims of a three-way common calibration at that t mixed different bases and are withdrawn. No formula in this section is promoted to a mandatory Book Info law.

## 7. Complete unchanged HJR source and application to the primary solution

Return to the ORIGINAL unmarked full128 with its owned heat/feedback/matter convention. For fixed alpha,m,z,C_work, beta=m alpha,

    Delta=D^2, B=I-alpha Delta, Z_h=Tr B^m,
    M_h=(1-z)I+zB^m,
    S_HJR=Tr(rho Delta)+log(C_work Z_h)/beta-r_R Tr log M_h.

Its full derivative remains

    DS_HJR=Tr[(rho-B^(m-1)/Z_h
                +r_R beta z B^(m-1) M_h^-1) DDelta]
                +Tr(Delta D rho).                       (18)

The complete-record normalization (1) is not the nonconstant Z_h in (18). All thermal modes, the reference factor128 and actual workspace constant remain. If calibrations move their derivatives must also be kept. This is the given conditional HJR price, not proof that it equals every physically compulsory Cost-Info ledger.

The existing `PRIMARY_CAR_PREPARATION_SOURCE.md`, equations (3)-(8), gives the exact required primary consumer. On its L4 periodic storage completion of the local nonvacuum chart, use the ACTUAL cost20 F/R density, all128 real Fourier columns and waveform

    b(u)=t u(u-1/4), c=0, sigma=p^3,
    w=(1,1,2,2), w+u=(2,1,2,2).

The native CAR rotation at w preserves every oldRIGHT Gram entry while the geometry and unprepared closed-history H,J are fixed. The owned full16 composition and original Fourier kernel 7/4096 give

    partial_angle S_HJR
       =-[7 p^7 sqrt(rho_w rho_(w+u))/2048] t+O(t^3).     (19)

The original integer routing gives count_w=39, count_(w+u)=48,

    rho_w=384/421, rho_(w+u)=6144/5473,
    coefficient approximately -0.000119122020097172.

Its magnitude is strictly between the exact rational bounds
45927/526250000 and 1640625/11477712896. Thus (19) is negative for every sufficiently small positive t on the owned analytic chart; no numerical t-radius is asserted.

Equation (1) has ZERO source in this preparation direction. A common normalization convention has ZERO source by (11). The unprepared Book determinant and heat term have ZERO preparation source on this fixed-D variation by their actual definitions. They therefore cannot cancel (19). A physical filter or a new independently charged preparation is a different complete execution and must be priced, not used as a free normalizer.

This finishes the proposed normalization repair test on the original primary family: the normalized full record is reconstructed, the true complement is used, the full HJR source is evaluated, and that candidate still fails a genuine independent preparation row. It does NOT prove that all native Book realizations fail, that all HJR solutions are flat, or that no coupled corrected geometry/preparation exists. The configured all42 Einstein-CAR theorem remains correct for its own action. No fictitious stress, gain table, changed z, discarded history or fitted action is introduced.

## 8. Executed checks and evidence boundaries

`check_normalization.py` implements the literal current native_round formulas on the legal L4 Fourier character (i,i,-1,-i), nu=3/5, proper role-1 boost theta=.08, all16 CAR components and both Julia defects with analytical Sylvester derivatives. It enumerates all128^2 ordered histories and independently reconstructs N_2,t and its jet by (2)-(3), at t=.7. This is a Fourier-block diagnostic, NOT a replay of the entire 256-site primary instrument or its rank128 preparation. The all-size proof carries oldRIGHT analytically; the unnormalized feedback fixture keeps the actual factor128.

The observed normalizer eigenvalues range from 0.243289765868066 to 0.243380698890563, so it is nonscalar. Its field derivative has Hilbert-Schmidt norm 0.00253999249826. The true normalized feedback source is -4.79117978836e-6; incorrectly freezing DN gives -6.94288931682e-6. Physical attenuation with all failures gives a DIFFERENT source -1.69010453001e-6. All are at the same fixed native z=2^-20.

There are 39 explicit conditions, including exact rational noncommuting controls and exact scalar-gauge cancellation. Normal and optimized Python runs agree byte-for-byte. Four deliberately mutated scripts are rejected: omitted normalizer jet, discarded filter failures, removed RIGHT factor, and frozen transformed input. Numerical checks have declared tolerances; the primary sign follows from the inherited analytic local formula and exact counts, not the 16D diagnostic. No historical all42/root/Lean suite or independent mathematical review is claimed.

The stage-word/clock and newest weighted-Ward results are preserved as separate consumers. A normalized record map, its full complementary feedback, and an independently defined Book memory-algebra partition still need their actual common-execution identification before any physical GR claim. The claim that just ONE scalar was the only remaining physical problem is withdrawn. `GR_closed=false`.
