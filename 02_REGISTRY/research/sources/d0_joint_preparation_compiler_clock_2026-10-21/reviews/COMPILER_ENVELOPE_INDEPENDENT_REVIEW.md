# Independent review: actual cap-one compiler envelope and nested minimum

Reviewer: `/root/clock_synthesis`, 21 October 2026.
Input repository snapshot: `dfc0275eea67ebc21ffe539de9b6ea96713863a5`.
The reviewed final package is `/workspace/scratch/07af0e1491e7/compiler_work`.

| Artifact | SHA256 |
|---|---|
| MONOTONE_COMPILER_ENVELOPE.md | af681cc76e2cdeec936a5e70645f4d76200c6ae0a69672fc034b424512227344 |
| check_monotone_compiler_envelope.py | 280b5daca6d81f6b97cbbda9859ca78066e7b610dbdc8afd1ae09ab62fbf6e88 |
| SOURCE_PINS.json | b7e0b3d19ffb97fa2c2e57ba7e4aed4a3edeb75e70b32bcb89940d600b18d687 |
| CHECK_RESULT.json | 1487c939af6c236e5bd0456f8ca52090ce55e6bf4fce2b74d0f35e360cdb5ff2 |

## Verdict

PASS for the stated actual-report, fixed-cost/stationary-delay N=1
factorization and its bounded nested retry comparison. The readiness
requirements, common initial maximum reserve, target-preserving query,
prefix-compatible charges and no-disappearing-abort-penalty assumptions
are essential. This is not a global minimum over all native programmes,
a field minimum, or a compulsory physical Book03/GR selector.

## Analytical review

1. **Actual report versus determinant.** The initial draft's shorthand
   determinant formula needed explicit chart typing. The final proof
   incorporates the requested correction: use the actual two-query report
   product everywhere off shell; determinant equality is exact only on
   the original configured fixed-basis chart, and arbitrary off-diagonal
   extensions have only the owned first-source contact at diagonal Sigma.
   No determinant/J2 Hessian transport is smuggled into the envelope.
2. **Whole paid price.** At N=1 the occupation factor is exactly one.
   Summing actual integer trace copies gives S_j=B_j+g_j F with the
   complete preparation/gate/controller/record baselines retained. Common
   positive g_j, target report laws and field-independent actual price
   assumptions are stated. Heterogeneous local costs are allowed; arbitrary
   heterogeneous local gains are correctly excluded unless later optimized.
3. **Finite nonsmooth envelope.** The two-sided positive-slope bound follows
   by comparing the active lines at the two scalar arguments. It proves
   Frechet differentiability with derivative zero whenever DF=0, and
   strict first-order descent whenever DF is nonzero. Thus ties do not
   introduce a false stationary point. Strict monotonicity preserves field
   extrema and saddles. The directional second coefficient uses the
   minimum active slope on positive Q and maximum on negative Q; its
   failure to be a quadratic form at indefinite unequal-slope ties is
   correctly retained.
4. **Smooth stationary section.** Implicit differentiation of
   B_z+F g_z=0 gives the displayed Schur correction. The inverse belongs
   only to a genuine nonsingular internal constraint quotient. At DF=0
   the mixed block vanishes, preserving the field Hessian up to positive
   gain; no nonexistent preparation or clock stationarity is assumed.
5. **One selector on Sigma.** Since every actual report equals r0 there,
   F0=−M h_phi(r0) is identical for the entire primary field family.
   The finite comparison at F0 needs no hidden field-estimation oracle.
   Selecting this implementation remains distinct from selecting the field.
6. **Common-prefix construction.** With the stated common reserve/layout,
   the shorter capped record is reconstructible from the longer record.
   Completed short histories are unchanged. Only histories reaching the
   short abort are extended. Complete-record entropy chain rule therefore
   gives the conditional extension price, including every retained failure,
   success index, sign and abort. Conditional quantum work remains pure on
   the declared input/reference cut. A disappeared short-abort charge or
   changed target sampling time would invalidate the comparison; both are
   explicitly ruled out rather than silently canceled.
7. **Native atom budget.** I read the original detector/preparation owners.
   Fair plus/minus trials have 5/7 forward letters and one bit, CZ/CCZ
   have 20/42 letters and one bit, and the full two-test X cycle has eight
   letters and two bits. The X sign is already in those two bits. The
   correction CNOT and canonical swap remain additional nonnegative cost.
   With log_phi(2)<2, the first extra stage atom gives net >4 and the
   first extra bank atom >3; subtracting the one possible final report's
   entropy <2 gives precisely the stated >2 and >1 conditional gaps.
8. **Exact divergence masses.** At fixed K the shorter stage-abort event
   has probability alpha_K(1−beta_L). At fixed L the shorter bank-abort
   event has probability 1−alpha_K. Each such event executes at least one
   further genuine trial in the longer programme, even if that trial fails.
   Thus the strict bounds (14)–(15) are justified for the declared nested
   product class and all fields on the target chart.
9. **What is minimized.** Separate per-block readiness alpha>=1/2 and
   beta>=1/2, together with exact monotonicity and the two adjacent
   threshold certificates, yield the unique (K,L)=(9,18). A combined
   alpha*beta>=1/2 requirement would be another task and is not asserted.
   Uniform selected caps at heterogeneous addresses follow only from the
   separable price and common per-block service requirement, as stated.

## Independent execution

I ran the final checker with

    python compiler_work/check_monotone_compiler_envelope.py \
      --repo /workspace/scratch/07af0e1491e7/d0_15

Its parsed output is exactly equal to the pinned CHECK_RESULT.json and all
10 input SHA256 pins pass. The unchanged checker was also run under python
-O during review, with identical mathematical output before the final
additional input pin; no assert-dependent validation is used. Readiness
signs use outward integer/rational intervals, not floating-point signs.
The imported original word constructors reproduce the actual native gate
counts without running the historical large suites. The rational envelope,
tie, Schur and hostile boundary fixtures agree with the analytical proof.

The original small renewal fixtures are explicitly not used as numerical
physical baselines. No unaffected full128, all42, continuum or Lean suite
was rerun or represented as newly accepted. No remaining correction was
found in the pinned final proof/checker.

## Post-integration addendum: concurrent append-only source publication

Independently inspected on 21 October 2026 after concurrent publication
`8463b0a42433cc16e48546b1d62ff8859ea037e8` was merged at
`1e99f0e02d762d6ff5bf3bb1b978d65dc3b2b5c6`. The preceding review is
preserved verbatim; its historical SHA256 was
`18b3ec5c4caa2f6bd61f9cdf7253d15a7d7cef1cd1e6fb76c3535c81248dcacf`.
The original pin table above records the package actually reviewed and
executed before that integration, not a claim that its old pin file is
the current integrated pin file.

The integrated compiler's `SOURCE_PINS.json` now has SHA256
`db64ab97706f748cdc56eb61145e6dea0a76e7dd34fe630c46d19eedbd84e080`.
It preserves the original `input_ref`, records the concurrent
`source_ref` and prior hash/blob for the changed source, and pins that
source's exact current bytes. I checked the diff and independently
hashed all ten current inputs against the integrated pins.

Exactly one input changed:
`02_REGISTRY/research/A4D_SAME_EXECUTION_SPATIAL_WEIGHTS_AND_COMPLETE_SOURCE_2026_10_21.md`.
Its original 18,886 bytes are an exact prefix of the current 20,156 bytes;
the only addition is the 1,270-byte section 7 pointer to the physical
cap-one composition. The former SHA256 is
`b13ef78db2ef108ce0435bc3b678822b4518d6e0eaa4d8610f4672cd5798eafd`;
the strict current SHA256 is
`42c9b9745f3c9ee78b868e991485bbaf8b77810f4261204d913fc87fc44377a1`.
The other nine input files are byte-for-byte unchanged from the original
input snapshot and pass their unchanged SHA256 pins.

The appendix retains the declared complete CQ source while identifying
the separate moving-query, absolute Book03/HJR valuation and independent
input composition obligations. It makes no physical-admission or
`GR_closed` claim and changes none of the compiler theorem's mathematical
premises or conclusions. In particular, the reviewed compiler result
still selects within its stated nested, target-preserving, fully paid
implementation class; it does not identify CQ entropy with Book branch
Info or impose an unpriced free upstream preparation domain.

The integrated proof, checker and CHECK_RESULT.json are byte-for-byte
identical to the three artifacts pinned in the original table. No
checker replay was necessary for this append-only documentation and
provenance change, and none is claimed by this addendum. The original
PASS verdict therefore continues to apply with the strict current input
pin file identified above.
