# Three-ratio fiber: the remaining full-class minor

Task: EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, Draft PR #310.
Input: e8f948be14e0e84f4da557e12f8317865d71214f.
No H_TORUS claim. No Einstein terminal.

## 1. What is already closed

Designated IR class: A4D_DESIGNATED_IR_RANGE_CLOSURE.md. Fourier support in the #216 ball, quarter center held at the sheet, response -1/2 G + O(h).

Two-ratio plane rho=(1,x,y,1): V(P0,P1,P2,P3) cap (C*)^2 = {(1,1)}, gcd = x^229 (x-1)^11. Interior rank 68 off the fold, 65 at the fold.

Spatial diagonal (1,r,r,r): rank 96 off r=1, gcd r^56 (r-1)^4.

Three-ratio torsion grid, periods 8, 12, 16, 24: interior rank 68 on N^3-1 points, rank 65 only at (1,1,1). Count check: 511+1=512, 1727+1=1728, 4095+1=4096, 13823+1=13824.

## 2. Exact z=-1 fiber of the interior block

At the fixed unit-circle ratio `rho=(1,x,y,-1)`, the four owned 68-by-68
chart minors in the normalized ratio chart have an exact CRT reconstruction
and characteristic-zero elimination certificate in
[`a4d_y_curved_joint_zminus1_fiber_check.py`](certificates/a4d_y_curved_joint_zminus1_fiber_check.py)
and its [pinned result ledger](certificates/a4d_y_curved_joint_zminus1_fiber_results.json).
The selected pair is

```text
R03 = Res_y(P0,P3),    R12 = Res_y(P1,P2).
```

Checked integer assignment duals give `ord_x R03 >= 230`, `ord_x R12 >= 272`,
and `deg_x R03 <= 2511`. At the good prime `500000003`, the exact modular
resultants have `deg R03 = 2511` and gcd `x^230`. The primitive-gcd reduction
lemma therefore yields the characteristic-zero identity
`gcd_Q[x](R03,R12)=x^230`. Since `x` is nonzero on the torus, the four chart
minors have no common zero on `(C*)^2`. At every point of this fixed fiber,
at least one selected 68-by-68 minor is nonzero, so the 68-row interior block
has row rank 68.

This closes only the interior block on `z=-1`. It does not prove full column
rank of the 136-by-96 joint symbol: the interior block still has 28 right
kernel directions, and the remaining rows must control them.

## 3. Exact remaining object

The continuous three-ratio chart is `rho=(1,x,y,z)` in `(C*)^3`. The
68-row phase-1/2 interior is a matrix over `Q[x,y,z]` after clearing
`14*x*y*z`. The exact `z=-1` fiber above is one slice only; the generic
`z`-dependent locus remains open.

Do not rerun the torsion grid. The earlier proposed one-fiber test is now
instantiated at `z0=-1` and closed above. The next interior-symbol question is
the genuinely `z`-dependent common-zero set in `(C*)^3`, or a uniform family
of fixed-z certificates that covers the unit-circle complement. The exact
`z=-1` result is only one slice and does not imply the generic fiber.

Even a complete classification of the four interior minors over `(C*)^3`
would not by itself close `H_TORUS`: the 68-row interior block has 28 right
kernel directions, and the remaining rows of the full 136-by-96 symbol must
control them. The full compact-complement rank and the nonlinear response
obligations remain separate.

## 4. Verdict

Designated IR stays closed. Full class stays PARTIAL/OPEN at this fiber. No new selector.
