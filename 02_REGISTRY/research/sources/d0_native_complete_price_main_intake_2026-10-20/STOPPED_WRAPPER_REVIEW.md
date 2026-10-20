# Read-only structural acceptance of the published stopped-source packet

Reviewer: `native_task_selector`, bounded integration audit within existing
PR #334. Source commit: `45372df30740f4e75c8b58013652a7665bf833cd`.

**Decision: accepted without required integration changes.** This audit read
source and JSON, parsed Python AST literals, compared bytes/hashes and read
Git blobs. No scientific checker, wrapper, mathematical replay or geometry
check was executed. No repository or frozen producer file was modified.

## Verified bindings

- The wrapper declares exactly **28 unique input paths and 28 literal
  SHA256 pins**; the sets agree and all current bytes match. They include the
  primary overview, proof, immutable scientific receipt, all five independent
  review/acceptance files and all four original upstream dependencies.
- All **27 newly added scientific paths** match their blobs in source
  `45372df3`. The **14 producer files** are byte-identical to the frozen
  `/tmp/d0_stopped_extension` originals and their unchanged manifest. All
  **five review files** are byte-identical to `/tmp/d0_cost_variation` originals
  and match the declared review hashes.
- The primary overview has SHA256
  `6e73ece4f1d4312e241e91860871019689bf28017088ef6431893a3286978b0b`,
  matching its literal pin, `SOURCE_INPUTS.json`, and the final independent
  acceptance's explicit reviewed hash.
- The four upstream dependencies match their declared commit, Git blob,
  byte count and SHA256. The current original checker is exactly the reviewed
  1cb version, with SHA256
  `a8997f58d3af738a2cf70f4a1d20dd6c9c509274c8e9b2393157a50038e2729d`.
  It differs from the historical failed snapshot, contains the corrected
  target, and uses active checks. The wrapper and both executed checkers have
  no `ast.Assert` nodes. The historical assertion-based failure is preserved
  separately and is never selected by the wrapper's run calls.

## Receipt immutability and non-circular boundary

The wrapper launches only the new all-cost checker and the current 1cb
checker, with `-O -B -W error`. It does not pass `--output`, and it contains
no filesystem mutation calls. The new checker's optional output-writing
branch is therefore inactive. The two expected output files are read and
literal-pinned; input hashes are checked before and after the child runs.
The new expected receipt records **275** active controls and retains SHA256
`b972503e95f0329700e3cc3544e6246cc8c896c5a9ebc3aef41c02ff06b71c6d`.

Of the 27 new scientific paths, the intentional exceptions to the wrapper's
own input pins are the wrapper itself and `FROZEN_REPLAY.json`/`.log`. This
avoids self-referential hashes. Their committed bytes were checked here;
the replay JSON correctly binds the wrapper SHA256
`5a5baccd4c59d0fe9f7e10a5b7e6407db1cd688707fb341a9b139b2049222bb1`
and the frozen replay-log hash. No proof, review or expected child receipt is
missing from the 28 input pins.

## Portability and runtime conditions

No blocking path/runtime risk was found by inspection. `ROOT` is derived
correctly from the wrapper location, child paths are absolute, and the child
working directory is the repository root. Launching from another current
directory does not create an implicit dependency. The original `/tmp` path
in the archived failed traceback is inert historical text; it is not used
by a portable replay. The active scripts use only the Python standard library.

The declared replay requires the complete repository checkout, including the
four original sibling dependencies; the packet directory alone is not a
standalone distribution. Frozen file bytes must be preserved: line-ending
conversion would correctly fail the SHA256 checks. Each child has a 45-second
timeout, requires empty stderr, and must reproduce the frozen textual output
exactly. These are explicit execution conditions, not problems observed in
this read-only audit. The already-recorded replay and required CI are not
re-certified by this structural review.
