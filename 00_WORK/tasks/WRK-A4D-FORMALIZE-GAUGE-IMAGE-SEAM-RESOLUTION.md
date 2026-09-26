# WRK-A4D-FORMALIZE-GAUGE-IMAGE-SEAM-RESOLUTION

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-formalize-gauge-image-seam-resolution`
Primary artifact: `03_FORMALIZATION/D0/Geometry/A4DGaugeImageResolution.lean`
Execution: `GitHub-first`

## Dependency gate

SATISFIED: #188 gauge-image memory and #193 canonical Grassmann graph-closure resolution are merged.

## Why delegated

The graph-closure carrier has already been selected by merged research #193. What remains here is bounded finite-dimensional formalization of ranges, incidences and quotient dimensions, with a clear firewall against reinterpreting limiting incidence directions as gauge.

## Owned theorem packet

Formalize the intrinsic finite-dimensional seam geometry, keeping three objects distinct:

- endpoint gauge image `U = range D_L`;
- limiting incidence plane `I_*` in the graph-closure carrier;
- lost quotient data `G_* = I_*/U`.

Targets:

- range/inclusion/quotient dimension lemmas;
- flat ranks `rank D0=60`, `dim ker D0=4` only if concretely provable from typed finite data;
- generic rank-64 vs flat rank-60 abstract dimension accounting;
- first-jet image-resolution theorem: a rank-4 transverse first jet determines the limiting four-plane modulo `U`;
- graph-closure statement sufficient to express that higher jets select boundary points rather than create arbitrary external memory.

Research #193 reports exceptional-fibre dimension 293 versus `Gr(4,196)` dimension 768. Do not turn the computational/algebraic-geometric dimension calculation into an axiom; formalize the structural carrier first and record the exact dimension proof as a blocker if mathlib infrastructure is disproportionate.

## Critical non-conflation

`G_*` is resolution data, NOT endpoint gauge. At flat, the true affine gauge remains `range D0`; the intrinsic quotient dimension is 196.

## GitHub execution contract

Run `python tools/task_dispatch.py WRK-A4D-FORMALIZE-GAUGE-IMAGE-SEAM-RESOLUTION`; open Draft PR; no path-history semantics beyond merged #193; zero `sorry`; never self-merge.

## Chat handoff

Return PR, SHA, formalized seam theorem, exact dimensions actually proved in Lean, and the smallest remaining graph-closure blocker.
