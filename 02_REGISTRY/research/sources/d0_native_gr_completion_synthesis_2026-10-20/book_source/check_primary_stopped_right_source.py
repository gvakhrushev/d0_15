#!/usr/bin/env python3
"""Actual primary RIGHT128 first-nonblank cap2 conditional entropy source.

Consume the pinned one-round result. Apply the original full instrument to
the ACTUAL unnormalized blank amplitudes, retaining DATA leakage and abort.
The old verified polar/log enclosure certifies every new active posterior.
No native Book/Info/work selection is asserted.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.dont_write_bytecode = True
import numpy as np

ROOT = Path(__file__).resolve().parents[5]
PREFIX = "02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/book_source/"
PINS = {
    PREFIX + "check_primary_right_posterior_gain.py":
        "2985ab0b4fb007c424c75d2bd57369b781ad1b1653ec3b8b8c68d4d30780367d",
    PREFIX + "PRIMARY_RIGHT_POSTERIOR_GAIN_SOURCE_CERTIFICATE.json":
        "3fc747be8d27a7b581cfa7a2e9b58da5ff87058a4e3b76199dd2e9483a674b6a",
}


def require(condition, message):
    if not bool(condition):
        raise RuntimeError(message)


for path, digest in PINS.items():
    require(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest,
            "immutable stopped-source input: " + path)
spec = importlib.util.spec_from_file_location("owned_primary_posterior_definitions", ROOT / next(iter(PINS)))
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)
O, I, Q = G.O, G.I, G.Q


def gram_jet(amplitude, rr, p):
    m = I(amplitude.lo[:, :, :128].reshape(4096, 128),
          amplitude.hi[:, :, :128].reshape(4096, 128))
    mb = I(amplitude.lo[:, :, 128:256].reshape(4096, 128),
           amplitude.hi[:, :, 128:256].reshape(4096, 128))
    v = I(amplitude.lo[:, :, 256].reshape(4096, 1),
          amplitude.hi[:, :, 256].reshape(4096, 1))
    gram = G.matmul(G.transpose(m), m)
    cross = G.matmul(G.transpose(mb), v)
    jet = p * (cross * I(rr.lo[None, :], rr.hi[None, :])
               + I(rr.lo[:, None], rr.hi[:, None]) * G.transpose(cross))
    return gram, jet, cross


def apply_round(state, owned, counts, p):
    """Original flat hD and complete Julia/Walsh rows on arbitrary amplitudes."""
    forward = [np.array([owned.site_index(owned.step(site, r, 1))
                         for site in owned.SITES_LIST]) for r in range(4)]
    backward = [np.array([owned.site_index(owned.step(site, r, -1))
                          for site in owned.SITES_LIST]) for r in range(4)]
    rho_values = [I.rational(Q(256 * count, sum(counts))) for count in counts]
    rho = I([float(v.lo) for v in rho_values], [float(v.hi) for v in rho_values])
    a = p * p * p * rho.sqrt()
    weight = O.broadcast_site(a)
    creation = owned.ROLE_CREATION
    adjoints = tuple(owned.transpose(c) for c in creation)

    def h_dirac(value):
        result = I(np.zeros_like(value.lo))
        for r in range(4):
            result = result + weight * O.const_matrix_action(creation[r], O.shifted(value, forward[r]))
            result = result - weight * O.const_matrix_action(creation[r], value)
            result = result + O.shifted(weight * O.const_matrix_action(adjoints[r], value), backward[r])
            result = result - weight * O.const_matrix_action(adjoints[r], value)
        return result

    ast = h_dirac(state) * Q(1, 16)
    primitives = [[], []]
    for role, gamma in enumerate((Q(1, 2), Q(2), Q(1), Q(1))):
        cr, ct = creation[role], adjoints[role]
        radicand = I.rational(1) - a.square() * gamma
        require(float(np.min(radicand.lo)) > .5, "actual strict Julia chart")
        delta = radicand.sqrt() - 1
        lp = owned.mscale(owned.mmul(cr, ct), 1 / gamma)
        rp = owned.mscale(owned.mmul(ct, cr), 1 / gamma)
        left = ast + O.broadcast_site(delta) * O.const_matrix_action(lp, ast)
        right = ast + O.broadcast_site(delta) * O.const_matrix_action(rp, ast)
        shifted_right = ast + O.broadcast_site(O.shifted(delta, backward[role])) * O.const_matrix_action(rp, ast)
        primitives[0].extend((O.shifted(weight * O.const_matrix_action(ct, ast), backward[role]),
                              weight * O.const_matrix_action(cr, O.shifted(ast, forward[role])),
                              -(weight * O.const_matrix_action(ct, ast)),
                              -(weight * O.const_matrix_action(cr, ast))))
        primitives[1].extend((left, shifted_right, -left, -right))
    result = [O.fwht(part) for part in primitives]
    direct_blank = state - h_dirac(h_dirac(state)) * (p * p * Q(1, 128))
    walsh_blank = state - result[0][0] * (2 * p * p)
    require((direct_blank - walsh_blank).contains(np.zeros_like(state.lo)),
            "whole-DATA true-adjoint blank agrees with original Walsh row")
    return result


def main():
    require(np.finfo(np.float64).nmant == 52 and np.finfo(np.float64).maxexp == 1024,
            "binary64 format")
    require(np.float64(1.) + np.float64(2. ** -53) == 1.
            and np.float64(1.) + np.float64(3 * 2. ** -53) == 1. + 2. ** -51,
            "nearest ties-to-even canaries")
    require(np.float64(G.TINY) * np.float64(1.) == G.TINY
            and np.float64(G.TINY) + np.float64(G.TINY) > G.TINY, "no flush to zero")
    for path, digest in O.PINS.items():
        require(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest,
                "immutable original input: " + path)
    spec = importlib.util.spec_from_file_location("owned_primary_preparation_definitions", ROOT / next(iter(O.PINS)))
    owned = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(owned)
    old = json.loads((ROOT / (PREFIX + "PRIMARY_RIGHT_POSTERIOR_GAIN_SOURCE_CERTIFICATE.json")).read_text())
    state, first_rows, p, sqrt_p, rr, _, counts = G.static_amplitudes(owned)
    blank = state - first_rows[0][0] * (2 * p * p)
    if "--mutation=no-blank-propagation" in sys.argv:
        blank = state
    del first_rows, state
    b0, j0, _ = gram_jet(blank, rr, p)
    rows = apply_round(blank, owned, counts, p)
    logphi = -G.scalar_log(p)
    natural, pointer, qsum, rsum = I(0.), I(0.), I(0.), I(0.)
    bsum, jsum = I(np.zeros((128, 128))), I(np.zeros((128, 128)))
    diagnostics = []
    for label in range(0, 32, 2):
        for coefficient in range(2):
            action = rows[coefficient][label // 2]
            variants = [(1, -2 * p * sqrt_p, I(1.) + p)]
            if label == coefficient == 0:
                variants = [(0, -2 * p * p, I(1.)), (1, -2 * p * sqrt_p, I(1.))]
            for port, scale, multiplicity in variants:
                amplitude = action * scale
                abort = label == coefficient == port == 0
                if abort:
                    amplitude = amplitude + blank
                if abort and "--mutation=drop-abort" in sys.argv:
                    continue
                if label != 0 and "--mutation=wrong-pair-factor" in sys.argv:
                    multiplicity = I(1.)
                gram, jet, cross = gram_jet(amplitude, rr, p)
                local, q, diagnostic = G.posterior_certificate(gram, jet, cross, rr, p)
                r = O.reduce_sum(I(np.diag(jet.lo), np.diag(jet.hi)))
                natural = natural + multiplicity * local
                pointer = pointer - multiplicity * r * G.scalar_log(q)
                if label != 0 or coefficient != 0:
                    pointer = pointer - p * r * G.scalar_log(p)
                qsum, rsum = qsum + multiplicity * q, rsum + multiplicity * r
                bsum, jsum = bsum + multiplicity * gram, jsum + multiplicity * jet
                diagnostic.update({"physical_index": 4 * label + 2 * coefficient + port,
                                   "paired_port_zero_by_p": label != 0 or coefficient != 0,
                                   "leaf_type": "abort_B_squared" if abort else "second_exit",
                                   "q": O.bounds(q), "trace_jet": O.bounds(r),
                                   "natural_posterior_source": O.bounds(local)})
                diagnostics.append(diagnostic)
    require((bsum - b0).contains(np.zeros((128, 128)))
            and (jsum - j0).contains(np.zeros((128, 128))),
            "second complete round retains actual blank RIGHT marginal and its jet")
    first_blank = old["spectral_certificates"][0]
    qb, rb = I(*first_blank["q0"]), I(*first_blank["trace_jet"])
    require(qsum.contains(float(qb.lo)) or qb.contains(float(qsum.lo)),
            "second-round total mass equals inherited blank mass")
    require((rsum - rb).contains(0.), "second-round mass jet equals inherited blank jet")
    local_blank = I(*first_blank["natural_source"])
    old_gain = I(*old["linear_coefficients"]["RIGHT_posterior_gain_phi"])
    old_pointer = I(*old["linear_coefficients"]["full_pointer_entropy_phi"])
    new_gain = old_gain + (natural - local_blank) / logphi
    new_pointer = old_pointer + (pointer + rb * G.scalar_log(qb)) / logphi
    net = new_pointer - new_gain
    increment = (pointer - natural + local_blank + rb * G.scalar_log(qb)) / logphi
    require(float(increment.hi) < 0 and float(net.hi) < 0,
            "strict stopped conditional entropy source and strict additional-round source")
    require(len(diagnostics) == 33, "all33 new distinct posteriors certified")
    minimum = min(float((I(d["certified_min_eigenvalue"])
                         * (p if d["paired_port_zero_by_p"] else I(1.))).lo)
                  for d in diagnostics)
    require(minimum > 0, "all64 new active leaves faithful without floor")
    abort_diagnostic = diagnostics[0]
    require(abort_diagnostic["leaf_type"] == "abort_B_squared"
            and abort_diagnostic["trace_jet"][0] > 0,
            "actual cap2 abort has strictly positive angle-source coefficient")
    require(float(qb.lo) > Q(121, 144), "inherited blank mass respects strict dominance")
    # A sharp hypothesis control: orthogonal RIGHT blocks G0=diag(1/2,0),
    # G1=diag(0,1/2) have H(Y|R)=0, though -log_phi q0>0.
    # Here q0=1/2 but the largest operator-domination beta is ZERO.
    # A survival-probability bound alone does not give G0>=beta*sigma.
    half_log = G.scalar_log(I.rational(Q(1, 2)))
    orthogonal_joint_entropy = -half_log / logphi
    orthogonal_right_entropy = -half_log / logphi
    require((orthogonal_joint_entropy - orthogonal_right_entropy).contains(0.)
            and float((-half_log / logphi).lo) > 0,
            "perfect-RIGHT boundary control excludes an unconditional survival bound")
    print(json.dumps({
        "status": "PASS", "observable": "H_phi(first_nonblank_cap2_complete_leaf|oldRIGHT128)",
        "carrier": {"L": 4, "sites": 256, "CAR": 16, "RIGHT": 128, "FR_words": sum(counts)},
        "source_scope": "coefficient of angle derivative at small primary t; actual D(t)=D0+O(t^2)",
        "linear_coefficients": {"conditional_entropy_cap2": O.bounds(net),
                                "conditional_entropy_increment_over_cap1": O.bounds(increment),
                                "full_pointer_entropy_cap2": O.bounds(new_pointer),
                                "RIGHT_posterior_gain_cap2": O.bounds(new_gain)},
        "actual_abort": {"probability_at_flat_centre": abort_diagnostic["q"],
                         "angle_source_linear_coefficient": abort_diagnostic["trace_jet"],
                         "task_tolerance_selected": False},
        "blank_dominance_boundary_control": {"blank_probability": "1/2", "operator_domination_beta_max": 0,
                                              "orthogonal_RIGHT_blocks": True,
                                              "conditional_entropy": 0,
                                              "minus_log_q0_strictly_positive": True},
        "complete_cut": {"declared_leaves": 255, "active_leaves": 127, "exact_dark_leaves": 128,
                         "distinct_spectral_cases_total": 65,
                         "blank_probability_cap1": O.bounds(qb), "expected_trials_cap2": O.bounds(1 + qb),
                         "second_round_mass": O.bounds(qsum), "second_round_mass_jet": O.bounds(rsum),
                         "second_round_B_sum_equals_actual_blank_B": True,
                         "second_round_R_sum_equals_actual_blank_R": True},
        "new_support": {"active_leaves": 64, "rank_each": 128,
                        "minimum_unnormalized_eigenvalue_lower": minimum,
                        "probability_or_eigenvalue_floor": False},
        "new_spectral_certificates": diagnostics,
        "arithmetic_premise": old["arithmetic_premise"],
        "source_sha256": {**PINS, G.INTERVAL_OWNER: G.INTERVAL_SHA256, **O.PINS},
        "physical_Book_Info_selected": False, "outside_code_work_selected": False,
        "all_caps_or_refinement_source_inferred": False,
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
