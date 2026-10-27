#!/usr/bin/env python3
"""Exact coframe-density identities and finite full-price source controls.
Not a native primitive compilation, full lattice root, Lean or GR acceptance.
"""
from __future__ import annotations
import json
import sympy as s
import mpmath as mp

mp.mp.dps = 100
checks=0

def require(ok, msg):
    global checks
    checks += 1
    if not bool(ok):
        raise ArithmeticError(msg)

def matzero(M, msg):
    require(all(s.cancel(v)==0 for v in M), msg)

def close(a,b,msg,tol=mp.mpf('1e-70')):
    require(abs(a-b)<=tol*max(1,abs(a),abs(b)),msg)

eta=s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
# A genuinely non-unimodular full coframe; rational square determinant.
e=s.Matrix([[2,s.Rational(1,3),0,s.Rational(1,5)],
            [0,1,s.Rational(1,7),0],
            [0,0,1,s.Rational(1,4)],[0,0,0,2]])
E=e.det(); require(E==4,'non-unimodular determinant')
et=e/s.sqrt(E)
require(et.det()==1/E,'determinant is inverted')
matzero(et/s.sqrt(et.det())-e,'coframe transformation is an involution')
g=e.T*eta*e; gt=et.T*eta*et
matzero(et.det()*gt.inv()-g.inv(),'same massless matter inverse density')
nu=s.Rational(3,5); h=s.Rational(1,8)

def N_B(e,r,t):
    U=nu*eta*e.inv().T
    N=(U[:,r]*U[:,t].T-U[:,t]*U[:,r].T)*eta
    B=-(h*h*nu*nu/U.det())*N
    return N,B

for r in range(4):
    for t in range(r+1,4):
        N,B=N_B(e,r,t)
        Nt,Bt=N_B(et,r,t)
        matzero(Bt-B/E,'all six geometric density homogeneities')
        matzero(Bt-(h*h/(nu*nu))*N,'all six native numerators are tilde cofactors')

# Normalize the continuum curvature contraction at the identity coframe.
# Each Omega_rs is an independently selected eta-skew curvature matrix.
Psum=s.Integer(0); RicciScalar=s.Integer(0)
for r in range(4):
    for t in range(r+1,4):
        anti=s.zeros(4); anti[r,t]=r+t+1; anti[t,r]=-(r+t+1)
        Omega=anti*eta
        N0,B0=N_B(s.eye(4),r,t)
        Psum+=-s.trace((B0/h**2)*Omega)/2
        RicciScalar+=2*(Omega*eta)[r,t]
require(s.cancel(Psum-RicciScalar/2)==0,
        'original six-face contraction is one-half Ricci density')

# Full 16x16 Frechet Jacobian, including determinant derivative.
vec_e=s.Matrix(list(e))
tr_row=s.Matrix(1,16,lambda i,j:e.inv()[j%4,j//4])
J=(s.eye(16)-vec_e*tr_row/2)/s.sqrt(E)
require(s.factor(J.det()+E**-8)==0,'Jacobian determinant -det(e)^-8')
vec_t=s.Matrix(list(et))
tr_t=s.Matrix(1,16,lambda i,j:et.inv()[j%4,j//4])
Jt=(s.eye(16)-vec_t*tr_t/2)/s.sqrt(et.det())
matzero(Jt*J-s.eye(16),'source pullback is invertible on all16 directions')

# Exact independent tetrad variations of same matter density.
v=s.Matrix([s.Rational(2,3),s.Rational(-1,5),s.Rational(3,7),s.Rational(1,4)])
for i in range(16):
    de=s.zeros(4); de[i//4,i%4]=1
    detv=s.Matrix(4,4,list(J*s.Matrix(list(de))))
    dg=de.T*eta*e+e.T*eta*de
    dgt=detv.T*eta*et+et.T*eta*detv
    left=-(v.T*g.inv()*dg*g.inv()*v)[0]
    dEt=et.det()*s.trace(et.inv()*detv)
    right=dEt*(v.T*gt.inv()*v)[0]-et.det()*(v.T*gt.inv()*dgt*gt.inv()*v)[0]
    require(s.cancel(left-right)==0,'full matter coframe derivative including density')

# Actual matrix-parity residual, in 4x4 form, on a smooth boost/rotation family.
def face_pair(L,k=mp.mpf('0.7'),l=mp.mpf('-0.2')):
    hh=mp.mpf(1)/L; x=k*hh**2; y=l*hh**2
    P=mp.matrix([[mp.cosh(x),mp.sinh(x),0,0],
                 [mp.sinh(x),mp.cosh(x),0,0],
                 [0,0,mp.cos(y),-mp.sin(y)],
                 [0,0,mp.sin(y),mp.cos(y)]])
    # Same genuine oriented volume map; B/h^2=one boost generator.
    B=mp.matrix([[0,hh**2,0,0],[hh**2,0,0,0],[0,0,0,0],[0,0,0,0]])
    tr=lambda A:sum(A[i,i] for i in range(A.rows))
    f=-tr(B*(P-P**-1))/4
    # Exterior character identity for the unchanged full CAR trace.
    a=-mp.det(mp.eye(4)+P)*tr(B*P*(mp.eye(4)+P)**-1)/8
    return a/hh**4,f/hh**4
smooth=[]
for L in (4,8,16,32):
    a0,f0=face_pair(L)
    da=mp.diff(lambda k:face_pair(L,k)[0],mp.mpf('0.7'))
    df=mp.diff(lambda k:face_pair(L,k)[1],mp.mpf('0.7'))
    smooth.append({'L':L,'density_residual_over_h4':mp.nstr((a0-f0)*L**4,24),
                   'source_residual_over_h4':mp.nstr((da-df)*L**4,24)})
require(all(abs(mp.mpf(t['density_residual_over_h4']))<1 for t in smooth),
        'bounded O(h4) normalized local density controls')
require(all(abs(mp.mpf(t['source_residual_over_h4']))<1 for t in smooth),
        'bounded O(h4) source controls')

# The existing moment operator forces eta_h^2=O(h^2) on this chart.
p_exact=(s.sqrt(5)-1)/2
a0=s.Rational(1,8)
require(bool(1-p_exact-a0*a0>0),'clock/grade14 normalization stays positive')
Nsites=4
sitepsi=[a0,-a0,a0,a0]
bank=s.zeros(Nsites*16,1)
for ix,amp in enumerate(sitepsi):
    bank[ix*16+1]=s.sqrt(p_exact)/s.sqrt(Nsites)
    bank[ix*16]=amp/s.sqrt(Nsites)
    bank[ix*16+14]=s.sqrt(1-p_exact-amp*amp)/s.sqrt(Nsites)
require(s.simplify((bank.T*bank)[0]-1)==0,'complete material moment bank normalized')
for ix,amp in enumerate(sitepsi):
    read=Nsites/s.sqrt(p_exact)*bank[ix*16+1]*bank[ix*16]
    require(s.simplify(read-amp)==0,'original moment returns spatial scalar')
hnorm=s.symbols('h_norm',positive=True)
q_uv=-(sitepsi[1]-sitepsi[0])**2/hnorm**2
require(s.simplify(q_uv+1/(16*hnorm**2))==0,'source norm lower bound 1/(16h^2)')
require(s.simplify(1/(64*(-q_uv))-hnorm**2/4)==0,'positivity attenuation at most h^2/4')

# SAME literal two-band reporter and complete cut heat+feedback.
p=(mp.sqrt(5)-1)/2; z=mp.mpf(2)**-20; beta=2*p*p
S=128; M=72441; W=50549
ready=2*10946*p**23

def report(x,y):
    ee=p*p*(1+x); u=p+p*p*y
    ell=4*ee*(1-ee); b=4*u*u*(1-u*u)
    aa=ell+(1-ell)*b
    return 1-(1-z*b)*(1-z*aa)

r0=report(0,0)
rf=4*z*(1-4*z*p**3)*p**11
rq=8*z*p**6*((1-4*z*p**3*(1+p**6))+(1-4*z*p**3)*p**6)
close(mp.diff(lambda x:report(x,0),0),rf,'true polynomial reporter geometry slope')
close(mp.diff(lambda y:report(0,y),0),rq,'true polynomial reporter matter slope')
lam=-rq/rf

def cut_price(r):
    qs=[1-ready,ready*(1-r),ready*r]
    ff=[4*q*(1-q) for q in qs]
    Z=mp.mpf(M*W-6)+2*sum(mp.exp(-beta*x) for x in ff)
    return mp.log(S*Z)/beta-S*sum(mp.log1p(-z*x) for x in ff)

kap=mp.diff(cut_price,r0); require(kap>0,'complete heat+feedback gain is positive')
base=cut_price(r0)
# Four unequal but field-INDEPENDENT source weights, volume=1/4 per cell.
rhos=[mp.mpf(1)/2,mp.mpf(3)/4,mp.mpf(5)/4,mp.mpf(3)/2]
Fs=[mp.mpf(1)/7,mp.mpf(-2)/9,mp.mpf(1)/4,mp.mpf(2)/11]
Qs=[mp.mpf(1)/17,mp.mpf(-1)/13,mp.mpf(1)/19,mp.mpf(1)/23]
dFs=[mp.mpf(2)/7,mp.mpf(1)/9,mp.mpf(-3)/10,mp.mpf(1)/8]
dQs=[mp.mpf(1)/29,mp.mpf(-1)/31,mp.mpf(2)/37,mp.mpf(1)/41]
close(sum(rhos)/4,1,'genuine unequal densities normalized')
target=sum(f+lam*q for f,q in zip(Fs,Qs))/4
target_source=sum(f+lam*q for f,q in zip(dFs,dQs))/4

def normalized_price(eps,t=mp.mpf(0),complete=True):
    rbar=sum(rho*report(eps*(ff+t*dff)/rho,-eps*(qq+t*dqq)/rho)
             for rho,ff,qq,dff,dqq in zip(rhos,Fs,Qs,dFs,dQs))/4
    if complete:
        return (cut_price(rbar)-base)/(kap*eps*rf)
    return (rbar-r0)/(eps*rf)

price_controls=[]
for j in (4,6,8,10):
    eps=mp.mpf(2)**(-j)
    val=normalized_price(eps)
    source=mp.diff(lambda t:normalized_price(eps,t),0)
    ev=abs(val-target); es=abs(source-target_source)
    require(ev/eps<1 and es/eps<1,'uniform O(eps) full price and source control')
    price_controls.append({'eps':'2^-'+str(j),'value_error':mp.nstr(ev,25),
        'source_error':mp.nstr(es,25),'value_error_over_eps':mp.nstr(ev/eps,25),
        'source_error_over_eps':mp.nstr(es/eps,25)})
require(all(mp.mpf(price_controls[i+1]['value_error'])<mp.mpf(price_controls[i]['value_error'])
            for i in range(len(price_controls)-1)), 'full-price value errors decrease')
require(all(mp.mpf(price_controls[i+1]['source_error'])<mp.mpf(price_controls[i]['source_error'])
            for i in range(len(price_controls)-1)), 'full-price source errors decrease')
# A hostile check: leaving rho in the target changes the limit.
wrong=sum(rho*(ff+lam*qq) for rho,ff,qq in zip(rhos,Fs,Qs)))/4
require(abs(wrong-target)>mp.mpf('1e-3'),'unequal prior cancellation is essential')
# Fixing a nonzero attenuation does NOT exactly give Einstein/Palatini.
require(abs(normalized_price(mp.mpf(1)/64)-target)>mp.mpf('1e-10'),
        'finite nonlinear price is not silently identified with linear target')

print(json.dumps({'status':'PASS_DENSITY_INVOLUTION_AND_FULL_PRICE_C1_CONTROL',
'checks':checks,'sympy':s.__version__,'precision_digits':mp.mp.dps,
'original_coframe_determinant':str(E),'involution_jacobian':str(J.det()),
'lambda_original':mp.nstr(lam,40),
'geometric_unweighted_controls':smooth,'full_price_source_controls':price_controls,
'native_gate_compilation_performed':False,'native_density_transformation_admitted':False,
'moment_norm_forces_small_signal':True,'native_execution_refinement_verified':False,'exact_general_roots_constructed':False,
'unconditional_GR_closed':False},indent=2))
