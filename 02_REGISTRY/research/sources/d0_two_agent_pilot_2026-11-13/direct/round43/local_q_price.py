#!/usr/bin/env python3
"""Named j=2 independent inner-Q finite full Book comparisons.

Consumes B82's literal cuts and B84's uniform prepared-source distance.
The production A41 post remains a mathematical finite word, not an emitted
Python object. Exact small supplied words exercise the paid two-slot recipe.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib,json,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;D=P.parent
B=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open')
sys.path.insert(0,str(D/'round42'));import fixed_post_paid_family as old
sys.path.insert(0,str(B/'round82'));import actual_q_kernel as kernel
gate,repeat=old.gate,old.repeat
CUTS=('Qf_dagger_after_common_RAW_mark','Qb_before_return_bank')


def with_q_slots(factory,sam,powers,slot_length,*,leg='centre',sign='centre',axis=2):
    """Insert TWO paid, fixed-length SAM slots at B82's original cut tags."""
    assert leg in ('centre','Qf','Qb') and sign in ('centre','plus','minus')
    assert (leg=='centre')==(sign=='centre') and 0<=axis<len(sam)
    seen=[]
    for block in factory():
        if block['op']!='B82_CUT':yield block;continue
        name=block['name'];assert name in CUTS and name not in seen;seen.append(name)
        active=(leg=='Qf' and name==CUTS[0]) or (leg=='Qb' and name==CUTS[1])
        power=0
        if active:
            # Original MG12 executes Q_f^T but Q_b: logical signs are opposite.
            which=0 if sign=='plus' else 1
            if leg=='Qf':which=1-which
            power=powers[which];yield repeat(power,gate('G',sam[axis]))
        yield from old.padding(slot_length-power,sam)
    assert seen==list(CUTS)


def extend_configuration(cfg):
    cfg=dict(cfg);slot=max(cfg['powers'])+4
    cfg['core_counts']=Counter(cfg['core_counts']);cfg['core_counts']['CX']+=2*slot
    cfg['Q_slot_calls']=slot;cfg['Lbase']+=2*slot;cfg['Nbase']+=2*slot
    cfg['K']=4*(cfg['Nbase'].bit_length()+3158+1638+75+1+cfg['dimension_debt'])
    return cfg


def budget(cfg):
    s,h,nu=F(1,1<<30),F(1,4),F(3,5)
    gs=F(1,1<<3158);eB=F(1,1<<3231);eW=F(1,1<<3244);eU=F(1,1<<14623)
    # Pointwise exterior-link error, no use of E Theta=0 here.
    assert 24/(1-24*s)<25 and F(17,16)**4<F(4,3)
    assert F(4,3)*25<34 and F(4,3)+34*s<F(3,2)
    plaquette=4*34*F(3,2)**3;assert plaquette==459
    # Difference of derivative-commutators <=4s, norm base <=2,
    # current plaquette norm<6; original trace16 /8 and coefficient400/9.
    f_derivative=3*F(400,9)*2*(4*6+2*plaquette)*s
    assert f_derivative==251200*s and f_derivative<(1<<18)*s
    assert F(2,25)+16*s<F(1,8)
    q_derivative=2/(nu*nu)*(s/F(64)+4*s*s+2*(nu+s)*s)
    assert q_derivative<8*s
    eps=F(1,1<<1531)
    reporter=(1<<47)*eps*(1<<26)+24*(1<<43)*eps*16**2
    assert reporter<F(1,1<<1457)
    edge_I=h**4*((1<<18)*s*s+24*8*s*s)+2*reporter
    assert edge_I<(1<<11)*s*s
    edge_M=2*edge_I/s+2*eB/gs
    assert edge_M<(1<<13)*s==F(1,1<<17)
    # B84: only 360 Choi sources change at j=2; old prefix is not exact ideal.
    lam=F(9,4)*s;assert 2*s+F(1,1<<3231)<lam
    q_error=F(3,8)*((lam*lam/2+2*eW)*F(1,1<<17)+2*eW/gs)+eU/gs
    assert q_error<F(1,1<<77)
    # Concrete A33 axis, not merely existence from a vector norm. The old
    # analytic source is u_sampling*S_j + native error, u_sampling>1/2.
    positive=s/F(6400);f_mean=(1<<10)*s*s
    old_scalar_lower=positive-f_mean-F(1,1<<1426)-F(1,1<<73)
    reduced_lower=old_scalar_lower/2-F(1,1<<2870)
    assert reduced_lower>F(1,1<<44)
    # Full finite-Q price: same derivative bounds and actual gain as A42,
    # but no eU term here because q_error already includes native post error.
    base=old.bounds(cfg)
    finite=base['incoming_finite_Taylor']+base['incoming_B63_angle_error']+base['heat_each_row']
    q_total=q_error+finite
    assert q_total<F(1,1<<75)
    q_lower=reduced_lower/2-q_total
    assert q_lower>F(1,1<<45)
    return {'pointwise_local_f_derivative_bound':f_derivative,
      'pointwise_local_q_derivative_bound':q_derivative,
      'reporter_remainder_sup':reporter,'pointwise_adjacent_I_tau_bound':edge_I,
      'pointwise_actual_M_edge_over_gs_bound':edge_M,
      'old_prefix_j2_distance_bound':lam,
      'Qb_analytic_minus_half_ideal_Pf_bound':q_error,
      'concrete_j2_reduced_Pf_lower':reduced_lower,
      'Q_full_finite_price_vs_analytic_error':finite,
      'Qb_full_finite_price_minus_half_ideal_Pf_bound':q_total,
      'Qb_positive_full_finite_price_lower':q_lower,
      'Qf_negative_full_finite_price_upper':-q_lower}


def build():
    cfg=extend_configuration(old.production_configuration());b=budget(cfg)
    assert cfg['n']==10407050782 and cfg['Nbase'].bit_length()==25457 and cfg['K']==137444
    parent=json.loads((D/'round42/FIXED_POST_PAID_FAMILY_PLAN.json').read_text())
    coords=[json.loads(x) for x in (B/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl').read_text().splitlines()]
    row=next(x for x in coords if x['sam_index']==2)
    assert row['kind']=='coframe' and row['component']==2 and row['role']==0 and row['site']==[0,0,1,1]
    b84=json.loads((B/'round84/B84_UNIFORM_SOURCE_BOUND.json').read_text())
    assert b84['old_prefix_each_state_error_strict_lt']=='2^-3232'
    assert b84['Lambda_coframe_strict_lt']=='2*s+2^-3231 < (9/4)*s'
    pins=[Path(__file__),D/'round42/fixed_post_paid_family.py',D/'round42/FIXED_POST_PAID_FAMILY_PLAN.json',
      D/'round41/SAM_ONLY_COMPILER_PLAN.json',D/'round37/ACTUAL_POST_SAM_STATIONARY_REDUCTION_RU.md',
      D/'round33/check_sampling_bias.py',D/'round33/SAMPLING_SOURCE_BIAS_CHECK.json',
      D/'round33/SAMPLING_SOURCE_BIAS_RU.md',D/'round11/source_operator_dag.py',
      D/'round27/PREPARED_SOURCE_MOMENT_LAW_RU.md',D/'round30/COMMON_SOURCE_MARKED_PLAN.json',
      B/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl',B/'round21/CHART_ENVELOPE_RESULT.json',
      B/'round25/targets.py',B/'round65/B65_CENTRE_SOURCE_AND_BOUNDS_RU.md',
      B/'round82/actual_q_kernel.py',B/'round82/B82_FOUR_SLOT_Q_KERNEL_RU.md',
      B/'round84/B84_UNIFORM_SOURCE_BOUND.json',B/'round84/B84_UNIFORM_ADJACENT_SOURCE_RU.md',
      D.parents[1]/'d0_retained_response_concentration_2026-10-28/GROWING_CLOCK_RU.md']
    return {'status':'CONCRETE_INDEPENDENT_INNER_Q_FINITE_FULL_BOOK_NONZERO_ROWS',
      'phase':'native source completion; remove uncomputed adjacent-kernel premise on one named axis',
      'coordinate':row,'sampler_s':'2^-30 unchanged','step_t':'2^-1618 unchanged',
      'initial_history':{'H0':'C','Omega0':1,'P0':'I_1','prior_paid_stages':0},
      'fixed_outgoing_word':'one A41 centre Uhat0=executed P_b^T, unchanged in all Q endpoints',
      'Q_convention':'Qb+ uses physical G^nplus at second cut; Qf+ uses G^nminus at first cut (executed Qf^T)',
      'two_inner_slots_common_calls_hex':hex(cfg['Q_slot_calls']),
      'early_births':cfg['n'],'late_retention_pairs':cfg['K'],
      'Lbase_hex':hex(cfg['Lbase']),'Nbase_hex':hex(cfg['Nbase']),
      'Nbase_bit_length':cfg['Nbase'].bit_length(),
      'actual_clock_layers_N_hex':hex(cfg['Nbase']+2*cfg['K']),
      'native_calls_including_retention_hex':hex(cfg['Lbase']+cfg['K']),
      'clock_dimension':'2^n*(Lbase-2+3*2^K)-1','last_actual_g':gate('G',cfg['n']+cfg['K']-1),
      'original_RAW_checkpoint_layer_hex':parent['original_RAW_checkpoint_layer_hex'],
      'original_checkpoint_is_before_first_inner_slot':True,
      'same_A42_centre_unitary_operator_not_same_clock':True,
      'actual_gain':'4 z p^K c_ref gs/(1-z+z p^K c0hat^2), same centre corner and K as A42',
      'pointwise_actual_M_adjacent_difference_over_gs_strict_lt':'2^-17',
      'Qb_analytic_minus_half_ideal_Pf_strict_lt':'2^-77',
      'Qb_full_finite_price_minus_half_ideal_Pf_strict_lt':'2^-75',
      'Qb_normalized_positive_full_finite_price_strict_gt':'2^-45',
      'Qf_normalized_negative_full_finite_price_strict_lt':'-2^-45',
      'exact_price_swap':'B(Qf+)=B(Qb-), B(Qf-)=B(Qb+) on this common two-slot family',
      'price_swap_proof':'equal complete unitary segment, same width/length, endpoint-identity stage gauge; T and transported P conjugate, full heat and feedback equal',
      'price_swap_is_full_original_task_FN_mark_transport':False,
      'bounds':{k:old.encode(v) for k,v in b.items()},
      'production_A41_word_or_kernel_table_materialized':False,
      'actual_Q_operator_price_rows_not_generic_toy_only':True,
      'full_original_H1_four_slot_mark_admission_proved':False,
      'full_Cost_Info_binding_or_refinement_proved':False,
      'new_action_Info_coefficient_or_selector_added':False,
      'physical_C_closed':False,'GR_closed':False,
      'source_sha256':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in pins}}


if __name__=='__main__':
    out=build();(P/'LOCAL_Q_PRICE_PLAN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','Nbase_bit_length','late_retention_pairs','Qb_normalized_positive_full_finite_price_strict_gt')}))
