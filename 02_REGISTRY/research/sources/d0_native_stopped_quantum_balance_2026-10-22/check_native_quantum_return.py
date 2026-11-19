#!/usr/bin/env python3
"""Bounded actual full128 quantum first-return application.

Only pinned AST definitions of the original CAR16 constructor and its owned
joint jet are loaded. No historical suite executes. All128 fine labels enter
the CP maps, terminal and count comparisons. Every finite cap retains aborts.
The compressed CQ entropy is a value lower bound, never a source bound.
Default execution compares the immutable receipt without writing. Checks
survive python -O. These are double-precision diagnostics, not intervals.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm, lu_factor, lu_solve, solve_sylvester

ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / "02_REGISTRY/research/sources"
NATIVE = BASE / "d0_book_uniform_source_2026-10-21/check_uniform_book_source.py"
JET_SOURCE = BASE / "d0_native_complete_cq_source_2026-10-22/check_complete_history_source.py"
HISTORY_RECEIPT = BASE / "d0_native_complete_cq_source_2026-10-22/COMPLETE_HISTORY_RESULT.json"
PINS = {
    "native_constructor": "1c501d5609dda3e14a3da95aad0c77ea04ef48bf94921793a403fb058a805fe9",
    "native_joint_jet": "cd0052f10bc43abb3736a1637c850c2a3d637f428dd116f6320f68bcf84e3931",
    "one_two_round_receipt": "6218f76ba21a2eeba064b9a855395d3fd358cf7c4d7ae58d4f56a5c1f9ef0515",
}
P = (np.sqrt(5.0)-1.0)/2.0
ELL = float(np.log(1/P))
EYE = np.eye(16, dtype=complex)
SUPER_EYE = np.eye(256, dtype=complex)
CHECKS = []
MATRIX_TOL, ENTROPY_TOL, FD_TOL = 2e-11, 3e-12, 3e-9
RECEIPT_ATOL, RECEIPT_RTOL = 3e-10, 2e-7


def require(condition, name):
    if not bool(condition):
        raise ArithmeticError(name)
    CHECKS.append(name)


def adj(x):
    return x.conj().T


def herm(x):
    return (x+adj(x))/2


def mat(x):
    return x.reshape(16, 16)


def vec(x):
    return x.reshape(256)


def tr(x):
    value = np.trace(mat(x))
    if abs(value.imag) > 1e-11:
        raise ArithmeticError("unexpected imaginary trace")
    return float(value.real)


def norm1(x):
    return float(np.linalg.svd(mat(x), compute_uv=False).sum())


def pinned_bytes(path, pin, label):
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == pin, "immutable "+label+" SHA256")
    return raw


def load_inputs():
    env = {"np": np, "P": P, "EYE": EYE,
           "expm": expm, "solve_sylvester": solve_sylvester}
    for path, key, names in (
        (NATIVE, "native_constructor", {"adj", "herm", "root", "creators", "native"}),
        (JET_SOURCE, "native_joint_jet", {"native_joint_jet", "prepared"}),
    ):
        raw = pinned_bytes(path, PINS[key], key)
        body = [node for node in ast.parse(raw).body
                if isinstance(node, ast.FunctionDef) and node.name in names]
        require({node.name for node in body} == names, "only owned AST definitions loaded: "+key)
        exec(compile(ast.Module(body=body, type_ignores=[]), str(path), "exec"), env)
    raw = pinned_bytes(HISTORY_RECEIPT, PINS["one_two_round_receipt"], "consumed entropy receipt")
    return env, json.loads(raw)["original_native_full128"]


def coarse_maps(k, dk):
    """Row-vectorization: vec(K X K*)=(K tensor conjugate K) vec(X)."""
    maps, jets = [], []
    for a in (0, 1):
        value, source = np.zeros((256, 256), complex), np.zeros((256, 256), complex)
        for kb, db in zip(k[a::2], dk[a::2]):
            value += np.kron(kb, kb.conj())
            source += np.kron(db, kb.conj())+np.kron(kb, db.conj())
        maps.append(value)
        jets.append(source)
    return maps, jets


def fine_apply(k, dk, x, dx):
    return (k@x@adj(k), dk@x@adj(k)+k@dx@adj(k)+k@x@adj(dk))


def port_apply(k, dk, a, x, dx):
    """Independent native-matrix evaluation retaining every parity label."""
    ks, ds = k[a::2], dk[a::2]
    ka, da = ks.conj().transpose(0, 2, 1), ds.conj().transpose(0, 2, 1)
    return (np.sum((ks@x)@ka, axis=0),
            np.sum((ds@x)@ka+(ks@dx)@ka+(ks@x)@da, axis=0))


def factors(maps):
    return [lu_factor(SUPER_EYE-maps[1-a]) for a in (0, 1)]


def solve(facs, a, x, dual=False):
    return lu_solve(facs[a], x, trans=2 if dual else 0)


def power_jet(a, da, exponent):
    """Binary matrix product rule, independent of native-state recurrence."""
    value, source = SUPER_EYE.copy(), np.zeros_like(a)
    power, dpower = a.copy(), da.copy()
    while exponent:
        if exponent & 1:
            source = source@power+value@dpower
            value = value@power
        exponent //= 2
        if exponent:
            dpower = dpower@power+power@dpower
            power = power@power
    return value, source


def positive_log(x):
    ev, u = np.linalg.eigh(herm(x))
    if ev.min() <= 0:
        raise ArithmeticError("strictly positive coarse DATA required; no clipping")
    return (u*np.log(ev))@adj(u), ev, u


def log_jet(ev, u, dx):
    """Stable logarithm divided differences, including degeneracies."""
    diff = ev[:, None]-ev[None, :]
    divided = np.empty_like(diff)
    mask = diff != 0
    np.divide(np.log1p(diff/ev[None, :]), diff, out=divided, where=mask)
    np.divide(np.ones_like(diff), ev[None, :], out=divided, where=~mask)
    return u@(divided*(adj(u)@dx@u))@adj(u)


def entropy_jet(x, dx):
    logs, ev, _ = positive_log(x)
    return -float(ev@np.log(ev)), -tr(dx@(logs+EYE))


def compressed(maps, jets, facs, rho, drho, check=False, label=""):
    rv, drv = vec(rho), vec(drho)
    q = np.array([tr(a@rv) for a in maps])
    dq = np.array([tr(da@rv+a@drv) for a, da in zip(maps, jets)])
    logrho, rev, ru = positive_log(rho)
    dlogrho = log_jet(rev, ru, drho)
    s0, ds0 = entropy_jet(rho, drho)
    value = source = mi = dmi = conditional = dconditional = cq = dcq = 0.0
    gaps, probs, dprobs, prefix_err, dprefix_err = [], [], [], [], []
    end, dend = np.zeros_like(rho), np.zeros_like(rho)
    for a in (0, 1):
        for b in (0, 1):
            prefix = maps[b]@maps[a]@rv
            dprefix = jets[b]@maps[a]@rv+maps[b]@jets[a]@rv+maps[b]@maps[a]@drv
            if b == a:
                x, dx = mat(prefix), mat(dprefix)
            else:
                y = solve(facs, a, prefix)
                dy = solve(facs, a, dprefix+jets[b]@y)
                x, dx = mat(maps[a]@y), mat(jets[a]@y+maps[a]@dy)
            end += x
            dend += dx
            p, dp = tr(x), tr(dx)
            if p <= 0:
                raise ArithmeticError("positive coarse prefix required")
            sigma = herm(x/p)
            dsigma = (dx-dp*sigma)/p
            logsigma, ev, _ = positive_log(sigma)
            gaps.append(float(ev.min()))
            probs.append(p)
            dprobs.append(dp)
            prefix_err.append(abs(p-tr(prefix)))
            dprefix_err.append(abs(dp-tr(dprefix)))
            ref, dref = q[a]*q[b], dq[a]*q[b]+q[a]*dq[b]
            lr = float(np.log1p((p-ref)/ref))
            # -p+ref cancels in the normalized total and stabilizes tiny MI.
            classical, dclassical = p*lr-p+ref, dp*lr+dref*(1-p/ref)
            quantum = tr(x@(logsigma-logrho))
            dquantum = tr(dx@(logsigma-logrho)-x@dlogrho)
            value += classical+quantum
            source += dclassical+dquantum
            mi += classical
            dmi += dclassical
            ss, dss = -float(ev@np.log(ev)), -tr(dsigma@(logsigma+EYE))
            conditional += p*ss
            dconditional += dp*ss+p*dss
            cq += -p*np.log(p)+p*ss
            dcq += -dp*(np.log(p)+1)+dp*ss+p*dss
    chi, dchi = s0-conditional, ds0-dconditional
    if check:
        require(norm1(end-rho) < MATRIX_TOL and norm1(dend-drho) < MATRIX_TOL,
                label+": compressed terminal DATA and full source equal rho,drho")
        require(max(prefix_err) < 2e-12 and max(dprefix_err) < 2e-12,
                label+": actual first-two-port traces and sources retained")
        require(min(gaps) > .05, label+": all normalized coarse blocks have checked positive spectral gap")
        require(np.linalg.norm(np.array(probs).reshape(2, 2)-np.outer(q, q)) > 1e-8,
                label+": actual two-port law is not iid")
        require(abs(value-mi-chi) < ENTROPY_TOL and abs(source-dmi-dchi) < ENTROPY_TOL,
                label+": direct moving-reference D equals MI plus Holevo, with full source")
        hv, hd = -float(q@np.log(q)), -float(dq@(np.log(q)+1))
        require(abs(value-s0-2*hv+cq) < ENTROPY_TOL and abs(source-ds0-2*hd+dcq) < ENTROPY_TOL,
                label+": independent entropy formula matches noncommuting log derivative")
        require(value > mi > 0 and chi > 0, label+": genuinely quantum compressed witness is positive")
    return {"relative_entropy_nats": float(value), "source_nats": float(source),
            "source_golden_units": float(source/ELL),
            "first_two_port_MI_nats": float(mi), "first_two_port_MI_source": float(dmi),
            "terminal_DATA_Holevo_nats": float(chi), "terminal_DATA_Holevo_source": float(dchi),
            "prefix_probabilities": np.array(probs).reshape(2, 2).tolist(),
            "prefix_probability_sources": np.array(dprobs).reshape(2, 2).tolist(),
            "normalized_DATA_min_eigenvalues": gaps, "rho_min_eigenvalue": float(rev.min()),
            "terminal_trace_norm_error": norm1(end-rho),
            "terminal_source_trace_norm_error": norm1(dend-drho),
            "initial_entropy_nats": s0, "initial_entropy_source": ds0,
            "one_port_q": q.tolist(), "one_port_dq": dq.tolist()}


def uncapped_checks(k, dk, maps, jets, facs, rho, drho, label):
    rv, drv = vec(rho), vec(drho)
    incoming, dincoming, residuals = [], [], []
    for a in (0, 1):
        x = solve(facs, a, maps[a]@rv)
        dx = solve(facs, a, jets[a]@rv+maps[a]@drv+jets[1-a]@x)
        residuals.append(float(np.linalg.norm((SUPER_EYE-maps[1-a])@x-maps[a]@rv)))
        incoming.append(x)
        dincoming.append(dx)
    require(max(norm1(x-rv) for x in incoming) < MATRIX_TOL and
            max(norm1(x-drv) for x in dincoming) < MATRIX_TOL,
            label+": both actual return resolvents equal rho with full derivative")
    terminal = sum((a@x for a, x in zip(maps, incoming)), np.zeros(256, complex))
    dterminal = sum((da@x+a@dx for a, da, x, dx in zip(maps, jets, incoming, dincoming)),
                    np.zeros(256, complex))
    require(norm1(terminal-rv) < MATRIX_TOL and norm1(dterminal-drv) < MATRIX_TOL,
            label+": exact uncapped terminal DATA balance and derivative")
    occ, docc = rv+sum(incoming), drv+sum(dincoming)
    last_errors, dlast_errors, count_errors, dcount_errors = [], [], [], []
    for z, (kb, db) in enumerate(zip(k, dk)):
        native, dnative = fine_apply(kb, db, rho, drho)
        last, dlast = fine_apply(kb, db, mat(incoming[z % 2]), mat(dincoming[z % 2]))
        count, dcount = fine_apply(kb, db, mat(occ), mat(docc))
        last_errors.append(norm1(last-native))
        dlast_errors.append(norm1(dlast-dnative))
        count_errors.append(abs(tr(count)-3*tr(native)))
        dcount_errors.append(abs(tr(dcount)-3*tr(dnative)))
    require(max(last_errors) < MATRIX_TOL and max(dlast_errors) < MATRIX_TOL,
            label+": all128 last-fine DATA blocks and derivatives equal one-round blocks")
    require(max(count_errors) < MATRIX_TOL and max(dcount_errors) < MATRIX_TOL,
            label+": all128 expected fine counts and derivatives equal three times one-round values")
    require(abs(tr(occ)-3) < 2e-12 and abs(tr(docc)) < 2e-12,
            label+": non-reset mean rounds is three with zero stationary source")
    return {"resolvent_linear_solve_residuals": residuals,
            "terminal_trace_norm_error": norm1(terminal-rv),
            "terminal_source_trace_norm_error": norm1(dterminal-drv),
            "last_fine_max_trace_norm_error": max(last_errors),
            "last_fine_source_max_trace_norm_error": max(dlast_errors),
            "expected_fine_count_max_error": max(count_errors),
            "expected_fine_count_source_max_error": max(dcount_errors),
            "expected_rounds": tr(occ), "expected_rounds_source": tr(docc)}


def native_capped(k, dk, rho, drho, cap):
    terminal, dterminal = np.zeros_like(rho), np.zeros_like(rho)
    occ, docc = rho.copy(), drho.copy()
    abort, dabort = np.zeros_like(rho), np.zeros_like(rho)
    for a in (0, 1):
        alive, dalive = port_apply(k, dk, a, rho, drho)
        for _ in range(cap):
            occ += alive
            docc += dalive
            match, dmatch = port_apply(k, dk, a, alive, dalive)
            terminal += match
            dterminal += dmatch
            alive, dalive = port_apply(k, dk, 1-a, alive, dalive)
        abort += alive
        dabort += dalive
    return terminal+abort, dterminal+dabort, occ, docc, abort, dabort


def capped_checks(k, dk, maps, jets, rho, drho, cap, label):
    terminal, dterminal, occ, docc, abort, dabort = native_capped(k, dk, rho, drho, cap)
    rv, drv = vec(rho), vec(drho)
    phi, dphi = sum(maps), sum(jets)
    boundary, dboundary = np.zeros(256, complex), np.zeros(256, complex)
    for a in (0, 1):
        power, dpower = power_jet(maps[1-a], jets[1-a], cap)
        boundary += power@rv
        dboundary += dpower@rv+power@drv
    defect = (SUPER_EYE-phi)@boundary
    ddefect = -dphi@boundary+(SUPER_EYE-phi)@dboundary
    error, derror = norm1(vec(terminal-rho)-defect), norm1(vec(dterminal-drho)-ddefect)
    require(error < MATRIX_TOL and derror < MATRIX_TOL,
            label+f": cap{cap} exact terminal defect and independent binary product-rule derivative")
    require(norm1(vec(occ)-3*rv+boundary) < MATRIX_TOL and
            norm1(vec(docc)-3*drv+dboundary) < MATRIX_TOL,
            label+f": cap{cap} finite occupation and source retain the boundary")
    require(abs(tr(terminal)-1) < 2e-12 and abs(tr(dterminal)) < 2e-12,
            label+f": cap{cap} every match and abort retained with source normalization")
    require(tr(abort) > 0, label+f": cap{cap} positive abort mass retained")
    counts, dcounts = [], []
    for kb, db in zip(k, dk):
        one, done = fine_apply(kb, db, rho, drho)
        count, dcount = fine_apply(kb, db, occ, docc)
        tail, dtail = fine_apply(kb, db, mat(boundary), mat(dboundary))
        counts.append(abs(tr(count)-3*tr(one)+tr(tail)))
        dcounts.append(abs(tr(dcount)-3*tr(done)+tr(dtail)))
    require(max(counts) < MATRIX_TOL and max(dcounts) < MATRIX_TOL,
            label+f": cap{cap} all128 fine counts retain cap defect and derivative")
    return {"later_trial_cap": cap, "abort_mass": tr(abort), "abort_source": tr(dabort),
            "expected_rounds": tr(occ), "expected_rounds_source": tr(docc),
            "terminal_boundary_trace_norm": norm1(defect),
            "terminal_boundary_source_trace_norm": norm1(ddefect),
            "terminal_formula_trace_norm_error": error,
            "terminal_source_formula_trace_norm_error": derror,
            "all128_count_max_error": max(counts), "all128_count_source_max_error": max(dcounts)}


def frozen_control(k, dk, maps, jets, facs, rho, cap=8):
    """A real gate variation with drho=0, off the stationary input section."""
    rv, zero = vec(rho), np.zeros(256, complex)
    phi, dphi = sum(maps), sum(jets)
    ddelta = dphi@rv
    dincoming = [solve(facs, a, ddelta) for a in (0, 1)]
    predicted = ddelta+sum((maps[a]@dincoming[a] for a in (0, 1)), zero.copy())
    terminal_source = zero.copy()
    for a in (0, 1):
        x = solve(facs, a, maps[a]@rv)
        dx = solve(facs, a, jets[a]@rv+jets[1-a]@x)
        terminal_source += jets[a]@x+maps[a]@dx
    require(norm1(terminal_source-predicted) < MATRIX_TOL,
            "frozen rho: terminal defect is [I+sum A R] ddelta")
    require(norm1(predicted) > 1e-4 and abs(tr(sum(dincoming))) > 1e-4,
            "frozen rho: terminal and mean-count preparation defects remain nonzero")
    last_defects, count_defects, last_errors = [], [], []
    # Direct count derivative minus three times the one-round derivative.
    occ, docc = 3*rho, mat(sum(dincoming))
    for z, (kb, db) in enumerate(zip(k, dk)):
        native, dnative = fine_apply(kb, db, rho, mat(zero))
        _, dlast = fine_apply(kb, db, rho, mat(dincoming[z % 2]))
        correction = kb@mat(dincoming[z % 2])@adj(kb)
        _, dcount = fine_apply(kb, db, occ, docc)
        last_defects.append(norm1(correction))
        last_errors.append(norm1(dlast-dnative-correction))
        count_defects.append(tr(dcount)-3*tr(dnative))
    require(max(last_errors) < MATRIX_TOL and max(last_defects) > 1e-6,
            "frozen rho: all128 last-fine outputs retain their nonzero boundary correction")
    require(max(abs(x) for x in count_defects) > 1e-5,
            "frozen rho: expected fine-count defects are not erased")
    terminal, dterminal, capocc, dcapocc, abort, dabort = native_capped(k, dk, rho, np.zeros_like(rho), cap)
    boundary, dboundary, extra, count_extra = zero.copy(), zero.copy(), ddelta.copy(), zero.copy()
    for a in (0, 1):
        t, dt = maps[1-a], jets[1-a]
        power, dpower = power_jet(t, dt, cap)
        boundary += power@rv
        dboundary += dpower@rv
        total, term = zero.copy(), ddelta.copy()
        for _ in range(cap):
            total += term
            term = t@term
        extra += maps[a]@total+power@ddelta
        count_extra += total
    naive = -dphi@boundary+(SUPER_EYE-phi)@dboundary
    corrected = naive+extra
    require(norm1(vec(dterminal)-corrected) < MATRIX_TOL,
            "frozen rho: finite source includes [I+sum G_aK] ddelta")
    require(norm1(vec(dterminal)-naive) > 1e-5,
            "frozen rho: differentiating only the stationary cap formula fails")
    require(norm1(vec(dcapocc)+dboundary-count_extra) < MATRIX_TOL,
            "frozen rho: finite occupation keeps sum R_aK ddelta")
    # Actual fine-outcome charge c_z=1+port(z), plus log reference weights.
    # Structural zero labels have zero operators and zero jets identically.
    f = np.zeros_like(rho)
    direct_count = 0.0
    positive = 0
    for z, (kb, db, dg) in enumerate(zip(k, dk, count_defects)):
        qz = tr(kb@rho@adj(kb))
        if not np.count_nonzero(kb):
            require(not np.count_nonzero(db), f"adjoint price: structural dark label{z} has zero jet")
            continue
        require(qz > 0, f"adjoint price: native fine label{z} positive probability")
        positive += 1
        weight = 1+(z % 2)+np.log(qz)/ELL
        f += weight*(adj(kb)@kb)
        direct_count += dg*weight
    logrho, _, _ = positive_log(rho)
    bv = sum((solve(facs, a, vec(f), True) for a in (0, 1)), zero.copy())
    bv += (vec(logrho)+sum((solve(facs, a, adj(maps[a])@vec(logrho), True)
                            for a in (0, 1)), zero.copy()))/ELL
    b = mat(bv)
    direct = direct_count+tr(mat(terminal_source)@logrho)/ELL
    dual = tr(b@mat(ddelta))
    require(norm1(b-adj(b)) < 2e-10, "actual adjoint preparation residual B is Hermitian")
    require(abs(direct-dual) < 2e-11,
            "actual native B pairing equals independently differentiated fine-count and terminal defects")
    # Deliberately reverse the noncommuting resolvent/map adjoint order.
    wrong = sum((solve(facs, a, vec(f), True) for a in (0, 1)), zero.copy())
    wrong += (vec(logrho)+sum((adj(maps[a])@solve(facs, a, vec(logrho), True)
                              for a in (0, 1)), zero.copy()))/ELL
    require(norm1(b@rho-rho@b) > 1e-4,
            "actual native adjoint preparation operator does not commute with rho")
    require(abs(direct-tr(mat(wrong)@mat(ddelta))) > 1e-5,
            "negative control: reversing native resolvent/map adjoint order changes the source")
    return {"direction": "r with frozen initial rho", "drho": 0,
            "stationarity_defect_source_trace_norm": norm1(ddelta),
            "terminal_defect_source_trace_norm": norm1(terminal_source),
            "terminal_formula_error": norm1(terminal_source-predicted),
            "mean_rounds_source": tr(sum(dincoming)),
            "last_fine_max_boundary_source_trace_norm": max(last_defects),
            "fine_count_max_source_defect": max(abs(x) for x in count_defects),
            "fine_count_sum_source_defect": float(sum(count_defects)),
            "cap": cap, "cap_missing_extra_source_trace_norm": norm1(extra),
            "cap_corrected_source_error": norm1(vec(dterminal)-corrected),
            "cap_occupation_extra_source_trace_norm": norm1(count_extra),
            "cap_mean_rounds_source": tr(dcapocc),
            "adjoint_preparation_price": {
                "fine_charge": "c_z=1+port(z); additional paid ledgers remain external",
                "positive_fine_labels": positive,
                "direct_count_boundary_source": float(direct_count),
                "direct_terminal_quantum_source": tr(mat(terminal_source)@logrho)/ELL,
                "direct_total": float(direct), "B_pairing": float(dual),
                "absolute_difference": float(abs(direct-dual)),
                "wrong_order_operator_trace_norm_difference": norm1(bv-wrong),
                "wrong_order_pairing_difference": float(abs(direct-tr(mat(wrong)@mat(ddelta)))),
                "B_rho_commutator_trace_norm": norm1(b@rho-rho@b)}}


def compare_receipt(actual, expected, where="result"):
    if isinstance(expected, dict):
        if not isinstance(actual, dict) or actual.keys() != expected.keys():
            raise ArithmeticError("receipt structure changed at "+where)
        for key in expected:
            compare_receipt(actual[key], expected[key], where+"."+key)
    elif isinstance(expected, list):
        if not isinstance(actual, list) or len(actual) != len(expected):
            raise ArithmeticError("receipt list changed at "+where)
        for index, (a, e) in enumerate(zip(actual, expected)):
            compare_receipt(a, e, where+f"[{index}]")
    elif isinstance(expected, float):
        if not np.isfinite(actual) or abs(actual-expected) > RECEIPT_ATOL+RECEIPT_RTOL*abs(expected):
            raise ArithmeticError("receipt numerical difference at "+where)
    elif type(actual) is not type(expected) or actual != expected:
        raise ArithmeticError("receipt exact value changed at "+where)


def run():
    env, history = load_inputs()
    r, nu, dtheta = 1/9, 3/5, 81/40
    theta = 2*np.arctanh(r)
    k, theta_jet = env["native"](theta, nu)
    primal, kr, _ = env["native_joint_jet"](env, theta, nu, dtheta, 0.0)
    require(k.shape == (128, 16, 16), "actual all128 original CAR16 matrices retained")
    require(np.linalg.norm(primal-k) < 1e-14 and np.linalg.norm(kr-dtheta*theta_jet) < 1e-13,
            "owned joint jet agrees with unchanged constructor and dtheta/dr=81/40")
    delta, ddelta, rho, drho, z = env["prepared"](k, kr)
    inverse = np.linalg.inv(delta)
    harmonic = 16/z
    dharmonic = 16*tr(inverse@ddelta@inverse)/z**2
    dnu_v = -nu*dharmonic/(2*harmonic)
    _, kv, _ = env["native_joint_jet"](env, theta, nu, dtheta, dnu_v)
    _, _, _, drho_v, _ = env["prepared"](k, kv)
    require(norm1(drho_v-drho) < MATRIX_TOL,
            "native nu scaling preserves normalized inverse preparation source on v")
    require(abs(dnu_v-history["dnu_v"]) < 2e-14, "same owned one-port-invisible native tangent")
    require(sum(not np.count_nonzero(kb) for kb in k) == 64 and
            all(not np.count_nonzero(k[i]) and not np.count_nonzero(kr[i]) and not np.count_nonzero(kv[i])
                for i in range(128) if (i//4)&1),
            "all128 slots retained; exactly64 structural odd-Walsh zeros")
    complete = sum((adj(kb)@kb for kb in k), np.zeros_like(EYE))
    require(norm1(complete-EYE) < MATRIX_TOL, "unchanged full128 channel is trace preserving")
    results, all_maps, all_jets = {}, {}, {}
    for name, jet, rhojet in (("r", kr, drho), ("v_one_port_invisible", kv, drho_v)):
        maps, jets = coarse_maps(k, jet)
        all_maps[name], all_jets[name] = maps, jets
        facs = factors(maps)
        phi, dphi = sum(maps), sum(jets)
        require(norm1(phi@vec(rho)-vec(rho)) < MATRIX_TOL and
                norm1(dphi@vec(rho)+phi@vec(rhojet)-vec(rhojet)) < MATRIX_TOL,
                name+": moving original inverse-square stationary family")
        derivative_complete = sum((adj(db)@kb+adj(kb)@db for kb, db in zip(k, jet)), np.zeros_like(EYE))
        require(norm1(derivative_complete) < MATRIX_TOL, name+": full128 derivative is trace preserving")
        dense = herm(np.arange(256).reshape(16, 16)+1j*np.arange(255, -1, -1).reshape(16, 16))/256
        action_errors = []
        for a in (0, 1):
            test, dtest = port_apply(k, jet, a, dense, rhojet)
            action_errors.extend((norm1(vec(test)-maps[a]@vec(dense)),
                                  norm1(vec(dtest)-jets[a]@vec(dense)-maps[a]@vec(rhojet))))
        require(max(action_errors) < MATRIX_TOL, name+": actual256 CP maps and jets equal native Kraus action")
        witness = compressed(maps, jets, facs, rho, rhojet, True, name)
        if name == "v_one_port_invisible":
            require(max(abs(x) for x in witness["one_port_dq"]) < 2e-13,
                    "v fixes original one-port readout without freezing DATA")
            require(abs(witness["source_nats"]) > 1e-5,
                    "v retains a nonzero compressed quantum source beyond the one-port screen")
        results[name] = {
            "uncapped_terminal": uncapped_checks(k, jet, maps, jets, facs, rho, rhojet, name),
            "finite_caps": [capped_checks(k, jet, maps, jets, rho, rhojet, cap, name) for cap in (1, 8, 64)],
            "compressed_CQ_witness": witness,
        }
    effects = [sum((adj(kb)@kb for kb in k[a::2]), np.zeros_like(EYE)) for a in (0, 1)]
    spectra = [np.linalg.eigvalsh(herm(effect)) for effect in effects]
    require(all(s.min() > 0 and s.max() < 1 for s in spectra),
            "both success effects strictly positive: actual CP resolvents converge in trace norm")
    frozen = frozen_control(k, kr, all_maps["r"], all_jets["r"], factors(all_maps["r"]), rho)
    finite_difference = {}
    def value(rr, nn):
        ks, _ = env["native"](2*np.arctanh(rr), nn)
        _, _, state, _, _ = env["prepared"](ks, np.zeros_like(ks))
        mm, jj = coarse_maps(ks, np.zeros_like(ks))
        return compressed(mm, jj, factors(mm), state, np.zeros_like(state))["relative_entropy_nats"]
    for name, dnu in (("r", 0.0), ("v_one_port_invisible", dnu_v)):
        step = 1e-4
        fd = (-value(r+2*step,nu+2*step*dnu)+8*value(r+step,nu+step*dnu)
              -8*value(r-step,nu-step*dnu)+value(r-2*step,nu-2*step*dnu))/(12*step)
        source = results[name]["compressed_CQ_witness"]["source_nats"]
        require(abs(fd-source) < FD_TOL, name+": independent five-point original-value derivative")
        finite_difference[name] = {"step": step, "value_derivative": float(fd),
                                   "analytic_source": source, "absolute_error": float(abs(fd-source))}
    consumed = {}
    for name in results:
        one, two = history["directions"][name]
        current = results[name]["compressed_CQ_witness"]
        require(one["depth"] == 1 and one["physical_word_slots"] == 128 and
                two["depth"] == 2 and two["physical_word_slots"] == 16384,
                name+": hash-consume owned one/two-round evidence without replay")
        chi = current["initial_entropy_nats"]-one["conditional_DATA_entropy"]
        dchi = current["initial_entropy_source"]-one["conditional_DATA_source"]
        first_deficit = two["dephasing_production"]-2*one["dephasing_production"]
        dfirst_deficit = two["dephasing_production_source"]-2*one["dephasing_production_source"]
        fine_pair_mi = 2*one["pointer_entropy"]-two["pointer_entropy"]
        dfine_pair_mi = 2*one["pointer_source"]-two["pointer_source"]
        value_error = (two["regularization"]["entropy_gain_value_error_bound"]+
                       2*one["regularization"]["entropy_gain_value_error_bound"])
        source_error = (two["regularization"]["entropy_gain_source_error_bound"]+
                        2*one["regularization"]["entropy_gain_source_error_bound"])
        require(first_deficit > 100*value_error,
                name+": consumed first-step Jensen deficit is positive beyond its analytic regularization bound")
        require(chi > current["relative_entropy_nats"] > 0,
                name+": last-fine Holevo lower bound exceeds the separate coarse quantum witness")
        require(fine_pair_mi > 0 and chi+fine_pair_mi < 3*chi-first_deficit,
                name+": inherited first-two-fine MI strictly tightens the full stopped value lower bound")
        consumed[name] = {
            "one_round_fine_Holevo_nats": chi, "one_round_fine_Holevo_source": dchi,
            "full_stopped_D_numerical_lower_nats": chi+fine_pair_mi,
            "full_stopped_D_symbolic_lower": "M_full_fine_stopped + chi_one",
            "consumed_first_two_fine_MI_nats": fine_pair_mi,
            "consumed_first_two_fine_MI_source": dfine_pair_mi,
            "source_of_lower_expression_not_source_bound": dchi+dfine_pair_mi,
            "full_stopped_D_upper_nats": 3*chi,
            "first_step_Jensen_deficit_nats": first_deficit,
            "first_step_Jensen_deficit_source": dfirst_deficit,
            "sharpened_full_stopped_D_upper_nats": 3*chi-first_deficit,
            "nominal_lower_and_sharpened_upper_golden_units":
                [(chi+fine_pair_mi)/ELL, (3*chi-first_deficit)/ELL],
            "source_of_sharpened_upper_expression_not_source_bound": 3*dchi-dfirst_deficit,
            "value_sandwich_proved_in_analytic_parent": True,
            "derivative_inequality_claimed": False,
            "nominal_bounds_are_not_outward_rounded_intervals": True,
            "consumed_Jensen_value_regularization_bound": value_error,
            "consumed_Jensen_source_regularization_bound": source_error,
            "consumed_Holevo_source_regularization_bound":
                one["regularization"]["entropy_gain_source_error_bound"],
            "historical_suite_replayed": False,
        }
    return {
        "status": "NUMERICAL_NATIVE_QUANTUM_RETURN_PASS",
        "input_commit": "e92ecb3bdc53a2b958b1cc09a7b0398f978c87f3",
        "pinned_source_sha256": PINS,
        "native": {"r": r, "nu": nu, "theta": float(theta), "dtheta_dr": dtheta,
                   "dnu_v": float(dnu_v), "phases": ["i", "i", "-1", "-i"],
                   "CAR_dimension": 16, "physical_fine_labels": 128, "coarse_ports": 2,
                   "superoperator_shape": [256, 256],
                   "port_effect_spectral_intervals": [[float(s.min()), float(s.max())] for s in spectra],
                   "return_resolvent_trace_norm_bounds": [float(1/s.min()) for s in spectra]},
        "directions": results,
        "frozen_preparation_negative_control": frozen,
        "independent_value_derivatives": finite_difference,
        "consumed_one_two_round_information": consumed,
        "verification": {"matrix_trace_norm_tolerance": MATRIX_TOL,
                         "independent_entropy_identity_tolerance": ENTROPY_TOL,
                         "independent_value_derivative_tolerance": FD_TOL,
                         "receipt_absolute_tolerance": RECEIPT_ATOL, "receipt_relative_tolerance": RECEIPT_RTOL,
                         "spectral_mode_clipping": False, "coarse_entropy_regularization": False,
                         "fine_entropy_evidence": "pinned all-mode amplitude-SVD receipt; no replay",
                         "all128_labels_in_CP_maps_terminal_and_counts": True,
                         "exponential_history_enumeration": False,
                         "old_suites_replayed": False, "interval_certificate": False},
        "scope": {"complete_stopped_entropy_value_computed": False,
                  "complete_stopped_entropy_source_computed": False,
                  "compressed_value_is_analytic_lower_bound": True,
                  "compressed_source_is_not_a_bound_on_complete_source": True,
                  "fixed_stationary_DATA_boundary_does_not_pay_for_preparation": True,
                  "physical_Book03_Info_selected": False, "all42_native_field_transport_proved": False,
                  "independent_upstream_Euler_closed": False, "GR_closed": False},
        "checks_passed": len(CHECKS), "checks": CHECKS,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true", help="explicitly author the new receipt")
    parser.add_argument("--print-only", action="store_true", help="diagnose without writing or comparing")
    args = parser.parse_args()
    if args.write_result and args.print_only:
        parser.error("choose one author/diagnostic mode")
    result = run()
    encoded = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)+"\n"
    target = Path(__file__).with_name("NATIVE_QUANTUM_RETURN_RESULT.json")
    if args.write_result:
        target.write_text(encoded)
    elif not args.print_only:
        compare_receipt(result, json.loads(target.read_text()))
    print(encoded, end="")


if __name__ == "__main__":
    main()
