# A4D HAQ coefficientwise identity

## Result

The accepted metric-response owner in merged PR #270 defines a matrix-valued
polynomial `C(d) = H_AQ(d)` that is homogeneous and linear in
`d_r = z_r^-1 - 1`. Its four exact coefficient matrices satisfy

`C(d) = d_0 C_0 + d_1 C_1 + d_2 C_2 + d_3 C_3`.

The coefficientwise certificate proves

`C(d) vec_sym(d d^T) = 0`

as a polynomial identity. Substituting `d_r = z_r^-1 - 1` therefore gives the
zero Laurent polynomial `C(z) vec_sym(q_0(z))` on `(C^×)^4`.

## Exact coefficient ledger

- Field: `Q`; constant and degree-greater-than-one coefficients of `C` vanish.
- Each `C_r` has shape `24 x 10`, exactly 18 nonzero entries, all with
  denominator 2.
- The ten coordinates are `SYM = [(a,b) | 0 <= a <= b < 4]`; the coordinate
  of `d d^T` is `d_a d_b`, with no off-diagonal `sqrt(2)` factor.
- The cubic monomials are ordered lexicographically descending in
  `d0 > d1 > d2 > d3`, from `d0^3` through `d3^3`. Each of their 24-vector
  coefficients is zero: 480 exact scalar equalities in total.
- The direct Laurent substitution is also exactly zero.

The machine-readable matrices and all 20 coefficient vectors are in
`certificates/a4d_haq_coefficientwise_identity_coefficients.json`. Reproduce
them with:

```sh
python3 02_REGISTRY/research/certificates/a4d_haq_coefficientwise_identity_check.py
```

The checker rebuilds `C` from the merged #270 source, pinned by SHA-256
`d7707248af8a30beb14591991d5a78f37cd73c9fef2ac7c29aae0e8b2003f0b7`, and
stops immediately after construction. It does not run the owner's rank,
kernel, or orbit calculations. It uses the owned `C = H_AQ` symbol, not the
separate J2 census operator also named `HAQ` and not the archived FUGU script.

## Boundary

At `z = (1,1,1,1)`, `d = 0` and `q_0 = d d^T = 0`. Thus this identity does not
establish a nonzero infrared germ there. It also does not transfer to the
conjugated slot `C(conj(z))` or the physical operator `[A(z) | C(conj(z))]`,
and it implies no `E_Q` cancellation, stress result, branch existence,
uniqueness, or continuum claim. Rank and kernel remain owned by #270 and were
not recomputed here.

## What this does not add to the kernel line

Merged #270 already proves the pointwise statement: for every `d != 0`,
`rank C(d) = 9` and `ker C(d) = span{vec_sym(d d^T)}`. The proof is a
projective cover by 9×9 minors whose chart ideals are the unit ideal, plus
the identity `C q = 0`. In particular the rank stays 9 when some, but not
all, coordinates `d_r` vanish. The total collapse `C = 0` occurs only at
`d = 0`, that is at `z = (1,1,1,1)`.

The coefficientwise ledger in this note is the explicit linear decomposition
behind that identity. It does not replace the #270 cover, and it does not
promote the kernel line to a stress theorem. A nowhere-zero holomorphic
section trivializes the holomorphic kernel line off `z = 1`. The normalized
section `q/||q||` is not that holomorphic frame, and its phase around a
divisor `z_r = 1` is not computed here. No monodromy, `c_1`, or `E_Q`
comparison is claimed.
