# WRK-GRAV-COMPENSATOR-NOETHER

## Class
WORKER

## Priority
**3 — PLANNED. Do not execute until CONTROL promotes it after the source-stratification and C1 integration sequence.**

## Parent
CTRL-MIGRATE-ACTIVE-WORK

## Repository
https://github.com/gvakhrushev/d0_15

Preferred future branch:
```text
work/grav-compensator-noether
```

Always branch from the then-current `origin/main`; there is no published worker branch to resume.

## Objective
Reimplement the accepted A1 compensator construction as a clean generic Lean owner for its actual Weyl/Stueckelberg Ward statements.

## Required source
Read literally:

- `02_REGISTRY/frontier/A1_COMPENSATOR_NOETHER_RESULT.md`
- `02_REGISTRY/RESEARCH_LEDGER.md`
- current `D0-HODGE-LINKS-001` note

Do not rely on a local-only 888-line payload unless every imported dependency is already present on current main.

## Required theorem package
Keep the work bounded to:

1. unsigned shift/divergence adjointness;
2. finite compensator shift invariance;
3. Euler edge/diagonal response;
4. off-shell Ward identity;
5. supported compensator elimination / projected response `BPlus G_phys = 0`;
6. positivity no-go if it is already part of the accepted result and remains short.

Do not try to derive the Hodge kinetic operator, quadratic matter source, TT readout or continuum Einstein bridge here.

## Current research boundary
A-X already classified the reduced A1 Hessian as contact/constraint stiffness, not spatial propagation.

A-CPL classified `W=I` as conditional until the actual A1 conformal weight is typed/selected.

Therefore this worker must **not**:
- claim A1 supplies Q_H;
- claim the physical weight is already forced to unity;
- identify the Ward operator with signed incidence/Bianchi;
- claim a matter→tensor source has been constructed.

## Semantic firewall
`BPlus` = unsigned Weyl/Ward endpoint-sum operator.

`BMinus` = signed Hodge/current divergence.

They are distinct. The C1 worker owns their carrier relation; this worker owns only the A1 variational/Ward side.

## Gates
Use a fresh current-main branch. Require clean `lake build D0.All`, all repository/work validators, zero `sorry`, and green GitHub CI before REVIEW.

## Exit condition
Current main owns the finite compensator gauge invariance, Euler response, Ward identity and supported projected-response theorem for the unsigned A1 operator, with no Bianchi/Einstein/Hodge overclaim.
