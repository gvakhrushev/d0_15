# Original stopped futures close the native marginal entropy source

22 October 2026. Existing scientific Draft [#334](https://github.com/gvakhrushev/d0_15/pull/334),
`constitutive/native-programme-v1`. Same-execution source composition;
`GR_closed=false`.

## Exact consumer

The [proof](PROOF.md), especially section 2a, applies to the **original
full128 first-anchor/first-match instrument**, with its existing declared
comparison cap `K>=d-1`, all mismatch/final-match/cap-abort leaves and
oldRIGHT retained. Its two actual special outcomes are

\[
K_0=B=I-2p^2\Delta>0,\qquad K_1=-2p\sqrt p\,\Delta.
\]

The already retained prefixes `(1,0,...,0)` contain no match: the original
comparator compares the full128 label, including the port bit. Summing
their complete remaining stopped subtrees gives real unconditioned
effects

\[
F_n=4p^3\Delta^2B^{2n},\qquad n=0,\ldots,d-1.
\]

These probabilities fix every spectral block weight. A polynomial
certificate puts `log(rho_*)` in their linear span, so any state `sigma`
with the same probabilities obeys

\[
S(\rho_*)-S(\sigma)=D(\sigma\Vert\rho_*),\qquad
\rho_*=\Delta^{-1}/\operatorname{Tr}\Delta^{-1}.
\]

Thus the actual dynamically selected inverse-square DATA state is the
unique maximum-entropy representative for these retained responses,
for **every positive native spectrum**. A more informative retained
family has the same maximizer at `rho_*`. Its marginal gain satisfies

\[
0\le I_F(\rho,y)\le I_{\rm blank}(\rho,\Delta_y)
\le D(\rho\Vert\rho_*(y)).
\]

This supplies the concrete substitution into the stationary-section /
native Poisson source: the marginal gain is identically zero on
`rho_*(y)`, all its total field jets are zero, and its independent DATA
first reaction and canonical primitive-DATA Poisson adjoint are zero.
The full-future maximizing map need not equal the blockwise-uniform
conditional expectation away from that section; normal input Hessians
need not vanish.

For a known two-band CAR16 fixture, cap `K=1` suffices. A fixed cap
`K=15` covers arbitrary positive spectra on that sixteen-dimensional
carrier and executes at most sixteen original rounds. Increasing a
previously smaller cap is still a paid change. The proof also gives a
separate fixed-horizon fifteen-round realization through ordinary blank
prefixes; it is not confused with an all-blank stopped leaf, which ends
after its second round.

**Preserved source terms:** the original complete stopped charged
operator, every comparison/controller/factory cost, full temporal CQ
information, finite preparation prefix and independent RIGHT equations.
No physical Book03 Info, fixed-temperature Gibbs law, actual Hodge/cut
identification, full42 transport or uniform refinement is selected here.
The central conditional expectation is a mathematical entropy map;
no inverse, spectral projector or new detector is executed.

## Exact input pins

All inputs below were read and their local bytes matched this immutable
checkpoint: `82d27e83b0ba0869911de80919de50c42f2944d8`.

| Consumed input | Git blob |
|---|---|
| [Original native constructor](../d0_book_uniform_source_2026-10-21/check_uniform_book_source.py) | `ee8de4635d24c668949ac9a0186616ab7d59f2ed` |
| [Original complete stopped execution](../d0_first_match_wald_2026-10-22/SEQUENTIAL_FULL128_BOOK_RETURN.md) | `2d5f49cf9c6c72f4da3bc5f587a3827eb30992c4` |
| [Native invariant preparation](../d0_native_preparation_closure_2026-10-21/PROOF.md) | `2dde923ce481a00db4928a9467819ccdb73cae5a` |
| [Prior one-port entropy application](../d0_native_complete_cq_source_2026-10-22/MAXIMUM_ENTROPY_PREPARATION.md) | `fcf4cd4b718fc71451c97c8ee68f76ae7416f9fb` |
| [Complete quantum-history source](../d0_native_complete_cq_source_2026-10-22/COMPLETE_HISTORY_SOURCE.md) | `cbd85b5173563f0f7bc5b17a31ddef7562916dff` |
| [Native entropic Poisson source](../../A4D_COMPLETE_NATIVE_FIRST_MATCH_ENTROPIC_POISSON_PREPARATION_AND_HESSIAN_2026_10_22.md) | `789e495d670ac2c5e8d880652a8924d2bf399877` |
| [Stationary-section source](../d0_coupled_cut_partition_2026-10-22/STATIONARY_SECTION_AND_WRITER.md) | `0d29bd25162f046436e8217fa108357d0f55952b` |
| [Actual channel and port cost](../../A4D_COMPLETE_RECORD_CHANNEL_AND_NATIVE_COST_SOURCE.md) | `df8611c7fa37fa71e883831b3f01f434532d99ce` |
| [Book06 retained-test entropy semantics](../../../../01_BOOKS/BOOK_06_EVOLUTION_FORGETTING_AND_TIME.md) | `99721fb50de66688564638f5f2b449a38675d7bd` |

## Bounded validation

[The checker](check_blank_future_entropy.py) loads only six definitions
from the pinned original constructor. The [frozen receipt](RESULT.json)
records **27 scoped checks**, including the newly added original
stopped-prefix effects and their complete first jets. The old 173-check
packet and original all42/full128 suites were not rerun.

The [independent review](INDEPENDENT_REVIEW.md) passed the final proof
and code, replayed these 27 checks read-only with exact receipt agreement,
and verified all nine input pins. Proof, checker and receipt bytes were
unchanged during that replay.

For the actual original CAR16 boost `r=1/9`, the largest stopped-prefix
effect and source errors are `6.18e-18` and `2.72e-18`. The genuine
retained leaf `(1,0^15)` has probability approximately
`0.000130857097896`, so the cap-abort is not removed. The receipt also
checks a noncommuting equal-moment competitor, exact rational weighted
three-band interpolation, and a hostile sign-colliding blank control.
The three-band matrix control is not claimed as another native fixture.

The all-spectrum and source statements are analytical proofs. Numerical
diagnostics are not interval enclosures or uniform conditioning bounds.
The receipt separately records the surviving charge of the fixed-horizon
alternative and the anchor-one **part** of the stopped port charge;
neither is mislabeled as the entire stopped physical price.

Read-only reproduction from the repository root:

```bash
python3 -B 02_REGISTRY/research/sources/d0_native_blank_future_entropy_2026-10-22/check_blank_future_entropy.py
```

The output can be compared with `RESULT.json`. Receipt creation is a
separate explicit `--write-result` authoring mode; reproduction does not
write or update expected evidence. Proof and checker SHA256 pins are in
the frozen receipt.
