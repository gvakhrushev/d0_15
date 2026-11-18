"""Lueders read, inverse and capped physical Spin restoration, all four Spin inputs."""
from collections import Counter
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
from math import log
import sympy as sp
from sympy.polys.matrices import DomainMatrix

default=Path(__file__).resolve().parent / "primary" / "native_execution.py"
path=Path(sys.argv[1]) if len(sys.argv)>1 else default
sha=hashlib.sha256(path.read_bytes()).hexdigest()
assert sha=="222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
spec=importlib.util.spec_from_file_location("restoration_native",path)
native=importlib.util.module_from_spec(spec);sys.modules[spec.name]=native;spec.loader.exec_module(native)
field=native.GOLDEN_FIELD
def dm(x): return DomainMatrix.from_Matrix(x).convert_to(field).to_sparse()
v=sp.Matrix([native.A,native.P]); emb=dm(sp.kronecker_product(v,sp.eye(4)))
U=dm(native.SOURCE_I_LOCAL); Li=dm(native.L_I); I4=dm(sp.eye(4));I8=dm(sp.eye(8))
assert U**3==U.transpose() and Li**2==-I4
pin=emb*emb.transpose(); qin=I8-pin
s=field.from_sympy(native.P**2+native.P**4);u=field.one-s;k=s*s+u*u
A=[U.transpose()*pin*U,U.transpose()*qin*U]
sw=[s,u]
# Digit zero is the physical outcome P, digit one its true unsplit complement.
for b,pb in enumerate(sw):
    assert emb.transpose()*A[b]*emb==I4.scalarmul(pb)
assert emb.transpose()*U*emb==I4.scalarmul(field.from_sympy(native.P))+Li.scalarmul(field.from_sympy(native.P**2))
# States just after the initial return test. D is an unnormalised failure isometry.
D=qin*A[0]*emb
assert D.transpose()*D==I4.scalarmul(s*u)
assert qin*A[1]*emb==-D
def scalar_gram(op):
    gram=op.transpose()*op
    v=gram.to_dok().get((0,0),field.zero)
    assert gram==I4.scalarmul(v)
    return v
def expo(b,times1=1):return (times1,0) if b==0 else (0,times1)
def add(v,w):return (v[0]+w[0],v[1]+w[1])
report=[]
for cap in range(5):
    leaves=[]
    for b,pb in enumerate(sw):
        ok=pin*A[b]*emb; fail=qin*A[b]*emb
        assert ok==emb.scalarmul(pb)
        leaves.append((b,True,ok,expo(b,2),0))
        queue=[(fail,(1,1),0)]
        for _ in range(cap):
            rest=[]
            for op,e,n in queue:
                # m is absolute original outcome, rather than a readout of s_b.
                for m in (0,1):
                    state=A[m]*op
                    success=pin*state
                    failure=qin*state
                    norm=scalar_gram(op)
                    assert scalar_gram(success)==norm*s*u
                    assert scalar_gram(failure)==norm*sw[1-m]**2
                    # Every successful branch has EXACTLY the original Spin map up to scalar phase.
                    coeff=(emb.transpose()*success).to_dok()[(0,0)]
                    assert success==emb.scalarmul(coeff)
                    # All terminal failures occupy the same orthogonal full-bank isometric image.
                    cfail=(D.transpose()*failure).to_dok()[(0,0)]/(s*u)
                    assert failure==D.scalarmul(cfail)
                    leaves.append((b,True,success,add(e,(1,1)),n+1))
                    rest.append((failure,add(e,expo(1-m,2)),n+1))
            queue=rest
        leaves.extend((b,False,op,e,n) for op,e,n in queue)
    tot=[field.zero]*2;bad=[field.zero]*2;es=eu=cycles=field.zero
    for b,ok,op,e,n in leaves:
        probability=scalar_gram(op)
        assert probability==s**e[0]*u**e[1]
        assert sum(e)==2+2*n
        tot[b]+=probability
        bad[b]+=(not ok)*probability
        es+=e[0]*probability;eu+=e[1]*probability;cycles+=n*probability
    assert tot==sw and bad==[s*u*k**cap]*2
    assert cycles==field.one-k**cap
    reads=2*(field.one+cycles)
    assert es==s*reads and eu==u*reads
    val=lambda x: float(field.to_sympy(x))
    h=-sum(val(x)*log(val(x)) for x in sw)
    report.append({"cap":cap,"full_leaves":len(leaves),"failure":val(sum(bad,field.zero)),
                   "expected_forward_calls":1+val(cycles),"entropy_nats":val(reads)*h})
# Occupation matrices for a mixed bank not commuting with the physical L_i.
rho=dm(sp.diag(1,2,3,4)/10)
forward0=emb*rho*emb.transpose()
F_rho=(D*rho*D.transpose()).scalarmul(field.one/(s*u))
Xinf=forward0+F_rho
A0=A[0]
assert A0*Xinf==Xinf*A0
dephase=lambda x: pin*x*pin+qin*x*qin
assert dephase(U*Xinf*U.transpose())==U*Xinf*U.transpose()
for cap in range(4):
    X=forward0+F_rho.scalarmul(field.one-k**cap)
    real=dephase(U*X*U.transpose())-U*X*U.transpose()
    base=U*F_rho*U.transpose()
    assert real==(base-dephase(base)).scalarmul(k**cap)
# Coherent coin OR: the joint yes projector contains both alternatives;
# the two flags are not separately measured.
weights=[field.from_sympy(native.P),field.from_sympy(native.P**4)]
assert weights[0]+weights[1]==field.one-field.from_sympy(native.P**3)
assert 2*(weights[0]+weights[1])*(field.one-weights[0]-weights[1])==field.from_sympy(4*native.P**5)
coin_v=sp.kronecker_product(v,v)
Icoin=sp.eye(4); e0=sp.diag(1,1,0,0); e11=sp.diag(0,0,0,1)
Pphysical=sp.kronecker_product(v*v.T,sp.eye(4))
bigcheck=dm(sp.kronecker_product(e0,sp.eye(8))+sp.kronecker_product(e11,Pphysical))
bigcol=dm(sp.kronecker_product(coin_v,native.SOURCE_I_LOCAL*sp.kronecker_product(v,sp.eye(4))))
assert bigcol.transpose()*bigcheck*bigcol==I4.scalarmul(weights[0]+weights[1]*s)
print(json.dumps({"status":"PASS","owner_sha256":sha,"native_gate":"controlled actual 4x4 quaternion L_i (8x8 SourceI); physical inverse uses 3 SourceI calls",
                  "all_spin_input_columns":4,"entangled_reference_extension":"all-column scalar Gram and scalar success Kraus",
                  "caps":report,"coherent_double_coin_collar_and_occupation_matrices":"PASS","physical_C_established":False},indent=2))
