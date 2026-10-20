#!/usr/bin/env python3
"""Bounded numerical controls of an analytically exact native horizon theorem."""
from math import ceil, cos, exp, log, log1p, pi, sin, sqrt
import json
import numpy as np

count=0
def check(v,msg):
    global count
    if not v: raise AssertionError(msg)
    count+=1

p=(sqrt(5)-1)/2
def native_data(h,a,b):
    x,y=h*a,h*b
    d=(x-y)**2
    f=d*(1+x*y/(1-x*y+sqrt((1-x*x)*(1-y*y))))
    w=4*sin(pi*h)**2
    eta=p*p*w*f/128
    return log1p(-eta),w,f

def risk(logc,n):
    return (1-sqrt(1-exp(2*n*logc)))/2

# The exact native scalar cross gives the all-input 2-subspace normal form.
# Test mixed, pure and entangled DATA/oldRIGHT fixtures without requiring a
# pure preparation. The analytic proof, not this fixture, owns all rho.
v=np.array([1,0,0,1],dtype=complex)/sqrt(2)
rhos=[np.outer(v,v.conj()),np.eye(4)/4,
      np.array([[.4,.1j,0,0],[-.1j,.2,0,0],[0,0,.3,.05],[0,0,.05,.1]])]
for rho in rhos:
    check(abs(np.trace(rho)-1)<1e-14,'same normalized full input')
    check(np.linalg.eigvalsh(rho).min()>-1e-14,'positive full input')
    for s in [0.2,0.6,0.9]:
        v0=np.array([1.,0.]); vs=np.array([s,sqrt(1-s*s)])
        A=np.outer(v0,v0); B=np.outer(vs,vs)
        D=A-B
        vals,vecs=np.linalg.eigh(D)
        P=vecs[:,vals>0]@vecs[:,vals>0].T
        e0=float(np.trace((np.eye(2)-P)@A))
        e1=float(np.trace(P@B))
        expected=(1-sqrt(1-s*s))/2
        full=np.kron(D,rho)
        norm=float(np.abs(np.linalg.eigvalsh(full)).sum())
        check(abs(norm-2*sqrt(1-s*s))<5e-14,'all-input trace norm')
        check(abs(e0-expected)<2e-14 and abs(e1-expected)<2e-14,
              'one measurement equalizes both conditional errors')

rows=[]
a,b=1/3,2/3
for delta in [.1,.01]:
    target=log(4*delta*(1-delta))
    coeff=-16*target/(p*p*pi*pi*(a-b)**2)
    excess=-p*(a*a+b*b)*target/(2*(a-b)**2)
    for L in [4,8,16,32,64]:
        h=1/L
        logc,w,f=native_data(h,a,b)
        x,y=h*a,h*b
        direct=x*x+y*y-x*y*(1+x*y+sqrt(1-x*x)*sqrt(1-y*y))
        check(abs(f-direct)<1e-17,'stable formula equals original native cross')
        n=ceil(target/(2*logc))
        check(2*n*logc<=target and 2*(n-1)*logc>target,
              'ceil horizon is sufficient and one less is impossible')
        check(risk(logc,n)<=delta+2e-16,'declared complete-record risk')
        port_extra=n*p*(p*p*h*h/64)*w*(a*a+b*b)/2
        check(port_extra>0,'every extra native return remains paid')
        err=abs(h**4*n/coeff-1)
        check(err<10*h*h,'sharp horizon coefficient with bounded finite-h remainder')
        if L==64:
            check(abs(port_extra/excess-1)<0.001,'finite retained port excess limit')
        rows.append({'L':L,'delta':delta,'n_min':n,
                     'h4_n':h**4*n,'limit':coeff,'port_excess':port_extra})

check(native_data(1/8,a,a)[0]==0,'identical hypotheses have no information')
check(risk(native_data(1/8,a,b)[0],0)==.5,'idle fails every nontrivial task')
print(json.dumps({'status':'PASS','checks':count,'fixtures':rows,
 'scope':'Fixed-horizon same-instrument coherent binary task; mathematical optimal readout; actual all-launch port cost only.',
 'native_task_forced':False,'full_Cost_Info_selected':False,'GR_closed':False},indent=2))
