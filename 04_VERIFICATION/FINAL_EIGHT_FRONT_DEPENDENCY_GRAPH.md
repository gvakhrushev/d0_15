# Final Eight-Front Closure — Dependency Graph (Iteration 22)

Honest status of the eight-front campaign. **Global closure is NOT achieved**: every front
produced a real finite owner for its *closable scope*, but nine named blockers remain (the
PROOF-TARGET rows below, `is_global_blocker = True` in `FINAL_EIGHT_FRONT_BLOCKERS.csv`). Three of
the eight proposed constructions were mathematically *false as stated* and were closed as no-gos or
narrowed, not faked:

- **F1** a finite 30-dim heat trace has **no `1/s` pole** (`c₋₁=0`, `c₀=30`); `12288/5` is not a
  finite-trace residue → NO-GO, not a Dixmier closure.
- **F3** Riemann–Hurwitz does **not** force the pair `(4,3)` (every cyclic cover is genus-0) →
  narrow CERT (branch index `1/n` + genus-0 identity), no uniqueness.
- **F7** the anomaly-free variety is **2-dimensional** `span{Y, B−L}` → NO-GO (row not forced),
  not a row-uniqueness owner.

## Per-front closure chain

| Front | Closed this campaign (real owner) | Status | Remaining blocker (named) |
|---|---|---|---|
| F1 Δα/Dixmier | `D0-DIXMIER-FESHBACH-FINITE-HEATTRACE-001` (finite trace ⇒ no pole) | NO-GO | residue→Δα normalization over the infinite/profinite `2¹¹` tower (`D0-ALPHA-FESHBACH-DIXMIER-OWNER-001`, ext. Dixmier/Wodzicki `ASSUMP-DIXMIER-TRACE`) |
| F2 CKM class-5 | `D0-CKM-CLASS5-SELECTOR-OWNER-001` (M1Forced selector witness) | CERT-CLOSED | none — exclusion already CORE (`D0-CLASS5-ALIASING-001`); selector now closed |
| F3 Lepton R-H | `D0-LEPTON-RIEMANN-HURWITZ-BRANCH-INDEX-001` (index `1/n` + genus-0 identity) | CERT-CLOSED | finite Green resolvent with provably-`(0,1/4,1/3)` indices + operator uniqueness (`D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001`) |
| F4 Phason w_DE | `D0-PHASON-ARCHIVE-CAPACITY-REDSHIFT-001` (redshift bijection + `w_N` exact) | CERT-CLOSED | continuum interpolation + physical negative-`w_DE` map (`D0-PHASON-WDE-Z-MAP-OWNER-001`, `D0-PHASON-WZ-EXPLICIT-FUNCTION-001`) |
| F5 Toral Markov | `D0-WILLIAMS-SHIFT-EQUIVALENCE-OWNER-001` (GL(2,ℤ) similarity + SE invariants) | CERT-CLOSED | Williams strong-shift-equivalence chain = topological conjugacy (`D0-TORAL-TIME-MARKOV-CONJUGACY-001`, ext. `ASSUMP-ADLER-WEISS`) |
| F6 Higgs EOM | `D0-HIGGS-LOGDET-STATIONARY-POTENTIAL-001` (Jacobi variation + stationarity) | CERT-CLOSED | proven double-well sign `f''(0)<0` (`D0-HIGGS-PHASON-CONDENSATION-OWNER-001`) |
| F7 Hypercharge row | `D0-HYPERCHARGE-ANOMALY-VARIETY-2DIM-001` (variety 2-dim, row not forced) | NO-GO | derived `Y_νR=0` + up/down branch selector = flow→Weyl map Φ (`D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001`) |
| F8 CMB n_s | `D0-CMB-NS-LAPLACIAN-IDS-OWNER-001` (IDS staircase + P(k) + spectrum-alone NO-GO) | CERT-CLOSED | canonical forced smoothing rule fixing `(k,u)` (`D0-CMB-IDS-SMOOTHING-OWNER-001`, `D0-CMB-PHASON-SPECTRUM-OWNER-001`) |

## Closed (8): 6 CERT-CLOSED + 2 NO-GO. Minted PROOF-TARGET with exact gaps (2): F4 z-map, F8 smoothing.

## Remaining global blockers: 9 (the PROOF-TARGET rows). Global "D0 complete" is therefore FALSE and is forbidden by `vp_eight_front_final_closure_no_overclaim.py`.
