#!/usr/bin/env python3
"""Exact full Euler incidence controls for the conformal forward bridge.

Only Fraction arithmetic; NumPy supplies indexing. This finite replay checks
the complete degree-two algebra, not the analytic limiting theorem.
"""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import importlib
import json
import sys
import numpy as np

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3])
parser.add_argument('--output',type=Path)
parser.add_argument('--expect',type=Path,default=Path(__file__).with_name('a4d_conformal_forward_response_results.json'))
args=parser.parse_args()
repo=args.repo.resolve()
cert=repo/'02_REGISTRY/research/certificates'
sys.path.insert(0,str(cert))
N=importlib.import_module('a4d_identity_quarter_nonlinear_response_check')
checks=[]


def weighted_euler(links,weights):
    degree=links.shape[2]-1
    ek=np.zeros((degree+1,4,4,6),dtype=object)
    for p in range(4):
        for face,(r,s) in enumerate(N.PAIRS):
            loc=[(p,r,False),((p+1)%4,s,False),((p+1)%4,r,True),(p,s,True)]
            factors=[N.jinv(links[x,y]) if inv else links[x,y] for x,y,inv in loc]
            prefix=[N.jconst(N.I,degree)]
            for factor in factors: prefix.append(N.jmul(prefix[-1],factor))
            suffix=[None]*5
            suffix[4]=N.jconst(N.I,degree)
            for i in range(3,-1,-1): suffix[i]=N.jmul(factors[i],suffix[i+1])
            for i,(x,y,inv) in enumerate(loc):
                co=N.jmul(suffix[i+1],N.WEIGHT[face].T@prefix[i])
                jet=-N.jmul(factors[i],co) if inv else N.jmul(co,factors[i])
                for k in range(degree+1):
                    for j in range(k+1):
                        for alpha in range(6):
                            ek[k,x,y,alpha]+=weights[p,j]*np.sum(jet[k-j].T*N.G[alpha])
    return ek.reshape(degree+1,4,24)


def multiply_at_link(field,weights):
    degree=field.shape[0]-1
    out=np.zeros_like(field)
    for k in range(degree+1):
        for j in range(k+1):
            out[k]+=weights[:,j,None]*field[k-j]
    return out


def packed(array):
    values=np.asarray(array,dtype=object)
    return [str(F(x)) for x in values] if values.ndim==1 else [packed(x) for x in values]


degree=2
eye_links=np.array([[N.jconst(N.I,degree) for _ in range(4)] for _ in range(4)])
one=np.zeros((4,degree+1),dtype=object)
one[:,0]=1
scale=np.zeros_like(one)
scale[:,0]=F(7,5)
assert not np.any(weighted_euler(eye_links,one))
for seed in range(3):
    logs=np.zeros((4,4,degree+1,4,4),dtype=object)
    for p in range(4):
        for role in range(4):
            logs[p,role,1]=sum((F(((17*p+11*role+7*a+13*seed)%19)-9,23)*N.G[a]
                                   for a in range(6)),np.zeros((4,4),dtype=object))
    links=np.array([[N.jexp(logs[p,role]) for role in range(4)] for p in range(4)])
    base=weighted_euler(links,one)
    assert np.array_equal(base,N.euler_links(links)[0])
    const=weighted_euler(links,scale)
    assert np.array_equal(const,F(7,5)*base)
    lam=one.copy()
    lam[:,1]=[F(2,7),F(-3,11),F(5,13),F(-7,17)]
    weighted=weighted_euler(links,lam)
    ell=weighted_euler(eye_links,lam)
    commutator=weighted-multiply_at_link(base,lam)-ell
    assert not np.any(commutator[:2])
    assert np.any(commutator[2])
    assert not np.any(ell[0]) and np.any(ell[1]) and not np.any(ell[2])
    checks.append({'seed':seed,
                   'constant_weight_full_rows_rescale':True,
                   'all_24_rows_each_phase_checked':True,
                   'weighted_identity_forcing_nonzero_degree_one':packed(ell[1]),
                   'weighted_Hessian_commutator_zero_degrees_zero_one':True,
                   'weighted_Hessian_commutator_degree_two':packed(commutator[2]),
                   'degree_two_commutator_nonzero_count':sum(bool(x) for x in commutator[2].flat)})

out={'schema':'d0-conformal-forward-bridge-exact-control/1',
     'input_head':'cc6cc38f',
     'owner_sha256':{name:hashlib.sha256((cert/name).read_bytes()).hexdigest()
                      for name in ('a4d_identity_quarter_nonlinear_response_check.py','a4d_designated_full_gap_check.py')},
     'checks':checks,
     'scope':'Exact weighted-face full Euler degree-two incidence identity; not a nonlinear root or original task terminal.'}
if args.output: args.output.write_text(json.dumps(out,indent=2)+'\n')
else:
    assert args.expect.is_file(), 'Missing immutable expected ledger'
    assert json.loads(args.expect.read_text())==out, 'Exact replay differs from immutable ledger'
print(json.dumps({'status':'PASS','all_24_rows':True,'rough_directions':len(checks),
                  'weighted_identity_forcing_retained':True,'commutator_first_nonzero_degree':2}))
