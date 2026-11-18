"""All-column checks against the literal pinned D0 G/CX/SourceI compiler."""
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from sympy import Matrix, eye, diag, sqrt, kronecker_product as kron
from sympy.polys.matrices import DomainMatrix

default=Path(__file__).resolve().parent / "primary" / "native_execution.py"
owner=Path(sys.argv[1]) if len(sys.argv)>1 else default
sha=hashlib.sha256(owner.read_bytes()).hexdigest()
assert sha=="222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
spec=importlib.util.spec_from_file_location("diamond_pinned_native",owner)
native=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=native
spec.loader.exec_module(native)
K=native.GOLDEN_FIELD
p,a=native.P,native.A
v=Matrix([a,p])
bus,spin1,spin2,data,old,b=range(6)
source=native.Gate("SourceI",(bus,spin1,spin2))
def cx(x,y):return native.Gate("CX",(x,y))
def swap(x,y):return (cx(x,y),cx(y,x),cx(x,y))
def phase_route(x,k):
    r=swap(bus,x)
    return r+(source,)*k+r
def execution(word):
    return native.Execution(6,(b,),(old,),tuple(word),native.G_CX_SOURCE_I,bus,(spin1,spin2))
def exact(m):
    return DomainMatrix.from_Matrix(m).convert_to(K).to_sparse()
def compiled(word):
    return exact(native.word_matrix(execution(word),max_qubits=6,max_expanded_stages=1500))
cz=phase_route(b,1)+phase_route(data,1)+(cx(b,data),)+phase_route(data,3)+(cx(b,data),)
wp=cz+(cx(b,data),)
wm=(cx(b,data),)+cz
g=native.Gate("G",(b,))
inv=native.inverse_word(execution((g,)),max_qubits=6,max_expanded_stages=100)
rf=inv+phase_route(b,2)+(g,)
assert compiled(rf)==exact(kron(eye(32),2*v*v.T-eye(2)))
# Chronological action is right to left on the column state.
def amp(t,m):
    w,u=(wp,wm) if t==1 else (wm,wp)
    return w+(rf+u+rf+w)*m
em=exact(kron(eye(32),v))
X=Matrix([[0,1],[1,0]])
expected_x=kron(eye(2**data),X,eye(2))
measure=exact(kron(eye(2**data),diag(0,1),eye(4)))
i64=exact(eye(64))
base=p**2+p**4
report=[]
for m in (0,2):
    vp,vm=compiled(amp(1,m)),compiled(amp(-1,m))
    assert vm==vp.transpose() and vp*vm==i64 and vm*vp==i64
    mid=em.transpose()*(vp.transpose()*measure*vp-vm.transpose()*measure*vm)*em
    k=0 if m==0 else 782624-350000*sqrt(5)
    assert mid==exact(k*expected_x)
    report.append({"even_m":m,"all_columns":64,"one_word_gates":len(amp(1,m)),"midpoint_effect_x_factor":str(k),"input_columns":32})
print(json.dumps({"status":"PASS","owner_sha256":sha,"R_gates":len(rf),"variants":report,
                  "native_gate_programmes_audited":True,"physical_C_established":False},indent=2))
