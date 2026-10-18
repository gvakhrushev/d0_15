# Quantile-clock map versus the owned recording engine (DRAFT candidate)

**Status:** DRAFT candidate. `gr_derived = false`. No row was added to `claims.csv`. `D0-HODGE-LINKS-001` stays open. Draft #334 and `exp/*` were not edited. This comparison does not derive GR.

Read-only pin: `origin/exp/a4d-joint-response-continuation-2026-10-16` at `3e4330235b9cea8adae9bb58a2b3e045af89f5d2` (2026-10-18). That tip contains `c3ae03b735dbde690bf1774fc3761846aff93248`. The quantile-clock memo blob is unchanged from that commit: `a5e1ad86319ec9449c863d6a78dff3985ffc2e01`.

The cited checker `02_REGISTRY/research/certificates/a4d_golden_quantile_clock_source_check.py` is absent at `cd077973b267dfd271d831c78dab2e9fe5b0c2fb` and still absent at the tip. A green CI run of the pin is not a run of that missing file. No receipt JSON is written.

## Question

Can the lower-triangular conditional-CDF placement `T_ρ` in `A4D_GOLDEN_QUANTILE_CLOCK_SAME_CAR_VOLUME_BRIDGE_2026_10_18.md` be executed by the existing recording engine, without a new gate? The moving Jacobian source (Q6)–(Q7) is compared with the engine's actual sampling placement on one nonconstant proper lapse and one shearing 4D density.

Execution means an owned primitive computes `T_ρ`. Retyping the CDF in this package is not that primitive.

## Positive control, not engine execution

Sympy 1.14 recomputes the memo's own algebra.

Lapse: `J = 1 + ε cos(2π t)`, `V = 1`, `F(t) = ∫_0^t J`, `p = (√5 − 1)/2`, `t_F = F^{-1}(p)`.

`D_ε t_F` at `ε = 0` equals `−sin(2π p)/(2π) = sin(π √5)/(2π)`, which is not zero. The moving cell `[0, t_F]` has mass `p` because `V = 1` and `F(t_F) = p`. The fixed interval `[0, p]` has mass `p + ε sin(2π p)/(2π)`.

Shear: `ρ = (1 + ε x0 x1)/(1 + ε/4)`. The memo fields `R0`, `R1`, `R2 = x2`, `R3 = x3` satisfy `det DR = ρ`. At `ε = 0`, `div(∂_ε R) = x0 x1 − 1/4 = ∂_ε log ρ`. The level `R1 = p` has boundary velocity `x0 p^3 / 2` with `p^3 = √5 − 2`, hence `x0 (√5 − 2)/2`, which depends on `x0` and is not identically zero.

These identities passing does not set `engine_executes_map`.

## What the owned engine actually samples

Scanned at the pin, with no new placement gate:

- Closed record, `certificates/a4d_native_closed_record_engine.py`: `step(state)`, `encode`, `literal_axis_gate`. The transition receives the current state, not a conditional CDF of `J` or `ρ`.
- Fock binding, `certificates/a4d_native_fock_record_binding_check.py`: `creator`, `record_basis`.
- Metric chronology, `certificates/a4d_native_record_metric_chronology_check.py`: `record(G, n, dG, dn)`.
- Joint chronological reduction checker, same certificate directory: no conditional-CDF marker.
- Golden address, `sources/d0_history_density_palatini_2026-10-16/check_density_palatini.py`: `split(leaf)` uses `axis = len(word) % 4`, F-width `p * width`, R-start `lo + p * width`, R-width `p**2 * width`. The function body has no density, `ε`, or Jacobian argument.
- Golden cost, `certificates/a4d_native_golden_cost_refinement_check.py`: `weight(w) = p**cost(w)`.

No scanned file contains a conditional-CDF, quantile, or `T_rho` placement. The executed sampler is therefore the fixed address rectangle `B_w` with `|B_w| = p^{cost}`.

The owned cocycle is left as written in `A4D_NATIVE_BRANCH_INFORMATION_COCYCLE.md`: `qρ(ω) = μ(ω) Tr(ρ Mω)`. This comparison does not set `qρ = μ`.

## Residuals

On the lapse tangent the engine keeps the first F-cell `[0, p]`. Its physical mass under `J` differs from the moving-cell mass `p` by

`ε sin(2π p)/(2π) = −ε sin(π √5)/(2π)`.

That is the fixed-cell mass error. It is the interior term of (Q7) when the boundary velocity is zero, so (Q6) for this engine sample is not the memo's `D_ε t_F`.

On the shearing density the engine's second wall after `F` then `F` stays at `x1 = p` for every `x0`. Formula (Q12) moves that wall with velocity `x0 (√5 − 2)/2`. The rectangular address boundary and the conditional-CDF boundary are not the same source.

Neither tangent has zero residual against the engine. Therefore both flags are false:

```text
engine_executes_map = false
sources_coincide = false
gr_derived = false
residual = lapse fixed-cell mass error eps*sin(2*pi*p)/(2*pi) = -eps*sin(pi*sqrt(5))/(2*pi); shear: engine keeps the rectangular address boundary x1=p while (Q12) moves the second boundary with x0 at velocity x0*(sqrt(5)-2)/2
```

## Pre-registered attacks

1. Retype (Q2)–(Q13), see that the algebra checks, and set `engine_executes_map` true. The hostile entry `forged_engine_executes_map(True)` raises `RetypedClockForgery` and does not return true. The positive control is not execution.

2. Set `qρ = μ` because `|B_w| = μ(w)`. The owned path weight is `qρ(ω) = μ(ω) Tr(ρ Mω)`. Reference cylinder volume is not that Born weight. The flag `qrho_identified_with_mu` stays false.

3. Treat a green CI result on the pin as a run of `a4d_golden_quantile_clock_source_check.py`. The path is absent at `cd077973` and at `3e433023`. `ci_ran_absent_certificate` stays false.

4. Call `|B_w| = p^{cost}` the physical cell mass under the nonconstant lapse. For the first F-cell the physical mass is `p + ε sin(2π p)/(2π)`, not `p`. Agreement of the address volume with `μ(F)` does not cancel (Q7).

5. Call the address walls the same object as (Q12) because both mention `p`. The engine wall `x1 = p` has derivative zero in `x0`. The conditional wall velocity `x0 (√5 − 2)/2` does not.

6. Add a gate that implements `T_ρ` and describe that gate as the existing engine. This package does not add the gate. `split` is read and compared; it is not replaced.

7. Read a failed identification, or a successful replay of the map algebra, as a derivation of GR. `gr_derived` stays false. No Einstein equation is selected by this residual.

## What this does not show

It does not show that the triangular map is algebraically wrong. It does not show that no later admitted sampler could compute `T_ρ`. It does not close the joint-response programme, the Hodge-links claim, or a physical clock law.

Reopening requires an owned primitive already inside the closed-record, Fock, chronology, or golden-address engine that computes the conditional-CDF placement, with both the lapse mass residual and the shear-wall residual identically zero, without setting `qρ = μ` and without adding that primitive in order to pass.

Checker: `sources/d0_quantile_clock_execution_2026-10-18/check_quantile_clock_execution.py`. The test `test_quantile_clock_execution.py` prints `PASS` under `python3` and `python3 -O`.
