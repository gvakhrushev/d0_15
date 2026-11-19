# Independent review: reconstructed nonvacuum stationary normal form

21 October 2026. Reviewer: metric_source_synthesis; bounded read-only review
within existing PR #334. **ACCEPT at the stated sufficient hypotheses.**
No blocking or nonblocking mathematical defect was found in the frozen
inputs below; no correction to their bytes was requested.

## Reviewed bytes

* `/private/tmp/d0_restoration_normalform_20261021/A4D_COMPLETE_PRICE_NONVACUUM_STATIONARY_NORMAL_FORM_2026_10_21.md`
  SHA-256 `5ad9461c6f1b8d964f0764697a38120d19d320714bc66d99a42898171e3a01a0`.
* `/private/tmp/d0_restoration_normalform_20261021/check_nonvacuum_normal_form.py`
  SHA-256 `dfb40e185a203a1d815415fc91d2c75d41ad05ad754e1cfa166553481202f7aa`.

Hashes were verified before and after review. Original source files were
read at repository head `8ba0bd929499e639b0fe4640ffa448631f3b024b`.

## Checks and findings

1. **Critical equivalence — accepted.** The first auxiliary section
   `s=x, pi=F_x` recovers the original complete price and every source.
   The extended coframe change is a local diffeomorphism on `pi_i/a_i>0`.
   Its new auxiliary Hessian `[[A,-I],[-I,0]]` is invertible even when
   A is singular. The implicit section through `(0,a)` therefore exists
   uniquely. Lifting, transforming and reducing full critical points gives
   a local bijection. The document correctly does not claim an off-shell
   physical-only radial identity or impose the radial equations first.

2. **Coupled K_YY — accepted.** With rows x and columns y, the mixed block
   is `[F_xy;D]` and section derivative is `[D;F_xy+F_xx D]`.
   Independent Schur multiplication gives
   `F_yy+D F_xy+F_yx D+D F_xx D`, exactly the pullback through `[D;I]`.
   The noncommuting two-cell fixture rejects the incorrectly reversed
   factor order. Its numerical section calculation is a diagnostic, while
   the displayed block proof establishes the general identity.

3. **Inertia — accepted.** The auxiliary quadratic form is congruent to
   `-2 s^T pi'` and has inertia `(n,n,0)`. At a full critical point the
   extended Hessians are congruent; both Schur reductions subtract that
   same inertia. Hence the physical Hessian inertias agree, including
   nullities, without a physical-Hessian inverse. The statement is
   correctly restricted to critical points and does not assert equivalence
   of higher-order degenerate minima or silently retain unchanged constraints.

4. **Independent homogeneity — conditional application accepted.** The
   original coframe owner explicitly uses a same-site wedge and independent
   links, yielding `f_i -> u_i f_i` for separate site scales. A fixed
   nondensitized inverse-metric material contraction scales oppositely.
   This does not yet prove the complete actual query/preparation/weight map
   has that independent-site law. Section 7 retains that exact missing
   application. A global scale identity or prior link elimination cannot
   replace the hypothesis. Internal and baseline sources remain in the
   transformed formula; nonconstant null matter is not set to zero as a
   source merely because its scalar density vanishes.

5. **Finite lambda — confirmed against the original owner.**
   `A4D_LOCAL_LEFT_CODED_CAR_NULL_MATTER_EINSTEIN_2026_10_18.md`, equations
   (11)–(12), gives `Lambda_sigma=2 sigma p^(-5)(R/Q+p^6)` at finite
   `z=2^(-20)`. The reconstructed detector ratio is precisely its positive
   scalar factor and becomes Lambda_minus when the actual material
   orientation is minus. It is not replaced by its zero-z limit
   `10+6 sqrt(5)`. The matched scalar ratio does not prove matched measures,
   cell weights or complete internal equations.

6. **All finite caps and kappa bound — confirmed at the declared unit-price
   interface.** `GOLDEN_EXACT_DETECTOR.md`, section 5, explicitly proves net
   reached-cycle lower bounds 18, 40, 4, first-CZ reach probability one,
   first-CCZ reach probability greater than 22/25 and absence of extra
   independently stochastic controller distinctions. Thus the consumed
   `kappa>266/5>53` is genuinely owned under those conditions. The entropy
   and geometric-sum estimates then give `V_N'(r0)>10 alpha beta` for
   every N>=2, while N=1 has the stated negative slope. The theorem does
   not apply that unit-price bound to arbitrary unknown Book valuations.

## Executed independent verification

The new checker was independently executed once, without editing its
expected values or rerunning old geometric/physical suites:

`python3 check_nonvacuum_normal_form.py --output INDEPENDENT_NORMALFORM_CHECK.json`

Result: **PASS**, elapsed 1.291104583 seconds in this run. The diagnostic
maximum normalized auxiliary residual was `9.104159286067898779e-87`; the
relative second-coefficient discrepancy was `1.2534939848095384107e-25`.
The full new receipt is
`/private/tmp/d0_restoration_allflag_20261021/INDEPENDENT_NORMALFORM_CHECK.json`,
SHA-256 `14e0e38e794eb230e5309ee51fdb03abac7bb11033dc28f0277c4b6c62ffc99d`.

This review accepts the conditional stationary normal form and its
specific detector operands. It does not accept native selection, a
preparation critical point, full42 admission, a physical coframe writer,
or GR closure. Historical missing artifacts/reviews remain unrecovered.
