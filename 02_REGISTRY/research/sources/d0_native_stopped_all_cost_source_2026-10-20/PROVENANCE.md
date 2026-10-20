# Provenance and reproduction: stopped Golden all-cost extension

This is a bounded proof/checker packet for existing D0 research owner #334,
not a new scientific task. Files were prepared only in
`/tmp/d0_stopped_extension`. No historical or current upstream file was edited.

## Source inputs

Repository: `gvakhrushev/d0_15`.

Historical commit: `f22c1864bd85e097166abd75dc048164d8d63c65`.

- Proof path:
  `02_REGISTRY/research/A4D_PROSPECTIVE_STOPPED_GOLDEN_MINIMUM_SOURCE_REVERSAL_2026_10_20.md`.
  Its byte-identical snapshot is `upstream_stopped_proof.md`.
  SHA256: `1e2815efc4daab717a7b84069607e287330360093d5a6eaedcfb55c080f9681a`.
- Checker path:
  `02_REGISTRY/research/sources/d0_prospective_stopped_golden_2026-10-20/check_stopped_source_minimum.py`.
  Its byte-identical snapshot is `upstream_check_stopped_source_minimum.py`.
  SHA256: `e022977c672f9c64c9c3ee27d652b009508a2b584b46232ec88c270ff61bbe70`.

Both snapshots were extracted with `git show COMMIT:PATH`, without changing
their bytes. The actual normal-Python failure is retained in
`UPSTREAM_REPRODUCTION.log` and `UPSTREAM_REPRODUCTION.json`.

Reviewed concurrent commit: `1cb164de3753f9dbaf214ea140eb9ea21a7b9d90`.

- Same proof path, byte-identical snapshot
  `upstream_reviewed_stopped_proof.md`.
  SHA256: `ea2016810eb5b7bbc3e41941faf66900d7c0c0b4d97c064f098275102aafc34e`.
- Same checker path, inspected directly at that commit.
  SHA256: `a8997f58d3af738a2cf70f4a1d20dd6c9c509274c8e9b2393157a50038e2729d`.
  This version concurrently corrected the factor-two target, made its checks
  active under `-O`, and added finite-cutoff checks. It is not the failed
  historical snapshot.

The reviewed proof supplies the explicit retained-work conditional entropy
bound and the actual full-pointer first-jet passage. The new theorem consumes
that bound; it does not replace it with an exact scalar off-stratum score.

## Historical failure and lawful one-target correction

At `T=5,ell=1`, exact Golden arithmetic gives

`q2'/q2^2 = 1/(2 p^(3/2))`, `B2=2`, and source `-p^(-3/2)`.

The historical checker computes that source but compares it with
`-2 p^(-3/2)`. Its final assertion consequently fails under normal Python.
The original proof's formulas (8) and (11) already have the correct value.

`corrected_check_stopped_source_minimum.py` changes exactly one source token:

```diff
-    target=-D(2)/(pp**D("1.5"))
+    target=-D(1)/(pp**D("1.5"))
```

No tolerance, assertion, formula producing the source, or earlier check was
weakened. Corrected snapshot SHA256:
`e6f20aa5c9850635165cdaff08f7c4799cdd441aced84be2d64739ac771f901f`.
Its normal-Python pass is retained in `CORRECTED_REPRODUCTION.log` and the same
reproduction JSON. Both historical scripts still use Python assertions; they
are evidence of normal-Python reproduction, not the new active certificate.

`UPSTREAM_TARGET_CORRECTION.patch` is the minimal historical unified diff
against f22. SHA256:
`c08c7806059a61e3cab0372d236882317c7ffe838d9eaf3eaaaf9f9b83257026`.
**Do not apply this patch to current upstream**: commit 1cb independently
resolved the issue already. This packet does not claim authorship of that
concurrent upstream correction.

## New proof and exact certificate

`STOPPED_ALL_COST_SOURCE.md` proves the analytic statements:

- `cos^2(k theta)` belongs to `Z[p]`; its conjugate and nonzero integer norm
  give `1-q_k>p^(5k)` for every positive integer k.
- The minimum exists for every finite real `T>=5,ell>=1`.
- `R_k=k/q_k` has unique minimum k=2. Every ell-price minimizer lies below
  the unit-price k2 score, without necessarily minimizing the unit-price score.
- Every minimizing branch has `k<T/12+13/3` and `B_k>=2`.
- Each branch source has exactly the same zero equation as the full `dJ2`.
- A true local minimum of the actual optimized score, with fixed prices and
  a full two-sided admissible field neighborhood, necessarily has `dJ2=0`,
  including at selection ties. No envelope differentiability is assumed.

`check_stopped_all_cost_source.py` uses only the Python standard library and
exact rational arithmetic. It independently replays the whole finite-window
proof with certified rational logarithm enclosures; verifies the required
Golden field and hyperbolic-comparison identities; checks the tail-bound
algebra and rotation-price comparison; and rejects the historical wrong
source normalization. Every check uses an explicit active `require`.

The finite k controls are tests of identities used in the proof, not a
substitute for its unbounded-k norm argument, irrationality or minimum
existence. The new checker does not rebuild geometry, enumerate enormous
histories or rerun old full128 experiments.

## Exact commands

Run these in this packet directory. The first exit status is intentionally
nonzero and was preserved as such:

```bash
python upstream_check_stopped_source_minimum.py
python corrected_check_stopped_source_minimum.py
python -O check_stopped_all_cost_source.py --output STOPPED_ALL_COST_RESULT.json
python check_stopped_all_cost_source.py
```

The original run exits 1 with the factor-two `AssertionError`. The corrected
historical run exits 0. The independent new checker exits 0 both normally and
under `-O`. `VALIDATION.json` records exact byte comparison of the normal and
optimized output with the saved scientific receipt, and the absence of
`ast.Assert` nodes in the new checker.

The scientific receipt has only exact integers, strings, booleans and hashes;
it has no floating diagnostics, timestamp, current directory, or platform
fields. Normal and optimized runs therefore compare byte-for-byte. The raw
historical failed-run traceback retains its original execution path as
historical evidence; it is not regenerated during a portable certificate run.

## Scope retained

The all-cost theorem is conditional on the specified first-port1 stopping
task, actual original code, declared full-pointer information, fixed prefix
and per-rotation costs, and the inherited full-field first jet. It removes
the upper bound on T and the exact-unit requirement for the G cost. It does
not force that task from D0, choose Book03 Info, absorb extra moving sources,
prove a physical local minimum exists, or prove that `dJ2=0` is sufficient
for one. A minimization restricted to Sigma would only constrain its tangent
directions; all42 source recovery needs the stated full field variations.

`full_D0_price_selected=false`, `GR_closed=false`.

`SHA256SUMS.json` lists the final packet files other than itself.
