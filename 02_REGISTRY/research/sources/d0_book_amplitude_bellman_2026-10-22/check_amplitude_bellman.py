#!/usr/bin/env python3
"""Bounded 90-digit original Golden amplitude-Born (nu=2) / scalar-Born
(nu=1) Bellman source test. Mathematical orthogonal-record binding only:
no native physical Book03 admission, no complete HJR, no GR closure.
Requires mpmath; checks persist under python -O.
"""
import itertools
import json
import mpmath as mp
mp.mp.dps=90
checks=0

def verify(cond, msg):
    global checks
    if not cond:
        raise RuntimeError(msg)
    checks+=1

def equal(a,b,msg,tol=mp.mpf("1e-58")):
    verify(abs(a-b)<=tol*max(1,abs(a),abs(b)),msg)

p=(mp.sqrt(5)-1)/2
phi=1/p
ell=mp.log(phi)
sigma=p*p
tau=mp.mpf("0.05")
zeta=mp.mpf(2)**(-20)
equal(p+sigma,1,"exact golden code")

def h_bin(r):
    return -(r*mp.log(r)+(1-r)*mp.log(1-r))/ell

def native_r(x,y):
    E=sigma*(1+x)
    L=4*E*(1-E)
    b=p-sigma*y
    B=4*b*b*(1-b*b)
    A=L+(1-L)*B
    return 1-(1-zeta*A)*(1-zeta*B)

P=[sigma,p]
cost=[mp.mpf(1),mp.mpf(2)]
H=-(sum(P[b]*mp.log(P[b]) for b in (0,1)))/ell
C=sum(P[b]*cost[b] for b in (0,1))
equal(H,2-p,"original genuine Golden nonblank entropy")
equal(C,1+p,"original genuine Golden port cost")
nu_result={}
for nu in (mp.mpf(1), mp.mpf(2), mp.mpf(3)):
    g=(1+1/nu)*H-C
    I=[cost[b]+mp.log(P[b])/(nu*ell)+g for b in (0,1)]
    equal(sum(P[b]*I[b] for b in (0,1)),H,"expected vertex Shannon")
    equal(I[1]-I[0],1+1/nu,"exact scalar/amplitude info gap")
    Z=sum(mp.exp(-nu*ell*(cost[b]-I[b])) for b in (0,1))
    equal(Z,mp.exp(nu*ell*g),"unique Book absolute scalar")
    for b in (0,1):
        equal(mp.exp(-nu*ell*(cost[b]-I[b]))/Z,
              P[b],"single-tree Born nu reproduction")
    meanS=sum(P[b]*(cost[b]-I[b]) for b in (0,1))
    pressure=-mp.log(Z)/(nu*ell)
    equal(meanS,C-H,"mean action C-H for all nu")
    equal(meanS-pressure,H/nu,"pressure-to-mean exact entropy gap")
    N=5
    suffix_g=[mp.mpf(0),N*g]
    froot=g+sum(P[b]*suffix_g[b] for b in (0,1))
    Iroot=[cost[b]+mp.log(P[b])/(nu*ell)+froot-suffix_g[b]
           for b in (0,1)]
    equal(sum(P[b]*Iroot[b] for b in (0,1)),H,
          "future conditional root expected gain conserved")
    leaves=[(P[0],cost[0],Iroot[0])]
    for seq in itertools.product((0,1),repeat=N):
        prob=P[1]
        charge=cost[1]
        gain=Iroot[1]
        for b in seq:
            prob*=P[b]
            charge+=cost[b]
            gain+=I[b]
        leaves.append((prob,charge,gain))
    verify(len(leaves)==33,"complete future 33 leaves")
    equal(sum(x[0] for x in leaves),1,"complete future Born normalization")
    Ztree=sum(mp.exp(-nu*ell*(x[1]-x[2])) for x in leaves)
    equal(Ztree,mp.exp(nu*ell*froot),"complete future absolute Book normalization")
    for prob,charge,gain in leaves:
        equal(mp.exp(-nu*ell*(charge-gain))/Ztree,prob,
              "every complete future leaf original Born")
    Hwhole=-sum(x[0]*mp.log(x[0]) for x in leaves)/ell
    Cwhole=sum(x[0]*x[1] for x in leaves)
    Smean=sum(x[0]*(x[1]-x[2]) for x in leaves)
    equal(Smean,Cwhole-Hwhole,"full future mean source identity")
    equal(froot,(1+1/nu)*Hwhole-Cwhole,
          "full future potential entropy/cost identity")
    nu_result[str(int(nu))]={
        "f_root_one_step":mp.nstr(g,22),
        "I0":mp.nstr(I[0],22),
        "I1":mp.nstr(I[1],22),
        "one_step_pressure":mp.nstr(pressure,22)
    }

# Exact moving native two-operand click and all first jets.
for nu in (mp.mpf(1),mp.mpf(2),mp.mpf(3)):
    def run(x,y):
        r=native_r(x,y)
        h=h_bin(r)
        C=1+r
        f=(1+1/nu)*h-C
        i0=1+mp.log(1-r)/(nu*ell)+f
        i1=2+mp.log(r)/(nu*ell)+f
        w0=mp.exp(-nu*ell*(1-i0))
        w1=mp.exp(-nu*ell*(2-i1))
        return (r,h,C,f,i0,i1,w0,w1)
    r,h,C,f,i0,i1,w0,w1=run(0,0)
    Z=w0+w1
    equal(w1/Z,r,"original nonlinear Golden click Born")
    equal(w0/Z,1-r,"original nonlinear Golden no-click Born")
    equal((1-r)*i0+r*i1,h,"original click expected local gain")
    equal((1-r)*(1-i0)+r*(2-i1),C-h,
          "original click mean action for amplitude and scalar")
    for component in (0,1):
        def native_path(a):
            coords=(a,0) if component==0 else (0,a)
            return run(*coords)
        def delta(a):
            r,h,C,f,i0,i1,w0,w1=native_path(a)
            return ((1-r)*(1-i0)+r*(2-i1))-(C-h)
        def pressure_gap(a):
            r,h,C,f,i0,i1,w0,w1=native_path(a)
            return -mp.log(w0+w1)/(nu*ell)+h/nu-(C-h)
        equal(mp.diff(delta,0),0,"original two-native-operand full mean first source")
        equal(mp.diff(pressure_gap,0),0,"original Born pressure/mean C1")
    verify(mp.isfinite(f),"finite absolute Book amplitude normalizer")

# Actual native N1 rare click: amplitude interpretation still requires signed gain.
rare=native_r(0,0)
Hr=h_bin(rare)
fr=mp.mpf("1.5")*Hr-(1+rare)
I1rare=mp.mpf(2)+mp.log(rare)/(2*ell)+fr
verify(I1rare < -12,"original native rare N1 amplitude Info must be negative")
equal(mp.mpf("1.5")*H-(1+p), mp.mpf(2)-mp.mpf("2.5")*p,
      "original Golden exact 3/2 amplitude anchor")

# Previously published 128x128 ORIGINAL no-reset partial ledger inputs:
H128=mp.mpf("0.5701407300473663")
C128=mp.mpf("2.0260945042476832")
j128=mp.mpf("1.5")*H128-C128
Z128=mp.exp(2*ell*j128)
equal((C128-H128)-(-j128),H128/2,
      "original no-reset full128 input mean/pressure difference")

print(json.dumps({
    "status":"conditional orthogonal-amplitude-BORN + per-node GAIN; physical GR_closed=false",
    "checks_passed":checks,
    "nu_values":nu_result,
    "amplitude_info_gap":"3/2 exact",
    "original_rare_native_amplitude_I1":mp.nstr(I1rare,28),
    "full128_existing_input_amplitude_j":mp.nstr(j128,24),
    "full128_existing_input_amplitude_Z2":mp.nstr(Z128,24),
    "orthogonal_original_Book_history_physically_selected":False
},indent=2))
