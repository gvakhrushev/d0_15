"""Independent exact one-bit pre-seal instrument and scalar stopped/cap-two formulas."""
import json, math
import sympy as S
from sympy.polys.matrices import DomainMatrix

p=(S.sqrt(5)-1)/2; a=S.sqrt(p)
F=S.QQ.algebraic_field(a)
def dm(M): return DomainMatrix.from_Matrix(M).convert_to(F)
def eq(A,B): assert dm(A)==dm(B)
I=S.eye(2); X=S.Matrix([[0,1],[1,0]]); Z=S.diag(1,-1)
A0,A1=p*I-p**2*X,a*p*(I+X)
B0,B1=p*I+p**2*X,-a*p*(I-X)
H=(B0*A1,B1*A0,B0*A0,B1*A1)
expect=(a*p*(I+X),-a*p*(I-X),p**3*I,S.zeros(2))
for T,U in zip(H,expect): eq(T,U)
s=4*p**3
law=(s/2,s/2,1-s,0)
for T,m in zip(H,law):
    eq(S.diag(*((T.T*T).diagonal())),m*I)
eq(sum((T.T*T for T in H),S.zeros(2)),I)
# A nontrivial DATA channel: two amplitude-damping branches. The copied
# environment is fully retained. Use rational coefficients (3,4,5).
K=(S.diag(1,S.Rational(3,5)),S.Matrix([[0,S.Rational(4,5)],[0,0]]))
for T,m in zip(H,law):
    Y=sum((S.kronecker_product(I[:,j],T[:,j],K[j]) for j in range(2)),S.zeros(8,2))
    eq(Y.T*Y,m*I)
    for i in range(2):
        for j in range(2):
            density=I[:,i]*I[:,j].T
            full=Y*density*Y.T
            reduced=sum((full[2*k:2*k+2,2*k:2*k+2] for k in range(4)),S.zeros(2))
            eq(reduced,m*sum((k*density*k.T for k in K),S.zeros(2)))
q,Hm,g=S.symbols("q H_m g",positive=True)
h=-q*S.log(q)-(1-q)*S.log(1-q)
assert S.simplify(S.diff((h+Hm)/(1-q),q)-(Hm-S.log(q))/(1-q)**2)==0
assert S.simplify(S.diff((1+g+q)/(1-q),q)-(g+2)/(1-q)**2)==0
assert S.simplify(S.diff((1+q)*(Hm+h),q)-(Hm+h+(1+q)*S.log((1-q)/q)))==0
assert S.simplify(S.diff((1+q)*(1+g+q),q)-(g+2+2*q))==0
p0=float(p); ss=4*p0**3; qq=ss*9/640
HH=-6*(ss*math.log(ss/2)+(1-ss)*math.log(1-ss))
hb=-qq*math.log(qq)-(1-qq)*math.log(1-qq)
dinf=(HH-math.log(qq))/(1-qq)**2; d2=HH+hb+(1+qq)*math.log((1-qq)/qq)
units=math.log(1/p0)
print(json.dumps(dict(status="PASS",three_outcomes=[ss/2,ss/2,1-ss],H6_nats=HH,q=qq,
    infinite=dict(C_slope=56/(1-qq)**2,I_nats_slope=dinf,I_base_phi_slope=dinf/units),
    cap2=dict(C_slope=56+2*qq,I_nats_slope=d2,I_base_phi_slope=d2/units),
    scope="Coherent accessible j and fresh blank E before compulsory readout; declared uniform gate count."),indent=2))
