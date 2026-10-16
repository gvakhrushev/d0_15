# Curved Y joint symbol: spatial-diagonal interior rank locus

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, PR #310.
Status: exact characteristic-zero theorem on the one-dimensional stratum
`lambda=(1,r,r,r)`, `r in C*`. It is not a classification of three
independent ratios.

For the 68 phase-1/phase-2 connection-plus-metric rows of the literal
`z=1` curved Y joint Bloch operator, write `I(r)` for the resulting
68-by-96 rational matrix.
Then

\[
\boxed{\operatorname{rank}I(r)=
\begin{cases}
65,&r=1,\\
67,&r=4/21,\\
68,&r\in\mathbb C^*\setminus\{1,4/21\}.
\end{cases}}
\]

In particular, the extra interior rank drop at `4/21` is real and exact,
but it lies off the physical unit circle. The **full** 136-by-96 joint
operator has rank 96 there: its boundary rows rescue that interior defect.
At `r=1` it has rank 95 and the owned Y-center kernel.

## Exact certificate

On this stratum every Laurent exponent is `-1`, `0`, or `1`, so `r I(r)`
is a polynomial matrix of entry degree at most two. The checker computes
two fixed 68-by-68 minors over `Q[r]` with exact determinant degrees 73
and 68. Their monic polynomial gcd is

\[
\gcd(D_0,D_1)=r^{45}(r-1)^3(r-4/21).
\]

The coordinate factor `r^45` is a unit on `C*`. Away from the two other
roots at least one minor is nonzero, proving full row rank 68. Direct
exact ranks at the two roots give 65 and 67. A separate exact rank of the
full matrix at `4/21` is 96, so the interior defect cannot be reported as
a joint resonance.

Replay:

```bash
python3 02_REGISTRY/research/certificates/a4d_y_curved_joint_spatial_diagonal_interior_check.py
```

The script constructs both minors from the owned rational Laurent
stencil, computes their characteristic-zero gcd without modular
inference, rechecks both exceptional interior ranks and the full joint
ranks, and compares the resulting ledger with pinned JSON. It does not
address unequal spatial ratios, the all-Bloch physical torus, nonlinear
center solvability, or the refinement-uniform metric-response remainder.
