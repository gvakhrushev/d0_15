# Cubic continuum Ricci correction and exact scalar stencil

The upstream #334 checker at source commit a76ffeb0680827745558c9c864242303b51a9223 computes the cubic continuum Ricci tensor and a source-forced correction. Replaying it as committed passes its first two fixtures, then exits nonzero on two rotated fixtures because its matrix equality assertions compare unsimplified SymPy expressions structurally.

A locally normalized replay compares every matrix-entry difference after exact SymPy simplification. It passes all four upstream fixtures and an additional symbolic family of arbitrary real orthogonal slopes `A=(p,q)`, `B=kappa*(-q,p)`. It verifies that the cubic Ricci components are removed by the displayed profile corrections and that the central five-point Laplacian yields the same cubic source exactly for every `h`.

This certifies a continuum Ricci jet through total amplitude degree three plus an exact scalar finite-difference identity. It does not certify third-order stationarity of the original 24 Cartan plus 16 coframe finite plaquette equations, a complete finite nonlinear root, or the compulsory native D0 price. The original upstream checker should be fixed at its source before being reported as passing.
