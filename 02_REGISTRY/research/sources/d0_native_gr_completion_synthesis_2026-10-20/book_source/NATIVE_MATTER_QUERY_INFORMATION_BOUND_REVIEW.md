# Review: local material-query information bound

20 October 2026. Existing Draft PR #334,
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`,
`native-programme-v1`. Bounded necessary-condition result; no parent
retirement, assembly acceptance, CORE or physical-GR promotion.

## Frozen statement and inputs

| Artifact | Raw-byte SHA256 |
| --- | --- |
| `NATIVE_MATTER_QUERY_INFORMATION_BOUND.md` | `8905773fc3690f9b22b51b7c7a65f7511b4deb32726b37d80a9f60227b46e43f` |
| `check_native_matter_query_information_bound.py` | `3e42965e3afe8865baddeebf2e97577409a1811cb9ca3953cde0be3043d31861` |
| `TWO_NATIVE_8D_DETERMINANT_SOURCE.md`, including application section 8 | `e613d9cec2e682bc93245b8a4a551ec77482aa77a0d9e79ed1fce66c26eb03ab` |

The proof/checker pair is frozen in local verification snapshot
`217cb02af761cc58362500581f6b7db65f9879c9`.
Its published input head is
`49f0c937d7e09d90f5b8db376849c6c821b493c9`.
The parent section 8 is a separately reviewed integration edit, with
its final hash in the table; it is not part of that two-file snapshot.
The snapshot retains the original parent input blob listed below.

| Consumed input at that head | Git blob |
| --- | --- |
| `../../d0_primary_native_domain_source_2026-10-20/RESULT.md` | `ed00d6609c6f9f88391c7ff076abc65a3524dbd1` |
| `../../../A4D_LOCAL_LEFT_CODED_CAR_NULL_MATTER_EINSTEIN_2026_10_18.md` | `75c40d133a23973a36ba5b95d34b4eb36ca96663` |
| `TWO_NATIVE_8D_DETERMINANT_SOURCE.md` before section 8 | `85e9d19012d543873269e3584b6ec2763b868637` |
| `GOLDEN_EXACT_DETECTOR.md` | `92b9003d783c24b1883a2a21f8b30625078afff7` |
| `check_determinant_preparation_bank.py` | `440fce3ba83c2b40a3e0c69ce43ac72dcf74c6b5` |

The imported ring helper has raw SHA256
`79417d85e03e6fb26cfd881f1fccdf69a043188e2a9cf2c8a686420b19682b7e`.
Its old checker is not executed. No geometry, large history or Lean
replay is needed for this new local calculation.

## Independent analytical decision and parent substitution

The primary-source reviewer and a second same-programme reviewer
accepted the final proof and the exact section 8 application at the
hashes above. They checked the full CAR/RIGHT128 normalization,
the admitted singleton tangent, inverse-PF factor, strict calibration,
Golden query derivative, complete-instrument inequality, variable
readiness and the positive denominator. The primary-source reviewer
also independently verified the strict rational finite bound above 46.

The accepted replacement in the parent argument is:

```text
If the only material-dependent input is n independent copies of C,
all other input states and complete instrument maps being fixed,
then reproducing the local d_b and its first matter jet requires

n >= beta Cq^2 rho_x^(-2) v_x^2 S /
     [h^2 d_0(1-d_0)(1+psi_y^2/slack_y^2)].
```

Here C is the actual normalized global CAR/site/RIGHT128 purification,
the variation is the original real amplitude at y=x+v, and v_x is
the actual calibrated null flux. The target is the original two-query
likelihood with the same Golden factors, not a newly fitted statistic.
No source norm or global normalization is changed.

For fixed positive strength/readiness/flux and uniform density/slack
bounds, a uniformly bounded copy-only replacement is excluded along
refinement. On a fixed four-dimensional site region the necessary
growth is Omega(h^(-6)). Variable parameter scalings retain the exact
inequality. The finite L=512 certificate, conditional on its stated
actual density and readiness bounds, requires at least 47 copies.
This is necessary and not sufficient.

The result changes only this local-query input route. It does not
derive a bound from the summed stationary Euler covector, whose
neighboring matter terms cancel; exclude a programme preserving only
the summed equations; or exclude material-dependent code, oracles,
archives and programme states. Those resources must enter their own
complete input and price. A fixed available-copy bound is not silently
converted into expected Cost.

The physical material-input map and its preparation/clock, compulsory
task and Book03 valuation, additional upstream source terms and
positive GR closure remain open. The original raw response terminal
remains separate. The assembly template was inspected; no positive
existence premise or task completion is claimed by this scoped result.

## Narrow exact checker

The checker verifies both Golden orientation signs by dual-number
arithmetic, the actual four-mask state and horizontal slack tangent,
all128 RIGHT cross-Gram first jets, the null forward stencil with
arbitrary Brinkmann H, strict Golden and rational calibration, the
three-outcome readiness Fisher identity and the rational copy bound.
The actual real Fourier basis consists of 64 cosine/sine pairs;
their summed weight is 1/S. Individual real columns are not falsely
assigned equal weight. Equality with a fixed unitary complex phase
basis is only a normalization cross-check.

The universal information inequality is the analytical
Cauchy--Schwarz/completeness proof in the note. Finite Kraus and tensor
fixtures verify its algebra and factors; they do not replace that proof.
Negative controls retain the factors S, inverse-PF and beta and reject
conditioning away the abort experiment.

The author ran normal and optimized Python 3.11.9 with `-B -W error`.
Both exited 0 with empty stderr and identical stdout, SHA256
`6893be73e42dcf694ff00229c433c2b71feb5e7f3b44d1da9340e5a23a9973b6`.
The affected `validate_repo.py` (zero warnings),
`validate_agent_protocol.py`, `validate_work.py` and `git diff --check`
passed.

## Independent isolated replay receipt

The same-programme reviewer independently executed the frozen pair in
a clean managed worktree at
`217cb02af761cc58362500581f6b7db65f9879c9`, using Python 3.11.9 on
Windows AMD64:

```text
python -B -W error 02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/check_native_matter_query_information_bound.py
python -O -B -W error 02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/check_native_matter_query_information_bound.py
```

Both exited 0 with empty stderr. Their 6,087-byte stdout was identical
and matched the author hash
`6893be73e42dcf694ff00229c433c2b71feb5e7f3b44d1da9340e5a23a9973b6`.
The reviewer independently checked the frozen proof/checker hashes,
all five input blobs and the imported helper hash, and accepted the
corrected 64-pair normalization.

An in-memory AST mutation removed `/rho` from the sparse matter
derivative calculation. The core assertion rejected it with
`RuntimeError: actual null-covector matter source retains inverse PF and calibration`.
The worktree was clean before and after. No tracked file was changed
and no previous geometry or Lean calculation was replayed.
