#!/usr/bin/env python3
"""Concrete two-bit coframe/CAR native grammars and exact paid inventories.

Reuses only generic primitive emitters. Sector binders, CODE widths and
common-angle multipliers are explicitly replaced. Literal inverse depth
is retained; the huge expanded words are deliberately not materialized.
"""
from pathlib import Path
from collections import Counter
from functools import lru_cache
import gzip,json,sys
sys.dont_write_bytecode=True
import two_bit_source_targets as t
P=Path(__file__).resolve().parent
sys.path.insert(0,str(t.D/'round20'));sys.path.insert(0,str(t.D/'round18'))
cf=t.load('a48_old_coframe_native',t.D/'round20/coframe_native.py')
car=t.load('a48_old_car_frame',t.D/'round18/car_frame.py')
prep=cf.prep;nb=prep.nb

@lru_cache(None)
def library(kind):
    assert kind in ('COFRAME','MATERIAL')
    with gzip.open(P/f'TWO_BIT_{kind}_LIBRARY.json.gz','rt') as f:return json.load(f)

def extend_layout(lay):
    """Only standalone old layouts; production owner must bind actual wires."""
    def move(value):
        if type(value) is int:return value+2688 if value>=2688 else value
        if isinstance(value,list):return [move(x) for x in value]
        return value
    out={key:move(value) for key,value in lay.items()};out['SAM']=list(range(5376))
    if 'all_SAM' in out:out['all_SAM']=out['SAM']
    return out

def coframe_layout():return extend_layout(cf.layout())
def material_layout():return extend_layout(car.layout())

def pair_bound(row,grade,a,b,angle,lay,controlled=True):
    controls,pattern=cf.outer(row,lay,controlled);width=len(grade);diff=a^b
    assert 0<=a<1<<width and 0<=b<1<<width and diff
    pivot=(diff&-diff).bit_length()-1
    flips=[j for j in range(width) if j!=pivot and (diff>>j)&1]
    transformed=a
    for j in flips:transformed^=((transformed>>pivot)&1)<<j
    assert (transformed>>pivot)&1
    for j in range(width):
        if j!=pivot:controls.append(grade[j]);pattern.append((transformed>>j)&1)
    permutation=[nb.gate('CX',grade[pivot],grade[j]) for j in flips]
    assert angle['native_exponent_multiplier']==1<<24
    out=cf.rotation_bound(controls,pattern,grade[pivot],int(angle['k']),24,permutation)
    assert len(set([*out['controls'],out['target'],lay['port'],*lay['spin']]))==out['K']+4
    return out

def fock_units(row,lib,lay,controlled=True):
    fam=lib['families'][row['family_id']]
    bind={tuple(x['factor']):x['angle_id'] for x in fam['angle_bindings']}
    for index,r in enumerate(fam['mode_rotations']):
        if r['exact_identity']:continue
        for a,b,sign in t.cf.fact.fock_pairs(r['mode']):
            yield pair_bound(row,lay['choi_output'][:4],a,b,
                 lib['angles'][bind[('mode',index,sign)]],lay,controlled)

def coframe_units(row,lib,lay,controlled=True,depth=0):
    assert type(depth) is int and depth>=0
    F=list(fock_units(row,lib,lay,controlled));units=[(b,1) for b in reversed(F)]
    controls,pattern=cf.outer(row,lay,controlled)
    flag=lay['choi_output'][4];aux=lay['aux_arbitrary']
    assert aux not in controls+[flag,lay['port'],*lay['spin']]
    xid=lib['controlled_X_power']['rotation_angle_id'];k=int(lib['angles'][xid]['k'])
    units.extend([(cf.rotation_bound(controls+[flag],pattern+[1],aux,k,25),0),
                  (cf.rotation_bound(controls,pattern,flag,k,24),0)])
    fam=lib['families'][row['family_id']]
    base=next(x['angle_id'] for x in fam['angle_bindings'] if x['factor'][0]=='base')
    units.append((pair_bound(row,[lay['choi_output'][0],flag],1,2,lib['angles'][base],lay,controlled),0))
    units.extend((b,0) for b in F)
    return [(b,d+depth) for b,d in (reversed(units) if depth%2 else units)]

def coframe_blocks(bank,lay=None,controlled=True,depth=0):
    lay=coframe_layout() if lay is None else lay;lib=library('COFRAME')
    rows=t.coframe_sectors(lib['catalogue_templates'],bank)
    if depth%2:rows=reversed(list(rows))
    for row in rows:
        for bound,d in coframe_units(row,lib,lay,controlled,depth):
            yield from cf.unit_blocks(bound,d,lay)

def bind_material(row,rotation,lay,angles):
    geom=prep.plane_geometry(rotation['other']);pivot=lay['grade'][geom['pivot']]
    controls=lay['internal_SITE']+[lay['SAM'][i] for i in row['SAM_indices']]+[lay['grade'][i] for i in geom['grade_controls']]
    pattern=[(row['site']>>j)&1 for j in range(8)]+row['SAM_pattern']+geom['grade_pattern']
    K=len(controls);assert K in (11,15)
    assert len(set([pivot,*controls,lay['port'],*lay['spin']]))==K+4
    entry=angles[rotation['angle_id']];assert entry['native_exponent_multiplier']==1<<15
    return {'controls':controls,'pattern':pattern,'target':pivot,'K':K,
      'permutation':[nb.gate('CX',pivot,lay['grade'][j]) for j in geom['flips']],
      'k':int(entry['k'])*(1<<(15-K)),'angle_id':rotation['angle_id']}

def material_blocks(bank,lay=None,depth=0):
    assert type(depth) is int and depth>=0
    lay=material_layout() if lay is None else lay;lib=library('MATERIAL')
    rows=lib['catalogue'][bank]
    for row in (reversed(rows) if depth%2 else rows):
        rots=lib['vectors'][row['vector_id']]['rotations']
        for rot in (reversed(rots) if depth%2 else rots):
            if rot['angle_id'] is not None:
                yield from cf.unit_blocks(bind_material(row,rot,lay,lib['angles']),depth,lay)

def invert(tree,depth,lay):
    for _ in range(depth):tree=nb.inverse_literal(tree,lay['port'],tuple(lay['spin']))
    return tree

def frame_blocks(bank,lay=None,depth=0):
    lay=material_layout() if lay is None else lay
    U,_,R=car.fixed_components(lay)
    stages=[('STAR',1),('R',0),('STAR',0),('M',1),('R',0),('M',0)]
    for kind,d in (reversed(stages) if depth%2 else stages):
        if kind=='M' and bank in ('q','y+','y-'):
            yield from material_blocks(bank,lay,depth+d)
        else:yield invert(R if kind=='R' else U,depth+d,lay)

def stringify(counts):return {k:str(counts[k]) for k in ('G_port','G_other','CX','SourceI')}

def coframe_inventory():
    lib=library('COFRAME');lay=coframe_layout();out={}
    for bank in lib['catalogue_templates']:
        total=Counter();macros=0;maxK=0;sectors=0
        for row in t.coframe_sectors(lib['catalogue_templates'],bank):
            units=coframe_units(row,lib,lay);sectors+=1;macros+=len(units)-1
            for bound,depth in units:
                total.update(cf.unit_counts(bound,depth));maxK=max(maxK,bound['K'])
        out[bank]={'sectors':sectors,'ideal_macro_occurrences':macros,
          'maximum_predicate_width':maxK,'native_forward':stringify(total),
          'native_literal_inverse':stringify(prep.raw_inverse_counts(total))}
    return out

def material_inventory():
    lib=library('MATERIAL');lay=material_layout();preps={};frames={}
    for bank,rows in lib['catalogue'].items():
        total=Counter();rotations=0
        for row in rows:
            for rot in lib['vectors'][row['vector_id']]['rotations']:
                if rot['angle_id'] is not None:
                    total.update(prep.pair_counts(bind_material(row,rot,lay,lib['angles'])));rotations+=1
        preps[bank]={'sectors':len(rows),'rotations':rotations,
          'native_forward':stringify(total),'native_literal_inverse':stringify(prep.raw_inverse_counts(total))}
    U,Ui,R=car.fixed_components(lay);base=car.resource(U,lay['port'])+car.resource(Ui,lay['port'])
    rr=car.resource(R,lay['port']);base.update({k:2*v for k,v in rr.items()})
    for bank in ('f','0','x+','x-','q','y+','y-'):
        total=Counter(base)
        if bank in preps:
            for key in ('native_forward','native_literal_inverse'):
                total.update({k:int(v) for k,v in preps[bank][key].items()})
        else:total.update(car.resource(U,lay['port']));total.update(car.resource(Ui,lay['port']))
        frames[bank]={'native_forward':stringify(total),
          'native_literal_inverse':stringify(prep.raw_inverse_counts(total))}
    return {'preparations':preps,'frames':frames}

def main():
    out={'status':'CONCRETE_TWO_BIT_LOCAL_NATIVE_GRAMMARS',
      'coframe':coframe_inventory(),'material':material_inventory(),
      'coframe_operator_error_le':'26*2^-3456','material_half_vector_operator_error_le':'3*2^-3456',
      'full_expanded_words_executed':False,'new_full_SOURCE_compiled':False,
      'physical_C_closed':False,'GR_closed':False}
    (P/'TWO_BIT_LOCAL_NATIVE_PLAN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'coframe_sectors':sum(b['sectors'] for b in out['coframe'].values())}))

if __name__=='__main__':main()
