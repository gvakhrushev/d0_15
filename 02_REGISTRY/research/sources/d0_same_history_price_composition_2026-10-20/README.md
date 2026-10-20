# Same-history paid cost and source composition

This packet is the reproducible source for
[the composed result](../../A4D_SAME_HISTORY_PRICE_AND_SOURCE_COMPOSITION_2026_10_20.md)
in the existing native PR334. The known original port price, clock contraction,
prepared feedback and initial-clock connection source use the same original
128-outcome process. The complete physical Book03 Cost-Info/admission and GR
terminal remain open.

## Proofs and accepted scope

| Object | Derivation | Decisive check |
|---|---|---|
| Every paid chronological history and its full source | [paid_port_history.md](paid_port_history.md) | check_paid_port_cost.py |
| Closed loops plus original open boundary and clock sources | [clock_source_reduction.md](clock_source_reduction.md) | check_clock_payment.py |
| Prepared price effect and retained work-complement correction | [prepared_price_feedback.md](prepared_price_feedback.md) | check_prepared_price_feedback.py |
| Actual finite Gamma jet, corrected coframe and full24 Palatini composition | [d0_sourced_connection_proof.md](d0_sourced_connection_proof.md) | d0_sourced_connection_probe.py |

The original positive-spatial native legs require negative spatial coframe
legs under V=eta e^(-T). Independent review discovered and corrected the old
positive LC label. The original Gamma(H,K) algebra is retained. The correct
LC is K=-H'/2. The snapshots preserve old source bytes and do not silently
rewrite earlier evidence. All24 in this packet means the declared connection
Fourier coefficient, with fixed protected8 preparation and observer; it is
not a full nonlinear field solution or a fixed-positive-clock theorem.

The prepared-feedback comparison includes actual retained-history isometry
jets and full input counting dimension. Its normalized absolute first-source
error O(n^3 p^n) does not select a physical weighting law or prove a nonzero
geometric signal. Marker and inverse execution still require admission/payment.

## Reproduce

Use Python3.11 or later and SymPy1.14.0. From this directory:

```bash
python3 -O -B -W error check_paid_port_cost.py --root inputs
python3 -O -B -W error check_clock_payment.py
python3 -O -B -W error check_prepared_price_feedback.py
python3 -O -B -W error d0_sourced_connection_probe.py --root inputs
python3 -O -B -W error check_connection_coframe_review.py
```

All scientific replay commands are read-only and write JSON to stdout. The
clock check supports an optional explicit receipt destination; normal replay
never rewrites expected evidence. Seven original pins are checked before and
after the connection calculation, and the paid-cost checker verifies its two
original pins. SOURCE_PINS.json records the published commit and exact blobs
for the full snapshot collection. The ordinary CI entrypoint additionally
checks all frozen proof/checker/result pins and compares complete deterministic
results, ignoring only the explicit elapsed-seconds field.

Independent reviews are retained with their exact source hashes. The earlier
prepared-feedback review covers sections1–4; the delta review additionally
covers section4a and its actual repeated-instrument application. The connection
review includes an independent coframe/torsion/scalar calculation, not a claim
to have independently regenerated every entry of the native24 Hessian.
