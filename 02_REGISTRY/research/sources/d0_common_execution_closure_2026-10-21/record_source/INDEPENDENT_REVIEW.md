# Independent review: uniform complete-record source universality

21 October 2026. Reviewer: `clock_synthesis`, independent of the proof
author/integrator. Existing #334, scientific input
`b1870ff3ecedd02e09388bc8b6fd8df4da54b990`.

**Verdict: PASS, with the conditions already stated in the frozen proof.**
No proof change was requested or made. This is an analytic first-source
review and one narrow optimized replay, not a Book selection or full GR
certificate.

## Pinned artifacts

| Artifact in `closure_universality` | SHA256 |
|---|---|
| `UNIFORM_RECORD_SOURCE_UNIVERSALITY.md` | `a8c17dc2975078071b8644a42a270ef695aaab4671d73f0901b0cfcb0060f5b1` |
| `check_uniform_record_source.py` | `53b1fdb8ad989eeb9425401b44e6e10af2424949be8f983ed140486f71ea4a13` |
| `SOURCE_PINS.json` | `9b04de9385df8f6711d22b316f880c3f33473c96729270b4e5b2f506c2573910` |
| `RESULT.json` | `9223e264716ee13936f210973ba151b3d295aaa7b331980022a66d1cce5463f8` |

All four source-pin hashes and byte counts were independently checked
using `git show b1870ff3:path`, including the original Book binding owner.
The actual native-processor and paid-bank interfaces were read separately
at frozen proof hashes `4a879a3bb986aca43f06cec760f882cec4e7c6446efd46d5add8a2f199e9381b`
and `8348922c3a093b06b91ad52249177238e8abab89057bdaf002deac0fd1ced1d7`.

## 1. Local two-stratum argument

At `p_t=1/M`, `r_t=r0`, a symmetric differentiable function of the
positive spectrum has the same cotangent coefficient at all coordinates
with the same report bit. Its simplex cotangent is defined modulo a
constant, but the difference `a1-a0` is unambiguous. Consequently

`D V=(a1-a0) D sum_t q_t1`

holds for every normalized probability tangent. The transcript-normal
term vanishes because `r0 sum_t Dp_t=0`; no off-family probability has
been frozen. Conditional pure-work/reference rotations change only
eigenvectors and are invisible to the stated spectral valuation.

The rank convention is correct: derivatives are taken on the fixed-rank
pure-conditional-work family. The proof does not differentiate Shannon
entropy through the creation of a new positive eigenvalue. At `r0=1/2`
the response can vanish; the nonzero-response requirement is retained.

## 2. Full factory profile and actual measured selector

Successful factory blocks have different fixed weights in general, so
their eigenvalue derivatives can have different spectral coefficients.
The proof correctly retains the weighted sum. Equal scalar readiness
would not be enough to equate the coefficients across local cells; the
full padded factory distributions and the full conditional report
responses are the stated conditions.

An actual measured uniform permutation produces a block direct sum.
At a diagonal input, those blocks repeat the same spectrum. The gradient
is therefore repeated and its differential averages the conditional
directions for the **corresponding repeated-spectrum valuation**. This
does not assert `V(direct sum)=average V`, and the proof explicitly avoids
that false equality for nonadditive valuations away from the diagonal.
The repeated spectrum can change the actual source coefficient; it does
not license carrying over a coefficient from the unpermuted valuation.
The claimed critical-point transport uses the actual common coefficient.

Previously measured selectors must remain in the complete record on a
later factory abort. The paid-bank theorem retains them. The processor's
deferred address/Bell readout avoids a new programme-dependent classical
prefix on its own factory abort. These two record rules are compatible.

## 3. The whole product valuation

The argument for `F(q1 tensor ... tensor qL)` is valid for a general
nonadditive symmetric differentiable spectral function. At identical
factor profiles, exchanging tensor factors merely permutes the complete
eigenvalue list, so all marginal cotangents are identical. Permuting
equal-probability labels within one successful factory slice likewise
makes that marginal cotangent constant on its two report strata.

Summing the slice contributions yields one coefficient times the sum of
conditional report sources when their response is common across the
successful slices. The proof states that condition and verifies its
consumer through the same ideal circuit on every completing factory
history. Without it the source is the sum of different slice responses,
as explicitly acknowledged.

The full product has many spectral strata. The proof correctly mentions
the `L+1` Hamming strata in the simple factory-free case; it never
identifies the complete spatial execution with a single binary report.
Only its complete probability spectrum is needed. Permuting LEFT
resources while retaining the old RIGHT registers does not require a
physical operation on RIGHT to apply this spectral argument.

For the complete Shannon processing profile the coefficient is exactly
`-gamma_F h_phi'(r0)`, not the conditional-only `-h_phi'(r0)`. The corrected
frozen version has this distinction. Any outer paid-permutation profile
is then included by its actual repeated-block derivative, rather than
silently discarded.

## 4. Scope of the primary-source consumer

The original field and material source is consumed on the specified
primary family, with fixed collar, fixed multiplicities and the actual
moment-map/Lorentz-projection interface. Equal coefficients preserve the
spatial Euler cancellations; unequal cell coefficients generally do not.
The independently prepared resource bank supplies separate normalized
input variations, not an arbitrary entangling tangent of the whole bank.

The theorem gives conditional first-source transfer. It does not prove
Book03 spectrality, relabelling invariance for future-distinct memory,
the nonzero response of a genuine Book valuation, source neutrality of
input creation, or selection of a stationary functional. It also does
not identify enlarged preparation Hessians or an unrestricted minimum.
These limitations are necessary and are present in the proof.

## 5. Narrow replay

Executed only the new checker under `python3 -O`, writing
`closure_price/UNIVERSALITY_REVIEW_REPLAY.json`. Its bytes equal the
frozen `RESULT.json` exactly, with the result hash listed above. The
checker uses explicit failure conditions rather than removable Python
assertions. It checks exact local, nonadditive whole-product and
measured-permutation derivatives, with unequal-label, unequal-cell,
unmatched-abort and zero-response controls.

The checker is a bounded set of algebra controls; the analytic proof
supplies the general differentiable theorem and the conditional factory
extension. No old root, rank, full32 Bell or all42 suite was replayed.
