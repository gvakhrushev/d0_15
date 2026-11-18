"""Two literal pre-sign programmes on the same six wires and the same printer."""
from hashlib import sha256
import importlib.util
from pathlib import Path
import sys

import sympy as sp
from sympy.polys.matrices import DomainMatrix


root = Path(__file__).resolve().parents[6]
source = root / "02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py"
assert sha256(source.read_bytes()).hexdigest() == "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
spec = importlib.util.spec_from_file_location("gap_native", source)
nt = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = nt
spec.loader.exec_module(nt)


def field(matrix):
    return DomainMatrix.from_Matrix(matrix).convert_to(nt.GOLDEN_FIELD).to_dense()


def cx(control, target):
    return nt.Gate("CX", (control, target))


p, a = nt.P, nt.A
port, bank, report, tail = 2, 3, 4, 5
tensor = sp.kronecker_product
v = sp.Matrix([a, p])
incoming = field(tensor(sp.eye(4), v, v, v, v))
inner_mark = field(tensor(sp.eye(4), sp.diag(0,1), sp.eye(8)))
emit_one = field(tensor(sp.eye(16), sp.diag(0,0,1,0)))
invalid = field(tensor(sp.eye(16), sp.diag(0,0,0,1)))
cold_gates = []
for gate, event in ((cx(bank,port), 2*p**3), (cx(port,bank), p**2)):
    sign = nt.Gate("SourceI", (port,0,1))
    taps = (gate, cx(port,report), sign, sign, gate, cx(report,tail),
            nt.Gate("G", (tail,)), cx(report,tail))
    word = nt.Execution(6, (), (), taps, nt.G_CX_SOURCE_I, port, (0,1))
    active = field(nt.gate_matrix(word,gate))
    cold_gates.append(active)
    first = active*incoming
    assert first.transpose()*inner_mark*first == field(event*sp.eye(4))
    final = field(nt.word_matrix(word,max_qubits=6))*incoming
    assert final.transpose()*emit_one*final == field((p**2+p**3*event)*sp.eye(4))
    assert invalid*final == field(sp.zeros(64,4))

diff = cold_gates[0] - cold_gates[1]
gram = diff.transpose()*diff
assert gram*gram == field(3*sp.eye(64))*gram
assert gram.to_Matrix().trace() == 96  # 32 singular values sqrt(3), twice in the schedule.
assert 64*sp.sqrt(3) < 112
assert field(sp.Matrix([[2*p**6-p**5]])) == field(sp.Matrix([[p**8]]))
lower = sp.Rational(617,1000)
upper = sp.Rational(618034,1000000)
assert lower**2+lower < 1 < upper**2+upper
assert lower**8/6 > sp.Rational(1,300)
feedback_bound = 4*(upper**4 + upper**7)**24/(2**20 - 1)
heat_bound = sp.Rational(6*112, 359*256**24)
assert 2*upper**2 < 1
assert feedback_bound + heat_bound < sp.Rational(1,2**76)
print("PASS: two paid 64-column words, pre-sign and terminal effects on all Spin inputs, two changed clock stages, finite marked/graph price separation.")
