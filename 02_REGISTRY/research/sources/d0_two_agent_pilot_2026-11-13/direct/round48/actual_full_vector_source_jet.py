#!/usr/bin/env python3
"""Consume A47's control theorem with the actual A48 SOURCE provider.

Finite comparison words are defined; no derivative of an integer word index
is taken. The source is the declared typed extension, not a proof that all
original physical marked prefixes or their prices have been identified.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from functools import lru_cache
from hashlib import sha256
import json,sys
sys.dont_write_bytecode=True
import two_bit_global_source as g
P=Path(__file__).resolve().parent;D=g.D
sys.path.insert(0,str(D/'round47'))
import full_vector_controls as a47

@lru_cache(None)
def control_plan():return json.loads((D/'round47/FULL_VECTOR_CONTROL_PLAN.json').read_text())
def decode(x):return F(int(x['numerator_hex'],16),int(x['denominator_hex'],16))

def control_blocks(index,sign):
    assert type(index) is int and 0<=index<2688 and sign in (-1,0,1)
    p=control_plan();lib=p['positive_G_power_library'];mac=a47.native.Macros()
    pair=(g.physical_wire(g.namespace()['layout']['SAM'][index]),
          g.physical_wire(g.namespace()['layout']['SAM'][2688+index]))
    length=int(p['each_padded_control_calls_hex'],16);used=0
    if sign:
        pairs=list(combinations(range(4),2))
        for ij in pairs+list(reversed(pairs)):
            k=int(lib['%d_%d'%ij][str(sign)]['k_hex'],16)
            yield from a47.plane_blocks(ij,k,pair,mac)
        used=sum(int(v,16) for v in p['raw_control_counts'][str(sign)].values())
    third=g.physical_wire(g.namespace()['layout']['SAM'][(index+1)%2688])
    yield from a47.old.padding(length-used,(*pair,third))

def comparison_prefix_blocks(index,sign):
    """Chronology P_sign; Bhat; P_minus_sign. Both controls are paid."""
    assert sign in (-1,0,1)
    yield from control_blocks(index,sign)
    yield from g.source_prefix_blocks()
    yield from control_blocks(index,-sign)

def main():
    p=control_plan();sigma=F(1,1<<80);step=F(1,1<<1700)
    eB=g.upper_inventory_and_error()['full_SOURCE_DATA_fibre_prefix_error']
    epsP=decode(p['control_vs_exp_tX_error']);d=a47.source_derivative_enclosure()
    extra=(eB+2*epsP)/(sigma*step)+F(4,3)*104*d['full_bank_M1']*step**2
    total=d['two_bit_ideal_axis_jet_error']+extra
    assert eB<F(1,1<<3423) and extra<F(1,1<<1642) and total<F(1,1<<44)
    # Check every CODE pairing agrees with the already certified A47 words.
    for j in range(2688):
        assert (2+j,11893771936+j)==tuple(g.physical_wire(g.namespace()['layout']['SAM'][q]) for q in (j,2688+j))
    counts={}
    for sign in (-1,0,1):
        c=a47.count_blocks(lambda sign=sign:control_blocks(0,sign))
        assert sum(c.values())==int(p['each_padded_control_calls_hex'],16)
        counts[str(sign)]={k:hex(v) for k,v in c.items()}
    out={'status':'ACTUAL_TWO_BIT_SOURCE_FINITE_FULL_VECTOR_JET_BOUND',
      'source_error':g.s.encode_error(eB),'actual_control_finite_difference_extra':g.s.encode_error(extra),
      'actual_control_finite_difference_extra_lt':'2^-1642',
      'full_axis_jet_error':g.s.encode_error(total),'full_axis_jet_error_lt':'2^-44',
      'comparison':'(Fhat_plus-Fhat_minus)/(2*sigma*t), each Fhat uses its independently compiled before/after controls',
      'sigma':'2^-80','t':'2^-1700','scope':'all SOURCE DATA columns on declared private RAW fibre and arbitrary reference entanglement; selected A23 full vacuum extension',
      'control_native_counts':counts,'all_four_comparison_controls_paid':True,
      'SourceI_calls':0,'no_exact_inverse_assumption_for_actual_controls':True,
      'new_SOURCE_precision_premise_of_A47_discharged':True,
      'physical_full_cost_gradient_identified':False,'original_all_Dnu_marked_maps_identified':False,
      'complete_corner_post_clock_price_family_constructed':False,
      'giant_word_executed':False,'physical_C_closed':False,'GR_closed':False,
      'source_sha256':{str(q):sha256(q.read_bytes()).hexdigest() for q in [Path(__file__),P/'two_bit_global_source.py',P/'TWO_BIT_GLOBAL_SOURCE_PLAN.json',D/'round47/full_vector_controls.py',D/'round47/FULL_VECTOR_CONTROL_PLAN.json',D/'round47/FULL_VECTOR_CONTROL_CHECK.json']}}
    (P/'ACTUAL_FULL_VECTOR_SOURCE_JET.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','actual_control_finite_difference_extra_lt','full_axis_jet_error_lt')}))

if __name__=='__main__':main()
