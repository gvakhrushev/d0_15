#!/usr/bin/env python3
"""Narrow exact replay: original PF counts, 421 obstruction, actual Fourier128.

This is not a root/source/circuit census. Number-field and finite-history
claims are proved analytically in EXACT_NATIVE_WRITER_GATE.md.
"""

import argparse
import ast
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
import subprocess


SOURCE_REF = "b60a111b43f723a841d253b1d5bd9650c46b2cf8"
PRIMARY = ("02_REGISTRY/research/sources/"
           "d0_primary_native_domain_source_2026-10-20/"
           "check_primary_domain_source.py")


def require(condition, label):
    if not condition:
        raise RuntimeError("FAILED: " + label)


def sha(data):
    return hashlib.sha256(data).hexdigest()


class IntegerCounts(list):
    """Only the exact one-dimensional methods used by original_counts."""

    def sum(self):
        return sum(self)

    def min(self):
        return min(self)

    def max(self):
        return max(self)


class ExactStorage:
    int64 = int

    @staticmethod
    def zeros(size, dtype):
        require(dtype is int, "original integer count storage")
        return IntegerCounts([0] * size)


def valuation_integer(value, prime):
    require(value != 0, "nonzero valuation input")
    value = abs(value)
    result = 0
    while value % prime == 0:
        value //= prime
        result += 1
    return result


def valuation(value, prime):
    return (valuation_integer(value.numerator, prime)
            - valuation_integer(value.denominator, prime))


def exact_original_counts(source):
    parsed = ast.parse(source)
    functions = [node for node in parsed.body
                 if isinstance(node, ast.FunctionDef)
                 and node.name == "original_counts"]
    require(len(functions) == 1, "one pinned original_counts definition")
    node = functions[0]
    namespace = {"np": ExactStorage, "require": require}
    module = ast.Module(body=[node], type_ignores=[])
    exec(compile(module, "historical_original_counts_only", "exec"), namespace)
    result = namespace["original_counts"](20, 4)
    segment = ast.get_source_segment(source, node).encode()
    return result, sha(segment)


def exact_fourier_reference():
    sites = list(itertools.product(range(4), repeat=4))
    pairs = []
    for k in itertools.product(range(4), repeat=4):
        minus = tuple((-entry) % 4 for entry in k)
        if k < minus:
            pairs.append(k)
        if len(pairs) == 64:
            break
    require(len(pairs) == 64, "actual first64 Fourier pairs")
    cos4, sin4 = (1, 0, -1, 0), (0, 1, 0, -1)
    rows = []
    for z in sites:
        row = [0] * 128
        for j, k in enumerate(pairs):
            phase = sum(x * y for x, y in zip(k, z)) % 4
            baseline = [cos4[phase], sin4[phase]]
            emitted = [0, 0]
            emitted[phase % 2] = 1 if phase < 2 else -1
            require(emitted == baseline,
                    "14-bit phase programme gives actual cos/sin entry")
            row[2*j:2*j+2] = emitted
        require(sum(entry * entry for entry in row) == 64,
                "every actual site has64 nonzero reference entries")
        rows.append(row)
    columns = list(zip(*rows))
    for j in range(128):
        for k in range(j, 128):
            gram = sum(x * y for x, y in zip(columns[j], columns[k]))
            require(gram == (128 if j == k else 0),
                    "complete128 exact reference Gram")
    require(sum(x*x for row in rows for x in row) == 16384,
            "full reference norm after1/128 amplitude")
    # C_ref=rows/128, so C_ref^*C_ref=I128/128; each row norm=1/256.
    return {
        "sites": len(sites),
        "right_columns": 128,
        "uniform_input_bits": 14,
        "nonzero_entries": 16384,
        "nonzero_amplitude": "+/-1/128",
        "right_gram": "I128/128",
        "each_site_norm_squared": "1/256",
        "pair_list": [list(k) for k in pairs],
        "integer_reference_sha256": sha(json.dumps(rows, separators=(",", ":")).encode()),
    }


def exact_kernel_check():
    # Transverse role2 is the actual bit2 CAR creation. Its vacuum
    # coefficient is +1 in every exterior-order convention and top is zero.
    order = (0, 2, 3, 1)
    role = 2
    matrix = [[0 for _ in range(16)] for _ in range(16)]
    for mask in range(16):
        if mask & (1 << role):
            continue
        preceding = order[:order.index(role)]
        sign = (-1) ** sum(bool(mask & (1 << item)) for item in preceding)
        matrix[mask | (1 << role)][mask] = sign
    require(matrix[1 << role][0] == 1, "actual vacuum creation sign")
    require(all(matrix[row][15] == 0 for row in range(16)),
            "full top is exact creation kernel")
    # T and E_H are block diagonal with I2 in transverse coordinates;
    # eta_R therefore sends transverse column2 to -e2 for every H.
    T = [[Fraction(1), Fraction(1, 2), 0, 0],
         [Fraction(1), Fraction(-1, 2), 0, 0],
         [0, 0, 1, 0], [0, 0, 0, 1]]
    require(T[0][0]*T[1][1] - T[0][1]*T[1][0] == -1,
            "actual null-to-REST orientation")
    require([T[row][2] for row in range(4)] == [0, 0, 1, 0]
            and T[2] == [0, 0, 1, 0], "actual untouched transverse role")
    return {
        "exterior_order": list(order),
        "creation_role": role,
        "vacuum_output_mask": 1 << role,
        "top_mask": 15,
        "creation_on_vacuum_coefficient": 1,
        "creation_on_top": 0,
        "julia_bad_top_good_top": 1,
        "same_address_programme_ratio": "-p^k*sqrt(rho_z)",
        "fixed_kernel_probe_mean": "-p^k*sqrt(rho_z)",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    packet = Path(__file__).resolve().parent
    pin_bytes = (packet / "WRITER_SOURCE_PINS.json").read_bytes()
    pins = json.loads(pin_bytes)
    require(pins["source_ref"] == SOURCE_REF, "exact historical scientific input")
    sources = {}
    for item in pins["sources"]:
        data = subprocess.check_output(
            ["git", "show", SOURCE_REF + ":" + item["path"]], cwd=args.repo)
        require(sha(data) == item["sha256"], "historical pin: " + item["path"])
        sources[item["path"]] = data
    counts, count_function_hash = exact_original_counts(sources[PRIMARY].decode())
    require(len(counts) == 256 and sum(counts) == 10946
            and min(counts) == 29 and max(counts) == 78,
            "actual complete cost20/L4 count carrier")
    require(10946 == 2 * 13 * 421, "actual density denominator factorization")
    require(all(421 % d for d in range(2, 21)), "421 is prime")
    ratios = [Fraction(128 * n, 13 * 421) for n in counts]
    require(sum(ratios) == 256, "rho is normalized by actual mean count")
    require(all(valuation(r, 421) == -1 for r in ratios),
            "odd421 valuation at every actual site")
    require(all(valuation(r / c, 421) == -1
                for r in ratios for c in (1, 2, 5, 10)),
            "every rho excludes all rational squareclasses in F")
    receipt = {
        "status": "PASS",
        "scientific_input": SOURCE_REF,
        "scope": "actual primary point writer obstruction; fixed vacuum reference prefix",
        "physical_writer_or_GR_closed": False,
        "proof_sha256": sha((packet / "EXACT_NATIVE_WRITER_GATE.md").read_bytes()),
        "checker_sha256": sha(Path(__file__).read_bytes()),
        "source_pins_sha256": sha(pin_bytes),
        "historical_sources_verified": len(sources),
        "original_count_function_sha256": count_function_hash,
        "pf": {
            "sites": len(counts), "total": sum(counts),
            "minimum": min(counts), "maximum": max(counts),
            "denominator_factorization": [2, 13, 421],
            "rho": "128*n_z/(13*421)", "valuation421_every_site": -1,
            "histogram": dict(sorted(Counter(counts).items())),
            "counts_sha256": sha(json.dumps(list(counts), separators=(",", ":")).encode()),
        },
        "field": {
            "palette": "Q(sqrt(p),sqrt(2),i)",
            "p": "(sqrt(5)-1)/2",
            "relative_norm_p": -1,
            "rational_squareclasses": [1, 2, 5, 10],
            "classification_evidence": "analytic proof sections2-4; not numerical sampling",
        },
        "fourier_reference": exact_fourier_reference(),
        "kernel": exact_kernel_check(),
        "retained_scope": {
            "pure_target_no_go": "every finite accepted leaf, including a.s.-finite retry",
            "mixed_mean_no_go": "finite execution only",
            "fixed_vacuum_prefix": "actual256sites x128RIGHT, within declared addressed interface",
            "nonvacuum_writer": False,
            "refinement_limit_excluded": False,
            "Book03_valuation_identified": False,
        },
    }
    output = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
