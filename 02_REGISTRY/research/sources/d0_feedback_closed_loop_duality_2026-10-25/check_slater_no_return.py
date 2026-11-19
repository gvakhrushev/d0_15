#!/usr/bin/env python3
"""Exact rational 4-mode closed CAR Slater realization of Book03 no-return.
This is a FINITE BORN instrument and full six-label test, not a claimed
D0 G/CX/SourceI primitive circuit, compulsory filled-state task, or GR proof.
"""
from __future__ import annotations
import itertools
import json
import sympy as S

r=S.Rational
z=r(1,2**20)
I2=S.eye(2)
O=S.Matrix([[r(3,5),-r(4,5)],[r(4,5),r(3,5)]])
t1,t2=r(1,4096),r(1,3072)

def amplitudes(t):
    return (1-t*t)/(1+t*t),2*t/(1+t*t)

a1,b1=amplitudes(t1)
a2,b2=amplitudes(t2)
A=O*S.diag(a1,a2)*O.T
B=O*S.diag(b1,b2)*O.T
F=B*B/z
U=A.row_join(-B).col_join(B.row_join(A))
checks=0

def check(pred,message):
    global checks
    checks+=1
    if not bool(pred):
        raise ArithmeticError(message)

def zero(m):
    if isinstance(m,S.MatrixBase):return all(S.cancel(x)==0 for x in m)
    return S.cancel(m)==0

check(O.T*O==I2 and O.det()==1,'real active basis gauge has no missing operator')
check(z>0 and z<1,'native Book ζ')
check(F==F.T and F[0,1]!=0,'nontrivial full matrix F')
for eig in (b1*b1/z,b2*b2/z):
    check(eig>0 and eig<1,'the true full F is a STRICT positive contraction')
check(zero(A*A+B*B-I2) and zero(A*B-B*A), 'original one-particle operator controls')
check(zero(U.T*U-S.eye(4)) and U.det()==1,'ALL four modes implement SO4')

# Fermionic two-particle Hilbert space wedge^2(C^4) has six orthogonal
# endpoint modes. Exterior-square amplitudes are EXACT 2x2 minors.
labels=list(itertools.combinations(range(4),2))
W=S.Matrix([[U.extract(list(out),list(inp)).det()
             for inp in labels] for out in labels])
check(len(labels)==6 and labels[0]==(0,1),'six complete fixed-number outcomes')
check(zero(W.T*W-S.eye(6)),'full wedge^2 unitary, no failed branch discarded')
check(W.det()==1,'actual wedge6 matrix is special orthogonal')
p=[S.factor(value**2) for value in W[:,0]]
check(all(value>0 for value in p),'ALL six occupation outcomes nonzero')
check(sum(p)==1,'all SIX recorded Born probabilities sum to unity')
p_empty=p[0]
check(zero(W[0,0]-A.det()),'no-archive Slater amplitude is det(A)')
check(zero(p_empty-(I2-z*F).det()),'Book survival determinant is ONE Born record')
check(p_empty<1 and p_empty>(1-z)**2,'strict Book archive event range')
check(1-p_empty>0 and sum(p[1:])==1-p_empty,'all five failure alternatives retained')

# SAME original active/archive split: the true original leakage K can be
# retained at a weakened amplitude WITHOUT any additional destination modes.
sqrt_z=r(1,1024)
K=B/sqrt_z
real_original_F=K.T*K
check(real_original_F==F,'the actual K dagger K effect is unchanged')
column=A.col_join(sqrt_z*K)
check(column.T*column==I2,'native P plus its SAME original Q is an isometry')
check(U[:,:2]==column,'the full closed SO4 unitary completes that prepared column')
check(K.det()!=0 and B.det()!=0,'rank2 original Q destination is minimal for full-rank K')
# Noncommuting honest variation of the ORIGINAL K leg, solving the unique
# positive-root Sylvester equation for the moving active prepared leg.
L=S.Matrix([[r(1,17),r(1,19)],[-r(1,23),r(1,29)]])
dF=K.T*L+L.T*K
check(dF*F!=F*dF,'true moving archive K has noncommuting field source')
xx=S.symbols('x00 x01 x10 x11')
X=S.Matrix(2,2,xx)
sol=S.solve(list(A*X+X*A+z*dF),list(xx),dict=True)
check(len(sol)==1,'unique derivative of positive active block')
dA=X.subs(sol[0])
check(zero(A*dA+dA*A+z*dF),'noncommuting positive-root Sylvester derivative')
dCol=dA.col_join(sqrt_z*L)
check(zero(column.T*dCol+dCol.T*column),'whole prepared column source remains normalized')

# Symbolic genuine source derivative with ORIGINAL ζ, not a fitted field.
t=S.symbols('t',real=True)
aa,bb=amplitudes(t)
At=O*S.diag(aa,a2)*O.T
Bt=O*S.diag(bb,b2)*O.T
Ft=Bt*Bt/z
survival=S.factor(At.det()**2)
survival_source=S.factor(-S.diff(survival,t)/survival)
trace_source=z*S.trace((I2-z*Ft).inv()*Ft.diff(t))
check(zero(survival_source-trace_source),'real moving field Born source equals full Book first source')
check(S.simplify(survival_source.subs(t,t1))!=0,'readout has nonzero true source')

# Ordinary one-particle Born with direct-sum channels is NOT the Book
# determinant; filled many-fermion occupancy is the load-bearing input.
psingle=1-z*S.trace(F)/2
check(zero(psingle-p_empty)==False,'single-particle Born cannot replace all-mode Book')
check(p_empty!=(1-z*F[0,0])*(1-z*F[1,1]),
      'offdiagonal F cannot be assigned independent physical basis modes')

print(json.dumps({
    'status':'PASS_EXACT_CLOSED_FERMI_SLATER_BOOK_NO_RETURN_BORN',
    'checks':checks,
    'zeta':'1/1048576',
    'original_active_dim':2,
    'closed_one_particle_dim':4,
    'closed_two_particle_dim':6,
    'all_six_born_outcomes_nonzero':True,
    'all_six_outcome_sum_exactly_one':True,
    'no_return_Book_probability':str(p_empty),
    'no_return_probability_numeric':str(S.N(p_empty,22)),
    'archive_escape_probability_numeric':str(S.N(1-p_empty,22)),
    'positive_full_CAR_and_no_archive':True,
    'physically_admitted_original_D0_word':False,
    'GR_closed':False
},sort_keys=True,indent=2))
