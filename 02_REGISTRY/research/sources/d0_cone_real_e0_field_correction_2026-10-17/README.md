# Real E0 first-field-correction consumer

[Proof and exact scope](../../A4D_CONE_REAL_E0_FIELD_CORRECTION.md).

`check_real_e0_field_correction.py` exports `run(repo=None)` and prints
deterministic JSON. It extracts frozen full16 creator/connection/D0/D1
definitions only, stopping before any old `assemble()` or `run()`.

The new result constrains real momentum-diagonal E0 preparations, allowing
arbitrary real first coframe/link/observer/measure jets. Axis1 must have
vacuum/top support. A common real balanced rank8 preparation has squared
projected eigen-equation residual at least `1/(8 s^4)`; its full128 reference
is retained. The GHZ, complex, momentum-coherent and other-geometry cases
are explicitly left open. No new action or physical admission is selected.

`RESULTS.json` is the normal stdout. `VALIDATION.json` records the actual
normal/optimized byte comparison, runtimes and input hashes. No previous
spectrum, native root, old suite or Lean target is replayed.
