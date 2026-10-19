# D0 → GR: native Golden preparation has a unit entropy defect and an exact code-pressure stationary completion

19 October 2026. **PHYSICAL-SOURCE RESEARCH / exact finite original-AF preparation test / NOT a new GR action / same Draft #381 consuming #334.** Pin upstream #334 at `bf9bc75ec13590991ea50799f3c90f5a17295a92` for this intake (the PR can move). Reuses [the actual Golden full binary return / old RIGHT preparation](A4D_MINIMAL_GOLDEN_MODAL_PF_RETURN_AND_BOOK_AGGREGATION_SEAM_2026_10_19.md), [the full Book same-history information normalization](A4D_COMPLETE_HISTORY_INFORMATION_SCALE.md), [the code cocycle](A4D_NATIVE_BRANCH_INFORMATION_COCYCLE.md), [partition correction](A4D_NATIVE_PARTITION_CORRECTED_BRANCH_INFORMATION.md), [C_Y response preservation](A4D_CY_RESPONSE_PRESERVING_CAPACITY_BOUNDARY_2026_10_19.md), [native full preparation fiber](A4D_NATIVE_FULL_PREPARATION_FIBER.md), and [the scene Book pressure](A4D_SCENE_PERRON_DOOB_SINGLE_HISTORY_GOLDEN_INFO_SOURCE_2026_10_19.md). No new geometric jet or action is selected. `GR_closed=false`.

## 1. ORIGINAL, not reweighted, two-sector finite AF probabilities

On the matched old LEFT/RIGHT Schmidt carrier for AF level N≥1, use the actual unchanged canonical preparation:

```text
n0 = F_(N+2), n1 = F_(N+1), p=phi^-1
mu_i = p^(N+1) for i∈type0; mu_j=p^(N+2) for j∈type1
C_i = N+1 for type0; C_j=N+2 for type1
n0*p^(N+1)+n1*p^(N+2)=1
mu_i=phi^(-C_i), mu0/mu1=phi.
```

This is the original old RIGHT/PF law. It is **not** the ordinary J₂ regular-trace Born weight. Keep the original matched normalized pure state `|Psi(mu)>=sum_i sqrt(mu_i)|i>_L |i>_R`, all original addresses and both registers.

On the common null/star return root the full *binary* conditional output `good/failure` of the one native k-Golden filled-return event has the same probability `g_*` for every address; thus its complete joint law is `q_(i,+)=mu_i g_*, q_(i,-)=mu_i(1-g_*)`. Both outcomes are explicitly retained.

## 2. Exact physical test: free Schmidt-preparation sector transfer has entropy first source -1

Let A_N=n0 p^(N+1), B_N=n1 p^(N+2), A_N+B_N=1. Redistribute **whole sector masses**, not one exponentially rare address, by

```text
mu_i(t)=mu_i (1+t/A_N) for type0;
mu_j(t)=mu_j (1-t/B_N) for type1,  -A_N<t<B_N.
Psi(t)=sum_i sqrt(mu_i(t))|i>_L |i>_R.
```

This is a smooth normalized complete pure LEFT/RIGHT matched-state path; it keeps all basis words and both registers. It CHANGES the old RIGHT eigenvalues, so it is **excluded** by an independently immutable old RIGHT preparation contract. It tests the alternative genuinely free preparation domain and is not automatically an admissible physical D0 variation.

At the null/star common `g_i=g_*` and fixed conditional instrument, the exact complete pointer entropy is `H_phi(Y,+/-)=H_phi(mu)+h_phi(g_*)`. Its genuine preparation derivative is

```text
D_t H_phi(Y,+/-)|0 = log_phi(mu_type1/mu_type0) = -1,
```

independent of N, k, h, Einstein matter coupling or site weights. This is the exact one-Golden-cost mismatch of the full **mean** pointer source on a free preparation fibre, not a local metric Euler obstruction.

### Crucial norm correction / uniform physical strength

A transfer between one pair of rare addresses has GNS derivative norm growing like phi^(N/2): its nonzero probability-coordinate derivative alone is NOT uniform. The all-sector path above repairs that loophole:

```text
||Psi'_N(0)||² = 1/4 sum_i (Dmu_i)²/mu_i
               = 1/4(1/A_N+1/B_N) = 1/(4 A_N B_N).
A_N→phi/sqrt(5), B_N→1/(phi sqrt(5)), A_N B_N→1/5.
||Psi'_N(0)||→sqrt(5)/2,
D_(unit-GNS direction) H_phi → -2/sqrt(5) != 0.
```

Thus the full entropy prep force persists on a **bounded-norm native GNS tangent** at arbitrarily deep refinement, IF that free LEFT/RIGHT sector-mass direction belongs to the physical admissible preparation tangent. This is conditional; fixed RIGHT forbids it and is still not physically forced upstream.

## 3. One primitive code cost cancels the force exactly—but only under a specified variational principle

The exact original Golden code length differs by one between the sectors. Along the same tangent:

```text
D_t E_mu C = (N+1)-(N+2) = -1.
D_t [H_phi(mu)-E_mu C]=(-1)-(-1)=0.
```

In fact for **every** positive normalized preparation nu over the same original labelled AF leaves, the *mathematical code-pressure functional* is

```text
F_code(nu)=H_phi(nu)-sum_i nu_i C_i
          = -D_phi(nu || mu) ≤ 0,
F_code(nu)=0 ⇔ nu=mu.
```

The native canonical original `mu` is therefore the UNIQUE full-simplex optimizer of original code entropy minus original expected code price with coefficient **exactly one**. The coefficient is not tuned to Einstein. This is the standard exact finite Gibbs/Kraft variational identity for the code reference `mu_i=phi^(-C_i)`; it DOES NOT prove that Book03 or true D0 stationary preparation uses `F_code` as the complete physical action. The original Book `Cost−Info` is not automatically `H-E C`.

## 4. Conditional joint native binary task: strict preparation selection + unchanged Einstein source

Let the complete binary return conditional probabilities vary with actual fields y and set `h_i(y)=h_phi(g_i(y))` for the specified measuring task. On the original SAME leaf labels define the **test** pressure (again, not promoted to native action)

```text
F_task(nu,y)=H_phi(nu)+sum_i nu_i h_i(y)-sum_i nu_i C_i
           = -D_phi(nu || mu)+sum_i nu_i h_i(y).
```

It has a UNIQUE exact maximum on the full positive normalized simplex:

```text
nu_i^*(y)=mu_i phi^(h_i(y)) / Z(y),
Z(y)=sum_i mu_i phi^(h_i(y)),
max_nu F_task=log_phi Z(y).
```

At the common null/star point, all `h_i=h_*` and hence `nu^*(y_*)=mu` **without imposing fixed RIGHT by hand**. By the envelope identity, for all eligible geometric+CAR tangents V,

```text
D_y max F_task|_(y*)[V] = sum_i mu_i Dh_i(y*)[V]
   = [2*g_* ln(g_*/(1-g_*))/ln(phi)] sum_i mu_i DJ_i[V].
```

This is EXACTLY the already-owned fixed-oldRIGHT two-outcome source up to the existing regular-vs-PF factor on source-bearing READY class0. Thus this conditional task pressure has both a unique preparation optimizer and the desired geometric+matter first source, without fitting the matter/Einstein ratio. It can supply a precisely specified **physical theorem target**.

**Crucial non-equivalence**: the conditional task pressure is not demonstrated to equal the Book03 whole action, and simply adding a code term to the measured mean action is forbidden without proving it belongs to the SAME native Cost−Info/verification history. The new result is an exact interface/necessary comparison, not selected physics.

## 5. Exact full Born-partition boundary: why the normalization cannot be used as the missing gravity action

If a single complete instrument defines `w_(i,+)=mu_i g_i(y), w_(i,-)=mu_i(1-g_i(y))`, then for every y:

```text
N_Born(y)=sum_i (w_(i,+)+w_(i,-))=sum_i mu_i=1,
D_y log_phi N_Born=0.
```

Thus its **raw scalar log-partition** has NO Einstein field source. Yet the expected same-history Book surprisal `E_q[-log_phi q]=H_phi(q)` has a nonzero known `DJ_i` source. These are distinct statistical objects. A claim that one normalization both equals 1 by complete Born trace preservation AND generates the nonzero gravitational source through `D log N` is impossible for this instrument. The previously owned general scalar Book raw normalizer `N` is not set to 1 unless its weights are **actually the same complete Born outcomes**. If the binding `w=q` is admitted, `D log N=0` is correct, and the mean entropy still has the conditional source and free-preparation defect.

Moreover `F_task` is *not* the log partition of this normalized Born instrument: `Z_task=sum_i mu_i phi^(h_i)` is a different ensemble. Claiming its physical force requires identifying its native execution and price, not simply relabelling its mathematical optimizer.

## 6. The **one** decisive physically owned next statement

Compare the genuine native full `H+J+R+Book` cost for the **same executed old-LEFT/RIGHT/ref128/CAR/clock binary word** with the full joint tangent. The following must be independently owned:

1. Either immutable RIGHT preparation is **dynamically forced**, excluding the all-sector tangent, or the complete physical source in this tangent carries +1 golden unit (per t) to cancel the mean Book entropy; the correct metric is the finite GNS norm, not an arbitrarily fixed probability-coordinate displacement.
2. If selecting the `F_code/F_task` pressure route, derive its *absolute* expected code contribution and optimization sign from the ORIGINAL physical Book and work/cost law—do NOT insert `-E C` into `H(q)` as a free counterterm. Prove it uses the same full retained labels, clock and controller with physical admissibility.
3. Then replay the complete 40+matter+prep+clock first covector, and preserve the existing raw #216 fixed-source terminal and refinement requirements. A root of a merely prescribed `F_task` is not a physical D0 joint root.

The exact companion [finite checker](sources/d0_physical_binary_return_2026-10-19/check_d0_physical_golden_preparation_pressure.py) tests the two-cost identity, whole-sector GNS norm, entropy gradient, code-pressure cancellation, conditional envelope and the normalized Born log-partition no-source boundary. `GR_closed=false`.
