# Stored-adjoint metric projection certificate

This packet replays the bounded exact result in
[`A4D_STORED_METRIC_PROJECTION_AND_SOURCE_COMPLETION.md`](../../A4D_STORED_METRIC_PROJECTION_AND_SOURCE_COMPLETION.md).
It proves the local regular kinematic image of the full stored-adjoint class,
its five linearized metric constraints on a full-support Fourier mode, and the
generic Bianchi-compatible conormal residual with its fixed-background
separating row.

Run from the repository root with Python 3.10+ and SymPy 1.14.0:

```sh
python3 02_REGISTRY/research/sources/d0_stored_metric_projection_2026-10-17/check_metric_projection.py
```

`RESULT.json` is the deterministic replay output. The checker pins the literal
full-CAR and Lean definitions plus the joint-chart and source-consumer texts.
Its exact checks include
a nonconstant rational own-edge fixture, full16 exterior intertwiners,
moving-observer restoration, source pairings with both off-diagonal entries,
a non-null linearized Einstein realization, and exceptional `Qk` controls.

The result is kinematic and source-geometric. It does not establish physical
admission, a selected source law, a stationary curved root, refinement,
soundness/recovery, or GR closure. The proposed completion row is forbidden
by the current stored metric tangent, so it names an obligation rather than
installing a new variation or detector.
