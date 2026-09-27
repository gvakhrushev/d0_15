# WRK-A4D-DIAGONAL-MICROSTRUCTURE-SLOW-BACKGROUND-RESPONSE

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`  
Research lane: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`

Repository: `gvakhrushev/d0_15`  
Base: `main`  
Branch: `wrk/a4d-diagonal-microstructure-slow-background-response`  
Primary artifact: `02_REGISTRY/research/A4D_DIAGONAL_MICROSTRUCTURE_SLOW_BACKGROUND_RESPONSE.md`  
Execution: `GitHub-first`

## Why delegated

Merged #232 supplies an exact curved, nongauge, period-four joint-vacuum family with
`E_K(eta,K(z))=E_Q(eta,K(z))=0`, but that flat-background identity does not determine
the response on a slowly varying metric/solder background. The first mixed coefficient
between the slow background and this ultraviolet microstructure is a bounded exact
finite-star calculation with a clear hostile PASS/FAIL outcome. It is independently
reviewable and should feed the broader EXPENSIVE response-decoupling theorem rather
than be recomputed inside that research lane.

## Dependencies and conventions

Consume the exact family and conventions owned by merged #232 and the metric-response
normalization/sensitivity conventions of #226. Pin their merged SHAs at execution start.
Use the repository's actual naked-star finite metric partial; do not replace it by a
continuum ansatz. Keep geometric Euler response distinct from a prescribed matter source.
The identity connection is allowed as a finite hostile comparator, but any comparison to
the designated smooth branch must state exactly which finite residual from #216/#223 is used.

## Objective

Let `K(z)` be the exact #232 period-four diagonal microstructure and sample a smooth
background on the finite star as

[
Q_h=\eta+hq_1+h^2q_2+O(h^3),
]

with slow variation across neighboring sites explicit. Compute exactly

[
\Delta E_Q(h,z)=E_Q(Q_h,K(z))-E_Q(Q_h,I)
]

through the first nonzero mixed coefficient relevant after the owned `h^{-2}`
normalization. Record coefficients of `h^m z^n` before choosing an amplitude scaling.
Then specialize at least

[
z_h=h,qquad z_h=h^2,
]

and determine whether the pointwise normalized response vanishes, has a finite nonzero
limit, or diverges. If the four period phases cancel only after a cell average, report
that as a separate averaged object; never replace the pointwise result by the average.

## Required gates

1. Reproduce the exact flat control `E_Q(eta,K(z))=0` from the owned #232 object without reopening its all-edge proof.
2. State the finite metric/solder variables and exact phase/site convention for the slow background; a constant perturbation is not a slow-background test.
3. Compute the first nonzero mixed `h^m z^n` metric-response tensor component(s) exactly; no numerical cancellation certifies zero.
4. Check all four period phases and report pointwise and phase-averaged responses separately.
5. Evaluate both `z_h=h` and `z_h=h^2`.
6. Compare the resulting order with the `h^{-2}` normalization from #226 and the smooth Einstein seed from #216/#223 only within their owned hypotheses.
7. If an obstruction appears, verify it belongs to the curved nongauge #232 family and is not a gauge/flat artifact or a merely connection-stationary #227 control.

## Terminals

Use `J2-DIAGONAL-MICROSTRUCTURE-SLOW-BACKGROUND-RESPONSE-NULL` only if the exact
calculation shows that the declared #232 microstructure contributes `o(h^2)` to the
pointwise metric response for the tested slow-background class and scalings.

Use `J2-DIAGONAL-MICROSTRUCTURE-EINSTEIN-RESPONSE-OBSTRUCTION-FOUND` only with an exact
nonzero coefficient producing an `O(h^2)` or larger normalized pointwise response
obstruction under a declared scaling.

If neither terminal is reached, keep the PR Draft/BLOCKED and name the exact first
missing mixed coefficient, background jet, or comparison convention. A phase-average
null result by itself is not the positive terminal.

## Scope fences

No new action density, Holst term, torsion constraint, spectral filter, boundary selector,
or connection-selection principle. No Lean-owner edits, claim/release-status promotion,
BOOK/public-claim edits, #202 edits, or child-task creation. This worker supplies an exact
finite hostile response input to the EXPENSIVE lane; it does not prove a continuum theorem.

## GitHub execution contract

Start from fresh current `main` only after this brief and manifest row are merged there.
Run `python tools/task_lifecycle.py start WRK-A4D-DIAGONAL-MICROSTRUCTURE-SLOW-BACKGROUND-RESPONSE` as the first task-branch change,
then open the Draft PR before any scientific artifact or certificate is added. Keep all
results in that PR, refresh against current `main`, run repository guards, retire the
task in the same PR before Ready, set `Lifecycle: REVIEW`, and never self-merge.

## Chat handoff

Return the execution PR number and head SHA, the terminal or exact blocker, the first
nonzero `h^m z^n` response coefficient, the pointwise versus averaged verdict for
`z_h=h` and `z_h=h^2`, and the validation/certificate commands. Do not paste the
full derivation into chat.
