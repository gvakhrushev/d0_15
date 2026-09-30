# Curved Y symbol: an unconditional uniform inverse on a physical symmetry sector

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, PR #310.
This is a theorem for a proper symmetry sector at the flat `z=1` Y vacuum,
not the all-Bloch premise or a fixed-curved-background response theorem.

Let `L` be divisible by four. In the unfolded four-phase Fourier carrier,
restrict the link field to the subgroup of characters

\[
\Omega_L=\{(q,qr,qr,qr):q^4=1,\ r^L=1\}.
\]

This is the fourfold phase orbit of the spatial-diagonal line. It is
closed under products and conjugation. Intersect it with the owner's
physical phase-support condition; the result is a nonzero translation
symmetry sector preserved by the literal local Euler map. Write the
owned physical coordinate split as `u=Bw+Cc`, and let `D_G c` be the
six phase-resolved graph differences. There is a constant `C`, independent
of `L`, such that for every field in this sector and every `1<=p<=infinity`,

\[
\boxed{\|w\|_{p,\mathrm{comp}}+\|D_{\mathcal G}c\|_p
\le C\|Q_{\rm shift}(Bw+Cc)\|_{p,\mathrm{comp}}.}
\]

In particular this holds in the actual unweighted owner sum norm `p=1`.
It keeps the physical constant Y amplitude as a genuine modulus; the
estimate controls its graph differences, not its value.

## Proof of the uniform estimate

On `lambda=(1,r,r,r)`, the [full-line exact certificate]
(A4D_Y_CURVED_JOINT_SPATIAL_DIAGONAL_FULL.md) gives `rank Q=96` for
every `r in S^1` except `r=1`. At `r=1` the rank is 95 and the kernel is
the owned Y center. The [center-gradient module]
(A4D_Y_CURVED_JOINT_CENTER_GRADIENT_MODULE.md) constructs an analytic
matrix `M` near this fold with `T=MQ`, where `T=(P,D_G A)` is exactly the
94-complement-plus-graph-gradient target. Away from the fold, the smooth
left division

\[
M(r)=T(r)(Q(r)^*Q(r))^{-1}Q(r)^*
\]

is valid. A smooth partition of unity on the circle glues these exact
divisions, giving a smooth periodic `M(r)` with `T(r)=M(r)Q(r)` everywhere.
Its Fourier coefficients are absolutely summable, so the periodized
one-dimensional convolution has an `l^p` norm bounded by their sum,
independently of `L`.

The literal phase covariance, checked coefficientwise in the owned
stencil and target, is `Q(q lambda) D_col(q)=D_row(q) Q(lambda)` and
`T(q lambda) D_col(q)=D_target(q) T(lambda)`, where each diagonal entry
is `q` to minus its phase index. These diagonal matrices are unitary
for `q^4=1`, so the division transports from `q=1` to all four copies.
Fourier projection onto each copy and onto `Omega_L` is an
average of translations with coefficients of modulus at most one; hence
its `l^p` norm is bounded independently of `L`. Summing four sectors
changes only a fixed fibre constant. Restricting back to physical
phase-supported fields gives the displayed estimate. No continuum
limit, finite-grid extrapolation, or unproved all-torus rank assertion
enters this argument.

The same proof gives a broader **linear** result. Regard the continuous
fourfold line `Omega` as a compact subset of the physical torus. Away
from its four folded points, full joint rank is an open condition. At
those points the owned local analytic division gives `T=MQ` on an open
neighborhood. A finite cover and partition of unity therefore produce
an open neighborhood `U` of all of `Omega` with a smooth exact division
`T=MQ` on `U`. There is some `epsilon>0` such that the torus
`epsilon`-tube around `Omega` lies inside `U`. Multiply `M` by a smooth
cutoff equal to one on a smaller tube and extend it by zero. Its
four-dimensional Fourier coefficients are absolutely summable.
Consequently the displayed refinement-uniform `l^p` estimate also
holds for fields whose Fourier support lies in that smaller tube.
Neither `epsilon` nor the operator constant is numerically certified.
Nonlinear products need not stay in the tube; the flat nonlinear
consequence below uses the exact subgroup `Omega_L`.

## Flat nonlinear consequence in the same sector

For the exact flat chart `K=K_Y(1+c) exp(Bw)`, the owned all-row
finite-stencil remainder satisfies

\[
\|R(c,w)\|_p \le
1152\|c\|_\infty\|D_{\mathcal G}c\|_p+
C_r(\|c\|_\infty+\|w\|_\infty)\|w\|_p,
\]

where `C_r` is uniform in `L` on a fixed compact chart. The symmetry
sector is closed under the local nonlinear operations. Therefore there
is a chart radius `rho>0`, independent of refinement, such that every
exact flat joint-critical field in this sector satisfying
`||c||_infinity+||w||_infinity<rho` has `w=0` and `D_G c=0` by absorption.
The even-carrier graph is connected, so `c` is constant. Conversely a
constant Y amplitude is the owned exact nongauge joint vacuum. Thus the
local flat stationary set in this sector is exactly the Y family.

This does not classify general four-dimensional Fourier fields. For a
fixed smooth nonconstant sampled metric, its coefficients break the
sector symmetry and the mixed current requires a separate uniform
estimate. No normalized response terminal follows from this theorem.
