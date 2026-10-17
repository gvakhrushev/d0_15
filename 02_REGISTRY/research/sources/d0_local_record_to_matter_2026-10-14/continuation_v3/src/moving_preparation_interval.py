#!/usr/bin/env python3
"""Outward interval bounds for the actual count filter AND its first preparation jet.
The event is fixed during differentiation. Full finite mode multiplicities retained.
"""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,math
from pathlib import Path
import mpmath as mp
ROOT=Path(__file__).resolve().parents[1]

def run(v2):
    old=v2/'input_v1/d0_local_matter_bridge'
    source=old/'src/interval_l8.py';rootfile=old/'results/interval_L8.json'
    spec=importlib.util.spec_from_file_location('pinned_l8_features',source)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    mp.mp.dps=75;mp.iv.dps=65;iv=mp.iv
    checks=[]
    def ck(name,condition):
        if not bool(condition):raise AssertionError((name,condition))
        checks.append(name)
    def val(v):return iv.mpf(v[0])+iv.mpf(v[1])*iv.sqrt(2)
    L=8;N=L**4;gamma=((iv.sqrt(5)-1)/2)**3;gammap=((mp.sqrt(5)-1)/2)**3
    rows=mod.features();ck('all_4096_spatial_modes',sum(n for _,n in rows)==N)
    a1=iv.mpf(128)-64*iv.sqrt(2);e1=gamma*a1/(4*L*L)
    e1p=gammap*mp.sin(mp.pi/L)**2
    eps_power=18;budget=16/e1p*mp.log(mp.mpf(L)**(4+eps_power)/4)
    T=int(mp.ceil(budget));Tiv=16/e1*iv.ln(iv.mpf(L)**(4+eps_power)/4)
    ck('integer_comparison_budget',iv.mpf(T-1)<Tiv and Tiv<iv.mpf(T))
    lo=int(mp.ceil(T*e1p/2));hi=int(mp.floor(3*T*e1p/2))
    ck('fixed_integer_lower_threshold',iv.mpf(lo-1)<T*e1/2 and T*e1/2<lo)
    ck('fixed_integer_upper_threshold',iv.mpf(hi)<3*T*e1/2 and 3*T*e1/2<hi+1)
    ck('kernel_first_derivative_excluded',lo>=2)
    root=json.loads(rootfile.read_text());d=iv.mpf(root['center_decimal_rationals'][0])+iv.mpf(['-1e-12','1e-12'])
    o=iv.mpf(root['center_decimal_rationals'][1])+iv.mpf(['-1e-12','1e-12'])
    gmax=iv.mpf('0.1');ck('same_v1_box_positive_bounded',d-o>0 and d+3*o<gmax)
    cache={}
    def filt(A):
        if A==(0,0):return iv.mpf(0),iv.mpf(0)
        if A in cache:return cache[A]
        e=gamma*val(A)/(4*L*L)
        ck('strict_effect_domain_'+str(A),e>0 and e<1)
        w=iv.mpf(math.comb(T,lo))*e**lo*(1-e)**(T-lo);f=w
        for k in range(lo,hi):
            w*=iv.mpf(T-k)/(k+1)*e/(1-e);f+=w
        # Exact telescoping derivative of the fixed acceptance window.
        lower=T*iv.mpf(math.comb(T-1,lo-1))*e**(lo-1)*(1-e)**(T-lo)
        upper=T*iv.mpf(math.comb(T-1,hi))*e**hi*(1-e)**(T-hi-1)
        fp=lower-upper
        cache[A]=(f,fp);return f,fp
    Z=iv.mpf(0);tail=iv.mpf(0);gap1=iv.mpf(0);gap2=iv.mpf(0)
    for (A,B),n in rows:
        f,_=filt(A);weight=n*f;Z+=weight
        if A!=(128,-64):tail+=weight
        gap=(val(A)-a1)*d+val(B)*o
        gap1+=weight*gap;gap2+=weight*gap*gap
    prob=Z/N;distance=tail/Z;mean_gap=gap1/Z
    chi=iv.mpf(0)
    for (A,B),n in rows:
        _,fp=filt(A);gap=(val(A)-a1)*d+val(B)*o
        chi+=n*abs(gap-mean_gap)*abs(fp)/Z
    ck('heralding_probability_kept',prob>iv.mpf('0.0019531249') and prob<iv.mpf('0.0019531251'))
    ck('finite_filter_is_not_exact',distance>0)
    ck('declared_state_accuracy',distance<iv.mpf(L)**(-eps_power))
    ck('moving_preparation_correction_is_not_assumed_zero',chi>0)
    # Generic source bound in declared coordinates: 10 G probes and at most
    # 64 normalized unitary-return tangent slots per site. dE vanishes on G
    # probes of the fixed reference. ||dE|| <= 4 gamma on each return probe.
    fixed_source=(128+576*gmax)*L**4*distance
    moving_source=256*gamma*L**6*chi
    total=fixed_source+moving_source
    variance=gap2/Z-mean_gap**2
    ck('variance_positive',variance>0)
    matter=2*iv.sqrt(variance);scaled_matter=L**2*matter
    ck('actual_complete_prepared_source_bound',total<iv.mpf('1e-10'))
    ck('actual_prepared_matter_bound',scaled_matter<iv.mpf('1e-8'))
    emax=4*gamma
    coarse_chi=2*(16*gmax*L**2)*T*distance/(e1*(1-emax))
    ck('all_modes_log_score_bound_is_conservative',chi<coarse_chi)
    fair_bits=4+4*3+2*T
    setup_attempts=int(mp.ceil(mp.log(2*fair_bits)/(-mp.log(1-2*gammap))))
    setup_failure=fair_bits*(1-2*gamma)**setup_attempts
    ck('full_setup_success_more_than_half',setup_failure<iv.mpf('0.5'))
    runs=int(mp.ceil(mp.mpf(L**4)/2*mp.log(mp.mpf(10)**6)))
    ck('bounded_whole_experiment_repetitions',iv.exp(-iv.mpf(2)*runs/L**4)<iv.mpf('1e-6'))
    return {'schema':'d0-moving-preparation-interval/1','status':'PASS','L':L,
     'spatial_modes':N,'Fock_components':16,'retained_history_multiplicities':'complete',
     'T':T,'fixed_event':[lo,hi],'state_accuracy_power':eps_power,
     'fair_bits_required':fair_bits,'attempts_per_fair_bit':setup_attempts,
     'setup_success_lower_interval':str(1-setup_failure),
     'bounded_attempts_for_total_failure_1e_minus6':runs,
     'acceptance_probability_interval':str(prob),'trace_distance_interval':str(distance),
     'preparation_covector_trace_norm_interval':str(chi),
     'hminus2_frozen_density_source_bound_interval':str(fixed_source),
     'hminus2_moving_preparation_source_bound_interval':str(moving_source),
     'hminus2_full_prepared_source_bound_interval':str(total),
     'full_matter_Hilbert_residual_interval':str(matter),
     'hminus2_full_matter_Hilbert_residual_interval':str(scaled_matter),
     'coarse_analytic_chi_bound_interval':str(coarse_chi),
     'input_sha256':{str(p.relative_to(v2)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (source,rootfile)},
     'scope':'First source jet on genuine unitary-preparation tangents at the commuting reference; bounded probe realization is a declared hypothesis.',
     'v1_root_is_pinned_conditional_input':True,'exact_finite_root':False,
     'common_H_J_R':False,'native_refinement_or_physical_forcing':False,
     'checks':checks,'interval_controls':len(checks)}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--v2',type=Path,default=ROOT.parent/'v2_snapshot/d0_research_v2');ap.add_argument('--write',action='store_true');args=ap.parse_args()
    out=run(args.v2);out['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    dest=ROOT/'results/moving_preparation_interval.json'
    if args.write:dest.write_text(json.dumps(out,indent=2)+'\n')
    elif json.loads(dest.read_text())!=out:raise AssertionError('IMMUTABLE_INTERVAL_RECEIPT_MISMATCH')
    print('PASS_MOVING_PREPARATION_INTERVAL',out['interval_controls'],'T',out['T'],'event',out['fixed_event'])
    for k in ('acceptance_probability_interval','trace_distance_interval','preparation_covector_trace_norm_interval','hminus2_full_prepared_source_bound_interval','hminus2_full_matter_Hilbert_residual_interval'):print(k,out[k])
if __name__=='__main__':main()
