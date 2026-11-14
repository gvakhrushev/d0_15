#!/usr/bin/env python3
"""Outward dyadic names for actual B25 CAR half-vectors and their rotations.

The entire SAM cube reduces to two local matter bits at each free site.
These are target formulas, not physical preparations or paid native gates.
"""
from pathlib import Path
from math import isqrt
from fractions import Fraction
import hashlib,importlib.util,json,sys
P=Path(__file__).resolve().parent;D=P.parent
B=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open')

class Dyadic:
    def __init__(self,bits):self.bits=bits;self.scale=1<<bits
    def rational(self,n,d=1):
        assert d>0
        return (n*self.scale//d,-((-n*self.scale)//d))
    def add(self,a,b):return (a[0]+b[0],a[1]+b[1])
    def neg(self,a):return (-a[1],-a[0])
    def sub(self,a,b):return self.add(a,self.neg(b))
    def mul(self,a,b):
        v=[x*y for x in a for y in b]
        return (min(v)//self.scale,-((-max(v))//self.scale))
    def div(self,a,b):
        assert b[0]>0
        lo=min(x*self.scale//y for x in a for y in b)
        hi=max(-((-x*self.scale)//y) for x in a for y in b)
        return (lo,hi)
    def sqrt(self,a):
        assert a[0]>=0
        lo=isqrt(a[0]*self.scale);hi=isqrt(a[1]*self.scale)
        if hi*hi<a[1]*self.scale:hi+=1
        return (lo,hi)
    def pow(self,a,n):
        out=self.rational(1)
        for _ in range(n):out=self.mul(out,a)
        return out
    def pi(self):
        # Machin formula. Each term and the alternating-series remainder
        # are enclosed by exact integers. No mpmath value certifies pi.
        def arctan_recip(q):
            total=(0,0);power=q;j=0
            while True:
                term=self.rational(1,(2*j+1)*power)
                total=self.add(total,term if j%2==0 else self.neg(term))
                j+=1;power*=q*q
                den=(2*j+1)*power
                if den>self.scale:
                    remainder=self.rational(1,den)[1]
                    return (total[0]-remainder,total[1]+remainder)
        return self.sub(self.mul(self.rational(16),arctan_recip(5)),
                        self.mul(self.rational(4),arctan_recip(239)))

def constants(iv):
    R=iv.rational;one=R(1)
    p=iv.div(iv.sub(iv.sqrt(R(5)),one),R(2));a=iv.sqrt(p)
    z=R(1,2**20);L=iv.mul(R(4),iv.pow(p,3));Q=iv.sub(one,iv.mul(z,L))
    p6=iv.pow(p,6);RR=iv.sub(one,iv.mul(iv.mul(z,L),iv.add(one,p6)))
    k0=iv.mul(iv.div(R(2),iv.pow(p,5)),iv.add(iv.div(RR,Q),p6))
    meta=json.loads((B/'round21/REFERENCE_METADATA.json').read_text());fh=Fraction(meta['F_h_rational'])
    # Original a_h=(h/2)*sqrt(F_h/k0), h=1/4.
    reference_amp=iv.div(iv.sqrt(iv.div(R(fh.numerator,fh.denominator),k0)),R(8))
    physical_amp=iv.div(iv.pi(),iv.mul(R(200),iv.sqrt(R(2))))
    return {'p':p,'sqrtp':a,'k0':k0,'reference_amp':reference_amp,'physical_amp':physical_amp}

def family_specs():
    out=[]
    for x0 in range(4):
        out.append({'id':f'q{x0}_fixed','kind':'q','x0':x0,'bits':None})
        for b0 in (0,1):
            for b15 in (0,1):out.append({'id':f'q{x0}_{b0}{b15}','kind':'q','x0':x0,'bits':[b0,b15]})
    out.extend([{'id':'y_positive','kind':'y','sign':1},{'id':'y_negative','kind':'y','sign':-1}])
    assert len(out)==22
    return out

def half_vector(iv,c,spec):
    R=iv.rational;one=R(1);p=c['p'];a=c['sqrtp']
    if spec['kind']=='q':
        x=spec['x0'];psi=[iv.mul(R((1,0,-1,0)[x]),c['physical_amp']),iv.mul(R((0,1,0,-1)[x]),c['physical_amp'])]
        if spec['bits'] is not None:
            for j,bit in enumerate(spec['bits']):psi[j]=iv.add(psi[j],iv.mul(R(1,2**30),iv.sub(R(bit),iv.pow(p,2))))
    else:psi=[iv.mul(R(spec['sign']),c['reference_amp']),R(0)]
    slack=iv.sub(iv.sub(one,p),iv.add(iv.pow(psi[0],2),iv.pow(psi[1],2)))
    assert slack[0]>iv.scale//3
    den=iv.sqrt(iv.mul(R(2),iv.add(one,a)))
    v={1:iv.div(iv.add(one,a),den),14:iv.div(iv.sqrt(slack),den),0:iv.div(psi[0],den),15:iv.div(psi[1],den)}
    return v,psi

def rotations(iv,v):
    # Chronological planar rotations (1,14), (1,0), (1,15).
    # Each (c,s) means |1> -> c|1>+s|other> before residual scaling.
    rem1=iv.sqrt(iv.add(iv.pow(v[1],2),iv.add(iv.pow(v[0],2),iv.pow(v[15],2))))
    rem2=iv.sqrt(iv.add(iv.pow(v[1],2),iv.pow(v[15],2)))
    assert rem1[0]>iv.scale*9//10 and rem2[0]>iv.scale*9//10
    return [{'other':14,'cos':rem1,'sin':v[14]},
            {'other':0,'cos':iv.div(rem2,rem1),'sin':iv.div(v[0],rem1)},
            {'other':15,'cos':iv.div(v[1],rem2),'sin':iv.div(v[15],rem2)}]

def catalogue():
    rows=[json.loads(x) for x in (B/'round21/ORIGINAL_PF_N20_L4.jsonl').read_text().splitlines()]
    coords=[json.loads(x) for x in (B/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl').read_text().splitlines()]
    matter={}
    for i,row in enumerate(coords):
        if row['kind']=='matter':
            key=(tuple(row['site']),row['grade']);assert key not in matter;matter[key]=i
    assert len(coords)==2688 and len(matter)==128
    out={k:[] for k in ['q','y+','y-']}
    for index,row in enumerate(rows):
        x=tuple(row['site']);keys=[(x,g) for g in (0,15)]
        assert (keys[0] in matter)==(keys[1] in matter)
        if keys[0] in matter:
            wires=[matter[key] for key in keys]
            for b0 in (0,1):
                for b15 in (0,1):out['q'].append({'site':index,'site_coordinates':list(x),'SAM_indices':wires,'SAM_pattern':[b0,b15],'vector_id':f'q{x[0]}_{b0}{b15}'})
        else:out['q'].append({'site':index,'site_coordinates':list(x),'SAM_indices':[],'SAM_pattern':[],'vector_id':f'q{x[0]}_fixed'})
        for name,axis in [('y+',1),('y-',0)]:out[name].append({'site':index,'site_coordinates':list(x),'SAM_indices':[],'SAM_pattern':[],'vector_id':'y_positive' if x[axis]%2==0 else 'y_negative'})
    assert len(out['q'])==448 and len(out['y+'])==len(out['y-'])==256
    return out
