# Independent read-only review of the joint-minimum replay and wrapper

20 October 2026. Reviewer: checkpoint_integration. Final publication source:
`83a4740021fbc552c75ecbd3cd888c408e5b4757`. No scientific checker was
executed in this review and no repository file was modified.

## Frozen artifacts reviewed

- `replay_packet.py`: SHA-256
  `2ad14e69cdd16d26fb38a588af2d059ac6f697cdde478bbd55c65074230ad751`.
- `a4d_native_joint_field_minimum_check.py`: SHA-256
  `f6a30356aa362d59034ef203f01799e43c962c7aaccf4a901145c429eeb07be8`.
- `SHA256SUMS.json`: SHA-256
  `ea02c359cd851512be63fb394c87c4052ff118dbaa1875b5b91c251150560b40`.
- `FROZEN_REPLAY.json`: SHA-256
  `adb10251dfebd439c4b50921d65b15b209aac1c375cc182ab41f9bd6e2d73c3b`.
- `VALIDATION.json`: SHA-256
  `f7d6818f4047024cf7683c8230a7fda7b853020799e0806ba96eaeb796567749`.

The companion `REPLAY_WRAPPER_STATIC_AUDIT.json` records the independently
recomputed hashes and exact dependency-set comparison.

## Acceptance

No correctness or publication blocker was found in this replay path.

All 41 packet pins match current bytes. All 22 historical snapshots match
their SOURCE_INPUTS hashes and packet pins. The wrapper's 42 literal INPUTS
are exactly the pinned files plus SHA256SUMS.json, with no missing or extra
path. Its repository root calculation and the replay's fixed script paths
resolve correctly.

Removing only FROZEN_REPLAY.json and VALIDATION.json from the final manifest
reconstructs the previous 39-file manifest byte for byte, with SHA-256
`4a49b6812cc961385603e4b1d4c6578627fead6346a99115a638b16afa65eaf8`.
Removing only those two literal INPUTS lines reconstructs the previous
wrapper byte for byte, with SHA-256
`529f3bd28803512f459cf57a8dee9c70d8aeb5b79b77f00da1ada38b4441670b`.
Thus the previously reviewed proof, replay logic and mathematical inputs
are unchanged. The frozen scientific replay truthfully reports the 39
pins present when it ran; the two added files are its later frozen receipt
and validation record. That historical count is not rewritten to 41.

The worktree advanced to concurrent merge HEAD
`a656d5992f7f8230b25dafd81a6d7521762c442d` during this read-only review.
All 43 scientific files were therefore also checked by Git blob identity
against the specifically requested source commit 83a47400; every identity
matches. This review does not widen the intake to other concurrent files.
The source commit's six routing changes comprise exactly 148 inserted
lines and zero deleted lines. Their patch and the 43-file copy identities
are saved separately for the forthcoming main-intake preservation check.

The direct original witness reads its immutable adjacent checker snapshot;
it does not invoke the original all40 theorem. The prospective checker is
called with an isolated TemporaryDirectory root populated by copyfile from
the frozen snapshots. All source paths are relative and contain no parent
traversal. All nine runtime prospective PINS and all seven INFO_INPUTS map
to the same verified snapshot bytes. No historical live repository file,
remote object or persistent /tmp artifact is needed by the committed replay.

Every replay condition uses an explicit failure path, not Python assert.
Subprocesses inherit the selected interpreter and environment, disable
bytecode output with -B, reject a nonzero return status, and parse stdout as
JSON. Unexpected stderr is rejected. The wrapper propagates replay failure.

The witness and prospective bridge are compared against their entire frozen
JSON receipts by exact semantic object equality. The floating Info component
uses its explicit semantic acceptance policy: PASS, 36 examples, error
thresholds 2e-12 / 2e-7 / 2e-12, negative paid pointer source, and exact
checker/note identity. The pinned Info producer itself actively verifies
each required identity and sign. This is a tolerance-based replay, not an
assertion of byte equality or equality of every diagnostic field with
INFO_CURRENT_RESULT.json; publication wording should retain that distinction.

All expected receipts are read, never rewritten. The prospective checker's
optional --output mode is not requested. The actual replay's only writes
are snapshot copies in its temporary tree; subprocess output is returned
through stdout. Packet hashes are rechecked after successful execution.
The outer repository runner additionally provides its existing tracked-file
mutation gate.

## Interpreter and dependency diagnosis

The successful original witness command was:

```sh
PYTHONPATH=/tmp/d0_native_validation_deps python3 -B /tmp/d0_joint_minimum_closure/check_joint_minimum_witness.py --root /workspace/scratch/98370b00de99/d0_physical_selection
```

At the time of this review, python3 resolves to
`/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3`,
version 3.12.14. The above PYTHONPATH supplies SymPy 1.14.0. The default
interpreter without that dependency path lacks SymPy; its import failure
occurs before the witness mathematics and does not contradict the earlier
PASS. The replay preserves PYTHONPATH in all subprocesses. Committed CI
already installs requirements.txt, which declares sympy>=1.12, before
research replay; no workflow change is required for this dependency.

This acceptance is a read-only code/provenance review. It does not substitute
for the root's actual common replay receipt, nor establish physical field
admission, compulsory Book information, or GR closure.
