# One-row numerical-matrix Lean pilot

These are two bounded attempts on the same 128×128 numerical A and computed
right inverse B over ZMod 1009. Both use existing cached dependencies; neither
is a final provenance-guarded build. No source-to-Lean matrix equality, full
128-row inverse, nonzero determinant or complex source conclusion is claimed.

`SavedFutureMatrixPilot.lean` is the first candidate. It failed (exit 1):
long array literals exceeded elaborator recursion depth, nested get! syntax
failed, and the axiom diagnostic was invalid, containing `sorryAx` because
of those errors. The corresponding path-free receipt records this failure.

`SavedFutureMatrixPackedPilot.lean` uses a different representation: two
strings of exactly 65536 ASCII digits, four decimal digits per matrix entry.
Independent byte-level review compared all 32768 values against saved A and B.
Its *first row only* passed (exit 0, 30.0 s). Its explicit trust footprint is
`propext`, `Classical.choice`, `Quot.sound`, and
`D0.Algebra.SavedFutureMatrixPacked.first_row_right_inverse._native.native_decide.ax_1_1`.
This is native computation, not a kernel-only decision proof.

The supervisors held the selected cooperative lock, checked for active Lean
processes, used a 3 GiB Windows job, stopped on low available RAM or timeout,
and set below-normal priority. They did not limit CPU affinity. Other checkouts
and direct invocations still require external coordination. Raw logs may contain
local paths and are not included; their digests appear in the receipts.

Generator sources consume pinned numerical JSON and generate candidates only.
The numerical A source SHA-256 is
`e63c1c1834b8db79d631fec2b375373a5948bcd4f1a57690f0cd3fed34981f46`;
B SHA-256 is `ccb3155efc38c91eb206b75e07699628414cac0e97e41f4865a6a95c1d6c2588`.
Proving the full A*B=I and connecting A with the original source effects
remain separate work; native_decide trust must remain visible. `files.json`
pins exact packet input bytes, not the build dependencies.

The Git copies normalize CRLF to LF where applicable; `files.json` preserves
the SHA-256 of the executed bytes alongside the Git-file hashes. Pilot Lean
inputs themselves were already LF and are stored byte-for-byte.
