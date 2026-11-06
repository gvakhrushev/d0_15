# Full numerical matrix inverse over GF(1009)

`SavedFutureMatrixAllRows.lean` uses packed decimal representations of the
saved numerical 128×128 matrix A and its inverse B. The source has two
claims: all coordinates of A*B equal the identity, then the corresponding
matrix equality. This finite, concrete, numerical verification uses no
assumed determinant conclusion.

On the exact input recorded below, one direct Lean run exited 0 in 62.015 s
with a 3 GiB job memory limit, lower-priority scheduling and an existing cached
dependency environment. The original preflight had refused to start because
available memory was below 4 GiB; the successful run occurred after memory
recovered. CPU affinity was not limited. Other checkouts and direct invocations
require external coordination. Raw logs may contain local paths and are not
included; the receipt retains their digest.

`#print axioms` reports `propext`, `Classical.choice`, `Quot.sound`, and
`D0.Algebra.SavedFutureMatrixPacked.all_rows_right_inverse._native.native_decide.ax_1_1`.
The last is a native-computation axiom. This is not a kernel-only reduction
certificate. No connection of A to the original source effects is claimed, and
no complex independence, physical admission or GR closure follows here.

Source matrix SHA-256
`e63c1c1834b8db79d631fec2b375373a5948bcd4f1a57690f0cd3fed34981f46`;
its separately computed inverse SHA-256
`ccb3155efc38c91eb206b75e07699628414cac0e97e41f4865a6a95c1d6c2588`.
Exact input and script bytes are listed in files.json; dependency cache
provenance is not established by this narrow run.

The Git copies normalize CRLF to LF where applicable; `files.json` preserves
the executed-byte SHA-256 alongside each stored-file hash. The Lean input
is LF already and is stored byte-for-byte.
