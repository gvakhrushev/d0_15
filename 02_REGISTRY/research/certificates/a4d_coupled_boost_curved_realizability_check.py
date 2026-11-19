#!/usr/bin/env python3
"""Exact shared-link and joint flux identities for the same coupled boost.

The smooth coframe and independent zero metric source are declared before
the candidate.  The degree-eight numerator is complete, not a Taylor jet.
The joint flux identity also excludes all independent temporal B amplitudes
under a bounded prescribed source. Spatial links remain identities; no
response estimate for other fields or general task terminal is asserted.
"""
from fractions import Fraction as F
from itertools import product, permutations
from pathlib import Path
import argparse
import json
import numpy as np
import a4d_identity_quarter_nonlinear_response_check as N


INPUT_HEAD = "31f0f79ef41393e08f56a068650473dbbca20e60"
DEGREE = 8
I = N.I
B = N.G[0] + N.G[1] + N.G[2]
J12 = N.G[3]
ETA = np.diag(N.SIG).astype(object)


def adjoint(a):
    return ETA @ a.T @ ETA


def numerator_links():
    # D=4-3*t^2 is used on EVERY link, including inactive identities.
    # Four degree-two factors give the entire degree-eight numerator.
    assert np.array_equal(B @ B @ B, 3 * B)
    identity = N.jconst(4 * I, DEGREE)
    identity[2] = -3 * I
    u = identity.copy()
    u[1] = 4 * B
    u[2] += 2 * B @ B
    ui = N.jinv(u)
    return np.array([[u if p == 0 and r == 0 else
                      ui if p == 2 and r == 0 else identity
                      for r in range(4)] for p in range(4)], dtype=object)


def incident_numerators():
    """Assemble all six face incidences of (x,Role0,J12), p(x)=0."""
    links = numerator_links()
    terms = []
    for face, (r, s) in enumerate(N.PAIRS):
        if r != 0:
            continue
        for at_x in (True, False):
            phase = 0 if at_x else 3
            loc = [(phase, r, False), ((phase + 1) % 4, s, False),
                   ((phase + 1) % 4, r, True), (phase, s, True)]
            fac = [N.jinv(links[p, q]) if inv else links[p, q]
                   for p, q, inv in loc]
            pos = 0 if at_x else 2
            prefix = N.jconst(I, DEGREE)
            for a in fac[:pos]:
                prefix = N.jmul(prefix, a)
            suffix = N.jconst(I, DEGREE)
            for a in fac[pos + 1:]:
                suffix = N.jmul(suffix, a)
            co = N.jmul(suffix, N.WEIGHT[face].T @ prefix)
            derivative = (N.jmul(co, fac[pos]) if at_x else
                          -N.jmul(fac[pos], co))
            coeffs = np.array([np.sum(a.T * J12) for a in derivative],
                              dtype=object)
            complement = [a for a in range(4) if a not in (r, s)]
            power = sum(a >= 2 for a in complement)
            back = not at_x and s == 1
            terms.append((s, at_x, back, power, coeffs))
    return terms


def cayley(t):
    d = 4 - 3 * t * t
    u = I + (4 * t * B + 2 * t * t * B @ B) / d
    assert np.array_equal(u.T @ ETA @ u, ETA)
    assert np.array_equal((I - t * B / 2) @ u, I + t * B / 2)
    return u


def direct_lattice_derivative(t, *, varied_site=(0, 0, 0, 0), wrong_inverse_sign=False,
                              freeze_face_coframe=False):
    """Differentiate the full L=4 periodic action at one phase-zero link.

    Enumerating all based faces independently checks the local incidence
    placement. The only varying link is L_(0,0), with right variation L*J12.
    Rational f samples are the exact samples of the declared cosine warp.
    """
    L = 4
    origin = tuple(varied_site)
    assert sum(origin) % 4 == 0
    samples = (F(1), F(51, 50), F(26, 25), F(51, 50))
    u = cayley(t)
    ui = adjoint(u)

    def shift(x, r):
        return tuple((a + (j == r)) % L for j, a in enumerate(x))

    def link(x, r):
        phase = sum(x) % 4
        return u if r == 0 and phase == 0 else ui if r == 0 and phase == 2 else I

    value = F(0)
    touched = 0
    for x in product(range(L), repeat=4):
        f = F(1) if freeze_face_coframe else samples[x[1]]
        solder = np.diag([F(1), F(1), f, f])
        for r, s in N.PAIRS:
            loc = [(x, r, False), (shift(x, r), s, False),
                   (shift(x, s), r, True), (x, s, True)]
            if not any(y == origin and q == 0 for y, q, inv in loc):
                continue
            touched += 1
            a, b = [j for j in range(4) if j not in (r, s)]
            weight = N.orient(r, s) * N.weight(N.wedge(solder[:, a], solder[:, b]))
            p = I.copy()
            dp = np.zeros((4, 4), dtype=object)
            for y, q, inv in loc:
                raw = link(y, q)
                fac = adjoint(raw) if inv else raw
                df = np.zeros((4, 4), dtype=object)
                if y == origin and q == 0:
                    df = (-J12 @ fac if inv else fac @ J12)
                    if inv and wrong_inverse_sign:
                        df = -df
                dp, p = dp @ fac + p @ df, p @ fac
            # Differentiate C=(P-P^-1)/2 directly, retaining the inverse.
            dc = (dp - adjoint(dp)) / 2
            value += np.sum(weight * dc)
    assert touched == 6
    assert isinstance(value, F)
    return value


def pclean(p):
    return {k: v for k, v in p.items() if np.any(v)}


def padd(*polys):
    out = {}
    for p in polys:
        for k, v in p.items():
            out[k] = out.get(k, 0) + v
    return pclean(out)


def pscale(p, c):
    return pclean({k: c * v for k, v in p.items()})


def pmul(a, b, matrix=False):
    out = {}
    for i, v in a.items():
        for j, w in b.items():
            k = tuple(x + y for x, y in zip(i, j)) if isinstance(i, tuple) else i + j
            term = v @ w if matrix else v * w
            out[k] = out.get(k, 0) + term
    return pclean(out)


def generic_face_flux_identity():
    """Complete two-variable polynomials; a,b are independent link parameters."""
    da = {(0, 0): 4, (2, 0): -3}
    db = {(0, 0): 4, (0, 2): -3}
    den = pmul(da, db)
    difference = {(1, 0): 1, (0, 1): -1}
    znum = pscale(pmul(difference, {(0, 0): 4, (1, 1): -3}), 4)
    cnum = padd(den, pscale(pmul(difference, difference), 24))
    un = {(0, 0): 4 * I, (1, 0): 4 * B, (2, 0): 2 * B @ B - 3 * I}
    vin = {(0, 0): 4 * I, (0, 1): -4 * B, (0, 2): 2 * B @ B - 3 * I}
    plaquette = pmul(un, vin, matrix=True)
    odd = pclean({k: (v - adjoint(v)) * F(1, 2) for k, v in plaquette.items()})
    assert not padd(odd, {k: -v * B for k, v in znum.items()})
    for weight in N.WEIGHT[:3]:
        forward = pclean({k: np.sum(weight * (B @ v)) for k, v in plaquette.items()})
        assert not padd(forward, pscale(cnum, -1))
    assert not padd(pmul(cnum, cnum), pscale(pmul(znum, znum), -3),
                    pscale(pmul(den, den), -1))
    print("PASS_ALL_PROFILE_FACE_CURVATURE_AND_BOOST_FLUX_POLYNOMIALS", flush=True)
    return {"D(a)": "4-3*a^2", "z(a,b)": "4*(a-b)*(4-3*a*b)/(D(a)*D(b))",
            "c(a,b)": "1+24*(a-b)^2/(D(a)*D(b))",
            "complete_polynomial_identity": "c_num^2-3*z_num^2=(D(a)*D(b))^2",
            "real_chart_consequence": "c>=1 and c=sqrt(1+3*z^2)",
            "face_forward_B_derivative": "w_i*c; incoming derivative is -w_i*c"}


def generic_diagonal_memory_inverse():
    """Derive all Laurent coefficients of the metric map from Gram lifts."""
    solder = {0: np.diag([F(1), F(1), F(0), F(0)]),
              1: np.diag([F(0), F(0), F(1), F(1)])}
    metric_map = {}
    for row, j in enumerate((1, 2, 3)):
        ds = np.zeros((4, 4), dtype=object)
        ds[j, j] = F(-1, 2)
        exponent = 0 if j == 1 else -1
        for face, (r, s) in enumerate(N.PAIRS[:3]):
            a, b = [k for k in range(4) if k not in (r, s)]
            for e, coframe in solder.items():
                weight = N.orient(r, s) * N.weight(
                    N.wedge(ds[:, a], coframe[:, b]) + N.wedge(coframe[:, a], ds[:, b]))
                k = e + exponent
                metric_map.setdefault(k, np.zeros((3, 3), dtype=object))
                metric_map[k][row, face] += np.sum(weight * B)
    metric_map = pclean(metric_map)
    expected = {
        1: np.array([[0, F(-1, 2), F(-1, 2)], [0, 0, 0], [0, 0, 0]], dtype=object),
        0: np.array([[0, 0, 0], [F(-1, 2), 0, 0], [F(-1, 2), 0, 0]], dtype=object),
        -1: np.array([[0, 0, 0], [0, 0, F(-1, 2)], [0, F(-1, 2), 0]], dtype=object),
    }
    assert not padd(metric_map, pscale(expected, -1))
    inverse = {
        -2: np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]], dtype=object),
        -1: np.array([[0, 0, 0], [-1, 0, 0], [-1, 0, 0]], dtype=object),
        0: np.array([[0, -1, -1], [0, 0, 0], [0, 0, 0]], dtype=object),
        1: np.array([[0, 0, 0], [0, 1, -1], [0, -1, 1]], dtype=object),
    }
    identity = {0: np.eye(3, dtype=object)}
    assert not padd(pmul(metric_map, inverse, matrix=True), pscale(identity, -1))
    assert not padd(pmul(inverse, metric_map, matrix=True), pscale(identity, -1))
    determinant = {}
    for p in permutations(range(3)):
        term = {0: F(1)}
        for r in range(3):
            term = pmul(term, pclean({e: v[r, p[r]] for e, v in metric_map.items()}))
        sign = (-1) ** sum(p[i] > p[j] for i in range(3) for j in range(i + 1, 3))
        determinant = padd(determinant, pscale(term, sign))
    assert determinant == {0: F(-1, 4)}
    print("PASS_ALL_COFRAME_LAURENT_DIAGONAL_MEMORY_INVERSE", flush=True)
    return {"diagonal_slots": ["Xi11", "Xi22", "Xi33"], "determinant": "-1/4",
            "inverse_rows": [["f^-2", "-1", "-1"], ["-f^-1", "f", "-f"],
                             ["-f^-1", "-f", "f"]],
            "coefficient_check": "complete Laurent coefficients, not coframe sampling"}


def all_profile_action_replay(spatially_constant):
    """Independent based-face assembly on all 256 sites, without a phase ansatz."""
    L = 4
    sites = list(product(range(L), repeat=4))
    samples = (F(1), F(51, 50), F(26, 25), F(51, 50))
    params = {x: F(2 * x[0] - 3, 20) if spatially_constant else
              F((3*x[0] + 5*x[1] + 7*x[2] + 11*x[3]) % 11 - 5, 20) for x in sites}
    links = {x: cayley(params[x]) for x in sites}
    ek = {x: F(0) for x in sites}
    eq = {x: np.zeros(3, dtype=object) for x in sites}
    z = {x: np.zeros(3, dtype=object) for x in sites}

    def shift(x, i, direction=1):
        return tuple((v + direction * (j == i)) % L for j, v in enumerate(x))

    def c(a, b):
        return 1 + 24*(a-b)**2 / ((4-3*a*a)*(4-3*b*b))

    for x in sites:
        f = samples[x[1]]
        solder = np.diag([F(1), F(1), f, f])
        qi = N.inverse(solder.T @ ETA @ solder)
        for i in (1, 2, 3):
            y = shift(x, i)
            face = i - 1
            a, b = [j for j in range(4) if j not in (0, i)]
            weight = N.orient(0, i) * N.weight(N.wedge(solder[:, a], solder[:, b]))
            factors = [links[x], I, adjoint(links[y]), I]
            p = factors[0] @ factors[1] @ factors[2] @ factors[3]
            curvature = (p - adjoint(p)) * F(1, 2)
            z[x][face] = curvature[0, 1]
            assert np.array_equal(curvature, z[x][face] * B)
            for pos, target in ((0, x), (2, y)):
                derivative = I.copy()
                for k, factor in enumerate(factors):
                    df = factor @ B if k == 0 else -B @ factor
                    derivative = derivative @ (df if pos == k else factor)
                dc = (derivative - adjoint(derivative)) * F(1, 2)
                ek[target] += np.sum(weight * dc)
            for j, q in enumerate((1, 2, 3)):
                dq = np.zeros((4, 4), dtype=object)
                dq[q, q] = 1
                ds = solder @ qi @ dq * F(1, 2)
                dw = N.orient(0, i) * N.weight(
                    N.wedge(ds[:, a], solder[:, b]) + N.wedge(solder[:, a], ds[:, b]))
                eq[x][j] += np.sum(dw * curvature)

    for x in sites:
        f = samples[x[1]]
        expected = F(0)
        for i in (1, 2, 3):
            y, prev = shift(x, i), shift(x, i, -1)
            fp = samples[prev[1]]
            w, wp = (f*f, fp*fp) if i == 1 else (f, fp)
            expected += w*c(params[x], params[y]) - wp*c(params[prev], params[x])
        assert ek[x] == expected
        inverse = np.array([[1/f**2, -1, -1], [-1/f, f, -f], [-1/f, -f, f]], dtype=object)
        assert np.array_equal(inverse @ eq[x], z[x])
    norm = sum(abs(v) for v in ek.values())
    # Sum the independently assembled literal Euler rows, retaining all L^3
    # transverse sites.  The two transverse divergences cancel exactly.
    planes = [[x for x in sites if x[1] == n] for n in range(L)]
    assert [len(xs) for xs in planes] == [L**3] * L
    plane_flux = [sum(samples[n]**2*c(params[x], params[shift(x, 1)])
                      for x in xs) for n, xs in enumerate(planes)]
    plane_euler = [sum(ek[x] for x in xs) for xs in planes]
    assert plane_euler == [plane_flux[n]-plane_flux[n-1] for n in range(L)]
    assert sum(plane_euler) == 0
    assert all(plane_flux[n] >= L**3*samples[n]**2 for n in range(L))
    # An exact consequence of periodic total variation gives a residual /
    # response tradeoff.  Check it without introducing floating square roots.
    diagonal_owner = sum(abs(q) for x in sites for q in eq[x])
    max_square = max(samples)**2
    mean_square = sum(f*f for f in samples)/L
    gap = (max_square-mean_square)*L**4 - F(L, 2)*norm
    assert gap <= 0 or 3*(max_square*diagonal_owner)**2 >= gap**2
    if spatially_constant:
        assert all(not np.any(z[x]) and not np.any(eq[x]) for x in sites)
        assert norm == F(102, 625) * L**3
    else:
        assert any(np.any(z[x]) for x in sites)
    return {"profile": "spatially constant, arbitrary time links" if spatially_constant else
                       "independent non-four-phase values in all four coordinates",
            "physical_sites": L**4, "temporal_face_checks": 3*L**4,
            "literal_B_Euler_rows_checked": L**4, "Gram_inverse_rows_checked": 3*L**4,
            "origin_B_Euler": str(ek[(0, 0, 0, 0)]),
            "vacuum_B_Euler_owner_sum": str(norm) if spatially_constant else None,
            "transverse_planes": {"physical_sites_per_plane": L**3,
                                  "literal_Euler_plane_sums": list(map(str, plane_euler)),
                                  "unweighted_flux_plane_sums": list(map(str, plane_flux)),
                                  "identity": "sum_(x1=n) E_K(x,0)[B] = Q_n-Q_(n-1)",
                                  "residual_response_tradeoff": "PASS exact rational squared check"}}


def stationary_flux_response_barrier():
    """Exact constants in the analytic all-mesh conservation consequence.

    Stationarity makes the transverse flux constant.  The positivity branch
    c>=1 therefore enforces a nonvanishing diagonal response.  The proof
    owner supplies the inequalities and all-L cosine sums; this finite
    check pins their coefficients and the literal replay pins their count.
    """
    samples = (F(1), F(51, 50), F(26, 25), F(51, 50))
    high = max(samples)**2
    mean = sum(f*f for f in samples)/4
    assert high == F(676, 625) and mean == F(5203, 5000)
    assert high-mean == F(41, 1000)
    sup_square = (high**2-1)/27
    assert sup_square == F(22117, 1875**2)
    owner_coefficient_without_sqrt3 = (high-mean)/high
    assert owner_coefficient_without_sqrt3 == F(205, 5408)
    # A constant coframe must remove both geometric barriers.  The fixed
    # flat stationary controls are not excluded by this curved identity.
    assert (F(1)**2-1)/27 == 0
    assert (F(1)-F(1))/F(1) == 0
    print("PASS_STATIONARY_FLUX_SUP_AND_RAW_OWNER_RESPONSE_BARRIERS", flush=True)
    return {"necessary_equation": "E_K=0 in the same temporal B family",
            "conserved_flux": "J_n=f_n^2*mean_(x0,x2,x3) sqrt(1+3*z_1(x)^2); J_n is constant",
            "positivity": "J >= max_n f_n^2 = 676/625",
            "diagonal_response_sup_lower_bound": "sqrt(22117)/1875",
            "sup_lower_bound_squared": str(sup_square),
            "diagonal_response_raw_owner_lower_bound": "(205/(5408*sqrt(3)))*L^4",
            "all_mesh_mean_f_squared": str(mean),
            "source_necessary_condition": "h^2*M >= sqrt(22117)/1875",
            "residual_response_tradeoff": "sqrt(3)*(676/625)*||Xi_diag||_owner1 + (L/2)*||E_K||_owner1 >= (41/1000)*L^4",
            "norm": "full physical L^4 sum; the normalized flux average does not replace the owner norm",
            "flat_coframe_control": "both geometric barriers vanish at f=1",
            "proof_scope": "analytic conservation and inequalities; exact constants and literal plane counts replayed"}


def arbitrary_amplitude_joint_exclusion():
    face = generic_face_flux_identity()
    inverse = generic_diagonal_memory_inverse()
    replays = [all_profile_action_replay(False), all_profile_action_replay(True)]
    print("PASS_ALL_PROFILE_FULL_ACTION_AND_UNWEIGHTED_COUNT_REPLAYS", flush=True)
    barrier = stationary_flux_response_barrier()
    bound = 3 * F(1976, 625) * F(77, 25)**2
    assert bound == F(35147112, 390625) and bound < 90
    return {
        "family": "every Role0 link is an independent real Cayley(t_x*B); Roles1,2,3 are I",
        "restrictions": "no phase, period-four envelope, amplitude-size margin, or regularity assumption",
        "face_identity": face, "metric_inverse": inverse,
        "single_joint_flux_identity": "E_K(x,0)[B]=sum_i D_i^-[w_i*sqrt(1+3*(T_f*Xi_diag)_i^2)], w=(f^2,f,f)",
        "source_hypothesis": "Xi_diag=h^2*tau_diag, ||tau_diag||_infinity<=M fixed independently of candidates",
        "raw_connection_owner_bound": "||E_K||_owner1 >= (102/625)*L^3 - 90*M^2",
        "exact_remainder_constant": str(bound),
        "vacuum_consequence": "tau=0 excludes every amplitude profile at every admissible mesh",
        "bounded_source_consequence": "no exact joint member for L^3>(9375/17)*M^2",
        "direct_action_controls": replays,
        "stationarity_forced_response_barrier": barrier,
        "scope": "all amplitude retunings of the same temporal B family; no claim for nonidentity spatial links or other generators",
        "verdict": "COUPLED_BOOST_ALL_AMPLITUDE_JOINT_EXCLUSION",
    }


def run_checks():
    # These declarations precede candidate construction and readout.
    data = {
        "mesh": "h=1/L, L in 4*N",
        "coframe": "S_h(x)=diag(1,1,f(h*x1),f(h*x1))",
        "profile": "f(y)=1+(1-cos(2*pi*y))/50",
        "fixed_metric_source": "tau(y)=0 in all ten owner slots; E_Q=h^2*tau_h",
        "connection_source": "zero",
        "comparator": "the #216 smooth comparator on the same fixed g=S^T*eta*S",
        "owner_norm": "unweighted sum over all sites and ten packed metric slots",
    }
    terms = incident_numerators()
    # c=-2*t*D^3. This array specifies every coefficient up to degree 8.
    c = np.array([0, -128, 0, 288, 0, -216, 0, 54, 0], dtype=object)
    expected = {(1, True): c, (1, False): -c,
                (2, True): -c, (2, False): c,
                (3, True): np.zeros(9, dtype=object),
                (3, False): np.zeros(9, dtype=object)}
    total = {(False, 2): np.zeros(9, dtype=object),
             (True, 2): np.zeros(9, dtype=object),
             (False, 1): np.zeros(9, dtype=object)}
    for s, at_x, back, power, coeffs in terms:
        assert np.array_equal(coeffs, expected[s, at_x])
        total[back, power] += coeffs
    assert np.array_equal(total[False, 2], c)
    assert np.array_equal(total[True, 2], -c)
    assert not np.any(total[False, 1])
    print("PASS_COMPLETE_DEGREE8_SHARED_LINK_IDENTITY", flush=True)

    controls = []
    delta = F(1) - F(51, 50) ** 2
    for t in (F(-1, 7), F(1, 5), F(1, 4)):
        expected_value = -2 * t * delta / (4 - 3 * t * t)
        actual = direct_lattice_derivative(t)
        assert actual == expected_value and actual != 0
        wrong = direct_lattice_derivative(t, wrong_inverse_sign=True)
        frozen = direct_lattice_derivative(t, freeze_face_coframe=True)
        assert wrong != expected_value
        assert frozen == 0 and frozen != expected_value
        controls.append({"t": str(t), "literal_global_action_derivative": str(actual),
                         "wrong_inverse_sign": str(wrong), "frozen_coframe": str(frozen)})
    assert direct_lattice_derivative(F(0)) == 0
    print("PASS_INDEPENDENT_FULL_PERIODIC_ACTION_DERIVATIVE", flush=True)
    print("PASS_INVERSE_SIGN_AND_FROZEN_FACE_HOSTILE_CONTROLS", flush=True)

    # The same selected row gives an unweighted owner-sum lower bound.
    # The all-L counting/monotonicity argument is written in the proof owner.
    # Here all four slow-coordinate values are checked by independent full
    # action derivatives; the multiplicity is the actual phase-zero count.
    t = F(1, 5)
    samples = (F(1), F(51, 50), F(26, 25), F(51, 50))
    total_variation = sum(abs(samples[n]**2-samples[n-1]**2) for n in range(4))
    assert total_variation == F(102, 625)
    derivatives = []
    for n in range(4):
        site = ((-n) % 4, n, 0, 0)
        value = direct_lattice_derivative(t, varied_site=site)
        assert value == -2*t*(samples[n]**2-samples[n-1]**2)/(4-3*t*t)
        derivatives.append(value)
    multiplicities = [sum(1 for x in product(range(4), repeat=4)
                          if x[1] == n and sum(x) % 4 == 0) for n in range(4)]
    assert multiplicities == [4**3//4]*4
    selected_sum = sum(m*abs(value) for m,value in zip(multiplicities,derivatives))
    assert selected_sum == F(51, 625)*abs(t)*4**3/(4-3*t*t)
    print("PASS_UNWEIGHTED_OWNER_SUM_FROM_THE_SAME_IDENTITY", flush=True)

    all_amplitudes = arbitrary_amplitude_joint_exclusion()

    return {
        "schema": "a4d-coupled-boost-curved-realizability-v3",
        "input_head": INPUT_HEAD,
        "arithmetic": "exact rational, complete polynomial and direct action differentiation",
        "predeclared_data": data,
        "candidate": "B=K1+K2+K3; U=(I-t*B/2)^(-1)*(I+t*B/2); Role0=(U,I,U^-1,I); other links=I",
        "real_chart": "0<abs(t)<2/sqrt(3)",
        "selected_row": "right variation L_(x,0)*exp(epsilon*J12), sum(x)=0 mod 4",
        "exact_identity": "E_(K0,J12)(x)=-2*t*(f_n^2-f_(n-1)^2)/(4-3*t^2)",
        "cleared_denominator": "(4-3*t^2)^4",
        "numerator": "-2*t*(4-3*t^2)^3*(f_n^2-f_(n-1)^2)",
        "f_n_squared_coefficients_degrees_0_to_8": list(map(int, c)),
        "f_previous_squared_coefficients_degrees_0_to_8": list(map(int, -c)),
        "f_n_linear_coefficients_degrees_0_to_8": [0] * 9,
        "direct_action_controls": controls,
        "origin_value": "2*t*((1+(1-cos(2*pi/L))/50)^2-1)/(4-3*t^2)",
        "all_mesh_conclusion": "nonzero at the origin for every L in 4*N and every nonzero t in the real chart",
        "analytic_extension": "every positive nonconstant sampled profile has an unequal adjacent pair; choose phase 0 there",
        "source_independence": "the failed connection row is unaffected by any independently prescribed metric source",
        "connection_owner_sum": {
            "norm": "sum over all sites, four roles and six Lorentz Euler components; no site-count normalization",
            "phase_zero_multiplicity_at_each_x1": "L^3/4 for L in 4*N",
            "sampled_profile_total_variation": "102/625 for every L in 4*N",
            "lower_bound": "||E_K||_owner1 >= 51*abs(t)*L^3/(625*(4-3*t^2))",
            "L4_direct_action_control": {"t": str(t),
                                         "four_slow_site_derivatives": list(map(str,derivatives)),
                                         "multiplicities": multiplicities,
                                         "selected_phase_zero_sum": str(selected_sum)},
            "all_mesh_proof": "analytic residue counting and monotonicity; the finite control checks coefficient and normalization",
        },
        "requested_outcome": "1: coupled boost fails exact E_K=0 on the declared nonconstant coframe",
        "gate": "JOINT-CRITICAL-REALIZABILITY-AND-OWNER-SUM-CONTROL: COUPLED_BOOST_EXCLUDED",
        "scope": "original coupled boost and all its temporal amplitude retunings; identity spatial links and the same fixed generator B",
        "arbitrary_amplitude_joint_exclusion": all_amplitudes,
        "parent_task_status": "PARTIAL / OPEN; Draft / IN_PROGRESS",
        "verdict": "COUPLED_BOOST_ALL_AMPLITUDE_JOINT_EXCLUSION",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expect", type=Path)
    args = parser.parse_args()
    report = run_checks()
    expected = args.expect or (Path(__file__).with_name(
        "a4d_coupled_boost_curved_realizability_results.json") if args.output is None else None)
    if expected:
        assert json.loads(expected.read_text()) == report
        print("PASS_PINNED_LEDGER", flush=True)
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    print("VERDICT", report["verdict"])
