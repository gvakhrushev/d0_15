#!/usr/bin/env python3
"""CAR relations certificate on the 16-state fermionic Fock space.

Verifies exact Canonical Anticommutation Relations (CAR) for 4 modes:
  {c_r, c_s} = 0
  {c_r†, c_s†} = 0
  {c_r, c_s†} = δ_rs I_16.

Includes reachable negative controls mutating the Jordan-Wigner phase convention.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROLES = [0, 1, 2, 3]  # A, B, C, D
N_MODES = 4
FOCK_DIM = 1 << N_MODES  # 16


def jw_phase(state: int, role: int) -> int:
    mask = (1 << role) - 1
    occupied_before = bin(state & mask).count("1")
    return -1 if occupied_before % 2 == 1 else 1


def construct_annihilation_matrix(role: int, mutate_sign: bool = False) -> list[list[int]]:
    mat = [[0] * FOCK_DIM for _ in range(FOCK_DIM)]
    for ket in range(FOCK_DIM):
        if (ket >> role) & 1:  # role is occupied
            bra = ket ^ (1 << role)
            phase = jw_phase(ket, role)
            if mutate_sign and role == 1 and (ket & 1):
                phase = -phase  # selective mutation breaks Jordan-Wigner grading
            mat[bra][ket] = phase
    return mat


def transpose(mat: list[list[int]]) -> list[list[int]]:
    dim = len(mat)
    return [[mat[j][i] for j in range(dim)] for i in range(dim)]


def mat_mul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    dim = len(a)
    res = [[0] * dim for _ in range(dim)]
    for i in range(dim):
        for k in range(dim):
            if a[i][k] != 0:
                for j in range(dim):
                    res[i][j] += a[i][k] * b[k][j]
    return res


def mat_add(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    dim = len(a)
    return [[a[i][j] + b[i][j] for j in range(dim)] for i in range(dim)]


def is_zero_matrix(mat: list[list[int]]) -> bool:
    return all(all(val == 0 for val in row) for row in mat)


def is_identity_matrix(mat: list[list[int]]) -> bool:
    dim = len(mat)
    for i in range(dim):
        for j in range(dim):
            expected = 1 if i == j else 0
            if mat[i][j] != expected:
                return False
    return True


def check_car_system(mutate: bool = False) -> tuple[bool, bool, bool]:
    c = [construct_annihilation_matrix(r, mutate_sign=mutate) for r in ROLES]
    c_dag = [transpose(c[r]) for r in ROLES]

    all_cc_zero = True
    all_cdag_cdag_zero = True
    all_anticomm_delta = True

    for r in ROLES:
        for s in ROLES:
            # {c_r, c_s}
            anti_cc = mat_add(mat_mul(c[r], c[s]), mat_mul(c[s], c[r]))
            if not is_zero_matrix(anti_cc):
                all_cc_zero = False

            # {c_r†, c_s†}
            anti_dag = mat_add(mat_mul(c_dag[r], c_dag[s]), mat_mul(c_dag[s], c_dag[r]))
            if not is_zero_matrix(anti_dag):
                all_cdag_cdag_zero = False

            # {c_r, c_s†}
            anti_mixed = mat_add(mat_mul(c[r], c_dag[s]), mat_mul(c_dag[s], c[r]))
            if r == s:
                if not is_identity_matrix(anti_mixed):
                    all_anticomm_delta = False
            else:
                if not is_zero_matrix(anti_mixed):
                    all_anticomm_delta = False

    return all_cc_zero, all_cdag_cdag_zero, all_anticomm_delta


def main() -> int:
    canonical_cc, canonical_cdag, canonical_mixed = check_car_system(mutate=False)
    mutated_cc, mutated_cdag, mutated_mixed = check_car_system(mutate=True)

    checks = {
        "fock_carrier_dimension_16": FOCK_DIM == 16,
        "canonical_cc_zero": canonical_cc,
        "canonical_cdag_cdag_zero": canonical_cdag,
        "canonical_mixed_kronecker_identity": canonical_mixed,
        "negative_mutated_sign_fails": not (mutated_cc and mutated_cdag and mutated_mixed),
    }

    payload = {
        "status": "PASS_ARCHIVE_CAR_RELATIONS" if all(checks.values()) else "FAIL_ARCHIVE_CAR_RELATIONS",
        "carrier_source": "D0.Geometry.ArchiveCARFockCarrier.ArchiveFockState",
        "operator_source": "D0.Geometry.ArchiveCARRelations",
        "fock_dimension": FOCK_DIM,
        "num_modes": N_MODES,
        "checks": checks,
    }

    print("operator_source: D0.Geometry.ArchiveCARRelations")
    print("carrier_source: D0.Geometry.ArchiveCARFockCarrier.ArchiveFockState")
    print(payload["status"])
    print(json.dumps(payload, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
