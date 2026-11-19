"""Exact finite-cap measured rewind for the pinned native D0 WORK diamond.

Usage: python3 check_rewind.py [path/to/native_execution.py]
The operator checks enumerate both signs and all leaves through three cycles.
The Shannon expression is verified by exact expected counts of log(s), log(u).
"""
from math import log
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import sympy as sp
from sympy.polys.matrices import DomainMatrix

default = Path(__file__).resolve().parent / "primary" / "native_execution.py"
owner = Path(sys.argv[1]) if len(sys.argv)>1 else default
source_hash = hashlib.sha256(owner.read_bytes()).hexdigest()
assert source_hash == "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
module = importlib.util.spec_from_file_location("rewind_native",owner)
native = importlib.util.module_from_spec(module)
sys.modules[module.name] = native
module.loader.exec_module(native)
K = native.GOLDEN_FIELD
p, a = native.P, native.A
s0 = p**2 + p**4
s = K.from_sympy(s0)
u = K.one-s
k = s*s+u*u
assert u == K.from_sympy(2*p**3)
assert K.one-k == 2*s*u

def exact(mat):
    return DomainMatrix.from_Matrix(mat).convert_to(K).to_sparse()

bus,spin1,spin2,data,old,b = range(6)
source = native.Gate("SourceI",(bus,spin1,spin2))

def cx(x,y): return native.Gate("CX",(x,y))
def swap(x,y): return (cx(x,y),cx(y,x),cx(x,y))
def routed(x,n): return swap(bus,x)+(source,)*n+swap(bus,x)

cz = routed(b,1)+routed(data,1)+(cx(b,data),)+routed(data,3)+(cx(b,data),)
v = sp.Matrix([a,p])
vperp = sp.Matrix([-p,a])
basis = [exact(sp.kronecker_product(sp.eye(32),x)) for x in (v,vperp)]
identity = exact(sp.eye(32))
d0 = exact(sp.kronecker_product(sp.eye(8),sp.diag(0,1),sp.eye(2)))
x_effect = exact(sp.kronecker_product(sp.eye(8),sp.Matrix([[0,1],[1,0]]),sp.eye(2)))
povm_sample = [d0, x_effect]
# Nondemolition P-reader: birth pointer in v, rotate both to read basis,
# copy, restore b to its original golden frame. Pointer readout is classical.
r=6
def read_ex(word):
    return native.Execution(7,(b,r),(old,),tuple(word),native.G_CX_SOURCE_I,bus,(spin1,spin2))
def inv_g(q):
    return native.inverse_word(read_ex((native.Gate("G",(q,)),)),max_qubits=7,max_expanded_stages=100)
read_word=inv_g(b)+inv_g(r)+(cx(b,r),native.Gate("G",(b,)))
reader=exact(native.word_matrix(read_ex(read_word),max_qubits=7,max_expanded_stages=100))
pointer_birth=exact(sp.kronecker_product(sp.eye(64),v))
for bit,bvec in enumerate([v,vperp]):
    extract=exact(sp.kronecker_product(sp.eye(64),sp.eye(2)[:,bit].T))
    projector=exact(sp.kronecker_product(sp.eye(32),bvec*bvec.T))
    assert extract*reader*pointer_birth==projector
assert len(read_word)==24
native_checks = {}
for sign,word in ((1,cz+(cx(b,data),)),(-1,(cx(b,data),)+cz)):
    ex = native.Execution(6,(b,),(old,),tuple(word),native.G_CX_SOURCE_I,bus,(spin1,spin2))
    W = exact(native.word_matrix(ex,max_qubits=6,max_expanded_stages=100))
    logical = sp.eye(64)-sp.kronecker_product(sp.eye(32),sp.diag(0,1))
    J = sp.Matrix([[0,-1],[1,0]])
    logical += sp.kronecker_product(sp.eye(8),sign*J,sp.eye(2),sp.diag(0,1))
    assert W==exact(logical)
    # Dilation and all four compressed blocks of the physical W / W*;
    # the fixed frame rotation does not imply that reading P is free.
    fwd = [[out.transpose()*W*inp for inp in basis] for out in basis]
    rev = [[fwd[j][i].transpose() for j in range(2)] for i in range(2)]
    A,B = fwd[0][0],fwd[1][0]
    assert A.transpose()*A==identity.scalarmul(s)
    assert B.transpose()*B==identity.scalarmul(u)
    assert A==exact(sp.kronecker_product(sp.eye(8),p*sp.eye(2)+sign*p**2*J,sp.eye(2)))
    assert B==exact(sp.kronecker_product(sp.eye(8),a*p*(sign*J-sp.eye(2)),sp.eye(2)))
    caps=[]
    for cap in range(4):
        # Each row carries the probability monomial s^ns u^nu.
        leaves = [((0,), A, 1, 0, K.one)]
        waiting = [((1,), B, 0, 1, K.one)]
        for _ in range(cap):
            next_waiting = []
            for prefix,op,ns,nu,weight in waiting:
                for mid in (0,1):
                    for end in (0,1):
                        actual = fwd[end][mid]*rev[mid][1]*op
                        # Global phase is - on the two-step successful (1,0) route.
                        if end==0:
                            factor = -u if mid==1 else u
                            new_weight = weight*factor
                            assert actual==A.scalarmul(new_weight)
                            new = (prefix+(mid,end),actual,ns+1,nu+1,new_weight)
                            leaves.append(new)
                        else:
                            factor = u if mid==0 else s
                            new_weight = weight*factor
                            assert actual==B.scalarmul(new_weight)
                            new = (prefix+(mid,end),actual,ns+2*(mid==1),nu+2*(mid==0),new_weight)
                            next_waiting.append(new)
            waiting = next_waiting
        leaves.extend(waiting)
        mass=fail=Es=Eu=Er=K.zero
        sign_norm_squares = [K.zero,K.zero]
        pullbacks=[identity.scalarmul(K.zero) for _ in povm_sample]
        for bits,op,ns,nu,weight in leaves:
            P_leaf=s**ns*u**nu
            assert op.transpose()*op==identity.scalarmul(P_leaf)
            mass+=P_leaf
            Es+=ns*P_leaf
            Eu+=nu*P_leaf
            Er+=len(bits)*P_leaf
            fail += (bits[-1]==1)*P_leaf
            sign_norm_squares[bits[-1]]+=weight*weight
            for j,E in enumerate(povm_sample):
                pullbacks[j]=pullbacks[j]+op.transpose()*E*op
        reads=K.one+2*u*sum((k**i for i in range(cap)),K.zero)
        assert mass==K.one and fail==u*k**cap
        # In the minimum coherent dilation, all fine addresses of a given final
        # status form ONE coherent label vector. The two vectors are orthogonal.
        assert s*sign_norm_squares[0]==K.one-fail
        assert u*sign_norm_squares[1]==fail
        assert Er==reads and Es==s*reads and Eu==u*reads
        for E, result in zip(povm_sample,pullbacks):
            predicted=(A.transpose()*E*A).scalarmul((K.one-fail)/s)+(B.transpose()*E*B).scalarmul(fail/u)
            assert result==predicted
        sval=float(K.to_sympy(s))
        fval=float(K.to_sympy(fail))
        h=lambda x: -x*log(x)-(1-x)*log(1-x)
        caps.append({"cap":cap,"leaves":len(leaves),"fail_numeric":fval,"mean_marks":float(K.to_sympy(reads)),
                     "complete_CQ_mark_nats":h(sval)*float(K.to_sympy(reads)),"minimal_coherent_label_nats":h(fval)})
    native_checks[str(sign)]=caps
print(json.dumps({
    "status":"PASS","owner_sha256":source_hash,"all_compiled_dilation_columns":64,"all_input_columns":32,
    "nondemolition_reader":{"native_gates":len(read_word),"complete_matrix_columns":128,"true_pointer_birth_input_columns":64,
            "projection_verified":"both pointer outcomes, with restoration of the measured golden basis"},
    "signs_and_caps":native_checks,"s":"p^2+p^4","u":"1-s","k":"s^2+u^2",
    "failure_probability":"u*k^N","unconditioned_data_channel":"(1-u*k^N) U(.)U* + u*k^N F(.)F*",
    "register_shannon_nats":"(-s log(s)-u log(u))*(1+2*u*(1-k^N)/(1-k))",
    "CQ_entropy_with_external_reference":"S(output+reference)=S(input+reference)+H(complete classical marks)",
    "minimal_coherent_label_entropy":"h2(u*k^N) upon tracing out final orthogonal b status and all DATA, for coherent joint address label and no further untraced address copy",
    "success_rotation":"A/sqrt(s)","failure_rotation":"B/sqrt(u)",
    "sign_and_input_effect":"fine mark law, its entropy and expected mark count are independent of sign and initial DATA/reference state",
    "scope":"Native W and nondemolition pointer operators verified. Classical reading and adaptive routing are assumed on this measured extension. Their physical pricing, full clock and H.1 admission are separate."
},indent=2))
