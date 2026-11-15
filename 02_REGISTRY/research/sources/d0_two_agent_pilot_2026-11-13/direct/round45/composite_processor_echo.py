#!/usr/bin/env python3
"""A paid genuine composite REPORT prefix and approximate G/CX undo.

The full source remainder is retained. Existing f-Choi/q-CAR copies are
reused only after the echo; this is not an eighth independent source arena.
Production words are finite lazy specifications, not materialized runs.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import hashlib,json,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;D=P.parent
sys.path.insert(0,str(D/'round43'));import local_q_price as p43
sys.path.insert(0,str(D/'round44'));import joint_source_reduction as p44
a=p43.kernel.source;old=p43.old;B=p43.B
BARRIER='A45_COMPOSITE_REPORT_ECHO'


@lru_cache(None)
def address_binding():
    plan=a.g.namespace();slots=plan['source_slots']
    f=next(i for i,r in enumerate(plan['reports']) if r['bank']=='f')
    match=lambda bank:{(v['walk'],v['copy']):(i,v) for i,v in enumerate(slots) if v['bank']==bank and v['kind']=='CAR'}
    fc,qc=match('f'),match('q');assert set(fc)==set(qc) and len(fc)==16
    mapping={};pairs=[]
    for key in sorted(fc):
        fi,fs=fc[key];qi,qs=qc[key]
        left=fs['source']+fs['RIGHT'];right=qs['source']+qs['RIGHT']
        assert len(left)==len(right)==19 and len(fs['source'])==len(qs['source'])==12
        for x,y in zip(left,right):
            assert x!=y and x not in mapping and y not in mapping
            mapping[x]=y;mapping[y]=x
        pairs.append({'walk':key[0],'copy':key[1],'f_slot':fi,'q_slot':qi,'f_wires':left,'q_wires':right})
    l=plan['layout'];assert all(mapping.get(mapping[q],mapping[q])==q for q in mapping)
    protected=set(l['SAM']+l['SITE']+l['spin']+[l['port'],l['aux_arbitrary'],l['oldRIGHT_witness'],l['qubits']])
    assert not protected.intersection(mapping)
    assert not set(q for slot in slots for q in slot['private']).intersection(mapping)
    choi=[i for i,v in enumerate(slots) if v['bank']=='f' and v['kind']=='Choi']
    assert len(choi)==180 and not set(q for i in choi for q in slots[i]['source']).intersection(mapping)
    return f,mapping,pairs,choi


def observer_profile(depth=0):
    """Full old REPORT/literal old inverse, addressed to the genuine factors."""
    assert depth in (0,1)
    report,mapping,_,_=address_binding()
    for tree in a.g.stage_blocks({'kind':'REPORT','report':report},a.g.namespace(),depth):
        yield a.g.report.a.remap_native(tree,lambda q:mapping.get(q,q))


def observer_compiler():
    l=a.g.namespace()['layout']
    return a.c.Compiler(l['port'],tuple(l['spin']),l['qubits'],old.native.Macros().ks['pi8'])


def observer_blocks(depth=0,include_macro_marks=False):
    """Physical G/CX; only closed original macro boundaries can be marked."""
    compiler=observer_compiler();pending=0
    for index,tree in enumerate(observer_profile(depth)):
        translated,pending,_=compiler.transform(tree,pending)
        if translated['op']!='seq' or translated['children']:
            yield a.b.physical_tree(translated)
        if include_macro_marks:
            assert pending==0,'a physical prefix cannot cut an unfinished SourceI pair'
            yield {'op':'A45_MARK','kind':'closed_processor_macro','depth':depth,'macro_index':index}
    assert pending==0


def observer_pair(include_marks=False):
    yield from observer_blocks(0,include_marks)
    if include_marks:yield {'op':'A45_MARK','kind':'complete_genuine_REPORT_before_undo'}
    yield from observer_blocks(1,False)
    if include_marks:yield {'op':'A45_MARK','kind':'completed_approximate_echo_before_original_REPORTs'}


def profile_with_cuts():
    stages=a.stages()
    for stage in stages:
        yield from a.stage_blocks(stage,0)
        if stage=={'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':0}:
            yield {'op':'B82_CUT','name':p43.CUTS[0]}
        if stage=={'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':1}:
            yield {'op':BARRIER}
    l=a.g.namespace()['layout']
    yield a.c.nb.z_word(l['port'],l['port'],tuple(l['spin']))
    for stage in reversed(stages):
        yield from a.stage_blocks(stage,1)
        if stage=={'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':1}:
            yield {'op':'B82_CUT','name':p43.CUTS[1]}


def compile_tagged(factory,compiler,observer_factory,physical_map):
    """Keep the ORIGINAL transducer state; insert the separately compiled echo."""
    pending=0;seen=0
    for tree in factory():
        if tree['op'] in ('B82_CUT',BARRIER):
            assert pending==0,'a SourceI pair must not cross a marked insertion'
            if tree['op']==BARRIER:
                seen+=1;yield from observer_factory()
            else:yield tree
            continue
        compiled,pending,_=compiler.transform(tree,pending)
        if compiled['op']!='seq' or compiled['children']:yield physical_map(compiled)
    assert pending==0 and seen==1


def compiled_core_with_cuts(include_marks=False):
    yield from compile_tagged(profile_with_cuts,a.c.production_compiler(),
      lambda:observer_pair(include_marks),a.b.physical_tree)


def translated_counts(counts,cz,cz_si,k):
    assert (counts['SourceI']-cz_si)%2==0
    pairs=(counts['SourceI']-cz_si)//2;assert pairs>=0
    weight=16*pairs+32*cz
    out=Counter(G=counts['G_port']+counts['G_other']+k*weight,
                CX=counts['CX']-6*cz+2*pairs)
    return out,weight,pairs


def inventory():
    receipt=json.loads((D/'round17/GLOBAL_REPORT_COMPILATION.json').read_text())
    forward=Counter({k:int(v) for k,v in receipt['native_forward_resources'].items()})
    backward=a.g.inverse_counts(forward);cz=75196;k=old.native.Macros().ks['pi8']
    f,wf,_=translated_counts(forward,cz,5*cz,k)
    b,wb,_=translated_counts(backward,cz,15*cz,k)
    total,weight,pairs=translated_counts(forward+backward,2*cz,20*cz,k)
    assert total==f+b and weight==wf+wb
    error=F(weight,1<<20000)
    assert error<F(1,1<<15846) and sum(total.values()).bit_length()==24233
    # Old RAW inverse frame, compiled with its ORIGINAL A29 certificate.
    r=len(a.resource_wires());ki=a.c.production_compiler().k
    frame=Counter(G=r+32*ki*r,CX=10*r)
    pre_error=a.inventory()['eta_common_new']+F(4*r,1<<7432)
    assert pre_error<F(1,1<<3232)
    original_processor_error=F(int(receipt['seven_report_all_known_approximate_macros']),1<<4096)
    assert original_processor_error<F(1,1<<4058)
    mark_error=pre_error+F(wf,1<<20000)+original_processor_error
    assert mark_error<F(1,1<<3231)
    return {'forward':f,'backward':b,'total':total,'weight':weight,'pairs':pairs,
      'error':error,'forward_error':F(wf,1<<20000),'old_RAW_inverse_counts':frame,
      'computational_source_prefix_error':pre_error,
      'original_processor_error_upper':original_processor_error,'full_genuine_prefix_error':mark_error}


def production_configuration():
    cfg=p43.extend_configuration(old.production_configuration());inv=inventory()
    cfg['core_counts']=Counter(cfg['core_counts'])+inv['total']
    length=sum(inv['total'].values());cfg['Lbase']+=length;cfg['Nbase']+=length
    cfg['K']=4*(cfg['Nbase'].bit_length()+3158+1638+75+1+cfg['dimension_debt'])
    assert cfg['n']==10407050782 and cfg['Nbase'].bit_length()==25457 and cfg['K']==137444
    return cfg


def budgets():
    cfg=production_configuration();inv=inventory();eps=inv['error'];gs=F(1,1<<3158)
    extra=F(3,2)*eps/gs
    base=old.bounds(cfg);oldq=p43.budget(cfg)
    q=oldq['Qb_full_finite_price_minus_half_ideal_Pf_bound']+extra
    assert q<F(1,1<<75)
    qlower=oldq['concrete_j2_reduced_Pf_lower']/2-q;assert qlower>F(1,1<<45)
    incoming=base['incoming_full_H_plus_J_vs_reduced_each_row']+extra
    assert incoming<F(1,1<<75) and 55*incoming<F(1,1<<70)
    # Same old fixed A41 post. Normalize the new compressed state before
    # applying A42's unit-vector identity: ||xi_new-xi_old||<=2 eps/r_old
    # <3 eps, since r_old>2/3. The post itself is not recompiled.
    m=len(cfg['sam']);half=(m+1)//2;t=F(1,1<<1618)
    delta=F(1,1<<14623)+3*eps+base['outgoing_probe_full_op_error']
    assert delta<F(1,1<<14622)
    post=(1<<half)*((1<<(half+1))*delta/gs+(1<<m)*delta*delta/(2*t*gs))
    post+=base['outgoing_heat_full_finite_covector_dual']
    assert post<F(1,1<<75)
    allq=p44.bounds()['all_SAM_Qb_minus_half_Pf_dual_operator_norm_upper']+extra
    assert allq<F(1,1<<32)
    return {'new_analytic_row_vs_old_actual_row_error':extra,
      'new_Qb_finite_vs_half_old_reduced_Pf_error':q,'new_Qb_finite_positive_lower':qlower,
      'new_Pf_finite_vs_old_reduced_error':incoming,'new_outgoing_finite_dual_upper':post,
      'new_all_real_SAM_Q_analytic_reduction_error':allq}


def build():
    cfg=production_configuration();inv=inventory();values=budgets();report,mapping,pairs,choi=address_binding()
    original=json.loads((D/'round43/LOCAL_Q_PRICE_PLAN.json').read_text())
    mark=int(original['original_RAW_checkpoint_layer_hex'],16)+cfg['Q_slot_calls']
    mark+=sum(inv['old_RAW_inverse_counts'].values())+sum(inv['forward'].values())
    pins=[Path(__file__),D/'round25/h1_namespace.py',D/'round25/reversible_report_stream.py',
      D/'round25/global_h1.py',D/'round25/H1_NAMESPACE_PLAN.json',
      D/'round17/GLOBAL_REPORT_PLAN.json',D/'round17/GLOBAL_REPORT_COMPILATION.json',
      D/'round27/PREPARED_SOURCE_MOMENT_LAW_RU.md',D/'round29/gcx_compiler.py',
      D/'round30/marked_source_schedule.py',D/'round30/SOURCE_RAW_MARK_REGISTRY.json',
      D/'round38/POST_ANGLE_CERTIFICATE.json',D/'round42/fixed_post_paid_family.py',
      D/'round43/LOCAL_Q_PRICE_PLAN.json',D/'round44/JOINT_SOURCE_REDUCTION_PLAN.json',
      B/'round58/CZ_EXACT_OCCURRENCES.json',B/'round58/B58_A25_GCX_COVERAGE_AUDIT_RU.md',
      B/'round86/B86_ORIGINAL_MARK_ADMISSION_RU.md']
    encode_counts=lambda v:{k:hex(x) for k,x in v.items()}
    return {'status':'PAID_GENUINE_COMPOSITE_PROCESSOR_PREFIX_WITH_CONTROLLED_ECHO',
      'consumer':'B86 missing full processor prefix on actual f-Choi/q-CAR resources, retaining entire correlated remainder',
      'insertion':'forward after computational RAW inverse frame, before all seven original REPORTs, inside SAM-disjoint S',
      'new_births':0,'new_independent_eighth_bank':False,'new_physical_SWAP_executed':False,
      'report_private_owner':'f','source_Choi_slots':choi,'source_CAR_binding':pairs,
      'remapped_logical_wires':len(mapping),'compiled_echo_counts':encode_counts(inv['total']),
      'compiled_forward_counts':encode_counts(inv['forward']),'compiled_backward_counts':encode_counts(inv['backward']),
      'compiled_echo_length_bit_length':sum(inv['total'].values()).bit_length(),
      'echo_all_column_error_strict_lt':'2^-15846','echo_exact_identity_claimed':False,
      'old_SourceI_literal_target_echo_is_exact_identity':True,'physical_SourceI_or_old_Spin_added':False,
      'complete_genuine_processor_map_error_strict_lt':'2^-3231',
      'source_remainder_is_retained_in_full':True,'original_private_inputs_RAW_and_sigma_zero_before_observer':True,
      'original_RAW_checkpoint_layer_hex':original['original_RAW_checkpoint_layer_hex'],
      'new_completed_genuine_REPORT_clock_layer_hex':hex(mark),
      'early_births':cfg['n'],'late_retention_pairs':cfg['K'],
      'Lbase_hex':hex(cfg['Lbase']),'Nbase_hex':hex(cfg['Nbase']),'Nbase_bit_length':cfg['Nbase'].bit_length(),
      'clock_dimension':'2^n*(Lbase-2+3*2^K)-1','last_actual_g':old.gate('G',cfg['n']+cfg['K']-1),
      'fixed_A41_post_recompiled_or_moved':False,
      'actual_gain':'4 z p^K c_ref gs/(1-z+z p^K c0new^2), recomputed at the NEW actual corner',
      'new_incoming_finite_each_row_error_strict_lt':'2^-75',
      'new_outgoing_all_plane_finite_dual_strict_lt':'2^-75',
      'new_Qb_j2_full_finite_normalized_price_strict_gt':'2^-45',
      'new_Qf_j2_full_finite_normalized_price_strict_lt':'-2^-45',
      'new_all_real_SAM_analytic_Q_reduction_error_strict_lt':'2^-32',
      'exact_same_family_Q_price_swap_preserved':True,
      'original_seven_REPORT_inputs_restored_exactly':False,
      'prefixes_inside_incomplete_SourceI_or_CZ_transported':False,
      'genuine_bank_untouched_through_later_REPORTs':False,
      'full_stronger_independent_unsplit_H1_FN_admission_proved':False,
      'production_post_or_all_native_stages_executed':False,
      'errors':{k:old.encode(inv[k]) for k in ('error','forward_error','computational_source_prefix_error','original_processor_error_upper','full_genuine_prefix_error')},
      'bounds':{k:old.encode(v) for k,v in values.items()},
      'physical_C_closed':False,'GR_closed':False,
      'source_sha256':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in pins}}


if __name__=='__main__':
    out=build();(P/'COMPOSITE_PROCESSOR_ECHO_PLAN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','compiled_echo_length_bit_length','Nbase_bit_length','late_retention_pairs')}))
