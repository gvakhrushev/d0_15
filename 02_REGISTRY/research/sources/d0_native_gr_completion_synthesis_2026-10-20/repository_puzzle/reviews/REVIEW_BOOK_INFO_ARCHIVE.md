# Independent review of the exact Book node-Info archive substitution

20 October 2026, full_price_weld, existing PR #334. Read-only source review.

Verdict: **PASS. No blocking mathematical or scope error found.**

Reviewed `/private/tmp/d0_puzzle_stationary_20261020/BOOK_INFO_ARCHIVE_STATIONARY_COMPOSITION.md`,
SHA-256 `1919e0a55e38f3fec4688eb6419c999b096e7ee8481e608d0e93d11a7c2a3f5b`.
Checker SHA-256 `143fe08aac6da6304bddffe1249a57275b896d8613b402c089eff5530fb221e2`.
The exact checker was independently run once: PASS in about 1.2 seconds;
the stationary localized archive norm was `1422692/46268279 > 0`.

The original archive/source owner was also read directly at repository
head `2c592f9b9437cd302fcd39352b85212341bff968`. Its full718 source formula,
rank32 future criterion and original Markov-Poisson definitions agree with
the objects consumed in the reviewed note. No rank census was repeated.

Key algebra verified independently:

* With m=-theta b-(1-theta)Pb and ZP=Z-I+Pi,
  `Zm= -Zb+(1-theta)b-(1-theta)Pi b`. Substitution in the old source formula
  and removal of only the actual im(S) terms gives exactly
  `G=-Q_A J1 D_pi Zb`. Both sign and theta independence are correct.
* `S^T J1=D_pi P D_pi^-1`. After centering b, the norm is
  `||Zb||_pi²-||PZb||_pi²=2<b,Zb>_pi-||b||_pi²`.
  No reversibility assumption is needed. Positivity comes from the archive
  norm, not a spurious claim that the nonsymmetric resolvent is positive.
* Balance gives the first source `-pi^T DI`. The full second source is
  `-pi^T D²I-ln(phi)<B_V,B_W>`; the history-relaxation sign is negative.
  A constant Info shift is archive-invisible but has a nonzero absolute
  pressure derivative. The note keeps that distinction.
* For affine Info on the stated open field chart, an interior local minimum
  requires stationarity plus a nonnegative Hessian. The two identities force
  every field derivative DI[V] to be constant over vertices, then zero by
  stationarity. Affinity extends this to the chart. Conversely constant Info
  gives constant pressure. The stated iff is correct, including non-strict
  minima, and does not apply to nonlinear Info or constrained directions.
* For nonlinear Info, the retained `-pi^T D²I` is indispensable. The displayed
  necessary inequality is correct and is not promoted to sufficiency.

Scope is proper: actual fixed C is a hypothesis of this scalar all-walk
sector, not a selected fundamental physical price. The checker uses one
exact admissible mathematical fixed-C fixture and does not call that fixture
the native selected law. Parallel work labels, archive-dependent dynamics,
full H+J+R, moving primitive costs, finite-clock terms, and the actual
field-to-Info binding are expressly left in their respective owners.

The result composes with the Book/Born Doob test only when both use this
same original support and its K-defined Perron P. A generic Julia/Golden
conditional detector law is not identified with P by this review.
