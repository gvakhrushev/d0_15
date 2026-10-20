# Primary recovery packet: complete terminal source gain + compatible residual

21 October 2026. Existing scientific owner: PR #334, `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`. This composes existing results, not a new task or a physical GR promotion.

## Input chain

1. [Primary exact nonvacuum case](../../D0_GR_PRIMARY_POSITIVE_CASE.md).
2. [Whole-family CAR/Book/causal source](../../A4D_CAUSAL_BOOK_SOURCE_TO_EXACT_GR_SYNTHESIS_2026_10_20.md), including its remaining Info/work source.
3. [Complete Golden terminal protocol](../d0_native_gr_completion_synthesis_2026-10-20/book_source/MINIMAL_GOLDEN_COMPLETE_SOURCE.md), sections 4-7. Actual query, primitive admission, fixed prefix and information cut remain explicit hypotheses.
4. [Normal-row recovery theorem](../../A4D_PRIMARY_NORMAL_SOURCE_RECOVERY_SYNTHESIS_2026_10_21.md). All other Euler rows must be solved, not discarded.
5. The gain-aware substitution below, checked by [the new executable](check_source_gain_composition.py) and recorded in [INTEGRATION_RESULT.json](INTEGRATION_RESULT.json).

## 1. A known proportional archive source is not an uncontrolled small error

Consume the original complete terminal owner, without re-claiming its circuit construction. On the whole common-null stratum Sigma,

`t=0`, `Dt=gamma_h DJ2`, `gamma_h=Q0 R0/(2 N_h)>0`.

Here `N_h` is the entire padded query dimension, including all trace multiplicities; `p=phi^-1`, `z=2^-20`, `L=1-p^6`, `M=1-p^12`, `Q0=1-zL`, `R0=1-zM` are the original fixed quantities.

The complete three-query execution has clean amplitudes `1-2t^2`, `2t(1-t^2)` and non-clean probability `4t^4(1-t^2)`. The actual G^2 postrotation, retaining all work, gives

`q1(0)=4p^3`, `q0(0)=p^6`, `Dq1=kappa Dt`, `kappa=8p^(9/2)>0`.

The two already-proved terminal readings therefore satisfy

`D S_terminal,coh = g_coh,h DJ2`,

`D S_terminal,ptr = g_ptr,h DJ2`,

`g_coh,h = gamma_h kappa`,

`g_ptr,h = gamma_h kappa (4+log_phi 4)`.

The gain ratio is `6.880840180825113`. At the original fixed z, `N_h g_coh,h = 0.4587909116461719` and `N_h g_ptr,h = 3.1568669394523643`. These are conditional alternatives under the owner's specified information cuts; the numbers do not select a compulsory physical reading.

The same gain multiplies all supplied whole-J2 first sources, including both original geometry and matter coefficients:

`(g b_J,h)/(g a_J,h)=b_J,h/a_J,h=lambda_-(2^-20)`.

Thus the known terminal source rescales the equations, not their configured gravity/matter ratio or stationary zero set on Sigma. It need not be small. This is a first-source composition, not equality of actions or Hessians.

## 2. The residual-to-metric bound must include the actual gain

For one supplied complete physical price and its genuinely selected terminal reading, define the remaining source

`R_rest,h = D S_full,h - g_h DJ2`.

This is analytical separation of a derived source. It does not subtract its paid value, introduce a counterterm or assign an Info table. Every remaining work/controller/clock/initial-preparation/code/normalization/history source stays in R_rest,h.

Suppose the normal theorem's compatibility premise holds on the ENTIRE admitted closed field ball: all other 15 coframe, 24 link, 2 material and genuinely independent internal equations have no unsolved remainder. Let r_h be the surviving normal coframe row and a_J,h the **unscaled** original J2 coefficient. For H=H0+v the actual equation is

`(g_h a_J,h/(2h)) (-Delta_h^perp) v + r_h(H0+v)=0`.

The correct normalized residual is

`rho_h(H) = 2h r_h(H)/(g_h a_J,h)`.

The original five-point unit-square bound `||(-Delta_h^perp)^-1||_(inf->inf)<=1/8` yields

`||v||_inf <= h sup||r_h||_inf / (4 |a_J,h| g_min,h)`,

provided `|g_h|>=g_min,h>0`, the residual is continuous on the same closed ball, and the right-hand-side bound fits its radius. The previous Brouwer proof then supplies an exact finite zero without a C2 entropy/source assumption. For the two fixed-clock terminal readings g_h is a known positive constant at each mesh. A field-dependent multiplier is admissible only after its actual whole-source factorization has been proved.

Only the remaining **normalized** residual must shrink. A sufficient O(h^2) metric-error condition is

`sup||r_h||_inf = O(h |a_J,h| g_min,h)`.

This is the declared primary profile estimate, not the original raw216 norm or arbitrary-spacetime C2 recovery. Source compatibility and field-writing/admission remain mandatory.

**Query size is not free.** Since the known gains scale as 1/N_h, omitting gamma_h understates error amplification. Doubling N_h doubles this correction bound for the same unnormalized residual and other factors fixed. Repeating an execution must retain both its gain and actual costs/clock; it is not a free normalization change.

## 3. Negative controls

- Zero gain cannot be divided out. The existing least-price G^0 coherent and G^0/G^1 pointer competitors have zero source on Sigma. The G^2 construction does not prove a prospective task excludes them. The field-minimum exclusion remains unchanged.
- `D S=g(y) DJ2` is not the derivative of an arbitrary product `g(y)J2(y)`: the latter has the extra source `J2 Dg`. A nonzero constant J2 baseline matters. No unpaid subtraction is introduced.
- A field-dependent interpolation of information readings adds `(S_ptr-S_coh) D theta`; it is not just interpolation of the gains. The two owner readings are alternative fixed contracts, not field-dependent tuning parameters.
- Even a tiny non-normal residual invalidates the one-row theorem. A tomographic inverse does not supply a full dynamical inverse or source compatibility.

The useful reduction is specific: the already-computed terminal component is removed from the list of UNKNOWN errors; the remaining actual upstream source must be checked with the correct signal denominator. Neither compulsory valuation nor prospective minimum has been derived.

## 4. Reproduction and evidence

Input snapshot: `4920a97750a85a0cf631057ba3cf0d5b65ed9013`.

The original checker and [RESULT.json](RESULT.json) remain byte-identical. In this continuation both ordinary Python and `python -O` reproduced that historical output, including every numerical value. The preserved checker Git blob is `92ce023873ddb780439dd54dd47415c740841113`.

From the repository root:

```bash
python3 02_REGISTRY/research/sources/d0_primary_normal_source_recovery_2026-10-21/check_primary_normal_source_recovery.py
python3 02_REGISTRY/research/sources/d0_primary_normal_source_recovery_2026-10-21/check_source_gain_composition.py
```

The new executable pins the old checker bytes and verifies complete retained-work normalization, the exact Golden jet, the gain and matter/gravity ratios, and the moving-source negative controls. A 49-site diagnostic checks gain-aware recovery and the inverse-gain relation for the same raw residual. The full original terminal circuit/source identity is a CONSUMED theorem, not re-proved by this small test. Its physical-admission premises are unchanged.

[INTEGRATION_RESULT.json](INTEGRATION_RESULT.json) is the actual new output; `python -O` reproduces it byte-for-byte. The numerical residuals are explicitly diagnostic, not evaluated native Info/work. No remote CI, independent acceptance or new Lean validation is claimed.

## 5. Concurrent orientation-verification theorem: preserve the distinct task and price

The parallel [native Golden17 stopped-orientation owner](../../A4D_NATIVE17_OPTIMAL_STOPPED_ORIENTATION_AND_INFO_2026_10_21.md), present by snapshot `5f92d32ac405f956fc5e10c4f06649e2728881f5`, proves an optimal expected measurement count for its specified IID two-hypothesis task on the existing positive 17-category instrument. At fixed target error and face amplitude xi=h^2 f with fixed f!=0, its count is Theta(h^-4), retaining neutral outcomes and the Bell success factor. This is not a re-proof or independent acceptance of that owner here.

Its task-relevant orientation information is bounded, while the accumulated verification expense grows. Therefore the optimal repeated verifier cannot be silently identified with the fixed-word terminal signal g_h DJ2, treated as a field-independent prefix, or declared a negligible remainder without a SAME-programme clock/price transport. Conversely a large price VALUE is not by itself a proof of a large FIRST source; the actual stopped-source derivative and any threshold changes must be calculated. No C1 continuation of an optimized integer-threshold envelope is assumed.

These statements are compatible: the present packet controls exact stationary recovery from an already supplied, correctly normalized continuous SOURCE; the parallel result identifies the expense and selection of a different declared verification TASK. The remaining physical question is which complete reachable execution and information contract the native programme actually admits and selects. Neither theorem answers that by renaming the other one's cost.

**Open:** compulsory price/admission/readout selection; complete upstream residual; its all-row compatibility and size; native stationary/constraint law versus prospective field minimum; generic joint recovery and raw216. `GR_closed=false`.
