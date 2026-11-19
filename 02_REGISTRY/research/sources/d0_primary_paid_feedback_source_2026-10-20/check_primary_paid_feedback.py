#!/usr/bin/env python3
"""Actual primary Schmidt-image paid-feedback cut, with full oldRIGHT trace.

Consumes frozen native definitions; does not replay entropy or all40 tests.
All records and the complete prepared-cut complement are retained.  The
cut is range(E) in DATA tensor I_RIGHT, not the one-vector prepared cut.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
import time

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.dont_write_bytecode = True

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
HELPER = ROOT / "02_REGISTRY/research/sources/d0_primary_full128_information_source_2026-10-20/primary_full128_helper.py"
HELPER_SHA256 = "c8f24203ab93c853641a83270170650cb02b41c48a66e942c322ce33a09257ea"
RECEIPT = HELPER.with_name("PRIMARY_FULL128_INFORMATION.json")
RECEIPT_SHA256 = "e460680c08c1addfa7e6c9b519dde396bd73ff51441095904b250acf0176e305"


def require(condition, message):
    if not bool(condition):
        raise ArithmeticError(message)


def load_owned():
    require(hashlib.sha256(HELPER.read_bytes()).hexdigest() == HELPER_SHA256,
            "published original primary helper pin")
    require(hashlib.sha256(RECEIPT.read_bytes()).hexdigest() == RECEIPT_SHA256,
            "published full128 primary receipt pin")
    spec = importlib.util.spec_from_file_location("owned_full128_definitions", HELPER)
    owned = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(owned)
    return owned


def maximum(matrix):
    return float(np.max(np.abs(matrix)))


def sym(matrix):
    return (matrix + matrix.T.conj()) / 2


def direct_effect(fixture, base, p, z, chi, parameter=0., jet=False):
    c, x, dc, dx = fixture.varied(base, "uniform_coframe", parameter, jet)
    ee = math.sqrt(128) * base["prep"]
    de = fixture.dirac(c, x, ee)
    de_matrix = de.reshape(4096, 128)
    effect = p * fixture.epsilon * (de_matrix.T @ de_matrix)
    kappa = math.sqrt(p) - p
    feedback = p * np.eye(128) - 2 * p * kappa * effect - kappa ** 2 * (effect @ effect)
    values = np.linalg.eigvalsh(sym(feedback))
    require(float(values.min()) > 0 and float(values.max()) < 1,
            "genuine finite prepared feedback spectrum in (0,1)")
    require(float(np.min(1 - z * values)) > 0,
            "all original feedback logarithm arguments positive")
    action = float(-chi * np.sum(np.log1p(-z * values)) / math.log(1 / p))
    result = {"effect": effect, "feedback": feedback, "J_phi": action,
              "cost_port": 1 + float(np.trace(effect).real) / 128,
              "DE": de, "E": ee, "c": c, "x": x,
              "minimum_feedback_eigenvalue": float(values.min()),
              "maximum_feedback_eigenvalue": float(values.max()),
              "minimum_log_argument": float(np.min(1 - z * values))}
    if jet:
        dde = fixture.dirac(dc, dx, ee).reshape(4096, 128)
        effect_jet = p * fixture.epsilon * (dde.T @ de_matrix + de_matrix.T @ dde)
        feedback_jet = (-2 * p * kappa * effect_jet - kappa ** 2 *
                        (effect @ effect_jet + effect_jet @ effect))
        action_jet = float(chi * z * np.trace(np.linalg.solve(
            np.eye(128) - z * feedback, feedback_jet)).real / math.log(1 / p))
        result.update({"effect_jet": effect_jet, "feedback_jet": feedback_jet,
                       "J_phi_jet": action_jet,
                       "cost_port_jet": float(np.trace(effect_jet).real) / 128,
                       "Rayleigh": float(np.sum(de_matrix ** 2)) / 128,
                       "Rayleigh_jet": float(2 * np.sum(de_matrix * dde)) / 128})
    return result


def complete_literal_port_grams(fixture, base):
    """Stream all128 original output amplitudes on all128 input columns.

    The frozen field-independent B reconstructs the literal Walsh/Golden
    Kraus rows. This computes OPERATOR port Grams, not their prepared trace.
    Zero rows are counted and retained; no probabilities are postselected.
    """
    vectors, _, _, _, _, _ = fixture.compressed_vectors(
        base, "uniform_coframe", with_jet=False, with_literal=False)
    grams = np.zeros((2, 128, 128))
    counts = [0, 0]
    zeros = [0, 0]
    for gamma in range(128):
        port = gamma % 2
        counts[port] += 1
        row = fixture.b[gamma]
        nonzero = np.flatnonzero(row)
        if len(nonzero) == 0:
            zeros[port] += 1
            continue
        value = np.zeros_like(base["prep"])
        for column in nonzero:
            value += row[column] * vectors[column]
        matrix = math.sqrt(128) * value.reshape(4096, 128)
        grams[port] += matrix.T @ matrix
    return grams, counts, zeros


def run(step):
    start = time.perf_counter()
    owned = load_owned()
    p, chi, n, z = owned.P, 128, 128, 2 ** -20
    fixture = owned.PrimaryFixture()
    base = fixture.base(None)
    center = direct_effect(fixture, base, p, z, chi, jet=True)
    effect, feedback = center["effect"], center["feedback"]
    effect_jet, feedback_jet = center["effect_jet"], center["feedback_jet"]
    ee = center["E"].reshape(4096, 128)
    require(maximum(ee.T @ ee - np.eye(n)) < 5e-14,
            "actual primary full128 E isometry")
    require(maximum(effect_jet + 2 * effect) < 2e-17,
            "actual inverse-leg uniform Dirac source R_E prime=-2R_E")
    kappa = math.sqrt(p) - p
    expected_feedback_jet = 4 * p * kappa * effect + 4 * kappa ** 2 * (effect @ effect)
    require(maximum(feedback_jet - expected_feedback_jet) < 2e-17,
            "exact uniform prepared-feedback source polynomial")
    eig_effect = np.linalg.eigvalsh(sym(effect))
    require(float(eig_effect.min()) > -2e-16 and float(eig_effect.max()) < 1,
            "actual return effect positive contraction up to declared float tolerance")
    require(float(np.trace(effect)) > 0, "actual Fourier128 flat input has nonzero return")

    grams, counts, zero_counts = complete_literal_port_grams(fixture, base)
    g0, g1 = grams
    norm_error = maximum(g0 + g1 - np.eye(n))
    return_error = maximum(g1 - effect)
    require(norm_error < 3e-14 and return_error < 3e-15,
            "literal all128 operator port Grams agree with full native Dirac return effect")
    literal_a = p * g0 + math.sqrt(p) * g1
    literal_g = p * g0 + p ** 2 * g1
    literal_feedback = np.eye(n) - literal_a @ literal_a
    literal_leakage = p ** 2 * g0 + p * g1 - literal_a @ literal_a
    expected_leakage = kappa ** 2 * (effect - effect @ effect)
    require(maximum(literal_feedback - feedback) < 5e-14,
            "true original complete-Q feedback from all128 output port Grams")
    require(maximum(literal_feedback - literal_g - literal_leakage) < 5e-14,
            "complete Q equals marker-one and retained marker-zero work complement")
    require(maximum(literal_leakage - expected_leakage) < 5e-14,
            "actual nonzero prepared-cut complement agrees with operator theorem")
    require(float(np.trace(literal_leakage)) > 1e-6,
            "hostile marker-only omission loses a nonzero complete complement")

    # Compressing the former whole-DATA feedback loses preparation leakage.
    r_data_e = p * fixture.epsilon * fixture.dirac(
        center["c"], center["x"], center["DE"]).reshape(4096, n)
    outside_e = r_data_e - ee @ effect
    prep_leakage = kappa ** 2 * (outside_e.T @ outside_e)
    compressed_old_feedback = (p * np.eye(n) - 2 * p * kappa * effect -
                               kappa ** 2 * (r_data_e.T @ r_data_e))
    require(maximum(feedback - compressed_old_feedback - prep_leakage) < 5e-16,
            "whole-DATA compression differs by retained outside-E preparation leakage")
    require(float(np.trace(prep_leakage)) > 1e-12,
            "hostile old-feedback compression control is nonzero on actual unequal density")

    saved = json.loads(RECEIPT.read_text(encoding="utf-8"))["cases"][0]
    cost_error = abs(center["cost_port"] - saved["primitive_port_cost"])
    cost_jet_error = abs(center["cost_port_jet"] - saved["primitive_port_cost_jet"])
    require(cost_error < 3e-14 and cost_jet_error < 3e-14,
            "same flat native port value/source as published full128 receipt")
    literal_cost = float(np.trace(g0 + 2 * g1).real) / n
    require(abs(literal_cost - center["cost_port"]) < 3e-14,
            "complete literal operator port cost uses all128 Schmidt columns")

    # The oldRIGHT spectator gives 128 identical input blocks. Avoid a dense
    # 16384-square Kronecker matrix: retain its full eigenvalue multiplicity.
    lam, eigenvectors = np.linalg.eigh(sym(feedback))
    diag_jet = np.diag(eigenvectors.T @ feedback_jet @ eigenvectors)
    full_eigenvalues = np.tile(lam, chi)
    full_source_diagonal = np.tile(diag_jet, chi)
    full_action = float(-np.sum(np.log1p(-z * full_eigenvalues)) / math.log(1 / p))
    full_source = float(z * np.sum(full_source_diagonal / (1 - z * full_eigenvalues)) /
                        math.log(1 / p))
    require(abs(full_action - center["J_phi"]) < 3e-14 and
            abs(full_source - center["J_phi_jet"]) < 3e-14,
            "full oldRIGHT counting determinant and source retain exact factor128")
    require(len(full_eigenvalues) == chi * n == 16384,
            "genuine Schmidt-image cut tensor all oldRIGHT has rank16384")
    ratio = center["J_phi_jet"] / -center["cost_port_jet"]
    bound = Fraction(16 * chi * n, 2 ** 20)
    require(bound == Fraction(1, 4) and 0 < ratio < float(bound),
            "standalone paid-feedback source has exact comparison bound1/4")

    minus = direct_effect(fixture, base, p, z, chi, parameter=-step)
    plus = direct_effect(fixture, base, p, z, chi, parameter=step)
    fd = {}
    for name, jet_name, tolerance in (("J_phi", "J_phi_jet", 2e-10),
                                      ("cost_port", "cost_port_jet", 2e-10)):
        numerical = (plus[name] - minus[name]) / (2 * step)
        error = abs(numerical - center[jet_name])
        require(error < tolerance, "independent global coframe centered derivative:" + name)
        fd[name] = {"centered_derivative": numerical, "absolute_error": error,
                    "float_verification_tolerance": tolerance}
    r_fd = (plus["effect"] - minus["effect"]) / (2 * step)
    require(maximum(r_fd - effect_jet) < 2e-10,
            "full128 operator return jet independently matches centered coframe variation")
    return {
        "status": "PASS", "elapsed_seconds": time.perf_counter() - start,
        "inputs": {"frozen_helper_sha256": HELPER_SHA256,
                   "published_full128_receipt_sha256": RECEIPT_SHA256,
                   "prior_primary_checker_sha256": owned.PRIOR_SHA256,
                   "definition_import_does_not_run_prior_checkers": True},
        "carrier": {"sites": 256, "CAR_grades": 16, "data_dimension": 4096,
                    "Schmidt_image_rank": n, "oldRIGHT_dimension": chi,
                    "genuine_cut_counting_dimension": chi * n,
                    "retained_record_outcomes": 128, "literal_rows_per_port": counts,
                    "exact_zero_rows_per_port_retained": zero_counts,
                    "actual_FR_cost_depth": 20, "actual_FR_words": int(fixture.counts.sum()),
                    "minimum_density": float(fixture.rho.min()),
                    "maximum_density": float(fixture.rho.max()),
                    "fixed_Golden_scale": fixture.scale, "ell": fixture.ell,
                    "epsilon": fixture.epsilon, "z": z,
                    "original_exterior_order": [0, 2, 3, 1]},
        "primary_flat": {"Rayleigh": center["Rayleigh"],
                         "Rayleigh_jet": center["Rayleigh_jet"],
                         "Cost_port": center["cost_port"],
                         "Cost_port_jet": center["cost_port_jet"],
                         "J_feedback_phi": center["J_phi"],
                         "J_feedback_phi_jet": center["J_phi_jet"],
                         "source_ratio_to_minus_Cost_port_jet": ratio,
                         "exact_analytic_ratio_upper_bound": str(bound),
                         "required_other_price_source_for_balance":
                             -center["cost_port_jet"] - center["J_phi_jet"],
                         "minimum_return_effect_eigenvalue": float(eig_effect.min()),
                         "maximum_return_effect_eigenvalue": float(eig_effect.max()),
                         "minimum_feedback_eigenvalue": center["minimum_feedback_eigenvalue"],
                         "maximum_feedback_eigenvalue": center["maximum_feedback_eigenvalue"],
                         "minimum_log_argument": center["minimum_log_argument"]},
        "complete_complement": {
            "literal_operator_normalization_max_error": norm_error,
            "literal_return_operator_max_error": return_error,
            "literal_true_feedback_max_error": maximum(literal_feedback - feedback),
            "work_complement_trace": float(np.trace(literal_leakage)),
            "minimum_work_complement_eigenvalue": float(np.linalg.eigvalsh(sym(literal_leakage)).min()),
            "outside_E_preparation_leakage_trace": float(np.trace(prep_leakage)),
            "outside_E_preparation_leakage_operator_norm": float(np.linalg.eigvalsh(sym(prep_leakage)).max()),
            "omitted_marker_zero_complement_control_nonzero": True,
            "compressing_whole_DATA_feedback_control_nonzero": True},
        "verification": {
            "E_adjoint_E_max_error": maximum(ee.T @ ee - np.eye(n)),
            "R_E_prime_plus_2R_E_max_error": maximum(effect_jet + 2 * effect),
            "published_port_value_difference": cost_error,
            "published_port_source_difference": cost_jet_error,
            "literal_port_cost_difference": abs(literal_cost - center["cost_port"]),
            "full_RIGHT_counting_action_difference": abs(full_action - center["J_phi"]),
            "full_RIGHT_counting_source_difference": abs(full_source - center["J_phi_jet"]),
            "finite_difference_step": step, "finite_difference": fd,
            "full_return_operator_FD_max_error": maximum(r_fd - effect_jet)},
        "scope": {"flat_scale_is_global_periodic": True, "fixed_exterior_collar_claimed": False,
                  "E_and_density_fixed_during_scale_variation": True,
                  "all_oldRIGHT_counting_multiplicities_retained": True,
                  "rank_one_cut_used": False, "physical_echo_admission_proved": False,
                  "complete_physical_Cost_Info_bound": False, "GR_closed": False,
                  "float_verification_not_interval_certificate": True}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fd-step", type=float, default=1e-4)
    parser.add_argument("--save", type=Path)
    args = parser.parse_args()
    require(args.fd_step > 0, "positive independent finite-difference step")
    result = run(args.fd_step)
    encoded = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.save is not None:
        require(args.save.resolve().parent == Path(__file__).resolve().parent,
                "receipt writes only inside this new packet")
        args.save.write_text(encoded, encoding="utf-8", newline="\n")
    print(encoded, end="")
