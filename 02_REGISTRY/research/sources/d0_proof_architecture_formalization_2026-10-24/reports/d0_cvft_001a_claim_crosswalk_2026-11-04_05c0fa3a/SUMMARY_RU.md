# Compiled crosswalk review for `D0-CVFT-001A`

At clean snapshot `05c0fa3a4662bda0204317b7c794cef280cdfe77`, the claim resolver compiled public import
`D0.All` and resolved all five theorem atoms declared in the existing `claims.csv` row
to the exact modules listed there. This establishes name and module resolution only.

The elaborated signatures show the scope boundary:

- `D0.Dynamics.internal_feedback_forced_by_split` proves only
  `1 ≤ feedbackSlots s` for a `RetainedTracedSplit`.
- `D0.Dynamics.internal_feedback_resolvent_series` takes a `FiniteFeedbackOperator`
  whose Boolean fields `constructedFromPQU`, `finiteResolvent`, and `noExternalMirror`
  are already supplied as true, then returns their conjunction.
- `D0.Cosmology.feedback_determinant_return_cycles` takes a `FeedbackPartitionFunction`
  with `determinantFinite`, `determinantNonzero`, and `returnCycleExpansion` already true.
- `D0.Cosmology.feedback_variation_universal_source` takes a
  `FeedbackVariationSource` whose finite-resolvent, finite-source, and internal-source
  Boolean fields are already true.
- `D0.Cosmology.feedback_pressure_trace_log` takes a `FeedbackPressureLaw` with its
  pressure-from-logZ-derivative and trace-log-finite Boolean fields already true.

Thus the five declared names resolve to their owner modules, but the last four are
field-assertion checks and do not construct a typed matrix operator or derive its source.
The separately compiled moving-projector theorem does construct and differentiate the
finite matrix Book03 price, but it is not one of these five claim atoms and supplies no
map from an admitted physical `P_N`/execution to those matrices. It is retained as a
separately scoped finite-matrix result. No `claims.csv` status, `formal_support` row,
release status, or assembly application was changed.

The five declaration signatures and dependencies are preserved in
[`claim_declarations.json`](claim_declarations.json); hashes and exact source pins are in
[`replay_manifest.json`](replay_manifest.json). The current registry `LEAN_PROVED` and
`CORE-FORMALIZED` values are recorded as source metadata only, not accepted by this review.
