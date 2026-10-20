# Review: exact Golden detector and full capped source

20 October 2026. Existing Draft PR #334 and
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`.
Bounded research acceptance; no assembly/CORE/physical-GR promotion
or parent retirement.

## Reviewed immutable content

| Artifact | Raw-byte SHA256 |
| --- | --- |
| `GOLDEN_EXACT_DETECTOR.md` | `d33c9c2cb2322e381723f481eb1fcf58058fd05ad88eda92c5597c026d02eb77` |
| `check_golden_exact_detector.py` | `5e1ad8cbd442cc90eef17ab61a3b97189876c4388d54f3761f6408832cafb2cd` |

The proof/checker pair is frozen in local verification snapshot
`89a63199db8547ee450ace02ab65cd129f2c3e7b`.
Its base is published input
`5966f9cedb3ed80a8e7d563ee9731d133cb6b2f6`.
The following input blobs were consumed unchanged:

| Input at that base | Git blob |
| --- | --- |
| `TWO_NATIVE_8D_DETERMINANT_SOURCE.md` | `30c5fbb0eb840e341b33aa66f336eb58b6ac3378` |
| `DETERMINANT_PREPARATION_BANK.md` | `e7b92fae0d6f3dc3e60499f0dd041c18003da872` |
| `FINITE_FUTURE_DETERMINANT_MINIMUM.md` | `2881788b0c48d7e6f193ed08316aa5706356db52` |

The checker imports the reviewed preparation-bank ring arithmetic;
it does not run that old checker, geometry replay or Lean build.

## Analytical decision and exact application

The primary-source reviewer accepted the proof at the hash above.
The review checked chronological controlled-G recursion and Kraus signs,
all four complete X-cycle outcomes, exact H/Toffoli action on entangled
inputs, and the literal expanded 20/42/8 gate-tick lower bounds.
It confirmed the original retained basis `{0,2}`, 43-Toffoli detector,
128N resource count, L=20 readiness inequality and the complete
stage-abort stopping law.

A second independent same-programme reviewer accepted both pinned files
after checking the complete record/source composition, the Boolean
polynomial checker, the new threshold comparison and all retained
physical assumptions. Neither review changes the original task's
acceptance or lifecycle state.

The exact consuming substitution is in
`TWO_NATIVE_8D_DETERMINANT_SOURCE.md`, section 7:

```text
S_total = S_pre + alpha [kappa-beta h_phi(q)] E_N(beta q),
kappa > 266/5 > 53,   alpha>=1/2, beta>1/2,
D S_full|Sigma = alpha c_N DJ2,   alpha c_N>6.
```

It supplies coherent Boolean detection through one explicit finite
programme on the addressed Golden/CNOT/parity-reading interface,
with all gate-abort outputs and actual expanded word costs retained.
The original all16+24+2 Euler family and each local multiplicity are
consumed unchanged. The coefficient comparison
`E_N/E'_N<=1+x` transports the owned N=2 threshold to this new renewal
law; the old integer-stage minimum is not silently reused.

The data-independent record assertion was checked at the full instrument
level: a standalone X outcome can depend on data, but after CZ with a
fresh plus resource the H transfer branches are scalar H and XH.
Their labels are uniform for arbitrary external entanglement. Abort
branches retain pure work and no efficiency bit is prematurely measured.

The accepted scope retains the parent pure-input/purifying-reference
convention; a separately moving initial mixed entropy adds its own
source. A fresh parity flag can implement each ancilla reading with
an additional paid CNOT and retained original ancilla. Addresses,
corrections and clock records in this specified controller are functions
of the measured records. Extra independently random physical records
would require adding their cost and entropy.

The numerical price bound assumes the actual literal G/CNOT letters cost
at least one unit each in the stated Cost-minus-base-phi-entropy ledger.
Different physical valuations cannot inherit the bound without their
own calculation. Moving original 8D query/matter-code access, interface
admission, compulsory task, physical Book03 Info, upstream H/R and
preparation sources, refinement of the full price and selection among
different programmes remain open.

## Checker scope

The exact rational ring checker verifies all basis columns of the
controlled rotations, the complete X-cycle matrices, H factorization,
an entangled input and Toffoli. A Boolean polynomial computation checks
the detector on its entire 46-input-bit domain, without sampling a
truth table. It verifies the finite readiness inequalities and source
gap arithmetic while retaining the owned determinant threshold as an
explicit input.

Two independent rational ledger fixtures contain 190 and 163 complete
leaves. They include gate abort, query success, horizon exhaustion,
teleport labels, variable correction/routing cost, entropy coefficients
and their first derivatives. Their assigned rational probabilities
are test fixtures, not purported native Golden probabilities.
Controls reject erasing aborts, substituting a forward gate for the
required inverse, and replacing coherent efficiency by an observed coin.

The checker author ran normal and optimized Python 3.11.9 invocations
with `-B -W error`; both exited 0 with empty stderr and byte-identical
JSON. This is author validation, separate from the isolated independent
replay recorded below.

The affected structural checks passed: `tools/validate_repo.py`
(zero warnings), `tools/validate_agent_protocol.py`,
`tools/validate_work.py`, and `git diff --check`.
The assembly template was inspected and the precise parent substitution
is recorded above; no new assembly acceptance was asserted.

## Independent isolated replay receipt

The same-programme reviewer executed the pinned pair in a clean managed
worktree at `89a63199db8547ee450ace02ab65cd129f2c3e7b`, using
Python 3.11.9 on 64-bit Windows:

```text
python -B -W error 02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/check_golden_exact_detector.py
python -O -B -W error 02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/check_golden_exact_detector.py
```

Both exited 0 with empty stderr. Their 4,878-byte stdout was identical,
SHA256 `a8ed476bd955457efb38469fbd2f9df8dca804af6726d54e36f0adc4a859f758`.
The reviewer independently checked both artifact hashes above.

An in-memory mutation replaced the second X-probe inverse G by forward
G. The core assertion rejected it with
`RuntimeError: all four exact X-cycle Kraus matrices and signs`.
The worktree was clean before and after; no files were changed.
