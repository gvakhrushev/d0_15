# Variational selection and native-clock synthesis: proof packet

21 October 2026. Existing Draft PR #334; scientific calculation inputs frozen
at `441bdef5a02bef09a74ebe48dcf4d5527ba18988` of `gvakhrushev/d0_15`.

Main synthesis:
[A4D_VARIATIONAL_SELECTION_AND_NATIVE_CLOCK_SYNTHESIS_2026_10_21.md](../../A4D_VARIATIONAL_SELECTION_AND_NATIVE_CLOCK_SYNTHESIS_2026_10_21.md).

This packet composes exact native-price boundaries, a weak material estimate,
a CAR clock/coframe identity, and the later exact double-zero/native-PF
constructions. It derives a concrete nonzero remaining coframe row and
transfers the actual Golden regularity bounds to material and clock estimates.
**It does not select the physical Book price, admit a native normal clock,
prove a full canonical constraint algebra, or close GR.**

## Results and their consumers

| Lane | Proven result | Exact scope and intended use |
|---|---|---|
| [book_binding](book_binding/PROOF.md) | READY scalar weights square to a different coherent law; initialized-cut trace-log is invariant under invertible right maps of the same full range | Reject scalar-amplitude and same-range cut refits as the missing source construction; other physical Book terms remain open |
| [input_price](input_price/PROOF.md) | Original Fourier block gives `F_4096(3/5,C2)-F_4096(1/2,C1)>52/25` for every normalized purified input | Native port price minus complete coherent-archive entropy; a specific finite input-independent comparison, not an all42 or full-price no-go |
| [paid_source, section 1](paid_source/PROOF.md) | Exact paid three-node descent in one common moment catalogue | General local corollary of the old complete-CQ saddle; the concurrent explicit finite witness is consumed as the stronger concrete result |
| [paid_source, section 2](paid_source/PROOF.md) | `||R_A,h||_-1,h <= 2 L tau ||(f_h/rho_h)V_A||_2,h` | Nonlinear-minus-affine material remainder, original sigma-minus source; an input for an eventual coupled whole-slab correction theorem |
| [clock_bracket](clock_bracket/PROOF.md) | Exact constant-frame normal-profile commutator with metric and spin terms; smooth original-stencil error O(h); heat and frozen-frame hostile controls | External CAR16 operator calculation; physical normal-clock admission and dynamical constraints remain unproved |
| [moving-frame addendum](clock_bracket/MOVING_FRAME_IDENTITY.md) | Full shift/profile defect equals the actual coframe derivative at a flat frame | Formal compensation is exact, including order-zero terms; moment-node writing, Clifford spin transport and the existing exterior link action are not identified |
| [late coframe application](late_application/COFRAME_RESIDUAL.md) | The exact double-zero representative has a remaining ambient source E_v=-2h/e+O(h²) at r=1 | Preserves the existing three-row theorem; rejects stationary claims based on the constant restricted action and gives the actual coupled correction target |
| [late PF/clock application](late_application/NATIVE_PF_AND_CLOCK_APPLICATION.md) | Actual Golden weights give O(h) material dual error, O(h⁴) PF-only dual correction and O(h) finite clock-commutator transfer | Consumes the original exact-cell theorem and explicit paid-depth schedule; complete adjoint, frame, clock-admission and all-row boundaries remain |


The actual compensated comparison subtracts the coframe derivative. A
Clifford spin rotation and an exterior Lorentz-link rotation can induce the
same vector rotation while differing on full CAR16. The required physical
transport cannot be inferred from that common vector action.

## Provenance and independent reviews

`SOURCE_PINS.json` lists twenty exact input files, their original repository
paths, byte sizes, SHA256 hashes and Git blob hashes. `inputs/` preserves those
bytes under the original path hierarchy. The copies are immutable scientific
inputs, not replacements for the live source owners.

LATE_SOURCE_PINS.json separately lists four consumed source files frozen at
c7e0c3d2f6bcfbcc8bd43034ff72da85b8cdd18a. They include the old original
exact-cell theorem, the new quantitative PF consumer, the exact double-zero
memo and its finite geometry checker. Their bytes are in late_inputs/.
The original twenty-file boundary and original scientific receipts are unchanged.

The four original checkers remain byte-identical to their reviewed versions;
the moving-frame checker and the late coframe-residual checker are separate
bounded calculations.
`CHECKER_PINS.json` pins the final proofs, checker code, expected receipts and
source manifests. `check_synthesis.py` checks those pins, replays all six
entrypoints against the two frozen input roots, compares the receipts and rechecks
the input bytes. It never rewrites expected results.

Historical reviews retain the hashes they actually examined. The paid-source
earlier final proof added the reviewer's unit-periodic-interval and mean-zero-test
clarifications; `paid_source/FINAL_REVIEW.md` accepts that exact delta. The
earlier clock review covered 55 controls; the final clock review covers the
later 66-control checker and identifies its exact final proof. The moving-frame
addendum has its own authored result, separately examined during integration.
The later paid-source prose also corrects a scope statement: the old
exact-cell theorem already supplied eventual positive native density at a
chosen adequate depth, although the original checker did not consume it.
The new late application uses it explicitly; its independent review covers
this correction without rewriting any original expected scientific receipt.
REVIEW_INTEGRATION.md records the final independent composition review.

Before publication the branch also incorporated:

* `c2818755`: the [explicit moment-writer native-selection test](../../A4D_MOMENT_WRITER_NATIVE_SELECTION_TEST_2026_10_21.md), including the stronger literal paid witness, the unconditional fair-code steering comparison, retained-code distance gap and full-column Book countercheck;
* `2961dc6e`: the Brinkmann EPS_PLUS/canonical-curvature sign and source typing correction.

These concurrent results are consumed analytically and preserved. They are
not relabelled as new calculations by this packet, and their old suites were
not rerun. The input snapshot of the four original receipts stays `441bdef5`.

Later integration also preserves the exact double-zero/PF constructions,
their six Lorentz Noether relations and nonflat two-stream controls, and
the signed vacuum-reference Julia cost-source candidate through fb0f45b7.
The latter has a different fixed input and a declared fine-CQ ledger;
its observable reconstruction is not compulsory Book03 price equality.
CONCURRENT_INTEGRATION.json fixes these analytically consumed source versions.


## Portable replay

Requirements: **Python 3.10 or later**, NumPy, SciPy and SymPy. The exact
book-binding and paid-source checkers use only the standard library. The
original native128 implementation also imports SciPy. The final replay used
Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0 and SymPy 1.14.0.

From any working directory:

```bash
python3 /absolute/path/to/d0_variational_selection_synthesis_2026-10-21/check_synthesis.py
```

The packet is standalone; Git and network access are not required. The
wrapper passes the frozen input directory explicitly, so historical defaults
inside two unchanged author checkers are never used. It disables bytecode
writes and sets one BLAS thread. It writes only JSON to stdout.

Receipt comparison keeps types, keys, Boolean flags, integers, rational
strings and high-precision Decimal strings exact. Only JSON binary-floating
diagnostics have a declared tolerance: relative `5e-12`, absolute `5e-13`.
Their scientific algebraic identities remain separately exact in the proofs
and symbolic checks. A finite fixture is not the general analytical theorem.

`VALIDATION.json` is the saved final wrapper output. Existing independent
replays and historical receipts remain unchanged. No full geometry factory,
raw216, original large full-history suite or Lean build is invoked by this
packet. Those mathematical claims are neither reaccepted nor upgraded here.

## Remaining application

The native PF density premise is now discharged on the explicit selected
sequence, together with the declared smooth-current bounds. The approximate
route still needs the other field rows and a stable coupled gauge/boundary
inverse. The exact double-zero route instead solves the remaining 15+24
ambient rows while preserving its actual currents and fixed endpoints;
the restricted sheet action supplies no additional equation. The clock
identity still needs a paid physical clock/coframe action on the same complete
execution and price, followed by a phase space, constraints and all required
reconstruction hypotheses. Exact field nodes and scalar readouts do not
supply either theorem. `GR_closed=false`.
