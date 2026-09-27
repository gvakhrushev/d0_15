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
