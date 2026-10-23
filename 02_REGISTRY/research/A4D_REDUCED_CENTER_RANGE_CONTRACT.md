# Reduced center/range contract at the designated sheet

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Pinned input: `d422070d1142c8c6a569450ac3fe9728371310e5`.
Baseline main: `e80a3b1ccf615fb4f70bf5900181592604928497`.
This note executes the typed contract and the first reduced-operator step.
It does not promote a physical terminal and does not alter the action.

## 1. Typed statement

Fix a smooth nondegenerate Lorentz metric `g` on the unit four-torus, sampled as `Q_h=g(h\cdot)` with `h=1/L`, `L in 4N`. Let `K_h^sm(g)` be the #216 smooth approximate sheet, with

```text
E_K(Q_h, K_h^sm) = O(h^\infty)
in the #216 Wiener topology,
h^{-2} E_Q(Q_h, K_h^sm) = -1/2 G[g] + O(h)
after owner ten-slot reconstruction.
```

Write `K_h = K_h^sm(g) exp(\delta_h)` in a genuine Lorentz quotient. Split

```text
\delta_h = \delta_{R,h} + \delta_{C,h}
```

where `\delta_C` spans the physical resonant center (the eight real identity-quarter axes, or their curved-frozen transport) and `\delta_R` is a range complement. Define

```text
D_h(g,K) = R_h[ h^{-2} (E_Q(Q_h,K) - E_Q(Q_h, K_h^sm)) ].
```

The positive closure, if reached, is `D_h -> 0` on the declared exact class, hence

```text
E_h(g,K_h) -> -1/2 G[g].
```

These are two transitions. The difference with the comparator is not itself `-1/2 G`.

## 2. What the first step already has

The literal Hessian is `H_h(g) = D_\delta E_K(Q_h, K_h^sm exp \delta)|_{\delta=0}`.
It is not `A(1)`. Owner `A4D_DESIGNATED_FULL_GAP_OBSTRUCTION`:

```text
rank A(1) = 24, det A(1) = 256,
rank A(i,i,i,i) = 16, rank(A;C)(i,i,i,i) = 20,
inf_{u \neq 0} ||H_h u||_p / ||u||_p \le C h^{2/3}
```

in every `1 \le p \le \infty`, by the quarter packet `v` with role-0 rotation `(1,-1,1)`.
A refinement-uniform full inverse is false. Polynomial loss on the range quotient is allowed.

The identity-quarter owner supplies the response factorization on strictly repeated four-phase fields:

```text
||mean E_Q||_p \le C ||log K||_\infty ( ||E_K||_p + ||\Pi_{\neq 0} E_Q||_p ),
```

constant independent of `L`. If the residual is `O(h^2)` in that norm and `||log K||_\infty \to 0`, then `h^{-2} ||mean E_Q|| \to 0`. Raw Lipschitz of `E_Q` does not give this.

Constant-coframe extension at this head: the same eight single-role/parity axes exhaust the small stationary center for every constant coframe near the identity, with the same residual gain.

## 3. Reduced estimate, scoped

On the repeated four-phase sector, range elimination is the analytic implicit-function graph `w = W(c) = O(|c|^2)` of the identity-quarter owner (normal derivative invertible on the 88 range rows). Therefore

```text
||\delta_R|| \le C ( ||P_R F(\delta)|| + ||\delta_C||^2 )
```

with `C` independent of `L` inside that sector. The `h^{-p}` loss of the full operator is carried by `\delta_C`, not by this range graph.

Transfer to a frozen curved coframe is owned for the quadratic defect of the whole quarter kernel (phase-mean odd curvature cancels on the kernel). Transfer to a genuinely varying coframe is not owned: estimate (6) of the identity-quarter memo cannot be applied cellwise while dropping boundary links.

## 4. Smallest remaining blocker

Gluing the quarter residual gain across a genuinely varying coframe: a commutator of the factorization `||mean E_Q|| \le C ||log K|| ||F||` with `\nabla g`, strong enough that the boundary-link error is `o(h^2)` in the owner sum norm on `Q_h = g(hx)`.

`H_TORUS` remains the algebraic input for a global range parametrix off this sector. It is not the first physical blocker: the quarter sector already has the response factorization, and the missing step is its variable-coframe error.

No action change. No selector. No Einstein terminal.
