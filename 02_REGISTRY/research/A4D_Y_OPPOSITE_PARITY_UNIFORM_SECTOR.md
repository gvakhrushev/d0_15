# Curved Y joint symbol: opposite-parity line and a uniform two-parity sector

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, PR #310.
Status: exact characteristic-zero rank theorem and a flat-background
uniform inverse on a proper Fourier symmetry sector. Neither the all-Bloch
rank premise nor the fixed-curved-background response terminal follows.

## Exact complex-line rank

For the literal `z=1` joint Bloch symbol `Q(lambda)` of size `136 x 96`,
consider the opposite-spatial-parity common-phase line

\[
\lambda=(\mu,-\mu,-\mu,-\mu),\qquad \mu\in\mathbb C^*.
\]

The certificate
`certificates/a4d_y_curved_joint_opposite_parity_full_check.py` proves

\[
\boxed{\operatorname{rank}Q(\mu,-\mu,-\mu,-\mu)=96
       \quad\text{for every }\mu\ne0.}
\]

It compiles the same owned 21-term rational Laurent stencil as the
spatial-diagonal and common-phase results. On this line every entry of
`14*mu*Q` is an integer polynomial of degree at most two. Two independently
selected `96 x 96` row charts have determinant degrees 144 and 118. Their
complete integer coefficients are reconstructed by a 256-point exact
finite-field transform over 21 primes. The product of the primes exceeds
twice the Leibniz coefficient bound, so the signed CRT lift is unique.
The first-prime monic gcd is `mu^48`, and exact division verifies that
`mu^48` divides both reconstructed integer determinants. Both exact degrees
are preserved at that prime. By Gauss's lemma the characteristic-zero gcd
cannot have degree greater than the reduced gcd; therefore

\[
\gcd_{\mathbb Q[\mu]}(D_0,D_1)=\mu^{48}
\]

up to a nonzero constant. Its only zero is excluded from `C*`. An
independent rational rank check gives rank 96 at `mu=1`. The certificate
records chart row sets, coefficient hashes, CRT primes and bounds in its
pinned JSON. No numerical singular-value scan is used in this theorem.

## Uniform inverse on a nonlinear-invariant physical sector

Let `L` be divisible by four and restrict the unfolded Fourier support to

\[
\Psi_L=\{(\mu,\varepsilon\mu,\varepsilon\mu,
             \varepsilon\mu):\mu^L=1,\ \varepsilon\in\{+1,-1\}\}.
\]

This is a subgroup of the finite character torus and is stable under the
common fourth-root phase covariance. Its intersection with the owner's
physical phase-supported carrier is therefore preserved by the literal
local nonlinear Euler map. For `epsilon=+1`, the owned common-phase
boundary certificate gives full rank except at `mu^4=1`, where the
kernel is exactly the one-dimensional Y center. The owned folded analytic
module gives a holomorphic division `T=M Q` there, with
`T=(P,D_G A)`. For `epsilon=-1`, the exact theorem above gives full rank
on the entire circle, so `T(Q*Q)^(-1)Q*` is a smooth division. The two
circles are disjoint. A partition of unity gives a smooth exact division
on their disjoint union, including all four folds.

Smooth Fourier multipliers on the two circles have absolutely summable
one-dimensional Fourier coefficients. Periodizing those coefficients on
`Z_L x Z_2` bounds the associated convolution uniformly in `L`. The
phase-support projection is a four-term translation average, also bounded
uniformly in every `l^p`. Consequently, for the owned split `u=Bw+Cc`,
and all `1<=p<=infinity`,

\[
\boxed{\|w\|_{p,\mathrm{comp}}+\|D_{\mathcal G}c\|_p
       \le C_\Psi\|Q_{\rm shift}u\|_{p,\mathrm{comp}},}
\]

with `C_Psi` independent of `L`. In particular `p=1` is the actual
unweighted owner sum norm. The constant Y amplitude remains free.
Because `Psi_L` is a subgroup, products, shifts and pointwise analytic
chart operations preserve the sector. The previously owned all-row flat
nonlinear remainder is therefore absorbed in a sufficiently small chart
with radius independent of `L`: every exact flat joint-critical field in
this sector is a constant Y vacuum, modulo the nongauge constant Y
modulus. The same local calculation yields the weak-metric/source size
bound of `A4D_Y_SPATIAL_DIAGONAL_UNIFORM_SECTOR.md` when both data and
solution retain this sector and the metric is close to `eta` in the stated
norm.

The subgroup generated jointly by `Psi_L` and the previously proved
spatial-diagonal sector contains the full two-dimensional surface
`(mu,mu*r,mu*r,mu*r)`. Full rank on that surface has **not** been proved;
the two sector theorems cannot be combined into a nonlinear theorem on
their union. A fixed smooth nonconstant sampled metric generally breaks
both symmetries. The genuinely three-ratio all-torus premise, curved
compatibility, and normalized response limit remain open.

Replay from the repository root:

```sh
python3 02_REGISTRY/research/certificates/a4d_y_curved_joint_opposite_parity_full_check.py
```
