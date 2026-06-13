#!/usr/bin/env python3
import math, json
from pathlib import Path

phi_golden = (1 + math.sqrt(5)) / 2
pi0 = (6/5) * phi_golden**2
tau0 = 2*pi0
tau = 2*math.pi

def euler_phi(n:int)->int:
    result=n
    m=n
    p=2
    while p*p<=m:
        if m%p==0:
            while m%p==0:
                m//=p
            result-=result//p
        p+=1
    if m>1:
        result-=result//m
    return result

A=4
rank=3
Omega8=8
V11=11
V13=13
V=33
d13=20
qT=A*V11
mT=A+rank
qEW=2*(A+1)*(2*V + A + 1)
mEW=(A+1)*d13 + V13

checks={}
checks['qT_formula'] = qT == 44
checks['mT_formula'] = mT == 7
checks['phi_44_terminal'] = euler_phi(qT) == d13 == 20
checks['qEW_formula'] = qEW == 710
checks['mEW_formula'] = mEW == 113
checks['phi_710'] = euler_phi(qEW) == 280
checks['ew_depth'] = euler_phi(qEW)//Omega8 == 35 and euler_phi(qEW)%Omega8 == 0
checks['old_shadow_35'] = V + rank - 1 == 35
checks['return_44_near_2pi'] = abs(qT/mT - tau) < 0.003
checks['return_710_near_2pi'] = abs(qEW/mEW - tau) < 1e-6
checks['d0_refined_return_4059_646'] = abs(4059/646 - tau0) < 2e-7
checks['tau0_close_to_2pi'] = abs(tau0 - tau) < 1e-4

results={
    'status':'PASS_V11_40_PHASE_UNFOLDING_MASTER_CHAIN' if all(checks.values()) else 'FAIL',
    'checks':checks,
    'values':{
        'tau_2pi': tau,
        'pi0': pi0,
        'tau0_2pi0': tau0,
        'tau0_minus_2pi': tau0-tau,
        'qT': qT,
        'mT': mT,
        'qT_over_mT': qT/mT,
        'qT_error_2pi': qT/mT - tau,
        'phi_44': euler_phi(qT),
        'qEW': qEW,
        'mEW': mEW,
        'qEW_over_mEW': qEW/mEW,
        'qEW_error_2pi': qEW/mEW - tau,
        'phi_710': euler_phi(qEW),
        'ew_depth': euler_phi(qEW)//Omega8,
        'd0_refined_return': '4059/646',
        'd0_refined_return_value': 4059/646,
        'd0_refined_return_error_tau0': 4059/646 - tau0,
    }
}
out=Path(__file__).with_suffix('.json')
out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding='utf-8')
print(results['status'])
for k,v in checks.items(): print(f'{k}: {v}')
