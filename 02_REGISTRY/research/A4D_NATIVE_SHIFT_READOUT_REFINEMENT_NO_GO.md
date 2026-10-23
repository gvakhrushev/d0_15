# Positive-ray affine-shift readout fails native refinement

**Scoped result, 15 October 2026.** The covariant candidate that sends each
nonzero affine edge shift to the D0 CAR record for its positive unit ray
reproduces the four chosen reference returns, and it has a nonzero candidate
metric response. It cannot also be the path-compositional, memoryless unitary
return of that edge. Exact subdivision already contradicts it.

## Owned path law and proposed readout

The joint quotient records an oriented affine edge as `(D,b)` and its native
composition as

```text
(D1,b1) (D2,b2) = (D1 D2, b1 + D1 b2).
```

This is the affine Cartan path law. With both linear parts equal to identity,
two successive copies of a nonzero shift `b` compose to the single endpoint
shift `2b`. In the candidate same-ray readout, positive-pairing normalization
for `G=I` sends both `b` and `2b` to the same observer `n=b/|b|`. Therefore the
readout of the merged path is the same matrix `U` as for one edge.

If the same physical path acts on a fixed instrument carrier by composing its
unitary returns, subdivision instead requires `U(2b)=U(b)U(b)`. The exact
Lean lemma in the adjacent capsule proves the abstract statement: a map from
an additive path carrier to any group that is invariant under doubling and
multiplicative under path concatenation must be identically the identity.

## Actual D0 CAR return witness

At the owned reference `G=I`, `n=e0`, the actual sixteen-component CAR record
operator has a two-dimensional reducing block

```text
        [ a  -p ]
R   =   [ p   a ],        a^2=p,  p+p^2=1,  a,p>0.
```

The exact matrix checker binds this to the existing full-Fock record
construction. It verifies `R^T R=I` and `R != I`. Thus the abstract
subdivision theorem would force `R=I`, while the owned return has a nonzero
off-diagonal coefficient `p`. Directly, `R^2 != R` (its upper-right entry
would require `2a=1`, contrary to the exact positive-root bounds).

This kills the **positive-ray, fixed-carrier, path-multiplicative** shift
readout. It does not kill a stateful history action, a cocycle that retains
subdivision data, a level-changing refinement map, or every native physical
instrument. In particular it is not a global NO-GO for D0. The result says
that the proposed direction-only map discards exactly the magnitude/history
needed to compose repeated affine translations while retaining a nontrivial
unitary response.

## What remains live

The next map must retain subdivision data in the state or act on a larger
history carrier, and must be derived from an existing D0 transition owner.
It must also specify how the enlarged carrier and readout pass through native
refinement. The current 16-state CAR return alone cannot supply this through
positive-ray normalization. No replacement operation or memory postulate is
introduced here.

Evidence: [generic Lean theorem](certificates/a4d_native_shift_readout_refinement.lean),
[exact owner-bound checker](certificates/a4d_native_shift_readout_refinement_check.py),
[compiler output](certificates/a4d_native_shift_readout_refinement_output.txt), and
[result receipt](certificates/a4d_native_shift_readout_refinement_results.json).
Reproduce with:

```sh
python3 02_REGISTRY/research/certificates/a4d_native_shift_readout_refinement_check.py
```
