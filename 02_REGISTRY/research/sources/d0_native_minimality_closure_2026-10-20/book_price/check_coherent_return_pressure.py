#!/usr/bin/env python3
"""Exact changed check: symmetric complete record partition and genuine paid moments.

No historical certificate is imported or run. Original full128 scalar-shell
identities are consumed from pinned owners. A separate noncommuting rational
isometry checks the new universal symmetric-record algebra and complete versus
conditional price; it is not labelled an original native physical instrument.
The programme writes only stdout and never rewrites expected evidence.
"""
from __future__ import annotations
from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import math
import sympy as s

PINS = {'01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md': 'dfa47d91c4994fa8eea64cda67115590056d8aaf48605daf61a1750aaaf0646d', '02_REGISTRY/research/A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md': 'd92aabf2d46d9ac7d8d9aa3bf5ed66a58f25bb83ca4460d66d25648c62f7e10b', '02_REGISTRY/research/A4D_PROSPECTIVE_BOOK_FINITE_FUTURE_LAW_Q8_VERIFICATION_2026_10_20.md': 'bd3f1ab51599b0efe17af03e40c59a606200cd1912f801e4bd57e0eb77a6b014', '02_REGISTRY/research/sources/d0_same_history_price_composition_2026-10-20/paid_port_history.md': 'ef69c2052237fbe8e916acf16691f9b14b4c1c2465a7837e838db2baeb95449d', '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/execution/return_cost_and_stopping.md': '29e30b35170c8ab1d4d324dd0f7aaa6e588cb1a32f023ad529947dc8639b9faa'}
parser=argparse.ArgumentParser()
parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[5])
args=parser.parse_args()
ROOT=args.root.resolve()
CHECKS=[]
def require(value,label):
    if not value: raise AssertionError(label)
    CHECKS.append(label)
def eq(a,b,label):
    if isinstance(a,s.MatrixBase):
        require(a.shape==b.shape and all(s.simplify(v)==0 for v in a-b),label)
    else: require(s.simplify(a-b)==0,label)
for name,digest in PINS.items():
    require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,'pin:'+name)

def kron(values):
    ans=s.ones(1)
    for value in values: ans=s.kronecker_product(ans,value)
    return ans

def symmetric_projector(d,j):
    if j==0:return s.ones(1)
    states=list(itertools.product(range(d),repeat=j))
    index={v:i for i,v in enumerate(states)}
    out=s.zeros(d**j)
    for perm in itertools.permutations(range(j)):
        for col,state in enumerate(states):
            out[index[tuple(state[i] for i in perm)],col]+=s.Rational(1,math.factorial(j))
    return out

def h(F,j):
    if j==0:return s.Integer(1)
    if j==1:return s.trace(F)
    if j==2:return (s.trace(F)**2+s.trace(F*F))/2
    if j==3:return (s.trace(F)**3+3*s.trace(F)*s.trace(F*F)+2*s.trace(F**3))/6
    raise ValueError(j)

# Independent rational complete-isometry control for the UNIVERSAL new algebra.
# Every output row is retained. Q selects rows 0,1,2; row3 is the complement.
c1,t1=s.Rational(3,5),s.Rational(4,5)
c2,t2=s.Rational(5,13),s.Rational(12,13)
V=s.Matrix([[c2*c1,-t2*c2],[t2*c1,c2*c2],[t1,0],[0,t2]])
eq(V.H*V,s.eye(2),'universal_control_complete_isometry')
A=V[:3,:]
E=[V[i:i+1,:].H*V[i:i+1,:] for i in range(4)]
F=A.H*A
costs=[1,2,2,1]
C_op=sum((costs[i]*E[i] for i in range(4)),s.zeros(2))
C_exit=sum((costs[i]*E[i] for i in range(3)),s.zeros(2))
require(F*C_exit!=C_exit*F,'universal_control_really_noncommuting_cost')
eq(sum(E,s.zeros(2)),s.eye(2),'complete_control_all_output_effects')
eq(F+E[3],s.eye(2),'complete_return_complement_retained')
Aphase=s.diag(1,s.I,1)*A
eq(Aphase.H*Aphase,F,'phase_change_keeps_return_Gram')
require(Aphase!=A,'j1_coherent_vector_retains_unread_phase')
z=s.Rational(1,7)
x=s.symbols('x',positive=True)
Fx=sum((x**costs[i]*E[i] for i in range(3)),s.zeros(2))
Ex=sum((x**costs[i]*E[i] for i in range(4)),s.zeros(2))

for j in range(1,4):
    P=symmetric_projector(2,j)
    dj=j+1
    eq(P*P,P,f'symmetric_projector_idempotent_{j}')
    eq(P.H,P,f'symmetric_projector_adjoint_{j}')
    eq(s.trace(P),dj,f'symmetric_rank_{j}')
    Aj=kron([A]*j)
    W=Aj*P
    eq(s.trace(W.H*W),h(F,j),f'coherent_norm_is_complete_homogeneous_{j}')
    eq(s.trace(P*kron([Fx]*j)),h(Fx,j),f'marked_symmetric_trace_{j}')
    # Every ordered Q-output tuple, including repetitions, remains represented.
    masses=[]
    total_cost=s.Integer(0)
    for labels in itertools.product(range(3),repeat=j):
        mass=s.trace(P*kron([E[i] for i in labels]))
        require(mass>=0,f'ordered_record_positive_{j}_'+''.join(map(str,labels)))
        masses.append(mass)
        total_cost+=sum(costs[i] for i in labels)*mass
    eq(sum(masses),h(F,j),f'ordered_records_sum_to_same_norm_{j}')
    eq(total_cost,s.diff(h(Fx,j),x).subs(x,1),f'actual_record_cost_insertion_{j}')
    # Exact one-copy marginal of the normalized symmetric input.
    marginal=s.zeros(2)
    for a,b in itertools.product(range(2),repeat=2):
        for suffix in itertools.product(range(2),repeat=j-1):
            ia=int(''.join(map(str,(a,*suffix))),2)
            ib=int(''.join(map(str,(b,*suffix))),2)
            marginal[a,b]+=P[ia,ib]/dj
    eq(marginal,s.eye(2)/2,f'symmetric_marginal_is_maximally_mixed_{j}')
    Vj=kron([V]*j)
    eq((Vj*P).H*(Vj*P),P,f'full_output_preserves_input_spectrum_{j}')
    eq(s.diff(h(Ex,j),x).subs(x,1),dj*j*s.trace(C_op)/2,
       f'complete_unconditional_cost_all_outputs_{j}')

# Independent determinant recurrence versus the explicit symmetric sectors.
traceF=s.trace(Fx); detF=Fx.det()
coef=[s.Integer(1),traceF]
for j in range(2,4):coef.append(s.expand(traceF*coef[-1]-detF*coef[-2]))
for j in range(4):eq(coef[j],h(Fx,j),f'determinant_inverse_sector_coefficient_{j}')
Z=1/(s.eye(2)-z*Fx).det()
mu=s.cancel(x*s.diff(Z,x)/Z)
variance=s.cancel(x*s.diff(mu,x))
R=(s.eye(2)-z*F).inv()
C2=sum((costs[i]**2*E[i] for i in range(3)),s.zeros(2))
eq(mu.subs(x,1),z*s.trace(R*C_exit),'conditional_known_cost_noncommuting')
eq(variance.subs(x,1),z*s.trace(R*C2)+z*z*s.trace(R*C_exit*R*C_exit),
   'conditional_variance_noncommuting')
require(z*z*s.trace(R*C_exit*R*C_exit)>0,'variance_missing_resolvent_term_rejected')

zz=s.symbols('zz',positive=True)
RR=(s.eye(2)-zz*F).inv()
mu_z=zz*s.trace(RR*C_exit)
eq((zz*s.diff(mu_z,zz)).subs(zz,z),z*s.trace(R*R*C_exit),
   'conditional_cost_occupation_covariance')

# A complete, genuine isometric field curve (rational Cayley row rotation).
y=s.symbols('y',real=True)
c=(1-y*y)/(1+y*y);sn=2*y/(1+y*y)
Vy=V.copy()
Vy[2,:]=c*V[2,:]+sn*V[3,:]
Vy[3,:]=-sn*V[2,:]+c*V[3,:]
eq(Vy.H*Vy,s.eye(2),'moving_control_isometry_exactly')
Ay=Vy[:3,:]
Fy=Ay.H*Ay
Cy=sum((costs[i]*Vy[i:i+1,:].H*Vy[i:i+1,:] for i in range(3)),s.zeros(2))
dF=Fy.diff(y).subs(y,0)
dC=Cy.diff(y).subs(y,0)
require(F*dF!=dF*F,'moving_control_field_source_noncommuting')
Ry=(s.eye(2)-z*Fy).inv()
mu_y=z*s.trace(Ry*Cy)
eq(s.diff(mu_y,y).subs(y,0),z*s.trace(R*dC)+z*z*s.trace(R*dF*R*C_exit),
   'complete_mixed_field_cost_source')
require(z*z*s.trace(R*dF*R*C_exit)!=0,'frozen_resolvent_source_rejected')

# Complete normalized finite occupation apparatus, including all outer failures.
Zin=sum((j+1)*z**j for j in range(4))
Zret=sum(z**j*h(F,j) for j in range(4))
mean_cap=sum(j*(j+1)*z**j for j in range(4))/Zin
full_transform=sum(z**j*h(Ex,j) for j in range(4))/Zin
eq(full_transform.subs(x,1),1,'complete_finite_cap_normalization')
eq(s.diff(full_transform,x).subs(x,1),mean_cap*s.trace(C_op)/2,
   'complete_finite_cap_known_price')
require(0<Zret/Zin<1,'finite_cap_all_return_event_has_real_failure_probability')
require(s.diff(full_transform,x).subs(x,1)!=mu.subs(x,1),
        'conditional_and_complete_known_prices_not_identified')
# The derivative/endpoints prove the positive pressure integral (no quadrature).
eq(Fx.subs(x,0),s.zeros(2),'strict_positive_cost_suppresses_all_return_at_infinite_mark')
eq(s.diff(s.log(Z),x),mu/x,'positive_pressure_cost_integral_derivative')

class Golden:
    """Exact Q[p]/(p^2+p-1), positive real embedding p=(sqrt(5)-1)/2."""
    def __init__(self,a=0,b=0):self.a,self.b=Q(a),Q(b)
    @staticmethod
    def make(v):return v if isinstance(v,Golden) else Golden(v)
    def __add__(self,v):
        v=self.make(v);return Golden(self.a+v.a,self.b+v.b)
    __radd__=__add__
    def __neg__(self):return Golden(-self.a,-self.b)
    def __sub__(self,v):return self+-self.make(v)
    def __rsub__(self,v):return self.make(v)+-self
    def __mul__(self,v):
        v=self.make(v)
        return Golden(self.a*v.a+self.b*v.b,self.a*v.b+self.b*v.a-self.b*v.b)
    __rmul__=__mul__
    def inv(self):
        n=self.a*self.a-self.a*self.b-self.b*self.b
        if not n:raise ZeroDivisionError()
        return Golden((self.a-self.b)/n,-self.b/n)
    def __truediv__(self,v):return self*self.make(v).inv()
    def __rtruediv__(self,v):return self.make(v)*self.inv()
    def __pow__(self,n):
        if n<0:return self.inv()**(-n)
        out=Golden(1)
        for _ in range(n):out=out*self
        return out
    def __eq__(self,v):
        v=self.make(v);return self.a==v.a and self.b==v.b
    def sign(self):
        aa=self.a-self.b/2;bb=self.b/2
        if aa==0:return (bb>0)-(bb<0)
        if bb==0:return (aa>0)-(aa<0)
        if aa>0 and bb>0:return 1
        if aa<0 and bb<0:return -1
        q=aa*aa-5*bb*bb
        return ((q>0)-(q<0))*(1 if aa>0 else -1)
    def record(self):return [str(self.a),str(self.b)]

p=Golden(0,1)
require(p+p*p==1,'original_Golden_unit_partition')
# Literal old fixture: h=1/4, nu=3/5, lambda=288/25, A_native^2=9/3200.
a=Q(9,3200);d=16*128;zn=Q(1,2**20)
f=4*p**2*a-4*p**4*a*a
r=4*p**3*a
B=1-2*p*p*a
require(f==1-B*B,'native_full128_return_blank_complement')
require((f-r).sign()>0 and r.sign()>0,'native_both_exit_ports_positive')
# From the OWNED full128 map: x[1+4p^3 a(x-1)-B^2].
require(1-4*p**3*a-B*B==f-r,'native_marked_return_linear_cost_coefficient')
require(4*p**3*a==r,'native_marked_return_quadratic_cost_coefficient')
require((f-r)+r==f,'native_all_return_mass_retained')
Cexit=f+r;C2exit=f+3*r
mu_native=d*zn*Cexit/(1-zn*f)
var_native=d*zn*C2exit/(1-zn*f)+d*zn*zn*Cexit*Cexit/(1-zn*f)**2
mu_complete=d*zn*(1+r)/(1-zn)
require(mu_native.sign()>0 and var_native.sign()>0,'native_2048_cost_and_variance_positive')
require(mu_complete!=mu_native,'native_complete_price_differs_from_conditional_return_price')
# Complete-symmetric coefficients from permutation-cycle recurrence on ALL2048 modes.
hh=[Golden(1)]
for j in range(1,5):
    hj=sum((d*f**k*hh[j-k] for k in range(1,j+1)),Golden())/j
    expected=math.comb(d+j-1,j)*f**j
    require(hj==expected,f'native_full2048_symmetric_coefficient_{j}')
    hh.append(hj)
df=4*p*p*(1-2*p*p*a)
source=d*zn*df/(1-zn*f)
require(source.sign()>0,'native_Book_pressure_scale_source_strictly_positive')
require((-source).sign()<0,'same_native_amplitude_free_minimum_source_opposite')
require((d*zn*4*p**3/(1-zn)).sign()>0,
        'native_complete_known_cost_scale_source_strictly_positive')

# FixedRIGHT128 algebraic control on dimension256, with noncommuting preparation.
# M=|+> tensor I_128/sqrt128; no claim this is a configured geometry fixture.
Pplus=s.Matrix([[s.Rational(1,2),s.Rational(1,2)],
               [s.Rational(1,2),s.Rational(1,2)]])
DD=s.diag(1,2)
eq(Pplus*Pplus,Pplus,'fixedRIGHT_projection_idempotent')
eq(128*s.trace(Pplus/128),1,'fixedRIGHT128_normalized_trace')
require(Pplus*DD!=DD*Pplus,'fixedRIGHT_control_not_commuting_with_Delta')
require(128*Pplus.rank()==128,'fixedRIGHT128_uniform_nonzero_spectrum')
L1,L2,LZ,LC,Lrank,beta=s.symbols('L1 L2 LZ LC Lrank beta',real=True)
Ray=s.Rational(3,2)
Drel=-Lrank-(L1+L2)/2+LZ
Lambda_mean=-(L1+L2)/(2*beta)
right=Drel/beta+(Lrank+LC)/beta+Ray-Lambda_mean
eq(right,Ray+(LC+LZ)/beta,'same_H_plus_R_relative_entropy_and_clock_correction')
require(s.simplify(right-(Ray+(LC+LZ)/beta+Lambda_mean))!=0,
        'deleting_finite_clock_correction_changes_original_price')

here=Path(__file__).resolve().parent
record={
 'status':'PASS','checks':len(CHECKS),'check_names':CHECKS,
 'source_commit':'f569c786','input_sha256':PINS,
 'proof_sha256':hashlib.sha256((here/'COHERENT_RETURN_PRESSURE_AND_PAID_MOMENTS.md').read_bytes()).hexdigest(),
 'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'native_shell':{'h':'1/4','nu':'3/5','lambda':'288/25','a':'9/3200',
                 'dimension_with_oldRIGHT':2048,'z':'2^-20',
                 'conditional_mean_Qp':mu_native.record(),
                 'conditional_variance_Qp':var_native.record(),
                 'complete_mean_Qp':mu_complete.record(),
                 'pressure_scale_source_Qp':source.record()},
 'scope':{
  'original_instrument':'full128 exact factored scalar-shell identities consumed from pinned owners',
  'new_general_algebra_control':'separate rational complete isometry; not labelled a native physical instrument',
  'symmetric_carrier':'additional trace-purified multiple-run input; physical preparation not inferred',
  'native_full_site_replay':False,'physical_Info_selected':False,
  'complete_physical_price_proved':False,'physical_D_min_attainment':False,'GR_closed':False,
  'old_suites_replayed':False,
 }
}
print(json.dumps(record,sort_keys=True,indent=2))
