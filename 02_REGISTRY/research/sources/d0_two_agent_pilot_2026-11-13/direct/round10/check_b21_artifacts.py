#!/usr/bin/env python3
"""Read-only, selected independent checks of B21 data; not an H.1 replay."""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("b21", type=Path)
args = parser.parse_args()
b = args.b21
rows = lambda f: [json.loads(x) for x in (b / f).read_text().splitlines()]
fr = rows("ORIGINAL_F_R_N20_L4.jsonl")
pf = rows("ORIGINAL_PF_N20_L4.jsonl")
chart = rows("L4_INTERIOR_CHART_COORDINATES.jsonl")
assert len(fr) == 10946 and len({r["word"] for r in fr}) == 10946
assert all(set(r["word"]) <= {"F", "R"} and
           r["word"].count("F") + 2*r["word"].count("R") == 20 for r in fr)
counts = Counter(tuple(r["site"]) for r in fr)
assert len(counts) == len(pf) == 256 and sum(r["N"] for r in pf) == 10946
assert all(counts[tuple(r["site"])] == r["N"] and
           Fraction(r["rho_numerator"], r["rho_denominator"]) ==
           Fraction(256*r["N"], 10946) for r in pf)
assert len(chart) == 2688 and sorted(r["sam_index"] for r in chart) == list(range(2688))
assert Counter(r["kind"] for r in chart) == {
    "coframe": 1024, "proper_link": 1536, "matter": 128}
for name in ["SC6_FORWARD.jsonl", "SC6_INVERSE.jsonl"]:
    gates = rows(name)
    assert len(gates) == 18176 and Counter(g["op"] for g in gates) == {
        "G": 5888, "CX": 4096, "SourceI": 8192}
    assert all(22 not in g["wires"] for g in gates)
ks = json.loads((b / "ORIGINAL_FOURIER128_L4.json").read_text())["kappa"]


def character(col, site):
    z = sum(k*x for k, x in zip(ks[col//2], site)) % 4
    return ((1, 0, -1, 0), (0, 1, 0, -1))[col % 2][z]


witness = sum(Fraction(r["N"], 10946*64) *
              character(19, r["site"]) * character(37, r["site"]) for r in pf)
assert witness == Fraction(-477, 700544)
with np.load(b / "CENTRE_JULIA32_TARGETS_NUMERIC.npz", allow_pickle=False) as data:
    matrices = np.concatenate([data["coframe_raw_and_pf"].reshape(-1, 32, 32),
                               data["proper_links"].reshape(-1, 32, 32)])
    error = float(np.max(np.abs(np.einsum("...ji,...jk->...ik", matrices, matrices,
                                        optimize=False) - np.eye(32))))
    assert matrices.shape == (3072, 32, 32) and error < 3e-14
with np.load(b / "SITE_LOADER_L4_CENTRE_NUMERIC.npz", allow_pickle=False) as data:
    p = (np.sqrt(5.) - 1)/2
    v = np.array([np.sqrt(p), p])
    born = v
    for _ in range(7):
        born = np.kron(born, v)
    target = np.sqrt(np.array([r["N"]/10946 for r in pf]))
    site_error = float(np.max(np.abs(np.einsum("ij,j->i", data["loader"], born,
                                             optimize=False) - target)))
    assert np.max(np.abs(data["chi"] - target)) < 1e-14 and site_error < 1e-14
inputs = ["ORIGINAL_F_R_N20_L4.jsonl", "ORIGINAL_PF_N20_L4.jsonl",
          "L4_INTERIOR_CHART_COORDINATES.jsonl", "SC6_FORWARD.jsonl",
          "SC6_INVERSE.jsonl", "ORIGINAL_FOURIER128_L4.json",
          "CENTRE_JULIA32_TARGETS_NUMERIC.npz", "SITE_LOADER_L4_CENTRE_NUMERIC.npz"]
result = {
    "status": "PASS_ROOT_SELECTED_B21_ARTIFACT_CHECKS",
    "scope": "Independent selected data checks; not a native seven-bank replay or interval certification of numeric targets",
    "F_R_words": len(fr), "cost_per_word": 20, "PF_sites": len(pf),
    "chart_coordinates": len(chart), "SC6_calls_each": 18176,
    "julia_matrix_count": len(matrices), "float_julia_orthogonality_error": error,
    "float_SITE_born_mapping_error": site_error,
    "exact_naive_PF_Fourier_offdiagonal": str(witness),
    "native_full_H1_executed": False, "GR_closed": False,
    "inputs": {f: hashlib.sha256((b/f).read_bytes()).hexdigest() for f in inputs}}
print(json.dumps(result, ensure_ascii=False, indent=2))
