#!/usr/bin/env python3
"""Positive G/CX DAGs for new post-SAM construction, including controlled W.

Each lowering approximates its EXACT signed target. An inverse flag reverses
the original target DAG before lowering; it does not invert an already
approximated new word or identify two physical histories/prices.
"""
from pathlib import Path
from collections import Counter
from itertools import islice
import json, sys
P=Path(__file__).resolve().parent


def gate(op,*wires):
    assert op in ('G','CX') and len(wires)==(1 if op=='G' else 2)
    assert len(set(wires))==len(wires)
    assert all(type(q) is int and q>=0 for q in wires)
    return {'op':op,'wires':list(wires)}


def seq(*children): return {'op':'seq','children':list(children)}


def repeat(n,child):
    assert type(n) is int and n>=1
    return {'op':'repeat','count':hex(n),'child':child}


def count_value(v):
    assert isinstance(v,str)
    n=int(v,16) if v.startswith('0x') else int(v)
    assert n>=1
    return n


def counts(tree):
    op=tree['op']
    if op=='seq':
        out=Counter()
        for t in tree['children']: out.update(counts(t))
        return out
    if op=='repeat': return Counter({k:count_value(tree['count'])*v for k,v in counts(tree['child']).items()})
    assert op in ('G','CX')
    gate(op,*tree['wires'])
    return Counter({op:1})


class Macros:
    def __init__(self,certificate=None):
        self.cert=certificate or json.loads((P/'POST_ANGLE_CERTIFICATE.json').read_text())
        assert self.cert['status']=='PASS_SEVEN_CERTIFIED_POSITIVE_G_POWERS'
        assert self.cert['error_bits']==20000
        self.ks={k:int(v['exponent_hex'],16) for k,v in self.cert['rotations'].items()}

    def power(self,q,n): return repeat(n,gate('G',q))
    def angle(self,q,name): return self.power(q,self.ks[name])

    def pi8(self,q,m):
        assert 1<=m<=15
        return self.power(q,m*self.ks['pi8'])

    def z(self,q,helper):
        assert q!=helper
        return seq(gate('CX',q,helper),self.pi8(helper,4),
                   gate('CX',q,helper),self.pi8(helper,12))

    def h(self,q,helper): return seq(self.z(q,helper),self.pi8(q,2))
    def x(self,q,helper): return seq(self.z(q,helper),self.pi8(q,4))

    def ccz(self,a,b,c,helper):
        assert len(set((a,b,c,helper)))==4
        controls=(a,b,c); out=[]
        for mask in range(8):
            selected=[controls[j] for j in range(3) if (mask>>j)&1]
            parity=[gate('CX',j,helper) for j in selected]
            out.append(seq(*parity,self.pi8(helper,1 if len(selected)%2==0 else 15),*reversed(parity)))
        return seq(*out)

    def ccx(self,a,b,c,helper):
        return seq(self.h(c,helper),self.ccz(a,b,c,helper),self.h(c,helper))

    def controlled_g(self,control,target,inverse=False):
        assert control!=target
        positive=self.angle(target,'half_theta'); negative=self.angle(target,'minus_half_theta')
        first,second=(negative,positive) if inverse else (positive,negative)
        return seq(first,gate('CX',control,target),second,gate('CX',control,target))

    def controlled_pi3(self,control,rebit,inverse=False):
        assert control!=rebit
        positive=self.power(rebit,self.ks['pi6']); negative=self.power(rebit,11*self.ks['pi6'])
        first,second=(negative,positive) if inverse else (positive,negative)
        return seq(first,gate('CX',control,rebit),second,gate('CX',control,rebit))

    def lower(self,tree,*,inverse=False,control=None,helper=None,wire_map=lambda q:q):
        """All-column compilation of an exact ORIGINAL G/CX DAG or its inverse.

        Error units are coefficients of δ=2^-20000, proved by telescoping
        against exact unitary targets. The repeat count multiplies errors of
        original leaves; lowering's new giant G exponents are NOT recompiled.
        """
        op=tree['op']
        if op=='seq':
            children=tree['children'][::-1] if inverse else tree['children']
            pieces=[self.lower(t,inverse=inverse,control=control,helper=helper,wire_map=wire_map) for t in children]
            return seq(*(t for t,e in pieces)),sum(e for t,e in pieces)
        if op=='repeat':
            n=count_value(tree['count'])
            t,e=self.lower(tree['child'],inverse=inverse,control=control,helper=helper,wire_map=wire_map)
            return repeat(n,t),n*e
        assert op in ('G','CX')
        w=tuple(wire_map(q) for q in tree['wires'])
        gate(op,*w)
        assert control is None or control not in w
        if op=='G':
            if control is not None: return self.controlled_g(control,w[0],inverse),2
            return (self.angle(w[0],'minus_theta'),1) if inverse else (gate('G',w[0]),0)
        if control is None: return gate('CX',*w),0
        assert helper is not None
        return self.ccx(control,*w,helper),100


def reverse_replay(factory):
    """Literal finite reverse of an immutable deterministic block provider.

    O(B^2) replay is deliberately explicit and memory bounded. This is a
    mathematical word constructor, not a claim that the production-sized
    stream has been materialised or run. The target is the actual compiled
    A30 stream, never a fresh compilation of its old SourceI inverse.
    """
    n=sum(1 for _ in factory())
    for i in range(n-1,-1,-1): yield next(islice(factory(),i,None))


def a30_owner():
    sys.path.insert(0,str(P.parent/'round30'))
    import marked_source_schedule as s
    return s


def copied_wire(q,copy_base,n=10407050782):
    assert type(copy_base) is int and copy_base>=n and 0<=q<n
    # Existing SAM (2..2689) is shared; every original WORK coordinate is new.
    if 2<=q<2690:return q
    return copy_base+q if q<2 else copy_base+q-2688


def actual_W_factory():
    s=a30_owner()
    for t in s.W_blocks(): yield s.b.physical_tree(t)


def controlled_W_blocks(branch,helper,copy_base,*,inverse=False,macros=None):
    """Finite G/CX blocks approximating controlled actual A30 W or W^T.

    Callers still owe all births, resets, state preparation, full clock,
    retained precision, physical task membership and full-source comparison.
    """
    m=macros or Macros(); n=10407050782; stop=copy_base+n-2688
    assert branch>=stop and helper>=stop and branch!=helper
    blocks=reverse_replay(actual_W_factory) if inverse else actual_W_factory()
    for t in blocks:
        out,error=m.lower(t,inverse=inverse,control=branch,helper=helper,
                          wire_map=lambda q:copied_wire(q,copy_base))
        yield out


def controlled_W_budget(macros=None):
    m=macros or Macros(); s=a30_owner(); census=s.inventory()['W_new']
    g,c=census['G'],census['CX']
    k8=m.ks['pi8']; kh=m.ks['half_theta']; km=m.ks['minus_half_theta']
    return {'G':g*(kh+km)+c*100*k8, 'CX':2*g+28*c,
            'error_units':2*g+100*c,'original_G':g,'original_CX':c}
