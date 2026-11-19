#!/usr/bin/env python3
"""Same-primary-field scale transport and a complete-CAR128 R source test.

Consumes the owned exact all40+2 Brinkmann reduction; does not replay it.
All Dirac applications use every role, every CAR grade, every reference
column, the true shifted positive adjoint, and the actual unequal old F/R
site counts.  The scientific conclusion is a preparation-dependent R
source on a configured J2 root, not selection of a complete physical price.
"""
from __future__ import annotations

import ast
import hashlib
import itertools
import json
import math
import os
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")

import numpy as np
import sympy as sp


P = (math.sqrt(5.0) - 1.0) / 2.0
ETA = np.diag([1.0, -1.0, -1.0, -1.0])
ETA_NULL = np.array([[0., 1., 0., 0.], [1., 0., 0., 0.],
                     [0., 0., -1., 0.], [0., 0., 0., -1.]])
T = np.array([[1., .5, 0., 0.], [1., -.5, 0., 0.],
              [0., 0., 1., 0.], [0., 0., 0., 1.]])


def require(condition, description):
    if not bool(condition):
        raise ArithmeticError(description)


def creators():
    source = (Path(__file__).resolve().parents[4] / "02_REGISTRY/research/certificates/"
              "a4d_native_curved_soldered_heat.py")
    require(hashlib.sha256(source.read_bytes()).hexdigest() ==
            "bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da",
            "original CAR creator source pin")
    tree = ast.parse(source.read_text(encoding="utf-8"))
    nodes = [node for node in tree.body if
             (isinstance(node, ast.FunctionDef) and node.name == "creator") or
             (isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and
               target.id == "EXTERIOR_ORDER" for target in node.targets))]
    require(len(nodes) == 2, "load only original creator and exterior-order definitions")
    scope = {"s": sp, "lru_cache": lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(source), "exec"), scope)
    require(scope["EXTERIOR_ORDER"] == (0, 2, 3, 1), "literal original exterior order")
    return np.array([np.array(scope["creator"](a)).astype(float) for a in range(4)])


CREATORS = creators()
I16 = np.eye(16)


def exterior_generator(a):
    return sum((a[i, j] * CREATORS[i] @ CREATORS[j].T
                for i in range(4) for j in range(4)), np.zeros((16, 16)))


N2 = np.zeros((4, 4))
N2[1, 2] = N2[2, 0] = 1
N3 = np.zeros((4, 4))
N3[1, 3] = N3[3, 0] = 1
REST_N = [T @ n @ np.linalg.inv(T) for n in (N2, N3)]
GN = np.array([exterior_generator(n) for n in REST_N])


def lift(k):
    g = np.einsum("...a,aij->...ij", k, GN)
    g2 = g @ g
    return I16 + g + g2 / 2 + g2 @ g / 6


def exact_car_and_scaling():
    """Exact original rest-basis identities, including all K coefficients."""
    c = [sp.Matrix(a.astype(int)) for a in CREATORS]
    tt = sp.Matrix([[1, sp.Rational(1, 2), 0, 0],
                    [1, -sp.Rational(1, 2), 0, 0],
                    [0, 0, 1, 0], [0, 0, 0, 1]])
    nn = [sp.Matrix(a.astype(int)) for a in (N2, N3)]
    rest = [tt * a * tt.inv() for a in nn]
    gg = [sum((a[i, j] * c[i] * c[j].T
               for i in range(4) for j in range(4)), sp.zeros(16))
          for a in rest]
    x, y = sp.symbols("Kx Ky", real=True)
    g = x * gg[0] + y * gg[1]
    require((g ** 4).applyfunc(sp.expand) == sp.zeros(16), "exact full16 null lift polynomial")
    ll = sp.eye(16) + g + g ** 2 / 2 + g ** 3 / 6
    cw = (c[0] - c[1]) / 2
    xx = cw * ll
    basis = [sp.eye(16)[:, mask] for mask in range(16)]
    expected_forward = [(basis[5] + basis[6]) / 4,
                        (basis[9] + basis[10]) / 4]
    expected_adjoint = [(-basis[9] + basis[10]) / 4,
                        (basis[5] - basis[6]) / 4]
    vectors = expected_forward + expected_adjoint
    for a, variable in enumerate((x, y)):
        dx = xx.diff(variable)
        for mask in (0, 1, 14, 15):
            require(sp.simplify(dx * basis[mask] -
                               (expected_forward[a] if mask == 1 else sp.zeros(16, 1)))
                    == sp.zeros(16, 1), "exact forward rest-clock CAR derivative")
            require(sp.simplify(dx.T * basis[mask] -
                               (expected_adjoint[a] if mask == 14 else sp.zeros(16, 1)))
                    == sp.zeros(16, 1), "exact adjoint spatial3 CAR derivative")
    gram = sp.Matrix.hstack(*vectors).T * sp.Matrix.hstack(*vectors)
    require(gram == sp.eye(4) / 8, "four actual link derivative vectors orthogonal")

    # Every possible v-role creator/annihilator applied to the actual
    # four-mask preparation misses the link-sensitive four-mask space.
    projector = sp.diag(*[int(mask in (5, 6, 9, 10)) for mask in range(16)])
    for a in (0, 1):
        for cc in (c[a], c[a].T):
            for mask in (0, 1, 14, 15):
                require(projector * cc * basis[mask] == sp.zeros(16, 1),
                        "coframe-H v-role image misses link-sensitive masks")

    scale, t, f, q, p = sp.symbols("s t f q p", nonzero=True, real=True)
    ep = p ** 2 * (1 + t ** 2 * f)
    bp = (p - p ** 2 * t ** 2 * q) ** 2
    replacement = {t: scale * t, f: f / scale ** 2, q: q / scale ** 2}
    require(sp.expand(ep.subs(replacement, simultaneous=True) - ep) == 0,
            "exact scaled configured AF query")
    require(sp.expand(bp.subs(replacement, simultaneous=True) - bp) == 0,
            "exact scaled configured scene query")
    # Original star density has degree two in coframe legs.  Check that
    # exponent together with an actual nonzero Lorentzian kinetic probe.
    hh = sp.Rational(1, 7)
    ee = sp.Matrix([[1, 0, 0, 0], [hh / 2, 1, 0, 0],
                    [0, 0, 1, 0], [0, 0, 0, 1]])
    eta_null = sp.Matrix(ETA_NULL.astype(int))
    metric = ee.T * eta_null * ee

    def epsilon4(values):
        return (-1) ** sum(values[i] > values[j] for i in range(4) for j in range(i + 1, 4))

    def actual_star_probe(coframe):
        # Original six-face contraction (all identities except one proper
        # null boost).  This is a nonzero off-shell homogeneity probe, not
        # another field-equation calculation.  The null-oriented convention
        # is the owner's formula (3.3), including its det(T)=-1 convention.
        plaquette = sp.diag(2, sp.Rational(1, 2), 1, 1)
        curvature = (plaquette - plaquette.inv()) / 2
        raised = curvature * eta_null.inv()
        legs = sp.Rational(1, 4) * coframe
        value = 0
        for r in range(4):
            for ss in range(r + 1, 4):
                if (r, ss) != (0, 1):
                    continue  # the other five actual plaquettes are identity
                uu, vv = [a for a in range(4) if a not in (r, ss)]
                for a in range(4):
                    for b in range(a + 1, 4):
                        for cc in range(4):
                            for dd in range(cc + 1, 4):
                                if len({a, b, cc, dd}) != 4:
                                    continue
                                value += (epsilon4((r, ss, uu, vv)) * epsilon4((a, b, cc, dd)) *
                                          (legs[a, uu] * legs[b, vv] - legs[b, uu] * legs[a, vv]) *
                                          raised[cc, dd])
        return sp.expand(value / sp.Rational(1, 4) ** 4)

    star = actual_star_probe(ee)
    require(star != 0 and sp.simplify(actual_star_probe(ee / scale) - star / scale ** 2) == 0,
            "nonzero original six-face star coframe homogeneity with fixed h")
    gradient = sp.Matrix([1, 2, 3, 4])
    qq = (gradient.T * metric.inv() * gradient)[0]
    qq_scaled = ((gradient / scale ** 2).T *
                 (metric / scale ** 2).inv() * (gradient / scale ** 2))[0]
    require(qq != 0 and sp.simplify(qq_scaled - qq / scale ** 2) == 0,
            "exact inverse-metric and scalar-amplitude kinetic scaling")
    require(sp.simplify(scale ** 2 * metric / scale ** 2 - metric) == sp.zeros(4),
            "exact calibrated metric dictionary")
    require(sp.simplify((t * t / scale ** 2) / (t * t) - scale ** -2) == 0,
            "fixed-query common-null first jet scale")
    return {"link_vector_norm_squared": "1/8", "full_link_gram": "I4/8",
            "fixed_query_first_source_factor": "s^-2",
            "off_shell_configured_query_transport": "t'=s*t"}


def original_counts(cost, size):
    """Literal old F/R boxes, with exact Q(p) cell routing.

    A pair (a,b) means a+b*p, p^2=1-p.  Comparison with each rational
    cell boundary reduces to the sign of A+B*sqrt(5), using integer
    squares.  Thus no floating box-centre decision enters the counts.
    """
    counts = np.zeros(size ** 4, dtype=np.int64)

    def radical_sign(a, b):
        if a == 0:
            return (b > 0) - (b < 0)
        if b == 0 or (a > 0) == (b > 0):
            return (a > 0) - (a < 0)
        difference = a * a - 5 * b * b
        return ((difference > 0) - (difference < 0)) * (1 if a > 0 else -1)

    def visit(remaining, depth, left, width):
        if remaining == 0:
            index = 0
            for axis in range(4):
                ca = 2 * left[axis][0] + width[axis][0]
                cb = 2 * left[axis][1] + width[axis][1]
                aa, bb = size * (2 * ca - cb), size * cb
                digit = 0
                for cut in range(1, size):
                    if radical_sign(aa - 4 * cut, bb) >= 0:
                        digit = cut
                    else:
                        break
                index = index * size + digit
            counts[index] += 1
            return
        axis = depth % 4
        wf = width.copy()
        wa, wb = width[axis]
        wf[axis] = (wb, wa - wb)
        visit(remaining - 1, depth + 1, left.copy(), wf)
        if remaining >= 2:
            lr, wr = left.copy(), width.copy()
            la, lb = left[axis]
            lr[axis] = (la + wb, lb + wa - wb)
            wr[axis] = (wa - wb, 2 * wb - wa)
            visit(remaining - 2, depth + 1, lr, wr)

    visit(cost, 0, [(0, 0)] * 4, [(1, 0)] * 4)
    require(int(counts.sum()) == 10946, "original cost20 Fibonacci count")
    require(int(counts.min()) == 29 and int(counts.max()) == 78,
            "original unequal counts29 through78")
    return counts


def reference_characters(size, indices):
    pairs = []
    for k in itertools.product(range(size), repeat=4):
        minus = tuple((-a) % size for a in k)
        if k < minus:
            pairs.append(k)
        if len(pairs) == 64:
            break
    require(len(pairs) == 64, "complete64 original real Fourier pairs exist")
    columns = []
    for k in pairs:
        phase = 2 * math.pi * (indices @ np.array(k)) / size
        columns.extend((math.sqrt(2 / size ** 4) * np.cos(phase),
                        math.sqrt(2 / size ** 4) * np.sin(phase)))
    ff = np.array(columns).T
    require(np.max(np.abs(ff.T @ ff - np.eye(128))) < 2e-14,
            "all128 Fourier reference columns orthonormal")
    require(np.max(np.abs(np.sum(ff * ff, axis=1) - 128 / size ** 4)) < 2e-14,
            "all128 reference columns have exact constant local diagonal")
    return ff


def main():
    exact = exact_car_and_scaling()
    size = 4
    sites = size ** 4
    ell = 1 / size
    indices = np.array(list(itertools.product(range(size), repeat=4)))
    forward, backward = [], []
    for role in range(4):
        plus, minus = indices.copy(), indices.copy()
        plus[:, role] = (plus[:, role] + 1) % size
        minus[:, role] = (minus[:, role] - 1) % size
        forward.append(np.ravel_multi_index(plus.T, (size,) * 4))
        backward.append(np.ravel_multi_index(minus.T, (size,) * 4))
    counts = original_counts(20, size)
    total = int(counts.sum())
    rho = sites * counts / total
    test = 1 + indices[:, 0] ** 2 + indices[:, 1] * indices[:, 2] + indices[:, 3]
    inverse_pf = sum((Fraction(int(n), total) *
                      Fraction(int(value) * total, sites * int(n))
                      for n, value in zip(counts, test)), Fraction())
    require(inverse_pf == Fraction(int(test.sum()), sites),
            "exact inverse-PF source with literal unequal old counts")

    # Fix a chart before shrinking the matter amplitudes: no field-dependent
    # change of the integer scale is taken in any source derivative.
    h_chart, k_sum_chart, margin = .2, .2, P
    generator_bound = max(np.linalg.norm(a, 2) for a in GN)
    bound = (math.sqrt(float(rho.max())) *
             max(1., math.sqrt(2.) + h_chart / (2 * math.sqrt(2.))) *
             math.exp(generator_bound * k_sum_chart))
    exponent, scale = 0, 1.
    while scale * bound > margin:
        exponent += 1
        scale = P ** exponent
    alpha = P * P * ell * ell / 128
    epsilon = 2 * alpha
    ff = reference_characters(size, indices)
    amp = scale * scale * .005

    def psi_derivative(u):
        return amp * np.array([-2 * math.pi * math.sin(2 * math.pi * u),
                               1.2 * math.pi * math.cos(2 * math.pi * u)])

    history = [np.array([amp, 0.])]
    for j in range(size):
        history.append(history[-1] + ell * psi_derivative((j + .5) * ell))
    require(np.linalg.norm(history[-1] - history[0]) < 1e-18,
            "actual midpoint material history closes at this regulator")
    psi = np.array(history[:-1])[indices[:, 0]]
    psi_s = psi / scale ** 2
    slack = np.sqrt(1 - P - np.sum(psi_s * psi_s, axis=1))
    matter = np.zeros((sites, 16))
    matter[:, 0], matter[:, 15] = psi_s[:, 0], psi_s[:, 1]
    matter[:, 1], matter[:, 14] = math.sqrt(P), slack
    prep = ff[:, None, :] * matter[:, :, None] / math.sqrt(128)
    flat_prep = prep.reshape(sites * 16, 128)
    require(np.max(np.abs(flat_prep.T @ flat_prep - np.eye(128) / 128)) < 2e-16,
            "actual normalized rest-clock preparation retains fullRIGHT128")
    require(abs(float(np.sum(prep * prep)) - 1) < 1e-14,
            "complete state normalizer one, no postselection")

    q0 = 1 - 2 ** -20 * 4 * P ** 3
    r0 = 1 - 2 ** -20 * 4 * P ** 3 * (1 + P ** 6)
    lam = -2 * P ** -5 * (r0 / q0 + P ** 6)
    u = indices[:, 0] * ell
    xx, yy = indices[:, 2] * ell - .5, indices[:, 3] * ell - .5

    def primary_h(amplitude, tau, x, y):
        energy = np.array([np.dot(psi_derivative(t), psi_derivative(t)) for t in tau])
        wave = (1 + .2 * np.sin(2 * math.pi * tau)) * (x * x - y * y)
        return -lam * energy * (x * x + y * y) + amplitude * wave

    def primary(amplitude):
        hh = primary_h(amplitude, u - ell / 2, xx, yy)
        advanced = primary_h(amplitude, u + ell / 2, xx, yy)
        kk = np.stack((.5 * (advanced - primary_h(amplitude, u + ell / 2, xx - ell, yy)),
                       .5 * (advanced - primary_h(amplitude, u + ell / 2, xx, yy - ell))), axis=1)
        return hh, kk

    def operator(hh, kk):
        ee = np.broadcast_to(np.eye(4), (sites, 4, 4)).copy()
        ee[:, 1, 0] = hh / 2
        rest_e = T @ ee
        inverse_legs = scale * np.sqrt(rho)[:, None, None] * (
            ETA @ np.linalg.inv(rest_e).transpose(0, 2, 1))
        cr = np.einsum("zar,aij->zrij", inverse_legs, CREATORS)
        xr = cr.copy()
        xr[:, 0] = cr[:, 0] @ lift(kk)
        native_metric = (rest_e.transpose(0, 2, 1) @ ETA @ rest_e) / scale ** 2
        target_metric = ee.transpose(0, 2, 1) @ ETA_NULL @ ee
        require(np.max(np.abs(scale ** 2 * native_metric - target_metric)) < 2e-15,
                "decoded density-dressed native metric is same primary metric")
        recovered_q = inverse_legs.transpose(0, 2, 1) @ ETA @ inverse_legs / rho[:, None, None]
        require(np.max(np.abs(np.linalg.inv(recovered_q) - native_metric)) < 2e-12,
                "actual inverse legs reconstruct the scaled operational metric")
        require(np.max(np.abs(hh)) < h_chart and
                np.max(np.sum(np.abs(kk), axis=1)) < k_sum_chart,
                "fields remain in the predeclared fixed-scale chart")
        actual_norm = max(float(np.linalg.svd(cr, compute_uv=False).max()),
                          float(np.linalg.svd(xr, compute_uv=False).max()))
        require(actual_norm < margin, "all four actual Julia inputs strictly contract")
        return cr, xr, actual_norm

    def apply_d(cr, xr, field):
        out = np.zeros_like(field)
        for role in range(4):
            out += xr[:, role] @ field[forward[role]] - cr[:, role] @ field
            out += (xr[:, role].transpose(0, 2, 1) @ field)[backward[role]]
            out -= cr[:, role].transpose(0, 2, 1) @ field
        return out / ell

    def gradients(cr, xr, kk, dc):
        result = np.zeros((sites, 2))
        for a in range(2):
            dx = cr[:, 0] @ lift(kk) @ GN[a]
            direct = dx @ prep[forward[0]]
            adjoint = dx.transpose(0, 2, 1) @ prep
            result[:, a] = 2 / ell * (
                np.einsum("zij,zij->z", dc, direct) +
                np.einsum("zij,zij->z", dc[forward[0]], adjoint))
        return result

    free = ((indices[:, 0] == 1) & (indices[:, 1] == 1) &
            (indices[:, 2] == 2) & (indices[:, 3] == 2))
    site = int(np.flatnonzero(free)[0])
    hessian = scale ** 2 * rho * (1 - np.sum(psi_s ** 2, axis=1)) / (4 * sites * ell ** 2)
    require(float(hessian.min()) > 0, "complete-preparation link Hessian strictly positive")
    records, previous = [], None
    max_gradient_error = max_hessian_error = max_h_independence_error = 0.
    for amplitude in (.125, .25):
        hh, kk = primary(amplitude)
        cr, xr, actual_norm = operator(hh, kk)
        dc = apply_d(cr, xr, prep)
        value = float(np.vdot(dc, dc).real)
        ddc = apply_d(cr, xr, dc)
        require(abs(float(np.vdot(prep, ddc).real) - value) < 2e-13,
                "true shifted positive adjoint gives R=normDC squared")
        grad = gradients(cr, xr, kk, dc)
        delta = 1 / 32
        finite = []
        for a in range(2):
            costs = []
            for sign in (-1, 1):
                perturbed = kk.copy()
                perturbed[site, a] += sign * delta
                changed_x = xr.copy()
                changed_x[site, 0] = cr[site, 0] @ lift(perturbed[site])
                changed_dc = apply_d(cr, changed_x, prep)
                costs.append(float(np.vdot(changed_dc, changed_dc).real))
            finite_grad = (costs[1] - costs[0]) / (2 * delta)
            finite_hessian = (costs[1] + costs[0] - 2 * value) / delta ** 2
            ge = abs(finite_grad - grad[site, a])
            he = abs(finite_hessian - hessian[site])
            max_gradient_error, max_hessian_error = max(max_gradient_error, ge), max(max_hessian_error, he)
            require(ge < 2e-12 and he < 2e-10,
                    "direct full native R agrees with analytic local link source and Hessian")
            finite.append({"polarization": a, "gradient": float(grad[site, a]),
                           "direct_finite_gradient": finite_grad,
                           "analytic_hessian": float(hessian[site]),
                           "direct_finite_hessian": finite_hessian})

        # The H-only change is an unrestricted coframe change at fixed K.
        # Its source cannot enter the four link-sensitive CAR masks.
        h_changed = hh + .01 * np.cos(indices[:, 0] + 2 * indices[:, 3])
        cc, xc, _ = operator(h_changed, kk)
        changed_grad = gradients(cc, xc, kk, apply_d(cc, xc, prep))
        h_error = float(np.max(np.abs(changed_grad - grad)))
        max_h_independence_error = max(max_h_independence_error, h_error)
        require(h_error < 3e-13, "link affine intercept independent of coframe H")

        # Consume the owned 40->3->1 classification on genuinely free sites.
        interior = np.all((indices >= 1) & (indices <= size - 2), axis=1)
        lap = (hh[forward[2]] + hh[backward[2]] + hh[forward[3]] +
               hh[backward[3]] - 4 * hh) / ell ** 2
        energy = np.sum((np.array(history[1:]) - np.array(history[:-1])) ** 2, axis=1) / ell ** 2
        residual = lap[forward[0]] + 4 * lam * energy[indices[:, 0]]
        require(np.max(np.abs(residual[interior])) < 3e-14,
                "same actual midpoint history solves owned configured J2 trace equation")
        cartan = np.stack((.5 * (hh - hh[backward[2]]),
                           .5 * (hh - hh[backward[3]])), axis=1)
        require(np.max(np.abs((kk[backward[0]] - cartan)[interior])) < 2e-16,
                "same finite representatives solve both owned independent Cartan rows")
        if previous is not None:
            old_k, old_g = previous
            affine_error = float(np.max(np.abs(grad - old_g - hessian[:, None] * (kk - old_k))))
            require(affine_error < 3e-13, "full link source affine with proved diagonal Hessian")
            difference = float(grad[site, 0] - old_g[site, 0])
            predicted_difference = float(hessian[site] * (kk[site, 0] - old_k[site, 0]))
            require(abs(predicted_difference) > 1e-8,
                    "two nonzero harmonic-wave amplitudes separate the actual interior R source")
            require(max(abs(float(grad[site, 0])), abs(float(old_g[site, 0]))) > abs(difference) / 3,
                    "at least one configured exact root has nonzero free-interior R link source")
        previous = kk, grad
        records.append({"wave_amplitude": amplitude, "R": value,
                        "max_Julia_input_norm": actual_norm,
                        "configured_trace_residual": float(np.max(np.abs(residual[interior]))),
                        "free_edge": indices[site].tolist(), "K": kk[site].tolist(),
                        "source": finite})

    result = {
        "status": "PASS", "exact_symbolic": exact,
        "carrier": {"grid": [size] * 4, "sites": sites, "CAR_grades": 16,
                    "reference_columns": 128, "Dirac_roles": 4,
                    "original_exterior_order": [0, 2, 3, 1],
                    "adjoint": "actual shifted positive adjoint", "normalizer": 1},
        "density": {"native_cost_depth": 20, "literal_FR_words": total,
                    "cell_routing": "exact Q(p), integer sign of A+B*sqrt(5)",
                    "min_count": int(counts.min()), "max_count": int(counts.max()),
                    "min_rho": float(rho.min()), "max_rho": float(rho.max()),
                    "counts_sha256": hashlib.sha256(json.dumps(counts.tolist()).encode()).hexdigest(),
                    "inverse_PF": "exact Fraction equality with actual counts"},
        "scale": {"p_exponent": exponent, "s": scale, "fixed_chart_bound": bound,
                  "scaled_bound": scale * bound, "strict_margin": margin,
                  "ell_unchanged": ell, "alpha_unchanged": alpha,
                  "epsilon_unchanged": epsilon,
                  "blank_lower_bound": 1 - 2 * P ** 2 * margin ** 2},
        "link_hessian": "s^2*rho_z*(1-|Psi_s,z|^2)/(4*S*ell^2)",
        "minimum_link_hessian": float(hessian.min()),
        "max_direct_gradient_error": max_gradient_error,
        "max_direct_hessian_error": max_hessian_error,
        "max_H_independence_error": max_h_independence_error,
        "two_primary_representatives": records,
        "source_difference": difference, "predicted_source_difference": predicted_difference,
        "scope": {"owned_all40_reduction_consumed": True,
                  "new_stationary_root_search": False,
                  "interior_fixed_collar_tangent": True,
                  "A_variation_is_not_an_admissible_global_cost_comparison": True,
                  "native_generator_admission_proved": False,
                  "complete_physical_Cost_minus_Info_selected": False,
                  "primitive_port_cost_or_Info_evaluated": False,
                  "full128_recycling_propagation_proved": False,
                  "GR_closed": False}}
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
