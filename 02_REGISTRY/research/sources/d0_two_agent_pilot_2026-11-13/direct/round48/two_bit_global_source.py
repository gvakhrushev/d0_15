#!/usr/bin/env python3
"""Bind the new SOURCE to A46's eight-report carrier and replace SourceI.

The appended high CODE bits are born explicitly. The old helper and all
existing report/source addresses stay fixed. This is a new finite G/CX word,
not a claim about the original physical history, selected price, or its
complete marked clock/postprocessing family.
"""
from pathlib import Path
from collections import Counter
from copy import deepcopy
from fractions import Fraction as F
from functools import lru_cache
import json,sys
sys.dont_write_bytecode=True
import two_bit_source_native as s
t=s.t;P=Path(__file__).resolve().parent;D=t.D;nb=s.nb
sys.path.insert(0,str(D/'round46'))
import independent_current_bank as previous
g=previous.g;ns=g.ns
macros=t.load('a48_precise_macros',D/'round38/gcx_post_macros.py')

@lru_cache(None)
def namespace():
    plan=deepcopy(previous.namespace());lay=plan['layout'];start=lay['qubits']
    lay['SAM']=lay['SAM']+list(range(start,start+2688));lay['qubits']+=2688
    plan['two_bit_high_CODE_interval']=[start,start+2688]
    assert len(lay['SAM'])==5376 and plan['SC6_local_to_global']==previous.namespace()['SC6_local_to_global']
    return plan

def birth_blocks():
    lo,hi=namespace()['two_bit_high_CODE_interval']
    return previous.birth_blocks()+[{'role':'two_bit_high_CODE_RAW','start':lo,'stop':hi}]

def physical_wire(q,m=0):
    p=namespace();lo,hi=p['two_bit_high_CODE_interval']
    if q<lo:return previous.physical_wire(q,m)
    assert type(q) is int and type(m) is int and m>=0 and lo<=q<hi
    return m+q-3

def physical_tree(tree,m=0):
    if tree['op']=='seq':return nb.seq(*(physical_tree(x,m) for x in tree['children']))
    if tree['op']=='repeat':return nb.repeat(int(tree['count']),physical_tree(tree['child'],m))
    assert tree['op'] in ('G','CX')
    return nb.gate(tree['op'],*(physical_wire(q,m) for q in tree['wires']))

def stage_blocks(stage,depth=0):
    plan=namespace();kind=stage['kind']
    if kind=='SITE':yield from s.site_blocks(ns.site_layout(plan),depth)
    elif kind=='SOURCE':
        slot=plan['source_slots'][stage['slot']]
        if slot['kind']=='Choi':yield from s.choi_blocks(slot['bank'],ns.choi_layout(plan,slot),depth)
        else:yield from s.car_blocks(slot['bank'],ns.car_layout(plan,slot),depth)
    elif kind=='RAW_RESOURCE_FRAME':
        d=depth+stage['intrinsic_inverse_depth'];w=previous.resource_wires()
        for q in reversed(w) if d%2 else w:yield g.invert(nb.gate('G',q),d,plan)
    else:yield from g.stage_blocks(stage,plan,depth)

def profile_with_cuts():
    schedule=previous.stages();plan=namespace()
    for stage in schedule:
        yield from stage_blocks(stage)
        if stage=={'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':0}:
            yield {'op':'B82_CUT','name':previous.p43.CUTS[0]}
    lay=plan['layout'];yield nb.z_word(lay['port'],lay['port'],tuple(lay['spin']))
    for stage in reversed(schedule):
        yield from stage_blocks(stage,1)
        if stage=={'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':1}:
            yield {'op':'B82_CUT','name':previous.p43.CUTS[1]}

def compiler():
    plan=namespace();lay=plan['layout']
    return previous.a.c.Compiler(lay['port'],lay['spin'],plan['old_compiler_helper'],macros.Macros().ks['pi8'])

def compiled_core_with_cuts():
    yield from previous.compile_tagged(profile_with_cuts,compiler(),physical_tree)

def core_blocks():
    for tree in compiled_core_with_cuts():
        if tree['op']!='B82_CUT':yield tree

def source_prefix_blocks():
    """Actual G/CX SOURCE prefix through the first RAW resource frame."""
    def profile():
        for stage in previous.stages():
            yield from stage_blocks(stage)
            if stage=={'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':0}:return
        raise AssertionError('missing SOURCE boundary')
    for tree in compiler().stream(profile()):yield physical_tree(tree)

def upper_inventory_and_error():
    plan=json.loads((P/'TWO_BIT_SOURCE_COMPONENT_PLAN.json').read_text())
    source=s.counter(plan['all_SOURCE_forward_componentwise_upper'])
    report=json.loads((D/'round17/GLOBAL_REPORT_COMPILATION.json').read_text())
    rp=s.counter(report['native_forward_resources'])
    r=len(previous.resource_wires());assert r==34112
    # Forward A includes RAW B_R and its literal inverse. Source includes SITE.
    frames=Counter(G_other=r,G_port=r,CX=6*r,SourceI=4*r)
    A=source+s.times(rp,8)+s.raw_counts(8)+frames
    A.update(G_port=5889,CX=4096,SourceI=8196) # port inverse and exact SC6
    W=A+s.inv(A)+Counter(SourceI=2)
    k=compiler().k
    # For each closed CZ: 32 base-angle errors and >=5 SourceI; for
    # each remaining pair:16 errors and 2 SourceI. No count cancellation.
    units=8*W['SourceI'];replacement=F(units,1<<20000)
    new=Counter(G=W['G_port']+W['G_other']+k*units,CX=W['CX']+W['SourceI'])
    known=report['seven_report_all_known_approximate_macros'];assert known%7==0
    source_error=s.error_bounds()['all1440Choi_128CAR_SITE']
    # The checkpoint is BEFORE every REPORT. SIGMA is exact; B_R consists
    # only of positive G. This bound covers every SOURCE DATA column with
    # the declared private RAW inputs, not only its prepared output vector.
    prefix_profile=source+s.raw_counts(8)+Counter(G_other=r)
    source_prefix_error=source_error+F(8*prefix_profile['SourceI'],1<<20000)
    eta=source_error+F(8*(known//7),1<<4096)
    eB=2*eta+replacement
    assert replacement<F(1,1<<15800) and eB<F(1,1<<3421)
    assert source_prefix_error<F(1,1<<3423)
    return {'A_profile_upper':A,'W_profile_upper':W,'W_G_CX_upper':new,
      'replacement_error':replacement,'canonical_A_error_before_replacement':eta,
      'full_canonical_compressed_error':eB,'source_error':source_error,
      'full_SOURCE_DATA_fibre_prefix_error':source_prefix_error}

def main():
    p=namespace();lay=p['layout'];u=upper_inventory_and_error()
    births=birth_blocks();n=sum(z['stop']-z['start'] for z in births)
    assert n==11893774624
    out={'status':'BOUND_TWO_BIT_G_CX_SOURCE_CORE_WITH_RIGOROUS_ERROR',
      'CODE_bits':5376,'RAW_births':n,'additional_high_CODE_births':2688,
      'logical_birth_blocks':births,'CODE_low_logical_first':lay['SAM'][0],
      'CODE_high_logical_interval':p['two_bit_high_CODE_interval'],
      'CODE_pair_physical_formula':'coordinate j -> (2+j,11893771936+j), j=0..2687',
      'old_compiler_helper_logical':p['old_compiler_helper'],
      'old_compiler_helper_physical':physical_wire(p['old_compiler_helper']),
      'source_slots':len(p['source_slots']),'Choi_copies':1440,'CAR_copies':128,
      'REPORT_banks':8,'SC6_uses_original_seven_reports':True,
      'counts_componentwise_upper_not_actual':{k:s.local.stringify(v) for k,v in u.items() if k.endswith('profile_upper')},
      'W_G_CX_componentwise_upper':{k:hex(v) for k,v in u['W_G_CX_upper'].items()},
      'W_call_count_upper_bit_length':sum(u['W_G_CX_upper'].values()).bit_length(),
      'errors':{k:s.encode_error(v) for k,v in u.items() if isinstance(v,F)},
      'G_CX_replacement_error_lt':'2^-15800','full_canonical_compressed_error_lt':'2^-3421',
      'full_SOURCE_DATA_fibre_G_CX_prefix_error_lt':'2^-3423',
      'A47_required_eB_lt_2pow_minus3300_satisfied':True,
      'component_generators_and_global_binding_implemented':True,
      'new_G_CX_core_defined':True,'full_expanded_word_executed':False,
      'exact_numeric_full_inventory_evaluated':False,
      'full_new_mark_clock_postprocessing_family_compiled':False,
      'old_A46_price_Q_and_post_bounds_transferred':False,
      'physical_C_closed':False,'GR_closed':False}
    (P/'TWO_BIT_GLOBAL_SOURCE_PLAN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','RAW_births','W_call_count_upper_bit_length','full_canonical_compressed_error_lt')}))

if __name__=='__main__':main()
