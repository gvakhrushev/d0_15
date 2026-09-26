# WRK-A4D-FORMALIZE-JOINT-HOLONOMY-RESIDUAL

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

Repository: `gvakhrushev/d0_15`
Base: `main`
Branch: `wrk/a4d-formalize-joint-holonomy-residual`
Primary artifact: `03_FORMALIZATION/D0/Geometry/A4DJointHolonomyResidual.lean`
Execution: `GitHub-first`

## Dependency gate

SATISFIED: #185 and the clean quotient-completeness result #196 are merged.

## Owned theorem packet

Start from
`R_2|1 = det(I-P1) t2 - (I-P2) adj(I-P1) t1`.

Targets:

- polynomial definition with no inverse/reference section;
- full affine conjugation covariance `R' = g R`;
- Lorentz quadratic invariance and the reviewed reversal identities;
- exact flat-holonomy vanishing;
- relation between two-loop residual components and the corresponding Plucker minors;
- abstract linear-algebra theorem: if `J D=0`, `rank D=4`, `rank J=12` in a 16-dimensional sector, then `ker J = range D`;
- a small typed nongauge witness if current finite carrier infrastructure supports it.

#196 certifies sector rank 12 and global rank 192 on declared generic homogeneous L=2 controls. Do NOT encode those Python ranks as axioms. Either prove the concrete ranks in Lean or leave the concrete completeness instantiation as an explicit blocker while formalizing the structural theorem.

## Scope

No global nonlinear quotient-completeness claim. No Einstein/torsion-free interpretation.

## GitHub execution contract

Run `python tools/task_dispatch.py WRK-A4D-FORMALIZE-JOINT-HOLONOMY-RESIDUAL`; open Draft PR; isolated module; zero `sorry`; narrow build first; self-retire only after stable build; never self-merge.

## Chat handoff

Return PR, SHA, theorem names, whether concrete rank-12/192 was proved or left certified-only, and validation results.
