#!/usr/bin/env python3
"""One exact shared-link Euler identity for the original coupled boost.

The smooth coframe and independent zero metric source are declared before
the candidate.  The degree-eight numerator is complete, not a Taylor jet.
This rejects this candidate on that curved coframe; it does not assert a
response estimate for other stationary fields or a general task terminal.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json
import numpy as np
import a4d_identity_quarter_nonlinear_response_check as N


INPUT_HEAD = "3708ccddc9f249760eab7ca7aa3d7108850a427e"
DEGREE = 8
I = N.I
B = N.G[0] + N.G[1] + N.G[2]
J12 = N.G[3]
ETA = np.diag(N.SIG).astype(object)


def adjoint(a):
    return ETA @ a.T @ ETA


def numerator_links():
    # D=4-3*t^2 is used on EVERY link, including inactive identities.
    # Four degree-two factors give the entire degree-eight numerator.
    assert np.array_equal(B @ B @ B, 3 * B)
    identity = N.jconst(4 * I, DEGREE)
    identity[2] = -3 * I
    u = identity.copy()
    u[1] = 4 * B
    u[2] += 2 * B @ B
    ui = N.jinv(u)
    return np.array([[u if p == 0 and r == 0 else
                      ui if p == 2 and r == 0 else identity
                      for r in range(4)] for p in range(4)], dtype=object)


def incident_numerators():
    """Assemble all six face incidences of (x,Role0,J12), p(x)=0."""
    links = numerator_links()
    terms = []
    for face, (r, s) in enumerate(N.PAIRS):
        if r != 0:
            continue
        for at_x in (True, False):
            phase = 0 if at_x else 3
            loc = [(phase, r, False), ((phase + 1) % 4, s, False),
                   ((phase + 1) % 4, r, True), (phase, s, True)]
            fac = [N.jinv(links[p, q]) if inv else links[p, q]
                   for p, q, inv in loc]
            pos = 0 if at_x else 2
            prefix = N.jconst(I, DEGREE)
            for a in fac[:pos]:
                prefix = N.jmul(prefix, a)
            suffix = N.jconst(I, DEGREE)
            for a in fac[pos + 1:]:
                suffix = N.jmul(suffix, a)
            co = N.jmul(suffix, N.WEIGHT[face].T @ prefix)
            derivative = (N.jmul(co, fac[pos]) if at_x else
                          -N.jmul(fac[pos], co))
            coeffs = np.array([np.sum(a.T * J12) for a in derivative],
                              dtype=object)
            complement = [a for a in range(4) if a not in (r, s)]
            power = sum(a >= 2 for a in complement)
            back = not at_x and s == 1
            terms.append((s, at_x, back, power, coeffs))
    return terms


def cayley(t):
    d = 4 - 3 * t * t
    u = I + (4 * t * B + 2 * t * t * B @ B) / d
    assert np.array_equal(u.T @ ETA @ u, ETA)
    assert np.array_equal((I - t * B / 2) @ u, I + t * B / 2)
    return u


def direct_lattice_derivative(t, *, varied_site=(0, 0, 0, 0), wrong_inverse_sign=False,
                              freeze_face_coframe=False):
    """Differentiate the full L=4 periodic action at one phase-zero link.

    Enumerating all based faces independently checks the local incidence
    placement. The only varying link is L_(0,0), with right variation L*J12.
    Rational f samples are the exact samples of the declared cosine warp.
    """
    L = 4
    origin = tuple(varied_site)
    assert sum(origin) % 4 == 0
    samples = (F(1), F(51, 50), F(26, 25), F(51, 50))
    u = cayley(t)
    ui = adjoint(u)

    def shift(x, r):
        return tuple((a + (j == r)) % L for j, a in enumerate(x))

    def link(x, r):
        phase = sum(x) % 4
        return u if r == 0 and phase == 0 else ui if r == 0 and phase == 2 else I

    value = F(0)
    touched = 0
    for x in product(range(L), repeat=4):
        f = F(1) if freeze_face_coframe else samples[x[1]]
        solder = np.diag([F(1), F(1), f, f])
        for r, s in N.PAIRS:
            loc = [(x, r, False), (shift(x, r), s, False),
                   (shift(x, s), r, True), (x, s, True)]
            if not any(y == origin and q == 0 for y, q, inv in loc):
                continue
            touched += 1
            a, b = [j for j in range(4) if j not in (r, s)]
            weight = N.orient(r, s) * N.weight(N.wedge(solder[:, a], solder[:, b]))
            p = I.copy()
            dp = np.zeros((4, 4), dtype=object)
            for y, q, inv in loc:
                raw = link(y, q)
                fac = adjoint(raw) if inv else raw
                df = np.zeros((4, 4), dtype=object)
                if y == origin and q == 0:
                    df = (-J12 @ fac if inv else fac @ J12)
                    if inv and wrong_inverse_sign:
                        df = -df
                dp, p = dp @ fac + p @ df, p @ fac
            # Differentiate C=(P-P^-1)/2 directly, retaining the inverse.
            dc = (dp - adjoint(dp)) / 2
            value += np.sum(weight * dc)
    assert touched == 6
    assert isinstance(value, F)
    return value


def run_checks():
    # These declarations precede candidate construction and readout.
    data = {
        "mesh": "h=1/L, L in 4*N",
        "coframe": "S_h(x)=diag(1,1,f(h*x1),f(h*x1))",
        "profile": "f(y)=1+(1-cos(2*pi*y))/50",
        "fixed_metric_source": "tau(y)=0 in all ten owner slots; E_Q=h^2*tau_h",
        "connection_source": "zero",
        "comparator": "the #216 smooth comparator on the same fixed g=S^T*eta*S",
        "owner_norm": "unweighted sum over all sites and ten packed metric slots",
    }
    terms = incident_numerators()
    # c=-2*t*D^3. This array specifies every coefficient up to degree 8.
    c = np.array([0, -128, 0, 288, 0, -216, 0, 54, 0], dtype=object)
    expected = {(1, True): c, (1, False): -c,
                (2, True): -c, (2, False): c,
                (3, True): np.zeros(9, dtype=object),
                (3, False): np.zeros(9, dtype=object)}
    total = {(False, 2): np.zeros(9, dtype=object),
             (True, 2): np.zeros(9, dtype=object),
             (False, 1): np.zeros(9, dtype=object)}
    for s, at_x, back, power, coeffs in terms:
        assert np.array_equal(coeffs, expected[s, at_x])
        total[back, power] += coeffs
    assert np.array_equal(total[False, 2], c)
    assert np.array_equal(total[True, 2], -c)
    assert not np.any(total[False, 1])
    print("PASS_COMPLETE_DEGREE8_SHARED_LINK_IDENTITY", flush=True)

    controls = []
    delta = F(1) - F(51, 50) ** 2
    for t in (F(-1, 7), F(1, 5), F(1, 4)):
        expected_value = -2 * t * delta / (4 - 3 * t * t)
        actual = direct_lattice_derivative(t)
        assert actual == expected_value and actual != 0
        wrong = direct_lattice_derivative(t, wrong_inverse_sign=True)
        frozen = direct_lattice_derivative(t, freeze_face_coframe=True)
        assert wrong != expected_value
        assert frozen == 0 and frozen != expected_value
        controls.append({"t": str(t), "literal_global_action_derivative": str(actual),
                         "wrong_inverse_sign": str(wrong), "frozen_coframe": str(frozen)})
    assert direct_lattice_derivative(F(0)) == 0
    print("PASS_INDEPENDENT_FULL_PERIODIC_ACTION_DERIVATIVE", flush=True)
    print("PASS_INVERSE_SIGN_AND_FROZEN_FACE_HOSTILE_CONTROLS", flush=True)

    # The same selected row gives an unweighted owner-sum lower bound.
    # The all-L counting/monotonicity argument is written in the proof owner.
    # Here all four slow-coordinate values are checked by independent full
    # action derivatives; the multiplicity is the actual phase-zero count.
    t = F(1, 5)
    samples = (F(1), F(51, 50), F(26, 25), F(51, 50))
    total_variation = sum(abs(samples[n]**2-samples[n-1]**2) for n in range(4))
    assert total_variation == F(102, 625)
    derivatives = []
    for n in range(4):
        site = ((-n) % 4, n, 0, 0)
        value = direct_lattice_derivative(t, varied_site=site)
        assert value == -2*t*(samples[n]**2-samples[n-1]**2)/(4-3*t*t)
        derivatives.append(value)
    multiplicities = [sum(1 for x in product(range(4), repeat=4)
                          if x[1] == n and sum(x) % 4 == 0) for n in range(4)]
    assert multiplicities == [4**3//4]*4
    selected_sum = sum(m*abs(value) for m,value in zip(multiplicities,derivatives))
    assert selected_sum == F(51, 625)*abs(t)*4**3/(4-3*t*t)
    print("PASS_UNWEIGHTED_OWNER_SUM_FROM_THE_SAME_IDENTITY", flush=True)

    return {
        "schema": "a4d-coupled-boost-curved-realizability-v1",
        "input_head": INPUT_HEAD,
        "arithmetic": "exact rational, complete polynomial and direct action differentiation",
        "predeclared_data": data,
        "candidate": "B=K1+K2+K3; U=(I-t*B/2)^(-1)*(I+t*B/2); Role0=(U,I,U^-1,I); other links=I",
        "real_chart": "0<abs(t)<2/sqrt(3)",
        "selected_row": "right variation L_(x,0)*exp(epsilon*J12), sum(x)=0 mod 4",
        "exact_identity": "E_(K0,J12)(x)=-2*t*(f_n^2-f_(n-1)^2)/(4-3*t^2)",
        "cleared_denominator": "(4-3*t^2)^4",
        "numerator": "-2*t*(4-3*t^2)^3*(f_n^2-f_(n-1)^2)",
        "f_n_squared_coefficients_degrees_0_to_8": list(map(int, c)),
        "f_previous_squared_coefficients_degrees_0_to_8": list(map(int, -c)),
        "f_n_linear_coefficients_degrees_0_to_8": [0] * 9,
        "direct_action_controls": controls,
        "origin_value": "2*t*((1+(1-cos(2*pi/L))/50)^2-1)/(4-3*t^2)",
        "all_mesh_conclusion": "nonzero at the origin for every L in 4*N and every nonzero t in the real chart",
        "analytic_extension": "every positive nonconstant sampled profile has an unequal adjacent pair; choose phase 0 there",
        "source_independence": "the failed connection row is unaffected by any independently prescribed metric source",
        "connection_owner_sum": {
            "norm": "sum over all sites, four roles and six Lorentz Euler components; no site-count normalization",
            "phase_zero_multiplicity_at_each_x1": "L^3/4 for L in 4*N",
            "sampled_profile_total_variation": "102/625 for every L in 4*N",
            "lower_bound": "||E_K||_owner1 >= 51*abs(t)*L^3/(625*(4-3*t^2))",
            "L4_direct_action_control": {"t": str(t),
                                         "four_slow_site_derivatives": list(map(str,derivatives)),
                                         "multiplicities": multiplicities,
                                         "selected_phase_zero_sum": str(selected_sum)},
            "all_mesh_proof": "analytic residue counting and monotonicity; the finite control checks coefficient and normalization",
        },
        "requested_outcome": "1: coupled boost fails exact E_K=0 on the declared nonconstant coframe",
        "gate": "JOINT-CRITICAL-REALIZABILITY-AND-OWNER-SUM-CONTROL: COUPLED_BOOST_EXCLUDED",
        "scope": "original coupled-boost family, not arbitrary corrected or independently coupled links",
        "parent_task_status": "PARTIAL / OPEN; Draft / IN_PROGRESS",
        "verdict": "COUPLED_BOOST_CURVED_REALIZABILITY_EXCLUDED",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expect", type=Path)
    args = parser.parse_args()
    report = run_checks()
    expected = args.expect or (Path(__file__).with_name(
        "a4d_coupled_boost_curved_realizability_results.json") if args.output is None else None)
    if expected:
        assert json.loads(expected.read_text()) == report
        print("PASS_PINNED_LEDGER", flush=True)
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    print("VERDICT", report["verdict"])
