# EXP-ATORUS-CAR-DIRAC-DISPERSION-TRUTH-REPAIR

## Class
EXPENSIVE

## Parent
CTRL-GRAVITY-DYNAMICS-CLOSURE

## Objective

The hopping-versus-difference audit is closed. `carDirac` is `hoppingCarDirac`. `hodgeCarDirac` owns the counting adjoint and fermionic parity. The remaining exit is the exact square and the spectral consequences that depend on it.

Repository edits for that square package belong to `WRK-ATORUS-CAR-HODGE-SQUARE-SHELL`.

## Frozen audit result

MEMO_50 establishes that the current directional owner is A_r = L/2(U_r+U_r^-1), so the spatial Fourier symbol is cosine hopping, not derivative/sine dispersion. Do not assume the advertised square-to-Laplacian relation.

## Required work

1. Derive the exact full 4D and fixed-time 3D Fourier symbols directly from current Lean definitions.
2. Derive the exact square using landed Clifford/CAR relations.
3. Classify actual kernel and lowest positive energies by L mod 4.
4. Audit every current theorem/docstring/claim involving archive_car_dirac_square_owner, carDiracKernelDim, zero modes, Dirac-square/Laplacian statements and spectral-shell claims.
5. Give the minimum truthful reclassification if the current matrix is intentionally a hopping/adjacency Clifford operator.
6. Search for the minimum corrected massless CAR/Hodge Dirac using ArchiveCubicalDifferential, full CAR, forward/backward adjoint structure and ArchiveNaturalTwistedDirac scaffolding if useful.
7. Prefer an all-L construction. A quarter-Brillouin complex twist valid only for special L is a control, not a universal repair.
8. Determine whether a real doubled formulation or complex Hermitian d+d* formulation gives D_corr² = Delta_Hodge exactly while preserving locality, parity and self-adjointness.
9. Only after the operator layer is repaired classify the six-label first shell and E→2π.

## Firewalls

Do not derive Lorentz stress here. Do not select the matter preparation state. Do not import a continuum Dirac operator as the definition.

## Remaining exit

Prove, for the landed `hodgeCarDirac`,

$$
D_H^2=-\sum_r\nabla_r^-\nabla_r^+\otimes I_{16},
$$

then the `L=2` normalization against the graph Laplacian, the kernel, the spatial first shell of rank 96 for `L>=3`, `E_1(L)=2L\sin(\pi/L)`, and `E_1(L)\to 2\pi`.

Do not promote those spectral statements before the square. Do not use `hoppingCarDirac` as the massless owner.

## Deliverable

MEMO_51_ATORUS_CAR_DIRAC_DISPERSION_TRUTH_REPAIR.md
