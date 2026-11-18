#!/usr/bin/env python3
"""A60: actual SOURCE near-product bound and bank-preserving code capacity.

Exact rational/symbolic fixtures and inherited production norm bounds.
No production state, price, encoder or physical Info is evaluated here.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json
import sys
import sympy as s

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
D = P.parent
sys.path.insert(0, str(D/'round55'))
import regular_comparison_task as parent


def production_bounds():
    source = parent.source.upper_inventory_and_error()
    enclosure = parent.paid.paid.control.a47.source_derivative_enclosure()
    M1 = enclosure['full_bank_M1']
    assert M1 == 1748
    eB = source['full_SOURCE_DATA_fibre_prefix_error']
    assert eB < F(1, 1 << 3423)
    sigma = F(1, 1 << 80)
    delta = M1*104*sigma+eB
    q = delta*delta
    assert delta < F(1, 1 << 62)
    assert q < F(1, 1 << 124)
    m = 5376
    assert len(parent.source.namespace()['layout']['SAM']) == m
    # The rank-N entropy bound uses lambda_max >= <anchor|rho|anchor>,
    # so the anchor need not lie in the span of the actual vertex states.
    # h2(q0) <= q0*(124+2), since ln(2)>1/2 and
    # -(1-q0)ln(1-q0)<=q0. Monotonicity applies below q0=2^-124.
    entropy_upper = F(m+124+2, 1 << 124)
    assert entropy_upper < F(1, 1 << 111)
    assert 1-q > F(1, 2)
    # All records/environment/clock degrees belong in d, NOT in a free
    # implicit archive. Check integer qubit implications without rounding.
    d1_threshold = (1-q)*(1 << m)
    assert (1 << (m-1)) < d1_threshold <= (1 << m)
    assert 9*(1 << (m-4)) < d1_threshold < 9*(1 << (m-3))
    return {'SOURCE_error_lt':'2^-3423', 'full_bank_M1':int(M1),
            'CODE_vertex_radius_lt':104, 'sigma':'2^-80',
            'uniform_actual_near_product_delta_lt':'2^-62',
            'bank_anchor_loss_lt':'2^-124', 'CODE_bits':m,
            'all_input_capacity':'2^b*d >= (1-delta^2)*2^5376',
            'record_qubits_if_total_side_d_equals_1_at_least':5376,
            'record_qubits_if_total_side_d_equals_9_at_least':5373,
            'd_equals_9_is_an_example_not_actual_history_clock':True,
            'canonical_pure_SOURCE_bank_entropy_bits_lt':'2^-111',
            'entropy_value_bound_is_not_source_bound':True}


def rotation(t):
    return s.Matrix([[(1-t*t)/(1+t*t),-2*t/(1+t*t)],
                     [2*t/(1+t*t),(1-t*t)/(1+t*t)]])


def finite_actual_model():
    # Four arbitrary CODE inputs, one fixed bank input.  Perturb CODE
    # before the controlled SOURCE, so the actual target is not diagonal
    # in CODE; no rare Born-conditional vector division is permitted.
    n = 4
    controlled = s.diag(*(rotation(s.Rational(j-1,100)) for j in range(n)))
    code = s.diag(rotation(s.Rational(1,1000)),s.eye(2))
    actual = controlled*s.kronecker_product(code,s.eye(2))
    assert actual.T*actual == s.eye(2*n)
    J = s.zeros(2*n,n)
    for j in range(n): J[2*j,j] = 1
    V = actual*J
    assert V.T*V == s.eye(n)
    Q = J*J.T
    assert Q*Q == Q and s.trace(Q) == n
    defect = s.simplify(s.trace((V-J).T*(V-J)))
    assert 0 < defect < s.Rational(1,64)
    projected = V.T*Q*V
    for j in range(n):
        assert projected[j,j] >= 1-defect
    assert n*(1-defect) <= s.trace(projected) <= n
    assert n*(1-defect) > n-1
    # An explicit bank change can store every label in BANK and zero the
    # separate record. It has a reversible decoder, but fails preservation
    # of the specified bank projector: it is not excluded by the theorem.
    swap = s.zeros(n*n)
    for a in range(n):
        for b in range(n): swap[b*n+a,a*n+b] = 1
    assert swap.T*swap == s.eye(n*n)
    for x in range(n):
        inp = s.eye(n*n)[:,x*n]
        out = swap*inp
        assert out == s.eye(n*n)[:,x]
        assert swap*out == inp
    return {'orthogonal_CODE_inputs':n,'full_CODE_bank_unitary_dimension':2*n,
            'actual_CODE_mixing_included':True,
            'rational_Frobenius_defect_lt':'1/64',
            'projector_trace_capacity_bound_exact':True,
            'reversible_bank_storage_countercontrol':True,
            'one_fixed_superposition_alone_used_to_infer_capacity':False}


def pure_bank_overlap_control():
    # Ideal pointwise bank preservation has the sharper exact Gram rule.
    # Products below are nonzero; hence isometry of orthogonal record
    # inputs forces all distinct output code vectors to be orthogonal.
    states = [rotation(s.Rational(j-1,100))*s.Matrix([1,0]) for j in range(4)]
    for x in states: assert (x.T*x)[0] == 1
    overlaps = [(states[j].T*states[k])[0] for j in range(4) for k in range(j+1,4)]
    assert all(z > s.Rational(99,100) for z in overlaps)
    # Same-spectrum does not imply a bound on finite differences after
    # division by the physical gain; no such inference is tested/claimed.
    return {'pairwise_nonzero_exact_bank_overlaps':len(overlaps),
            'pointwise_pure_bank_preservation_requires_orthogonal_codes':True,
            'actual_rare_CODE_conditional_states_claimed_uniformly_close':False}


def main():
    checks = {'status':'PASS_ACTUAL_SOURCE_BANK_PRESERVING_CAPACITY_BOUND',
              'production':production_bounds(),
              'exact_noncommuting_fixture':finite_actual_model(),
              'ideal_pure_bank_gram_control':pure_bank_overlap_control(),
              'physical_Info_selected':False,'physical_Cost_intertwiner_proved':False,
              'physical_C_closed':False,'GR_closed':False}
    paths = [Path(__file__), D/'round47/full_vector_controls.py',
             D/'round47/FULL_VECTOR_CONTROL_CHECK.json',
             D/'round54/regular_global_source.py',
             D/'round54/REGULAR_GLOBAL_SOURCE_RU.md',
             D/'round55/regular_comparison_task.py',
             D/'round55/REGULAR_FIELD_TASK_AND_FRONTIERS_RU.md',
             D/'round58/RESULT.json',D/'round59/RESULT.json']
    for receipt in (D/'round47/FULL_VECTOR_CONTROL_CHECK.json',):
        for name,digest in json.loads(receipt.read_text())['source_sha256'].items():
            assert sha256(Path(name).read_bytes()).hexdigest()==digest
    checks['input_sha256'] = {str(q):sha256(q.read_bytes()).hexdigest() for q in paths}
    (P/'SOURCE_RECORD_CAPACITY_CHECK.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(checks['status'])


if __name__=='__main__': main()
