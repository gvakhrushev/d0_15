#!/usr/bin/env python3
"""Scoped numerical audit of the Golden two-aperture source projector.

Only the original local Golden report/Cost-minus-Shannon function and
finite-difference algebra are checked. This neither constructs a paid
M1-admitted two-aperture operation nor certifies physical GR.
Requires mpmath. Run: python3 check_golden_source_projection.py
"""
import json
import mpmath as mp

mp.mp.dps = 100
p = (mp.sqrt(5)-1)/2
phi = 1/p
sig = p*p
zeta = mp.mpf(2)**(-20)
gamma = sig*(1+sig)/(1-sig)

def assert_close(x, y, exponent=70):
    if abs(x-y) > mp.mpf(10)**(-exponent) * max(1,abs(y)):
        raise AssertionError(f"{mp.nstr(x,30)} != {mp.nstr(y,30)}")

assert_close(p+p*p,1)
assert_close(1-sig,p)
assert_close(1/(1-sig),phi)
assert_close(-sig/(1-sig),-p)
assert_close(gamma,3*p-1)
assert 0<gamma<1
assert_close((1+sig)/(1-sig),mp.sqrt(5))

for n in range(1,11):
    w = [mp.binomial(n,j)*(-sig)**(n-j)/(1-sig)**n for j in range(n+1)]
    assert_close(sum(w),1)
    assert_close(sum(map(abs,w)),5**(mp.mpf(n)/2))
    assert_close(sum(wj*sig**j for j,wj in enumerate(w)),0)
    for k in (0,1,2,3,4,9):
        lhs=sum(wj*sig**(j*k) for j,wj in enumerate(w))
        eig=((sig**k-sig)/(1-sig))**n
        assert_close(lhs,eig)

def report(x,y):
    E=p*p*(1+x)
    L=4*E*(1-E)
    b=p-p*p*y
    B=4*b*b*(1-b*b)
    A=L+(1-L)*B
    return 1-(1-zeta*A)*(1-zeta*B)

def entropy(r):
    return -(r*mp.log(r)+(1-r)*mp.log(1-r))/mp.log(phi)

r0=report(0,0)

def c(x,y):
    r=report(x,y)
    return (r-entropy(r))-(r0-entropy(r0))

a=mp.diff(lambda x:c(x,0),0)
b=mp.diff(lambda y:c(0,y),0)
assert a != 0 and b != 0

f0=mp.mpf("0.2")
q0=mp.mpf("-0.1")
rho0=mp.mpf("1.3")
df=mp.mpf("0.7")
dq=mp.mpf("-0.4")
drho=mp.mpf("0.15")
tau=mp.mpf("0.05")

def fields(Y):
    return (f0+df*Y,q0+dq*Y,rho0+drho*Y)

def S(t,Y):
    f,q,rho=fields(Y)
    return rho/t*c(t*f/rho,t*q/rho)

def DS_formula(t):
    f,q,rho=fields(0)
    x,y=t*f/rho,t*q/rho
    cx=mp.diff(lambda u:c(u,y),x)
    cy=mp.diff(lambda v:c(x,v),y)
    return cx*df+cy*dq+(c(x,y)-x*cx-y*cy)*drho/t

for t in (tau,sig*tau,sig**3*tau):
    assert_close(mp.diff(lambda Y:S(t,Y),0),DS_formula(t))

def projected(n,Y):
    return sum(
        mp.binomial(n,j)*(-sig)**(n-j)*S(sig**j*tau,Y)
        for j in range(n+1)
    )/(1-sig)**n

target=a*df+b*dq
errors = []
for n in range(11):
    e=mp.diff(lambda Y:projected(n,Y),0)-target
    errors.append(mp.nstr(e,19))
assert abs(mp.mpf(errors[1]))<abs(mp.mpf(errors[0]))
assert abs(mp.mpf(errors[10]))<abs(mp.mpf(errors[1]))

def positive_mix(F):
    def S_t(t):
        return c(t*F,0)/t
    return mp.mpf(".4")*S_t(tau)+mp.mpf(".6")*S_t(sig*tau)

mix_hessian=mp.diff(positive_mix, mp.mpf(".15"),2)
assert mix_hessian>0

print(json.dumps({
    "scope":"original Golden r/c only; no physical Book03 selector",
    "p":mp.nstr(p,25),
    "sigma":mp.nstr(sig,25),
    "two_scale_coefficients":[mp.nstr(phi,25),mp.nstr(-p,25)],
    "C1_contraction_gamma":mp.nstr(gamma,25),
    "total_abs_weights_n_is_5_to_n_over_2":True,
    "moving_rho_source_identity":"PASS",
    "signed_projector_errors_n0_to_10":errors,
    "positive_mix_second_f_derivative":mp.nstr(mix_hessian,19),
    "GR_closed":False
},indent=2))
