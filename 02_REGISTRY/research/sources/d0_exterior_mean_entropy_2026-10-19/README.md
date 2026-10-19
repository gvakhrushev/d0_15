# Full exterior mean-entropy source

Start with the Russian integration note: [README_RU.txt](README_RU.txt). The preserved source and checker are in [RESULT_RU.md](RESULT_RU.md) and [check_exterior_mean_source.py](check_exterior_mean_source.py); the exact receipt is [RESULT.json](RESULT.json).

This is a scoped readout-source result. It does not select the full native D0 price or replace the two-tick feedback action.

The separate [basis-completion control](check_exterior_basis_ambiguity.py) gives an exact same-compression counterexample: a Hadamard rotation inside the failure space changes the full Shannon source. Its receipt is [BASIS_COMPLETION_CONTROL.json](BASIS_COMPLETION_CONTROL.json). This identifies the output-basis selection as load-bearing; it does not claim that both completions are physically native-admissible.
