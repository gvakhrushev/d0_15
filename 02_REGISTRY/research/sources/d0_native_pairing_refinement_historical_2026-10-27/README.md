# Historical pairing-refinement source inputs

These eleven Lean files are byte-preserved Git blobs from commit
`2f3360c5d3bfcb40d4791b23ade8e82e03f887c8`. Each source path, Git blob ID and
SHA-256 is recorded in [MANIFEST.json](MANIFEST.json). The bytes were obtained
with `git show <commit>:<path>` and match the existing immutable pairing
certificate ledger. They are stored here so replay does not depend on that
commit remaining reachable from a remote branch.

`tools/native_pairing_refinement_inputs.py` admits this set only for
`a4d_native_pairing_refinement_source_check.py` in a fresh detached research
runner worktree. It verifies the manifest, original checker and receipt, all
66 ledger inputs and the 12 Lean-receipt inputs before applying the eleven
possible overlays. It records which files were replaced and restores them
after the checker finishes. An unlisted mismatch or a changed pinned artifact
fails the replay.

This is a replay of historical inputs and a historical Lean receipt. It does
not establish compatibility of the maintained Lean sources, a new compilation,
native admission or physical GR. Current-source compatibility is a separate
Lean check.
