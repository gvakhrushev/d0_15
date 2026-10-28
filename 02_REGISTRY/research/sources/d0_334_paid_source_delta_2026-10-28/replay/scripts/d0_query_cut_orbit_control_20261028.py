"""Exact rational 2x2 verification of independent QUERY and moving-cut rows.
No claim of physical admission of either variation.
"""
from pathlib import Path
import sympy as S
import hashlib,json
c=S.Rational(3,5);u=S.Rational(4,5);z=S.Rational(1,4)
I=S.eye(2);P=S.diag(1,0);E=I-P;U=S.Matrix([[c,u],[u,-c]])
K=U*P-P*U
assert U.T==U and U*U==I and K.T==-K
vU=K*U-U*K;vP=K*P-P*K
C=E*U*P; F=C.T*C;res=(I-z*F).inv()
def dJ(dU,dP):
 dC=-dP*U*P+E*dU*P+E*U*dP
 return S.simplify(2*z*S.trace(res*C.T*dC))
query=dJ(vU,S.zeros(2));cut=dJ(S.zeros(2),vP);joint=dJ(vU,vP)
assert query==S.Rational(16,35) and cut==S.Rational(-16,35) and joint==0
assert S.simplify(F[0,0]-(1-c*c))==0
assert S.simplify(4*z*c*u*u/(1-z+z*c*c)-query)==0
# Stronger check dF=[K,F]: simultaneous conjugation of complete escape operator.
dC=-vP*U*P+E*vU*P+E*U*vP
dF=dC.T*C+C.T*dC
assert dF==K*F-F*K
print(json.dumps({'status':'PASS','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'carrier':'rational 2x2; P rank 1, z=1/4','c':'3/5','u':'4/5','query_first_source_fixed_cut':str(query),'moving_cut_first_source_fixed_U':str(cut),'joint_first_source':str(joint),'simultaneous_dF':'[K,F]','scope':'finite operator identity only; no admitted physical variation, field map or GR closure'},indent=2))
