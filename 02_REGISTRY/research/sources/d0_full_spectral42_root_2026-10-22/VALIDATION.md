# Actual validation and scope

Two complete runs of the final `check_spectral42.py`, normally and under
`python -O`, completed successfully and printed byte-identical JSON matching
`RESULT.json`. Both recomputed all 1764 enclosed Hessian entries from 904
distinct centre evaluations, the complex analytic majorant, verified inverse,
whole-ball contraction and physical-coordinate domain checks.

The full constitutive chart and 47-lift application were run normally and
under `python -O`; outputs are byte-identical and match `LIFT_RESULT.json`.
All load-bearing guards use explicit exceptions. The inherited exponential
preconditions are checked again without relying on removable assertions.

Candidate discovery used an independent JAX implementation; high-precision
refinement reused the exact original model. Neither is an existence proof.
Only the outward-interval/Cauchy/Banach calculation certifies the root.

During development an initial diagnostic guessed the two saddle diagonal
signs in the opposite order. That guard failed. The final certificate checks
the computed positive H00 and negative H55, including the entire Cr allowance.
The action, candidate and existence argument were not altered to fix the sign
expectation. An intermediate run was stopped before completing its obsolete
diagnostic; neither run is reported as passing.

This uses the installed mpmath interval/transcendental implementation, with
its software trust boundary. It is not Lean, an independently written second
interval engine, an external scientific review, repository-wide CI, or a
native D0/GR admission certificate. Old large scientific suites were not
rerun as part of this new root proof.

`PREVIOUS_DELIVERY.json` records the independently verified remote publication
of all 29 earlier archive files. New work is appended without changing them.
