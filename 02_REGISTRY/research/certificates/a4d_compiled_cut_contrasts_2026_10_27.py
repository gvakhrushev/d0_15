#!/usr/bin/env python3
"""All-column compilation -> whole cut price -> finite variational contrasts.

Scope: the stated endpoint cut-Hodge/feedback functional and the inherited
addressed/prepared Golden/CNOT compiler class. This is NOT a full D0 gate
admission proof, native runtime-heat identification, all42 solver, or CI.
No assert statements: normal and python -O have identical checks.
"""
from __future__ import annotations
import json
import sys
from fractions import Fraction
import mpmath as mp
import numpy as np
import sympy as sp

mp.mp.dps=90
checks=0

def require(ok, message):
    global checks
    checks+=1
    if not bool(ok):
        raise ArithmeticError(message)

def close(x,y,message,tol=mp.mpf('1e-65')):
    require(abs(x-y)<=tol*max(1,abs(x),abs(y)),message)

def matrix_close(X,Y,message,tol=mp.mpf('1e-65')):
    require(X.rows==Y.rows and X.cols==Y.cols,message+' shape')
    require(max(abs(X[i,j]-Y[i,j]) for i in range(X.rows) for j in range(X.cols))<=tol,message)

def zero_exact(X,message):
    require(all(sp.cancel(x)==0 for x in X),message)

def opnorm(X):
    ev=mp.eigsy(X.T*X,eigvals_only=True)
    return mp.sqrt(max(mp.mpf(0),max(ev)))

def rotation(dim,i,j,angle):
    R=mp.eye(dim);c,s=mp.cos(angle),mp.sin(angle)
    R[i,i]=R[j,j]=c;R[j,i]=s;R[i,j]=-s
    return R

# Exact finite algebra: C maps P to Q, hence C^2=0 and paired nonzero spectra.
t=sp.Rational(3,5);u=sp.Rational(4,5)
U=sp.Matrix([[t,-u],[u,t]])
P=sp.diag(1,0);C=(sp.eye(2)-P)*U*P
zero_exact(C*C, 'literal cut differential is square zero')
F=C.T*C;D=C.T*C+C*C.T
zero_exact(F-sp.diag(u*u,0),'return on the actual retained cut')
zero_exact(D-u*u*sp.eye(2),'both cut heat eigenvalues retained')
J=sp.zeros(4,2);J[0,0]=J[1,1]=1
P4=J*P*J.T
U4=sp.diag(U,sp.Matrix([[0,-1],[1,0]]))
C4=(sp.eye(4)-P4)*U4*P4
zero_exact(C4-J*C*J.T,'spectator/complement all-column action is irrelevant only to this cut')
D4=C4.T*C4+C4*C4.T
zero_exact(D4-J*D*J.T,'padding adds actual harmonic heat modes, not deletions')
require(D4.eigenvals()=={u*u:2,sp.Integer(0):2},'two added harmonic modes')

# A genuinely moving prepared cut is transported, NOT frozen.
xi=sp.symbols('xi',real=True)
Aprep=sp.Matrix([[1-xi*xi,-2*xi],[2*xi,1-xi*xi]])/(1+xi*xi)
Pmove=Aprep*P*Aprep.T
Ufixed=sp.diag(1,-1)
Cm=(sp.eye(2)-Pmove)*Ufixed*Pmove
Utransport=Aprep.T*Ufixed*Aprep
Ct=(sp.eye(2)-P)*Utransport*P
zero_exact(Ct-Aprep.T*Cm*Aprep,'whole prepared-cut differential transported exactly')
zero_exact(Ct.T*Ct-Aprep.T*(Cm.T*Cm)*Aprep,'all return eigenvalues preserve the moving cut')
source_m=sp.diff(sp.trace(Cm.T*Cm),xi).subs(xi,sp.Rational(1,2))
source_t=sp.diff(sp.trace(Ct.T*Ct),xi).subs(xi,sp.Rational(1,2))
require(sp.cancel(source_m-source_t)==0 and source_m!=0,'moving-cut source survives preparation transport')
require((sp.eye(2)-P)*Ufixed*P==sp.zeros(2),'freezing the active cut would delete the real source')

# Negative control: matching ONE occupied input does not control the rank-2 cut.
Pbad=sp.diag(1,1,0,0);Ub=sp.eye(4)
Vb=sp.Matrix([[1,0,0,0],[0,t,0,-u],[0,0,1,0],[0,u,0,t]])
require(Ub[:,0]==Vb[:,0],'hostile matrices match the one prepared blank')
Cb=(sp.eye(4)-Pbad)*Vb*Pbad
require(sp.trace(Cb.T*Cb)>0,'blank-only equality does not preserve full feedback')

# Literal Golden word on its original active two-dimensional factor.
p=(mp.sqrt(5)-1)/2
G=mp.matrix([[mp.sqrt(p),-p],[p,mp.sqrt(p)]])
close(p+p*p,1,'native Golden identity')
matrix_close(G.T*G,mp.eye(2),'native G is orthogonal')
alpha=mp.atan(mp.mpf(3)/4) # exact target matrix entries 4/5,3/5.
theta=mp.atan2(p,mp.sqrt(p))
# Deterministic search; integer m becomes the recorded finite programme.
angles=np.arange(1,4097,dtype=float)*float(theta)-float(alpha)
chord=2*np.abs(np.sin(angles/2))
m=int(np.argmin(chord))+1
Vm=mp.eye(2)
for _ in range(m):
    Vm=G*Vm
Ut=mp.matrix([[mp.mpf(4)/5,-mp.mpf(3)/5],[mp.mpf(3)/5,mp.mpf(4)/5]])
delta_native=opnorm(Vm-Ut)
require(delta_native<mp.mpf('0.003'),'executed forward Golden word approximates exact rational target')
# Two real CNOTs conjugate the target; spectator is retained on all 8 columns.
def kron(A,B):
    out=mp.zeros(A.rows*B.rows,A.cols*B.cols)
    for i in range(out.rows):
        for j in range(out.cols):out[i,j]=A[i//B.rows,j//B.cols]*B[i%B.rows,j%B.cols]
    return out
CX=mp.zeros(8)
for b in range(8):
    target=b ^ (2 if b&4 else 0)
    CX[target,b]=1
U8=CX*kron(Ut,mp.eye(4))*CX
V8=CX*kron(Vm,mp.eye(4))*CX
P8=mp.diag([1,1,1,1,0,0,0,0])
matrix_close(V8.T*V8,mp.eye(8),'literal native word all eight columns orthogonal')
close(opnorm(V8-U8),delta_native,'CNOT conjugacy and retained spectator keep complete norm error')
C0=(mp.eye(8)-P8)*U8*P8
C1=(mp.eye(8)-P8)*V8*P8
F0,F1=C0.T*C0,C1.T*C1
D0,D1=F0+C0*C0.T,F1+C1*C1.T
require(opnorm(C1-C0)<=delta_native*(1+mp.mpf('1e-60')),'all-column cut error <= delta')
require(opnorm(F1-F0)<=2*delta_native,'feedback error <= 2 delta')
require(opnorm(D1-D0)<=2*delta_native,'orthogonal paired blocks: entire heat error <= 2 delta')

def whole_cut_price(C,beta,z,padding=0,spectator=1):
    F=C.T*C;D=F+C*C.T
    ef=mp.eigsy(F,eigvals_only=True);ed=mp.eigsy(D,eigvals_only=True)
    Z=mp.mpf(padding)+sum(mp.exp(-beta*d) for d in ed)
    return mp.log(spectator*Z)/beta-spectator*sum(mp.log1p(-z*f) for f in ef)

btest=mp.mpf(3)/4;ztest=mp.mpf(1)/16
Ltest=2+2*4*ztest/(1-ztest)
price0=whole_cut_price(C0,btest,ztest)
price1=whole_cut_price(C1,btest,ztest)
require(abs(price1-price0)<=Ltest*delta_native,'literal native word: full heat-plus-feedback price bound')

# General ancillary leakage: no reset and no replacement by a reduced channel.
leak_controls=[]
for angle in (mp.mpf(1)/10,mp.mpf(1)/100,mp.mpf(1)/1000):
    T=mp.eye(4);T[0,0]=T[1,1]=mp.mpf(3)/5;T[0,1]=-mp.mpf(4)/5;T[1,0]=mp.mpf(4)/5
    # J keeps both logical columns; the actual output leaks into a new record.
    V=rotation(4,0,2,angle)*T
    JJ=mp.zeros(4,2);JJ[0,0]=JJ[1,1]=1
    PP=mp.diag([1,0,0,0])
    logical=mp.matrix([[mp.mpf(3)/5,-mp.mpf(4)/5],[mp.mpf(4)/5,mp.mpf(3)/5]])
    d=opnorm(V*JJ-JJ*logical)
    CC=(mp.eye(4)-PP)*V*PP
    TT=(mp.eye(4)-PP)*T*PP
    L=2+2*ztest/(1-ztest)
    error=abs(whole_cut_price(CC,btest,ztest)-whole_cut_price(TT,btest,ztest))
    require(opnorm(CC-TT)<=d*(1+mp.mpf('1e-60')),'leaking compiled isometry: whole cut estimate')
    require(0<error<=L*d,'retained leakage: nonzero full price change with all harmonic modes')
    leak_controls.append({'angle':mp.nstr(angle,8),'all_column_error':mp.nstr(d,30),'price_error':mp.nstr(error,30),'certified_upper':mp.nstr(L*d,30)})

# The actual original full-cut probability price with the REAL large baseline.
z=mp.mpf(2)**-20;beta=2*p*p;sR=128
M,W=72441,50549
ready=2*10946*p**23

def report(x,y):
    ee=p*p*(1+x);uu=p+p*p*y
    ell=4*ee*(1-ee);bb=4*uu*uu*(1-uu*uu)
    aa=ell+(1-ell)*bb
    return 1-(1-z*bb)*(1-z*aa)

def qs(r):return [1-ready,ready*(1-r),ready*r]
def ff(q):return 4*q*(1-q)
def price(r,extra=0):
    q=qs(r)
    ZZ=mp.mpf(M*W+extra-6)+2*sum(mp.exp(-beta*ff(v)) for v in q)
    return mp.log(sR*ZZ)/beta-sR*sum(mp.log1p(-z*ff(v)) for v in q)
def price_derivative(r,extra=0):
    return mp.diff(lambda rr:price(rr,extra),r)

r0=report(0,0);rf=mp.diff(lambda x:report(x,0),0);rq=mp.diff(lambda y:report(0,y),0)
lam=-rq/rf
eta_rat=Fraction(13,5)/(64*Fraction(1,2**20)*(1-Fraction(1,2**19))*M*(W-2))
require(eta_rat<Fraction(1,80000),'real large-carrier thermal bound')
# Uniform padding cannot silently be called a constant PRICE; it preserves
# the stationary set here because both complete prices are monotone in r.
pad_controls=[]
for extra in (0,1,10**5,10**12):
    k=price_derivative(r0,extra)
    require(k>0,'whole price keeps positive gain with actual added harmonic modes')
    q=qs(r0)
    # Direct matrix model has 6 dimensions; all extra modes counted analytically.
    R=mp.zeros(6)
    for j,qj in enumerate(q):
        tij=1-2*qj;sij=2*mp.sqrt(qj*(1-qj))
        R[2*j,2*j]=tij;R[2*j+1,2*j+1]=-tij
        R[2*j,2*j+1]=R[2*j+1,2*j]=sij
    P6=mp.diag([1,0,1,0,1,0]);C=(mp.eye(6)-P6)*R*P6
    direct=whole_cut_price(C,beta,z,padding=M*W+extra-6,spectator=sR)
    close(direct,price(r0,extra),'entire large-carrier scalar price matches retained matrix spectrum')
    pad_controls.append({'extra_harmonic_modes_per_RIGHT':extra,'kappa':mp.nstr(k,35)})

# Finite contrasts: SAME nonlinear original report, unequal site probabilities,
# non-null individual f and q, with a known saddle of the limiting scalar.
rhos=list(map(mp.mpf,['0.5','0.75','1.25','1.5']))
fc=[mp.mpf(1)/7,-mp.mpf(2)/9,mp.mpf(1)/4,mp.mpf(2)/11]
qc=[mp.mpf(1)/13,-mp.mpf(1)/17,mp.mpf(2)/19,mp.mpf(1)/23]
a=[mp.mpf(1),-mp.mpf(1),mp.mpf(2),-mp.mpf(2)]
b=[mp.mpf(3),-mp.mpf(2),-mp.mpf(3),mp.mpf(2)]
close(sum(rhos)/4,1,'unequal full site law normalized')

def rbar(eps,u,v):
    return sum(rho*report(eps*(f0+ai*u+(u*u-v*v)/2)/rho,
                          -eps*(q0+bi*v)/rho)
               for rho,f0,q0,ai,bi in zip(rhos,fc,qc,a,b))/4

contrast_controls=[]
for hden in (8,16,32,64):
    h=mp.mpf(1)/hden;eps=h*h/64;step=h*h
    kappa=price_derivative(r0);gain=kappa*eps*rf
    # q states are from the supplied candidate; not an asserted all42 geometry.
    def PP(u,v):return price(rbar(eps,u,v))
    cx=(PP(step,0)-PP(-step,0))/(2*step*gain)
    cy=(PP(0,step)-PP(0,-step))/(2*step*gain)
    # exact reference I has zero derivative at (0,0), a genuine saddle.
    kappa_tol=p**(hden//8+2)
    require(max(abs(cx),abs(cy))<=kappa_tol/4,'non-null finite contrasts meet the stated Golden test tolerance')
    rank=3*sR
    Lprice=2+2*rank*z/(1-z)
    delta_budget=gain*step*kappa_tol/(4*Lprice)
    # Worst admissible signs on the independently compiled price values.
    compiler_contrast_error=2*Lprice*delta_budget/(2*step*gain)
    close(compiler_contrast_error,kappa_tol/4,'gain-aware compiler precision yields finite-source budget')
    require(delta_budget>0,'every finite precision requirement is finite and positive')
    contrast_controls.append({'h':'1/'+str(hden),'eps':mp.nstr(eps,20),
        'source_contrasts':[mp.nstr(cx,32),mp.nstr(cy,32)],
        'norm_over_eps':mp.nstr(max(abs(cx),abs(cy))/eps,25),
        'gain':mp.nstr(gain,25),'step':mp.nstr(step,20),
        'kappa_tolerance':mp.nstr(kappa_tol,20),'whole_word_compiler_budget':mp.nstr(delta_budget,25)})

# Hostile controls: convergence of values or words alone is not SOURCE fidelity.
x,dh=sp.symbols('x dh',real=True,positive=True)
require(sp.diff(dh*sp.sin(x/dh**2),x).subs(x,0)==1/dh,
        'uniformly small value error can have unbounded first source')
# The prior exact-root distinction is retained, not erased by kappa wording.
require(sp.diff(x**3/3+dh*x,x)==x*x+dh,
        'approximate stationary records do not imply exact finite roots')
# Explicit scalar source-test schedule with positive margins, no fitted force.
for k in range(1,9):
    tol=p**k;C,H=mp.mpf(7),mp.mpf(5)
    mesh=tol/(4*C);step=tol/(2*H)
    gamma=mesh**4;L=mp.mpf(6)
    delta=gamma*step*tol/(4*L)
    error=C*mesh+H*step/2+L*delta/(gamma*step)
    close(error,3*tol/4,'fully explicit finite-test recovery error budget')

out={
 'status':'PASS_COMPILED_CUT_PRICE_AND_FINITE_SOURCE_CONTROLS',
 'checks':checks,'python':sys.version.split()[0],'sympy':sp.__version__,
 'precision_digits':mp.mp.dps,
 'source_head':'c7708742bea04684ffd6aed16774cfdf1b94b129',
 'executed_literal_native_control':{'forward_G_count':m,'CNOT_count':2,
   'complete_operator_dimension':8,'all_column_error':mp.nstr(delta_native,35),
   'whole_cut_price_error':mp.nstr(abs(price1-price0),35),
   'whole_price_upper_bound':mp.nstr(Ltest*delta_native,35),
   'scope':'Original G power plus two exact CNOTs; NOT the large GR programme'},
 'ancillary_leakage_controls':leak_controls,
 'full_padding_controls':pad_controls,
 'finite_nonnull_source_contrasts':contrast_controls,
 'full_NATIVE_GR_programme_compiled':False,
 'Book03_cut_price_selected_from_M1':False,
 'general_exact_lattice_roots_proved':False,
 'raw216_closed':False,'unconditional_GR_closed':False
}
print(json.dumps(out,indent=2,ensure_ascii=False))
