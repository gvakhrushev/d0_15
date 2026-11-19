# Nonvacuum collective preparation: paid implementation and two-sided source recovery

22 October 2026. Scoped research in existing Draft PR #334, task
`EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`,
`constitutive/native-programme-v1`.

## Consumer and result

The [integrated proof](../../A4D_NONVACUUM_COLLECTIVE_PREPARATION_SOURCE_EQUIVALENCE_2026_10_22.md)
consumes the existing exact nonvacuum all-mesh field solution, actual moment
encoders, coherent attenuation and the earlier full-polynomial overlap lemma.
The changed input is a genuinely paid coherent choice of distinct resource
banks and the first-conditional cancellation for the complete nonvacuum
history score. The complete logical iid law and its field equations are
preserved exactly at every finite bank size; the new factory and clock law
is fully included in the price.

With the actual source gain `a=Gamma*tau*gamma`, the result is

\[
E_h\leq \frac{\sqrt N\,\|d_{\mathrm{prep}}S_{h,N}\|_{\mathrm{pure}}}
{2\Gamma_{h,N}\tau_h|\gamma_h|}
\leq\sqrt{E_h^2+\frac{C_h^2}{N-1}}.
\]

Here E_h is the weighted norm of ALL free deduplicated field equations.
The pure covector is taken on the full kind-input bank with the fixed
actual encoder and retained purifiers. The lower bound excludes spurious
stationarity from unscaled averaging. The actual ten-flag attenuation
gives a linear-in-tau remainder, so readiness and signal are each divided
out exactly once. Independent apparatus, preparer, clock and the remaining
physical Book03 source are not assumed stationary.

## Files

| File | Exact role |
|---|---|
| [global_audit/NONVACUUM_WHOLE_TAPE_U_STATISTIC.md](global_audit/NONVACUUM_WHOLE_TAPE_U_STATISTIC.md) | Whole-history score, nonvacuum cancellation, overlap upper bound and one-excitation lower bound |
| [joint_source/PAID_COHERENT_INJECTION_AND_WHOLE_TAPE_SOURCE.md](joint_source/PAID_COHERENT_INJECTION_AND_WHOLE_TAPE_SOURCE.md) | Actual coherent without-replacement selector, finite caps, complete priced law and actual gain |
| [causal_domain/PAID_JOINT_NORMAL_AND_NATIVE_TASK_FIBRE.md](causal_domain/PAID_JOINT_NORMAL_AND_NATIVE_TASK_FIBRE.md) | Finite paid positive/negative correlation preparations with equal decoded fields and full retained failures |
| [check_native_attenuation_gain.py](check_native_attenuation_gain.py) | Exact Q(p) check of all 1,024 sign columns, signal and material ratio |
| [global_audit/REVIEW_INTEGRATED_SOURCE.md](global_audit/REVIEW_INTEGRATED_SOURCE.md) | Independent integrated normalization, chart and scope review; its two minor corrections are incorporated |
| [causal_domain/REVIEW_COLLECTIVE_SOURCE.md](causal_domain/REVIEW_COLLECTIVE_SOURCE.md) | Independent review, including the necessary deferred-report schedule correction |
| [joint_source/REVIEW_SOURCE_COMPOSITION.md](joint_source/REVIEW_SOURCE_COMPOSITION.md) | Independent gain/source review and independent original-report differentiation |
| [SOURCE_PINS.json](SOURCE_PINS.json) | Exact consumed repository blobs and original attachment hashes |
| [RESULT.json](RESULT.json) | Actual final-run receipts, scope, runtime and artifact hashes |

The old overlap lemma is in
`A4D_LABELLED_GOLDEN_RECORD_FULL_SOURCE_2026_10_18.md`, section 6.78,
equations (13ir)--(13it). Its older scalar-free-vacuum application is not
relabelled as the new nonvacuum result.

## Reproduce the changed checks

Requires ordinary Python 3 with its standard library. Run from this folder:

```sh
python3 run_checks.py
```

This executes only the four new bounded checkers, keeps each exact receipt,
and regenerates the integrated run record. Assertions must be enabled;
the runner rejects optimized Python mode. The four commands separately are:

```sh
python3 check_native_attenuation_gain.py
python3 global_audit/check_nonvacuum_whole_tape.py
python3 joint_source/check_paid_coherent_injection.py
python3 causal_domain/check_paid_joint_normal.py
```

The expected counted groups are 2,070 exact Q(p) checks, 103 exact rational
checks, and 2,992 exact plus 67 floating-logarithm checks. The fourth checker
also verifies every flag outcome for depths 1 through 16 and 34 cyclic
count shells; it does not claim an enumerated assertion count. Its 90-digit
entropy secants and the formatted real diagnostics are not interval proofs.
These checks test the changed finite identities. They do not replay the
historical full42/full128, Golden compiler or Lean certificates.

## Preserved limits

The actual reporter must defer all logical report measurements and terminal
0/10 emissions until every logical factory has succeeded. This makes abort
transcripts input independent in the specified nonadaptive execution. No
such schedule equivalence is assumed for adaptive Book03 stopping.

The result gives approximate complete pure-preparation stationarity in the
specified counted-CQ implementation and actual normalization. It is not an
exact finite joint root, a density-cone minimum or stability theorem, an
autonomous C1 native code writer, or compulsory selection of the complete
physical D0 action. Concurrent information-only nonselection and joint-index
results retain their original scope. `GR_closed=false` and
`full_D0_price_selected=false`; no lifecycle or claim is promoted.
