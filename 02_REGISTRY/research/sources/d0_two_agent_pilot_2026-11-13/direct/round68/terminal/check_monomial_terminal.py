"""Reconstruct the two terminal masses with the A67 six-wire native reader."""
from hashlib import sha256
import importlib.util
from pathlib import Path
import sys

import sympy as sp
from sympy.polys.matrices import DomainMatrix


root = Path(__file__).resolve().parents[7]
source = root / "02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py"
assert sha256(source.read_bytes()).hexdigest() == "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
spec = importlib.util.spec_from_file_location("monomial_native", source)
nt = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = nt
spec.loader.exec_module(nt)


def golden(matrix):
    return DomainMatrix.from_Matrix(matrix).convert_to(nt.GOLDEN_FIELD).to_dense()


def scalar(value):
    return golden(value * sp.eye(4))


def amp(value):
    return nt.GOLDEN_FIELD.from_sympy(sp.sympify(value))


def cx(control, target):
    return nt.Gate("CX", (control, target))


p, a = nt.P, nt.A
port, work, report, tail = 2, 3, 4, 5
source_i = nt.Gate("SourceI", (port, 0, 1))
toggle = cx(port, work)
active = cx(work, port)
move = (toggle, active, toggle)
zwork = (*move, source_i, source_i, *move)
base = (*zwork, *zwork, toggle, toggle)
kick = (*zwork, toggle, *zwork, toggle)
pre = (active, cx(port, report), source_i, source_i)
post = (active, cx(report, tail), nt.Gate("G", (tail,)), cx(report, tail))
layout = nt.Execution(6, (), (), pre + base + post, nt.G_CX_SOURCE_I, port, (0, 1))
nt.validate_execution(layout, max_qubits=6, max_expanded_stages=32)
mats = {gate: golden(nt.gate_matrix(layout, gate)) for gate in set(layout.gates)}
v = sp.Matrix([a, p])
tensor = sp.kronecker_product
incoming = golden(tensor(sp.eye(4), v, v, v, v))
masks = ((1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
projectors = [golden(tensor(sp.eye(16), sp.diag(*mask))) for mask in masks]
address_law = ((0, 0, p**2), (0, 1, p**4), (1, 0, p**3), (1, 1, p**3))


def identity4_coefficient(block):
    value = block.to_list()[0][0]
    assert block == scalar(nt.GOLDEN_FIELD.to_sympy(value))
    return value


def output(word, weight):
    port_weight = golden(tensor(sp.eye(4), sp.diag(1, weight), sp.eye(8)))
    weighted_source = port_weight * mats[source_i]
    columns = incoming
    for gate in pre:
        columns = mats[gate] * columns
    for gate in word:
        matrix = weighted_source if gate == source_i else mats[gate]
        columns = matrix * columns
    for gate in post:
        columns = mats[gate] * columns
    assert (projectors[2] * columns).is_zero_matrix
    return [projector * columns for projector in projectors[:2]]


for weight in (sp.Integer(1), p):
    masses = {}
    overlaps = {}
    for name, word in (("P", base), ("K", kick)):
        columns = output(word, weight)
        masses[name] = [identity4_coefficient(col.transpose() * col) for col in columns]
        overlaps[name] = [identity4_coefficient(incoming.transpose() * col) for col in columns]
        for b in (0, 1):
            theta = (a, p) if b == 0 else (p, a)
            delta = (p, a*p)[b]
            norm = passive = 0
            for e, y, probability in address_law:
                count = 4*y if name == "P" else 2*(y + (y^e))
                modulus = weight**count
                sign = (-1)**e if name == "P" else 1
                norm += probability * theta[e]**2 * modulus**2
                passive += probability * theta[e] * modulus * sign
            assert masses[name][b] == amp(norm)
            assert overlaps[name][b] == amp(delta * passive)

    for b, click in ((0, p**2), (1, p)):
        assert masses["P"][b] - masses["K"][b] == amp(p**3 * (1 - weight**4)**2 * click)
    mp, mk = (sum(masses[name], nt.GOLDEN_FIELD.zero) for name in ("P", "K"))
    fp, fk = masses["P"][1] / mp, masses["K"][1] / mk
    assert (amp(p) - fk) * mk == (amp(p) - fp) * mp
    if weight == 1:
        assert mp == mk == amp(1) and fp == fk == amp(p**2 + 2*p**6)
        for b, delta in ((0, p), (1, p*a)):
            diff = (overlaps["K"][b]**2 - overlaps["P"][b]**2) / masses["P"][b]
            assert diff * masses["P"][b] == amp(delta**2 * a*p * (1 - (1 - 4*p**3)**2))
            assert nt.GOLDEN_FIELD.to_sympy(diff) > 0
    else:
        assert mp == amp(p + p**10)
        assert mk == amp(p**2 + 2*p**7 + p**12)
        assert nt.GOLDEN_FIELD.to_sympy(mp - mk) > 0

# On the measured flags, f=q fixes the full mass from the e=0 sector alone.
Q, r, k = sp.symbols("Q r k", real=True)
q = p**2 + p**3 * Q
assert sp.simplify(p - q - (p - p**2)*(1 - Q)) == 0
background, excited = sp.symbols("background excited", positive=True)
total = (1 - Q)*background + Q*excited
clicked = p**2*(1 - Q)*background + p*Q*excited
assert sp.simplify(clicked - q*total - (p - p**2)*Q*(1-Q)*(excited-background)) == 0

# Normal, noncommuting old-memory transports and a nonnormal positive-factor pair.
def hs_squared(matrix):
    return sp.trace(matrix.adjoint() * matrix)


def contrast(left, right):
    return (hs_squared(left*left) + hs_squared(right*right)
            - hs_squared(left*right) - hs_squared(right*left))


u = sp.diag(2, 1)
v = sp.Matrix([[2, 1], [1, 2]])
assert u*v != v*u and u.is_positive_definite and v.is_positive_definite
assert contrast(u, v) == hs_squared(u*u - v*v) > 0
assert contrast(u*v, v*u) == -26

# Two moving tariff ratios and a geometric change in the normalized mass ratio.
mratio = (1 + (k+r)*Q) / (1 + k*Q)
den = (1 + k*Q) * (1 + (k+r)*Q)
for variable, numerator in ((Q, r), (r, Q*(1 + k*Q)), (k, -r*Q**2)):
    assert sp.cancel(sp.diff(sp.log(mratio), variable) - numerator / den) == 0

print("PASS: both 18-stage words, both absolute masses and passive amplitudes, noisy readouts, calibrated background, and moving tariffs")
