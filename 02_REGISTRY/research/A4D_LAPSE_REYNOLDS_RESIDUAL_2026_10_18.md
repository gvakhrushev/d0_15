# Lapse Reynolds residual (DRAFT candidate)

**Status:** DRAFT candidate. `exact_cancellation = false`. `coefficient_chosen = false`. `gr_derived = false`. No `claims.csv` row. `D0-HODGE-LINKS-001` stays open. PR #334 is not edited. `native_measure_admission_claimed = false`. `finite_schur_limit_claimed = false`. This note does not derive GR.

**Pin.** Read-only `git show` / `git grep` on `origin/exp/a4d-joint-response-continuation-2026-10-16`. The tip is `f3fe3c80ae69f122edc8cbef19c71fb22a1d68e6`. It is a strict descendant of `c3ae03b735dbde690bf1774fc3761846aff93248`. `check_native_scalar_price_response.py` and `A4D_GOLDEN_QUANTILE_CLOCK_SAME_CAR_VOLUME_BRIDGE_2026_10_18.md` are byte-identical on those two commits. The extracted pin checker was executed and returned `PASS_INTERVAL` for schema `d0-full-price-lapse-source/1`.

## Question

On the fixed-β H+J+R root, the reduced lapse coefficient `A − B²/C` lies in `(0.0057230, 0.0057231)`. Does the boundary jet of the Reynolds Ward (Q7) cancel that coefficient when cells move?

No coefficient is chosen to force the two sides to agree. The conditional price is not replaced by a new action.

## Owned inputs

The lapse object is the continuum conditional-price Schur complement at `β = 2p²`, `z = 2^{-20}`, `M = 128`, matrix `K = [[A, iB], [−iB, C]]`, reduced value `A − B²/C`. The pin states that this reduced Hessian is strictly positive and is not an Einstein vacuum gauge Hessian. That statement is an input, not a derivation of the Einstein equation performed here. It is not a finite Schur limit and it does not admit the native measure. The unit-cosine physical Hessian is half of the reduced value.

(Q7), from the clock memo, keeps the boundary term:

```
0 = (1/V) ∫_{C_w} [D J − J D log V] dx
    + (1/V) ∫_{∂C_w} J (velocity · normal) dS.
```

On `J_ε = 1 + ε cos(2π t)`, `V_ε = 1`, the same memo gives

```
D_ε t_F |₀ = −sin(2π p)/(2π) ≠ 0.
```

Section 6.40 of the labelled full-source memo records the fixed-cell mass error `p + ε sin(2π p)/(2π)` and the repair `X_ε = F_ε^{-1} X_word`, which restores mass `p`. That repair is the cell-mass Ward. It is not a term of (13dh).

## What was recomputed

The committed checker recomputes both sides. It does not import the pin file and it does not paste the lapse digits as the proof.

The recomputed reduced value lies in `(0.0057230, 0.0057231)`. At the declared `10^{-25}` matrix tail, twenty digits are

```
A − B²/C = 0.0057230517558896483875.
```

The companion entries are `A = 0.0054788385630043212246`, `B = 0.0026159527191139030879`, `C = -0.028021453500477849771`. The physical half is `0.0028615258779448241937`.

The boundary contribution is order `ε¹`:

```
D_ε t_F |₀ = −sin(2π p)/(2π) = sin(π√5)/(2π)
            = 0.10750761934232042979.
```

Sympy identifies the interior integral with the negative of this value, so their sum is 0 with coefficient 1, not a fitted coefficient. The moving-cell mass minus `p` vanishes through order `ε³`. The order-`ε²` and order-`ε³` coefficients of the moving boundary are `0.07927277265931789939` and `0.033926103485778212305`.

## Verdict

The boundary jet is not a summand of the reduced lapse Hessian. They are different observables: an order-`ε¹` cell-transport scalar, and an order-`ε²` conditional-price Schur complement. The momentum sum for `A`, `B`, and `C` has no boundary integrand `J (velocity · normal)`.

`exact_cancellation` is true only for an identical zero with no fitted factor. That does not happen.

The quantitative residual is the difference actually computed:

```
residual = (A − B²/C) − D_ε t_F|₀
         = -0.1017845675864307814
         ∈ (−0.11, −0.10).
```

The opposite unit sign is `0.11323067109821007818`, also not zero. The sign was not selected after the fact: both unit signs fail, and so do `±` the order-`ε²` and order-`ε³` jet coefficients, and `±` those coefficients against the physical half. The same-order cell-mass residual is the zero already proved for the moving mass. Subtracting that zero leaves the lapse enclosure `(0.0057230, 0.0057231)`.

The internal (Q7) cancellation is real and is checked. It cancels the interior mass defect. It does not cancel the price Hessian.

## Negative control

Solving `factor * boundary = 0.005723` produces a factor near `0.05323`, not `±1`. `accept_fitted_match` raises `fitted_factor_rejected` and has no return path. The factor is not stored. `coefficient_chosen` stays false. A checker that accepted this factor would fail the test.

## Pre-registered attacks

1. **Fitted scale.** Multiply the boundary jet by whatever constant hits `0.005723` or the reduced midpoint. Rejected. `exact_cancellation` forbids a fitted factor. The solved factor is not a unit coefficient.

2. **Sign choice.** Declare cancellation by `reduced + boundary = 0` after seeing that `reduced − boundary` is negative. Both unit signs were computed before any selection. Neither interval contains 0.

3. **Wrong jet order.** Treat the order-`ε²` or order-`ε³` motion coefficient as the lapse Hessian. Both were enclosed and excluded from `(0.0057230, 0.0057231)`, as was the physical half `reduced/2`.

4. **Ward zero substituted for the price.** The identity interior + boundary = 0 is the cell-mass Ward. Reporting that zero as if it were `A − B²/C` would erase a positive recomputed interval. The checker keeps the two flags apart: the Ward sum is 0, and `exact_cancellation` against the lapse coefficient is false.

5. **Drop the boundary.** The clock memo forbids dropping it. The fixed-cell slope that remains is `sin(2π p)/(2π) = −0.10750761934232042979`, which is the opposite of the boundary value and is also outside the lapse window. Keeping the boundary restores mass `p` and still does not enter the price sum.

6. **Same-order mass channel.** The order-`ε²` residual of the moving-cell mass is 0. Zero is not the positive reduced Hessian, so the channel in which the boundary really is a summand does not cancel the lapse coefficient.

7. **Admission or Schur promotion.** Matching or failing to match these two scalars does not admit the native measure and does not create a finite Schur limit. Both claims stay false, as in the pin symbol owner.

8. **Reading positivity as GR.** The reduced coefficient stays positive, so this comparison does not turn it into a vacuum gauge zero. That survival is not a derivation of the Einstein equation, not a closure of `D0-HODGE-LINKS-001`, and not a no-go against every future sampling source. `gr_derived = false`.

9. **Moving the root.** `β`, `z`, and `M` stay at `2p²`, `2^{-20}`, and `128`. They are not varied to hunt a numerical match.

10. **A new action.** Defining a fresh price whose Euler equation is the Ward would replace the conditional price. That replacement is not this comparison.

## What this does not show

It does not show that (Q7) is false. The boundary term is required, and on this family it cancels the interior integral exactly. It does not show that the lapse enclosure was miscomputed. It does not show that no later admitted execution can put a clock jet into the same row as the conditional price. The reopening condition is narrower than that: on this same root, the (Q7) boundary contribution and the reduced lapse row have to be one observable, and their difference with coefficient 1 has to be the zero interval.

Checker: `02_REGISTRY/research/sources/d0_lapse_reynolds_residual_2026-10-18/check_lapse_reynolds_residual.py`. `python3` and `python3 -O` both print `PASS`.
