#!/usr/bin/env python3
"""Lazy linear-zero predicate and its paid native lowering.

This emits one *part* of a proposed state-preparation circuit.  It is not
an emitted U*, and coefficients k_boolean/k_phase require independent
certification at the actually needed precision.  All scratch must be born
and prepared in 0; oldRIGHT/external supports may not be addressed.
"""
from pathlib import Path
import importlib.util,sys
sys.dont_write_bytecode=True
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
spec=importlib.util.spec_from_file_location('owned_native_boolean',D/'round14/native_boolean.py')
nb=importlib.util.module_from_spec(spec);spec.loader.exec_module(nb)

class Ranges:
    """Index a concatenation of ranges without materialising billions of ids."""
    def __init__(self,*ranges):
        self.ranges=tuple(ranges)
        assert all(isinstance(r,range) and r.step==1 for r in ranges)
        self.n=sum(map(len,ranges))
    def __len__(self):return self.n
    def __getitem__(self,i):
        if i<0:i+=self.n
        assert 0<=i<self.n
        for r in self.ranges:
            if i<len(r):return r[i]
            i-=len(r)
        raise IndexError

def zero_predicate_ir(controls,target,work,reverse=False):
    """Exact logical toggle [all controls zero], with clean work restored.

    Lazy O(1) descriptor memory, O(N) emitted gates. Caller owns disjoint
    supports; reverse emits the literal inverse order, not a free identity.
    """
    k=len(controls);assert k>=3 and len(work)>=k-2
    def first():
        return [('X',work[0]),('CX',controls[1],work[0]),
                ('CX',controls[0],work[0]),('CCX',controls[0],controls[1],work[0])]
    def middle(i):
        return [('CX',work[i-2],work[i-1]),('CCX',work[i-2],controls[i],work[i-1])]
    center=[('CX',work[k-3],target),('CCX',work[k-3],controls[k-1],target)]
    yield from first()
    for i in range(2,k-1):yield from middle(i)
    yield from (reversed(center) if reverse else center)
    for i in range(k-2,1,-1):yield from reversed(middle(i))
    yield from reversed(first())

def lower_ir(ir,k_boolean,aux,port,spin):
    """Actual paid compact A14 G/CX/SourceI DAG for a logical IR leaf."""
    op,*w=ir
    if op=='CX':return nb.gate('CX',*w)
    if op=='X':return nb.boolean_word('X',k_boolean,target=w[0],port=port,spin=spin)
    assert op=='CCX'
    return nb.boolean_word('CCX',k_boolean,control=tuple(w[:2]),target=w[2],aux=aux,port=port,spin=spin)

def zero_phase_native(controls,flag,work,rebit,k_boolean,k_phase,aux,port,spin):
    """Paid F; flag-controlled rebit phase; literal inverse F, lazily.

    Semantics depend on certified Boolean/phase errors, explicit work/Spin
    conditions and clean comparator scratch; no certification is invented.
    """
    assert len(controls)>=3
    for op in zero_predicate_ir(controls,flag,work):yield lower_ir(op,k_boolean,aux,port,spin)
    yield nb.selective_rotation([flag],[1],rebit,k_phase,port,spin)
    for op in zero_predicate_ir(controls,flag,work,reverse=True):
        # Approximate native X/CCX need not be exact involutions: reverse the
        # actual lowered tree, with every inverse occurrence and cost intact.
        yield nb.inverse_literal(lower_ir(op,k_boolean,aux,port,spin),port,spin)

def literal_inverse_count(t):
    """Owned T map for primitive counts, including all inverse overhead."""
    return {'G_port':t.get('G_port',0)+t.get('G_other',0),'G_other':0,
            'CX':t.get('CX',0)+6*t.get('G_other',0),
            'SourceI':3*t.get('SourceI',0)+4*(t.get('G_port',0)+t.get('G_other',0))}
