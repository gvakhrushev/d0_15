#!/usr/bin/env python3
"""Exact parallel-path/raw-link cotangent coefficient conversion, not a norm limit.

Only the pinned native full16 creator definition is executed.  All tests below
are new algebraic jet tests; no old run(), compiler, or spectral suite is used.
"""
from __future__ import annotations

import ast
from collections import Counter
import hashlib
import json
from pathlib import Path

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
CAR_PATH = "02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py"
CAR_SHA = "bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da"
EDGE_PATH = "02_REGISTRY/research/certificates/a4d_native_joint_adjoint_source.py"
EDGE_SHA = "71ba142e284974db57d67c91a77ccd08a7e4f9759e8fc8daef7c5938774c0b28"


class Checks:
    def __init__(self):
        self.groups = Counter()

    def require(self, condition, group, label):
        if not bool(condition):
            raise AssertionError(group+":"+label)
        self.groups[group] += 1

    def equal(self, left, right, group, label):
        if isinstance(left, s.MatrixBase):
            value = (left-right).applyfunc(s.cancel)
            self.require(value == s.zeros(*left.shape), group, label)
        else:
            self.require(s.cancel(left-right) == 0, group, label)


def comm(a, b):
    return a*b-b*a


def covariant_derivative(value, omega, coordinate):
    return value.diff(coordinate)+comm(omega, value)


def cotangent_derivative(value, omega, coordinate, weight=1, pairing="trace"):
    """Adjoint for the NAMED real trace or positive Hilbert--Schmidt pairing."""
    density = s.diff(weight, coordinate)/weight
    if pairing == "trace":
        return -value.diff(coordinate)-comm(omega, value)-density*value
    if pairing == "hilbert_schmidt":
        return -value.diff(coordinate)+comm(omega.T, value)-density*value
    raise ValueError("unknown_cotangent_pairing")


def inverse_cotangent_coefficients(j0, j1, j2, omega, coordinate,
                                   weight=1, pairing="trace", omega1=None,
                                   log_weight1=0):
    """ell coefficients through h².  Optional omega_h/weight_h first jets.

    omega1 and log_weight1 mean omega_h=omega+h*omega1+..., and
    log(weight_h)=log(weight)+h*log_weight1+....  They are NOT x derivatives.
    """
    star = lambda value: cotangent_derivative(value, omega, coordinate, weight, pairing)
    ell1 = j1-star(j0)/2
    ell2 = j2-star(j1)/2+star(star(j0))/12
    if omega1 is not None:
        first = (-comm(omega1, j0) if pairing == "trace"
                 else comm(omega1.T, j0))
        first -= s.diff(log_weight1, coordinate)*j0
        ell2 -= first/2
    elif log_weight1 != 0:
        ell2 += s.diff(log_weight1, coordinate)*j0/2
    return j0, ell1, ell2


def polynomial_product(left, right, degree):
    size = left[0].rows
    return [sum((left[k]*right[n-k] for k in range(n+1)), s.zeros(size))
            for n in range(degree+1)]


def inverse_series(values):
    size = values[0].rows
    result = [s.eye(size)]
    for n in range(1, len(values)):
        result.append(-sum((values[k]*result[n-k] for k in range(1, n+1)),
                           s.zeros(size)))
    return result


def owned_creators(repo, checks):
    for path, digest in ((CAR_PATH, CAR_SHA), (EDGE_PATH, EDGE_SHA)):
        data = (repo/path).read_bytes()
        checks.require(hashlib.sha256(data).hexdigest() == digest,
                       "source", "native_definition_pin")
    tree = ast.parse((repo/CAR_PATH).read_text())
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                and n.name == "creator")
    node.decorator_list = []
    scope = {"s": s, "EXTERIOR_ORDER": (0, 2, 3, 1)}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[])),
                 CAR_PATH, "exec"), scope)
    return [scope["creator"](r) for r in range(4)]


def run(repo=None):
    repo = Path(repo) if repo is not None else ROOT
    checks = Checks()
    c = owned_creators(repo, checks)
    x, eps = s.symbols("x eps", real=True)
    eta = s.diag(1, -1, -1, -1)
    basis = lambda a, b: s.eye(4)[:, a]*s.eye(4)[b, :]
    boost01 = basis(0, 1)+basis(1, 0)
    boost02 = basis(0, 2)+basis(2, 0)
    rotation12 = basis(1, 2)-basis(2, 1)
    rotation23 = basis(2, 3)-basis(3, 2)
    omega = (1+x)*boost01+x*x*rotation12+x**3*boost02/3
    variation = (1-x*x)**3*((1-x)*rotation12+(2+x)*boost02+x*x*rotation23)
    for value in (omega, variation):
        checks.equal(value.T*eta+eta*value, s.zeros(4), "path", "actual_Lorentz_Lie_algebra")
    checks.require(comm(omega, variation) != s.zeros(4), "hostile", "noncommuting_path_jet")
    checks.require(omega.diff(x) != s.zeros(4) and variation.diff(x) != s.zeros(4),
                   "hostile", "both_endpoints_really_move")
    moved = omega+eps*variation
    path = [s.eye(4)]
    for n in range(3):
        path.append((path[-1].diff(x)+moved*path[-1])/(n+1))
    base = [value.subs(eps, 0) for value in path]
    jet = [value.diff(eps).subs(eps, 0) for value in path]
    checks.equal(base[1], omega, "path", "first_coefficient")
    checks.equal(base[2], (omega.diff(x)+omega*omega)/2,
                 "path", "second_coefficient_with_endpoint")
    checks.equal(base[3], (omega.diff(x, 2)+omega.diff(x)*omega
                 +2*omega*omega.diff(x)+omega**3)/6,
                 "path", "third_coefficient_with_noncommuting_order")
    inverse = inverse_series(base)
    product = polynomial_product(base, inverse, 3)
    for n in range(4):
        checks.equal(product[n], s.eye(4) if n == 0 else s.zeros(4),
                     "path", "actual_inverse_series")
        metric = sum((base[k].T*eta*base[n-k] for k in range(n+1)), s.zeros(4))
        checks.equal(metric, eta if n == 0 else s.zeros(4),
                     "path", "proper_Lorentz_transport_metric_jet")
    xi = polynomial_product(jet, inverse, 3)[1:]
    lvar = covariant_derivative(variation, omega, x)
    l2var = covariant_derivative(lvar, omega, x)
    for got, expected in zip(xi, (variation, lvar/2, l2var/6)):
        checks.equal(got, expected, "path", "left_trivialized_raw_link_jet")
    reversed_jet = polynomial_product(inverse, jet, 3)[1:]
    checks.require((reversed_jet[1]-xi[1]).applyfunc(s.cancel) != s.zeros(4),
                   "hostile", "wrong_left_right_trivialization_detected")
    frozen = [s.eye(4), moved, moved**2/2, moved**3/6]
    frozen_base = [v.subs(eps, 0) for v in frozen]
    frozen_jet = [v.diff(eps).subs(eps, 0) for v in frozen]
    frozen_xi = polynomial_product(frozen_jet, inverse_series(frozen_base), 3)[1:]
    checks.require((frozen_xi[1]-xi[1]).applyfunc(s.cancel) != s.zeros(4),
                   "hostile", "frozen_endpoint_detected")
    gamma = lambda value: sum((value[a, b]*c[a]*c[b].T for a in range(4)
                               for b in range(4)), s.zeros(16))
    checks.equal(gamma(lvar), gamma(variation).diff(x)+comm(gamma(omega), gamma(variation)),
                 "full16", "actual_exterior_representation_covariant_jet")
    checks.equal(gamma(comm(omega, variation)), comm(gamma(omega), gamma(variation)),
                 "full16", "all_grades_Lie_functor")
    checks.require(gamma(variation).shape == (16, 16), "full16", "no_exterior_truncation")
    # Cotangent reconstruction with a genuinely nonconstant positive weight.
    weight = (2+x)**2
    ell = [(1+x*x)*boost02+(2-x)*rotation12,
           (1-x)*boost01+x*rotation23,
           (1+x)*rotation12+x*x*boost02]
    for pairing in ("trace", "hilbert_schmidt"):
        star = lambda value: cotangent_derivative(value, omega, x, weight, pairing)
        j = [ell[0], ell[1]+star(ell[0])/2,
             ell[2]+star(ell[1])/2+star(star(ell[0]))/6]
        restored = inverse_cotangent_coefficients(*j, omega, x, weight, pairing)
        for got, expected in zip(restored, ell):
            checks.equal(got, expected, "cotangent", pairing+"_inverse_coefficients")
        wrong2 = j[2]-star(j[1])/2+star(star(j[0]))/6
        checks.require((wrong2-ell[2]).applyfunc(s.cancel) != s.zeros(4),
                       "hostile", pairing+"_one_sixth_is_not_one_twelfth")
        pair = (lambda a, b: s.trace(a*b)) if pairing == "trace" else (
                lambda a, b: s.trace(a.T*b))
        for n in range(3):
            lhs = sum((pair(ell[n-k], xi[k]) for k in range(n+1)), 0)
            integrand = s.cancel(weight*(lhs-pair(j[n], variation)))
            checks.equal(s.integrate(integrand, (x, -1, 1)), 0,
                         "cotangent", pairing+"_integrated_actual_path_source")
        no_density = cotangent_derivative(ell[0], omega, x, 1, pairing)
        checks.require((star(ell[0])-no_density).applyfunc(s.cancel) != s.zeros(4),
                       "hostile", pairing+"_moving_density_channel_detected")
        omega1 = (1+x)*rotation23
        log_weight1 = x*x/3
        first_star = (-comm(omega1, ell[0]) if pairing == "trace" else comm(omega1.T, ell[0]))
        first_star -= s.diff(log_weight1, x)*ell[0]
        moving_j2 = j[2]+first_star/2
        restored = inverse_cotangent_coefficients(j[0], j[1], moving_j2,
                omega, x, weight, pairing, omega1, log_weight1)
        checks.equal(restored[2], ell[2], "cotangent", pairing+"_moving_h_background")
        fixed_wrong = inverse_cotangent_coefficients(j[0], j[1], moving_j2,
                                                       omega, x, weight, pairing)[2]
        checks.require((fixed_wrong-ell[2]).applyfunc(s.cancel) != s.zeros(4),
                       "hostile", pairing+"_frozen_h_background_detected")
    checks.require((cotangent_derivative(ell[0], omega, x, 1, "trace")
                    -cotangent_derivative(ell[0], omega, x, 1, "hilbert_schmidt"))
                   .applyfunc(s.cancel) != s.zeros(4),
                   "hostile", "boost_HS_adjoint_is_not_invariant_trace_adjoint")
    tau = s.symbols("tau", real=True)
    checks.equal(s.integrate(s.exp(2*s.pi*s.I*tau), (tau, 0, 1)), 0,
                 "scope", "averaging_map_not_globally_invertible")
    return {"status": "PASS", "exact_checks": sum(checks.groups.values()),
            "check_groups": dict(sorted(checks.groups.items())),
            "source_pins": {CAR_PATH: CAR_SHA, EDGE_PATH: EDGE_SHA},
            "carrier": {"Lorentz_vector_dimension": 4, "exterior_dimension": 16},
            "jet_convention": "coefficients of h^j, no factorial in ell_j/j_j",
            "inverse_second_coefficient": "1/12",
            "scope": {"fixed_or_explicitly_moving_smooth_background_jets": True,
                      "nonconstant_noncommuting_proper_parallel_transport": True,
                      "all_native_spatial_link_slots_apply_edgewise": True,
                      "all_grid_C0_inverse_or_remainder_is_proved": False,
                      "physical_link_law_or_native_admission_is_selected": False,
                      "old_check_entrypoints_executed": False}}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
