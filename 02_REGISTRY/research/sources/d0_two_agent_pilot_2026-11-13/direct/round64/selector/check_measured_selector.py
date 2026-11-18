"""Replay both measured arms on the project’s exact native matrices."""
from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import product
from pathlib import Path
import sys

import sympy as sp
from sympy.polys.matrices import DomainMatrix


root = Path(__file__).resolve().parents[7]
source = root / "02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py"
assert sha256(source.read_bytes()).hexdigest() == "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
spec = importlib.util.spec_from_file_location("native_selector_source", source)
nt = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = nt
spec.loader.exec_module(nt)


def cx(i, j):
    return nt.Gate("CX", (i, j))


def z(wire, spin):
    swap = (cx(0, wire), cx(wire, 0), cx(0, wire))
    return swap + (nt.Gate("SourceI", (0, *spin)),)*2 + swap


def execution(count, gates):
    return nt.Execution(count, (), (), tuple(gates), nt.G_CX_SOURCE_I, 0, (count-2, count-1))


def over_field(m):
    return DomainMatrix.from_Matrix(m).convert_to(nt.GOLDEN_FIELD).to_dense()


# Two Golden births, genuine reset/copy. No zero-blank assumption.
a, p = nt.A, nt.P
v = sp.Matrix([a, p])
e0, e1 = sp.eye(2)[:, 0], sp.eye(2)[:, 1]
reset = z(2, (3, 4)) + (nt.Gate("G", (2,)),) + z(2, (3, 4))
prefix = execution(5, reset + (cx(1, 2),))
assert len(prefix.gates) + 2 == 20
pre = nt.word_matrix(prefix, max_qubits=5, max_expanded_stages=18)
def insert(bits):
    return sp.kronecker_product(sp.eye(2), bits, sp.eye(4))
isometry = over_field(pre) * over_field(insert(sp.kronecker_product(v, v)))
flag_pair = a*sp.kronecker_product(e0,e0) + p*sp.kronecker_product(e1,e1)
assert isometry == over_field(insert(flag_pair))

# Actual x distinct from port. Test all 16 incoming columns on both bodies.
z1 = z(1, (2, 3))
g1 = (nt.Gate("G", (1,)),)
words = (execution(4, (cx(0,1),)*18), execution(4, g1+z1+g1+z1))
assert [Counter(g.op for g in w.gates) for w in words] == [
    Counter(CX=18), Counter(G=2, CX=12, SourceI=4)]
for w in words:
    assert nt.exact_matrix_equal(nt.word_matrix(w, max_qubits=4, max_expanded_stages=18), sp.eye(16))

# Internal gauges of each slot, retaining every intermediate column.
identity = over_field(sp.eye(16))
def prefixes(w):
    mats = {g: over_field(nt.gate_matrix(w,g)) for g in set(w.gates)}
    trajectory = [identity]
    for g in w.gates:
        trajectory.append(mats[g]*trajectory[-1])
    return trajectory, [mats[g] for g in w.gates]
left, fl = prefixes(words[0])
right, fr = prefixes(words[1])
gauge = [b*a_.transpose() for a_,b in zip(left,right)]
assert gauge[0] == gauge[18] == identity
assert all(vv.transpose()*vv == identity for vv in gauge)
assert all(gauge[i+1]*fl[i] == fr[i]*gauge[i] for i in range(18))

# Four complete configurations. Positive quantities are complete effect masses.
m00, m01, m10, m11, scale, address0, address1 = sp.symbols(
    "m00 m01 m10 m11 s address0 address1", positive=True)
m = [[m00,m01],[m10,m11]]
odds = {(i,j): m[1][j]/m[0][i] for i,j in product(range(2), repeat=2)}
assert sp.cancel(odds[0,0]*odds[1,1]-odds[0,1]*odds[1,0]) == 0
sub = {m00:address0,m01:address0*scale**4,m10:address1,m11:address1*scale**4}
assert sp.cancel((odds[0,1]/odds[1,0]).subs(sub)-scale**8) == 0
assert sp.simplify(sp.diff(sp.log(scale**8),scale)-8/scale) == 0
print("PASS: paid flag on 8 old columns; both 18-call words on 16 columns; all prefix gauges; four measured address configurations and crossed odds.")
