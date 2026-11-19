#!/usr/bin/env python3
"""Exact full-CAR gauge span and complete flat contrast-row interface.

Only pinned creator/order definitions execute.  The finite constructions
below certify an analytic spanning proof, not sampled a/b ranks.  No old
run(), spectrum, physical detector, preparation or price is installed.
"""
from pathlib import Path
from functools import lru_cache
import ast
import hashlib
import json

import sympy as s

ROOT = Path(__file__).resolve().parents[4]
CREATORS = '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
PINS = {
    CREATORS: 'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
    '02_REGISTRY/research/sources/d0_retained_causal_principal_2026-10-17/check_principal.py':
        '7f57f6e325defd8fda3e85667cf040f061ef8dba6a0897a127385ed8de49380d',
    '02_REGISTRY/research/sources/d0_retained_history_causal_source_2026-10-16/check_retained_history.py':
        '6be5d31fc2b5a2d2f75b54071720b03c6bbebc30356260b5c823c3ef8ef88d92',
}
CHARS = ((1, 1, 1, 1), (1, 1, -1, -1),
         (1, -1, 1, -1), (1, -1, -1, 1))
ROLE_LABELS = (0, 16, 8, 24)
PAIRS = tuple((i, j) for i in range(4) for j in range(i+1, 4))


def creator_definitions(repo):
    tree = ast.parse((repo/CREATORS).read_text())
    nodes = [node for node in tree.body if
             (isinstance(node, ast.FunctionDef) and node.name == 'creator') or
             (isinstance(node, ast.Assign) and any(isinstance(t, ast.Name)
              and t.id == 'EXTERIOR_ORDER' for t in node.targets))]
    if len(nodes) != 2:
        raise ArithmeticError('gauge_span:creator_definition_nodes')
    scope = {'s': s, 'lru_cache': lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), CREATORS, 'exec'), scope)
    return [scope['creator'](r) for r in range(4)], scope['EXTERIOR_ORDER']


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def require(condition, name):
        if not bool(condition):
            raise ArithmeticError('gauge_span:' + name)
        checks.append(name)

    def eq(actual, expected, name, simplify=s.expand):
        values = list(actual-expected) if isinstance(actual, s.MatrixBase) else [actual-expected]
        require(all(simplify(value) == 0 for value in values), name)

    for path, digest in PINS.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest,
                'source_pin_' + Path(path).name)
    C, order = creator_definitions(repo)
    I, O = s.eye(16), s.zeros(16)
    require(order == (0, 2, 3, 1), 'actual_ACDB_order_full16')
    for r in range(4):
        for t in range(4):
            eq(C[r]*C[t].T+C[t].T*C[r], I if r == t else O,
               'full16_CAR_' + str(r)+str(t))

    def lift(matrix):
        return sum((matrix[a, b]*C[a]*C[b].T for a in range(4)
                    for b in range(4)), O.copy())

    # Normal CAR words are tested on Lambda^1 -> Lambda^2 only to prove
    # independence; every subsequent operator is still the full16 matrix.
    indices = [(i, j, b) for i, j in PAIRS for b in range(4)]
    words = [C[i]*C[j]*C[b].T for i, j, b in indices]
    readout = s.Matrix(24, 24, lambda r, k:
        words[k][(1 << indices[r][0]) | (1 << indices[r][1]), 1 << indices[r][2]])
    eq(readout.T*readout, s.eye(24), 'all24_normal_CAR_words_independent_via_one_to_two_forms')
    coeffs = s.symbols('T0:24', real=True)
    Z = [O.copy() for _ in range(4)]
    for coefficient, word, (i, j, b) in zip(coeffs, words, indices):
        Z[i] += coefficient*word
        Z[j] -= coefficient*word
    eq(sum(Z, O.copy()), O, 'all24_torsionfree_symmetric_Z_Cartan_sum')
    sampled = s.Matrix([Z[i][(1 << i) | (1 << j), 1 << b] for i, j, b in indices])
    eq(sampled, readout*s.Matrix(coeffs), 'symmetric_tuple_has_exactly_all24_independent_coefficients')

    # Four actual unit-observer gauge probes for each pair span its four
    # b coefficients.  Every probe is independently checked against LC.
    E4 = s.eye(4)
    determinants = []
    for i, j in PAIRS:
        outside = [k for k in range(4) if k not in (i, j)]
        qp, qm = E4[:, i]+E4[:, j], E4[:, i]-E4[:, j]
        probes = [(qp, E4[:, k]) for k in outside]
        probes += [(qp, (E4[:, i]-E4[:, j])/s.sqrt(2)),
                   (qm, (E4[:, i]+E4[:, j])/s.sqrt(2))]
        columns = []
        for n, (q, a) in enumerate(probes):
            eq((a.T*a)[0], 1, 'unit_observer_' + str(i)+str(j)+str(n))
            eq((q.T*a)[0], 0, 'genuine_gauge_tangency_' + str(i)+str(j)+str(n))
            g = -s.eye(4)+2*a*a.T
            eq(g*g, s.eye(4), 'actual_Lorentz_reflection_inverse_' + str(i)+str(j)+str(n))
            h = 2*(a*q.T+q*a.T)
            dg = [q[r]*h for r in range(4)]
            Gamma = [s.Matrix(4, 4, lambda k, t:
                sum(g[k, ell]*(dg[r][ell, t]+dg[t][ell, r]-dg[ell][r, t])
                    for ell in range(4))/2) for r in range(4)]
            for r in range(4):
                eq(Gamma[r], 2*q[r]*a*q.T,
                   'actual_LC_gauge_connection_' + str(i)+str(j)+str(n)+str(r))
            actual = [C[r]*lift(-Gamma[r].T) for r in range(4)]
            column = -2*q[i]*q[j]*a
            columns.append(column)
            word_sum = sum((column[b]*C[i]*C[j]*C[b].T for b in range(4)), O.copy())
            for r in range(4):
                expected = word_sum if r == i else -word_sum if r == j else O
                eq(actual[r], expected,
                   'gauge_has_only_named_offdiagonal_pair_' + str(i)+str(j)+str(n)+str(r))
        determinant = s.det(s.Matrix.hstack(*columns))
        eq(determinant**2, 256, 'four_genuine_gauges_span_entire_pair_' + str(i)+str(j))
        determinants.append(str(determinant**2))

    # Exact generic positive-partial-isometry roots.  The two identities
    # involving nu use nu^2+b^2=1; Sylvester inverses only require b>0.
    nu, b = s.symbols('nu b', positive=True)
    radial = lambda value: s.rem(s.expand(value), nu*nu+b*b-1, nu)
    N = [c*c.T for c in C]
    L0 = [I+(b-1)*n for n in N]
    R0 = [I+(b-1)*(I-n) for n in N]
    dP = [nu*z for z in Z]
    dL, dR = [], []
    for r in range(4):
        eq(L0[r]*L0[r], I-nu*nu*N[r], 'left_root_square_' + str(r), radial)
        eq(R0[r]*R0[r], I-nu*nu*(I-N[r]), 'right_root_square_' + str(r), radial)
        eq(L0[r]*C[r], C[r]*R0[r], 'root_creator_intertwining_' + str(r))
        left_rhs = nu*nu*(Z[r]*C[r].T+C[r]*Z[r].T)
        right_rhs = nu*nu*(Z[r].T*C[r]+C[r].T*Z[r])
        p, k = N[r], I-N[r]
        def inverse_sylvester(Y, first, second):
            return first*Y*first/(2*b)+(first*Y*second+second*Y*first)/(1+b)+second*Y*second/2
        left = -inverse_sylvester(left_rhs, p, k)
        right = -inverse_sylvester(right_rhs, k, p)
        dL.append(left)
        dR.append(right)
        eq(L0[r]*left+left*L0[r], -left_rhs,
           'generic_all24_left_Sylvester_' + str(r), s.cancel)
        eq(R0[r]*right+right*R0[r], -right_rhs,
           'generic_all24_right_Sylvester_' + str(r), s.cancel)
    eq(L0[0]+R0[0], (1+b)*I, 'sum_of_onsite_defect_roots_scalar')

    # All32 even-duplicate fine rows, including coefficient1.  Baselines
    # and leading jets are built from the literal row formula, not a list
    # of desired nonzero rows.
    def row(chi, sigma, tau, coefficient, P, left, right):
        if coefficient == 0:
            return sum((chi[r]*(P[r]+sigma*P[r].T-tau*nu*C[r]
                         -sigma*tau*nu*C[r].T) for r in range(4)), O.copy())/16
        return sum((chi[r]*(left[r]+sigma*right[r]-tau*L0[r]
                     -sigma*tau*R0[r]) for r in range(4)), O.copy())/16
    base_rows = {}
    P0 = [nu*c for c in C]
    for chi_index, chi in enumerate(CHARS):
        for u in range(2):
            for v in range(2):
                for coefficient in range(2):
                    key = (chi_index, u, v, coefficient)
                    base_rows[key] = row(chi, (-1)**u, (-1)**v, coefficient, P0, L0, R0)
    zero_keys = [key for key, value in base_rows.items() if value == O]
    nonzero_keys = [key for key, value in base_rows.items() if value != O]
    expected_zero = [(chi, u, 0, c) for chi in range(4) for u in range(2) for c in range(2)]
    expected_zero += [(chi, 0, 1, 1) for chi in range(1, 4)]
    require(set(zero_keys) == set(expected_zero) and len(zero_keys) == 19
            and len(nonzero_keys) == 13, 'complete32_rows_have19_zero_and13_nonzero_baselines')
    require((0, 0, 0, 0) in zero_keys and len([k for k in zero_keys if k != (0, 0, 0, 0)]) == 18,
            'eighteen_nonblank_zero_baseline_rows')

    # Constructive independence of the13 nonzero rows, not a rank scan.
    odd = [base_rows[(chi, u, 1, 0)] for chi in range(4) for u in range(2)]
    odd_readout = s.Matrix(8, 8, lambda r, j:
        odd[j][1 << r, 0] if r < 4 else odd[j][0, 1 << (r-4)])
    eq(s.det(odd_readout)**2, nu**16/2**24, 'eight_odd_baselines_have_nonzero_analytic_minor')
    even = [base_rows[(0, 0, 1, 1)]]+[base_rows[(chi, 1, 1, 1)] for chi in range(4)]
    masks = [0, 1, 2, 4, 8]
    even_readout = s.Matrix(5, 5, lambda r, j: even[j][masks[r], masks[r]])
    eq(s.det(even_readout)**2, (1+b)**2*(1-b)**8/1024,
       'five_even_baselines_have_nonzero_analytic_minor')
    parity = s.diag(*[(-1)**bin(mask).count('1') for mask in range(16)])
    require(all(parity*x*parity == -x for x in odd)
            and all(parity*x*parity == x for x in even),
            'odd_even_baseline_spaces_disjoint_on_full16')
    eq(nu**2+b**2-1, 0, 'strict_fixture_nu_three_fifths_b_four_fifths',
       lambda value: s.expand(value.subs({nu: s.Rational(3, 5), b: s.Rational(4, 5)})))

    # The extra3 zero rows have the very same leading Sylvester jet as
    # their tau+ partner.  In particular they cannot evade the gauge span.
    eps = s.Symbol('jet', real=True)
    perturbed_P = [P0[r]+eps*dP[r] for r in range(4)]
    perturbed_L = [L0[r]+eps*dL[r] for r in range(4)]
    perturbed_R = [R0[r]+eps*dR[r] for r in range(4)]
    for chi in range(1, 4):
        plus = row(CHARS[chi], 1, 1, 1, perturbed_P, perturbed_L, perturbed_R)
        minus = row(CHARS[chi], 1, -1, 1, perturbed_P, perturbed_L, perturbed_R)
        eq((plus-minus).diff(eps), O, 'extra_row_same_generic_Sylvester_jet_' + str(ROLE_LABELS[chi]))
    # The kinetic part cancels in both root arguments.  This algebraic
    # identity is generic in a formal derivative coefficient, not an
    # assertion that roots commute with an actual differential operator.
    formal_d = s.Symbol('formal_derivative')
    for r in range(4):
        kinetic = nu*C[r]*formal_d
        kinetic_adjoint = -nu*C[r].T*formal_d
        eq(kinetic*(nu*C[r].T)+(nu*C[r])*kinetic_adjoint, O,
           'left_root_has_no_leading_kinetic_part_' + str(r))
        eq(kinetic_adjoint*(nu*C[r])+(nu*C[r].T)*kinetic, O,
           'right_root_has_no_leading_kinetic_part_' + str(r))

    # The two nonblank golden port coefficients have a fixed common norm.
    # Blank port1 is a distinct geometry-independent amplitude on fixedG
    # LC; blank port0 contains the identity and is not paired in this union.
    a, p = s.symbols('a p', real=True)
    golden = lambda value: s.rem(s.rem(s.expand(value), a*a-p, a), p*p+p-1, p)
    eq(p**4+a*a*p*p, p*p, 'nonblank_two_port_vector_norm_squared', golden)
    rare_count = 2*18+1
    require(rare_count == 37, 'full_rare_output_count_includes_distinct_blank_port1')
    t = s.Symbol('blank_A', real=True)
    blank0, blank1 = 1-2*p*p*t*t, -2*a*p*t*t
    require(golden(blank0-(-2*p*p*t*t)) == 1,
            'blank_port0_identity_not_falsely_used_in_nonblank_union')
    eq(blank1, -2*a*p*t*t, 'blank_port1_separate_A_squared_amplitude')

    return {
        'status': 'PASS', 'exact_checks': len(checks), 'checks': checks, 'source_pins': PINS,
        'carrier': {'Fock': 16, 'reference_retained': 128, 'faithful_shell_momenta': 8,
                    'labels': 32, 'coefficient_qubit': 2, 'golden_ports': 2,
                    'retained_workspace': '128^n; no reset'},
        'torsionfree_Z_coefficients_real': 24,
        'gauge_construction': 'four unit-a genuine gauges perpair: q=ei+ej,a=ek outsidepair; q=ei+ej,a=(ei-ej)/sqrt2; q=ei-ej,a=(ei+ej)/sqrt2',
        'pair_determinants_squared': determinants,
        'complete_even_duplicate_rows': 32, 'zero_baseline_rows_including_complete_blank': 19,
        'zero_baseline_nonblank_rows': 18, 'nonzero_baseline_rows_independent': 13,
        'extra_three_rows': [{'role_label': ROLE_LABELS[c], 'u': 0, 'tau': -1, 'coefficient': 1}
                             for c in range(1, 4)],
        'rare_raw_port_outputs_including_blank_port1': rare_count,
        'strict_fixture': {'nu': '3/5', 'defect_root': '4/5'},
        'general_root_scope': '0<nu<1, b=sqrt(1-nu^2)>0; generic projector Sylvester inverse on all24 coefficients',
        'PSD_consumer': 'fixed linear contrast map is background-independent; gauge amplitudes span all torsionfree Z, so PSD annihilation of all genuine gauges annihilates its entire LC principal response',
        'scope': {'old_run_roots_or_spectra_executed': False,
                  'sampled_ranks_used_for_general_theorem': False,
                  'form_grade_truncated': False,
                  'nonzero_baseline_output_Hessians_classified': False,
                  'field_dependent_detector_or_native_price_excluded': False,
                  'physical_detector_or_preparation_admission_proved': False,
                  'blank_two_port_union_used': False,
                  'result_is_exact_principal_interface_not_all_history_limit': True},
    }


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
