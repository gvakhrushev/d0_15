#!/usr/bin/env python3
"""Exact basis/response checks and every owned coordinate-to-mark binding."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import hashlib, itertools, json
import sympy as S
import mean_geometry_lift as m
P = Path(__file__).resolve().parent


def main():
    coordinates, blocks = m.catalogue_binding(); bounds = m.bound_certificate()
    assert [c['sam_index'] for c in coordinates] == list(range(2688))
    old = m.sched.g.namespace(); binding = m.marks.original_binding()
    for c in coordinates:
        q_sam = old['layout']['SAM'][c['sam_index']]
        assert m.sched.b.physical_wire(q_sam) == 2+c['sam_index']
        if c['kind'] == 'proper_link':
            block = blocks[c['link_block']]
            assert block['site'] == c['site'] and block['role'] == c['role']
            assert c['generator'] == c['decoded_component_ab']
        else:
            t = binding['leaf_templates'][c['original_leaf_template']]
            assert t['location'] == 'base'
            assert binding['site_bindings'][c['external_SITE_index']]['site'] == c['site']
            if c['kind'] == 'coframe':
                assert t['direction'] == c['role'] and t['output'] == 1 << c['component'] and t['input'] == 0
            else:
                assert t['cross_masks'] == [1, c['grade']]
    for block in blocks:
        assert len(block['matrix_entries']) == 16
        assert {(e['row'], e['column']) for e in block['matrix_entries']} == set(itertools.product(range(4), repeat=2))
    # Exact extraction convention on ALL 6x6 basis components.
    eta = S.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
    pairs = list(itertools.combinations(range(4), 2))
    for col, (a, b) in enumerate(pairs):
        skew = S.zeros(4); skew[a,b] = 1; skew[b,a] = -1
        K = eta*skew
        assert K.T*K == S.diag(*[int(i in (a,b)) for i in range(4)])
        for row, (i,j) in enumerate(pairs):
            assert (eta*K)[i,j] == int(row == col)
    # Exact finite fixture for the ACTUAL diagonal-operator derivative,
    # including a table which depends jointly on different SAM coordinates.
    p = (S.sqrt(5)-1)/2; a = S.sqrt(p); u = 2*a*p
    phi = S.Matrix([a**(3-bin(x).count('1'))*p**bin(x).count('1') for x in range(8)])
    values = [S.Rational((x*x+3*x+1) % 13, 17) for x in range(8)]
    E = S.diag(*values)
    for j in range(3):
        J = S.zeros(8)
        for x in range(8):
            J[x^(1<<j), x] = -1 if x & (1<<j) else 1
        derivative = (phi.T*(E*J-J*E)*phi)[0]
        influence = 0
        for x in range(8):
            if x & (1<<j):
                continue
            ones = bin(x).count('1')
            influence += p**(2-ones)*p**(2*ones)*(values[x|(1<<j)]-values[x])
        assert S.simplify(derivative-u*influence) == 0
    # The completed physical raw lift and the two possible source gains
    # have an exact factor-s relation. Do not suppress it in a source claim.
    s = bounds['s']; assert s == Fraction(1, 2**30)
    assert bounds['bias'] < Fraction(1, 2**48)
    assert Fraction(20,3) < 8
    endpoint = m.sched.inventory()['full_compressed_error']
    assert 55*endpoint*2**3188 < Fraction(1, 2**37)
    assert Fraction(20,3)*55*endpoint*2**3188 < Fraction(1, 2**34)
    files = [Path(__file__), P/'mean_geometry_lift.py', P/'MEAN_GEOMETRY_LIFT_PLAN.json',
             m.D/'round30/SOURCE_RAW_MARK_REGISTRY.json', m.B/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl',
             m.B/'round25/precision_name.py']
    out = {'status': 'PASS_ALL_RAW_CHART_BINDINGS_AND_EXACT_RESPONSE_IDENTITIES',
           'coordinate_bindings': len(coordinates), 'coordinate_counts': dict(Counter(c['kind'] for c in coordinates)),
           'full_link_matrix_bindings': len(blocks), 'exact_eta_K_components': 36,
           'exact_three_SAM_diagonal_response_fixture': True,
           'actual_large_mean_or_J_evaluated': False,
           'native_error_terms_alone_are_not_full_source_consistency': True,
           'source_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
           'physical_C_closed': False, 'GR_closed': False}
    (P/'MEAN_GEOMETRY_LIFT_CHECK.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({'status': out['status'], 'coordinates': len(coordinates), 'link_blocks': len(blocks)}))


if __name__ == '__main__':
    main()
