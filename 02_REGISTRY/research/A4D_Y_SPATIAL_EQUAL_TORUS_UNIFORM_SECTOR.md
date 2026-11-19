# Curved Y joint symbol: complete spatial-equal torus and uniform sector

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, PR #310.
This is an exact continuous physical two-torus theorem and a flat-sector
uniform inverse, not the full four-torus or the curved-response terminal.
It is centered at the finite-amplitude z=1 Y vacuum. The
[designated identity-sheet full-gap obstruction]
(A4D_DESIGNATED_FULL_GAP_OBSTRUCTION.md) concerns a different background
and does not conflict with this symmetry-sector estimate.

## Exact rank theorem

For the literal 136-by-96 full joint Bloch symbol at the constant z=1 Y
vacuum, set

\[
\lambda=(\mu,\mu r,\mu r,\mu r),\qquad |\mu|=|r|=1.
\]

The two exact certificates below prove that Q has rank 96 except at
r=1 and mu^4=1. At each of those four folds its rank is 95 and its
kernel is the owned one-dimensional physical Y center. This covers the
continuous two-real-dimensional subtorus, not a finite character grid.

The spatial 3-cycle and an odd spatial swap accompanied by fast-phase
+2 act as signed permutation representations. All seven nonzero
bivariate coefficient matrices of 14*mu*r*Q intertwine both actions.
The 96 inputs split as 16 trivial, 16 sign and 32 copies of the
two-dimensional standard representation; the outputs split as 24, 24
and 44 copies. On each standard copy a swap-minus vector generates the
swap-plus vector by (I+swap)*cycle. Full column rank is therefore
equivalent to ranks 16, 16 and 32 on three smaller exact blocks.

For the sign block, a connection-only determinant is a nonzero monomial
times F(mu,r)F#(mu,r), with F#=mu^8*r^4*F(1/mu,1/r). On the unit torus
F# is a nonzero monomial times the complex conjugate of F. A second,
metric-containing determinant is a nonzero monomial times

\[
(\mu^2+1)(3\mu^2r+r+2)(8\mu^2r-\mu^2+7)
(r-1)^2(\mu^2r^2+1).
\]

The two nontrivial middle factors can vanish on the unit torus only at
mu^2=-1,r=1, by taking their absolute values. At mu=+/-i, F is (r-1)
times a cubic with reciprocal gcd one. At r=1, F is (mu^4-1) times a
quartic with reciprocal gcd one. The resultant of F and mu^2*r^2+1 is
(mu^2+1) times a degree-14 polynomial with reciprocal gcd one. Thus
the two sign charts have no common physical zero outside the folds.
The trivial determinants are exactly their sign counterparts after
mu -> i*mu (up to an overall sign), so the same argument applies.
Exact folded ranks alternate: trivial has 15,16,15,16 and sign has
16,15,16,15 at mu=1,i,-1,-i.

For the 32-column standard block, the connection chart is a nonzero
monomial times F32 of bidegree (32,32). The metric chart is a nonzero
monomial times

\[
(\mu r-1)(\mu r+1)(r+1)^2(r-1)^6(\mu^2r^2+1)G12,
\]

where G12 has bidegree (12,12). Exact elimination gives

\[
\operatorname{Res}_r(F32,G12)=c\mu^{144}P(\mu^4),\qquad
\deg P=120,\qquad
\gcd(P(w),w^{120}P(1/w))=1.
\]

Since P has real coefficients, it cannot have a unit-circle root:
any such root would also belong to its reciprocal. The remaining
simple factors lie on r=+1, r=-1 or mu*r in {1,i,-1,-i}.
On r=+1, r=-1 and mu*r=1, two independent exact univariate standard
minors have gcds x^12, x^16 and x^48. Their only common roots are the
excluded x=0. Common quarter-phase covariance transports the last line
to all four fourth roots; its phase diagonal preserves the standard
isotypic subspace. Hence the standard block has rank 32 everywhere on
the physical two-torus. The two block arguments give the rank theorem.

The certificates build the literal rational stencil and all determinant
coefficients; they pin chart rows and a digest of the large resultant.
They use integer, rational and Gaussian-rational arithmetic only.

```sh
python3 02_REGISTRY/research/certificates/a4d_y_curved_joint_spatial_equal_s3_check.py
python3 02_REGISTRY/research/certificates/a4d_y_curved_joint_spatial_equal_torus_check.py
```

## Uniform nonlinear-invariant sector

For L divisible by four, restrict physical Fourier support to the
subgroup

\[
\Omega_L^{(2)}=\{(\mu,\mu r,\mu r,\mu r):\mu^L=r^L=1\}.
\]

It contains both previously certified one-dimensional sectors and is
closed under products, conjugation and shifts. At the four folds the
[owned analytic module](A4D_Y_CURVED_JOINT_CENTER_GRADIENT_MODULE.md)
gives a local exact division T=M Q for the transverse-plus-center-
gradient target T=(P,D_G A). Away from them the rank theorem gives the
smooth division M=T(Q*Q)^(-1)Q*. A partition of unity on the compact
two-torus glues these exact divisions. Its two-dimensional Fourier
coefficients are absolutely summable, and their periodization gives a
convolution bound independent of L. The subgroup and physical-phase
projections are translation averages of norm one. Thus, for the owned
split u=Bw+Cc and every 1<=p<=infinity,

\[
\|w\|_{p,\mathrm{comp}}+\|D_{\mathcal G}c\|_p
\le C_\Sigma\|Q_{\mathrm{shift}}(Bw+Cc)\|_{p,\mathrm{comp}},
\]

where C_Sigma is independent of refinement. In particular p=1 is the
actual unweighted owner sum norm. The constant nongauge Y modulus stays
free. The owned all-row nonlinear remainder is absorbed in a fixed
small chart because this subgroup is product-closed: every exact flat
joint-critical field there is a constant Y vacuum. The weak-metric/
source mixed-current bound from
[the earlier sector theorem](A4D_Y_SPATIAL_DIAGONAL_UNIFORM_SECTOR.md)
also holds on this larger sector when metric, source and solution retain
the symmetry and its stated small-chart norm hypotheses hold.

A fixed smooth nonconstant sampled metric generally breaks this
symmetry. Sitewise O(h^2) data also do not automatically meet the
unweighted sum-norm hypothesis over L^4 sites. The full three-ratio
physical torus, nonlinear curved compatibility and normalized
comparison-response limit remain open.

There is a further exact scope boundary: the
[spatial-equal curvature-tangent theorem]
(A4D_Y_SPATIAL_EQUAL_CURVATURE_TANGENT.md) proves that every smooth
metric tangent in this symmetry sector has zero contraction with the
surviving `-Y tensor Y` normal-jet curvature direction. After the owned
joint compatibility conditions, its linearized curvature is therefore
zero. The sector inverse cannot alone continue that nonflat normal jet.
