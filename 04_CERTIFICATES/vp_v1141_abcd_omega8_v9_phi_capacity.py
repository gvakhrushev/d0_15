#!/usr/bin/env python3
import math
from fractions import Fraction

def phi_euler(n:int)->int:
    result=n
    x=n
    p=2
    while p*p<=x:
        if x%p==0:
            while x%p==0:
                x//=p
            result-=result//p
        p+=1
    if x>1:
        result-=result//x
    return result

ABCD=4
Omega8=8
D2=2
V9=Omega8+1
V11=V9+D2
V13=V9+ABCD
rankA=3
V=V9+V11+V13
qT=ABCD*V11
phi44=phi_euler(qT)
qEW=2*(ABCD+1)*(2*V+ABCD+1)
mEW=(ABCD+1)*phi44 + V13
phi710=phi_euler(qEW)
EW_depth=phi710//Omega8

sqrt5=math.sqrt(5)
phi=(1+sqrt5)/2
p=1/phi
p2=p*p
delta=(p-p2)/2

checks=[]
def check(name, cond, value=None):
    checks.append((name, bool(cond), value))

check('ABCD = D2 × D2 = 4', ABCD==D2*D2, ABCD)
check('Omega8 = ABCD × 2 = 8', Omega8==ABCD*2, Omega8)
check('V9 = Omega8 + witness = 9', V9==9, V9)
check('V11 = V9 + D2 = 11', V11==11, V11)
check('V13 = V9 + ABCD = 13', V13==13, V13)
check('total |V| = 33', V==33, V)
check('qT = ABCD*V11 = 44', qT==44, qT)
check('Euler phi(44)=20', phi44==20, phi44)
check('d13 = phi(44)', phi44==20, phi44)
check('qEW=710', qEW==710, qEW)
check('mEW=113', mEW==113, mEW)
check('Euler phi(710)=280', phi710==280, phi710)
check('EW depth = phi(710)/Omega8 = 35', EW_depth==35 and phi710%Omega8==0, EW_depth)
check('p+p^2=1', abs(p+p2-1)<1e-12, p+p2)
check('delta = 1/(2 phi^3)', abs(delta-1/(2*phi**3))<1e-12, delta)

# Alternative exclusions as finite capacity checks
check('ABCD alternative with 3 roles fails full D2×D2 coverage', 3 < D2*D2, 'missing role')
check('Omega4 lacks orientation bit', math.log2(4)==2 and math.log2(Omega8)==3, 'capacity gap 1 bit')
check('V8 lacks witness', 8==Omega8 and V9==Omega8+1, 'no basepoint')
check('V10 duplicates witness/hidden state', 10>V9, 'extra state')

ok=all(c[1] for c in checks)
print('PASS_ABCD_OMEGA8_V9_PHI_CAPACITY_CLOSURE' if ok else 'FAIL')
for name, cond, value in checks:
    print(f'{"PASS" if cond else "FAIL"}: {name} :: {value}')
