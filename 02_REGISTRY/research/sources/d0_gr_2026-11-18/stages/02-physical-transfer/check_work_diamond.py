"""Replay the WORK diamond and its honest optional binary record.

Usage: python3 check_work_diamond.py [/path/to/native_execution.py]
The optional argument is the exact pinned primary source, never a replacement
gate library. The record calculation retains both outputs and the uninitialized
columns of the canonical-born hardware.
"""
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import sympy as sp

DEFAULT = Path(__file__).resolve().parent / "primary" / "native_execution.py"
owner = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
digest = hashlib.sha256(owner.read_bytes()).hexdigest()
assert digest == "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
spec = importlib.util.spec_from_file_location("diamond_native_owner", owner)
native = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = native
spec.loader.exec_module(native)
p, a = native.P, native.A
K = native.GOLDEN_FIELD
I = sp.eye(2)
J = sp.Matrix([[0,-1],[1,0]])
v, vp = sp.Matrix([a,p]), sp.Matrix([-p,a])
G = native.G_LOCAL
bus, spin1, spin2, data, old, b, reader = range(7)
source = native.Gate("SourceI",(bus,spin1,spin2))


def exact(x,y):
    assert native.exact_matrix_equal(x,y)


def cx(control, target):
    return native.Gate("CX",(control,target))


def swap(i,j):
    return (cx(i,j),cx(j,i),cx(i,j))


def routed(q, count):
    r = swap(bus,q) if q!=bus else ()
    return r + (source,)*count + r


def execution(gates, size):
    return native.Execution(size,tuple(range(5,size)),(old,),tuple(gates),
                            native.G_CX_SOURCE_I,bus,(spin1,spin2))


def inv_g(q,size):
    g = native.Gate("G",(q,))
    return native.inverse_word(execution((g,),size),max_qubits=size,max_expanded_stages=100)


def inventory(gates):
    return dict(sorted(Counter(gate.op for gate in gates).items()))


def lift2(local, axis, size):
    return sp.kronecker_product(sp.eye(2**axis), local, sp.eye(2**(size-axis-1)))


def full_matrix(gates, size):
    return native.word_matrix(execution(gates,size),max_qubits=size,max_expanded_stages=100)


cz = routed(b,1)+routed(data,1)+(cx(b,data),)+routed(data,3)+(cx(b,data),)
assert inventory(cz)=={"CX":20,"SourceI":5}
actual = {}
for sign,gates in ((1,cz+(cx(b,data),)),(-1,(cx(b,data),)+cz)):
    u = full_matrix(gates,6)
    select = lift2(sp.diag(0,1),b,6)
    logical = sp.eye(64)-select + select*lift2(sign*J,data,6)
    assert u==logical
    j0, j1 = sp.kronecker_product(sp.eye(32),v), sp.kronecker_product(sp.eye(32),vp)
    signed_j = lift2(sign*J,data,5)
    A = p*sp.eye(32)+p**2*signed_j
    B = a*p*(signed_j-sp.eye(32))
    exact(j0.T*u*j0,A)
    exact(j1.T*u*j0,B)
    exact(A.T*A,(p**2+p**4)*sp.eye(32))
    exact(B.T*B,2*p**3*sp.eye(32))
    exact(A.T*A+B.T*B,sp.eye(32))

    # Separate optional paid record. The two InvG calls rotate the control
    # back to its born basis and genuinely blank the fresh reporter.
    read = inv_g(b,7)+inv_g(reader,7)+(cx(b,reader),)
    assert inventory(read)=={"CX":13,"G":2,"SourceI":8}
    total = gates+read
    full = full_matrix(total,7)
    bproj0=lift2(sp.diag(1,0),b,7)
    bproj1=sp.eye(128)-bproj0
    pointer_x=lift2(sp.Matrix([[0,1],[1,0]]),reader,7)
    expected=(bproj0+bproj1*pointer_x)*lift2(G.T,reader,7)*lift2(G.T,b,7)*sp.kronecker_product(logical,I)
    # G.T introduces algebraic entries only in the two read rotations.
    exact(full,expected)
    input_j=sp.kronecker_product(sp.eye(32),v,v)
    # Compare each actual pair of output columns before squaring: |00> A,
    # |11> B, neither |01> nor |10> carries any part of the prepared input.
    prepared=full*input_j
    for label in range(4):
        decoder=sp.kronecker_product(sp.eye(32),sp.eye(4)[:,label]).T
        exact(decoder*prepared, {0:A,3:B}.get(label,sp.zeros(32)))
    actual[str(sign)]={"diamond":inventory(gates),"paid_record_total":inventory(total),
                       "diamond_calls":len(gates),"with_record_calls":len(total)}
# Test the two-position echo on every hardware column using real gates, without
# intermediate readers. Each address has the same fixed source port and DATA.
from itertools import product
def block_at(q, sign):
    phase = routed(q,1)+routed(data,1)+(cx(q,data),)+routed(data,3)+(cx(q,data),)
    return phase+(cx(q,data),) if sign==1 else (cx(q,data),)+phase

controls = (b, reader)
sign_patterns = list(product((1,-1), repeat=2))
forward, undo = {}, {}
for signs in sign_patterns:
    fg=tuple(g for q,t in zip(controls,signs) for g in block_at(q,t))
    bg=tuple(g for q,t in reversed(tuple(zip(controls,signs))) for g in block_at(q,-t))
    assert len(fg)==len(bg)==52
    forward[signs]=full_matrix(fg,7)
    undo[signs]=full_matrix(bg,7)
    assert undo[signs]==forward[signs].T

j2=sp.kronecker_product(sp.eye(32),v,v)
for t in sign_patterns:
    for u in sign_patterns:
        mismatch=[q for q,i,j in zip(controls,t,u) if i!=j]
        phase=sp.eye(128)
        for q in mismatch:
            phase=phase*lift2(sp.diag(1,-1),q,7)
        joint=undo[u]*forward[t]
        assert joint==phase
        exact(j2.T*joint*j2, p**(3*len(mismatch))*sp.eye(32))
print(json.dumps({"status":"PASS","native_owner_sha256":digest,"full_diamond_columns":64,
                  "full_record_columns":128,"two_position_exact_echo_pairs":16,"arbitrary_input_columns":32,
                  "q_good":"p^2+p^4","q_failure":"2*p^3","cases":actual,
                  "scope":"Complete hardware identities and paid coherent copy. Actual readout admission, full Cost-Info, H.1 and GR are separate."},indent=2))
