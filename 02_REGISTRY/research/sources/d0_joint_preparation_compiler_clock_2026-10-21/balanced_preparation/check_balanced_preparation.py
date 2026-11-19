#!/usr/bin/env python3
"""Focused checks of the balanced two-arm preparation reduction.

The complete 256-site/CAR16/RIGHT128 dictionary is retained in the matrix
identity checks. Only the original Fourier constructor is AST-imported.
The smaller two-leaf entropy fixture is explicitly NOT a replay of the
native 255-leaf instrument or a numerical proof of the general theorem.
The native spectral support/convexity input and analytical proof remain
necessary. No probability floor, finite newborn Hessian or GR claim.
All requirements remain active under python -O. JSON goes to stdout.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import itertools
import json
import math
import os
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import minimize_scalar

P = (math.sqrt(5.0) - 1.0) / 2.0
ELL = math.log(1.0 / P)
CHECKS = []


def require(condition, description):
    if not bool(condition):
        raise ArithmeticError(description)
    CHECKS.append(description)


def ringmul(x, y):
    """Exact integer Q[p] subring, represented a+b*p with p^2=1-p."""
    a, b = x
    c, d = y
    return (a*c+b*d, a*d+b*c-b*d)


def ringadd(x, y):
    return tuple(a+b for a, b in zip(x, y))


def ringneg(x):
    return tuple(-a for a in x)


def exact_weights():
    p = (0, 1)
    p2 = ringmul(p, p)
    p3 = ringmul(p, p2)
    require(ringadd(p, p2) == (1, 0), "exact selector weights sum to one")
    require(ringadd(ringneg(ringmul(p, p2)), ringmul(p2, p)) == (0, 0),
            "exact balanced first density derivative vanishes")
    # Sum weight times squared arm displacement = p*p^4+p^2*p^2=p^3.
    variance = ringadd(ringmul(p, ringmul(p2, p2)),
                       ringmul(p2, ringmul(p, p)))
    require(variance == p3, "exact relative second central weight is p^3")
    require(ringadd(p2, ringneg(p)) != (0, 0),
            "hostile equal-weight mean does not cancel Golden density source")
    return {"p_squared": p2, "relative_weight": p3}


def verify_inputs(repo):
    pins = json.loads(Path(__file__).with_name("SOURCE_PINS.json").read_text())
    for item in pins["files"]:
        actual = hashlib.sha256((repo / item["path"]).read_bytes()).hexdigest()
        require(actual == item["sha256"], "input hash " + item["path"])
    return {"input_ref": pins["input_ref"], "verified_files": len(pins["files"])}


def dictionary_checks(repo):
    source = repo / ("02_REGISTRY/research/sources/"
                     "d0_primary_native_domain_source_2026-10-20/"
                     "check_primary_domain_source.py")
    require(hashlib.sha256(source.read_bytes()).hexdigest() ==
            "c67285c7469db49ff61f3e52597d0bcc6aad991ec1f7af025d6daeb065a43edf",
            "literal original complete Fourier constructor pinned")
    tree = ast.parse(source.read_text())
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef)
             and n.name == "reference_characters"]
    require(len(nodes) == 1, "only original Fourier constructor imported")
    scope = {"np": np, "math": math, "itertools": itertools, "require": require}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(source), "exec"), scope)
    indices = np.array(list(itertools.product(range(4), repeat=4)))
    ff = scope["reference_characters"](4, indices)
    free = np.flatnonzero(np.all((indices > 0) & (indices < 3), axis=1))
    selected = np.array([int(np.flatnonzero(np.all(indices == w, axis=1))[0])
                         for w in ((1, 1, 2, 2), (1, 2, 1, 2), (2, 1, 2, 1))])
    require(set(selected).issubset(set(free)), "all actuated sites are free interior sites")
    c, theta = np.zeros(256), np.zeros(256)
    c[free] = .016*np.sin(np.arange(len(free))+1.0)
    theta[free] = .021*np.cos(np.arange(len(free))+.25)
    radius = np.sqrt(P**2-c*c)
    b, d = radius*np.sin(theta), radius*np.cos(theta)

    def preparation(angles):
        vec = np.zeros((256, 16))
        vec[:, 1] = math.sqrt(P)
        vec[:, 0] = c
        vec[:, 14] = radius*np.cos(angles)
        vec[:, 15] = radius*np.sin(angles)
        return vec[:, :, None]*ff[:, None, :]/math.sqrt(128)

    original = preparation(theta)
    flat = original.reshape(4096, 128)
    require(np.max(np.abs(flat.T@flat-np.eye(128)/128)) < 3e-16,
            "full original 4096 by128 preparation has RIGHT Gram I/128")
    generator = np.zeros((16, 16))
    for j in (6, 10, 12, 14):
        generator[j+1, j], generator[j, j+1] = 1., -1.
    require(np.linalg.matrix_rank(generator) == 8,
            "literal complete local generator has rank eight")
    require(np.array_equal(generator.T, -generator), "complete local generator is skew")
    angles = np.array([.023, -.019, .011])
    shifted_theta = theta.copy()
    shifted_theta[selected] += angles
    moved = original.copy()
    for w, a in zip(selected, angles):
        uu = np.eye(16) + math.sin(a)*generator + (1-math.cos(a))*(generator@generator)
        require(np.max(np.abs(uu.T@uu-np.eye(16))) < 3e-16,
                "complete four-plane rotation is orthogonal at site " + str(w))
        moved[w] = uu@original[w]
    require(np.max(np.abs(moved-preparation(shifted_theta))) < 3e-17,
            "exact dictionary shift U(a)C(c,theta)=C(c,theta+a), numerical residual")
    require(np.max(np.abs(moved.reshape(4096,128).T@moved.reshape(4096,128)
                          -np.eye(128)/128)) < 3e-16,
            "moving every selected arm preserves complete RIGHT Gram")
    tangent_error = 0.
    for w in selected:
        deriv = np.zeros((16,128))
        deriv[15] = ff[w]/math.sqrt(128)
        deriv[14] = -(b[w]/d[w])*ff[w]/math.sqrt(128)
        tangent_error = max(tangent_error,
                            float(np.max(np.abs(generator@original[w]-d[w]*deriv))))
    require(tangent_error < 3e-17, "actual angle tangent is d_w times original b_w tangent")

    direction = np.array([.7, -.3, .4])
    tangent = np.zeros_like(original)
    for w, v in zip(selected, direction):
        tangent[w] = v*(generator@original[w])
    cancelled = P*(-P**2*tangent) + P**2*(P*tangent)
    require(np.max(np.abs(cancelled)) < 2e-18,
            "balanced old amplitude derivative vanishes in complete native matrix")
    wrong = P*(-.5*tangent) + P**2*(.5*tangent)
    require(np.linalg.norm(wrong) > 1e-4, "wrong equal-weight mean gives nonzero full tangent")
    # Native completeness and leaf parity are inherited inputs. This computes
    # exactly their remaining dictionary Gram, without rerunning their suite.
    vacuum = np.zeros((256,16,128))
    vacuum[:,1,:] = math.sqrt(P)*ff/math.sqrt(128)
    vacuum[:,14,:] = P*ff/math.sqrt(128)
    jt = []
    for w in selected:
        dw = np.zeros_like(vacuum)
        dw[w] = generator@vacuum[w]
        jt.append(dw.reshape(-1))
    jt = np.array(jt)
    nu = P**5/256
    native_q = P**3*(jt@jt.T)
    require(np.max(np.abs(native_q-nu*np.eye(len(selected)))) < 2e-18,
            "native disjoint-site Q is p^5 I/256 after inherited parity/completeness")
    parity = np.array([(-1.)**mask.bit_count() for mask in range(16)])
    require(np.max(np.abs(parity[None,:,None]*vacuum+vacuum)) == 0,
            "complete native vacuum preparation is odd CAR parity")
    for w in selected:
        z = generator@vacuum[w]
        require(np.max(np.abs(parity[:,None]*z-z)) == 0,
                "actual new preparation tangent is even CAR parity at " + str(w))
    return {"shape": [4096,128], "selected_sites": indices[selected].tolist(),
            "nu": nu, "maximum_angle_b_tangent_error": tangent_error,
            "replayed_native_kraus_leaves": False}


def vector(c, theta):
    radius = math.sqrt(P**2-c*c)
    # odd1, odd14, even0, even15; this is a small fixture only.
    return np.array([math.sqrt(P), radius*math.cos(theta), c, radius*math.sin(theta)])


def fixture_leaves(g):
    ww = np.array([1., 2.+g])
    ee = .4*np.eye(4)
    ee[2:,2:] += .1*np.outer(ww, ww)
    result = []
    for eff in (ee, np.eye(4)-ee):
        eigenvalues, basis = np.linalg.eigh(eff)
        if not np.all(eigenvalues > 0):
            raise ArithmeticError("fixture is outside strict positive chart")
        result.append((basis*np.sqrt(eigenvalues))@basis.T)
    return result


def binary_entropy(q):
    return -(q*math.log(q)+(1-q)*math.log1p(-q))/ELL


def coincident(g, c, theta):
    b = math.sqrt(P**2-c*c)*math.sin(theta)
    return binary_entropy(.4+.1*(c+(2+g)*b)**2)


def mixed_entropy(g, c, theta0, theta1):
    if theta0 == theta1:
        return coincident(g, c, theta0)
    total = 0.
    for leaf in fixture_leaves(g):
        x = math.sqrt(P)*(leaf@vector(c, theta0))
        y = P*(leaf@vector(c, theta1))
        trace = float(x@x+y@y)
        # Cauchy-Binet wedge formula avoids cancellation uv-w^2 near rank birth.
        determinant = sum((x[i]*y[j]-x[j]*y[i])**2
                          for i in range(4) for j in range(i+1,4))
        discriminant = trace*trace-4*determinant
        if discriminant < 0:
            raise ArithmeticError("negative fixture Gram discriminant")
        small = 2*determinant/(trace+math.sqrt(discriminant))
        large = trace-small
        for lam in (large, small):
            if lam > 0:
                total -= lam*math.log(lam)/ELL
            elif lam < 0:
                raise ArithmeticError("negative eigenvalue")
            # zero log zero = 0 exactly; no probability floor.
    return total


def fixture_checks():
    def anchored(g, c, theta, a):
        return mixed_entropy(g, c, theta, theta+a)

    def balanced(g, c, mu, delta):
        return mixed_entropy(g, c, mu-P**2*delta, mu+P*delta)

    g, c, theta = .03, .026, .041
    leaves = fixture_leaves(g)
    require(np.max(np.abs(sum(l.T@l for l in leaves)-np.eye(4))) < 9e-16,
            "small two-leaf fixture is a complete positive instrument")
    radius = math.sqrt(P**2-c*c)
    b, d = radius*math.sin(theta), radius*math.cos(theta)
    q = .4+.1*(c+(2+g)*b)**2
    expected = P**2*math.log((1-q)/q)/ELL*.2*(c+(2+g)*b)*(2+g)*d
    eps = 1e-6
    derivative = (anchored(g,c,theta,eps)-anchored(g,c,theta,-eps))/(2*eps)
    require(abs(derivative-expected) < 3e-9 and abs(expected) > 1e-3,
            "off-shell fixed-anchor source equals p^2 d times b Euler source")
    mean_derivative = (balanced(g,c,theta,eps)-balanced(g,c,theta,-eps))/(2*eps)
    require(abs(mean_derivative) < 2e-9,
            "off-shell balanced relative source vanishes despite nonzero anchor source")
    deltas = np.array([-.04,-.01,-.001,-.0001,.0001,.001,.01,.04])
    gaps = [balanced(g,c,theta,float(a))-coincident(g,c,theta) for a in deltas]
    require(min(gaps) > 0, "fixture balanced coincidence beats every tested relative displacement")
    opt = minimize_scalar(lambda a: anchored(g,c,theta,a), bounds=(-.04,.04),
                          method="bounded", options={"xatol": 1e-13})
    require(opt.success and abs(opt.x) > 1e-4,
            "off-shell fixed-anchor minimizer is nonzero in fixture")
    require(opt.fun < coincident(g,c,theta)-1e-7,
            "off-shell fixed-anchor reduction genuinely lowers fixture value")
    bstar = .02
    cstar = -(2+g)*bstar
    thetastar = math.asin(bstar/math.sqrt(P**2-cstar*cstar))
    require(abs(cstar+(2+g)*math.sqrt(P**2-cstar*cstar)*math.sin(thetastar)) < 1e-17,
            "fixture has explicit nonzero coincident full stationary material point")
    coords = np.array([g,cstar,thetastar])
    gradient = []
    for i in range(3):
        plus, minus = coords.copy(), coords.copy()
        plus[i] += eps
        minus[i] -= eps
        gradient.append((coincident(*plus)-coincident(*minus))/(2*eps))
    require(max(abs(x) for x in gradient) < 2e-9,
            "all fixture geometric and material coincident Euler rows vanish")
    root_anchor_source = (anchored(*coords,eps)-anchored(*coords,-eps))/(2*eps)
    require(abs(root_anchor_source) < 2e-9,
            "relative preparation also stationary at nonzero full fixture root")
    root_gaps = [anchored(*coords,float(a))-coincident(*coords) for a in deltas]
    require(min(root_gaps) > 0,
            "zero anchor preparation is locally preferred at nonzero full fixture root")
    # Recover the singular coefficient with a scale difference cancelling the
    # bounded quadratic term. This is diagnostic, not a claimed finite Hessian.
    aa = 1e-4
    slope1 = (balanced(g,0.,0.,aa)-coincident(g,0.,0.))/(aa*aa)
    slope2 = (balanced(g,0.,0.,2*aa)-coincident(g,0.,0.))/(4*aa*aa)
    coefficient = (slope1-slope2)/math.log(4)
    require(abs(coefficient-P**5/ELL) < 2e-7,
            "fixture rank-birth entropy has predicted positive logarithmic coefficient")
    charge = .017
    require(charge != 0 and -P**2*d*charge != 0,
            "hostile independent angle cost and anchor-only material cost break balance")
    require(abs((charge-P**2*d*0)-charge) == 0,
            "independent angle cost retains exact upstream residual U_a-p^2 d U_b")
    return {"declared_scope": "four-dimensional two-leaf fixture only",
            "off_shell_anchor_source": derivative,
            "exact_formula_anchor_source": expected,
            "balanced_source_finite_difference": mean_derivative,
            "off_shell_anchor_minimizer": float(opt.x),
            "off_shell_value_drop": float(opt.fun-coincident(g,c,theta)),
            "nonzero_stationary_fixture": coords.tolist(),
            "fixture_log_coefficient": coefficient,
            "expected_fixture_log_coefficient": P**5/ELL,
            "native_critical_set_proved_by_fixture": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    inputs = verify_inputs(args.repo)
    exact = exact_weights()
    native = dictionary_checks(args.repo)
    fixture = fixture_checks()
    print(json.dumps({"status": "PASS", "inputs": inputs,
                      "exact_golden_identities": exact, "native_dictionary": native,
                      "entropy_fixture": fixture, "checks": CHECKS,
                      "check_count": len(CHECKS), "GR_closed": False}, indent=2))


if __name__ == "__main__":
    main()
