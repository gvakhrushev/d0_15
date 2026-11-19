"""Exact native paid relations and finite-dimensional controllability checks."""
import hashlib
import importlib.util
import sys
from collections import Counter
from pathlib import Path

import sympy as sp

default = Path(__file__).resolve().parents[1] / "primary" / "native_execution.py"
path = Path(sys.argv[1]) if len(sys.argv) > 1 else default
assert hashlib.sha256(path.read_bytes()).hexdigest() == "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c"
spec = importlib.util.spec_from_file_location("native_owner_paid_fibres", path)
native = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = native
spec.loader.exec_module(native)
spin1, spin2, bus, target, old = range(5)
s = native.Gate("SourceI", (bus, spin1, spin2))
c = native.Gate("CX", (target, bus))
reverse = native.Gate("CX", (bus, target))
swap = (c, reverse, c)
identity = sp.eye(32)

def mat(word):
    ex = native.Execution(5, (), (old,), tuple(word), native.G_CX_SOURCE_I, bus, (spin1, spin2))
    return native.word_matrix(ex, max_qubits=5, max_expanded_stages=40)

def pauli_z(q):
    return sp.kronecker_product(sp.eye(2**q), sp.diag(1, -1), sp.eye(2**(4-q)))

grouped = (c,c,s,s,s,s)
ordered = (c,s,s,c,s,s)
assert Counter(ordered) == Counter(grouped)
assert mat(grouped) == identity
assert mat(ordered) == pauli_z(target)
assert mat(swap + grouped + swap) == identity
assert mat(swap + ordered + swap) == pauli_z(bus)
assert mat((s,)*4) == mat((c,)*4) == identity
assert mat((reverse,)*2) == mat((c,)*2) == identity
for q, zq, length in [(bus,(s,s),6), (target,swap + (s,s) + swap,18)]:
    g = native.Gate("G", (q,))
    loop = (g,) + zq + (g,) + zq
    assert len(loop) == length
    assert native.exact_matrix_equal(mat(loop), mat((c,) * length))
g = native.Gate("G", (target,))
z_route = swap + (s,s) + swap
inv_g = z_route + (g,) + z_route
cells = [w + inv_g + w + (g,) for w in [grouped, ordered]]
assert len(cells[0]) == len(cells[1]) == 30
assert Counter(gate.op for gate in cells[0]) == Counter(CX=16,SourceI=12,G=2)
assert Counter(cells[0]) == Counter(cells[1])
assert native.exact_matrix_equal(mat(cells[0]), identity)
assert native.exact_matrix_equal(mat(cells[1]), mat((g,g)))
p = native.P
trace = sp.simplify(2*(p-p**2))
assert sp.simplify(trace - (2*sp.sqrt(5)-4)) == 0
assert trace.subs(sp.sqrt(5), -sp.sqrt(5)) < -2

def parity(integer):
    return bin(integer).count("1") % 2

def gf2_rank(columns):
    pivots = {}
    for col in columns:
        while col:
            pivot = col.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = col
                break
            col ^= pivots[pivot]
    return len(pivots)

for n in range(1, 7):
    d = 2**n
    pairs = [(x,z) for x in range(1,d) for z in range(1,d) if parity(x&z)]
    assert len(pairs) == d*(d-1)//2
    for x,z in pairs:
        kern = [u for u in range(1,d) if not parity(u&z)]
        columns = [x]
        for u in kern:
            if gf2_rank(columns + [u]) > len(columns):
                columns.append(u)
                if len(columns) == n:
                    break
        assert len(columns) == n and columns[0] == x
        assert [parity(z & col) for col in columns] == [1] + [0]*(n-1)
        assert all(parity(z&j) != parity(z&(j^x)) for j in range(d))
    if n <= 3:
        generators = []
        for x,z in pairs:
            m = sp.zeros(d)
            for j in range(d):
                m[j^x,j] = (-1)**parity(z&j)
            assert m.T == -m
            generators.append(m.reshape(d*d,1))
        assert sp.Matrix.hstack(*generators).rank() == d*(d-1)//2
print("PASS: native full-carrier 6/18-stage relations, 30-stage matched rotation, irrational angle, GF(2) conjugates through six bits and explicit Lie algebra ranks through three bits.")
