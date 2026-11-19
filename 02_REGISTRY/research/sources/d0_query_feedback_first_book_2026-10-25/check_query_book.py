#!/usr/bin/env python3
"""Bounded all-column/full-source checks for the original feedback-first query.

Small N clocks enumerate EVERY root with exact scene multiplicities. The
large recovery schedule is checked with rational inequalities, not unrolled.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import mpmath as mp
import sympy as sp
import query_book as qb

SOURCES = Path(__file__).resolve().parent.parent
DOMAIN = SOURCES / "d0_native_execution_domain_2026-10-24"
sys.path.insert(0, str(DOMAIN))
import native_execution as ne
from check_native_execution_domain import Quadratic

CHECKS = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    CHECKS.append(name)


def trace(a):
    return mp.fsum(a[i, i] for i in range(a.rows))


def maxnorm(a):
    return max(abs(v) for v in a)


def matrix_numeric(a):
    return mp.matrix([[mp.mpf(str(sp.N(a[i, j], 80)))
                       for j in range(a.cols)] for i in range(a.rows)])


def paired_partition(matrix, N, beta):
    phases = [mp.arg(v) for v in mp.eig(matrix, left=False, right=False)]
    return 2*mp.fsum(mp.exp(-beta*(1-mp.cos((t+2*mp.pi*k)/N)))
                    for t in phases for k in range(N))


def run():
    mp.mp.dps = 70
    tol = mp.mpf("1e-50")
    p, zeta = qb.golden(), mp.mpf(2)**-20
    beta = mp.mpf(1)
    projector = mp.diag([1, 0, 1, 0, 0, 0, 0, 0])
    cx = mp.matrix([[1, 0, 0, 0], [0, 1, 0, 0],
                    [0, 0, 0, 1], [0, 0, 1, 0]])
    for x, y in ((mp.mpf(0), mp.mpf(0)), (mp.mpf(".03"), mp.mpf("-.02"))):
        E, e = p*p*(1+x), qb.angles(x, y)[0]
        t, u8 = qb.tail(E), qb.query(x, y)
        check(f"literal complete T4 equals CX times R tensor I at x={x}",
              maxnorm(t-cx*qb.kron(qb.rotation(e), mp.eye(2))) < tol)
        check(f"complete query and unmatched tail are orthogonal on all columns at x={x}",
              maxnorm(u8.T*u8-mp.eye(8)) < tol and maxnorm(t.T*t-mp.eye(4)) < tol)
        f = projector*u8.T*(mp.eye(8)-projector)*u8*projector
        a, b = qb.bands(x, y)
        eigenvalues = sorted(mp.eigsy(f, eigvals_only=True))
        check(f"actual fixed rank2 cut has exactly A B and six zero bands at x={x}",
              max(abs(v-w) for v, w in zip(eigenvalues, sorted([0]*6+[a, b]))) < tol
              and trace(projector) == 2)
        check(f"actual all8 return determinant equals the two-band feedback at x={x}",
              abs(-mp.log(mp.det(mp.eye(8)-zeta*f))-qb.feedback(x, y, zeta)) < tol)
        for N in (6, 10, 14, 20):
            z8, z4 = qb.partitions(x, y, N, beta)
            check(f"ALL roots of literal8 and unmatched4 spectra give full partitions x={x} N={N}",
                  abs(z8-paired_partition(u8, N, beta)) < tol
                  and abs(z4-paired_partition(t*t, N, beta)) < tol)
    # The local configured value is a literal six-stage G/CX word; padding
    # is actual even CX pairs. This is NOT six global native stages for the
    # entire 22976-scene direct sum, whose addressed compilation is separate.
    gates = (ne.Gate("G", (0,)), ne.Gate("CX", (0, 1)),
             ne.Gate("G", (0,)), ne.Gate("CX", (0, 1)),
             ne.Gate("G", (2,)), ne.Gate("G", (2,)))
    local = ne.Execution(3, (0, 2), (), gates)
    base = ne.word_matrix(local)
    check("six actual local G/CX stages reproduce the configured full8 query on every column",
          maxnorm(matrix_numeric(base)-qb.query(0, 0)) < tol)
    check("literal native input blanks give the same rank2 computational return cut",
          ne.cut_projector(local) == sp.diag(1, 0, 1, 0, 0, 0, 0, 0))
    bounds = dict(max_qubits=3, max_expanded_stages=100)
    for N in (6, 10, 14, 20):
        padding = (ne.Gate("CX", (0, 1)),)* (N-6)
        padded = ne.Execution(3, (0, 2), (), gates+padding)
        inventory = ne.inventory(padded, **bounds)
        check(f"literal even identity padding preserves all local columns and actual stage count N={N}",
              inventory.gate_count == N and inventory.g_count == 4
              and ne.exact_matrix_equal(ne.word_matrix(padded), base))
    rows = []
    # Unequal integer address multiplicities check the global logheat,
    # not a sum of independent local heat prices or a normalized address mean.
    counts, zero = (1, 2), ((mp.mpf(0), mp.mpf(0)),)*2
    copies = sum(counts)
    eps = mp.mpf("1e-16")
    for N in (6, 10, 14, 20):
        c = qb.source_coefficients(N, beta, copies, zeta)
        for address in range(2):
            for axis, coefficient in ((0, "aN"), (1, "bN")):
                def value(step):
                    operands = [list(t) for t in zero]
                    operands[address][axis] = step
                    return qb.price(operands, counts, N, beta, zeta)
                fd = (value(eps)-value(-eps))/(2*eps)
                check(f"global complete H plus J source matches independent address derivative N={N} address={address} axis={axis}",
                      abs(fd-counts[address]*c[coefficient]) < mp.mpf("1e-27"))
        z8, z4 = qb.partitions(0, 0, N, mp.mpf(0))
        modes = copies*(qb.ACTIVE*z8+qb.UNMATCHED*z4)
        check(f"ALL full4 times22976scene paired modes retained N={N}",
              modes == 2*N*4*22976*copies and modes == 2*N*91904*copies)
        # Incorrectly deleting unmatched columns changes the thermal source.
        theta = mp.asin(p)
        only_active = 4*mp.sqrt(p)*qb.character(4*theta, N, beta, True)/(beta*copies*qb.partitions(0, 0, N, beta)[0])
        check(f"hostile omitted-unmatched heat gives a different source N={N}",
              abs(c["unmatched_hx"]) > mp.mpf("1e-40")
              and abs(c["hx"]-only_active) > mp.mpf("1e-40"))
        rows.append({"N": N, "beta": "1", "copies": copies,
                     **{name: mp.nstr(value, 32) for name, value in c.items()},
                     "paired_modes": int(modes)})
    # Exact rational sufficient source budget; no large clock is evaluated.
    q, plo, phi = Quadratic(0, 1), Fraction(309, 500), Fraction(619, 1000)
    zz = Fraction(1, 2**20)
    check("exact Golden p lies strictly between309/500 and619/1000",
          (q-plo).sign() > 0 and (phi-q).sign() > 0)
    lower_jx = 4*zz*plo**11
    upper_ratio = 2*(1+phi**6)/plo**5
    budget = 52/(qb.ACTIVE*lower_jx)
    r, qden = 1-zz+zz*q**12, 1-zz+zz*q**6
    check("exact rational bounds give jx lower calibration and absolute lambda0 less than24",
          lower_jx > 0 and upper_ratio < 24
          and r.sign() > 0 and (1-r).sign() > 0 and (qden-r).sign() > 0
          and (4*zz*q**11-lower_jx*r).sign() > 0)
    check("exact source-recovery coefficient is strictly smaller than2^23",
          budget < 2**23)
    schedules = []
    for L in (2, 3, 4, 8, 16):
        N = 2**23*L*L
        check(f"actual integer even padding schedule controls aN sign and lambda error below h squared L={L}",
              N % 2 == 0 and N >= 6 and Fraction(2, N) < qb.ACTIVE*lower_jx
              and Fraction(2, N) < qb.ACTIVE*8*zz*plo**6
              and budget/N < Fraction(1, L*L))
        schedules.append({"L": L, "h": f"1/{L}", "N": N,
                          "lambda_error_strict_upper": str(budget/N), "target_h_squared": str(Fraction(1, L*L))})
    return {"checks": CHECKS, "checks_passed": len(CHECKS), "rows": rows,
            "recovery_schedule": schedules, "exact_recovery_constant": str(budget),
            "scene": {"matched_pairs": qb.ACTIVE, "unmatched_columns": qb.UNMATCHED,
                      "tail_dimension": 4, "scene_dimension": 22976, "per_copy_dimension": 91904,
                      "fixed_feedback_rank_per_matched_pair": 2},
            "source_convention": "address j gradient is count_j*(aN,bN); heat denominator includes all copies once",
            "matrix_scope": "literal local8/local4 and ALL smallN roots only; full22976scene trace by exact multiplicities",
            "numeric_arithmetic": "70-digit mpmath non-interval; exact native/Q(p)/Fraction controls separate",
            "six_native_stages_for_entire_original_scene_claimed": False,
            "large_N_clock_unrolled": False, "old_root_or_PASS42_replayed": False,
            "continuous_native_word_selector_proved": False, "full_physical_query_admission_proved": False,
            "physical_Cost_Info_binding_proved": False, "independent_controller_preparation_Euler_proved": False,
            "original_spatial_R_identified": False, "fixed_lambda_minus_collar_reused": False,
            "aperture_scope": "one common fixed tau_h per mesh; no variable tau_j source cancellation claimed",
            "GR_closed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    result.update(schema="d0.query-feedback-first-book-check/1", status="PASS")
    repo = SOURCES.parents[2]
    paths = [Path(__file__).resolve(), Path(qb.__file__).resolve(), Path(__file__).with_name("PROOF.md"),
             DOMAIN/"native_execution.py", DOMAIN/"check_native_execution_domain.py",
             repo/"02_REGISTRY/research/sources/d0_physical_cap1_execution_composition_2026-10-21/moving_query/PROOF.md",
             repo/"02_REGISTRY/research/A4D_LOCAL_LEFT_CODED_CAR_NULL_MATTER_EINSTEIN_2026_10_18.md",
             repo/"02_REGISTRY/research/A4D_SAME_EXECUTION_SPATIAL_WEIGHTS_AND_COMPLETE_SOURCE_2026_10_21.md",
             repo/"02_REGISTRY/gr_assembly/sources/d0_double_null_quadratic_cartan_2026-10-19/arbitrary_brinkmann_all40.md",
             repo/"02_REGISTRY/research/A4D_EXACT_NONVACUUM_GR_MIDPOINT_C2_RECOVERY_2026_10_20.md"]
    result["inputs_sha256"] = {str(p.relative_to(repo)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    result["runtime"] = {"python": sys.version.split()[0], "mpmath": mp.__version__, "sympy": sp.__version__}
    text = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
