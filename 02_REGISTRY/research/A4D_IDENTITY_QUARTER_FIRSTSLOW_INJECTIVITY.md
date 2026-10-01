# Quarantined first-slow calculation: wrong Euler placement

Task: `EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE`, Draft PR #310.
Status: negative control only. The former physical interpretation is withdrawn.

The retained checker stacks `(A;C)`, whereas independent literal plaquette
Hessians and the metric readout give the physical symbol `(A^T;C)` in the
canonical `flat_symbols` convention. Their ranks agree at the diagonal quarter
point, so the former rank-20 check did not detect the error.

For the wrong-placement control the exact range chart, forty real cubic minor
equations and positive resultant remain valid algebra. They do not prove a
physical first-slow lower bound, isolated quarter zero, or stability of such
a bound on varying coframes. The executable and pinned ledger now explicitly
identify this scope.

For the physical symbol, the reduced quarter derivative at
`k=(1,1,0,0)` has rank three and kills the center amplitude `(0,0,1,1)`.
There are continuous physical resonance circles through the quarter point.
The corrected coefficientwise audit, polynomial kernels and maximal minors
are owned by [the physical resonance-circle memo](A4D_IDENTITY_PHYSICAL_RESONANCE_CIRCLES.md).

The valid one-coordinate owners use `(A^T;C)` and their separate circle
`(mu,z,mu,mu)`; this correction does not change their single-direction opening.

Replay of the retained negative control:

```sh
python3 02_REGISTRY/research/certificates/a4d_identity_quarter_firstslow_injectivity_check.py
```

Control terminal: `A4D-IDENTITY-WRONG-PLACEMENT-FIRSTSLOW-CONTROL`.
No task-level closure is claimed.
