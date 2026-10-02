#!/usr/bin/env python3
"""Audit one harmonic/sign candidate using the mandatory #232/#227 controls.

This does not add a microstructure family or claim a joint response NO-GO.
It checks the proposed invariant and terminal implication themselves. The
source and all-period statements are proved in A4D_SOURCE_IMAGE_COLLAPSE.md.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json

import numpy as np
import sympy as sp
import a4d_identity_quarter_nonlinear_response_check as N


I = N.I
ETA = np.diag(N.SIG).astype(object)
Y = N.T[0]
B = N.G[0] + N.G[1] + N.G[2]


def ck(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def inverse(a):
    return ETA @ a.T @ ETA


def family(generator, t):
    u = N.inverse(I - t * generator * F(1, 2)) @ (I + t * generator * F(1, 2))
    links = np.array([[I.copy() for _ in range(4)] for _ in range(4)], dtype=object)
    links[0, 0] = u
    links[2, 0] = inverse(u)
    return links


def face_momenta(links):
    """Literal right plaquette derivative, retaining the inverse variation."""
    out = []
    for p in range(4):
        row = []
        for f, (r, s) in enumerate(N.PAIRS):
            plaquette = (links[p, r] @ links[(p + 1) % 4, s]
                         @ inverse(links[(p + 1) % 4, r]) @ inverse(links[p, s]))
            pi = inverse(plaquette)
            row.append([np.sum(N.WEIGHT[f] * (plaquette @ x + x @ pi)) * F(1, 2)
                        for x in N.G])
        out.append(row)
    return np.array(out, dtype=object)


def ordinary_codifferential(momentum):
    out = np.zeros((4, 4, 6), dtype=object)
    for p in range(4):
        for f, (r, s) in enumerate(N.PAIRS):
            difference = momentum[p, f] - momentum[(p - 1) % 4, f]
            out[p, r] += difference
            out[p, s] -= difference
    return out


def complete_y_stationarity():
    # Every link has the same D=4+3*t^2 denominator. Thus degree eight
    # contains the entire D^4 Euler numerator, including inactive links.
    ck("OWNED_Y_CUBED_MINUS_THREE_Y", np.array_equal(Y @ Y @ Y, -3 * Y))
    links = np.array([[N.jconst(4 * I, 8) for _ in range(4)] for _ in range(4)], dtype=object)
    links[:, :, 2] = 3 * I
    links[0, 0, 1] = 4 * Y
    links[2, 0, 1] = -4 * Y
    links[0, 0, 2] = links[2, 0, 2] = 3 * I + 2 * Y @ Y
    ek, eq = N.euler_links(links)
    ck("COMPLETE_Y_STATIONARY_NUMERATOR_ALL_DEGREE_EIGHT_COEFFICIENTS", not np.any(ek))
    ck("PREDECLARED_ZERO_SOURCE_Y_ALL_DEGREE_EIGHT_COEFFICIENTS", not np.any(eq))


def exact_harmonic_difference():
    t = sp.Symbol("t", real=True)
    d = 4 + 3 * t*t
    u = I + (4 * t * Y + 2 * t*t * (Y @ Y)) / d
    ui = inverse(u)
    ck("OWNED_Y_NONZERO_CURVATURE_NUMERATOR", all(
        sp.factor(a - b) == 0 for a, b in zip(((u - ui) / 2).flat, (4*t*Y/d).flat)))
    links = np.array([[I.copy() for _ in range(4)] for _ in range(4)], dtype=object)
    links[0, 0] = u
    links[2, 0] = ui
    actual = face_momenta(links)
    base = face_momenta(np.array([[I.copy() for _ in range(4)] for _ in range(4)], dtype=object))
    delta = sum(actual - base) / 4
    expected = np.zeros((6, 6), dtype=object)
    expected[:3, :3] = np.array([[-2, 1, 1], [1, -2, 1], [1, 1, -2]], dtype=object) * t*t / d
    ck("EVERY_HARMONIC_MOMENT_COEFFICIENT", all(
        sp.factor(a - b) == 0 for a, b in zip(delta.flat, expected.flat)))
    codiff = ordinary_codifferential(actual)
    ck("STATIONARITY_DOES_NOT_MAKE_CANONICAL_CURRENT_ORDINARY_COCLOSED",
       sp.factor(codiff[0, 1, 1] + 4*t/d) == 0 and codiff[0, 1, 1] != 0)
    a, h = sp.symbols("a h", positive=True)
    limit = sp.limit((-2*t*t/d).subs(t, a*h) / (h*h), h, 0)
    ck("SOURCE_NULL_HARMONIC_MEMORY_SURVIVES_H2_SCALING", limit == -a*a/2)
    ck("POSITIVE_Y_PARAMETERS_HAVE_DISTINCT_HARMONIC_VALUES",
       -2*F(1, 5)**2/(4 + 3*F(1, 5)**2) == -F(2, 103)
       and -2*F(1, 7)**2/(4 + 3*F(1, 7)**2) == -F(2, 199))
    return {"face_order": [list(x) for x in N.PAIRS],
            "delta_harmonic_temporal_boost_block": [[-2, 1, 1], [1, -2, 1], [1, 1, -2]],
            "block_multiplier": "t^2/(4+3*t^2)", "all_other_harmonic_entries": "zero",
            "ordinary_codifferential_witness": "(p=0,role=1,generator=K2): -4*t/(4+3*t^2)",
            "h2_normalized_harmonic_limit_t_ah": "(face01,K1): -a^2/2",
            "both_source_equations": "E_K=0, Xi=h^2*tau=0 exactly; tau=0 prescribed before links",
            "metric_response_gap": "zero exactly"}


def owned_boost_sign_control():
    links = family(B, F(1, 5))
    shifted = links[[1, 2, 3, 0]].copy()
    eka, eqa = N.euler_links(links[:, :, None])
    ekb, eqb = N.euler_links(shifted[:, :, None])
    ck("BOTH_OWNED_BOOST_REPRESENTATIVES_STATIONARY", not np.any(eka) and not np.any(ekb))
    ck("SAME_HARMONIC_VECTOR_AND_AMPLITUDE_SIGN", np.array_equal(
        sum(face_momenta(links)), sum(face_momenta(shifted))))
    ck("SAME_ORIGIN_RESPONSE_SIGN", eqa[0, 0, 4] == eqb[0, 0, 4] and eqa[0, 0, 4] < 0)
    ck("DIFFERENT_SITEWISE_RESPONSE_REQUIRES_DIFFERENT_SOURCES", not np.array_equal(eqa, eqb))
    return {"original_signs": [1, 1, -1, -1], "translated_signs": [1, -1, -1, 1],
            "same_harmonic_momentum": True, "same_positive_amplitude": True,
            "same_origin_Xi11": str(eqa[0, 0, 4]),
            "domain": "full E_K fiber, not two solutions with the same prescribed smooth source",
            "consequence": "one global amplitude sign is not full sitewise sign memory"}


def transport_and_norm_checks():
    u = family(Y, F(1, 5))[0, 0]
    x = N.G[0]
    # At phase zero T0 T1 acts by Ad_U and T1 T0 by the identity.
    commutator = u @ x @ inverse(u) - x
    ck("CURVED_Y_TRANSPORT_DIFFERENCES_DO_NOT_FORM_FLAT_COMPLEX", np.any(commutator))
    flux = np.array([1, 0, -1, 0], dtype=object)
    divergence = flux - flux[[3, 0, 1, 2]]
    ck("DIVERGENCE_ZERO_SIGNED_SUM_NONZERO_OWNER_NORM", sum(divergence) == 0
       and sum(abs(x) for x in divergence) == 4)
    return {"covariant_difference_identity": "[T_r-I,T_s-I]=(Ad_P_rs-I) T_s T_r",
            "curved_Y_commutator_nonzero_components": int(np.count_nonzero(commutator)),
            "period_four_flux": list(map(int, flux)),
            "period_four_divergence": list(map(int, divergence)),
            "signed_divergence_sum": 0, "unweighted_divergence_l1": 4,
            "repeated_h2_divergence_normalized_owner1": "L^4, despite zero signed mean",
            "norm_control_scope": "algebraic norm obstruction, not an asserted realizable joint response"}


def run_checks():
    complete_y_stationarity()
    harmonic = exact_harmonic_difference()
    boost = owned_boost_sign_control()
    transport = transport_and_norm_checks()
    return {"schema": "a4d-harmonic-sign-candidate-audit-v1",
            "input_head": "f3b6b24e8d8ab00c9aa0e3496bc367a542cb5b8f",
            "arithmetic": "exact Q; full Cayley Euler numerators; coefficientwise rational current identity",
            "controls_consumed": ["mandatory #232/Y joint vacuum", "mandatory #227/B connection-stationary response"],
            "Y_source_null_harmonic_counterexample": harmonic, "B_global_sign_insufficiency_control": boost,
            "transport_and_raw_norm_obstructions": transport,
            "generic_same_source_identity": "Xi(K1)-Xi(K2)=(Xi(K1)-h^2*tau)-(Xi(K2)-h^2*tau)=0",
            "correct_negative_target": "predeclare tau, solve full admissible joint equations, separate h^2*tau from designated Xi in the declared norm",
            "nonclaims": ["no A4D-JOINT-MICROSTRUCTURE-METRIC-RESPONSE-NOGO",
                          "no rejection of every possible finite sufficient invariant",
                          "ordinary Hodge projection of the literal momentum is not a transported cohomology theorem"],
            "verdict": "CANONICAL-HARMONIC-SIGN-TERMINAL-DICHOTOMY-INVALID"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expect", type=Path)
    args = parser.parse_args()
    report = run_checks()
    expected = args.expect or (Path(__file__).with_name("a4d_harmonic_sign_candidate_audit_results.json")
                               if args.output is None else None)
    if expected:
        assert json.loads(expected.read_text()) == report
        print("PASS_PINNED_LEDGER", flush=True)
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    print("VERDICT", report["verdict"], flush=True)
