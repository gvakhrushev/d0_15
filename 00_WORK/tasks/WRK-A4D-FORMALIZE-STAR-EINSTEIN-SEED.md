# WRK-A4D-FORMALIZE-STAR-EINSTEIN-SEED

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-formalize-star-einstein-seed`
Primary artifact: `03_FORMALIZATION/D0/Geometry/A4DStarEinsteinSeed.lean`
Execution: `GitHub-first`

## Dependency gate

SATISFIED: #201 is merged with green guards.

## Why delegated

#201 is now one of the load-bearing OTO results and should not remain Python-only: after eliminating the auxiliary Lorentz-connection block, the naked star action has exactly the finite Lorentz Einstein ray and no extra spatial ray.

## Owned theorem packet

Formalize as much as is honest from merged #201:

- the finite flat quadratic star response after connection elimination;
- conversion from 16 coframe perturbations to the ten symmetric metric perturbations;
- exact coefficient identity `K_star,metric(k) = (1/4) K_E_eta(k)` across the ten `k_a k_b` coefficients;
- therefore zero coefficient of the independent `E_sp` ray;
- determinant/adjugate homogeneity giving `R=O(X^4 t)`;
- any quadratic residual readout has `Q=O(X^8 t^2)`, hence zero flat 2-jet under the simultaneous flat scaling.

Prefer theorem-level polynomial identities. If the full Schur-complement matrix equality is too large for direct Lean reduction, formalize reusable algebra plus enough exact coefficient lemmas to close the equality; do not assume the Python certificate.

## Boundary

Do NOT formalize `E_eta -> Einstein tensor` here as a finite theorem. The normal-jet identification and Lovelock/Navarro classification remain bridge/research statements with explicit continuum hypotheses.

## GitHub execution contract

Run `python tools/task_dispatch.py WRK-A4D-FORMALIZE-STAR-EINSTEIN-SEED`; open Draft PR; isolate module; zero `sorry`; update `D0.All` only after full build; self-retire before Ready; never self-merge.

## Chat handoff

Return PR, SHA, exact coefficient theorem(s), residual-order theorem(s), build/guard results, and any matrix equality still certified-only.
