# Weighted two-field / non-VSI source continuation

Existing scientific owner: **PR #334**, not a new task. Pinned source snapshot:
`401eafb2958e9d9626db833a25f02b35b3871c16`.

Read [the full proof and source-boundary statement](../../A4D_WEIGHTED_TWO_FIELD_RANK2_AND_FINITE_SOURCE_2026_10_21.md).

## What is supplied

The current repository already proves `d(rho*y/F_x)=0` and the weighted Einstein/source reduction. This packet consumes that proof. It supplies a two-scalar local comparison/converse, an explicit rank-two non-VSI representative in the **original** metric on `Q=0`, an exact actual forward-difference two-material-row lift, and the missing explicit material term of the finite Ward-defect equation.

The seed metric and source are

```
g=diag(r exp(r²/2), -exp(r²/2)/r, -r², -r²), r>0,
psi1=r²/2, psi2=x, mu=1/r²,
Ric=diag(1,1/r²,0,0), R=0,
Ric_ab Ric^ab=2 exp(-r²)/r²>0.
```

The same continuum family was published concurrently by `b5175db6` in `d0_covariant_multiscalar_price/CROSSING_STREAMS.md`; this packet does NOT claim it a second time. The distinct additional consumer is the exact finite two-material-row lift and its connection to the retained finite Ward defect. It is not a VSI/Brinkmann wave or rank-one dust. The FULL two-field source is a counterstream sum. To realize the configured fixed-coordinate CQ equations, use the explicit volume-matching clock `dt/dr=exp(r²/2)/(kappa epsilon²)`, with the **existing finite-z** `kappa=-b/a`, not a fitted constant. Arbitrary positive prescribed PF weights survive because both query densities vanish. The real baseline and its independent upstream derivatives remain outside that field-only statement.

## Reproduce

Dependencies: Python 3.9 or later, NumPy, SciPy, SymPy, mpmath. Exact tested versions and source hashes are in `VALIDATION.json`; the requirements file declares compatible lower bounds, not an assertion that all versions were tested.

```bash
OPENBLAS_NUM_THREADS=1 python3 02_REGISTRY/research/sources/d0_weighted_two_field_rank2_2026-10-21/check_weighted_two_field_rank2.py --repo .
```

For an offline standalone replay from this directory, omit `--repo`. The result explicitly reports that historical Git objects were not re-read locally. `--repo` verifies the immutable object IDs in `SOURCE_INPUTS.json`. `--output new_receipt.json` writes only the chosen new output; the checker never rewrites historical receipts or other repository files.

The supplied `RESULT.json` is the actual NEW local stdout. Ordinary and optimized Python outputs match byte-for-byte. It is not a recreation of the earlier chat's unavailable 65-check receipt. This run has **122 checks** and includes exact continuum tensors/torsion, the literal scalar probability/master law at70 digits, the finite two-field history and a general two-/four-dimensional material source-defect replay.

## Exact next parent input

At a full finite root the derived finite equation is

```
k D+q = -a e_geom + h R_material - r_extra.
```

Here `R_material` is explicit and tested on the original forward-difference density. This line uses the inverse-metric Lie-type tangent. For the literal coframe Lie tangent, retain the additional `-k B:p:p` term proved in section5.1; the two finite tangents must not be conflated. `e_geom` must still be obtained from the ORIGINAL finite coframe/link source on the same Lie-type tangent. None of these terms is set to zero. No complete new finite all42 root, unknown physical Book valuation, paid moving-field writer, arbitrary metric descent or upstream root is claimed.

The new rank-two fixture and its fixed collar are the next actual all40 geometric test. The two material rows already vanish in the reduced finite normal form; their midpoint material field recovers the continuum at O(h²). The continuum result and the finite material result are separate statements.

## Scope and references

- The existing weighted theorem and nonlinear K are inputs, not newly claimed.
- All actual compiler/time/absolute-price obligations remain with their existing owners.
- The stationary normal form does not remove a negative field direction or prove a minimum.
- The local two-field comparison has known constrained/mimetic relatives (arXiv:1310.2790, 1909.01248); no historical novelty, ghost-freedom or general perturbative stability is asserted.
- `GR_closed=false`. New remote CI, Lean, independent review and physical acceptance are not asserted.
