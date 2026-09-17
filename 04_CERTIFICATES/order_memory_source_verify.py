#!/usr/bin/env python3
"""Exact source-to-port construction and adverse controls, 2026-09-08."""
from pathlib import Path
from cert_runtime import output_path
import hashlib
import json
import sympy as S

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
paths = [
    "03_FORMALIZATION/D0/Integration/V15/RawZone.lean",
    "03_FORMALIZATION/D0/Representation/OrderMemoryReadout.lean",
    "03_FORMALIZATION/D0/Representation/SourcePortPreparation.lean",
    "03_FORMALIZATION/D0/Representation/PreparationMemoryBound.lean",
    "03_FORMALIZATION/D0/Representation/PortFrameCovariance.lean",
]
texts = [(ROOT/p).read_text() for p in paths]


def matrix(text, marker):
    body = text.split(marker,1)[1].split("!![",1)[1].split("]",1)[0]
    return S.Matrix([[S.sympify(x) for x in row.split(",")] for row in body.split(";")])


checks = []


def check(name, value):
    if not bool(value):
        raise AssertionError(name)
    checks.append(name)


def eq(A,B):
    if isinstance(A,S.MatrixBase):
        return all(S.simplify(x)==0 for x in A-B)
    return S.simplify(A-B)==0


D=matrix(texts[0],"def DW")
A=matrix(texts[0],"def AW")
G=matrix(texts[0],"def Gq")
P=matrix(texts[0],"def Pact")
P0=matrix(texts[0],"def P0")
K=D*A-A*D
check("active projector really comes from source commutator",P==-K*K/2840)
E=(D-22*S.eye(3))*(D-20*S.eye(3))/8
C=P*E*P
R=C/S.trace(C)
Q=P-R
Z=S.eye(3)-2*R
check("normalization from source",S.trace(C)==S.Rational(567,710))
check("input port matches Lean explicit matrix",Q==matrix(texts[2],"theorem inputPort_explicit"))
for name,port in (("signal",R),("input",Q)):
    check(f"{name} idempotent",port*port==port)
    check(f"{name} metric self-adjoint",port.T*G==G*port)
    check(f"{name} rank one",port.rank()==1)
check("complementary active ports",Q+R==P and Q*R==S.zeros(3))
check("reversal preserves source metric",Z.T*G*Z==G)
check("reversal reverses generator",Z*K*Z==-K)
check("neutral sector is retained",Z*P0==P0)
q=S.Matrix([0,1,2]); r=K*q
check("old energy frame recovered",Q*q==q and R*r==r and Q*r==S.zeros(3,1))
check("all projected states have the recovered direction",Q==q*S.Matrix([[0,S.Rational(11,63),S.Rational(26,63)]]))

left=matrix(texts[1],"def left")
a,b,c,d=S.symbols("a b c d")
Li=left.subs({a:0,b:1,c:0,d:0})
Lj=left.subs({a:0,b:0,c:1,d:0})
X=S.kronecker_product(S.eye(3)-R,S.eye(4))+S.kronecker_product(R,Li)
G12=S.kronecker_product(G,S.eye(4))
H=S.kronecker_product(R,Li)
check("interaction generator is metric skew",H.T*G12==-G12*H)
check("interaction generator square",H*H==-S.kronecker_product(R,S.eye(4)))
check("local action is exact quarter-turn polynomial",X==S.eye(12)+H+H*H)
check("interaction generator cubic",H**3==-H)
check("coupling metric conservation",X.T*G12*X==G12)
check("coupling square is source reversal",X*X==S.kronecker_product(Z,S.eye(4)))
check("coupling fourth power identity",X**4==S.eye(12))
realigned=S.Matrix(9,16,lambda u,v:X[(u//3)*4+v//4,(u%3)*4+v%4])
check("coupling requires interaction: operator Schmidt rank two",realigned.rank()==2)
minor=X[0,0]*X[4,5]-X[0,1]*X[4,4]
check("exact nonseparability witness",minor==S.Rational(5657,8946))

lam=S.sqrt(2840); p=(S.sqrt(5)-1)/2
F=S.Matrix.hstack(q,r/lam)
U=P0+S.sqrt(p)*P+p*K/lam
golden=S.Matrix([[S.sqrt(p),-p],[p,S.sqrt(p)]])
check("source frame has one common normalization",eq(F.T*G*F,63*S.eye(2)))
check("golden source flow intertwines",eq(U*F,F*golden))
F12=S.kronecker_product(F,S.eye(4))
check("local port gate intertwines with previous apparatus",eq(X*F12,F12*S.diag(S.eye(4),Li)))
check("common j intertwines",eq(S.kronecker_product(S.eye(3),Lj)*F12,F12*S.diag(Lj,Lj)))
check("source neutral input never leaks into prepared active frame",eq(S.kronecker_product(P0,S.eye(4))*F12,S.zeros(12,8)))

# Selected preparation is not free resetting: conserve the full complement.
fail=S.eye(3)-Q
check("selected plus failed responses conserve input",Q.T*G*Q+fail.T*G*fail==G)
check("both branches reconstruct input",Q+fail==S.eye(3))
check("preparation has a real failure case",Q*S.Matrix([1,0,0])==S.zeros(3,1))
check("failure archive keeps that input",fail*S.Matrix([1,0,0])==S.Matrix([1,0,0]))
v0,v1,v2=S.symbols("v0 v1 v2",real=True)
incoming=S.Matrix([v0,v1,v2])
check("preparation response is explicit",eq((incoming.T*Q.T*G*Q*incoming)[0],(11*v1+26*v2)**2/63))

# Maximum degree is an explicit rule, not a falsely proved unique M1 choice.
# Alternative source projectors exist, yet each reverses the same planar flow.
alternatives=[]
for deg in (24,22,20):
    spectral=S.eye(3)
    for other in (24,22,20):
        if other!=deg:
            spectral=spectral*(D-other*S.eye(3))/(deg-other)
    compressed=P*spectral*P
    port=compressed/S.trace(compressed)
    flip=S.eye(3)-2*port
    check(f"degree {deg}: reflection reverses the same source flow",flip*K*flip==-K)
    check(f"degree {deg}: rank-one positive-metric port",port.rank()==1 and port.T*G==G*port)
    alternatives.append(port)
check("source frames are not uniquely selected by existence",len({tuple(x) for x in alternatives})==3)

# Universal planar identity, not inference from the three examples.
u,v=S.symbols("u v")
J=S.Matrix([[0,-1],[1,0]])
reflection=S.Matrix([[1-2*u,-2*v],[-2*v,2*u-1]])
check("every frame: anticommutation identity",eq(reflection*J,-J*reflection))
ideal=S.groebner([u*u+v*v-u],u,v)
check("every orthogonal port: reflection involution",all(ideal.reduce(S.expand(x))[1]==0 for x in reflection*reflection-S.eye(2)))
check("every orthogonal port: same flow reversal",all(ideal.reduce(S.expand(x))[1]==0 for x in reflection*J*reflection+J))

result={
    "status":"PASS", "checks_passed":len(checks), "checks":checks,
    "scope":"Source-derived port and coupling representation; selective preparation; no physical-actuation or M1-uniqueness promotion.",
    "source_sha256":{path:hashlib.sha256(text.encode()).hexdigest() for path,text in zip(paths,texts)},
    "input_port":[[str(x) for x in Q.row(i)] for i in range(3)],
    "interaction_minor":str(minor), "operator_schmidt_rank":2,
    "unproved_physical_step":"Realize the derived coupled operator, not merely independent scene and memory operators.",
}
output_path(__file__, "source_verification.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k not in ("checks","source_sha256","input_port")},ensure_ascii=False,indent=2))
