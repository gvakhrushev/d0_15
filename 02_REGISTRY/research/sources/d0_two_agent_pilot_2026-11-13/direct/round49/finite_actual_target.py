#!/usr/bin/env python3
"""Scalar finite-circuit evaluation without a 2^n indexed state container.

This deliberately slow path-sum implements the mathematical production
recipe. It consumes the actual G/CX word, not its ideal inverse/reflection.
Production queries are NOT run: their cost is enormous. Small fixtures
exercise exactly the same algorithm. Increasing interval precision makes
every finite sum converge; no unprovided target-entry oracle is accepted.
"""
from pathlib import Path
from bisect import bisect_left
from functools import lru_cache
import sys
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(D/'round41'))
import sam_only_compiler as a41
e=a41.e

def popcount(n):return bin(n).count('1')

def indices(bits):
    """No allocation of a table or of the integer 2^(number of G calls)."""
    assert type(bits) is int and bits>=0
    i=0
    while i.bit_length()<=bits:
        yield i;i+=1

def ipow(iv,x,n):
    assert type(n) is int and n>=0
    out=iv.rat(1)
    while n:
        if n&1:out=iv.mul(out,x)
        n>>=1
        if n:x=iv.mul(x,x)
    return out

class ActualDiagonal:
    def __init__(self,total,sam,word_factory,*,path_limit=None):
        self.total=total;self.sam=tuple(sam);self.factory=word_factory
        assert type(total) is int and total>=len(sam)
        assert len(set(sam))==len(sam) and all(0<=q<total for q in sam)
        self.order=sorted(sam);self.sindex={q:j for j,q in enumerate(sam)}
        self.work=total-len(sam);self.path_limit=path_limit

    def work_index(self,q):
        assert 0<=q<self.total and q not in self.sindex
        return q-bisect_left(self.order,q)

    @lru_cache(None)
    def g_calls(self):
        # Counts actual repeat DAGs. No numerical upper bound is used here.
        from paid_padding import native
        return sum(native.counts(t)['G'] for t in self.factory())

    def entry(self,label,iv):
        assert 0<=label<1<<len(self.sam)
        a=iv.field(e.A);p=iv.field(e.SIN);out=iv.rat(0);paths=0;ng=self.g_calls()
        for start in indices(self.work):
            for choices in indices(ng):
                paths+=1
                if self.path_limit is not None:assert paths<=self.path_limit,'explicit fixture execution limit'
                state=start;weight=iv.rat(1);j=0
                for tree in self.factory():
                    for gate in e.leaves(tree):
                        op=gate['op'];w=gate['wires'];target=w[-1]
                        assert target not in self.sindex,'actual centre core must be CODE control-only'
                        bit=1<<self.work_index(target)
                        if op=='G':
                            flip=(choices>>j)&1;j+=1
                            if flip:
                                weight=iv.mul(weight,iv.neg(p) if state&bit else p);state^=bit
                            else:weight=iv.mul(weight,a)
                        else:
                            assert op=='CX' and len(w)==2 and w[0]!=target
                            c=w[0]
                            enabled=((label>>self.sindex[c])&1) if c in self.sindex else ((state>>self.work_index(c))&1)
                            if enabled:state^=bit
                assert j==ng
                born_power=2*self.work+popcount(start)+popcount(state)
                out=iv.add(out,iv.mul(weight,ipow(iv,a,born_power)))
        # Exact compression of an orthogonal word has |entry|<=1.
        out=(max(-iv.S,out[0]),min(iv.S,out[1]));assert out[0]<=out[1]
        return out

class PositiveTarget:
    """chi and unnormalised h=chi+M chi/||M chi||, entry by entry."""
    def __init__(self,core):self.core=core;self.m=len(core.sam)
    def chi(self,b,iv):return ipow(iv,iv.field(e.A),self.m+popcount(b))
    @lru_cache(maxsize=2)
    def radius(self,bits):
        iv=e.Dyadic(bits);out=iv.rat(0)
        for b in indices(self.m):
            x=iv.mul(self.chi(b,iv),self.core.entry(b,iv));out=iv.add(out,iv.mul(x,x))
        return iv.sqrt(out)
    def value(self,kind,b,iv):
        chi=self.chi(b,iv)
        if kind=='chi':return chi
        assert kind=='h'
        value=self.core.entry(b,iv)
        if value[0]<=0:raise e.NeedPrecision('positive actual compression not enclosed')
        return iv.mul(chi,iv.add(iv.rat(1),iv.div(value,self.radius(iv.bits))))
    def star(self,kind,j,bits):
        """Normalisation of the vector cancels from each Givens ratio."""
        iv=e.Dyadic(bits);assert 1<=j<1<<self.m
        x=self.value(kind,0,iv);sq=iv.mul(x,x)
        k=j+1
        while k<1<<self.m:
            x=self.value(kind,k,iv);sq=iv.add(sq,iv.mul(x,x));k+=1
        x=iv.sqrt(sq);y=self.value(kind,j,iv)
        radius=iv.sqrt(iv.add(sq,iv.mul(y,y)))
        c=iv.div(x,radius);s=iv.neg(iv.div(y,radius))
        # A41 divides the angle by the zero-Walsh multiplicity.
        for _ in range(self.m-1):
            nc=iv.sqrt(iv.div(iv.add(iv.rat(1),c),iv.rat(2)))
            s=iv.div(s,iv.mul(iv.rat(2),nc));c=nc
        return c,s

def select_from_intervals(target,*,initial_bits=20480):
    pn,q,cert=a41.uniform_grid();bits=initial_bits
    pi0=[int(v,16) for v in cert['pi_interval_hex']];pb=cert['precision_bits']
    while True:
        iv=e.Dyadic(bits)
        try:
            c,s=target(bits);ratio=iv.div(s,c)
            if not -iv.S<ratio[0]<=ratio[1]<iv.S:raise e.NeedPrecision()
            angle=(a41.atan_signed(iv,ratio[0])[0],a41.atan_signed(iv,ratio[1])[1])
            if bits<=pb:
                shift=pb-bits;pi=(pi0[0]>>shift,-((-pi0[1])>>shift))
            else:pi=tuple(v<<(bits-pb) for v in pi0)
            tau=iv.div(angle,(2*pi[0],2*pi[1]))
            if 2*q*(tau[1]-tau[0])<=iv.S:
                j=(q*(tau[0]+tau[1])+iv.S)//(2*iv.S)
                return (j*pow(pn,-1,q))%q or q
        except e.NeedPrecision:pass
        bits*=2

def post_blocks(core,*,selector=select_from_intervals):
    """Actual four star lists on CODE only, recomputing finite entries.

    The function is also the production recipe; there is no production
    NotImplemented branch and no target table supplied by a caller.
    The full production scalar/path sums have not been evaluated.
    """
    target=PositiveTarget(core);m=target.m;assert m>=3
    for kind,reverse,opposite in [('h',False,False),('h',True,False),
                                  ('chi',False,True),('chi',True,True)]:
        j=1 if reverse else (1<<m)-1
        while 0<j<1<<m:
            def angle(bits):
                c,s=target.star(kind,j,bits)
                return c,(-s[1],-s[0]) if opposite else s
            k=selector(angle)
            yield from a41.star_blocks(core.sam,j,k)
            j+=1 if reverse else -1
