# Flat-record inputs now consumed by SOURCE #310

These source files were originally preserved at #323, commit `2e183cd64a3fe65bcb55dff3a4ff9cf94c72b990`. They are copied as the same Git blobs, not re-derived or renamed CORE results.

- [Original synthesis](SYNTHESIS_RU.md): flat golden record, metric rank 10, two internal amplitude modes, conditional intrinsic quadratic-form selection.
- [Exact nonlinear continuation](CONTINUATION_RU.md): variance chart, full gradient metric, two-tick determinant and the distinct information readings.
- [Original checker](check_flat_record.py), [original result](result.json).
- [Continuation checker](check_nonlinear_split.py), [continuation result](nonlinear_result.json).

The [new SOURCE theorem](../../A4D_RECORD_PRICE_METRIC_SOURCE_INTEGRATION.md) consumes these inputs. Its two new outputs are the local metric obtained from the same comparator price, and phase-completed source lifts on nonhomogeneous smooth fields. It links directly to the actual source evaluator rather than introducing another operational flow.

Source preservation, new finite exact checks, mathematical integration and physical admission remain separate statuses. The original texts retain their historical scope; no independent re-audit of every prior proof is implied.
