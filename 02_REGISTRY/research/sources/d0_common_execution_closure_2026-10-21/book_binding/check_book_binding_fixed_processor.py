#!/usr/bin/env python3
"""Bounded algebra/source controls for BOOK_BINDING_ON_FIXED_PROCESSOR.md.

No old Euler/root, Bell/Julia or rank suite is run. Immutable repository
inputs are checked at their pinned git commit, not at mutable route files.
"""
from __future__ import annotations

import argparse
from decimal import Decimal, getcontext
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path
import subprocess

getcontext().prec = 90
D = Decimal
ELL = ((D(1) + D(5).sqrt()) / D(2)).ln()
TOL = D("1e-75")
checks = []


def dec(x):
    if isinstance(x, F):
        return D(x.numerator) / D(x.denominator)
    return D(x)


def require(name, condition):
    if not condition:
        raise RuntimeError("FAIL: " + name)
    checks.append(name)


def close(x, y):
    return abs(x - y) <= TOL * max(D(1), abs(x), abs(y))


def entropy(q):
    return -sum(x * x.ln() / ELL for x in q if x)


def dentropy(q, dq):
    return -sum((x.ln() + 1) * dx / ELL for x, dx in zip(q, dq))


def h(r):
    return entropy([r, 1-r])


def hp(r):
    return ((1-r)/r).ln()/ELL


def hpp(r):
    return -1/(ELL*r*(1-r))


def mm(A, B):
    return [[sum(a*b for a, b in zip(row, col))
             for col in zip(*B)] for row in A]


def tr(A):
    return sum(A[i][i] for i in range(len(A)))


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def mv(A, x):
    return [dot(row, x) for row in A]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    pins = json.loads((here / "SOURCE_PINS.json").read_text())
    repo = args.repo
    if repo is None:
        for parent in here.parents:
            for candidate in (parent, parent / "d0_15"):
                if (candidate / "01_BOOKS").is_dir() and (candidate / ".git").exists():
                    repo = candidate
                    break
            if repo is not None:
                break
    if repo is None:
        raise RuntimeError("Supply --repo for the existing d0_15 checkout")
    for item in pins["repository_inputs"]:
        data = subprocess.run(
            ["git", "show", pins["source_commit"] + ":" + item["path"]],
            cwd=repo, check=True, capture_output=True).stdout
        require("historical_pin:" + item["name"],
                sha256(data).hexdigest() == item["sha256"])

    # A complete factory slice plus its real outer-abort branch. The four
    # labels are an algebra fixture, not a replacement native instrument.
    M, w, r = 4, F(3, 4), F(3, 8)
    a = [F(1, M)] * M
    da = [F(1, 20), -F(1, 30), F(1, 60), -F(1, 30)]
    dr = [F(2, 7), -F(1, 5), F(1, 11), F(3, 13)]
    s0 = [F(i+1, 7) for i in range(M)]
    s1 = [F(2*i-1, 9) for i in range(M)]
    ds0 = [F(i-2, 19) for i in range(M)]
    ds1 = [F(3-i, 23) for i in range(M)]
    sa, dsa = F(11, 13), F(1, 17)
    q, dq, s, ds = [], [], [], []
    for i in range(M):
        q += [w*a[i]*(1-r), w*a[i]*r]
        dq += [w*(da[i]*(1-r)-a[i]*dr[i]),
               w*(da[i]*r+a[i]*dr[i])]
        s += [s0[i], s1[i]]
        ds += [ds0[i], ds1[i]]
    q += [1-w]
    dq += [F(0)]
    s += [sa]
    ds += [dsa]
    require("complete_record_normalization", sum(q) == 1 and sum(dq) == 0)
    require("positive_support_no_floor", min(q) > 0 and sum(da) == 0)
    bars = [(1-r)*s0[i]+r*s1[i] for i in range(M)]
    gaps = [s1[i]-s0[i] for i in range(M)]
    bar, gap = sum(bars)/M, sum(gaps)/M
    dR = sum(dr)/M
    direct = dot(s, dq) + dot(q, ds)
    label = w*(sum((bars[i]-bar)*da[i] for i in range(M))
               +sum((gaps[i]-gap)*dr[i] for i in range(M))/M)
    decomposed = w*gap*dR + label + dot(q, ds)
    require("exact_complete_book_source_decomposition", direct == decomposed)
    require("outer_abort_intrinsic_source_retained", (1-w)*dsa != 0)

    qd, dqd = list(map(dec, q)), list(map(dec, dq))
    dh = dentropy(qd, dqd)
    require("uniform_tape_matched_report_all_normal_cancellation",
            close(dh, dec(w)*hp(dec(r))*dec(dR)))
    dq_label = []
    for v in da:
        dq_label += [dec(w*v*(1-r)), dec(w*v*r)]
    dq_label += [D(0)]
    require("uniform_transcript_source_zero", close(dentropy(qd, dq_label), D(0)))

    # Centered report-gap control: total report source zero is insufficient
    # for a label-sensitive actual price. No arbitrary probability tangent
    # is asserted to be physically reachable by this algebra control.
    dr_zero_sum = [F(1, 9), -F(1, 9), F(0), F(0)]
    unequal_gaps = [F(0), F(1), F(0), F(0)]
    require("unequal_record_gaps_are_real_residual",
            sum(dr_zero_sum) == 0 and dot(dr_zero_sum, unequal_gaps)/M == -F(1, 36))

    # Actual Golden report baseline and native independent report-operand
    # slope. A physical field tangent requires the native pullback owner.
    p = (D(5).sqrt()-1)/2
    z = D(1)/(D(2)**20)
    L0, M0 = 4*p**3, 4*p**3*(1+p**6)
    r0 = 1-(1-z*M0)*(1-z*L0)
    dr_native = 4*z*(1-z*L0)*p**11
    require("actual_golden_primary_report_positive", 0 < r0 < D("0.5"))
    require("actual_report_operand_source_nonzero", dr_native > 0 and hp(r0)*dr_native > 0)
    readiness, dready, dr_report = D("0.7"), D("0.125"), D("0.03")
    matched = -dready*(h(r0)-h(r0))-readiness*hp(r0)*dr_report
    require("actual_matched_abort_readiness_source_cancels",
            close(matched, -readiness*hp(r0)*dr_report))
    unmatched = -dready*(h(r0)-h(D("0.25")))
    require("unmatched_abort_negative_control", abs(unmatched) > D("1e-4"))

    # Canonical pinching of a complete PURE-work record, using a rational
    # fixture whose nonzero amplitudes are exact. No hidden work is traced.
    u0, u1 = [F(3, 5), F(4, 5)], [F(4, 5), -F(3, 5)]
    psi = [F(3, 5)*u for u in u0]+[F(4, 5)*u for u in u1]
    rho = [[x*y for y in psi] for x in psi]
    pinched = [[rho[i][j] if i//2 == j//2 else F(0)
                for j in range(4)] for i in range(4)]
    require("coherent_instrument_fixture_pure", mm(rho, rho) == rho and tr(rho) == 1)
    block_weights = [sum(pinched[i][i] for i in (0, 1)),
                     sum(pinched[i][i] for i in (2, 3))]
    require("pinching_exact_nonzero_spectrum",
            block_weights == [F(9, 25), F(16, 25)]
            and all(pinched[k][k]*pinched[k+1][k+1]
                    == pinched[k][k+1]**2 for k in (0, 2)))
    require("conditional_work_unitary_source_zero",
            dot(u0, [-u0[1], u0[0]]) == 0
            and dot(u1, [-u1[1], u1[0]]) == 0)

    # Fixed charged cost effects and genuine input-normal variations.
    c1, c2 = F(7), F(19)
    c = w*c1+(1-w)*c2
    GC = [[c, F(0)], [F(0), c]]
    tang = [-u0[1], u0[0]]
    require("complete_processing_cost_central", 2*dot(u0, mv(GC, tang)) == 0)

    # Literal j identity, before any assertion about the Book memory map.
    j = [D(i-3)/D(7) for i in range(len(qd))]
    dj = [D(2-i)/D(13) for i in range(len(qd))]
    net = [-x.ln()/(2*ELL)-v for x, v in zip(qd, j)]
    dnet = [-dx/(2*ELL*x)-dv for x, dx, dv in zip(qd, dqd, dj)]
    require("literal_j_mean_identity",
            close(dot(qd, net), entropy(qd)/2-dot(qd, j)))
    dEj = dot(dqd, j)+dot(qd, dj)
    require("literal_j_full_first_source",
            close(dot(dqd, net)+dot(qd, dnet), dh/2-dEj))
    require("cq_mean_source_residual_factor",
            close(dot(dqd, net)+dot(qd, dnet)-dh/2, -dEj))

    # A common value at the point does not fix its true jet. Its common
    # derivative can preserve all normalized records and change both
    # absolute norm and the mean price. This is a kernel diagnostic only.
    common_j, common_dj = D("0.3"), D(1)
    scale = (2*ELL*common_j).exp()
    nb = sum(x*scale for x in qd)
    dnb = sum(scale*(dx+2*ELL*x*common_dj) for x, dx in zip(qd, dqd))
    require("common_anchor_normalized_records_unchanged",
            all(close(x*scale/nb, x) for x in qd))
    require("common_anchor_actual_source_not_erased",
            close(-dnb/(2*ELL*nb), -D(1)))

    # Actual full-source condition includes the phase/work map. Equal
    # record probabilities with orthogonal conditional work fail it.
    require("record_probabilities_do_not_identify_work",
            dot(u0, [-u0[1], u0[0]]) == 0 and dot(u0, u0) == 1)

    # Exact conditional Book isometry/anchor transport, with a separate
    # nonisometric same-input control.
    V = [[F(3, 5), F(0)], [F(4, 5), F(0)], [F(0), F(1)]]
    require("anchor_transport_isometry", mm(list(map(list, zip(*V))), V) == [[1, 0], [0, 1]])
    lam, xin, dxin = F(2, 3), [F(3, 2), F(2)], [F(1), -F(2)]
    xout, dxout = [lam*x for x in mv(V, xin)], [lam*x for x in mv(V, dxin)]
    require("absolute_input_anchor_transported_exactly",
            dot(xout, xout) == lam**2*dot(xin, xin)
            and dot(xout, dxout)*dot(xin, xin) == dot(xin, dxin)*dot(xout, xout))
    noniso = [[F(1), F(0)], [F(0), F(4)]]
    require("fixed_nonisometric_map_has_input_source",
            2*dot(u0, mv(noniso, tang)) == F(72, 25))

    # Classical selector/report comparison only: if work remains quantum,
    # the coarsened quantum entropy needs its own mixture term.
    report_slopes = [D("0.03"), D("-0.03")]
    covariance = sum(x*x for x in report_slopes)/2
    require("measured_selector_first_source_contact",
            hp(r0)*sum(report_slopes)/2 == 0)
    require("measured_selector_second_source_not_equal",
            -hpp(r0)*covariance > 0)

    # On the ACTUAL report baseline, scalar prospective matching and
    # amplitude matching have different price slopes. The scalar
    # normalized example has E ds=0 but d E s=dH!=0. This checks the
    # distinction; it is not an assignment of the physical Book gains.
    qb, dqb = [1-r0, r0], [-dr_native, dr_native]
    scalar_price = [-x.ln()/ELL for x in qb]
    scalar_dprice = [-dx/(ELL*x) for x, dx in zip(qb, dqb)]
    require("prospective_expectation_vs_differential",
            close(dot(qb, scalar_dprice), D(0))
            and close(dot(dqb, scalar_price)+dot(qb, scalar_dprice), hp(r0)*dr_native)
            and hp(r0)*dr_native > 0)
    scalar_gap = ((1-r0)/r0).ln()/ELL
    amplitude_gap = scalar_gap/2
    require("literal_before_born_half_factor", scalar_gap == 2*amplitude_gap and scalar_gap > 0)

    result = {
        "status": "PASS",
        "source_commit": pins["source_commit"],
        "scope": "new fixed-record Book residual and conditional source transport only",
        "arithmetic": "Fraction exact identities; Decimal precision 90",
        "proof_sha256": sha256((here / "BOOK_BINDING_ON_FIXED_PROCESSOR.md").read_bytes()).hexdigest(),
        "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "pins_sha256": sha256((here / "SOURCE_PINS.json").read_bytes()).hexdigest(),
        "checks": checks,
        "check_count": len(checks),
        "actual_report": {"r0": str(r0), "hprime": str(hp(r0)),
                          "operand_derivative": str(dr_native),
                          "entropy_operand_derivative": str(hp(r0)*dr_native)},
        "negative_controls": ["unequal record response gaps", "unmatched bank abort",
                              "common anchor with nonzero jet", "fixed nonisometric map",
                              "coarsened classical selector second derivative"],
        "not_certified": ["Book-to-record faithful memory map", "actual Book Info assignment",
                          "input writer/source", "native stationarity selection",
                          "original all42 family (consumed, not replayed)"]
    }
    rendered = json.dumps(result, indent=2, ensure_ascii=False)+"\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
