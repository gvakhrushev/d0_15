# Finite Golden words realize the original two-query price on a dense grid and recover its first source

21 October 2026. Existing research owner #334, EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE; constitutive/native-programme-v1. Input `086fab99d8aaed7f712e9a3d2858c516b61901fc`. Bounded constructive continuation of [physical cap-one composition](A4D_PHYSICAL_CAP1_EXECUTION_COMPOSITION_2026_10_21.md), specifically its missing moving-query source map. This is a source-consistent family of actual finite addressed words, not an exact differentiable finite-word family or a physical field-writer theorem. `GR_closed=false`.

## 1. Changed mathematical input and exact consumer

The existing [moving-query proof](sources/d0_physical_cap1_execution_composition_2026-10-21/moving_query/PROOF.md) establishes the full8D native value

`U_*=[CX(G tensor I2)]^2 tensor G^2`,

but shows that one FIXED word has zero ordinary parameter derivative and cannot provide the required field jet. Its same-cut moving-compression obstruction is retained, not contradicted. The original complete source uses

`U(theta_E,theta_b)=[CX(R(theta_E) tensor I2)]^2 tensor R(theta_b)^2`,
`E=p^2(1+x)`, `b=(p-p^2 y)^2`,
`theta_E=arcsin sqrt(E)`, `theta_b=arcsin sqrt(b)`

on the sourced sigma=-1 chart. Here x=eta_query^2 f and y=eta_query^2 q are the original dimensionless operands; the positive square-root branch is used near the primary point. Both baseline angles are theta=arcsin p, p=phi^-1, a=sqrt(p).

**New constructive result:** different exact finite G/CNOT words, all having the SAME per-address primitive inventory and duration at each resolution, realize U on an arbitrarily fine two-angle grid. With the already-owned fixed-cut N=1 CQ ledger, their actual price divided differences converge to the entire required operator and price first jet. There is no added continuously adjustable gate, no moving encoder/decoder, no free inverse, no success postselection, and no change of the original query's return cut or known inputs.

General approximate finite-gate compilation is established background (Dawson--Nielsen, arXiv:quant-ph/0505030); it is not claimed as a new universality theorem. The D0-specific construction below needs only the given one-axis Golden gate and its literal CNOT echo. It does NOT import Solovay--Kitaev resource bounds for this restricted gate family. Nor does it evade exact universal-programmer limitations (Nielsen--Chuang, arXiv:quant-ph/9703032): the finite programmes are different, their resources grow, and their difference quotients are not a derivative of one fixed processor with a finite continuous programme register.

## 2. Equal-cost forward cells, including every controller complement

Use the existing paid known-one control c and the existing addressed target gate G. Let X_c=CNOT(c,target). Define the two chronological three-letter cells

`W_+ : X_c, X_c, G`,
`W_- : X_c, G, X_c`.

On c=1 they implement G and G^-1 respectively. On c=0 BOTH implement G. Each contains exactly one forward G and two CNOT at the SAME addresses. The controller is unchanged; the original oldRIGHT is untouched. All c=0 columns are retained and checked, not replaced with an identity complement.

For any odd N and odd integer k with |k|<=N, take (N+k)/2 plus cells and (N-k)/2 minus cells. The resulting exact complete operator is

`W_(N,k)=|0><0|_c tensor G^N + |1><1|_c tensor G^k`.       (1)

Every such word has N G and 2N CNOT occurrences. At fixed additive per-address primitive durations its arrival time and primitive charge are independent of k. In particular different cell orders are not an uncharged inverse query or a reset of the physical clock. The word is a supplied deterministic programme, not a randomly measured programme label. Known-one preparation, routing, all actual stored instructions and the previous compiler ledger remain as in the original declared interface.

Use FOUR copies of these rotation slots in the original U: twice for theta_E, twice for theta_b. The two tail CNOTs are unchanged. One query therefore has

`4N G + (8N+2) CNOT`,

and the two-query detector uses

`8N G + (16N+4) CNOT`.                                  (2)

This is only the query portion of the actual ledger; bank/OR/measurement/abort/routing costs are not removed. The known-one c=0 complement of the whole query is the SAME across all settings of the grid, because each slot there is G^N. Its c=1 block is the desired original full8D U. Thus no controller or six-dimensional query complement is dropped.

## 3. Small native displacements exist without an external angle catalogue

The fixed angle theta is an irrational multiple of pi. An elementary exact proof uses

`2cos(2theta)=4p-2=2sqrt(5)-4`.

This number has irreducible polynomial `t^2+8t-4`; its algebraic conjugate is `-4-2sqrt(5)<-2`. If exp(2i theta) were a root of unity, every conjugate of its sum with its inverse would lie in [-2,2], a contradiction.

Consequently there are integers Q_j,m_j with

`epsilon_j=2(Q_j theta-m_j pi) -> 0`, `epsilon_j != 0`.

Such returns can be selected using only the native algebraic matrices: for each prescribed rational error threshold, search finite powers for `||G^(2Q)-I||` below that threshold. Density of this irrational circle rotation makes the search terminate. The theorem does not designate this search as a compulsory physical scheduler. Continued fractions merely give convenient analytical/test examples; no arbitrary enumeration of alternative Book histories or Beatty selector is introduced.

Choose `N_j=2Q_j+1`. The three exact words with exponents `1-2Q_j,1,1+2Q_j` have c=1 blocks

`R(theta-epsilon_j), R(theta), R(theta+epsilon_j)`.

They all have inventory (2). These are actual computed native rotations, not approximations of those three angles.

For a bounded two-angle grid, let |k_E|,|k_b|<=K_j and choose the common odd length `N_j=2Q_j K_j+1`. Exponents `1+2Q_j k_E` and `1+2Q_j k_b` then implement exactly

`U(theta+k_E epsilon_j, theta+k_b epsilon_j)`.

For a fixed small angle neighborhood one may choose K_j of order 1/|epsilon_j|, obtaining arbitrarily fine exact grids of the SAME nonlinear query. This is an existence/resource construction. No polylogarithmic cost, bounded continuum runtime, or cost-free field-to-program conversion is claimed.

## 4. Full8D first-source consistency, rather than differentiating a constant word

Let U_E^+/- and U_b^+/- denote the four native endpoints obtained by changing only the indicated angle. Central differences satisfy

`(U_E^+ - U_E^-)/(2epsilon_j) = partial_theta_E U_* + O(epsilon_j^2)`,
`(U_b^+ - U_b^-)/(2epsilon_j) = partial_theta_b U_* + O(epsilon_j^2)`.  (3)

This is an operator identity in the limit, not only a matched trace. For each angle the product contains two varying rotations; the operator norm of the third derivative is at most 8. Taylor's integral remainder therefore bounds either error in (3) by `4 epsilon_j^2/3`. No unmeasured output is omitted.

The corresponding ACTUAL finite density coordinates are

`x_+/-=sin^2(theta+/-epsilon_j)/p^2-1`,
`y_+/-=-(sin(theta+/-epsilon_j)-p)/p^2`.

Their exact differences are

`x_+-x_- = (2a/p) sin(2epsilon_j)`,
`y_+-y_- = -(2a/p^2) sin(epsilon_j)`.

Both are nonzero for small nonzero epsilon_j. Hence the divided differences in the original x,y coordinates converge, with quadratic error, to the already-owned required query jet, including its nonzero trace:

`D_x U_*=(a/2) partial_theta_E U_*`,
`D_y U_*=-a^3 partial_theta_b U_*`,
`Tr(D_x U_*)=-8p^5`, `Tr(D_y U_*)=+32p^4`.                (4)

The old fixed-word/same-cut theorem still holds. Equations (3)-(4) use different actual words and a specified limit, not a purported ordinary derivative of a finite countable family. The rounded staircase map from arbitrary real fields to nearest programmes does NOT have its ordinary derivative equal to (3).

## 5. The complete N=1 CQ price survives the compilation, with a real clock budget

Consume the unchanged [full Golden detector](sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/GOLDEN_EXACT_DETECTOR.md), including its paid pure known inputs, coherent efficiency coins, data-independent completion transcript, all aborts and preserved work. Replace ONLY each of its two U calls by the finite words above. They are unitary and add no stochastic compiler failure. Thus alpha and beta are unchanged, and every completed transcript has the exact original report law at the native endpoint:

`r(U)=1-(1-zA(U))(1-zB(U))`,
`A(U)=<+|[I-W(U)*W(U)]|+>`,
`B(U)=<-|[I-W(U)*W(U)]|->`, `W(U)=P*UP`.

The fixed input cut is the original rank-two span of |0>,|2> in full8D. Every complement and efficiency outcome is retained before the same final report measurement. At the actual grid values this is EXACTLY the existing nonlinear r(x,y), not an approximation to its probability.

For fixed compilation resolution and N=1, the complete given CQ price is

`S_j(x,y)=B_j-alpha beta h_phi(r(x,y))`.                 (5)

B_j includes the actual added query ticks and all inherited bank/compiler/routing cost and entropy. Its VALUE grows with word length. Under the original held per-address cost, deterministic schedule and frozen-query comparison interface, it is the SAME for the grid settings at that resolution. A known deterministic final clock shift changes neither the old compiler transcript entropy nor its conditional full-work purity. Therefore (5) implies

`[S_j(x_+,0)-S_j(x_-,0)]/(x_+-x_-) -> -alpha beta h_phi'(r0) r_x`,
`[S_j(0,y_+)-S_j(0,y_-)]/(y_+-y_-) -> -alpha beta h_phi'(r0) r_y`.    (6)

Convergence is O(epsilon_j^2) on the fixed positive report chart, by the central Taylor quotient and the exact nonzero denominators. The 85-digit checker confirms the full original output matrices and these ACTUAL complete-price differences, including a large common paid query baseline. The generic analytic proof does not infer convergence from the finite sample table.

No zero-gain readout is substituted. With the original z=2^-20, K_pre=9, L_gate=20, sigma=-1,

`a_CQ=-2.3854299355446938880440572389058e-7`,
`b_CQ=+5.5858197648835163727834285435703e-6`,
`b_CQ/a_CQ=lambda_minus(2^-20)=-23.41640675188407497289558...`.

Thus the native finite-program source approaches both the geometry and the material coefficients together, with their actual finite-z ratio. The same original inverse-PF/copy-count map may consume this as a QUERY-LEVEL first-source approximation; its actual field-to-program and norm transport are still required.

### Why the cap-one choice matters

At larger cap N, a common additional query price T_j contributes

`alpha T_j E_N(beta r)`.

Its source is `alpha beta T_j E_N'(beta r) dr`, generally nonzero. Equal cost per attempt is not zero total source when the number of attempts depends on the field. The present neutral-prefix claim uses the already selected N=1 execution, where E_1=1 exactly. It is not silently extended to arbitrary stopped histories.

An unpadded use of `G^(1+2Q)` and `G^(1-2Q)` would also fail: expanding every inverse as XGX gives one-rotation unit-cost difference `4-4Q`, whose divided difference does not vanish. The equal-cost cells (1) are therefore part of the mathematical source realization, not an optional coding convenience.

## 6. Full field-source consumer and what this does not prove

For an already supplied physical density map y_field -> (x_b,y_b), the original all42 covector is the chain-rule pullback of the two local query slopes, summed with the ACTUAL integer multiplicities. If T_h is the norm of that weighted pullback, this construction gives a query-induced source error bounded by `C_h T_h epsilon_j^2` on a controlled chart. A refinement schedule must use the actual source normalization and make this error fit the existing recovery budget. One cannot omit T_h, the signal coefficient, the additional physical clocks, or the remaining upstream sources.

In particular on the original primary directional relation `delta x=-lambda_minus delta y`, the exact source cancels while the compiled secant has a measured O(epsilon_j^2) defect. This is a real nontrivial cancellation of TWO approximated source components, not an artificial declaration that the query is constant.

**Discharged scoped premise:** prescribed query values on arbitrarily fine two-parameter grids, and their source-consistent finite differences, need no new continuously adjustable rotation gate inside the existing addressed Golden/CNOT/known-one palette. The matrices, controller complement, per-setting clock and same-CQ source are explicit.

**Not discharged:** an autonomous native geometry-to-programme map from one complete initial D0 state; physical field-writer tangent coverage; compulsory absolute Book03 valuation; a field-evolving or order-dependent primitive ledger; minimum selection; finite all42 native critical points; uniform physical runtime/refinement bounds. In particular source consistency of discrete comparisons is not an exact differentiable family at any finite programme length. Admitting the existing addressed palette and input resources remains the inherited physical hypothesis.

This replaces an unspecified analogue-query primitive by a concrete discrete implementation/precision/clock interface. It does not replace the remaining map by relabeling programme indices as actual coframe and Lorentz fields.

## 7. Actual bounded validation

[Checker](sources/d0_paid_golden_query_secants_2026-10-21/check_paid_golden_query_secants.py), [actual output](sources/d0_paid_golden_query_secants_2026-10-21/RESULT.json), and immutable inputs/validation metadata are stored beside it.

| Q | Two-query G+CNOT ticks | Larger relative slope error | Matter/geometry ratio |
|---:|---:|---:|---:|
| 33 | 1,612 | 2.589e-4 | -23.4154830535 |
| 1,193 | 57,292 | 4.628e-6 | -23.4163902386 |
| 4,192 | 201,244 | 2.655e-7 | -23.4164058047 |
| 17,961 | 862,156 | 8.168e-9 | -23.4164067227 |

At the last example the primary tangent cancellation defect is `-6.951976120042577e-15`. These are high-precision numerical checks, not interval enclosures or experimentally measured errors. The exact word identities and asymptotic Taylor theorem are analytical. No claim of minimal or efficient compilation is made: matrix powering in the checker does not shorten the physically paid word.

Normal and `python -O` stdout agree byte-for-byte. Exact symbolic checks include all controller columns and the original four-tail/full8D endpoint identity. Native finite powers, actual compressed complement effects, report positivity, complete price secants and a nonconstant-ledger countercontrol are checked. No old geometric/Lean suite or independent scientific acceptance is re-claimed.

## 8. Pinned provenance and structural references

All repository inputs refer to `086fab99d8aaed7f712e9a3d2858c516b61901fc`:

- `sources/d0_physical_cap1_execution_composition_2026-10-21/moving_query/PROOF.md`, blob `280d4b93f3113d94691609b20cd7c27793e61499`: actual U, required two angle jets, countability and same-cut obstruction.
- its `check_native_query_value_and_jet.py`, blob `1a21cac195f4f4f1a9a617695d2e327f0763ecde`: literal matrices, P and retained +/- effects.
- `sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/GOLDEN_EXACT_DETECTOR.md`, blob `92b9003d783c24b1883a2a21f8b30625078afff7`: existing known-one echo, paid fixed addressed compiler and full N=1 CQ price.
- `A4D_SAME_EXECUTION_SPATIAL_WEIGHTS_AND_COMPLETE_SOURCE_2026_10_21.md`: original 42-source/copy-count consumer, not proved again here.
- `A4D_PHYSICAL_CAP1_EXECUTION_COMPOSITION_2026_10_21.md`: remaining physical query/price/input distinctions.

References distinguish established background from the present original-query application: [Dawson--Nielsen, quant-ph/0505030](https://arxiv.org/abs/quant-ph/0505030); [Nielsen--Chuang, quant-ph/9703032](https://arxiv.org/abs/quant-ph/9703032). No external approximation theorem is used to waive a D0 clock, input, reference or price obligation.

## 9. Exact source evaluation from four probability contexts

The follow-up checker `sources/d0_paid_golden_query_secants_2026-10-21/check_exact_four_setting_source.py` computes the original full8D operator/report jets and stencil weights exactly in `Q(a)[z]`, where `a^4+a^2-1=0`, then applies the CQ entropy chain rule at the baseline. Seven operator settings,

`(1,1), (3,1), (-1,1), (1,3), (1,-1), (1,5), (1,-3)`,

reduce by exact report symmetry to four distinct probability contexts: `(1,1), (3,1), (1,3), (1,5)`. Each setting is an actual equal-inventory two-query word: 40 Golden gates, 84 CNOTs and 124 unit query ticks. The full controller complement, original fixed rank-two cut, unconditional abort factor, and retained CQ readout are kept.

Writing `ell_{e,b}=alpha beta r_{e,b}` for the unconditional complete-report probabilities and `h_phi` for the binary entropy in base `1/p`, the exact chain-rule source is reconstructed as

```math
S_f=-h_phi'(r_{1,1}) (a/2) w_E (ell_{3,1}-ell_{1,1}),
S_q=h_phi'(r_{1,1}) a^3[-w_1 ell_{1,1}+(w_1-w_2)ell_{1,3}+w_2 ell_{1,5}],
```

with exact stencil coefficients

```math
w_E=-173a^3/124-70a/31,
w_1=-21449a^3/10505-34712a/10505,
w_2=2049697447a^3/3670783160+414560017a/458847895.
```

The probability-side symbolic source error is zero; the four-context chain-rule reconstruction matches the full source to the checker’s `1e-70` numerical tolerance. The finite-`z` source ratio is `S_q/S_f=-23.416406751884074972895582064895...`. This is an exact evaluator for the declared CQ price derivative; it is not a finite difference of entropy values. Applying the probability stencil directly to the nonlinear entropy differs from the correct chain-rule result by `9.738373384822754845e-11` in the checker’s 85-digit numerical control.

The physical-sampling control remains severe: under the checker’s independent full-run model, the geometry source needs about `2.054e14` runs per nonbaseline setting for 1% RMS error. Finite-shot error is not removed. More fundamentally, the exact evaluator still supplies no physical field-to-program map or autonomous descent, does not select Book 03 `Info` or its input constraints, does not recompute the complete bank/detector ledger, and does not solve the all42 stationary system. The result closes a finite query-source evaluation step only; `GR_closed=false`.

The exact checker, stored output `RESULT_FOUR_SETTING.json`, and local input pins are adjacent to the source. Ordinary and optimized checker runs agree byte-for-byte. The output is a symbolic/high-precision computation, not an interval enclosure or experimental measurement.
