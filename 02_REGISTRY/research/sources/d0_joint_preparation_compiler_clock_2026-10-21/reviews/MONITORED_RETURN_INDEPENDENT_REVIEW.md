# Independent review: complete monitored-return CQ source

Date: 21 October 2026. Reviewer: `prep_synthesis`, a separate bounded
analytical reviewer inside the existing PR #334 continuation.

## Verdict

**Accept the stated mathematical application on the declared monitored
four-dimensional return component.** It closes the original owner's
missing nonlinear CQ-information first-source estimate and retains the
finite abort. It does not select physical Book03 Info, admit the monitor
or continuous field map, or identify this execution with the separate
local8D cap1 or full128 cap2 programmes.

The initial draft needed an explicit spectator-price condition. That
condition has been added before this review was pinned: entropy neutrality
for a retained pure spectator does not make spin-dependent work or its
independent preparation source disappear. The final text supplies the
actual effective effect and its complete derivative, together with an
appropriate positive counterexample.

## Frozen reviewed bytes

All three files were read in `/workspace/scratch/07af0e1491e7/clock_work/`.
Their SHA256 digests after the correction and independent replay are:

| File | SHA256 |
|---|---|
| `COMPLETE_MONITORED_CQ_SOURCE.md` | `88ae2feab137fdb9f4365fa4a42d3ab91c43e6b77173c5b80da0aec78c46e4c5` |
| `check_complete_monitored_cq_source.py` | `6858ff2bb4488b91196b6b3300cf6aa30187670a2c56233184895459bcc6f39e` |
| `COMPLETE_MONITORED_CQ_RESULT.json` | `67ccfdb933bc6de306919ed8218ff9aa8283c324ac853d0aa5d9326dadb65e57` |

The consumed old owner was read at local input
`dfc0275eea67ebc21ffe539de9b6ea96713863a5`:
`02_REGISTRY/research/A4D_NATIVE_CLOCK_WORK_RETURN_SOURCE_SYNTHESIS_2026_10_21.md`,
particularly sections 4–5. Its genuine sixteen-stage monodromy,
four-step contraction and compatible linear-price convention are inputs;
this review does not claim a fresh replay of that older apparatus builder.

## Analytical checks

1. **Complete information algebra.** For the stated initial product
   `j tensor psi`, with the logical/reference factor retained and pure,
   each stopped outcome has a pure conditional work state. Thus the
   complete CQ entropy is precisely the Shannon entropy of
   `(p_1,...,p_N,s_N)`. The abort vector is retained and normalized only
   when identifying its conditional state. The zero-probability case
   follows by continuous extension. A coherent flag and a dephased CQ
   pointer have different entropies, as the proof expressly records.

2. **Occupation and actual cost typing.** Unitarity gives
   `I-V V*=P`, so the finite sum telescopes to
   `I-V^N(V*)^N`. The stated linear cost and its complete derivative follow.
   The status code contributes `C=(g+2b)I-b M* P M` and
   `Tr C=4g+7b`. A true spectator-dependent effect must be replaced by
   `C_eff=(id tensor omega_psi)(C_full)` and differentiated in both factors.
   The new counterexample has derivative `-8 sin(2a)` while its CQ entropy
   remains independent of the spectator angle, correctly exposing the
   previously implicit boundary.

3. **Uniform power and source estimates.** The old
   `||V^4||^2<=3/4` bound yields the stated `A theta^n` estimate. The
   differentiated power is the ordered sum of all `n` placements of `DV`;
   no commuting assumption is used. Both bounds in equation (4), including
   the first-return prefactor derivative, follow with the printed constants.

4. **No probability floor.** The amplitude entropy is C1 at a zero
   amplitude. On the stated small-amplitude interval its first derivative
   is bounded by the monotone function `x(1-2 ln x)`. The cutoff
   `A theta^36=(3/4)^4=81/256<e^-1` is correct. The argument bounds
   amplitudes from above; it never replaces a small nonzero probability
   by an imposed lower cutoff.

5. **Value and first-source tails.** The entropy aggregation identity
   retains the conditional tail and gives a nonnegative value error.
   Summing `n r^(n-1)` and `n(n-1)r^(n-1)` gives exactly the stated
   `T1_N,T2_N`. Differentiating the retained abort entropy supplies the
   additional `u N+v N^2` term in `B_N`; it is not absent. The whole-price
   estimate (9) additionally contains both `s_N D w_N` and
   `w_N D s_N`. The old cost estimate is consumed with the same fixed cut.

6. **Limiting source and regularity.** Uniform convergence of the C1
   source tails proves C1 regularity of `H_infinity` on the specified
   open unitary chart. It does not imply a finite entropy Hessian at
   newly bright histories. The displayed second-history derivative
   `a_2'(0)=-(1-c^2)` correctly witnesses the amplitude-rank birth.

7. **Interval enclosure.** The Decimal interval arithmetic uses directed
   elementary operations and brackets the correctly rounded square-root
   and logarithm results by adjacent representable values. Negation uses
   exact endpoint sign reversal. Every recurrence, the finite abort
   entropy and the analytic tail are enclosed. The exact tangent norm
   `||dM/dc||=1/sqrt(1-c^2)` is the appropriate multiplier for the tail.
   The final strict interval is positive, so fixed supplied cycle/status
   charges give the stated strictly negative complete price source.

## Independent execution

Command:

```sh
"$CODEX_PRIMARY_RUNTIME_PYTHON" \
  /workspace/scratch/07af0e1491e7/clock_work/check_complete_monitored_cq_source.py
```

The final corrected checker was run independently with Python 3.12.14.
It exited with code 0 and all **40** explicit controls passed. The parsed
output was equal to every field of the frozen result JSON, not only its
PASS label. This includes the interval source endpoints and the
spectator-price counterexample. No new large native128, geometry, Lean
or remote-CI run is claimed.

## Remaining scope

The logarithmic-in-mesh cap prescription removes truncation error only
when the actual gain and price/field budgets satisfy its hypotheses.
It does not erase `D Tr C-D H_infinity`, which is explicitly nonzero in
the supplied native analytic control. Moving cuts, operator-valued abort
charges outside the stated type, and additional history-dependent work
require their real source contracts. This result must not be added to
another programme's price without a same-execution binding.
