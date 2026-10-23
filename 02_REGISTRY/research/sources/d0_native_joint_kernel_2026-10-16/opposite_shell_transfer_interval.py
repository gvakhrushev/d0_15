"""One rigorous opposite-sign shell-transfer restriction, q=(1,7,0,0).

The NEW general symbol algebra chooses a finite-decimal 8x8 congruence on
all inactive full-leg columns.  Immutable full16 creator geometry and
arithmetic then validate that congruence independently over the complete
owned root rectangle.  All4096 momenta, the complete heat normalizer,
reference128, feedback, and signed complement resolvent remain present.

Only the common scalar owner's spectral_intervals() definitions are used;
its original guards execute unchanged.  This file independently constructs
the opposite-sign edge/pair cache, with exact feature equality and exact
feature subtraction before interval arithmetic.  No historical run(), root
search, expected-output writer, or existing-file mutation is invoked.

The restricted heat/CAR S4 congruence transfers this result to q=(0,1,7,0).
It is NOT an S4 symmetry or gauge admission of the full native SO3 chart.
The separate exact all-shell rank5 theorem is needed to identify these
eight directions with kerT modulo the six representation directions.
"""
from __future__ import annotations

import os
for _name in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS",
              "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_name] = "1"

from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import platform

import mpmath as mp
import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
Q, INACTIVE, DIMENSION = (1, 7, 0, 0), (2, 3), 8
PINS = {
    "native_chart_check.py": "1cb2bd82796634b414b76a5396b629c98c3679aee3ce7aa63dfc34647ab84b65",
    "ordered_operator_check.py": "f2f9903685c2c522d4c850d335dfb9435c932182962402da499ff8a7a10a9418",
    "full_symbol_diagnostic.py": "6084660c02a1012a4beb619e71e61015dda0d7ebb44207bf6faa7d5281404b25",
    "nonzero_symbol_algebra.py": "b74c1a10ab6e1051dfb50942abf019cb19aeb890460bc98b919d2e848deecba1",
    "full_symbol_interval_weights.py": "0d8651dae3b6b7ba2049a1c71ac47895e536f9ccc5f85bf9978c133c75ccfc18",
    "full_shell_transfer_interval.py": "13632b21ddf9d0363343d319ebe949295b6cf9d46195ffe2a48dcebbfacdfb32",
    "full_symbol_interval.py": "2bb2f26be6d6484d087a2e2e2591b681c793b5932790e3552c2b9fdc5021c84d",
    "full_symbol_interval_geometry.py": "7fa48bf73ba7e8c51dbdf0b4a432e2801ae04cf61a018303a3f345680f5284d6",
    "shell_transfer_all_orbits.py": "d8db3de5b34e4ee4ac7a9efb4676072d18b455dec5a72f0beb6b46b40a99eb1a",
}


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("opposite_shell_transfer_interval:"+label)


def _check_pins():
    for name, digest in PINS.items():
        require(hashlib.sha256((HERE/name).read_bytes()).hexdigest() == digest,
                "immutable_helper_pin:"+name)


def _load(name):
    require(name+".py" in PINS, "only_explicitly_pinned_direct_helper")
    path = HERE/(name+".py")
    require(hashlib.sha256(path.read_bytes()).hexdigest() == PINS[name+".py"],
            "immutable_import:"+name)
    spec = importlib.util.spec_from_file_location("opposite_shell_"+name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def spectral_intervals(repo=None):
    """Live outward intervals, with an independently enumerated q1700 cache."""
    repo = ROOT if repo is None else Path(repo).resolve()
    owner = _load("full_symbol_interval_weights")
    original = owner.spectral_intervals(repo)  # All existing guards really run.
    result = dict(original)
    iv = original["iv_ctx"]
    modes, features, data = (original[key] for key in ("modes", "features", "feature_data"))
    mode_index = {mode: index for index, mode in enumerate(modes)}
    outgoing = tuple(mode_index[tuple((mode[r]+Q[r]) % owner.L for r in range(4))]
                     for mode in modes)
    require(all(index != other for index, other in enumerate(outgoing)),
            "nonzero_frequency_has_no_diagonal_trace_rank_one_term")
    edge_keys = tuple(tuple(sorted((features[index], features[other])))
                      for index, other in enumerate(outgoing))
    pair_counts = Counter(edge_keys)
    equal_edges = sum(count for (left, right), count in pair_counts.items() if left == right)
    sqrt2 = iv.sqrt(2)

    def real_pair(pair):
        return pair[0]+pair[1]*sqrt2

    def gap(left, right):
        da = tuple(right[0][j]-left[0][j] for j in range(2))
        dc = tuple(right[1][j]-left[1][j] for j in range(2))
        return original["d"]*real_pair(da)+original["o"]*real_pair(dc)

    pairs, gaps = {}, []
    for key in sorted(pair_counts):
        left, right = key
        dl, dr = data[left], data[right]
        if left == right:
            dd, difference = dl["derivative"], iv.mpf(0)
        else:
            difference = gap(left, right)
            require(owner._separated(difference), "new_exact_feature_gap_interval_separated")
            gaps.append(owner._absolute_lower(difference))
            dd = (dr["kappa"]-dl["kappa"])/difference
        pairs[key] = {
            "dd": dd, "gamma_J": dl["chi"]+dr["chi"],
            "weight_X": dd-dl["rho"]*dr["resolvent"]-dr["rho"]*dl["resolvent"],
            "energy_gap": difference, "equal_exact_features": left == right,
        }
    require(len(modes) == sum(pair_counts.values()) == 4096 and len(data) == 119
            and set(pairs) == set(edge_keys), "all_modes_and_exact_pair_cache_complete")
    shell = original["shell_feature"]
    shell_edges = tuple(index for index, other in enumerate(outgoing)
                        if features[index] == shell and features[other] == shell)
    actual_shell_edges = {(modes[index], modes[outgoing[index]]) for index in shell_edges}
    require(actual_shell_edges == {
                ((0, 1, 0, 0), (1, 0, 0, 0)),
                ((7, 0, 0, 0), (0, 7, 0, 0)),
            }, "exactly_two_owned_opposite_sign_shell_transfers")
    require(all(pairs[edge_keys[index]]["equal_exact_features"] for index in shell_edges),
            "both_shell_transfers_use_analytic_derivative_not_small_gap_quotient")
    result.update(q=Q, outgoing=outgoing, edge_keys=edge_keys, pair_data=pairs,
                  pair_counts=pair_counts, exact_equal_edges=equal_edges,
                  minimum_distinct_gap_lower=min(gaps), shell_edge_indices=shell_edges)
    for name in ("dd", "gamma_J", "weight_X"):
        result[name] = tuple(pairs[key][name] for key in edge_keys)
    result["source_pins"] = {**original["source_pins"], **PINS}
    result["metadata"] = {
        **original["metadata"], "q": list(Q),
        "unordered_feature_pairs": len(pairs),
        "exact_equal_feature_directed_edges": equal_edges,
        "occupied_to_occupied_directed_edges": len(shell_edges),
        "minimum_distinct_gap_lower": owner._decimal(min(gaps), owner.ROUND_FLOOR),
        "new_q_edges_independently_enumerated": True,
        "common_owner_guards_executed_unchanged": True,
        "common_owner_sha256": PINS["full_symbol_interval_weights.py"],
    }
    return result


def _choose(repo):
    algebra = _load("nonzero_symbol_algebra")
    shared = algebra.shared_spectral_data(repo)
    assembled = algebra.assemble_symbol(Q, shared, use_stationary_root_identity=False)
    labels = assembled["basis"]["labels"]
    slots = [i for i, label in enumerate(labels) if label[0] == "inactive_full_leg"]
    require([labels[i] for i in slots] == [["inactive_full_leg", r, j]
                                         for r in INACTIVE for j in range(4)],
            "all_eight_inactive_full_leg_slots_in_canonical_order")
    require(len(slots) == DIMENSION and assembled["basis"]["dimension"] == 13,
            "complete_mean_slice_and_inactive_restriction_dimensions")
    H = assembled["H"][np.ix_(slots, slots)]
    require(np.isfinite(H).all() and assembled["Hermitian_relative_error"] < 1e-10,
            "finite_Hermitian_numerical_choice_only")
    values, vectors = np.linalg.eigh(H)
    require(np.min(np.abs(values)) > 1e-5, "stop_on_tiny_or_ambiguous_numerical_pivot")
    B = vectors/np.sqrt(np.abs(values))[None, :]
    exact = [[(format(z.real, ".17g"), format(z.imag, ".17g")) for z in row] for row in B]
    return {"q": list(Q), "B": exact, "signs": np.sign(values).astype(int),
            "choice_only": {"new_algebra_slots": slots,
                            "new_algebra_numerical_eigenvalues": values.tolist(),
                            "weighted_J_not_stationary_shortcut": True,
                            "numerical_choice_is_not_the_inertia_proof": True}}


def _restricted_S4_facts(inertia):
    # Cycle0->1->2->0 maps q1700 to q0170.  Verify the identity separately
    # for the a and b coefficients of U=F eta; no root value is substituted.
    P = np.array([[0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]], int)
    eta = np.diag([1, -1, -1, -1])
    R = eta@P@eta
    Ua, Ub = eta, (np.ones((4, 4), int)-np.eye(4, dtype=int))@eta
    require(np.array_equal(P@Ua, Ua@R) and np.array_equal(P@Ub, Ub@R)
            and np.array_equal(R.T@R, np.eye(4, dtype=int)),
            "exact_symbolic_a_b_background_identity_PU_equals_UR")
    target_q = tuple(int(value) for value in P@np.array(Q))
    require(target_q == (0, 1, 7, 0), "opposite_sign_target_role_permutation")
    target_inactive = tuple(r for r in range(4) if target_q[r] == 0)
    T = np.zeros((DIMENSION, DIMENSION), int)
    for source_role_index, role in enumerate(INACTIVE):
        target_role = int(np.flatnonzero(P[:, role])[0])
        offset = 4*target_inactive.index(target_role)
        T[offset:offset+4, 4*source_role_index:4*source_role_index+4] = R
    require(np.array_equal(T.T@T, np.eye(DIMENSION, dtype=int))
            and np.all(np.sum(np.abs(T), axis=0) == 1),
            "exact_signed_permutation_of_all_inactive_coframe_slots")
    return {
        "source_q": list(Q), "target_q": list(target_q),
        "target_inactive_roles": list(target_inactive),
        "role_permutation_P": P.tolist(), "internal_orthogonal_R": R.tolist(),
        "inactive_slot_signed_permutation_T": T.tolist(),
        "background_identity": "U=F*eta, F=(a-b)I+b11T; P*U=U*(eta*P*eta)",
        "jet_map": "q'=Pq, k'=Pk, A'=P*A*R^T, W=exterior(R)",
        "operator_intertwining": "D(Pk)=W*D(k)*W^*; J'=W*J*W^*; X'=W*X*W^*",
        "scalar_trace_invariance": "lambda(Pk)=lambda(k); full Z, shell128 and Tr16 preserved",
        "exact_congruence": "H_q=T^* H_(Pq) T; T real signed permutation",
        "uniform_on_same_root_rectangle": True,
        "transferred_restriction_inertia": dict(inertia),
        "full_native_SO3_chart_S4_symmetry_or_physical_gauge_claim": False,
    }


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    _check_pins()
    mp.mp.dps, mp.iv.dps = 100, 80
    info = np.finfo(np.float64)
    require(info.eps == 2.0**-52 and info.nmant == 52 and info.maxexp == 1024
            and np.dtype(np.complex128).itemsize == 16, "IEEE_binary64_storage")
    arithmetic = _load("full_symbol_interval")  # Arithmetic definitions ONLY.
    geometry_owner = _load("full_shell_transfer_interval")  # No run or _choose.
    choice = _choose(repo)
    weights = spectral_intervals(repo)
    geometry = geometry_owner.creator_geometry(choice["B"], INACTIVE, repo)
    sector = geometry_owner._validate_sector(choice, weights, geometry, arithmetic)
    require(sector["restriction_dimension"] == DIMENSION
            and sector["Hermitian_operator_distance_from_signature_upper"] < 1,
            "strict_whole_rectangle_eight_dimensional_inertia_not_numerical_guess")
    owner = _load("full_symbol_interval_weights")
    pair_payload = [{"features": key, **{name: owner.interval_record(row[name]) for name in
                                         ("dd", "gamma_J", "weight_X", "energy_gap")}}
                    for key, row in sorted(weights["pair_data"].items())]
    payload = json.dumps(pair_payload, sort_keys=True, separators=(",", ":")).encode()
    sector.update(inactive_roles=list(INACTIVE), independently_required_exact_rank_T=5,
                  numerical_preconditioner_choice=choice["choice_only"])
    result = {
        "schema": "d0-native-opposite-shell-transfer-interval/1",
        "status": "VALIDATED_OPPOSITE_SIGN_SHELL_TRANSFER_RESTRICTION",
        "momenta": 4096, "exterior_dimension": 16, "reference_dimension": 128,
        "sector": sector,
        "restricted_heat_S4_congruence": _restricted_S4_facts(sector["validated_restriction_inertia"]),
        "full_Z": owner.interval_record(weights["Z"]),
        "signed_ground_resolvent": owner.interval_record(weights["resolvent"][0]),
        "two_exact_shell_transfers": [[list(weights["modes"][index]),
                                       list(weights["modes"][weights["outgoing"][index]])]
                                      for index in weights["shell_edge_indices"]],
        "outward_decimal_new_q_pair_payload_sha256": hashlib.sha256(payload).hexdigest(),
        "source_sha256": {**PINS, "opposite_shell_transfer_interval.py":
                          hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        "owned_input_pins": weights["source_pins"],
        "arithmetic_environment": {"python": platform.python_version(), "numpy": np.__version__,
                                   "mpmath": mp.__version__, "float": "IEEE_binary64_with_outward_budgets"},
        "floating_Gram_real_operation_bound_per_entry": 2**26,
        "complex_Gram_gamma_multiplier": 2,
        "old_run_root_search_receipt_write_or_existing_file_mutation": False,
        "all_mode_census_full_joint_kernel_physical_admission_or_GR_claim": False,
    }
    _check_pins()
    return result


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
