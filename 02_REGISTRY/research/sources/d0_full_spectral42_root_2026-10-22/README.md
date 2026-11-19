# Exact full spectral root: one unchanged 42-field chart

Read [THEOREM.md](THEOREM.md) for the spectral contract and proof.

The full paired-Hodge heat plus feedback has a unique exact nonflat root in
`B_infinity(spectral_center,1e-25)`. The entire 42x42 Hessian is enclosed by
outward complex interval arithmetic with explicit Cauchy truncation bounds.
Its one global thermal and four constitutive equations give an exact
nondegenerate 47-variable stationary lift, not an unconstrained minimum.

```
python check_spectral42.py
python -O check_spectral42.py
python check_lift47.py
```

These commands print results without rewriting stored evidence. Only
`mpmath` is required. The original geometry implementation and scalar jets
are exact copies of pinned upstream Git blobs; the exact rational collar
and former CQ centre are retained in `inputs/`.

The full normal and optimized interval runs agree byte-for-byte, as do the
47-lift chart checks. See [VALIDATION.md](VALIDATION.md), [RESULT.json](RESULT.json)
and [LIFT_RESULT.json](LIFT_RESULT.json).

The five extra variables are mathematical elimination coordinates, not
independently actuated physical preparers. The chosen paired Hodge is not
identified with compulsory scene heat. Native action/variation admission,
complete apparatus equations and generic refinement are not claimed.
`GR_closed=false`. Existing Draft PR #334 remains the scientific owner.
