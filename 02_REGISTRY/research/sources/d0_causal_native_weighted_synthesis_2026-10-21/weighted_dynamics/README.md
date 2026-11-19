# Weighted dynamics: existing continuum proof and the finite-source continuation

Existing scientific owner: PR #334 / EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.

The substantive weighted law from the prior conversation is already in this repository:

- [WEIGHTED_WARD_AND_DUST.md](WEIGHTED_WARD_AND_DUST.md): exact weighted invariant, both scalar currents, the actual original-metric map, dust converse and finite-source boundary.
- [check_weighted_ward.py](check_weighted_ward.py) and [RESULT.json](RESULT.json): its original high-precision replay; unchanged.
- [REVIEW.md](REVIEW.md): its existing independent review; not a review of the new continuation.

The new [CONTINUUM_TO_FINITE_WARD.md](CONTINUUM_TO_FINITE_WARD.md) consumes section9 of that owner. It computes the material product/inverse-chain defect AND the geometric defect of the unchanged six-face Palatini action. The exact finite identity includes all16+24+2 source rows:

`L_h^* E_h=(a/b) W_geom + [K'(tau q/rho)/b] D_h^+q + W_mat`.

It does not set the defects to zero. A conditional smooth-field bound then controls how closely actual finite stationary roots satisfy the continuum constant-kinetic constraint. Physical roots and native smoothness/admission are not asserted.

New bounded replays:

```
OPENBLAS_NUM_THREADS=1 python3 check_discrete_material_ward.py
OPENBLAS_NUM_THREADS=1 python3 check_full_star_ward.py
```

Run these from this directory, or use their full repository paths. Dependencies: NumPy, SciPy, SymPy and mpmath. New actual outputs are `DISCRETE_MATERIAL_RESULT.json` and `FULL_WARD_RESULT.json`; prior receipts are not overwritten. The new source bindings and hashes are in `WARD_SOURCE_PINS.json`.

The earlier chat's separate 65-check script was not recovered. The new executable reproduces its quoted Golden master numbers and supplies its own real receipt; it does not attest that historical run. The correct convention is positive `y=tau q/rho` with sigma=-1 INSIDE the master F.

All results stay research-scoped. Independent review of the new stencil calculation, full native price/writer selection, joint roots and physical GR/raw216 remain open.
