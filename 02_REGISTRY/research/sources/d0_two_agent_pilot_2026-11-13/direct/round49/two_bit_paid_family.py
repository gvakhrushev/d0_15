#!/usr/bin/env python3
"""Four independent paid slots, one fixed actual post, and exact clocks.

The exact total lengths belong to NEW identity-padded words. Original
unpadded lengths are bounded, not reported as computed. The production
post is defined by the concrete finite actual-circuit evaluator and has
not been evaluated at production size. Physical Book admission stays open.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from collections import Counter
import json,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;D=P.parent
sys.path.insert(0,str(D/'round48'))
import two_bit_global_source as source
import actual_full_vector_source_jet as control
import finite_actual_target as target
import paid_padding as pad
native=pad.native;old=pad.old
CUTS=source.previous.p43.CUTS

@lru_cache(None)
def configuration():
    n=sum(x['stop']-x['start'] for x in source.birth_blocks())
    sam=tuple(source.physical_wire(q) for q in source.namespace()['layout']['SAM'])
    m=len(sam);assert m==5376 and n==11893774624
    _,q,_=target.a41.uniform_grid();k8=native.Macros().ks['pi8'];assert k8<=q
    stars=4*((1<<m)-1);L=1<<(m-1)
    post=Counter(G=stars*L*q,CX=4*(((1<<m)-1)*(m-1)*L+2*(m*L-(1<<m)+1)))
    core=source.upper_inventory_and_error()['W_G_CX_upper']
    probe=old.plane_upper(m,q,k8)
    coreL=sum(core.values())+4;postL=sum(post.values())+4;probeL=sum(probe.values())+4
    controlL=int(control.control_plan()['each_padded_control_calls_hex'],16)
    base=coreL+postL+probeL+4*controlL;Nbase=n+base;debt=m+(m+1)//2
    K=4*(Nbase.bit_length()+3208+1700+20+75+1+debt)
    assert Nbase.bit_length()==30833 and K==175604
    return {'n':n,'sam':sam,'m':m,'coreL':coreL,'postL':postL,'probeL':probeL,
      'controlL':controlL,'Lbase':base,'Nbase':Nbase,'K':K,'dimension_debt':debt,
      'core_upper':core,'post_upper':post,'probe_upper':probe,'q':q,'k8':k8,
      'post_error':F(stars*L,1<<20000)}

@lru_cache(None)
def actual_core_target():
    c=configuration()
    return target.ActualDiagonal(c['n'],c['sam'],source.core_blocks)

def actual_post_blocks():
    yield from target.post_blocks(actual_core_target())

def probe_power(sign,m):
    """Cayley target angle 2 atan(sign*t/2), with opposite exact signs."""
    assert sign in (-1,1) and m>=3
    def angle(bits):
        iv=target.e.Dyadic(bits);z=iv.rat(sign,1<<1701);z2=iv.mul(z,z)
        den=iv.add(iv.rat(1),z2)
        c=iv.div(iv.add(iv.rat(1),iv.neg(z2)),den)
        s=iv.div(iv.mul(iv.rat(2),z),den)
        for _ in range(m-1):
            nc=iv.sqrt(iv.div(iv.add(iv.rat(1),c),iv.rat(2)))
            s=iv.div(s,iv.mul(iv.rat(2),nc));c=nc
        return c,s
    return target.select_from_intervals(angle)

def actual_probe_blocks(plane,sign):
    assert sign in (-1,1);c=configuration()
    yield from old.plane_blocks(*plane,probe_power(sign,c['m']),c['sam'],native.Macros())

def slot_signs(arm,sign):
    assert arm in ('centre','matched','Pf','Qf','Qb','Pb','post_probe')
    assert sign in (-1,0,1) and ((arm=='centre')==(sign==0))
    if arm=='matched':return dict(zip(('Pf','Qf','Qb','Pb'),(sign,-sign,sign,-sign)))
    out={k:0 for k in ('Pf','Qf','Qb','Pb')}
    if arm in out:out[arm]=-sign if arm in ('Qf','Pb') else sign
    return out

def family_blocks(cfg,core_factory,post_factory,control_factory,probe_factory,
                  *,arm='centre',sign=0,axis=0,plane=None,keep_marks=False):
    """Chronology Pf; B; Qf^T; middle; Qb; return; Pb^T; fixed U; probe.

    Outgoing local Pb acts BEFORE fixed U. The generic post probe acts
    AFTER it and is explicitly a separate basis, not the same direction.
    """
    signs=slot_signs(arm,sign);sam=cfg['sam'];seen=[]
    def ctr(name):
        yield from pad.counted_pad(lambda:control_factory(axis,signs[name]),cfg['controlL'],sam)
    yield from ctr('Pf')
    for tree in pad.counted_pad(core_factory,cfg['coreL'],sam,tag_ops=('B82_CUT',)):
        if tree['op']!='B82_CUT':yield tree;continue
        assert tree['name'] in CUTS and tree['name'] not in seen;seen.append(tree['name'])
        if keep_marks:yield tree
        yield from ctr('Qf' if tree['name']==CUTS[0] else 'Qb')
    assert seen==list(CUTS)
    yield from ctr('Pb')
    yield from pad.counted_pad(post_factory,cfg['postL'],sam)
    active=(lambda:probe_factory(plane,sign)) if arm=='post_probe' else (lambda:iter(()))
    yield from pad.counted_pad(active,cfg['probeL'],sam)

def raw_control_factory(axis,sign):
    # A47 already paid padding consumes exactly its frozen control length.
    # family_blocks adds a NEW four-call reserve to each slot (see below).
    yield from control.control_blocks(axis,sign)

def production_configuration():
    c=dict(configuration())
    # counted_pad requires >=4 reserve even when the original A47 word
    # already has an exact length. Charge that reserve in every history.
    c['controlL']+=4;c['Lbase']+=16;c['Nbase']+=16
    assert c['Nbase'].bit_length()==30833 and c['K']==175604
    return c

def production_blocks(*,arm='centre',sign=0,axis=0,plane=None,keep_marks=False):
    c=production_configuration()
    yield from family_blocks(c,source.compiled_core_with_cuts,actual_post_blocks,
      raw_control_factory,actual_probe_blocks,arm=arm,sign=sign,axis=axis,plane=plane,keep_marks=keep_marks)

def execution_stages(cfg,block_factory):
    """Complete finite iterator; use small supplied fixtures to execute it."""
    for q in range(cfg['n']):
        yield {'kind':'canonical_RAW_birth','wire':q,'role':'early','carrier_qubits_after':q+1}
    for tree in block_factory():
        if tree['op']=='B82_CUT':yield {'kind':'source_mark','name':tree['name']};continue
        for gate in target.e.leaves(tree):yield {'kind':'square_unitary_edge','gate':gate}
    for j in range(cfg['K']):
        q=cfg['n']+j
        yield {'kind':'canonical_RAW_birth','wire':q,'role':'retention','carrier_qubits_after':q+1}
        yield {'kind':'final_unitary_g' if j==cfg['K']-1 else 'square_unitary_edge','gate':native.gate('G',q)}

def bounds(cfg):
    step=F(1,1<<1700);gs=F(1,1<<3208);z=F(1,1<<20);m=cfg['m']
    e=cfg['post_error'];assert e<F(1,1<<9247)
    mu=F((1<<(m-1))+40*m,1<<20000);delta=e+mu
    half=(m+1)//2
    post_l2=(1<<(half+1))*delta/gs+(1<<m)*delta*delta/(2*step*gs)
    post_dual=(1<<half)*post_l2
    assert post_dual<F(1,1<<661)
    gamma0=F(8,3)*z*gs
    heat=F(6*cfg['Nbase'],359)/(step*gamma0)*F(1,1<<(cfg['K']//4))
    assert F(5,6)**4<F(1,2)
    heat_dual=(1<<cfg['dimension_debt'])*heat
    assert heat_dual<F(1,1<<75)
    cerror=source.upper_inventory_and_error()['full_canonical_compressed_error']
    assert F(67,100)-cerror>F(2,3)
    return {'post_full_operator_error':e,'probe_full_operator_error':mu,
      'post_independent_skew_dual_finite_feedback_error':post_dual,
      'heat_one_price_contrast':heat,'heat_full_skew_dual':heat_dual,
      'normalization_gamma0_lower':gamma0,
      'actual_M_positive_lower':F(67,100)-cerror,
      'actual_M_vs_ideal_report_corner_error':cerror}

def encode(v):return {'numerator_hex':hex(v.numerator),'denominator_hex':hex(v.denominator)}

def main():
    c=production_configuration();b=bounds(c)
    out={'status':'CONSTRUCTIVE_TWO_BIT_FOUR_SLOT_PADDED_CLOCK_AND_FIXED_ACTUAL_POST',
      'RAW_early_births':c['n'],'CODE_bits':c['m'],'four_slot_order':['Pf','Qf_dagger','Qb','Pb_dagger'],
      'matched_physical_signs':[1,-1,1,-1],'fixed_post_after_fourth_control':True,
      'independent_post_probe_after_fixed_post_is_distinct_basis':True,
      'exact_new_padded_lengths_hex':{k:hex(c[k]) for k in ('coreL','postL','probeL','controlL','Lbase','Nbase')},
      'exact_lengths_are_for_emitted_padding_not_original_upper_counts':True,
      'late_retention_pairs':c['K'],'dimension_debt_bits':c['dimension_debt'],
      'clock_layers_N_hex':hex(c['Nbase']+2*c['K']),
      'clock_dimension':'2^n*(Lbase-2+3*2^K)-1','last_gate':'G on n+K-1',
      'actual_native_calls_hex':hex(c['Lbase']+c['K']),
      'post_target':'R_chi R_h, h proportional to chi+M_A48 chi/||M_A48 chi||; fixed at centre',
      'post_target_uses_actual_A48_G_CX_word':True,
      'production_scalar_path_sum_and_post_provider_implemented':True,
      'production_target_entries_or_word_evaluated':False,
      'production_execution_practical_claimed':False,
      'bounds':{k:encode(v) for k,v in b.items()},
      'post_operator_error_lt':'2^-9247','post_independent_skew_dual_error_lt':'2^-661',
      'heat_full_skew_dual_error_lt':'2^-75',
      'gain_scope':'candidate same Book reader and owned g*sigma; physical source identification remains separate',
      'original_Dnu_marks_or_vacuum_extension_identified':False,
      'whole_price_stationarity_proved':False,'physical_C_closed':False,'GR_closed':False}
    (P/'TWO_BIT_PAID_FAMILY_PLAN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'Nbase_bits':c['Nbase'].bit_length(),'K':c['K'],
      'post_error_lt':out['post_operator_error_lt'],'post_dual_error_lt':out['post_independent_skew_dual_error_lt']}))

if __name__=='__main__':main()
