# D0: source-faithful record geometry — research handoff

Read `SYNTHESIS_RU.md`, then `EXPENSIVE_AI_BRIEF_RU.md`.

This is a local research packet for the existing gvakhrushev/d0_15 #310 programme, not a new registered task, remote commit or GR closure.

## Replay

Python 3.11+; SymPy and NumPy. Exact environment is recorded in VALIDATION.json.

```sh
python check_record_2jet.py > fresh_exact.json
python -O check_record_2jet.py > fresh_exact_optimized.json
cmp fresh_exact.json fresh_exact_optimized.json
python check_mutations.py
python check_heat_window.py
```

The first script verifies exact finite algebra for the analytic second-jet germ. The heat script has an exact rational coefficient plus floating diagnostics; the asymptotic argument is in SYNTHESIS_RU.md. No full previous mathematical replay or Lean build has been claimed.

Inputs are byte-preserved, not edited to agree with the synthesis. Generated older packages are inputs, not independent evidence for newly enlarged conclusions. Source/ref pointers remain explicit; no direct native action is replaced by an arbitrary U(4) germ.
