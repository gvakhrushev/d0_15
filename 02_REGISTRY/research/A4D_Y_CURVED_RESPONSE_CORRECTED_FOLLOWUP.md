# A4D Y curved response — next closure gate

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`
Execution PR: #310
Status: `IN_PROGRESS` / nonlinear continuation open
Action: unchanged naked star action; no added selector or torsion equation.

## Corrected finite result

The result at `ea6e9d0` used the wrong mixed Bloch placement and its finite TT-defect interpretation is withdrawn. The corrected convention is connection equation `lambda^(-s)` and metric readout `lambda^(+s)`.

Two exact certificates are now pinned in this PR:

- `a4d_y_curved_response_phase_corrected_check.py` verifies the 10-component aggregate response for all four Bloch axes, the exact flat and curved connection ranks, the center/range equations, and a hostile swapped-phase control. Its four `q12` averages and defect ranks match the submitted corrected ledger.
- `a4d_y_curved_normaljet_compatibility_check.py` builds all 40 phase-resolved metric rows and the 20-dimensional Riemann normal-jet system. Exact ranks, kernels, curvature projection, smooth-source compatibility, and response comparison match the pinned JSON.

The normal-jet result is:

- connection ranks: flat 80, curved `z=1` 94; curved center dimension 2;
- quadratic phase system: rank 10, nullity 30, curvature projection rank 20;
- all-direction first-slow system: rank 43, nullity 5, curvature projection rank 1;
- smooth-source fast-phase-erasure system: rank 5, nullity 2, curvature projection rank 1;
- response difference from the independently built Einstein control: rank 0 on the compatible smooth-source kernel.

After normalization, the only compatible curved direction is `-Y tensor Y`, with `Y=(1,-1,1)` in spatial bivector order `(12,13,23)`. Its common response is `(3/2,0,0,0,-1/2,-1,-1,-1/2,-1,-1/2)` in metric-coordinate order `(q00,q01,q02,q03,q11,q12,q13,q22,q23,q33)`, exactly equal to the flat Einstein control.

These are finite exact normal-jet statements. They do not construct an exact branch on a curved background or prove a refinement-uniform limit.

## Reproduction

From the repository root:

```bash
python3 02_REGISTRY/research/certificates/a4d_y_curved_response_phase_corrected_check.py
python3 02_REGISTRY/research/certificates/a4d_y_curved_normaljet_compatibility_check.py
```

The first checker also records the submitted report JSON as provenance; it cross-checks its aggregate four-axis fields, not the report's per-site `q12` arrays. The normal-jet checker is the source of the full phase-resolved compatibility theorem.

## Remaining target: nonlinear continuation

Continue the surviving curved normal jet `J` to an exact stationary branch

`K_h(J) = K_Y + a_h(J)`

over sampled smooth metrics `Q_h(J)` with `q(0)=0`, `partial q(0)=0`, and `partial^2 q(0)=J`. Solve the literal finite connection Euler equation `E_K(Q_h,K_h)=0`, retaining the center variables and imposing the full cokernel equations at every order.

Acceptable proof routes include analytic Lyapunov–Schmidt/Kuranishi continuation with a convergent majorant, Newton–Kantorovich on a certified range complement plus the exact reduced center equation, or another finite-dimensional analytic continuation with constants tracked in `h`. The continuation radius must support the background scaling, and omitted orders must be controlled.

The branch must then satisfy the owner-topology estimate

`|E_Q(Q_h,K_h) - E_Q(Q_h,K_h^sm)| = o(h^2)`

uniformly under refinement. Control near-resonant complements, the allowed stationary-center amplitudes, conjugate Bloch-sector interactions, and the declared compact set of smooth background parameters.

If continuation fails, return the first exact reduced center or cokernel equation that fails, its rational/polynomial obstruction, the surviving nonlinear curvature variety, and whether the obstruction forces the Y amplitude to shrink with `h`. A finite normal-jet compatibility result is not itself a nonlinear failure.

## Selector and terminal rules

Do not claim a selector is required unless two exact source-compatible stationary branches over the same admissible smooth background have different normalized metric responses. The corrected finite normal-jet response agrees with Einstein on its compatible direction.

Keep PR #310 Draft and the lifecycle `IN_PROGRESS` until the nonlinear continuation and uniform remainder are proved or refuted. Neither global task terminal has been reached:

- Positive: `A4D-JOINT-PALATINI-RESPONSE-DECOUPLING-CLOSED`.
- Negative: `A4D-JOINT-MICROSTRUCTURE-METRIC-RESPONSE-NOGO`.
