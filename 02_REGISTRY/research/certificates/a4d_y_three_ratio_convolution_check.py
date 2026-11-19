#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""Exact three-ratio finite convolution; continuous torus and rescue remain open.

Restored after the execution environment disconnected during publication.
The same mathematical checks passed locally, including pinned JSON replay.
GitHub CI must independently replay this recovered source.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

from flint import fmpq_mat, nmod_mat
import numpy as np
import sympy as sp
import a4d_y_curved_joint_rational_stencil as S

HERE = Path(__file__).resolve().parent
OUT = HERE / "a4d_y_three_ratio_convolution_results.json"
PRIME = 1000033
GENERATOR = 5
ORDERS = (8, 12, 16, 24)
DIGESTS = (
    "174967b4db8ee3d878e9eb70b05636aa37c4b5bf977ae07aff5229f1306aea54",
    "5c2c9098657a5c4621251aad49e0cea8c27a1d55fe3e5b1e3437466b625638a2",
    "47ac012fe2fc4cc0e7297d796035440ae9f9439f4e0a50bc13be738ec6ee51df",
    "e2823e737e249f7c240f4f308ef2c8403c2612431b99b3dcdfe85f7a2373233f",
)


def ck(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def compile_interior():
    rows = list(range(24, 72)) + list(range(106, 126))
    ri = {r: i for i, r in enumerate(rows)}
    data = {}
    for offset, terms in ((0, S.ATERMS), (96, S.QTERMS)):
        for d, es in terms.items():
            M = data.setdefault(d[1:], np.zeros((68, 96), dtype=np.int64))
            for (r, c), value in es.items():
                if r + offset not in ri:
                    continue
                row = r + offset
                phase = row // 24 if row < 96 else (row - 96) // 10
                if phase - c // 24 + sum(d) != 0:
                    raise AssertionError("INTERIOR_FLOQUET_WRAP_OR_PHASE_ERROR")
                z = 14 * value
                if z.denominator != 1:
                    raise AssertionError("DENOMINATOR_CLEARING")
                M[ri[row], c] += z.numerator
    ck("ACTUAL_INTERIOR_HAS_NO_COMMON_FLOQUET_WRAP", bool(data))
    return data


def run(write=False):
    ck("GOOD_PRIME", sp.isprime(PRIME) and PRIME % 14 != 0)
    ck("PRIMITIVE_FIELD_GENERATOR", all(
        pow(GENERATOR, (PRIME - 1) // q, PRIME) != 1
        for q in sp.factorint(PRIME - 1)))
    data = compile_interior()
    ds = list(data)
    terms = np.array(list(data.values()))
    center = np.sum(terms, axis=0)
    ck("FOLDED_INTERIOR_RANK65_OVER_Q", fmpq_mat(center.tolist()).rank() == 65)
    ck("INTEGER_ACCUMULATION_BOUND",
       len(ds) * (PRIME - 1) * int(np.max(abs(terms))) < 2**63)
    records = []
    for N, expected in zip(ORDERS, DIGESTS):
        ck("GOOD_ROOT_ORDER_" + str(N), (PRIME - 1) % N == 0 and PRIME % N != 0)
        omega = pow(GENERATOR, (PRIME - 1) // N, PRIME)
        ck("PRIMITIVE_ROOT_" + str(N), pow(omega, N, PRIME) == 1 and all(
            pow(omega, N // q, PRIME) != 1 for q in sp.factorint(N)))
        X = sp.symbols("X")
        phi = sp.Poly(sp.cyclotomic_poly(N, X), X)
        ck("CYCLOTOMIC_REDUCTION_" + str(N), int(phi.eval(omega)) % PRIME == 0)
        roots = [pow(omega, k, PRIME) for k in range(N)]
        counts, genuine, distinct = Counter(), Counter(), Counter()
        digest = hashlib.sha256()
        for a in range(N):
            for b in range(N):
                for c in range(N):
                    ids = (a, b, c)
                    co = np.array([
                        roots[(a*d[0] + b*d[1] + c*d[2]) % N] for d in ds
                    ], dtype=np.int64)
                    M = np.remainder(np.einsum("d,dij->ij", co, terms), PRIME)
                    rank = nmod_mat(68, 96, M.reshape(-1).tolist(), PRIME).rank()
                    if rank != (65 if ids == (0, 0, 0) else 68):
                        raise AssertionError(("EXTRA_INTERIOR_RANK_DROP", N, ids, rank))
                    counts[rank] += 1
                    if all(ids):
                        genuine[rank] += 1
                    if len(set(ids + (0,))) == 4:
                        distinct[rank] += 1
                    digest.update(bytes(ids) + bytes([rank]))
        ck("ALL_THREE_RATIO_CHARACTERS_" + str(N),
           counts == {65: 1, 68: N**3-1}
           and genuine == {68: (N-1)**3}
           and distinct == {68: (N-1)*(N-2)*(N-3)})
        ck("RANK_LEDGER_" + str(N), digest.hexdigest() == expected)
        records.append({
            "period": N, "primitive_root_mod_prime": omega,
            "rank65_characters": 1, "rank68_characters": N**3-1,
            "all_three_ratios_nonunit": (N-1)**3,
            "all_four_characters_pairwise_distinct": (N-1)*(N-2)*(N-3),
            "interior_convolution_rank": 68*N**3-3,
            "interior_convolution_left_nullity": 3,
            "interior_convolution_right_nullity": 28*N**3+3,
            "rank_digest_sha256": digest.hexdigest(),
        })
    result = {
        "schema": "a4d-y-three-ratio-convolution-v1",
        "input": "literal z=1 Y joint stencil, phase-1/2 interior rows",
        "zone_variables": "lambda_j=mu*rho_j, rho0=1, w=mu^4",
        "interior_shape": [68, 96], "denominator_clearing": 14,
        "good_prime": PRIME, "field_generator": GENERATOR,
        "records": records,
        "conclusion": "on these finite complex character tori only (1,1,1) drops interior rank",
        "scope": [
            "nonzero modular maximal minors certify characteristic-zero ranks at these roots",
            "no continuous three-ratio or full joint compact-complement theorem",
            "full-row-rank interior still has right nullity 28 off the fold",
            "no exact curved joint field, rescue estimate, or metric response terminal",
        ],
    }
    if write:
        OUT.write_text(json.dumps(result, indent=2) + "\n")
        print("WROTE", OUT, flush=True)
    else:
        ck("RESULTS_MATCH_PINNED_JSON", json.loads(OUT.read_text()) == result)
    print("PASS_THREE_RATIO_FINITE_CONVOLUTION", flush=True)


if __name__ == "__main__":
    run("--write" in sys.argv)
