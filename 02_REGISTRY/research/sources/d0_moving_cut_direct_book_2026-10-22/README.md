# Original D0 Book03 moving prepared-cut bridge (22 October 2026)

This is one **bounded exact mathematical result** on the original Golden/H/controlled-phase and full128 carrier, published under existing Draft PR #334. It is not a physically compulsory Book03 programme, new action, or a GR proof; `GR_closed=false`.

**New result:** for an isometric native preparation `W` with actual binary output projector Π, set `E=W†ΠW`, and use as Book active cut the *prepared image projector* `P=|0><0|⊗WW†`. Then a **fixed** Golden–CZ–Golden comparator (no moving inverse) has the literal Book03 effect `F=4p E(I-pE)` even when E is noncommuting/noncentral. It matches the earlier `V†CZV` reporter's exact source without executing `V†`, and preserves the protected input rank. The fixed H–CZ–H comparator instead has `F=2E−E²`. Its new application to the **original, every-history native full128 isometry** gives `F_post,n=I−B^(4n)` and exact noncommuting source equality with the old two-n-round blank feedback **as functions**, not as paid executions. A marked-history noncentral normalizer has an exact root-free `logdet N−logdet[(1−z)N+zD_b N^−1D_b]` formula for **both** comparator choices.

**Critical obstruction:** if the prepared output plane is an unpriced free Grassmann variable, a scalar fractional effect at the fair root is not stationary. The actual Golden independent-input critical spectrum is `{0,1,φ/2}`; the extra interior point saturates feedback and has zero source, not an Einstein root selection. Book03 must select/pay the field-moving prepared active cut and include actual Info/controller/clock/oldRIGHT source before the conditional 42-field gain is physical.

## Files

- `PROOF.md`: analytic theorem, native full128/clock and noncommuting marked generalization, 42-source conditional consumer, complete free-input Euler classification.
- `check_moving_cut_book.py`: 63 independent labelled exact symbolic/algebra checks on a noncommuting prepared 2×4 fixture, full original comparator, genuine noncommuting derivatives, allround 2-clock relation, moving marked-normalizer, Golden-input exceptional root, and 42-source report algebra. No assertions (`python -O` retains every test).
- `RESULT.json`, `RESULT_OPTIMIZED.json`: actual ordinary and optimized checker stdout; **byte identical**.
- `VALIDATION.json`: source/checker hashes and exact supported claims.
- `SOURCE_PINS.json`: historical GitHub input commit and immutable source blob identifiers consumed.

Reproduce from this directory:

```bash
python3 check_moving_cut_book.py > /tmp/moving_cut.normal.json
python3 -O check_moving_cut_book.py > /tmp/moving_cut.optimized.json
cmp /tmp/moving_cut.normal.json /tmp/moving_cut.optimized.json
python3 validate_packet.py
```

Nothing in these checks is a full physical M1/G0 admission, new native controller, true Book03 pathwise Info, independent upstream root, original rank216 recovery, independent review, or a fresh repository-wide Lean/CI run. `GR_closed=false`.
