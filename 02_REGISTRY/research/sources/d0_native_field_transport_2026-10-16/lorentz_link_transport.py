"""Positive polar part of an ACTUAL constrained Lorentz pull link.

D maps target vectors to source vectors: D.T*g_source*D=g_target.
The pairing observers u come from the full CAR reading; they are not
identified with the record/engine's first-grade axis.  The invariant below
is a diagnostic, not a selected physical action or a new transition law.
Only pinned owner definitions are consumed, never their check entrypoints.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import sys

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
NATIVE_PATH = "02_REGISTRY/research/sources/d0_lorentz_reflection_source_2026-10-16/native_current.py"
NATIVE_SHA256 = "d9282fad2124f57addeeeece96e34ba017a041d63002f37f0c2e990661f175c3"
ETA = s.diag(1, -1, -1, -1)


def require(condition: object, label: str) -> None:
    if not bool(condition):
        raise AssertionError(label)


def native_owner(repo: Path):
    require(hashlib.sha256((repo/NATIVE_PATH).read_bytes()).hexdigest() == NATIVE_SHA256,
            "native_full_current_source_pin")
    name = "lorentz_link_owned_native_current_definitions"
    spec = importlib.util.spec_from_file_location(name, repo/NATIVE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("native_current_definitions_unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def unit_current_jet(g, J, dg, dJ):
    """Timelike normalization with every metric/current denominator term."""
    kappa = (J.T*g*J)[0]
    dkappa = (J.T*dg*J+2*J.T*g*dJ)[0]
    return J/s.sqrt(kappa), dJ/s.sqrt(kappa)-J*dkappa/(2*kappa**s.Rational(3, 2))


def polar_link(D, h_source, h_target, positive_root=None):
    """D=R*B.  Caller supplies positive pairings and, optionally, exact B.

    M is h_target-selfadjoint positive; B is its principal square root.
    Supplying an already certified exact root avoids repeated diagonalization.
    """
    M = h_target.inv()*D.T*h_source*D
    B = M**s.Rational(1, 2) if positive_root is None else positive_root
    R = D*B.inv()
    return M, B, R


def square_root_jet(B, dM):
    """Unique full Sylvester derivative B*dB+dB*B=dM, no frozen eigenbasis."""
    d = B.rows
    operator = s.kronecker_product(B, s.eye(d))+s.kronecker_product(s.eye(d), B.T)
    row_major = operator.inv()*s.Matrix(list(dM))
    return s.Matrix(d, d, list(row_major))


def polar_link_jet(D, dD, hs, dhs, ht, dht, B):
    M = ht.inv()*D.T*hs*D
    dM = -ht.inv()*dht*M+ht.inv()*(dD.T*hs*D+D.T*dhs*D+D.T*hs*dD)
    dB = square_root_jet(B, dM)
    R = D*B.inv()
    dR = dD*B.inv()-R*dB*B.inv()
    return M, dM, dB, dR


def observer_overlap_jet(gs, us, ut, D, dgs, dus, dut, dD):
    """c_pair and dc_pair, independent of the record-axis selection rule."""
    c = (us.T*gs*D*ut)[0]
    dc = (dus.T*gs*D*ut+us.T*dgs*D*ut+
          us.T*gs*dD*ut+us.T*gs*D*dut)[0]
    return c, dc


def exterior_trace_jet(c, dc, density_ratio=1, density_ratio_jet=0):
    """Tr[(Lambda D)^sharp Lambda D]=16*zeta*c^2 on the constrained domain.

    zeta=omega_source/omega_target when site densities are part of W.
    This is a diagnostic source; it is not identified with H, J or R.
    """
    return (16*density_ratio*c*c,
            16*density_ratio_jet*c*c+32*density_ratio*c*dc)


def run(repo: Path | None = None) -> dict:
    repo = ROOT if repo is None else Path(repo).resolve()
    native = native_owner(repo)
    data = native.native_data(repo)  # definitions/state only, not run_checks
    C = data["C"]
    ext, dcompound = C.C.ext, C.C.dcompound
    checks = []

    def eq(actual, expected, label):
        difference = actual-expected
        values = list(difference) if isinstance(difference, s.MatrixBase) else [difference]
        require(all(s.simplify(C.red(value)) == 0 for value in values), label)
        checks.append(label)

    e0, I = s.eye(4)[:, 0], s.eye(4)
    D = s.eye(4)
    D[:2, :2] = s.Matrix([[s.Rational(5, 4), s.Rational(3, 4)],
                          [s.Rational(3, 4), s.Rational(5, 4)]])
    hs = native.reflection(ETA, e0)
    ht = native.reflection(ETA, e0)
    eq(D.T*ETA*D, ETA, "actual_covariant_Lorentz_pull_constraint")
    eq(D.det(), 1, "proper_rational_boost_no_metric_update")
    M, B, R = polar_link(D, hs, ht, positive_root=D)
    eq(B*B, M, "supplied_positive_root_actual_link_M")
    require(B.eigenvals() == {s.Integer(2): 1, s.Rational(1, 2): 1, s.Integer(1): 2},
            "root_is_positive_not_an_arbitrary_Lorentz_factor")
    checks.append("root_is_positive_not_an_arbitrary_Lorentz_factor")
    eq(B.T*ETA*B, ETA, "positive_polar_part_is_true_Lorentz_boost")
    eq(R, I, "unitarization_removes_entire_actual_boost_here")
    eq(R.T*ETA*R, ETA, "unitary_polar_part_preserves_Lorentz_form")
    eq(R.T*hs*R, ht, "unitary_polar_part_preserves_positive_pairing")
    c, _dc = observer_overlap_jet(ETA, e0, e0, D, s.zeros(4), s.zeros(4, 1), s.zeros(4, 1), s.zeros(4))
    eq(c, s.Rational(5, 4), "actual_observer_pair_overlap")
    fullD, fullM = ext(D), ext(M)
    eq(fullD.T*ext(hs)*fullD, ext(ht)*fullM, "all16_actual_exterior_link_Gram")
    expected_spectrum = {s.Integer(4): 4, s.Rational(1, 4): 4, s.Integer(1): 8}
    require(fullM.eigenvals() == expected_spectrum, "full16_squared_singular_values_all_grades")
    checks.append("full16_squared_singular_values_all_grades")
    eq(s.trace(fullM), (I+M).det(), "full_exterior_trace_is_four_dimensional_determinant")
    eq(s.trace(fullM)-16, 16*(c*c-1), "full16_boost_diagnostic_exact_nine")
    eq(s.trace(ext(R).T*ext(hs)*ext(R))-16, 0, "unitarization_discards_nonzero_boost_diagnostic")

    def symmetric(prefix):
        slots = [(i, j) for i in range(4) for j in range(i, 4)]
        symbols = s.symbols(prefix+"0:10", real=True)
        result = s.zeros(4)
        for value, (i, j) in zip(symbols, slots):
            result[i, j] = result[j, i] = value
        return result

    # One generic constrained jet contains ALL ten metric slots at BOTH ends,
    # all six Lorentz link slots and all three observer directions at each end.
    dgs, dgt = symmetric("source_metric"), symmetric("target_metric")
    As, At = -ETA*dgs/2, -ETA*dgt/2
    skew = s.zeros(4)
    for value, (i, j) in zip(s.symbols("link0:6", real=True),
                              [(i, j) for i in range(4) for j in range(i+1, 4)]):
        skew[i, j], skew[j, i] = value, -value
    K = ETA*skew
    dus = As*e0+s.Matrix([0, *s.symbols("source_observer0:3", real=True)])
    dut = At*e0+s.Matrix([0, *s.symbols("target_observer0:3", real=True)])
    dD = As*D-D*At+D*K
    eq(dD.T*ETA*D+D.T*dgs*D+D.T*ETA*dD, dgt,
       "generic_full_metric_and_link_constraint_jet")
    eq((2*e0.T*ETA*dus+e0.T*dgs*e0)[0], 0, "source_observer_unit_jet")
    eq((2*e0.T*ETA*dut+e0.T*dgt*e0)[0], 0, "target_observer_unit_jet")
    dhs = native.reflection_jet(ETA, e0, dgs, dus)
    dht = native.reflection_jet(ETA, e0, dgt, dut)
    _M, dM, dB, dR = polar_link_jet(D, dD, hs, dhs, ht, dht, B)
    eq(B*dB+dB*B, dM, "full_generic_Sylvester_jet_not_frozen_basis")
    eq(dB.T*ETA*B+B.T*dgt*B+B.T*ETA*dB, dgt,
       "moving_positive_part_remains_target_Lorentz")
    eq(dR.T*ETA+dgs+ETA*dR, dgt, "moving_R_has_full_Lorentz_endpoint_jet")
    eq(dR.T*hs+dhs+ht*dR, dht, "moving_R_has_full_positive_pairing_jet")
    eq(dR*e0+dut, dus, "moving_R_aligns_pairing_observer_not_record_axis")
    c, dc = observer_overlap_jet(ETA, e0, e0, D, dgs, dus, dut, dD)
    dtrace = s.trace(dcompound(M, dM))
    eq(dtrace, 32*c*dc, "generic_all_metric_link_observer_exterior_source")
    zeta, dzeta = s.symbols("density_ratio density_ratio_jet", real=True)
    weighted_trace, weighted_source = exterior_trace_jet(c, dc, zeta, dzeta)
    eq(weighted_trace, zeta*s.trace(fullM), "whole_pairing_density_ratio_retained")
    eq(weighted_source, dzeta*s.trace(fullM)+zeta*dtrace,
       "whole_pairing_density_source_not_silently_removed")

    X = s.zeros(4)
    X[0, 1] = X[1, 0] = 1
    _M, boost_dM, boost_dB, boost_dR = polar_link_jet(D, X*D, hs, s.zeros(4), ht, s.zeros(4), B)
    eq(boost_dB, X*D, "actual_boost_source_is_in_dB")
    eq(boost_dR, s.zeros(4), "unitarized_link_has_zero_boost_source")
    eq(s.trace(dcompound(M, boost_dM)), 30, "full16_actual_boost_source_thirty")
    frozen_dR = X*D*B.inv()
    require(frozen_dR.T+frozen_dR != s.zeros(4), "hostile_frozen_B_breaks_pairing_jet")
    checks.append("hostile_frozen_B_breaks_pairing_jet")

    # Actual full-CAR matter preparation, with no guard restriction or reset.
    # Target is its owned t=0 rest-current state, source its t=1 state.
    parameter, matter = data["parameter"], data["m"]
    m = C.mat(matter.subs(parameter, 1))
    dm_family = matter.diff(parameter).subs(parameter, 1)
    J = C.current(I, m)
    target_J = C.current(I, matter.subs(parameter, 0))
    eq(target_J, e0, "actual_target_full_CAR_current_rest")
    eq(J, s.Matrix([1, -s.Rational(2, 3), 0, 0]), "actual_source_full_CAR_current")
    N = C.red((m.T*m)[0])
    eq(N, 3, "actual_matter_normalizer_three")
    eq((dm_family.T*m+m.T*dm_family)[0], 4, "actual_moving_matter_normalizer_four")
    dm = s.Matrix(s.symbols("full_matter_jet0:16", real=True))
    dJ = native.full_current_jet(C, I, m, s.zeros(4), dm)
    us, dus = unit_current_jet(ETA, J, s.zeros(4), dJ)
    hs_current = native.reflection(ETA, J)
    dh_current = native.reflection_jet(ETA, J, s.zeros(4), dJ)
    actual_c, actual_dc = observer_overlap_jet(ETA, us, e0, I, s.zeros(4), dus, s.zeros(4, 1), s.zeros(4))
    actual_source = s.trace(dcompound(hs_current, dh_current))
    eq(actual_source, 32*actual_c*actual_dc,
       "actual_all16_matter_covector_matches_exterior_link_source")
    eq(s.trace(ext(hs_current))-16, s.Rational(64, 5), "actual_current_induced_boost_diagnostic")
    family_substitution = dict(zip(dm, dm_family))
    eq(actual_source.subs(family_substitution), s.Rational(768, 25),
       "actual_preparation_boost_source_keeps_normalizer")
    alphas = C.car_operators()[3]
    frozen_dJ = s.Matrix([0]+[2*(dm_family.T*A*m)[0]/N for A in alphas])
    _u, frozen_du = unit_current_jet(ETA, J, s.zeros(4), frozen_dJ)
    _c, frozen_dc = observer_overlap_jet(ETA, us, e0, I, s.zeros(4), frozen_du, s.zeros(4, 1), s.zeros(4))
    eq(32*actual_c*frozen_dc, s.Rational(2304, 25),
       "hostile_frozen_current_normalizer_gives_wrong_source")
    require(s.Rational(2304, 25) != s.Rational(768, 25), "normalizer_mutation_rejected")
    checks.append("normalizer_mutation_rejected")
    return {"exact_checks": len(checks), "checks": checks,
            "native_current_source_pin": {NATIVE_PATH: NATIVE_SHA256},
            "full_exterior_dimension": 16, "squared_singular_multiplicities": [4, 4, 8],
            "generic_metric_slots_each_endpoint": 10, "generic_link_Lorentz_slots": 6,
            "actual_matter_covector_slots": 16, "rational_boost_diagnostic": "9",
            "rational_boost_source": "30", "actual_current_source": "768/25",
            "density_ratio_retained": True, "pairing_observer_equals_record_axis_claimed": False,
            "future_orientation_selected": False, "diagnostic_is_physical_action": False,
            "new_metric_link_or_temporal_transition_law_derived": False}
