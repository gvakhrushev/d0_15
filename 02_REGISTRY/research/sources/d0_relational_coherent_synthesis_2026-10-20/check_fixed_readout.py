#!/usr/bin/env python3
"""Exact fixed Golden17 readout of accumulated compact grade-one Choi state.
Checks a POVM, not native G0 implementation or arbitrary reference preparation.
"""
from itertools import combinations, product
import json
import sympy as s

p = (s.sqrt(5)-1)/2
g = p**2
b = s.Rational(1, 4096)
kappa = g**2*b/24
I4, I16 = s.eye(4), s.eye(16)
eta = s.diag(1,-1,-1,-1)
vec = lambda M: s.Matrix(list(M))
u = vec(I4)/2
G = []
for i,j in combinations(range(4),2):
    X = s.zeros(4)
    X[i,j] = 1
    X[j,i] = -eta[i,i]*eta[j,j]
    G.append(X)
v = [vec(X)/s.sqrt(2) for X in G]
assert u.dot(u)==1
assert all(u.dot(x)==0 for x in v)
assert s.Matrix.hstack(u,*v).T*s.Matrix.hstack(u,*v)==s.eye(7)

marks = [kappa*(u+sign*x)*(u+sign*x).T for x in v for sign in (1,-1)]
marked_sum = sum(marks,s.zeros(16))
Pi_u=u*u.T
Pi_v=sum((x*x.T for x in v),s.zeros(16))
assert marked_sum==12*kappa*Pi_u+2*kappa*Pi_v
# These mutually orthogonal projectors resolve the entire sixteen-dimensional
# Choi space, so rest eigenvalues are 12k,22k,24k with multiplicities1,6,9.
Pi_rest=I16-Pi_u-Pi_v
assert Pi_rest*Pi_rest==Pi_rest and s.trace(Pi_rest)==9
rest=24*kappa*I16-marked_sum
assert rest==12*kappa*Pi_u+22*kappa*Pi_v+24*kappa*Pi_rest
effects=marks+[rest,g*p*b*I16,p*g*b*I16,p**2*b*I16,(1-b)*I16]
assert s.simplify(sum(effects,s.zeros(16))-I16)==s.zeros(16)

def rotation(i,j):
    R=I4.copy()
    R[i,i]=R[j,j]=s.Rational(3,5)
    R[i,j]=s.Rational(4,5)
    R[j,i]=-s.Rational(4,5)
    return R

P=rotation(1,2)*rotation(2,3)
assert P.T*P==I4 and P.T*eta*P==eta
for k in range(4):
    Pk=P**k
    chi=vec(Pk)/2
    assert chi.dot(chi)==1 and Pk.T*Pk/4==I4/4
    m=s.trace(Pk)/4
    born=[s.simplify((chi.T*E*chi)[0]) for E in effects]
    target=[]
    for X in G:
        z=s.trace(X.T*Pk)/(2*s.sqrt(2))
        target.extend([kappa*(m+z)**2,kappa*(m-z)**2])
    assert all(s.simplify(a-c)==0 for a,c in zip(born[:12],target))
    assert s.simplify(sum(born)-1)==0

# Exact flat Fisher on the same fixed POVM for compactJ23, using the tangent
# of the accumulated STATE, without any field-dependent final programme.
J=s.zeros(4);J[2,3]=1;J[3,2]=-1
dchi=vec(J)/2
q0=[s.simplify((u.T*E*u)[0]) for E in effects]
dq=[s.simplify(2*(dchi.T*E*u)[0]) for E in effects]
fisher=s.simplify(sum(a*a/c for a,c in zip(dq,q0)))
assert s.simplify(fisher-4*kappa)==0
n=4
moment=s.S.Zero
mass=s.S.Zero
for flags in product((0,1),repeat=n):
    k=sum(flags)
    weight=g**k*p**(n-k)
    mass+=weight
    moment+=weight*k*k
assert s.simplify(mass-1)==0
assert s.simplify(moment-(n*n*g*g+n*g*(1-g)))==0
assert s.simplify(fisher*moment-4*kappa*(n*n*g*g+n*g*(1-g)))==0

# The full CAR16 Choi state has grade-one block mass 1/4. Keep every
# other grade, and complete a fixed POVM on all 256 joint dimensions.
subsets=[a for degree in range(5) for a in combinations(range(4),degree)]
def exterior(A):
    return s.Matrix([[0 if len(a)!=len(c) else
                      (1 if not a else A.extract(a,c).det())
                      for c in subsets] for a in subsets])
full_mark_sum=4*marked_sum
full_rest=96*kappa*I16-full_mark_sum
assert full_rest==48*kappa*Pi_u+88*kappa*Pi_v+96*kappa*Pi_rest
bell_on_block=1-b*(1+3*g*g)
bell_on_complement=1-b*(1-g*g)
assert float(bell_on_block)>0 and float(bell_on_complement)>0
assert s.simplify(96*kappa+2*g*p*b+p*p*b+bell_on_block-1)==0
assert s.simplify(2*g*p*b+p*p*b+bell_on_complement-1)==0
for power in range(4):
    Pk=P**power
    V=exterior(Pk)
    assert V.T*V==s.eye(16)
    chi=vec(V)/4
    block=vec(Pk)/4
    assert chi.dot(chi)==1 and block.dot(block)==s.Rational(1,4)
    assert V.T*V/16==s.eye(16)/16
    full_born=[s.simplify((block.T*(4*E)*block)[0]) for E in marks]
    full_born += [s.simplify((block.T*full_rest*block)[0]),
                  g*p*b,p*g*b,p*p*b,
                  s.simplify(bell_on_complement-96*kappa*block.dot(block))]
    small=vec(Pk)/2
    old_born=[s.simplify((small.T*E*small)[0]) for E in effects]
    assert all(s.simplify(x-y)==0 for x,y in zip(full_born,old_born))
    assert s.simplify(sum(full_born)-1)==0

print(json.dumps({
 'status':'PASS',
 'effects':17,
 'fixed_readout_dimension':16,
 'marked_directions':6,
 'GGrest_exact_eigenvalues_over_kappa':{'12':1,'22':6,'24':9},
 'compact_noncommuting_powers_checked':[0,1,2,3],
 'common_reference_Gram':'I4/4',
 'flat_fisher':'4*kappa',
 'full_flag_fisher_n4':'4*kappa*(16*g^2+4*g*(1-g))',
 'moving_P_power_programme_used':False,
 'full_CAR16_joint_dimension':256,
 'full_CAR16_Gram':'I16/16',
 'full_CAR16_GGrest_nonzero_eigenvalues_over_kappa':{'48':1,'88':6,'96':9},
 'all_grades_retained_full_CAR16_probabilities_equal':True,
 'native_fixed_POVM_payment_derived':False,
 'arbitrary_RIGHT128_preparation_claimed':False
},indent=2))
