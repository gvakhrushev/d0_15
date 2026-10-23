# Independent review of balanced native preparation

21 October 2026. Reviewer: the bounded compiler/native-admission assistant
within existing PR #334. No coauthor files or repository files were edited.

Reviewed draft:
`/workspace/scratch/07af0e1491e7/prep_notes/BALANCED_NATIVE_PREPARATION.md`

Reviewed SHA256:
`7b9d3afe684f34695a4dfd6d89a8db457ba9cf47002733c65e9a2dc5c5751d68`

## 1. Verdict and exact scope

**PASS analytically for the stated local, fixed-mesh, continuous-chart
theorems**, conditional on the inherited active-support certificate and
the same original full128 coherent conditional-entropy functional.
Sections 3 and 7 supply the required new applications: relative strong
convexity after moving both arms, and preservation of the complete field
Hessian at every selected-material-source-zero point. Neither is obtained
by differentiating the old little-o value asymptotic.

The previously requested C2 regularity clarification is incorporated in
the final draft's sections 8--9 and accepted. The added explicit interior
anchor-section condition and parity-specific expansion boundary are also
correct. Section 5 below records why the weaker C2 gradient bound suffices.

This review does not identify the coincident-arm action with J2, prove a
GR root for it, transfer it to the different N=1 CQ cut, derive physical
Book selection, or show that arbitrary real angles are attained by a
finite native word. All those boundaries are correctly retained in the
draft. The independently replayed focused checker and exact artifact
hashes are recorded in section 7; no historical geometry/rank suite was
repeated.

## 2. The coordinate and small-cluster calculations type-check

The populated 14/15 plane is exactly closed under each full rank-eight
generator; all its other planes are retained and have zero amplitude in
this preparation dictionary. With c fixed,

    b=R sin(theta), d=R cos(theta), db/dtheta=d>0.

Thus shifting theta by a is exactly the actual matrix action, and
`mu=theta+p^2 a, delta=a` is an invertible coordinate change when the
selected b rows are genuine free interior material coordinates. It is
not available for a prescribed anchor or a fixed boundary value.

For both arms the selector rotation sends the actual amplitude to

    V=[Xbar, sqrt(p^3)(X_+-X_-)],
    Xbar=p X_-+p^2 X_+.

At coincidence `V0=[X,0]`. Its relative derivative is
`V1=[0,sqrt(p^3)Y]`, with `Y=L sum_w v_w J_w C`.
Writing `G=X*X`, differentiation of the separated new-cluster projector
gives the off-diagonal block `-G^-1 X* sqrt(p^3)Y`. Therefore

    D_delta(V E_new)|0=[0,sqrt(p^3)(I-P)Y],
    P=X G^-1 X*.

This proves equation (5) using only the old faithful inverse. The
coherent selector's new kernel is never inverted.

At vacuum the populated masks 1 and 14 have odd CAR parity, while
`J_w C0` occupies mask15 and is even. Each original Kraus leaf has
definite parity, so the projected overlap vanishes leaf by leaf.
Completeness then gives

    Q(v)=p^3 ||sum_w v_w J_w C0||_HS^2
        =p^3 [p^2/(2*128)] sum_w v_w^2
        =(p^5/256)||v||^2.

Disjoint site supports remove cross terms. This verifies the stated
coefficient and its uniformity in the parity-preserving finite geometric
chart. Continuity supplies the small-material lower bound; it does not
supply a mesh-uniform bound.

## 3. Relative strong convexity through new ranks

For `f_eta(s)=-s^2 ln(s^2+eta)` and
`u=s^2/(s^2+eta) in [0,1]`, direct differentiation gives

    f_eta''=-2 ln(s^2+eta)-10u+4u^2,
    f_eta'/s=-2 ln(s^2+eta)-2u.

Both exceed `-2 ln(epsilon^2+eta)-6` on the small singular-value
ball, because `(1-u)(6-4u)>=0`. The even scalar function minus
the corresponding positive quadratic is convex and nondecreasing on
nonnegative singular values; equivalently, all the spectral Hessian
divided differences have that lower bound. Hence the matrix amplitude
entropy is strongly convex on this ball.

The nonlinear composition introduces the additional term

    <grad E_eta(Z), D_delta^2 Z[v,v]>.

The analytic spectral projector bounds the second factor uniformly.
For sufficiently small amplitudes, `s |ln(s^2+eta)|` is bounded by a
constant times `R(1+|ln R|)`, uniformly as eta tends to zero. Thus this
term cannot cancel the logarithmically increasing positive quadratic
term from `||D_delta Z[v]||_HS^2>=nu||v||^2/4`.

The old separated cluster contributes only bounded smooth curvature.
Integration on line segments gives a fixed positive strong-convexity
constant for the chosen sufficiently small ball, uniformly for small
eta. Passing to the actual continuous entropy preserves this inequality.
The C1 amplitude limit has the exact zero relative derivative at
delta=0 because both arms move with weights cancelling to first order.
Consequently zero is the unique relative stationary point and minimum.

This argument checks both possible failure points: matrix singular-value
convexity rather than scalar eigenvalue differentiation, and nonlinear
amplitude-composition curvature rather than an unjustified direct
convexity claim in delta.

## 4. All-source-zero Hessian preservation

The inherited separated-cluster expansion may be centered at any nearby
point, not only at vacuum. For `r_a=|a|`, write

    Z(y,a)=r_a Zhat(y,a/r_a,r_a).

Analyticity makes Zhat and its y derivatives bounded uniformly over
the compact angular set. Also

    ||Z||_HS^2=Q_y(a)+O(r_a^3),

with the same y-derivative estimate. The entropy of Zhat and its first
amplitude derivative are bounded on bounded sets, including new zeros.
Therefore the residual `r_a^2 E(Zhat)` and its y derivative are both
O(r_a^2); the additional `O(r_a^3 ln r_a)` term has the same bound.
The old cluster has an ordinary uniform Taylor expansion. This verifies
both bounds in (15), including the important parameter derivative.

At a point y* with s(y*)=0, uniqueness gives a*(y*)=0. Comparing the
minimizing value with a=0 yields, after shrinking the chart,

    |a*(y)| ln(1/|a*(y)|) <= C |s(y)|.

Since s is differentiable, `s(y*+h)=O(|h|)`. Inverting the increasing
small-radius function gives

    |a*(y*+h)|=O(|h|/ln(1/|h|)).

The complete gradient difference then has the bounds

    (D_y s).a* = O(|h|/ln(1/|h|)) = o(|h|),
    (D_y Q)(a*) ln(1/|a*|^2) = O(|h|^2/ln(1/|h|)) = o(|h|),
    D_y R = O(|a*|^2) = o(|h|).

No assumption that `D_y Q` vanishes at the nonvacuum point is needed.
The envelope identity therefore proves differentiability of the full
reduced gradient at y*, with Hessian exactly equal to that of A0.
This is stronger than a second value expansion along a ray. It does
not assign a finite preparation Hessian or claim neighborhood-wide C2
regularity.

The exact balanced coordinate map then proves the two critical-set
equalities in sections 4--5. The explicit source identity

    s_w=p^2 d_w partial_(b_w) A0

has the correct positive slack d_w, rather than R_w. It also shows why
the selected preparation source is zero at every genuine full root,
without assuming that a prescribed waveform is such a root.

## 5. Source, price, and regularity caveats

The original counting/central-gain price has precisely the stated form

    Price_count=A-log_phi(2)-log_phi(64) E T,
    E T=1+Tr(B rho B*).

At cap2 this is a smooth linear functional of the same actual density,
plus the same coherent entropy. Equation (2) therefore cancels its
relative derivative at coincidence. Its own material source must be
included in s and A0; a second port-cost term cannot be appended.

A genuinely smooth `W(g,c,rho)` passes this test because it depends on
the selected angles only through the same rho. A generic upstream
`U(y,a)` passes only if

    U_a-p^2 d U_b=0

throughout the relevant coincidence section. The displayed hostile
anchor-only term generally fails it. The theorem thus retains rather
than suppresses genuinely independent preparation, material, clock or
work sources. A different information cut or a negative newborn-entropy
term is outside the bounded-curvature extension.

**Accepted regularity clarification.** For the C2 upstream U of section 9,
Taylor's theorem gives a value remainder O(|a|^2), but in general not
`D_y R_U=O(|a|^2)` without another derivative or a suitable Lipschitz
mixed derivative. This does not invalidate the conclusions. C2 implies

    U_y(y,a)-U_y(y,0)=O(|a|)

uniformly on a smaller chart, which is already o(|h|) at the minimizing
angle above. Strong convexity uses only bounded second relative
derivatives, and the value comparison uses only the quadratic value
remainder. The C2 extension should cite this direct gradient bound
rather than assert that every literal bound in (15) remains unchanged;
the final reviewed version now does exactly this.

The final section 8 also correctly limits the fixed-anchor conclusions
to an actual common interior minimizer section. Such a section exists
locally around any coincidence point with zero COMPLETE selected source:
the bounded additional curvature is dominated by the positive logarithmic
curvature, zero is the unique anchor minimum there, and its boundary gap
persists under small parameter changes. For the displayed counting ledger,
vacuum material derivatives vanish by the original parity, so this local
qualification is satisfied there. It would not automatically hold at the
original vacuum for an arbitrary W with nonzero material force.

Finally, a generic C2 added price does not inherit the original
parity-specific cubic source remainder or its specialized vacuum
asymptotic. The final draft preserves that distinction explicitly.

## 6. Novelty and consumer

The original logarithmic source-reduction proof already supplied the
small-cluster amplitude method, anchor strong convexity and Hessian
preservation at vacuum. The new result uses the exact two-arm mean
coordinate to extend the argument to:

1. the unique coincident relative minimum for every nearby mean field;
2. the exact full stationary-set equality in the same mathematical
   variational problem;
3. complete field-Hessian preservation at every selected-source-zero
   point, including any nonzero-matter root of that same functional.

This removes an independent relative-preparation equation from the
declared same-functional stationary system. It does not prove that
system has the primary Einstein/CAR roots or that it is the physically
selected full action. The continuous-control and fixed-mesh boundaries
must accompany the result when the parent integrates it.

## 7. Frozen checker review and independent optimized-mode replay

Reviewed checker:
`/workspace/scratch/07af0e1491e7/balanced_work/check_balanced_preparation.py`

* Checker SHA256:
  `9c47c832b820997c056a607074128ed0b9b77faec482d3d54272acd8b01c9ce3`
* Balanced `SOURCE_PINS.json` SHA256:
  `050516fe7b75b6c7c35e3c90d1fc8e98bad02e5f87c01d0c56f723565f195d8c`
* Root normal-run and independent optimized-run receipt SHA256, identical:
  `4133366b05ab68e33238804dc8b80aa046b267131446f62babfb3da3003a2a18`

Independent command:

```sh
python3 -O /workspace/scratch/07af0e1491e7/balanced_work/check_balanced_preparation.py --repo /workspace/scratch/07af0e1491e7/d0_15
```

Result: **PASS, 44 active checks, five original input hashes verified**.
Independent JSON is saved as
`/workspace/scratch/07af0e1491e7/compiler_work/BALANCED_INDEPENDENT_REPLAY.json`.
Explicit `require` exceptions remain active under -O.
The final proof-only clarification in sections 8--9 was reviewed after
this replay; the checker, its inputs and mathematical core were unchanged,
so an additional identical numerical run was unnecessary.

The complete dictionary is constructed as a 256-by16-by128 tensor and
then reshaped to 4096-by128. It uses all original Fourier columns; no
reference, site or CAR grade is removed. Three actuated sites are actual
free interior sites. The literal four-plane skew generator is retained
at full local rank eight, and its complete rotation acts on the whole
local16-by128 amplitude. The angle/material tangent residual is
`1.3552527156068805e-20`. The exact Golden coefficient is checked in
the integer ring before the separate floating-point native-dictionary
control.

Source extraction is narrowly AST-limited to the original hash-pinned
`reference_characters` function. Its inspected body constructs only
the original real Fourier columns and checks their Gram and row norms;
the original module's main function and native geometry/instrument suite
are not executed.

The four-dimensional two-leaf entropy fixture is correctly labelled in
both code and receipt. Its nonzero stationary material point and anchor
minimum are diagnostic controls of the theorem's mechanism; the receipt
explicitly sets `native_critical_set_proved_by_fixture=false` and
`replayed_native_kraus_leaves=false`. Its logarithmic coefficient is
`p^5/ln(phi)`, with the fixture's own row normalization, rather than the
native coefficient `p^5/(256 ln(phi))`. No full255 or native Hessian
theorem is claimed from this fixture.

The small eigenvalue is evaluated through a nonnegative wedge-squared
determinant and the stable formula
`lambda_small=2 determinant/(trace+sqrt(discriminant))`.
Negative discriminants or eigenvalues raise errors. The only omitted
entropy term is an exactly zero eigenvalue under the standard
`0 log 0=0` convention; no positive probability is floored or clipped.
Numerical minimization is a bounded fixture diagnostic, while existence,
uniqueness and all-root Hessian preservation remain analytical results.

### Sources inspected

All source paths below are relative to `/workspace/scratch/07af0e1491e7/d0_15`.

* `02_REGISTRY/research/sources/d0_native_logarithmic_source_reduction_2026-10-21/PROOF.md`,
  sections 2--7 and 9, for the inherited carrier, support, amplitude
  regularity, source and anchor-envelope assumptions.
* `02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/NATIVE_COHERENT_CHOICE_SOURCE.md`,
  sections 3--6, for the actual complete coherent cut and p^2 compression.
* `02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/PRIMARY_STOPPED_PORT_PRICE_AND_PREPARATION_EULER.md`,
  for the actual cap2 counting-price and nonlinear preparation boundary.
