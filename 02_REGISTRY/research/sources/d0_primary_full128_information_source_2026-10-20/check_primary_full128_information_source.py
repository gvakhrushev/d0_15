#!/usr/bin/env python3
"""Actual one-round full128 pointer/coherent entropy and paid-port jets.

Regularization is explicit.  No probability/eigenvalue floor, physical Info
identification, entropy-based selector or new source subtraction is used.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")

import numpy as np

from primary_full128_helper import P, PRIOR_SHA256, PrimaryFixture, require


def evaluate(fixture, base, variation, eta, parameter=0., with_jet=False, with_literal=False):
    vectors, derivative, rayleigh, rjet, sylvester, literal = fixture.compressed_vectors(
        base, variation, parameter, with_jet, with_literal)
    flat = vectors.reshape(33, -1)
    gram = flat @ flat.T
    gram_jet = None
    jet_hs = 0.
    if with_jet:
        dflat = derivative.reshape(33, -1)
        gram_jet = dflat @ flat.T + flat @ dflat.T
        jet_hs = float(np.linalg.norm(dflat))
    require(abs(float(np.trace(gram)) - 1) < 2e-14,
            "literal all128 probability normalizer retained by isometry")
    record = fixture.b @ gram @ fixture.b.T
    probabilities = np.diag(record)
    probability_jet = np.diag(fixture.b @ gram_jet @ fixture.b.T) if with_jet else None
    eigenvalues, eigenvectors = np.linalg.eigh((gram + gram.T) / 2)
    minimum_eigenvalue = float(eigenvalues.min())
    minimum_probability = float(probabilities.min())
    require(minimum_eigenvalue > -eta and minimum_probability > -eta,
            "every explicit regularized log argument positive without clipping")
    require(minimum_eigenvalue > -2e-15 and minimum_probability > -2e-15,
            "negative numerical eigen/probability values limited to float roundoff")
    coherent = float(-np.sum(eigenvalues * np.log(eigenvalues + eta)))
    pointer = float(-np.sum(probabilities * np.log(probabilities + eta)))
    cost = float(np.sum(probabilities[0::2]) + 2 * np.sum(probabilities[1::2]))
    cost_expected = 1 + P * fixture.epsilon * rayleigh
    require(abs(cost - cost_expected) < 3e-14, "all128 primitive paid-port mean")
    result = {
        "pointer_entropy_eta_nats": pointer, "coherent_entropy_eta_nats": coherent,
        "primitive_port_cost": cost, "expected_cost_from_D": cost_expected,
        "Rayleigh": rayleigh, "probability_sum": float(probabilities.sum()),
        "minimum_raw_Gram_eigenvalue": minimum_eigenvalue,
        "minimum_raw_probability": minimum_probability,
        "minimum_Gram_log_argument": minimum_eigenvalue + eta,
        "minimum_pointer_log_argument": minimum_probability + eta,
        "maximum_Sylvester_residual": sylvester,
        "exactly_zero_physical_B_rows": int(np.sum(np.all(fixture.b == 0, axis=1)))}
    if literal is not None:
        q_error = float(np.max(np.abs(probabilities - literal["probabilities"])))
        require(q_error < 2e-14, "all128 probabilities match independent literal original Walsh Kraus sum")
        result["literal_all128_Walsh_probability_error"] = q_error
        result["literal_all128_probability_sum"] = float(literal["probabilities"].sum())
        if with_jet:
            dq_error = float(np.max(np.abs(probability_jet - literal["probability_jets"])))
            require(dq_error < 2e-14, "all128 jets match independent literal original Walsh Kraus sum")
            result["literal_all128_Walsh_probability_jet_error"] = dq_error
            result["literal_all128_probability_jet_sum"] = float(literal["probability_jets"].sum())
    if with_jet:
        require(abs(float(np.trace(gram_jet))) < 5e-14 and
                abs(float(probability_jet.sum())) < 5e-14,
                "all128 derivative normalizer retained")
        diagonal = np.diag(eigenvectors.T @ gram_jet @ eigenvectors)
        coherent_jet = float(-np.sum(diagonal * (
            np.log(eigenvalues + eta) + eigenvalues / (eigenvalues + eta))))
        pointer_jet = float(-np.sum(probability_jet * (
            np.log(probabilities + eta) + probabilities / (probabilities + eta))))
        cost_jet = float(np.sum(probability_jet[0::2]) + 2 * np.sum(probability_jet[1::2]))
        cost_jet_expected = P * fixture.epsilon * rjet
        require(abs(cost_jet - cost_jet_expected) < 3e-14,
                "literal all128 paid-port source equals independently applied D source")
        result.update({
            "pointer_entropy_eta_jet_nats": pointer_jet,
            "coherent_entropy_eta_jet_nats": coherent_jet,
            "primitive_port_cost_jet": cost_jet,
            "expected_cost_jet_from_D": cost_jet_expected,
            "Rayleigh_jet": rjet, "purified_jet_HS_norm": jet_hs,
            "pointer_true_source_regularization_error_bound": 4 * math.sqrt(128 * eta) * jet_hs,
            "coherent_true_source_regularization_error_bound": 4 * math.sqrt(33 * eta) * jet_hs,
            "port_minus_pointer_true_source_regularization_error_bound":
                4 * math.sqrt(128 * eta) * jet_hs / math.log(1 / P),
            "port_minus_coherent_true_source_regularization_error_bound":
                4 * math.sqrt(33 * eta) * jet_hs / math.log(1 / P),
            "port_cost_minus_pointer_eta_in_phi_units_jet": cost_jet - pointer_jet / math.log(1 / P),
            "port_cost_minus_coherent_eta_in_phi_units_jet": cost_jet - coherent_jet / math.log(1 / P)})
    return result


def run(eta=1e-12, step=2e-4):
    started = time.perf_counter()
    fixture = PrimaryFixture()
    prior_receipt_path = (Path(__file__).resolve().parent.parent /
                          "d0_primary_native_domain_source_2026-10-20/PRIMARY_DOMAIN_SOURCE.json")
    prior_receipt = json.loads(prior_receipt_path.read_text(encoding="utf-8"))
    cases = []
    for variation in ["uniform_coframe"] + [f"coframe_role_{r}" for r in range(4)]:
        cases.append((None, variation))
    cases.extend((amplitude, "interior_u_link_N2") for amplitude in (.125, .25))
    results = []
    for amplitude, variation in cases:
        base = fixture.base(amplitude)
        analytic = evaluate(fixture, base, variation, eta, with_jet=True,
                            with_literal=variation in ("uniform_coframe", "interior_u_link_N2"))
        if variation == "uniform_coframe":
            scale_error = abs(analytic["Rayleigh_jet"] + 2 * analytic["Rayleigh"])
            require(scale_error < 2e-13, "independent global flat dilation identity R'=-2R")
            analytic["independent_global_R_scale_identity_error"] = scale_error
        if amplitude is not None:
            prior_row = next(row for row in prior_receipt["two_primary_representatives"]
                             if row["wave_amplitude"] == amplitude)
            value_error = abs(analytic["Rayleigh"] - prior_row["R"])
            source_error = abs(analytic["Rayleigh_jet"] - prior_row["source"][0]["gradient"])
            require(value_error < 1e-12 and source_error < 1e-12,
                    "same primary fixture and free-link source as published predecessor receipt")
            analytic["published_primary_R_difference"] = value_error
            analytic["published_primary_R_jet_difference"] = source_error
        minus = evaluate(fixture, base, variation, eta, parameter=-step)
        plus = evaluate(fixture, base, variation, eta, parameter=step)
        finite_errors = {}
        for name, jet_name in (("pointer_entropy_eta_nats", "pointer_entropy_eta_jet_nats"),
                               ("coherent_entropy_eta_nats", "coherent_entropy_eta_jet_nats"),
                               ("primitive_port_cost", "primitive_port_cost_jet")):
            finite = (plus[name] - minus[name]) / (2 * step)
            error = abs(finite - analytic[jet_name])
            tolerance = (2e-9 if variation.startswith("coframe") or variation == "uniform_coframe"
                         else 2e-10) if name != "primitive_port_cost" else 2e-10
            require(error < tolerance, "independent centered finite-difference source: " + name)
            finite_errors[name] = {"finite_difference": finite, "absolute_error": error,
                                   "float_verification_tolerance": tolerance}
        analytic.update({"wave_amplitude": amplitude, "variation": variation,
                         "centered_finite_difference": finite_errors,
                         "minimum_FD_Gram_eigenvalue": min(minus["minimum_raw_Gram_eigenvalue"],
                                                            plus["minimum_raw_Gram_eigenvalue"]),
                         "minimum_FD_Gram_log_argument": min(minus["minimum_Gram_log_argument"],
                                                              plus["minimum_Gram_log_argument"])})
        results.append(analytic)
    for key in ("Rayleigh_jet", "pointer_entropy_eta_jet_nats", "coherent_entropy_eta_jet_nats",
                "primitive_port_cost_jet"):
        require(abs(sum(row[key] for row in results[1:5]) - results[0][key]) < 3e-13,
                "four genuine coframe directions sum to the uniform source")
    return {
        "status": "PASS", "elapsed_seconds": time.perf_counter() - started,
        "primary_checker_source_sha256": PRIOR_SHA256,
        "carrier": {"sites": 256, "CAR_grades": 16, "reference_columns": 128,
                    "prepared_matrix_shape": [4096, 128], "retained_outcomes": 128,
                    "compressed_vectors": 33, "original_exterior_order": [0, 2, 3, 1],
                    "actual_unequal_FR_cost_depth": 20, "actual_FR_words": int(fixture.counts.sum()),
                    "fixed_scale": fixture.scale, "fixed_scale_Golden_exponent": fixture.exponent,
                    "ell": fixture.ell, "epsilon": fixture.epsilon},
        "compression_isometry": {
            "exact_rational_check": "integer_G.T@integer_G=16I32",
            "Golden_identity": "p+p^2=1; cross terms cancel",
            "maximum_B_adjoint_B_error": float(np.max(np.abs(fixture.b.T @ fixture.b - np.eye(33)))),
            "physical_record": "transpose of the vector Gram; same entropy spectrum"},
        "regularization": {"eta": eta, "formula": "-Tr G log(G+eta I)",
                           "coherent_value_error_bound": 33 * eta,
                           "pointer_value_error_bound": 128 * eta,
                           "negative_eigenvalues_clipped": False, "probability_floor": False,
                           "analytic_source_bound": "4 sqrt(M eta) ||V_prime||HS",
                           "roundoff_is_not_interval_certified": True},
        "finite_difference_step": step, "cases": results,
        "scope": {"one_original_fresh_round": True, "oldRIGHT_reference_retained": True,
                  "both_shifted_Julia_defects_and_jets_retained": True,
                  "physical_Book_Info_identified": False, "all_costs_paid": False,
                  "bare_HJR_source_screening_proved": False, "GR_closed": False,
                  "flat_scale_is_global_periodic": True,
                  "curved_link_storage_seam_fixed": True,
                  "interior_link_tangent_has_no_seam_support": True}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--eta", type=float, default=1e-12)
    parser.add_argument("--fd-step", type=float, default=2e-4)
    args = parser.parse_args()
    require(args.eta > 0 and args.fd_step > 0, "positive explicit numerical parameters")
    print(json.dumps(run(args.eta, args.fd_step), sort_keys=True, indent=2))
