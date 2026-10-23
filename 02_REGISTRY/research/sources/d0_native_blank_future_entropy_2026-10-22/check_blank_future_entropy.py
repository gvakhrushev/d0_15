#!/usr/bin/env python3
"""Bounded native blank-future / entropy-source application.

Only six definitions from the pinned original native constructor are loaded.
No previous suite runs, no 128**N tape is enumerated, and no ill-conditioned
floating-point Vandermonde inverse is used. Receipt writing is explicit.
"""
from __future__ import annotations

import argparse
import ast
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.linalg import expm, solve_sylvester


ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
NATIVE_PATH = ROOT / "02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py"
NATIVE_BLOB = "ee8de4635d24c668949ac9a0186616ab7d59f2ed"
P = (np.sqrt(5.0) - 1.0) / 2.0
EYE = np.eye(16, dtype=complex)
CHECKS: list[str] = []


def require(condition, description):
    if not bool(condition):
        raise ArithmeticError(description)
    CHECKS.append(description)


def adj(a):
    return a.conj().T


def herm(a):
    return (a + adj(a)) / 2


def tr(a):
    z = np.trace(a)
    if abs(z.imag) > 1e-10:
        raise ArithmeticError("non-real trace")
    return float(z.real)


def matrix_log(a):
    values, vectors = np.linalg.eigh(herm(a))
    if values.min() <= 0:
        raise ArithmeticError("strictly positive entropy control required")
    return (vectors * np.log(values)) @ adj(vectors)


def entropy(a):
    return -tr(a @ matrix_log(a))


def relative_entropy(a, b):
    return tr(a @ (matrix_log(a) - matrix_log(b)))


def native_namespace():
    raw = NATIVE_PATH.read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    require(blob == NATIVE_BLOB, "original native constructor immutable blob")
    env = {"np": np, "expm": expm, "solve_sylvester": solve_sylvester,
           "P": P, "EYE": EYE}
    names = {"adj", "herm", "tr", "root", "creators", "native"}
    seen = set()
    for node in ast.parse(raw.decode()).body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            exec(compile(ast.Module(body=[node], type_ignores=[]), str(NATIVE_PATH), "exec"), env)
            seen.add(node.name)
    require(seen == names, "only six constructor definitions loaded; no old suites")
    return env


def native_checks():
    env = native_namespace()
    k, dk = env["native"](2 * np.arctanh(1 / 9), 3 / 5)
    dk = dk * (81 / 40)  # The actual r=tanh(theta/2) derivative.
    zero = np.zeros_like(EYE)
    completeness = sum((adj(a) @ a for a in k), zero.copy())
    completeness_jet = sum((adj(da) @ a + adj(a) @ da for a, da in zip(k, dk)), zero.copy())
    require(len(k) == 128 and np.linalg.norm(completeness - EYE) < 2e-12
            and np.linalg.norm(completeness_jet) < 2e-12,
            "actual complete full128 round and its full first source")

    # Independent port-effect readout fixes Delta; do not define it from K[0].
    port = sum((adj(a) @ a for a in k[1::2]), zero.copy())
    dport = sum((adj(da) @ a + adj(a) @ da for a, da in zip(k[1::2], dk[1::2])), zero.copy())
    delta, ddelta = herm(port / (4 * P**3)), herm(dport / (4 * P**3))
    b, db = k[0], dk[0]
    require(np.linalg.norm(b - (EYE - 2 * P**2 * delta)) < 2e-12
            and np.linalg.norm(db + 2 * P**2 * ddelta) < 2e-12,
            "the single fine blank and its jet equal I-2p^2 Delta")
    eigenvalues = np.linalg.eigvalsh(delta)
    require(eigenvalues.min() > 0 and eigenvalues.max() < 1
            and np.linalg.eigvalsh(herm(b)).min() > np.sqrt(5) - 2,
            "native positive contraction sector and positive injective blank")

    inverse = np.linalg.inv(delta)
    z = tr(inverse)
    rho = inverse / z
    drho = -inverse @ ddelta @ inverse / z + inverse * tr(inverse @ inverse @ ddelta) / z**2
    mu, h = F(141489, 10240000), F(69399, 5030720)
    dh = F(-20040939, 9885993640)
    require(abs(tr(delta) / 16 - float(mu)) < 2e-13
            and abs(16 / z - float(h)) < 2e-13
            and abs(16 * tr(inverse @ inverse @ ddelta) / z**2 - float(dh)) < 2e-12,
            "original native two-band fixture and moving preparation normalization")

    def star(x):
        return sum((adj(a) @ x @ a for a in k), zero.copy())

    def star_jet(x, dx):
        return sum((adj(da) @ x @ a + adj(a) @ dx @ a + adj(a) @ x @ da
                    for a, da in zip(k, dk)), zero.copy())

    # Completeness sums every suffix, including all failure outcomes, in O(N).
    horizon = 15
    suffix, dsuffix = [EYE.copy()], [zero.copy()]
    for _ in range(horizon):
        dsuffix.append(star_jet(suffix[-1], dsuffix[-1]))
        suffix.append(star(suffix[-1]))
    power, dpower = EYE.copy(), zero.copy()
    effect_error, jet_error, probabilities = 0.0, 0.0, []
    for n in range(horizon + 1):
        full_effect = adj(power) @ suffix[horizon - n] @ power
        full_jet = (adj(dpower) @ suffix[horizon - n] @ power
                    + adj(power) @ dsuffix[horizon - n] @ power
                    + adj(power) @ suffix[horizon - n] @ dpower)
        blank_effect = adj(power) @ power
        blank_jet = adj(dpower) @ power + adj(power) @ dpower
        effect_error = max(effect_error, float(np.linalg.norm(full_effect - blank_effect)))
        jet_error = max(jet_error, float(np.linalg.norm(full_jet - blank_jet)))
        probabilities.append(tr(rho @ full_effect))
        dpower, power = db @ power + b @ dpower, b @ power
    require(effect_error < 2e-11 and jet_error < 2e-11,
            "all sixteen prefix effects and jets from one complete fifteen-round tape")
    require(abs(probabilities[0] - 1) < 2e-12
            and all(0 < probabilities[n + 1] < probabilities[n] for n in range(horizon)),
            "prefix probabilities are actual nested unconditioned events")

    # Stronger consumer: the ORIGINAL capped first-match tape. Anchor label 1
    # differs from ordinary blank label 0, so every subsequent 0 is a mismatch.
    anchor, danchor = k[1], dk[1]
    require(np.linalg.norm(anchor + 2 * P * np.sqrt(P) * delta) < 2e-12
            and np.linalg.norm(danchor + 2 * P * np.sqrt(P) * ddelta) < 2e-12,
            "actual port-one blank-label anchor is the invertible native Delta Kraus")
    matched = adj(anchor) @ anchor
    dmatched = adj(danchor) @ anchor + adj(anchor) @ danchor
    stopped_suffix, dstopped_suffix = [EYE.copy()], [zero.copy()]
    qcost, dqcost = zero.copy(), zero.copy()
    for _ in range(horizon):
        rlast, drlast = stopped_suffix[-1], dstopped_suffix[-1]
        stopped_suffix.append(matched + star(rlast) - adj(anchor) @ rlast @ anchor)
        dstopped_suffix.append(dmatched + star_jet(rlast, drlast)
                               - adj(danchor) @ rlast @ anchor
                               - adj(anchor) @ drlast @ anchor
                               - adj(anchor) @ rlast @ danchor)
        next_qcost = EYE + port + star(qcost) - adj(anchor) @ qcost @ anchor
        next_dqcost = (dport + star_jet(qcost, dqcost)
                      - adj(danchor) @ qcost @ anchor
                      - adj(anchor) @ dqcost @ anchor
                      - adj(anchor) @ qcost @ danchor)
        qcost, dqcost = next_qcost, next_dqcost
    power, dpower = EYE.copy(), zero.copy()
    stopped_effect_error, stopped_jet_error = 0.0, 0.0
    stopped_effects, stopped_probabilities = [], []
    for n in range(horizon + 1):
        prefix, dprefix = power @ anchor, dpower @ anchor + power @ danchor
        suffix_r, suffix_dr = stopped_suffix[horizon - n], dstopped_suffix[horizon - n]
        full_effect = adj(prefix) @ suffix_r @ prefix
        full_jet = (adj(dprefix) @ suffix_r @ prefix
                    + adj(prefix) @ suffix_dr @ prefix
                    + adj(prefix) @ suffix_r @ dprefix)
        b2n = adj(power) @ power
        db2n = adj(dpower) @ power + adj(power) @ dpower
        weighted_effect = 4 * P**3 * delta @ delta @ b2n
        weighted_jet = 4 * P**3 * ((ddelta @ delta + delta @ ddelta) @ b2n
                                   + delta @ delta @ db2n)
        stopped_effect_error = max(stopped_effect_error, float(np.linalg.norm(full_effect - weighted_effect)))
        stopped_jet_error = max(stopped_jet_error, float(np.linalg.norm(full_jet - weighted_jet)))
        stopped_effects.append(full_effect)
        stopped_probabilities.append(tr(rho @ full_effect))
        dpower, power = db @ power + b @ dpower, b @ power
    require(stopped_effect_error < 2e-12 and stopped_jet_error < 2e-12,
            "actual stopped anchor-one mismatch prefixes and full jets equal 4p^3 Delta^2 B^(2n)")
    require(stopped_probabilities[-1] > 0
            and all(stopped_probabilities[n + 1] < stopped_probabilities[n] for n in range(horizon)),
            "the all-mismatch cap-abort remains a strictly positive genuine stopped leaf")
    anchor_cost_effect = 2 * matched + adj(anchor) @ qcost @ anchor
    danchor_cost_effect = (2 * dmatched + adj(danchor) @ qcost @ anchor
                           + adj(anchor) @ dqcost @ anchor + adj(anchor) @ qcost @ danchor)
    anchor_cost = tr(rho @ anchor_cost_effect)
    danchor_cost = tr(drho @ anchor_cost_effect + rho @ danchor_cost_effect)
    require(3 * stopped_probabilities[0] < anchor_cost
            < 2 * (horizon + 1) * stopped_probabilities[0],
            "native stopped anchor-one charge includes all its matched and aborted suffixes")

    # Exact old quadratic identity supplies projectors; there is no eigenvalue cutoff.
    gap = np.sqrt(float(mu * (mu - h)))
    lm, lp = float(mu) - gap, float(mu) + gap
    plus = herm((delta - lm * EYE) / (lp - lm))
    minus = EYE - plus
    require(np.linalg.norm(plus @ plus - plus) < 2e-11
            and abs(tr(plus) - 8) < 2e-10,
            "owned native two-band projectors used without mode truncation")

    def central(x):
        return tr(minus @ x) * minus / 8 + tr(plus @ x) * plus / 8

    require(np.linalg.norm(central(rho) - rho) < 2e-12,
            "actual invariant input equals its blank-moment entropy representative")
    seed = np.diag(np.linspace(-1, 1, 16)).astype(complex)
    tangent = herm(seed - central(seed))
    tangent /= np.linalg.norm(tangent)
    competitor = rho + 0.005 * tangent
    require(np.linalg.eigvalsh(competitor).min() > 0
            and np.linalg.norm(competitor @ delta - delta @ competitor) > 1e-7,
            "faithful genuinely noncommuting native competitor")
    moment_error = max(abs(tr((competitor - rho) @ np.linalg.matrix_power(b, 2 * n)))
                       for n in range(horizon + 1))
    gain = entropy(rho) - entropy(competitor)
    kl = relative_entropy(competitor, rho)
    require(moment_error < 2e-12 and gain > 1e-5 and abs(gain - kl) < 2e-12,
            "actual matching future moments have exact entropy-minus-KL certificate")
    require(max(abs(tr((competitor - rho) @ effect)) for effect in stopped_effects) < 2e-12,
            "same noncommuting KL certificate applies to the original stopped-prefix constraints")

    input_state = 0.82 * rho
    input_state[0, 0] += 0.18
    center = central(input_state)
    blank_gain = entropy(center) - entropy(input_state)
    kl_total = relative_entropy(input_state, rho)
    kl_center = relative_entropy(center, rho)
    require(blank_gain > 0 and kl_center > 0
            and abs(blank_gain - relative_entropy(input_state, center)) < 3e-12
            and abs(kl_total - blank_gain - kl_center) < 3e-12,
            "off-section noncommuting input has the exact Pythagorean gain bound")
    eta = min(np.linalg.eigvalsh(competitor).min(), np.linalg.eigvalsh(rho).min())
    quadratic_bound = float(np.linalg.norm(competitor - rho)**2 / (2 * eta))
    require(0 < kl <= quadratic_bound,
            "faithful input gain obeys the rank-change-safe quadratic source bound")

    # Actual state/jet propagation pays all rounds; no reset or frozen rho.
    state, dstate = rho.copy(), drho.copy()
    cost, dcost = float(horizon), 0.0
    for _ in range(horizon):
        cost += tr(state @ port)
        dcost += tr(dstate @ port + state @ dport)
        next_state = sum((a @ state @ adj(a) for a in k), zero.copy())
        next_dstate = sum((da @ state @ adj(a) + a @ dstate @ adj(a) + a @ state @ adj(da)
                          for a, da in zip(k, dk)), zero.copy())
        state, dstate = next_state, next_dstate
    cost_formula = horizon * (1 + 4 * P**3 * float(h))
    source_formula = horizon * 4 * P**3 * float(dh)
    require(abs(cost - cost_formula) < 2e-11 and abs(dcost - source_formula) < 2e-11
            and abs(dcost) > 0.01,
            "real finite continuation charge has its surviving nonzero full source")
    require(np.linalg.norm(state - rho) < 2e-11 and np.linalg.norm(dstate - drho) < 2e-11,
            "same native invariant section and its full moving-state jet")

    return {"dimension": 16, "fixed_continuation_rounds": horizon,
            "retained_prefix_events_including_whole_space": horizon + 1,
            "fixed_horizon_physical_outcome_slots": 128**horizon,
            "prefix_effect_max_error": effect_error, "prefix_source_max_error": jet_error,
            "last_blank_prefix_probability": probabilities[-1],
            "original_first_match_comparison_cap": horizon,
            "original_first_match_max_rounds": horizon + 1,
            "stopped_anchor_label": 1, "stopped_mismatch_label": 0,
            "stopped_prefix_effect_max_error": stopped_effect_error,
            "stopped_prefix_source_max_error": stopped_jet_error,
            "stopped_anchor_probability": stopped_probabilities[0],
            "stopped_all_blank_mismatch_abort_probability": stopped_probabilities[-1],
            "stopped_anchor_one_part_of_port_charge": anchor_cost,
            "stopped_anchor_one_part_of_port_charge_r_source": danchor_cost,
            "native_same_moments_noncommuting_entropy_deficit": gain,
            "native_same_moments_quantum_relative_entropy": kl,
            "off_section_blank_gain": blank_gain, "off_section_total_kl_bound": kl_total,
            "quadratic_bound": quadratic_bound,
            "actual_port_charge": cost, "actual_port_charge_r_source": dcost,
            "marginal_invariant_section_gain": 0,
            "marginal_invariant_section_all_total_jets": 0}


def algebraic_controls():
    # A declared three-band MATRIX control, not another physical native fixture.
    # With B=diag(1/3,1/2,2/3), Delta=(I-B)/(2p^2), rho*=(3,4,6)/13.
    blank = [F(1, 3), F(1, 2), F(2, 3)]
    nodes = [x * x for x in blank]
    weights = [F(3, 13), F(4, 13), F(6, 13)]
    determinant = (nodes[1] - nodes[0]) * (nodes[2] - nodes[0]) * (nodes[2] - nodes[1])
    require(determinant == F(35, 3888), "exact three-band blank-square Vandermonde determinant")
    moments = [sum(w * x**n for w, x in zip(weights, nodes)) for n in range(3)]
    # p times the genuine anchored moments: 4p^4 Delta^2=(I-B)^2.
    anchored_moments = [sum(w * (1 - b)**2 * x**n for w, b, x in zip(weights, blank, nodes))
                        for n in range(3)]
    reconstructed = []
    anchored_reconstructed = []
    for a in range(3):
        other = [nodes[b] for b in range(3) if b != a]
        denominator = (nodes[a] - other[0]) * (nodes[a] - other[1])
        coeff = [other[0] * other[1] / denominator,
                 -(other[0] + other[1]) / denominator, 1 / denominator]
        reconstructed.append(sum(c * moment for c, moment in zip(coeff, moments)))
        anchored_reconstructed.append(sum(c * moment for c, moment in zip(coeff, anchored_moments))
                                      / (1 - blank[a])**2)
    require(reconstructed == weights, "exact retained blank moments recover all three block weights")
    require(anchored_reconstructed == weights,
            "exact positive-anchor weighted moments recover the same three block weights")

    rho = np.diag([float(x) for x in weights])
    competitor = rho.astype(complex)
    competitor[0, 1] = competitor[1, 0] = 0.02
    gain = entropy(rho) - entropy(competitor)
    require(gain > 0 and abs(gain - relative_entropy(competitor, rho)) < 2e-14,
            "three-band matching-moment competitor obeys the quantum KL certificate")

    altered = [w - F(1, 100) * v for w, v in zip(weights, [1, -2, 1])]
    same_port = sum((w - old) * (1 - b) for w, old, b in zip(altered, weights, blank))
    blank_difference = sum((w - old) * b*b for w, old, b in zip(altered, weights, blank))
    coarse_gain = entropy(np.diag([float(x) for x in altered])) - entropy(rho)
    require(sum(altered) == 1 and min(altered) > 0 and same_port == 0
            and coarse_gain > 0 and blank_difference == F(-1, 1800),
            "one-port entropy-improving alternative is rejected by real blank futures")

    # Hostile control: squaring a nonpositive blank can erase a distinction.
    hostile_b = [F(2, 5), F(-2, 5)]
    hostile_rho = np.diag([0.7, 0.3])
    require(hostile_b[0]**2 == hostile_b[1]**2
            and entropy(np.eye(2) / 2) > entropy(hostile_rho),
            "positive-blank hypothesis is necessary; a sign-colliding control fails")
    return {"carrier": "three-band finite-matrix algebraic control, not native admission",
            "blank_eigenvalues": [str(x) for x in blank],
            "stationary_weights": [str(x) for x in weights],
            "vandermonde_determinant": str(determinant),
            "moments": [str(x) for x in moments],
            "p_times_anchored_moments": [str(x) for x in anchored_moments],
            "coarse_one_port_entropy_increase": coarse_gain,
            "coarse_competitor_blank_moment_difference": str(blank_difference),
            "nonpositive_blank_hostile_control_detected": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-result", action="store_true",
                        help="explicit authoring mode: write the local RESULT.json receipt")
    args = parser.parse_args()
    native = native_checks()
    controls = algebraic_controls()
    result = {"status": "PASS", "checks": len(CHECKS), "check_names": CHECKS,
              "input_commit": "82d27e83b0ba0869911de80919de50c42f2944d8",
              "native_input_blob": NATIVE_BLOB,
              "proof_sha256": hashlib.sha256((HERE / "PROOF.md").read_bytes()).hexdigest(),
              "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "native": native, "algebraic_controls": controls,
              "scope": {"unique_native_marginal_entropy_representative": True,
                        "original_first_match_source_consumer": True,
                        "requires_declared_first_match_cap_at_least_d_minus_one": True,
                        "increases_a_smaller_first_match_cap_for_free": False,
                        "alternative_fixed_horizon_blank_future_realization": True,
                        "extends_first_match_task_for_free": False,
                        "full_future_maximizer_equals_central_map_off_section": False,
                        "whole_history_source_is_zero": False,
                        "joint_RIGHT_selection_proved": False,
                        "finite_exact_invariant_preparation_proved": False,
                        "mesh_uniform_conditioning_proved": False,
                        "compulsory_Book03_Info_selected": False,
                        "GR_closed": False}}
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_result:
        (HERE / "RESULT.json").write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
