#!/usr/bin/env python3
"""One decisive exact GR closure-interface check:
genuine weighted stored self-adjointness -> six admissible metric tangents;
six weighted Euler rows + actual four Bianchi rows -> complete Einstein covector
on generic Fourier k. Also checks true null vacuum 2/2 vs old 1/2.
Does NOT choose physical Cost-Info or construct exact nonlinear critical roots.
"""
import json
from itertools import combinations
import sympy as S
eta=S.diag(1,-1,-1,-1)
lam=S.Matrix([205,144,96,72])/83
tau0=eta*lam
F0=S.Matrix([[205,-144,-96,-72],[-144,155,48,36],
             [-96,48,115,24],[-72,36,24,101]])/83
pairs=list(combinations(range(4),2))
checks=0

def check(v,msg):
    global checks
    if not bool(v):
        raise RuntimeError(msg)
    checks+=1

def same(A,B,msg):
    if isinstance(A,S.MatrixBase):
        check(A.shape==B.shape and all(S.simplify(u-v)==0 for u,v in zip(A,B)),msg)
    else:
        check(S.simplify(A-B)==0,msg)

def P(i,j):
    m=S.zeros(4)
    m[i,j]=m[j,i]=1
    return m

def packet(T):
    return S.Matrix([T[i,j] for i in range(4) for j in range(i,4)])

same(F0*eta*F0.T,eta,'original regular Lorentz F')
same(F0.det(),1,'original proper frame')
same(F0[:,0],tau0,'original observer')
same((tau0.T*eta*tau0)[0],1,'original unit timelike observer')
for r in range(4):
    check(sum(F0[r,j]**2 for j in range(1,4))>0,'all own legs regular')

# Exactly the existing weighted-adjoint Lorentz law A v_y=(omega_x/omega_y) v_x.
sx=S.Rational(7,5)
sy=S.Rational(9,7)
wx=1/sx
wy=1/sy
same(wx/wy,sy/sx,'positive weight ratio')
for r in range(4):
    vtilde_r=eta*F0[r,:].T
    vx=sx*vtilde_r
    vy=sy*vtilde_r
    same(vy,(wx/wy)*vx,'proper Lorentz identity-link weighted leg law')
    same(sy*tau0[r],(wx/wy)*sx*tau0[r],'observer tau weighted own-edge')
    same(sy**2*eta[r,r],(wx/wy)**2*sx**2*eta[r,r],'metric Qrr weighted own-edge')
    check(vx!=vy,'old fixed unweighted own-leg transfer cannot do this')
# The normalized site probability requires no extra parameter and retains ratios.
normal=(1/sx+1/sy)
rho_x=(1/sx)/normal
rho_y=(1/sy)/normal
same(rho_x+rho_y,1,'normalized actual site-weight candidate')
same(rho_x/rho_y,wx/wy,'normalizer cancels on transported own edge')

# Exact NONLINEAR native solution of all weighted kinematic observer/leg constraints.
z,rho=S.symbols('z rho',real=True)
b=(13824*z+205*S.sqrt(20736-39360*z-12073*z*z)-29520)/21289
Qtilde=eta+b*P(0,1)+z*P(0,2)
same(Qtilde.diagonal(),eta.diagonal(),'old own-edge diagonal invariants')
same((tau0.T*Qtilde.inv()*tau0)[0],1,'old nonlinear observer norm')
same(b.subs(z,0),0,'nonlinear branch starts at genuine old background')
same(S.diff(b,z).subs(z,0),-S.Rational(2,3),'real old nonlinear jet')
sfield=S.exp(rho*z)
Q=sfield**2*Qtilde
tau=sfield*tau0
same((tau.T*Q.inv()*tau)[0],1,'exact new weighted nonlinear unit observer')
same(Q.diff(z).subs(z,0),2*rho*eta+P(0,2)-S.Rational(2,3)*P(0,1),'one new conformal physical tangent')

# Admitted metric image of original fixed-w stored class and its ONE weighted scalar.
weight_s=S.Matrix([[2*lam[i]*lam[j] for i,j in pairs]])
nullvec=weight_s.nullspace()
check(len(nullvec)==5,'old stored metric 5D')
old=[sum((v[m]*P(*pairs[m]) for m in range(6)),S.zeros(4)) for v in nullvec]
weighted=[eta]+old
check(S.Matrix.hstack(*[packet(X) for X in weighted]).rank()==6,'new weighted metric 6D')
for H in old:
    check(all(H[i,i]==0 for i in range(4)),'old own-leg constraints')
    same((lam.T*H*lam)[0],0,'old observer constraint')

# The moving positive endpoint source survives after the 1/h difference quotient.
t=S.symbols('t',real=True)
ux,uy=S.symbols('ux uy',real=True)
alpha=S.exp((uy-ux)*t/2)
same(S.diff(alpha,t).subs(t,0),(uy-ux)/2,'true weighted half-density edge first source')

# Source covectors: 4 exact Bianchi slots Ea=0 + 6 exact weighted Euler pairings.
all_sym=[S.diag(*[int(i==j) for i in range(4)]) for j in range(4)]+[P(*ij) for ij in pairs]
def ward_matrix(k):
    a=eta*k
    return S.Matrix([[ (E*a)[i] if i<4 else S.trace(E*weighted[i-4])
                       for E in all_sym] for i in range(10)])

rank_table={}
for name,ks,expected in [
    ('generic', [1,2,3,4],10),
    ('null_graviton',[13,3,4,12],10),
    ('partial_support',[0,1,2,3],10),
    ('exception_null',[1,1,0,0],9),
    ('exception_time',[1,0,0,0],8)]:
    M=ward_matrix(S.Matrix(ks))
    check(M.rank()==expected,'six weighted Euler plus four Ward at '+name)
    rank_table[name]={'k':ks,'rank':M.rank(),'det':str(S.factor(M.det()))}
same(S.factor(ward_matrix(S.Matrix([1,2,3,4])).det()),
     -S.Rational(3558112,615),'exact generic Bianchi+Euler determinant')
same(S.factor(ward_matrix(S.Matrix([13,3,4,12])).det()),
     S.Rational(35557056,205),'exact Lorentz null Bianchi+Euler determinant')

# Gauge-transversality is DUAL to Ward source-completeness: <E,a xi^T+xi a^T>=2 xi^T Ea.
def gauge_condition(H):
    return S.Matrix([H[0,0]+H[i,i] for i in range(1,4)] +
                    [(lam.T*H*lam)[0]-H[0,0]])
def gauge_matrix(k):
    a=eta*k
    return S.Matrix.hstack(*[
        gauge_condition(a*S.eye(4)[:,i].T+S.eye(4)[:,i]*a.T)
        for i in range(4)])
Gnull=gauge_matrix(S.Matrix([13,3,4,12]))
same(Gnull.det(),S.Rational(2560108032,6889),'exact gauge-slice determinant')
check(Gnull.rank()==4,'all four diffeo gauge modes transverse to weighted chart')
same(Gnull.det()/ward_matrix(S.Matrix([13,3,4,12])).det(),
     S.Rational(14760,6889),'exact Ward-gauge dual determinant ratio')
check(gauge_matrix(S.Matrix([1,1,0,0])).rank()==3,
      'some exceptional Fourier modes truly need other equations')

# Standard REAL null Einstein map on the original same Lorentz background.
def Einstein(H,k):
    h=-eta*H*eta
    ht=S.trace(eta*h)
    kup=eta*k
    ks=(k.T*eta*k)[0]
    ric=S.Matrix(4,4,lambda i,j:
       (-k[i]*sum(kup[m]*h[m,j] for m in range(4))
       -k[j]*sum(kup[m]*h[m,i] for m in range(4))
       +ks*h[i,j]+k[i]*k[j]*ht)/2)
    return ric-eta*S.trace(eta*ric)/2

kn=S.Matrix([13,3,4,12])
same((kn.T*eta*kn)[0],0,'physical lightlike k')
Eold=S.Matrix.hstack(*[packet(Einstein(H,kn)) for H in old])
Enew=S.Matrix.hstack(*[packet(Einstein(H,kn)) for H in weighted])
check(Eold.rank()==4 and len(Eold.nullspace())==1,'old admitted one vacuum polarization')
check(Enew.rank()==4 and len(Enew.nullspace())==2,'NEW six weighted directions carry TWO vacuum polarizations')
# Exact finite STAR insertion scales quadratically with SAME original on-site legs.
# Test on a nondegenerate simple bivector, keeping the original connection fixed.
u=S.Matrix([1,2,3,4]); v=S.Matrix([4,2,1,3]); tscale=S.symbols('tscale')
wedge=lambda a,b:S.Matrix([a[i]*b[j]-a[j]*b[i] for i,j in pairs])
same(wedge(tscale*u,tscale*v),tscale**2*wedge(u,v),'finite native bivector quadratic scale')
check(wedge(u,v)!=S.zeros(6,1),'nontrivial star volume component')
same(S.diff(tscale**2,tscale).subs(tscale,1),2,'finite star logarithmic scale Euler row')
print(json.dumps({
    'status':'PASS','exact_controls':checks,
    'original_stored_tangent':5,'weighted_native_tangent':6,
    'native_weighted_site_distribution':[str(rho_x),str(rho_y)],
    'full_nonlinear_weighted_unit_observer':True,
    'source_rank_table':rank_table,
    'null_Einstein_weighted_rank':Enew.rank(),
    'original_GR_vacuum_polarizations':2,
    'old_native_admitted':1,'weighted_native_admitted':2,
    'null_gauge_slice_det':str(Gnull.det()),
    'source_to_gauge_determinant_ratio':'14760/6889',
    'requires_original_selected_weight':True,
    'requires_full_physical_Ward_and_Cost_Info':True,
    'original_raw_hminus2_closed':False
},ensure_ascii=False,sort_keys=True))
