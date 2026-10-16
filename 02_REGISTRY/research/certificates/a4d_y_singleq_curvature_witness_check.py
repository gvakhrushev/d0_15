#!/usr/bin/env python3
"""Exact single-q compatibility and curvature witness for the corrected Y response.

At z=1 and Bloch axis e0, this reconstructs the 10-by-10 corrected response
defect for a phase-independent metric source, checks its order-zero and
order-one connection Fredholm conditions, and verifies a supplied
10-by-10 algebraic Riemann normal-jet witness by exact membership and pairing.

The witness is a finite response pairing.  It is not asserted to satisfy the
full coupled spatial-center/fast-phase-erasure normal-jet system or to extend
to a nonlinear joint-critical branch.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

import a4d_y_curved_normaljet_compatibility_check as C
import a4d_y_curved_response_quotient_check as B

ROOT = Path(__file__).resolve().parents[3]
RESULT_PATH = ROOT / "02_REGISTRY/research/certificates/a4d_y_singleq_curvature_witness_results.json"


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name)


def frobenius(X: sp.Matrix, Y: sp.Matrix) -> sp.Expr:
    return sp.factor(sum(X[i, j] * Y[i, j] for i in range(X.rows) for j in range(X.cols)))


def run(write: bool = False) -> None:
    # The submitted witness in metric-coordinate / derivative-pair order.
    witness = sp.zeros(10)
    witness[4, 7] = witness[7, 4] = -2
    witness[5, 5] = 1

    Hflat, labels, flat_faces = B.action_connection_hessian(sp.Integer(0))
    Nflat = C.dm_kernel_columns(Hflat)
    A1f, _A2f, B0f, B1f, _B2f, _D0f = B.lowcolor_coefficients(
        0, Hflat, flat_faces, labels, 0
    )
    flat_t0 = Nflat.T * B0f
    flat_t1 = Nflat.T * B1f
    check("FLAT_SINGLEQ_T0_T1_COKERNEL_RANK_ZERO",
          C.dm_rank(flat_t0) == 0 and C.dm_rank(flat_t1) == 0)

    H, labels, faces = B.action_connection_hessian(sp.Integer(1))
    N = C.centers(H, labels, 1)
    A1, A2, B0, M1, B2, _D0 = B.lowcolor_coefficients(0, H, faces, labels, 1)
    B1 = -M1
    t0 = N.T * B0
    a0_range = B.bordered_solve(H, N, -B0)
    t1 = N.T * (A1 * a0_range + B1)
    check("CURVED_SINGLEQ_T0_T1_COKERNEL_RANK_ZERO",
          C.dm_rank(t0) == 0 and C.dm_rank(t1) == 0)

    a1_range = B.bordered_solve(H, N, -(A1 * a0_range + B1))
    y1 = B.bordered_solve(H, N, -A1 * N)
    center_t2 = (N.T * (A2 * N + A1 * y1)).applyfunc(sp.factor)
    center = -center_t2.inv() * N.T * (A1 * a1_range + A2 * a0_range + B2)
    a0 = a0_range + N * center
    a1 = a1_range + y1 * center
    order2_rhs = A1 * a1 + A2 * a0 + B2
    check("CURVED_SINGLEQ_ORDER2_FREDHOLM",
          N.T * order2_rhs == sp.zeros(2, 10))
    _a2_range = B.bordered_solve(H, N, -order2_rhs)

    q12 = C.SYM.index((1, 2))
    center_q12 = [sp.factor(center[i, q12]) for i in range(2)]
    check("Q12_CENTER_AMPLITUDE", center_q12 == [-sp.Rational(3311, 3750), 0])

    # Exact corrected second-order response formula from the phase-corrected
    # low-color Schur calculation, normalized per phase and compared to 1/2 G.
    response = sp.zeros(10)
    for i in range(10):
        for j in range(10):
            ai, aj = a0[:, i], a0[:, j]
            bi, bj = a1[:, i], a1[:, j]
            value = (
                (ai.T * A1 * bj + aj.T * A1 * bi) / 2
                + ai.T * A2 * aj
                + ai.T * B2[:, j]
                + aj.T * B2[:, i]
                - (B1[:, i].T * bj + B1[:, j].T * bi) / 2
            )[0]
            response[i, j] = sp.factor(value / 4)
    einstein = C.einstein_k([1, 0, 0, 0]) / 2
    defect = (response - einstein).applyfunc(sp.factor)
    defect_rank = C.dm_rank(defect)
    defect_q12 = sp.factor(defect[q12, q12])
    check("SINGLEQ_DEFECT_RANK6_AND_Q12",
          defect_rank == 6 and defect_q12 == -sp.Rational(34163, 118125))

    # Verify that the 10x10 witness is an actual algebraic Riemann normal jet.
    jet_maps, riemann_basis, _riemann_coordinates = C.riemann_basis()
    jet_matrix = sp.Matrix.vstack(*[jet_maps[pair] for pair in C.DIRPAIRS])
    jet_vector = sp.Matrix([witness[i, j] for j in range(10) for i in range(10)])
    jet_image_rank = C.dm_rank(jet_matrix)
    jet_augmented_rank = C.dm_rank(jet_matrix.row_join(jet_vector))
    check("WITNESS_IS_ALGEBRAIC_RIEMANN_JET",
          len(riemann_basis) == 20 and jet_image_rank == 20
          and jet_augmented_rank == jet_image_rank)
    witness_pairing = frobenius(defect, witness)
    check("WITNESS_PAIRING_NONZERO", witness_pairing == -sp.Rational(27247, 17500))

    # The number of nonzero pairings is tied to this explicitly generated
    # rational nullspace basis; the concrete witness matrix is basis-free.
    basis_pairings = []
    for riemann_index in range(20):
        jet = sp.Matrix.hstack(*[
            jet_maps[pair][:, riemann_index] for pair in C.DIRPAIRS
        ])
        basis_pairings.append(frobenius(defect, jet))
    nonzero_basis_pairings = sum(value != 0 for value in basis_pairings)
    check("SIX_NONZERO_PAIRINGS_IN_PINNED_RIEMANN_BASIS",
          nonzero_basis_pairings == 6)

    result = {
        "schema": "a4d-y-singleq-curvature-witness-v1",
        "terminal": "A4D-Y-SINGLEQ-CURVATURE-WITNESS-CERTIFIED",
        "scope": "exact finite corrected response at z=1 on the phase-independent source; a valid algebraic Riemann jet has nonzero pairing, but full curved-background compatibility and nonlinear continuation are not established",
        "conventions": {
            "axis": "e0",
            "mixed_phase": "connection RHS lambda^(-1), metric readout lambda^(+1)",
            "metric_coordinate_order": [f"q{a}{b}" for a, b in C.SYM],
            "witness_jet_columns": [str(pair) for pair in C.DIRPAIRS],
            "witness_jet_rows": [f"q{a}{b}" for a, b in C.SYM],
            "pairing": "Frobenius pairing of the corrected 10x10 single-q defect with the 10x10 normal-jet matrix",
        },
        "single_q": {
            "flat_t0_cokernel_rank": C.dm_rank(flat_t0),
            "flat_t1_cokernel_rank": C.dm_rank(flat_t1),
            "curved_t0_cokernel_rank": C.dm_rank(t0),
            "curved_t1_cokernel_rank": C.dm_rank(t1),
            "center_amplitude_q12": [str(value) for value in center_q12],
            "defect_rank": defect_rank,
            "defect_q12": str(defect_q12),
        },
        "curvature_witness": {
            "riemann_space_dimension": len(riemann_basis),
            "jet_map_rank": jet_image_rank,
            "witness_in_jet_map_image": True,
            "normal_jet_matrix": C.matrix_json(witness),
            "pairing": str(witness_pairing),
            "nonzero_pairings_on_pinned_basis_generators": nonzero_basis_pairings,
            "basis_generator_pairings": [str(value) for value in basis_pairings],
        },
        "nonclaims": [
            "this witness is not shown to satisfy the full spatial-center and fast-phase-erasure normal-jet system",
            "the full compatible curvature normal-jet certificate still has an Einstein response on its surviving direction",
            "no nonlinear joint-critical curved-background branch or refinement-uniform o(h^2) estimate is proved",
        ],
    }

    if write:
        RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n")
        print("WROTE", RESULT_PATH)
    else:
        check("RESULTS_MATCH_PINNED_JSON", result == json.loads(RESULT_PATH.read_text()))
    print("SINGLEQ_DEFECT_Q12", defect_q12)
    print("WITNESS_PAIRING", witness_pairing)
    print("NONZERO_BASIS_PAIRINGS", nonzero_basis_pairings)
    print("TERMINAL", result["terminal"])


if __name__ == "__main__":
    run(write="--write" in __import__("sys").argv)
