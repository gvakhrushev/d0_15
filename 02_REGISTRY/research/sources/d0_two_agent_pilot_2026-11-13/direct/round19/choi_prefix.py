#!/usr/bin/env python3
"""Actual 2049-address/Bell prefix, optionally coherently branch-controlled.

The controlled Julia SELECT is a separate explicit missing operator. No
function here claims to emit the full Omega or half-vector preparation.
"""
from pathlib import Path
from collections import Counter
import importlib.util,sys,json
P=Path(__file__).resolve().parent;D=P.parent
sp=importlib.util.spec_from_file_location('a19_nb',D/'round14/native_boolean.py')
nb=importlib.util.module_from_spec(sp);sys.modules[sp.name]=nb;sp.loader.exec_module(nb)

def layout():
    return {'SAM':list(range(2688)),'address':list(range(2688,2700)),
            'choi_input':list(range(2700,2705)),'choi_output':list(range(2705,2710)),
            'branch':2710,'port':2711,'spin':[2712,2713],
            'aux_arbitrary':2714,'oldRIGHT_witness':2715,'qubits':2716,
            'private_clean_work':[]}

def instructions(lay,controlled):
    outer=[lay['branch']] if controlled else [];bits=[1] if controlled else []
    yield {'op':'address_rotation','controls':outer,'pattern':bits,'target':lay['address'][11]}
    for q in lay['address'][:11]:yield {'op':'H','controls':[lay['address'][11],*outer],'pattern':[0,*bits],'target':q}
    for i,j in zip(lay['choi_input'],lay['choi_output']):
        yield {'op':'H','controls':outer,'pattern':bits,'target':i}
        yield {'op':'X','controls':[i,*outer],'pattern':[1,*bits],'target':j}

def lower(inst,cert,lay):
    controls=inst['controls'];pattern=inst['pattern'];target=inst['target'];K=len(controls)
    assert K<=2 and len(pattern)==K
    assert len(set([*controls,target,lay['port'],*lay['spin'],lay['aux_arbitrary']]))==K+5
    port=lay['port'];spin=tuple(lay['spin']);aux=lay['aux_arbitrary']
    if inst['op']=='address_rotation':
        assert K in (0,1)
        k=int(cert['address_power']['k'])*(2**(1-K))
        return nb.selective_rotation(controls,pattern,target,k,port,spin)
    assert inst['op'] in ('H','X')
    k=int(cert['boolean_common_power']['k'])
    # Same exact native angles for every predicate width, including the
    # optional branch. Phase on arbitrary aux approximates controlled Z.
    phase=nb.selective_rotation([*controls,target],[*pattern,1],aux,(16*k)//(2**(K+1)),port,spin)
    multiplier=4 if inst['op']=='H' else 8
    rotation=nb.selective_rotation(controls,pattern,target,(multiplier*k)//(2**K),port,spin)
    return nb.seq(phase,rotation)

def prefix_blocks(cert,lay=None,controlled=True,reverse=False):
    lay=layout() if lay is None else lay;sequence=list(instructions(lay,controlled))
    for inst in (reversed(sequence) if reverse else sequence):
        tree=lower(inst,cert,lay)
        yield nb.inverse_literal(tree,lay['port'],tuple(lay['spin'])) if reverse else tree

def resource(tree,port):
    if tree['op']=='seq':
        out=Counter()
        for child in tree['children']:out.update(resource(child,port))
        return out
    if tree['op']=='repeat':return Counter({q:int(tree['count'])*v for q,v in resource(tree['child'],port).items()})
    if tree['op']=='G':return Counter({'G_port' if tree['wires'][0]==port else 'G_other':1})
    return Counter({tree['op']:1})

def raw_inverse_counts(c):return Counter({'G_port':c['G_port']+c['G_other'],'G_other':0,'CX':c['CX']+6*c['G_other'],'SourceI':3*c['SourceI']+4*(c['G_port']+c['G_other'])})

def inventory(cert):
    lay=layout();out={}
    for controlled in (False,True):
        forward=Counter();reverse=Counter()
        for block in prefix_blocks(cert,lay,controlled):forward.update(resource(block,lay['port']))
        for block in prefix_blocks(cert,lay,controlled,True):reverse.update(resource(block,lay['port']))
        assert +reverse==+raw_inverse_counts(forward)
        out['controlled' if controlled else 'uncontrolled']={'forward':{q:str(v) for q,v in forward.items()},'literal_inverse':{q:str(v) for q,v in reverse.items()}}
    return out
