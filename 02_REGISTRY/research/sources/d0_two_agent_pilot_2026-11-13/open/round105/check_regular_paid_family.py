#!/usr/bin/env python3
"""Check field-bound A54 use, conditional positivity, clock and small post."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from hashlib import sha256
from itertools import islice
import json,sys
import mpmath as mp
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P))
import regular_paid_family as r
sys.path.insert(0,str(r.D/'round54'))
import regular_global_source as api
p=r.paid

# Verify both owner receipts against their exact dependencies before use.
a54=r.D/'round54'
for receipt in ('REGULAR_GLOBAL_SOURCE_PLAN.json','REGULAR_GLOBAL_SOURCE_CHECK.json'):
    data=json.loads((a54/receipt).read_text())
    for name,digest in data['source_sha256'].items():
        assert sha256(Path(name).read_bytes()).hexdigest()==digest,(receipt,name)
assert json.loads((a54/'REGULAR_GLOBAL_SOURCE_CHECK.json').read_text())['status']=='PASS_PARAMETERIZED_SOURCE_GLOBAL_COMPOSITION'

# Uniform lower bound, exact rational, conditional on all inherited premises.
u=api.upper_inventory_and_error();e=u['full_canonical_compressed_error']
assert e<F(1,1<<3421) and u['full_SOURCE_DATA_fibre_prefix_error']<F(1,1<<3423)
margin=r.source_positive_margin(e)
assert margin['source_drift_lt']==F(181792,1<<32)
assert margin['actual_diagonal_lower_gt']>F(669,1000)>F(2,3)
assert 2688<52**2
try:r.source_positive_margin(F(1,1<<3421))
except ValueError:pass
else:raise AssertionError('non-strict error accepted')

# Two immutable actual field/source objects share layout and one common
# certified core upper but never share their field-bound actual target.
field0=api.t.FieldCentre()
values=[F(0)]*2688;values[0]=F(1,1<<34);values[1024]=F(-1,1<<35);values[2560]=F(1,1<<36)
field1=api.t.FieldCentre(tuple(values))
upper=u['W_G_CX_upper'];f0=r.RegularPaidFamily(api,field0,upper);f1=r.RegularPaidFamily(api,field1,upper)
for family,field in ((f0,field0),(f1,field1)):
    assert family.source.field is field and family.source.sources.field is field
    assert family.source.sources.components.field is field
    assert family.actual_core_target().factory.__self__ is family.source
    assert family.actual_core_target().factory.__func__ is family.source.core_blocks.__func__
    assert family.actual_core_target() is family.actual_core_target()
assert f0.actual_core_target() is not f1.actual_core_target()
assert f0.actual_core_target().factory.__self__ is not p.source
assert f0.field_packet!=f1.field_packet
for k in ('n','sam','m','coreL','controlL','postL','probeL','Lbase','Nbase','K','dimension_debt'):
    assert f0.cfg[k]==f1.cfg[k],k
old=p.production_configuration()
assert f0.cfg['Nbase'].bit_length()==30833 and f0.cfg['K']==175604
assert f0.cfg['Nbase']!=old['Nbase'] and f0.cfg['coreL']!=old['coreL']
assert f0.bounds()['post_skew_dual_error']<F(1,1<<661)
assert f0.bounds()['heat_full_skew_dual_error']<F(1,1<<75)
assert f0.bounds()['post_corner_lower']>F(2,3)
# The real A54 field-specific coframe provider sees the coordinate change;
# differing certified k are evidence of two different actual native words,
# not a calculation of their intractable full production compressions.
row=next(z for z in api.t.coframe_rows('f') if 0 in z['coordinates'])
digits=(0,1,2,3)
lib0=f0.source.sources.components.coframe_library(row,digits)
lib1=f1.source.sources.components.coframe_library(row,digits)
keys=set(lib0['angles']) & set(lib1['angles'])
assert any(lib0['angles'][key]['k']!=lib1['angles'][key]['k'] for key in keys if key!='X')

# Guard detects changing *either* exposed field or the component field.
f0.source.field=field1
try:f0.actual_core_target()
except RuntimeError:pass
else:raise AssertionError('changed source field accepted')
f0.source.field=field0
f0.source.sources.components.field=field1
try:f0.blocks().__next__()
except RuntimeError:pass
else:raise AssertionError('changed component field accepted')
f0.source.sources.components.field=field0
bad=Counter(upper);bad['G']=0
try:r.RegularPaidFamily(api,field0,bad)
except ValueError:pass
else:raise AssertionError('inadequate core upper accepted')

# The production word really starts with the proper four-slot control,
# including paid control padding. Never expands the huge source/post.
cases=[('centre',0,0,None),('matched',1,0,None),('Pf',-1,2687,None),
       ('Qf',1,0,None),('Qb',-1,2687,None),('Pb',1,0,None),
       ('post_probe',1,0,(0,(1<<5376)-1))]
starts=0
for arm,sign,axis,plane in cases:
    sign_pf=p.slot_signs(arm,sign)['Pf']
    expected=p.pad.counted_pad(lambda:p.raw_control_factory(axis,sign_pf),f1.cfg['controlL'],f1.cfg['sam'])
    lhs=list(islice(f1.blocks(arm=arm,sign=sign,axis=axis,plane=plane),6))
    rhs=list(islice(expected,6))
    # A zero control can yield fewer than 6 blocks; following SOURCE is not
    # part of this first-slot comparison, so compare the entire RHS prefix.
    assert lhs[:len(rhs)]==rhs and rhs
    starts+=1

# A small actual G/CX path sum: swapping which CODE bit controls the real
# source changes M(label=1), and that change reaches the chosen post target.
nb=p.native
sa=p.target.ActualDiagonal(4,(0,1,2),lambda:iter([nb.gate('CX',0,3)]))
sb=p.target.ActualDiagonal(4,(0,1,2),lambda:iter([nb.gate('CX',1,3)]))
iv=p.target.e.Dyadic(256);ea=sa.entry(1,iv);eb=sb.entry(1,iv)
assert ea[1]<eb[0]
with mp.workdps(100):
    golden=(mp.sqrt(5)-1)/2;v=2*mp.sqrt(golden)*golden
    assert mp.mpf(int(ea[0]))/iv.S<v<mp.mpf(int(ea[1]))/iv.S
    assert mp.mpf(int(eb[0]))/iv.S<=1<=mp.mpf(int(eb[1]))/iv.S
pa=p.target.PositiveTarget(sa);pb=p.target.PositiveTarget(sb)
ca,ta=pa.star('h',1,256);cb,tb=pb.star('h',1,256)
assert ta[1]<tb[0] or tb[1]<ta[0]
# Use the actual uniform-grid selector for each real path-derived target;
# no fixed ideal M table or old source enters either target.
ka=p.target.select_from_intervals(lambda bits:pa.star('h',1,bits))
kb=p.target.select_from_intervals(lambda bits:pb.star('h',1,bits))
assert ka!=kb

# An alternative path for one logical slot must really remain independent.
for s in (-1,1):
    assert p.slot_signs('matched',s)==dict(Pf=s,Qf=-s,Qb=s,Pb=-s)
    for arm in ('Pf','Qf','Qb','Pb'):
        signs=p.slot_signs(arm,s)
        assert sum(v!=0 for v in signs.values())==1 and signs[arm]!=0

paths=[P/'regular_paid_family.py',P/'check_regular_paid_family.py',r.D/'round49/two_bit_paid_family.py',
       r.D/'round49/finite_actual_target.py',r.D/'round54/regular_global_source.py',
       r.D/'round54/regular_source_native.py',r.D/'round54/REGULAR_GLOBAL_SOURCE_PLAN.json',
       r.D/'round54/check_regular_global_source.py',r.D/'round54/REGULAR_GLOBAL_SOURCE_CHECK.json',
       r.D/'round54/REGULAR_GLOBAL_SOURCE_RU.md',
       P.parent/'round91/B91_FULL_VECTOR_JET_AND_SOURCE_FIBRE_RU.md']
out={'status':'PASS_B105_FIELD_BOUND_ACTUAL_POST_CONDITIONAL',
     'A54_source_science_frozen_at_time_of_check':True,
     'positivity_conditional_on_A54_B91_and_CODE_control_only':True,
     'uniform_actual_M_lower_gt':'669/1000','post_corner_lower_gt':'2/3',
     'same_uniform_new_clock_for_two_field_names':True,
     'new_Nbase_is_not_old_A49_Nbase':True,'new_Nbase_bit_length':f0.cfg['Nbase'].bit_length(),
     'new_K':f0.cfg['K'],'path_sum_and_post_provider_bound_to_new_source':True,
     'actual_A54_coframe_angle_word_changes_with_field':True,
     'small_actual_G_CX_sources_give_different_M_and_post_powers':True,
     'seven_actual_control_start_smokes':starts,
     'four_independent_slots_preserved':True,
     'post_skew_dual_error_lt':'2^-661','full_heat_skew_dual_error_lt':'2^-75',
     'source_stationarity_at_nonzero_Y_proved':False,'physical_C_closed':False,'GR_closed':False,
     'input_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in paths}}
(P/'B105_REGULAR_PAID_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='input_sha256'},indent=2))
