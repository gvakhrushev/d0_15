"""Rigorous full-spectrum scalar weights for q2000 and q1100.

The immutable q3300 interval owner supplies the common 119-feature spectral
data, full Z, all shell densities, and signed complement resolvents. Its
guards are executed unchanged. This module independently constructs the
directed edges and exact feature-pair cache for each new q. No existing guard
is skipped, monkeypatched, or weakened; no old certificate run is called.

All4096 modes, all16 Fock components, all128 occupied shell states and the
published entire root rectangle are retained. No inertia/kernel assertion,
root solve, receipt regeneration, or file output occurs here.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OWNER = "02_REGISTRY/research/sources/d0_native_joint_kernel_2026-10-16/full_symbol_interval_weights.py"
OWNER_SHA256 = "0d8651dae3b6b7ba2049a1c71ac47895e536f9ccc5f85bf9978c133c75ccfc18"
SECTORS = ((2, 0, 0, 0), (1, 1, 0, 0))


def require(condition, label):
    if not bool(condition):
        raise ArithmeticError("shell_transfer_interval_weights:"+label)


def _owner(repo):
    path = repo/OWNER
    require(hashlib.sha256(path.read_bytes()).hexdigest() == OWNER_SHA256,
            "immutable_complete_spectral_owner_pin")
    spec = importlib.util.spec_from_file_location("shell_transfer_interval_scalar_owner", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def spectral_intervals(repo=None, q=(2, 0, 0, 0)):
    """Same live-interval interface as full_symbol_interval_weights.

    Only outgoing/edge-dependent values are replaced in a shallow copy;
    the immutable feature rows and interval context are reused unchanged.
    Counts are independently obtained from every actual new-q edge.
    """
    started = time.perf_counter()
    repo = ROOT if repo is None else Path(repo).resolve()
    q = tuple(q)
    require(q in SECTORS, "only_explicit_q2000_or_q1100_sectors")
    owner = _owner(repo)
    original = owner.spectral_intervals(repo)  # all original guards really run.
    result = dict(original)
    iv = original["iv_ctx"]
    modes, features, data = (original[key] for key in ("modes", "features", "feature_data"))
    mode_index = {mode: index for index, mode in enumerate(modes)}
    outgoing = tuple(mode_index[tuple((mode[r]+q[r]) % owner.L for r in range(4))]
                     for mode in modes)
    require(all(index != other for index, other in enumerate(outgoing)),
            "nonzero_q_has_no_diagonal_momentum_block")
    edge_keys = tuple(tuple(sorted((features[index], features[other])))
                      for index, other in enumerate(outgoing))
    pair_counts = Counter(edge_keys)
    equal_edges = sum(count for (left, right), count in pair_counts.items() if left == right)
    sqrt2 = iv.sqrt(2)

    def real_pair(pair):
        return pair[0]+pair[1]*sqrt2

    def energy_gap(left, right):
        # Exact coefficient subtraction precedes interval arithmetic.
        da = tuple(right[0][i]-left[0][i] for i in range(2))
        dc = tuple(right[1][i]-left[1][i] for i in range(2))
        return original["d"]*real_pair(da)+original["o"]*real_pair(dc)

    pairs = {}
    gaps = []
    for key in sorted(pair_counts):
        left, right = key
        dl, dr = data[left], data[right]
        if left == right:
            dd = dl["derivative"]
            difference = iv.mpf(0)
        else:
            difference = energy_gap(left, right)
            require(owner._separated(difference),
                    "distinct_exact_features_have_interval_separated_new_q_gap")
            gaps.append(owner._absolute_lower(difference))
            dd = (dr["kappa"]-dl["kappa"])/difference
        pairs[key] = {"dd": dd, "gamma_J": dl["chi"]+dr["chi"],
                      "weight_X": dd-dl["rho"]*dr["resolvent"]-dr["rho"]*dl["resolvent"],
                      "energy_gap": difference, "equal_exact_features": left == right}
    require(sum(pair_counts.values()) == len(modes) == 4096
            and set(pairs) == set(edge_keys), "complete_new_q_pair_cache_covers_every_mode")
    shell = original["shell_feature"]
    shell_edges = tuple(index for index, other in enumerate(outgoing)
                        if features[index] == shell and features[other] == shell)
    expected_shell_edges = 1 if q == SECTORS[0] else 2
    require(len(shell_edges) == expected_shell_edges, "exact_one_or_two_occupied_transfers")
    require(all(pairs[edge_keys[index]]["equal_exact_features"] for index in shell_edges),
            "all_occupied_transfers_take_exact_analytic_equal_energy_branch")
    result.update(outgoing=outgoing, pair_data=pairs, edge_keys=edge_keys,
                  exact_equal_edges=equal_edges, minimum_distinct_gap_lower=min(gaps),
                  q=q, pair_counts=pair_counts, shell_edge_indices=shell_edges,
                  source_pins={**original["source_pins"], OWNER: OWNER_SHA256})
    result["metadata"] = {
        **original["metadata"], "q": list(q), "unordered_feature_pairs": len(pairs),
        "exact_equal_feature_directed_edges": equal_edges,
        "occupied_to_occupied_directed_edges": len(shell_edges),
        "minimum_distinct_gap_lower": owner._decimal(min(gaps), owner.ROUND_FLOOR),
        "common_feature_owner_guards_executed_unchanged": True,
        "common_owner_sha256": OWNER_SHA256,
        "new_q_edges_independently_enumerated": True,
    }
    for name in ("dd", "gamma_J", "weight_X"):
        result[name] = tuple(pairs[key][name] for key in edge_keys)
    result["seconds"] = time.perf_counter()-started
    return result


def _summary(repo, q):
    result = spectral_intervals(repo, q)
    owner = _owner(repo)
    pairs = [{"features": key, **{name: owner.interval_record(row[name]) for name in
                                 ("dd", "gamma_J", "weight_X", "energy_gap")}}
             for key, row in sorted(result["pair_data"].items())]
    payload = json.dumps(pairs, sort_keys=True, separators=(",", ":")).encode()
    return {"q": list(q), "seconds": round(result["seconds"], 4),
            "root_box": result["root_box"], "metadata": result["metadata"],
            "source_pins": result["source_pins"],
            "full_Z": owner.interval_record(result["Z"]),
            "signed_ground_resolvent": owner.interval_record(result["resolvent"][0]),
            "all_128_shell_states_retained": True,
            "shell_transfers": [[list(result["modes"][index]),
                                 list(result["modes"][result["outgoing"][index]])]
                                for index in result["shell_edge_indices"]],
            "weight_summary": {name: owner._summary(result[name]) for name in
                               ("lambda", "sqrt_lambda", "dd", "gamma_J", "weight_X")},
            "outward_decimal_new_q_pair_payload_sha256": hashlib.sha256(payload).hexdigest(),
            "scalar_enclosures_only_kernel_or_inertia_claim": False}


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    return {"schema": "d0-native-shell-transfer-interval-scalar-weights/1",
            "status": "PASS_RIGOROUS_SCALAR_ENCLOSURES_NOT_INERTIA",
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "sectors": [_summary(repo, q) for q in SECTORS],
            "existing_source_or_guard_mutations": False,
            "old_run_root_solve_or_receipt_write": False,
            "physical_admission_or_GR_claim": False}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
