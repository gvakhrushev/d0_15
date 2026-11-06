#!/usr/bin/env python3
"""Exact source and critical-set controls; no new physical admission claim."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
import sympy as s
from sympy.polys.matrices import DomainMatrix

OWNER_REL = Path('02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py')
ROOT = next((p for p in [Path.cwd(), *Path(__file__).resolve().parents]
             if (p / OWNER_REL).is_file()), None)
if ROOT is None:
    raise RuntimeError('Run from the repository or install this checker within it')
OWNER = ROOT / OWNER_REL
OWNER_SHA = '222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c'

def require(ok, label):
    if not ok:
        raise RuntimeError(label)

def zero(M):
    return all(s.cancel(s.expand(v)) == 0 for v in M)

def reflection(cosines, sines):
    A, B = s.diag(*cosines), s.diag(*sines)
    return A.row_join(B).col_join(B.row_join(-A))

def full_source(P, T, dP, dT, z):
    I = s.eye(P.rows)
    C = (I-P)*T*P
    dC = -dP*T*P+(I-P)*dT*P+(I-P)*T*dP
    F = C.adjoint()*C
    dF = dC.adjoint()*C+C.adjoint()*dC
    return s.cancel(z*s.trace((I-z*F).inv()*dF))

def antihermitian_basis(n):
    for i in range(n):
        X = s.zeros(n); X[i,i] = s.I
        yield X
        for j in range(i):
            X = s.zeros(n); X[i,j] = 1; X[j,i] = -1
            yield X
            X = s.zeros(n); X[i,j] = s.I; X[j,i] = s.I
            yield X

def source_case(cosines, sines, z=s.Rational(1,4)):
    r = len(cosines); d=2*r
    P=s.diag(*([1]*r+[0]*r)); T=reflection(cosines,sines)
    require(zero(T*T-s.eye(d)) and T.adjoint()==T, 'whole reflection')
    A=T[:r,:r]; R=((1-z)*s.eye(r)+z*A*A).inv()
    XA=T*P*T*P-P*T*P*T  # [T,PTP]
    require(XA.adjoint()==-XA, 'anti-Hermitian detecting generator')
    dT=XA*T-T*XA
    require(zero(dT[:r,:r]+2*A*(s.eye(r)-A*A)), 'full corner derivative')
    expected=s.cancel(4*z*s.trace(R*A*A*(s.eye(r)-A*A)))
    actual=full_source(P,T,s.zeros(d),dT,z)
    require(actual==expected, 'full original determinant source')
    all_rows=[]
    for X in antihermitian_basis(d):
        dT=X*T-T*X
        original=full_source(P,T,s.zeros(d),dT,z)
        reduced=s.cancel(-2*z*s.trace(R*A*dT[:r,:r]))
        require(original==reduced, 'all complex relative source directions')
        dP=X*P-P*X
        require(full_source(P,T,dP,dT,z)==0, 'full moving-cut covariance')
        all_rows.append(original)
    critical=all(c in (-1,0,1) for c in cosines)
    require(all(x==0 for x in all_rows)==critical, 'critical iff projection escape')
    return {'rank':r,'cosines':[str(c) for c in cosines],
            'positive_source':str(actual),'directions':len(all_rows),
            'critical':critical}

cases=[
    source_case([s.Rational(3,5)],[s.Rational(4,5)]),
    source_case([s.Rational(3,5),-s.Rational(3,5)],[s.Rational(4,5)]*2),
    source_case([s.Rational(3,5),-s.Rational(5,13),s.Rational(8,17)],
                [s.Rational(4,5),s.Rational(12,13),s.Rational(15,17)]),
    source_case([s.Integer(1),s.Integer(0),s.Integer(-1)],
                [s.Integer(0),s.Integer(1),s.Integer(0)]),
]

# The old [T,P] detector can cancel between opposite compression eigenvalues.
P=s.diag(1,1,0,0); T=reflection([s.Rational(3,5),-s.Rational(3,5)], [s.Rational(4,5)]*2)
X0=T*P-P*T; XA=T*P*T*P-P*T*P*T
wrong=full_source(P,T,s.zeros(4),X0*T-T*X0,s.Rational(1,4))
right=full_source(P,T,s.zeros(4),XA*T-T*XA,s.Rational(1,4))
require(wrong==0 and right==s.Rational(96,175), 'mixed-sign hostile control')

# A nontrivially moving stationary section retains its exact, constant full det.
t=s.symbols('t', real=True)
cs=(1-t*t)/(1+t*t); sn=2*t/(1+t*t)
V=s.Matrix([[cs,0,-sn,0],[0,1,0,0],[sn,0,cs,0],[0,0,0,1]])
P0=s.diag(1,1,0,0); T0=reflection([1,0],[0,1])
Pt=V*P0*V.T; Tt=V*T0*V.T
C=(s.eye(4)-Pt)*Tt*Pt; F=C.T*C
det=s.cancel((s.eye(4)-s.Rational(1,4)*F).det())
require(det==s.Rational(3,4), 'stationary section full determinant constant')
require(s.diff(det,t)==0, 'stationary reduced first and second source zero')

# Consume the actual native 26-stage, 32-column reflection from §7cu.
require(hashlib.sha256(OWNER.read_bytes()).hexdigest()==OWNER_SHA,'native owner pin')
spec=importlib.util.spec_from_file_location('native_query_stationarity_owner',OWNER)
n=importlib.util.module_from_spec(spec); sys.modules[spec.name]=n; spec.loader.exec_module(n)
field=n.GOLDEN_FIELD
def golden_zero(M):
    return DomainMatrix.from_Matrix(s.Matrix(M)).convert_to(field).is_zero_matrix
port,q=0,1; spin=(2,3); old=(4,); SI=n.Gate('SourceI',(port,*spin))
swap=(n.Gate('CX',(port,q)),n.Gate('CX',(q,port)),n.Gate('CX',(port,q)))
def ex(word): return n.Execution(5,(port,q),old,tuple(word),n.G_CX_SOURCE_I,port,spin)
Vword=swap+(n.Gate('G',(port,)),)+swap
Vinv=n.inverse_word(ex(Vword),max_qubits=5,max_expanded_stages=1000)
Zword=swap+(SI,SI)+swap
obj=ex(Vinv+Zword+Vword)
n.validate_execution(obj,max_qubits=5,max_expanded_stages=1000)
inv=n.inventory(obj,max_qubits=5,max_expanded_stages=1000)
require((inv.gate_count,inv.g_count,inv.cx_count,inv.source_i_count,inv.cut_rank)==(26,2,18,6,8),'native inventory')
Tn=s.Matrix(n.word_matrix(obj,max_qubits=5,max_expanded_stages=1000))
i=s.Matrix(n.input_isometry(obj,max_qubits=5,max_expanded_stages=1000))
Pn=i*i.T; An=Pn*Tn*Pn; Xn=Tn*An-An*Tn
c=n.P**3
require(golden_zero(Tn*Tn-s.eye(32)) and Tn.T==Tn,'native whole reflection')
require(golden_zero(i.T*Tn*i-c*s.eye(8)),'native scalar compression')
require(golden_zero(i.T*(Xn*Tn-Tn*Xn)*i+2*c*(1-c*c)*s.eye(8)), 'native detecting direction exact')
native_positive=s.simplify(4*8*s.Rational(1,4)*c*c*(1-c*c)/(s.Rational(3,4)+s.Rational(1,4)*c*c))
def positive_in_q_sqrt5(value, label):
    value=s.expand(value)
    b=value.coeff(s.sqrt(5)); a=s.expand(value-b*s.sqrt(5))
    require(a.is_Rational and b.is_Rational and a<0 and b>0 and 5*b*b>a*a,label)
positive_in_q_sqrt5(native_positive,'native strictly nonzero exact algebraic source')
z_native=s.Rational(1,2**20)
native_original=s.simplify(4*8*z_native*c*c*(1-c*c)/(1-z_native+z_native*c*c))
positive_in_q_sqrt5(native_original,'original z native strictly nonzero exact algebraic source')

result={'status':'PASS','sympy':s.__version__,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'input_commit':'172876cdf38bfce6f87fdd4a059d524b60c10eb9','native_owner_sha256':OWNER_SHA,
        'exact_matrix_cases':cases,'tested_complex_relative_directions':sum(x['directions'] for x in cases),
        'mixed_sign_old_detector':str(wrong),'mixed_sign_positive_detector':str(right),
        'moving_stationary_section_det':str(det),
        'native_query':{'stages':26,'full_dimension':32,'active_rank':8,'compression':'p^3 I_8',
                        'positive_source_at_z_1_4':str(native_positive),
                        'positive_source_at_original_z_2_neg_20':str(native_original)},
        'scope':'Exact finite full-source identities and actual native base; full orbit physical admission not asserted; heat theorem consumed, not replayed; no GR closure.'}
print(json.dumps(result,indent=2,sort_keys=True))
