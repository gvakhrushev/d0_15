"""Exact raw-head jets, reference calibration and a physical torus adjoint test."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
import sys

import numpy as np

sys.dont_write_bytecode = True
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'round84'/'prepare'))
import check_curvature_variance as old
G,one,p,z,rf,rq,phi,b = old.G,old.o,old.p,old.z,old.rf,old.rq,old.phi,old.b
zero=G()
check=old.check


def convolution(x,y):
    result=[zero for _ in range(len(x)+len(y)-1)]
    for i,a in enumerate(x):
        for j,beta in enumerate(y):
            result[i+j]+=a*beta
    return result


def scaled(x,s):
    return [a*s for a in x]


def add(x,y):
    return [a+b for a,b in zip(x+[zero]*max(0,len(y)-len(x)),
                               y+[zero]*max(0,len(x)-len(y)))]


def pure_matter_coefficients():
    u2=convolution([p,p*p],[p,p*p])
    B=scaled(convolution(u2,add([one],scaled(u2,G(-1)))),G(4))
    A=add([old.L0],scaled(B,one-old.L0))
    result=add(scaled(add(A,B),z),scaled(convolution(A,B),G(-1)*z*z))
    check(len(result)==9 and result[0]==old.r0 and result[1]==rq,'SC1 full degree')
    return result


cs=pure_matter_coefficients()
mom=[sum(comb(8,j)*j**k for j in range(1,9)) for k in range(8)]
check(mom[:2]==[255,1024], 'positive selector moments')


def a_ref(epsilon):
    return old.report(zero,b*epsilon)-old.report(zero,zero-b*epsilon)


def parseval():
    h=G(F(1,32768)); X=G(F(2,39)); M=G(F(-9,20))
    from_heads=zero; from_signed=zero
    for j in range(1,9):
        ep=G(j)*h
        raw=(a_ref(ep)*(old.report(ep*X,zero)-old.r0)
             +G(2)*rq*b*ep*(old.report(zero,zero-ep*M)-old.r0))
        w=G(F(comb(8,j),j*j))
        from_heads+=w*raw
        from_signed+=G((-1)**(j-1))*w*raw
    result=zero
    for k in range(8):
        even=k-k%2
        coeff=cs[even+1]*b**even*old.inv(rq)
        geometric=coeff*(X if k%2==0 else G(-1)*phi*X*X)
        matter=cs[k+1]*old.inv(rf)*(G(-1)*M)**(k+1)
        result+=G(mom[k])*h**k*(geometric+matter)
    norm=G(2)*b*rf*rq*h*h
    check(result*norm==from_heads and from_signed==norm*(X-old.k0*M),'exact complete price and exact signed projection')


def odd_matter(arg):
    return sum((G(2)*cs[j]*(arg**j) for j in (1,3,5,7)),zero)


def reference_checks():
    # The root itself is an algebraic number; use exact ordered-field brackets,
    # never substitute a numerical root for exact equality.
    h=G(F(1,32768))
    relative=G(F(1,10**12)); gates=[]
    for j in range(1,9):
        ep=G(j)*h; d=b*ep; left=d*(one-relative); right=d*(one+relative)
        check(old.sign(G(2)*rq*d-odd_matter(left))>0 and
              old.sign(odd_matter(right)-G(2)*rq*d)>0, 'positive calibrated matter amplitude bracket')
        check(old.sign(odd_matter(d)-G(2)*rq*d)<0, 'raw36 uncorrected finite mismatch at the original angle')
        gates.append(odd_matter(d))
    # On the 24-selector with native apparent material multiplication a, all
    # raw heads have the same physical gradient direction on local F=M=0.
    a24=gates[0]*old.inv(G(2)*rq*b*h)
    for j in range(1,9):
        ep=G(j)*h
        check(gates[0]*rf*ep==G(2)*rq*b*h*rq*ep*a24*old.inv(old.k0),
              'fixed reference 24 makes the exact null jet collinear')
    # On the adjusted 36 family the defining equation makes the polynomial in
    # epsilon degree <=9. Test on real non-null field moments, all eight terms.
    X=G(F(7,23)); M=G(F(5,17))
    from_heads=zero
    for j in range(1,9):
        ep=G(j)*h
        raw=G(2)*rq*b*ep*(old.report(ep*X,zero)+old.report(zero,G(-1)*ep*M)-G(2)*old.r0)
        from_heads+=G(F((-1)**(j-1)*comb(8,j),j*j))*raw
    check(from_heads==G(2)*b*rf*rq*h*h*(X-old.k0*M),'calibrated36 still recovers full polynomial on non-null fields')


def real(a):
    return float(old.display(a))


def physical_adjoint(L, trace=False):
    # An actual four-torus invariant in three coordinates, U1=exp(H*k(x0)*K01).
    # The other three proper links are I. The full trace equals the formula
    # checked separately on CAR16. Both physical matter components vary.
    H=1/L; t=np.arange(L)*2*np.pi/L
    k=.07*np.sin(t); s=5+.15*np.cos(t); rho=1+.12*np.sin(t)
    psi=np.array([.035*np.sin(t),.02*np.cos(2*t)])
    def jet(fields):
        link,scale,density,values=fields
        slope=(np.roll(values,-1,axis=1)-values)/H
        face=H*(np.roll(link,-1)-link)
        X=-np.sinh(face)/(H*H*density*scale**2)
        M=np.sum(slope*slope,axis=0)/(density*scale**2)
        h=H*H/512
        P=np.zeros(L); px=np.zeros(L); pm=np.zeros(L)
        for m in range(1,8):
            n=m-m%2
            D=real(cs[n+1]*b**n*old.inv(rq))
            cm=real(cs[m+1]*old.inv(rf))
            factor=mom[m]*(h**(m-1))
            sign=(-1)**(m+1)
            geom=D*X if n==m else -real(phi)*D*X*X
            dg=D if n==m else -2*real(phi)*D*X
            P+=factor*(geom+cm*sign*M**(m+1))
            px+=factor*dg
            pm+=factor*cm*(m+1)*sign*M**m
        gx=px*np.cosh(face)/scale**2
        gk=(gx-np.roll(gx,1))/H
        gs=-2*density*(px*X+pm*M)/scale
        gr=P-px*X-pm*M
        gpsi=pm[None,:]*slope/scale[None,:]**2
        gpsi=2*(np.roll(gpsi,1,axis=1)-gpsi)/H
        return np.mean(density*P),(gk,gs,gr,gpsi)
    fields=(k,s,rho,psi); P,grad=jet(fields)
    dirs=(np.cos(t)+.1*(-1.)**np.arange(L),np.sin(t),np.cos(3*t),
          np.array([np.sin(t),np.cos(t)+.2*(-1.)**np.arange(L)]))
    delta=2e-7
    forward=jet(tuple(x+delta*d for x,d in zip(fields,dirs)))[0]
    backward=jet(tuple(x-delta*d for x,d in zip(fields,dirs)))[0]
    observed=(forward-backward)/(2*delta)
    pred=sum(np.sum(g*d)/L for g,d in zip(grad,dirs))
    check(abs(pred-observed)<1e-5*(1+abs(pred)), 'adjoint versus physical perturbation')
    return float(np.sqrt(sum(np.sum(g*g)/L for g in grad)))


def check_trace():
    from check_smooth_twofield_reference import fock_trace
    from check_shared_site_union import eye
    v=F(1,20); ca=(1+v*v)/(1-v*v); sa=2*v/(1-v*v)
    P=eye(4); P[0][0]=P[1][1]=ca; P[0][1]=P[1][0]=sa
    N=[[F(0)]*4 for _ in range(4)]; N[0][1]=N[1][0]=F(1)
    check(-fock_trace(N,P)/8==-sa,'actual oriented full CAR16 plaquette, all grades')


if __name__=='__main__':
    parseval(); reference_checks(); check_trace()
    l2={L:round(physical_adjoint(L),10) for L in (8,16,32,64,128)}
    print(json.dumps({'source':old.PIN,'positive_moments':mom,
          'both_field_axes_and_signed_selector_exact':True,
          'original24_zero_invariant_null_jet_exact':True,
          'alternative36_exact_inverse_reference_relative_bracket':'1e-12 at H=1/4,h=1/32768',
          'complete_CAR_face_exact':True,'raw_normalized_error_over_h_physical_dual_L2_fixture':l2,
          'all_compiled_instrument_and_physical_total_price':False},indent=2))
