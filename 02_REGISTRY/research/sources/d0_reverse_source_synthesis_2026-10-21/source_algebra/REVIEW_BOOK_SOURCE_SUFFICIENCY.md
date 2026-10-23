# Independent review: native Book source sufficiency and CAR parity

21 October 2026. Reviewer: `native_admission`; author: `clock_synthesis`.
Scientific input: `2961dc6ee4abcda0a0fb2aa36dc6ecd7e62a6535`.
Existing #334 only. Repository not edited. **Verdict: PASS within the stated
source/cut/interface scope.** No outstanding mathematical correction.

## 1. Frozen inputs and independent replay

Reviewed the complete proof, checker, seven-source historical manifest and
the consumed normalization implementation. The final artifacts are:

| Artifact in `strategy_primitives/` | SHA256 |
|---|---|
| `BOOK_SOURCE_SUFFICIENCY_AND_NATIVE_PARITY.md` | `5a70535e168116d842eef7be902e3944ef908f22837dca5ce95c26979c0b3461` |
| `check_book_source_sufficiency.py` | `02b392162dc401331b7a34139dc3fc82247e1c39b3caca11bb722a8d2fa1e33e` |
| `SOURCE_PINS.json` | `f58cafc351512631255ebff564ac610bb9e37ea249a2874ed78b7d538f47bbfe` |
| `RESULT.json` | `7c6fabf54cab7f7d091eaa1a3b334607a4147f0d6499c3fb09dd4e13c067f775` |

Ran exactly one optimized narrow replay:

```text
PYTHONPATH=/tmp/d0_pydeps python3 -O strategy_primitives/check_book_source_sufficiency.py --repo /workspace/scratch/07af0e1491e7/d0_15 --output /workspace/scratch/07af0e1491e7/strategy_reverse/BOOK_SOURCE_INDEPENDENT_RESULT.json
```

It passed all 50 conditions. The independent result is byte-identical to
the author result, with SHA256
`7c6fabf54cab7f7d091eaa1a3b334607a4147f0d6499c3fb09dd4e13c067f775`.
The checks remain active under `-O`. Historical inputs are verified with
`git show source_ref:path`; the one imported current implementation is also
byte-checked against its historical scientific pin. The original module's
`main`, `exact_checks`, `primary_application` and historical suites are not
invoked. The original `CHECKS` list remains empty.

## 2. First-source theorem and its exact necessity scope

The consumed feedback is

\[
 J=r_R(\operatorname{Tr}\log N-\operatorname{Tr}\log Q),
 \qquad Q=(1-z)N+zB.
\]

At an anchor with positive N and with N,B in a fixed represented unital
*-algebra A, both inverse coefficients lie in A. Trace self-adjointness of
the conditional expectation therefore proves value and first-source equality
after projecting the effect jets. No commutation between N and B is needed.
The moving-z term is retained, and the moving-cut contribution W* (DP) W
is included in DB before the projection. These points are essential and
are correctly handled in the proof.

For fixed z, the two gradient matrices are

\[
 K_N=N^{-1}-(1-z)Q^{-1},\qquad K_B=zQ^{-1}.
\]

The proof's positivity K_N >= 0 and K_B > 0 follows from
Q >= (1-z)N and inverse order reversal. For independent arbitrary Hermitian
jets DN,DB, factorization of the source through their projected jets is
equivalent to K_N,K_B belonging to A: test the two orthogonal complements
separately. The explicit inversion Q=z K_B^{-1} and
N=[K_N+(1-z)K_B/z]^{-1} then proves the claimed equivalent membership of
N,B. Hence C*(N,B) is the minimal unital *-algebra for that universal source
test. The proof explicitly distinguishes this algebraic necessity from
physical admission of all such jets; a smaller actual tangent class can
require less data. This distinction is correct.

The ordinary represented trace and every block multiplicity remain. The
argument does not license replacing a full trace by a chosen prepared-input
expectation or by one selected parity sector.

## 3. Second-source boundary

I independently checked the cancellation of acceleration terms and the
vanishing of mixed retained/orthogonal terms. Bimodularity places the
weighted retained jet in A, so its trace pairing with an orthogonal jet
vanishes even when the anchor effects do not commute. This leaves exactly

\[
 (J-J_A)''=r_R\left(
 \|Q^{-1/2}q_\perp Q^{-1/2}\|_{HS}^2-
 \|N^{-1/2}n_\perp N^{-1/2}\|_{HS}^2\right).
\]

The formula is valid also for moving z: its first-order scalar term is
inside A, while its genuine acceleration is canceled rather than frozen.
The exact controls +8/9 and -8 satisfy 0 < B < N <= I on a neighborhood,
so both signs are substantive. The marked case has no fixed Hessian sign.
For N identically I the second term vanishes, giving the stated
nonnegative defect. The author correctly declines to transport stability
or minima from a first-source quotient alone.

## 4. Actual native parity application

The original CAR creators and annihilators are odd; exterior proper-link
maps are even. Consequently the contracted CAR columns are odd and their
two positive Julia defects are even. The original Walsh transform mixes
within each column. Multiplying by the odd native A gives the claimed
parity of every K_(b,j), including the identity term at j=0. Products of
these operators have definite history parity. Thus every K_word* K_word
is even and the full cost-marked normalizer is even at every finite
horizon, without assuming a scalar normalizer.

The blank-history corner is even. The more general cut statement correctly
requires commutation with the specified output/history parity. It does not
derive that cut from the parity argument. The fixed parity expectation
therefore yields the exact two-block first-source evaluation.

One scope clarification was requested during review and is present in the
final proof: **8+8 is the CAR16 Fourier-block fixture**. On the full S-site
DATA carrier the parity sectors have dimensions 8S and 8S. The global
formula keeps off-site correlations and the complete spatial trace. No
translation symmetry or further Fourier decomposition is inferred for a
heterogeneous geometry.

The new numerical application uses the pinned original 128-Kraus fixture
at theta=.08, mark t=.7 and horizon two. Two applications of its complete
transfer recurrence represent all 128^2 chronological histories; this is
not a fresh full 256-site primary simulation. Both Kraus and jet parity
errors are zero in this fixture. Its normalizer eigenvalue spread is about
9.09330225e-5, and the complete field source is about -4.79117979e-6.
The unmarked source is also nonzero, about -6.85370711e-6. Each source is
recovered from both parity blocks with the original oldRIGHT factor 128.
These numbers are floating controls with declared tolerances; the all-size
identity is the structural parity proof.

## 5. Relation to the reverse reconstruction and Book interface

This result is compatible with the real-Golden two-effect inverse in
`REVERSE_BOOK_EFFECT_RECONSTRUCTION.md`: first identify the two anchor
effects, then evaluate the source on a proved sufficient algebra. The
projection theorem is complex-Hermitian. The unequal real Golden probes
alone do not reconstruct arbitrary imaginary off-diagonal Fourier entries;
one needs an actual real-basis transport or separately admitted phase
probes for such an operational composition. Neither packet silently grants
that extra access.

I checked the cited Book06 sections: they explicitly require a retained
quotient/test interface and keep the fine archive witness distinct from a
maximum-entropy representative. Book03's finite code-cost test bound does
not make the affordable tests closed under operator multiplication. The
author's distinction between a mathematical source algebra and an actually
paid forgetting/test operation is therefore necessary and correctly made.

The contribution is a proved smaller consumer for the specified original
feedback source, not a new microscopic selection law. It does not select
Book Info, determine the physical cut or heat, supply a same-initial
controller, cancel the independent preparation source, or remove the
Hessian defect. Those limitations are explicit. `GR_closed=false` remains
the correct status.
