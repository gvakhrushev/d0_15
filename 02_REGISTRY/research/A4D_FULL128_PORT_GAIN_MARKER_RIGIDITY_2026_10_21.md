# Full128 port-marker weights: explicit bases and corrected extra-factor law

21 October 2026. Existing #334. This corrects the earlier comparison of an unmarked Kraus base with an already marked base, and the unsupported physical scaling F->aF. `GR_closed=false`.

## Original fixed data

For each nonblank pair the original Kraus operators are K_0=pL and K_1=sqrt(p)L, p=phi^-1, with reporting charges (1,2). The normalized conditional data coincide. The supplied analytical cost mark gives

    q_t(0)=p/(p+exp(-t)),   q_t(1)=exp(-t)/(p+exp(-t)).

This analytical tilting is not itself a trace-preserving original execution. A physical implementation must retain failures and its real additional work. The charge gap1 in the following equations is the ORIGINAL reporting gap, not the unspecified total charge of a new filter.

## Four different, correctly typed equations

With a factor ratio phi^(-1+Delta I), direct division gives:

| Base and target | Required Delta I |
|---|---|
| Absolute coefficients on normalized branch vectors, target sqrt(q_t) | 3/2-t/(2 ln phi) |
| Absolute scalar weights, target q_t | 2-t/ln phi |
| EXTRA coefficients on ORIGINAL UNMARKED Kraus operators, target q_t | 1-t/(2 ln phi) |
| EXTRA coefficients on a base ALREADY representing the desired record, preserve that base | 1 |

For the third row, the original amplitude ratio is 1/sqrt(p), while the target is exp(-t/2)/sqrt(p). Thus the extra ratio is exp(-t/2), proving the corrected law. The fourth row instead requires equal extra multipliers. It does not transform the unmarked record into q_t.

At t=ln phi the entries are respectively 1,1,1/2,1. At t=2 ln phi they are 1/2,0,0,1. The earlier claim of a common three-way uniform-point calibration compared different bases and is withdrawn. These are transformations between representations, not a physical contradiction or a selection of Book Info.

## The actual complementary source

A normalizer cannot be inserted into the original complement by assuming F_a=aF. For the literal full-history map W, put N=W*W and A=i*W. The normalized map W N^-1/2 has

    J=-128 logdet[(1-z)N+zA*A]+128 logdet N.

A common scalar cancels in both value and source. A REAL flag-filter instead gives F_filter=I-A_t*A_t and retains all original success AND failure histories; it changes the execution and its cost.

The [executed full128 proof](A4D_FULL128_NORMALIZATION_AND_TRUE_BOOK_SOURCE_2026_10_21.md) computes N and its full jet by chronological transfer, checks all16384 two-round histories, derives the source without a commuting assumption, and applies it to the existing primary HJR preparation row. No full physical Book binding or GR closure follows from this port-ratio algebra. Historical prior text: commit 21fdd9887de75003ebf49bdd67b85734f0d5d4b6.
