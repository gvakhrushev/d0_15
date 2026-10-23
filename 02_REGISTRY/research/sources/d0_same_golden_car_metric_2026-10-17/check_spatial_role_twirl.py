#!/usr/bin/env python3
"""D0 16-CAR observer stress: exact 24 signed spatial-role twirl.
Conditional algebraic source decomposition, not physical Cost-Info selection.
"""
from __future__ import annotations
import itertools, json, hashlib
from pathlib import Path
import sympy as s
HOME=Path(__file__).resolve().parent
checks=[]
def ck(cond,name):
    if not bool(cond):raise ArithmeticError(name)
    checks.append(name)
def eq(x,y,name):
    if isinstance(x,s.MatrixBase): ck(all(s.simplify(v)==0 for v in x-y),name)
    else:ck(s.simplify(x-y)==0,name)
N=16
c=[]
for r in range(4):
    C=s.zeros(N)
    for mask in range(N):
        if not (mask & (1<<r)):
            dst=mask | (1<<r)
            sign=(-1)**sum((mask>>i)&1 for i in range(r))
            C[dst,mask]=sign
    c.append(C)
g=[x-x.T for x in c];h=[x+x.T for x in c]
O={(i,j):g[i]*h[j] for i in range(1,4) for j in range(1,4)}
Iobs=sum((O[i,i] for i in range(1,4)),s.zeros(N))

def Omap(F):return sum((F[i,j]*O[i+1,j+1] for i in range(3) for j in range(3)),s.zeros(N))

def parity(xs):return (-1)**sum(xs[i]>xs[j] for i in range(len(xs)) for j in range(i+1,len(xs)))

def lift_signed(R):
    L=s.eye(4)
    for i in range(3):
     for j in range(3): L[i+1,j+1]=R[i,j]
    # correct upper-left pure time, no mixes
    Q=s.zeros(N)
    for mask in range(N):
        occupied=[j for j in range(4) if mask&(1<<j)]
        images=[];coeff=1
        for j in occupied:
            row=next(i for i in range(4) if L[i,j]!=0)
            images.append(row);coeff*=L[row,j]
        outmask=sum(1<<i for i in images)
        Q[outmask,mask]=coeff*parity(images)
    return Q

def perm_parity(perm):return parity(perm)
rot=[]
for perm in itertools.permutations(range(3)):
    for sg in itertools.product((-1,1),repeat=3):
        if perm_parity(perm)*sg[0]*sg[1]*sg[2]!=1:continue
        R=s.zeros(3)
        for j in range(3): R[perm[j],j]=sg[j]
        rot.append((R,lift_signed(R)))
ck(len(rot)==24,'exact_24_orientation_preserving_spatial_signed_permutations')
for idx,(R,Q) in enumerate(rot):
    eq(R.T*R,s.eye(3),f'R3_orthogonal_{idx}')
    eq(R.det(),1,f'R3_proper_{idx}')
    eq(Q.T*Q,s.eye(N),f'Fock16_exterior_orthogonal_{idx}')
    for i in range(3):
        eq(Q*g[i+1]*Q.T,sum((R[j,i]*g[j+1] for j in range(3)),s.zeros(N)),f'moving_gamma_{idx}_{i}')
        eq(Q*h[i+1]*Q.T,sum((R[j,i]*h[j+1] for j in range(3)),s.zeros(N)),f'moving_hatgamma_{idx}_{i}')

S0=s.Matrix([[s.Rational(1,3),s.Rational(5,7),s.Rational(-2,5)],
             [s.Rational(-3,4),s.Rational(4,9),s.Rational(2,11)],
             [s.Rational(7,6),s.Rational(-1,8),s.Rational(5,3)]])

def twirl(F):return sum((R*F*R.T for R,Q in rot),s.zeros(3))/24

def twirl_car(X):return sum((Q*X*Q.T for R,Q in rot),s.zeros(N))/24
for i in range(3):
 for j in range(3):
    E=s.zeros(3);E[i,j]=1
    eq(twirl(E),s.trace(E)*s.eye(3)/3,f'all_nine_spatial_matrix_units_average_{i}{j}')
F=S0
B=Omap(F)
P=twirl_car(B)
eq(P,s.trace(F)*Iobs/3,'same_FULL16_car_exact_reynolds_spatial_trace_sector')
eq(P,Omap(twirl(F)),'CAR_and_spatial_reynolds_commute')

def hs(X,Y):return s.trace(X.T*Y)/16
Qobs=s.expand(s.trace(F)**2-s.trace(F.T*F))
Pcomp=B-P
rho=s.simplify(2*hs(P,P)-hs(Pcomp,Pcomp))
eq(rho,Qobs,'invariant_plus2_and_nontrivial_archive_minus1_source')
eq(3*hs(B,P)-hs(B,B),Qobs,'full16_one_superoperator_3PminusI_source')
eq(hs(Pcomp,P),0,'isotropic_and_anisotropic_CAR_parts_orthogonal')
# Genuine moving source under an arbitrary non-symmetric 3x3 observer jet.
t=s.symbols('t',real=True)
dF=s.Matrix([[s.Rational(1,4),1,0],[-1,s.Rational(-1,3),s.Rational(2,7)],
             [s.Rational(3,8),s.Rational(-1,5),s.Rational(1,2)]])
Ft=F+t*dF
Qt=s.expand(s.trace(Ft)**2-s.trace(Ft.T*Ft))
Bt=Omap(Ft);Pt=twirl_car(Bt)
eq(s.expand(2*hs(Pt,Pt)-hs(Bt-Pt,Bt-Pt)),Qt,'complete_moving_observer_source_at_all_t')
eq(s.diff(Qt,t).subs(t,0),2*s.trace(F)*s.trace(dF)-2*s.trace(F.T*dF),'dQ_dobserver_all_9_entries')
# Constant transported-frame change: all full16 CAR conjugates read identically.
R,Q=rot[7]
eq(hs(Q*B*Q.T,Q*B*Q.T),hs(B,B),'co_moving_fock_frame_full_quadratic_norm_invariant')
eq(hs(Q*B*Q.T,Q*Iobs*Q.T),hs(B,Iobs),'co_moving_trace_source_invariant')

result={
 'status':'EXACT FINITE SO3 SUBGROUP REYNOLDS / OBSERVER CAR SOURCE; native admission and physical Cost-Info open',
 'group_size':24,'full_car_dimension':16,'golden_type':'same complete CAR observer sector',
 'checks_count':len(checks),'check_labels_sha256':hashlib.sha256('\n'.join(checks).encode()).hexdigest(),
 'frame_invariant_trace':str(s.trace(F)),'observer_complete_norm':str(s.trace(F.T*F)),
 'observer_complete_source':str(Qobs),'moving_source':str(s.diff(Qt,t).subs(t,0)),
 'twirl_theorem':'Pi(B(C)) = B((tr C/3) I3), implemented by 24 real proper signed permutations on full16 exterior algebra',
 'quadratic_action_source':'Qobs = 2||Pi B||_tr16^2 - ||(I-Pi)B||_tr16^2',
 'physical_boundary':'a finite spatial frame twirl is an exact algebraic expectation, NOT an already physically selected Price or a free controlled native gate'
}
path=HOME/'ROLE_TWIRL.json'
path.write_text(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+'\n',encoding='utf-8')
print('PASS',len(checks),'24 spatial proper-role symmetries on SAME16 CAR; observer source symmetry-twirl exact')
print('SHA256',hashlib.sha256(path.read_bytes()).hexdigest())
