#!/usr/bin/env python3
"""Original Golden-only four-arm matching, complete binary reporter and Info firewall.

Exact Q(sqrt(5)) coin/cocycle algebra. The original full128 CAR/Walsh/Julia
mixed coefficients are independently tested by check_native_four_arm_exact.py.
Neither script claims native Book03 selection.
"""
from itertools import product
import sympy as S

p=(S.sqrt(5)-1)/2
phi=1/p
A=p
B=p**2
assert S.simplify(A+B-1)==0
strings=[''.join(w) for w in product('AB',repeat=4)]
def mass(word):
    out=S.Integer(1)
    for ch in word:
        out*=A if ch=='A' else B
    return out

assert S.simplify(sum(mass(w) for w in strings)-1)==0
arms=('ABAB','ABBA','BAAB','BABA')
assert all(S.simplify(mass(w)-p**6)==0 for w in arms)
assert S.simplify(sum(mass(w) for w in strings if w not in arms)
                  -(1-4*p**6))==0

x,y,z,w=S.symbols('x y z w',real=True)
Q=S.expand(p**6*(2+x-y-z+w))
# The two pairs of independently matched native history references.
assert S.simplify(Q.subs({x:y,z:w})-2*p**6)==0
assert S.simplify(Q.subs({x:z,y:w})-2*p**6)==0
assert S.simplify(S.diff(Q,x)-p**6)==0
assert S.simplify(S.diff(Q,y)+p**6)==0
q0=2*p**6
assert 0<float(q0)<float(p**2)<1
assert 0<float(4*p**6)<1

# Native fixed 0/10 binary prefix reporter has cost1+q and Kraft weights
# mu=(p,p**2).  Prove KL identity symbolically WITHOUT trusting log rewrites.
q=S.symbols('q',positive=True)
h=-(q*S.log(q)+(1-q)*S.log(1-q))/S.log(phi)
cost=1+q
KL=(q*S.log(q/p**2)+(1-q)*S.log((1-q)/p))/S.log(phi)
L,X,Y=S.symbols('L X Y',nonzero=True)
h_formal=-(q*X+(1-q)*Y)/L
KL_formal=(q*(X+2*L)+(1-q)*(Y+L))/L
assert S.simplify(1+q-h_formal-KL_formal)==0
assert abs(float((cost-h-KL).subs(q,S.Rational(1,3)).evalf(30)))<1e-28
kappa=S.diff(cost-h,q).subs(q,q0)
kappa2=1-S.log((1-q0)/q0)/S.log(phi)
assert abs(float((kappa-kappa2).evalf(40)))<1e-35
assert float(kappa)<0
# All pure metric and pure link jets vanish; full mixed 6x6 Hessian is
# [[0,kappa*p^6*M],[kappa*p^6*M.T,0]] and has inertia (3+,3-) when det M!=0.

# But FULL observed Golden COIN+FLAG information is DIFFERENT from
# the marginal final b and retains actual, generally nonzero flat source.
H_binary=lambda t: -(t*S.log(t)+(1-t)*S.log(1-t))/S.log(phi)
H_coin=-sum(mass(s)*S.log(mass(s)) for s in strings)/S.log(phi)
H_joint=H_coin+p**6*sum(H_binary(t) for t in (x,y,z,w))
qs=S.Rational(1,13)
g=S.simplify((S.diff(H_joint,x)+S.diff(H_joint,y))
             .subs({x:qs,y:qs,z:qs,w:qs}))
assert S.simplify(g-2*p**6*S.diff(H_binary(q),q).subs(q,qs))==0
assert float(g)>0

print('PASS original 16 complete four-draw Golden branches: four equal p^6 arms')
print('PASS normalized positive four-arm marginal, both reference axes constant')
print('PASS original fixed 0/10 binary Golden Cost-Info and nonzero mixed multiplier')
print('PASS full measured coin+flag Info has NONZERO independent flat source')
print('VALUES',{'p':float(p),'p6':float(p**6),'Qref':float(q0),
                'KLref':float(KL.subs(q,q0)),
                'mixed_source_multiplier':float(kappa*p**6),
                'H_coin_flag_flat_source_control':float(g)})
