# Review: the complete Golden detector under an absolute Book mean binding

20 October 2026. Existing Draft PR #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`,
`native-programme-v1`. Conditional source application, no physical
Book binding or mean aggregation selected, and no task retirement,
assembly acceptance, CORE or physical-GR promotion.

## Pinned artifacts and inputs

| Artifact | Raw-byte SHA256 |
| --- | --- |
| `GOLDEN_DETECTOR_BOOK_MEAN_SOURCE.md` | `4f7d5376318793beca791bc013622f0d5d3571b09728cab950dcfef6cfeb7191` |
| `check_golden_detector_book_mean_source.py` | `b0e99a92205731f9c35d8e166e1902ba5610d4d898f0df9327f0b8c9cbab9a36` |
| `TWO_NATIVE_8D_DETERMINANT_SOURCE.md`, including section 9 | `00f79905cf764919ff8328a89cd29941d970e77f8c6420ad93007f5ad61a51fc` |

The proof/checker pair is frozen in local verification snapshot
`46992b4833b2c31f5c0480003561311febebba75`, based on published input
`dec8b42af5b2f3afa9d0d537ac011041a51cb6c3`.
The parent section 9 is a separately reviewed integration edit,
not part of that two-file snapshot.

The proof's five input blobs were independently checked against that
published head. In particular the canonical Book03 blob is
`ecdd31abb52c94e9f2a157a80c7c49a6f5ac31aa`, raw SHA256
`dfa47d91c4994fa8eea64cda67115590056d8aaf48605daf61a1750aaaf0646d`.
No canonical Book definition has been changed.

The checker imports exact ring arithmetic and the finite preparation
fixture from `check_determinant_preparation_bank.py`, blob
`440fce3ba83c2b40a3e0c69ce43ac72dcf74c6b5`, raw SHA256
`79417d85e03e6fb26cfd881f1fccdf69a043188e2a9cf2c8a686420b19682b7e`.
It does not run that old checker, the Golden gate compiler, geometry
or Lean suites.

## Analytical decision and exact parent application

The primary-source reviewer accepted the final proof and parent at the
hashes above. A second same-programme reviewer independently checked
the complete-record entropy, setup differential, source application,
input pins and the distinction between local and total entropy.
The final wording explicitly identifies the local version of formula
(3); the total formula retains one actual J_total without assuming
that its absolute weight factors across blocks.

The accepted application in parent section 9 is

```text
H_total=sum_b m_b {H_pre,b
             +alpha[H_T+beta h_phi(q_b)]E_N(beta q_b)},
S_mean,total=theta H_total-J_total,
D S_mean,total|Sigma=theta alpha c_H DJ2
                              +D(theta H_pre,total-J_total).
```

Here theta=1/2 consumes the owned absolute-amplitude binding on the
same complete leaf alphabet with normalized full branch vectors and
native phases; theta=1 consumes the distinct scalar-probability
binding. Both require physical mean aggregation. On the original
null family, alpha>=1/2, beta>1/2 and q_0<2^(-19) imply the entropy
source multiplier is greater than 3 or 6 respectively, for every N>=1.
Exact integer arithmetic verifies the intervening h'_phi(q_0)>27 bound.

The result removes a demand for literal equality of Book price with
the specified CQ price `E Cost-H_phi(record)`: the actual first-source
transport is sufficient for the same original all16+24+2 equations and
finite-z coupling. No such transport is asserted until the actual
absolute residual and all extra sources are evaluated.

The reviews specifically retained these boundaries:

* Current normalized probabilities do not determine the common J_total.
  Its derivative can change or cancel the entropy source.
* `D E[S]`, `E[D S]` and the amplitude log-normalizer source are distinct.
  The latter two give only `-D J`; the positive multiplier cannot be
  transferred to them by notation.
* The extra-marker-on-Kraus binding has theta=0 and no positive entropy
  source guarantee. Neither binding nor physical Info is selected here.
* The full setup differential (9) retains D alpha, D beta, D H_T and
  D H_pre. Independent preparation/controller/clock equations are not
  discharged by equality on the physical field section.
* Common local alpha, beta, horizon and H_T are needed. Different
  deterministic transcript labels need not have equal costs; extra
  random records need their actual entropy and may reweight the source.
* Costs cancel algebraically only under the supplied binding. No
  execution, copy preparation or minimum-description cost is made free.

The material-access mechanism, physical gain/common normalization,
compulsory task, upstream terms and controlled GR refinement remain
open. The original raw terminal and task lifecycle are unchanged.
The assembly template was inspected; this scoped conditional application
does not fill an accepted positive existence premise.

## Narrow validation

The checker enumerates two independent rational finite ledgers with
119 and 78 complete leaves. Preparation aborts, gate aborts, ready
no-clicks and unresolved horizon outcomes all have positive mass.
Unequal transcript-correlated costs and their actual mean first jets
are retained. Exact formal logarithm-coefficient identities prove
the entropy, both mean bindings, and their differentials; no numerical
independence of logarithms is assumed.

An additional 119-leaf moving-setup fixture verifies all five nonzero
terms of differential (9), including D alpha=1/50, D beta=-1/17 and
D q=2/9. These are declared ledger fixtures, not replacements for
native Golden probabilities or a physical controller model.

Independent Decimal evaluations at precision 85 check the complete
leaf mean by a symmetric difference with step 1e-18 and error below
1e-32. The decisive identities are exact; this numerical comparison
is only a second implementation check.

Negative controls reject omitted preparation aborts, conditioning
away beta, discarding the field-independent internal entropy's renewal
source, and erasing the nonzero common J derivative.

Author validation used Python 3.11.9 with `-B -W error`, in normal and
optimized modes. Both exited 0 with empty stderr and byte-identical
stdout, SHA256
`8bb15eea29f8394e53c12af929d8dcd97f2cdd71e1378e255c01f56fe8735e35`.
The affected `validate_repo.py` (zero warnings),
`validate_agent_protocol.py`, `validate_work.py` and `git diff --check`
passed. The independent isolated replay is recorded below separately
from the author's validation.

## Independent isolated replay receipt

The same-programme reviewer executed the frozen pair in a clean managed
worktree at `46992b4833b2c31f5c0480003561311febebba75`, using Python 3.11.9:

```text
python -B -W error 02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/check_golden_detector_book_mean_source.py
python -O -B -W error 02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/check_golden_detector_book_mean_source.py
```

Both exited 0 with empty stderr and identical 7,991-byte stdout,
SHA256 `8bb15eea29f8394e53c12af929d8dcd97f2cdd71e1378e255c01f56fe8735e35`.
The reviewer checked both artifact hashes, the final local/total wording
and the full setup differential.

An independent in-memory AST mutation omitted the actual gate-abort
record append while retaining its branch termination. The core assertion
rejected it with `RuntimeError: full prep/stage/horizon leaf mass`.
Git was clean before and after; no file was changed and no old geometry
or gate computation was replayed.

## Concurrent route boundary retained at publication

The concurrent [same-carrier field-minimum exclusion](../../../A4D_NATIVE_JOINT_FIELD_MINIMUM_EXCLUSION_2026_10_20.md)
and its [price-graph realization bridge](../../d0_native_joint_field_minimum_2026-10-20/PROSPECTIVE_FIELD_REALIZATION_BRIDGE.md)
were inspected before publication, from the existing PR head
`eb015b59` containing `ce3deb4a`. They retain the implementation optimum
at a fixed field but exclude the proposed full-open-field minimum for
the stated source-preserving price on the primary family.

The present Book mean source calculation does not repair that minimum
premise. It does not turn an externally supplied field query into an
admitted field-writing action or derive field stationarity from a word
optimum. The next physical bridge still requires the actual same-initial
reachable field-and-price graph or an independently supplied native
stationary/constraint law. No source-neutral completion or restriction
chosen to enforce Einstein is supplied as a substitute.
