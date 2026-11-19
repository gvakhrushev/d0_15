# Full stopped price: field saddle, absolute normalization and native task

Continuation of existing Draft PR #334, 20 October 2026. Research input:
`972ce692a84b5b23bdf91e93a047b1882ad582d4`; integration base `dec8b42a`.
This packet updates the [Russian synthesis](../../../A4D_GOLDEN_FULL_SOURCE_SELECTION_SYNTHESIS_2026_10_20.md)
and is consumed by the existing [causal full-source parent](../../../A4D_CAUSAL_BOOK_SOURCE_TO_EXACT_GR_SYNTHESIS_2026_10_20.md).

The previous adaptive theorem remains valid as a NECESSARY minimum-to-Euler
implication. The new actual native calculation shows that its full-field
minimum premise fails at the flat Einstein–CAR representative and at nearby
nonvacuum roots on each fixed mesh. No stationary Einstein root is removed.
A separate exact result proves that absolute Book normalization determines
whether the same stopped programme family even has a cheapest finite member.

| Result | Proof | Verification |
|---|---|---|
| Actual whole-J2 price has field descent, including complete work | [Field saddle](STOPPED_FIELD_SADDLE.md) | `check_stopped_field_saddle.py`; [independent review](REVIEW_STOPPED_FIELD_SADDLE.md) |
| A zero first-source remainder on the whole neighboring null curve cannot stabilize it; exact second-form requirement | [Residual lemma](CORRECTION_SECOND_JET.md) | `check_correction_second_jet.py`; [integration review](INTEGRATION_REVIEW.md) |
| Same stopped tape and fixed-programme source, different existence/winner under two absolute bindings | [Normalization](STOPPED_INFORMATION_NORMALIZATION.md) | `check_stopped_information_normalization.py`; [independent review](STOPPED_INFORMATION_NORMALIZATION_REVIEW.md) |
| Exact future-observable algebra is M2; this does not choose scalar Info or absolute weight | [Future algebra](FUTURE_ALGEBRA_AND_STOPPED_NORMALIZATION.md) | `check_future_algebra_and_stopped_normalization.py`; integration review |
| Mandatory next record and future completeness do not force a particular unresolved query now | [Task countermodel and conditional construction](FORCED_RECORD_FUTURE_TEST_972CE.md) | `check_forced_record_future_test.py`; integration review |

The five scripts check actual matrices, exact stencil/algebra, capped
complete distributions, and explicit finite countermodels. Universal
statements are proved in the notes and not inferred from a finite scan.
The future-algebra checker uses ordinary assertions and must run WITHOUT
Python optimization. Others use explicit guards. Final normal-mode runs,
Python/SymPy versions and outputs are in [VALIDATION.json](VALIDATION.json).
The two original reviews additionally preserve the checks performed by
their authors/reviewers. They are not conflated with the integration runs.

From this directory, with Python 3 and SymPy available:

```sh
python3 check_stopped_field_saddle.py
python3 check_correction_second_jet.py
python3 check_stopped_information_normalization.py
python3 check_future_algebra_and_stopped_normalization.py
python3 check_forced_record_future_test.py
```

[SOURCE_PINS.json](SOURCE_PINS.json) records original Git blobs and SHA-256
at the inspected commit. [CONTENT_SHA256.json](CONTENT_SHA256.json) covers
this packet except itself. These provenance files do not confer native
admission or physical closure. The original source_selection packet and
its fifteen-check receipt are not rewritten.

Scope: retained actual coframe/shared-link/matter directions, supplied
native query, task and price ledger. Adaptive value has descent, not
necessarily ascent at ties. Nonvacuum persistence is fixed-mesh only.
Conditional normalizer choices are not selected as a physical law. The
abstract task countermodel is not a model of every D0 axiom. Coherent
superpositions of arbitrary programmes and a compulsory total H+J+R price
are not identified with the tested stopped family. GR_closed remains false.

The next parent substitution is the actual total price, its scalar Info
and absolute normalization, and the full residual source. If the existing
Book03 finite stationarity rule is used, its full stack and all independent
variations must be bound to this same execution; it cannot be replaced by
the assertion that the stopped field saddle is a programme-induced minimum.
