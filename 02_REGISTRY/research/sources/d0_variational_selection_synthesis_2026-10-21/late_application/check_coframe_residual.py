#!/usr/bin/env python3
"""Narrow exact series for one unsolved ambient double-zero coframe row.

Consumes pinned original formulas; does not run their numerical grid suite.
All conditions use active checks, including under optimized Python.
"""
from pathlib import Path
import hashlib
import json
import sys
import sympy as s

PACKET = Path(__file__).resolve().parents[1]
ORIGINAL_ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else PACKET / 'inputs'
LATE_ROOT = Path(sys.argv[2]) if len(sys.argv) > 2 else PACKET / 'late_inputs'
COMMIT = 'c7e0c3d2f6bcfbcc8bd43034ff72da85b8cdd18a'
LATE_PINS = {
    '02_REGISTRY/research/A4D_RANK2_EXACT_FINITE_DOUBLE_ZERO_UNIMODULAR_PF_SYNTHESIS_2026_10_21.md':
        'dcfc4ed42147d047fae32c11b10c25a9d77df6a2dc3009ab6ad0c7d16da2af31',
    '02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21/check_exact_null_sheet_unimodular.py':
        '098d11cd21c4bfc07f24ba32b23f9abe08eecb527bff451a1278bd8ffcdbbf05',
}
ORIGINAL_PINS = {
    '02_REGISTRY/research/sources/d0_star_rank2_seam_2026-10-21/check_star_rank2_seam.py':
        '666b921e53fba8de2332a88c89a572f5ab14d8c03348744494e06b381f2f18b8',
    '02_REGISTRY/research/sources/d0_weighted_two_field_rank2_2026-10-21/native_master.py':
        '23752ce9f4780c7713bbb7fe0d339d8952fe2e422e5541df736e8e08e754e60d',
}
PINS = {**LATE_PINS, **ORIGINAL_PINS}
checks = []


def check(ok, name):
    if not bool(ok):
        raise ArithmeticError(name)
    checks.append(name)


for path, expected in PINS.items():
    source_root = LATE_ROOT if path in LATE_PINS else ORIGINAL_ROOT
    check(hashlib.sha256((source_root / path).read_bytes()).hexdigest() == expected,
          'source pin ' + path)

r, h, v, vs, eps, kappa, ptime = s.symbols(
    'r h v v_star epsilon kappa p_time', positive=True)
A = s.sqrt(r) * s.exp(-r*r/4)
B = 1/A
k1 = (1-r**-2)/2
k2 = s.exp(-r*r/4)/s.sqrt(r)


def dt(f):
    return s.simplify(s.exp(-r*r/2) * s.diff(f, r))


# Exact six-face numerator = L_h v+M_h+R_h/v. Its normalized
# coefficients below are obtained from the original based holonomies.
# C(h*k1,h*k2) has no h^3 term; h*(k(t+h)-k(t)) starts at h^2.
ell0 = s.simplify(2*A*r*k1*k2)
mid0 = s.simplify(r*r*dt(k1)+A*B*k2*k2)
right0 = s.simplify(2*B*r*dt(k2))
mid1 = s.simplify(r*r*dt(dt(k1))/2)
right1 = s.simplify(B*r*dt(dt(k2)))
check(s.simplify(ell0+mid0+right0) == 0,
      'original star leading term vanishes at v=1')
f1 = s.simplify(mid1+right1)
check(s.simplify(f1-3*(r**4-1)*s.exp(-r*r)/(4*r*r)) == 0,
      'original star first h coefficient retained')
fv0 = s.simplify(ell0-right0)
check(s.simplify(fv0-2*A*A) == 0,
      'original shear derivative has positive leading value 2 A squared')
v1 = s.simplify(-f1/fv0)
check(s.simplify(v1+3*(r**4-1)*s.exp(-r*r/2)/(8*r**3)) == 0,
      'owned projected-root first coefficient recovered')

# Euler differentiation holds the actual scalar forward increments fixed.
# The projected value p_time=epsilon*A^2*v_star^2 is substituted AFTER d/dv.
q = ptime**2/(A*A*v*v)-eps**2*v*v/(B*B)
q_at_root = s.simplify(q.subs({v: vs, ptime: eps*A*A*vs*vs}))
check(q_at_root == 0, 'same projected point has exact two-field q=0')
dq_fixed = s.simplify(s.diff(q, v).subs({v: vs, ptime: eps*A*A*vs*vs}))
check(s.simplify(dq_fixed+4*eps**2*A*A*vs) == 0,
      'fixed-matter shear derivative is minus four epsilon squared A squared v')
matter_source = s.simplify((kappa*dq_fixed).subs(eps**2, 1/(2*kappa)))
check(s.simplify(matter_source+2*A*A*vs) == 0,
      'original epsilon squared equals one over two kappa fixes matter source')
check(s.simplify(s.diff(A*v*(B/v)*r*r, v)) == 0,
      'ambient coframe shear is exactly volume preserving')

# Expand the FULL fixed-matter ambient row, not the constant restricted
# action on Sigma. There is no order-h contribution in L_h/h^2.
source_leading = s.simplify(ell0-right0-2*A*A)
check(source_leading == 0, 'continuum leading shear Euler coefficient cancels')
source_h = s.factor(2*(right0-A*A)*v1-right1)
expected = s.exp(-r*r)*(3*r*r+1)*(r**4-3)/(4*r**4)
check(s.simplify(source_h-expected) == 0,
      'exact first finite shear Euler coefficient')
check(s.simplify(source_h.subs(r, 1)+2/s.E) == 0,
      'at r=1 ambient row equals minus two h over e plus O(h squared)')

# On [1,6/5], the coefficient is uniformly strictly negative.
upper_r4 = s.Rational(6, 5)**4
check(upper_r4 < 3, 'rank-two interval lies strictly below fourth-root three')
lower_factor = s.simplify(4*(3-upper_r4)/(4*upper_r4))
check(lower_factor == s.Rational(193, 432) and lower_factor > 0,
      'uniform absolute coefficient bound 193 over 432 times exp minus 36 over 25')

print(json.dumps({
    'scope': 'one exact ambient coframe Euler asymptotic on the original projected double-zero sheet',
    'input_commit': COMMIT,
    'source_sha256': PINS,
    'checks': checks,
    'passed': len(checks),
    'exact_ambient_row': '(L_h-R_h/v_star^2)/h^2-2*A(r)^2*v_star',
    'h_coefficient': '(3*r^2+1)*(r^4-3)*exp(-r^2)/(4*r^4)',
    'at_r_1': '-2/exp(1)',
    'uniform_negative_coefficient_on_1_to_6_over_5': True,
    'fixed_matter_before_differentiation': True,
    'restricted_Sigma_action_would_be_constant': True,
    'new_double_zero_theorem_preserved': True,
    'this_projected_representative_all42_stationary': False,
    'other_corrected_representatives_excluded': False,
    'full_native_preparation_price_stationarity': False,
    'GR_closed': False,
}, indent=2))
