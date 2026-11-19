"""Full joint descriptor/report CQ on the conditional ten-sign L=4 slice."""
from itertools import product
import json
import mpmath as m
m.mp.dps=75
p=(m.sqrt(5)-1)/2; ell=m.log(1/p); a=p*m.sin(712*m.asin(p)); A2=a*a
z=m.mpf(2)**-20; L=4*p**3; Lam=m.mpf(1) # example only, not a physical bound

def rfun(y):
    u=p+p*p*y; B=4*u*u*(1-u*u); Ac=L+(1-L)*B
    return 1-(1-z*B)*(1-z*Ac)

def ent(x):
    return -x*m.log(x)-(1-x)*m.log(1-x)

def data(sig):
    # The eight true Hq signs use distinct CAR pairs. The original ten-sign
    # coefficient lift is multiaffine with the ordered monomial convention.
    coeff=m.taylor(lambda t:rfun(sig*t/64),m.mpf(0),8)
    vals=[m.mpf(0),-2*A2/Lam,-4*A2/Lam]
    probs=[m.mpf(13)/16,m.mpf(1)/8,m.mpf(1)/16]
    # One u-probability s for all 16 independent u-writers, v=1/2.
    # probabilities 1-B(s)/4-(1-s)^2/4, B(s)/4, (1-s)^2/4
    dprobs=[m.mpf(1)/4,m.mpf(0),-m.mpf(1)/4]
    expected_h=m.mpf(0); dh=m.mpf(0); E_R=m.mpf(0);d_R=m.mpf(0);nonzero=0
    for ii in product(range(3),repeat=8):
        q=m.mpf(0);prod=m.mpf(1)
        for k in range(9):
            if k:prod*=vals[ii[k-1]]
            q+=coeff[k]*prod
        assert 0<q<1
        w=m.fprod(probs[i] for i in ii)
        score=sum((dprobs[i]/probs[i] for i in ii),m.mpf(0))
        expected_h+=w*ent(q);dh+=w*score*ent(q)
        E_R+=w*q;d_R+=w*score*q
        nonzero+=1
    ystar=sig*(-A2/(2*Lam))/64
    direct=rfun(ystar); dr=m.diff(rfun,ystar)*sig*A2/(64*Lam)
    assert abs(E_R-direct)<m.mpf('1e-68')
    assert abs(d_R-dr)<m.mpf('1e-68')
    information=ent(E_R)-expected_h
    d_info=m.log((1-E_R)/E_R)*d_R-dh
    assert information>0
    # Exact coefficient identity: full CQ derivative vs naive separate h(E R).
    full=d_R-dh/ell
    naive=d_R*(1-m.log((1-E_R)/E_R)/ell)
    assert abs(full-naive-d_info/ell)<m.mpf('1e-68')
    return dict(sign=sig,conditional_categories=nonzero,
      final_report_probability=m.nstr(E_R,35),
      derivative_report_per_s=m.nstr(d_R,35),
      full_classical_joint_entropy_nat=m.nstr(32*m.log(2)+expected_h,35),
      conditional_report_entropy_nat=m.nstr(expected_h,35),
      full_record_report_mutual_information_nat=m.nstr(information,35),
      mutual_information_derivative_per_s=m.nstr(d_info,35),
      full_partial_code_minus_cq_derivative_per_s=m.nstr(full,35),
      incorrectly_assuming_independent_report_derivative_per_s=m.nstr(naive,35),
      code_minus_cq_derivative_difference=m.nstr(full-naive,35))

result={'status':'PASS','model':'conditional complete classical H/Q/R ledger, all quantum memories retained; no Book03 cost assertion',
 'common_scalar_ready_and_success_condition_assumed':True,
 'complete_eight_sign_factorization_on_shared_site_and_oldRIGHT_assumed':True,
 'independent_fresh_CAR_alone_proves_common_site_factorization':False,
 'shared_site_counterexample_ref':'COMPLEMENTED_ACTUAL_HQ_REPORT_RU.md section 2',
 'original_report_Lambda_1_only_illustrative':True,
 'true_Fourier_CAR_material_copies':16,'independent_recorded_descriptor_bits':32,
 'independent_Hq_signs':8,'q_categories_per_sign':['0','-2A^2/Lambda','-4A^2/Lambda'],
 'central_q_category_masses':['13/16','1/8','1/16'],
 'categories_enumerated':3**8,'absolute_writer_codes_length':96,
 'report_codes_lengths':[1,2],'full_book_info_and_field_42_source_proved':False,
 'positive_and_negative_sign_results':[data(1),data(-1)],'GR_closed':False}
print(json.dumps(result,indent=2,sort_keys=True))
