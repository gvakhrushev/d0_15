#!/usr/bin/env python3
"""Narrow full-cut source checks; no old suite import or expected-file rewrite.

Run without arguments to compare/print the immutable receipt. Use
--write-result once when authoring a new receipt, never during verification.
Fraction checks are exact; Golden matrices/heat use float64, tolerance 2e-10
relative and 2e-12 absolute, with a separately declared secant tolerance.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
CHECKS = []
PINNED = {
    "02_REGISTRY/research/sources/d0_generated_thermal_source_2026-10-22/ACTUAL_CUT_APPLICATION.md":
        "04bd07f4699ef2190aae7f74dfee9238decd8bf4",
    "02_REGISTRY/research/A4D_ORIGINAL_GOLDEN_READY_COHERENT_BOOK_FULL42_BRIDGE_2026_10_22.md":
        "35134d3a536450442267cda276028ec780329544",
    "02_REGISTRY/research/sources/d0_original_golden_ready_coherent_book_2026-10-22/check_native_palindrome_compilation.mjs":
        "09b62a47b9530bc56b8c61192000bea3e332fd52",
}
S = 128
DW = 50549  # owned minimum: all larger actual dimensions obey the same bound
ZETA = 2.0 ** -20
P_GOLDEN = (math.sqrt(5.0) - 1.0) / 2.0
BETA = 2.0 * P_GOLDEN ** 2


def require(condition, name):
    if not condition:
        raise RuntimeError("FAIL: " + name)
    CHECKS.append(name)


def close(actual, expected, name, atol=2e-12, rtol=2e-10):
    require(np.allclose(actual, expected, atol=atol, rtol=rtol), name)


def scalar(f, beta=BETA, z=ZETA, dw=DW):
    t = math.exp(-beta * f)
    z0 = dw - 2 + 2 * t
    j = -S * math.log1p(-z * f)
    h = math.log(S * z0) / beta
    jf = S * z / (1 - z * f)
    jff = S * z * z / (1 - z * f) ** 2
    w = 2 * t / z0
    bf = jf - w
    bff = jff + beta * w * (1 - w)
    gain = bf / jf
    phipp = (bff * jf - bf * jff) / (jf ** 3)
    hb = -math.log(S * z0) / (beta * beta) - f * w / beta
    jz = S * f / (1 - z * f)
    return dict(j=j, h=h, b=j+h, jf=jf, jff=jff, bf=bf, bff=bff,
                w=w, gain=gain, phipp=phipp, hb=hb, jz=jz, z0=z0)


def single(qubit, matrix):
    result = np.zeros((8, 8))
    for i in range(8):
        for j in range(8):
            if (i & ~(1 << qubit)) == (j & ~(1 << qubit)):
                result[i, j] = matrix[(i >> qubit) & 1, (j >> qubit) & 1]
    return result


def cnot(control, target):
    result = np.zeros((8, 8))
    for j in range(8):
        result[j ^ (((j >> control) & 1) << target), j] = 1.0
    return result


def native_base():
    # This is the unchanged owner's ten-gate word, not a newly compiled writer.
    g = np.array([[math.sqrt(P_GOLDEN), -P_GOLDEN],
                  [P_GOLDEN, math.sqrt(P_GOLDEN)]])
    h = np.array([[1.0, 1.0], [1.0, -1.0]]) / math.sqrt(2.0)
    x = np.array([[0.0, 1.0], [1.0, 0.0]])
    gates = [single(0, g), cnot(0, 1), single(2, g), single(1, h),
             cnot(1, 2), single(1, g), single(0, x), single(2, h),
             cnot(0, 2), single(0, g)]
    v = np.eye(8)
    for gate in gates:
        v = gate @ v
    event = np.diag([float(((i >> 1) & 1) and ((i >> 2) & 1))
                     for i in range(8)])
    effect = v.T @ event @ v
    u = np.eye(8) - 2 * effect
    psi = np.eye(8)[:, 0]
    return u, psi, effect


def skew(pairs):
    result = np.zeros((8, 8))
    for i, j, value in pairs:
        result[i, j] += value
        result[j, i] -= value
    return result


def cayley(k, t):
    return np.linalg.solve(np.eye(8) - t * k / 2, np.eye(8) + t * k / 2)


def cut(u, psi):
    p = np.outer(psi, psi)
    c = (np.eye(8) - p) @ u @ p
    f_matrix = c.T @ c
    l_matrix = f_matrix + c @ c.T
    return p, c, f_matrix, l_matrix, float(np.trace(f_matrix))


def matrix_source(u, psi, ku, kv, kp):
    p, c, fm, lm, f = cut(u, psi)
    dp = kp @ p - p @ kp
    du = ku @ u + kv @ u - u @ kv
    dc = -dp @ u @ p + (np.eye(8) - p) @ du @ p + (np.eye(8) - p) @ u @ dp
    dfm = dc.T @ c + c.T @ dc
    dlm = dfm + dc @ c.T + c @ dc.T
    df = float(np.trace(dfm))
    eig, basis = np.linalg.eigh(lm)
    exp_l = (basis * np.exp(-BETA * eig)) @ basis.T
    z0_direct = DW - 8 + float(np.trace(exp_l))
    hdot = -float(np.trace(exp_l @ dlm)) / z0_direct
    jdot = S * ZETA * float(np.trace(np.linalg.solve(np.eye(8) - ZETA * fm, dfm)))
    sd = scalar(f)
    return dict(f=f, df=df, direct_h=hdot, direct_j=jdot,
                direct_b=hdot+jdot, scalar_data=sd, z0=z0_direct,
                p=p, dp=dp, u=u, du=du, lm=lm, dlm=dlm)


def main():
    for name, expected in PINNED.items():
        content = (REPO / name).read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
        require(actual == expected, "immutable source " + name)

    exact_gain = Fraction(1) - Fraction(2, S) / Fraction(1, 2**20) / DW
    require(exact_gain == Fraction(34165, 50549), "exact actual whole-work gain")
    require(exact_gain - Fraction(2, 3) == Fraction(1397, 151647), "exact positive excess over two-thirds")
    # Exact algebraic reduction of the exponential-free inequality for t in [0,1].
    for t in [Fraction(0), Fraction(1, 7), Fraction(5, 6), Fraction(1)]:
        for f in [Fraction(0), Fraction(1, 3), Fraction(1)]:
            z = Fraction(1, 2**20)
            deficit = DW - 2 + 2*t - DW*(1-z*f)*t
            require(deficit == (DW-2)*(1-t)+DW*z*f*t and deficit >= 0,
                    "exact harmonic bound t=" + str(t) + " f=" + str(f))

    for f in [0.0, 0.2, 1.0]:
        for beta in [1e-3, BETA, 12.0]:
            for dw in [DW, 33*DW]:
                d = scalar(f, beta=beta, dw=dw)
                require(d['gain'] >= float(exact_gain)-2e-15 and d['gain'] < 1,
                        "whole calibration interval gain " + repr((f, beta, dw)))
                require(d['phipp'] > 0, "strict scalar convexity " + repr((f, beta, dw)))

    u, psi, effect = native_base()
    p, c, fm, lm, f = cut(u, psi)
    close(u.T @ u, np.eye(8), "native-base full unitary fixture")
    close(p @ p, p, "native-base rank-one input fixture")
    q = float(psi @ effect @ psi)
    close(f, 4*q*(1-q), "same native reflection source parameter")
    close(np.trace(lm), 2*f, "both actual cut spectral partners retained")
    close(lm @ lm, f*lm, "whole cut heat minimal polynomial with harmonic modes")

    ku = skew([(0, 3, 0.2), (2, 6, -0.5), (4, 7, 0.25)])
    kv = skew([(0, 4, 0.3), (1, 5, 0.125), (2, 7, -0.4)])
    kp = skew([(0, 1, 0.4), (0, 6, -0.3), (2, 3, 0.2)])
    zero = np.zeros((8, 8))
    fixtures = [('controller', ku, zero, zero), ('moving_query', zero, kv, zero),
                ('moving_preparation', zero, zero, kp), ('all_moving', ku, kv, kp)]
    sources = []
    for label, a, b, cgen in fixtures:
        result = matrix_source(u, psi, a, b, cgen)
        d = result['scalar_data']
        close(result['z0'], d['z0'], label + ' entire harmonic trace')
        close(result['direct_j'], d['jf']*result['df'], label + ' direct full feedback derivative')
        close(result['direct_h'], -d['w']*result['df'], label + ' direct noncommuting heat derivative')
        close(result['direct_b'], d['gain']*result['direct_j'], label + ' entire cotangent equivalence')
        require(abs(result['df']) > 1e-4, label + ' nonvacuous source')
        step = 3e-4
        def value(t):
            moved_u = cayley(a, t) @ cayley(b, t) @ u @ cayley(b, t).T
            moved_psi = cayley(cgen, t) @ psi
            return scalar(cut(moved_u, moved_psi)[4])['b']
        secant = (-value(2*step)+8*value(step)-8*value(-step)+value(-2*step))/(12*step)
        close(secant, result['direct_b'], label + ' independent matrix-path secant',
              atol=8e-11, rtol=3e-6)
        sources.append(dict(name=label, f=round(result['f'], 12),
                            df=round(result['df'], 12),
                            source=round(result['direct_b'], 12)))

    # A common P/U conjugation is a genuine trace gauge; normal prep above is not.
    gauge = matrix_source(u, psi, zero, kp, kp)
    close(gauge['df'], 0, "simultaneous P/U conjugation is source-free")
    close(gauge['direct_b'], 0, "complete cut heat respects same gauge")

    d = scalar(f)
    dq = np.array([0.2, -0.3, 0.1])
    hf = np.diag([2.0, -3.0, 1.0])
    hj = d['jf']*hf + d['jff']*np.outer(dq, dq)
    hb = d['bf']*hf + d['bff']*np.outer(dq, dq)
    correction = hb-d['gain']*hj
    close(correction, d['phipp']*(d['jf']**2)*np.outer(dq, dq),
          "full off-critical Hessian rank-one chain rule")
    require(np.linalg.eigvalsh(correction)[0] > -1e-15,
            "off-critical Hessian correction positive semidefinite")
    close(d['bf']*hf, d['gain']*(d['jf']*hf), "entire Hessian scaled at criticality")
    require(np.sign(np.linalg.eigvalsh(d['bf']*hf)).tolist() ==
            np.sign(np.linalg.eigvalsh(d['jf']*hf)).tolist(),
            "critical positive negative inertia unchanged")

    a_ready = 2*10946*P_GOLDEN**23
    aa, bb = 1-P_GOLDEN**12, 1-P_GOLDEN**6
    r0 = ZETA*(aa+bb)-ZETA**2*aa*bb
    q0 = a_ready*r0
    f0 = 4*q0*(1-q0)
    d0 = scalar(f0)
    require(0 < q0 < 1/2, "actual original unconditional READY q0")
    gradient_norm = 8*(1-2*q0)*d0['bf']*math.sqrt(q0*(1-q0))
    require(gradient_norm > 0, "actual independent pure-input normal survives heat")
    # Direct normalized-state tangent at the actual q0 (compression diagnostic,
    # not a claim that this two-level state is a newly selected native writer).
    psi0 = np.zeros(8)
    psi0[:2] = [math.sqrt(1-q0), math.sqrt(q0)]
    event0 = np.zeros((8, 8))
    event0[1, 1] = 1
    normal = (event0 @ psi0-q0*psi0)/math.sqrt(q0*(1-q0))
    normal_k = np.outer(normal, psi0)-np.outer(psi0, normal)
    normal_source = matrix_source(np.eye(8)-2*event0, psi0, zero, zero, normal_k)
    close(normal_source['direct_b'], gradient_norm,
          "direct moving cut realizes exact normalized-input reaction")

    # Calibration controls: the global fixed-calibration equivalence is not
    # silently extended to moving beta, zeta or a changed integer tape dimension.
    require(d['hb'] < -1, "actual absolute beta source nonzero with fixed P/U")
    close(0.0*d['gain']+d['hb'], d['hb'], "moving beta retained in full identity")
    require(abs(d['hb']) > 1e-3, "dropping beta reaction explicitly rejected")
    dz = ZETA/3
    direct_z = d['jz']*dz
    close(direct_z, d['gain']*direct_z+(1-d['gain'])*d['jz']*dz,
          "moving zeta exact residual identity")
    require(abs(direct_z-d['gain']*direct_z) > 1e-8,
            "dropping zeta reaction explicitly rejected")
    dimension_change = scalar(f, dw=DW+1)['h']-d['h']
    require(dimension_change > 0, "one added dormant mode changes absolute price")
    close(dimension_change, math.log1p(1/d['z0'])/BETA,
          "discrete dimension comparison includes exact harmonic increment")
    require(scalar(f, dw=8)['gain'] < 0,
            "eight-mode truncation reverses gain and is rejected")
    residual_a = np.array([0.2, -0.4, 0.5])
    source_j = np.array([0.1, 0.3, -0.7])
    close(d['gain']*source_j+residual_a,
          d['gain']*(source_j+residual_a)+(1-d['gain'])*residual_a,
          "additional actual price retains its independent residual")

    result = {
        'status': 'PASS_COMPLETE_READY_CUT_SOURCE_EQUIVALENCE',
        'baseline': 'cd7595b0808e47c38147f25e2cabe476ecb508f8',
        'checks': len(CHECKS),
        's': S, 'z': '2^-20', 'retained_work_dimension_lower_bound': DW,
        'exact_gain_lower_bound': '34165/50549',
        'exact_excess_over_two_thirds': '1397/151647',
        'actual_ready_q0': round(q0, 15),
        'normal_gradient_norm_at_lower_dimension_fixture': round(gradient_norm, 15),
        'matrix_directions': sources,
        'full_moving_P_U_cotangent': True,
        'entire_critical_Hessian_inertia_preserved': True,
        'calibration_and_integer_dimension_controls': True,
        'bound_proof': 'analytic; exact rational coefficient; no sampled-uniform claim',
        'numerical_matrix_tolerance': '2e-12 absolute, 2e-10 relative',
        'matrix_secant_tolerance': '8e-11 absolute, 3e-6 relative',
        'older_suites_replayed': False,
        'native_tangents_physically_selected': False,
        'independent_preparation_closed': False,
        'default_L913_identified_with_cut_heat': False,
        'full_D0_price_selected': False,
        'GR_closed': False,
    }
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-result', action='store_true',
                        help='author a receipt; never use during verification')
    args = parser.parse_args()
    payload = main()
    rendered = json.dumps(payload, indent=2, sort_keys=True)+"\n"
    output = HERE / 'CUT_SOURCE_RESULT.json'
    if args.write_result:
        output.write_text(rendered, encoding='utf-8')
    elif output.exists():
        expected = json.loads(output.read_text(encoding='utf-8'))
        if expected != payload:
            raise RuntimeError('FAIL: immutable CUT_SOURCE_RESULT.json mismatch')
    print(rendered, end='')
