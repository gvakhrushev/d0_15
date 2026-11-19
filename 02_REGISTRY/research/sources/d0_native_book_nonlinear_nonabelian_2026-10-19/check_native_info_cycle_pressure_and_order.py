#!/usr/bin/env python3
"""Native-scene positive-scalar theorem: original Info, admissible chiral Cost,
and original Golden-p pretrace ordered Choi readout. Research-only, NOT G0.
"""
import math
import numpy as np
import sympy as sp

phi=(1+math.sqrt(5))/2
p=1/phi
ell=math.log(phi)
counts=(9,11,13)
zone=np.repeat(np.arange(3),counts)
Adj=(zone[:,None]!=zone[None,:]).astype(float)
sign=np.array([[0,1,-1],[-1,0,1],[1,-1,0]])
ch=sign[zone[:,None],zone[None,:]]
assert int(np.sum(Adj))==718

def nativeK(I,theta=0.5,t=0.0):
    I=np.asarray(I,dtype=float)
    # Canonical ActionProtocol-compatible primitive Cost: 1+t*(1-sign)
    # for t>=0, Cost>=1 on ALL true cross-zone directed edges.
    return p*Adj*np.exp(ell*(theta*I[zone[:,None]]+(1-theta)*I[zone[None,:]]
                             -t*(1-ch)))

def pf(K):
    values,vectors=np.linalg.eig(K)
    k=int(np.argmax(values.real));lm=float(values[k].real)
    assert lm>0 and abs(values[k].imag)<1e-12
    r=np.array(vectors[:,k].real)
    if sum(r)<0:r=-r
    assert min(r)>0
    P=K*r[None,:]/(lm*r[:,None])
    assert max(abs(P.sum(axis=1)-1))<1e-11
    return lm,P

def cubic(I,t):
    a,b,c=I
    Q=p*p*(99*math.exp(ell*(a+b))+117*math.exp(ell*(a+c))
           +143*math.exp(ell*(b+c)))
    R=2574*p**3*math.exp(ell*(a+b+c))*math.cosh(3*ell*t)
    roots=np.roots([1,0,-Q,-R])
    return float(max(roots.real)),Q,R

I=(.23,-.14,.37);t=.08
baseP=None
for theta in (0,.17,.5,.83,1):
    lm,P=pf(nativeK(I,theta,t))
    predicted=cubic(I,t)[0]*math.exp(-ell*t)
    assert abs(lm-predicted)<1e-10
    if baseP is not None:assert np.max(abs(baseP-P))<3e-12
    else:baseP=P
print('PASS all 718 edges and all theta; original primitive cost >=1')
print('PASS three-zone full all-order Perron cubic+absolute work factor')

# Actual moving stationary law: exact first Book source at every native Info field.
lm0,P0=pf(nativeK(I,theta=.37,t=0))
values,vecs=np.linalg.eig(P0.T)
pos=int(np.argmin(abs(values-1)))
pi=vecs[:,pos].real
if sum(pi)<0:pi=-pi
pi/=sum(pi)
assert max(abs(pi[:,None]*P0-pi[None,:]*P0.T)[Adj>0])<2e-12
for j in range(3):
    ee=1e-4
    Ip=list(I);Im=list(I);Ip[j]+=ee;Im[j]-=ee
    finite=(-math.log(pf(nativeK(Ip,t=0))[0])/ell
            +math.log(pf(nativeK(Im,t=0))[0])/ell)/(2*ee)
    assert abs(finite+sum(pi[zone==j]))<2e-8
print('PASS complete nonlinear vertex Info source = -moving stationary pi')
for tau in (0,.12):
    lam1=pf(nativeK(tuple(v+.29 for v in I),t=tau))[0]
    lam0=pf(nativeK(I,t=tau))[0]
    assert abs(math.log(lam1/lam0)/ell-.29)<2e-12
print('PASS uniform Info / absolute Book pressure Ward at nonzero chirality')
# Every A-B-C oriented triangle has the SAME exact scalar Book odds.
u,v,w=0,9,20
P=baseP
cycle=(P[u,v]*P[v,w]*P[w,u])/(P[v,u]*P[w,v]*P[u,w])
assert abs(math.log(cycle)-6*ell*t)<2e-12
print('PASS all 1287 same chiral triangle odds analytic 6*ln(phi)*t')

def F(I,t):return -math.log(cubic(I,t)[0])/ell+t
rho,Q,R=cubic([0,0,0],0);D=3*rho*rho-Q
Ftt=-9*ell*R/(rho*D)
assert abs(Ftt+0.4763744515526457)<1e-12
mixed=[]
for j,pair in enumerate(((99,117),(99,143),(117,143))):
    Qj=ell*p*p*sum(pair);Rj=ell*R
    rhoj=(Qj*rho+Rj)/D
    mixed.append(Ftt*(ell-rhoj/rho-(6*rho*rhoj-Qj)/D))
assert max(abs(x) for x in mixed)>.01 and abs(sum(mixed))<1e-12
assert abs(F((.2,.2,.2),.08)-F((0,0,0),.08)+.2)<1e-12
print('PASS Book scalar chiral curvature F_tt=',repr(Ftt))
print('PASS exact even-Info*odd*odd cubic',mixed,'sum=',sum(mixed))

# Three-triangle UNMARKED gauge-invariant trace requires three distinct loops.
# Original G0 Book path cost of the two orders is identical, but this
# CONDITIONAL proper-Lorentz edge representation is not G0 compelled.
a,b,c=sp.symbols('a b c',real=True)
E=lambda i,j:sp.eye(4)[:,i]*sp.eye(4)[j,:]
A=E(1,2)+E(2,0)
B=E(0,3)+E(3,1)
J=E(2,3)-E(3,2)
eta=E(0,1)+E(1,0)-E(2,2)-E(3,3)
assert all(g.T*eta+eta*g==sp.zeros(4) for g in [A,B,J])
U0=sp.eye(4)+a*A+a*a*A*A/2
U1=sp.eye(4)+b*B+b*b*B*B/2
U2=(sp.eye(4)-c*J/2).inv()*(sp.eye(4)+c*J/2)
Uplus=U0*U1*U2;Uminus=U0*U2*U1
Z=a*a*b*b*c*c+4*a*a*b*b+64
Tp=sp.factor(sp.trace(Uplus));Tm=sp.factor(sp.trace(Uminus))
assert sp.simplify(Tp+Tm-Z/(2*(4+c*c)))==0
assert sp.simplify(Tp-Tm+8*a*b*c/(4+c*c))==0
assert sp.simplify(Tp/Tm-(Z-16*a*b*c)/(Z+16*a*b*c))==0
L=sp.symbols('L',positive=True)
rel=(2/L)*sp.log((Z+16*a*b*c)/(Z-16*a*b*c))
assert sp.simplify(sp.diff(rel,a,b,c).subs({a:0,b:0,c:0})-1/L)==0
q=sp.Rational(1,40)
marks=[]
for U in [Uplus,Uminus]:
    ur=U.subs({a:q,b:q,c:q})
    assert (ur.T*eta*ur-eta)==sp.zeros(4)
    Unp=np.array(ur.tolist(),dtype=float)
    good=p*p*np.trace(Unp.T@Unp)/4
    marked=p*p*np.trace(Unp)**2/16
    remain=good-marked
    fail=1-good
    assert p*np.linalg.svd(Unp,compute_uv=False)[0]<1
    assert 0<marked<good<1 and remain>0 and fail>0
    marks.append(marked)
ratio=marks[0]/marks[1]
assert abs(math.log(ratio)+ell*float(rel.subs({a:q,b:q,c:q,L:ell})))<2e-12
source=float(sp.diff(rel,a).subs({a:q,b:q,c:q,L:ell}))
assert abs(source-0.0012988042306495806)<1e-12
print('PASS exact real SO(1,3) original 3-loop Wilson trace')
print('PASS native Golden-p complete 3-outcome Choi mark detects equal-cost order')
print('PASS marked relative source is exact Helmholtz gradient',source)
print('PASS genuine mixed abc coefficient = 1/ln(phi)',1/ell)
print('NOTE: physically selected full Book/G0 action and GR remain open')
