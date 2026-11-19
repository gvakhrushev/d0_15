"""Strict curvature and local/global error bound in the stated QND model."""
from fractions import Fraction as F
import json
import mpmath as mp
from check_independent_shift_shared_site import correlation_checks

def need(x,msg):
    if not x:raise AssertionError(msg)

# Golden root p in (309/500,619/1000), with p^2=1-p and p^3=2p-1.
pl,pu=F(309,500),F(619,1000);p2l=1-pu;umin=F(153,250)
z=F(1,2**20);Lmax=4*(2*pu-1)
need(0<Lmax<1,'L0<1 on entire rational interval')
# u=p+p²y in (0.612, 5/8) for |y|<=1/64.
need(pl-(1-pl)/64>umin,'lower u endpoint')
need(pu+(1-pu)/64<F(5,8),'upper u endpoint')
# -B''=8p^4(6u²-1); curvature bracket >=(2-L0)(1-z).
curvature_part=8*p2l*p2l*(6*umin*umin-1)
bracket_part=(2-Lmax)*(1-z)
need(curvature_part*bracket_part>F(3,2),'strict -R_second > 3z/2')
site=correlation_checks();need(site['local_F_histogram']=={'-1':64,'0':128,'1':64},'true site field')
need(site['shared_shift_example_assumes_QND_Site_and_same_shift'],'QND needed for shared comparison')
mp.mp.dps=100;p=(mp.sqrt(5)-1)/2;A=p*mp.sin(712*mp.asin(p));zz=mp.mpf(2)**-20;L=4*p**3
Lambda=mp.mpf(1) # numerical illustration only, not physical bound

def R(y):
 u=p+p*p*y;B=4*u*u*(1-u*u);AA=L+(1-L)*B
 return 1-(1-zz*B)*(1-zz*AA)
b=A*A/(32*Lambda)
gap=R(0)-(R(-b)+2*R(0)+R(b))/4
bound=3*zz*A**4/(8192*Lambda**2)
need(gap>bound>0,'true finite numerical gap exceeds certified lower bound')
# Integral second-order formula and direct global/local distinct outcomes.
calc=(R(0)-(R(-b)+R(b))/2)/2
need(abs(calc-gap)<mp.mpf('1e-90'),'exact pair identity')
res={'status':'PASS','p_rational_lower':str(pl),'p_rational_upper':str(pu),
 'u_lower':str(umin),'u_upper':'5/8','minus_B_doubleprime_over_unit_lower':str(curvature_part),
 'bracket_lower':str(bracket_part),'product_lower_gt_3_over_2':True,
 'strict_curvature':'-R_second(y)>3*z/2 for abs(y)<=1/64',
 'general_local_global_gap_bound':'3*z*Var_X(q)/(16384*Lambda^2)',
 'explicit_F_distribution':site['local_F_histogram'],
 'explicit_q_variance':'2*A^4','explicit_gap_bound':'3*z*A^4/(8192*Lambda^2)',
 'illustrative_Lambda_one_not_proved_physical':True,
 'illustrative_exact_gap':mp.nstr(gap,40),
 'illustrative_strict_lower_bound':mp.nstr(bound,40),
 'common_site_QND_and_per_history_independent_sign_effect_assumed':True,
 'full_book_cost_local_gate_source_and_GR_closed':False,'GR_closed':False}
print(json.dumps(res,indent=2,sort_keys=True))
