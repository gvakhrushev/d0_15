#!/usr/bin/env python3
"""Independent eighth current source and REPORT; seven-input comparator.

Finite lazy specification, not a materialized production run. The fresh
REPORT is cancelled only in the ideal logical comparator argument; every
native preparation, REPORT, literal inverse, birth and clock edge is paid.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from copy import deepcopy
import hashlib,json,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;D=P.parent
sys.path.insert(0,str(D/'round45'));import composite_processor_echo as prev
a=prev.a;g=a.g;old=prev.old;p43=prev.p43;B=prev.B


@lru_cache(None)
def namespace():
    """Append AFTER the old compiler helper; do not move that helper."""
    base=g.namespace();plan=deepcopy(base);l=plan['layout']
    helper=base['layout']['qubits'];start=helper+1
    template=next(r for r in base['reports'] if r['bank']=='f')
    r=deepcopy(template);shift=start-template['private_start']
    r['bank']='current_f_choi_q_car';r['private_start']=start
    for key in ('sigma','all_READY','REPORT','source_private_start'):r[key]+=shift
    r['source_slots']=[]
    for si in template['source_slots']:
        src=deepcopy(base['source_slots'][si])
        for key in ('source','private','address','choi_input','choi_output','RIGHT','internal_SITE','grade'):
            if key in src:src[key]=[q+shift for q in src[key]]
        src['bank']='f' if src['kind']=='Choi' else 'q'
        src['arena']='independent_current'
        r['source_slots'].append(len(plan['source_slots']));plan['source_slots'].append(src)
    plan['reports'].append(r)
    l['qubits']=r['source_private_start']+r['source_private_width']
    plan['old_compiler_helper']=helper
    plan['fresh_logical_interval']=[start,l['qubits']]
    # SC6 stays byte-for-byte the original seven-report mapping.
    assert plan['SC6_local_to_global']==base['SC6_local_to_global']
    return plan


def physical_wire(q,initial_raw_bits=0):
    plan=namespace();helper=plan['old_compiler_helper'];m=initial_raw_bits
    assert type(q) is int and type(m) is int and m>=0
    assert 0<=q<plan['layout']['qubits'] and q not in (0,1,3)
    if q<=helper:return a.b.physical_wire(q,m)
    return m+q-3


def physical_tree(tree,initial_raw_bits=0):
    op=tree['op']
    if op=='seq':return a.c.nb.seq(*(physical_tree(z,initial_raw_bits) for z in tree['children']))
    if op=='repeat':return a.c.nb.repeat(int(tree['count']),physical_tree(tree['child'],initial_raw_bits))
    assert op in ('G','CX')
    return a.c.nb.gate(op,*(physical_wire(q,initial_raw_bits) for q in tree['wires']))


def birth_blocks():
    p=namespace();r=p['reports'][7]
    return a.b.birth_blocks()+[
      {'role':'independent_current_REPORT_and_source_DATA_RAW','start':r['private_start'],'stop':r['source_private_start']},
      {'role':'independent_current_source_private_RAW','start':r['source_private_start'],'stop':p['layout']['qubits']}]


@lru_cache(None)
def resource_wires():
    p=namespace();fresh=[]
    for si in p['reports'][7]['source_slots']:
        slot=p['source_slots'][si];fresh.extend(slot['source'])
        if slot['kind']=='CAR':fresh.extend(slot['RIGHT'])
    assert len(fresh)==len(set(fresh))==4264
    out=a.resource_wires()+tuple(fresh)
    assert len(out)==len(set(out))==34112
    return out


def stages():
    p=namespace();out=[{'kind':'SITE'}]
    for ri,r in enumerate(p['reports']):
        out.append({'kind':'SIGMA','report':ri})
        out.extend({'kind':'SOURCE','slot':si} for si in r['source_slots'])
    out.extend([{'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':0},
                {'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':1}])
    out.extend({'kind':'REPORT','report':ri} for ri in range(8))
    out.extend([{'kind':'PORT_ZERO'},{'kind':'SC6'}])
    return out


def stage_blocks(stage,depth=0):
    assert type(depth) is int and depth>=0
    p=namespace()
    if stage['kind']!='RAW_RESOURCE_FRAME':
        yield from g.stage_blocks(stage,p,depth);return
    actual=depth+stage['intrinsic_inverse_depth'];wires=resource_wires()
    for q in reversed(wires) if actual%2 else wires:
        yield g.invert(a.c.nb.gate('G',q),actual,p)


def profile_with_cuts(include_marks=False):
    p=namespace();schedule=stages()
    for stage in schedule:
        yield from stage_blocks(stage,0)
        if stage=={'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':0}:
            yield {'op':'B82_CUT','name':p43.CUTS[0]}
        if include_marks and stage.get('kind')=='REPORT':
            yield {'op':'A46_MARK','kind':'complete_REPORT','report':stage['report'],'depth':0}
    l=p['layout'];yield a.c.nb.z_word(l['port'],l['port'],tuple(l['spin']))
    for stage in reversed(schedule):
        yield from stage_blocks(stage,1)
        if stage=={'kind':'RAW_RESOURCE_FRAME','intrinsic_inverse_depth':1}:
            yield {'op':'B82_CUT','name':p43.CUTS[1]}


def compile_tagged(factory,compiler,map_tree):
    pending=0
    for tree in factory():
        if tree['op'] in ('B82_CUT','A46_MARK'):
            assert pending==0,'a mark cannot split an unfinished SourceI pair'
            yield tree;continue
        out,pending,_=compiler.transform(tree,pending)
        if out['op']!='seq' or out['children']:yield map_tree(out)
    assert pending==0


def compiled_core_with_cuts(include_marks=False):
    # production_compiler owns the OLD helper address, not new layout.qubits.
    yield from compile_tagged(lambda:profile_with_cuts(include_marks),a.c.production_compiler(),physical_tree)


def core_blocks():
    for tree in compiled_core_with_cuts():
        if tree['op']!='B82_CUT':yield tree


@lru_cache(None)
def inventory():
    base=a.inventory();receipt=json.loads((D/'round17/GLOBAL_REPORT_COMPILATION.json').read_text())
    report=Counter({k:int(v) for k,v in receipt['native_forward_resources'].items()})
    source=g.times(g.choi.inventory('f')['RAW_prepared_forward'],180)+g.times(g.car.inventory('q')['source_forward'],16)
    sigma=Counter(G_port=1,CX=6,SourceI=4)
    forward=source+sigma+report
    frames=Counter(G_port=3*4264,G_other=4264,CX=18*4264,SourceI=24*4264)
    W=base['W_old_profile']+forward+g.inverse_counts(forward)+frames
    cz=1052744+2*75196;cz_si=10527440+20*75196
    new,rot=a.translate_counts(W,cz,cz_si)
    checkpoint=base['checkpoint_old_profile']+source+sigma+Counter(G_other=4264)
    pc,pr=a.translate_counts(checkpoint,0,0)
    fresh_error=180*g.choi.errors()[2]+16*g.car.error_bound('q')
    # A17 uniform closed-macro count divides into seven identical REPORTs.
    known=int(receipt['seven_report_all_known_approximate_macros']);assert known%7==0
    er=F(known//7,1<<4096)
    _,eta=g.canonical_input_error()
    eta0=base['eta_common_old']+fresh_error
    ep=eta0+F(pr,1<<7432);eW=F(rot,1<<7432)
    eB=2*(eta+fresh_error+er)+eW
    assert ep<F(1,1<<3232) and eW<F(1,1<<3244) and eB<F(1,1<<3231)
    assert F(67,100)-eB>F(2,3)
    return {'fresh_SOURCE':source,'fresh_SIGMA':sigma,'fresh_REPORT':report,
      'added_A':forward,'added_four_RAW_frames':frames,'W_old_profile':W,'W_new':new,
      'W_CZ':cz,'W_CZ_SourceI':cz_si,'W_rotations':rot,
      'checkpoint_old_profile':checkpoint,'checkpoint_new':pc,'checkpoint_rotations':pr,
      'eta_common_old':eta0,'eta_common_new':ep,'fresh_source_error':fresh_error,
      'one_REPORT_macro_error':er,'replacement_error':eW,'full_compressed_error':eB}


def production_configuration():
    oldcfg=old.production_configuration();_,q,_=old.a41.uniform_grid()
    n=sum(z['stop']-z['start'] for z in birth_blocks())
    cfg=old.align(n,oldcfg['sam'],inventory()['W_new'],oldcfg['post_counts'],oldcfg['powers'],q,old.native.Macros().ks['pi8'])
    cfg['post_counts_are_production_upper_bound']=True
    cfg['post_target_core']='A46 actual M, recomputed by the finite A41 recipe; not the A30 target'
    cfg=p43.extend_configuration(cfg)
    assert cfg['n']==11893771936 and cfg['Nbase'].bit_length()==25457 and cfg['K']==137444
    return cfg


def bounds():
    cfg=production_configuration();base=old.bounds(cfg);s=F(1,1<<30);gs=F(1,1<<3158)
    eB,eW,eU,ep=(F(1,1<<k) for k in (3231,3244,14623,3232))
    # Recompute the inserted-source kernel bound, not just endpoint M.
    assert 540*F(3,32)**2<F(35,16)**2
    lam=F(9,4)*s;assert F(35,16)*s+2*ep<lam
    qb=p43.budget(cfg)
    assert qb['old_prefix_j2_distance_bound']==lam
    ideal2=(540*256*F(3,16)**2+360*256*F(81,16)**2+32*F(11,10)**2)*s*s
    assert ideal2<(1539*s)**2
    delta=1540*s;assert 1539*s+2*ep<delta
    tau=104*F(1,1<<3083)+(1<<25)*2704*s+eB/gs;assert tau<85
    allq=F(3,4)*(tau*(2*delta*delta+2*eW)+eW/gs)+eU/gs
    assert allq<F(1,1<<31)
    assert base['incoming_full_H_plus_J_vs_reduced_each_row']<F(1,1<<75)
    return {'fresh_j2_prefix_distance':lam,'global_ideal_source_distance_squared':ideal2,
      'global_old_profile_source_distance':delta,'centred_actual_M_spread_over_gs':tau,
      'all_real_SAM_Q_analytic_reduction_error':allq,
      'Qb_finite_vs_half_reduced_Pf_error':qb['Qb_full_finite_price_minus_half_ideal_Pf_bound'],
      'Qb_finite_positive_lower':qb['Qb_positive_full_finite_price_lower'],
      'incoming_finite_vs_reduced_each_row':base['incoming_full_H_plus_J_vs_reduced_each_row'],
      'outgoing_finite_dual':base['outgoing_full_H_plus_J_finite_covector_dual']}


def build():
    p=namespace();inv=inventory();cfg=production_configuration();bd=bounds();fresh=p['reports'][7]
    pins=[Path(__file__),D/'round25/h1_namespace.py',D/'round25/global_h1.py',
      D/'round25/H1_NAMESPACE_PLAN.json',D/'round25/GLOBAL_H1_PLAN.json',
      D/'round17/GLOBAL_REPORT_COMPILATION.json',D/'round29/gcx_compiler.py',
      D/'round29/gcx_birth_clock.py',D/'round30/marked_source_schedule.py',
      D/'round41/exact_target.py',D/'round41/sam_only_compiler.py',D/'round41/SAM_ONLY_COMPILER_PLAN.json',
      D/'round42/fixed_post_paid_family.py',D/'round43/local_q_price.py',
      D/'round44/joint_source_reduction.py',D/'round45/composite_processor_echo.py',
      B/'round57/GADGET_G_POWER_CERTIFICATE.json',B/'round58/CZ_EXACT_OCCURRENCES.json',
      old.a41.CERT,B/'round84/B84_UNIFORM_SOURCE_BOUND.json']
    return {'status':'INDEPENDENT_CURRENT_BANK_PAID_FINITE_CONSTRUCTION',
      'fresh_report':fresh,'fresh_source_slots':[p['source_slots'][i] for i in fresh['source_slots']],
      'fresh_logical_interval':p['fresh_logical_interval'],'old_compiler_helper_logical':p['old_compiler_helper'],
      'old_compiler_helper_physical':physical_wire(p['old_compiler_helper']),
      'old_aux_physical':physical_wire(2),'early_RAW_births':cfg['n'],'new_RAW_births':1486721154,
      'birth_blocks':birth_blocks(),'source_DATA_RIGHT_frame_wires':len(resource_wires()),
      'SC6_local_to_global_unchanged':p['SC6_local_to_global'],'SC6_reports':7,'prepared_REPORT_arenas':8,
      'A_stages':stages(),'native_counts':{k:hex(v) for k,v in inv['W_new'].items()},
      'core_call_bit_length':sum(inv['W_new'].values()).bit_length(),
      'Nbase_hex':hex(cfg['Nbase']),'Lbase_hex':hex(cfg['Lbase']),'Nbase_bit_length':cfg['Nbase'].bit_length(),
      'late_retention_pairs':cfg['K'],'clock_dimension':'2^n*(Lbase-2+3*2^K)-1',
      'post_target':cfg['post_target_core'],'post_fixed_across_new_family':True,
      'post_counts_are_target_independent_upper_bounds':True,
      'actual_gain':'4 z p^K c_ref gs / (1-z+z p^K c0_new^2)',
      'original_ideal_seven_report_scalar_target_unchanged':True,
      'fresh_REPORT_exact_native_commutation_claimed':False,
      'fresh_SOURCE_all_dirty_column_commutation_claimed':False,
      'full_coherent_remainder_retained':True,'fresh_source_retained_through_seven_original_REPORTs':True,
      'canonical_source_prefix_error':g.encode_error(inv['eta_common_new']),
      'canonical_compressed_error':g.encode_error(inv['full_compressed_error']),
      'all_column_replacement_error':g.encode_error(inv['replacement_error']),
      'bounds':{k:old.encode(v) for k,v in bd.items()},
      'giant_word_executed':False,'production_post_provider_implemented':False,
      'all_original_Dnu_marks_and_first_jets_bound':False,'full_original_FN_admission_proved':False,
      'original_Cost_Info_binding_proved':False,'physical_C_closed':False,'GR_closed':False,
      'source_sha256':{str(q):hashlib.sha256(q.read_bytes()).hexdigest() for q in pins}}


if __name__=='__main__':
    result=build();(P/'INDEPENDENT_CURRENT_BANK_PLAN.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','early_RAW_births','Nbase_bit_length','late_retention_pairs')}))
