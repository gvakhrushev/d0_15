# Independent scope review of the causal/native/weighted synthesis

21 October 2026. Reviewer: `clock_synthesis`. Read-only comparison of the
integrator with the frozen clock/weighted/native proofs. No numerical
replay and no repository edits.

**Final disposition: PASS; all requested scope clarifications and editorial
corrections are incorporated.** The synthesis does not identify the three
different execution contracts or transport conclusions beyond the matching
order. The final changed paragraphs, including the finite-cap readiness
bound, were read separately without rerunning any numerical check.

## Reviewed snapshot

| Artifact | SHA256 at this review |
| --- | --- |
| `A4D_CAUSAL_NATIVE_SOURCE_AND_WEIGHTED_DYNAMICS_2026_10_21.md` | `d3f05bc13512a518c1f0a6738d4e91952774908f1ded5727ee81c004094bbaa3` |
| `NATIVE_POLYNOMIAL_FIRST_JET.md` | `4d098d1e6ad8cb7daf477b498f808b7b962d6432f3da78ae573e321dbbcb915d` |
| `FORWARD_ARCHIVE_BOOK_DETERMINANT.md` | `3c75cc1c7c9928d2209fe58a930105412860aa6c2503801dadcd1ea7b10a5e70` |
| `WEIGHTED_WARD_AND_DUST.md` | `dfb7ef92acbf21ea2154d9d197e9884c59ddc13fdfa912d293403696c283e01d` |

This is an integration/scope review, not a replacement for the native
proof's own independent mathematical review and checker.
The initial integrator review concerned SHA256
`851f02c676ebb2eedb56a73ce19c5761ecca0cd434f2d1b38e5d1251fa0a908d`;
the table records the final clarified text. The other proof pins did not
change during this final check.

## Cross-carrier tests

* **Native jets versus full nonlinear dynamics:** PASS. Sections 1 and 2
  explicitly restrict exact report matching to full ambient two-jets at
  the original primary family. They do not substitute the new report for
  the complete off-null function K used in section 4. The weighted dust
  solutions therefore remain consumers of the original specified weighted
  CQ price, not asserted exact solutions of the new polynomial programme.
* **Causal Book feedback versus fresh measured full128:** PASS. The exact
  determinant retains the compulsory one-tick boundary, all n+1 encounters,
  dark modes, moving-z source and possible absolute boundary divergence.
  Sections 1 and 5 explicitly retain the causal execution's own routing,
  preparation and Info ledger. No equality with the fresh128 measured
  programme's full Cost-minus-Info is asserted.
* **Native report versus input/call price:** PASS. The new readiness is
  computed from the expanded programme and common padded schedules, with
  the original local-copy multiplicities. Root and Hessian transfer is
  explicitly conditional on the actual baseline being field independent;
  DB_new and D2B_new survive otherwise. Supplied copies are not declared
  free, and moving Julia access is still a supplied interface.
* **Reduced versus original metric:** PASS. Section 4 preserves
  g=U^-1 g_tilde and the determined original-coframe torsion. It does not
  call every nonnull reduced dust metric the original physical GR metric.
  The null U=1 exception and the finite Ward-defect boundary are kept.
* **Concurrent Golden-word source limits:** PASS. The native exact fixed
  finite-circuit jets and the separate equal-cost word/secant limit are
  presented as distinct constructions. Programme indices are not promoted
  to already written physical fields.

## Incorporated scope clarifications

1. Section 3 now specifies that the matching finite jets enter the SAME B,
   with fixed horizon and active-cut rank and zero initial archive
   component. This does not require fixed bright/dark rank. Independently
   populated archive/preparation sources are outside that determinant
   comparison and remain in the actual ledger.
2. Section 4 now retains the weighted theorem's interface hypothesis
   D_field B0=0, with M, tau and the stated common calibrations fixed.
   Varying those quantities has the actual chain-rule terms; full
   stationarity in those upstream variables is not supplied by the Ward
   identity.
3. Section 2.4 now retains the native proof's condition that a selected
   relative-preparation variation has no additional dependence through
   the Julia field writer at the declared field coordinates. If it does,
   that writer's actual chain rule remains. LEFT-density stationarity alone
   would not cancel that independent dependence.
4. Section 2.3 now states the exact coefficient condition: the fixed constants
   h, rho_z, tau lie in Q(p), as in the native proof's equation (1), or
   their separate exact preparation is supplied. The original stated
   dyadic/Golden interface meets this condition. An arbitrary real tau
   should not be inferred from the statement that majority preserves tau.

The scalar equation's delimiter is corrected. The null-dust class is now
explicitly positive and local, within the cited proof's regular
nonzero-null-gradient domain.

The added `g_new>=1/2` statement agrees with the frozen native proof's
section 9: a finite resource bank has finitely many positive herald success
probabilities; finite coefficient caps and sufficiently large full nested
factory caps bound their two total failure probabilities by 1/4 each.
All retries are paid. The integrator explicitly limits this to each fixed
carrier and makes no runtime or copy-count bound. It does not substitute
the old 43-Toffoli readiness or the old (9,18) optimizer.

None of these clarifications changes a proved equation or adds a new
scientific premise. They carry the existing proof domains explicitly.
Physical query/writer admission, the complete same-execution
price, native metric readout and the discrete/refinement Ward estimates
remain the stated next obligations. `GR_closed=false`.
