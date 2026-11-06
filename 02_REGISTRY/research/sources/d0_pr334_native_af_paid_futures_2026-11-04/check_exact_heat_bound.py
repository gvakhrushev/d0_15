"""Exact rational heat-tail and full-price gap for the matched native pair.

The all-size closed-walk/moment identity is proved in the companion text.
No numerical spectrum or fitted action is used in these inequalities.
"""
from fractions import Fraction as F
from math import factorial
import json

checks=[]
def need(ok,label):
    if not ok:
        raise ArithmeticError(label)
    checks.append(label)

lo,hi=F(3,5),F(5,8)
need(lo+lo*lo<1<hi+hi*hi,'exact Golden collar 3/5 < p < 5/8')
need(2*(1-hi)==F(3,4) and 2*(1-lo)==F(4,5),
     'beta=2p2=2(1-p) has strict collar 3/4 < beta < 4/5')
# e<3 follows from n! >= 2^(n-1), with strict inequality for n>=3.
# Thus exp(2 beta)<exp(2)<9.
N=69; shortest=N-2; D=16+32+64*67
need((shortest,D,425*D,359*D)==(67,4336,1842800,1556624),
     'actual common whole-clock dimension and all modes')
heat_bound=F(528,1077)*9*F(8,5)**shortest/F(factorial(shortest))
need(heat_bound<F(1,10**80),'strict full heat contrast below 1e-80')
zeta=F(1,2**20)
J_lower=128*zeta*lo**11
need(J_lower==F(177147,400000000000),'exact rational lower bound for J1-J0')
need(J_lower-heat_bound>F(4,10**7),'full B1-B0 strictly exceeds 4e-7')
# Common observer is paid, not folded into the pair clock above.
need(67+54==121 and 16+32+121*64==7792,
     'complete pair plus common observer counts its extra54calls')
observer_heat_bound=F(528,1077)*9*F(8,5)**121/F(factorial(121))
need(observer_heat_bound<F(1,10**170),'paid-observer full heat contrast below 1e-170')
need(hi**5<F(1,8),'1-2p5 is strictly greater than 3/4')
observer_J_lower=96*zeta*lo**7
need(observer_J_lower-observer_heat_bound>F(2,10**6),
     'full price contrast with paid54-call observer exceeds 2e-6')
result={'status':'PASS','checks':checks,
        'heat_upper_rational':str(heat_bound),
        'J_lower_rational':str(J_lower),
        'full_price_gap_strict_lower':'4/10000000',
        'pair_counts':{'calls':67,'births':2,'N':N,'D':D,
                       'full_Hodge_modes':425*D,'harmonic_offset':359*D},
        'observer_counts':{'extra_calls':54,'complete_calls':121,
                           'complete_births':2,'complete_N':123,'complete_D':7792,
                           'full_Hodge_modes':425*7792,'harmonic_offset':359*7792},
        'observer_heat_upper_rational':str(observer_heat_bound),
        'observer_J_lower_rational':str(observer_J_lower),
        'observer_full_price_gap_strict_lower':'2/1000000',
        'scope':{'physical_Info_selected':False,'equal_inventory_means_equal_Cost':False,
                 'universal_same_task_admission':False,'GR_closed':False}}
print(json.dumps(result,sort_keys=True,indent=2))
