#!/usr/bin/env python3
"""Native h=1/4 exact full42 CQ root:
rank D(r0,r1)=1 at stationarity, rank Hess CQ=42 rigorously consumed,
therefore rank(weighted SECOND-JET field->reported-moments)>=41.

Only original strict two-report interval and original Hessian receipts
are consumed, pin-checked. Exact rational 42D examples show sharpness.
NOT physical Book03 heat/Info/writer selection or generic GR.
"""
from __future__ import annotations
import argparse
from decimal import Decimal,localcontext
from fractions import Fraction
import hashlib,json
from pathlib import Path

PINS={
 "02_REGISTRY/research/sources/d0_exact_full42_h4_2026-10-22/"
 "RIGOROUS_EXACT42_CERTIFICATE.json":
 "9f4bdef4c367660539c588db01819330ff0d55b3",
 "02_REGISTRY/research/sources/d0_exact_full42_h4_2026-10-22/"
 "REPORT_BRIDGE_RESULT.json":
 "2c7193f54da76aaf108d2821c45daddac7457f02",
}

def frozen(repo,path,expected):
    b=(repo/path).read_bytes()
    actual=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
    if actual!=expected:raise AssertionError((path,actual,expected))
    return json.loads(b)

def exact_linear_rank_example():
    N=42
    # Stationary source: alpha DM1 + beta DM2 = 0.
    # Both first reporter source covectors span ONLY e0.
    alpha=Fraction(3)
    beta=Fraction(-2)
    grad1=[Fraction(int(j==0)) for j in range(N)]
    grad2=[-alpha/beta*g for g in grad1]
    assert all(alpha*g+beta*h==0 for g,h in zip(grad1,grad2))
    assert grad1[0]!=0 and grad2[0]!=0
    # ANY first-jet quadratic pullback J^T G J has its support only
    # in e0⊗e0, leaving 41 exact coordinate kernel vectors.
    G=((Fraction(2,7),Fraction(3,5)),
       (Fraction(3,5),Fraction(11,9)))
    Q=[[sum(G[a][b]*([grad1,grad2][a][i])*
             ([grad1,grad2][b][j])
             for a in range(2) for b in range(2))
        for j in range(N)] for i in range(N)]
    assert all(Q[i][j]==0 for i in range(N)
               for j in range(N) if i!=0 or j!=0)
    assert Q[0][0]!=0
    # Demonstrate sharpness of general rank bound:
    # choose a SOURCE-map second-jet contribution of rank exactly41.
    second=[[Fraction(int(i==j and i>0)) for j in range(N)]
            for i in range(N)]
    H=[[second[i][j]+Q[i][j] for j in range(N)] for i in range(N)]
    assert H[0][0]==Q[0][0]!=0
    assert all(H[i][i]==1 for i in range(1,N))
    assert all(H[i][j]==0 for i in range(N)
               for j in range(N) if i!=j)
    # Exact rank via diagonal pivots, no floating eigenvalues.
    return {'ambient_field_dimension':N,
            'first_report_Jacobian_rank':1,
            'pullback_first_jet_metric_rank':1,
            'rank_41_second_jet_example':'diag(0,1,...,1)',
            'rank_42_total_Hessian_example':'diag(Q00,1,...,1)',
            'bound_rank_second_jet_at_least':'42-1=41 SHARP'}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[4])
    p.add_argument('--json',type=Path)
    opts=p.parse_args()
    repo=opts.repo.resolve()
    cert,report=[frozen(repo,path,sha) for path,sha in PINS.items()]
    with localcontext() as ctx:
        ctx.prec=78
        assert cert['dimension']==42 and cert['time_intervals']==2
        assert cert['root_cube_radius']=='1E-30'
        assert cert['scope']['all42_mathematically_stationary']
        neumann=(Decimal(cert['qcenter_including_error'])+
                 Decimal(cert['qchange_via_cauchy_bound']))
        assert neumann < Decimal('0.001')
        assert Decimal(report['report_interval_gap_lower'])>Decimal('5.80688e-11')
        assert Decimal(report['report0_D_abs_lower_at_root'])>Decimal('2.26378e-8')
        sminus=Decimal(report['hprime_ratio_minus_one_lower'])
        assert sminus>Decimal('2.37636e-6')
        dm=Decimal(report['mean_report_D_abs_lower_at_root'])
        assert dm>Decimal('2.68978e-14')
        DM1=2*dm
        assert DM1>Decimal('5.37956e-14')
        # From h'0 Dr0+h'1 Dr1=0 and Dr0 !=0, the exact
        # nonzero collinearity is Dr1=-s Dr0, s=h'0/h'1>1.
        # Since M1=r0+r1, M2=(r0^2+r1^2)/2,
        # DM1=(1-s)Dr0 and DM2=(r0-s*r1)Dr0 => both
        # first trace-moment gradients span one REAL line.
        result={'status':'PASS_NATIVE_CQ_FISHER_RANK1_FORCES_SECOND_JET_RANK_GE41',
         'root':{'original_h':'1/4',
           'full_CQ_Hessian_rank':42,
           'Neumann_Hessian_invertibility_upper':str(neumann),
           'original_r0_gradient_D29_abs_lower':report['report0_D_abs_lower_at_root'],
           'original_r1_over_r0_gradient_ratio':'-hprime(r0)/hprime(r1)',
           'original_mean_report_D29_abs_lower':str(dm),
           'M1_trace_D29_abs_lower':str(DM1)},
         'exact':{
           'report_first_Jacobian_rank':1,
           'M1_M2_first_Jacobian_rank':1,
           'all_first_jet_Fisher_pullback_rank_upper':1,
           'configured_CQ_Hessian_rank':42,
           'weighted_second_jet_rank_lower':41,
           'split':'D2H=(alpha D2M1+beta D2M2)+'
                   'DM^T (D2Psi) DM',
           'critical_point_tensoriality':
             'non-tensorial second field reparam terms vanish because '
             'alpha DM1+beta DM2=DH=0',
           'exact_rational_42D_sharpness':exact_linear_rank_example(),
         },
         'historical_pins':PINS,
         'scope':{
           'applies_only_to_two_coarse_original_N1_Bernoulli_reports':True,
           'full128_conditional_quantum_history_Fisher_rank_ruled_out':False,
           'full42_original_second_jet_Hessian_recomputed_here':False,
           'h4_Hessian_inertia_newly_established':False,
           'physically_selected_Book03_HJR':False,'GR_closed':False}
        }
    out=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
    print(out,end='')
    if opts.json:opts.json.write_text(out,encoding='utf-8')

if __name__=='__main__':
    main()
