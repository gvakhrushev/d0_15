# D0: the original full N1 CQ temporal two-CAR elimination leaves a block-tridiagonal geometric Hessian plus an EXACT rank-two border

22 October 2026. Existing research PR #334 / EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE / native-programme-v1. **Exact analytical same-price composition**, with an independently executed high-precision original N1 finite price/root check, not compulsory native Book03 full H+J+R, not a certified global original geometric root or GR closure.

This consumes ALREADY OWNED original inputs:
- Original complete N1 sigma-minus GoldenMaster source, with canonical null/cart coframe sign pullback x=-tau f_star/rho, native z=2^-20 and both actual two-real-CAR scalar time gradients, pinned in sources/d0_weighted_two_field_rank2_2026-10-21/native_master.py and sources/d0_star_rank2_seam_2026-10-21/full_n1_euler_analytic.py.
- Original all-cell finite Golden/PF C2 schedule and REAL interval-coercive two-CAR flux theorem A4D_NATIVE_GOLDEN_PF_C2_TWO_CAR_SLAB_SCHUR_2026_10_22.md. Its quantified positive rectangle is NOT reproved.
- Original full nonlinear N1 temporal Lorentz SO+(1,3) gauge quotient, fixed BOTH true field collars, and exact block-nearest-neighbor Euler theorem A4D_FULL_N1_NATIVE_TEMPORAL_GAUGE_QUOTIENT_MULTISLAB_ROOTS_2026_10_22.md. The n3/n4/n5 nonflat 78/114/150-equation original ROOTS there remain floating numerical witnesses only.

## 1. Exact full original scalar Euler and its two-vector current

Let j=0,...,n-1 be original time-anchored based-face cells; rho_j>0 are their TRUE native fixed-count PF weights. Let theta be all original independent coframe/proper-link coordinates AFTER the owned genuine residual temporal gauge quotient, with BOTH actual time-end field collars fixed. Let u_j=(psi_(j+1)-psi_j)/h be the two real temporal CAR gradients and keep their REAL specified transverse CAR difference vectors fixed for this temporal reduction. The actual native kinetic density has exactly

    q_j = a_j |u_j|² + 2 b_j·u_j+c_j,
    a_j=g_j^00>0,
    b_(j,A)=sum_(s>0) g_j^(0s) D_s^+ psi_A,
    c_j=sum_(A,s,t>0) g_j^(st) D_s^+psi_A D_t^+psi_A.

All a,b,c arise from the same original coframe; no external material potential is inserted. The entire same-N1 complete CQ field-price component is, divided by ONE fixed nonzero factory/time-source constant for mathematical Hessian comparison,

    S(theta,psi)=sum_j ell_j(theta,u_j);
    ell_j = rho_j F_N(-tau f_star,j(theta)/rho_j,tau q_j/rho_j) /(-tau a_N),
    tau=1/20, a_N=F_N,x(0,0)<0.

F_N is the genuine original nine/twenty cap, sigma-minus GoldenMaster
F_N(x,y)=-alpha beta [h_phi(r(x,-y))-h_phi(r0)] with its ORIGINAL native two-band output r and native z=2^-20. The readiness alpha beta is positive and may be divided out of the field EULER only as one fixed common multiplier: its actual physical cost/clock/source is not pronounced free.

Define the full measured-CQ native material-slope ratio

    v_j = -F_N,y(x_j,y_j)/a_N > 0,
    d_j = a_j u_j+b_j,
    J_j = v_j d_j in R².

The genuine FULL first derivative of ell_j is D_u ell_j=2 J_j. Therefore ALL 2(n-1) original temporal scalar Euler rows are EXACTLY

    D_(psi_j)S = 2/h (J_(j-1)-J_j)=0,
    J_j = common two-current J,
    h sum_j u_j = psi_n-psi_0 = Delta.              (1)

This is nonlinear through the FULL same r(x,y) and does not freeze q=0 after variation. ALL produced q_j are retained and paid at their genuine native report probability.

## 2. Uniform positive time-scalar local inverse and full endpoint map

Put H_j = D_(u_j) J_j. With v_y the derivative of v with respect to the SAME original second Golden operand, an EXACT differentiation gives

    H_j = a_j v_j I_2 + (2 tau/rho_j) v_y,j d_j d_j^T.        (2)

The owned rigorous whole-rectangle interval test proves F_y>0 and
F_y+2(y-y_perp)F_yy>0 (with explicit positive numerical lower bounds) for |x|,|y|,|y-y_perp|<=1/128. These are precisely the two true eigenchannels of H_j after the positive factor a_j/|a_N|. Hence H_j is SPD on the actual admitted timelike chart. If a_j>=a_min>0, its minimal eigenvalue m_flux>0 is independent of the number of intervals, as long as all cells stay in the same rectangle. For fixed two temporal endpoint values the scalar Dirichlet Hessian is

    H_(psi psi) = (2/h²) Incidence^T diag(H_j) Incidence >0.
    lambda_min(H_(psi psi)) >= 8 m_flux /(n h)².           (3)

The last bound uses 4 sin²(pi/(2n))>=4/n². Therefore on a fixed-length time interval the temporal scalar inverse has an explicit mesh-independent coercive lower bound, rather than an unquantified global inverse. This does NOT apply to the pure-null Brinkmann g^uu=0 in lieu of timelike g^00>0.

Each original cell equation J_j(u_j;theta)=J is locally invertible with D_J u_j=H_j^-1>0. Its TWO-component endpoint map h sum_j u_j(J)=Delta has derivative h sum_j H_j^-1>0. On the strict native source chart there is a unique local fixed-endpoint scalar solution psi_*(theta); no full 2(n-1)-dimensional scalar Newton is required. True final boundary values are preserved.

## 3. NEW theorem: EXACT low-rank (at most TWO) global memory after temporal material elimination

At psi_*(theta), define the original actual geometric covectors

    B_j = D_theta J_j |_u_j   (2 by m),
    H_j = D_u J_j > 0,
    W = sum_j H_j^-1           (2 by 2, SPD),
    C = sum_j H_j^-1 B_j       (2 by m),
    m = dimensions of genuine gauge-reduced geometric variables.

Importantly B_j differentiates BOTH original coframe/holonomy f_star,j and the SAME metric/car q_j, including the TRUE predecessor based-face appearances and Lorentz-frame transport; it is not an independent prescribed curvature/source adjustment.

Differentiate the exact common-current condition J_j=J and the fixed-endpoint sum:
    delta u_j = -H_j^-1 B_j delta theta
                + H_j^-1 W^-1 C delta theta,
    delta J = W^-1 C delta theta.                          (4)

The exact envelope source is D_theta S_red = D_theta S(theta,psi_*) with S_red(theta)=S(theta,psi_*(theta)). Substituting (4) into the second derivative, using D_theta D_u ell_j=2 B_j^T, gives

    BOX: K_eff = K_local + 2 C^T W^-1 C,
    K_local = D_theta² S|_u - 2 sum_j B_j^T H_j^-1 B_j.    (5)

Thus the ENTIRE extra global field coupling from both genuine CAR time potentials, under the original full nonlinear source price, is a symmetric PSD correction of rank <=2. It is NOT a fitted rank-two gravitational term or a replacement for the complete matter Hessian; (5) is algebraically identical to the full true constrained Schur elimination.

The original N1 local score cell j depends on physical field nodes j and j+1 only (true forward CAR current and four-edge temporal plaquette). The owned offshell exact temporal gauge quotient preserves this locality. Consequently D_theta² S|_u and every B_j^T H_j^-1 B_j are block tridiagonal. Therefore

    BOX: K_local = original temporal block-TRIDIAGONAL geometric operator;
         K_eff = K_local + one global rank <= 2 border.   (6)

This remains true for arbitrary time-dependent positive native PF weights, PROVIDED the existing fixed native address/price chart is used. No uniform-site prior and no independent extra temporal controller action.

At n intervals the owned true Lorentz gauge quotient removes 6(n-2) exact redundancies:
    original free fields =42(n-1);
    gauge-reduced fields =36n-30;
    exact two-real-CAR flux eliminates 2(n-1);
    BOX geometric unknowns m=34n-28.                       (7)

New genuine block sizes: [34,...,34,40] (n-2 copies of 34, one final 40). At n=3,4,5: 78->74, 114->108, 150->142. These counts are not informal half-Euler truncation: the old exact Noether identity reconstructs the removed original Lorentz Euler rows, while (1) exactly solves the two original scalar rows.

## 4. One native geometric block-Schur inverse and ONE 2x2 final pivot

The ordinary exact Woodbury formula gives, wherever the genuinely computed K_local is invertible,

    BOX:
    K_eff^-1 = K_local^-1
      -2 K_local^-1 C^T [W+2 C K_local^-1 C^T]^-1 C K_local^-1.  (8)

The remaining global invertibility condition for that representation is the genuine 2x2 matrix G2=W+2 C K_local^-1 C^T. It may be indefinite/singular because the 34/40 geometrical Palatini blocks are indefinite; their invertibility is NOT claimed. If a particular local nonpivoted block factorization fails, use the equivalent 2-border system, valid without K_local^-1:

    [ K_local  2 C^T ] [dtheta]  = [rtheta]
    [ C        -W   ] [dJ    ]    [0     ].               (9)

Schur-eliminating the strictly SPD -W gives exactly K_eff, with no new source and no correction fit. This supplies the explicit target for the already owned TRUE original block-tridiagonal Schur pivots and a genuinely 2-dimensional extra determinant/inverse control. A certified full root/refinement still needs a rigorous original geometric pivot estimate and real collar/gauge control, not just a smaller matrix.

## 5. Executed 75-decimal independent nonlinear Golden source check; BOTH currents active

The separately executed high-precision checker uses the actual original native Golden r(x,y), H_phi, exact p=(sqrt5-1)/2, z=2^-20, tau=1/20, both real CAR species with time-varying nonzero current and a true nonzero spatial gradient of species 2. The real Lorentzian Cartesian coframe metric chart e_00=X, e_01=k, e_11=1/X gives

    g^00=X^-2-k², g^01=X*k, g^11=-X²,

so the native current has truly independent components for variable coframe k (unlike an accidentally rank-one diagonal matter fixture). The original f_j values are seeded from the owned exact based-six-face non-VSI expression on actual erfi-time radii. The local numeric Hessian diagnostic treats f_j and k_j as separate coordinates to isolate this flux/metric theorem; it is NOT a replay of all40 original coframe/connection f_j variations under k, whose chain rule is already retained in the analytic B_j of (5).

At three real time intervals, with genuine nonzero r and two current components, the independently re-solved full original nonlinear CQ entropy derivatives give:

    PF=[1,1,1]:
       before flux mismatch 0.00581567379357
       after common-current root 2.18e-72
       independent full entropy scalar Euler 6.20e-75
       min eigen H_j 38.583980004
       rank-two C minor 1.045906972e-4 (nonzero)
       reduced Hessian vs independently re-solved full source 1.43e-36
       direct inverse vs 2x2 Woodbury 5.53e-76

    PF=[1,2,1]:
       before flux mismatch 0.00597220750239
       after common-current root 2.04e-71
       independent full entropy scalar Euler 1.37e-74
       min eigen H_j 38.583969257
       rank-two C minor 1.045415932e-4 (nonzero)
       reduced Hessian vs independently re-solved full source 1.44e-36
       direct inverse vs 2x2 Woodbury 1.11e-75

An additional 64-bit 4-interval PF=(1,1.2,.9,1.1) test with the real nonzero k coframe has a genuine two-component rank, max current Euler 4.5e-16, full Hessian/independent source comparison <7e-7 and the direct-vs-Woodbury inverse mismatch <1e-14. A strictly diagonal/co-moving matter configuration gives only rank ONE, correctly showing that rank two is a generic possibility, not a universal equality. The actual scalar Jacobian lower bound, not these floating values, establishes the analytic invertibility premise.

The high-precision checker uses the literal original 75-digit GoldenMaster formula; it is a standalone source-level exact-price computation at sampled original geometry, not an independent run of the enormous original 256-cell/full128 process. Test-side f,k independent variations are only a local analytic coordinate check; the proof (5)–(6) holds for the true original based curvature f(theta) and all allowed independent geometry coordinates.

## 6. Honest physical and mathematical closure boundary

**Discharged inside the already declared complete fixed CQ field source**: the entire simultaneous two-real scalar temporal Euler block, its nonlocal influence, its mesh-uniform positive inverse on the admitted timelike chart and the apparent full-time dense geometric Schur cost. The existing 34/40 geometric connected blocks and ONE true 2x2 terminal current pivot are now the only remaining mathematical inverse conditions for this finite slab source, with their real native PF and original two-ended collar. The exact full42 stationary source set and old geometric Einstein coefficient were never replaced.

**Still open**: certified interval/analytic nonsingularity of the actual original indefinite geometric 34/40 time blocks and the true 2x2 pivot at the nonflat numerical CQ roots; actual full native Book03 compulsory absolute Info/H+J+R/cut/input cost, other full4D spatial matter variations, true physical field writer and controller selection and global smooth continuum refinement. One local analytic inverse theorem for the CQ price is not the derivation of fundamental GR, and no extra causal-time action or scalar root is imported. Scientific status research / #334 Draft, GR_closed=false.

Independent local executed checker path: check_native_n1_rank2_temporal_border.py under sources/d0_n1_rank2_temporal_border_2026-10-22. All source identities are exact algebra; decimals are numerical diagnostics. No independent science review or fresh Lean assertion.
