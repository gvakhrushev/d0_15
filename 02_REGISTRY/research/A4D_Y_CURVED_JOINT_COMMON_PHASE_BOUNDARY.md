# Curved Y joint symbol: the entire common-phase boundary line

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, PR #310.
Status: exact characteristic-zero theorem on one complex character line.
This does not classify unequal ratios or close the physical response task.

For the literal `z=1` curved Y joint Bloch operator of size `136 x 96`, set

\[
\lambda_0=\lambda_1=\lambda_2=\lambda_3=\mu\in\mathbb C^*,
\qquad w=\mu^4.
\]

Then

\[
\boxed{\operatorname{rank}Q(\mu,\mu,\mu,\mu)
 =\begin{cases}95,&w=1,\\96,&w\ne1.\end{cases}}
\]

Thus the full joint operator has precisely the four folded rank drops on
the entire nonzero common-phase complex line. At each folded point its
kernel is the one-dimensional Y center identified by the folded owner.

## Exact elimination

In a row of fast phase `p` and connection column of phase `q`, a Laurent
coefficient with spatial shift `d` acquires power
`p-q+sum(d)` after multiplying the row by `mu^p` and the column by
`mu^(-q)`. The literal stencil verifies that this power is divisible by
four and lies between `-4` and `4`. These diagonal rescalings are
invertible for `mu!=0`, so the rank is that of

\[
\widehat Q(w)=w^{-1}T_{-1}+T_0+wT_1.
\]

The 68 connection-plus-metric rows in fast phases 1 and 2 have no wrap:
their block `I` lies entirely in `T_0`, has exact rank 65, and has a
31-dimensional right kernel with rational basis `N`. For `w!=0`, multiply
the remaining 68 rows by `w` and restrict them to that kernel:

\[
P(w)=\left(T_{-1}+wT_0+w^2T_1\right)_{\rm boundary}N
       \in\mathbb Q[w]^{68\times31}.
\]

The certificate computes two fixed 31-by-31 determinants of `P(w)`
directly over `Q[w]`. Their degrees are 36 and 42 and their exact monic
gcd is

\[
\gcd(D_0,D_1)=w^{23}(w-1).
\]

The factor `w^23` is irrelevant on the complex character torus, where
`w!=0`. Thus for `w!=1` at least one selected minor is nonzero, and
`P(w)` has column rank 31. At `w=1`, direct exact arithmetic gives
`rank P(1)=30`; together with `rank I=65` this yields full rank 95.
All rank, determinant and gcd calculations are over characteristic zero;
there is no inference from sampled phases or modular agreement.

Replay:

```bash
python3 02_REGISTRY/research/certificates/a4d_y_curved_joint_common_phase_boundary_check.py
```

The script consumes the owned 21-term rational Laurent stencil, checks the
zone-folding law coefficient by coefficient, builds the exact interior
kernel, computes both determinant polynomials and their gcd, checks the
folded ranks, and compares the result with its pinned JSON. It does not
address simultaneous variation of all three ratios, the full physical
unit-torus locus, nonlinear Y-center solvability, or a refinement-uniform
response remainder.
