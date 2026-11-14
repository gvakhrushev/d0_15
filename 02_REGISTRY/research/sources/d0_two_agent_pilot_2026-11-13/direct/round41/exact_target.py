#!/usr/bin/env python3
"""Small executable reference for the constructive A37 target theorem.

Production evaluation is NOT implemented: CPython indexed containers cannot
have length 2^2688. The unrestricted finite algorithm is mathematical only.
The small-case implementation has no target-table/angle oracle: all entries
are computed in Q(a), a=sqrt(p), a^4+a^2-1=0, then by positive square roots.
"""
from fractions import Fraction as F
from dataclasses import dataclass
from math import isqrt
from pathlib import Path
import json,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;D=P.parent


class Q4:
    def __init__(self,v=0):
        self.v=v.v if isinstance(v,Q4) else tuple(F(x) for x in v) if isinstance(v,(tuple,list)) else (F(v),F(0),F(0),F(0))
        assert len(self.v)==4
    def __add__(self,b):
        b=Q4(b);return Q4(tuple(x+y for x,y in zip(self.v,b.v)))
    __radd__=__add__
    def __neg__(self):return Q4(tuple(-x for x in self.v))
    def __sub__(self,b):return self+-Q4(b)
    def __mul__(self,b):
        b=Q4(b);out=[F(0)]*7
        for i,x in enumerate(self.v):
            for j,y in enumerate(b.v):out[i+j]+=x*y
        for k in range(6,3,-1):out[k-4]+=out[k];out[k-2]-=out[k]
        return Q4(out[:4])
    __rmul__=__mul__
    def __eq__(self,b):return self.v==Q4(b).v
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        out=Q4(1);base=self
        while n:
            if n&1:out=out*base
            base=base*base;n>>=1
        return out


A=Q4((0,1,0,0));SIN=A*A


def rotation_power(n):
    assert isinstance(n,int) and n>=0
    c,s=Q4(1),Q4(0);u,v=A,SIN
    while n:
        if n&1:c,s=c*u-s*v,s*u+c*v
        u,v=u*u-v*v,2*u*v;n>>=1
    return c,s


def born(n):
    # Bit j is tensor wire j; a^(n+popcount(b)) is its exact amplitude.
    return [A**(n+bin(b).count('1')) for b in range(1<<n)]


def leaves(tree):
    op=tree['op']
    if op=='seq':
        for t in tree['children']:yield from leaves(t)
    elif op=='repeat':
        raw=tree['count'];n=int(raw,16) if raw.startswith('0x') else int(raw)
        assert n>0
        for _ in range(n):yield from leaves(tree['child'])
    else:
        assert op in ('G','CX');yield tree


def compressed_entry(total,sam,b,word_factory):
    """<born_WORK| W_b |born_WORK>, checking SAM control-only literally.

    Each actual leaf is used, including repetitions; no ideal W/inverse is
    substituted for the already compiled A30 word.
    """
    sam=tuple(sam);assert len(set(sam))==len(sam) and all(0<=q<total for q in sam)
    assert 0<=b<(1<<len(sam))
    sam_index={q:j for j,q in enumerate(sam)}
    work=[q for q in range(total) if q not in sam_index]
    wi={q:j for j,q in enumerate(work)};v=born(len(work));state=list(v)
    for tree in word_factory():
        for gate in leaves(tree):
            op=gate['op'];w=gate['wires']
            assert all(0<=q<total for q in w)
            target=w[-1];assert target in wi,'actual W must not target SAM'
            t=1<<wi[target]
            if op=='G':
                assert len(w)==1
                for x in range(len(state)):
                    if x&t:continue
                    y=x|t;u,vv=state[x],state[y]
                    state[x],state[y]=A*u-SIN*vv,SIN*u+A*vv
            else:
                assert len(w)==2 and w[0]!=w[1]
                control=w[0]
                for x in range(len(state)):
                    if x&t:continue
                    enabled=((b>>sam_index[control])&1) if control in sam_index else ((x>>wi[control])&1)
                    if enabled:state[x],state[x|t]=state[x|t],state[x]
    return sum((x*y for x,y in zip(v,state)),Q4())


@dataclass(eq=False)
class Expr:
    op:str
    args:tuple
    def __add__(self,b):return Expr('add',(self,expr(b)))
    __radd__=__add__
    def __neg__(self):return Expr('neg',(self,))
    def __sub__(self,b):return self+-expr(b)
    def __mul__(self,b):return Expr('mul',(self,expr(b)))
    __rmul__=__mul__
    def __truediv__(self,b):return Expr('div',(self,expr(b)))


def expr(v):return v if isinstance(v,Expr) else Expr('field',(Q4(v),))
def root(v):return Expr('sqrt',(expr(v),))
def norm(v):return root(sum((x*x for x in v),expr(0)))


def target_vectors(table,sam_bits,power=0,sam_index=0):
    assert len(table)==1<<sam_bits and 0<=sam_index<sam_bits
    chi=born(sam_bits);psi=list(chi)
    c,s=rotation_power(power);t=1<<sam_index
    for b in range(1<<sam_bits):
        if not b&t:psi[b],psi[b|t]=c*chi[b]-s*chi[b|t],s*chi[b]+c*chi[b|t]
    x=[expr(a*b) for a,b in zip(table,psi)];r=norm(x);xi=[a/r for a in x]
    chi=list(map(expr,chi));summed=[a+b for a,b in zip(chi,xi)];hn=norm(summed)
    return chi,xi,[a/hn for a in summed],r


def production_target(*args,**kwargs):
    """No false promise that a Python list can have 2^2688 entries."""
    raise NotImplementedError('Production target is specified by the mathematical theorem, not implemented by this small reference')


class NeedPrecision(Exception):pass


class Dyadic:
    """Integer outward intervals at denominator 2^bits, no float operations."""
    def __init__(self,bits):self.bits=bits;self.S=1<<bits
    def rat(self,n,d=1):
        v=F(n,d);return v.numerator*self.S//v.denominator,-((-v.numerator*self.S)//v.denominator)
    def add(self,x,y):return x[0]+y[0],x[1]+y[1]
    def neg(self,x):return -x[1],-x[0]
    def mul(self,x,y):
        ps=[a*b for a in x for b in y]
        return min(ps)>>self.bits,-((-max(ps))>>self.bits)
    def div(self,x,y):
        if y[0]<=0:raise NeedPrecision('positive denominator not enclosed')
        return min(a*self.S//b for a in x for b in y),max(-((-a*self.S)//b) for a in x for b in y)
    def sqrt(self,x):
        if x[0]<0:raise NeedPrecision('positive radicand not enclosed')
        lo=isqrt(x[0]*self.S);hi=isqrt(x[1]*self.S)
        return lo,hi+(hi*hi<x[1]*self.S)
    def field(self,x):
        a=self.sqrt(self.div(self.add(self.sqrt(self.rat(5)),self.rat(-1)),self.rat(2)))
        out=self.rat(0)
        for c in reversed(x.v):out=self.add(self.mul(out,a),self.rat(c))
        return out
    def evaluate(self,targets):
        # Iterative traversal avoids dependence on Python's recursion limit
        # for the very large (but finite) exact target expression graph.
        cache={};todo=[(t,False) for t in targets]
        while todo:
            t,ready=todo.pop()
            if t in cache:continue
            if t.op=='field':cache[t]=self.field(t.args[0]);continue
            if not ready:
                todo.append((t,True));todo.extend((a,False) for a in t.args if a not in cache);continue
            xs=[cache[a] for a in t.args]
            cache[t]={'add':self.add,'neg':self.neg,'mul':self.mul,'div':self.div,'sqrt':self.sqrt}[t.op](*xs)
        return [cache[t] for t in targets]
