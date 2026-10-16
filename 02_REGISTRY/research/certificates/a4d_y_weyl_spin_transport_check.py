#!/usr/bin/env python3
"""Full exact Y-vacuum residual for right/left/symmetric Weyl spin correction."""
from fractions import Fraction as F
from pathlib import Path
import argparse, hashlib, importlib, json, sys
import numpy as np

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3])
p.add_argument('--output',type=Path)
p.add_argument('--expect',type=Path,default=Path(__file__).with_name('a4d_y_weyl_spin_transport_results.json'))
args=p.parse_args()
sys.path.insert(0,str(args.repo/'02_REGISTRY/research/certificates'))
N=importlib.import_module('a4d_identity_quarter_nonlinear_response_check')
d=8
Y=N.G[3]-N.G[4]+N.G[5]
W=[N.G[0]*F(1,2),np.zeros((4,4),dtype=object),-N.G[3]*F(1,2),-N.G[4]*F(1,2)]


def mul(a,b):
    out=np.zeros_like(a)
    out[0]=N.jmul(a[0],b[0])
    out[1]=N.jmul(a[0],b[1])+N.jmul(a[1],b[0])
    return out


def const(a):
    out=np.zeros((2,d+1,4,4),dtype=object)
    out[0,0]=a
    return out


def inv(a):
    out=np.zeros_like(a)
    out[0]=N.jinv(a[0])
    out[1]=N.jinv(a[1])
    return out


def links_for(kind):
    links=np.array([[const(N.I) for _ in range(4)] for _ in range(4)])
    # Clear D=4+3t^2 on every link, including inactive identities.
    # Each full Euler term contains exactly four factors, so D^4 EK is
    # a COMPLETE degree-eight polynomial. Lorentz transpose supplies
    # inverse numerator and its first-variation numerator directly.
    links[:,:,0,0]=4*N.I
    links[:,:,0,2]=3*N.I
    for ph,sgn in ((0,1),(2,-1)):
        links[ph,0,0,1]=sgn*4*Y
        links[ph,0,0,2]+=2*(Y@Y)
    for ph in range(4):
        for role in range(4):
            if kind=='right': links[ph,role,1]=links[ph,role,0]@W[role]
            elif kind=='left': links[ph,role,1]=W[role]@links[ph,role,0]
            elif kind=='symmetric': links[ph,role,1]=(links[ph,role,0]@W[role]+W[role]@links[ph,role,0])*F(1,2)
            elif kind!='frozen': raise ValueError(kind)
    return links


def euler(kind):
    links=links_for(kind)
    ek=np.zeros((2,d+1,4,24),dtype=object)
    for ph in range(4):
        for role in range(4):
            for face,(r,s) in enumerate(N.PAIRS):
                # Target base x has x_1=0 and phase ph. Each incident face
                # has lambda_z=1+epsilon*z_1; epsilon is the slow conformal gradient.
                incidences=[]
                if role==r: incidences=[(0,ph,0),(2,(ph-1)%4,-int(s==1))]
                elif role==s: incidences=[(1,(ph-1)%4,-int(r==1)),(3,ph,0)]
                for occurrence,bp,offset in incidences:
                    loc=[(bp,r,False),((bp+1)%4,s,False),((bp+1)%4,r,True),(bp,s,True)]
                    fac=[inv(links[x,y]) if inverse else links[x,y] for x,y,inverse in loc]
                    pref=[const(N.I)]
                    for f in fac: pref.append(mul(pref[-1],f))
                    suf=[None]*5;suf[4]=const(N.I)
                    for i in range(3,-1,-1):suf[i]=mul(fac[i],suf[i+1])
                    co=mul(mul(suf[occurrence+1],const(N.WEIGHT[face].T)),pref[occurrence])
                    jet=-mul(fac[occurrence],co) if loc[occurrence][2] else mul(co,fac[occurrence])
                    for degree in range(d+1):
                        for a in range(6):
                            ek[0,degree,ph,6*role+a]+=np.sum(jet[0,degree].T*N.G[a])
                            ek[1,degree,ph,6*role+a]+=np.sum((jet[1,degree]+offset*jet[0,degree]).T*N.G[a])
    assert not np.any(ek[0]),kind
    return ek[1]


rows=[]
for kind in ('frozen','right','left','symmetric'):
    residual=euler(kind)
    if kind!='frozen': assert not np.any(residual[0])
    nonzero=[]
    for degree in range(d+1):
        for ph in range(4):
            for row in range(24):
                if residual[degree,ph,row]: nonzero.append([degree,ph,row,str(F(residual[degree,ph,row]))])
    assert nonzero
    first=min(r[0] for r in nonzero)
    if kind!='frozen':
        # Exact closed witness: D^4 EK[phase0,Role1,J12] is
        # t(2+t) D^3 / 2, not an extrapolation from Taylor coefficients.
        expected=np.zeros(d+1,dtype=object)
        from math import comb
        for j in range(4):
            coefficient=F(comb(3,j)*4**(3-j)*3**j)
            expected[1+2*j]+=coefficient
            expected[2+2*j]+=coefficient*F(1,2)
        assert np.array_equal(residual[:,0,9],expected)
    rows.append({'kind':kind,'all_24_rows_each_phase_retained':True,
                 'stationary_Y_base_all_rows_zero':True,
                 'first_nonzero_Y_amplitude_degree':first,
                 'first_nonzero_coefficients':[r for r in nonzero if r[0]==first],
                 'all_cleared_numerator_coefficients_degree_eight':nonzero})

out={'schema':'d0-y-weyl-correction-hostile-control/1',
     'input_head':'cc6cc38f',
     'owner_sha256':{name:hashlib.sha256((args.repo/'02_REGISTRY/research/certificates'/name).read_bytes()).hexdigest() for name in ('a4d_identity_quarter_nonlinear_response_check.py','a4d_designated_full_gap_check.py')},
     'metric_first_jet':'q_lambda=lambda eta, lambda=1+epsilon*y_1',
     'UV_vacuum':'Y=Cayley(t*(J12-J13+J23)), phase role0=(U,I,U^-1,I)',
     'Weyl_LC_coefficients':[N.G[0].tolist(),'0',(-N.G[3]).tolist(),(-N.G[4]).tolist()],
     'Weyl_LC_common_factor':'epsilon/2',
     'scope':'First slow-gradient full Euler residual; not a proof against all UV-dependent conformal corrections.',
     'cleared_denominator':'(4+3*t^2)^4',
     'exact_common_witness_phase0_role1_J12':'epsilon*t*(2+t)/(2*(4+3*t^2)) + O(epsilon^2)',
     'controls':rows}
encoded=json.loads(json.dumps(out,default=str))
if args.output:args.output.write_text(json.dumps(encoded,indent=2)+'\n')
else:
    assert args.expect.is_file(), 'Missing immutable expected ledger'
    assert json.loads(args.expect.read_text())==encoded, 'Exact replay differs from immutable ledger'
print(json.dumps({'status':'PASS','first_nonzero_degrees':{r['kind']:r['first_nonzero_Y_amplitude_degree'] for r in rows}}))
