# Independent review: Hermitian memory tangent span

Assembly-Acceptance: lean-memory-tangent-span-to-mv-slot 6a6ee2276dd51bf6cae7f9bfa552b5e55167d3e24fe846d86b44ec0cff884d8e

Decision: ACCEPT for the scoped `mv_tangent_span` obligation only.

Reviewer: Codex CONTROL independent reviewer (merge_research_intake, 2026-10-20).
Result owner: PR #353 / WRK-A4D-LEAN-MV-TANGENT-SPAN (original worker).

## Reviewed statement and published evidence

The reviewed assembly application is
`lean-memory-tangent-span-to-mv-slot` at published commit
`16b8b0b749dc49554ee521ca0aa97c6bc06bb5c4`.

GitHub's commit API identifies its tree as
`8cd22f624eceaa53d59382cb1284ae3785df373f`. This is exactly the tree of
the independently reviewed local frozen commit
`95365482b511e7fc33c02d89173a38bc2029fcd8`; the published reference is the
durable review target. The application digest was independently recomputed
as `6a6ee2276dd51bf6cae7f9bfa552b5e55167d3e24fe846d86b44ec0cff884d8e`.

The original task brief at
`304a6dd3c53b7cf3c35353fbdc40aa0444fc77ec` asks for the generic finite
Hermitian-matrix equivalence: vanishing of `Tr(S M)` against every
admissible Hermitian traceless source-neutral test `S` is equivalent to
membership of `M` in the real span of `{I,J1,J2,J3}`. It does not ask
for a physical operator or a field equation.

The proof owner is
`03_FORMALIZATION/D0/Research/MemoryTangentSpan.lean` at published source
commit `304a6dd3c53b7cf3c35353fbdc40aa0444fc77ec`, SHA-256
`c7b8ac25b6dbc20752e95ebe6d5220fb82170d0c6baccf51bc5416f8f47f78fa`,
Git blob `63157d8b3fceb61db487ba2cac82441acab616d6`.

Its bytes are identical in the reviewed published tree. The terminal theorem
is `D0.Research.MemoryTangentSpan.trace_vanishes_iff_memRealSpan`.
Both directions have explicit proof owners:
`admissible_trace_vanishes_of_memRealSpan` and
`memRealSpan_of_admissible_trace_vanishes`.

## Hypotheses and interface maps

The application uses the direct method on the identical `mv-span-v1`
interface. No carrier transport or additional scientific dependency is used.

- `finite_index` maps identically to the target hypothesis: one fixed finite
  index type `n`, with decidable equality, throughout the statement.
- `hermitian_data` maps identically to the target hypothesis: `J1`, `J2`,
  `J3` and `M` are Hermitian matrices on `n`; admissible `S` range over
  all Hermitian matrices satisfying `Tr(S)=0` and `Tr(S Jr)=0`
  for each of the three fixed sources.

The carrier is the real vector space of Hermitian complex matrices.
The span coefficients are real. The trace convention is unchanged:
the proof explicitly identifies the real part of `Tr(S J)` with that
complex trace when both arguments are Hermitian. The identity component
is represented by the tracelessness condition.

No linear independence of `{I,J1,J2,J3}`, invertibility of its Gram
matrix, or physical interpretation of the matrices is assumed. No
continuum or refinement map is asserted.

## Applicability argument

Let `L_i(S)=Re Tr(S source_i)` for the ordered quadruple
`source_i=(I,J1,J2,J3)`, and let `K(S)=Re Tr(S M)` on the real
Hermitian matrix space. The admissibility constraints are exactly the
intersection of the four kernels, using the proved real-trace identity.

Vanishing against every admissible test gives
`intersection ker(L_i) <= ker(K)`. The dual-space span lemma therefore
expresses `K` as a real linear combination of the four forms.

The residual matrix `R=M-sum_i c_i source_i` is Hermitian and pairs to
zero with every Hermitian matrix. Testing against `R` itself gives
`Tr(R R)=sum_ij |R_ij|^2=0`, so `R=0`. This establishes real span
membership. The converse follows by linearity and the four neutral
trace conditions.

The resulting equivalence is precisely the original bounded task
terminal and the statement owned by `mv_tangent_span`. The finite
controls additionally preserve the distinction between tracelessness
and source-neutrality and demonstrate why a single-vector ray identity
does not replace the full matrix-span statement.

## Boundary and remaining assumptions

This acceptance supplies only the generic finite-dimensional
`mv_tangent_span` support premise on `mv-span-v1`.

The finite-index and Hermitian-data hypotheses remain explicit. Any
physical use must separately establish that its actual matrices and
complete admissible variation class satisfy this interface. Identifying
the source data with the memorandum's `B_r` does not construct or select
a physical operator.

This decision does not discharge `matter_source_ward` on
`native-programme-v1`. It does not establish the full native action,
physical matter-source identification, the joint Ward identity,
on-shell stationarity, a nonlinear curved solution, refinement-uniform
transport, or GR closure.

The independent review checks the exact statement, proof structure,
immutable source bytes, published tree identity and application maps.
Actual Lean build validation for the integration is a separate PR gate;
no Lean build was rerun as part of this bounded review.
