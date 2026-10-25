#!/usr/bin/env python3
"""Bounded clock-Rayleigh controls and the existing complete 7y application.

The small matrices are generic unitary controls, not admitted native pulses.
The long native example consumes its frozen Book receipt and phase helper;
it never rebuilds a 512-dimensional endpoint or a 14-million-mode clock.
"""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

import mpmath as mp

SOURCES = Path(__file__).resolve().parent.parent
WRITER = SOURCES / "d0_native_terminal_code_writer_2026-10-25"
sys.path.insert(0, str(WRITER))
import terminal_code_writer as tw
from check_native_execution_domain import Quadratic

CHECKS = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    CHECKS.append(name)


def tr(a):
    return mp.fsum(a[i, i] for i in range(a.rows))


def norm(a):
    return mp.sqrt(max(mp.mpf(0), max(mp.eighe(a.H*a, eigvals_only=True))))


def comm(a, b):
    return a*b-b*a


def derivative(function, u):
    value = function(u)
    return mp.matrix([[mp.diff(lambda v: function(v)[i, j], u)
                       for j in range(value.cols)] for i in range(value.rows)])


def clock(gates):
    n, d = len(gates), gates[0].rows
    shift = mp.zeros(n*d)
    for j, gate in enumerate(gates):
        for a in range(d):
            for b in range(d):
                shift[d*((j+1) % n)+a, d*j+b] = gate[a, b]
    return mp.eye(n*d)-(shift+shift.H)/2


def endpoint(gates):
    result = mp.eye(gates[0].rows)
    for g in gates:
        result = g*result
    return result


def principal(angle):
    return mp.arg(mp.exp(1j*angle))


def run():
    mp.mp.dps = 70
    tol = mp.mpf("1e-55")
    n, d, u = 5, 2, mp.mpf(".23")
    x = mp.matrix([[0, 1], [1, 0]])
    y = mp.matrix([[0, -1j], [1j, 0]])
    z = mp.diag([1, -1])
    pulse = lambda h, t: mp.cos(t)*mp.eye(2)+1j*mp.sin(t)*h
    def gates(v):
        return (pulse(z, v), pulse(x, mp.mpf(".4")+v/5),
                pulse(y, 13*v/100), pulse(z, mp.mpf(".17")),
                pulse(x, mp.mpf("-.11")))
    delta = clock(gates(u))
    dd = derivative(lambda v: clock(gates(v)), u)
    yp = derivative(lambda v: endpoint(gates(v)), u)
    speed = norm(yp)/n
    values, vectors = mp.eighe(delta)
    weights = [mp.mpf(n*d-j)/55 for j in range(n*d)]
    sigma = vectors*mp.diag(weights)*vectors.H
    source = mp.re(tr(sigma*dd))
    check("generic N5 d2 complete unitary clock is Hermitian and normalized occupation commutes",
          norm(delta-delta.H) < tol and abs(tr(sigma)-1) < tol
          and norm(comm(delta, sigma)) < tol)
    check("every stationary eigenvector Rayleigh source obeys endpoint speed divided by N",
          max(abs(mp.re((vectors[:, j].H*dd*vectors[:, j])[0]))
              for j in range(n*d)) <= speed+tol)
    check("full spectral-diagonal normalized occupation obeys the same source bound",
          abs(source) <= speed+tol)
    endpoint_phases = [mp.arg(v) for v in mp.eig(endpoint(gates(u)), left=False, right=False)]
    root_values = sorted(1-mp.cos((phase+2*mp.pi*j)/n)
                         for phase in endpoint_phases for j in range(n))
    check("all small-clock eigenvalues equal every endpoint phase root with no mode removed",
          max(abs(a-b) for a, b in zip(values, root_values)) < tol)
    check("minimum over all small-clock roots equals the principal-phase ground formula",
          abs(min(values)-(1-mp.cos(min(abs(principal(t)) for t in endpoint_phases)/n))) < tol)
    # Fixed-spectrum preparation tangents contribute zero at a stationary state.
    k = mp.zeros(n*d)
    for j in range(n*d-1):
        k[j, j+1], k[j+1, j] = mp.mpf(j+1)/7, -mp.mpf(j+1)/7
    ds = comm(k, sigma)
    check("moving fixed-spectrum occupation commutator contributes zero at stationarity",
          abs(tr(delta*ds)) < tol and abs(tr(ds)) < tol
          and norm(ds) > mp.mpf(".01"))
    def envelope(v):
        eigenvalues = mp.eighe(clock(gates(v)), eigvals_only=True)
        return mp.fsum(w*a for w, a in zip(weights, eigenvalues))
    eps = mp.mpf("1e-18")
    ep = (envelope(u+eps)-envelope(u-eps))/(2*eps)
    check("ordered minimizing fixed-spectrum envelope finite source obeys endpoint speed divided by N",
          abs(ep) <= speed+mp.mpf("1e-30") and abs(ep-source) < mp.mpf("1e-30"))

    # A rapidly changing prefix gauge has CONSTANT endpoint. Bounding the full
    # DDelta by endpoint speed would fail; only stationary expectations cancel.
    large, angle = mp.mpf(37), mp.mpf(".7")
    def gauge_gates(v):
        return (tw.rotation(large*v), tw.rotation(angle-large*v),
                mp.eye(d), mp.eye(d), mp.eye(d))
    gd = clock(gauge_gates(u))
    gdp = derivative(lambda v: clock(gauge_gates(v)), u)
    gy = derivative(lambda v: endpoint(gauge_gates(v)), u)
    gv, gu = mp.eighe(gd)
    gs = gu*mp.diag(weights)*gu.H
    kg = mp.zeros(n*d)
    kg[2, 3], kg[3, 2] = -large, large
    check("constant endpoint prefix-gauge derivative is the actual full clock commutator",
          norm(gy) < tol and norm(gdp-comm(kg, gd)) < tol)
    check("stationary clock and fixed-spectrum moving-gauge source vanish despite large full derivative",
          abs(tr(gs*gdp)) < tol and abs(tr(gd*comm(kg, gs))) < tol
          and norm(gdp) > 10)
    ev, eu = mp.eighe(gdp)
    nonstationary = eu[:, len(ev)-1]*eu[:, len(ev)-1].H
    bad_source = mp.re(tr(nonstationary*gdp))
    check("negative control nonstationary preparation detects a large constant-endpoint source",
          bad_source > 10 and norm(comm(nonstationary, gd)) > mp.mpf(".01"))
    # Commutation alone does NOT control a spectrum-changing occupation.
    lo, hi = gu[:, 0]*gu[:, 0].H, gu[:, n*d-1]*gu[:, n*d-1].H
    occupation = (lo+hi)/2
    occupation_dot = 50*(lo-hi)
    occupation_source = mp.re(tr(gd*occupation_dot))
    check("negative control commuting variable occupations have an unconstrained source",
          norm(comm(gd, occupation)) < tol and norm(comm(gd, occupation_dot)) < tol
          and abs(tr(occupation_dot)) < tol and abs(occupation_source) > 50)
    fixed_weights = [Fraction(3, 5), Fraction(2, 5)]
    fixed_derivatives = [Fraction(7), Fraction(-7)]
    block0 = delta[:d, :d]
    block0_dot = dd[:d, :d]
    check("literal clock stage0 compression is exactly I_d and its derivative block is zero",
          block0 == mp.eye(d) and block0_dot == mp.zeros(d))
    check("stage0 preparation has exactly R=1 and DR=0 for any normalized moving internal density",
          sum(fixed_weights) == 1 and sum(fixed_derivatives) == 0
          and all(block0[j, j] == 1 and block0_dot[j, j] == 0 for j in range(d)))

    # Consume the published 7y price calculation, checking all frozen inputs.
    receipt_path = WRITER / "CHECK_RESULT.json"
    old = json.loads(receipt_path.read_text(encoding="utf-8"))
    helper = Path(tw.__file__).resolve()
    book_proof = WRITER / "BOOK_PROOF.md"
    check("the consumed complete native writer receipt is the frozen PASS42 7y application",
          old["status"] == "PASS" and old["checks_passed"] == 42
          and old["parameters"]["N"] == 14142
          and old["parameters"]["paired_clock_modes"] == 14481408
          and "Jprime>1/5000" in old["proved_source_bounds"]
          and old["inputs_sha256"][helper.name] == hashlib.sha256(helper.read_bytes()).hexdigest()
          and old["inputs_sha256"][book_proof.name] == hashlib.sha256(book_proof.read_bytes()).hexdigest())
    base = Quadratic(-1, 2)  # cos(2 theta)=p-p^2=p^3.
    terms = [Quadratic(1), base]
    for _ in range(2, 1162):
        terms.append(2*base*terms[-1]-terms[-2])
    check("exact Q(p) finite native features give u67-u1 greater than 1/50",
          (terms[67]-terms[1]-Fraction(1, 50)).sign() > 0)
    check("exact Q(p) finite native features give u1-u1161 greater than 1/100",
          (terms[1]-terms[1161]-Fraction(1, 100)).sign() > 0)
    stages = 14142
    a2 = Fraction(100, 91*stages**2)
    slope = Fraction(1, 5000)-2*Fraction(1, 13000)
    check("exact squared norm bound gives a less than 1/13000 on the whole u interval",
          a2 < Fraction(1, 13000**2))
    check("full H plus stationary-or-optimized fixed-spectrum R leaves S-prime greater than 3/65000",
          slope == Fraction(3, 65000) and slope > 0)
    check("both optimized full-source finite gaps exceed 4e-7 for every fixed occupation spectrum",
          slope*Fraction(1, 50) > Fraction(4, 10**7)
          and slope*Fraction(1, 100) > Fraction(4, 10**7))
    p = (mp.sqrt(5)-1)/2
    theta = mp.atan2(p, mp.sqrt(p))
    phi = principal(66*theta)
    rows = []
    for row in old["rows"]:
        feature = mp.cos(2*row["n"]*theta)
        phases = tw.phase_representatives(theta, phi, feature)
        ground = 1-mp.cos(min(abs(principal(t)) for t in phases)/stages)
        jprime = tw.full_feedback_source(phi, feature, mp.mpf(1)/4)
        check(f"native n{row['n']} keeps the genuine fixed-parameter J source above 1/5000",
              jprime > mp.mpf(1)/5000 and mp.mpf(1)/5 < feature < mp.mpf(3)/10
              and abs(feature-mp.mpf(row["u"])) < mp.mpf("1e-24"))
        check(f"native n{row['n']} ground clock energy obeys the whole paired spectral lower-mode formula",
              0 <= ground <= 2 and len(phases) == 8)
        rows.append({"n": row["n"], "u": mp.nstr(feature, 30),
                     "old_B_full_writer": row["B_full_writer"],
                     "ground_clock_energy": mp.nstr(ground, 30),
                     "B_plus_ground_R": mp.nstr(mp.mpf(row["B_full_writer"])+ground, 30),
                     "D_J": mp.nstr(jprime, 30), "feature_Qp_sha256": terms[row["n"]].digest()})
    check("ground-energy optimized example preserves both actual native full-source contrasts",
          mp.mpf(rows[1]["B_plus_ground_R"]) > mp.mpf(rows[0]["B_plus_ground_R"])
          > mp.mpf(rows[2]["B_plus_ground_R"]))
    return {"checks": CHECKS, "checks_passed": len(CHECKS), "rows": rows,
            "small_clock": {"N": n, "d": d, "matrix_dimension": n*d,
                            "endpoint_speed_over_N": mp.nstr(speed, 30),
                            "stationary_R_source": mp.nstr(source, 30),
                            "prefix_gauge_full_DDelta_norm": mp.nstr(norm(gdp), 30),
                            "nonstationary_source": mp.nstr(bad_source, 30),
                            "variable_occupation_source": mp.nstr(occupation_source, 30)},
            "uniform_bounds": {"a_squared": str(a2), "a_strict_upper": "1/13000",
                               "J_source_strict_lower": "1/5000", "S_source_strict_lower": "3/65000",
                               "optimized_gap_strict_lower": "4e-7", "u_interval": ["1/5", "3/10"]},
            "numeric_arithmetic": "70-digit mpmath, non-interval; exact Q(p)/Fraction certificates separate",
            "matrix_scope": "generic N5 d2 full10 clock only; no native512 or long clock matrix replay",
            "long_heat_replayed": False, "old_PASS42_replayed": False,
            "all_native_stationarity_or_admission_proved": False,
            "original_spatial_R_identified_with_clock_R": False,
            "Book03_25_selects_this_R": False, "oldRIGHT_subset_preparation_admission_proved": False,
            "all_unoptimized_finite_R_gaps_claimed": False, "GR_closed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    result.update(schema="d0.native-clock-rayleigh-source-check/1", status="PASS")
    paths = [Path(__file__).resolve(), Path(tw.__file__).resolve(),
             WRITER/"CHECK_RESULT.json", WRITER/"BOOK_PROOF.md", WRITER/"WRITER_PROOF.md",
             tw.ri.DOMAIN/"check_native_execution_domain.py", tw.ri.DOMAIN/"native_execution.py",
             Path(tw.ri.__file__).resolve()]
    result["inputs_sha256"] = {str(p.relative_to(SOURCES)): hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in paths}
    primary = SOURCES.parent/"A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"
    body = primary.read_bytes()
    start = body.index(b"## 7z.")
    end = body.index(b"\n## ", start+1)+1
    section = body[start:end]
    result["primary_proof"] = {"section": "7z", "bytes": len(section),
                               "sha256": hashlib.sha256(section).hexdigest()}
    result["runtime"] = {"python": sys.version.split()[0], "mpmath": mp.__version__}
    output = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    main()
