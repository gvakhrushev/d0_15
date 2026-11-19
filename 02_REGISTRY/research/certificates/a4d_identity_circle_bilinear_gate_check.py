#!/usr/bin/env python3
"""Exact bilinear metric gate for every pair of circle frequencies.

Formal Laurent/amplitude variables reconstruct the full two-frequency
vertex. The even connection inverse is checked coefficientwise. The
accompanying memo classifies the real quadratic zero cone analytically.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse
import json
import numpy as np
import a4d_identity_quarter_nonlinear_response_check as N
import a4d_identity_physical_resonance_circles_check as P
import a4d_identity_circle_even_inverse_check as R

class Poly:
    def __init__(self, terms=None):
        self.d={k:P.QI.of(v) for k,v in (terms or {}).items() if v}
    @classmethod
    def of(cls,x):return x if isinstance(x,cls) else cls({(0,0,0,0):P.QI.of(x)})
    def __add__(self,o):
        d=self.d.copy()
        for k,v in self.of(o).d.items():d[k]=d.get(k,P.QI())+v
        return Poly(d)
    __radd__=__add__
    def __neg__(self):return Poly({k:-v for k,v in self.d.items()})
    def __sub__(self,o):return self+-self.of(o)
    def __rsub__(self,o):return self.of(o)+-self
    def __mul__(self,o):
        d={}
        for k,v in self.d.items():
            for l,w in self.of(o).d.items():
                m=tuple(a+b for a,b in zip(k,l));d[m]=d.get(m,P.QI())+v*w
        return Poly(d)
    __rmul__=__mul__
    def __truediv__(self,o):return self*(1/P.QI.of(o))
    def __bool__(self):return bool(self.d)

def monomial(exponent):return Poly({exponent:P.QI.of(1)})
A=monomial((1,0,0,0));B=monomial((0,1,0,0))
E=monomial((0,0,1,0));FREQ=monomial((0,0,0,1))
CONST,LINEAR,COORD=P.circle_kernel(1)
VA=[Poly.of(x/CONST[COORD])+A*(y/CONST[COORD]) for x,y in zip(CONST,LINEAR)]
VB=[Poly.of(x/CONST[COORD])+B*(y/CONST[COORD]) for x,y in zip(CONST,LINEAR)]
ZERO=(0,0,0,0)

def unitpow(n):
    return (P.QI.of(1),P.Q,P.QI.of(-1),-P.Q)[n%4]

def forcing():
    ek=[Poly() for _ in range(24)];eq=[Poly() for _ in range(10)]
    for face,(r,s) in enumerate(N.PAIRS):
        roles=[r,s,r,s]; invs=[False,False,True,True]
        offsets=[ZERO,tuple(int(j==r) for j in range(4)),
                 tuple(int(j==s) for j in range(4)),ZERO]
        bases=list(dict.fromkeys(tuple(-v for v in z) for z in offsets))
        for base in bases:
            locs=[tuple(x+y for x,y in zip(base,o)) for o in offsets]
            fac=[]
            for loc,role,inv in zip(locs,roles,invs):
                n=loc[0]+loc[1];fixed=unitpow(loc[2]+loc[3])
                sa=monomial((n,0,0,0))*fixed*E
                sb=monomial((0,n,0,0))*fixed*FREQ
                coords=[VA[6*role+j]*sa+VB[6*role+j]*sb for j in range(6)]
                logs=N.jconst(np.zeros((4,4),dtype=object),2)
                logs[1]=sum((N.G[j]*coords[j] for j in range(6)),np.zeros((4,4),dtype=object))
                link=N.jexp(logs);fac.append(N.jinv(link) if inv else link)
            prefix=[N.jconst(N.I,2)]
            for f in fac:prefix.append(N.jmul(prefix[-1],f))
            suffix=[None]*5;suffix[4]=N.jconst(N.I,2)
            for j in range(3,-1,-1):suffix[j]=N.jmul(fac[j],suffix[j+1])
            if base==ZERO:
                for m in range(10):eq[m]+=np.sum(N.DWEIGHT[face][m]*prefix[4][2])
            for j,(loc,role,inv) in enumerate(zip(locs,roles,invs)):
                if loc!=ZERO:continue
                co=N.jmul(suffix[j+1],N.WEIGHT[face].T@prefix[j])
                jet=-N.jmul(fac[j],co) if inv else N.jmul(co,fac[j])
                for g in range(6):ek[6*role+g]+=np.sum(jet[2].T*N.G[g])
        print('face',face,'done',flush=True)
    def cross(v):return Poly({(k[0],k[1],0,0):x for k,x in v.d.items() if k[2:]==(1,1)})
    return [cross(v) for v in ek],[cross(v) for v in eq]

def run_checks():
    fk,fq=forcing();H,INV=R.build_inverse()
    w=[Poly() for _ in range(24)]
    for j,block in enumerate(INV):
        shift=monomial((j-3,j-3,0,0))
        for r in range(24):
            for c in range(24):
                if block[r,c]:w[r]-=fk[c]*block[r,c]*shift
    # Check every Laurent coefficient of the full even connection equation.
    check=fk.copy()
    for j,block in enumerate(H):
        shift=monomial((j-1,j-1,0,0))
        for r in range(24):
            for c in range(24):
                if block[r,c]:check[r]+=w[c]*block[r,c]*shift
    assert not any(check)
    cp=np.array(N.flat_symbols([1,1,-1,-1])[1],dtype=object)
    cm=np.array(N.flat_symbols([-1,-1,-1,-1])[1],dtype=object)
    C=[(cp+cm)/2,(cp-cm)/2]
    q=fq.copy()
    for j,block in enumerate(C):
        shift=monomial((j,j,0,0))
        for r in range(10):
            for c in range(24):
                if block[r,c]:q[r]+=w[c]*block[r,c]*shift
    qexpected = [
        {(0,0):P.QI(0,2),(1,1):2,(1,2):-1,(2,1):-1,(2,2):2},
        {(1,1):-4,(1,2):2,(2,1):2,(2,2):-4},
        {(0,0):-P.Q,(1,1):P.Q},
        {(0,0):-P.Q,(1,1):P.Q},
        {(0,0):P.QI(0,-2),(1,1):2,(1,2):-1,(2,1):-1,(2,2):2},
        {(0,0):P.Q,(1,1):-P.Q},
        {(0,0):P.Q,(1,1):-P.Q}, {}, {}, {}]
    for actual, expected in zip(q, qexpected):
        assert actual.d == {(k[0],k[1],0,0):P.QI.of(x) for k,x in expected.items()}
    assert (q[0]-q[4]).d == {(0,0,0,0):P.QI(0,4)}
    print('PASS_ALL_TWO_FREQUENCY_LAURENT_COEFFICIENTS_AND_REAL_AXIS_GATE',flush=True)
    # A changed sign of the actual range graph must break the connection
    # equation. This is an exact polynomial negative control.
    mutated = fk.copy()
    for j, block in enumerate(H):
        shift = monomial((j-1,j-1,0,0))
        for r in range(24):
            for c in range(24):
                if block[r,c]:mutated[r]-=w[c]*block[r,c]*shift
    assert any(mutated)
    return {'schema':'a4d-identity-circle-bilinear-gate-v1',
            'input_head':'de71bf30e9cfd34614fc8178255d456c49ebb8b1',
            'arithmetic':'exact Q(i) Laurent polynomials in two frequency and two amplitude variables',
            'operator':'circle v(a) at (a,a,i,i), polarize two arbitrary nonzero complex input frequencies',
            'even_connection_correction':'all coefficients of H(ab)w+f_AB vanish',
            'Qcross':[[[list(k[:2]),str(v.re),str(v.im)] for k,v in sorted(x.d.items())] for x in q],
            'polarization_normalization':'cross coefficient = twice the symmetric quadratic functional',
            'physical_envelope':'u(n,p)=i^p v(T)Z(n)+conjugate, n=x0+x1, p=x2+x3 mod4',
            'quadratic_metric_phase2':'2 Re(i Z_n^2+P_n, -2 P_n, i*(Z_(n+1)^2-Z_n^2)/2, i*(Z_(n+1)^2-Z_n^2)/2, -i Z_n^2+P_n, -i*(Z_(n+1)^2-Z_n^2)/2, -i*(Z_(n+1)^2-Z_n^2)/2, 0,0,0)',
            'P_n':'Z_(n+1)^2-Z_(n+1)*Z_(n+2)+Z_(n+2)^2',
            'quadratic_zero_cone':'Z=0 or Z_n=t*epsilon_n*i^n, or i*t*epsilon_n*i^n, t>0, epsilon_n in {+1,-1}',
            'nonclaims':['quadratic zero-cone members are not exact nonlinear roots',
                         'arbitrary sign sequences have not passed the cubic gate',
                         'no varying-coframe theorem or common-response cancellation is asserted'],
            'verdict':'ALL_CIRCLE_ENVELOPE_QUADRATIC_GATE_CERTIFIED; TASK_TERMINAL_OPEN'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--expect',type=Path)
    args=parser.parse_args()
    report=run_checks()
    expected=args.expect or (Path(__file__).with_name('a4d_identity_circle_bilinear_gate_results.json')
                            if args.output is None else None)
    if expected:
        assert json.loads(expected.read_text())==report
        print('PASS_PINNED_LEDGER',flush=True)
    if args.output:args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('VERDICT',report['verdict'])
