# Three-ratio fiber: the remaining full-class minor

Task: EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE, Draft PR #310.
Input: e8f948be14e0e84f4da557e12f8317865d71214f.
No H_TORUS claim. No Einstein terminal.

## 1. What is already closed

Designated IR class: A4D_DESIGNATED_IR_RANGE_CLOSURE.md. Fourier support in the #216 ball, quarter center held at the sheet, response -1/2 G + O(h).

Two-ratio plane rho=(1,x,y,1): V(P0,P1,P2,P3) cap (C*)^2 = {(1,1)}, gcd = x^229 (x-1)^11. Interior rank 68 off the fold, 65 at the fold.

Spatial diagonal (1,r,r,r): rank 96 off r=1, gcd r^56 (r-1)^4.

Three-ratio torsion grid, periods 8, 12, 16, 24: interior rank 68 on N^3-1 points, rank 65 only at (1,1,1). Count check: 511+1=512, 1727+1=1728, 4095+1=4096, 13823+1=13824.

## 2. Exact remaining object

The continuous three-ratio chart is rho=(1,x,y,z) in (C*)^3. The 68-row phase-1/2 interior is a matrix over Q[x,y,z] after clearing 14*x*y*z.

Do not rerun the torsion grid. The missing identity is one generic fiber of the owned two-ratio elimination:

Fix z0 in Z, z0 not 0 or 1. Let D_i(x,y) be the four chart minors of the interior at rho=(1,x,y,z0), cleared as in the two-ratio owner. Compute

gcd_Q[x](Res_y(P0,P1), Res_y(P2,P3))

by the same char-zero lift: integer valuation, Schur order at x=1, infinity degree, one good prime.

Pass: the gcd is a power of x(x-1), and the only torus zero is (1,1). Then this fiber has no extra interior zero.
Fail: a torus zero with z0 != 1 is an H_TORUS counterexample on a genuine three-ratio line.

One fiber does not close (C*)^3. It is the same certificate shape as the closed two-ratio plane, and it is the smallest object that can either extend that plane or kill H_TORUS.

## 3. Verdict

Designated IR stays closed. Full class stays PARTIAL/OPEN at this fiber. No new selector.
