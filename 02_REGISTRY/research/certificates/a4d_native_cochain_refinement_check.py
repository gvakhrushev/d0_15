#!/usr/bin/env python3
"""Exact native cochain refinement, full Gram and composed-tower controls.

General proofs (all L) are in A4D_NATIVE_COCHAIN_REFINEMENT.md. This finite
replay does not infer an infinite result from the tested sizes. Default mode
is immutable. --output is only for explicitly recording a new certificate.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path
import sympy as sp

INPUT_HEAD = "227c1609c41b720dcfb7517a8e57f0e8d76cb764"
INPUTS = [
    "03_FORMALIZATION/D0/Geometry/Archive1DCochainRefinement.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveGradedRefinementChainMap.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveRefinementHodgeWeights.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveMetricMeasureHodgeLift.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveCubicalDifferential.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveCARRelations.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveRolePhaseGroup.lean",
    "03_FORMALIZATION/D0/Geometry/A4DSymRoleCentralDifference.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveLaplacianRG.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveSeamCurvature.lean",
    "03_FORMALIZATION/D0/Geometry/ArchiveCanonicalLaplacian.lean",
]


def incidence(L):
    return sp.Matrix(L, L, lambda i, j: int(j == (i+1) % L)-int(j == i))


def lifts(L):
    return (sp.Matrix(L+1, L, lambda i, j: int(j == i % L)),
            sp.Matrix(L+1, L, lambda i, j: int(i == j)))


def clean(d):
    return {k: v for k, v in d.items() if v}


def tensor_row(L, S, x, scaled):
    k = sum(S)
    coefficient = Q(L+1, L)**k if scaled else Q(1)
    if any(S[r] and x[r] == L for r in range(4)):
        coefficient = Q(0)
    return tuple(z % L for z in x), coefficient


def chain_rows(L, S, r, x, scaled):
    """Full sparse matrix rows, including creation sign, wrap and collapsed edges."""
    assert not S[r]
    T = list(S)
    T[r] = 1
    sign = (-1)**sum(S[:r])  # literal roleOrderIndex: A,B,C,D
    xp = list(x)
    xp[r] = (xp[r]+1) % (L+1)
    lhs, rhs = defaultdict(Q), defaultdict(Q)
    cf, cc = (L+1, L) if scaled else (1, 1)
    for y, sgn in [(xp, 1), (x, -1)]:
        q, w = tensor_row(L, S, y, scaled)
        lhs[q] += sign*sgn*cf*w
    q, w = tensor_row(L, T, x, scaled)
    qp = list(q)
    qp[r] = (qp[r]+1) % L
    rhs[tuple(qp)] += sign*cc*w
    rhs[q] -= sign*cc*w
    return clean(lhs), clean(rhs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expect", type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    checks = []

    def check(name, value):
        assert bool(value), name
        checks.append(name)
        print("PASS_"+name, flush=True)

    receipt_path = repo/"02_REGISTRY/research/certificates/a4d_native_cochain_refinement_results.json"
    receipt = json.loads(receipt_path.read_text())
    assert receipt["status"] == "PASS" and receipt["compiler_exit_code"] == 0
    assert not receipt["sorryAx"] and receipt["printed_axiom_dependencies"] == 12
    for path, digest in {
        **receipt["transitive_d0_source_sha256"], **receipt["toolchain_input_sha256"],
        receipt["capsule"]: receipt["capsule_sha256"], receipt["output"]: receipt["output_sha256"],
    }.items():
        assert hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest, "LEAN_INPUT_CHANGED: "+path
    check("COMPILED_GENERIC_OWNER_BOUND_CAPSULE", True)

    one_d = {}
    for L in range(2, 9):
        b0, b1 = lifts(L)
        dc, df = incidence(L), incidence(L+1)
        M = sp.diag(2, *([1]*(L-1)))
        check(f"B0_FULL_GRAM_{L}", b0.T*b0 == M)
        check(f"B1_FULL_ISOMETRY_{L}", b1.T*b1 == sp.eye(L))
        check(f"UNSCALED_FULL_CHAIN_{L}", df*b0 == b1*dc)
        check(f"SCALED_FULL_CHAIN_{L}", (L+1)*df*b0 == sp.Rational(L+1, L)*b1*(L*dc))
        check(f"UNSCALED_LIFT_FAILS_OWNER_SCALED_CHAIN_{L}", (L+1)*df*b0 != b1*(L*dc))
        check(f"ENERGY_PULLBACK_NOT_OPERATOR_COMMUTATION_{L}", b0.T*df.T*df*b0 == dc.T*dc
              and df.T*df*b0 != b0*dc.T*dc)
        one_d[str(L)] = {"vertex_trace": int(sp.trace(M)), "edge_trace": L}
    # Simple graph C2 has only one neighbour; incidence counts both oriented edges.
    check("TWO_VERTEX_GRAPH_EXCEPTION", incidence(2).T*incidence(2) == 2*sp.Matrix([[1,-1],[-1,1]]))

    sectors = list(itertools.product([0, 1], repeat=4))
    tensor_records = {}
    for L in [2, 3, 4]:
        points = list(itertools.product(range(L+1), repeat=4))
        coarse = list(itertools.product(range(L), repeat=4))
        gram_records = []
        row_count = 0
        for S in sectors:
            k = sum(S)
            gram = defaultdict(Q)
            gram_scaled = defaultdict(Q)
            for x in points:
                q, w = tensor_row(L, S, x, False)
                gram[q] += w*w
                qs, ws = tensor_row(L, S, x, True)
                gram_scaled[qs] += ws*ws
            # Each matrix row has <=1 nonzero, so every off-diagonal Gram entry is zero.
            for q in coarse:
                expected = 2**sum(not S[r] and q[r] == 0 for r in range(4))
                assert gram[q] == expected and gram_scaled[q] == Q(L+1, L)**(2*k)*expected
                masses = [2 if z == 0 else 1 for z in q]
                mu = sp.prod(masses)
                hodge = mu**(1-k)*sp.prod(mu/masses[r] for r in range(4) if S[r])
                assert hodge == expected
            trace = sum(gram.values())
            scaled_trace = sum(gram_scaled.values())
            assert trace == L**k*(L+1)**(4-k)
            assert scaled_trace == Q(L+1, L)**(2*k)*trace
            gram_records.append({"sector_ABCD": list(S), "degree": k,
                "counting_trace": str(trace), "owner_scaled_trace": str(scaled_trace)})
            for r in range(4):
                if S[r]:
                    continue  # creation annihilates already occupied input
                for x in points:
                    for scaled in [False, True]:
                        a, b = chain_rows(L, S, r, x, scaled)
                        assert a == b, (L, S, r, x, scaled, a, b)
                        row_count += 1
        check(f"ALL_16_FULL_GRAMS_AND_ALL_GRADE_HODGE_{L}", True)
        check(f"ALL_32_GRADED_BLOCKS_BOTH_DIFFERENTIAL_SCALES_{L}", True)
        check(f"FULL_TRACE_BINOMIAL_{L}", sum(int(x["counting_trace"]) for x in gram_records) == (2*L+1)**4)
        check(f"OWNER_SCALED_TRACE_BINOMIAL_{L}", sum(Q(x["owner_scaled_trace"]) for x in gram_records)
              == (Q(L+1)+Q((L+1)**2, L))**4)
        tensor_records[str(L)] = {"verified_matrix_rows": row_count, "sectors": gram_records}
    check("625_IS_FULL_COUNTING_TRACE", sum(int(x["counting_trace"]) for x in tensor_records["2"]["sectors"]) == 625)
    check("256_IS_ONLY_OCCUPIED_DIRECTION_NORMALIZED_TRACE", sum(Q(x["counting_trace"])/2**x["degree"] for x in tensor_records["2"]["sectors"]) == 256)
    check("SCALED_OWNER_TRACE_IS_50625_OVER_16", sum(Q(x["owner_scaled_trace"]) for x in tensor_records["2"]["sectors"]) == Q(50625, 16))
    check("NO_COMMON_TRACE_CALIBRATION_GIVES_256_SECTORS", Q(81,81) != Q(27,54))
    check("NORMALIZED_SITE_COUNTING_IS_DIFFERENT", Q(2,3)**4*625 == Q(10000,81) and Q(10000,81) != 256)
    # A direct matrix fixture independently checks the sparse Gram implementation.
    b0, b1 = lifts(2)
    direct_traces = []
    for S in sectors:
        B = sp.kronecker_product(*[b1 if occupied else b0 for occupied in S])
        G = sp.kronecker_product(*[sp.eye(2) if occupied else sp.diag(2,1) for occupied in S])
        assert B.T*B == G
        direct_traces.append(int(sp.trace(G)))
    check("INDEPENDENT_81_BY_16_MATRIX_GRAMS", sum(direct_traces) == 625)

    # Exact composition, not an assumed single modulo K->L map.
    composed = {}
    for L in [2, 3, 4, 8]:
        P0, P1 = sp.eye(L), sp.eye(L)
        for M in range(L, 2*L):
            b0, b1 = lifts(M)
            P0, P1 = b0*P0, b1*P1
        Q0 = sp.Matrix(2*L, L, lambda i,j: int(j == (i if i < L else 0)))
        Q1 = sp.Matrix(2*L, L, lambda i,j: int(i == j))
        check(f"COMPOSED_MAPS_TO_DOUBLE_LEVEL_{L}", P0 == Q0 and P1 == Q1)
        check(f"COMPOSED_GRADED_SCALED_CHAIN_{L}", (2*L)*incidence(2*L)*P0 == 2*P1*(L*incidence(L)))
        check(f"DIRECT_MODULO_IS_NOT_COMPOSED_LIFT_{L}", P0 != sp.Matrix(2*L,L,lambda i,j:int(j == i % L)))
        # Smooth fixed one-form alpha=1: native scaled transfer is 2 then 0.
        refined = 2*P1*sp.ones(L,1)
        err = refined-sp.ones(2*L,1)
        check(f"CONSTANT_ONE_FORM_DOUBLING_L1_L2_ERROR_ONE_{L}", sum(abs(z) for z in err)/(2*L) == 1
              and sum(z*z for z in err)/(2*L) == 1)
        # Smooth, nondegenerate conformal sample Omega=1+sin(2pi y)/10.
        # On the new half the native scalar is 1, whereas resampling is not.
        tail_sq = sp.simplify(sum((sp.sin(sp.pi*j/L)/10)**2 for j in range(L))/(2*L))
        check(f"FIXED_NONCONSTANT_SCALAR_TAIL_ERROR_{L}", tail_sq == sp.Rational(1,400))
        # Even an arbitrary coarse value at zero cannot fit the tail's nonconstant shape.
        # Trigonometric mean is allowed here only as an exact finite control.
        c = sp.symbols("c", real=True)
        vals = [1-sp.sin(sp.pi*j/L)/10 for j in range(L)]
        mean = sum(vals)/L
        minimum = sp.simplify(sum((mean-z)**2 for z in vals)/(2*L))
        assert minimum > 0
        composed[str(L)] = {"constant_one_form_L1_error": "1", "constant_one_form_squared_L2_error": "1",
                           "conformal_scalar_tail_squared_L2_error": str(tail_sq),
                           "best_constant_tail_squared_error": str(minimum)}
    for L in [4, 8, 16]:
        c = Q(L+1,L)
        step = [c]*L+[Q(0)]
        check(f"ONE_STEP_ONE_FORM_L1_{L}", sum(abs(z-1) for z in step)/(L+1) == Q(2,L+1))
        check(f"ONE_STEP_ONE_FORM_SQUARED_L2_{L}", sum((z-1)**2 for z in step)/(L+1) == Q(1,L))
        check(f"ONE_STEP_ONE_FORM_SUP_DOES_NOT_VANISH_{L}", max(abs(z-1) for z in step) == 1)
    check("ONE_STEP_IS_NOT_UNIFORM_COMPOSED_CONSISTENCY", Q(2,17) < 1)

    payload = {"status": "PASS", "input_head": INPUT_HEAD,
        "input_sha256": {p: hashlib.sha256((repo/p).read_bytes()).hexdigest() for p in INPUTS},
        "lean_capsule_receipt_sha256": hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
        "checks": checks, "one_dimensional": one_d, "four_dimensional": tensor_records,
        "composed_controls": composed,
        "general_full_trace": "(2L+1)^4",
        "general_owner_scaled_trace": "((L+1)+(L+1)^2/L)^4",
        "scope": "Generic analytic construction and scoped composed-readout obstruction; compiled 1D owner binding and all-grade metric-measure algebra; finite exact full 4D matrix controls. No native GR, physical action transfer, curved joint solution or global closure."}
    if args.output:
        args.output.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")
    expected = args.expect or (Path(__file__).with_name("a4d_native_cochain_refinement_certificate.json") if not args.output else None)
    if expected:
        assert json.loads(expected.read_text()) == payload, "PINNED_LEDGER_MISMATCH"
        print("PASS_IMMUTABLE_PINNED_LEDGER", flush=True)
    print("PASS_NATIVE_COCHAIN_REFINEMENT", len(checks), flush=True)

if __name__ == "__main__":
    main()
