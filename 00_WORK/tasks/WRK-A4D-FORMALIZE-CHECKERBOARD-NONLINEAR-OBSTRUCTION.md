# WRK-A4D-FORMALIZE-CHECKERBOARD-NONLINEAR-OBSTRUCTION

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-formalize-checkerboard-nonlinear-obstruction`
Primary artifact: `03_FORMALIZATION/D0/Geometry/A4DCheckerboardNonlinearObstruction.lean`
Execution: `GitHub-first`

## Dependency gate

SATISFIED: the exact packet from historical #187 was salvaged/reviewed into merged #199/#200.

## Why delegated

The nonlinear obstruction is now a stable exact finite theorem from merged #199/#200. Its real-quadratic core is suitable for Lean, while formalization is useful precisely because the result must remain scoped to the three L=2 checkerboard sectors and must not drift into a wave interpretation.

## Owned theorem packet

For each of the three nonzero Lorentz-null L=2 checkerboard sectors, after quotienting the ten accepted flat gauge directions, the two-dimensional physical null plane has exact obstruction form

`T(a u + b v, a u + b v, w0) = -(32/3)(a^2+b^2)`.

Formalize the finite algebra needed to conclude this vanishes over the reals iff `a=b=0`. If the full 40-variable cubic coefficient reconstruction is too expensive, formalize a typed exact basis/witness and make the remaining enumeration explicit rather than axiomatic.

## Scope

This is local near the canonical flat solder and finite L=2. It does not exclude disconnected curved stationary points; #202 is actively searching such a sector. Do not call these modes waves or physical time.

## GitHub execution contract

Run `python tools/task_dispatch.py WRK-A4D-FORMALIZE-CHECKERBOARD-NONLINEAR-OBSTRUCTION`; open Draft PR; isolated module; zero `sorry`; never self-merge.

## Chat handoff

Return PR, SHA, exact obstruction theorem scope, validation results, and any finite enumeration left outside Lean.
