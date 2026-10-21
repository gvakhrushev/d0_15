# D0: actual clock/work double Schur, coherent delay and complete monitored price

21 October 2026. Supporting synthesis in existing PR #334, EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, constitutive/native-programme-v1. Input checkpoint: 92c00ccbf39e6e21e4383f7a7b573ab7c7c6f1be. No new task, Book03 price selection, physical tick identification or GR promotion.

## 1. Exact missing parent substitution and reused inputs

The existing [clock Schur owner](sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/NATIVE_CLOCK_SCHUR_RETURN.md), section 4, explicitly leaves a further elimination of the arm/record work complement. This note computes it on that SAME apparatus, including its determinant and full source, rather than deleting the work blocks or assigning a clock multiplier.

Inputs at the stated checkpoint:

- `04_CERTIFICATES/order_memory_control_verify.py`, blob ba02280e475b0124395622bfd99257c2820ae026: literal quaternion and Golden gates, WRITE and the sixteen-stage reversible extension.
- `03_FORMALIZATION/D0/Representation/OrderMemoryReadout.lean`, blob 6c31b0c089869f7e6fc07185ef343c6bdce35b2d: original rational quaternion representation.
- `book_source/NATIVE_STAGE_CLOCK_AND_POINTED_DESCENT.md`, blob 0f24c6e0149a84b584130a1206cec605ed078858: actual stage cuts and nonfactorizing windows.
- `book_source/NATIVE_CLOCK_SCHUR_RETURN.md`, blob c9501fa1ae11f0c30ef1ccb190c9ff7b812b5444: clock elimination, archive determinant one, complete monodromy.
- `04_CERTIFICATES/vp_archive_neumann_tick_owner.py`, blob 548449b1bb6d7392d8f71b021c45344ee659b2c6: archive-delay grammar, with convergence left separate. The convergence below concerns the current three-coordinate work block, NOT its old retained3/archive30 scene.
- `sources/d0_native_minimality_closure_2026-10-20/prospective/STOPPED_CLOCK_SOURCE.md`, blob 21031109172282833a938a79cef2ff7dec889266: entire stopped-tape price as an operator. Its CAR16/all128 first-exit instrument is not automatically the present monitored-return process.

The general connection of unitary return amplitudes, Schur functions and quantum recurrence is established mathematics: Grünbaum–Velázquez–Werner–Werner, arXiv:1202.3903; Bourgain–Grünbaum–Velázquez–Wilkening, arXiv:1302.7286. The new contribution is the explicit original D0 application and its price/source estimates, not a new abstract Kac theorem.

## 2. Actual chronological word and exact remaining work block

The original carrier is arm2 x spin4 x record2, not the exterior CAR16 representation merely because both dimensions are sixteen. The order programme is the chronological list

    G, X,Y,X,X,X,Y,Y,Y, X,X,G,X,X, WRITE, idle.

The first fifteen operations are the original reported trial; idle is the supplied closure. All repeated-monodromy statements below concern that declared sixteen-transition extension. Its encoded cycle is not a physical elapsed-time reset.

With p=phi^-1, a=sqrt(p), G=[[a,-p],[p,a]], the exact original monodromy is WRITE G* Z G. Reordering to (arm,record) x spin gives M tensor I4, with

    c=p-p²=p³=sqrt(5)-2, k=2p sqrt(p), c²+k²=1,
    M=[[ c, 0,-k, 0],
       [ 0, c, 0,-k],
       [ 0,-k, 0,-c],
       [-k, 0,-c, 0]].                                    (1)

The preparation j is its first arm/record basis vector, with all four spin columns retained. The identity programme is WRITE and fixes j. The checker reconstructs both complete16 products from the literal native letters before using (1). Extending c,k analytically does not admit a new arbitrary-angle native primitive.

The existing stage elimination gives det(I256-tW)=det(I16-qM_full), q=t^16. t and q remain analysis markers, not physical z, Golden probability or elapsed time.

Split M=[[A,B],[C,D]] at j, A=c, with D the THREE work coordinates. Define

    N(q)=1-cq-c²q²+cq³,
    Delta(q)=(1-q²)(1-2cq+q²),
    Theta(q)=(c-c²q-cq²+q³)/N(q).                         (2)

The exact remaining Schur calculation is

    det(I3-qD)=N(q),
    Theta=A+qB(I3-qD)^(-1)C,
    S_j(I-qM)=1-qTheta=Delta/N,
    j*(I-qM)^(-1)j=N/Delta.                              (3)

Thus the true twelve-dimensional work determinant is N^4 and the effective four-spin determinant is (Delta/N)^4. Their product reproduces Delta^4, with no extra factor16. For the coherent logdet STATISTIC already used by the owner,

    J_full=-4 log Delta=-4 log N-4 log(Delta/N).           (4)

The work term is NOT source-neutral: partial_c N=-q-2cq²+q³. Replacing the active Schur by the direct corner 1-qc or omitting N^4 changes the source. At q=1, N=1-c²>0 but Delta=0: a regular archive inverse does not make the full resolvent invertible.

For arbitrary noncommuting actual block variations, R=(I-qD)^(-1) gives

    dTheta=dA+(dq)BRC+q(dB)RC+qBR(dC)
              +qBR[(dq)D+q(dD)]RC,
    dJ_full=Tr[R((dq)D+q dD)]
       +Tr[(I-qTheta)^(-1)((dq)Theta+q dTheta)].          (5)

Moving cut, pairing and preparation belong in these block derivatives. If real scalar stage weights are supplied, q=product_r w_r carries dq=q sum_r dlog w_r; noncommuting price weights stay in the ordered product. No physical weight or Info is assigned by (5).

## 3. Convergence, exact positive defect and the native Golden delay

Exact Krylov arithmetic yields

    det[j,Mj,M²j,M³j]=(1-c²)².                            (6)

For real |c|<1, j is cyclic. A unit-modulus eigenvector of the contraction D would, by norm conservation, be a unitary eigenvector of M orthogonal to j and all M^n j. Hence no such vector exists: rho(D)<1. The actual work Neumann series converges, including q=1. This supplies the analytic premise, not just finitely many formal terms. At the native c=p³ and 0<=q<=1, N(q)>=1-c-c²=3c>0.

The standard unitary-colligation defect, now applied to the literal original blocks, is

    I-Theta(q)*Theta(q)
      =(1-q²) C*(I-qD*)^(-1)(I-qD)^(-1)C.                (7)

Its actual scalar positive factor is

    K(q)=(1-c²)[(1+q²-cq)²-q²]/N(q)²,
    Theta(1)=1, K(1)=Theta'(1)=(3-c)/(1+c).              (8)

At the original Golden point,

    K(1)=sqrt(5),
    f(q)=qTheta(q), f(1)=1, f'(1)=1+sqrt(5)=2phi.         (9)

f is the first-return AMPLITUDE generating function. Its derivative is a coherent amplitude moment, not a measured mean waiting time. The perfect terminal return has no value-level memory, but the retained marker-dependent response does. This is a response identity on the original word, not a new physical constant. Dividing (7) by 1-q² is not a free physical source normalization, and the singular full inverse must not be evaluated at q=1.

## 4. Separate monitored completion: exact complete occupation and price

A distinct declared process checks the existing preparation subspace after each full cycle, retains a fresh yes/no record and continues after no. This adds a monitor and a retained elapsed count; its physical admission, readout work and protection of earlier flags remain premises. It is not the unmonitored coherent loop or the old fifteen-step trial.

Set P=jj*, Q=I-P and V=QM. The unnormalized surviving state before cycle n+1 is V^n P(V*)^n. Unitarity yields the exact finite identity

    I-VV*=P,
    sum_(n=0)^(N-1) V^n P(V*)^n=I-V^N(V*)^N.             (10)

By (6), V has no surviving unit-circle sector. Its total occupation is therefore I4, giving

    Pr(eventual monitored return)=1,
    E(number of complete cycles)=4.                     (11)

This is a direct application of quantum Kac recurrence, not a new general theorem. The sixteen-stage closure therefore contributes64 expected encoded transitions before the additional monitoring operations. The identity programme returns in one cycle; its unused dark work space must not be incorrectly charged by assuming full cyclicity.

For a supplied positive one-cycle price effect C COMPATIBLE with this process,

    E(total supplied cycle price)=Tr_4 C.                (12)

This is an exact expectation identity, not permission to choose an arbitrary physical price or insert a measurement of C that changes the unitary evolution. A genuine success->0/failure->10 status code has C=2I-M*PM and expected total length7; a scalar full-cycle gate price g adds4g. The quantity4 in (11), the coherent moment2phi in (9), and a complete physical elapsed time are not interchangeable.

With unchanged spin and an arbitrary correlated spectator reference, the actual native M factors as M tensor I_spin,R. The occupation is I_arm,record tensor rho_spin,R; the effective logical price is Tr_arm,record C. It is scalar only when that true partial trace is scalar. Returned amplitudes are scalar on spin, preserving its conditional reference state. No general prepared-state source is erased by Lorentz equivariance.

A nonlinear prepared-state Info or history-dependent work is not automatically a fixed C. Its source remains. The measured price (12) and coherent determinant (4) cannot simply be added and called one physical action.

## 5. A uniform finite-cap FIRST-SOURCE bound for the existing gain-aware consumer

Let G4=sum_(n=0)^3 V^n P(V*)^n=I-V^4(V*)^4. Exact calculation gives det G4=(1-c²)^4, and Tr G4<=4. The arithmetic/geometric-mean inequality on the other three positive eigenvalues gives

    lambda_min(G4)>=27(1-c²)^4/64.

For |c|<=1/4, including the actual native p³,

    lambda_min(G4)>=eta0=1366875/4194304>1/4,
    ||V^4||²<3/4.                                       (13)

This weaker3/4 contraction also holds for ANY unitary M' with the same fixed P and

    ||M'-M||<epsilon0=(eta0-1/4)/8
                     =318299/33554432>0.00948.           (14)

Indeed, four-power telescoping bounds the power difference by4||M'-M|| and the Gram difference by8||M'-M||. Thus the bound is valid on a real open noncommuting unitary neighborhood, not only on an imagined scalar-parameter variation. Any physically admitted field must still map into that neighborhood through its genuine primitive dictionary.

Writing R_N=V^N(V*)^N, one gets for N>=8 and differentiable variations with P fixed,

    ||R_N|| <= (3/4)^floor(N/4),
    ||D R_N|| <= (8N/3)||DV||(3/4)^floor(N/4).             (15)

The derivative is the ordered sum of N terms; the bound follows from
floor(j/4)+floor((N-1-j)/4)>=floor((N-1)/4)-1. It assumes no commuting field derivative.

The finite-cap known cycle-price part is exactly S_N=Tr[C(I-R_N)] and S_infty=Tr C. Consequently

    |D S_N-D S_infty|
      <=4[||DC||+(8N/3)||C||||DV||](3/4)^floor(N/4).      (16)

Additional cap-abort price, moving preparation/cut, nonlinear Info and clock work remain explicit; bounded terminal effects have analogous tails, but entropy support births do not inherit (16) without further analysis.

For the original primary recovery theorem's real gain g_h, an admitted component satisfying (13)-(16) can have its history truncation error made o(g_h) by choosing N_h with the right side divided by g_h tending to zero. Polynomial field/norm/gain bounds require only N_h=O(log(1/h)). This is a bound for one specific actual price component, not proof of all42 compatibility, a selected clock, or full physical GR. It retains the previously emphasized real signal denominator.

## 6. What the integration supplies and does not supply

The chain is now explicit:

    original quaternion/Golden chronological word
      -> actual256 stage elimination (owned)
      -> computed work determinant N(q)^4 and transfer Theta (new)
      -> convergent work return and its full first source
      -> separately admitted monitored completion
      -> exact compatible price and uniform finite-source tail.

Unlike the earlier conditional paired-epoch construction, the first three maps use the literal published stage operator and actual work cut: no new shared clock/data tensor factorization or spectator heat lift is assigned. But they do not prove that the original one-tick Book action equals a sixteen-stage coherent loop statistic, nor that the primary CAR16/all128 heat operator has this arm/spin/record form.

The newest complete-price two-density, explicit-dynamics and protected-null recovery results remain valid independent consumers with their own price, field, gain and preparation hypotheses. They cannot be identified with (4) or (12) from matching dimensions or symbols. The remaining physical question is the SAME actual native programme/cut/Info/work/heat and field-writer or stationarity map, not another geometry search.

The original parent now has its requested work-archive remainder explicitly. Applying the construction to the real primary all128/cap2 word requires its own chronological blocks and cut; neither its source nor the unsolved preparation equations are silently replaced.

## 7. Validation

The companion `sources/d0_native_nested_return_source_2026-10-21/check_native_nested_return.py` was actually run normally and with python -O. Both outputs and RESULT.json are identical:63 checks pass. The script reconstructs both full16 native programmes exactly over Q[a]/(a^4+a²-1), derives the work/active determinants, defect, native sqrt(5), reachability and finite occupation, and the rational open-neighborhood bound. Numeric controls construct the actual full256 clock and an independent noncommuting first-source perturbation, and check the Golden first-return and finite-cap tails. Infinite statements are proved above, not extrapolated from400 terms.

The numerical skew perturbation is a matrix source control, not a newly admitted D0 gate. The original fifteen-step trial, sixteen-step closure and monitored repetition are distinct. No unchanged all128 spectral/geometry/Lean suite was rerun; independent review, remote CI, compulsory Book Info and physical GR acceptance are not claimed. GR_closed=false.
