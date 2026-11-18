#!/usr/bin/env python3
"""Actual scratch-free all-zero joint reflection via a Gray Walsh cycle.

Target is arbitrary aux: angle pi gives -I_aux on the joint zero anchor.
No target/flag is assumed clean. Only native G and CX appear forward.
Literal inverses retain their real G/CX/SourceI histories and multiplicities.
"""
from pathlib import Path
from collections import Counter
import importlib.util,sys
P=Path(__file__).resolve().parent;D=P.parent
s=importlib.util.spec_from_file_location('a22_nb',D/'round14/native_boolean.py');nb=importlib.util.module_from_spec(s);sys.modules[s.name]=nb;s.loader.exec_module(nb)
def validate(controls,aux,port,spin,protected=()):
    assert len(controls)>=1 and len(spin)==2
    assert len(set([*controls,aux,port,*spin]))==len(controls)+4
    assert not set(protected)&set([*controls,aux,port,*spin])
def block_at(index,controls,aux,k):
    K=len(controls);terms=1<<K;assert 0<=index<=terms and k>0
    if index==0:return nb.repeat(k,nb.gate('G',aux))
    if index==terms:return nb.gate('CX',controls[-1],aux)
    flip=(index&-index).bit_length()-1
    return nb.seq(nb.gate('CX',controls[flip],aux),nb.repeat(k,nb.gate('G',aux)))
def blocks(controls,aux,k,port,spin,protected=(),inverse_depth=0):
    controls=list(controls);spin=tuple(spin);validate(controls,aux,port,spin,protected)
    assert type(inverse_depth) is int and inverse_depth>=0
    total=(1<<len(controls))+1
    indices=reversed(range(total)) if inverse_depth%2 else range(total)
    for index in indices:
        tree=block_at(index,controls,aux,k)
        for _ in range(inverse_depth):tree=nb.inverse_literal(tree,port,spin)
        yield tree
def inverse_counts(c):
    return Counter({'G_port':c['G_port']+c['G_other'],'G_other':0,'CX':c['CX']+6*c['G_other'],
                    'SourceI':3*c['SourceI']+4*(c['G_port']+c['G_other'])})
def counts(K,k,inverse_depth=0):
    assert K>=1 and k>0
    c=Counter({'G_port':0,'G_other':(1<<K)*k,'CX':1<<K,'SourceI':0})
    for _ in range(inverse_depth):c=inverse_counts(c)
    return c
