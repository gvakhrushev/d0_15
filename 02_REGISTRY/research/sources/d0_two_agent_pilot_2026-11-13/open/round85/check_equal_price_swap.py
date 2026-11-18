#!/usr/bin/env python3
"""Independent exact rational gauge test of two equal-width source slots."""
from pathlib import Path
import json,hashlib
import sympy as s
R=s.Rational
I=s.eye
# Two nontrivial SAM gates, work-only middle. Both slots have two real paid
# stages; identity slot consists of two involutive SAM X gates, not a free gap.
r=s.Matrix([[R(3,5),-R(4,5)],[R(4,5),R(3,5)]])
x=s.Matrix([[0,1],[1,0]])
w=s.Matrix([[R(5,13),-R(12,13)],[R(12,13),R(5,13)]])
q1=s.kronecker_product(r,I(2));q2=s.kronecker_product(x,I(2))
x4=s.kronecker_product(x,I(2));S1=s.kronecker_product(I(2),w);S2=s.kronecker_product(I(2),x)
early=[q1,q2,S1,S2,x4,x4]
late=[x4,x4,S1,S2,q1,q2]
def multiply(gates):
    a=I(4)
    for gate in gates:a=gate*a
    return a
assert multiply(early)==multiply(late)
assert all(g.T*g==I(4) for g in early+late)
# An initially canonical 1->4 birth and a late 4->8 birth; all intermediate
# actions remain fixed width and equal length, and final retained G is shared.
v=s.Matrix([1,0,0,0]);birth=I(4).col_join(s.zeros(4,4))
glast=s.kronecker_product(r,I(4))
def make(gates):
    actions=[v]+gates+[birth,glast]; passive=[v]+[I(4)]*len(gates)+[birth,I(8)]
    dims=[1]+[4]*(len(gates)+1)+[8]; assert len(actions)==len(dims)
    starts=[];n=0
    for d in dims:starts.append(n);n+=d
    def inc(j):
        a=I(dims[j])
        for k in range(j,len(dims)-1):a=passive[k]*a
        return a
    ret=inc(0).T
    for j in range(1,len(dims)):
        ret=ret.col_join((I(dims[j])-passive[j-1]*passive[j-1].T)*inc(j).T)
    assert ret.T*ret==I(8)
    shift=s.zeros(n)
    for j in range(len(dims)-1):shift[starts[j+1]:starts[j+1]+dims[j+1],starts[j]:starts[j]+dims[j]]=actions[j]
    ef=s.zeros(8,n);ef[:,starts[-1]:]=I(8)
    t=shift+ret*actions[-1]*ef
    p=s.zeros(n);a=I(1);prefix=[]
    for j in range(len(dims)):
        prefix.append(a);p[starts[j]:starts[j]+dims[j],starts[j]:starts[j]+dims[j]]=a*a.T
        if j<len(dims)-1:a=actions[j]*a
    return t,p,prefix,dims,starts
T,P,a,d,starts=make(early);Tp,Pp,ap,dp,_=make(late)
assert d==dp and T.T*T==I(T.rows) and Tp.T*Tp==I(T.rows)
vs=[I(1)];ue=I(4);ul=I(4);vs.append(I(4))
for e,l in zip(early,late):
    ue=e*ue;ul=l*ul;vs.append(ul*ue.T)
assert vs[-1]==I(4)
vs.append(I(8));V=s.diag(*vs)
assert V.T*V==I(V.rows) and Tp==V*T*V.T and Pp==V*P*V.T
# The last gate and all end/birth blocks coincide, including full return and
# birth-complements; so F=P T* (1-P) T P is unitarily conjugate as well.
F=P*T.T*(I(T.rows)-P)*T*P;Fp=Pp*Tp.T*(I(T.rows)-Pp)*Tp*Pp
assert Fp==V*F*V.T
# Delta0(T)=I-B⊗I-C⊗(T+T*) obeys the same similarity for arbitrary
# scene matrices; use exact rational noncommuting 2x2 B,C as a fixture.
B=s.Matrix([[R(1,3),R(1,7)],[R(1,7),R(2,5)]])
C=s.Matrix([[R(1,8),R(1,11)],[R(1,11),R(1,6)]])
D=I(2*T.rows)-s.kronecker_product(B,I(T.rows))-s.kronecker_product(C,T+T.T)
Dp=I(2*T.rows)-s.kronecker_product(B,I(T.rows))-s.kronecker_product(C,Tp+Tp.T)
VV=s.kronecker_product(I(2),V)
assert Dp==VV*D*VV.T
# Negative control: a fixed intermediate SAM mark need not survive. Same
# terminal word is therefore insufficient for marked-map equivalence.
mark=s.kronecker_product(s.diag(1,-1),I(2));j=2
assert a[j].T*mark*a[j] != ap[j].T*mark*ap[j]
out={'status':'PASS_EXACT_FINITE_EQUAL_LENGTH_GAUGE_SWAP_FIXTURE',
 'equal_terminal_unitary':True,'complete_clock_T_and_P_conjugate':True,
 'full_birth_complement_included':True,'feedback_operator_conjugate':True,
 'heat_Delta0_conjugate':True,'intermediate_fixed_SAM_mark_negative_control':True,
 'fixture_not_production_execution':True,'original_task_marked_map_admission_proved':False,
 'GR_closed':False,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('B85_EQUAL_PRICE_SWAP_FIXTURE.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'])
