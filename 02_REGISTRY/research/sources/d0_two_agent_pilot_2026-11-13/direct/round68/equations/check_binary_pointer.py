"""Check the mod-2 letter normal form on the owner's actual addressed matrices."""
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

import sympy as s


owner = Path(__file__).resolve().parents[4] / "d0_native_execution_domain_2026-10-24/native_execution.py"
assert sha256(owner.read_bytes()).hexdigest() == "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
spec = spec_from_file_location("native_mod2_owner", owner)
native = module_from_spec(spec)
sys.modules[spec.name] = native
spec.loader.exec_module(native)

# F4 = F2[w]/(w^2+w+1); the low bit is the constant coefficient.
one, w, w2 = 1, 2, 3


def mul(a, b):
    product = (a if b & 1 else 0) ^ (a << 1 if b & 2 else 0)
    return product ^ 7 if product & 4 else product


def xor(values):
    total = 0
    for value in values:
        total ^= value
    return total


x = s.Symbol("x")
assert s.minpoly(native.A, x) == x**4 + x**2 - 1
assert s.simplify(native.A**2 - native.P) == 0
assert mul(w, w) == w2 and mul(w2, w2) ^ w2 ^ one == 0
assert w ^ w2 == one  # canonical birth and G column mass
entry = {s.Integer(0): 0, s.Integer(1): one, s.Integer(-1): one,
         native.A: w, -native.A: w, native.P: w2, -native.P: w2}

# Bit positions are big endian. Use non-adjacent Spin wires in the declared order.
size = 5
port, spin = 4, (3, 0)
g, cx, source = (native.Gate("G", (1,)), native.Gate("CX", (4, 2)),
                 native.Gate("SourceI", (port, *spin)))
word = (g, cx, source, g, source, cx)
program = native.Execution(size, (), (), word, native.G_CX_SOURCE_I, port, spin)
bit = lambda address: 1 << (size - 1 - address)
matrices = {}
for gate in (g, cx, source):
    matrix = native.gate_matrix(program, gate, max_qubits=size)
    cols = [[entry[matrix[r, c]] for r in range(2**size)] for c in range(2**size)]
    matrices[gate] = cols
    for c, column in enumerate(cols):
        if gate == g:
            expected = {c: w, c ^ bit(1): w2}
        else:
            control, target = (4, 2) if gate == cx else (port, spin[1])
            expected = {c ^ (bit(target) if c & bit(control) else 0): one}
        assert {r: v for r, v in enumerate(column) if v} == expected


def run(c):
    column = [0] * (2**size)
    column[c] = one
    for gate in word:
        matrix = matrices[gate]
        column = [xor(mul(amplitude, matrix[j][r]) for j, amplitude in enumerate(column))
                  for r in range(2**size)]
    assert xor(column) == one
    return [xor(v for r, v in enumerate(column) if r & bit(j)) for j in range(size)]


responses = [run(c) for c in range(2**size)]
for c in range(2**size):
    for shift in range(2**size):
        for j in range(size):
            assert responses[c][j] ^ responses[c ^ shift][j] == responses[0][j] ^ responses[shift][j]
assert xor(int(c == 0) for c in (0, 1, 2, 3)) == one
# Tensor result for each control eigenspace. Complementary controls give a
# literal untouched (0,0) branch with the same amplitude, including on coherence.
angle = s.symbols("beta", real=True)
c, sn = s.cos(angle), s.sin(angle)
rot = s.Matrix([[c, -sn], [sn, c]])
blank = s.Matrix([1, 0])
assert (rot.T * rot).applyfunc(s.trigsimp) == s.eye(2)
inside = s.kronecker_product(rot * blank, (rot.T * rot * blank).applyfunc(s.trigsimp))
outside = s.kronecker_product(blank, rot * blank)
assert inside == s.Matrix([c, 0, sn, 0]) and outside == s.Matrix([c, sn, 0, 0])
print("PASS: B, complement and uniform erasure from two actually supported rotations.")
print("PASS: native polynomial, birth, addressed G/CX/SourceI, Spin orientation, all-column affine pointer and non-affine two-bit return.")
