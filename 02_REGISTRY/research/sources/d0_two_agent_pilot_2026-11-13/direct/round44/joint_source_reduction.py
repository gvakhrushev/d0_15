#!/usr/bin/env python3
"""Dimension-free internal feedback reduction at the pinned actual centre.

No production matrix, extra word, or physical tangent-domain admission is
constructed here. The bound is a logical analytic source statement on the
real SAM skew space, hence restricts to whichever directions are admitted.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib,json,sys
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent;D=P.parent
B=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open')
sys.path.insert(0,str(D/'round43'));import local_q_price as previous


def bounds():
    s=F(1,1<<30);gs=F(1,1<<3158)
    eB,eW,eU,ep=(F(1,1<<k) for k in (3231,3244,14623,3232))
    # Whole-label difference, not an adjacent edge. Distinct Julia addresses
    # are orthogonal blocks; coframe and proper-link blocks remain distinct.
    choi_co=F(3,16);choi_link=F(81,16)
    assert 24*2/F(256)==choi_co and 24*54/F(256)==choi_link
    ideal_squared=(360*256*choi_co**2+180*256*choi_link**2+16*F(11,10)**2)*s*s
    assert ideal_squared<F(1089**2)*s*s
    delta=1100*s
    assert 1089*s+2*ep<delta
    # Compare to the SAME central scalar I_tau(Y0). No large absolute
    # constant sigma/(gs) is inserted into the commutator bound.
    tau_over_gs=104*F(1,1<<3083)+(1<<25)*2704*s+eB/gs
    assert tau_over_gs<85
    error=F(3,4)*(tau_over_gs*(2*delta*delta+2*eW)+eW/gs)+eU/gs
    assert error<F(1,1<<32)
    old_triangle=(1024*F(9,4)+1536*F(25,2)+128*F(5,4))*s
    assert delta<old_triangle
    return {'global_ideal_source_distance_squared_upper':ideal_squared,
            'global_old_profile_source_distance_upper':delta,
            'centred_actual_M_spread_over_gs_upper':tau_over_gs,
            'all_SAM_Qb_minus_half_Pf_dual_operator_norm_upper':error}


def build():
    rows=[json.loads(line) for line in (B/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl').read_text().splitlines()]
    co=Counter((tuple(x['site']),x['role']) for x in rows if x['kind']=='coframe')
    links=Counter((tuple(x['site']),x['role']) for x in rows if x['kind']=='proper_link')
    matter=Counter(tuple(x['site']) for x in rows if x['kind']=='matter')
    assert len(co)==256 and set(co.values())=={4}
    assert len(links)==256 and set(links.values())=={6}
    assert len(matter)==64 and set(matter.values())=={2}
    values=bounds()
    pins=[Path(__file__),D/'round27/PREPARED_SOURCE_MOMENT_LAW_RU.md',
      D/'round30/COMMON_SOURCE_MARKED_PLAN.json',D/'round30/marked_source_schedule.py',
      D/'round37/ACTUAL_POST_SAM_STATIONARY_REDUCTION_RU.md',
      D/'round41/SAM_ONLY_COMPILER_PLAN.json',D/'round42/FIXED_POST_PAID_FAMILY_PLAN.json',
      D/'round43/LOCAL_Q_PRICE_RU.md',D/'round43/RESULT.json',
      B/'round21/CHART_ENVELOPE_RESULT.json',B/'round21/L4_INTERIOR_CHART_COORDINATES.jsonl',
      B/'round24/TORUS_CHOI_ADDRESSES.jsonl',B/'round25/targets.py',
      B/'round65/B65_CENTRE_SOURCE_AND_BOUNDS_RU.md',B/'round65/SCALAR_HESSIAN_ENVELOPE.json',
      B/'round82/B82_FOUR_SLOT_Q_KERNEL_RU.md',B/'round82/actual_q_kernel.py',
      B/'round84/B84_UNIFORM_ADJACENT_SOURCE_RU.md',B/'round84/B84_UNIFORM_SOURCE_BOUND.json']
    return {'status':'ALL_REAL_SAM_SKEW_ANALYTIC_INNER_SOURCE_REDUCTION',
      'consumer':'independent preparation-source composition after A43; no exponential SAM-dimension loss',
      'centre':'A30 actual core, one A41 fixed executed outgoing Uhat0; incoming and inner endpoints identity',
      'pointwise_source_pair_domain':'every pair of complete SAM labels on original fixed B25 L4 cube',
      'coframe_addresses':len(co),'proper_link_addresses':len(links),'variable_material_sites':len(matter),
      'global_old_profile_source_distance_strict_lt':'1100*s, s=2^-30',
      'centred_actual_M_spread_over_gs_strict_lt':'85',
      'Qb_minus_half_reduced_Pf_analytic_dual_norm_strict_lt':'2^-32',
      'Qf_plus_half_reduced_Pf_analytic_dual_norm_strict_lt':'2^-32',
      'norm':'sup over all real SAM skew Y with ||Y||op<=1; valid on every admitted restriction',
      'exact_kernel_map':'K(R)=L Hadamard R; Phi(Y)=L Hadamard Y',
      'joint_return':'c=x^T K(R) y, x=Vb^T chi, y=Pf chi, R=Qb Qf^T',
      'joint_nonzero_feedback_stationarity_if_all_skew_admitted':['K y=c x','K^T x=c y','R^T (diag(x) L diag(y)) symmetric'],
      'all_skew_domain_admission_proved':False,
      'all_skew_finite_native_comparisons_or_heat_paid':False,
      'same_fixed_FN_fibre_or_unsplit_bank_proved':False,
      'uniform_mesh_refinement_or_recompiled_s_family_proved':False,
      'production_kernel_materialized':False,
      'bounds':{k:previous.old.encode(v) for k,v in values.items()},
      'new_action_Info_or_selector_added':False,'physical_C_closed':False,'GR_closed':False,
      'source_sha256':{str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in pins}}


if __name__=='__main__':
    out=build();(P/'JOINT_SOURCE_REDUCTION_PLAN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out['status'])
