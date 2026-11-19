#!/usr/bin/env python3
"""Actual no-reset CAR16 source normalization; new numerical diagnostics only.

The dimension-only inequalities and finite-tree tangent telescopes are analytic.
The native constants printed here are ordinary floating-point diagnostics, not
outward interval certificates. Original pinned files are only AST-read.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm, solve_sylvester

P = (np.sqrt(5.0)-1)/2
EYE = np.eye(16, dtype=complex)
PINS = {
    "check_uniform_book_source.py": "ee8de4635d24c668949ac9a0186616ab7d59f2ed",
    "check_complete_history_source.py": "c133c6aec28e2a4068b36a6d9646bc8fb04fc2a4",
}
CHECKS = []


def require(ok, description):
    if not bool(ok):
        raise ArithmeticError(description)
    CHECKS.append(description)


def adj(x):
    return x.conj().T


def herm(x):
    return (x+adj(x))/2


def trace(x):
    return float(np.trace(x).real)


def source_inputs(input_dir):
    if input_dir is not None:
        return {name: input_dir/name for name in PINS}
    for start in (Path.cwd(), Path(__file__).resolve().parent):
        for parent in (start, *start.parents):
            base = parent/"02_REGISTRY/research/sources"
            paths = {
                "check_uniform_book_source.py": base/"d0_book_uniform_source_2026-10-21/check_uniform_book_source.py",
                "check_complete_history_source.py": base/"d0_native_complete_cq_source_2026-10-22/check_complete_history_source.py",
            }
            if all(path.is_file() for path in paths.values()):
                return paths
    raise FileNotFoundError("use --input-dir with both pinned original files")


def load_inputs(paths):
    env = dict(np=np, expm=expm, solve_sylvester=solve_sylvester,
               P=P, EYE=EYE, ENTROPY_ETA=1e-22)
    requested = [
        {"adj", "herm", "tr", "root", "creators", "native"},
        {"native_joint_jet", "prepared", "entropy_amplitude", "entropy_source"},
    ]
    for (name, pin), names in zip(PINS.items(), requested):
        raw = paths[name].read_bytes()
        blob = hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
        require(blob == pin, "pinned original "+name)
        seen = set()
        for node in ast.parse(raw.decode()).body:
            if isinstance(node, ast.FunctionDef) and node.name in names:
                exec(compile(ast.Module(body=[node], type_ignores=[]), str(paths[name]), "exec"), env)
                seen.add(node.name)
        require(seen == names, "restricted AST definitions "+name)
    return env


def merged(k, dk):
    out, dot = [k[0], k[1]], [dk[0], dk[1]]
    for j in range(1, 64):
        m, dm = k[2*j]/P, dk[2*j]/P
        require(np.linalg.norm(k[2*j+1]-np.sqrt(P)*m) < 2e-15,
                "unchanged scalar merged pair "+str(j))
        require(np.linalg.norm(dk[2*j+1]-np.sqrt(P)*dm) < 2e-14,
                "unchanged scalar pair jet "+str(j))
        out.append(m)
        dot.append(dm)
    live = [i for i, x in enumerate(out) if np.count_nonzero(x)]
    require(len(out) == 65 and len(live) == 33, "65 physical and 33 live merged slots")
    return np.asarray(out)[live], np.asarray(dot)[live]


def block_history(env, k, dk, c, dc, depth):
    nodes = [(c, dc)]
    for _ in range(depth):
        nodes = [(kb@a, dkb@a+kb@da) for a, da in nodes for kb, dkb in zip(k, dk)]
    entropy = source = pointer = dpointer = norm = mass = dmass = 0.0
    for a, da in nodes:
        p = float(np.vdot(a, a).real)
        dp = 2*float(np.vdot(a, da).real)
        sv, ds = env["entropy_amplitude"](a, da)
        entropy += sv
        source += ds
        pointer -= p*np.log(p)
        dpointer -= dp*(np.log(p)+1)
        norm += float(np.vdot(da, da).real)
        mass += p
        dmass += dp
    require(abs(mass-1) < 2e-12 and abs(dmass) < 2e-12,
            "whole merged history normalization depth "+str(depth))
    return dict(depth=depth, live_words=len(nodes), entropy=entropy, source=source,
                pointer=pointer, pointer_source=dpointer,
                conditional_entropy=entropy-pointer,
                conditional_source=source-dpointer, tangent_norm2=norm)


def advance(k, dk, state):
    # Sums over all fine histories sharing one coarse port prefix.
    x, y, z = state  # sum AA*, sum dA A*, sum dA dA*
    xx = yy = zz = np.zeros_like(x)
    for a, da in zip(k, dk):
        xx = xx+a@x@adj(a)
        yy = yy+da@x@adj(a)+a@y@adj(a)
        zz = zz+da@x@adj(da)+da@adj(y)@adj(a)+a@y@adj(da)+a@z@adj(a)
    return xx, yy, zz


def stopped_norm(k, dk, rho, c, dc, cap):
    initial = (rho, dc@adj(c), dc@adj(dc))
    occupation = rho.copy()
    terminal_norm = 0.0
    for anchor in (0, 1):
        live = advance(k[anchor::2], dk[anchor::2], initial)
        for step in range(cap):
            occupation += live[0]
            match = advance(k[anchor::2], dk[anchor::2], live)
            terminal_norm += trace(match[2])
            live = advance(k[1-anchor::2], dk[1-anchor::2], live)
            if step+1 == cap:
                terminal_norm += trace(live[2])
    return terminal_norm, herm(occupation)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    env = load_inputs(source_inputs(args.input_dir))
    r, nu = 1/9, 3/5
    theta, dtheta = 2*np.arctanh(r), 2/(1-r*r)
    k, dr, _ = env["native_joint_jet"](env, theta, nu, dtheta, 0.)
    delta, dd, rho, drho, z = env["prepared"](k, dr)
    h = 16/z
    hr = 16*trace(np.linalg.solve(delta, dd)@np.linalg.inv(delta))/z**2
    dnuv = -nu*hr/(2*h)
    _, dv, _ = env["native_joint_jet"](env, theta, nu, dtheta, dnuv)
    _, _, _, drhov, _ = env["prepared"](k, dv)
    require(np.linalg.norm(sum((adj(x)@x for x in k), np.zeros_like(EYE))-EYE) < 2e-13,
            "original full128 completeness")
    require(np.linalg.norm(sum((x@rho@adj(x) for x in k), np.zeros_like(EYE))-rho) < 2e-13,
            "same original stationary preparation")
    phistar = sum((np.kron(x.T, adj(x)) for x in k), np.zeros((256, 256), complex))
    projection = np.outer(EYE.flatten(order="F"), rho.T.flatten(order="F"))
    poisson = np.eye(256)-phistar+projection
    c = env["root"](rho)
    result = {"native_inputs": PINS, "dimension": 16, "r": r, "nu": nu,
              "dnu_v": dnuv, "moment_constant": float(np.log(16)),
              "poisson_condition_number": float(np.linalg.cond(poisson)),
              "interval_certificate": False, "GR_closed": False, "directions": {}}
    for name, dk, dstate in (("r", dr, drho), ("v_one_port_null", dv, drhov)):
        beta = sum((adj(x)@dx for x, dx in zip(k, dk)), np.zeros_like(EYE))
        b = herm(-1j*beta)
        phase = trace(rho@b)
        x = herm(np.linalg.solve(poisson, (b-phase*EYE).flatten(order="F")).reshape((16, 16), order="F"))
        dkh = np.asarray([dx+1j*(x@a-a@x)-1j*phase*a for a, dx in zip(k, dk)])
        horizontal = sum((adj(a)@da for a, da in zip(k, dkh)), np.zeros_like(EYE))
        require(np.linalg.norm(horizontal) < 2e-13, name+" actual horizontal operator condition")
        require(abs(trace(rho@x)) < 2e-12, name+" centered native Poisson generator")
        dstateh = dstate+1j*(x@rho-rho@x)
        sld = herm(solve_sylvester(rho, rho, 2*dstateh))
        dch = .5*sld@c
        require(np.linalg.norm(dch@adj(c)+c@adj(dch)-dstateh) < 2e-13,
                name+" Bures input amplitude realizes conjugated preparation jet")
        dc = solve_sylvester(c, c, dstate)
        eh = herm(sum((adj(da)@da for da in dkh), np.zeros_like(EYE)))
        kappa, u = trace(rho@eh), float(np.vdot(dch, dch).real)
        si, dsi = env["entropy_source"](rho, dstate)
        mk, md = merged(k, dk)
        _, mdh = merged(k, dkh)
        require(np.linalg.norm(sum((adj(a)@da for a, da in zip(mk, mdh)), np.zeros_like(EYE))) < 2e-13,
                name+" same horizontal gauge on merged instrument")
        require(np.linalg.norm(sum((adj(da)@da for da in mdh), np.zeros_like(EYE))-eh) < 2e-13,
                name+" scalar pair reduction preserves tangent energy")
        histories = []
        for depth in (1, 2):
            raw = block_history(env, mk, md, c, dc, depth)
            gauged = block_history(env, mk, mdh, c, dch, depth)
            require(abs(gauged["tangent_norm2"]-(u+depth*kappa)) < 2e-12,
                    name+" exact linear whole-word tangent telescope depth "+str(depth))
            require(abs(raw["source"]-gauged["source"]) < 2e-11 and
                    abs(raw["pointer_source"]-gauged["pointer_source"]) < 2e-11,
                    name+" mathematical gauge preserves all retained entropy sources depth "+str(depth))
            conditional_bound = 2*np.log(16)*np.sqrt(u+depth*kappa)
            require(abs(gauged["conditional_source"]) <= conditional_bound,
                    name+" actual conditional source obeys dimension-only bound depth "+str(depth))
            raw["horizontal_norm2"] = gauged["tangent_norm2"]
            raw["conditional_source_bound"] = float(conditional_bound)
            histories.append(raw)
        caps = []
        for cap in (1, 2, 8, 64):
            norm2, occupation = stopped_norm(k, dkh, rho, c, dch, cap)
            predicted = u+trace(occupation@eh)
            min_remainder = float(np.linalg.eigvalsh(herm(3*rho-occupation)).min())
            require(abs(norm2-predicted) < 2e-12, name+" stopped finite-tree tangent telescope cap "+str(cap))
            require(min_remainder > -2e-13 and norm2 <= u+3*kappa+2e-12,
                    name+" first-return occupation gives cap-uniform source norm cap "+str(cap))
            caps.append(dict(cap=cap, tangent_norm2=norm2, occupation_predicted=predicted,
                             occupation_psd_remainder_min=min_remainder))
        per_tick = {}
        for length in (4096, 1000000, 100000000):
            per_tick[str(length)] = float((abs(dsi)+2*np.log(16)*np.sqrt(u+length*kappa))/length)
        result["directions"][name] = dict(beta_norm=float(np.linalg.norm(beta)),
             phase=phase, poisson_generator_frobenius=float(np.linalg.norm(x)),
             horizontal_residual=float(np.linalg.norm(horizontal)),
             kappa=kappa, input_amplitude_norm2=u, tangent_energy_operator_norm=float(np.linalg.eigvalsh(eh).max()),
             input_entropy=si, input_entropy_source=dsi,
             fixed_window_quantum_boundary_source_per_tick_bound=per_tick,
             stopped_quantum_boundary_source_bound=float(abs(dsi)+2*np.log(16)*np.sqrt(u+3*kappa)),
             histories=histories, stopped_caps=caps)
    result["checks_passed"] = len(CHECKS)
    result["checks"] = CHECKS
    encoded = json.dumps(result, indent=2)+"\n"
    if args.json:
        args.json.write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
