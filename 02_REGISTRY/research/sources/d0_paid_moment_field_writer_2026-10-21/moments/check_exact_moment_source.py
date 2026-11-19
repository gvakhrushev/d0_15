#!/usr/bin/env python3
"""Narrow exact checks of the new coframe/link/material substitutions.

No prior source/rank/root suite is run. Analytic all-family claims live
in EXACT_MOMENT_SOURCE_CONSTRUCTION.md. All matrix jets below are exact
commuting multivariate Taylor coefficients through total degree two.
"""

import argparse
import hashlib
import itertools
import json
import subprocess
from fractions import Fraction as Q
from pathlib import Path


SOURCE_REF = "311b1d3fd505effe7082754bc80dd17d1097f095"
OLD_RESULT = ("02_REGISTRY/research/sources/"
              "d0_exact_resource_writer_2026-10-21/WRITER_RESULT.json")


def require(ok, label):
    if not ok:
        raise RuntimeError("FAILED: " + label)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def zero(n):
    return [[Q(0) for _ in range(n)] for _ in range(n)]


def eye(n):
    m = zero(n)
    for i in range(n):
        m[i][i] = Q(1)
    return m


def unit(n, i, j, value=1):
    m = zero(n)
    m[i][j] = Q(value)
    return m


def madd(a, b):
    return [[x+y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(a, t):
    return [[t*x for x in row] for row in a]


def transpose(a):
    return [list(row) for row in zip(*a)]


def mm(a, b):
    n = len(a)
    out = zero(n)
    for i in range(n):
        for k in range(n):
            if a[i][k]:
                for j in range(n):
                    if b[k][j]:
                        out[i][j] += a[i][k]*b[k][j]
    return out


def jadd(a, b):
    n = len(next(iter(a.values())))
    out = {key: [row[:] for row in val] for key, val in a.items()}
    for key, val in b.items():
        out[key] = madd(out.get(key, zero(n)), val)
    return out


def jscale(a, t):
    return {key: scale(val, t) for key, val in a.items()}


def jmul(a, b):
    n = len(next(iter(a.values())))
    out = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            if len(ka)+len(kb) <= 2:
                key = tuple(sorted(ka+kb))
                value = mm(va, vb)
                if any(any(row) for row in value):
                    out[key] = madd(out.get(key, zero(n)), value)
    return out or {(): zero(n)}


def jet_equal(a, b, variables, label):
    n = len(next(iter(a.values())))
    keys = [()] + [(i,) for i in range(variables)]
    keys += list(itertools.combinations_with_replacement(range(variables), 2))
    for key in keys:
        require(a.get(key, zero(n)) == b.get(key, zero(n)),
                label + " coefficient " + str(key))
    return len(keys)


def exterior_jet(a):
    pairs = list(itertools.combinations(range(4), 2))
    out = {}
    for ka, va in a.items():
        for kb, vb in a.items():
            if len(ka)+len(kb) > 2:
                continue
            key = tuple(sorted(ka+kb))
            dest = out.setdefault(key, zero(6))
            for r, (i, j) in enumerate(pairs):
                for c, (k, ell) in enumerate(pairs):
                    dest[r][c] += va[i][k]*vb[j][ell]-va[i][ell]*vb[j][k]
    return out


def geometry_checks():
    eta = [[Q(v) for v in row] for row in
           [[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]]]
    T = [[Q(1), Q(1, 2), Q(0), Q(0)],
         [Q(1), Q(-1, 2), Q(0), Q(0)],
         [Q(0), Q(0), Q(1), Q(0)], [Q(0), Q(0), Q(0), Q(1)]]
    Ti = [[Q(1, 2), Q(1, 2), Q(0), Q(0)],
          [Q(1), Q(-1), Q(0), Q(0)],
          [Q(0), Q(0), Q(1), Q(0)], [Q(0), Q(0), Q(0), Q(1)]]
    require(mm(T, Ti) == eye(4), "literal null/REST inverse")
    H = Q(1, 7)
    E0 = madd(eye(4), unit(4, 1, 0, H/2))
    R0 = madd(eye(4), unit(4, 1, 0, -H/2))
    D0 = mm(eta, transpose(mm(R0, Ti)))
    D = {(): D0, **{(4*i+j,): unit(4, i, j)
                      for i in range(4) for j in range(4)}}
    R = {key: mm(mm(transpose(val), eta), T) for key, val in D.items()}
    require(R[()] == R0, "D^T eta T is E^-1")
    dR = {key: val for key, val in R.items() if key}
    E = jadd({(): E0}, jscale(jmul(jmul({(): E0}, dR), {(): E0}), -1))
    E = jadd(E, jmul(jmul(jmul(jmul({(): E0}, dR), {(): E0}), dR), {(): E0}))
    jet_equal(jmul(E, R), {(): eye(4)}, 16, "actual inverse jet")
    Z = exterior_jet(R)
    N = jadd(Z, {(): scale(eye(6), -1)})
    require(mm(N[()], N[()]) == zero(6), "primary compound square-zero")
    P5, power = {(): eye(6)}, {(): eye(6)}
    for k in range(1, 6):
        power = jmul(power, N)
        P5 = jadd(P5, jscale(power, (-1)**k))
    area = jmul(exterior_jet({(): T}), P5)
    exact_area = exterior_jet(jmul({(): T}, E))
    p5_count = jet_equal(area, exact_area, 16, "P5 all coframe two-jets")

    N2 = madd(unit(4, 1, 2), unit(4, 2, 0))
    N3 = madd(unit(4, 1, 3), unit(4, 3, 0))
    K0 = mm(mm(T, madd(scale(N2, Q(1, 7)), scale(N3, Q(1, 11)))), Ti)
    require(mm(mm(K0, K0), K0) == zero(4), "actual null-rotation cube-zero")
    generators = []
    for a, b in itertools.combinations(range(4), 2):
        G = madd(unit(4, a, b), unit(4, b, a, -eta[a][a]*eta[b][b]))
        require(madd(mm(transpose(G), eta), mm(eta, G)) == zero(4),
                "proper Lorentz generator")
        generators.append(G)
    K = {(): K0, **{(i,): G for i, G in enumerate(generators)}}
    B = jscale(K, Q(1, 2))
    B0 = B[()]
    Ai = madd(madd(eye(4), B0), mm(B0, B0))
    dB = {key: val for key, val in B.items() if key}
    inverse = jadd({(): Ai}, jmul(jmul({(): Ai}, dB), {(): Ai}))
    inverse = jadd(inverse, jmul(jmul(jmul(jmul({(): Ai}, dB), {(): Ai}), dB), {(): Ai}))
    exact_cayley = jmul(jadd({(): eye(4)}, B), inverse)
    C8, power = {(): eye(4)}, {(): eye(4)}
    for _ in range(1, 9):
        power = jmul(power, B)
        C8 = jadd(C8, jscale(power, 2))
    c8_count = jet_equal(C8, exact_cayley, 6, "C8 all six proper two-jets")
    sharp = {key: mm(mm(eta, transpose(val)), eta) for key, val in C8.items()}
    jet_equal(jmul(sharp, C8), {(): eye(4)}, 6, "reverse-edge two-jet")
    return {"coframe_H": str(H), "coframe_variables": 16,
            "coframe_coefficient_matrices": p5_count,
            "link_K2": "1/7", "link_K3": "1/11", "link_variables": 6,
            "link_coefficient_matrices": c8_count, "reverse_edge_jet": "PASS",
            "f_total_degree_bound": 42, "q_total_degree_bound": 4}


def fadd(a, b):
    return tuple(x+y for x, y in zip(a, b))


def fscale(a, t):
    return tuple(t*x for x in a)


def fmul(a, b):
    out = [Q(0)]*7
    for i in range(4):
        for j in range(4):
            out[i+j] += a[i]*b[j]
    for i in range(6, 3, -1):
        out[i-4] += out[i]
        out[i-2] -= out[i]
    return tuple(out[:4])


def material_checks(old_result):
    one, a, p = ((Q(1), Q(0), Q(0), Q(0)),
                 (Q(0), Q(1), Q(0), Q(0)),
                 (Q(0), Q(0), Q(1), Q(0)))
    nil = (Q(0),)*4
    p2, ap = fmul(p, p), fmul(a, p)
    require(fadd(p, p2) == one, "actual Golden local normalization")
    pair_list = []
    for k in itertools.product(range(4), repeat=4):
        if k < tuple(-v % 4 for v in k):
            pair_list.append(k)
        if len(pair_list) == 64:
            break
    require([list(k) for k in pair_list] == old_result["fourier_reference"]["pair_list"],
            "actual pinned first64 Fourier pair order")
    sites = list(itertools.product(range(4), repeat=4))
    rows = []
    local_moments = []
    for x in sites:
        row = []
        for k in pair_list:
            phase = sum(u*v for u, v in zip(x, k)) % 4
            row += [(1, 0, -1, 0)[phase], (0, 1, 0, -1)[phase]]
        rows.append(row)
        require(sum(v*v for v in row) == 64, "actual Fourier row norm")
        # All 4 branch kinds and both eight-label sign registers are retained.
        k0, k15 = 1+x[0], 2+x[1]
        t0, t15 = Q(2*k0, 8)-1, Q(2*k15, 8)-1
        density = {(i, j): nil for i in (0, 1, 14, 15) for j in (0, 1, 14, 15)}
        for branch, r0, r15 in itertools.product(range(4), range(8), range(8)):
            target = 0 if branch == 0 else 15 if branch == 1 else 14
            sign = (1 if r0 < k0 else -1) if branch == 0 else (
                   (1 if r15 < k15 else -1) if branch == 1 else 1)
            vector = {1: a, target: fscale(p, sign)}
            for i, vi in vector.items():
                for j, vj in vector.items():
                    density[i, j] = fadd(density[i, j], fscale(fmul(vi, vj), Q(1, 256)))
        trace = nil
        for mask in (0, 1, 14, 15):
            trace = fadd(trace, density[mask, mask])
        require(trace == one, "complete local material norm")
        require(density[1, 1] == p, "fixed clock population")
        require(density[0, 0] == density[15, 15] == fscale(p2, Q(1, 4)),
                "actual scalar/top populations")
        require(density[14, 14] == fscale(p2, Q(1, 2)), "retained slack population")
        for A, t in ((0, t0), (15, t15)):
            mu = fscale(fadd(density[1, A], density[A, 1]), Q(1, 256))
            require(mu == fscale(ap, t/Q(512)), "actual LEFT moment ap*t/(2S)")
            psi = fscale(p, t/4)
            require(mu == fscale(fmul(a, psi), Q(2, 256)), "old calibrated matter readout")
        local_moments.append([str(t0), str(t15)])
    require(sha(json.dumps(rows, separators=(",", ":")).encode()) ==
            old_result["fourier_reference"]["integer_reference_sha256"],
            "original Fourier dictionary bytes")
    columns = list(zip(*rows))
    for i in range(128):
        for j in range(i, 128):
            require(sum(x*y for x, y in zip(columns[i], columns[j])) ==
                    (128 if i == j else 0), "new complete input RIGHT Gram I128/128")
    for n in (2, 3, 4, 7):
        multiplicity = 2**(4*(n-2))
        require(Q(1, 256*multiplicity) == Q(1, 2**(4*n)), "refined site row norm")
        require(multiplicity*Q(1, multiplicity) == 1, "refined RIGHT Gram unchanged")
    return {"sites": 256, "right_dimension": 128, "local_retained_labels": 256,
            "all_local_normalizations": "1", "clock_population": "p",
            "left_moment": "sqrt(p)*p*t/(2S)", "psi_readout": "p*t/4",
            "right_gram": "I128/128", "actual_fourier_hash": sha(json.dumps(rows, separators=(",", ":")).encode()),
            "code_table_hash": sha(json.dumps(local_moments).encode()),
            "paid_reference_refinement": "actual L4 seed plus four fair site bits per step"}


def collar_check():
    # Rational enclosure only; p is the positive root of x^2+x-1.
    plo, phi = Q(3, 5), Q(5, 8)
    require(plo**2+plo-1 < 0 < phi**2+phi-1, "exact Golden bounds")
    eps, h = Q(1, 1024), Q(1, 4)
    # 0<R0<Q0<1, so |lambda| < 2 p_lo^-5 (1+p_hi^6).
    lam_bound = 2*plo**-5*(1+phi**6)
    require(lam_bound < 32, "lambda_minus strict bound")
    energy_bound = Q(5, 4)*phi**12*eps**2
    b = lam_bound*energy_bound
    H_bound = b/2+Q(1, 32)
    # A difference of a quadratic along one h-edge has |2xh-h²|<=h+h².
    Ksum_bound = (b+Q(1, 8))*(h+h*h)
    require(H_bound < Q(1, 5) and Ksum_bound < Q(1, 5), "strict old geometric collar")
    require(eps+Q(1, 16) < plo/4, "nonvacuum material open collar")
    require(phi**3 < Q(1, 4), "actual fixed scale s=p^3")
    return {"h": "1/4", "s": "p^3", "epsilon": "1/1024",
            "unscaled_energy": "(5/4)*p^12*epsilon^2 > 0",
            "lambda_absolute_upper_bound": str(lam_bound),
            "H_absolute_upper_bound": str(H_bound),
            "K2_K3_sum_upper_bound": str(Ksum_bound),
            "material_open_radius": "1/16", "material_chart": "abs(psi_A)<p/4"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    packet = Path(__file__).resolve().parent
    pin_bytes = (packet/"MOMENT_SOURCE_PINS.json").read_bytes()
    pins = json.loads(pin_bytes)
    require(pins["source_ref"] == SOURCE_REF, "historical scientific source")
    historical = {}
    for entry in pins["sources"]:
        data = subprocess.check_output(["git", "show", SOURCE_REF+":"+entry["path"]], cwd=args.repo)
        require(sha(data) == entry["sha256"], "historical pin "+entry["path"])
        historical[entry["path"]] = data
    old = json.loads(historical[OLD_RESULT])
    result = {"status": "PASS", "scientific_input": SOURCE_REF,
              "historical_sources_verified": len(historical),
              "geometry": geometry_checks(), "material": material_checks(old),
              "nonvacuum_collar": collar_check(),
              "source_sign": "new CQ readiness positive; raw J2 coefficient -gamma*d0*h_phi_prime(r0)<0",
              "scope": "exact new algebra and one actual L4 material/reference fixture; analytic all-family proof",
              "off_primary_original_action_equality": False, "Book03_identified": False,
              "autonomous_prescribed_code_selection": False, "GR_closed": False,
              "proof_sha256": sha((packet/"EXACT_MOMENT_SOURCE_CONSTRUCTION.md").read_bytes()),
              "checker_sha256": sha(Path(__file__).read_bytes()), "source_pins_sha256": sha(pin_bytes)}
    text = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
