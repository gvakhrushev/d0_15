# WRK-A4D-FORMALIZE-RESOLVED-ENERGY-VARIATION

Class: `WORKER`  
State on registration: `PLANNED`  
Parent: `CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE`

## Dependency gate

Requires merged #189 and the stable resolved-carrier contract.

## Objective

Formalize the resolved quadratic quotient energy and its first variation.

Primary module:
`03_FORMALIZATION/D0/Geometry/A4DResolvedAffineEnergy.lean`.

Targets:

- observer-positive inner product on edge cochains;
- orthogonal projection onto a supplied finite-dimensional incidence subspace;
- `E_I(b)=dist(b,I)^2`;
- zero-locus theorem `E_I=0 ↔ b∈I`;
- frame/full-affine invariance under transported `I`;
- projector/Grassmannian derivative under the selected constrained contract;
- separating-variation theorem sufficient to establish independence of the
  star and resolved-energy Euler channels if the research hypotheses are
  exactly met.

Do not formalize `d_P=2` until the physical quotient task proves it.
