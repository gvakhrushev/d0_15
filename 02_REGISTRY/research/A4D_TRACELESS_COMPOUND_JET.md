# Traceless heat jet is the compound, not the radial balance

Input: owned compound law `W_Q^k = sqrt|det Q| * compound_k(Q^{-1})` and the radial theorem `H'(0)=2*E_beta` on `q(t)=exp(2t)q`.
Status: calculation on that law. Not a native preparation and not a rho0 comparison.

## What the radial path actually uses

In dimension 4, `det(exp(2t)Q)=exp(8t)det Q`, so `sqrt|det|` scales by `exp(4t)` and `compound_k(Q^{-1})` by `exp(-2kt)`. The product is the owned grade law `exp((4-2k)t)`. Consecutive grades then differ by `exp(-2t)`, which is equation (2) of the radial-balance memo and the source of `H'(0)=2*E_beta`.

## Traceless variation

Let `Q=I+eps*A` with `A` symmetric and `tr A=0`. Then

```text
det(Q)=1+O(eps^2),    sqrt|det Q|=1+O(eps^2).
```

The determinant factor is stationary on this traceless path. For a spatially
constant Q its common scalar multiplier cancels from W^{-1}d^T W even on
the radial path: the radial adjoint response comes from the relative
compound weights of consecutive degrees. The first-order weight change
on the present traceless path is only the compound:

```text
Q^{-1}=I-eps*A+O(eps^2),
W^k(eps)=compound_k(I-eps*A)+O(eps^2).
```

A 2-dimensional check: radial `A=lam*I` leaves `W^1` unmoved at first order, while traceless `A=diag(a,-a)` plus off-diagonal `b` moves `W^1` by `eps*diag(-a,a)` and off-diagonal `-b*eps`. So the radial theorem does not constrain this jet.

If the spectrum depended only on the conformal factor, the first derivative along a volume-preserving circle would average to 0, and the second-order average of one heat mode would be `beta*mu*(beta*mu-2)*exp(-beta*mu)/2`. The compound deformation shows that this conformal reduction is false at first order: a traceless `A` changes the adjoint before any second-order det term.

## Consequence for the vector

The next certificate is not another radial contraction. It is the derivative of the same bootstrap `H` along `compound_k(I-eps*A)` for traceless `A`, projected onto the constraint tangent with `tr A=0`. The radial balance remains the admission condition on the dilation ray and does not answer the nine traceless components.

The [constant-metric heat calculation](A4D_NATIVE_POSITIVE_HEAT_RADIAL_BALANCE.md#5-all-ten-flat-heat-coefficients-and-a-nonzero-traceless-response)
now supplies all ten coefficients for this positive Hodge binding and a
uniformly nonzero traceless response at an anisotropic flat metric, with
an explicit version for every fixed positive beta. A nonzero adjoint jet
alone would not establish this price response; the full retained heat
trace is differentiated. Full local joint variation, native preparation
and the rho0 comparison remain separate open obligations.
