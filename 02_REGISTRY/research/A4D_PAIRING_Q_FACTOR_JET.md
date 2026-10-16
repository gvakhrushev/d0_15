# Matter pairing does not cancel the factor heat jet

Input formula, not yet a head owner: `Q=-q+2*v*v^T/k` with `k=v^T*q^{-1}*v>0`.
Status: session check on that formula. Not a heat law and not a source theorem.

## Identities of Q

`Q(lambda*v)=Q(v)` and `Q(-v)=Q(v)`. The time orientation is invisible. On `q -> s*q`, `Q -> s*Q`, so a common dilation preserves the radial heat derivative of a weight built from Q.

On a diagonal `q=diag(q11,q22)` with `v=(1,0)`, `Q=diag(q11,-q22)`. Along the factor imbalance `q11=1+eps`, `q22=1-eps`, both eigenvalues of Q move at first order. A pure tilt of `v` rotates Q and, in the equal-factor model, leaves its spectrum at `{1,-1}`.

## Heat comparison, two-factor toy

Take `beta=log 2`, factor eigenvalues `1` and `4`, and the same Gibbs price used for the radial law, with scales `s1,s2`.

```text
radial H'(0) = 4/3
traceless H'(0) = 4/9
2(E1-E2) = -6
```

The traceless heat derivative is order one and is not the compensating value `-2(E1-E2)`. On the isotropic base both sides vanish, so that case does not test the compensator.

## Consequence

This pairing is a real order-one candidate on the factor tangent, unlike the recorded observer remainder `O(1/L^2)`. It does not by itself cancel `2(E1-E2)`. The next exact step is the same derivative on the owned Hodge weight, not another tilt identity. If that owned derivative also fails to match, the Feshbach coupling jet is the remaining order-one object.
