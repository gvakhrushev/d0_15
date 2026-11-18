#!/usr/bin/env python3
"""One actual fixed-chart sampling row, with exact symbolic/rational bounds.

No new roots or parameters. The geometric-root/source-map premise is B65.
The matrix bounds are proved in SAMPLING_SOURCE_BIAS_RU.md; this script
checks their constants, the actual chart address, and the polynomial moment
identity independently of the closed expectation formula.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import ast
import json
import sympy as S

P = Path(__file__).resolve().parent
D = P.parent
B = Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open')


def named_assignment(tree, name):
    return next(n.value for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))


def main():
    targets = B/'round25/targets.py'
    tree = ast.parse(targets.read_text())
    assert ast.unparse(named_assignment(tree, 'SAMP')) == '2 ** (-30)'
    assert ast.unparse(named_assignment(tree, 'EPSILON_EXACT')) == 'Fraction(1, 2 ** 1531)'
    assert ast.unparse(named_assignment(tree, 'NU')) == '0.6'
    assert ast.unparse(named_assignment(tree, 'H')) == '0.25'
    rows = [json.loads(t) for t in (B/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl').read_text().splitlines()]
    site = [0, 0, 1, 1]
    row = next(r for r in rows if r['site'] == site and r['kind'] == 'coframe'
               and r['role'] == 0 and r['component'] == 2)
    assert row['sam_index'] == 2
    for role in range(4):
        target = [(v+int(i == role)) % 4 for i, v in enumerate(site)]
        assert sum(r['kind'] == 'matter' and r['site'] == target for r in rows) == 2
    assert sum(r['kind'] == 'matter' and r['site'] == site for r in rows) == 2
    env = json.loads((B/'round21/CHART_ENVELOPE_RESULT.json').read_text())
    assert F(env['coframe_creator_norm_strict_upper']) < 1
    b65 = json.loads((B/'round65/SCALAR_HESSIAN_ENVELOPE.json').read_text())
    assert b65['local_f_value_bound_lt'] == '2^13'
    assert b65['local_q_value_bound_lt'] == '16'
    assert json.loads((D/'round30/COMMON_SOURCE_MARKED_PLAN.json').read_text())['total_RAW_births'] == 10407050782

    # Exact independent polynomial Bernoulli moment reduction. Bits are
    # distinct actual matter coordinates; their moments are E[b^k]=r, k>0.
    r, s, a, h, nu, d = S.symbols('r s a h nu d', nonzero=True)
    bits = S.symbols('b0:6')
    centre = S.Matrix([a, 0])
    forward0 = S.Matrix([0, a])
    forward2 = S.Matrix([a, 0])
    noises = [S.Matrix([s*(bits[2*i]-r), s*(bits[2*i+1]-r)]) for i in range(3)]
    dv = (forward0 + noises[1] - centre - noises[0])/h
    dx = (forward2 + noises[2] - centre - noises[0])/h
    # All terms independent of this coframe coordinate cancel in the secant.
    q = -(d*d*dv.dot(dv) + 2*d*nu*dv.dot(dx))/nu**2
    secant = S.expand((q.subs(d, s*(1-r))-q.subs(d, -s*r))/s)
    poly = S.Poly(secant, *bits)
    actual = S.expand(sum(coefficient*r**sum(k > 0 for k in powers)
                          for powers, coefficient in poly.terms()))
    variance = s*s*r*(1-r)
    expected = -s*(1-2*r)*(2*a*a/h**2 + 4*variance/h**2)/nu**2 - 4*variance/(nu*h**2)
    assert S.simplify(actual-expected) == 0
    assert S.simplify(actual.subs(s, 0)) == 0
    # Ignoring shared base-point fluctuations omits the second term.
    wrong = -s*(1-2*r)*(2*a*a/h**2 + 4*variance/h**2)/nu**2
    assert S.simplify(actual-wrong+4*variance/(nu*h**2)) == 0

    s0, h0, nu0, eps = F(1, 2**30), F(1, 4), F(3, 5), F(1, 2**1531)
    # p in (3/5,5/8), hence kappa=1-2p^2=2p-1>1/5,
    # Var(b)=p^3=2p-1<1/4, ||K_a||_F^2=2 (all six).
    assert F(3,5)**2+F(3,5) < 1 < F(5,8)**2+F(5,8)
    eta = S.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
    for i in range(4):
        for j in range(i+1,4):
            aa = S.zeros(4); aa[i,j] = 1; aa[j,i] = -1
            kk = eta*aa
            assert (kk.T*kk).trace() == 2
            assert kk.trace() == 0 and kk.T*eta + eta*kk == S.zeros(4)
    # E||dLambda(Theta)||^2 <=16 E||Theta||_F^2<48 s^2.
    # E dLambda(Theta)=0; exp remainder <= second moment/[2(1-24s)].
    mean_exp = F(24,1)/(1-24*s0)
    assert mean_exp < 25
    assert F(17,16)**4 < F(4,3)
    assert F(4,3)*mean_exp < 34
    assert F(4,3) + 34*s0*s0 < F(3,2)
    loop_error_coefficient = 4*34*F(3,2)**3
    assert loop_error_coefficient == 459
    local_f_error_coefficient = 3*F(400,9)*4*loop_error_coefficient
    assert local_f_error_coefficient == 244800 < 2**18
    f_error = F(2**10)*s0*s0
    # k0>20, pi>3: the main scalar contribution after h^4 is >s/6400.
    positive = 20*h0**4*s0*F(1,5)*F(9,2500)/nu0**2
    assert positive == s0/F(6400) and positive > F(1,2**43)

    # Genuine nonlinear reporter correction, not an omitted linearization.
    # B65: |r_xx/r_x0|<2^47, |r_yy/r_y0|<2^43 on |x|,|y|<=1.
    # rho_min>1/2; |f|<2^13, |q|<16, k0<24, 0<a_y<1.
    remainder_sup = 2**47*eps*(2**13)**2 + 24*2**43*eps*16**2
    assert remainder_sup < F(1,2**1457)
    reporter_secant = 2*remainder_sup/s0
    assert reporter_secant < F(1,2**1426)
    # A30: e/(g*s)<2^-73. A32: full H+J per SAM row <2^-73
    # under Gamma_s. Divide by u=2p sqrt(p)>1/2 for this scalar row.
    native = F(1,2**73)
    finite_book = F(1,2**72)
    lower = positive - f_error - reporter_secant - native - finite_book
    assert lower > F(1,2**44)
    # Source after A31 correction evaluates on y=J_actual e_j as d_j/u;
    # ||y||<1+2^-23<2, so its full norm exceeds 2^-45.
    assert F(1)+F(1,2**23) < 2
    pins = [Path(__file__), targets, B/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl',
            B/'round21/CHART_ENVELOPE_RESULT.json', B/'round24/TORUS_BOUNDARY_REVIEW_RU.md',
            B/'round65/B65_CENTRE_SOURCE_AND_BOUNDS_RU.md', B/'round65/SCALAR_HESSIAN_ENVELOPE.json',
            D/'round11/source_operator_dag.py', D/'round27/PREPARED_SOURCE_MOMENT_LAW_RU.md',
            D/'round30/COMMON_SOURCE_MARKED_PLAN.json', D/'round31/RESULT.json', D/'round32/RESULT.json']
    out = {'status': 'PASS_FIXED_SAMPLER_NONZERO_SOURCE_ROW', 'coordinate': row,
           'scope': 'fixed B25 cube, original ideal source law, actual A30 scalar core and A32 finite H+J comparison; conditional on pinned owner/source-map proofs',
           'q_secant_exact': '-s*(1-2*p^2)*(pi^2/2500+4*s^2*p^3/h^2)/nu^2 - 4*s^2*p^3/(nu*h^2)',
           'Bernoulli_polynomial_identity_exact': True,
           'geometry_only_central_row_zero': True,
           'positive_matter_contribution_gt': 's/6400 >2^-43',
           'averaged_geometric_secant_abs_lt': '2^10*s^2=2^-50',
           'nonlinear_reporter_secant_error_lt': '2^-1426',
           'native_scalar_row_error_lt': '2^-73',
           'finite_H_plus_J_scalar_row_error_lt': '2^-72',
           'actual_normalized_finite_comparison_scalar_gt': '2^-44',
           'corrected_raw_covector_norm_gt': '2^-45',
           'physical_direction': 'y=J_actual e_2; covector[y]=FD_SAM2/(u_sampling*Gamma_s), Gamma0=Gamma_s/s',
           'endpoint_price_order': 'Book_H_plus_J(endpoint plus)>Book_H_plus_J(endpoint minus)',
           'new_native_centre_history_constructed': False,
           'exact_stationary_history_or_minimum_claimed': False,
           'all_other_rows_or_uniform_refinement_proved': False,
           'full_Cost_Info_selection_proved': False,
           'source_sha256': {str(f):sha256(f.read_bytes()).hexdigest() for f in pins},
           'physical_C_closed': False, 'GR_closed': False}
    (P/'SAMPLING_SOURCE_BIAS_CHECK.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','coordinate','actual_normalized_finite_comparison_scalar_gt','corrected_raw_covector_norm_gt')}))


if __name__ == '__main__':
    main()
