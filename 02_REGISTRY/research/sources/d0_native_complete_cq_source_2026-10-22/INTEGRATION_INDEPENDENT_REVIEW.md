# Independent review: final complete-source integration

22 October 2026. Reviewer: independent `native_definitions` subagent.
Existing scientific owner: Draft PR #334. This is a static integration
review of the final four files below, their declared source closure and
the relevant consumed source definitions. No numerical checker or old
suite was executed for this review. The reviewer changed only this record.

## Verdict

**PASS for the declared integration and read-only replay contract.**
The reviewed integration preserves the distinct information objectives,
instrument carriers, projector types and geometric source scopes. The
entrypoint checks the complete declared input closure before executing
its three bounded consumers, compares their frozen receipt interfaces,
and rejects changed frozen inputs. No blocking issue remains in the
reviewed bytes.

One notation issue was reported and corrected by the author before this
final review: in `CONCURRENT_INTAKE.md`, equation (8)'s identity and trace
are now explicitly restricted to `ran(Q_c)`, matching the consumed
stage-cut theorem. No scientific proof, child checker or expected
numerical receipt was changed to make the integration pass.

## Exact reviewed integration bytes

| File | SHA256 |
|---|---|
| `README.md` | `e10faa6baf360c91a1f03195a815ab3938df100523cc81c0b0a7af8b903b9a3b` |
| `CONCURRENT_INTAKE.md` | `ff614b5f0de556439632356c86da1360555cdf451a8e714bdbf0ad27aa5c8ecc` |
| `SOURCE_PINS.json` | `04e999ec84d444f23631c3c1ad709bd178d7195b8afe46982d0311cf648ab7ac` |
| `../../certificates/a4d_native_complete_source_reduction_check.py` | `22a7248ffb2483256de69a740c6edd722f62148132f682cce2b0649bfb7aefab` |

The parent synthesis consumed by the manifest retains SHA256
`5f4f889276f1516870a085d7109b0b3d72c6b0664b5628e8bdf36e78d2052c10`.
This review is an external record of those bytes. It is intentionally
neither its own input nor an input to the numerical replay it reviews.

## 1. Information source and preparation transport

The README and concurrent intake consistently distinguish the measured
CQ entropy from the maximum-entropy forgetting gain:

\[
I_{\rm gain}=S(\Gamma)-S(\rho),\qquad
\mathrm dI_{\rm gain}=\mathrm dS(\Gamma)-\mathrm dS(\rho).
\]

For the two declared prices, with `ell=log(phi)`, the intake correctly
derives

\[
\mathscr S_{\rm gain}=\mathscr S_{\rm CQ}+S(\rho)/\ell,
\qquad
M_{\rm gain}=M_{\rm CQ}-(\log\rho+I)/\ell.
\]

The sign agrees with differentiating entropy on the stated
smooth-support domain. Centering the input cotangent in the stationary
adjoint Poisson equation removes the identity term. Consequently the
intake's mean-zero Poisson correction in equation (6) also has the
correct sign and centering. This is a transport of an actual moving
preparation source, not a prescription that this source vanish.

The parent equations include the initial entropy derivative for the CQ
price and cancel it for the forgetting-gain price. The numerical table
keeps pointer, CQ and gain sources separate. The nonzero native initial
entropy derivative is not treated as a constant. A retained pure
purification is explicitly a different joint-state case: efficient
conditional branches are pure, so pointer entropy, joint CQ entropy and
the gain coincide there. An independent fixed oldRIGHT128 spectator
adds a constant to normalized entropy and does not multiply its source
by 128; its constant cancels from the gain.

The one-moment maximum-entropy marginal theorem remains separate from
this full-history information. Its generated dual multiplier is not
identified with the original fixed Golden heat calibration. Its zero
first gain on the native two-band point is not used to suppress the
conditional quantum-work or temporal-history terms.

## 2. Concurrent two-Kraus calculation and original full128 application

The intake accurately describes the consumed concurrent executable.
Its concrete channel has the displayed two Kraus matrices, a
two-dimensional stationary density and a declared binary length ledger.
Complete stopped words include matched and capped-abort leaves. The
initial density is diagonal and every word preserves diagonality, so
the executable's diagonal eigenmass calculation is valid for its
fixture despite the noncommuting Kraus operators.

The general stationary-Poisson formula is applicable under its stated
unique-stationary-state and mixing-inverse assumptions. The intake does
not claim that the concurrent numerical calculation evaluated all
original CAR16/full128 blocks. Conversely, the packet's one/two-round
full128 entropy diagnostics are not presented as the complete original
stopped Cost-plus-all-Info cotangent. Its actual finite preparation,
selected information algebra and physical price still require their
own application. The declared two-Kraus code lengths are not promoted
to a selected Golden physical price.

No concurrent executable is called by the new wrapper. Its source is
included as a frozen scientific input, with its publication and content
identity recorded.

## 3. Conditional expectation, active cut and geometric scope

The entropy pinching `E` is correctly typed as a conditional expectation
on an operator algebra. The Book active projector `P_N` is an operator
on the physical Hilbert space. Selecting all history-diagonal
quantum-work tests determines the former maximum-entropy representative;
it does not thereby select an internal stage projector `Q_c`.

The corrected principal-angle formula is evaluated on `ran(Q_c)`, so
inactive complement dimensions do not enter its logarithmic trace.
The clock-only theorem retains the original fixed stage advance and
its field-independent crossing count. The intake does not infer zero
history information from the zero clock-only feedback source. The Q8
consumer supplies a discrete contrast for a declared internal cut,
without proving either physical selection or a continuous all42 source.

The actual-cut multiplier result retains its rank-one apparatus,
independent spectator, dimension and fixed-calibration scope. Its
global source equivalence concerns the constructed cut heat plus its
own feedback. Geometric inheritance remains on the previously proved
common-null source family. It does not become an off-null equality
with the separately configured 42-field action.

The concurrent finite off-null full42 continuation is consumed as a
separate conditional theorem. Its `3e-22` whole-covector bound applies
in its own normalized finite chart and is sufficient, not necessary.
The README explicitly supplies no transport of the Fourier-fixture
numbers to that chart and makes no claim that the bound is satisfied
or violated. No mesh-uniform refinement, physical source selection or
GR closure is inferred.

## 4. Input closure and content provenance

A read-only static audit found:

- 19 owned input rows, each matching both its declared SHA256 and its
  reconstructed Git blob identity;
- 15 frozen artifact rows, each matching its declared SHA256;
- exactly 35 distinct `INPUTS` entries, equal to the union of those 34
  rows and `SOURCE_PINS.json`, with no omission or extra entry;
- all repository files read by the three numerical consumers inside
  that closure, including the original constructor and the cut
  consumer's three pinned sources and expected receipt.

The three concurrent `e02855` inputs now reside byte-for-byte in
`published_inputs/`. Each row preserves its original `source_path`,
publication commit, SHA256 and Git blob. Their snapshots match the
previously inspected scientific bytes exactly. This stabilizes the
consumed historical intake while those original source paths continue
to evolve; it does not substitute an alternate runtime constructor.
The native constructor and actual-cut runtime dependencies remain at
their original live paths with their original content pins. The final
snapshot change preserves the 35-input closure and changes no receipt,
comparison rule or numerical consumer.

Sixteen publication-commit/path mappings were also verified against
the locally available Git objects. The three rows published at
`e02855b68a1de758436b0e80c1ee98171bc5c4f4` were not present in that local
Git history. Their local content hashes and blob identities were
verified; their remote commit/path attribution is the separately
reported GitHub API intake by the parent and concurrent source reviewer.
This review does not claim an offline verification of those three
publication mappings.

The wrapper validates content against the committed manifest; it does
not fetch or independently authenticate remote publication history at
runtime. The manifest and entrypoint are anchored by their reviewed
Git bytes and the hashes above. There is no circular claim that a
manifest authenticates its own provenance by hashing itself.

## 5. Fail-closed replay and absence of writes

Static inspection confirms that missing files, mismatched SHA256 or
declared Git blobs, duplicate paths, and a difference between manifest
closure and `INPUTS` cause failure before a child calculation runs.
The wrapper records the manifest's bytes as part of the before/after
input snapshot and separately records its own bytes.

Only the three explicitly named new checkers are invoked, using the
current Python interpreter, `-B`, and `-O` when the caller is optimized.
The environment also disables bytecode writing. No authoring flag is
passed. The cut and history consumers' receipt-writing branches require
explicit flags and are unreachable in this invocation; the marginal
checker has no evidence-writing operation. The native source is loaded
through the already reviewed six-definition pinned AST slice, not by
executing its old test suite.

Nonzero child exits, stderr, malformed output, changed receipt keys or
list lengths, altered strings/flags/counts, and nonfinite diagnostics
are rejected. Boolean and integer interfaces are type-checked. The
regularization parameters and independent-value control tolerance are
exact. Other diagnostics use the documented `2e-9` absolute and `2e-8`
relative comparison; fields ending in `error_bound` use `1e-18` absolute
and `2e-8` relative. These are replay tolerances, not replacement
mathematical error bounds. The cut consumer also compares its own
rounded receipt exactly.

The wrapper enforces the inventories 100, 23 and 50 and false
`GR_closed` flags. It revalidates every frozen file and the manifest
after the children, compares the full input snapshot and checks that
its own bytes are unchanged. Its gates use explicit exceptions and do
not disappear under optimized Python. The wrapper itself contains no
file-writing operation.

## Review boundary

This final integration review used file reads, static source inspection,
hash/blob reconstruction and available Git-object queries only. It
did not import or execute the registered entrypoint or a numerical
consumer. The parent's separately planned isolated committed replay
and structural guards are not claimed as results of this review.

The accepted outcome is a reproducible bounded source packet with its
distinct interfaces preserved. Selection of the actual Book03
heat/cut/retained algebra, complete paid preparation/controller and
source transport to the geometric carrier remain open. `GR_closed=false`
is the correct integrated status.
