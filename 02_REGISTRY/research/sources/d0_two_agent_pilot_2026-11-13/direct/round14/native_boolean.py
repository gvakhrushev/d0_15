#!/usr/bin/env python3
"""Finite native-word DAGs for all-column X, H and CCX approximation.

Leaves are only actual G/CX/SourceI calls. Repeat counts are exact integers.
The common-port negative POWER is a designed new schedule; old raw marks and
prices are not identified with the old letter-by-letter inverse schedule.
"""
from collections import Counter
from itertools import product


def gate(name,*wires):return {'op':name,'wires':list(wires)}
def seq(*children):return {'op':'seq','children':list(children)}
def repeat(count,child):
    assert type(count) is int and count>=1
    return {'op':'repeat','count':str(count),'child':child}
def swap(a,b):return seq(gate('CX',a,b),gate('CX',b,a),gate('CX',a,b))
def source(port,spin):return gate('SourceI',port,*spin)


def z_word(q,port,spin):
    core=seq(source(port,spin),source(port,spin))
    return core if q==port else seq(swap(q,port),core,swap(q,port))


def rotation_power(q,k,port,spin):
    assert k!=0 and q not in spin
    if k>0:return repeat(k,gate('G',q))
    # Exact G^(-m)=Z G^m Z; the entire power remains on port between SWAPs.
    core=seq(source(port,spin),source(port,spin),repeat(-k,gate('G',port)),
             source(port,spin),source(port,spin))
    return core if q==port else seq(swap(q,port),core,swap(q,port))


def selective_rotation(controls,pattern,target,k,port,spin):
    """Owned Walsh identity, all columns; no clean target assumption needed."""
    assert len(controls)==len(pattern) and len(set(controls))==len(controls)
    assert target not in controls and k>=1 and all(b in (0,1) for b in pattern)
    assert not set(controls+[target]).intersection([port,*spin])
    terms=[]
    for mask in range(2**len(controls)):
        subset=[i for i in range(len(controls)) if (mask>>i)&1]
        parity=[gate('CX',controls[i],target) for i in subset]
        sign=(-1)**sum(pattern[i] for i in subset)
        terms.append(seq(*parity,rotation_power(target,sign*k,port,spin),*reversed(parity)))
    return seq(*terms)


def boolean_word(name,k,control=(0,1),target=2,aux=3,port=4,spin=(5,6)):
    if name in ('X','H'):
        assert len(set([target,port,*spin]))==4
        multiplier=4 if name=='X' else 2
        return seq(z_word(target,port,spin),rotation_power(target,multiplier*k,port,spin))
    assert name=='CCX'
    assert len(set([*control,target,aux,port,*spin]))==7
    # At alpha=4*k*theta=pi/2 mod2pi, the first block is conditional Z_t
    # with identity on arbitrary aux; the second is conditional J_t.
    return seq(selective_rotation([*control,target],[1,1,1],aux,k,port,spin),
               selective_rotation(list(control),[1,1],target,k,port,spin))


def inverse_literal(tree,port,spin):
    """True paid raw reverse: expand inverse of EACH actual primitive leaf.

In particular a repeat of positive G becomes that many 5/11-call inverses;
it is NOT silently replaced by a cheaper newly routed inverse power.
"""
    op=tree['op']
    if op=='seq':return seq(*(inverse_literal(x,port,spin) for x in reversed(tree['children'])))
    if op=='repeat':return repeat(int(tree['count']),inverse_literal(tree['child'],port,spin))
    if op=='CX':return tree
    if op=='SourceI':return repeat(3,tree)
    assert op=='G'
    return rotation_power(tree['wires'][0],-1,port,spin)


def counts(tree):
    op=tree['op']
    if op=='seq':
        total=Counter()
        for child in tree['children']:total.update(counts(child))
        return dict(total)
    if op=='repeat':return {k:int(tree['count'])*v for k,v in counts(tree['child']).items()}
    return {op:1}


def leaves(tree):
    """Each syntactic primitive leaf once; not the giant expanded word."""
    if tree['op']=='seq':
        for child in tree['children']:yield from leaves(child)
    elif tree['op']=='repeat':yield from leaves(tree['child'])
    else:yield tree


def expand(tree,limit):
    assert sum(counts(tree).values())<=limit,'explicit expansion bound exceeded'
    def rec(t):
        if t['op']=='seq':
            for x in t['children']:yield from rec(x)
        elif t['op']=='repeat':
            for _ in range(int(t['count'])):yield from rec(t['child'])
        else:yield t
    yield from rec(tree)


def validate_schema(tree,qubits,port,spin,old_right):
    """Inductive validation of all expansion leaves and exact repetition sizes."""
    op=tree['op']
    if op=='seq':
        assert isinstance(tree['children'],list)
        for child in tree['children']:validate_schema(child,qubits,port,spin,old_right)
        return
    if op=='repeat':
        assert str(int(tree['count']))==tree['count'] and int(tree['count'])>=1
        validate_schema(tree['child'],qubits,port,spin,old_right);return
    assert op in ('G','CX','SourceI')
    wires=tree['wires'];assert len(wires)=={'G':1,'CX':2,'SourceI':3}[op]
    assert len(set(wires))==len(wires) and all(type(w) is int and 0<=w<qubits for w in wires)
    assert not set(wires).intersection(old_right)
    if op=='SourceI':assert wires==[port,*spin]
    else:assert not set(wires).intersection(spin)
