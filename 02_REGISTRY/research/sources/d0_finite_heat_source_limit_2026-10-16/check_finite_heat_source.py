#!/usr/bin/env python3
"""Bounded checks for SAME-finite-operator clock/source approximation.

The scalar inequalities are analytical statements, checked here on rational
boundary/interior fixtures with certified exponential enclosures.  A separate
full16 high-precision finite difference checks trace functional calculus and
moving observer adjoint/normalizers.  The tiny variable-coefficient lattice
checks the exact CAR-square/commutator algebra, not a continuum heat limit.
No predecessor check entrypoint is imported or executed.
"""
from __future__ import annotations

import ast
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import mpmath as mp
import sympy as s


ROOT = Path(__file__).resolve().parents[4]
CAR_PATH = "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py"
CAR_SHA256 = "bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da"


class Checks:
    def __init__(self):
        self.groups = Counter()

    def require(self, condition, group, name):
        if not bool(condition):
            raise AssertionError(group+":"+name)
        self.groups[group] += 1


def owned_creators(repo, checks):
    data = (repo/CAR_PATH).read_bytes()
    checks.require(hashlib.sha256(data).hexdigest() == CAR_SHA256,
                   "source", "literal_full16_CAR_owner")
    tree = ast.parse(data.decode("utf-8"))
    fn = next(x for x in tree.body if isinstance(x, ast.FunctionDef)
              and x.name == "creator")
    fn.decorator_list = []
    namespace = {"s": s, "EXTERIOR_ORDER": (0, 2, 3, 1)}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn], type_ignores=[])),
                 CAR_PATH, "exec"), namespace)
    return [s.SparseMatrix(namespace["creator"](r)) for r in range(4)]


def exp_minus_enclosure(x, terms=100):
    """Exact rational enclosure: inverse of positive exp Taylor bounds."""
    x = F(x)
    if x < 0 or x >= terms+2:
        raise ValueError("positive_exponential_enclosure_domain")
    term = F(1)
    total = term
    for n in range(1, terms+1):
        term *= x/n
        total += term
    next_term = term*x/(terms+1)
    upper = total+next_term/(1-x/F(terms+2))
    return 1/upper, 1/total


def scalar_checks(checks):
    fixtures = [(2, F(1, 5), F(0)), (2, F(1, 5), F(1, 10)),
                (2, F(1, 5), F(1)), (2, F(1, 5), F(8, 5)),
                (3, F(2, 5), F(9, 5)), (8, F(1, 4), F(6)),
                (16, F(3, 4), F(4)), (31, F(1, 3), F(7, 3))]
    for m, b0, t in fixtures:
        b = 1-t/m
        checks.require(m >= 2 and 0 < b0 <= b <= 1,
                       "scalar_exact", "admitted_rational_window")
        lo, hi = exp_minus_enclosure(t)
        hlo, _ = exp_minus_enclosure(t/2)
        k, p = b**m, b**(m-1)
        if not t:
            checks.require(lo == hi == k == p == 1,
                           "scalar_exact", "zero_mode_retained")
            continue
        checks.require(lo >= k, "scalar_exact", "clock_below_heat")
        checks.require(hi-k <= t*t*lo/(2*m*b0),
                       "scalar_exact", "value_error_bound")
        err = max(abs(p-lo), abs(p-hi))
        checks.require(err <= hlo*(t+t*t/(2*b0))/m,
                       "scalar_exact", "derivative_half_heat_bound")
        checks.require(err <= lo*(t/b0+t*t/(2*b0*b0))/m,
                       "scalar_exact", "derivative_same_heat_bound")
        z = F(2, 7)
        a = 1-z
        # E/F(E) is increasing, so endpoint enclosures are sufficient.
        target = p/(a+z*k)
        feedback_err = max(abs(target-lo/(a+z*lo)),
                           abs(target-hi/(a+z*hi)))
        checks.require(feedback_err <= hlo*(t/a+t*t/(2*b0*a*a))/m,
                       "scalar_exact", "feedback_derivative_bound")
    return {"rational_fixtures": len(fixtures),
            "exponential_enclosure_terms": 100,
            "includes_zero_and_B_equals_b0": True}


def comm(a, b):
    return a*b-b*a


def discrete_checks(c, checks):
    eye16 = s.eye(16)
    for a in range(4):
        for b in range(4):
            checks.require(c[a]*c[b].T+c[b].T*c[a] == int(a == b)*eye16,
                           "CAR_exact", "creation_contraction")
            checks.require(c[a]*c[b]+c[b]*c[a] == s.zeros(16),
                           "CAR_exact", "creation_creation")
    checks.require((c[0]*c[2]*c[3]*c[1])[15, 0] != 0,
                   "CAR_exact", "top_grade_retained")
    sites = [(x, y) for x in range(2) for y in range(2)]
    shifts = [s.SparseMatrix(4, 4, lambda i, j: int(
        sites[j] == ((sites[i][0]+int(r == 0)) % 2,
                     (sites[i][1]+int(r == 1)) % 2))) for r in range(2)]
    shifts += [s.eye(4), s.eye(4)]
    h = s.Rational(1, 2)
    derivative = {eps: [(shifts[r]**eps-s.eye(4))/(eps*h)
                        for r in range(4)] for eps in (-1, 1)}
    u = []
    for x, y in sites:
        u.append(s.Matrix([[1+s.Rational(x, 10), s.Rational(y, 11),
                            s.Rational(x+y, 13), 0],
                           [s.Rational(x, 17), 1+s.Rational(y, 19), 0,
                            s.Rational(x-y, 23)],
                           [0, 0, 1, 0], [0, 0, 0, 1]]))
    checks.require(all(v.det() > 0 for v in u),
                   "lattice_exact", "pointwise_invertible_coframe")
    coeff = [[s.diag(*[v[r, a] for v in u]) for a in range(4)]
             for r in range(4)]
    zero4 = s.zeros(4)
    p = {eps: [sum((coeff[r][a]*derivative[eps][r] for r in range(4)), zero4)
               for a in range(4)] for eps in (-1, 1)}
    b = [sum((s.diag(*(derivative[-1][r]*s.Matrix([v[r, a] for v in u])))
              *shifts[r].T for r in range(4)), zero4) for a in range(4)]
    for a in range(4):
        checks.require(p[1][a].T == -p[-1][a]-b[a],
                       "lattice_exact", "full_coefficient_adjoint")
    checks.require(any(b[a] != zero4 for a in range(4)),
                   "hostile_exact", "frozen_adjoint_coefficient_detected")
    for eps in (-1, 1):
        for delta in (-1, 1):
            rhs = s.zeros(4)
            for r in range(4):
                for q in range(4):
                    dr, dq = derivative[eps][r], derivative[delta][q]
                    ur, vq = coeff[r][0], coeff[q][1]
                    drv = s.diag(*(dr*s.Matrix([v[q, 1] for v in u])))
                    dqu = s.diag(*(dq*s.Matrix([v[r, 0] for v in u])))
                    rhs += h*(eps*ur*drv-delta*vq*dqu)*dr*dq+ur*drv*dq-vq*dqu*dr
            checks.require(comm(p[eps][0], p[delta][1]) == rhs,
                           "lattice_exact", "mixed_difference_commutator")
    nonzero_pb = False
    for r in range(2):
        for q in range(2):
            ur = coeff[r][1]
            gv = derivative[-1][q]*s.Matrix([v[q, 1] for v in u])
            g = s.diag(*gv)
            dg = s.diag(*(derivative[1][r]*gv))
            du = s.diag(*(derivative[-1][q]*s.Matrix([v[r, 1] for v in u])))
            lhs = comm(ur*derivative[1][r], g*shifts[q].T)
            rhs = h*(ur*dg+g*du)*derivative[1][r]*shifts[q].T+ur*dg*shifts[q].T
            checks.require(lhs == rhs, "lattice_exact", "P_B_coefficient_difference")
            nonzero_pb = nonzero_pb or lhs != zero4
    checks.require(nonzero_pb, "hostile_exact", "P_B_not_vacuous")
    kron = lambda a, z: s.SparseMatrix(s.kronecker_product(a, z))
    d = sum((kron(p[1][a], c[a]) for a in range(4)), s.zeros(64))
    d = s.SparseMatrix(d)
    big_d = d+d.T
    principal = sum((kron(p[1][a].T*p[1][a], eye16) for a in range(4)), s.zeros(64))
    mixed = sum((kron(comm(p[1][a], p[1][b_].T), c[a]*c[b_].T)
                 for a in range(4) for b_ in range(4)), s.zeros(64))
    cc = sum((kron(comm(p[1][a], p[1][b_]), c[a]*c[b_])
              for a in range(4) for b_ in range(a+1, 4)), s.zeros(64))
    ii = sum((kron(comm(p[1][a].T, p[1][b_].T), c[a].T*c[b_].T)
              for a in range(4) for b_ in range(a+1, 4)), s.zeros(64))
    checks.require(big_d*big_d == principal+mixed+cc+ii,
                   "lattice_exact", "full16_CAR_square_all_commutators")
    checks.require(mixed != s.zeros(64) and cc+ii != s.zeros(64),
                   "hostile_exact", "wrong_commutator_signs_detected")
    # C0 observer variation cannot bound the WHOLE commutator graph norm.
    boost = s.zeros(4)
    boost[0, 1] = boost[1, 0] = -1
    k = sum((boost[a, b_]*c[a]*c[b_].T for a in range(4)
             for b_ in range(4)), s.zeros(16))
    rough_k = kron(s.diag(1, 1, -1, -1), k)
    constant = s.kronecker_product(s.ones(4, 1), s.eye(16)[:, 1])
    flat = kron(derivative[1][0], c[0])
    rough = comm(rough_k, flat)*constant
    checks.require(rough != s.zeros(64, 1),
                   "hostile_exact", "rough_observer_commutator_not_zero")
    checks.require((2*rough).dot(2*rough) == 4*rough.dot(rough),
                   "hostile_exact", "observer_commutator_scales_as_inverse_mesh")
    return {"sites": 4, "exterior_dimension": 16, "matrix_dimension": 64,
            "square_terms": "Ta*Ta + CaIb[Ta,Tb*] + CaCb[Ta,Tb] + IaIb[Ta*,Tb*]"}


def mp_matrix(a):
    return mp.matrix([[mp.mpf(int(s.numer(a[i, j])))/int(s.denom(a[i, j]))
                       for j in range(a.cols)] for i in range(a.rows)])


def trace(a):
    return sum(a[i, i] for i in range(a.rows))


def exterior(a):
    out = s.zeros(16)
    subsets = [[r for r in range(4) if mask & (1 << r)] for mask in range(16)]
    # CAR owner's exterior order is A,C,D,B, not numeric mask order.
    order = (0, 2, 3, 1)
    subsets = [[r for r in order if mask & (1 << r)] for mask in range(16)]
    for i, rows in enumerate(subsets):
        for j, cols in enumerate(subsets):
            if len(rows) == len(cols):
                out[i, j] = a.extract(rows, cols).det() if rows else 1
    return out


def full16_source_checks(c, checks):
    with mp.workdps(80):
        n = [c[a]*c[a].T for a in range(4)]
        original = (c[0]/9+c[1]/11+c[2]/13+c[3]/15+c[0]*n[1]/17+c[2]*n[3]/19)/4
        variation = (c[1]*n[0]-c[3]*n[2])/25+c[0]/33
        l0 = s.eye(4)
        l0[0, 0] = l0[1, 1] = s.Rational(5, 4)
        l0[0, 1] = l0[1, 0] = -s.Rational(3, 4)
        eta = s.diag(1, -1, -1, -1)
        observer = s.Matrix([s.Rational(5, 4), s.Rational(3, 4), 0, 0])
        checks.require(l0.T*l0 == -eta+2*(eta*observer)*(eta*observer).T,
                       "source_exact", "literal_timelike_observer_pairing")
        i0 = exterior(l0)
        boost = s.zeros(4)
        boost[0, 1] = boost[1, 0] = -1
        k = sum((boost[a, b]*c[a]*c[b].T for a in range(4)
                 for b in range(4)), s.zeros(16))
        d = i0*original*i0.inv()
        v = i0*variation*i0.inv()
        dd = v+comm(k, d)
        big_d, dbig_d = d+d.T, dd+dd.T
        delta = big_d*big_d
        jet = big_d*dbig_d+dbig_d*big_d
        checks.require(comm(delta, jet) != s.zeros(16),
                       "hostile_exact", "spectral_variation_noncommuting")
        checks.require(dd != v, "hostile_exact", "moving_observer_adjoint_detected")
        beta, m, mass, z = s.Rational(3, 5), 7, s.Rational(2, 7), s.Rational(1, 9)
        alpha, b0 = beta/m, s.Rational(1, 10)
        eye = s.eye(16)
        b = eye-alpha*delta
        checks.require(max(sum(abs(delta[i, j]) for j in range(16)) for i in range(16))
                       *alpha < 1-b0, "source_exact", "full_B_positive_window")
        clock, p = b**m, b**(m-1)
        zk = s.trace(clock)
        fk = (1-z)*eye+z*clock
        dhk = -s.trace(p*jet)/zk
        djk = mass*z*beta*s.trace(fk.inv()*p*jet)
        # Independent full-time program evaluation, not a spectral-jet replay.
        om, vm, im, km = map(mp_matrix, (original, variation, i0, k))
        dm, jm = mp_matrix(delta), mp_matrix(jet)
        bm, mm, zm = mp.mpf(3)/5, mp.mpf(2)/7, mp.mpf(1)/9
        al = bm/m
        psi = mp.matrix([mp.mpf(r+1)/17 for r in range(16)])
        dpsi = mp.matrix([mp.mpf((-1)**r*(r+2))/29 for r in range(16)])
        w, dw = im*psi, km*im*psi+im*dpsi
        norm = (w.T*w)[0]
        dnorm = 2*(w.T*dw)[0]
        r0 = (w.T*dm*w)[0]/norm
        dr = (w.T*jm*w)[0]/norm+2*(dw.T*(dm-r0*mp.eye(16))*w)[0]/norm
        frozen_n = (w.T*jm*w)[0]/norm+2*(dw.T*dm*w)[0]/norm
        checks.require(abs(dnorm) > mp.mpf("1e-4") and abs(dr-frozen_n) > mp.mpf("1e-6"),
                       "hostile_highprecision", "matter_normalizer_not_frozen")
        def program(t):
            it = mp.expm(t*km)*im
            dt = it*(om+t*vm)*(it**-1)
            dt = dt+dt.T
            de = dt*dt
            bt = mp.eye(16)-al*de
            kt = bt**m
            et = mp.expm(-bm*de)
            wt = it*(psi+t*dpsi)
            rt = (wt.T*de*wt)[0]/(wt.T*wt)[0]
            hk = mp.log(mp.mpf(5)/3*trace(kt))/bm
            he = mp.log(mp.mpf(5)/3*trace(et))/bm
            jk = -mm*mp.log(mp.det((1-zm)*mp.eye(16)+zm*kt))
            je = -mm*mp.log(mp.det((1-zm)*mp.eye(16)+zm*et))
            return hk, jk, he, je, rt
        step = mp.mpf("1e-18")
        plus, minus = program(step), program(-step)
        fd = [(x-y)/(2*step) for x, y in zip(plus, minus)]
        heat = mp.expm(-bm*dm)
        ze = trace(heat)
        fe = (1-zm)*mp.eye(16)+zm*heat
        dhe = -trace(heat*jm)/ze
        dje = mm*zm*bm*trace((fe**-1)*heat*jm)
        exact_dhk = mp_matrix(s.Matrix([dhk]))[0]
        exact_djk = mp_matrix(s.Matrix([djk]))[0]
        for name, got, expected in zip(("clock_H", "clock_J", "ordinary_H", "ordinary_J", "moving_R"),
                                       fd, (exact_dhk, exact_djk, dhe, dje, dr)):
            checks.require(abs(got-expected) < mp.mpf("1e-30")*max(1, abs(expected)),
                           "source_highprecision", name+"_independent_time_derivative")
        pk = mp_matrix(p)
        zkm = mp_matrix(s.Matrix([zk]))[0]
        # d(Tr K/Tr K) includes BOTH nonzero terms, total zero.
        dzk = -bm*trace(pk*jm)
        checks.require(abs(dzk) > mp.mpf("1e-5"),
                       "hostile_highprecision", "global_Z_jet_nonzero")
        checks.require(abs(dzk/zkm-zkm*dzk/zkm**2) < mp.mpf("1e-70"),
                       "source_highprecision", "normalized_trace_jet_zero")
        checks.require(abs(dzk/zkm) > mp.mpf("1e-6"),
                       "hostile_highprecision", "omitted_global_normalizer_detected")
        frozen_dd = v+v.T
        frozen_jet = mp_matrix(big_d*frozen_dd+frozen_dd*big_d)
        checks.require(abs(-trace(pk*frozen_jet)/zkm-exact_dhk) > mp.mpf("1e-8"),
                       "hostile_highprecision", "omitted_observer_commutator_detected")
        # ||H0^-1 jet H0^-1|| <= ||jet||_F, without commuting assumptions.
        ell = mp.sqrt(trace(jm*jm))
        def moment(j, at, weighted=False):
            f = mp.expm(-at*dm)
            out = dm**j*f
            return trace((mp.eye(16)+dm)*out) if weighted else trace(out)
        b0m, am = mp.mpf(1)/10, 1-zm
        m2 = moment(2, bm)
        hbound = ell/(m*zkm)*(bm*moment(1, bm/2, True)
                  +bm**2*moment(2, bm/2, True)/(2*b0m)
                  +bm**2*m2*moment(0, bm, True)/(2*b0m*ze))
        jbound = ell*mm*zm*bm/m*(bm*moment(1, bm/2, True)/am
                  +bm**2*moment(2, bm/2, True)/(2*b0m*am**2))
        checks.require(abs(exact_dhk-dhe) <= hbound,
                       "source_highprecision", "full_H_source_bound")
        checks.require(abs(exact_djk-dje) <= jbound,
                       "source_highprecision", "full_J_source_bound")
        base = program(mp.mpf(0))
        value_bound = bm**2*m2/(2*m*b0m)
        checks.require(0 < ze-zkm <= value_bound,
                       "source_highprecision", "full_trace_value_bound")
        checks.require(0 < base[2]-base[0] <= value_bound/(bm*zkm),
                       "source_highprecision", "full_H_value_bound")
        checks.require(0 < base[1]-base[3] <= mm*zm*value_bound/am,
                       "source_highprecision", "full_J_value_bound")
        checks.require(abs((fd[0]+fd[1]+fd[4])-(fd[2]+fd[3]+fd[4])
                           -(exact_dhk+exact_djk-dhe-dje)) < mp.mpf("1e-30"),
                       "source_highprecision", "same_actual_R_source_cancels")
        return {"matrix_dimension": 16, "reference_fixture": "all16 raw amplitudes retained",
                "precision_decimal_digits": 80, "finite_difference_step": "1e-18",
                "noncommuting_Delta_jet": True, "moving_Lorentz_observer_pairing": True,
                "beta": "3/5", "m": m, "b0": "1/10"}


def run(repo=None):
    repo = Path(repo) if repo is not None else ROOT
    checks = Checks()
    c = owned_creators(repo, checks)
    scalar = scalar_checks(checks)
    lattice = discrete_checks(c, checks)
    source = full16_source_checks(c, checks)
    highprecision = sum(n for group, n in checks.groups.items() if "highprecision" in group)
    return {"status": "PASS", "exact_checks": sum(checks.groups.values())-highprecision,
            "highprecision_checks": highprecision, "total_checks": sum(checks.groups.values()),
            "check_groups": dict(sorted(checks.groups.items())),
            "source_pins": {CAR_PATH: CAR_SHA256},
            "scalar": scalar, "lattice": lattice, "source_fixture": source,
            "scope": {"same_finite_Delta_only": True, "all16_exterior_components": True,
                      "no_commuting_variation_assumption": True,
                      "rational_scalar_fixtures_are_not_all_t_proof": True,
                      "highprecision_source_is_a_fixture_not_interval_certificate": True,
                      "full_observer_operator_graph_bound_from_C0_is_claimed": False,
                      "continuum_heat_or_source_limit_is_proved": False,
                      "native_preparation_or_physical_admission_is_proved": False,
                      "predecessor_check_entrypoints_executed": False}}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
