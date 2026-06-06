#!/usr/bin/env python3
import math
from math import gcd
phi=(1+math.sqrt(5))/2
delta0=(math.sqrt(5)-2)/2
pi0=(6/5)*phi**2
tau0=2*pi0

def euler_phi(n):
    result=n
    p=2
    x=n
    while p*p<=x:
        if x%p==0:
            while x%p==0:
                x//=p
            result-=result//p
        p+=1
    if x>1:
        result-=result//x
    return result

def branch_count(q):
    return sum(1 for a in range(q) if gcd(a,q)==1)

def nearest_error(q,tau):
    m=round(q/tau)
    return m, abs(q-m*tau)

checks=[]
for q, expected in [(6,2),(44,20),(710,280)]:
    checks.append((f'phi({q})', branch_count(q), expected, branch_count(q)==expected))

m44,e44=nearest_error(44,tau0)
checks.append(('44 return within delta0', e44 < delta0, True, e44 < delta0))
checks.append(('d13=phi(44)', branch_count(44), 20, branch_count(44)==20))
checks.append(('EW depth=phi(710)/8', branch_count(710)//8, 35, branch_count(710)==8*35))

m4059,e4059=nearest_error(4059,tau0)
checks.append(('4059/646 refined D0 return', m4059, 646, m4059==646))
checks.append(('4059 return error small', e4059 < delta0**4, True, e4059 < delta0**4))

status='PASS_V11_39_PHASE_UNFOLDING_THEOREM' if all(c[3] for c in checks) else 'FAIL'
print(status)
for name,got,exp,ok in checks:
    print(f'{name}: got={got} expected={exp} ok={ok}')
print(f'tau0={tau0:.15f} delta0={delta0:.15f}')
print(f'44-{m44}tau0 error={e44:.15f}')
print(f'4059-{m4059}tau0 error={e4059:.15f}')
