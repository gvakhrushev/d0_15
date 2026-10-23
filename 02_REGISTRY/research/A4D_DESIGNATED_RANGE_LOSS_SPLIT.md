# Designated range loss versus quarter universality

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Pinned parent: `ef92b92bc906da9292da668f0290231e4da09ba5`.
Baseline main: `e80a3b1ccf615fb4f70bf5900181592604928497`.
This note rechecks the previous blocker and splits it. No action change. No terminal.

## 1. Recheck

`A4D_REDUCED_CENTER_RANGE_CONTRACT.md` named one blocker: glue the identity-quarter residual gain (6) across a varying coframe so that `Delta E_Q = o(h^2)` in the owner sum.

That glue is required only if the declared class includes extra quarter packets on top of `K_h^sm`. It is not required for one designated sheet with center amplitude held at the #216 value.

Inputs rechecked against owners, not re-derived:

- `A4D_IDENTITY_QUARTER_NONLINEAR_RESPONSE.md` (6): on strictly repeated four-phase fields,
  `||mean E_Q||_p <= C ||log K||_inf (||E_K||_p + ||Pi_ne0 E_Q||_p)`,
  and the note explicitly forbids applying (6) cellwise while dropping boundary links.
- `A4D_DESIGNATED_FULL_GAP_OBSTRUCTION.md`: full inverse false, `inf ||H_h u||/||u|| <= C h^{2/3}`.
- Identity-quarter normal derivative: rank 88 on the range rows, invertible. The `h^{-p}` loss sits in the center, not in that graph.
- #216: `E_K(Q_h, K_h^sm) = O(h^infty)` in its Wiener topology, so the center projection of that residual is the same order.

## 2. Designated sheet, scoped lemma

Write `F_h(delta) = E_K(Q_h, K_h^sm exp delta)`, `r_h = F_h(0) = O(h^infty)`.
Split `delta = delta_R + delta_C` with `delta_C` in the physical quarter center.

On the repeated four-phase sector the range graph satisfies

```text
||delta_R|| <= C ( ||P_R F(delta)|| + ||delta_C||^2 )
```

with `C` independent of `L`. Set `delta_C = 0`. Then any solution of the range equations with `||delta_R||` small has

```text
||delta_R|| <= C ||r_h|| = O(h^infty).
```

The phase-common readout (1) then gives `||mean E_Q|| = O(h^infty)` on that sector. After `h^{-2}` this is `o(1)`. This uses only the flat/constant-coframe gain.

Transfer to `K_h^sm(g)` needs one missing estimate, and only that estimate:

```text
the range block of H_h(g), on a complement of the approximate
quarter kernel, has inverse loss at most h^{-p} for some finite p,
uniformly in the owner sum, for the #216 comparison connection.
```

If that loss holds, `h^{-p} O(h^infty) = O(h^infty)`, and the designated difference stays `o(h^2)`. The false full inverse is not used. `A(1)` is not used as an operator norm.

This lemma does not construct the exact root on a varying coframe. It reduces designated closure to the range-block loss.

## 3. Extra quarter packets, still open

Frozen quadratic nullity holds for every constant coframe near the identity, and the phase-mean odd curvature cancels on the whole quarter kernel. On `Q_h = g(hx)` the stencil sees `Q(x+e) - Q(x) = O(h)`. The leading commutator of the frozen null is therefore

```text
e(x) = O(h) |kappa(x)|^2 + O(h) |kappa(x)| |D kappa(x)|
```

per site. In the unweighted sum a sufficient condition for `o(h^2)` is

```text
||kappa||_inf ||kappa||_1 = o(h).
```

No exact joint root on a fixed curved `g` is known to obey this. A quarter packet of width `ell ~ h^{-2/3}` and amplitude `O(1)` fails it. Such a packet is not an exact root; the gap owner only bounds the linear symbol.

So universality over extra centers remains open. Designated closure does not wait on it.

## 4. Verdict

`PARTIAL/OPEN`.

Smallest designated blocker: range-block inverse loss `h^{-p}` on the complement of the quarter kernel for `H_h = D E_K` at `K_h^sm(g)`, one fixed nonconstant smooth `g`, owner sum norm.

Smallest universality blocker: the commutator bound `||kappa||_inf ||kappa||_1 = o(h)` for exact extra centers, or a certified counterexample.

No Einstein terminal. No selector. No uniqueness claim.
