# Review: intrinsic RIGHT posterior-gain application

21 October 2026. Supporting native-programme-v1 research in existing
Draft [#334](https://github.com/gvakhrushev/d0_15/pull/334).
Input `0db4b499c307ae3fee11d6a6f71722cf7b8b6b81`.
No physical GR or compulsory Book Info acceptance is recorded.

## 1. Frozen analytical and executable inputs

All paths below are relative to this directory.

| Artifact | SHA-256 | Git blob |
| --- | --- | --- |
| [Proof](PRIMARY_RIGHT_POSTERIOR_GAIN_SOURCE.md) | `3e177e614fb2b30d202f13af65d9896211afeebd68bcb2b497800a7ed0edaba5` | `d9b777bfb6eaea65642e27f049375ab07e68430c` |
| [Checker](check_primary_right_posterior_gain.py) | `2985ab0b4fb007c424c75d2bd57369b781ad1b1653ec3b8b8c68d4d30780367d` | `c3b0162036e224c6f0111e72ed77bec3d6554b9c` |
| [Certificate, LF storage](PRIMARY_RIGHT_POSTERIOR_GAIN_SOURCE_CERTIFICATE.json) | `3fc747be8d27a7b581cfa7a2e9b58da5ff87058a4e3b76199dd2e9483a674b6a` | `1a55c95736945835e2a35c3fd47cad8a835600ab` |
| [Consuming parent through §13](TWO_NATIVE_8D_DETERMINANT_SOURCE.md) | `feb36f954a616118b32b5cd6386be4e65eba77b084fb47e73644a32d2d49eea0` | `e8b9423373b208b4332fd2cb3f454f1c39893203` |

The raw certificate preserves every one of the33 distinct posterior
spectral enclosures, full64-outcome multiplicities, exact64 dark
outcomes and six runtime input hashes. The prior's exact identity is
analytical; interval containment separately checks the constructed
matrix sum and its zero first jet.

## 2. Author replay

Bounded implementation owner `/root/readout_checker` wrote only the
new checker. Python3.11.9 / NumPy2.2.6, input0db4b499:

```text
python -B -W error check_primary_right_posterior_gain.py
python -O -B -W error check_primary_right_posterior_gain.py
```

Both exited0, stderr empty, in64.894 and70.828 seconds. Their stdout
was byte-identical,35,314 bytes, SHA-256
`cc5d42cdc309cb536485d513c3793ab40b59add2e23ac30b2c49c941485fee80`.
Git stores the same JSON with CRLF converted to LF:34,348 bytes and
the separate exact hash in §1. No other byte or numerical value changed.
These were changed-calculation checks; no unchanged
old mathematical or Lean suite was replayed.

Certified Golden-unit leading angle coefficients:

| Observable | Lower endpoint | Upper endpoint |
| --- | --- | --- |
| RIGHT/full-pointer posterior gain | 2.1910472674029542e-9 | 2.1910477557180062e-9 |
| Known port cost | -2.7461810898740312e-8 | -2.746181089819066e-8 |
| Known port cost minus that gain | -2.965285865445832e-8 | -2.965285816559361e-8 |

All64 active B_gamma have certified rank128, with global minimum
eigenvalue greater than1.8599583513003547e-13. These are unnormalized
posterior matrices, not a rank cutoff. Sum q contains1; sum Tr R
contains0; the full matrix sums contain I/128 and0 entrywise.

## 3. Independent analytical review

Read-only reviewers `/root/primary_source_review` and
`/root/same_programme_source` reviewed the exact proof/checker hashes
in §1. Both accepted the actual Gram/partial-trace transpose, the
outcome-wise central-prior maximum, original Fourier-pair witness,
fixed-parity small-t jet, full64/64 outcome routing and posterior
support argument.

The second reviewer required the actual port multiplier:
Cost_port=1+p epsilon R, so its coefficient is -p epsilon a_R,
not the Rayleigh coefficient -a_R. The proof was corrected before
freezing. It also states that posterior logs use the entire declared
periodic-storage L4 fixture; the source coefficient has no asserted
independence from arbitrary exterior completion or mesh refinement.

The spectral proof uses an arbitrary numerical eigensystem only as
a candidate. Interval Frobenius residuals bound operator norms; polar
correction, a strictly positive lambda_min-epsilon, the resolvent
log bound and the rank-two nuclear trace bound certify its source.
The reviewers found no remaining mathematical correction.

The explicit arithmetic premise remains IEEE binary64 nearest
arithmetic without FTZ/overflow and the stated direct einsum finite-dot
model, optionally FMA. Canaries check representative runtime behavior;
they do not prove every possible backend implements that model.
No eigenvalue floor or eigensolver accuracy hypothesis is used.

## 4. Exact parent application and retained premises

The parent §13 consumes the original preparation's actual reference
C_t* C_t=I_128/128 and its complete instrument's posteriors. Thus the
owned central gain theorem now has a concrete original-RIGHT input.
It also consumes the certified full-fine preparation-source sign;
the positive value witness by itself never establishes that sign.

This removes an unspecified reference on this particular supplied
cut. It does not close the parent native constitutive/selection
premise. Physical RIGHT tests, compulsory Book Info, the same-initial
preparation/field/controller graph, complete nonuniform code prices,
absolute Book normalization and required work remain. The later-round
and refinement applications, full native GR and raw216 remain open.

## 5. Independent frozen replay

Reviewer `/root/primary_source_review` used the isolated managed
worktree `C:/Users/kmeze/.codex/worktrees/right-posterior-verify/d0_15`
at local frozen commit `9ffc1a2bf3bfa43fa8f1fb3c05dce75584474701`.
Initial status was clean; exact proof, checker and stored certificate
hashes matched §1. This commit identifies the verification input;
it was not claimed as an independently published remote ref.

The normal `python -B -W error` replay exited0 in65.9518422 seconds;
the `python -O -B -W error` replay exited0 in65.4764871 seconds.
Both had empty stderr and identical35,314-byte stdout matching the
author SHA-256 in §2. Converting only CRLF to LF matched the stored
34,348-byte certificate and its SHA-256 exactly.

The single in-memory AST mutation changed only the actual clock
component of C_0 from f/128 to f/64. Slack, expected checks and all
other source expressions were untouched. It failed in65.2809111
seconds with `RuntimeError('complete full-fine probability and jet')`;
it produced no certificate and no false PASS. The exception was
captured by the independent harness, with empty stdout/stderr.

The checker remained byte-identical. The worktree was clean before
and after, with unchanged HEAD9ffc1a2b. No source file, expected
coefficient or scientific statement was rewritten for validation.

## 6. Integrated structural validation

Parallel published changes through
`c4cb6a93193864057e7903cba8bc607b431ecdf8` were integrated before
the final structural checks. The same six runtime inputs remained
byte-identical. Nine GitHub reads at that immutable remote commit
verified the runtime/analytical owner contents and blobs, including
the unchanged consuming parent before the appended §13.

On integrated local checkpoint
`742f3795046cc007cc8c8a78b9a21576e40c21d2`, Python3.11.9 passed once:

```text
python tools/validate_repo.py
python tools/validate_work.py
python tools/validate_agent_protocol.py
python tools/gr_assembly.py check
python tools/gr_assembly.py render --check
python tools/render_work_status.py --check
python tools/generate_lean_views.py --check
```

All exited0; repository warnings0, work/Lean views current, assembly
valid and `scientific_promotion=false`. The new proof/review relative
links resolved and the parent prefix through §12 was unchanged.
No mathematical input changed after the isolated replay. This section
records checks only; the four artifact hashes in §1 remain unchanged.
