#!/usr/bin/env python3
"""Exact saturated readout identity on the owned full-eight frozen reduction.

The ten mean quartic slots are controlled pointwise by the full real fast
source and the common first-slow transport-annihilating cubic rows. This
is not a full-link, variable-coframe or analytic-remainder theorem.
"""
from __future__ import annotations
from pathlib import Path
from itertools import combinations_with_replacement, product as cartesian_product
from fractions import Fraction as F
import argparse
import hashlib
import json
from flint import fmpq, fmpq_mat

FILES = (
    'a4d_identity_quarter_nonlinear_response_results.json',
    'a4d_full_quartic_source_quotient_results.json',
    'a4d_spatial_transport_entropy_results.json',
)
SOURCE_BLOBS = {
    'a4d_identity_quarter_nonlinear_response_results.json': '481db19fe7f42daf470ed8caea3af358ea8ff91f',
    'a4d_full_quartic_source_quotient_results.json': '238f0e94aefb5dceb012f355199560e56e591977',
    'a4d_spatial_transport_entropy_results.json': '0c71395b5299453fd53297c14f1995ee4afb272d',
}
PAIRS = [(i,j) for i in range(4) for j in range(4)
         if i == j or i == 0 or j == 0]
M2 = list(combinations_with_replacement(range(8), 2))
M3 = list(combinations_with_replacement(range(8), 3))
M5 = list(combinations_with_replacement(range(8), 5))


def dot(a,b):
    return sum((x*y for x,y in zip(a,b)), F(0))


def add_into(a,m,v):
    a[m] = a.get(m,F(0))+v
    if not a[m]:
        del a[m]


def multiply(a,b):
    out = {}
    for m,x in a.items():
        for n,y in b.items():
            add_into(out,tuple(sorted(m+n)),x*y)
    return out


def vector_polynomials(monomials,coefficients,width):
    out = [{} for _ in range(width)]
    for m,row in zip(monomials,coefficients):
        for j,v in enumerate(row):
            if F(v):
                add_into(out[j],tuple(m),F(v))
    return out


def right_nullspace(rows,width):
    rr,rank = fmpq_mat([[fmpq(x.numerator,x.denominator) for x in row]
                       for row in rows]).rref()
    pivots = [next(j for j in range(width) if rr[i,j]) for i in range(rank)]
    result = []
    for free in range(width):
        if free in pivots:
            continue
        v = [F(0)]*width
        v[free] = F(1)
        for i,j in enumerate(pivots):
            v[j] = -F(str(rr[i,free]))
        assert all(dot(row,v) == 0 for row in rows)
        result.append(v)
    return result,rank


def polynomial_coefficients(c):
    return [[list(m),str(v)] for m,v in sorted(c.items()) if v]


def decode_polynomial(c):
    return {tuple(m):F(v) for m,v in c}


def evaluate(poly,c):
    return sum((v*product(c[i] for i in m) for m,v in poly.items()),F(0))


def product(values):
    out = F(1)
    for value in values:
        out *= value
    return out


def run_checks(root):
    owned,readout,transport = [json.loads((root/name).read_text()) for name in FILES]
    blobs = {}
    for name in FILES:
        b = (root/name).read_bytes()
        blobs[name] = hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    assert blobs == SOURCE_BLOBS, 'owned source ledger changed'
    Q3 = vector_polynomials(owned['cubic_monomials'],
                            owned['cubic_gate_coefficients'],28)
    powers = readout['quartic_readout_monomial_powers']
    mon4 = [tuple(i for i,n in enumerate(p) for _ in range(n)) for p in powers]
    R4 = vector_polynomials(mon4,readout['complete_quartic_readout_coefficients'],10)
    G = [[[F(v) for v in row] for row in matrix]
         for matrix in transport['first_slow_full_gamma']]
    stacked = [[G[mu][j][col] for j in range(28)]
               for mu in range(4) for col in range(8)]
    N,rank_G = right_nullspace(stacked,28)
    assert rank_G == 12 and len(N) == 16
    for mu in range(4):
        for n in N:
            for col in range(8):
                assert dot(n,[G[mu][j][col] for j in range(28)]) == 0
    NQ3 = []
    for n in N:
        pol = {}
        for j in range(28):
            for m,v in Q3[j].items():
                add_into(pol,m,n[j]*v)
        NQ3.append(pol)
    t0 = {(0,1):F(1),(0,2):F(-1),(0,3):F(1),
          (4,5):F(-1),(4,6):F(1),(4,7):F(-1)}
    phase = [{tuple(sorted((i,4+j))):F(1)} for i,j in PAIRS]
    def is_controlled(m):
        return any(i in m and 4+j in m for i,j in PAIRS)
    good = [m for m in M5 if not is_controlled(m)]
    index = {m:i for i,m in enumerate(good)}
    assert len(good) == 172
    cols = []
    labels = []
    for m in M3:
        cols.append(multiply(t0,{m:F(1)})); labels.append(('t0',m))
    for n,pol in enumerate(NQ3):
        for m in M2:
            cols.append(multiply(pol,{m:F(1)})); labels.append(('N',n,m))
    k = len(cols)
    assert k == 696
    target = [multiply({(i,):F(1)},pol) for i in range(8) for pol in R4]
    mat = [[fmpq(0)]*(k+80) for _ in good]
    for j,pol in enumerate(cols+target):
        for m,v in pol.items():
            if m in index:
                mat[index[m]][j] = fmpq(v.numerator,v.denominator)
    rr,rank = fmpq_mat(mat).rref()
    pivots = [next(j for j in range(k+80) if rr[i,j]) for i in range(rank)]
    assert rank == 144 and all(j < k for j in pivots)
    solutions = [[F(0)]*k for _ in range(80)]
    for row,pivot in enumerate(pivots):
        for t in range(80):
            solutions[t][pivot] = F(str(rr[row,k+t]))
    witnesses = []
    constants = []
    for i in range(8):
        source_t0 = F(0)
        source_phase = [F(0)]*10
        cubic_columns = [F(0)]*28
        for j in range(10):
            target_index = 10*i+j
            residual = target[target_index].copy()
            a = {}
            b = [{} for _ in N]
            for coefficient,col,label in zip(solutions[target_index],cols,labels):
                if not coefficient:
                    continue
                for m,v in col.items():
                    add_into(residual,m,-coefficient*v)
                if label[0] == 't0':
                    add_into(a,label[1],coefficient)
                else:
                    add_into(b[label[1]],label[2],coefficient)
            assert all(is_controlled(m) for m in residual)
            controlled = [{} for _ in PAIRS]
            for m,v in sorted(residual.items()):
                pair = next(n for n,(r,s) in enumerate(PAIRS) if r in m and 4+s in m)
                r,s = PAIRS[pair]
                rest = list(m);rest.remove(r);rest.remove(4+s)
                add_into(controlled[pair],tuple(rest),v)
            # Coefficientwise replay of the complete degree-five identity.
            reconstructed = multiply(t0,a)
            for pol,multiplier in zip(NQ3,b):
                for m,v in multiply(pol,multiplier).items():
                    add_into(reconstructed,m,v)
            for pol,multiplier in zip(phase,controlled):
                for m,v in multiply(pol,multiplier).items():
                    add_into(reconstructed,m,v)
            assert reconstructed == target[target_index]
            source_t0 += sum(abs(v) for v in a.values())
            for n,multiplier in enumerate(controlled):
                source_phase[n] += sum(abs(v) for v in multiplier.values())
            # Combine annihilator multipliers into actual 28 joint-row multipliers.
            direct = [{} for _ in range(28)]
            for n,multiplier in zip(N,b):
                for row in range(28):
                    for m,v in multiplier.items():
                        add_into(direct[row],m,n[row]*v)
            for row,pol in enumerate(direct):
                cubic_columns[row] += sum(abs(v) for v in pol.values())
            # Every quadratic coefficient row annihilates every full8 transport.
            for m in M2:
                coeff = [pol.get(m,F(0)) for pol in direct]
                for mu in range(4):
                    for col in range(8):
                        assert dot(coeff,[G[mu][row][col] for row in range(28)]) == 0
            witnesses.append({'coordinate':i,'metric_slot':j,
                't0_multiplier':polynomial_coefficients(a),
                'annihilator_multipliers':[[n,polynomial_coefficients(pol)]
                    for n,pol in enumerate(b) if pol],
                'controlled_phase_multipliers':[[n,polynomial_coefficients(pol)]
                    for n,pol in enumerate(controlled) if pol]})
        constants.append({'coordinate':i,'t0_norm':str(source_t0),
                          'phase_norm':str(max(source_phase)),
                          'cubic_row_norm':str(max(cubic_columns)),
                          'source_norm':str(F(110,3)*source_t0+F(140,3)*max(source_phase))})
    C3 = max(F(v['cubic_row_norm']) for v in constants)
    C2 = max(F(v['source_norm']) for v in constants)
    # Existing source bounds are real-image statements; their pin is part of the input.
    assert readout['raw_eight_moment_bound_constant'] == '110/3'
    assert readout['raw_controlled_phase_bound_constant'] == '140/3'
    # Pointwise memory laws: averaged cubic gates are insufficient, but the actual
    # annihilator gate at the visible atom is nonzero and controls its readout.
    c = [F(0),F(1),F(0),F(0),F(0),F(0),F(1),F(0)]
    assert all(evaluate(pol,c) == 0 for pol in vector_polynomials(
        owned['quadratic_monomials'],owned['quadratic_gate_coefficients'],10))
    assert any(evaluate(pol,c) != 0 for pol in R4)
    assert any(evaluate(pol,c) != 0 for pol in NQ3)
    assert sum(abs(evaluate(pol,c)) for pol in R4) <= C3*sum(abs(evaluate(pol,c)) for pol in Q3)
    # Hostile deletion of the controlled source part and coefficient mutation.
    omit_source = False
    for witness in witnesses:
        i,j = witness['coordinate'],witness['metric_slot']
        only_cubic = {}
        for n,multiplier in witness['annihilator_multipliers']:
            for m,v in multiply(NQ3[n],decode_polynomial(multiplier)).items():
                add_into(only_cubic,m,v)
        if only_cubic != target[10*i+j]:
            omit_source = True
    assert omit_source
    first = next(w for w in witnesses if w['controlled_phase_multipliers'])
    pair,original_multiplier = first['controlled_phase_multipliers'][0]
    multiplier = decode_polynomial(original_multiplier)
    coefficient_monomial = min(multiplier)
    add_into(multiplier,coefficient_monomial,F(1))
    mutated_reconstruction = multiply(t0,decode_polynomial(first['t0_multiplier']))
    for n,mult in first['annihilator_multipliers']:
        for m,v in multiply(NQ3[n],decode_polynomial(mult)).items():
            add_into(mutated_reconstruction,m,v)
    for n,mult in first['controlled_phase_multipliers']:
        actual = multiplier if n == pair else decode_polynomial(mult)
        for m,v in multiply(phase[n],actual).items():
            add_into(mutated_reconstruction,m,v)
    assert mutated_reconstruction != target[10*first['coordinate']+first['metric_slot']]
    # A full-eight rough field gives temporal as well as spatial finite differences.
    # The detector identity is checked pointwise, not by cancelling a signed sum.
    grid = {}
    for site in cartesian_product(range(3),repeat=4):
        grid[site] = [F(((j+2)*(site[0]+2*site[1]+3*site[2]+5*site[3])
                          +j*j+site[1]*site[2]) % 11-5,17+j) for j in range(8)]
    raw_readout = raw_residual = raw_source = F(0)
    rho = max(abs(v) for amplitude in grid.values() for v in amplitude)
    Q2 = vector_polynomials(owned['quadratic_monomials'],owned['quadratic_gate_coefficients'],10)
    for site,amplitude in grid.items():
        residual = [evaluate(pol,amplitude) for pol in Q3]
        for mu in range(4):
            neighbour = list(site);neighbour[mu] = (neighbour[mu]+1)%3
            delta = [v-u for u,v in zip(amplitude,grid[tuple(neighbour)])]
            residual = [v+dot(row,delta) for v,row in zip(residual,G[mu])]
        assert [dot(n,residual) for n in N] == [evaluate(pol,amplitude) for pol in NQ3]
        metric = sum(abs(evaluate(pol,amplitude)) for pol in R4)
        cubic = sum(abs(v) for v in residual)
        source = sum(abs(evaluate(pol,amplitude)) for pol in Q2)
        local_rho = max(abs(v) for v in amplitude)
        assert metric <= C3*local_rho*cubic+C2*local_rho**2*source
        raw_readout += metric;raw_residual += cubic;raw_source += source
    assert raw_readout <= C3*rho*raw_residual+C2*rho**2*raw_source
    print('PASS_ALL80_SATURATED_IDENTITIES_AND_ALL512_NG_ZERO_ENTRIES',flush=True)
    print('PASS_FULL8_POINTWISE_READOUT_BOUND_NO_TEMPORAL_DERIVATIVE',flush=True)
    print('PASS_SOURCE_OMISSION_AND_COEFFICIENT_MUTATION_CONTROLS',flush=True)
    return {'arithmetic':'exact QQ/FLINT coefficientwise linear elimination',
        'model':'full8 frozen quarter reduction; complete ten-slot mean quartic readout',
        'input_git_blobs':blobs,'amplitude_order':readout['amplitude_order'],
        'metric_slots':readout['packed_metric_slots'],'controlled_phase_pairs':[list(p) for p in PAIRS],
        'full_transport_span_rank':rank_G,'common_annihilator_dimension':len(N),'annihilator':[[str(v) for v in row] for row in N],
        'transport_zero_entries_checked':16*4*8,
        'degree5_quotient_monomials':len(good),'degree5_generator_columns':k,
        'degree5_generator_rank':rank,'saturated_identities_checked':80,
        'coordinate_bounds':constants,'raw_C3':str(C3),'raw_C2':str(C2),
        'hostile_full8_grid':{'shape':[3]*4,'sites':81,'rho':str(rho),
            'readout_raw1':str(raw_readout),'reduced_residual_raw1':str(raw_residual),
            'fast_source_raw1':str(raw_source)},
        'identity_witnesses':witnesses,
        'identity_witness_sha256':hashlib.sha256(json.dumps(witnesses,
            sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        'pointwise_bound':'||R4(c)||1 <= C3*rho(c)*||R3(c)||1 + C2*rho(c)^2*||Q2(c)||1',
        'raw_grid_bound':'same constants on arbitrary finite grid and arbitrary componentwise differences',
        'reason':'NG_mu=0 pointwise; divide identity c_i*R4 by a coordinate attaining rho(c)',
        'visible_atom_annihilator_gate_nonzero':True,'source_omission_rejected':True,
        'coefficient_mutation_rejected':True,
        'verdict':'FULL8-FROZEN-QUARTIC-READOUT-CONTROLLED-BY-REAL-JOINT-GATES',
        'nonclaims':['No pullback to full shared links or variable coframe is asserted.',
        'No bound on the analytic O(|c|6) remainder or normal-graph extraction is asserted.',
        'No parent response terminal, source realizability or fixed smooth curved witness is asserted.']}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source-dir',type=Path,default=Path(__file__).resolve().parent)
    ap.add_argument('--output',type=Path)
    args = ap.parse_args()
    result = run_checks(args.source_dir)
    target = args.output or Path(__file__).with_name('a4d_quartic_joint_transport_syzygy_results.json')
    if args.output:
        # The explicit sparse 80-identity witness stays inspectable without
        # four megabytes of formatting-only whitespace.
        target.write_text(json.dumps(result,separators=(',',':'))+'\n')
    else:
        assert json.loads(target.read_text()) == result,'pinned saturated readout ledger changed'
    print('PASS_PINNED_SATURATED_QUARTIC_READOUT_LEDGER')
