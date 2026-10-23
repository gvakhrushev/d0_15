"""Full-spectrum numerical restrictions for q2000 and q1100.

Only inactive-role creator jets are used: all four components on roles
1,2,3 at q2000 (12 coordinates), and roles2,3 at q1100 (8 coordinates).
These are actual admissible affine native leg families with identity links:
each varied leg is independent of its own spatial coordinate. They lie in
ker T because every occupied-to-occupied transfer has those role phases1.

COMPLETENESS modulo six representation directions requires the separate
exact rank-T theorem (expected ranks3 and5); it is not inferred from these
spectra. The restriction retains ALL4096 momenta, ALL16 exterior components,
shell/reference128, the full heat normalizer, feedback, and the indefinite
off-shell resolvent including the ground state. No old run(), root search,
receipt or proof document is executed/changed. Output is stdout only.
"""
from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import time

import numpy as np
import sympy as s


ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
L, FOCK, REFERENCE = 8, 16, 128
SECTORS = (((2, 0, 0, 0), (1, 2, 3), 3),
           ((1, 1, 0, 0), (2, 3), 5))


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("full_shell_transfer_diagnostic:"+label)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _numeric(matrix):
    return np.array(matrix.evalf(18).tolist(), dtype=np.complex128)


def _sector(q, inactive, expected_rank, *, definition, operator, features,
            modes, index, tk, D, creators, creators_s, legs_s, root,
            return_data=False):
    outgoing = np.array([index[tuple((k[r]+q[r]) % L for r in range(4))]
                         for k in modes])
    # This consumes definitions only, not definition.run() or a q3300 run.
    spectral = definition._spectral_data(features, outgoing, root)
    lam, rho, r = spectral["lambda"], spectral["rho"], spectral["resolvent"]
    chi = rho+spectral["kappa"]
    require(np.max(np.abs(np.einsum("kij,kjl->kil", D, D)
                          -lam[:, None, None]*np.eye(FOCK))) < 3e-11,
            "all_mode_CAR_squares_match_exact_feature_energies")
    roles = np.repeat(inactive, 4)
    components = np.tile(np.arange(4), len(inactive))
    count = len(roles)
    require(all(q[r] == 0 for r in inactive), "actual_inactive_role_constraint")

    # Independent literal stored API control, on every retained field slot.
    k_control = (1, 2, 3, 5)
    l_control = tuple((k_control[r]+q[r]) % L for r in range(4))
    tc = tk[index[k_control]]
    for rr, jj in zip(roles, components):
        column = s.zeros(31, 1)
        column[4*int(rr)+int(jj)] = 1
        literal = _numeric(operator.first_jet(column, legs_s, k_control, l_control, creators_s))
        compiled = L*((tc[rr]-1)*creators[jj]
                      +(tc[rr].conjugate()-1)*creators[jj].T)
        require(np.max(np.abs(literal-compiled)) < 1e-12,
                "literal_ordered_first_jet_agrees_on_each_inactive_leg_slot")

    weight_J = chi+chi[outgoing]
    weight_X = spectral["dd"]-rho*r[outgoing]-rho[outgoing]*r
    H_J, H_X = np.zeros((count, count), complex), np.zeros((count, count), complex)
    shell = rho > 0
    shell_edges = np.flatnonzero(shell & shell[outgoing])
    require(len(shell_edges) == (1 if q[0] == 2 else 2),
            "complete_actual_occupied_to_occupied_edge_count")
    shell_X_max = 0.0
    for offset in range(0, len(modes), 128):
        sl = slice(offset, offset+128)
        z = (tk[sl][:, roles]-1).T
        J = L*(z[:, :, None, None]*creators[components, None, :, :]
               +z.conj()[:, :, None, None]*creators[components, None, :, :].transpose(0, 1, 3, 2))
        X = (np.einsum("kij,akjl->akil", D[outgoing[sl]], J)
             +np.einsum("akij,kjl->akil", J, D[sl]))
        positions = shell_edges[(shell_edges >= offset) & (shell_edges < offset+128)]-offset
        if len(positions):
            shell_X_max = max(shell_X_max, float(np.max(np.abs(X[:, positions]))))
        jf, xf = J.reshape(count, -1, 256), X.reshape(count, -1, 256)
        H_J += np.einsum("akn,bkn,k->ab", jf.conj(), jf, weight_J[sl])
        H_X += np.einsum("akn,bkn,k->ab", xf.conj(), xf, weight_X[sl])
    require(shell_X_max == 0.0, "all_occupied_to_occupied_X_blocks_zero_T_compatibility")
    H = H_J+H_X
    Hermitian_error = float(np.linalg.norm(H-H.conj().T)/max(1, np.linalg.norm(H)))
    require(Hermitian_error < 3e-12, "full_restricted_Hermitian_matrix")
    H = (H+H.conj().T)/2
    eigenvalues = np.linalg.eigvalsh(H)
    tolerance = 1e-9*max(1.0, float(np.max(np.abs(eigenvalues))))
    inertia = {"positive": int(np.sum(eigenvalues > tolerance)),
               "negative": int(np.sum(eigenvalues < -tolerance)),
               "unresolved_at_diagnostic_tolerance": int(np.sum(np.abs(eigenvalues) <= tolerance))}
    result = {"q": list(q), "inactive_roles": list(inactive),
            "field_slots_role_component": [[int(r), int(j)] for r, j in zip(roles, components)],
            "restriction_dimension": count,
            "full4096_momenta": len(modes), "all16_exterior_components": FOCK,
            "full_reference_dimension": REFERENCE,
            "full_Z": spectral["Z"], "shell_epsilon": spectral["epsilon"],
            "ground_resolvent_negative_retained": float(spectral["resolvent"][0]),
            "exact_energy_feature_groups": spectral["unique_features"],
            "exact_equal_energy_directed_edges": spectral["equal_edges"],
            "minimum_distinct_energy_gap": spectral["minimum_distinct_gap"],
            "occupied_to_occupied_directed_edges": len(shell_edges),
            "all_occupied_X_blocks_max": shell_X_max,
            "Hermitian_relative_error": Hermitian_error,
            "restricted_eigenvalues_native_leg_coefficient_norm": eigenvalues.tolist(),
            "diagnostic_signature": inertia, "diagnostic_eigenvalue_tolerance": tolerance,
            "direct_Y_Frobenius_norm": float(np.linalg.norm(H_J)),
            "spectral_and_matter_Schur_Frobenius_norm": float(np.linalg.norm(H_X)),
            "separate_exact_rank_T_needed_for_quotient_completeness": expected_rank,
            "rank_T_proven_here": False, "complete_joint_kernel_certified": False}
    return (result, {"H": H}) if return_data else result


def run(repo=None, *, return_data=False):
    start = time.perf_counter()
    repo = ROOT if repo is None else Path(repo).resolve()
    definition_path = HERE/"full_symbol_diagnostic.py"
    ordered_path = HERE/"ordered_operator_check.py"
    definition = _load(definition_path, "shell_transfer_scalar_definitions")
    operator = _load(ordered_path, "shell_transfer_ordered_operator")
    chart = operator.chart_helper()
    chart.owned_definitions(repo)  # actual stable pins, no owner run().
    receipt = json.loads((repo/chart.RECEIPT).read_text())
    root = receipt["interval"]["root_center"]
    features_of = definition.exact_features(repo)
    modes = tuple(itertools.product(range(L), repeat=4))
    index = {mode: i for i, mode in enumerate(modes)}
    features = tuple(features_of(k) for k in modes)
    creators_s, exterior_order = operator.owned_car(repo)
    creators = np.array([_numeric(C) for C in creators_s])
    first_outgoing = np.array([index[tuple((k[r]+SECTORS[0][0][r]) % L for r in range(4))]
                               for k in modes])
    spectral = definition._spectral_data(features, first_outgoing, root)
    a, b = map(s.Rational, (spectral["a"], spectral["b"]))
    F = (a-b)*s.eye(4)+b*s.ones(4)
    legs_s = [chart.ETA*F[r, :].T for r in range(4)]
    legs = np.array([_numeric(v).reshape(4) for v in legs_s])
    roots8 = np.array([complex(s.sympify(z).evalf(18)) for z in operator.ROOTS8])
    tk = roots8[np.array(modes)]
    cu = np.einsum("ra,aij->rij", legs, creators)
    D = L*(np.einsum("kr,rij->kij", tk-1, cu)
           +np.einsum("kr,rji->kij", tk.conj()-1, cu))
    sectors = [_sector(q, inactive, rank_T, definition=definition, operator=operator,
                       features=features, modes=modes, index=index, tk=tk, D=D,
                       creators=creators, creators_s=creators_s, legs_s=legs_s, root=root,
                       return_data=return_data)
               for q, inactive, rank_T in SECTORS]
    data = None
    if return_data:
        data = [pair[1] for pair in sectors]
        sectors = [pair[0] for pair in sectors]
    elapsed = time.perf_counter()-start
    require(elapsed < 45, "new_diagnostic_under_45_seconds")
    result = {"status": "NUMERICAL_DIAGNOSTIC_ONLY", "seconds": round(elapsed, 4),
            "root_center_d_o": root, "root_radius_not_propagated": receipt["interval"]["root_radius"],
            "owned_exterior_order": list(exterior_order),
            "source_pins": {**chart.PINS, **definition.PINS},
            "consumed_definition_sha256": {
                path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                for path in (definition_path, ordered_path)},
            "sectors": sectors,
            "all_other_native_directions_removed_only_if_separate_rank_T_proof": True,
            "old_checker_runs_root_search_or_receipt_mutations": False,
            "physical_admission_or_GR_claim": False}
    return (result, data) if return_data else result


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
