# #334 §7fh: original full128 instrument to native words

This is a **pinned owner-source intake**, not independent scientific or C0
acceptance. It preserves the complete diff `201ee52c792b7c1f3819224358c3d289756172c0..c4dfd283348093ede9c1ebacefa731abad75d3bd`,
the two complete resulting owner blobs, the exact embedded checker and its
owner receipt, and all 22 pre-insertion input blob and SHA-256 pins. The
[manifest](MANIFEST.json) records them; `original_uniform_source.py` preserves
the exact separate original constructor required by the checker's AST load.
The owner changes neither the #402 brief nor its research source directly.
The earlier [§7fg intake](../d0_334_post_567_201_intake_2026-11-05/README.md)
remains an independent part of this dependency chain.

On the original full128 operator, the one-sided born-frame target
`U_sharp = R(U) B_rec^T` preserves every computational record projection and
prepared output, including the original matrix-valued port charge. With the
existing all-column compiler and the stated actual carrier, helper/reference
input and finite cap, the owner gives a controlled price and source comparison.
The result is an operator/compilation transport under those hypotheses, not an
executed or printed 4096-column native word, exact finite synthesis, or a
mesh-uniform bound. It does not identify the full128 source with the XF source,
select Book03 Info, or establish the complete physical Cost−Info.

In particular, the independent retention-row obstruction in §7fg remains:
transport of this instrument does not cancel or solve that separate source.
The actual prepared/generated input and its derivatives, full stopped-price
and other independent nuisance equations, retained reference, terminal,
clock, work and paid compilation remain to be connected on one execution.
Contract C, physical admission, refinement and Einstein-source comparison
remain open. `scientific_promotion=false`, `GR_closed=false`.

## Reproduction and limits

The [original checker](check_transport.py) is extracted byte for byte. Its
65 conditions classify as 45 nominal numerical, 11 symbolic, 5 structural
and 4 provenance checks. The floating checks use tolerances and **are not
interval certificates**; a passing check does not independently prove every
analytical or physical claim in the owner text.

In an isolated scratch root containing only the pinned original constructor,
normal and `-O` Python 3.12.13 runs with warnings as errors both passed, gave
identical stdout SHA-256 `b391683230bc7e61cbf9b96cde731da09a5c5d0acdd90122e97e32d43214dd64`,
and produced empty stderr. NumPy 2.5.4 and SciPy 1.18.1 differ from the
owner's NumPy 2.3.5 and SciPy 1.16.3; both used SymPy 1.14.0. The local
receipt is therefore not byte-identical to the [owner receipt](owner_receipt.json):
environment, nominal residuals and selected values differ. Both report the
same nominal maximum residual `9.7699626167013776e-15`. The exact owner stack
was unavailable in the offline cache; no identical replay is claimed.

A second environment, Python 3.9.6 / NumPy 2.0.2 / SciPy 1.13.1 / SymPy
1.14.0, failed in both modes under `-Werror` with a divide-by-zero warning in
the original constructor matrix multiplication before any claimed checks
completed. Its stderr is retained rather than hidden or suppressed. Exact
runs, statuses, platform, receipt differences and file hashes are in
[comparison.json](results/comparison.json); the retained stdout and stderr
are in [results](results/).

Integrity verification does not execute owner code:

```sh
python3 02_REGISTRY/research/sources/d0_334_post_201_c4d_intake_2026-11-05/verify_intake.py --verify-source-objects
```

To replay in a cached environment, this runs the pinned owner code in a
scratch directory; it is not a sandbox:

```sh
uv run --offline --python 3.12 --with numpy --with scipy --with sympy python 02_REGISTRY/research/sources/d0_334_post_201_c4d_intake_2026-11-05/replay_bounded.py
```
