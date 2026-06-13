# -*- coding: utf-8 -*-
"""
D0-CERT 24.5.1 — QEC [[4,2,2]]: EXP(16^G) vs POLY DP vs φ-proxy

Goal:
- Show the exponential sweep 16^G (visible in runtime).
- Provide an exact POLYNOMIAL counting method via DP on a finite space
  of 5-qubit Pauli strings (4^5=1024), without enumerating 16^G configurations.
- Keep φ-proxy as an O(1) channel (APPX), but separate it from exact DP.

Important for D0:
- No hidden knobs: inputs only (A) volume G, (B) bridge-p (if counting probability).
- All results must be reproducible and checkable (PASS/FAIL).
"""

import time
import argparse
import os
from pathlib import Path
from itertools import product
from typing import Dict, List, Tuple

from d0.protocol import load_protocol, P
from d0.io import get_outdir, save_json
from d0.report import CertReport
from d0.constants import eps2

# =========================
#  CORE: Pauli algebra (strings; phase ignored)
# =========================
pauli_to_index = {"I": 0, "X": 1, "Y": 2, "Z": 3}
index_to_pauli = ["I", "X", "Y", "Z"]

# multiplication table ignoring phase
pauli_multi_mat = [
    [0, 1, 2, 3],
    [1, 0, 3, 2],
    [2, 3, 0, 1],
    [3, 2, 1, 0],
]


def multiply(pauli_string1: str, pauli_string2: str) -> str:
    new_paulis = []
    for q in range(5):
        ind = pauli_multi_mat[
            pauli_to_index[pauli_string1[q]]
        ][
            pauli_to_index[pauli_string2[q]]
        ]
        new_paulis.append(index_to_pauli[ind])
    return "".join(new_paulis)


cnot_rules = {
    "II": "II",
    "IX": "IX",
    "IY": "ZY",
    "IZ": "ZZ",
    "XI": "XX",
    "XX": "XI",
    "XY": "YZ",
    "XZ": "YY",
    "YI": "YX",
    "YX": "YI",
    "YY": "XZ",
    "YZ": "XY",
    "ZI": "ZI",
    "ZX": "ZX",
    "ZY": "IY",
    "ZZ": "IZ",
}

tq_paulis = [
    "II", "IX", "IY", "IZ",
    "XI", "XX", "XY", "XZ",
    "YI", "YX", "YY", "YZ",
    "ZI", "ZX", "ZY", "ZZ",
]


def tq_pauli_qubits(tq_pauli: str, i: int, j: int) -> str:
    pauli_string = "IIIII"
    if i < j:
        return f"{pauli_string[0:i]}{tq_pauli[0]}{pauli_string[i+1:j]}" \
               f"{tq_pauli[1]}{pauli_string[j+1:]}"
    else:
        return f"{pauli_string[0:j]}{tq_pauli[1]}{pauli_string[j+1:i]}" \
               f"{tq_pauli[0]}{pauli_string[i+1:]}"


def cnot(i: int, j: int, pauli_string: str) -> str:
    sij = pauli_string[i] + pauli_string[j]
    new_sij = cnot_rules[sij]
    if i < j:
        return f"{pauli_string[0:i]}{new_sij[0]}{pauli_string[i+1:j]}" \
               f"{new_sij[1]}{pauli_string[j+1:]}"
    else:
        return f"{pauli_string[0:j]}{new_sij[1]}{pauli_string[j+1:i]}" \
               f"{new_sij[0]}{pauli_string[i+1:]}"


# =========================
#  CORE: Stabilizers
# =========================
error_detection_stabilizer_generators = [
    "XXXXI", "ZZZZI", "IIIIZ", "ZZIII", "ZIZII", "XIXII", "XXIII",
]
logical_state_stabilizer_generators = [
    "XXXXI", "ZZZZI", "IIIIZ", "ZZIII", "ZIZII",
]


def build_group(gens: List[str]) -> set:
    # brute generate group by multiplying subsets (small: 2^k)
    group = set(["IIIII"])
    for g in gens:
        group = group.union({multiply(s, g) for s in list(group)})
    return group


error_detection_stabilizer_group = build_group(error_detection_stabilizer_generators)
logical_state_stabilizer_group = build_group(logical_state_stabilizer_generators)

# =========================
#  Gates pattern
# =========================
BASE_CNOT_PATTERN = [(1, 2), (1, 0), (2, 3), (3, 4), (0, 4)]


# =========================
#  EXP (legacy): enumeration
# =========================
def run_full_enumeration_legacy(G: int, max_configs: int, verbose: bool = True):
    t0 = time.time()
    base = 16
    total_configs = base ** G
    limit = min(total_configs, max_configs)

    num_undetected = [0] * (G + 1)
    num_undetected_logical = [0] * (G + 1)

    gates = [BASE_CNOT_PATTERN[i % len(BASE_CNOT_PATTERN)] for i in range(G)]

    for conf_idx in range(limit):
        indices = []
        tmp = conf_idx
        num_errors = 0
        for _ in range(G):
            digit = tmp % base
            tmp //= base
            indices.append(digit)
            if digit != 0:
                num_errors += 1

        pauli_string = "IIIII"
        for gate_idx, (i, j) in enumerate(gates):
            pauli_string = cnot(i, j, pauli_string)
            tq = tq_paulis[indices[gate_idx]]
            pauli_string = multiply(pauli_string, tq_pauli_qubits(tq, i, j))

        no_error_detected = (pauli_string in error_detection_stabilizer_group)
        valid_logical_state = (pauli_string in logical_state_stabilizer_group)

        if no_error_detected:
            num_undetected[num_errors] += 1
            if not valid_logical_state:
                num_undetected_logical[num_errors] += 1

    elapsed = time.time() - t0
    cfg_per_sec = (limit / elapsed) if elapsed > 0 else float("inf")
    t_full_est_rate = (total_configs / cfg_per_sec) if cfg_per_sec > 0 else float("inf")

    stats = {
        "G": G,
        "total_configs": total_configs,
        "processed_configs": limit,
        "num_undetected": num_undetected,
        "num_undetected_logical": num_undetected_logical,
        "time_sec": elapsed,
        "truncated": (limit < total_configs),
        "cfg_per_sec": cfg_per_sec,
        "t_full_est_rate": t_full_est_rate,
        "method": "exp_legacy",
    }

    if verbose:
        print(f"\n=== FULL ENUM (EXP/legacy) G={G} ===")
        print(f"Total configurations:     16^{G} = {total_configs:e}")
        print(f"Actually processed:       {limit:e}")
        print(f"Enumeration time:         {elapsed:.3f} s")
        print("Undetected (n=0..G):")
        print("  ", stats["num_undetected"])
        print("Undetected+LOGICAL (n=0..G):")
        print("  ", stats["num_undetected_logical"])
        if stats["truncated"]:
            print("[WARN] truncated by --max-configs")
            print(f"[EST] enum throughput: {stats['cfg_per_sec']:.3e} cfg/s")
            print(f"[EST] full enum time (rate): ~{stats['t_full_est_rate']:.3f} s")

    return stats


# =========================
#  POLY DP (exact): 1024-state DP
# =========================
ALL_STATES_5Q = ["".join(p) for p in product(index_to_pauli, repeat=5)]
STATE_TO_INDEX = {s: i for i, s in enumerate(ALL_STATES_5Q)}
N_STATES = len(ALL_STATES_5Q)  # 1024


def _precompute_transitions_for_gate(i: int, j: int) -> List[List[int]]:
    """table[state_idx][digit] = next_state_idx for given (i,j)"""
    table = [[0] * 16 for _ in range(N_STATES)]
    for s_idx, s in enumerate(ALL_STATES_5Q):
        s_prop = cnot(i, j, s)
        for d, tq in enumerate(tq_paulis):
            new_s = multiply(s_prop, tq_pauli_qubits(tq, i, j))
            table[s_idx][d] = STATE_TO_INDEX[new_s]
    return table


# Precompute for 5 gate types in the pattern
TRANS_TABLES: Dict[Tuple[int, int], List[List[int]]] = {
    (i, j): _precompute_transitions_for_gate(i, j) for (i, j) in set(BASE_CNOT_PATTERN)
}


def run_poly_dp_exact(G: int, verbose: bool = True):
    """
    Exact DP computing the same stats as EXP enumeration, but in polynomial time in G.

    dp[state_idx][k] = number of sequences of length t that lead to this Pauli string
                       with exactly k non-identity two-qubit insertions.

    Complexity: O(G * 1024 * 16 * G) ~ O(1024 * 16 * G^2).
    """
    t0 = time.time()
    gates = [BASE_CNOT_PATTERN[i % len(BASE_CNOT_PATTERN)] for i in range(G)]

    dp = [[0] * (G + 1) for _ in range(N_STATES)]
    dp[STATE_TO_INDEX["IIIII"]][0] = 1

    for step, (i, j) in enumerate(gates):
        table = TRANS_TABLES[(i, j)]
        new_dp = [[0] * (G + 1) for _ in range(N_STATES)]

        for s_idx in range(N_STATES):
            row = dp[s_idx]
            # quick skip if row all zeros
            if all(v == 0 for v in row):
                continue

            # digit 0: no error count increment
            ns0 = table[s_idx][0]
            nr0 = new_dp[ns0]
            for k in range(G + 1):
                v = row[k]
                if v:
                    nr0[k] += v

            # digits 1..15: +1 error
            for d in range(1, 16):
                ns = table[s_idx][d]
                nr = new_dp[ns]
                for k in range(G):
                    v = row[k]
                    if v:
                        nr[k + 1] += v

        dp = new_dp

    # Aggregate to the same outputs as legacy
    num_undetected = [0] * (G + 1)
    num_undetected_logical = [0] * (G + 1)

    for s_idx, s in enumerate(ALL_STATES_5Q):
        if s in error_detection_stabilizer_group:
            row = dp[s_idx]
            for k, cnt in enumerate(row):
                if cnt:
                    num_undetected[k] += cnt
                    if s not in logical_state_stabilizer_group:
                        num_undetected_logical[k] += cnt

    elapsed = time.time() - t0
    stats = {
        "G": G,
        "num_undetected": num_undetected,
        "num_undetected_logical": num_undetected_logical,
        "time_sec": elapsed,
        "method": "poly_dp_exact",
    }

    if verbose:
        print(f"\n=== POLY DP (exact) G={G} ===")
        print(f"DP time: {elapsed:.6f} s")
        print("Undetected (n=0..G):")
        print("  ", num_undetected)
        print("Undetected+LOGICAL (n=0..G):")
        print("  ", num_undetected_logical)

    return stats


# =========================
#  φ-proxy (APPX): O(1)
# =========================
def phi_logical_fidelity_small_p(p: float, C: float = 12.0) -> float:
    return 1.0 - C * (p ** 2)


def run_phi_proxy(G: int, p: float, C: float = 12.0, verbose: bool = True):
    t0 = time.time()
    F = phi_logical_fidelity_small_p(p, C=C)
    elapsed = time.time() - t0
    stats = {"G": G, "F_phi": F, "time_sec": elapsed, "C": C, "method": "phi_proxy"}
    if verbose:
        print(f"\n=== PHI METHOD (proxy, O(1)) G={G} ===")
        print(f"p = {p}")
        print(f"C = {C}")
        print(f"F_phi(p) ≈ {F:.12f}")
        print(f"φ-proxy time: {elapsed:.6f} s")
    return stats


# =========================
#  CERT: Golden for G=5
# =========================
GOLDEN_G = 5
GOLDEN_UND_G5 = [1, 7, 282, 4222, 31637, 94923]
GOLDEN_LOG_G5 = [0, 0, 144, 3024, 24240, 70896]


def check_golden_counts(stats) -> bool:
    return (stats["G"] == GOLDEN_G
            and stats["num_undetected"] == GOLDEN_UND_G5
            and stats["num_undetected_logical"] == GOLDEN_LOG_G5)


# =========================
#  CLI
# =========================
def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--protocol", default=os.environ.get("D0_PROTOCOL", "protocols/book5_qec_comparison.json"))
    ap.add_argument("--core-only", action="store_true", help="disable bridge(p,C) usage (still runs DP)")
    return ap.parse_args()


def main():
    args = parse_args()
    PROT = load_protocol(args.protocol)
    outdir = get_outdir() / "cert_24_5_1_qec"
    outdir.mkdir(parents=True, exist_ok=True)

    rep = CertReport(cert_id="CERT_24_5_1_QEC", protocol_id=PROT.protocol_id)
    rep.add("PROTO_LOADED", True, protocol=args.protocol)

    G_list = list(map(int, P(PROT, "G_list", [2, 3, 4, 5, 6])))
    p = float(P(PROT, "p_bridge", 0.01))
    C = float(P(PROT, "C_bridge", 12.0))
    max_configs = int(P(PROT, "max_configs", 16**5))
    exp_G_max = int(P(PROT, "exp_G_max", 4))

    if args.core_only:
        p = None
        C = None
        rep.add("MODE_CORE_ONLY", True, enabled=True)
    else:
        rep.add("MODE_CORE_ONLY", True, enabled=False, p_bridge=p, C_bridge=C)

    print("==== D0-CERT 24.5.1 — φ-QEC [[4,2,2]] — EXP vs POLY vs φ-proxy ====")
    print(f"p={p}, C={C}, G_list={G_list}, max_configs={max_configs}, exp_G_max={exp_G_max}")
    print(f"|S_err|={len(error_detection_stabilizer_group)} (expect 128), "
          f"|S_log|={len(logical_state_stabilizer_group)} (expect 32)")
    print("CERT: allowed inputs are (A) volume G, (B) bridge p. No hidden knobs.\n")

    last_full_G = None
    last_full_time = None

    for G in G_list:
        print("\n" + "=" * 64)
        print(f"G={G}")
        print("=" * 64)

        # POLY exact DP
        stats_poly = run_poly_dp_exact(G, verbose=True)

        # EXP enumeration (legacy) for timing comparison (optional)
        stats_exp = None
        if G <= exp_G_max:
            stats_exp = run_full_enumeration_legacy(G, max_configs=max_configs, verbose=True)

        # φ-proxy
        stats_phi = None
        if p is not None and C is not None:
            stats_phi = run_phi_proxy(G, p=p, C=C, verbose=True)

        # Golden check
        if G == GOLDEN_G:
            gold_ok = check_golden_counts(stats_poly)
            rep.add("GOLDEN_G5_COUNTS", bool(gold_ok), G=int(G), eps2=float(eps2))
            print("\nCERT G=5 GOLDEN (POLY):", "VALID" if gold_ok else "FAILED")
            if stats_exp is not None and (not stats_exp["truncated"]):
                print("CERT G=5 GOLDEN (EXP):", "VALID" if check_golden_counts(stats_exp) else "FAILED")

        # Compare exp time estimate vs poly
        if stats_exp is not None:
            # projection of full exp time if truncated
            t_full_est_proj = None
            if not stats_exp["truncated"]:
                last_full_G = G
                last_full_time = stats_exp["time_sec"]
            else:
                if last_full_G is not None and last_full_time is not None:
                    t_full_est_proj = last_full_time * (16 ** (G - last_full_G))

            t_exp_effective = stats_exp["time_sec"]
            if stats_exp["truncated"]:
                t_exp_effective = t_full_est_proj if (t_full_est_proj is not None) else stats_exp["t_full_est_rate"]

            speedup_poly_vs_exp = t_exp_effective / max(stats_poly["time_sec"], 1e-12)
            speedup_phi_vs_poly = None
            if stats_phi is not None:
                speedup_phi_vs_poly = stats_poly["time_sec"] / max(stats_phi["time_sec"], 1e-12)

            print("\n--- Summary for G =", G, "---")
            print(f"  EXP total configs:        {stats_exp['total_configs']:e}")
            print(f"  EXP processed/total:      {stats_exp['processed_configs']:e}  "
                  f"({stats_exp['processed_configs']/stats_exp['total_configs']:.3e} fraction)")
            print(f"  EXP time (measured):      {stats_exp['time_sec']:.6f} s")
            if stats_exp["truncated"]:
                print(f"  EXP full time est (rate): ~{stats_exp['t_full_est_rate']:.3f} s")
                if t_full_est_proj is not None:
                    print(f"  EXP full time est (proj): ~{t_full_est_proj:.3f} s")
            print(f"  POLY DP time (exact):     {stats_poly['time_sec']:.6f} s")
            if stats_phi is not None:
                print(f"  φ-proxy time (APPX):      {stats_phi['time_sec']:.6f} s")
            print(f"  SPEEDUP (EXP_full_est / POLY): ~{speedup_poly_vs_exp:.3e}x")
            if speedup_phi_vs_poly is not None:
                print(f"  SPEEDUP (POLY / φ-proxy): ~{speedup_phi_vs_poly:.3e}x")
        else:
            print("\n--- Summary for G =", G, "---")
            print(f"  POLY DP time (exact):     {stats_poly['time_sec']:.6f} s")
            if stats_phi is not None:
                print(f"  φ-proxy time (APPX):      {stats_phi['time_sec']:.6f} s")

    print("\n=== INTERPRETATION (D0) ===")
    print("- EXP method: complexity ~ 16^G (visible in projected/estimated full time).")
    print("- POLY DP: exact computation on finite state space 4^5=1024 (polynomial in G).")
    print("- φ-proxy: APPX/O(1) channel; use only inside ε²-protocol / calibration.")

    out_json = outdir / P(PROT, "outputs")["json"]
    save_json(out_json, rep.to_dict())
    return 0 if rep.ok() else 2


if __name__ == "__main__":
    raise SystemExit(main())
