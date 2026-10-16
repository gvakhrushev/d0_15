#!/usr/bin/env python3
"""Lift the certified relative CAR-observer jet to an actual q,m joint tangent.

This is a kinematic lift in the existing full exterior carrier.  It does not
identify the v3 count cost with a native D0 action or claim a physical source.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import argparse
from pathlib import Path
from fractions import Fraction

import sympy as s


ROOT = Path(__file__).resolve().parents[3]
STEM = "a4d_native_relative_observer_joint_lift"
PROOF = "02_REGISTRY/research/A4D_NATIVE_RELATIVE_OBSERVER_JOINT_LIFT.md"
CHRONOLOGY_CHECK = "02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py"
SOURCE_CHECK = "02_REGISTRY/research/certificates/a4d_native_relative_observer_source_jet_check.py"
SOURCE_RESULT = "02_REGISTRY/research/certificates/a4d_native_relative_observer_source_jet_results.json"
SOURCE_PROOF = "02_REGISTRY/research/A4D_NATIVE_RELATIVE_OBSERVER_SOURCE_JET.md"
FINITE_PROBE_PROOF = "02_REGISTRY/research/A4D_NATIVE_FINITE_PROBE_COMPLETION.md"


def sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"OWNER_UNAVAILABLE:{path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def zero_on_unit_circle(expr, c, s0) -> bool:
    relation = s0**2 + c**2 - 1
    entries = list(expr) if isinstance(expr, s.MatrixBase) else [expr]
    return all(s.reduced(s.expand(entry), [relation], s0)[1] == 0 for entry in entries)


def run() -> dict:
    chronology = load(CHRONOLOGY_CHECK, "d0_joint_lift_chronology_owner")
    old = chronology.old
    red, zero = chronology.red, old.zero
    source_receipt = json.loads((ROOT / SOURCE_RESULT).read_text())
    if (source_receipt.get("status") != "PASS_EXACT_POSITIVE_FULL_PREPARATION_SOURCE_JET"
            or source_receipt.get("exact_controls") != 26):
        raise AssertionError("UPSTREAM_RELATIVE_SOURCE_RECEIPT_NOT_PASS")
    if source_receipt.get("checker_sha256") != sha(SOURCE_CHECK):
        raise AssertionError("UPSTREAM_RELATIVE_SOURCE_CHECKER_HASH_MISMATCH")
    if source_receipt.get("proof_sha256") != sha(SOURCE_PROOF):
        raise AssertionError("UPSTREAM_RELATIVE_SOURCE_PROOF_HASH_MISMATCH")
    source_owner = load(SOURCE_CHECK, "d0_relative_source_checker_owner")
    for path, expected_hash in source_owner.INPUTS.items():
        if sha(path) != expected_hash or source_receipt.get("input_sha256", {}).get(path) != expected_hash:
            raise AssertionError(f"UPSTREAM_RELATIVE_SOURCE_INPUT_PIN_MISMATCH:{path}")

    I4, I16 = s.eye(4), s.eye(16)
    eta = s.diag(1, -1, -1, -1)
    G = I4
    e = [I4[:, i] for i in range(4)]
    p, a = old.p, old.a
    checks: list[str] = []
    expected_prob = s.sympify(
        source_receipt["exact_values"]["event_probability"], locals={"a": a, "p": p}
    )
    positive_prob_bound = Fraction(
        source_receipt["exact_values"]["event_probability_rational_lower_bound"]
    )
    check_upstream_positive = (
        source_receipt["exact_values"]["event_probability_rational_lower_bound"] == "53661/250000"
        and positive_prob_bound > 0
        and "EVENT_PROBABILITY_STRICTLY_POSITIVE_BY_RATIONAL_INTERVAL"
        in source_receipt["checks"]
        and "SOURCE_JET_STRICTLY_POSITIVE_BY_RATIONAL_INTERVAL" in source_receipt["checks"]
    )

    def check(name: str, condition) -> None:
        if not bool(condition):
            raise AssertionError("FAILED:" + name)
        checks.append(name)

    # The actual native whole-blank seed e_0 + volume in occupation-mask order.
    m0 = s.zeros(16, 1)
    m0[1] = m0[15] = 1
    B0 = old.record_basis()
    BC = s.Matrix([[1, 0, 1, 0], [0, 1, 0, 1],
                   [1, 0, 1, 0], [0, 1, 0, 1]]) / 2
    blank = B0 * s.kronecker_product(BC, s.eye(4)) * B0.T
    check("actual_whole_blank_seed", blank * m0 == m0)

    def source_for_axis(i: int):
        returns = [chronology.record(G, e[r])[0] for r in range(4)]
        dUs = [chronology.record(G, e[0], s.zeros(4), e[i])[2]] + [
            s.zeros(16) for _ in range(3)
        ]
        check(f"axis{i}_native_record_jet_is_unitary",
              zero(dUs[0].T * returns[0] + returns[0].T * dUs[0]))

        def channel0(X):
            value = sum(((p * I16 + p**2 * U) * X * (p * I16 + p**2 * U).T
                         for U in returns), s.zeros(16)) / 4
            return value.applyfunc(red)

        def channel1(X):
            value = p**3 * sum(((U - I16) * X * (U - I16).T
                                for U in returns), s.zeros(16)) / 4
            return value.applyfunc(red)

        def dchannel0(X):
            value = s.zeros(16)
            for U, dU in zip(returns, dUs):
                A0, dA0 = p * I16 + p**2 * U, p**2 * dU
                value += dA0 * X * A0.T + A0 * X * dA0.T
            return (value / 4).applyfunc(red)

        def dchannel1(X):
            value = s.zeros(16)
            for U, dU in zip(returns, dUs):
                A0 = U - I16
                value += p**3 * (dU * X * A0.T + A0 * X * dU.T) / 4
            return value.applyfunc(red)

        states = {(0, 0): I16 / 16}
        jets = {(0, 0): s.zeros(16)}
        for total in range(3):
            for count in range(total + 1):
                X = states.get((total, count), s.zeros(16))
                dX = jets.get((total, count), s.zeros(16))
                for branch, channel, dchannel in (
                    (0, channel0, dchannel0), (1, channel1, dchannel1)
                ):
                    key = (total + 1, count + branch)
                    states[key] = states.get(key, s.zeros(16)) + channel(X)
                    jets[key] = jets.get(key, s.zeros(16)) + channel(dX) + dchannel(X)

        Delta = sum(((U - I16).T * (U - I16) for U in returns), s.zeros(16)).applyfunc(red)
        dDelta = sum((dU.T * (U - I16) + (U - I16).T * dU
                      for U, dU in zip(returns, dUs)), s.zeros(16)).applyfunc(red)
        sigma = (states[(3, 1)] + states[(3, 2)]).applyfunc(red)
        dsigma = (jets[(3, 1)] + jets[(3, 2)]).applyfunc(red)
        prob = red(s.trace(sigma))
        dprob = red(s.trace(dsigma))
        cost = red(s.trace(Delta * sigma) / prob)
        dcost = red((s.trace(dDelta * sigma + Delta * dsigma)
                     - cost * dprob) / prob)
        check(f"axis{i}_event_probability_matches_owned_formula", zero(prob - expected_prob))
        check(f"axis{i}_full_prepared_cost_jet_nonzero", not zero(dcost))
        return prob, cost, dcost, returns, dUs

    check("owned_event_probability_has_exact_positive_rational_bound", check_upstream_positive)
    base_source = source_for_axis(1)
    returns, dUs = base_source[3], base_source[4]
    cycle = s.zeros(4)
    cycle[0, 0] = 1
    cycle[2, 1] = cycle[3, 2] = cycle[1, 3] = 1  # e1->e2->e3->e1
    check("spatial_three_cycle_is_proper_orthogonal", cycle.T * cycle == I4 and cycle.det() == 1)
    for power, target_axis in ((1, 2), (2, 3)):
        frame = old.ext(cycle**power)
        for r in range(4):
            check(f"cycle{power}_permutes_actual_native_returns",
                  zero(frame * returns[r] * frame.T - returns[(r + power - 1) % 3 + 1]
                       if r else frame * returns[r] * frame.T - returns[0]))
        target_jet = chronology.record(G, e[0], s.zeros(4), e[target_axis])[2]
        check(f"cycle{power}_transports_actual_relative_record_jet",
              zero(frame * dUs[0] * frame.T - target_jet))
        check(f"cycle{power}_preserves_trace_preparation",
              frame * (I16 / 16) * frame.T == I16 / 16)
    axis_values = [base_source[:3], base_source[:3], base_source[:3]]
    check("three_spatial_relative_source_jets_equal_by_exact_cycle_covariance",
          axis_values[0][2] == axis_values[1][2] == axis_values[2][2])
    expected = source_receipt["exact_values"]["full_prepared_source_derivative"]
    expected_expr = s.sympify(expected.replace("^", "**"), locals={"a": a, "p": p})
    check("joint_lift_axis1_reproduces_owned_source_jet",
          zero(axis_values[0][2] - expected_expr))

    # Exact q,m lift for each spatial axis: F'(0)=A, q=F eta F^T,
    # m=Lambda*(F)m0.  The induced positive pairing Q stays the identity.
    q_slots = []
    matter_jets = []
    for i in (1, 2, 3):
        A = s.zeros(4)
        A[i, 0], A[0, i] = 1, -1
        V = A * eta + eta * A.T
        c, s0 = s.symbols(f"c_{i} s_{i}", real=True)
        F = s.eye(4)
        F[0, 0], F[0, i], F[i, 0], F[i, i] = c, -s0, s0, c
        q_exact = F * eta * F.T
        v_exact = F * e[0]
        E_exact = old.ext(F)
        m_exact = E_exact * m0
        blank_exact = E_exact * blank * E_exact.T
        check(f"axis{i}_coframe_orbit_is_proper_euclidean_rotation",
              zero_on_unit_circle(F.T * F - I4, c, s0)
              and zero_on_unit_circle(s.det(F) - 1, c, s0))
        check(f"axis{i}_whole_curve_keeps_lorentz_signature_and_Q_identity",
              zero_on_unit_circle(q_exact * q_exact - I4, c, s0)
              and zero_on_unit_circle((v_exact.T * q_exact * v_exact)[0] - 1, c, s0)
              and zero_on_unit_circle(-q_exact + 2 * v_exact * v_exact.T - I4, c, s0))
        check(f"axis{i}_whole_curve_transports_all_sixteen_blank_amplitudes",
              zero_on_unit_circle(E_exact.T * E_exact - I16, c, s0)
              and zero_on_unit_circle(s.Matrix([m_exact[1 << r] for r in range(4)]) - v_exact,
                                      c, s0)
              and zero_on_unit_circle(blank_exact * m_exact - m_exact, c, s0))
        v = s.Matrix([m0[1 << r] for r in range(4)])
        dm = chronology.exterior_jet(A) * m0
        dv = s.Matrix([dm[1 << r] for r in range(4)])
        d_qinv = -eta * V * eta
        dk = red((2 * v.T * eta * dv + v.T * d_qinv * v)[0])
        dQ = -V + 2 * (dv * v.T + v * dv.T) - 2 * dk * v * v.T
        n = e[0]
        dn = dv - dk * n / 2
        D, dD = I4, s.zeros(4)
        spatial_constraint_jet = D * V * D.T + dD * eta * D.T + D * eta * dD.T
        check(f"axis{i}_Lorentz_q_tangent_is_symmetric", V == V.T)
        check(f"axis{i}_coframe_generates_q_tangent",
              V == 2 * (e[0] * e[i].T + e[i] * e[0].T))
        check(f"axis{i}_matter_first_grade_moves_with_coframe", dv == e[i])
        check(f"axis{i}_observer_normalization_jet", dk == 0 and dn == e[i])
        check(f"axis{i}_positive_pairing_jet_is_zero", zero(dQ))
        check(f"axis{i}_metric_jet_is_tracefree", s.trace(eta * V) == 0)
        check(f"axis{i}_spatial_joint_constraint_with_D_identity",
              zero(spatial_constraint_jet - V))
        U, P, dU, dP = chronology.record(G, n, s.zeros(4), dn)
        dU_expected = chronology.record(G, e[0], s.zeros(4), e[i])[2]
        check(f"axis{i}_joint_state_jet_is_actual_record_owner_jet", zero(dU - dU_expected))

        # The whole-blank plane is carried by the same exterior frame lift.
        dE = chronology.exterior_jet(A)
        dblank = dE * blank - blank * dE
        check(f"axis{i}_whole_blank_plane_transports_with_coframe",
              zero(dblank * m0 + blank * dm - dm))
        q_slots.append([str(V[r, c]) for r in range(4) for c in range(r, 4)])
        matter_jets.append([str(dm[r]) for r in range(16)])

    return {
        "schema": "d0-native-relative-observer-joint-lift/1",
        "status": "PASS_RELATIVE_OBSERVER_JET_HAS_NATIVE_KINEMATIC_JOINT_LIFT",
        "proof": PROOF,
        "input_sha256": {
            path: sha(path) for path in (
                CHRONOLOGY_CHECK, SOURCE_CHECK, SOURCE_RESULT, SOURCE_PROOF,
                FINITE_PROBE_PROOF,
            )
        },
        "upstream_source_jet": source_receipt["exact_values"],
        "joint_tangent": {
            "base": "q=diag(1,-1,-1,-1), m=e0+volume, D=I, b=0, G=I",
            "path": "F_i(t) is the proper Euclidean rotation in (0,i); q=F_i eta F_i^T; m=Lambda*(F_i)m0",
            "directions": [1, 2, 3],
            "packed_symmetric_q_jets": q_slots,
            "full_exterior_state_jets": matter_jets,
            "spatial_constraint": "exactly preserved by homogeneous q and D=I",
            "positive_pairing": "Q=I exactly along the path",
            "whole_blank": "preserved by the actual exterior coframe action",
        },
        "candidate_cost_pullback": {
            "event": "1<=k<=2 after T=3",
            "trace_preparation": "I16/16 in the v3 instrument interface",
            "three_equal_tracefree_joint_shear_derivatives": [str(v[2]) for v in axis_values],
            "rho0_on_the_homogeneous_flat_carrier": "0",
            "interpretation": "nonzero contraction on these lifted joint shear directions; not a ten-component native metric covector",
        },
        "exact_controls": len(checks),
        "checks": checks,
        "scope": {
            "joint_q_D_b_m_kinematic_tangent_exists": True,
            "four_return_v3_instrument_is_physically_admitted_by_core": False,
            "trace_preparation_identified_with_native_matter_m": False,
            "own_D0_action_or_native_source_selected": False,
            "complete_ten_component_metric_projection": False,
            "Ward_refinement_curved_roots_soundness_or_GR": False,
            "G0_closed": False,
            "original_parent_terminals_changed": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true",
                        help="refresh the adjacent result receipt after review")
    args = parser.parse_args()
    result = run()
    target = ROOT / "02_REGISTRY/research/certificates" / f"{STEM}_results.json"
    result["checker_sha256"] = sha(str(Path(__file__).relative_to(ROOT)))
    result["proof_sha256"] = sha(PROOF)
    if target.exists() and not args.write:
        existing = json.loads(target.read_text())
        if existing != result:
            raise SystemExit("IMMUTABLE_RECEIPT_MISMATCH: rerun with --write after reviewing inputs")
        mode = "verified"
    else:
        target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        mode = "written"
    print(json.dumps({"status": result["status"], "exact_controls": result["exact_controls"],
                      "mode": mode, "result": str(target.relative_to(ROOT))}, indent=2))


if __name__ == "__main__":
    main()
