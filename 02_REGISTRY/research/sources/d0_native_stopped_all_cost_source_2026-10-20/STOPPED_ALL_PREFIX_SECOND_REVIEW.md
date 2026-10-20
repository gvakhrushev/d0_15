# Independent review: every minimizing stopped Golden branch has a nonzero multiplier

Reviewer: `cost_variation`, read-only bounded subtask of existing PR #334.
Date: 20 October 2026. No repository or remote files were modified.

## Input and verdict

Reviewed upstream input:
`02_REGISTRY/research/A4D_PROSPECTIVE_STOPPED_GOLDEN_MINIMUM_SOURCE_REVERSAL_2026_10_20.md`
at commit `f22c1864bd85e097166abd75dc048164d8d63c65`, Git blob
`a0caf318769e2388857a5041395034b788da159d`.

**Accepted:** under the input's declared stopped component-price model,
for every real prefix price T >= 5, a minimum over all positive integers k
exists, and every minimizing branch has B_k > 0 and a nonzero scalar
coefficient multiplying Dt. The upper bound T <= 50 is unnecessary for
this nonvanishing result. It remains necessary for the separately stated
claim that the unique minimizing index is k = 2.

The argument below independently derives the new unbounded-T part. The
already proved input theorem, unique k = 2 on [5,50], supplies that compact
interval. No new finite scan or unproved numerical cutoff is used.

## Exact retained assumptions and price derivative

Let p = (sqrt(5)-1)/2, phi = 1/p, theta = arcsin(p), and
q_k = sin^2(k theta). The programme selects one fixed integer k >= 1 before
execution, applies the same actual fresh-work comparison until the first
port1, and retains every failure. Each attempt pays the field-independent
pre-report prefix T+k with one tick per Golden gate; the original reporter
uses the code 0/10. Information is the complete stopped pointer Shannon
entropy in phi units. The supplied native scalar probability first jets and
their uniform geometric tail bound are retained. There is no unaccounted
moving per-trial price or information source.

The resulting value and first jet at the common-null stratum are

    S_k(T) = [T+k+D_phi(Bern(q_k)||Bern(p^2))]/q_k,
    D S_k = -B_k q'_k/q_k^2 Dt,
    B_k = T+k+log_phi[(1-q_k)/p],
    q'_k = 4 cos(k theta) sin(k theta).

For an independent check of the derivative, if D(q) denotes the binary
relative entropy, then

    q D'(q)-D(q) = -log_phi[(1-q)/p].

Differentiating (T+k+D(q))/q gives exactly the stated source, including
the derivative of the expected number of paid attempts. At k = 2,
q_2=4p^3, 1-q_2=p^6, so B_2=T-3.

The assumptions are those of the input's defined component-price model.
This argument neither derives the compulsory stopping task from M1 nor
identifies pointer Shannon entropy with an unspecified full Book action.

## 1. No degenerate Golden branch

If theta/pi were rational, zeta = exp(2 i theta) would be a root of unity.
Every conjugate of zeta+zeta^(-1) would then lie in [-2,2]. But

    2 cos(2 theta) = 4p-2 = 2 sqrt(5)-4

has the conjugate -2 sqrt(5)-4 < -2. Therefore theta/pi is irrational.
Consequently, for every positive integer k,

    0 < q_k < 1,  cos(k theta) != 0,  sin(k theta) != 0,  q'_k != 0.

## 2. Algebraic norm supplies an all-k lower bound on failure probability

Put r_k=1-q_k=cos^2(k theta) and x=2p-1=cos(2 theta). Then

    r_k = [1+ChebyshevT_k(x)]/2.

This quantity belongs to Z[p], not merely to (1/2) Z[p]. Indeed x is
congruent to 1 modulo 2 in Z[p], and the recurrence
ChebyshevT_(k+1)=2x ChebyshevT_k-ChebyshevT_(k-1), with initial values
1 and x, gives ChebyshevT_k(x) congruent to 1 modulo 2 for every k.
Equivalently, r_0=1, r_1=p, and

    r_(k+1)=2x r_k-r_(k-1)+(1-x)

is a recurrence entirely in Z[p].

The other real embedding sends p to -phi and x to -phi^3. Write
eta=arcosh(phi^3)>0. The conjugate is

    r'_k = [1+(-1)^k cosh(k eta)]/2.

For even k it is cosh^2(k eta/2), and for odd k it is
-sinh^2(k eta/2). Thus it is nonzero and

    |r'_k| <= cosh^2(k eta/2) < exp(k eta).

Also eta < 5 log(phi). This can be checked without a numerical logarithm:

    cosh(5 log(phi)) = 5 sqrt(5)/2 > 2+sqrt(5) = phi^3.

The norm r_k r'_k is a nonzero rational integer. Concretely, the norm of
a+bp is a^2-ab-b^2. Therefore |r_k r'_k| >= 1, and since r_k>0,

    r_k >= 1/|r'_k| > exp(-k eta) > p^(5k).

It follows strictly that

    B_k = T+k+1+log_phi(r_k) > T-4k+1.                 (A)

This estimate holds for every k >= 1, independently of minimization.

## 3. A minimizing index cannot outrun the paid prefix

Relative entropy is nonnegative, and q_k<1, hence S_k(T)>T+k for T>=5.
In particular S_k(T) tends to infinity with k. A finite minimizer exists;
every minimizer satisfies

    k <= S_2(T)-T.

The right hand side is affine in T, with slope

    1/q_2-1 = p^3/4 < 1/4.

The upstream sharp endpoint S_2(50)-50<7 is enough. A weaker independent
endpoint avoids all logarithm enclosures for the new argument:

* D_phi(Bern(q)||Bern(p^2)) <= 2 for every q in [0,1], because the
  negative entropy is nonpositive and the two reference code lengths
  are 2 and 1.
* p>8/13, since (8/13)^2+8/13-1=-1/169<0 and the defining quadratic is
  increasing on the positive axis.
* q_2=8p-4>12/13, hence

      S_2(50)-50 <= 54/q_2-50 < 17/2 < 51/4.

The affine function (T+1)/4-[S_2(T)-T] is therefore strictly positive
at T=50 and has strictly positive slope. For every T>=50 and every
minimizer,

    k < (T+1)/4.

Combining this inequality with (A) proves B_k>0 for every minimizer and
every T>=50. On 5<=T<=50 the input's unique minimizer k=2 has B_2=T-3>=2.
Together these give the claimed theorem for all real T>=5.

## Exact interpretation and exclusions

Because q'_k != 0, every minimizing branch has

    -B_k q'_k/q_k^2 != 0.

Thus each such branch's first source is a nonzero scalar multiple of the
same inherited Dt=gamma_h D J_2. Its stationary covector vanishes exactly
where Dt vanishes. It would be incorrect to say that the covector itself
is nonzero at a stationary Einstein--CAR solution.

No all-T uniqueness is established. At an index tie, the assertion holds
separately for every minimizing programme. It does not assert equal signs
of their coefficients, differentiability of the lower envelope, or a
common first variation of that envelope. No uniform lower bound on the
absolute source coefficient as T grows is established either.

The result removes an upper compiler-prefix bound only from this
conditional nonzero-multiplier question. It does not remove the actual
stopping-task requirement, the assumed unit Golden-gate charge, the
pointer-Info choice, or the need to account for every additional moving
native price/record contribution. It does not prove that the compulsory
native prefix has the stipulated T or that complete GR is selected.

This is an analytical second review. The native-selector agent's separate
extension proof/checker was not available when the argument was reviewed;
its execution is not claimed here.
