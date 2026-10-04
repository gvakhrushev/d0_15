# Native continuum closure: phi-Cauchy tower, pi0 seam

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Input: `720dee65f8c1c186f5862602a4723486eff4b566`.
Status: closure of the continuum reading. Not a raw-owner UV bound.

## Theorem

A continuum state is a thread of the refinement tower, not a point of the full Lorentz domain.

BOOK_07 replaces the real line by the operational equality

```text
|a_k - b_k| <= phi^{-k}.
```

BOOK_02 closes the cycle on a floor by `pi_0 = (6/5) phi^2` in `Q(phi)`, with seam `12/5`, not by the classical period. A thread is continuum-admissible only if its holonomy defect from the identity preparation stays inside that Cauchy ball at every floor and its seam angle lies in `Q(phi)`.

On this class the owned action-probe completion applies. For a smooth metric and probe fixed before the links, and for preparations with log `O(h)` and full connection residual `O(h^2)`,

```text
|T_h - DI(g)[V]| <= C (h/epsilon + epsilon^2),
```

and at `epsilon = h^{1/3}` the error is `O(h^{2/3})`. The unique completion output is the Einstein variation of the unchanged action. This is a limit of readings, not a substituted tensor.

## Exclusion of the full-domain witness

The exact vacuum at `720dee65` uses spatial rotations by a half-turn, `tr P = 0`, and `||P-I|| >= 2` in every node gauge. For every floor `k` with `phi^{-k} < 2` this state fails the Cauchy test against the identity thread. It is not a refinement of a continuum state. Its source `Xi = 0` on the curved cosine warp therefore does not split the continuum observable.

The cosine profile `cos(2 pi y)` imports the classical period. The volume gap `pi^2/2500` is the curvature of that imported circle. It is a BRIDGE comparison, not a CORE equality in `Q(phi)`.

## What remains a different sentence

The raw unweighted owner sum for UV fields without a uniform `C^7` extension is not phi-natural: it counts sites on one floor. This closure does not prove that sum is `O(h)`. The small-chart task in the parent memo stays open until this admissibility is accepted as the native domain. No action term, selector or public claim is added.

Verdict: continuum Einstein is the probe on the phi-Cauchy / pi0-seam tower. The order-2 vacuum is outside that tower.
