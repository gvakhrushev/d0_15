#!/usr/bin/env python3
"""Finite addressed native preparation of B25 q/y CAR half-vectors.

No quantum private work, free angles, new gate primitives or SAM rewriting.
The huge program is emitted lazily; counts retain all inactive sectors.
"""
from pathlib import Path
from collections import Counter
import importlib.util,json,sys
P=Path(__file__).resolve().parent;D=P.parent
sp=importlib.util.spec_from_file_location('a18_native_boolean',D/'round14/native_boolean.py')
nb=importlib.util.module_from_spec(sp);sys.modules[sp.name]=nb;sp.loader.exec_module(nb)

def plane_geometry(other):
    assert other in (0,14,15)
    diff=1^other;pivot=(diff&-diff).bit_length()-1
    flips=[j for j in range(4) if j!=pivot and (diff>>j)&1]
    anchor=1
    if (anchor>>pivot)&1:
        for j in flips:anchor^=1<<j
    controls=[j for j in range(4) if j!=pivot]
    return {'pivot':pivot,'flips':flips,'grade_controls':controls,
            'grade_pattern':[(anchor>>j)&1 for j in controls],
            'orientation':-1 if (anchor>>pivot)&1 else 1}

def layout():
    return {'SAM':list(range(2688)),'internal_SITE':list(range(2688,2696)),
            'grade':list(range(2696,2700)),'RIGHT':list(range(2700,2707)),
            'port':2707,'spin':[2708,2709],'oldRIGHT_witness':2710,
            'qubits':2711,'private_quantum_work':[]}

def bind_plane(row,rotation,lay,angles):
    g=plane_geometry(rotation['other']);pivot=lay['grade'][g['pivot']]
    controls=lay['internal_SITE']+[lay['SAM'][i] for i in row['SAM_indices']]+[lay['grade'][i] for i in g['grade_controls']]
    pattern=[(row['site']>>j)&1 for j in range(8)]+row['SAM_pattern']+g['grade_pattern']
    K=len(controls);assert K in (11,13)
    assert len(set([pivot,*controls,lay['port'],*lay['spin']]))==K+4
    permutation=[nb.gate('CX',pivot,lay['grade'][j]) for j in g['flips']]
    entry=angles[rotation['angle_id']]
    return {'controls':controls,'pattern':pattern,'target':pivot,
            'permutation':permutation,'k':int(entry['k'])*(2**(13-K)),
            'K':K,'angle_id':rotation['angle_id']}

def pair_blocks(bound,lay,reverse=False):
    """Actual native forward or literal paid inverse, block by block."""
    K=bound['K'];terms=1<<K;port=lay['port'];spin=tuple(lay['spin'])
    order=range(terms+2) if not reverse else reversed(range(terms+2))
    for index in order:
        if index==0:block=nb.seq(*bound['permutation'])
        elif index==terms+1:block=nb.seq(*reversed(bound['permutation']))
        else:
            mask=index-1;subset=[j for j in range(K) if (mask>>j)&1]
            parity=[nb.gate('CX',bound['controls'][j],bound['target']) for j in subset]
            sign=(-1)**sum(bound['pattern'][j] for j in subset)
            block=nb.seq(*parity,nb.rotation_power(bound['target'],sign*bound['k'],port,spin),*reversed(parity))
        yield nb.inverse_literal(block,port,spin) if reverse else block

def preparation_blocks(bank,library,lay=None,reverse=False):
    assert bank in ('q','y+','y-');lay=layout() if lay is None else lay
    rows=library['catalogue'][bank];vectors=library['vectors'];angles=library['angles']
    for row in (reversed(rows) if reverse else rows):
        rots=vectors[row['vector_id']]['rotations']
        for rotation in (reversed(rots) if reverse else rots):
            if rotation['angle_id'] is None:continue
            yield from pair_blocks(bind_plane(row,rotation,lay,angles),lay,reverse)

def pair_counts(bound):
    K=bound['K'];terms=1<<K;negative=terms//2 if any(bound['pattern']) else 0;k=bound['k']
    return Counter({'G_port':negative*k,'G_other':(terms-negative)*k,
                    'CX':K*terms+6*negative+2*len(bound['permutation']),
                    'SourceI':4*negative})

def raw_inverse_counts(counts):
    gp=counts['G_port'];go=counts['G_other']
    return Counter({'G_port':gp+go,'G_other':0,'CX':counts['CX']+6*go,
                    'SourceI':3*counts['SourceI']+4*(gp+go)})

def inventory(library):
    lay=layout();out={}
    for name,rows in library['catalogue'].items():
        forward=Counter();rotations=0
        for row in rows:
            for rotation in library['vectors'][row['vector_id']]['rotations']:
                if rotation['angle_id'] is None:continue
                forward.update(pair_counts(bind_plane(row,rotation,lay,library['angles'])));rotations+=1
        out[name]={'sectors':len(rows),'nonidentity_planar_rotation_occurrences':rotations,
                   'native_forward':{k:str(v) for k,v in forward.items()},
                   'native_literal_inverse':{k:str(v) for k,v in raw_inverse_counts(forward).items()}}
    return out
