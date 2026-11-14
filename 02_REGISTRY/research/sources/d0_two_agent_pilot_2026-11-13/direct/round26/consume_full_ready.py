#!/usr/bin/env python3
"""Consume A25's declared ideal reporter to discharge the READY factor gap.

This is its ideal canonical-input law, not an exact actual-native READY law
or an admission/equivalence proof for the original physical H1 execution.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib,json,sys
import mpmath as mp
P=Path(__file__).resolve().parent;D=P.parent
sys.path.insert(0,str(D/'round25'));import global_h1 as g
def main():
    ns=g.namespace();local=ns['local_report'];schedule=g.stages(ns)
    selectors=json.loads((D/'round12/SELECTOR_COMPILATION.json').read_text())
    old=json.loads((D/'round15/PREPROCESSOR_READY_COMPOSITION.json').read_text())
    budget=json.loads((g.B/'round29/BUDGET_CERTIFICATE.json').read_text())
    M=selectors['selector_fair_qubits_per_report'];T=selectors['padded_interpreter_slots_per_ten_sign_report']
    ti=F(selectors['ready_probabilities']['internal_slot']);tt=F(selectors['ready_probabilities']['top_slot'])
    assert M==local['fair_bank_count']==10248262 and T==1054
    assert F(selectors['ready_probabilities']['postprocessor'])==1
    assert len(local['selector_and_post_READY_wires'])==2*456+8*19+1==1065
    assert local['READY_total_flags']==M+T+10+1==10249327
    assert Counter(s['kind'] for s in schedule)=={'SITE':1,'SOURCE':1372,'SIGMA':7,'REPORT':7,'PORT_ZERO':1,'SC6':1}
    assert [r['bank'] for r in ns['reports']]==list(g.ns.BANKS)
    # The comparator really reads ONLY the existing seven READY/report pairs
    # and five selectors. No loader/fixed-point private flag is a new READY.
    mapping=ns['SC6_local_to_global'];readouts=[q for r in ns['reports'] for q in (r['all_READY'],r['REPORT'])]
    assert mapping[5:19]==readouts
    private=set(q for s in ns['source_slots'] for q in s['private'])
    assert not private.intersection(mapping)
    for r in ns['reports']:
        assert r['all_READY']==g.ns.report_wire(ns,r,local['all_READY_wire'])
        assert r['REPORT']==g.ns.report_wire(ns,r,local['report_wire'])
        assert r['sigma_bit']==0
    # Reconsume the earlier exact bound rather than infer alpha from 7-fold
    # readiness or attach a p penalty to every deterministic unitary letter.
    failure=M*F(53,100)**28+T*(1-ti)**7+10*(1-tt)**7
    assert failure==F(old['failure_union_bound_rational']) and failure<F(1,2)
    assert 1-2*F(309,500)**3<F(53,100)
    # Independent outward interval evaluation of the exact declared ideal law.
    mp.iv.dps=100;iv=mp.iv;p=(iv.sqrt(5)-1)/2
    assert p>iv.mpf(309)/500
    rational=lambda f:iv.mpf(f.numerator)/f.denominator
    q28=1-(1-2*p**3)**28
    alpha=q28**M*(1-(1-rational(ti))**7)**T*(1-(1-rational(tt))**7)**10
    assert alpha>iv.mpf('0.74068') and alpha<iv.mpf('0.74069')
    joint=alpha**7;assert joint>iv.mpf('0.12229') and joint<iv.mpf('0.12231')
    # Existing B29 dyadic floor; its reference constants and chart stay fixed.
    assert budget['g_floor_gt']=='2^-3128' and budget['g_times_s_floor_gt']=='2^-3158'
    assert budget['m']==2688 and budget['s']=='2^-30' and budget['epsilon_h']=='2^-1531'
    parts,eta=g.canonical_input_error();e=2*eta;gs=F(1,2**3158)
    ratios={'unit_generator':e/gs,'unit_scaled_chart_with_owner_lift':55*e/gs,
            'unit_physical_chart_with_owner_lift':55*2**30*e/gs}
    exponents={'unit_generator':73,'unit_scaled_chart_with_owner_lift':67,'unit_physical_chart_with_owner_lift':37}
    for key,value in ratios.items():assert value<F(1,2**exponents[key])
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    pins=[Path(__file__),D/'round25/global_h1.py',D/'round25/GLOBAL_H1_PLAN.json',D/'round25/H1_NAMESPACE_PLAN.json',
          D/'round17/GLOBAL_REPORT_PLAN.json',D/'round17/GLOBAL_REPORT_COMPILATION.json',D/'round17/GLOBAL_REPORT_ASSEMBLY_RU.md',
          D/'round12/SELECTOR_COMPILATION.json',D/'round15/PREPROCESSOR_READY_COMPOSITION.json',g.B/'round29/BUDGET_CERTIFICATE.json',
          g.B/'round49/SC6_ACTIVE_PORT_OWNER_CHECK.json']
    out={'status':'DECLARED_IDEAL_A25_REPORTER_READY_AND_CONDITIONAL_GAIN_CONSUMPTION',
         'source_sha256':{str(p):sha(p) for p in pins},
         'ideal_ready_definition':'alpha=q28^10248262 * (1-(1-tau_internal)^7)^1054 * (1-(1-tau_top)^7)^10',
         'alpha_is_one_full_declared_ideal_reporter_probability':True,'alpha_is_not_seven_report_joint_probability':True,
         'deterministic_source_preparations_add_READY_factors':False,'new_loader_flags_in_SC6_inputs':False,
         'alpha_interval':str(alpha),'ideal_seven_report_joint_ready_interval':str(joint),'alpha_gt':'1/2',
         'exact_actual_native_READY_probability_or_field_independence_proved':False,
         'ideal_product_source_and_original_Beta_law_identification_needed_for_Pj':True,
         'gain_floor_after_original_reference_and_moment_law_binding':{'g_gt':'2^-3128','g_times_s_gt':'2^-3158'},
         'canonical_input_error_bound':g.encode_error(eta),'compressed_effect_error_bound':g.encode_error(e),
         'conditional_native_only_normalized_error':{k:{'strict_upper_bound':'2^-'+str(exponents[k]),'exact_conservative_ratio':g.encode_error(v)} for k,v in ratios.items()},
         'retained_obligations':['Original seven source-moment/report law on the declared ideal prepared product states',
                                 'Physical births/canonical checkpoint and old marked-map identification',
                                 'Actual marks and Neumann-corrected geometric lift',
                                 'Taylor term and actual reference/geometry source errors',
                                 'Full old-prefix/heat/clock/work/Info and true Gamma_s including retention weight'],
         'native_error_bound_is_not_total_T10_or_full_physical_source_bound':True,
         'physical_C_closed':False,'GR_closed':False}
    (P/'FULL_READY_GAIN_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'alpha_gt':'1/2','conditional_native_error_physical_unit_lt':'2^-37'}))
if __name__=='__main__':main()
