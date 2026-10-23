# Native coframe → operator → geometric source

Consumer: [the integrated derivation](../../A4D_NATIVE_COFRAME_HEAT_SOURCE_BRIDGE.md)
in existing Draft #334, SOURCE `158ae785`.

This packet connects the reconstructed Lorentz connection to the existing
full16 positive-adjoint forward operator, computes its actual local heat
source, and follows its16 leading tensor null directions into a4. It does
not assume a finite-v8 source limit or select physical primitives/calibrations.

| Input/output | Meaning |
| --- | --- |
| `USER_INPUT_RU.txt` | Exact supplied text. Its scalar-weight/contorsion matching assertions are checked, not adopted as premises. |
| `torsion_a2_gram_check.py`, `GRAM_RESULTS.json` | All24 exact Gram entries and SO4 decomposition; rank8, inertia4+/4-/16zero. |
| `torsion_heat_consumer_check.py`, `KERNEL_RESULTS.json` | True tensor operator kernel, density shift, right-Clifford connection and nonzero a4 witness; consumes the frozen Gram without recomputing it. |
| `KERNEL_PREVIOUS_RESULTS.json` | Preserved earlier prototype receipt referenced by the extended consumer; historical context, not a replay input. |
| `ppwave_bridge_check.py`, `PPWAVE_RESULTS.json` | Actual full16 LC link sign, nilpotency correction, both Bochner completions, positive scalar curvature and Lorentz/positive-source mismatch. |
| `VALIDATION.json` | Exact inputs/output hashes and normal/optimized receipt. |

Run from repository root, in dependency order:

```sh
python3 02_REGISTRY/research/sources/d0_coframe_heat_source_2026-10-16/torsion_a2_gram_check.py
python3 02_REGISTRY/research/sources/d0_coframe_heat_source_2026-10-16/torsion_heat_consumer_check.py
python3 02_REGISTRY/research/sources/d0_coframe_heat_source_2026-10-16/ppwave_bridge_check.py
```

Adding `-O` must produce byte-identical scientific JSON for each helper.
They extract only the two pinned CAR definition nodes; none executes the
old root, interval-kernel,89-CAR or211-reconstruction suites. Rejection uses
explicit exceptions, so optimized mode does not disable checks.

The all-constant-tensor a4 classification and complete price-source
coefficients are analytic proofs in the owner; a finite witness is not
presented as their proof. The actual Cartan convention is `d=d_ext-Q_T`.
The Gram helper uses `Z_Q=Q_T+Q_T*`; its q and constant-curvature heat
invariants are unchanged by the corresponding overall sign. The pp-wave
helper separately checks the physical native +omega_LC convention.
