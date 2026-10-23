# Actual variable-field record channel

17 October 2026; same Draft #334, input `aa834d4f`.
Consumer: [the variable-field conservativity proof](../../A4D_VARIABLE_RECORD_CHANNEL_CONSERVATIVITY.md)
and the complete record/source argument, Section 14.

The owner proves a unique conservative minimal QDS for the actual
spatially varying limiting generator on the full compact torus, all 16
form components and reference 128. Its CPTP predual acts on the entire
trace class. The actual discrete marginal channels converge in trace
norm for all converging trace-class preparations: exact first-jump
contractions establish fixed jump layers, then conservation controls
the positive tails. All 127 literal nonblank record slots are retained
in this argument. The proof uses the actual fixed-phase rows, a full CAR gap
and a subprincipal Lyapunov correction, then verifies the joint graph
core and the published conservation criterion.

`check_variable_channel.py` checks only its bounded algebraic inputs:

- The first jet of an actual rotating creator retains all 64 native
  limiting rows and their fixed Hermitian/anti-Hermitian phases. Its
  matrix derivative connection is nonzero although its trace vanishes.
  A variable scalar Kraus phase rejects the false inference from
  pointwise normalization alone.
- The actual constant proper boost gives the stated signed cubic defect
  of the bare energy. The proposed correction cancels it in every form
  component, while the opposite sign leaves a nonzero cubic term.
- The exact golden blank/nonblank split has the correct special jump
  coefficient and telescoping effect identity. The literal native CFL
  bound makes the no-jump operator a positive contraction.
- The generic Clifford commutator identity and an actual degree-seven
  witness support the complete internal gap, without enumerating ranks
  or spectra.

Only pinned creator/native-row definitions execute. Neither prior
`run()` functions nor grid, history, Choi or spectral calculations are
replayed. The new calculation passes 43 exact checks normally and with
optimization, with identical JSON. `RESULTS.json` and `VALIDATION.json`
record the result and input hashes.

```sh
python3 02_REGISTRY/research/sources/d0_variable_record_channel_2026-10-17/check_variable_channel.py
python3 -O 02_REGISTRY/research/sources/d0_variable_record_channel_2026-10-17/check_variable_channel.py
```

The PDE/QDS and full trajectory theorems are analytic results,
independently reviewed in their written form. This fixture does not prove it by finite extrapolation.
Entropy/source limits, physical operations,
clock/code/Info selection and Einstein equality remain separate. The
Lyapunov correction changes no physical operator, action or state space.
