#!/usr/bin/env python3
"""Deterministic finite algebra cert for typed meson defect transfer."""
from __future__ import annotations

import numpy as np


EDGE_DIM = 4
GEN_DIM = 3
CARRIER_DIM = EDGE_DIM * GEN_DIM


def psd_from_fixture(a: np.ndarray) -> np.ndarray:
    return a.T @ a


def lift_edge(a: np.ndarray) -> np.ndarray:
    return np.kron(a, np.eye(GEN_DIM))


def lift_gen(b: np.ndarray) -> np.ndarray:
    return np.kron(np.eye(EDGE_DIM), b)


def is_psd(a: np.ndarray, tol: float = 1e-10) -> bool:
    eigs = np.linalg.eigvalsh((a + a.T) / 2.0)
    return bool(np.all(eigs >= -tol))


L_M_core = np.diag([400.0, 401.0, 402.0, 403.0])
R_chi = psd_from_fixture(
    np.array(
        [
            [1.0, 0.0, 1.0, 0.0],
            [0.0, 1.0, 0.0, 1.0],
            [1.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 1.0],
        ]
    )
)
R_vsp = psd_from_fixture(
    np.array(
        [
            [2.0, 0.0, 0.0, 1.0],
            [0.0, 1.0, 1.0, 0.0],
            [0.0, 1.0, 2.0, 0.0],
            [1.0, 0.0, 0.0, 1.0],
        ]
    )
)

cycle = np.array(
    [
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ]
)
F_fl = np.eye(GEN_DIM) - cycle
R_fl = F_fl.T @ F_fl

edge_total = L_M_core + R_chi + R_vsp
total = lift_edge(edge_total) + lift_gen(R_fl)

support = np.zeros(CARRIER_DIM)
for edge in (0, 1, 2):
    for gen in (0, 1, 2):
        support[edge * GEN_DIM + gen] = 1.0
Pi_M = np.diag(support)
C_mes = Pi_M @ total @ Pi_M

assert CARRIER_DIM == 12
assert is_psd(L_M_core)
assert is_psd(R_chi)
assert is_psd(R_vsp)
assert is_psd(R_fl)
assert is_psd(lift_edge(edge_total))
assert is_psd(lift_gen(R_fl))
assert np.allclose(Pi_M @ Pi_M, Pi_M)
assert is_psd(C_mes)

# Bare lower-Hodge lift is internally generation-degenerate.
L_lift = lift_edge(L_M_core)
for edge in range(EDGE_DIM):
    diag = [L_lift[edge * GEN_DIM + gen, edge * GEN_DIM + gen] for gen in range(GEN_DIM)]
    assert len(set(np.round(diag, 12))) == 1

# Permutation-only flavour witness has orbit-Laplacian spectrum: split, but no
# nontrivial hierarchy among nonzero orbit modes.
flavour_eigs = np.linalg.eigvalsh(R_fl)
nonzero_flavour_eigs = [x for x in flavour_eigs if x > 1e-10]
assert len(nonzero_flavour_eigs) == 2
assert np.allclose(nonzero_flavour_eigs, [3.0, 3.0])

print("PASS_MESON_DEFECT_TRANSFER_ALGEBRA")
print(f"edge_dim = {EDGE_DIM}")
print(f"generation_dim = {GEN_DIM}")
print(f"carrier_dim = {CARRIER_DIM}")
print("flavour_lift_in_total = PASS")
print("projector_idempotent = PASS")
print("total_psd = PASS")
print("projected_transfer_psd = PASS")
print("lower_hodge_internal_degeneracy = PASS")
print(f"permutation_flavour_eigs = {np.round(flavour_eigs, 12).tolist()}")
