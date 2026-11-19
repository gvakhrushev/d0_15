#!/usr/bin/env python3
"""Exact phase-resolved compatible-source response at the curved Y vacuum.

This certificate refines the four-phase, e0 response at z=1 from a common
10-component metric source to a 40-component site-resolved source.  It forms
the zero- and first-order Fredholm conditions, restricts the source to their
common kernel, and computes the second-order averaged metric response there.

All arithmetic is rational.  The extension of the response defect from the
compatible subspace to R^40 is explicitly the Euclidean orthogonal projection
onto that subspace; this convention is recorded because the physical
stationary response is only defined on compatible sources.

This is a finite normal-jet calculation.  It does not prove a nonlinear
stationary branch or a refinement-uniform remainder estimate.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

import a4d_y_curved_normaljet_compatibility_check as C
import a4d_y_curved_response_quotient_check as B

ROOT = Path(__file__).resolve().parents[3]
RESULT_PATH = ROOT / "02_REGISTRY/research/certificates/a4d_y_phase_resolved_compatible_response_results.json"


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name)


def run(write: bool = False) -> None:
    H, labels, faces0 = B.action_connection_hessian(sp.Integer(1))
    faces = C.with_base_phases(faces0)
    N = C.centers(H, labels, 1)
    A1, A2, _M0, _M1, _M2, C0, C1, C2, Dphase = C.blocks_all(H, faces, labels)

    # The metric source has one ten-vector per fast phase.  The connection
    # RHS carries lambda^{-1}; the metric readout carries lambda^{+1}.
    B0 = C0.T
    B1 = -C1[0].T
    B2 = C2[(0, 0)].T
    A = A1[0]
    A2e0 = A2[(0, 0)]

    T0 = N.T * B0
    T0_rank = C.dm_rank(T0)
    K0 = C.dm_kernel_columns(T0)
    check("T0_RANK1_KERNEL39", T0_rank == 1 and K0.cols == 39)

    # For sources outside ker(T0), project away the exact cokernel component
    # before taking the canonical range solution.  On K0 this does nothing.
    range_projector = sp.eye(96) - N * (N.T * N).inv() * N.T
    a0_all = B.bordered_solve(H, N, -range_projector * B0)
    check("RANGE_PROJECTOR_REMOVES_T0_COKERNEL",
          N.T * (range_projector * B0) == sp.zeros(2, 40)
          and H * a0_all + range_projector * B0 == sp.zeros(96, 40))

    T1 = N.T * (A * a0_all + B1)
    T1_on_K0 = T1 * K0
    T1_rank = C.dm_rank(T1_on_K0)
    K1 = C.dm_kernel_columns(T1_on_K0)
    K = K0 * K1
    check("T1_RANK2_COMPATIBLE_DIM37", T1_rank == 2 and K.cols == 37)
    check("BOTH_FREDHOLM_CONDITIONS", T0 * K == sp.zeros(2, 37)
          and T1 * K == sp.zeros(2, 37))

    # Exact range and center solve through order t^2 on the compatible class.
    a0_range = B.bordered_solve(H, N, -B0 * K)
    a1_range = B.bordered_solve(H, N, -(A * a0_range + B1 * K))
    y1 = B.bordered_solve(H, N, -A * N)
    center_t2 = (N.T * (A2e0 * N + A * y1)).applyfunc(sp.factor)
    check("CENTER_T2_NONDEGENERATE", center_t2.det() != 0)
    center = -center_t2.inv() * N.T * (A * a1_range + A2e0 * a0_range + B2 * K)
    a0 = a0_range + N * center
    a1 = a1_range + y1 * center
    order2_forcing = A * a1 + A2e0 * a0 + B2 * K
    check("ORDER2_FREDHOLM", N.T * order2_forcing == sp.zeros(2, 37))
    a2_range = B.bordered_solve(H, N, -order2_forcing)
    check("ORDER2_RANGE_SOLVE", H * a2_range + order2_forcing == sp.zeros(96, 37))

    # Average the phase-resolved metric readout to one ten-component response.
    average = sp.zeros(10, 40)
    for phase in range(4):
        average[:, 10 * phase:10 * (phase + 1)] = sp.eye(10) / 4
    response_t1 = (average * (C0 * a1 + C1[0] * a0)).applyfunc(sp.factor)
    response_t2 = (average * (
        Dphase * K + C0 * a2_range + C1[0] * a1 + C2[(0, 0)] * a0
    )).applyfunc(sp.factor)

    einstein = C.einstein_k([1, 0, 0, 0]) / 2
    defect_on_K = (response_t2 - einstein * average * K).applyfunc(sp.factor)
    defect_rank = C.dm_rank(defect_on_K)
    check("T2_DEFECT_RANK8_ON_COMPATIBLE_CLASS", defect_rank == 8)

    # Extend by zero on K^perp, making the reported 10x40 matrix canonical.
    projection_K = (K * (K.T * K).inv() * K.T).applyfunc(sp.factor)
    defect_full = (defect_on_K * (K.T * K).inv() * K.T).applyfunc(sp.factor)
    full_rank = C.dm_rank(defect_full)
    full_kernel_dim = 40 - full_rank
    check("ORTHOGONAL_EXTENSION_10_BY_40_RANK8_KERNEL32",
          defect_full.shape == (10, 40) and full_rank == 8 and full_kernel_dim == 32
          and defect_full * (sp.eye(40) - projection_K) == sp.zeros(10, 40))

    # The smooth, phase-independent source is a ten-dimensional subspace of K.
    common_source = sp.zeros(40, 10)
    for phase in range(4):
        common_source[10 * phase:10 * (phase + 1), :] = sp.eye(10)
    common_coordinates, params = K.gauss_jordan_solve(common_source)
    check("COMMON_SOURCE_LIES_IN_COMPATIBLE_CLASS", params.rows == 0
          and K * common_coordinates == common_source)
    single_defect = (defect_on_K * common_coordinates).applyfunc(sp.factor)
    single_rank = C.dm_rank(single_defect)
    q12 = C.SYM.index((1, 2))
    q12_defect = sp.factor(single_defect[q12, q12])
    check("SINGLE_SOURCE_RANK6_Q12_REGRESSION",
          single_rank == 6 and q12_defect == -sp.Rational(34163, 118125))
    check("AVERAGED_T1_VANISHES_ON_SMOOTH_SOURCE",
          response_t1 * common_coordinates == sp.zeros(10, 10))

    result = {
        "schema": "a4d-y-phase-resolved-compatible-response-v1",
        "terminal": "A4D-Y-PHASE-RESOLVED-COMPATIBLE-RESPONSE-CERTIFIED",
        "scope": "exact rational finite normal-jet response at z=1 on the t0/t1-compatible source subspace; nonlinear continuation and refinement-uniform remainder remain open",
        "conventions": {
            "axis": "e0",
            "source_space": "R^40, ten metric coordinates on each of four fast phases",
            "connection_rhs": "lambda^(-1)",
            "metric_readout": "lambda^(+1)",
            "full_map_extension": "Euclidean orthogonal projection onto the t0/t1-compatible source subspace, then zero on its orthogonal complement",
        },
        "compatibility": {
            "t0_cokernel_rank": T0_rank,
            "t0_kernel_dimension": K0.cols,
            "t1_cokernel_rank_on_t0_kernel": T1_rank,
            "compatible_dimension": K.cols,
        },
        "response": {
            "t1_average_zero_on_full_compatible_class": response_t1 == sp.zeros(10, 37),
            "t1_average_rank_on_full_compatible_class": C.dm_rank(response_t1),
            "t2_defect_rank_on_compatible_class": defect_rank,
            "t2_defect_map_shape": list(defect_full.shape),
            "t2_defect_map_rank": full_rank,
            "t2_defect_map_kernel_dimension": full_kernel_dim,
            "single_smooth_source_defect_rank": single_rank,
            "single_smooth_source_q12_defect": str(q12_defect),
            "center_t2": C.matrix_json(center_t2),
        },
        "nonclaims": [
            "the finite compatible-class defect does not establish a nonlinear joint-critical branch",
            "no refinement-uniform o(h^2) estimate is proved",
            "the submitted scalar 2626083/44800 is not identified by this source convention and is not adopted",
        ],
    }

    if write:
        RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n")
        print("WROTE", RESULT_PATH)
    else:
        check("RESULTS_MATCH_PINNED_JSON", result == json.loads(RESULT_PATH.read_text()))
    print("COMPATIBLE_DIMENSION", K.cols)
    print("T1_AVERAGE_RANK_ON_COMPATIBLE_CLASS", result["response"]["t1_average_rank_on_full_compatible_class"])
    print("T2_DEFECT_RANK", defect_rank)
    print("SINGLE_Q12_DEFECT", q12_defect)
    print("TERMINAL", result["terminal"])


if __name__ == "__main__":
    run(write="--write" in __import__("sys").argv)
