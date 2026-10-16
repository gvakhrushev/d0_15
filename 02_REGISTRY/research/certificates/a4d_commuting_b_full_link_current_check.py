#!/usr/bin/env python3
"""Literal full-link B currents, Lorentz Ward reduction and transport torque.

The all-period maximum principle and smooth-source estimate are proved in
A4D_COMMUTING_B_FULL_LINK_CURRENT_RIGIDITY.md. These exact finite controls
derive the face coefficients and replay every shared incidence independently
of a four-phase ansatz. No source is assigned from a tested candidate.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json

import numpy as np
import sympy as sp
import a4d_identity_quarter_nonlinear_response_check as N


INPUT_HEAD = "53450f234a2a48d7b5e6a6bd1715ba2dcbac35f3"
I = N.I
ETA = np.diag(N.SIG).astype(object)
B = N.G[0] + N.G[1] + N.G[2]
READOUT = np.array([0, 0, 0, 0, -1, 1, 1, -1, 1, -1], dtype=object)


def ck(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def adjoint(a):
    return ETA @ a.T @ ETA


def pair(w, a):
    return np.sum(w * a)


def cayley(a, generator=B):
    out = N.inverse(I - a * generator * F(1, 2)) @ (I + a * generator * F(1, 2))
    assert np.array_equal(out.T @ ETA @ out, ETA)
    return out


def face_weights(solder):
    """Derive Gram and vertical solder variations from the actual weights."""
    qi = N.inverse(solder.T @ ETA @ solder)
    lifts = []
    for r, s in N.SYM:
        dq = np.zeros((4, 4), dtype=object)
        dq[r, s] = dq[s, r] = 1
        ds = solder @ qi @ dq * F(1, 2)
        assert np.array_equal(ds.T @ ETA @ solder + solder.T @ ETA @ ds, dq)
        lifts.append(ds)
    variations = lifts + [g @ solder for g in N.G]
    weights, derivatives = [], []
    for r, s in N.PAIRS:
        u, v = [j for j in range(4) if j not in (r, s)]
        sign = N.orient(r, s)
        weights.append(sign * N.weight(N.wedge(solder[:, u], solder[:, v])))
        derivatives.append([
            sign * N.weight(N.wedge(ds[:, u], solder[:, v])
                            + N.wedge(solder[:, u], ds[:, v]))
            for ds in variations
        ])
    return np.array(weights), np.array(derivatives)


def local_constitutive_checks():
    ck("B_CUBED_3B", np.array_equal(B @ B @ B, 3 * B))
    weights, derivatives = face_weights(I)
    ck("INDEPENDENT_GRAM_LIFT_MATCHES_OWNER", np.array_equal(derivatives[:, :10], N.DWEIGHT))
    d = sp.Matrix([[pair(derivatives[f, j], B) for f in range(6)] for j in range(10)])
    v = sp.Matrix([[pair(derivatives[f, 10 + j], B) for f in range(6)] for j in range(6)])
    temporal = sp.Matrix([1, 1, 1, 0, 0, 0])
    spatial = sp.Matrix([0, 0, 0, 1, -1, 1])
    ck("FLAT_WARD_RANK_FOUR", v.rank() == 4)
    ck("FLAT_WARD_KERNEL_EXACTLY_TWO_CURRENTS", v * temporal == sp.zeros(6, 1)
       and v * spatial == sp.zeros(6, 1)
       and sp.Matrix.hstack(temporal, spatial).rank() == 2)
    ck("SPATIAL_CURRENT_RESPONSE_INVISIBLE", d * spatial == sp.zeros(10, 1))
    ck("STATIONARY_READOUT_ONE_SCALAR", d * temporal == sp.Matrix(READOUT))

    f = sp.Symbol("f", positive=True)
    solder = np.diag([1, 1, f, f]).astype(object)
    weights_f = []
    diag_d = sp.zeros(3, 6)
    for face, (r, s) in enumerate(N.PAIRS):
        u, v0 = [j for j in range(4) if j not in (r, s)]
        w = N.orient(r, s) * N.weight(N.wedge(solder[:, u], solder[:, v0]))
        weights_f.append(w)
        for row, leg in enumerate((1, 2, 3)):
            ds = np.zeros((4, 4), dtype=object)
            ds[leg, leg] = -sp.Rational(1, 2) / solder[leg, leg]
            dw = N.orient(r, s) * N.weight(N.wedge(ds[:, u], solder[:, v0])
                                           + N.wedge(solder[:, u], ds[:, v0]))
            diag_d[row, face] = sp.simplify(pair(dw, B))
    action = [sp.simplify(pair(w, B)) for w in weights_f]
    ck("WARP_ALL_SIX_FACE_WEIGHTS", action == [f**2, f, f, 0, 0, 0])
    ck("SPATIAL_B_CURVATURE_CANNOT_CHANGE_DIAGONAL_SOURCE", diag_d[:, 3:] == sp.zeros(3))
    tf = sp.Matrix([[f**-2, -1, -1], [-f**-1, f, -f], [-f**-1, -f, f]])
    ck("FULL_LINK_WARP_SOURCE_INVERSE", (tf * diag_d[:, :3] - sp.eye(3)).applyfunc(sp.simplify) == sp.zeros(3))
    ck("DIAGONAL_SOURCE_MAP_DETERMINANT", sp.simplify(diag_d[:, :3].det()) == -sp.Rational(1, 4))

    z, c = sp.symbols("z c", real=True)
    p = I + z * B + (c - 1) * (B @ B) / 3
    ck("FULL_FACE_ODD_CURVATURE", np.array_equal((p - adjoint(p)) / 2, z * B))
    for w in weights_f:
        ck("FULL_FACE_B_VARIATION", sp.expand(pair(w, B @ p) - c * pair(w, B)) == 0)
    lorentz = sp.Matrix(p @ adjoint(p) - I)
    ck("EVEN_ODD_CONSTITUTIVE_IDENTITY", all(
        sp.rem(sp.expand(e), c*c - 3*z*z - 1, c) == 0 for e in lorentz))
    return {"flat_Gram_map": [[str(x) for x in row] for row in d.tolist()],
            "flat_vertical_map": [[str(x) for x in row] for row in v.tolist()],
            "vertical_rank": 4, "readout_on_stationarity": list(map(int, READOUT)),
            "invisible_spatial_current": [0, 0, 0, 1, -1, 1],
            "warp_diagonal_map": [[str(x) for x in row] for row in diag_d.tolist()],
            "warp_action_weights": list(map(str, action))}


def lattice_replay(shape, *, warp=False, noncommuting=False):
    sites = list(product(*(range(n) for n in shape)))

    def shift(x, r, step=1):
        return tuple((a + (step if j == r else 0)) % shape[j] for j, a in enumerate(x))

    links = {}
    for x in sites:
        for r in range(4):
            a = F((sum((j + 2) * v for j, v in enumerate(x))
                   + 3 * r + x[0] * x[1]) % 11 - 5, 47)
            generator = (N.G[(sum(x) + r) % 6] + N.G[(sum(x) + r + 2) % 6] * F(1, 3)
                         if noncommuting else B)
            links[x, r] = cayley(a, generator)
    profile = (F(1), F(51, 50), F(26, 25), F(51, 50))
    cache = {f: face_weights(np.diag([F(1), F(1), f, f])) for f in (profile if warp else (F(1),))}
    data = {x: cache[profile[x[1]] if warp else F(1)] for x in sites}
    ek = {x: np.zeros((4, 6), dtype=object) for x in sites}
    eq = {x: np.zeros(10, dtype=object) for x in sites}
    vertical = {x: np.zeros(6, dtype=object) for x in sites}
    currents = {}
    constitutive = {}
    torque = {}
    for x in sites:
        weights, derivatives = data[x]
        for face, (r, s) in enumerate(N.PAIRS):
            locations = [(x, r, False), (shift(x, r), s, False),
                         (shift(x, s), r, True), (x, s, True)]
            factors = [adjoint(links[y, q]) if inv else links[y, q] for y, q, inv in locations]
            prefix = [I]
            for a in factors:
                prefix.append(prefix[-1] @ a)
            suffix = [None] * 5
            suffix[4] = I
            for i in range(3, -1, -1):
                suffix[i] = factors[i] @ suffix[i + 1]
            p = prefix[4]
            pi = adjoint(p)
            curvature = (p - pi) * F(1, 2)
            w = weights[face]
            assert pair(w, p) == pair(w, curvature)
            for j in range(10):
                eq[x][j] += pair(derivatives[face, j], curvature)
            for j in range(6):
                vertical[x][j] += pair(derivatives[face, 10 + j], curvature)
            for i, (y, q, inv) in enumerate(locations):
                co = suffix[i + 1] @ w.T @ prefix[i]
                derivative = -factors[i] @ co if inv else co @ factors[i]
                for g in range(6):
                    ek[y][q, g] += pair(derivative.T, N.G[g])
            if not noncommuting:
                z = curvature[0, 1]
                c = (np.trace(p) - 2) * F(1, 2)
                assert np.array_equal(curvature, z * B) and c >= 1 and c*c - 3*z*z == 1
                constitutive[x, r, s] = (z, c)
                currents[x, r, s] = pair(w, B @ p)
            if r == 0:
                def momentum(a):
                    return pair(w, (a @ p + pi @ a) * F(1, 2))
                l0 = links[x, 0]
                li = links[shift(x, 0), s]
                currents[x, "J", s] = momentum(l0 @ B @ adjoint(l0))
                torque[x, s] = momentum(l0 @ (B - li @ B @ adjoint(li)) @ adjoint(l0))

    def coordinates(a):
        assert np.array_equal(a + adjoint(a), np.zeros((4, 4), dtype=object))
        return np.array([a[r, s] for r, s in N.PAIRS], dtype=object)

    for x in sites:
        for g in range(6):
            ward = vertical[x][g]
            for r in range(4):
                a = adjoint(links[x, r]) @ N.G[g] @ links[x, r]
                ward += ek[x][r] @ coordinates(a) - ek[shift(x, r, -1)][r, g]
            assert ward == 0, ("Ward", x, g, ward)
    ck("LITERAL_LOCAL_LORENTZ_WARD_" + ("NONCOMMUTING" if noncommuting else "FULL_B"), True)
    mismatches_without_torque = 0
    for x in sites:
        actual = sum(ek[x][0, :3])
        divergence = sum(currents[x, "J", s] - currents[shift(x, s, -1), "J", s]
                         for s in (1, 2, 3))
        remainder = sum(torque[shift(x, s, -1), s] for s in (1, 2, 3))
        assert actual == divergence + remainder
        mismatches_without_torque += actual != divergence
    ck("FULL_NONCOMMUTING_CURRENT_PLUS_TORQUE", True)
    if noncommuting:
        ck("ORDINARY_DIVERGENCE_WITHOUT_TORQUE_REJECTED", mismatches_without_torque > 0)
    else:
        ck("ALL_SPATIAL_B_LINKS_HAVE_ZERO_TORQUE", not any(torque.values()))
        for x in sites:
            for r in range(4):
                prediction = F(0)
                for s in range(4):
                    if s == r:
                        continue
                    a, b = sorted((r, s))
                    sign = 1 if r < s else -1
                    prediction += sign * (currents[x, a, b] - currents[shift(x, s, -1), a, b])
                assert sum(ek[x][r, :3]) == prediction
            if warp:
                f = profile[x[1]]
                diag = np.array([eq[x][j] for j in (4, 7, 9)], dtype=object)
                tf = np.array([[f**-2, -1, -1], [-f**-1, f, -f], [-f**-1, -f, f]], dtype=object)
                assert np.array_equal(tf @ diag, np.array([constitutive[x, 0, s][0] for s in (1, 2, 3)]))
        ck("EVERY_ROLE_FULL_LINK_B_CURRENT_" + ("WARP" if warp else "FLAT"), True)
    return {"shape": list(shape), "sites": len(sites), "faces": 6 * len(sites),
            "warp": warp, "noncommuting": noncommuting,
            "spatial_links_nonidentity": sum(not np.array_equal(links[x, r], I) for x in sites for r in (1, 2, 3)),
            "nonzero_spatial_B_curvatures": (sum(constitutive[x, r, s][0] != 0 for x in sites
                                                for r, s in N.PAIRS if r != 0) if not noncommuting else None),
            "scalar_current_mismatches_when_torque_is_deleted": mismatches_without_torque}


def stationary_and_difference_controls():
    t = F(1, 7)
    u = cayley(t)
    links = np.array([[I.copy() for _ in range(4)] for _ in range(4)], dtype=object)
    links[0, 0] = u
    links[2, 0] = adjoint(u)
    ek, eq = N.euler_links(links[:, :, None])
    amplitude = 4 * t / (4 - 3 * t*t)
    expected = np.array([s * amplitude * READOUT for s in (1, 1, -1, -1)], dtype=object)
    ck("EXACT_STATIONARY_NONSMOOTH_RESPONSE_REMAINS_ALLOWED", not np.any(ek) and np.array_equal(eq[0], expected))
    ck("OWNER_COMPONENT_COUNT_SIX", sum(abs(x) for x in READOUT) == 6)
    # Periodic powers of the difference cannot kill a nonconstant sign cycle.
    ranks = []
    for length in (2, 3, 5, 8):
        d = sp.eye(length)
        for j in range(length):
            d[j, (j - 1) % length] -= 1
        for order in (1, 2, 5, 6):
            ck(f"PERIODIC_DIFFERENCE_KERNEL_N{length}_K{order}", (d**order).rank() == length - 1)
        epsilon = sp.Matrix([1] * (length - 1) + [-1])
        fifth = d**5 * epsilon
        ck(f"NONCONSTANT_SIGN_FIFTH_DIFFERENCE_N{length}", max(abs(x) for x in fifth) >= 2)
        ranks.append([length, length - 1])
    # The Euler projections alone do not replace the Ward gate: three
    # independently constant temporal even fluxes solve these projections.
    unequal = sp.Matrix([1, 2, 3, 0, 0, 0])
    _, derivatives = face_weights(I)
    vertical = sp.Matrix([[pair(derivatives[f, 10 + j], B) for f in range(6)] for j in range(6)])
    ck("UNEQUAL_CONSTANT_TEMPORAL_FLUXES_FAIL_FULL_WARD", vertical * unequal != sp.zeros(6, 1))
    # On an open path a nonconstant affine sequence has zero second difference.
    affine = sp.Matrix([0, 1, 2])
    first_open = sp.Matrix([[-1, 1, 0], [0, -1, 1]])
    second_open = sp.Matrix([[1, -2, 1]])
    ck("PERIODICITY_IS_ESSENTIAL", second_open * affine == sp.zeros(1, 1)
       and first_open * affine != sp.zeros(2, 1))
    return {"stationary_hostile_amplitude": str(amplitude), "stationary_hostile_signs": [1, 1, -1, -1],
            "readout_l1_factor": 6, "difference_kernel_ranks": ranks,
            "raw_normalized_bound": "h^-2 ||Xi||_owner1 <= 3 M_k h^(k-4), k>=1",
            "source_requirement": "predeclared samples with max_r ||partial_r^k tau_11||_infinity <= M_k"}


def run_checks():
    local = local_constitutive_checks()
    grids = [lattice_replay((2, 4, 2, 2)), lattice_replay((2, 4, 2, 2), warp=True),
             lattice_replay((2, 2, 2, 2), noncommuting=True)]
    controls = stationary_and_difference_controls()
    return {"schema": "a4d-commuting-b-full-link-current-v1", "input_head": INPUT_HEAD,
            "arithmetic": "exact Q plus coefficientwise symbolic f; literal four-factor face products",
            "local_constitutive_maps": local, "full_lattice_replays": grids, "controls": controls,
            "flat_theorem": "full E_K=0 implies Xi=z*m with |z| constant; uniformly C5 independent sources give raw normalized O(h)",
            "warped_theorem": "all four roles in exp(R B) retain ||E_K||_owner1 >= (102/625)L^3-90*M^2 for bounded diagonal sources",
            "general_current_identity": "E_K(x,0)[B]=sum_i D_i^- J_i(x)+sum_i T_i(x-e_i); T_i is the exact spatial adjoint-transport torque",
            "nonclaims": ["no unrestricted noncommuting source-image collapse", "no classification of the invisible spatial current",
                          "no change of action, source prescription, Lorentz quotient, selector or BOOK/CORE claims"],
            "verdict": "FULL-COMMUTING-B-SMOOTH-SOURCE-RIGIDITY; NONCOMMUTING-TRANSPORT-TORQUE-RETAINED"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expect", type=Path)
    args = parser.parse_args()
    report = run_checks()
    expected = args.expect or (Path(__file__).with_name("a4d_commuting_b_full_link_current_results.json")
                               if args.output is None else None)
    if expected:
        assert json.loads(expected.read_text()) == report
        print("PASS_PINNED_LEDGER", flush=True)
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    print("VERDICT", report["verdict"], flush=True)
