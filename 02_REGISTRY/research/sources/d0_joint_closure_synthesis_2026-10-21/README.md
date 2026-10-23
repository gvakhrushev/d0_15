# Joint preparation, density rigidity and complete return source

Supporting scientific continuation in the existing Draft PR #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.

The [integrating proof](../../A4D_JOINT_CLOSURE_SOURCE_SYNTHESIS_2026_10_21.md)
states the exact substitutions and physical boundaries. Three mathematical
packets are consumed on their own declared actions:

| Packet | New result | Independent review |
|---|---|---|
| [Centred preparation](../d0_centered_preparation_2026-10-21/PROOF.md) | Exact joint critical-set and minimum equivalence with the diagonal cap2 price; selected preparation source is a material Euler row. | [Review](../d0_centered_preparation_2026-10-21/INDEPENDENT_REVIEW.md) |
| [Density rigidity](../d0_native_density_rigidity_2026-10-21/PROOF.md) | Forced constant densities, all-cap stationary-set and fixed-collar Jacobi-kernel equality, local timelike/null irrotational dust converses. | [Review](../d0_native_density_rigidity_2026-10-21/INDEPENDENT_REVIEW.md) |
| [Complete return](../d0_complete_return_entropy_2026-10-21/PROOF.md) | Uniform complete C1 entropy-source limit with unresolved output, and a rigorous nonzero native source interval. | [Review](../d0_complete_return_entropy_2026-10-21/INDEPENDENT_REVIEW.md) |

The continuum result uses exactly its stated fixed coordinate measure,
constant parameters and independent coframe/connection/scalar variations.
The dust classification concerns the one-real-scalar sector. The cap2
preparation theorem uses the independently varied original material angles
and selected k CAR directions. The return result keeps P/j fixed and its
own monitored information cut. These do not amount to an identified complete
Book03 execution, arbitrary preparation admission or physical GR closure.

## Focused reproduction

Run from the repository root with Python 3. SymPy 1.14.0 and mpmath 1.3.0
were used for the first two scripts; the third uses only the standard library.

```sh
python3 02_REGISTRY/research/sources/d0_centered_preparation_2026-10-21/check_centered_preparation.py
python3 02_REGISTRY/research/sources/d0_native_density_rigidity_2026-10-21/check_density_rigidity.py
python3 02_REGISTRY/research/sources/d0_complete_return_entropy_2026-10-21/check_complete_return_entropy.py .
```

Each script prints its result and verifies its consumed input hashes. No
expected output is rewritten. Actual normal and optimized outputs are in
the individual packets. Author-stage receipts remain unchanged; the attached
independent reviews and [integration review](INTEGRATION_REVIEW.md) record
the subsequent acceptance of the stated mathematical scope.

The [integration receipt](INTEGRATION_VALIDATION.json) records the integrator's
actual focused replays, source preservation, affected structural checks and
scope. The [artifact manifest](ARTIFACT_MANIFEST.json) fixes the resulting
proof, review, source and entrypoint bytes. The three analytical arguments
remain necessary; small exact/numerical fixtures are their targeted controls.

## Concurrent evidence

The original inputs were read at dfc0275e. The published concurrent commits
8463b0a4 and afc4294f are preserved as ancestors. The one append-only changed
source used by density rigidity has its original bytes stored and checked
as a snapshot, without changing its expected hash. See
[concurrent-input compatibility](CONCURRENT_INPUTS.md) and its independent
provenance audit. No unchanged all128, geometry, Book03 comparator or Lean
scientific suite is claimed as newly replayed.
