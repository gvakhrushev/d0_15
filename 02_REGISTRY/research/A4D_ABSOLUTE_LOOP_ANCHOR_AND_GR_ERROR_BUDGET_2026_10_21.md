# Absolute loop calibration and the GR source error budget

21 October 2026. Two bounded compositions in existing PR #334,
EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE,
constitutive/native-programme-v1. Phase: native realization and recovery
composition. Local input snapshot 9fb8018fc2d1c7ce671f4a1d5ab1640ecacb8b61.
Write paths are this proof and its checker/receipt in the existing
source_selection/metric directory. No separate execution is opened.

The first result is an inverse theorem for the independently ASSUMED family
F=aF0, with an explicit full first derivative. It is not an identifiability
theorem for the original full128 Book execution. The second propagates
errors in that conditional family to the already-owned normal-row GR
recovery, subject to its actual source support and gain. Neither result
supplies the native information law or its measurement for free.

## 1. Recovering a common weight from one absolute loop jet

The [corrected scalar-weight note](A4D_BOOK03_SOURCE_IDENTIFIABILITY_THEOREM_2026_10_21.md)
proves only the fixed-representation graph statement. Its former universal
claim about the full physical source has been withdrawn. Independently
suppose a particular actual carrier really supplies a KNOWN finite-dimensional
Hermitian F0(y)>=0, F0!=0, and feedback F=a(y)F0(y), a>0. This
factorization and its phase/amplitude typing are hypotheses requiring an
actual application; relative scalar branch ratios do not prove them.

In the [actual full128 normalized complementary determinant](A4D_FULL128_NORMALIZATION_AND_TRUE_BOOK_SOURCE_2026_10_21.md),
W->WL for an invertible input-coordinate L leaves the value and full
source invariant. In particular W->aW does NOT supply F->aF. A physical
attenuation with its retained failure changes the actual return corner
and gives F'=I-A'*A', rather than aF. Thus the theorem below cannot
repair that original source by fitting a scalar normalizer. Its inverse
has no application there without a separately proved different map.

For the original r=128, fixed physical z>0, and an ADMITTED interval
where I-zaF0 is positive, put

    L(a,y)=-r logdet(I-zaF0),     R=(I-zaF0)^(-1),
    chi=partial_a L=r z Tr(R F0)>0.                     (1)

Therefore a->L is strictly increasing and invertible on its actual
admissible image. An actual absolute value L fixes exactly one a there.
The physical contraction constraint aF0<=I, when required, restricts
that image; an arbitrary desired L is not assumed admissible.

All moving-cut, reference, preparation and field derivatives belong in
dF0. Direct determinant differentiation gives, without assuming
[F0,dF0]=0,

    dL=r Tr R[za dF0+z F0 da+a F0 dz],
    da={dL-r Tr R[za dF0+a F0 dz]}/chi.                 (2)

Thus one independently supplied absolute loop VALUE AND FULL JET,
together with the known relative operator jet and physical z,dz,
reconstructs the missing common scalar and its jet. One scalar jet has
components on all 42 field directions and every genuinely independent
internal direction; it is not one numerical slope.

Since R>=I on this positive chart,

    chi>=r z Tr F0,
    |a-b|<=|L(a)-L(b)|/(r z Tr F0).                    (3)

Equation (3) is an explicit conditioning bound at fixed y,F0,z. It is
lost at F0=0. On a non-Hermitian coherent return the monotonicity argument
is unavailable. A normalized readout provides no absolute L. A total
price S=L+K supplies L only after the ENTIRE actual K and dK are known.
These are necessary physical limits of the inverse, not new fitted
values of Book Info or a permitted rescaling of z.

## 2. A complete first-source error bound for that common mode

Keep the relative operator F0 and its physical derivative exact. Let a
be the actual anchor and b an independently obtained approximation.
At fixed z assume both resolvents have the SAME positive lower margin

    I-zaF0>=delta I,   I-zbF0>=delta I, delta>0.

For a unit admitted physical tangent V, put D=D_V F0, s=D_V a,
t=D_V b, and E(a,s)=r z Tr[R_a(a D+F0 s)].
The exact noncommutative identities needed are

    a R_a-b R_b=(a-b)R_a R_b,
    R_a-R_b=z(a-b)R_a F0 R_b.                           (4)

They use that both resolvents are functions of the SAME F0; D need not
commute with it. Trace duality and positivity yield

    |E(a,s)-E(b,t)| <= r z {
      |a-b| ||D||_1/delta^2
      + (Tr F0/delta)|s-t|
      + z Tr(F0^2)|a-b| |t|/delta^2 }.                 (5)

Here ||D||_1 is the trace norm on the actual full fibre. Taking the
supremum over the original tangent norm gives a bound for the full
covector. No division by the number of clock, CAR or oldRIGHT modes
is made. Moving-z errors and errors in F0,dF0 require their additional
terms from (2); they are not covered by pretending z or the cut is fixed.

This bound converts actual anchor uncertainty into a source uncertainty.
It does not bound other paid heat, Info, preparation or work contributions.
Their genuine residual must be added before using a dynamical theorem.

## 3. Composing the anchor budget with the actual primary source gain

Consume the [primary normal-row recovery](A4D_PRIMARY_NORMAL_SOURCE_RECOVERY_SYNTHESIS_2026_10_21.md)
and its gain-aware application in
[the positive case](D0_GR_PRIMARY_POSITIVE_CASE.md).
Let the SAME admitted full source have nonzero configured gain g_h,
|g_h|>=g_min,h>0, and let a_J,h be the original J2 coefficient.
All extra ambient and independent internal rows must vanish throughout
the admitted closed field ball, except the original normal coframe row.
Let e_h bound that remaining COMPLETE normal-row error, including (5)
and every other actual source term.

The owned Dirichlet inverse and Brouwer argument then give exact finite
stationary representatives with

    ||H_nat-H_configured||_infinity
       <= h e_h/(4 |a_J,h| g_min,h),                   (6)

provided the displayed bound fits inside that same admitted field ball.
Continuity suffices; no entropy C2 or positive field Hessian is required.
The actual source gain is kept.

For O(h^2) profile recovery it is sufficient that

    e_h=O(h |a_J,h| g_min,h).                           (7)

For illustration ONLY, if |a_J,h| stays bounded away from zero and the
actual gain scales as h^4 because its actual query dimension scales as
h^(-4), then e_h=O(h^5) suffices. This is not a universal D0 gain:
the newer local-report construction and other native executions retain
their own readiness, trace-copy counts and normalization.

For the specific two-forward-copy Route B report-to-Book construction,
the original covered spatial reporter has W>=528 L^4 actual copies, and
the coherent/purified uniform-address selector occupies the full work
carrier, so D>=W. Its exact declared-interface source gain therefore
satisfies g_h<=C h^8/gamma_m, with the fixed C given by
[the Route B refinement proof](sources/d0_native_book_reflection_bridge_2026-10-21/FORWARD_BELL.md#7-refinement-bound-from-the-actual-spatial-address-register). The paid moment writer can choose finite caps with
gamma_m>=1/2; selector admission and any extra selector readiness remain
separate premises. Under the same-source hypotheses above, the owned
sufficient O(h^2) recovery tolerance is e_h=O(h |a_J,h| g_h), hence no
looser than O(h^9 |a_J,h|) for this Route B interface. This is a
route-specific sufficient error target, not a universal gain law or a
necessary condition for other recovery theorems.

A non-normal component of the scalar anchor jet, however small, can
invalidate the hypothesis of (6). In particular a common gain is ONE
scalar function but its derivative is an unrestricted covector. It
cannot be renamed a purely normal perturbation. If this support test
fails, the actual coupled field/internal system must be solved.
Equation (6) controls the stated profile norm and the owned transverse
energy consequence, not the raw216 h^(-2) all-ten response norm.

## 4. The next same-execution calculation

The [causal clock and stationary descent synthesis](A4D_CAUSAL_CLOCK_MINIMUM_AND_STATIONARY_SOURCE_DESCENT_2026_10_21.md)
and the recovery bound have a common consumer: the actual Book
field-to-instrument map. First determine its genuine complementary
operator and complete source from that execution. Use (1)-(5) only if
the independent F=aF0 hypothesis actually holds. Otherwise retain the
true operator normalization, return, input and work derivatives and use
the resulting full residual directly in the support test for (6)-(7).

The absolute anchor is not supplied by this inverse, normalized history
statistics, or an Einstein target. The native physical continuation and
stationary/constraint law, independent preparations and the common
execution map remain required. GR_closed=false.

The [exact checker](sources/d0_native_gr_completion_synthesis_2026-10-20/source_selection/metric/check_absolute_anchor_budget.py)
uses noncommuting rational matrices, the original z=2^-20 as well as a
second diagnostic regulator, a moving-z negative control, the exact
resolvent identity, rational error bounds and the h^5 gain control.
Its [receipt](sources/d0_native_gr_completion_synthesis_2026-10-20/source_selection/metric/ABSOLUTE_ANCHOR_BUDGET_CERTIFICATE.json)
is a finite algebraic check; the all-mesh implication is the analytic
composition above with the owned recovery theorem.

The original normal and optimized author runs produced byte-identical
27-control output, SHA256
`7a96bfab31536bac49ad59daddae13803045be17802eadebb000fa2b4c53d645`.
After reading the corrected owner in published 43adff71, this note
explicitly withdraws any automatic physical application of F=aF0 and
updates that input pin. The unchanged conditional algebra is replayed
on the corrected inputs; its current receipt is linked above. Historical
evidence remains in f7a8a534. Independent acceptance and physical
valuation remain open.

Corrected-input replay: 27 exact controls pass in normal and `-O` mode,
matching the saved receipt with stdout line endings normalized and no stderr.
Current receipt SHA256:
`799385c72d1ed15c28cfac6bd7c583f76394e51213cac7b097ff7038ebfa54a6`;
checker SHA256:
`f73cf3afb3ed05291288173145283e7c06cea91bf9d9476091478036a41b4d13`.
The changed pin was reviewed together with its actual complementary-source
correction; it is not treated as evidence that F=aF0 holds there.
