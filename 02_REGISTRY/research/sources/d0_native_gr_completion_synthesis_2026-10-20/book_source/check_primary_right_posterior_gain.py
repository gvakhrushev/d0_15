#!/usr/bin/env python3
"""Verified full-fine RIGHT/posterior information source on the primary collar.

The eigensolver proposes a basis only.  Interval residuals, a polar correction,
and the integral Lipschitz bound for log certify its use, including faithful
support of every nonzero physical outcome.  No eigenvalue floor is used.
The observable is not an identification of physical Book Info.
"""

import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import sys

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.dont_write_bytecode = True
import numpy as np


INTERVAL_OWNER = ("02_REGISTRY/research/sources/"
                  "d0_native_gr_completion_synthesis_2026-10-20/book_source/"
                  "check_primary_car_pointer_source.py")
INTERVAL_SHA256 = "63c8f13e115ee9a16c58846e7eafc268b24e5ed7659fdbfe2f72e38c1eef0d77"
ROOT = Path(__file__).resolve().parents[5]


def require(condition, message):
    if not bool(condition):
        raise RuntimeError(message)


require(hashlib.sha256((ROOT / INTERVAL_OWNER).read_bytes()).hexdigest() == INTERVAL_SHA256,
        "pinned interval definitions")
_spec = importlib.util.spec_from_file_location("owned_pointer_interval_definitions_only",
                                             ROOT / INTERVAL_OWNER)
O = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(O)
I, Q, up, down = O.I, O.Q, O.up, O.down
UNIT, TINY = O.UNIT, O.TINY


def transpose(value):
    return I(value.lo.T, value.hi.T)


def midpoint_radius(value):
    center = value.lo * .5 + value.hi * .5
    radius = up(np.maximum(up(center - value.lo), up(value.hi - center)))
    zero = (value.lo == 0) & (value.hi == 0)
    radius = np.where(zero, 0., radius)
    require(np.all(np.isfinite(center)) and np.all(np.isfinite(radius))
            and np.all(radius >= 0), "finite center-radius conversion")
    return center, radius


def dot_nearest(left, right):
    # optimize=False uses NumPy's direct C contraction, not a BLAS GEMM.
    # The explicit arithmetic premise is a binary64 sum of k products, in
    # any order, optionally with fused multiply-add; gamma_(2k) covers it.
    return np.einsum("ik,kj->ij", left, right, optimize=False)


def matmul(left, right):
    """Outward center-radius product with a componentwise gamma_(2k) bound."""
    require(left.lo.ndim == right.lo.ndim == 2
            and left.lo.shape[1] == right.lo.shape[0], "matrix product shapes")
    k = left.lo.shape[1]
    require(2 * k * UNIT < 1, "finite matrix-product gamma bound")
    gamma = I.rational(2 * k * UNIT / (1 - 2 * k * UNIT)).hi
    require(float(gamma) < 1, "positive product error denominator")
    a, ar = midpoint_radius(left)
    b, br = midpoint_radius(right)
    underflow = up((2 * k + 1) * TINY)

    def positive_product_upper(x, y):
        approximate = dot_nearest(x, y)
        require(np.all(np.isfinite(approximate)) and np.all(approximate >= 0),
                "finite nonnegative direct contraction")
        return up(up(approximate + underflow) / down(1 - gamma))

    center = dot_nearest(a, b)
    absolute = positive_product_upper(np.abs(a), np.abs(b))
    error = up(up(gamma * absolute) + underflow)
    error = up(error + positive_product_upper(np.abs(a), br))
    error = up(error + positive_product_upper(ar, np.abs(b)))
    error = up(error + positive_product_upper(ar, br))
    require(np.all(np.isfinite(center)) and np.all(np.isfinite(error)),
            "no overflow in interval contraction")
    return I(down(center - error), up(center + error))


def norm_upper(value):
    squared = O.reduce_sum(value.square())
    # The exact sum of squares is nonnegative even when the reduction's
    # outward lower endpoint crosses zero near an exact residual.
    require(float(squared.hi) >= 0, "nonnegative squared norm upper bound")
    return float(I(0., float(squared.hi)).sqrt().hi)


def exact_upper(value):
    """Make a dyadic scalar upper bound usable in interval expressions."""
    return I(float(value))


_LOGS = {}


def scalar_log(value):
    key = (float(value.lo), float(value.hi))
    if key not in _LOGS:
        _LOGS[key] = O.logarithm(value)
    return _LOGS[key]


def static_amplitudes(owned):
    """Literal analytic Julia/Walsh construction, all CAR16 and RIGHT128.

    Columns are C0, C_B, and the bare data basis vector e_(w,15).
    C_B contains the full 128 reference columns, not their contracted kernel.
    """
    counts = owned.actual_counts(ROOT)
    f = np.array(owned.fourier_numerators(), dtype=np.int64)
    for label in range(32):
        for word in range(16):
            first = (-1) ** (label & (2 * word)).bit_count()
            second = (-1) ** (label & (2 * word + 1)).bit_count()
            expected = 0 if label % 2 else 2 * (-1) ** ((label // 2) & word).bit_count()
            require(first + second == expected, "exact original dark Walsh rows")
    for column in range(16):
        require(O.fwht([Q(row == column) for row in range(16)])
                == [Q((-1) ** (row & column).bit_count(), 16) for row in range(16)],
                "literal Walsh transform basis and normalization")
    sites, right, w = 256, 128, owned.site_index(owned.W)
    forward = [np.array([owned.site_index(owned.step(site, r, 1))
                         for site in owned.SITES_LIST]) for r in range(4)]
    backward = [np.array([owned.site_index(owned.step(site, r, -1))
                          for site in owned.SITES_LIST]) for r in range(4)]
    p = (I.rational(5).sqrt() - 1) * Q(1, 2)
    sqrt_p, sigma = p.sqrt(), p * p * p
    rho_entries = [I.rational(Q(sites * count, sum(counts))) for count in counts]
    rho = I([float(v.lo) for v in rho_entries], [float(v.hi) for v in rho_entries])
    a = sigma * rho.sqrt()
    weight = O.broadcast_site(a)
    state_lo = np.zeros((sites, 16, 2 * right + 1))
    state_hi = np.zeros_like(state_lo)
    clock, slack = sqrt_p * I(f / 128.), p * I(f / 128.)
    state_lo[:, 1, :right], state_hi[:, 1, :right] = clock.lo, clock.hi
    state_lo[:, 14, :right], state_hi[:, 14, :right] = slack.lo, slack.hi
    for z, site in enumerate(owned.SITES_LIST):
        entry = I(f[z] / 128.) * owned.B(site)
        state_lo[z, 15, right:2 * right] = entry.lo
        state_hi[z, 15, right:2 * right] = entry.hi
    state_lo[w, 15, 2 * right] = state_hi[w, 15, 2 * right] = 1.
    state = I(state_lo, state_hi)
    creation = owned.ROLE_CREATION
    adjoints = tuple(owned.transpose(c) for c in creation)
    gamma = (Q(1, 2), Q(2), Q(1), Q(1))
    dstate = I(np.zeros_like(state_lo))
    for role in range(4):
        dstate = dstate + weight * O.const_matrix_action(creation[role], O.shifted(state, forward[role]))
        dstate = dstate - weight * O.const_matrix_action(creation[role], state)
        dstate = dstate + O.shifted(weight * O.const_matrix_action(adjoints[role], state), backward[role])
        dstate = dstate - weight * O.const_matrix_action(adjoints[role], state)
    astate = dstate * Q(1, 16)  # dstate=h D0 state, A=h D0/16.
    primitives = [[], []]
    min_radicand = 1.
    for role in range(4):
        cr, ct = creation[role], adjoints[role]
        radicand = I.rational(1) - a.square() * gamma[role]
        min_radicand = min(min_radicand, float(np.min(radicand.lo)))
        require(np.min(radicand.lo) > Q(1, 2), "strict analytic Julia domain")
        delta = radicand.sqrt() - 1
        lp = owned.mscale(owned.mmul(cr, ct), 1 / gamma[role])
        rp = owned.mscale(owned.mmul(ct, cr), 1 / gamma[role])
        require(owned.mmul(lp, lp) == lp and owned.mmul(rp, rp) == rp,
                "exact CAR analytic defect projectors")
        left = astate + O.broadcast_site(delta) * O.const_matrix_action(lp, astate)
        right_action = astate + O.broadcast_site(delta) * O.const_matrix_action(rp, astate)
        shifted_right = astate + O.broadcast_site(O.shifted(delta, backward[role])) * O.const_matrix_action(rp, astate)
        primitives[0].extend((O.shifted(weight * O.const_matrix_action(ct, astate), backward[role]),
                              weight * O.const_matrix_action(cr, O.shifted(astate, forward[role])),
                              -(weight * O.const_matrix_action(ct, astate)),
                              -(weight * O.const_matrix_action(cr, astate))))
        primitives[1].extend((left, shifted_right, -left, -right_action))
    transformed = [O.fwht(part) for part in primitives]
    rr = I(f[w] / 128.)
    return state, transformed, p, sqrt_p, rr, min_radicand, counts


def posterior_certificate(gram, tangent, cross, rr, p):
    """Bound Tr[tangent log(gram/Tr gram)] using a verified polar basis."""
    center, _ = midpoint_radius(gram)
    center = (center + center.T) / 2
    values, basis = np.linalg.eigh(center)
    require(np.all(np.isfinite(values)) and float(values.min()) > 0,
            "candidate eigenvalues positive; not a support cutoff")
    n = len(values)
    candidate = I(basis)
    defect = matmul(transpose(candidate), candidate) - I(np.eye(n))
    delta = norm_upper(defect)
    require(delta < Q(1, 2), "candidate admits controlled polar correction")
    delta_i = exact_upper(delta)
    polar_distance = delta_i / (1 + (I(1.) - delta_i).sqrt())
    basis_norm = (I(1.) + delta_i).sqrt()
    factor = 2 * basis_norm * polar_distance + polar_distance.square()
    reconstruction = matmul(candidate * I(values[None, :]), transpose(candidate))
    residual = norm_upper(gram - reconstruction)
    epsilon = exact_upper(residual) + factor * float(values.max())
    lower_eigen = I(float(values.min())) - epsilon
    require(float(lower_eigen.lo) > 0, "every true posterior eigenvalue certified positive")
    q = O.reduce_sum(I(np.diag(gram.lo), np.diag(gram.hi)))
    require(float(q.lo) > 0, "true outcome probability positive")
    logq = scalar_log(q)
    logs = [scalar_log(I(float(value))) - logq for value in values]
    log_diag = I([float(v.lo) for v in logs], [float(v.hi) for v in logs])
    rotated = matmul(matmul(transpose(candidate), tangent), candidate)
    diagonal = I(np.diag(rotated.lo), np.diag(rotated.hi))
    approximate = O.reduce_sum(diagonal * log_diag)
    max_log = max(float(np.max(np.abs(log_diag.lo))), float(np.max(np.abs(log_diag.hi))))
    log_error = epsilon / lower_eigen + factor * max_log
    # The exact tangent is p(c r^T+r c^T), so nuclear norm <=2p||c||2||r||2.
    nuclear = 2 * p * exact_upper(norm_upper(cross)) * exact_upper(norm_upper(rr))
    source_error = nuclear * log_error
    source = approximate + I(-float(source_error.hi), float(source_error.hi))
    return source, q, {
        "dimension": n, "certified_rank": n,
        "candidate_min_eigenvalue": float(values.min()),
        "certified_min_eigenvalue": float(lower_eigen.lo),
        "orthogonality_defect_F_upper": delta,
        "reconstruction_residual_F_upper": residual,
        "polar_distance_op_upper": float(polar_distance.hi),
        "true_reconstruction_error_op_upper": float(epsilon.hi),
        "matrix_log_error_op_upper": float(log_error.hi),
        "tangent_nuclear_norm_upper": float(nuclear.hi),
        "source_spectral_error_upper": float(source_error.hi),
    }


def main():
    require(np.finfo(np.float64).nmant == 52 and np.finfo(np.float64).maxexp == 1024,
            "binary64 format")
    require(np.float64(1.) + np.float64(2. ** -53) == 1.
            and np.float64(1.) + np.float64(3 * 2. ** -53) == 1. + 2. ** -51,
            "nearest ties-to-even canaries")
    require(np.float64(TINY) * np.float64(1.) == TINY
            and np.float64(TINY) + np.float64(TINY) > TINY, "no flush to zero canaries")
    for path, expected in O.PINS.items():
        require(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected,
                "immutable input: " + path)
    spec = importlib.util.spec_from_file_location("owned_preparation_definitions_only", ROOT / next(iter(O.PINS)))
    owned = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(owned)
    state, transformed, p, sqrt_p, rr, min_radicand, counts = static_amplitudes(owned)
    source, pointer, qsum, rsum, port_cost = I(0.), I(0.), I(0.), I(0.), I(0.)
    bsum, jsum = I(np.zeros((128, 128))), I(np.zeros((128, 128)))
    diagnostics = []
    logphi = -scalar_log(p)
    for label in range(0, 32, 2):
        for coefficient in range(2):
            action = transformed[coefficient][label // 2]
            variants = [(1, -2 * p * sqrt_p, I(1.) + p)]
            if label == coefficient == 0:
                variants = [(0, -2 * p * p, I(1.)), (1, -2 * p * sqrt_p, I(1.))]
            for port, scale, multiplicity in variants:
                amplitude = action * scale
                if label == coefficient == port == 0:
                    amplitude = amplitude + state
                m = I(amplitude.lo[:, :, :128].reshape(4096, 128),
                      amplitude.hi[:, :, :128].reshape(4096, 128))
                mb = I(amplitude.lo[:, :, 128:256].reshape(4096, 128),
                       amplitude.hi[:, :, 128:256].reshape(4096, 128))
                v = I(amplitude.lo[:, :, 256].reshape(4096, 1),
                      amplitude.hi[:, :, 256].reshape(4096, 1))
                gram = matmul(transpose(m), m)
                cross = matmul(transpose(mb), v)
                jet = p * (cross * I(rr.lo[None, :], rr.hi[None, :])
                           + I(rr.lo[:, None], rr.hi[:, None]) * transpose(cross))
                local, q, diagnostic = posterior_certificate(gram, jet, cross, rr, p)
                r = O.reduce_sum(I(np.diag(jet.lo), np.diag(jet.hi)))
                source = source + multiplicity * local
                pointer = pointer - multiplicity * r * scalar_log(q)
                # For nonblank paired ports: q0=p q1 and r0=p r1.
                if label != 0 or coefficient != 0:
                    pointer = pointer - p * r * scalar_log(p)
                    port_cost = port_cost + (p + 2) * r
                else:
                    port_cost = port_cost + (1 + port) * r
                qsum, rsum = qsum + multiplicity * q, rsum + multiplicity * r
                bsum, jsum = bsum + multiplicity * gram, jsum + multiplicity * jet
                diagnostic.update({"physical_index": 4 * label + 2 * coefficient + port,
                                   "paired_port_zero_by_p": label != 0 or coefficient != 0,
                                   "q0": O.bounds(q), "trace_jet": O.bounds(r),
                                   "natural_source": O.bounds(local)})
                diagnostics.append(diagnostic)
    gain = source / logphi
    pointer = pointer / logphi
    known_net = port_cost - gain
    wrong_unconditional = gain - pointer
    require(qsum.contains(1.) and rsum.contains(0.), "complete full-fine probability and jet")
    require(bsum.contains(np.eye(128) / 128) and jsum.contains(np.zeros((128, 128))),
            "actual fixed RIGHT prior and zero prior jet")
    require(float(gain.lo) > 0, "strict actual RIGHT/posterior conditional gain source")
    require(float(pointer.hi) < 0, "pointer entropy is a distinct observable")
    require(float(gain.hi) < float(wrong_unconditional.lo),
            "hostile omitted conditional normalizer has disjoint source")
    require(float(known_net.hi) < 0, "strict known port Cost minus posterior-gain source")
    fine_min = min(float((I(d["certified_min_eigenvalue"])
                         * (p if d["paired_port_zero_by_p"] else I(1.))).lo)
                   for d in diagnostics)
    require(fine_min > 0 and len(diagnostics) == 33, "all64 active fine posteriors faithful")
    report = {
        "status": "PASS", "observable": "I_R:Y=log_phi128-sum q_gamma S_phi(B_gamma/q_gamma)",
        "source_scope": "coefficient of angle derivative at small matter t; D(t)=D0+O(t^2)",
        "carrier": {"L": 4, "CAR": 16, "RIGHT": 128, "FR_words": sum(counts),
                    "w": list(owned.W), "sigma": "p^3"},
        "linear_coefficients": {"RIGHT_posterior_gain_phi": O.bounds(gain),
                                "full_pointer_entropy_phi": O.bounds(pointer),
                                "known_port_cost": O.bounds(port_cost),
                                "known_port_cost_minus_RIGHT_posterior_gain": O.bounds(known_net),
                                "wrong_omitted_conditional_normalizer_phi": O.bounds(wrong_unconditional)},
        "complete_normalization": {"sum_q": O.bounds(qsum), "sum_trace_jet": O.bounds(rsum),
                                   "all_B_sum_contains_I_over128": True, "all_jet_sum_contains_zero": True,
                                   "active_fine_labels": 64, "exact_Walsh_dark_labels": 64},
        "support": {"certified_full_fine_min_eigenvalue_lower": fine_min,
                    "every_active_posterior_rank": 128, "probability_or_eigenvalue_floor": False,
                    "minimum_Julia_radicand_lower": min_radicand},
        "spectral_certificates": diagnostics,
        "arithmetic": "outward binary64 intervals; gamma_(2k) direct matrix contractions; exact rational log tails; verified polar eigensystem residual",
        "arithmetic_premise": "IEEE binary64 nearest arithmetic without FTZ/overflow; optimize=False direct einsum is a sum of k binary64 products and at most k-1 additions in any order, optionally FMA; no eigensolver accuracy premise",
        "physical_Book_Info_identified": False,
        "physical_RIGHT_read_admission_inferred": False,
        "finite_t_or_native_actuation_word_bound_certified": False,
        "source_sha256": {INTERVAL_OWNER: INTERVAL_SHA256, **O.PINS},
    }
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
