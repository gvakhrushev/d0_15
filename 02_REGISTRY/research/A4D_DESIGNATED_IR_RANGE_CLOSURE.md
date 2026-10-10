# Designated IR range closure

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Input: `b0097485b54049be12079d01857c494009991930`.
Baseline: `e80a3b1ccf615fb4f70bf5900181592604928497`.
No action change. No uniqueness claim. No full-class terminal.

## 1. Class

Let `g` be a fixed smooth nondegenerate Lorentz metric on the unit four-torus, `Q_h = g(h\cdot)`, `h=1/L`, `L in 4N`. Let `K_h^sm(g)` be the #216 sheet:

```text
E_K(Q_h, K_h^sm) = O(h^infty) in the #216 Wiener topology,
h^{-2} E_Q(Q_h, K_h^sm) = -1/2 G[g] + O(h)
after the owner ten-slot reconstruction.
```

Declare the IR correction class: `delta` has Fourier support in a fixed ball `|theta| <= theta0` on which the #216 IR parametrix has a period-independent gap, and the quarter-center coordinate of `delta` is zero. Write `K_h = K_h^sm exp delta_R` in that class.

## 2. Range inverse in this class

The full lattice inverse is false: `inf ||H_h u||/||u|| <= C h^{2/3}` by the quarter packet. That packet is excluded from this class by the center constraint and by the IR support. On the IR ball, `det A(1) = 256` and the #216 parametrix is uniform. Therefore

```text
||delta_R|| <= C ||E_K(Q_h, K_h^sm)|| = O(h^infty),
```

with `C` independent of `L`. No `h^{-p}` UV loss enters. `A(1)` is used only as the IR symbol, which is the regime where that replacement is owned.

## 3. Response

The metric readout is Lipschitz on a fixed chart. An `O(h^infty)` correction changes `E_Q` by `O(h^infty)`. After `h^{-2}` the difference with the comparator vanishes. The comparator already reconstructs to `-1/2 G[g] + O(h)`. Hence on this class

```text
E_h(g, K_h) = -1/2 G[g] + O(h).
```

This is the designated IR theorem. It is not response universality, not an owner-sum theorem on unrestricted lattice fields, and not an exact-root theorem outside the IR ball.

## 4. What this does not close

The full stationary class still needs a range inverse off the IR ball. Owned slices (spatial diagonal, opposite-parity line, spatial-equal two-torus, two-ratio characteristic zero, three-ratio torsion grid) leave one algebraic object: the continuous three-ratio interior of `(C*)^3`. Until that rank is 96 off the fold, `H_TORUS` stays open and the unrestricted class stays open.

Verdict: designated IR class closed as a scoped theorem. Full class `PARTIAL/OPEN` at the continuous three-ratio locus.
