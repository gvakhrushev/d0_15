# Full-register native compilation, internal clock heat and finite-test source recovery

27 October 2026. Existing scientific owner: gvakhrushev/d0_15, Draft #334, native-programme-v1. Input c7708742bea04684ffd6aed16774cfdf1b94b129. Research theorem, not a claim/BOOK/assembly promotion. `unconditional_GR_closed=false` and raw216 remain open.

## 0. Consumed results and exact intended scope

Consume, rather than reprove, the source geometry and its declared physical hypotheses:

- `A4D_NATIVE_GOLDEN_PROGRAM_COMPILATION.md`: the literal addressed Golden/CNOT class, actual preparations and retained ancillary all-input error contract. Its earlier external density input is Y. Shi, arXiv:quant-ph/0205115v2.
- `A4D_DENSITY_INVOLUTION_COMPLETE_PRICE_GENERAL_SOURCE_2026_10_27.md`: actual coframe/link/CAR moment report, its true nonuniform PF weights, complete candidate price and general bounded-smooth Einstein-scalar first-source limit with the genuine nonzero gain.
- `A4D_ORIGINAL_GOLDEN_READY_COHERENT_BOOK_FULL42_BRIDGE_2026_10_22.md`: whole coherent comparison V* R V, complete retained work and the three-status report. Previously sealed classical records are NOT silently made coherent again.
- `sources/d0_coupled_cut_partition_2026-10-22/COUPLED_PARTITION_PROOF.md`: full cut heat, all harmonic modes and strict source monotonicity.
- `A4D_COMPLETE_BOOK_SOURCE_FIXED_INITIAL_APPLICATION_2026_10_27.md`: eliminate generated internal states with their true price; retain genuinely independent inputs.
- Original result 7ct821-827, commit c4f5c2f2dc2b1a129e8ca09074e543c3a2906fb4: actual normalized K(9,11,13) internal clock heat and its generic non-reflection monodromy dependence. Its nonzero 26-stage heat source is NOT contradicted below.
- `D0_GR_CLOSURE_CONTRACT_RU.md`, especially section 5: a separate finite-test macroscopic result does not change exact-root or raw-norm requirements.

New result: in an explicitly addressed native gate class, a finite primitive word has a generated internal stage cut whose feedback is exactly the endpoint feedback. The original scene/clock incidence heat is exactly field-independent at the ideal coherent reflection, and its complete compiled error is bounded. Combining this with the already-owned smooth source theorem gives both directions of a FINITE-TEST macroscopic source statement. This is NOT construction of exact stationary finite roots, selection of the class from M1, or proof of a common physically selected infinite history.

The immediately preceding local intrinsic-metric/stationarity packet was replayed in this session: 59 checks, normal and python -O, identical receipts. It was not falsely treated as having been pushed to this branch.

## 1. All columns on a FIXED register: no uncontrolled ancillary heat

Let p=(sqrt(5)-1)/2 and G=[[sqrt(p),-p],[p,sqrt(p)]]=exp(theta J), J=[[0,-1],[1,0]].

### Irrational original angle

The actual algebraic number 2 cos(2theta)=2sqrt(5)-4 has minimal polynomial x^2+8x-4 and conjugate -2sqrt(5)-4<-2. Were theta/pi rational, it would be a root-of-unity trace, all of whose conjugates lie in [-2,2]. Thus theta/pi is irrational and the nonnegative even powers G^(2m) are dense in SO(2). This is a property of the original fixed gate, not a new continuous primitive.

### CNOT supplies every skew real Pauli direction

For n qubits, d=2^n, let P(a,b)=X^a Z^b, a,b in F_2^n. The d(d-1)/2 strings with a dot b=1 are real skew, square to -I, are Hilbert-Schmidt orthogonal, and form a basis of so(d). A binary reversible coordinate change T acts by (a,b)->(Ta,T^(-T)b). This GL(n,F_2) action is transitive on a dot b=1: use a as first basis vector and complete with a basis of ker(b). Every such T is a CNOT/SWAP circuit, and SWAP is three CNOTs. Therefore every skew string is, up to sign, a CNOT conjugate of local J.

The closure of words C G_i^(2m) C^-1 contains every associated one-parameter group. Their Lie algebra is all of so(d); the generated closed connected group is SO(d). Each displayed block has EVEN total native length and C^-1 is the reversed sequence of self-inverse CNOTs.

**Theorem 1.** Every computably specified target in SO(2^n), n>=2, admits a finite EVEN original G/CNOT word with any requested positive full-register operator-norm error. No untested compiler ancilla is needed. An effective, potentially very inefficient compiler enumerates even words and certified norm bounds until the strict target bound is met; density proves termination. No efficient runtime claim is made.

For determinant -1 targets, a fixed additional -1 padding block puts the full target in SO; it and its heat are retained. Faithful realification of a complex unitary also lies in SO but changes multiplicities, which must be retained. Protected oldRIGHT can remain an exact spectator by compiling only live/work. No actuation on a sealed archive is inferred.

CNOT^2=I permits any FINITE list of even words to have the same finite even clock, paid by explicit padding. This is a same-clock comparison, not a proof of global D_min optimality. Enforce clock length N>=3.

## 2. The active clock cut is generated from the actual word

Let g_0,...,g_(N-1) be the actual word and V=g_(N-1)...g_0 its full endpoint. Set A_0=I, A_t=g_(t-1)...g_0. The internal stage operation and transported active projector are

    S_g=sum_t |t+1 mod N><t| tensor g_t,
    P_g=sum_t |t><t| tensor A_t P_0 A_t*, Q_g=I-P_g.          (1)

The full work and spectator columns stay present. Once the word and P_0 are supplied, P_g has no extra continuous argument. With A_clock=diag(A_t),

    A_clock* S_g A_clock=T_V,
    A_clock* P_g A_clock=I_N tensor P_0,

where T_V has identity edge transport except V on the wrap edge. Direct multiplication yields

    P_g S_g* Q_g S_g P_g
      ~= 0_(first N-1 stages) direct_sum P_0 V*Q_0 V P_0.    (2)

Thus the one-step autonomous feedback determinant is EXACTLY the endpoint determinant. All other stage modes have determinant factor one, not deleted modes. A scene-root active cut can be tensored in while leaving every scene fibre in the heat.

The cut is a finite internally computed predicate, but its actual selection and physical implementation remain explicit premises. A different initial-stage-only blank projector gives a different operator and may give trivial immediate leakage. The programme clock is not spacetime time or a declaration that spacetime is periodic.

A moving generated preparation P_y=A_y P_0 A_y* is included by compiling the WHOLE conjugated operation A_y* U_y A_y at fixed P_0. This retains all cut derivatives, preparations, inverses and work. It does not turn an independently free input into a generated one.

## 3. Full original scene/clock incidence heat

Use the original K(9,11,13): 33 vertices, 359 edges, vertex degrees 24,22,20. Its product with the N-stage cycle has 33N vertices and 392N edges, each carrying the actual d-dimensional data/work fibre. Scene edges have identity transport; clock edges have the actual g_t. Let

    R_s=(D_s+2I)^(-1/2), B_s=R_s A_s R_s, C_s=R_s^2,
    ||C_s||=1/22.

For the actual normalized covariant graph differential d_g, prefix gauge gives

    Delta_0(V)=I-B_s tensor I-C_s tensor(T_V+T_V*).           (3)

This is the original internal normalized graph form in result 7ct, not a fitted endpoint cut heat. Since Delta_1=d_g d_g* and Delta_0=d_g* d_g have the same nonzero singular-square spectrum, the ENTIRE 0+1 heat is

    Z_01(V)=359 N d+2 Tr exp[-beta Delta_0(V)].               (4)

All zero modes are included. On the common carrier H^0 direct_sum H^1, put the active feedback cut in H^0 and extend its clock unitary by a fixed identity on H^1. The feedback there is zero while the entire Delta_1 heat remains. This is an explicit two-grade realization, not a claim that every higher clique degree or a differently selected Book Hodge operator equals this pair.

## 4. Exact runtime heat neutrality of the actual coherent comparison

The already supplied comparison target is W_y=A_y* R A_y, with FIXED complete selfadjoint involution R. Controlled direct sums of the three original fixed status reflections plus idle blocks have this form and fixed full +/- multiplicities. All source/preparation/query work belongs to A_y.

W_y and W_y0 are conjugate on the ENTIRE register. Applying the same conjugation at every stage and scene vertex conjugates (3), and (4) preserves every harmonic mode. Therefore, for fixed N,d,beta,

    H_01(W_y)=beta^-1 log Z_01(W_y)=constant,
    D_y H_01(W_y)=0.                                       (5)

The ideal full internally clocked price is consequently

    B_runtime,ideal(y)=H_01(N,d)+J(rbar(y)),
    D B_runtime,ideal=J'(rbar) D rbar.                      (6)

This is a theorem about the full runtime heat of the specified word class, not an assumption that heat has no field dependence. Its value remains paid and changes with clock, dimension and temperature.

The original full cut candidate B_C(rbar) and feedback J(rbar) both have strictly positive derivatives on the owned report interval. Hence (6) has exactly their same field stationary set and, with its own actual gain, the same already-derived smooth Einstein-scalar source limit. Equality of unrelated heat operators is unnecessary.

**Critical scope:** an appended COPY, sealing, dephasing, observer controller or new record operation changes the completed word. It need not remain a reflection. Recompute that full source; the existing non-reflection 26-stage counterexample remains valid. This theorem uses the declared deferred/coherent comparison, not a secretly unmeasured version of an already sealed history.

## 5. Full compiled runtime price, not merely a prepared amplitude

Theorem 1 gives a genuine finite primitive word V with ||V-W||<=delta on EVERY complete live/work column. For the same clock and full carrier,

    ||T_V-T_W||=||V-W||,
    ||Delta_0(V)-Delta_0(W)||<=delta/11.                    (7)

For selfadjoint matrices X,Y on the same space, min-max eigenvalue bounds give

    |beta^-1 log Tr exp(-beta X)
      -beta^-1 log Tr exp(-beta Y)|<=||X-Y||.

Adding the positive constant 359Nd and doubling both traces preserves the exponential sandwich. Therefore

    |H_01(V)-H_01(W)|<=delta/11.                            (8)

For endpoint active rank r INCLUDING real spectators, ||F_V-F_W||<=2delta. Integrating the logdet derivative on their common positive-contraction segment gives

    |J(V)-J(W)|<=2r z delta/(1-z).

Combine with (8):

    |B_runtime(V)-B_runtime,ideal(W)|<=L_clock delta,
    L_clock=1/11+2r z/(1-z).                               (9)

This includes dirty/unoccupied-column runtime heat. Its validity is why Theorem 1 strengthens prepared-subspace compilation to full-register compilation. It does not control arbitrary added physical prices by renaming them heat.

### Complementary endpoint-cut theorem with retained compiler ancillas

The older contract ||VJ-JU||<=delta, with isometry J attaching actual prepared ancillas, also supplies a useful separate result. Use P'=JPJ*, C'=Q'VP', C0=JQUPJ*. Exactly

    C'-C0=Q'(VJ-JU)PJ*,
    ||F'-F0||<=2delta, ||Delta'-Delta0||<=2delta,             (10)

where Delta=C*C+CC*. The two heat differences occupy orthogonal P'/Q' blocks, so the bound is 2delta, not 4delta. On the same complete carrier,

    |B_cut(C')-B_cut(C0)|<=[2+2r z/(1-z)]delta.              (11)

Every added ancillary zero mode remains: Z_padded=(D-d)+Z_logical. This padding contribution is generally FIELD DEPENDENT; it is not discarded as a constant. The original three-status monotonicity and normalized source bounds survive retained padding. The runtime theorem (9), however, uses full-register error, not just (10).

## 6. Do not differentiate a discrete compiler: finite normalized source contrasts

Let Gamma_h>0 be the genuine small source gain of the SAME ideal candidate and t>0 a compatible field-comparison step. Compile the finite pair y+tv,y-tv on a common paid register/clock. Their actual complete prices give

    T_comp(y;v)=[B_comp(y+tv)-B_comp(y-tv)]/(2t Gamma_h).

Equation (9) proves

    |T_comp-T_ideal|<=L_clock delta/(t Gamma_h).             (12)

The source error is NOT merely O(delta). Discarding the small Gamma_h or t would invalidate the transfer. For Golden tolerance kappa_k=phi^-k choose

    delta_k<=Gamma_h t kappa_k/(4L_clock).                  (13)

This is a real precision requirement, not a claim the huge word at that accuracy was emitted. At finite k only finitely many targets are involved, and even-word padding gives the common clock. The ideal heat baseline cancels from the paired contrast while remaining in both absolute physical prices.

## 7. Two directions of an explicitly MACROSCOPIC finite-test theorem

Use the already-owned candidate source consistency on a bounded regular smooth chart and compatible smooth tests:

    ||D J_h-D S||<=E(h), E(h)->0,
    J_h=[B_ideal,h-B_ideal,h(r0)]/Gamma_h.                   (14)

Here S is the existing Palatini-scalar limit in the derived density metric. Runtime ideal (6) has this property from the same polynomial report and feedback. Assume DS has Lipschitz constant H along the tested paths. The finite quotient is an integral of D J_h, so

    |T_comp,h,t(y;v)-DS(y)[v]|
      <=E(h)+H t/2+L_clock delta/(Gamma_h t).               (15)

Choose a countable dense family v_j of compactly supported compatible smooth tests with norm<=1. For each k test only j<=k.

**Recovery of finite witnesses.** For any supplied COMPUTABLE smooth solution DS(y)=0 in this chart, take h_k,t_k with E(h_k)<=kappa_k/4 and H t_k/2<=kappa_k/4 and use (13). Then every first-k compiled test has |T_comp|<=3kappa_k/4. Certified arithmetic error<=kappa_k/4 gives finite PASS witnesses. Targets are computed from the original coframe/link/matter report, not from inserting the Einstein tensor as an observable. Effective construction requires the actual regularity/bounds and cannot use an unencoded continuum oracle.

**Soundness.** Suppose a sequence of such finite witnesses has uniformly regular smoothly convergent field interpolations y_k->y, errors in (15) tending to zero, and passes all first-k tests. For any fixed j, eventually j<=k and (15) implies DS(y)[v_j]=0. By density and continuity DS(y)=0 on all compactly supported tests. Varying the independent connection first gives the owned Einstein-scalar equations.

This is a bidirectional statement in the DECLARED finite-test/macroscopic topology. It is NOT a compactness theorem for arbitrary executions, physical dynamics selecting the witnesses, or exact stationary roots at each mesh. Nor do separately compiled stages automatically produce a single physically compatible history/refinement tower.

The distinction is strict: S_h(x)=x^3/3+h x has derivative x^2+h>0 for h>0, but S_0 has a stationary point. Vanishing finite residuals do not prove exact roots. The previous inverse-Hessian/exact-root obligations and raw216 remain unchanged.

The derived continuum action's off-shell Lorentz/diffeomorphism Ward identities likewise give vanishing finite-test Ward defects through (15), not an asserted exact diffeomorphism symmetry of every finite word.

## 8. The genuine remaining original-D0 comparison

The construction uses only the stated original gate palette, internal registers, original scene and actual history price. It removes a computational/execution source gap WITHIN THAT DECLARED CLASS. It does not prove:

1. Admission of arbitrarily addressed G/CNOT, all supplied finite preparations and resources from the original foundational process.
2. Physical selection/implementation of the generated prefix cut and this entire 0+1 runtime price, or a proved source-equivalent map from the actual complete Book action including any terminal apparatus and independent inputs.
3. One physically compatible refinement tower and strong exact-root/raw-norm recovery when those are the intended claims.

For a real additional price R_h=B_actual-B_runtime, the exact remaining source contrast is

    [R_h(y+tv)-R_h(y-tv)]/(2t Gamma_h).                      (16)

It must be computed/bounded on the actual common execution; it is not a proposed counterterm. A truly field-independent same-task cost cancels, however large. Field-dependent archive, clock, temperature, preparation and controller prices do not cancel merely because they are internal. No unconditional D0-to-GR conclusion is asserted without these premises.

## 9. What was actually executed

Two new bounded checkers ran in normal and python -O modes; each pair produced identical JSON. Tests raise exceptions, not removable asserts.

**61 cut/source checks:** exact rational cut identities; all-column negative control; an ACTUALLY MULTIPLIED word of 746 original Golden rotations plus two CNOT conjugations on all8 columns; full ancillary leakage and nonzero price error; large complete harmonic baselines; moving-cut source; unequal four-cell source contrasts; true-gain accuracy budgets and exact-root negative control. Native small-word norm error is about 0.00052373655825 and full cut-price error 0.00037414188688, below 0.00132679928090. This is NOT the huge general-GR circuit.

**80 full-register/clock checks:** exact irrational Golden trace algebra; CNOT orbits of all skew Pauli directions on2–6 qubits (6,28,120,496,2016 directions); all8 columns of an exact rational four-stage prefix cut with feedback trace576/625; actual33-vertex359-edge scene; full528-dimensional0-grade spectra at three reflection parameters; all6800 paired0/1 dimensions retained; equitable-partition evaluation checked against the full heat; non-reflection perturbations evaluated at80 digits. At angle error0.02 the genuine full heat difference is 9.7335587529354154855e-13, not zero, and obeys delta/11.

An initial arbitrary 1e-12 nonzero threshold was too large; exact scene decomposition and high precision exposed the smaller actual nonzero heat difference. No theorem was weakened. A structural four-cell diagnostic also rejected an unsupported guessed constant3 for its error bound; the final test uses the predeclared Golden tolerance and records its actual coefficient, not the false guess.

Python3.13.5, SymPy1.14.0, mpmath90/80 digits, NumPy/SciPy for bounded spectral checks. General results follow from the proofs, not extrapolation from samples. No huge original READY/GR word, full all42 root solve, Lean, CI or independent review was run. The earlier59-check local packet was replayed, not counted as a newly proved theorem. Draft status and all physical-closure flags stay unchanged.
