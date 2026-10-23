#!/usr/bin/env python3
"""Exact real fast-source coercivity and the full frozen quartic readout.

All eight owned center amplitudes are retained. A real discriminant removes
the apparent one-dimensional source kernel. Literal polynomial jets include
the cubic normal correction before extracting the ten mean metric slots.
This is a frozen identity-chart result, not a full fixed-source theorem.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import time
import numpy as np
from flint import fmpq, fmpq_mpoly_ctx
import a4d_identity_quarter_nonlinear_response_check as N
from a4d_designated_full_gap_check import QI

HERE = Path(__file__).resolve().parent
SOURCE_BLOBS = {
    'a4d_identity_quarter_nonlinear_response_check.py': '55d2268c12049e613a4cb07be7744c980a6eac97',
    'a4d_identity_quarter_nonlinear_response_results.json': '481db19fe7f42daf470ed8caea3af358ea8ff91f',
    'a4d_designated_full_gap_check.py': 'a843847c4c169da6dba98e9608fc265fac534d56'
}
XI = [F(x) for x in (3, 1, 1, 1, 1, 1, -1, 1)]
LEFT_INVERSE = [['2', '3/2', '3/2', '1/2', '2', '1', '0', '2', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'], ['1', '1', '0', '0', '1', '0', '0', '0', '0', '0'], ['1', '0', '1', '0', '0', '0', '0', '1', '0', '0'], ['2', '1', '1', '1', '1', '1', '0', '1', '0', '0'], ['1', '1/2', '1/2', '1/2', '1', '0', '0', '0', '0', '0'], ['-1', '-1/2', '-1/2', '-1/2', '0', '0', '0', '-1', '0', '0'], ['2', '3/2', '3/2', '1/2', '1', '1', '0', '1', '0', '0']]
L = [[F(x) for x in row] for row in LEFT_INVERSE]

def literal_polynomial_readout():
    start=time.monotonic()
    root=HERE
    owned=json.loads((root/'a4d_identity_quarter_nonlinear_response_results.json').read_text())
    ctx=fmpq_mpoly_ctx.get(('a0','a1','a2','a3','b0','b1','b2','b3'))
    x=ctx.gens();Z=x[0]*0;ONE=Z+1

    def rat(v):
        q=F(v);return fmpq(q.numerator,q.denominator)

    def zm():return [[Z for _ in range(4)] for _ in range(4)]
    I=[[ONE if i==j else Z for j in range(4)] for i in range(4)]

    def add(a,b):return [[a[i][j]+b[i][j] for j in range(4)] for i in range(4)]
    def scale(a,k):return [[v*k for v in row] for row in a]
    def mm(a,b):
        c=zm()
        for i in range(4):
            for k in range(4):
                if a[i][k]:
                    for j in range(4):
                        if b[k][j]:c[i][j]+=a[i][k]*b[k][j]
        return c
    def jconst(a,d=4):return [a]+[zm() for _ in range(d)]
    def jmul(a,b):
        n=len(a)-1;c=[zm() for _ in range(n+1)]
        for k in range(n+1):
            for j in range(k+1):c[k]=add(c[k],mm(a[j],b[k-j]))
        return c
    def jexp(a):
        n=len(a)-1;out=jconst(I,n);power=jconst(I,n);factor=1
        for k in range(1,n+1):
            power=jmul(power,a);factor*=k
            for d in range(n+1):out[d]=add(out[d],scale(power[d],fmpq(1,factor)))
        return out
    def jinv(a):return [[[a[d][j][i]*N.SIG[i]*N.SIG[j] for j in range(4)] for i in range(4)] for d in range(len(a))]
    def contracted(a,b):return sum((a[i][j]*rat(b[i,j]) for i in range(4) for j in range(4) if b[i,j]),Z)
    def constant(a):return [[Z+rat(a[i,j]) for j in range(4)] for i in range(4)]
    gen=[constant(a) for a in N.G]
    weight=[constant(a) for a in N.WEIGHT]

    logs=[[jconst(zm()) for r in range(4)] for p in range(4)]
    for p in range(4):
        for r in range(4):
            amplitude=(x[r],x[r+4],-x[r],-x[r+4])[p]
            logs[p][r][1]=scale(constant(N.T[r]),amplitude)
    for m,row in zip(owned['quadratic_monomials'],owned['quadratic_normal_coefficients']):
        v=x[m[0]]*x[m[1]]
        for p in range(4):
            for r in range(4):
                for j in range(6):
                    q=F(row[24*p+6*r+j])
                    if q:logs[p][r][2]=add(logs[p][r][2],scale(gen[j],v*rat(q)))

    def euler(logs,connection=True):
        links=[[jexp(logs[p][r]) for r in range(4)] for p in range(4)]
        eq=[[Z for _ in range(10)] for _ in range(4)]
        ek=[[Z for _ in range(24)] for _ in range(4)]
        eq3=[[Z for _ in range(10)] for _ in range(4)]
        for p in range(4):
            for face,(r,s) in enumerate(N.PAIRS):
                loc=[(p,r,False),((p+1)%4,s,False),((p+1)%4,r,True),(p,s,True)]
                fac=[jinv(links[a][b]) if inv else links[a][b] for a,b,inv in loc]
                pref=[jconst(I)]
                for f in fac:pref.append(jmul(pref[-1],f))
                for metric in range(10):
                    eq[p][metric]+=contracted(pref[4][4],N.DWEIGHT[face][metric])
                    if connection:eq3[p][metric]+=contracted(pref[4][3],N.DWEIGHT[face][metric])
                if not connection:continue
                suf=[None]*5;suf[4]=jconst(I)
                for i in range(3,-1,-1):suf[i]=jmul(fac[i],suf[i+1])
                wt=[[weight[face][j][i] for j in range(4)] for i in range(4)]
                for i,(a,b,inv) in enumerate(loc):
                    co=jmul(suf[i+1],[mm(wt,v) for v in pref[i]])
                    jet=jmul(fac[i],co) if inv else jmul(co,fac[i])
                    for j in range(6):
                        transpose=[[jet[3][v][u] for v in range(4)] for u in range(4)]
                        ek[a][6*b+j]+=(-1 if inv else 1)*contracted(transpose,N.G[j])
        mean=[sum((eq[p][j] for p in range(4)),Z)*fmpq(1,4) for j in range(10)]
        return mean,[ek[p]+eq3[p] for p in range(4)]

    bare,source=euler(logs)
    cols,B=N.quarter_reduction()
    re=[(source[0][j]-source[2][j])*fmpq(1,4) for j in range(34)]
    im=[(-source[1][j]+source[3][j])*fmpq(1,4) for j in range(34)]
    project=[]
    for row in B:
        a=sum((rat(v.re)*re[j]-rat(v.im)*im[j] for j,v in enumerate(row)),Z)
        b=sum((rat(v.re)*im[j]+rat(v.im)*re[j] for j,v in enumerate(row)),Z)
        project.append((a,b))
    for o in range(28):
        expected=Z
        for m,row in zip(owned['cubic_monomials'],owned['cubic_gate_coefficients']):
            expected+=rat(row[o])*x[m[0]]*x[m[1]]*x[m[2]]
        actual=project[20+o%14][o//14]
        assert actual==expected
    for j,col in enumerate(cols):
        wr,wi=project[j]
        co=[-2*wr,2*wi,2*wr,-2*wi]
        for p in range(4):logs[p][col//6][3]=add(logs[p][col//6][3],scale(gen[col%6],co[p]))
    complete,_=euler(logs,connection=False)
    data={'monomials':[], 'coefficients':[], 'bare_coefficients':[]}
    mon=sorted(set().union(*(set(v.to_dict()) for v in complete+bare)))
    for m in mon:
        assert sum(m)==4
        data['monomials'].append([int(k) for k in m])
        data['coefficients'].append([str(v.to_dict().get(m,0)) for v in complete])
        data['bare_coefficients'].append([str(v.to_dict().get(m,0)) for v in bare])
    return data


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def moments(c):
    a, b = c[:4], c[4:]
    return [a[0]*(a[1]-a[2]+a[3])-b[0]*(b[1]-b[2]+b[3]),
            a[0]*b[0], a[1]*b[1], a[2]*b[2], a[3]*b[3],
            a[0]*b[1]+a[1]*b[0], a[0]*b[2]+a[2]*b[0],
            a[0]*b[3]+a[3]*b[0]]


def evaluate(data, c, field='coefficients'):
    out = [F(0)]*10
    for powers, row in zip(data['monomials'], data[field]):
        v = F(1)
        for j, p in enumerate(powers):
            v *= c[j]**p
        if v:
            out = [x+v*F(y) for x, y in zip(out, row)]
    return out


def source_coercivity(owned):
    matrix = [[F(x) for x in row] for row in owned['quadratic_gate_matrix']]
    assert all(dot(row, XI) == 0 for row in matrix)
    assert all(sum(L[i][o]*matrix[o][j] for o in range(10))
               == F(i == j)-XI[i]*F(j == 1)
               for i in range(8) for j in range(8))
    # An arbitrary nonzero vector on ker(M) violates the real discriminant.
    assert XI[5]**2-4*XI[1]*XI[2] == -3
    gate_columns = [sum(abs(L[i][j]) for i in range(8))
                    +F(40, 3)*(abs(L[5][j])+abs(L[2][j]))
                    for j in range(10)]
    phase_columns = [F(52, 3)*(abs(L[5][j])+abs(L[2][j]))
                     +2*sum(abs(L[i][j]) for i in (2, 3, 4))
                     +sum(abs(L[i][j]) for i in (5, 6, 7))
                     for j in range(10)]
    assert max(gate_columns) == F(110, 3)
    assert max(phase_columns) == F(140, 3)
    ctx = fmpq_mpoly_ctx.get(tuple('x'+str(j) for j in range(8)))
    x = ctx.gens()
    t = moments(x)
    for j in range(1, 4):
        assert (x[0]*x[j+4]-x[j]*x[4])**2 == t[j+4]**2-4*t[1]*t[j+1]
    for m, row in zip(owned['quadratic_monomials'], owned['quadratic_gate_coefficients']):
        powers = tuple(m.count(j) for j in range(8))
        for o in range(10):
            actual = sum((t[i]*fmpq(matrix[o][i].numerator, matrix[o][i].denominator)
                          for i in range(8)), x[0]*0).to_dict().get(powers, 0)
            assert F(str(actual)) == F(row[o])
    return matrix


def factor_readout(data):
    assignment = []
    factors = {}
    for m, row in zip(data['monomials'], data['coefficients']):
        if not any(F(v) for v in row):
            continue
        a = [i for i in range(4) if m[i]]
        b = [i for i in range(4) if m[4+i]]
        assert a and b, 'pure-parity mean response must vanish at degree four'
        pairs = [(i, j) for i in a for j in b]
        controlled = [p for p in pairs if 0 in p or p[0] == p[1]]
        pair = min(controlled or pairs)
        residual = m[:]
        residual[pair[0]] -= 1
        residual[4+pair[1]] -= 1
        assert min(residual) >= 0 and sum(residual) == 2
        reconstructed = residual[:]
        reconstructed[pair[0]] += 1
        reconstructed[4+pair[1]] += 1
        assert reconstructed == m
        factors[pair, tuple(residual)] = [F(x) for x in row]
        assignment.append([list(pair), residual])
    norms = {(i, j): sum(sum(abs(v) for v in row)
                         for (pair, m), row in factors.items() if pair == (i, j))
             for i in range(4) for j in range(4)}
    free = max(v for (i, j), v in norms.items() if i and j and i != j)
    controlled = max(v for (i, j), v in norms.items() if not(i and j and i != j))
    assert free == F(99, 8) and controlled == F(459, 4)
    assert controlled*F(140, 3) == 5355
    return assignment, [[str(norms[i, j]) for j in range(4)] for i in range(4)]


def numeric_literal_readout(c):
    """Independent Fraction/NumPy Euler replay, rather than polynomial evaluation."""
    cols, transform = N.quarter_reduction()
    w2, q2 = N.quadratic(c)
    logs = N.logs_of(c, 4, w2)
    ek, eq = N.euler(logs)
    assert not np.any(ek[:3])
    assert not np.any(sum(eq[:3, p, :] for p in range(4)))
    source = np.concatenate((ek[3], eq[3]), axis=1)
    fourier = np.array([QI((F(source[0, j])-F(source[2, j]))/4,
                          (-F(source[1, j])+F(source[3, j]))/4)
                       for j in range(34)], dtype=object)
    reduced = transform@fourier
    bare = [F(x) for x in sum(eq[4])/4]
    w3 = [QI() for _ in range(24)]
    for k, col in enumerate(cols):
        w3[col] = -reduced[k]
    for p in range(4):
        coefficients = [2*x.re if p == 0 else -2*x.im if p == 1
                        else -2*x.re if p == 2 else 2*x.im for x in w3]
        for r in range(4):
            logs[p, r, 3] = sum(coefficients[6*r+j]*N.G[j] for j in range(6))
    ek, eq = N.euler(logs)
    source = np.concatenate((ek[3], eq[3]), axis=1)
    complete = transform@np.array([
        QI((F(source[0, j])-F(source[2, j]))/4,
           (-F(source[1, j])+F(source[3, j]))/4) for j in range(34)], dtype=object)
    assert not any(complete[:20])
    assert all(x == y for x, y in zip(complete[20:], reduced[20:]))
    # C(1)=0 kills the still-unsolved fourth-order normal contribution to the mean.
    assert not np.any(N.C0)
    return [F(x) for x in sum(eq[4])/4], bare, [F(x) for x in q2]


def raw_grid(data, matrix):
    rho = F(0)
    metric = source = cross = gate = F(0)
    controlled_phase = F(0)
    for x in product(range(4), repeat=4):
        c = [F(((j+2)*(x[0]+2*x[1]+3*x[2]+5*x[3])+j*j+x[1]*x[2]) % 13-6,
               19+j) for j in range(8)]
        rho = max(rho, *(abs(v) for v in c))
        t = moments(c)
        q = [dot(row, t) for row in matrix]
        w = [dot(row, q) for row in L]
        assert t == [XI[i]*t[1]+w[i] for i in range(8)]
        assert 3*t[1]**2 <= 2*t[1]*(w[5]-2*w[2])+w[5]**2
        assert abs(t[1]) <= F(4, 3)*(abs(w[5])+abs(w[2]))
        assert sum(abs(v) for v in t) <= F(110, 3)*sum(abs(v) for v in q)
        phase = sum(abs(c[i]*c[j+4]) for i in range(4) for j in range(4)
                    if 0 in (i, j) or i == j)
        assert phase <= F(140, 3)*sum(abs(v) for v in q)
        controlled_phase += phase
        metric += sum(abs(v) for v in evaluate(data, c))
        source += sum(abs(v) for v in q)
        gate += sum(abs(v) for v in t)
        cross += sum(abs(c[i]*c[j+4]) for i in range(1, 4) for j in range(1, 4) if i != j)
    bound = rho**2*(F(99, 8)*cross+5355*source)
    assert gate <= F(110, 3)*source and controlled_phase <= F(140, 3)*source
    assert metric <= bound
    return {'shape': [4]*4, 'sites': 256, 'rho': str(rho),
            'quartic_metric_raw1': str(metric), 'fast_quadratic_source_raw1': str(source),
            'eight_moments_raw1': str(gate), 'controlled_phase_products_raw1': str(controlled_phase),
            'six_cross_phase_products_raw1': str(cross), 'readout_bound': str(bound)}


def run_checks():
    for name, sha in SOURCE_BLOBS.items():
        content = (HERE/name).read_bytes()
        assert hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest() == sha
    owned = json.loads((HERE/'a4d_identity_quarter_nonlinear_response_results.json').read_text())
    matrix = source_coercivity(owned)
    data = literal_polynomial_readout()
    assert len(data['monomials']) == 224
    assignment, norms = factor_readout(data)
    points = [[0,0,1,-1,0,0,0,0], [0,0,0,0,0,0,1,-1],
              [0,1,0,0,0,0,1,0], [0,0,1,0,0,-1,0,0],
              [F(j-3, j+2) for j in range(8)]]
    controls = []
    for c in points:
        c = [F(x) for x in c]
        literal, bare, q2 = numeric_literal_readout(c)
        assert literal == evaluate(data, c)
        assert bare == evaluate(data, c, 'bare_coefficients')
        assert q2 == [dot(row, moments(c)) for row in matrix]
        controls.append({'amplitudes': [str(x) for x in c], 'source_Q2': [str(x) for x in q2],
                         'complete_mean_metric_degree4': [str(x) for x in literal],
                         'W2_only_mean_metric_degree4': [str(x) for x in bare]})
    assert all(x == '0' for x in controls[0]['complete_mean_metric_degree4'])
    assert controls[0]['complete_mean_metric_degree4'] == controls[1]['complete_mean_metric_degree4']
    visible = ['1/16','0','0','-1/8','0','0','0','0','0','1/16']
    assert controls[2]['complete_mean_metric_degree4'] == visible
    assert controls[3]['complete_mean_metric_degree4'] == visible
    assert controls[2]['W2_only_mean_metric_degree4'] != visible
    assert all(x == '0' for x in controls[2]['source_Q2'])
    # Symmetric rational amplitude laws have identical means/covariances,
    # zero averaged quadratic/cubic gates, and different quartic readouts.
    c = [F(x) for x in points[2]]
    laws = [[(F(1, 2), c), (F(1, 2), [-x for x in c])],
            [(F(1, 8), [2*x for x in c]), (F(1, 8), [-2*x for x in c]),
             (F(3, 4), [F(0)]*8)]]
    first = [[sum(w*z[i] for w, z in law) for i in range(8)] for law in laws]
    second = [[[sum(w*z[i]*z[j] for w, z in law) for j in range(8)]
               for i in range(8)] for law in laws]
    assert first[0] == first[1] == [F(0)]*8 and second[0] == second[1]
    mean_metric = [[sum(w*evaluate(data, z)[j] for w, z in law)
                    for j in range(10)] for law in laws]
    assert mean_metric[0] == [F(x) for x in visible]
    assert mean_metric[1] == [4*F(x) for x in visible]
    for law in laws:
        assert all(sum(w*dot(matrix[j], moments(z)) for w, z in law) == 0
                   for j in range(10))
        for j in range(28):
            assert sum(w*sum(F(row[j])*z[m[0]]*z[m[1]]*z[m[2]]
                             for m, row in zip(owned['cubic_monomials'],
                                               owned['cubic_gate_coefficients']))
                       for w, z in law) == 0
    grid = raw_grid(data, matrix)
    print('PASS_REAL_SOURCE_IMAGE_COERCIVITY_AND_10_PHASE_PRODUCTS', flush=True)
    print('PASS_FULL_QUARTIC_READOUT_W3_AND_INDEPENDENT_DENSE_EULER', flush=True)
    print('PASS_SIX_CROSS_PHASE_BOUND_RAW_256_SITE_AND_HOSTILE_CONTROLS', flush=True)
    return {
        'arithmetic': 'exact Q polynomial jets via FLINT; independent Fraction/Q(i) Euler controls',
        'model': 'eta, owned eight quarter centers and the analytic normal graph; mean metric degree four',
        'source_blobs': SOURCE_BLOBS,
        'amplitude_order': ['a0','a1','a2','a3','b0','b1','b2','b3'],
        'packed_metric_slots': ['00','01','02','03','11','12','13','22','23','33'],
        'source_gate_matrix': [[str(x) for x in row] for row in matrix],
        'kernel_vector': [str(x) for x in XI], 'left_inverse': LEFT_INVERSE,
        'kernel_real_discriminant': '-3',
        'raw_eight_moment_bound_constant': '110/3',
        'raw_controlled_phase_bound_constant': '140/3',
        'uncontrolled_phase_products': [[i,j] for i in range(1,4) for j in range(1,4) if i != j],
        'quartic_readout_monomial_powers': data['monomials'],
        'complete_quartic_readout_coefficients': data['coefficients'],
        'full_cubic_owner_coefficients_checked': 120*28,
        'pure_parity_quartic_readout_zero': True,
        'quartic_factor_assignments': assignment,
        'quadratic_factor_coefficient_norms': norms,
        'raw_six_cross_phase_bound_constant': '99/8',
        'raw_fast_source_readout_bound_constant': '5355',
        'literal_controls': controls, 'raw_grid': grid,
        'two_laws_same_first_and_second_moments': True,
        'two_laws_zero_averaged_quadratic_and_cubic_gates': True,
        'two_laws_quartic_metric_means': [[str(v) for v in row] for row in mean_metric],
        'hostile_second_moment_only_readout_rejected': True,
        'hostile_omit_cubic_normal_correction_rejected': True,
        'hostile_linear_source_kernel_is_not_realizable': True,
        'verdict': 'REAL-FAST-SOURCE-COERCIVITY-AND-QUARTIC-READOUT-QUOTIENT-CERTIFIED',
        'nonclaims': [
            'No exact stationary family is constructed by these source-zero amplitude controls.',
            'Pure-parity invisibility is a degree-four mean-readout identity, not an all-order assertion.',
            'The six products require their quadratic correlations; they are not a complete six-number memory.',
            'The probability laws are algebraic moment controls, not realizable stationary lattice fields.',
            'No exact full-link, varying-coframe, all-frequency or fixed-source parent convergence is asserted.'
        ]
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-json', action='store_true')
    args = parser.parse_args()
    report = run_checks()
    target = Path(__file__).with_name('a4d_full_quartic_source_quotient_results.json')
    if args.write_json:
        target.write_text(json.dumps(report, indent=2)+'\n')
    else:
        assert json.loads(target.read_text()) == report, 'pinned quartic quotient ledger changed'
    print('PASS_PINNED_FULL_QUARTIC_SOURCE_QUOTIENT_LEDGER')
