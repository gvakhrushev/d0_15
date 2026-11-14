#!/usr/bin/env python3
"""Compose A23 RAW vacuum/Fourier with the actual A18 full CAR map.

Three predicate-zero wires are explicitly prepared from three RAW v wires.
The target is the declared A23 extension followed by the original B25 M_b.
Admission, original marked-prefix equivalence and full physical C stay open.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from functools import lru_cache
import hashlib,importlib.util,json,sys
P=Path(__file__).resolve().parent;D=P.parent
sys.path.insert(0,str(D/'round18'))
import car_frame as f
s=importlib.util.spec_from_file_location('a24_vacuum',D/'round23/car_vacuum_prefix.py');v=importlib.util.module_from_spec(s);sys.modules[s.name]=v;s.loader.exec_module(v)
nb=f.m.nb
def layout():return f.layout()
def private(l):return [l['predicate_flag'],*l['predicate_work']]
def validate(l,extra_external=()):
    v.validate(l,[*private(l),l['native_aux_arbitrary'],*extra_external])
    assert len(private(l))==3 and len(l['SAM'])==2688
@lru_cache(maxsize=1)
def library():return json.loads((D/'round18/MATERIAL_PREPARATION_LIBRARY.json').read_text())
def invert(t,depth,l):
    for _ in range(depth):t=nb.inverse_literal(t,l['port'],tuple(l['spin']))
    return t
def material_blocks(bank,l,depth):
    odd=depth%2
    for t in f.m.preparation_blocks(bank,library(),l,reverse=bool(odd)):yield invert(t,depth-odd,l)
def frame_stages(depth):
    stages=[('STAR',1),('R',0),('STAR',0),('M',1),('R',0),('M',0)]
    return [(kind,depth+d) for kind,d in (reversed(stages) if depth%2 else stages)]
def frame_blocks(bank,l=None,depth=0):
    l=layout() if l is None else l;U,Ui,R=f.fixed_components(l)
    assert type(depth) is int and depth>=0 and bank in ('y+','y-','f','0','x+','x-','q')
    for kind,d in frame_stages(depth):
        if kind=='M' and bank in ('y+','y-','q'):yield from material_blocks(bank,l,d)
        else:yield invert(R if kind=='R' else U,d,l)
def source_blocks(bank,l=None,depth=0,extra_external=()):
    l=layout() if l is None else l;validate(l,extra_external)
    assert type(depth) is int and depth>=0
    groups=['PRIVATE_RAW','VACUUM','FRAME']
    for group in (reversed(groups) if depth%2 else groups):
        if group=='PRIVATE_RAW':
            qs=private(l)
            for q in (reversed(qs) if depth%2 else qs):yield invert(nb.rotation_power(q,-1,l['port'],tuple(l['spin'])),depth,l)
        elif group=='VACUUM':yield from v.prefix_blocks(l,depth,[*private(l),l['native_aux_arbitrary'],*extra_external])
        else:yield from frame_blocks(bank,l,depth)
def inventory(bank):
    old=json.loads((D/'round18/CAR_FRAME_PLAN.json').read_text())['banks'][bank]
    frame=Counter({k:int(z) for k,z in old['native_forward'].items()});vac=v.inventory()['prefix_forward'];raw=Counter({'G_port':3,'G_other':0,'CX':18,'SourceI':12})
    full=raw+vac+frame
    return {'predicate3_RAW_to_zero':raw,'vacuum19_RAW_prefix':vac,'CAR_frame':frame,'source_forward':full,'source_literal_inverse':v.inverse_price(full)}
def error_bound(bank):
    prefix=v.error_bound()[1];frame=Fraction(0) if bank in ('f','0','x+','x-') else 28*Fraction(1,2**4096)
    error=prefix+frame;assert error<Fraction(1,2**3259)
    return error
def main():
    l=layout();validate(l);h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    pins=[Path(__file__),D/'round23/car_vacuum_prefix.py',D/'round23/CAR_VACUUM_PREFIX_PLAN.json',D/'round23/CAR_VACUUM_PREFIX_CHECK.json',
          D/'round18/car_frame.py',D/'round18/material_preparation.py',D/'round18/MATERIAL_PREPARATION_LIBRARY.json',D/'round18/CAR_FRAME_PLAN.json',D/'round18/CAR_FRAME_CHECK.json']
    banks={}
    for bank in ('y+','y-','f','0','x+','x-','q'):
        error=error_bound(bank)
        banks[bank]={'native':{name:{k:str(c[k]) for k in ('G_port','G_other','CX','SourceI')} for name,c in inventory(bank).items()},
                     'error_numerator_hex':hex(error.numerator),'error_denominator_hex':hex(error.denominator),'full_operator_on_declared_predicate_RAW_fibre_error_lt':'2^-3259',
                     'CAR_frame_exact_identity':bank in ('f','0','x+','x-')}
    all_error=sum((16*error_bound(bank) for bank in banks),Fraction());assert all_error<Fraction(1,2**3252)
    out={'status':'CONCRETE_RAW_CAR_SOURCE_WITH_VACUUM_AND_FULL_FRAME','source_sha256':{str(p):h(p) for p in pins},'layout':l,
         'chronology':['predicate3 RAW inverse','A23 source19 RAW vacuum/Fourier prefix','A18 actual full CAR frame'],
         'source_RAW_wires':19,'predicate_RAW_wires':3,'additional_unpriced_clean_inputs':0,'native_aux_arbitrary_requires_physical_WORK_or_protected_factor_binding':True,
         'all_source19_columns_covered_on_declared_predicate_RAW_fibre':True,
         'ideal_born_output':'sum_x,grade,r m_b(x)[grade]*chi_ref(x,r)|x,grade,r> tensor |0^3>predicate',
         'prefix_full_column_extension':'The explicit A23 extension, not an unidentified old marked prefix',
         'all7_banks':banks,'all112_sources_error_lt':'2^-3252','all112_error_numerator_hex':hex(all_error.numerator),'all112_error_denominator_hex':hex(all_error.denominator),
         'literal_inverse_integer_depth_retained':True,'constant_CAR_maps_keep_all_paid_stages':True,
         'hybrid_uses_ideal_clean_predicate_prefixes':True,'actual_private_output_is_not_assumed_exactly_clean':True,
         'physical_births_marks_admission_proved':False,'actual_T6_scalar_proved':False,'full_giant_word_executed':False,'physical_C_closed':False,'GR_closed':False}
    (P/'FULL_CAR_SOURCE_PLAN.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'total_RAW_wires_per_source':22,'all112_sources_error_lt':out['all112_sources_error_lt']}))
if __name__=='__main__':main()
