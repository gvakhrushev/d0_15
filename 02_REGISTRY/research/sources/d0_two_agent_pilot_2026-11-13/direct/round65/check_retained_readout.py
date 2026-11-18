"""Exact native columns for a two-tag readout and its complete recorded price."""
from hashlib import sha256
from fractions import Fraction
from heapq import heapify, heappop, heappush
import importlib.util
from itertools import product
from math import comb
from pathlib import Path
import sys

import sympy as sp
from sympy.polys.matrices import DomainMatrix


root = Path(__file__).resolve().parents[6]
source = root / "02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py"
assert sha256(source.read_bytes()).hexdigest() == "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
spec = importlib.util.spec_from_file_location("native_retained_reader", source)
nt = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = nt
spec.loader.exec_module(nt)


def cx(control, target):
    return nt.Gate("CX", (control, target))


def z_on_tag(tag, spin):
    swap = (cx(0, tag), cx(tag, 0), cx(0, tag))
    return swap + (nt.Gate("SourceI", (0, *spin)),) * 2 + swap


def field(matrix):
    return DomainMatrix.from_Matrix(matrix).convert_to(nt.GOLDEN_FIELD).to_dense()


def exact_scalar(lhs, rhs):
    return field(sp.Matrix([[lhs]])) == field(sp.Matrix([[rhs]]))


a, p = nt.A, nt.P
yes, erase = p**3, 2*a*p
v = sp.Matrix([a, p])
eye = sp.eye
tensor = sp.kronecker_product
product_tags = tensor(v, v)
zero, one = sp.diag(1, 0), sp.diag(0, 1)
expected = (yes*zero, sp.zeros(2), erase*eye(2), yes*one)
# Cover both a report on PORT and a report on a distinct live WORK wire.
for report in (0, 1):
    first, second = report+1, report+2
    spin = (report+3, report+4)
    width = report+5
    z2 = z_on_tag(second, spin)
    g1, g2 = nt.Gate("G", (first,)), nt.Gate("G", (second,))
    gates = (cx(report, first), cx(report, second), g1) + z2 + (g2,) + z2
    program = nt.Execution(width, (), (), gates, nt.G_CX_SOURCE_I, 0, spin)
    assert len(gates) == 20
    old_width = 2**(report+1)
    birth = field(tensor(eye(old_width), product_tags, eye(4)))
    columns = field(nt.word_matrix(program, max_qubits=width)) * birth
    for tag, block in enumerate(expected):
        projection = tensor(eye(old_width), eye(4)[tag, :], eye(4))
        assert field(projection)*columns == field(tensor(eye(2**report), block, eye(4)))
assert exact_scalar(yes**2 + erase**2, 1)
assert exact_scalar((product_tags.T*tensor(sp.Matrix([p,a]), sp.Matrix([p,a])))[0], erase**2)

# The optional parity wrapper acts on each matrix block (new bit y, old bit x).
X = sp.Matrix([[0, 1], [1, 0]])
for old in range(2):
    for new in range(2):
        marker = X**(old ^ new)*v
        recorded = tensor(nt.G_LOCAL*marker, nt.G_LOCAL.T*marker)
        target = sp.Matrix([yes*int(old == new), 0, erase, yes*int(old != new)])
        assert field(recorded) == field(target)

# Conditional record on an arbitrary earlier CQ block is a classical split.
q, s = sp.symbols("q s", positive=True)
masses = ((1-q)*s, (1-q)*(1-s), q*(1-s), q*s)
assert sp.expand(sum(masses)-1) == 0
length = sum(prob*size for prob, size in zip(masses, (2, 3, 3, 4)))
assert sp.expand(length - (3 + s*(2*q-1))) == 0
assert sp.diff(length, q).expand() == 2*s
for old_prob, mass_yes, mass_erase in ((1-q, masses[0], masses[1]), (q, masses[3], masses[2])):
    assert sp.cancel(mass_yes/old_prob) == s
    assert sp.cancel(mass_erase/old_prob) == 1-s


def optimal_lengths(weights):
    heap = [(weight, (i,)) for i, weight in enumerate(weights)]
    heapify(heap)
    lengths = [0]*len(weights)
    while len(heap) > 1:
        left, leaves_left = heappop(heap)
        right, leaves_right = heappop(heap)
        merged = leaves_left + leaves_right
        for leaf in merged:
            lengths[leaf] += 1
        heappush(heap, (left + right, merged))
    return lengths


def mean_length(law, lengths):
    assert len(law) == len(lengths)
    return sum(mass*size for mass, size in zip(law, lengths))


for repeat in range(1, 7):
    for success in (Fraction(1, 18), Fraction(1, 2)):
        law = [success**sum(flags)*(1-success)**(repeat-sum(flags))
               for flags in product((0, 1), repeat=repeat)]
        base = mean_length(law, optimal_lengths(law))
        for prob in (Fraction(2, 5), Fraction(1, 2)):
            weights = [factor*mass for factor in (1-prob, prob) for mass in law]
            lengths = optimal_lengths(weights)
            ell0 = mean_length(law, lengths[:len(law)])
            ell1 = mean_length(law, lengths[len(law):])
            assert min(ell0, ell1) >= base
            assert (1-prob)*ell0 + prob*ell1 <= base + 1
            assert -1/(1-prob) <= ell1-ell0 <= 1/prob

def clock_contrast(repeat, success, tariff):
    centre = 25*repeat
    return sum(comb(repeat, count)*success**count*(1-success)**(repeat-count)
               * (tariff(centre+count) - tariff(centre-count)) for count in range(repeat+1))


success = Fraction(1, 18)
for repeat in (1, 2, 24):
    assert clock_contrast(repeat, success, lambda t: t) == 2*repeat*success
    assert clock_contrast(repeat, success, lambda t: t*t) == 4*(25*repeat)*repeat*success
    assert clock_contrast(repeat, success, lambda t: int(t >= 25*repeat+1)) > 0
lower = Fraction(617,1000)
assert lower*lower + lower < 1 and 48*lower**8 > 1
print("PASS: native retained reader, all protected columns and parity blocks, full CQ split, printed source, optimal-code bound and 24-pair clock criterion.")
