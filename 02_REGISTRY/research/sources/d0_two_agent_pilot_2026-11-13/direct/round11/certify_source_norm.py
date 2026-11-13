#!/usr/bin/env python3
"""Exact all-input tensor-operator majorant; no empirical state norm used."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
path = HERE/'SOURCE_TENSOR_DAG.json'
dag = json.loads(path.read_text())
plo, phi = F(309, 500), F(619, 1000)
assert plo*plo+plo < 1 < phi*phi+phi
# A is the ACTIVE programme-address count, not the padded register size.
# This is an upper-bound contract A<=4096, not an assignment A=4096.
A_max, d, S = 4096, 32, 256
rho_min = F(256*29, 10946)
bound, degrees = [], []
for index, n in enumerate(dag['nodes']):
    op = n['op']
    if op == 'const':
        a, b = F(n['a']), F(n['b'])
        norm = max(abs(a+b*plo), abs(a+b*phi))
        degree = [0, 0]
    elif op == 'var':
        if n['kind'] == 'choi_coframe':
            norm, degree = F(A_max*d, 2), [1, 0]
        elif n['kind'] == 'choi_link':
            norm, degree = F(A_max*d), [1, 0]
        else:
            assert n['kind'] == 'matter_X'
            norm, degree = F(1), [0, 1]
    else:
        args = n['args']
        assert args and all(type(k) is int and 0 <= k < index for k in args)
        assert op in ('add', 'mul')
        if op == 'add':
            norm = sum(bound[k] for k in args)
            degree = [max(degrees[k][j] for k in args) for j in range(2)]
        else:
            norm = F(1)
            for k in args:
                norm *= bound[k]
            degree = [sum(degrees[k][j] for k in args) for j in range(2)]
    assert degree == n['degree']
    bound.append(norm)
    degrees.append(degree)
roots = {name: bound[k]/rho_min for name, k in dag['roots'].items()}
assert degrees[dag['roots']['H_f_before_inverse_PF']] == [82, 0]
assert degrees[dag['roots']['H_q_before_inverse_PF']] == [2, 2]
largest = max(roots.values())
power = max(0, largest.numerator.bit_length()-largest.denominator.bit_length())
while F(2)**power < largest:
    power += 1
assert F(2)**power >= largest and (power == 0 or F(2)**(power-1) < largest)
result = {
    'status': 'PASS_EXACT_FULL_INPUT_SOURCE_OPERATOR_MAJORANT',
    'operator_dag_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
    'checked_nodes': len(bound), 'leaf_count': sum(n['op'] == 'var' for n in dag['nodes']),
    'contract': {'active_programme_addresses_at_most': A_max,
                 'active_A_not_padding_denominator': True, 'julia_d': d,
                 'uniform_internal_CAR_sites_S': S, 'rho_min': str(rho_min),
                 'h': '1/4', 'nu': '3/5',
                 'global_H1_catalogue_and_halo_not_proved_by_this_certificate': True},
    'leaf_norm_upper': {'coframe_moment': str(F(A_max*d, 2)),
                        'link_matrix_moment': str(F(A_max*d)), 'material_X': '1'},
    'golden_isolating_interval': [str(plo), str(phi)],
    'source_operator_norm_upper_rational': {k: str(v) for k, v in roots.items()},
    'common_Lambda_h': f'2^{power}', 'common_Lambda_h_integer': str(2**power),
    'epsilon_h': f'2^-{power+6}',
    'canonical_copy_degrees': {k: degrees[v] for k, v in dag['roots'].items()},
    'ten_sign_copies': {'Choi': 2*82+8*2, 'material': 8*2},
    'seven_unspecialized_calls_copy_bound': {'Choi': 7*(2*82+8*2), 'material': 7*8*2},
    'norm_method': 'triangle inequality; disjoint-copy tensor product norm; identity padding norm one; exact rational arithmetic',
    'positive_effects': '(I +/- H_f/Lambda_h)/2 and (I +/- H_q/Lambda_h)/2 are positive contractions on ALL input columns under the contract',
    'not_claimed': ['native sign/compiler word', 'READY probability', 'physical bank admission',
                    'full H1 source or geometric gain', 'physical Cost-Info binding'],
    'GR_closed': False}
(HERE/'SOURCE_NORM_CERTIFICATE.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: result[k] for k in ['status', 'checked_nodes', 'common_Lambda_h',
                                      'epsilon_h', 'ten_sign_copies']}))
