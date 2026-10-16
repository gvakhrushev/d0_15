#!/usr/bin/env python3
"""Exact four-phase identity-center reduction for the literal A4D action.

All scalar operations use Q or Q(i); NumPy supplies object-array indexing only.
Reconstructs all 36 quadratic and 120 cubic coefficients, without loading a
coefficient oracle. See A4D_IDENTITY_QUARTER_NONLINEAR_RESPONSE.md for the
analytic blow-up argument, its response estimate and its restricted scope.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json
import argparse
import numpy as np
from a4d_designated_full_gap_check import GEN,PAIRS,SYM,SIG,STAR_MAP,flat_symbols,QI,orient

I=np.eye(4,dtype=object)
G=np.array(GEN,dtype=object)
T=np.array([G[3]-G[4]+G[5],G[1]-G[2]+G[5],G[0]-G[2]+G[4],G[0]-G[1]+G[3]])
TC=np.array([[0,0,0,1,-1,1],[0,1,-1,0,0,1],[1,0,-1,0,1,0],[1,-1,0,1,0,0]],dtype=object)
STAR=np.zeros((6,6),dtype=object)
for col,(row,sign) in enumerate(STAR_MAP): STAR[row,col]=sign
G2=np.diag([SIG[a]*SIG[b] for a,b in PAIRS]).astype(object)

def wedge(a,b): return np.array([a[i]*b[j]-a[j]*b[i] for i,j in PAIRS],dtype=object)

def weight(area):
    area=area@G2@STAR
    out=np.zeros((4,4),dtype=object)
    for x,(a,b) in zip(area,PAIRS): out[a,b]+=x*F(SIG[b],2);out[b,a]-=x*F(SIG[a],2)
    return out

WEIGHT=[];DWEIGHT=[]
for a,b in PAIRS:
    u,v=[i for i in range(4) if i not in (a,b)]
    WEIGHT.append(orient(a,b)*weight(wedge(I[:,u],I[:,v])))
    ds=[]
    for r,s in SYM:
        d=np.zeros((4,4),dtype=object);d[r,s]=F(SIG[r],2);d[s,r]=F(SIG[s],2)
        ds.append(orient(a,b)*weight(wedge(d[:,u],I[:,v])+wedge(I[:,u],d[:,v])))
    DWEIGHT.append(np.array(ds))

def jmul(a,b):
    n=len(a)-1
    c=np.zeros_like(a)
    for k in range(n+1):
        for j in range(k+1): c[k]+=a[j]@b[k-j]
    return c

def jconst(a,d):
    out=np.zeros((d+1,4,4),dtype=object);out[0]=a;return out

def jexp(a):
    n=len(a)-1; out=jconst(I,n); power=out.copy(); factor=1
    for k in range(1,n+1):
        power=jmul(power,a);factor*=k;out+=power*F(1,factor)
    return out

def jinv(a):
    return a.swapaxes(-1,-2)*np.array(SIG,dtype=object)[None,:,None]*np.array(SIG,dtype=object)[None,None,:]

def euler(logs):
    # logs[p,r,degree,4,4].  Right-trivialized connection Euler; metric
    # variations use the true Gram section at identity.
    d=logs.shape[2]-1
    links=np.array([[jexp(logs[p,r]) for r in range(4)] for p in range(4)])
    return euler_links(links)

def euler_links(links):
    d=links.shape[2]-1
    ek=np.zeros((d+1,4,4,6),dtype=object);eq=np.zeros((d+1,4,10),dtype=object)
    for p in range(4):
        for face,(r,s) in enumerate(PAIRS):
            loc=[(p,r,False),((p+1)%4,s,False),((p+1)%4,r,True),(p,s,True)]
            fac=[jinv(links[x,y]) if inv else links[x,y] for x,y,inv in loc]
            prefix=[jconst(I,d)]
            for f in fac: prefix.append(jmul(prefix[-1],f))
            suffix=[None]*5;suffix[4]=jconst(I,d)
            for i in range(3,-1,-1): suffix[i]=jmul(fac[i],suffix[i+1])
            prod=prefix[4]
            for m in range(10):
                for n in range(d+1):eq[n,p,m]+=np.sum(DWEIGHT[face][m]*prod[n])
            for i,(x,y,inv) in enumerate(loc):
                co=jmul(suffix[i+1],WEIGHT[face].T@prefix[i])
                jet=-jmul(fac[i],co) if inv else jmul(co,fac[i])
                for n in range(d+1):
                    for g in range(6):ek[n,x,y,g]+=np.sum(jet[n].T*G[g])
    return ek.reshape(d+1,4,24),eq

def inverse(a):
    n=len(a);b=[[F(x) for x in row]+[F(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        p=next(i for i in range(j,n) if b[i][j]);b[j],b[p]=b[p],b[j]
        v=b[j][j];b[j]=[x/v for x in b[j]]
        for i in range(n):
            if i!=j and b[i][j]:
                v=b[i][j];b[i]=[x-v*y for x,y in zip(b[i],b[j])]
    return np.array([r[n:] for r in b],dtype=object)

def real_matrix(a):
    assert all(not x.im for row in a for x in row)
    return np.array([[x.re for x in row] for row in a],dtype=object)

A0,C0=flat_symbols([1]*4);A2,C2=flat_symbols([-1]*4)
H0INV=inverse(real_matrix(A0).T);H2INV=inverse(real_matrix(A2).T)
C2=real_matrix(C2)

def logs_of(amplitudes,degree=2,correction=None):
    z=np.asarray(amplitudes,dtype=object).reshape(2,4)
    coefficients=np.stack([z[0],z[1],-z[0],-z[1]])
    logs=np.zeros((4,4,degree+1,4,4),dtype=object)
    logs[:,:,1]=coefficients[:,:,None,None]*T[None,:,:,:]
    if correction is not None:
        for p in range(4):
            for r in range(4):logs[p,r,2]=sum(correction[p,6*r+g]*G[g] for g in range(6))
    return logs

def quadratic(amplitudes):
    ek,eq=euler(logs_of(amplitudes))
    assert not np.any(ek[:2]) and not np.any(eq[:2])
    fk=ek[2];fq=eq[2]
    assert not np.any(fk[0]-fk[2]) and not np.any(fk[1]-fk[3])
    k0=sum(fk)/4;k2=(fk[0]-fk[1]+fk[2]-fk[3])/4
    w0=-H0INV@k0;w2=-H2INV@k2
    w=np.array([w0+(-1)**p*w2 for p in range(4)])
    q0=sum(fq)/4;q2=(fq[0]-fq[1]+fq[2]-fq[3])/4+C2@w2
    assert not np.any(q0),q0
    return w,q2

def quarter_reduction():
    a,c=flat_symbols([QI(F(0),F(1))]*4)
    a=[list(x) for x in zip(*a)]
    q=a+c
    columns=[j for j in range(24) if j not in (5,11,16,21)]
    m=[[q[i][j] for j in columns]+[QI.of(i==j) for j in range(34)] for i in range(34)]
    for k in range(20):
        p=next(i for i in range(k,34) if m[i][k]);m[k],m[p]=m[p],m[k]
        z=m[k][k];m[k]=[x/z for x in m[k]]
        for i in range(34):
            if i!=k and m[i][k]:
                z=m[i][k];m[i]=[x-z*y for x,y in zip(m[i],m[k])]
    transform=np.array([row[20:] for row in m],dtype=object)
    assert not any(x for row in m[20:] for x in row[:20])
    return columns,transform


def row_reduce(rows):
    a = [[F(x) for x in row] for row in rows]
    rank = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        z = a[rank][j]
        a[rank] = [x/z for x in a[rank]]
        for i in range(len(a)):
            if i != rank and a[i][j]:
                z = a[i][j]
                a[i] = [x-z*y for x, y in zip(a[i], a[rank])]
        rank += 1
    return a[:rank]


def exact_strings(values):
    out = []
    for x in np.asarray(values, dtype=object).flat:
        assert isinstance(x, (int, F, np.integer)), type(x)
        out.append(str(F(x)))
    return out


def reconstruct_quadratic():
    basis = np.eye(8, dtype=object)
    coefficients = {}
    for i in range(8):
        coefficients[(i, i)] = quadratic(basis[i])
    for i, j in combinations(range(8), 2):
        w, q = quadratic(basis[i]+basis[j])
        coefficients[(i, j)] = (
            w-coefficients[(i, i)][0]-coefficients[(j, j)][0],
            q-coefficients[(i, i)][1]-coefficients[(j, j)][1])
    return coefficients


def cubic(amplitudes, quadratic_coefficients, transform):
    correction = sum(amplitudes[i]*amplitudes[j]*w
                     for (i, j), (w, _) in quadratic_coefficients.items())
    ek, eq = euler(logs_of(amplitudes, 3, correction))
    assert not np.any(ek[:3])
    source = np.concatenate([ek[3], eq[3]], axis=1)
    assert not np.any(source[0]+source[2])
    assert not np.any(source[1]+source[3])
    fourier = np.array([
        QI((F(source[0, j])-F(source[2, j]))/4,
           (-F(source[1, j])+F(source[3, j]))/4)
        for j in range(34)])
    reduced = transform@fourier
    return np.array([x.re for x in reduced[20:]] +
                    [x.im for x in reduced[20:]], dtype=object)


def reconstruct_cubic(quadratic_coefficients, transform):
    basis = np.eye(8, dtype=object)
    coefficients = {}
    evaluate = lambda v: cubic(v, quadratic_coefficients, transform)
    for i in range(8):
        coefficients[(i, i, i)] = evaluate(basis[i])
    for i, j in combinations(range(8), 2):
        plus = evaluate(basis[i]+basis[j])
        plus -= coefficients[(i, i, i)]+coefficients[(j, j, j)]
        minus = evaluate(basis[i]-basis[j])
        minus -= coefficients[(i, i, i)]-coefficients[(j, j, j)]
        coefficients[(i, i, j)] = (plus-minus)/2
        coefficients[(i, j, j)] = (plus+minus)/2
    for i, j, k in combinations(range(8), 3):
        value = evaluate(basis[i]+basis[j]+basis[k])
        for a in (i, j, k):
            value -= coefficients[(a, a, a)]
        for a, b in combinations((i, j, k), 2):
            value -= coefficients[(a, a, b)]+coefficients[(a, b, b)]
        coefficients[(i, j, k)] = value
    return coefficients


def check_linear_and_axes():
    assert not any(bool(x) for row in C0 for x in row)
    for z in (QI.of(1), QI.of(-1), QI(F(0), F(1))):
        a, c = flat_symbols([z]*4)
        a = np.array(a, dtype=object).T
        c = np.array(c, dtype=object)
        for j in range(24):
            logs = np.zeros((4, 4, 2, 4, 4), dtype=object)
            powers = [QI.of(1)]
            for p in range(1, 4):
                powers.append(powers[-1]*z)
            for p in range(4):
                logs[p, j//6, 1] = powers[p].re*G[j % 6]
            ek, eq = euler(logs)
            for p in range(4):
                assert all(ek[1, p, k] == (a[k, j]*powers[p]).re
                           for k in range(24))
                assert all(eq[1, p, k] == (c[k, j]*powers[p]).re
                           for k in range(10))
    # Clear the common Cayley denominator D=4-kappa*t^2 on EVERY
    # link, including the inactive identities.  Each Euler term has four
    # link factors, so the degree-eight jets are the complete D^4 numerator,
    # not a low-order test or a finite sample in the amplitude.
    for role in range(4):
        kappa = -3 if role == 0 else 1
        assert np.array_equal(T[role]@T[role]@T[role], kappa*T[role])
        for parity in (0, 1):
            links = np.array([[jconst(4*I, 8) for _ in range(4)]
                              for _ in range(4)])
            links[:, :, 2] = -kappa*I
            for p, sign in ((parity, 1), (parity+2, -1)):
                links[p, role, 1] = sign*4*T[role]
                links[p, role, 2] = 2*T[role]@T[role]-kappa*I
            ek, eq = euler_links(links)
            assert not np.any(ek) and not np.any(eq)


def quadratic_structure(coefficients):
    # a0..a3,b0..b3; q2 = M*t, with the t-polynomials in the proof memo.
    t = [
        {(0, 1): 1, (0, 2): -1, (0, 3): 1,
         (4, 5): -1, (4, 6): 1, (4, 7): -1},
        {(0, 4): 1}, {(1, 5): 1}, {(2, 6): 1}, {(3, 7): 1},
        {(0, 5): 1, (1, 4): 1},
        {(0, 6): 1, (2, 4): 1},
        {(0, 7): 1, (3, 4): 1}]
    anchors = [(0, 1), (0, 4), (1, 5), (2, 6), (3, 7),
               (0, 5), (0, 6), (0, 7)]
    matrix = np.array([coefficients[m][1] for m in anchors]).T
    for m, (_, value) in coefficients.items():
        assert np.array_equal(value, matrix@np.array([p.get(m, 0) for p in t]))
    kernel = np.array([3, 1, 1, 1, 1, 1, -1, 1])
    assert not np.any(matrix@kernel)
    assert len(row_reduce(matrix)) == 7
    return matrix, kernel


def restrict(coefficients, mapping):
    out = {}
    for monomial, vector in coefficients.items():
        polynomial = {(): F(1)}
        for i in monomial:
            following = {}
            for previous, value in polynomial.items():
                for j, z in enumerate(mapping[i]):
                    if z:
                        key = tuple(sorted(previous+(j,)))
                        following[key] = following.get(key, 0)+value*z
            polynomial = following
        for m, z in polynomial.items():
            if m not in out:
                out[m] = np.zeros(28, dtype=object)
            out[m] += z*vector
    return {m: row for m, row in out.items() if np.any(row)}


def plane_checks(cubic_coefficients):
    planes = []
    for parity in (0, 1):
        mapping = [[0, 0, 0] for _ in range(8)]
        for k, row in enumerate([[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, -1, 1]]):
            mapping[4*parity+k] = row
        planes.append(('temporal_'+str(parity), mapping))
    for phases in product((0, 1), repeat=3):
        mapping = [[0, 0, 0] for _ in range(8)]
        for role, phase in enumerate(phases, 1):
            mapping[4*phase+role][role-1] = 1
        planes.append(('spatial_'+''.join(map(str, phases)), mapping))
    mixed = [(0, 0, 1), (0, 0, 2), (0, 1, 1), (0, 1, 2),
             (0, 2, 2), (1, 1, 2), (1, 2, 2)]
    report = []
    for name, mapping in planes:
        restricted = restrict(cubic_coefficients, mapping)
        columns = sorted(restricted)
        expected = sorted(mixed+([(1, 1, 1), (2, 2, 2)]
                                  if name.startswith('temporal') else []))
        assert columns == expected
        rows = row_reduce(np.array([restricted[m] for m in columns]).T)
        assert np.array_equal(np.array(rows), np.eye(len(columns), dtype=object))
        report.append({'plane': name, 'mapping': mapping,
                       'rank': len(rows), 'row_space_monomials': columns})
    return report


def differential_at_axis(coefficients, axis):
    dimension = len(next(iter(coefficients.values())))
    matrix = np.zeros((dimension, 8), dtype=object)
    for m, coefficient in coefficients.items():
        for k, j in enumerate(m):
            if all(x == axis for x in m[:k]+m[k+1:]):
                matrix[:, j] += coefficient
    return matrix


def evaluate_polynomial(coefficients, values):
    result = np.zeros_like(next(iter(coefficients.values())))
    for monomial, coefficient in coefficients.items():
        multiplier = F(1)
        for j in monomial:
            multiplier *= values[j]
        result += multiplier*coefficient
    return result


def run_checks():
    check_linear_and_axes()
    print('PASS_LITERAL_LINEAR_PLACEMENT_AND_EIGHT_EXACT_AXIS_FAMILIES', flush=True)
    quadratic_coefficients = reconstruct_quadratic()
    matrix, kernel = quadratic_structure(quadratic_coefficients)
    columns, transform = quarter_reduction()
    assert columns == [j for j in range(24) if j not in (5, 11, 16, 21)]
    print('PASS_QUADRATIC_GATE_AND_ZERO_MEAN_QUADRATIC_RESPONSE', flush=True)
    cubic_coefficients = reconstruct_cubic(quadratic_coefficients, transform)
    restrictions = plane_checks(cubic_coefficients)
    q2 = {m: value for m, (_, value) in quadratic_coefficients.items()}
    ranks = []
    for axis in range(8):
        derivative = np.concatenate([differential_at_axis(q2, axis),
                                     differential_at_axis(cubic_coefficients, axis)])
        rank = len(row_reduce(derivative))
        assert rank == 7
        ranks.append(rank)
        assert not np.any(q2[(axis, axis)])
        assert not np.any(cubic_coefficients[(axis, axis, axis)])
        assert not np.any(quadratic_coefficients[(axis, axis)][0])
    # Dense rational polarization control, separate from the reconstruction
    # directions; checks W2, q2 and all real/imaginary cubic output entries.
    dense = [F(i-3, i+2) for i in range(8)]
    w, q = quadratic(dense)
    reconstructed_w = sum(dense[i]*dense[j]*value[0]
                          for (i, j), value in quadratic_coefficients.items())
    assert np.array_equal(w, reconstructed_w)
    assert np.array_equal(q, evaluate_polynomial(q2, dense))
    assert np.array_equal(cubic(dense, quadratic_coefficients, transform),
                          evaluate_polynomial(cubic_coefficients, dense))
    mixed = [0, 1, 1, 0, 0, 0, 0, 0]
    assert not np.any(evaluate_polynomial(q2, mixed))
    assert np.any(evaluate_polynomial(cubic_coefficients, mixed))
    phase_mixed = [1, 0, 0, 0, 1, 0, 0, 0]
    assert np.any(evaluate_polynomial(q2, phase_mixed))
    print('PASS_CUBIC_CONE_EIGHT_BLOWUP_RANKS_AND_HOSTILE_CONTROLS', flush=True)
    return {
        'arithmetic': 'exact Q and Q(i); NumPy object arrays; no floats',
        'model': 'eta, links depend only on p=sum(x) mod 4, identity log chart',
        'fast_joint_rows': 126,
        'linear_real_rank': 88,
        'center_real_dimension': 8,
        'center_generator_rows': [exact_strings(row) for row in TC],
        'quarter_normal_columns': columns,
        'literal_linear_characters_checked': ['1', '-1', 'i'],
        'exact_axis_families': 8,
        'cleared_axis_identity_degree': 8,
        'quadratic_gate_matrix': [exact_strings(row) for row in matrix],
        'quadratic_gate_matrix_kernel': exact_strings(kernel),
        'quadratic_monomials': [list(m) for m in sorted(quadratic_coefficients)],
        'quadratic_normal_coefficients': [exact_strings(quadratic_coefficients[m][0])
                                          for m in sorted(quadratic_coefficients)],
        'quadratic_gate_coefficients': [exact_strings(q2[m]) for m in sorted(q2)],
        'mean_metric_quadratic_coefficients_zero': True,
        'cubic_monomials': [list(m) for m in sorted(cubic_coefficients)],
        'cubic_gate_coefficients': [exact_strings(cubic_coefficients[m])
                                     for m in sorted(cubic_coefficients)],
        'cubic_nonzero_scalar_coefficients': sum(bool(x)
            for value in cubic_coefficients.values() for x in value),
        'quadratic_cone_plane_restrictions': restrictions,
        'blowup_axis_derivative_ranks': ranks,
        'dense_rational_reconstruction_check': True,
        'mixed_quadratic_zero_cubic_nonzero_control': True,
        'temporal_two_parity_quadratic_nonzero_control': True,
        'verdict': 'IDENTITY_QUARTER_NONLINEAR_CLASSIFICATION_AND_RESPONSE_CERTIFIED',
        'nonclaims': ['no arbitrary Bloch or varying-envelope classification',
                      'no fixed-curved normal rescue or Einstein terminal',
                      'no refinement claim from finite-dimensional norm equivalence']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--expect', type=Path)
    args = parser.parse_args()
    report = run_checks()
    # JSON canonicalization turns tuples into lists before the pinned replay.
    report = json.loads(json.dumps(report))
    if args.expect:
        assert json.loads(args.expect.read_text()) == report
        print('PASS_PINNED_LEDGER')
    if args.output:
        args.output.write_text(json.dumps(report, indent=2)+'\n')
    print('RESULT: eight local four-phase branches; mean response has a residual gain.')
