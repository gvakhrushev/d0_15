#!/usr/bin/env python3
"""Bounded literal full128 controls for the coherent-mode/info-price theorem.

Pinned native definitions are imported without their historical runners.
Every check is active under python -O. No long-history enumeration, geometry
rebuild, compulsory Info assignment, or physical GR acceptance is performed.
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

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
sys.dont_write_bytecode = True

import mpmath as mp
import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
PINNED = {
    "02_REGISTRY/research/sources/d0_native_relative_transfer_2026-10-17/check_native_relative_transfer.py":
        "dfa8fffb08d421f2a2a0fa91a3044492ab94bfd6bd7d1e86b110b52c2e0ff065",
    "02_REGISTRY/research/sources/d0_native_relative_history_first_jet_2026-10-20/check_relative_history_first_jet.py":
        "0c69dc21fd66e06eefacf9ab047f186ff1e4e93818aff38aca4187968a70b468",
    "02_REGISTRY/research/sources/d0_native_relative_history_first_jet_2026-10-20/RESULT.md":
        "d1c3cff174b2e4d03481ca6b3d18a1da2d3b65baba1f2dbf886324d8ce7f607d",
    "02_REGISTRY/research/A4D_NATIVE_FULL128_RELATIVE_TRANSFER_AND_CONDENSED_DESCENT.md":
        "577cbc909f766468fbef8ab38a5986ae761d348b075c2f38b2e1a88b704d4b3e",
}
COUNTS: dict[str, int] = {}


def require(condition, label, group):
    if not bool(condition):
        raise ArithmeticError(f"{group}: {label}")
    COUNTS[group] = COUNTS.get(group, 0) + 1


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def maximum(a):
    return float(np.max(np.abs(a)))


def adjoint(a):
    return a.swapaxes(-1, -2).conj()


def load_snapshot(path, name):
    spec = importlib.util.spec_from_file_location(name, HERE / "inputs" / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scalar_effect(mats):
    return np.einsum("gji,gjk->ik", mats.conj(), mats)


def scalar_output(mats):
    return np.einsum("gij,gkj->ik", mats, mats.conj())


def binary_entropy(q):
    if q == 0 or q == 1:
        return 0.0
    return -q * math.log(q) - (1-q) * math.log1p(-q)


def entropy(values):
    values = np.asarray(values, float)
    return -float(np.sum(values[values > 0] * np.log(values[values > 0])))


def round_value(value):
    """Readable deterministic scientific values, without environmental fields."""
    return round(float(value), 10)


def exact_walsh_and_car(owned, literal):
    group = "exact_original_walsh_car"
    require(owned.ORDER == (0, 2, 3, 1), "original creator ordering", group)
    signs = np.array([1 if (j & 4) == 0 else -1 for j in range(32)], dtype=int)
    transform = literal.walsh @ signs
    expected = np.zeros(32, dtype=int)
    expected[4] = 32
    require(np.array_equal(transform, expected), "literal duplicated sign word is Walsh4", group)
    zero_rows = owned.native_select(sp.Integer(0), sp.Integer(1), [sp.Integer(1)]*4)
    for alpha, row in enumerate(zero_rows):
        require(row == (owned.I if alpha == 9 else owned.O),
                f"exact native SELECT row {alpha} at limiting coefficient", group)
    identity = np.eye(16, dtype=complex)
    traces = []
    for role in range(4):
        c = literal.creators[role]
        require(np.array_equal(c @ c.T + c.T @ c, identity), "exact CAR diagonal", group)
        for sign in (-1, 1):
            q = 1j*sign*(c-c.T)
            require(np.array_equal(q, q.conj().T), "limiting Q self-adjoint", group)
            require(np.array_equal(q @ q, identity), "limiting Q squared is identity", group)
            require(np.trace(q) == 0, "limiting Q has balanced full16 trace", group)
            traces.append(int(np.trace(q).real))
    require(transform[9] == 0 and transform[1] == 0,
            "hostile label9/label1 confuse the flattened alpha9 with Walsh4", group)
    return {"walsh_character": 4, "flattened_SELECT_index": 9,
            "limiting_physical_Kraus_indices": [18, 19],
            "eight_Q_block_traces": traces,
            "full_DATA_dimension": 128, "oldRIGHT_dimension": 128}


def literal_physical_rounds(literal):
    group = "literal_full128_eight_blocks"
    p = literal.p
    identity = literal.identity
    ls = (4, 8, 16, 32, 64)
    amplitudes = (0.25, 0.5, 0.75)
    rows_out = []
    max_errors = {key: 0.0 for key in
                  ("TP", "unital", "TP_jet", "unital_jet", "blank", "blank_jet",
                   "return_price_effect", "return_price_jet", "normalized_jump_TP")}
    convergence = {"L": [], "jump_value_error": [], "jump_jet_error": [],
                   "normalized_jump_error": [], "normalized_jump_jet": []}
    dropped_blank = None
    for L in ls:
        h = 1.0/L
        w = 4*math.sin(math.pi*h)**2
        eps = p*p*h*h/64
        tau = eps*h*h
        n = 128*L**4
        errs = [0.0, 0.0, 0.0, 0.0]
        for a in amplitudes:
            nu = h*a
            xx = eps*a*a*w
            dxx = 2*eps*a*w
            blank = 1-xx/2
            u = xx-xx*xx/4
            du = dxx*(1-xx/2)
            expected_return = p*xx
            for role in range(4):
                for sign in (-1, 1):
                    phases = np.ones(4, dtype=complex)
                    phases[role] = np.exp(sign*2j*math.pi*h)
                    K, dK_nu = literal.kraus(nu, phases, with_jet=True)
                    dK = h*dK_nu  # Actual physical a derivative, never the nu derivative.
                    require(K.shape == (128, 16, 16), "all128 outcomes on each real CAR16 block", group)
                    require(np.isfinite(K).all() and np.isfinite(dK).all(), "finite literal matrices and jets", group)
                    tp, unital = scalar_effect(K), scalar_output(K)
                    cross_in = np.einsum("gji,gjk->ik", dK.conj(), K)
                    cross_out = np.einsum("gij,gkj->ik", dK, K.conj())
                    tp_jet, unital_jet = cross_in+cross_in.conj().T, cross_out+cross_out.conj().T
                    ret, dret = K[1::2], dK[1::2]
                    ret_effect = scalar_effect(ret)
                    ret_cross = np.einsum("gji,gjk->ik", dret.conj(), ret)
                    ret_jet = ret_cross+ret_cross.conj().T
                    errors = {
                        "TP": maximum(tp-identity), "unital": maximum(unital-identity),
                        "TP_jet": maximum(tp_jet), "unital_jet": maximum(unital_jet),
                        "blank": maximum(K[0]-blank*identity),
                        "blank_jet": maximum(dK[0]+dxx*identity/2),
                        "return_price_effect": maximum(ret_effect-expected_return*identity),
                        "return_price_jet": maximum(ret_jet-p*dxx*identity),
                    }
                    for key, value in errors.items():
                        max_errors[key] = max(max_errors[key], value)
                        require(value < 8e-13, f"actual {key} identity", group)
                    J = K[1:]/math.sqrt(u)
                    dJ = (dK[1:] - K[1:]*(du/(2*u)))/math.sqrt(u)
                    norm_error = maximum(scalar_effect(J)-identity)
                    max_errors["normalized_jump_TP"] = max(max_errors["normalized_jump_TP"], norm_error)
                    require(norm_error < 2e-12, "normalized entire127-jump isometry", group)
                    q = 1j*sign*(literal.creators[role]-literal.creators[role].T)
                    target = np.zeros_like(K)
                    target[18] = -2*math.pi*a*p*q
                    target[19] = -2*math.pi*a*math.sqrt(p)*q
                    dtarget = target/a
                    scaled, dscaled = K.copy()/math.sqrt(tau), dK.copy()/math.sqrt(tau)
                    scaled[0] = 0
                    dscaled[0] = 0
                    errs[0] = max(errs[0], maximum(scaled-target))
                    errs[1] = max(errs[1], maximum(dscaled-dtarget))
                    normalized_target = target[1:]/(2*math.pi*a)
                    errs[2] = max(errs[2], maximum(J-normalized_target))
                    errs[3] = max(errs[3], maximum(dJ))
                    if L == 4 and a == 0.5 and role == 0 and sign == 1:
                        physical_step = 2.0**-18
                        plus, _ = literal.kraus(h*(a+physical_step), phases)
                        minus, _ = literal.kraus(h*(a-physical_step), phases)
                        fd_error = maximum((plus-minus)/(2*physical_step)-dK)
                        require(fd_error < 2e-10, "independent actual physical-a derivative spot check", group)
                        wrong_ret_cross = np.einsum("gji,gjk->ik", dK_nu[1::2].conj(), ret)
                        wrong_ret_jet = wrong_ret_cross+wrong_ret_cross.conj().T
                        require(maximum(wrong_ret_jet-ret_jet/h) < 2e-15,
                                "wrong nu jet differs by the missing physical chain factor", group)
                        require(maximum(wrong_ret_jet-ret_jet) > 1e-6,
                                "hostile omission of h changes the actual paid source", group)
                        special = scalar_effect(K[1:2])
                        special_expected = p*eps*h*h*(a*a*w)**2/256
                        require(maximum(special-special_expected*identity) < 2e-18,
                                "literal port1/blank retained mass", group)
                        require(special_expected > 1e-9, "dropping special failure has visible finite defect", group)
                        kept = np.delete(K, 1, axis=0)
                        require(maximum(scalar_effect(kept)-identity) > 1e-9,
                                "hostile omission of port1/blank fails normalization", group)
                        dropped_blank = {"one_round_missing_probability": round_value(special_expected),
                                         "n_round_missing_expected_returns": round_value(n*special_expected),
                                         "direct_physical_a_derivative_error": round_value(fd_error),
                                         "wrong_native_nu_source_factor": 1/h}
            rows_out.append({"L": L, "a": a, "rounds": n,
                             "nonblank_mean": round_value(n*u),
                             "nonblank_mean_derivative": round_value(n*du),
                             "paid_port_excess": round_value(n*p*xx),
                             "paid_port_excess_derivative": round_value(n*p*dxx)})
        convergence["L"].append(L)
        for key, value in zip(("jump_value_error", "jump_jet_error", "normalized_jump_error", "normalized_jump_jet"), errs):
            convergence[key].append(round_value(value))
        require(errs[0] < 18*h and errs[1] < 25*h,
                "all original marks and actual jets approach the two-mark limit", group)
        require(errs[2] < 3*h and errs[3] < 3*h,
                "normalized jumps approach the Golden Q marks with zero a jet", group)
    for key in ("jump_value_error", "jump_jet_error", "normalized_jump_error", "normalized_jump_jet"):
        values = convergence[key]
        require(values[-1] < values[0]/10, "observed common fine-mesh convergence: "+key, group)
    return {"meshes": list(ls), "physical_amplitudes": list(amplitudes),
            "evaluated_block_instruments": len(ls)*len(amplitudes)*8,
            "all128_outcomes_per_block": True,
            "max_identity_errors": {k: round_value(v) for k,v in max_errors.items()},
            "convergence": convergence, "actual_paid_clock": rows_out,
            "hostile_dropped_port1_blank": dropped_blank,
            "maximally_mixed_full128_DATA_entropy_exact": "log(128), by proved literal unitality"}


def coherent_poisson_cats(p):
    group = "coherent_poisson_cat_controls"
    T = 2*p*p
    k = np.arange(120, dtype=float)
    results = []
    for Lambda in (0.1, 0.48902733391562237, 2.0, 6.0):
        coeff = np.empty(len(k))
        coeff[0] = math.exp(-Lambda/2)
        for j in range(1, len(k)):
            coeff[j] = coeff[j-1]*math.sqrt(Lambda/j)
        prob = coeff*coeff
        require(abs(float(prob.sum())-1) < 2e-14, "controlled finite coherent/Poisson tail", group)
        require(abs(float(prob@k)-Lambda) < 3e-13, "Poisson mean from complete coefficients", group)
        peven = float(prob[::2].sum())
        podd = float(prob[1::2].sum())
        expected_odd = (1-math.exp(-2*Lambda))/2
        require(abs(podd-expected_odd) < 2e-14, "actual even/odd sector weights", group)
        a = math.sqrt(Lambda/(4*math.pi**2*T))
        dLambda = 8*math.pi**2*T*a
        dcoeff = coeff*(k-Lambda)*dLambda/(2*Lambda)
        dprob = prob*(k-Lambda)*dLambda/Lambda
        positive = prob > 0
        fisher = float(np.sum(dprob[positive]**2/prob[positive]))
        qfi = 4*(float(dcoeff@dcoeff)-float(coeff@dcoeff)**2)
        expected_fisher = 16*math.pi**2*T
        require(abs(fisher-expected_fisher) < 2e-11 and abs(qfi-expected_fisher) < 2e-11,
                "counting exactly saturates the real coherent amplitude Fisher", group)
        require(abs(float(dprob.sum())) < 2e-13, "all-count first source normalized", group)
        cat_entropies = []
        parity = np.where((k.astype(int) % 2) == 0, 1.0, -1.0)
        negative = coeff*parity
        for r in (-1.0, -0.3, 0.0, 0.6, 1.0):
            # Direct finite coherent-cat density; keep cross-number coherence.
            rho = ((1+r)*np.outer(coeff, coeff)+(1-r)*np.outer(negative, negative))/2
            eigen = np.linalg.eigvalsh(rho)
            require(eigen.min() > -2e-14, "retained coherent cat is positive", group)
            eigen[np.abs(eigen) < 2e-14] = 0
            rad = math.sqrt(r*r+(1-r*r)*math.exp(-4*Lambda))
            expected = np.array([(1-rad)/2, (1+rad)/2])
            require(maximum(eigen[-2:]-expected) < 4e-14, "actual two nonzero record eigenvalues", group)
            ent = entropy(eigen)
            require(abs(ent-binary_entropy((1-rad)/2)) < 2e-12, "full fresh-record entropy formula", group)
            if r == 0:
                require(abs(ent-binary_entropy(expected_odd)) < 2e-12, "maximally mixed DATA cat entropy", group)
            cat_entropies.append({"r": r, "entropy": round_value(ent)})
        pointer_entropy = entropy(prob)
        coherent_entropy = binary_entropy(expected_odd)
        require(pointer_entropy > coherent_entropy+0.01,
                "hostile dephasing count coherences changes Info on same state", group)
        results.append({"Lambda": Lambda, "even": round_value(peven), "odd": round_value(podd),
                        "count_Fisher": round_value(fisher), "coherent_QFI": round_value(qfi),
                        "count_Shannon": round_value(pointer_entropy),
                        "fresh_coherent_entropy": round_value(coherent_entropy),
                        "cat_entropies": cat_entropies})
    for aa, bb in ((0.1, 0.3), (0.3, 0.5)):
        la, lb = 4*math.pi**2*T*aa*aa, 4*math.pi**2*T*bb*bb
        cross_terms = np.empty(120)
        cross_terms[0] = math.exp(-(la+lb)/2)
        for j in range(1, len(cross_terms)):
            cross_terms[j] = cross_terms[j-1]*math.sqrt(la*lb)/j
        expected = math.exp(-2*math.pi**2*T*(aa-bb)**2)
        require(abs(float(cross_terms.sum())-expected) < 3e-14,
                "coherent mode reproduces the owned all-input cross", group)
    return {"number_cutoff": 119, "controls": results,
            "pointer_count_is_only_classically_sufficient": True,
            "record_only_entropy_is_not_global_pure_output_entropy": True}


def finite_clock_entropy(p):
    group = "finite_event_clock_entropy"
    a = 0.25
    phi = 1/p
    lam = 4*math.pi**2*a*a
    Lambda = 2*p*p*lam
    dLambda = 16*math.pi**2*p*p*a
    rows = []
    for L in (8, 16, 32, 64, 128, 256):
        h = 1/L
        eps = p*p*h*h/64
        tau = eps*h*h
        w = 4*math.sin(math.pi*h)**2
        n = 128*L**4
        xx, dxx = eps*a*a*w, 2*eps*a*w
        u, du = xx-xx*xx/4, dxx*(1-xx/2)
        m, dm = n*u, n*du
        flag_H = n*binary_entropy(u)
        flag_dH = n*du*(math.log1p(-u)-math.log(u))
        prob = [math.exp(n*math.log1p(-u))]
        logchoose = [0.0]
        for j in range(1, 100):
            prob.append(prob[-1]*(n-j+1)*u/(j*(1-u)))
            logchoose.append(logchoose[-1]+math.log(n-j+1)-math.log(j))
        mass = sum(prob)
        Hcount = entropy(prob)
        position_H = sum(q*l for q,l in zip(prob, logchoose))
        require(abs(mass-1) < 3e-13, "bounded binomial count tail", group)
        require(abs(Hcount+position_H-flag_H) < 2e-10,
                "exact event/timestamp entropy decomposition", group)
        finite_part = flag_H-m*math.log(1/tau)
        finite_derivative = flag_dH-dm*math.log(1/tau)
        target = Lambda*(1-math.log(lam))
        dtarget = -dLambda*math.log(lam)
        require(abs(finite_part-target) < 45*h*h,
                "finite-h timestamp subtraction has the stated limit", group)
        require(abs(finite_derivative-dtarget) < 250*h*h,
                "actual analytic clock entropy first source", group)
        # The owned proof controls the remaining mark entropy uniformly in C1.
        # This bounded check concerns the exact event-clock term, not a made-up
        # finite-h iid replacement for the changing-data mark process.
        paid_derivative = n*p*dxx
        log_slope = (paid_derivative-flag_dH/math.log(phi))/math.log(1/h)
        rows.append({"L": L, "Lambda_h": round_value(m),
                     "event_entropy": round_value(flag_H),
                     "count_entropy": round_value(Hcount),
                     "occupied_clock_entropy": round_value(position_H),
                     "finite_time_density_entropy": round_value(finite_part),
                     "finite_time_density_entropy_derivative": round_value(finite_derivative),
                     "paid_excess_derivative": round_value(paid_derivative),
                     "Cost_minus_event_Info_log_slope": round_value(log_slope)})
    require(rows[-1]["occupied_clock_entropy"] > rows[0]["occupied_clock_entropy"]+20,
            "hostile count-only Shannon erases the genuinely retained timestamps", group)
    return {"fixed_a": a, "controls": rows,
            "exact_remaining_mark_term_not_numerically_replaced": True,
            "asymptotic_full_pointer_price_log_slope": round_value(-64*math.pi**2*p*p*a/math.log(phi)),
            "physical_timestamp_counterterm_admitted": False}


def strict_minimum():
    group = "strict_coherent_price_minimum"
    with mp.workdps(90):
        phi = (1+mp.sqrt(5))/2
        p = 1/phi
        logphi = mp.log(phi)
        def equation(x):
            return 2*x*mp.atanh(x)-p*logphi
        lo, hi = mp.mpf("0.2"), mp.mpf("0.5")
        require(equation(lo) < 0 < equation(hi), "strict monotone root bracket", group)
        for _ in range(310):
            mid = (lo+hi)/2
            if equation(mid) < 0:
                lo = mid
            else:
                hi = mid
        x = (lo+hi)/2
        Lambda = -mp.log(x)/2
        a = mp.sqrt(Lambda/(8*mp.pi**2*p*p))
        def g(z):
            q = (1-mp.exp(-2*z))/2
            H = -q*mp.log(q)-(1-q)*mp.log(1-q)
            return p*z-H/logphi
        def gp(z):
            xx = mp.exp(-2*z)
            return p-2*xx*mp.atanh(xx)/logphi
        def gpp(z):
            xx = mp.exp(-2*z)
            return (4*xx*mp.atanh(xx)+4*xx*xx/(1-xx*xx))/logphi
        require(abs(equation(x)) < mp.mpf("1e-85"), "90-digit bracketed root residual", group)
        require(abs(Lambda-mp.mpf("0.48902733391562237")) < mp.mpf("1e-17"),
                "independent decimal minimum value", group)
        for z in (mp.mpf("0.01"), mp.mpf("0.1"), Lambda, mp.mpf("1"), mp.mpf("3")):
            require(abs(mp.diff(g,z)-gp(z)) < mp.mpf("1e-80"), "actual first derivative", group)
            require(abs(mp.diff(g,z,2)-gpp(z)) < mp.mpf("1e-78"), "actual second derivative", group)
            require(gpp(z) > 0, "strict convexity formula positive", group)
        require(gp(Lambda-mp.mpf("0.01")) < 0 < gp(Lambda+mp.mpf("0.01")),
                "opposite finite bracketing source signs", group)
        require(g(Lambda) < 0 and g(Lambda) < g(Lambda-mp.mpf("0.1"))
                and g(Lambda) < g(Lambda+mp.mpf("0.1")), "strict nonzero minimum beats endpoint and neighbours", group)
        require(p > 0, "including oldRIGHT removes the entropy source and leaves positive slope", group)
        return {"working_decimal_digits": 90,
                "root_equation": "2*x*atanh(x)=p*log(phi)",
                "x_star": mp.nstr(x, 70), "Lambda_star": mp.nstr(Lambda, 70),
                "a_star": mp.nstr(a, 70), "g_at_minimum": mp.nstr(g(Lambda), 70),
                "g_second_derivative_at_minimum": mp.nstr(gpp(Lambda), 70),
                "root_residual_absolute": mp.nstr(abs(equation(x)), 8),
                "root_bracket_width": mp.nstr(hi-lo, 8),
                "g_with_oldRIGHT_slope": mp.nstr(p, 70),
                "finite_h_minimizer_uniqueness_asserted": False}


def run():
    COUNTS.clear()
    for relative, expected in PINNED.items():
        require(digest(HERE/"inputs"/relative) == expected, "immutable input "+relative, "provenance")
    owned = load_snapshot(next(k for k in PINNED if k.endswith("check_native_relative_transfer.py")),
                          "native_coherent_price_owned_transfer")
    history = load_snapshot(next(k for k in PINNED if k.endswith("check_relative_history_first_jet.py")),
                            "native_coherent_price_owned_history")
    # Intentionally do NOT call load_owned() or run() in either snapshot:
    # their historical repository ROOT differs from this mirrored input root.
    literal = history.LiteralRound(owned)
    result = {
        "schema": "d0-native-full128-coherent-info-price/1",
        "source_commit": "c7a2e7c39fab6b60fa70a553998e9aa2ccc89f3f",
        "frozen_source_sha256": PINNED,
        "checker_sha256": digest(Path(__file__)),
        "proof_sha256": digest(HERE/"FULL128_COHERENT_LIMIT_AND_INFO_PRICE.md"),
        "exact_walsh_car": exact_walsh_and_car(owned,literal),
        "literal_finite_instruments": literal_physical_rounds(literal),
        "coherent_limit_controls": coherent_poisson_cats(literal.p),
        "finite_clock_entropy": finite_clock_entropy(literal.p),
        "strict_minimum": strict_minimum(),
        "scope": {
            "all_original128_outcomes_checked": True,
            "all_eight_first_shell_CAR16_blocks_checked": True,
            "actual_physical_a_derivatives_checked": True,
            "long_history_words_enumerated": False,
            "general_C1_convergence_is_analytical_input": True,
            "coherent_limit_is_fixed_isometric_image_not_free_decoder": True,
            "fresh_record_and_record_plus_oldRIGHT_are_distinct_Info_algebras": True,
            "compulsory_Book03_Info_selected": False,
            "full_D0_price_selected": False,
            "GR_closed": False,
        },
        "receipt_comparison": {
            "diagnostic_absolute_decimal_places": 10,
            "rounded_zero_diagnostic_is_not_exact_algebraic_zero": True,
            "floats_compare_absolute_tolerance": 1e-9,
            "floats_compare_relative_tolerance": 1e-10,
            "integers_booleans_strings_and_hashes_compare_exactly": True,
            "comparison_tolerances_do_not_replace_active_scientific_checks": True,
            "active_literal_identity_absolute_tolerance": 8e-13,
            "active_normalized_jump_absolute_tolerance": 2e-12,
            "active_direct_derivative_absolute_tolerance": 2e-10,
        },
    }
    for relative, expected in PINNED.items():
        require(digest(HERE/"inputs"/relative) == expected, "unchanged input after calculation "+relative, "provenance")
    result["check_groups"] = dict(COUNTS)
    result["check_count"] = sum(COUNTS.values())
    result["status"] = "PASS"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional path for the deterministic JSON receipt")
    args = parser.parse_args()
    payload = json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2)+"\n"
    if args.output is not None:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
