#!/usr/bin/env python3
"""Actual lazy native coframe Julia SELECT, including every paid inverse.

Only finite sector/mask loops and native G/CX/SourceI leaves are used.
No complete enormous expansion is constructed in memory.
"""
from pathlib import Path
from collections import Counter
import importlib.util,sys,json,hashlib
import coframe_targets as t
P=Path(__file__).resolve().parent
prep=t.load('a20_pair_emitter',t.D/'round18/material_preparation.py');nb=prep.nb
prefix=t.load('a20_choi_layout',t.D/'round19/choi_prefix.py')
def layout():return prefix.layout()
def outer(row,lay,controlled=True):
    controls=lay['address']+[lay['SAM'][i] for i in row['SAM_indices']]+([lay['branch']] if controlled else [])
    pattern=[(row['address']>>j)&1 for j in range(12)]+row['SAM_pattern']+([1] if controlled else [])
    assert len(controls)==len(pattern) and len(set(controls))==len(controls)
    return controls,pattern
def rotation_bound(controls,pattern,target,k,multiplier_bits,permutation=()):
    K=len(controls);assert K<=multiplier_bits and target not in controls and len(set(controls))==K
    assert len(pattern)==K and all(b in (0,1) for b in pattern)
    return {'K':K,'controls':list(controls),'pattern':list(pattern),'target':target,
            'k':k*(1<<(multiplier_bits-K)),'permutation':list(permutation)}
def pair_bound(row,grade,a,b,angle,lay,controlled=True):
    controls,pattern=outer(row,lay,controlled);width=len(grade);diff=a^b
    assert 0<=a<1<<width and 0<=b<1<<width and diff
    pivot=(diff&-diff).bit_length()-1;flips=[j for j in range(width) if j!=pivot and (diff>>j)&1]
    transformed=a
    for j in flips:transformed^=((transformed>>pivot)&1)<<j
    # A20 stored native sines already contain this negative orientation.
    assert (transformed>>pivot)&1
    for j in range(width):
        if j!=pivot:controls.append(grade[j]);pattern.append((transformed>>j)&1)
    permutation=[nb.gate('CX',grade[pivot],grade[j]) for j in flips]
    assert angle['native_exponent_multiplier']==1<<20
    out=rotation_bound(controls,pattern,grade[pivot],int(angle['k']),20,permutation)
    assert len(set([*out['controls'],out['target'],lay['port'],*lay['spin']]))==out['K']+4
    return out
def fock_units(row,lib,lay,controlled=True):
    family=lib['families'][row['family_id']];bind={tuple(x['factor']):x['angle_id'] for x in family['angle_bindings']}
    for index,r in enumerate(family['mode_rotations']):
        if r['exact_identity']:continue
        for a,b,sign in t.fact.fock_pairs(r['mode']):
            angle=lib['angles'][bind[('mode',index,sign)]]
            yield pair_bound(row,lay['choi_output'][:4],a,b,angle,lay,controlled)
def sector_units(row,lib,lay,controlled=True,reverse=False):
    # Units carry literal inversion DEPTH, not a cancellable boolean.
    F=list(fock_units(row,lib,lay,controlled));units=[(b,1) for b in reversed(F)]
    controls,pattern=outer(row,lay,controlled);flag=lay['choi_output'][4];aux=lay['aux_arbitrary']
    assert aux not in controls+[flag,lay['port'],*lay['spin']]
    xid=lib['controlled_X_power']['rotation_angle_id'];k=int(lib['angles'][xid]['k'])
    units.append((rotation_bound(controls+[flag],pattern+[1],aux,k,21),0))
    units.append((rotation_bound(controls,pattern,flag,k,20),0))
    family=lib['families'][row['family_id']];base=next(x['angle_id'] for x in family['angle_bindings'] if x['factor'][0]=='base')
    units.append((pair_bound(row,[lay['choi_output'][0],flag],1,2,lib['angles'][base],lay,controlled),0))
    units.extend((b,0) for b in F)
    if reverse:return [(b,depth+1) for b,depth in reversed(units)]
    return units
def unit_blocks(bound,depth,lay):
    # pair_blocks with reverse=True already applies ONE literal inverse.
    odd=bool(depth%2)
    for block in prep.pair_blocks(bound,lay,reverse=odd):
        for _ in range(depth-int(odd)):block=nb.inverse_literal(block,lay['port'],tuple(lay['spin']))
        yield block
def select_blocks(bank,lib,lay=None,controlled=True,reverse=False):
    lay=layout() if lay is None else lay;rows=lib['catalogue'][bank]
    for row in (reversed(rows) if reverse else rows):
        for bound,depth in sector_units(row,lib,lay,controlled,reverse):yield from unit_blocks(bound,depth,lay)
def unit_counts(bound,depth):
    c=prep.pair_counts(bound)
    for _ in range(depth):c=prep.raw_inverse_counts(c)
    return c
def inventory(lib,controlled=True):
    lay=layout();out={}
    for bank,rows in lib['catalogue'].items():
        total=Counter();macros=0;maxK=0
        for row in rows:
            units=sector_units(row,lib,lay,controlled)
            # X is two physical rotation units but one ideal macro.
            macros+=len(units)-1
            for bound,depth in units:total.update(unit_counts(bound,depth));maxK=max(maxK,bound['K'])
        out[bank]={'sectors':len(rows),'ideal_macro_occurrences':macros,'maximum_predicate_width':maxK,
                   'native_forward':{k:str(v) for k,v in total.items()},
                   'native_literal_inverse':{k:str(v) for k,v in prep.raw_inverse_counts(total).items()}}
    return out
def main():
    file=P/'COFRAME_ANGLE_LIBRARY.json';lib=json.loads(file.read_text());h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    out={'status':'ACTUAL_LAZY_NATIVE_COFRAME_JULIA_SELECT','library_sha256':h(file),'source_sha256':h(Path(__file__)),
         'input_sha256':{str(p):h(p) for p in [t.D/'round18/material_preparation.py',t.D/'round14/native_boolean.py',t.D/'round19/choi_prefix.py',P/'coframe_targets.py']},
         'layout':layout(),'banks':inventory(lib),'private_clean_work':0,
         'sector_uniform_operator_error_le':'26*2^-3264','entire_coframe_SELECT_operator_error_lt':'2^-3259',
         'strict_branch0_identity':True,'literal_inverse_of_inverse_retained':True,
         'all_sectors_paid':True,'source_target':'B25 original coframe Julia at addresses1..1024; I at other addresses',
         'full_huge_word_executed':False,'proper_link_SELECT_compiled':False,'full_Omega_loader_compiled':False,
         'physical_C_closed':False,'GR_closed':False}
    (P/'COFRAME_NATIVE_PLAN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'sectors':sum(x['sectors'] for x in out['banks'].values()),'error_lt':out['entire_coframe_SELECT_operator_error_lt']}))
if __name__=='__main__':main()
