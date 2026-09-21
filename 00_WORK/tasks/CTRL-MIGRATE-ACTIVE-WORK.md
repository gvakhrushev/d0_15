# CTRL-MIGRATE-ACTIVE-WORK

## Class
CONTROL

## Objective
Integrate selected unique legacy payloads onto current main without importing stale registry/docs assumptions or obsolete scaffolding.

## Current queue policy
The migration lane is deliberately throttled while the gravity closure lane is being cleaned up.

Current child states:

- `WRK-GRAV-COMPENSATOR-NOETHER` — PLANNED, priority 3 in the worker restart queue.
- `WRK-GEO-CAR-DIRAC-PARITY` — PLANNED / paused.
- `WRK-CERT-ARTIFACT-FRESHNESS` — PLANNED / paused.

The old `WRK-HODGE-SCENE-COCHAIN` payload is no longer an active child; its literal scene Hodge owner was integrated previously.

CONTROL must explicitly promote a PLANNED task before an ordinary worker begins it.

## Rules
1. Reimplement from fresh current main; do not resume unpublished local dirt as canonical state.
2. One worker task should normally be IN_PROGRESS at a time during this cleanup.
3. Every worker stops at REVIEW and waits for CONTROL acceptance.
4. No worker may create additional child tasks or broaden scope.

## Exit condition
Selected reconciliation payloads have been reimplemented or deliberately rejected on current main, with every selected worker reviewed and no unclassified legacy payload remaining in this batch.
