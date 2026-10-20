#!/usr/bin/env python3
"""Original full128 isotropic relative-history first jet at finite clock.

Exact general cross differentiation plus actual literal one-round matrix
jets. No history-word enumeration, physical Info assignment or fixed-h
infinite-depth bound. Existing source definitions are imported, not replayed.
"""
from __future__ import annotations

import argparse
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
import sympy as sp

ROOT = Path(__file__).resolve().parents[4]
PRIOR = ROOT / "02_REGISTRY/research/sources/d0_native_relative_transfer_2026-10-17/check_native_relative_transfer.py"
PRIOR_SHA256 = "dfa8fffb08d421f2a2a0fa91a3044492ab94bfd6bd7d1e86b110b52c2e0ff065"


def require(condition, message):
    if not bool(condition):
        raise ArithmeticError(message)


def maximum(matrix):
    return float(np.max(np.abs(matrix)))


def adjoint(matrix):
    return matrix.swapaxes(-1, -2).conj()


def load_owned():
    require(hashlib.sha256(PRIOR.read_bytes()).hexdigest() == PRIOR_SHA256,
            "pinned original full128 relative-transfer fixture")
    spec = importlib.util.spec_from_file_location("owned_relative_transfer_definitions", PRIOR)
    owned = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(owned)
    require(owned.ORDER == (0, 2, 3, 1), "original exterior creator order")
    return owned


def exact_general_jet():
    x, y = sp.symbols("x y", real=True)
    p, w = sp.symbols("p w", positive=True)
    n = sp.symbols("n", positive=True, integer=True)
    bx, by = sp.sqrt(1 - x ** 2), sp.sqrt(1 - y ** 2)
    t = (1 + x * y + bx * by) / 2
    f = x ** 2 + y ** 2 - 2 * t * x * y
    positive_form = (x - y) ** 2 + x * y / 2 * ((x - y) ** 2 + (bx - by) ** 2)
    require(sp.simplify(f - positive_form) == 0, "owned general f and positive difference form")
    c = 1 - p ** 2 * w * f / 128
    f0 = sp.simplify(f.subs(y, x))
    cx0 = sp.simplify(sp.diff(c, x).subs(y, x))
    cy0 = sp.simplify(sp.diff(c, y).subs(y, x))
    q = sp.simplify(sp.diff(c, x, y).subs(y, x))
    expected = p ** 2 * w / 128 * (2 - x ** 2) / (1 - x ** 2)
    require(f0 == cx0 == cy0 == 0, "zero diagonal discrepancy and exact zero connection")
    require(sp.simplify(q - expected) == 0, "general mixed source q_h from full cross")
    # Differentiate c(y,x)^n before specializing the independent arms.
    cn = c ** n
    connection_n = sp.simplify(sp.diff(cn, x).subs(y, x))
    mixed_n = sp.simplify(sp.diff(cn, x, y).subs(y, x))
    require(connection_n == 0 and sp.simplify(mixed_n - n * q) == 0,
            "full changing-data history jet follows from exact scalar transfer")
    # A genuine connection produces the cross-time term that a naive
    # independent-copy sum would miss: V(t)=exp(i a t)V0(t).
    a = sp.symbols("a", real=True)
    phase_kernel = sp.exp(sp.I * a * (x - y)) * c
    phase_connection = sp.simplify(sp.diff(phase_kernel, x).subs(y, x))
    phase_mixed = sp.simplify(sp.diff(phase_kernel, x, y).subs(y, x))
    phase_n_mixed = sp.simplify(sp.diff(phase_kernel ** n, x, y).subs(y, x))
    require(sp.simplify(phase_connection - sp.I * a) == 0,
            "hostile phase has a nonzero coherent connection")
    require(sp.simplify(phase_mixed - q - a ** 2) == 0,
            "hostile one-round phase norm includes a squared connection")
    require(sp.simplify(phase_n_mixed - n * phase_mixed - n * (n - 1) * a ** 2) == 0,
            "hostile connection retains the n(n-1) cross-time norm")
    exact_points = []
    for nu in (sp.Rational(3, 5), sp.Rational(5, 13)):
        qpoint = sp.simplify(q.subs({x: nu, w: 2}))
        exact_points.append({"nu": str(nu), "q_h_at_h_1_over_4": str(qpoint),
                             "n_h_q_h_at_h_1_over_4": str(sp.simplify(2048 * qpoint))})
    return {"f_xy_on_diagonal": str(sp.simplify(sp.diff(f, x, y).subs(y, x))),
            "q_h": str(sp.factor(q)), "connection": str(cx0),
            "n_round_connection": str(connection_n),
            "n_round_derivative_norm_squared": str(sp.factor(mixed_n)),
            "exact_points": exact_points,
            "hostile_phase_connection": str(phase_connection),
            "hostile_phase_one_round_norm_squared": str(sp.factor(phase_mixed)),
            "hostile_phase_n_round_norm_squared": str(sp.factor(phase_n_mixed)),
            "hostile_phase_omitted_cross_time_term": "n*(n-1)*a**2"}


def exact_sector_normalization():
    b, db, z, tt = sp.symbols("B dB z T", real=True)
    nn = sp.symbols("n", positive=True, integer=True)
    u = 1 - b ** 2
    du = -2 * b * db
    generating_round = b ** 2 + u * z
    require(sp.simplify(generating_round.subs(z, 1) ** nn - 1) == 0,
            "binomial count-generating product has exact total mass1")
    derivative_round = 2 * b * db + du * z
    require(sp.simplify((nn * generating_round ** (nn - 1) * derivative_round).subs(z, 1)) == 0,
            "complete scalar count-sector derivative sums exactly to zero")
    # A polynomial coefficient calibration fixes the mass convention;
    # the general binomial identity is the generating product above.
    coefficient = sp.expand((b ** 2 + sp.Symbol("u") * z) ** 4).coeff(z, 2)
    require(sp.simplify(coefficient - sp.binomial(4, 2) * b ** 4 * sp.Symbol("u") ** 2) == 0,
            "sector coefficient counts ordered occupied cells without an extra factorial")
    cell_volume_k2 = sp.factor(nn * (nn - 1) / 2 * (tt / nn) ** 2)
    require(sp.simplify(cell_volume_k2 - tt ** 2 * (1 - 1 / nn) / 2) == 0,
            "two-event total time-cell volume is binomial(n,2)*epsilon**2")
    limit_k2 = sp.limit(cell_volume_k2, nn, sp.oo)
    require(sp.simplify(limit_k2 - tt ** 2 / 2) == 0,
            "two-event cells converge to the ordered-simplex volume T**2/2")
    require(sp.simplify(limit_k2 / sp.factorial(2) - tt ** 2 / 2) != 0,
            "hostile extra factorial gives a wrong simplex volume")
    return {"sector_mass": "binomial(n,k)*B**(2*(n-k))*u**k; u=1-B**2",
            "count_generating_product": "(B**2+u*z)**n",
            "exact_total_mass": 1, "exact_total_mass_source": 0,
            "one_word_time_cell_volume": "epsilon**k",
            "one_word_embedding_squared_amplitude": "epsilon**(-k)",
            "one_word_embedding_norm_squared": 1,
            "total_k2_time_cell_volume": str(cell_volume_k2),
            "fixed_T_k2_volume_limit": str(limit_k2),
            "additional_factorial_used": False,
            "hostile_extra_factorial_limit": str(limit_k2 / 2)}


def exact_physical_scale():
    h, p = sp.symbols("h p", positive=True)
    aa, bb = sp.symbols("a b", positive=True)
    w = 4 * sp.sin(sp.pi * h) ** 2
    x, y = h * aa, h * bb
    t = (1 + x * y + sp.sqrt(1 - x ** 2) * sp.sqrt(1 - y ** 2)) / 2
    f = x ** 2 + y ** 2 - 2 * x * y * t
    scaled_difference = ((aa - bb) ** 2 + aa * bb / 2 *
                         (h ** 2 * (aa - bb) ** 2 +
                          (sp.sqrt(1 - h ** 2 * aa ** 2) -
                           sp.sqrt(1 - h ** 2 * bb ** 2)) ** 2))
    require(sp.simplify(f / h ** 2 - scaled_difference) == 0,
            "physical coframe cross is the exact nu=ha substitution")
    f_limit = sp.simplify(scaled_difference.subs(h, 0))
    require(sp.simplify(f_limit - (aa - bb) ** 2) == 0,
            "physical f(ha,hb)/h**2 converges to (a-b)**2")
    # Differentiate the actual nu family with respect to a, including
    # its h factor. The new clock is distinct from the old fixed-nu one.
    q_phys = h ** 2 * p ** 2 * w / 128 * (2 - h ** 2 * aa ** 2) / (1 - h ** 2 * aa ** 2)
    n_new, n_old = 128 / h ** 4, 128 / h ** 2
    new_norm_limit = sp.simplify(sp.limit(n_new * q_phys, h, 0))
    old_norm_limit = sp.simplify(sp.limit(n_old * q_phys, h, 0))
    require(sp.simplify(new_norm_limit - 8 * sp.pi ** 2 * p ** 2) == 0 and old_norm_limit == 0,
            "physical a-jet vanishes on old clock and survives on h**(-4) clock")
    epsilon = p ** 2 * h ** 2 / 64
    tau = epsilon * h ** 2
    delta = aa ** 2 * w
    blank = 1 - epsilon * delta / 2
    vacuum_exponent = sp.simplify(sp.limit(-2 * n_new * sp.log(blank), h, 0))
    require(sp.simplify(vacuum_exponent - 8 * sp.pi ** 2 * p ** 2 * aa ** 2) == 0,
            "physical complete blank probability matches the owned kappa128 exponent")
    old_vacuum_exponent = sp.simplify(sp.limit(-2 * n_old * sp.log(blank), h, 0))
    port_surplus = sp.simplify(sp.limit(n_new * p * epsilon * delta, h, 0))
    require(old_vacuum_exponent == 0 and
            sp.simplify(port_surplus - 8 * sp.pi ** 2 * p ** 3 * aa ** 2) == 0,
            "old physical horizon is vacuum while the new port surplus remains genuinely paid")
    delta_tilde_limit = sp.simplify(sp.limit(delta / h ** 2, h, 0))
    cross_rate_limit = sp.simplify(2 * sp.pi ** 2 * f_limit)
    require(sp.simplify((n_new * tau) * delta_tilde_limit - vacuum_exponent) == 0,
            "rescaled Fock vacuum exponent uses T=2p**2 without a new coefficient")
    return {"physical_coframe_parameter": "nu_h=h*a",
            "q_phys": str(sp.factor(q_phys)), "q_phys_chain_rule": "h**2*q_h(h*a)",
            "new_n_h": "128/h**4", "tau_h": "epsilon_h*h**2=p**2*h**4/64",
            "rescaled_horizon": "n_new*tau_h=2*p**2",
            "new_n_h_q_phys_limit": str(new_norm_limit),
            "old_n_h_q_phys_limit": str(old_norm_limit),
            "f_ha_hb_over_h2_limit": str(f_limit),
            "Delta_tilde_limit": str(delta_tilde_limit),
            "cross_rate_limit": str(cross_rate_limit),
            "new_complete_blank_probability_limit": "exp(-8*pi**2*p**2*a**2)",
            "new_blank_probability_exponent": str(vacuum_exponent),
            "old_complete_blank_probability_limit": 1,
            "original_epsilon_duration_on_new_horizon": "2*p**2/h**2",
            "mandatory_original_port_clock_baseline": "128/h**4",
            "new_clock_is_not_the_previous_fixed_clock": True,
            "field_sensitive_port_surplus_limit": str(port_surplus)}


class LiteralRound:
    """Numpy evaluation of the owned native_select/reflection/Golden words.

    The literal word pairs and duplication are copied from the pinned
    native_select definition; creator matrices come directly from that
    imported owner. An independent exact-owner call pins every SELECT row.
    """
    def __init__(self, owned):
        self.owned = owned
        self.p = float(owned.p)
        self.identity = np.eye(16, dtype=complex)
        self.creators = [np.array(owned.creator(r)).astype(complex) for r in range(4)]
        self.walsh = np.array([[(-1) ** ((label & word).bit_count())
                                for word in range(32)] for label in range(32)])

    def rows(self, nu, phases, with_jet=False):
        b = math.sqrt(1 - nu ** 2)
        db = -nu / b
        words, derivative = [], []
        for r in range(4):
            creator = self.creators[r]
            proj_l, proj_r = creator @ creator.T, creator.T @ creator
            pp, cc = nu * phases[r] * creator, nu * creator
            ll = self.identity + (b - 1) * proj_l
            rr = self.identity + (b - 1) * proj_r
            dpp, dcc = phases[r] * creator, creator
            dll, drr = db * proj_l, db * proj_r
            for term, tangent in zip(((pp, ll), (pp.conj().T, rr), (-cc, -ll), (-cc.T, -rr)),
                                     ((dpp, dll), (dpp.conj().T, drr), (-dcc, -dll), (-dcc.T, -drr))):
                words.extend((term, term))
                derivative.extend((tangent, tangent))
        rows = np.einsum("lj,jcuv->lcuv", self.walsh, np.array(words)).reshape(64, 16, 16) / 32
        drows = None
        if with_jet:
            drows = np.einsum("lj,jcuv->lcuv", self.walsh, np.array(derivative)).reshape(64, 16, 16) / 32
        return rows, drows

    def kraus(self, nu, phases, with_jet=False):
        rows, drows = self.rows(nu, phases, with_jet)
        a = rows[0]
        action = adjoint(rows) @ a
        physical = np.empty((128, 16, 16), dtype=complex)
        physical[0::2] = -2 * self.p ** 2 * action
        physical[1::2] = -2 * self.p * math.sqrt(self.p) * action
        physical[0] += self.identity
        delta = None
        if with_jet:
            daction = adjoint(drows) @ a + adjoint(rows) @ drows[0]
            delta = np.empty_like(physical)
            delta[0::2] = -2 * self.p ** 2 * daction
            delta[1::2] = -2 * self.p * math.sqrt(self.p) * daction
        return physical, delta


def gram(left, right):
    return np.einsum("gji,gjk->ik", left.conj(), right)


def run(step):
    start = time.perf_counter()
    owned = load_owned()
    symbolic = exact_general_jet()
    sectors = exact_sector_normalization()
    physical_scaling = exact_physical_scale()
    literal = LiteralRound(owned)
    first_phases = [1j, 1, 1, 1]
    exact_rows = owned.native_select(sp.Rational(3, 5), sp.Rational(4, 5), [sp.I, 1, 1, 1])
    expected_rows = np.array([np.array(row).astype(complex) for row in exact_rows])
    actual_rows, _ = literal.rows(3 / 5, first_phases)
    calibration_error = maximum(actual_rows - expected_rows)
    require(calibration_error < 5e-16, "all64 SELECT rows match independently imported exact owner")
    h, n, w = .25, 2048, 2.
    epsilon = literal.p ** 2 * h ** 2 / 64
    cases = []
    maxima = {"normalization": 0., "connection": 0., "mixed_q": 0.,
              "all128_matrix_derivative_FD": 0., "full_cross": 0.,
              "blank_scalar": 0., "blank_scalar_jet": 0.,
              "all127_nonblank_effect": 0., "all127_nonblank_effect_jet": 0.}
    omitted_blank_port1_defects = []
    for role in range(4):
        for sign in (1, -1):
            phases = [1 + 0j] * 4
            phases[role] = sign * 1j
            point_kraus = []
            for rational in (sp.Rational(3, 5), sp.Rational(5, 13)):
                nu = float(rational)
                kk, dk = literal.kraus(nu, phases, with_jet=True)
                minus, _ = literal.kraus(nu - step, phases)
                plus, _ = literal.kraus(nu + step, phases)
                fd = (plus - minus) / (2 * step)
                q = literal.p ** 2 * w / 128 * (2 - nu ** 2) / (1 - nu ** 2)
                normalization_error = maximum(gram(kk, kk) - literal.identity)
                connection_error = maximum(gram(kk, dk))
                mixed_error = maximum(gram(dk, dk) - q * literal.identity)
                fd_error = maximum(fd - dk)
                delta = nu ** 2 * w / h ** 2
                delta_prime = 2 * nu * w / h ** 2
                blank = 1 - epsilon * delta / 2
                blank_prime = -epsilon * delta_prime / 2
                nonblank = epsilon * delta - epsilon ** 2 * delta ** 2 / 4
                nonblank_prime = (epsilon - epsilon ** 2 * delta / 2) * delta_prime
                blank_error = maximum(kk[0] - blank * literal.identity)
                blank_jet_error = maximum(dk[0] - blank_prime * literal.identity)
                nonblank_error = maximum(gram(kk[1:], kk[1:]) - nonblank * literal.identity)
                nonblank_jet_error = maximum(gram(dk[1:], kk[1:]) + gram(kk[1:], dk[1:]) -
                                              nonblank_prime * literal.identity)
                require(max(blank_error, blank_jet_error, nonblank_error, nonblank_jet_error) < 3e-15,
                        "actual blank and ALL127 nonblank effects and their scalar derivatives")
                # Physical index1 is port1/blank: it belongs to the127
                # marked outputs, even though its continuum limit is zero.
                omitted_defect = nonblank * literal.identity - gram(kk[2:], kk[2:])
                special_effect = gram(kk[1:2], kk[1:2])
                special_expected = epsilon ** 2 * delta ** 2 / (4 * literal.p)
                special_prime = epsilon ** 2 * delta * delta_prime / (2 * literal.p)
                require(maximum(omitted_defect - special_effect) < 3e-15 and
                        maximum(special_effect - special_expected * literal.identity) < 3e-15,
                        "hostile omission of port1/blank loses its actual nonzero effect")
                require(maximum(gram(dk[1:2], kk[1:2]) + gram(kk[1:2], dk[1:2]) -
                                special_prime * literal.identity) < 3e-15,
                        "actual special port1/blank derivative retained")
                require(special_expected > 0 and special_prime > 0,
                        "omitted special blank-port effect and source are strictly nonzero")
                omitted_blank_port1_defects.append(special_expected)
                require(normalization_error < 3e-15 and connection_error < 3e-15 and mixed_error < 3e-15,
                        "actual all128 original normalization, zero connection and mixed-q matrix")
                require(fd_error < 2e-9, "all128 actual matrix derivatives match centered finite difference")
                maxima["normalization"] = max(maxima["normalization"], normalization_error)
                maxima["connection"] = max(maxima["connection"], connection_error)
                maxima["mixed_q"] = max(maxima["mixed_q"], mixed_error)
                maxima["all128_matrix_derivative_FD"] = max(maxima["all128_matrix_derivative_FD"], fd_error)
                for key, error in (("blank_scalar", blank_error), ("blank_scalar_jet", blank_jet_error),
                                   ("all127_nonblank_effect", nonblank_error),
                                   ("all127_nonblank_effect_jet", nonblank_jet_error)):
                    maxima[key] = max(maxima[key], error)
                cases.append({"momentum_role": role, "momentum_sign": sign, "nu": str(rational),
                              "q_h": q, "n_h_q_h": n * q,
                              "normalization_max_error": normalization_error,
                              "connection_max_error": connection_error,
                              "mixed_q_max_error": mixed_error,
                              "Delta_h_scalar": delta, "Delta_h_scalar_jet": delta_prime,
                              "blank_B": blank, "blank_B_jet": blank_prime,
                              "nonblank_u": nonblank, "nonblank_u_jet": nonblank_prime,
                              "omitted_port1_blank_norm_defect": special_expected,
                              "omitted_port1_blank_source_defect": special_prime,
                              "all128_matrix_derivative_FD_max_error": fd_error})
                point_kraus.append(kk)
            vx, vy = 3 / 5, 5 / 13
            bx, by = 4 / 5, 12 / 13
            t = (1 + vx * vy + bx * by) / 2
            f = vx ** 2 + vy ** 2 - 2 * t * vx * vy
            cross_expected = 1 - literal.p ** 2 * w * f / 128
            cross_error = maximum(gram(point_kraus[1], point_kraus[0]) - cross_expected * literal.identity)
            require(cross_error < 3e-15, "owned full128 two-arm scalar cross on all eight first-shell momenta")
            maxima["full_cross"] = max(maxima["full_cross"], cross_error)
    nu_min, nu_max = 5 / 13, 3 / 5
    compact_uniform_bound = 4 * math.pi ** 2 * literal.p ** 2 * (1 + 1 / (1 - nu_max ** 2))
    require(max(row["n_h_q_h"] for row in cases) < compact_uniform_bound,
            "exact physical-clock mixed norm is below the compact-chart uniform bound")
    physical_cases = []
    for rational in (sp.Rational(3, 5), sp.Rational(5, 13)):
        aa = float(rational)
        nu = h * aa
        kk, dnu_kk = literal.kraus(nu, first_phases, with_jet=True)
        da_kk = h * dnu_kk
        minus, _ = literal.kraus(h * (aa - step), first_phases)
        plus, _ = literal.kraus(h * (aa + step), first_phases)
        fd = (plus - minus) / (2 * step)
        q_phys = h ** 2 * literal.p ** 2 * w / 128 * (2 - nu ** 2) / (1 - nu ** 2)
        connection_error = maximum(gram(kk, da_kk))
        mixed_error = maximum(gram(da_kk, da_kk) - q_phys * literal.identity)
        fd_error = maximum(fd - da_kk)
        require(connection_error < 3e-15 and mixed_error < 3e-15 and fd_error < 2e-9,
                "literal physical nu=ha matrices retain the complete rescaled a-jet")
        delta_phys = aa ** 2 * w
        tau = epsilon * h ** 2
        require(maximum(kk[0] - (1 - tau * (delta_phys / h ** 2) / 2) * literal.identity) < 3e-15,
                "same physical blank equals I-tau*Delta_tilde/2")
        physical_cases.append({"a": str(rational), "actual_nu_h": nu,
                               "h": h, "n_new": 128 * 4 ** 4, "tau_h": tau,
                               "q_phys": q_phys, "n_new_q_phys": 128 * 4 ** 4 * q_phys,
                               "old_n_q_phys": n * q_phys,
                               "connection_max_error": connection_error,
                               "mixed_q_phys_max_error": mixed_error,
                               "all128_a_derivative_FD_max_error": fd_error})
    physical_scaling["literal_positive_first_role_controls_at_existing_mesh"] = physical_cases
    return {
        "status": "PASS", "elapsed_seconds": time.perf_counter() - start,
        "original_fixture_source_sha256": PRIOR_SHA256,
        "imported_owner_main_not_executed": True,
        "exact_general_cross_differentiation": symbolic,
        "scalar_sector_and_embedding_calibration": sectors,
        "separate_physical_coframe_scaling": physical_scaling,
        "hostile_omitted_port1_blank": {
            "minimum_actual_norm_defect": min(omitted_blank_port1_defects),
            "all_eight_momenta_and_both_nu_detect_omission": True},
        "literal_matrix_verification": {
            "independent_exact_owner_SELECT_calibration_error": calibration_error,
            "maximum_errors": maxima, "centered_difference_step": step,
            "centered_difference_float_tolerance": 2e-9, "cases": cases},
        "carrier": {"CAR_grades": 16, "first_shell_momenta": 8,
                    "oldRIGHT_dimension": 128, "retained_single_round_outcomes": 128,
                    "actual_SELECT_rows": 64, "duplicated_SELECT_words": 32,
                    "original_exterior_order": [0, 2, 3, 1],
                    "data_first_shell_dimension": 128,
                    "with_oldRIGHT_input_dimension": 16384,
                    "oldRIGHT_lift": "every displayed operator tensor I128; no reference truncation",
                    "h": h, "n_h": n, "epsilon_h": epsilon,
                    "n_h_epsilon_h": n * epsilon},
        "compact_chart": {"nu_min": nu_min, "nu_max": nu_max,
                          "n_h_q_h_uniform_upper_bound": compact_uniform_bound,
                          "exact_bound_formula": "4*pi**2*p**2*(1+1/(1-nu_max**2))",
                          "diagonal_Born_tape_derivative_TV_bound": "2*sqrt(n_h*q_h)",
                          "one_arm_normalized_cylinder_derivative_TV_bound":
                              "c_h**(-k)*(sqrt(k*q_h(x))+k*abs(partial_x(log(c_h))))*norm(chi)*norm(psi)",
                          "uniform_depth_range": "0 <= k <= n_h = 128/h**2"},
        "scope": {"finite_physical_clock_family_only": True,
                  "fixed_h_infinite_depth_bound_claimed": False,
                  "independent_data_copies_assumed": False,
                  "full_history_words_enumerated": False,
                  "changing_data_handled_by_exact_cross_transfer": True,
                  "moving_endpoint_preparations_included": False,
                  "nonuniform_primary_preparation_application_claimed": False,
                  "full_Book_Info_or_memory_readout_identified": False,
                  "TV_C1_refinement_convergence_proved": False,
                  "raw_h_minus_2_source_convergence_proved": False,
                  "float_matrix_checks_are_not_interval_certificates": True,
                  "GR_closed": False}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fd-step", type=float, default=2e-5)
    parser.add_argument("--save", type=Path)
    args = parser.parse_args()
    require(args.fd_step > 0, "positive independent finite-difference step")
    result = run(args.fd_step)
    encoded = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.save is not None:
        require(args.save.resolve().parent == Path(__file__).resolve().parent,
                "receipt writes stay inside this new source packet")
        args.save.write_text(encoded, encoding="utf-8", newline="\n")
    print(encoded, end="")
