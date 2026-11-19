# Curved Y joint symbol: full spatial-diagonal complex line

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, PR #310.
Status: exact characteristic-zero theorem on one complex line. This does
not classify three independent ratios or the entire physical Bloch torus.

For the literal `z=1` curved-Y joint symbol with all 96 connection and
40 metric rows, put `lambda=(1,r,r,r)`, `r in C*`. Then

\[
\boxed{\operatorname{rank}Q(1,r,r,r)=
\begin{cases}95,&r=1,\\96,&r\in\mathbb C^*\setminus\{1\}.
\end{cases}}
\]

Thus the additional interior rank drop at `r=4/21` is completely rescued
by boundary rows. There is no other full-joint resonance anywhere on this
complex line, including off the unit circle.

## Exact determinant certificate

The owned rational Laurent stencil gives an integer polynomial matrix
`M(r)=14r Q(1,r,r,r)` with entry degree at most two. Take two 96-row
charts: the 96 connection rows, and a chart selected with metric rows
first by exact rational row reduction at `r=3`. Their determinant degrees
are respectively 136 and 130. Exact integer reconstruction and the
finite-field degree bound prove their monic gcd over `Q[r]` is

\[
\boxed{r^{56}(r-1)^4.}
\]

Here is why the modular step is a characteristic-zero proof. Each
determinant has formal degree at most 192. For each prime `p=1 mod 256`,
its values at all 256 roots of unity recover every coefficient modulo
`p` by the exact inverse DFT. The integer coefficient absolute value is
bounded by

\[
B=\prod_{i=1}^{96}\sum_{j=1}^{96}\sum_{k=0}^{2}|[r^k]M_{ij}(r)|,
\]

using the Leibniz expansion. The product of the 21 certified primes
exceeds `2B` for both charts, so signed CRT uniquely reconstructs every
integer coefficient, including all zero coefficients. Both reconstructed
determinants divide exactly by `r^56(r-1)^4`. At the first prime
`998244353`, their modular gcd is exactly this polynomial and their
degrees are still 136 and 130, with nonzero leading coefficients.
Reduction therefore cannot lower the degree of any characteristic-zero
common factor; the exact gcd has degree at most 60. The displayed exact
factor already has degree 60. Finally, the literal matrix has exact
rank 95 at `r=1`.

Replay:

```bash
python3 02_REGISTRY/research/certificates/a4d_y_curved_joint_spatial_diagonal_full_check.py
```

The checker consumes the owned stencil, reconstructs both determinants,
verifies the factor and degree argument, checks the exceptional rank, and
compares its row charts, prime list, coefficient hashes and bounds with
the pinned JSON. It changes no action, source convention, or physical
claim. The three-ratio continuous torus theorem, mixed curved nonlinear
current, and refinement-uniform metric-response estimate remain open.
