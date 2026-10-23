#!/usr/bin/env python3
"""Complete conditional-work information on the original native instrument.

This is a bounded source diagnostic, not a selected Book03 information law.
The native constructor is imported by a pinned AST slice; no old suite runs.
Exact rational mass/source controls accompany numerical spectral entropies.
All checks execute under python -O. Receipt generation is explicit.
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
NATIVE_PATH = ROOT / "02_REGISTRY/research/sources/d0_book_uniform_source_2026-10-21/check_uniform_book_source.py"
NATIVE_BLOB = "ee8de4635d24c668949ac9a0186616ab7d59f2ed"
P = (np.sqrt(5.0) - 1.0) / 2.0
EYE = np.eye(16, dtype=complex)
CHECKS = []
ENTROPY_ETA = 1e-22


def require(condition, description):
    if not bool(condition):
        raise ArithmeticError(description)
    CHECKS.append(description)


def native_namespace():
    raw = NATIVE_PATH.read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    require(blob == NATIVE_BLOB, "immutable original native constructor blob")
    env = {"np": np, "expm": expm, "solve_sylvester": solve_sylvester,
           "P": P, "EYE": EYE}
    names = {"adj", "herm", "tr", "root", "creators", "native"}
    seen = set()
    for node in ast.parse(raw.decode()).body:
        if isinstance(node, ast.FunctionDef) and node.name in names:
            exec(compile(ast.Module(body=[node], type_ignores=[]), str(NATIVE_PATH), "exec"), env)
            seen.add(node.name)
    require(seen == names, "only the six required native definitions are loaded")
    return env


def adj(a):
    return a.conj().T


def herm(a):
    return (a + adj(a)) / 2


def entropy_amplitude(a, da, eta=ENTROPY_ETA):
    """All-mode S_eta(AA*) and its analytic amplitude source.

    SVD produces nonnegative lambda=squared singular values without clipping
    eigenvalues or omitting any positive quantum mode. All singular values,
    including zeros, enter the same regularized source formula.
    """
    u, singular, vh = np.linalg.svd(a, full_matrices=False)
    lam = singular*singular
    dlam = 2*singular*np.diag(adj(u) @ da @ adj(vh)).real
    logs = np.log(lam+eta)
    return (float(-np.sum(lam*logs)),
            float(-np.sum(dlam*(logs+lam/(lam+eta)))))


def entropy_source(a, da, eta=ENTROPY_ETA):
    """Convenience for the strictly positive rational/initial/blank blocks."""
    eigenvalues, basis = np.linalg.eigh(herm(a))
    if eigenvalues.min() <= 0:
        raise ArithmeticError("matrix convenience requires strictly positive input; use actual amplitude")
    c = (basis*np.sqrt(eigenvalues)) @ adj(basis)
    dc = solve_sylvester(c, c, da)
    return entropy_amplitude(c, dc, eta)


def branch(k, dk, rho, drho):
    value = k @ rho @ adj(k)
    source = dk @ rho @ adj(k) + k @ drho @ adj(k) + k @ rho @ adj(dk)
    return value, source


def native_joint_jet(env, theta, nu, dtheta, dnu):
    """Differentiate the unchanged original words in both actual parameters.

    The original native() differentiates theta only. This extension retains
    exactly its words while also differentiating nu and both Julia defects.
    Its primal and theta jet are checked against that unchanged constructor.
    """
    cs = env["creators"]()
    generator = cs[0] @ adj(cs[1]) + cs[1] @ adj(cs[0])
    u = expm(theta * generator)
    du = dtheta * u @ generator
    zero = np.zeros_like(EYE)
    phases = (1j, 1j, -1.0, -1j)
    words, jets = [], []
    for direction, c in enumerate(cs):
        base, dbase = nu * c, dnu * c
        v = u if direction == 1 else EYE
        dv = du if direction == 1 else zero
        x = base @ v * phases[direction]
        dx = (dbase @ v + base @ dv) * phases[direction]
        left = env["root"](EYE - x @ adj(x))
        right = env["root"](EYE - adj(x) @ x)
        dl = solve_sylvester(left, left, -dx @ adj(x) - x @ adj(dx))
        dr = solve_sylvester(right, right, -adj(dx) @ x - adj(x) @ dx)
        l0 = env["root"](EYE - base @ adj(base))
        r0 = env["root"](EYE - adj(base) @ base)
        dl0 = solve_sylvester(l0, l0, -dbase @ adj(base) - base @ adj(dbase))
        dr0 = solve_sylvester(r0, r0, -adj(dbase) @ base - adj(base) @ dbase)
        for word, jet in zip(((x, left), (adj(x), right), (-base, -l0), (-adj(base), -r0)),
                             ((dx, dl), (adj(dx), dr), (-dbase, -dl0), (-adj(dbase), -dr0))):
            words.extend((word, word))
            jets.extend((jet, jet))
    rows, drows = [], []
    for label in range(32):
        signs = [(-1) ** (bin(label & j).count("1") & 1) for j in range(32)]
        for b in range(2):
            rows.append(sum((signs[j] * words[j][b] for j in range(32)), zero.copy()) / 32)
            drows.append(sum((signs[j] * jets[j][b] for j in range(32)), zero.copy()) / 32)
    a, da = rows[0], drows[0]
    out, dout = [], []
    for j, row in enumerate(rows):
        v = adj(row) @ a
        dv = adj(drows[j]) @ a + adj(row) @ da
        out.extend(((EYE if j == 0 else zero) - 2 * P**2 * v, -2 * P * np.sqrt(P) * v))
        dout.extend((-2 * P**2 * dv, -2 * P * np.sqrt(P) * dv))
    return np.asarray(out), np.asarray(dout), rows


def prepared(k, dk):
    delta = herm((EYE - k[0]) / (2 * P**2))
    ddelta = herm(-dk[0] / (2 * P**2))
    inverse = np.linalg.inv(delta)
    z = float(np.trace(inverse).real)
    dinverse = -inverse @ ddelta @ inverse
    rho = inverse / z
    drho = dinverse / z - rho * float(np.trace(dinverse).real) / z
    return delta, ddelta, rho, drho, z


def cq_depth(k, dk, rho, drho, depth):
    active = [(a, da) for a, da in zip(k, dk)
              if np.count_nonzero(a) or np.count_nonzero(da)]
    require(len(active) == 64, f"only 64 structurally zero native labels pruned, depth {depth}")
    ev, u = np.linalg.eigh(herm(rho))
    c = (u*np.sqrt(ev)) @ adj(u)
    dc = solve_sylvester(c, c, drho)
    nodes = [(c, dc)]
    for _ in range(depth):
        next_nodes = []
        for amplitude, amplitude_source in nodes:
            for kb, dkb in active:
                next_nodes.append((kb @ amplitude, dkb @ amplitude + kb @ amplitude_source))
        nodes = next_nodes
    pointer = dpointer = cq = dcq = mass = dmass = cq_fine = dcq_fine = 0.0
    end = np.zeros_like(rho)
    dend = np.zeros_like(rho)
    amplitude_source_norm2 = 0.0
    for amplitude, amplitude_source in nodes:
        state = amplitude @ adj(amplitude)
        source = amplitude_source @ adj(amplitude) + amplitude @ adj(amplitude_source)
        q = float(np.vdot(amplitude, amplitude).real)
        dq = float(2*np.vdot(amplitude, amplitude_source).real)
        if q <= 0:
            raise ArithmeticError("unexpected zero on native active strict chart")
        pointer -= q * np.log(q)
        dpointer -= dq * (np.log(q) + 1)
        s, ds = entropy_amplitude(amplitude, amplitude_source)
        fine_s, fine_ds = entropy_amplitude(amplitude, amplitude_source, eta=1e-24)
        cq += s
        dcq += ds
        cq_fine += fine_s
        dcq_fine += fine_ds
        mass += q
        dmass += dq
        end += state
        dend += source
        amplitude_source_norm2 += float(np.vdot(amplitude_source, amplitude_source).real)
    require(abs(mass - 1) < 2e-12 and abs(dmass) < 2e-12, f"complete mass and source, depth {depth}")
    require(np.linalg.norm(end - rho) < 2e-12 and np.linalg.norm(dend - drho) < 2e-12,
            f"moving original stationary marginal, depth {depth}")
    si, dsi = entropy_source(rho, drho)
    jet_norm = float(np.sqrt(np.linalg.eigvalsh(herm(sum(
        (adj(da)@da for da in dk), np.zeros_like(rho)))).max()))
    amplitude_jet_bound = depth*jet_norm+float(np.linalg.norm(dc))
    total_dim = 16*128**depth
    source_bound = 4*np.sqrt(total_dim*ENTROPY_ETA)*amplitude_jet_bound
    initial_source_bound = 4*np.sqrt(16*ENTROPY_ETA)*float(np.linalg.norm(dc))
    require(np.sqrt(amplitude_source_norm2) <= amplitude_jet_bound+1e-12,
            f"whole-word amplitude source obeys analytical bound, depth {depth}")
    require(abs(dcq-dcq_fine) < max(1e-11, 2*source_bound),
            f"all-mode source stable under smaller regularization, depth {depth}")
    require(source_bound < 1e-7, f"analytic regularization bound below actual source scale, depth {depth}")
    return {"depth": depth, "physical_word_slots": 128**depth,
            "positive_word_slots": len(nodes),
            "pointer_entropy": pointer, "pointer_source": dpointer,
            "complete_CQ_entropy": cq, "complete_CQ_source": dcq,
            "conditional_DATA_entropy": cq - pointer,
            "conditional_DATA_source": dcq - dpointer,
            "dephasing_production": cq - si,
            "dephasing_production_source": dcq - dsi,
            "regularization": {"eta": ENTROPY_ETA, "eta_check": 1e-24,
                               "eta_check_value": cq_fine, "eta_check_source": dcq_fine,
                               "value_error_bound": total_dim*ENTROPY_ETA,
                               "source_error_bound": source_bound,
                               "initial_entropy_value_error_bound": 16*ENTROPY_ETA,
                               "initial_entropy_source_error_bound": initial_source_bound,
                               "entropy_gain_source_error_bound": source_bound+initial_source_bound,
                               "entropy_gain_value_error_bound": (total_dim+16)*ENTROPY_ETA,
                               "measured_whole_amplitude_jet_norm": float(np.sqrt(amplitude_source_norm2)),
                               "amplitude_jet_norm_upper_bound": amplitude_jet_bound}}


def rational_tree():
    """Finite noncommuting retained-preparation tree with exact rational jets."""
    def mat(a):
        return np.asarray([[F(x) for x in row] for row in a], dtype=object)

    t = F(1, 3)
    den = 1 + t*t
    rotation = mat([[(1-t*t)/den, -2*t/den], [2*t/den, (1-t*t)/den]])
    drotation = mat([[-4*t/den**2, -2*(1-t*t)/den**2],
                    [2*(1-t*t)/den**2, -4*t/den**2]])
    factors = [mat([[F(3, 5), 0], [0, F(4, 5)]]),
               mat([[F(4, 5), 0], [0, F(3, 5)]])]
    k = [factor @ rotation for factor in factors]
    dk = [factor @ drotation for factor in factors]
    zero = mat([[0, 0], [0, 0]])
    rho = mat([[F(2, 3), F(1, 12)], [F(1, 12), F(1, 3)]])
    require(np.array_equal(sum((a.T @ a for a in k), zero.copy()), mat([[1, 0], [0, 1]])),
            "exact rational instrument completeness")
    require(not np.array_equal(k[0] @ k[1], k[1] @ k[0]), "actual noncommuting rational history")
    nodes = {(): (rho, zero.copy())}
    live, leaves = [], []
    # Two paid/retained preparation rounds, then anchor and at most two later trials.
    def walk(word):
        if len(word) >= 4 and (word[-1] == word[2] or len(word) == 5):
            leaves.append(word)
            return
        live.append(word)
        state, source = nodes[word]
        for b, (a, da) in enumerate(zip(k, dk)):
            nodes[word+(b,)] = (a @ state @ a.T,
                               da @ state @ a.T + a @ source @ a.T + a @ state @ da.T)
            walk(word+(b,))
    walk(())
    require(sum((np.trace(nodes[w][0]) for w in leaves), F(0)) == 1,
            "exact capped mass includes preparation, matches and aborts")
    require(sum((np.trace(nodes[w][1]) for w in leaves), F(0)) == 0,
            "exact complete capped first source normalization")
    def es(word):
        a, da = nodes[word]
        return entropy_source(np.asarray(a, dtype=complex), np.asarray(da, dtype=complex))
    initial = es(())
    leaf = np.sum(np.asarray([es(w) for w in leaves]), axis=0)
    jumps = []
    for w in live:
        jumps.append(np.sum(np.asarray([es(w+(b,)) for b in range(2)]), axis=0) - es(w))
    accumulated = np.sum(np.asarray(jumps), axis=0)
    require(np.linalg.norm(leaf - initial - accumulated) < 5e-13,
            "full quantum finite-tree entropy and first-source telescope")
    require(min(jump[0] for jump in jumps) > 0,
            "each actual full-register pinching produces nonnegative entropy")
    pointer = dpointer = 0.0
    for w in leaves:
        a, da = nodes[w]
        q, dq = float(np.trace(a)), float(np.trace(da))
        pointer -= q*np.log(q)
        dpointer -= dq*(np.log(q)+1)
    require(abs(leaf[1] - dpointer) > 1e-5,
            "deleting retained conditional quantum work changes the complete source")
    require(any(len(w) == 5 and w[-1] != w[2] for w in leaves), "genuine capped abort words retained")
    return {"paid_retained_preparation_rounds": 2, "later_trial_cap": 2,
            "leaf_count": len(leaves), "live_node_count": len(live),
            "initial_entropy": float(initial[0]), "initial_source": float(initial[1]),
            "leaf_CQ_entropy": float(leaf[0]), "leaf_CQ_source": float(leaf[1]),
            "pointer_entropy": pointer, "pointer_source": dpointer,
            "sum_local_dephasing": accumulated.tolist(),
            "exact_rational_mass_and_source": True}


def native_checks(env):
    r, nu = 1/9, 3/5
    theta = 2*np.arctanh(r)
    dtheta_dr = 2/(1-r*r)
    k, dtheta_native = env["native"](theta, nu)
    primal, dr, rows = native_joint_jet(env, theta, nu, dtheta_dr, 0.0)
    require(np.linalg.norm(primal-k) < 1e-14, "joint jet keeps unchanged original 128 matrices")
    require(np.linalg.norm(dr-dtheta_dr*dtheta_native) < 1e-13, "analytic r jet retains dtheta/dr")
    require(all(not np.count_nonzero(k[i]) and not np.count_nonzero(dr[i])
                for i in range(128) if (i//4)&1),
            "odd Walsh rows vanish by identical adjacent-word cancellation")
    delta, ddelta, rho, drho, z = prepared(k, dr)
    s0, ds0 = entropy_source(rho, drho)
    h = 16/z
    h_r = 16*float(np.trace(np.linalg.inv(delta) @ ddelta @ np.linalg.inv(delta)).real)/z**2
    dnu_v = -nu*h_r/(2*h)
    _, dv, _ = native_joint_jet(env, theta, nu, dtheta_dr, dnu_v)
    _, ddelta_v, _, drho_v, _ = prepared(k, dv)
    h_v = 16*float(np.trace(np.linalg.inv(delta) @ ddelta_v @ np.linalg.inv(delta)).real)/z**2
    require(abs(h_v) < 1e-14, "actual one-port-invisible tangent has zero h source")
    require(abs(float(np.trace(drho).real)) < 1e-14 and abs(float(np.trace(drho_v).real)) < 1e-14,
            "both moving inverse-square preparation jets are normalized")
    # Exact theorem's stationary-block formula is tested on every native label.
    port1_errors, port0_errors = [], []
    for j, row in enumerate(rows):
        g = adj(row) @ row / z
        port1_errors.append(np.linalg.norm(k[2*j+1] @ rho @ adj(k[2*j+1]) - 4*P**3*g))
        if j:
            port0_errors.append(np.linalg.norm(k[2*j] @ rho @ adj(k[2*j]) - 4*P**4*g))
    require(max(port1_errors) < 1e-15 and max(port0_errors) < 1e-15,
            "every stationary nonblank quantum block equals its original row formula")
    require(np.linalg.norm(k[0] @ rho @ adj(k[0]) - k[0] @ k[0] @ np.linalg.inv(delta)/z) < 1e-14,
            "ordinary blank keeps actual B squared inverse-Delta block")
    outcomes = {}
    for name, jet, rhojet in (("r", dr, drho), ("v_one_port_invisible", dv, drho_v)):
        outcomes[name] = [cq_depth(k, jet, rho, rhojet, n) for n in (1, 2)]
        require(all(abs(x["conditional_DATA_source"]) > .01 for x in outcomes[name]),
                "conditional DATA source is material on " + name)
    require(outcomes["v_one_port_invisible"][0]["pointer_source"] > .005,
            "full 128-pointer response survives exact one-port screen")
    require(outcomes["v_one_port_invisible"][0]["complete_CQ_source"] < -.01,
            "retained conditional DATA reverses that full-pointer source sign")
    # A real purified input has rank-one conditional DATA/reference blocks.
    c = env["root"](rho)
    dc = solve_sylvester(c, c, drho)
    pure = cpure = 0.0
    pure_source = cpure_source = 0.0
    for kb, dkb in zip(k, dr):
        amplitude = (kb @ c).reshape(-1)
        damplitude = (dkb @ c + kb @ dc).reshape(-1)
        q = float(np.vdot(amplitude, amplitude).real)
        dq = float(2*np.vdot(amplitude, damplitude).real)
        if q > 0:
            pure -= q*np.log(q)
            pure_source -= dq*(np.log(q)+1)
            cpure += q
            cpure_source += dq
    require(abs(cpure-1) < 1e-13 and abs(cpure_source) < 1e-13,
            "actual retained-purification branch norm and source")
    one = outcomes["r"][0]
    require(abs(pure-one["pointer_entropy"]) < 1e-13 and abs(pure_source-one["pointer_source"]) < 1e-13,
            "purified DATA/reference CQ entropy equals full pointer entropy")
    # Independent oldRIGHT128 is a tensor factor, not 128 copies of entropy.
    a, da = branch(k[0], dr[0], rho, drho)
    sv, sd = entropy_source(a, da)
    scaled_v, scaled_d = entropy_source(a/128, da/128)
    q, dq = float(np.trace(a).real), float(np.trace(da).real)
    require(abs(128*scaled_v-sv-q*np.log(128)) < 1e-12 and
            abs(128*scaled_d-sd-dq*np.log(128)) < 1e-12,
            "independent spectator contributes additive log128 and its exact block source")
    # Value-based derivative checks are independent of the spectral-source formula.
    def one_value(rr, nn):
        ks, _ = env["native"](2*np.arctanh(rr), nn)
        _, _, state, _, _ = prepared(ks, np.zeros_like(ks))
        c = env["root"](state)
        return sum(entropy_amplitude(ka @ c, np.zeros_like(c))[0] for ka in ks)
    finite_difference = {}
    for name, dnu in (("r", 0.0), ("v_one_port_invisible", dnu_v)):
        e = 1e-4
        fd = (-one_value(r+2*e,nu+2*e*dnu)+8*one_value(r+e,nu+e*dnu)
              -8*one_value(r-e,nu-e*dnu)+one_value(r-2*e,nu-2*e*dnu))/(12*e)
        expected = outcomes[name][0]["complete_CQ_source"]
        require(abs(fd-expected) < 2e-9, "independent original value derivative on " + name)
        finite_difference[name] = fd
    return {"r": r, "theta": theta, "nu": nu, "dtheta_dr": dtheta_dr,
            "h": h, "h_r": h_r, "dnu_v": dnu_v, "h_v": h_v,
            "initial_mixed_DATA_entropy": s0, "initial_mixed_DATA_r_source": ds0,
            "directions": outcomes, "independent_value_sources": finite_difference,
            "purified_one_round_CQ_entropy": pure,
            "purified_one_round_CQ_r_source": pure_source,
            "independent_oldRIGHT128_entropy_increment": float(np.log(128)),
            "full_physical_slots_retained": True,
            "dark_slots_skipped_only_in_numerical_sums": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="explicitly generate the new receipt")
    args = parser.parse_args()
    env = native_namespace()
    result = {"scope": "finite complete quantum/CQ information, not selected physical Book03 Info",
              "native_constructor_git_blob": NATIVE_BLOB,
              "rational_stopped_tree": rational_tree(),
              "original_native_full128": native_checks(env),
              "verification": {"exact_arithmetic": "rational stopped-tree probabilities and first sources",
                               "numerical_arithmetic": "NumPy/SciPy double matrix spectral entropy and analytic jets",
                               "all_positive_eigenvalues_retained": True,
                               "regularization_eta": ENTROPY_ETA,
                               "smaller_eta_check": 1e-24,
                               "positive_spectrum_method": "all singular values of actual Kraus amplitudes squared; no eigenvalue clipping",
                               "independent_value_source_tolerance": 2e-9,
                               "interval_certificate": False,
                               "old_suites_replayed": False},
              "physical_Book03_Info_identified": False, "GR_closed": False,
              "checks_passed": len(CHECKS), "checks": CHECKS}
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.write:
        Path(__file__).with_name("COMPLETE_HISTORY_RESULT.json").write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
