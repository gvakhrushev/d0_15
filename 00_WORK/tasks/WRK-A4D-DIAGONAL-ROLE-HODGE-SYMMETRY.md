# WRK-A4D-DIAGONAL-ROLE-HODGE-SYMMETRY

## Class

WORKER

## Parent

CTRL-GRAVITY-DYNAMICS-CLOSURE

## State

IN_PROGRESS

## Objective

Own the diagonal Role permutation on `ArchiveRolePhaseGroup N × ArchiveFockState`, the equivariance of `D_H` and `D_H²`, the fermion-number commutators, and the Role-A stabilizer action on the spatial first shell.

## Owned in this landing

* Site action `(σ · x)(r) = x(σ⁻¹ r)`, with `σ · (x + e_r) = (σ · x) + e_{σ r}`.
* Diagonal transport combines that pullback with the owned signed Fock matrix. It is a linear equivalence, preserves the counting pairing, and commutes with `d`, `d†`, `D_H`, and `D_H²`.
* Fock-only transport, which leaves the site fixed, does not commute with `D_H`.
* Fermion number satisfies `[N, d] = d`, `[N, d†] = -d†`, and `[N, D_H] = d - d†`. A concrete witness shows the first-order commutator is nonzero. Number commutes with `D_H²`.
* Parity anticommutes with `D_H` and commutes with `D_H²`.
* The stabilizer `σ(A) = A` preserves the A-invariant sector and the rank-96 shell. A swap that moves `A` need not preserve the A-invariant sector.
* For `archiveFibers N ≥ 3`, `D_H²` restricted to `spatialShellSubmodule` is `shellEnergy²` times the identity. The `L = 2` rank-48 degeneration is unchanged.
* The same diagonal action also commutes with `hoppingCarDirac`. The operators remain distinct through their squares.
* `spatialShellHodgeSquareCompression` is not the BOOK finite feedback operator.

## Still open

* A site-independent fibre commutant of `D_H` is not classified here.
* No identification of the shell compression with `P_N U_N† Q_N U_N P_N` is claimed.
