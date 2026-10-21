# Quantitative paid resource writer and hidden Book-gain fibre

**21 October 2026.** Existing research owner #334. Status: independent finite algebraic derivations plus author-level reproducible checks. Not physical Book03 admission; `GR_closed=false`.

## I. New quantitative resource-writer theorem (same complete native gate grammar)

Consume `PROOF.md` §2: if U_a∈O(d), d=2^q, a∈{1,…,A}, has **rational** entries and R clears all entry denominators, the full coherent Golden/CNOT writer has successful Kraus corner `K_s=(R/(dB)) direct_sum_a U_a`, `B=2^{ceil(log2 R)}`. Its complete failure effect is `(1−s)I`, `s=R²/(d²B²)>1/(4d²)`, including all protected oldRIGHT. This theorem keeps the full quantum failure record unmeasured, with only the aggregate herald classically registered. Native H/Toffoli factories have their own true success/failure tape and are charged.

**Strengthening (explicit common-denominator bit bound).** For ANY finite list of A real orthogonal d×d target matrices and any 0<ε<1, there exist rational orthogonal approximants U_hat_a with

`max_a ||U_hat_a−U_a||_op ≤ ε`, a single integer R clearing ALL entries, and

`bitlen(R) ≤ 1 + A d(d−1) [1+2 log2 ceil(2d(d−1)/ε)]`.

Proof: Givens reduction expresses an O(d) target as at most d(d−1)/2 plane rotations and exact diagonal signs. Split each plane angle into two half-angle rotations; there are at most m=d(d−1) factors. Each split angle lies in [−π/2,π/2]; its tangent half-angle parameter r lies in [−1,1]. Round to k/Q with Q=ceil(2m/ε). Its exact rational entries are `(Q²−k²)/(Q²+k²)` and `2kQ/(Q²+k²)`, so every factor is EXACTLY orthogonal and has denominator ≤2Q². The rotation map is 2-Lipschitz in r, and nearest-grid rounding gives error ≤1/Q per factor. Product telescoping therefore bounds total operator error by m/Q≤ε/2. Set R equal to the product of the denominators over every factor and every address. Each entry of every full approximant has denominator dividing R, and the bit bound follows by taking logarithms. Exact sign flips do not affect R. No measurement, postselection, selected state or arbitrary quantum angle gate enters the mathematical approximation.

The signed integer tables use `A d² (bitlen(R)+2)` retained bits; a direct reversible lookup/comparator circuit uses polynomially many Toffoli/CNOT operations in A,d,bitlen(R). The writer's success `s>1/(4d²)` is independent of A and ε, despite the potentially enormous VALUE of R. Thus for fixed d=16,32 and finite address list, accuracy demands **polynomial circuit size in A and log(1/ε)**, not an exponential-length cost caused by clearing denominators. This is an upper bound, not a practical optimizer or an unpriced compilation oracle: the classical process computing the matrices/tables and all native factory, clock, work and controller resources must be physically supplied and paid.

A finite common table set may be compiled from stipulated numerical field values, but that does **not** make an exact C¹ field-to-controller map from ONE physical D0 initial state. A finite or countable set of fixed words is not an open field chart. The result controls achievable finite value/source stencils under an explicitly supplied compiler, as in `PROOF.md` §7. It does not select the compiler or its Book03 gain/loop evaluation.

**Independent targeted check.** `check_uniform_compiler.py` verifies three full O(4) targets through twelve exact rational rotations each, a common 819-bit denominator, exact matrix orthogonality, operator error and the lower bound on complete herald readiness. This is a finite witness, while the stated bound follows for all finite A,d from the argument above.

## II. New exact no-shortcut theorem: mean information does not identify Book amplitude curvature

This is a separate but essential source-selection control. Let a positive full native record have probabilities q_i and orthogonal recorded branches, and suppose the **baseline** Book amplitude weights are correctly aligned:

`w_i(0)=a sqrt(q_i)`, `a>0`.

For ANY real vector v with `Σ_i q_i v_i=0` (a mean-preserving branch-gain tangent), define candidate Book gains

`I_i(f)=I_i(0)+f v_i`.

The literal expected gain `Σ q_i I_i(f)` remains EXACTLY constant, as do all actual native Kraus outcomes, probabilities, oldRIGHT and counted charges; we have changed only the proposed **Book gain map**, not the execution. The corresponding Book quadratic-record norm obeys

`N(f)/N(0)=Σ_i q_i exp(2 ln(phi) f v_i)`.

Consequently:

`D_f[-log_phi(N(f)/N(0))]_(f=0)=0`,

`D_f²[-log_phi(N(f)/N(0))]_(f=0) = −4 ln(phi) Var_q(v) < 0`

whenever v is nonconstant. Proof: differentiate the finite exponential sum twice, normalize N(0), and use E_q v=0. This is a strict negative Hessian on the (number-of-positive-branches−1)-dimensional invisible-to-mean gain fibre. It is an **alternative mathematical Info assignment**, not an actually admitted physical variation or a claim that Book03 freely permits arbitrary gains. If equality of the full normalized Book amplitude vector with the native coherent record is required *throughout a neighborhood*, all such nonzero tangent deformations are rejected. Matching just the mean Shannon gain, even exactly for all f, is not enough.

### Exact original two-Golden-port witness

On every original nonblank k, `(q0,q1)=(p²,p)`, `p=phi^-1`, and charges `(C0,C1)=(1,2)`. Its Shannon value is `H_phi(q)=2p²+p=2−p`.

Choose baseline branch gains

`I0(0)=H_phi(q)−3p/2`, `I1(0)=H_phi(q)+3p²/2`.

Both are positive. They have literal mean `H_phi(q)` and relative gap `I1−I0=3/2`, so the baseline absolute-amplitude branch **ratio** agrees exactly with the original native port amplitudes. Now change

`I0(f)=I0(0)+p f`, `I1(f)=I1(0)−p² f`.

Because `p+p²=1`, the mean gain stays exactly `H_phi(q)` for all sufficiently small f, while the native record stays unchanged. Yet the normalized Book port1 probability has derivative

`D_f q1^Book(0) = −2 p³ ln(phi) !=0`,

and its log-quadratic-response action has

`D_f² [−log_phi(N(f)/N(0))]_(0) = −4 p³ ln(phi) <0`.

Thus the actual same-record `Cost−mean Shannon Info` can agree exactly for an entire family of candidate gains while the Book **amplitude/second-source** differs. A common absolute normalization does not repair this relative mismatch. At the matched baseline the first log-norm jet happens to vanish, so even matching first derivatives AT ONE POINT does not fix the second source. This is stronger than a bare common-scalar ambiguity, but it is not a no-go for Book03: Book03 might fix the branch gains through its own full memory/Info rule. That rule must be derived, not silently substituted by a mean.

**Independent exact check:** `check_gain_fibre.py` reduces all identities symbolically modulo `p²+p−1`, including the exact coefficient `p³=2p−1`. Both normal Python and `python -O` pass.

## III. Combined decision for the existing #334 main route

- The **conditional physical-preparation premise** of the fixed processor has a constructive finite Golden/CNOT candidate with protected RIGHT, all failures and paid counted-CQ entropy, now with an explicit polynomial upper bound in precision and address count. The parent fixed-processor/weighted-source results are consumed unchanged.
- The **actual common complete initial controller** and its physical field-dependent code generation are not selected. A finite family of separately compiled instructions is not a smooth executed variation. A fixed selector over the family instead yields a paid selector mixture and its own source. Those cannot be identified without one actual same-history map.
- **Book03 amplitude weights are not determined by the expected CQ entropy**, even if all branch charges and mean gains match; the hidden gain-fibre example proves that stronger negative statement. Book's actual ordered-memory and quadratic response must decide the admissible branch map, including its first/second variations and absolute fixed-z loop normalization.
- The **physical 42-source test** and independent upstream equations remain open, as does original RAW-216 mesh refinement. No GR promotion is justified by the resource writer or hidden gain theorem alone.

The next valid calculation is not another observer or detector: run the *literal complete Book03 valuation on the same supplied paid writer+processor execution*, including its branch gains and memory classes, and compare the resulting full source with the already-proved conditional CQ source. Any missing branch gain must be labelled an unselected physical input. No fitted Info, compensating source, or revised action is allowed.

`GR_closed=false`.
