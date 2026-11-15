#!/usr/bin/env python3
"""Fixed A41 post; independent incoming SAM and outgoing plane comparisons.

Production is a mathematically specified finite family, not a materialized
Python word. Small explicit words exercise the actual paid-stage assembler.
Last g is the last retention G: the clock coefficient is 3, not A39's 4.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib,json,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;D=P.parent
sys.path.insert(0,str(D/'round41'));import sam_only_compiler as a41
sys.path.insert(0,str(D/'round38'));import gcx_post_macros as native
sys.path.insert(0,str(D/'round32'));import finite_book_comparison as incoming
gate,repeat,seq=native.gate,native.repeat,native.seq


def padding(length,sam):
    assert type(length) is int and (length==0 or length>=4)
    assert len(sam)>=3
    a,b,c=sam[:3];A=gate('CX',a,b);B=gate('CX',b,c);C=gate('CX',a,c)
    twos,fives=incoming.identity_counts(length)
    if twos:yield repeat(twos,seq(A,A))
    if fives:yield seq(A,B,A,B,C)


def plane_affine(a,b,sam):
    m=len(sam);assert 0<=a<b<(1<<m)
    delta=a^b;pivot=(delta&-delta).bit_length()-1
    ops=[('X',sam[j]) for j in range(m) if (a>>j)&1]
    ops += [('CX',sam[pivot],sam[j]) for j in range(m) if j!=pivot and (delta>>j)&1]
    return pivot,ops


def plane_blocks(a,b,k,sam,macros):
    """SAM-only approximation to any plane, all helper wires also SAM.

    k approximates the required angle divided by L, as in A41/B80. Each X
    occurrence is independently lowered to the owned all-column X macro;
    reverse target order does not mean adjointing the new approximate word.
    """
    sam=tuple(sam);assert len(sam)>=3 and len(set(sam))==len(sam)
    pivot,ops=plane_affine(a,b,sam)
    def lower(op):
        if op[0]=='CX':return gate(*op)
        q=op[1];helper=next(x for x in sam if x!=q)
        return macros.x(q,helper)
    for op in ops:yield lower(op)
    yield from a41.star_blocks(sam,1<<pivot,k)
    for op in reversed(ops):yield lower(op)


def plane_counts(m,a,b,k,k8):
    assert 0<=a<b<(1<<m) and k>=1
    ones=bin(a).count('1');diff=bin(a^b).count('1');L=1<<(m-1)
    return Counter(G=L*k+40*ones*k8,CX=(m-1)*L+2*(diff-1)+4*ones)


def plane_upper(m,q,k8):
    L=1<<(m-1)
    return Counter(G=L*q+40*m*k8,CX=(m-1)*L+2*(m-1)+4*m)


def align(total,sam,core_counts,post_counts,powers,probe_q,k8):
    """Common lengths for one fixed post and independent pre/probe slots."""
    assert len(sam)>=3 and min(powers)>=1
    preL=max(powers)+4;postL=sum(post_counts.values())+4
    probe=plane_upper(len(sam),probe_q,k8);probeL=sum(probe.values())+4
    Lbase=preL+sum(core_counts.values())+postL+probeL;Nbase=total+Lbase
    debt=len(sam)+(len(sam)+1)//2
    K=4*(Nbase.bit_length()+3158+1638+75+1+debt)
    return {'n':total,'sam':tuple(sam),'core_counts':core_counts,'post_counts':post_counts,
            'powers':powers,'preL':preL,'postL':postL,'probeL':probeL,'probe_upper':probe,
            'Lbase':Lbase,'Nbase':Nbase,'dimension_debt':debt,'K':K}


def execution_stages(cfg,core_factory,post_factory,macros,*,incoming_sign='centre',
                     incoming_index=0,outgoing_plane=None,outgoing_power=None):
    """Small executable assembler; caller supplies literal finite words.

    Production post_factory is not implemented in A41. In the production
    theorem it denotes the uniquely prescribed A41 centre word, kept FIXED
    in every comparison, with padding to the proved upper length.
    """
    if cfg.get('post_counts_are_production_upper_bound'):
        raise NotImplementedError('Production actual post length/provider is mathematical, not implemented; this assembler requires exact small word counts')
    sam=cfg['sam'];n=cfg['n'];K=cfg['K'];assert K>=1
    assert incoming_sign in ('centre','plus','minus') and 0<=incoming_index<len(sam)
    power=0 if incoming_sign=='centre' else cfg['powers'][0 if incoming_sign=='plus' else 1]
    for q in range(n):yield {'kind':'canonical_RAW_birth','wire':q,'role':'original','carrier_qubits_after':q+1}
    def blocks():
        if power:yield repeat(power,gate('G',sam[incoming_index]))
        yield from padding(cfg['preL']-power,sam)
        yield from core_factory()
        yield from post_factory()
        yield from padding(cfg['postL']-sum(cfg['post_counts'].values()),sam)
        probe_count=0
        if outgoing_plane is not None:
            assert incoming_sign=='centre' and outgoing_power is not None
            a,b=outgoing_plane
            yield from plane_blocks(a,b,outgoing_power,sam,macros)
            probe_count=sum(plane_counts(len(sam),a,b,outgoing_power,macros.ks['pi8']).values())
        yield from padding(cfg['probeL']-probe_count,sam)
    for tree in blocks():
        for g in a41.e.leaves(tree):yield {'kind':'square_unitary_edge','gate':g}
    for j in range(K):
        q=n+j
        yield {'kind':'canonical_RAW_birth','wire':q,'role':'late_retention','carrier_qubits_after':q+1}
        yield {'kind':'final_unitary_g' if j==K-1 else 'square_unitary_edge','gate':gate('G',q)}


def production_configuration():
    plan=json.loads((D/'round41/SAM_ONLY_COMPILER_PLAN.json').read_text())
    core=json.loads((D/'round30/COMMON_SOURCE_MARKED_PLAN.json').read_text())
    _,q,_=a41.uniform_grid();macros=native.Macros();k8=macros.ks['pi8'];assert k8<=q
    n=core['total_RAW_births'];sam=tuple(range(2,2690))
    cc=Counter({k:int(v) for k,v in core['new_native_counts'].items()})
    # Upper post counts determine a single exact padding target. The actual
    # number of post G calls is defined by the A41 finite selector recipe,
    # not evaluated here. The actual padding is upper_length-actual_length+4.
    upper=Counter(G=int(plan['upper_G_calls_hex'],16),CX=int(plan['exact_CX_calls_hex'],16))
    cfg=align(n,sam,cc,upper,incoming.powers(),q,k8)
    cfg['post_counts_are_production_upper_bound']=True
    return cfg


def encode(v):
    v=F(v);return {'numerator_hex':hex(v.numerator),'denominator_hex':hex(v.denominator)}


def bounds(cfg):
    m=len(cfg['sam']);half=(m+1)//2;z,t,gs=F(1,1<<20),F(1,1<<1618),F(1,1<<3158)
    e=F(1,1<<14623);angle=F(1,1<<4852)
    # With fixed native post and its own centre denominator, the derivative
    # error is linear in e/gs, not e/(t gs) and not a co-moving-section claim.
    fixed_post=e/gs
    bracket=8/(1-z)+24*z/(1-z)**2+16*z*z/(1-z)**3
    taylor=t*t*bracket/(16*gs);angular=angle/(t*gs)
    gamma_lower=F(8,3)*z*gs
    heat=F(6*cfg['Nbase'],359)/(t*gamma_lower)*F(1,1<<(cfg['K']//4))
    assert F(5,6)**4<F(1,2)
    assert heat<F(1,1<<(cfg['dimension_debt']+76))
    pre=fixed_post+taylor+angular+heat;corrected=55*pre
    assert pre<F(1,1<<75) and corrected<F(1,1<<70)
    L=1<<(m-1);mu=F(L+40*m,1<<20000);delta=e+mu
    assert mu<F(1,1<<17312) and delta<F(1,1<<14622)
    post_l2=(1<<(half+1))*delta/gs+(1<<m)*delta*delta/(2*t*gs)
    post_dual=(1<<half)*post_l2
    heat_dual=(1<<cfg['dimension_debt'])*heat
    assert post_dual<F(1,1<<8775) and heat_dual<F(1,1<<76)
    assert post_dual+heat_dual<F(1,1<<75)
    return {'fixed_native_post_incoming_derivative_error':fixed_post,
      'incoming_finite_Taylor':taylor,'incoming_B63_angle_error':angular,
      'heat_each_row':heat,'incoming_full_H_plus_J_vs_reduced_each_row':pre,
      'incoming_corrected_2688_covector_error':corrected,
      'outgoing_probe_full_op_error':mu,'outgoing_state_combined_error':delta,
      'outgoing_feedback_full_finite_covector_dual':post_dual,
      'outgoing_heat_full_finite_covector_dual':heat_dual,
      'outgoing_full_H_plus_J_finite_covector_dual':post_dual+heat_dual,
      'incoming_covector_norm_lower':F(1,1<<46)-corrected,
      'incoming_covector_norm_upper':F(1,1<<16)+corrected,
      'incoming_covector_vs_actual_mean_geometry':F(1,1<<15)+corrected}


def build():
    cfg=production_configuration();b=bounds(cfg);n=cfg['n'];K=cfg['K'];m=len(cfg['sam'])
    assert n==10407050782 and cfg['Nbase'].bit_length()==25457 and K==137444
    core=json.loads((D/'round30/COMMON_SOURCE_MARKED_PLAN.json').read_text())
    mark=n+cfg['preL']+int(core['joint_RAW_source_checkpoint_native_prefix_calls'])
    assert mark<cfg['Nbase']
    pins=[Path(__file__),D/'round41/exact_target.py',D/'round41/sam_only_compiler.py',
      D/'round41/SAM_ONLY_COMPILER_PLAN.json',D/'round41/RESULT.json',
      D/'round38/gcx_post_macros.py',D/'round38/POST_ANGLE_CERTIFICATE.json',
      D/'round37/POST_SAM_REDUCTION_PLAN.json',D/'round31/MEAN_GEOMETRY_LIFT_PLAN.json',
      D/'round30/marked_source_schedule.py',D/'round30/COMMON_SOURCE_MARKED_PLAN.json',
      D/'round32/finite_book_comparison.py',incoming.core.g.B/'round63/SUFFICIENT_ENDPOINT_G_CERTIFICATE.json',
      D.parents[1]/'d0_retained_response_concentration_2026-10-28/RAW_CYLINDER_REALIZATION_RU.md',
      D.parents[1]/'d0_retained_response_concentration_2026-10-28/GROWING_CLOCK_RU.md']
    return {'status':'MATHEMATICAL_FULL_PAID_FAMILY_WITH_FIXED_POST_AND_INDEPENDENT_PRE_POST_ROWS',
      'phase':'native realization; full Book price and independent external preparation sources',
      'initial_history':{'H0':'C','Omega0':1,'P0':'I_1','prior_paid_stages':0},
      'fixed_post':'one A41 centre word Uhat0; identical word in every incoming comparison',
      'original_MG12_convention':'executed outgoing word V_b=P_b^T; V_b=Uhat0 at centre; no free native inverse is emitted',
      'incoming_family':'P_f=I or B63 G_j^nplus/nminus, 0<=j<2688; V_b=P_b^T fixed',
      'outgoing_family':'P_f=I fixed; executed V_b=Qhat_ab_sign Uhat0, all 0<=a<b<2^2688',
      'outgoing_exact_target_signs':'R_ab of same actual B63 plus exponent and its exact inverse',
      'post_moved_with_incoming_P_f':False,'new_compiler_private_or_copied_WORK_births':0,
      'actual_SAM_support_for_all_pre_post_words':True,
      'early_births':n,'late_retention_pairs':K,'dimension_debt_bits':cfg['dimension_debt'],
      'common_pre_calls_hex':hex(cfg['preL']),'common_post_calls_hex':hex(cfg['postL']),
      'common_probe_calls_hex':hex(cfg['probeL']),'Lbase_hex':hex(cfg['Lbase']),
      'Nbase_hex':hex(cfg['Nbase']),'Nbase_bit_length':cfg['Nbase'].bit_length(),
      'actual_native_calls_including_retention_hex':hex(cfg['Lbase']+K),
      'actual_clock_layers_N_hex':hex(cfg['Nbase']+2*K),
      'clock_dimension':'2^n*(Lbase-2+3*2^K)-1','final_dimension':'2^(n+K)',
      'last_actual_g':gate('G',n+K-1),'last_actual_g_in_common_retention_not_deferred_post':True,
      'original_RAW_checkpoint_layer_hex':hex(mark),
      'original_A30_prefix_maps_preserved_for_declared_incoming_state':True,
      'full_original_H1_marks_and_four_slots_proved':False,
      'C':'p^(K/2) c, c=<chi|Qhat Uhat0 M P_f|chi>',
      'J':'-log(1-z+z*p^K*c^2)',
      'H':'beta^-1 log(359D+2 Tr_(33D) exp(-beta Delta0(T))); all425D modes',
      'actual_native_centre_gain':'4 z p^K c_ref gs/(1-z+z p^K c0hat^2)',
      'gain_lower':'(8/3) z gs p^K; c_ref>2/3, gs>2^-3158',
      'independent_incoming_source':'-c0hat * <chi|Uhat0 M X|chi>/(2 c_ref gs)',
      'ideal_fixed_post_incoming_source':'-D_X <chi|M^2|chi>/(4 c_ref gs), equal to A37 reduced first source',
      'incoming_each_row_error_strict_lt':'2^-75','incoming_corrected_covector_error_strict_lt':'2^-70',
      'outgoing_full_finite_covector_dual_strict_lt':'2^-75',
      'outgoing_norm_scope':'linear functional of all Givens-plane finite price contrasts, dual of skew operator norm; not an exact smooth native gradient',
      'bounds':{k:encode(v) for k,v in b.items()},
      'production_post_provider_or_word_materialized':False,
      'production_word_construction_scope':'A41 mathematical finite recipe plus exact length padding; executable assembler tested only with supplied small words',
      'new_action_Info_or_source_coefficient_added':False,'same_prior_F_N_fibre_claimed':False,
      'independent_inner_Q_rows_stationary_claimed':False,
      'full_Cost_Info_binding_or_refinement_proved':False,
      'physical_C_closed':False,'GR_closed':False,
      'source_sha256':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in pins}}


if __name__=='__main__':
    out=build();(P/'FIXED_POST_PAID_FAMILY_PLAN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','Nbase_bit_length','late_retention_pairs','incoming_corrected_covector_error_strict_lt')}))
