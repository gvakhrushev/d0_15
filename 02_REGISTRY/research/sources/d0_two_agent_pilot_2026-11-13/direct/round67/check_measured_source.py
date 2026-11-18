"""Exact readout projectors before and after an independent paid back-leg sign."""
from hashlib import sha256
from collections import Counter
import importlib.util
from pathlib import Path
import sys

import sympy as s
from sympy.polys.matrices import DomainMatrix

root = Path(__file__).resolve().parents[6]
history = root / "02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py"
assert sha256(history.read_bytes()).hexdigest() == "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
spec = importlib.util.spec_from_file_location("measured_native", history)
nt = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = nt
spec.loader.exec_module(nt)


def field(matrix):
    return DomainMatrix.from_Matrix(matrix).convert_to(nt.GOLDEN_FIELD).to_dense()


def scalar(value):
    return field(value * s.eye(4))


p, a = nt.P, nt.A
u, d = (a + p) / 2, (a - p) / 2
tensor = s.kronecker_product
v = s.Matrix([a, p])
incoming = field(tensor(s.eye(4), v, v, v, v))
masks = [field(tensor(s.eye(16), s.diag(*mask)))
         for mask in ((1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))]
port, bank, report, tail = 2, 3, 4, 5


def cx(control, target):
    return nt.Gate("CX", (control, target))


sign = nt.Gate("SourceI", (port, 0, 1))
# The auxiliary WORK may be dirty. Route the actual sign through a real SWAP.
move = (cx(port, bank), cx(bank, port), cx(port, bank))
sign_work = (*move, sign, sign, *move)
toggle = (cx(port, bank),)
identity = (*sign_work, *sign_work, *toggle, *toggle)
commutator = (*sign_work, *toggle, *sign_work, *toggle)
assert Counter(identity) == Counter(commutator)
def full_matrix(gates):
    program = nt.Execution(6, (), (), gates, nt.G_CX_SOURCE_I, port, (0, 1))
    return field(nt.word_matrix(program, max_qubits=6))

assert full_matrix(identity) == field(s.eye(64))
assert full_matrix(commutator) == full_matrix((sign, sign))

for active, event in ((cx(bank, port), 2*p**3), (cx(port, bank), p**2)):
    x = 1 - 2*event
    for kick in (False, True):
        back_gates = commutator if kick else identity
        gates = (active, cx(port, report), sign, sign, *back_gates,
                 active, cx(report, tail), nt.Gate("G", (tail,)), cx(report, tail))
        program = nt.Execution(6, (), (), gates, nt.G_CX_SOURCE_I, port, (0, 1))
        final = field(nt.word_matrix(program, max_qubits=6)) * incoming
        assert masks[2] * final == field(s.zeros(64, 4))
        for mask, eps, delta in zip(masks, (1, -1), (p, p*a)):
            q = (1 + eps*p**3*x)/2
            columns = mask * final
            assert columns.transpose() * columns == scalar(q)
            predicted = delta * (u + eps*d*x if kick else u*x + eps*d)
            compressed = incoming.transpose() * columns
            assert compressed == scalar(predicted)
            # RC3 uses the range projection, including its inverse Gram.
            assert compressed * compressed.transpose() == scalar(predicted**2)
            base = (u*x + eps*d)**2
            shifted = (u + eps*d*x)**2
            assert field(s.Matrix([[shifted - base - a*p*(1-x*x)]])) == field(s.zeros(1, 1))

assert field(s.Matrix([[u**2-d**2-a*p]])) == field(s.zeros(1, 1))

# Two canonical flags have equal success masses at 01 and 10 on every geometry.
# Their first measured bit is copied into a fresh, retained WORK register.
prob = (p, p**2)
amplitudes = (a, p)
successes = ((0, 1), (1, 0))
balance = sum(prob[i]*prob[j]*(1-2*i) for i, j in successes)
compression = sum(prob[i]*prob[j]*amplitudes[i]**2 for i, j in successes)
assert scalar(balance) == scalar(0)
assert scalar(compression) == scalar(p**3)


def active_count(word, e, y):
    port_value, work_value = e, y
    count = 0
    for gate in word:
        if gate == sign:
            count += port_value
        elif gate == cx(port, bank):
            work_value ^= port_value
        elif gate == cx(bank, port):
            port_value ^= work_value
        else:
            raise ValueError(gate)
    assert (port_value, work_value) == (e, y)
    return count


for e in (0, 1):
    for i, j in successes:
        extra = active_count(commutator, e, i) - active_count(identity, e, i)
        assert extra == 2*e*(1-2*i)
        assert scalar(prob[i]*prob[j]*extra) == scalar(2*p**3*e*(1-2*i))

# Analytic monotonicity for every matched event and both printer weights.
x, k, u, d = s.symbols("x k u d", real=True)
for eps in (1, -1):
    raw = 2*(u*x + eps*d)**2/(1 + eps*k*x)
    assert s.simplify(s.diff(raw, x, 2) - 4*(u-k*d)**2/(1+eps*k*x)**3) == 0
    assert s.simplify(s.diff(raw, x).subs(x, 0) - 2*eps*d*(2*u-k*d)) == 0

# Independent-preparation derivative in a real rotation example at a matched centre.
theta, left = s.symbols("theta left", real=True)
# A(theta) rotates a fixed real input by theta. The back leg can move alone.
for eps in (1, -1):
    numerator = u*s.cos(left+theta) + eps*d*s.cos(left-theta)
    assert s.simplify(s.diff(numerator, left).subs(left, theta) + u*s.sin(2*theta)) == 0

# One conditional branch rotated by a native positive-rank isometry.
# Reach defect at the passive optimum is the squared sine, also for ancillas.
v0 = s.Matrix([s.Rational(3,5), s.Rational(4,5)])
proj = v0*v0.T
j0 = s.Matrix([1,0])
assert 1-(j0.T*proj*j0)[0] == ((s.eye(2)-proj)*j0).norm()**2
for b in (p, p**3):
    assert field(s.Matrix([[b*(1-(j0.T*proj*j0)[0])]])) == field(s.Matrix([[b*s.Rational(16,25)]]))
print("PASS measured H.1: actual native forward and back words, exact bit effects and range compressions; convexity, recovery defect, and sign-kick identity.")
