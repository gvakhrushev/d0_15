#!/usr/bin/env python3
"""Exact arithmetic completion and source-equivalence controls for D0 #334.

Uses the existing ten-sign polynomial; no target Einstein coefficient is fitted.
The threshold circuit is represented by exact integers, not emitted as a huge
primitive gate list. Logical Boolean/herald/source-bank admission remains owned
by its source interface. No full GR, lattice-root, Lean, or CI closure is claimed.
"""
from __future__ import annotations
import hashlib
import itertools
import json
import platform
from fractions import Fraction as Q
from pathlib import Path
import mpmath as mp
import sympy as s

mp.mp.dps = 180
CHECKS = 0

def require(cond: bool, msg: str) -> None:
    global CHECKS
    CHECKS += 1
    if not bool(cond):
        raise ArithmeticError(msg)

def near(a, b, msg: str, tol='1e-115') -> None:
    require(abs(a-b) <= mp.mpf(tol)*max(mp.mpf(1), abs(a), abs(b)), msg)

def eqmat(a, b, msg: str) -> None:
    require(a.shape == b.shape and all(s.simplify(v) == 0 for v in a-b), msg)

p, x, y, z = s.symbols('p x y z', real=True)
z0 = s.Rational(1, 2**20)
eps0 = s.Rational(1, 64)
E = p**2*(1+x)
u = p+p**2*y
ell = 4*E*(1-E)
b = 4*u**2*(1-u**2)
a = ell+(1-ell)*b
R = s.rem(s.expand(1-(1-z*b)*(1-z*a)), p*p+p-1, p)
R0 = s.expand(R.subs({x:0,y:0,z:z0}))
rf = s.expand(s.diff(R,x).subs({x:0,y:0,z:z0}))
rq = s.expand(s.diff(R,y).subs({x:0,y:0,z:z0}))

# Exact rational bracketing of the positive Golden root.
lo, hi = Q(0), Q(1)
for _ in range(450):
    mid=(lo+hi)/2
    if mid*mid+mid-1 < 0: lo=mid
    else: hi=mid
require(lo*lo+lo-1 < 0 < hi*hi+hi-1, 'certified Golden isolating interval')

def pair(expr):
    cp=s.Poly(s.rem(s.expand(expr),p*p+p-1,p),p)
    return Q(cp.nth(0)),Q(cp.nth(1))

def qbound(v):
    aa,bb=v
    return (aa+bb*lo,aa+bb*hi) if bb >= 0 else (aa+bb*hi,aa+bb*lo)

def phi_step(v):
    aa,bb=v
    return aa+bb,aa

def pmul(v,w):
    aa,bb=v;cc,dd=w
    return aa*cc+bb*dd,aa*dd+bb*cc-bb*dd

def ppow(n):
    v=(1,0); base=(0,1)
    while n:
        if n&1: v=pmul(v,base)
        base=pmul(base,base); n//=2
    return v

rows_by_sigma={}
coefficients={}
for sigma in (-1,1):
    pol=s.Poly(s.expand(R.subs({x:eps0*x,y:sigma*eps0*y,z:z0})),x,y)
    cs={powers:pair(c) for powers,c in pol.terms()}
    coefficients[sigma]=cs
    require(len(cs)==27,'all original 3x9 coefficient slots retained')
    rows=[]
    for signs in itertools.product((-1,1), repeat=10):
        ps=[1,signs[0],signs[0]*signs[1]]
        pt=[1]
        for v in signs[2:]: pt.append(pt[-1]*v)
        aa=Q(0);bb=Q(0)
        for (i,j),(cc,dd) in cs.items():
            sign=ps[i]*pt[j]
            aa+=sign*cc;bb+=sign*dd
        lower,upper=qbound((aa,bb))
        require(0<lower<=upper<1,'strict original branch probability and complement')
        rows.append((aa,bb))
    rows_by_sigma[sigma]=rows
    mean=(sum(v[0] for v in rows)/1024,sum(v[1] for v in rows)/1024)
    require(mean==pair(R0),'ten independent unbiased signs recover original r0')

# Check the whole actual polynomial, not only its constant term, under
# independent signs with distinct rational means. Products encode first powers.
ss,tt=Q(2,7),Q(-3,11)
for sigma in (-1,1):
    av=(Q(0),Q(0))
    for signs,value in zip(itertools.product((-1,1),repeat=10),rows_by_sigma[sigma]):
        weight=Q(1)
        for i,sign in enumerate(signs):
            mean=ss if i<2 else tt
            weight*= (1+mean*sign)/2
        av=(av[0]+weight*value[0],av[1]+weight*value[1])
    target=pair(R.subs({x:eps0*s.Rational(ss.numerator,ss.denominator),
                       y:sigma*eps0*s.Rational(tt.numerator,tt.denominator),z:z0}))
    require(av==target,'exact full nonlinear ten-sign Born moment identity')

allrows=rows_by_sigma[-1]+rows_by_sigma[1]
require(all(c.denominator & (c.denominator-1)==0 for row in allrows for c in row),
        'only dyadic denominators in original constant decoder')
B=max(c.denominator.bit_length()-1 for row in allrows for c in row)
require(B==94,'actual common dyadic exponent of entire original decoder')
D=2**B
original=[]
for aa,bb in allrows:
    original.append(((int(aa*D),int(bb*D)),(int((1-aa)*D),int(-bb*D))))
transformed=original
n=0
while any(min(pairval)<0 for row in transformed for pairval in row):
    transformed=[tuple(phi_step(v) for v in row) for row in transformed]
    n+=1
    require(n<200,'finite common prefix positivity search')
require(n==6,'one common Golden depth suffices for both sigma and all 1024 rows')
F=[0,1]
for _ in range(n+1): F.append(F[-1]+F[-2])
capacity_A=D*F[n+1];capacity_B=D*F[n]
raw={str(sigma):[] for sigma in (-1,1)}
for k,(src,dst) in enumerate(zip(original,transformed)):
    yes,no=dst
    require(yes[0]+no[0]==capacity_A and yes[1]+no[1]==capacity_B,
            'exact complete prefix capacities, both outcomes')
    require(0<=yes[0]<=capacity_A and 0<=yes[1]<=capacity_B,
            'thresholds lie inside real prefix rank ranges')
    # p^n(A+Bp)=D beta. All arithmetic here is integer in Z[p].
    require(pmul(ppow(n),yes)==src[0], 'exact threshold reproduces decoder probability')
    # Fair pairs success alpha=(2p^3)^B. Whole click is p^(3B+n)(A+Bp).
    joint=pmul(ppow(3*B+n),yes)
    require(all(isinstance(v,int) for v in joint),'unconditional ready-click is in Z[p]')
    sigma=-1 if k<1024 else 1
    raw[str(sigma)].append([str(yes[0]),str(yes[1])])

# Enumerate the actual SIX Golden coin strings only, retaining all suffixes.
prefixes={}
for bits in itertools.product((0,1),repeat=n):
    acc=0
    for length,bit in enumerate(bits,1):
        acc+=1+bit
        if acc>=n:
            key=bits[:length]
            prefixes[key]=acc
            break
require(sum(v==n for v in prefixes.values())==F[n+1], '13 prefix leaves of exponent six')
require(sum(v==n+1 for v in prefixes.values())==F[n], '8 overshoots of exponent seven')
require(len(prefixes)==21,'no prefix outcome discarded')

# Replay integrality boundary and its constructive resolution for r0.
a0,b0=pair(R0)
field_trace=2*a0-b0
require(field_trace==Q(-5505109,17179869184),'old arithmetic obstruction retained')
require(field_trace.denominator!=1,'r0 alone not algebraically integral')
alpha_pair=tuple(2**B*v for v in ppow(3*B))
completed=pmul(alpha_pair,(a0,b0))
require(all(v.denominator==1 for v in completed),'alpha r0 now algebraically integral')

# Construct the source MOMENTS from internally encoded coordinates, not
# from a supplied field-dependent Julia/Choi unitary. Fresh selector records
# purify the mixed source and remain in the completed reflection.
v0,v1,v2=s.symbols('v0 v1 v2',real=True)
vs=[v0,v1,v2]
c=s.Integer(16);omega=s.Rational(1,8)
base=s.eye(4)[:,0]
Hs=[]
rho=(1-3*omega)*(base*base.T)
for k,v in enumerate(vs,1):
    ej=s.eye(4)[:,k]
    plus=(base+ej)/s.sqrt(2);minus=(base-ej)/s.sqrt(2)
    rho+=(omega/2+v/(2*c))*(plus*plus.T)
    rho+=(omega/2-v/(2*c))*(minus*minus.T)
    H=c*(base*ej.T+ej*base.T)
    Hs.append(H)
require(s.simplify(s.trace(rho)-1)==0,'complete moment bank normalization')
for i,H in enumerate(Hs):
    require(s.simplify(s.trace(H*rho)-vs[i])==0,'all original-type anchored moments recovered')
    for j,v in enumerate(vs):
        require(s.simplify(s.trace(H*rho.diff(v))-(1 if i==j else 0))==0,
                'moment lift has full coordinate tangent rank')
    require(all(s.diff(rho[k,k],vs[i])==0 for k in range(4)),
            'source coordinate variations preserve bank diagonal')
poly_op=s.kronecker_product(Hs[0],Hs[1])+s.kronecker_product(Hs[2],Hs[2])
require(s.simplify(s.trace(poly_op*s.kronecker_product(rho,rho))-v0*v1-v2*v2)==0,
        'independent regenerated banks implement the actual tensor-polynomial mechanism')
# A finite Q(p) catalogue, including nondyadic coordinate denominators.
catalogue=[(s.Rational(2,5),-s.Rational(1,3),s.Rational(1,7)),
           (p/3,-s.Rational(2,7),s.Rational(1,9)),
           (-p/5,s.Rational(4,9),-s.Rational(3,7))]
partitions=[]
for values in catalogue:
    weights=[1-3*omega]
    for v in values:weights.extend([omega/2+v/(2*c),omega/2-v/(2*c)])
    pairs=[pair(w) for w in weights]
    require(sum(v[0] for v in pairs)==1 and sum(v[1] for v in pairs)==0,
            'source mixture all outcomes sum to one')
    require(all(qbound(w)[0]>0 for w in pairs),'whole source mixture has positive slack')
    partitions.append(pairs)
Dsrc=1
for row in partitions:
    for pr in row:
        for v in pr:Dsrc=__import__('math').lcm(Dsrc,v.denominator)
Bsrc=Dsrc.bit_length() # 2^Bsrc > Dsrc, includes an explicit abort outcome.
scaled=[]
for row in partitions:
    rr=[(int(Dsrc*v[0]),int(Dsrc*v[1])) for v in row]
    rr.append((2**Bsrc-Dsrc,0))
    scaled.append(rr)
nsrc=0
while any(min(v)<0 for row in scaled for v in row):
    scaled=[[phi_step(v) for v in row] for row in scaled]
    nsrc+=1
    require(nsrc<200,'finite Golden source-bank selector depth')
for row,oldrow in zip(scaled,partitions):
    for vv,ww in zip(row[:-1],oldrow):
        require(pmul(ppow(nsrc),vv)==(int(Dsrc*ww[0]),int(Dsrc*ww[1])),
                'full source-bank success weights have exact target conditional law')
    total=(sum(v[0] for v in row),sum(v[1] for v in row))
    require(pmul(ppow(nsrc),total)==(2**Bsrc,0),
            'source-bank aborts and successes kept in complete law')
source_bank_control={'dimension':4,'real_coordinates':3,
 'catalogue_size':len(catalogue),'common_denominator':Dsrc,
 'fair_bits':Bsrc,'additional_prefix_depth':nsrc,
 'conditional_probability_numerator':Dsrc,
 'conditional_probability_denominator':2**Bsrc,
 'primitive_boolean_implementation_emitted':False}

# Universal scalar feedback derivatives, verified without numerical fitting.
t,zz=s.symbols('t zz',real=True)
f=4*t*(1-t)
j=-s.log(1-zz*f)
j2=s.factor(s.diff(j,t,2))
expected=-8*zz*(1-2*zz+zz*f)/(1-zz*f)**2
require(s.simplify(j2-expected)==0,'exact strict concavity identity')
# Bounds are exact by monotonicity in f in [0,1].
ff=s.symbols('f',real=True)
qpos=(1-2*zz+zz*ff)/(1-zz*ff)**2
require(s.cancel(s.diff(qpos,ff)-zz*(3-4*zz+zz*ff)/(1-zz*ff)**3)==0,
        'concavity bound monotone in f for 0<z<1/2')

# Full output reflections. Exact rational input amplitudes, all dirty columns.
psi=s.Matrix([s.Rational(2,3),0,s.Rational(2,3),0,s.Rational(1,3),0])
e0=s.eye(6)[:,0]; vec=e0-psi
A=s.eye(6)-2*vec*vec.T/(vec.T*vec)[0]
eqmat(A*e0,psi,'full unitary preparation, not a partial amplitude')
eqmat(A.T*A,s.eye(6),'all six preparation columns')
T=s.eye(6)
T[2,2]=T[3,3]=s.Rational(3,5);T[2,3]=-s.Rational(4,5);T[3,2]=s.Rational(4,5)
P=e0*e0.T
feedback=[]
for category,prob in enumerate((s.Rational(4,9),s.Rational(4,9),s.Rational(1,9))):
    Pi=s.zeros(6)
    Pi[2*category,2*category]=Pi[2*category+1,2*category+1]=1
    Z=s.eye(6)-2*Pi
    M1=A.T*Z*A
    M2=T.T*M1*T
    eqmat(M1*M1,s.eye(6),'whole endpoint is a reflection')
    eqmat(M2*M2,s.eye(6),'different dirty-column implementation is also a reflection')
    F1=P*M1.T*(s.eye(6)-P)*M1*P
    F2=P*M2.T*(s.eye(6)-P)*M2*P
    eqmat(F1,4*prob*(1-prob)*P,'literal all-column complement formula')
    eqmat(F2,F1,'full feedback invariant on implementation fibre')
    feedback.append(str(s.trace(F1)))
# Nontriviality: not every completed matrix is the same.
require(M1!=M2,'the theorem is not restricted to identical complete matrices')

pp=(mp.sqrt(5)-1)/2
zv=mp.mpf(2)**-20
sr=128
alpha0=(2*pp**3)**B
rzero=mp.mpf(a0.numerator)/a0.denominator + (mp.mpf(b0.numerator)/b0.denominator)*pp
rf0=mp.mpf(str(s.N(rf.subs(p,(s.sqrt(5)-1)/2),190)))
rq0=mp.mpf(str(s.N(rq.subs(p,(s.sqrt(5)-1)/2),190)))
lam=-rq0/rf0

def jval(v): return -mp.log1p(-4*zv*v*(1-v))
def jp(v): return 4*zv*(1-2*v)/(1-4*zv*v*(1-v))
def jpp(v):
    fv=4*v*(1-v)
    return -8*zv*(1-2*zv+zv*fv)/(1-zv*fv)**2

def price(alpha,r):
    return sr*(jval(1-alpha)+jval(alpha*(1-r))+jval(alpha*r))
def kr(alpha,r):
    return sr*alpha*(jp(alpha*r)-jp(alpha*(1-r)))
def krr(alpha,r):
    return sr*alpha**2*(jpp(alpha*r)+jpp(alpha*(1-r)))

alphas=(mp.mpf(1),mp.mpf(2)/5,alpha0,mp.mpf('1e-50'))
slope_rows=[]
for alpha in alphas:
    for rv in (rzero,mp.mpf(1)/8,mp.mpf(1)/4):
        derivative=kr(alpha,rv)
        low=8*sr*zv*(1-2*zv)*alpha**2*(1-2*rv)
        high=8*sr*zv/(1-zv)*alpha**2*(1-2*rv)
        require(0<low<=derivative<=high,'all failure-inclusive source gains positive')
        require(abs(mp.diff(lambda rr:price(alpha,rr),rv)-derivative) <= abs(derivative)*mp.mpf('1e-60'),
                'derivative of complete price, relative test even for tiny readiness')
        ratio=abs(krr(alpha,rv)/kr(alpha,rzero))
        bound=2/((1-zv)*(1-2*zv)*(1-2*rzero))
        require(ratio<=bound,'uniform normalized Hessian bound as readiness tends to zero')
    slope_rows.append({'alpha':mp.nstr(alpha,45),
                       'kappa_at_r0':mp.nstr(kr(alpha,rzero),45),
                       'kappa_div_alpha_squared':mp.nstr(kr(alpha,rzero)/alpha**2,45)})

# Consume the genuine nonlinear report with unequal fixed density weights.
def report(xx,yy):
    E=pp**2*(1+xx); u=pp+pp**2*yy
    ell=4*E*(1-E);bb=4*u*u*(1-u*u)
    aa=ell+(1-ell)*bb
    return 1-(1-zv*bb)*(1-zv*aa)
rhos=[mp.mpf(1)/2,mp.mpf(3)/4,mp.mpf(5)/4,mp.mpf(3)/2]
Fs=[mp.mpf(1)/7,-mp.mpf(2)/9,mp.mpf(1)/5,mp.mpf(3)/13]
Qs=[mp.mpf(1)/43,mp.mpf(1)/37,-mp.mpf(1)/31,mp.mpf(1)/47]
vF=[mp.mpf(1)/11,-mp.mpf(1)/17,mp.mpf(1)/19,mp.mpf(1)/23]
vQ=[-mp.mpf(1)/71,mp.mpf(1)/67,mp.mpf(1)/73,mp.mpf(1)/79]
target=sum((vF[i]+lam*vQ[i])/4 for i in range(4))

def rbar(eps,tau):
    return sum(rhos[i]*report(eps*(Fs[i]+tau*vF[i])/rhos[i],
                         -eps*(Qs[i]+tau*vQ[i])/rhos[i])/4 for i in range(4))
convergence=[]
for alpha in (mp.mpf(1),alpha0,mp.mpf('1e-50')):
    errors=[]
    for k in (4,6,8,10):
        eps=mp.mpf(2)**-k
        rv=rbar(eps,0)
        drv=mp.diff(lambda tt:rbar(eps,tt),mp.mpf(0))
        source=kr(alpha,rv)*drv/(kr(alpha,rzero)*eps*rf0)
        error=abs(source-target)
        errors.append(error)
        convergence.append({'alpha':mp.nstr(alpha,20),'eps_power':k,
                            'source_error':mp.nstr(error,35),
                            'source_error_div_eps':mp.nstr(error/eps,35)})
    require(all(errors[i+1]<errors[i] for i in range(3)),
            'consistency survives exact tiny factory probability')

# Decisive negative control: field-dependent readiness contributes its own row.
a_test=mp.mpf(2)/5; rtest=mp.mpf(1)/5
extra=mp.diff(lambda aa:price(aa,rtest),a_test)
require(abs(extra)>mp.mpf('1e-6'),'readiness cannot be frozen if actually field dependent')
# Scalar source theorem is not an unrestricted matrix/cost equivalence.
# Two subregions with different local reports can have a cancellation for one
# price and not another if readiness is applied locally before summation.
r1=mp.mpf(1)/8;r2=mp.mpf(1)/4
v1=mp.mpf(1);v2=-kr(mp.mpf(1),r1)/kr(mp.mpf(1),r2)
local_changed=kr(a_test,r1)*v1+kr(a_test,r2)*v2
require(abs(local_changed)>mp.mpf('1e-12'),
        'global same-report composition not a free per-cell replacement')

# Implementation choice at fixed task cannot change classical stationarity.
# Force a price crossing by FIELD-INDEPENDENT baselines, never a fitted source.
aA=mp.mpf(1);aB=mp.mpf(2)/5
rstar=mp.mpf(1)/5
baseB=price(aA,rstar)-price(aB,rstar)
def env(rr):return min(price(aA,rr),baseB+price(aB,rr))
step=mp.mpf('1e-8')
require(env(rstar-step)<env(rstar)<env(rstar+step),
        'finite cheapest-implementation envelope remains strictly increasing at a switch')
require(abs((env(rstar+step**2)-env(rstar))/step)<mp.mpf('1e-10'),
        'finite-envelope stationary report has vanishing small-step slope')
# Ranks/capacities are an actual executable classical threshold description.
HERE=Path(__file__).resolve().parent
threshold_payload={'format':'event thresholds A+B*p after multiplying beta by 2^94 phi^6',
 'fair_bits':B,'golden_depth':n,
 'capacity_type6':str(capacity_A),'capacity_type7':str(capacity_B),
 'sign_order':'lexicographic (-1,+1)^10; first two S, next eight T',
 'thresholds_by_sigma':raw}
threshold_bytes=(json.dumps(threshold_payload,indent=2,sort_keys=True)+'\n').encode()
(HERE/'thresholds.json').write_bytes(threshold_bytes)
res={
 'status':'PASS_COMPLETE_HERALD_SOURCE_CLASS',
 'checks':CHECKS,'python':platform.python_version(),'sympy':s.__version__,
 'mpmath_digits':mp.mp.dps,
 'original_sign_branches_per_sigma':1024,'both_original_sigma_checked':True,
 'dyadic_denominator_bits':B,'common_golden_prefix_depth':n,
 'golden_prefix_type_counts':[F[n+1],F[n]],
 'direct_Golden_coin_preparation_calls':2*B+n,
 'coin_factory_readiness':mp.nstr(alpha0,55),
 'logical_Boolean_gate_cost_and_readiness_included_in_194':False,
 'old_nonintegral_r0_trace':str(field_trace),
 'source_bank_control':source_bank_control,
 'completed_alpha_r0_integral':True,
 'native_full_threshold_table_sha256':hashlib.sha256(threshold_bytes).hexdigest(),
 'exact_echo_feedback_traces':feedback,
 'source_gains':slope_rows,'original_lambda':mp.nstr(lam,45),
 'source_convergence':convergence,
 'field_dependent_readiness_extra_source':mp.nstr(extra,40),
 'forbidden_local_reweighting_residual':mp.nstr(local_changed,40),
 'whole_primitive_threshold_circuit_emitted':False,
 'source_banks_generated_from_books_00_01':False,
 'complete_internal_clock_diagonalization_replayed':False,
 'general_lattice_roots_constructed':False,
 'full_G0_or_unconditional_GR_closed':False}
print(json.dumps(res,indent=2))
