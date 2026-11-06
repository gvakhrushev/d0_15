# Four-commit #334 source intake: original comparison and prepared-price defect

This is a pinned research intake for the existing #402 formalization owner.
The upstream research owner is Draft PR #334. The verified range is
`05cc38dc6283f45995a4c86fb69067c87734bb4c..2900145fe674629b61949587917a3a2ea5188797`.
The four commits are, in order:

1. `e6e46c805f8a51c6965aa6abbd8fc3e4b71a7d74` — original reader and fixed input comparison, full-clock heat source.
2. `66edbcfd458daecd133baca3b44528931e2ebfc5` — full reversible comparison, both flag sectors and the complete READY factor.
3. `cfe6755a0ddf5174698f003db59531a1ebd93fa1` — same-family clock/source composition and bounded off-shell witness.
4. `2900145fe674629b61949587917a3a2ea5188797` — exact prepared-price defect and surviving heat source.

[MANIFEST.json](MANIFEST.json) pins each commit, both changed path/blob pairs,
the two original files at the base and at all four commits (ten exact XZ
snapshots), the complete unmodified four-commit Git patch, and the four
section byte intervals in the final memo. Git objects, lengths and SHA-256
are separately verifiable. The full memo and task brief are retained inside
the snapshots; they have **not** replaced the #402-owned files. To inspect a
snapshot in a separate temporary location, decompress the chosen `.xz` file;
do not overwrite the active task brief or source memo.

## Source slices and retained boundaries

- **Original reader (SR):** the stated full growing-clock calculation
  uses the original report together with a fixed comparison to the canonical
  born input. The memo's negative control shows that omitting the input
  reflection leaves the full reflection trace constant despite a changing
  measured probability. Its target identity and actual compiled history,
  READY/gain, all old rows and compiler errors retain their own hypotheses;
  the bounded check does not emit an exact native reflection or replay full
  heat or geometry.
- **Full reversible comparison (XF):** the specified construction retains
  both flag sectors, the paid last spectator and the original complete
  READY factor. Its kappa/source-class application is conditional on the
  declared carrier, task, comparison maps and full error/normalization
  budget. A few finite word checks do not establish the all-round-trip
  result or select a universal task.
- **Same-family clock/source (SC, §7fd):** the owner states a conditional
  master-law soundness and recovery composition on its declared Cauchy and
  clock family, with a same-family nonzero off-shell source witness. That is
  a scoped research argument, not an independent acceptance or a proof of
  the unchanged A–D terminal. In particular the actual complete Cost−Info
  binding and exact finite joint-root obligation remain open; no equality
  of finite zero sets follows from a kappa limit.
- **Prepared-price defect (PB, §7fe):** on the stated original
  initial/generated-prefix lifts, the owner retains the complete quantum
  continuation and calculates a nonzero relative-entropy first-source
  defect. The exact support control is separate from that source statement.
  Replacing the actual preparation by a freely optimized Gibbs state is not
  an established native operation. The neutral full quantum continuation
  and the different flag, full-output and report entropies remain distinct;
  no particular Info law, sampler, marginal or new physical price is selected.
  The owner also retains the conditional PB6 comparison: if the same admitted
  execution actually selects and pays for the Gibbs variational state and the
  normalized feedback source vanishes, its source can match the original B
  after the declared sign conversion. The variational minimum alone does not
  prove that preparation or equality of absolute prices.
  The proposed next consumer is the existing full price effect with its
  preparation, effect, residual and work variations intact.

These are source-intake descriptions, not independent mathematical or physical
acceptance. The exact scientific parent, carrier, input preparation, source
norm and limitations remain as in #334. No claim or assembly status is
changed, and `GR_closed=false`.

## Bounded reproductions

The four exact Python blocks were extracted byte-for-byte from the pinned
final memo, and their SHA-256 values were checked against the owner entries.
They were run in ordinary and `-O` modes with `-Werror`; each pair produced
identical JSON, exactly matching the owner's published receipt hash, with
empty stderr:

| Check | Bounded scope | Count | Local runtime |
|---|---|---:|---|
| `sr` | original reader, input reflection, two-bit fixture and true growing clock | 59 | Python 3.12.13, SymPy 1.14.0 |
| `xf` | full flag, native reader fixtures and small growing clock | 61 | Python 3.12.13, SymPy 1.14.0 |
| `clock` | exact timelike-clock source witness | 8 | Python 3.9.6, SymPy 1.14.0 |
| `price` | prepared-state/entropy and small Golden clock controls | 24 | Python 3.9.6, SymPy 1.14.0 |

The first SR/XF attempts on Python 3.9.6 reached receipt writing and failed:
that interpreter lacks `Path.write_text(..., newline=...)`. A subsequent bare
Python 3.12.13 environment lacked SymPy. Both diagnostics are retained under
[`diagnostics/`](diagnostics/); neither is a passing run. The successful
Python 3.12 run used the already cached SymPy 1.14.0, offline. The owner's
recorded environment for its final bounded runs was Python 3.12.14 and SymPy
1.14.0. Exact arithmetic and matching output do not turn a finite test into
a replay of the general proof, a native compiler run, a PDE solver, Lean,
CI, or a physical GR acceptance.

Verify source snapshots, embedded checker identity, patch and stored receipts
without executing archived code:

```sh
python3 02_REGISTRY/research/sources/d0_334_post_05cc_290_intake_2026-11-05/verify_intake.py --verify-source-objects
```

The `--verify-source-objects` option also compares each snapshot and the full
patch against locally available Git objects; without it the check only
verifies the self-contained pinned metadata and stored bytes.

For a fresh bounded replay using an already cached Python 3.12 and SymPy:

```sh
uv run --offline --python 3.12 --with sympy==1.14.0 python 02_REGISTRY/research/sources/d0_334_post_05cc_290_intake_2026-11-05/replay_bounded.py
```

This intentionally executes trusted upstream Python (including its pinned
RO/SR helper blocks) in a disposable directory; it is **not a sandbox**. It
requires Python 3.10 or later and SymPy 1.14.0. It does not overwrite source
or expected evidence. The exact local outputs, stderr and the failed runtime
diagnostics are retained here for review.
