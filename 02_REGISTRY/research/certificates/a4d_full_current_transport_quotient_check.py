#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=180
"""All-role current identity and the obstruction to a local transport quotient.

Exact rational controls for A4D_GLOBAL_SOURCE_IMAGE_TORQUE_CLOSURE.md.
The transport examples are local curvature controls, not asserted stationary
shared-link realizations or fixed-source theory counterexamples.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json

import numpy as np
import sympy as sp

import a4d_identity_quarter_nonlinear_response_check as N
import a4d_stationary_response_memory_check as R


INPUT_HEAD = "551eba1a84fe15ebdcd100b90348f291bd109692"
I = N.I
ETA = np.diag(N.SIG).astype(object)
ZERO = np.zeros((4, 4), dtype=object)


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def adj(a):
    return ETA @ a.T @ ETA


def ad(a, x):
    return a @ x @ adj(a)


def pair(w, a):
    return np.sum(w * a)


def coordinates(x):
    assert np.array_equal(x + adj(x), ZERO)
    return np.array([x[a, b] for a, b in N.PAIRS], dtype=object)


def cayley(t, generator):
    out = N.inverse(I - t * generator / 2) @ (I + t * generator / 2)
    assert np.array_equal(out.T @ ETA @ out, ETA)
    assert sp.Matrix(out.tolist()).det() == 1 and out[0, 0] >= 1
    return out


def momenta(w, p, x):
    pi = adj(p)
    left = pair(w, (x @ p + pi @ x) / 2)
    right = pair(w, (p @ x + x @ pi) / 2)
    v, c = (p + pi) / 2, (p - pi) / 2
    even = pair(w, (v @ x + x @ v) / 2)
    odd = pair(w, (x @ c - c @ x) / 2)
    assert left == even + odd and right == even - odd
    assert np.array_equal(v @ c, c @ v)
    assert np.array_equal(v @ v - c @ c, I)
    return left, right, even, odd


def local_transport_check():
    _, _, vertical, m, d, _, _ = R.face_data(I)
    m, d = sp.Matrix(m.tolist()), sp.Matrix(d.tolist())
    av = sp.Matrix(vertical.tolist()) * m
    null = sp.Matrix.hstack(*m.nullspace())
    metric_null = sp.Matrix.hstack(*d.nullspace())
    ad_generators = []
    for x in N.G:
        block = sp.Matrix.hstack(*[
            sp.Matrix(coordinates(x @ y - y @ x).tolist()) for y in N.G
        ])
        ad_generators.append(sp.diag(*([block] * 6)))
    transfer = sp.Matrix.hstack(*[a * null for a in ad_generators])
    one = sp.Matrix.hstack(null, transfer)
    basis = sp.Matrix.hstack(*one.columnspace())
    two = sp.Matrix.hstack(basis, *[a * basis for a in ad_generators])
    ward_kernel = sp.Matrix.hstack(*(av * transfer).nullspace())
    check("FULL_SOLDER_NULL_DIMENSION_20", null.cols == 20)
    check("FIRST_ADJOINT_SPAN_DIMENSION_35", one.rank() == 35)
    check("SECOND_ADJOINT_SPAN_DIMENSION_36", two.rank() == 36)
    check("FIRST_SOLDER_TRANSFER_RANK_15", (m * transfer).rank() == 15)
    check("FIRST_TRANSFER_WARD_RANK_6", (av * transfer).rank() == 6)
    visible = d * transfer * ward_kernel
    check("WARD_PRESERVING_SOURCE_TRANSFER_RANK_9", visible.rank() == 9)
    trace = sp.Matrix([[1, 0, 0, 0, -1, 0, 0, -1, 0, -1]])
    check("FIRST_NULL_TRANSFER_HAS_ZERO_METRIC_TRACE", not any(trace * visible))
    qtransfer = sp.Matrix.hstack(*[a * metric_null for a in ad_generators])
    check("METRIC_NULL_FIRST_ADJOINT_SPAN_IS_FULL_36",
          sp.Matrix.hstack(metric_null, qtransfer).rank() == 36)

    # A deliberately predeclared local source direction: packed q23=1.
    z = sp.zeros(36, 1)
    z[10] = z[15] = 1  # C02=J13, C03=J12.
    target = sp.zeros(10, 1)
    target[8] = 1
    first = ad_generators[0] * z  # [K1,J13]=K3, [K1,J12]=K2.
    check("EXPLICIT_INITIAL_FULL_SOLDER_CURRENT_ZERO", not any(m * z))
    check("EXPLICIT_TRANSFER_STILL_SATISFIES_WARD", not any(av * first))
    check("EXPLICIT_TRANSFER_PACKED_Q23_EQUALS_ONE", d * first == target)

    # Coefficientwise finite boost identity: g=(I-a K1/2)^-1(I+a K1/2).
    # Clearing its denominator makes this an exact all-parameter identity.
    a = sp.Symbol("a", real=True)
    gnum = (4 - a*a) * I + 4*a*N.G[0] + 2*a*a*(N.G[0] @ N.G[0])
    finite = []
    for face in range(6):
        c = sum((F(z[6*face+j]) * N.G[j] for j in range(6)), ZERO.copy())
        moved = gnum @ c @ adj(gnum)
        finite.extend(moved[r, s] for r, s in N.PAIRS)
    finite = sp.Matrix(finite)
    denom = 4 - a*a
    expected = denom * ((4 + a*a)*z + 4*a*first)
    check("FINITE_ADJOINT_IDENTITY_ALL_COEFFICIENTS",
          all(sp.expand(x) == 0 for x in finite - expected))
    check("FINITE_TRANSFER_WARD_ZERO_ALL_COEFFICIENTS",
          all(sp.expand(x) == 0 for x in av * finite))
    check("FINITE_TRANSFER_SOURCE_ALL_COEFFICIENTS",
          all(sp.expand(x) == 0 for x in d * finite - 4*a*denom*target))

    # Transporting solder together with curvature preserves the zero current.
    g = cayley(F(1, 7), N.G[0])
    curves = [sum((F(z[6*f+j])*N.G[j] for j in range(6)), ZERO.copy())
              for f in range(6)]
    moved_curves = [ad(g, c) for c in curves]
    slots, _, h = R.tensor_memory(g, moved_curves)
    check("SIMULTANEOUS_LORENTZ_GAUGE_REMAINS_RESPONSE_NULL",
          not np.any(slots) and not np.any(h))
    # A role-coordinate change is an algebraic local carrier isomorphism.
    # It does not replace the four independent lattice shift operators.
    coframe_checks = 0
    for s in (
        np.diag([F(1), F(7, 6), F(5, 4), F(9, 8)]),
        np.array([[F(1), F(1, 7), F(1, 11), F(0)],
                  [F(0), F(1), F(1, 13), F(1, 17)],
                  [F(1, 19), F(0), F(1), F(1, 23)],
                  [F(1, 29), F(1, 31), F(0), F(1)]], dtype=object),
    ):
        si = sp.Matrix(N.inverse(s).tolist())
        det = sp.Matrix(s.tolist()).det()
        role = sp.Matrix([[si[r, a]*si[t, b] - si[t, a]*si[r, b]
                           for r, t in N.PAIRS] for a, b in N.PAIRS])
        carrier = sp.kronecker_product(role, sp.eye(6))
        _, _, vs, ms, ds, _, _ = R.face_data(s)
        ms, ds = sp.Matrix(ms.tolist()), sp.Matrix(ds.tolist())
        assert ms == det*sp.kronecker_product(sp.eye(4), si)*m*carrier
        assert sp.Matrix(vs.tolist())*ms == det*av*carrier
        for ag in ad_generators:
            assert carrier*ag == ag*carrier
        # Ten metric test matrices transform by S^-T q S^-1.
        metric_test = sp.zeros(10)
        for j, (a0, b0) in enumerate(N.SYM):
            dq = sp.zeros(4)
            dq[a0, b0] = dq[b0, a0] = 1
            moved = si.T*dq*si
            for k, (a1, b1) in enumerate(N.SYM):
                metric_test[j, k] = moved[a1, b1]
        assert metric_test.det() != 0
        assert ds == det*metric_test*d*carrier
        coframe_checks += 1
    check("LOCAL_ALL_COFRAME_ROLE_ISOMORPHISM", coframe_checks == 2)
    return {
        "solder_null_dimension": 20,
        "first_adjoint_span_dimension": 35,
        "second_adjoint_span_dimension": 36,
        "first_solder_transfer_rank": 15,
        "first_ward_rank": 6,
        "ward_preserving_source_transfer_rank": 9,
        "metric_null_first_adjoint_span_dimension": 36,
        "initial_curvature": {"02": "J13", "03": "J12"},
        "first_transported_curvature": {"02": "K3", "03": "K2"},
        "finite_packed_response": "4*a/(4-a^2) times unit q23",
        "nonidentity_coframe_coefficient_controls": coframe_checks,
        "all_coframe_extension": "exterior-square role isomorphism; no shift mixing",
        "scope": "local curvature carrier; shared-link stationarity not asserted",
    }


def lattice_current_check():
    shape = (2, 3, 2, 2)
    sites = list(product(*(range(n) for n in shape)))

    def shift(x, r, step=1):
        return tuple((v + (step if j == r else 0)) % shape[j]
                     for j, v in enumerate(x))

    links, solders, gauges = {}, {}, {}
    for x in sites:
        f = F(20 + sum(x), 20)
        s = np.diag([F(1), F(1), f, F(21, 20)]).astype(object)
        s[0, 2] = F(x[1] - 1, 23)
        solders[x] = s
        gauges[x] = cayley(F(sum(x)+1, 71), N.G[(sum(x)+3) % 6])
        for r in range(4):
            t = F((sum((j+1)*v for j, v in enumerate(x))+3*r) % 9 - 4, 53)
            generator = N.G[(sum(x)+r) % 6] + N.G[(sum(x)+r+2) % 6] / 3
            links[x, r] = cayley(t, generator)

    literal = {x: np.zeros((4, 6), dtype=object) for x in sites}
    h, slots, vertical = {}, {}, {}
    faces = {}
    for x in sites:
        q, _, vert, _, _, weights, _ = R.face_data(solders[x])
        curvatures = []
        for fi, (r, s) in enumerate(N.PAIRS):
            locations = ((x, r, False), (shift(x, r), s, False),
                         (shift(x, s), r, True), (x, s, True))
            factors = [adj(links[y, role]) if inv else links[y, role]
                       for y, role, inv in locations]
            prefix = [I]
            for f in factors:
                prefix.append(prefix[-1] @ f)
            suffix = [None]*5
            suffix[4] = I
            for j in range(3, -1, -1):
                suffix[j] = factors[j] @ suffix[j+1]
            p, w = prefix[4], weights[fi]
            pi = adj(p)
            c = (p - pi) / 2
            curvatures.append(c)
            faces[x, r, s] = (w, p)
            faces[x, s, r] = (-w, pi)
            # Independent direct differentiation of every underlying factor.
            for j, (y, role, inverse) in enumerate(locations):
                for k, g in enumerate(N.G):
                    df = -g @ factors[j] if inverse else factors[j] @ g
                    dp = prefix[j] @ df @ suffix[j+1]
                    dc = (dp + pi @ dp @ pi) / 2
                    literal[y][role, k] += pair(w, dc)
        slots[x], _, h[x] = R.tensor_memory(solders[x], curvatures)
        gs = gauges[x] @ solders[x]
        gslots, _, gh = R.tensor_memory(gs, [ad(gauges[x], c) for c in curvatures])
        assert np.array_equal(gslots, slots[x])
        assert np.array_equal(gh, adj(gauges[x]).T @ h[x])
        gauged_weights = R.face_data(gs)[5]
        for fi, (r, s) in enumerate(N.PAIRS):
            w, _ = faces[x, r, s]
            assert np.array_equal(gauged_weights[fi],
                                  adj(gauges[x]).T @ w @ gauges[x].T)
        vertical[x] = vert @ h[x].reshape(16)
        xi = np.zeros((4, 4), dtype=object)
        for val, (a, b) in zip(slots[x], N.SYM):
            xi[a, b] = xi[b, a] = val if a == b else val / 2
        a = N.inverse(q) @ solders[x].T @ h[x]
        gamma = (a - a.T) / 2
        assert np.array_equal(h[x], 2*ETA @ solders[x] @ xi
                              + ETA @ solders[x] @ gamma)

    transport_omission = 0
    odd_omission = 0
    current_rows = 0
    gauge_rows = 0
    for x in sites:
        for r in range(4):
            for g in N.G:
                actual = literal[x][r] @ coordinates(ad(adj(links[x, r]), g))
                da, do, ordinary = F(0), F(0), F(0)
                for s in range(4):
                    if s == r:
                        continue
                    y = shift(x, s, -1)
                    w, p = faces[x, r, s]
                    wy, py = faces[y, r, s]
                    _, _, ax, ox = momenta(w, p, g)
                    carried = ad(links[y, s], g)
                    _, _, ay, oy = momenta(wy, py, carried)
                    _, _, a0, o0 = momenta(wy, py, g)
                    da += ax - ay
                    do += ox + oy
                    ordinary += ax - a0 + ox + o0
                    # Reverse orientation: A antisymmetric, O symmetric.
                    ws, ps = faces[x, s, r]
                    _, _, ar, orev = momenta(ws, ps, g)
                    assert ar == -ax and orev == ox
                    # Covariance under independent local vertex gauges.
                    wxg = adj(gauges[x]).T @ w @ gauges[x].T
                    pxg = ad(gauges[x], p)
                    gxg = ad(gauges[x], g)
                    assert momenta(wxg, pxg, gxg) == momenta(w, p, g)
                    lg = gauges[y] @ links[y, s] @ adj(gauges[x])
                    assert np.array_equal(ad(lg, gxg), ad(gauges[y], carried))
                    gauge_rows += 1
                assert actual == da + do, (x, r, g, actual, da, do)
                transport_omission += actual != ordinary
                odd_omission += actual != da
                current_rows += 1
        # Local Lorentz Ward identity from the literal link derivatives.
        for k, g in enumerate(N.G):
            ward = vertical[x][k]
            face_odd = F(0)
            for r, s in N.PAIRS:
                face_odd += momenta(*faces[x, r, s], g)[3]
            assert vertical[x][k] == -2*face_odd
            for r in range(4):
                ward += literal[x][r] @ coordinates(ad(adj(links[x, r]), g))
                ward -= literal[shift(x, r, -1)][r, k]
            assert ward == 0
    check("ALL_ROLE_LITERAL_CURRENT_ROWS", current_rows == 24*len(sites))
    check("ALL_ROLE_LOCAL_LORENTZ_COVARIANCE", gauge_rows == 72*len(sites))
    check("LOCAL_WARD_AND_ODD_MOMENTUM_IDENTITY", True)
    check("EXACT_SOLDER_SOURCE_PLUS_VERTICAL_SPLIT", True)
    check("DELETING_ADJOINT_TRANSPORT_REJECTED", transport_omission > 0)
    check("DELETING_ODD_CURVATURE_MOMENTUM_REJECTED", odd_omission > 0)
    return {"shape": list(shape), "sites": len(sites),
            "literal_current_rows": current_rows,
            "gauge_covariance_rows": gauge_rows,
            "wrong_rows_without_transport": transport_omission,
            "wrong_rows_without_odd_momentum": odd_omission}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = {"input_head": INPUT_HEAD,
              "local_transport": local_transport_check(),
              "all_role_current": lattice_current_check(),
              "parent_status": "PARTIAL / OPEN"}
    path = Path(__file__).with_name("a4d_full_current_transport_quotient_results.json")
    if args.write:
        path.write_text(json.dumps(result, indent=2) + "\n")
    else:
        check("PINNED_EXACT_RESULT_MATCHES", json.loads(path.read_text()) == result)
    print("RESULT ALL_ROLE_CURRENT_AND_NULL_TO_VISIBLE_TRANSPORT_CERTIFIED", flush=True)
    print("RESULT FIXED_SOURCE_GLOBAL_RESPONSE_THEOREM_OPEN", flush=True)


if __name__ == "__main__":
    main()
