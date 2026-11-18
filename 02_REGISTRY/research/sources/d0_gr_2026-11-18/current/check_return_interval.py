"""Verify the LC1 unread-tail control on the original six-wire gate implementation."""

from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from types import ModuleType

import mpmath as mp
import sympy as sp

root = Path(__file__).resolve().parent
owner = root / "source" / "native_execution.py"
revision = "15f5b786ed912a0e91d660e337bf60a7c15c7cfa"
owner_path = "02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py"
source = owner.read_bytes() if owner.is_file() else subprocess.check_output(
    ["git", "-C", str(root), "show", f"{revision}:{owner_path}"]
)
if hashlib.sha256(source).hexdigest() != "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c":
    raise ValueError("unexpected native gate implementation")
ne = ModuleType("pinned_return_interval_gates")
sys.modules[ne.__name__] = ne
exec(compile(source, owner_path, "exec"), ne.__dict__)


def verify(condition, message):
    if not condition:
        raise ValueError(message)


def cx(i, j):
    return ne.Gate("CX", (i, j))


src, reader, tail = 0, 4, 5
g = ne.Gate("G", (tail,))
switch = cx(reader, tail)
swap = (cx(src, tail), cx(tail, src), cx(src, tail))
z = swap + (ne.Gate("SourceI", (src, 1, 2)),) * 2 + swap


def execution(word):
    return ne.Execution(6, (3, 4, 5), (), tuple(word), ne.G_CX_SOURCE_I, src, (1, 2), ())


def native_matrix(gate):
    return ne.gate_matrix(execution((gate,)), gate)


Z = sp.eye(64)
for gate in z:
    Z = native_matrix(gate) * Z
G = native_matrix(g)
D = native_matrix(switch)
verify(Z == sp.diag(*([1, -1] * 32)), "routed Z changed a spectator")
verify(Z * G * Z == G.T, "Z did not invert the addressed G")
verify(G == sp.kronecker_product(sp.eye(32), ne.G_LOCAL), "incorrect G address")
for j in range(64):
    verify(D[j ^ ((j >> 1) & 1), j] == 1, "incorrect reader control")


def word(n, width):
    # Printed chronologically. The rightmost factor of a matrix acts first.
    h = z + (g,) * (width - n) + z + (g,) * (width + n)
    return (switch,) + h + (switch,) + h


for width in (3, 21, 100):
    reference = Counter(word(0, width))
    for n in range(width + 1):
        w = word(n, width)
        ne.validate_execution(execution(w), max_qubits=6, max_expanded_stages=len(w) + 1)
        verify(Counter(w) == reference and len(w) == 4 * width + 34, "inventory changed")

# Symbolic all-n verification. A unit-modulus complex scalar stores a real
# plane rotation; conjugation by X or Z reverses its exponent.
n, width = sp.symbols("n N", integer=True)
h_exponent = (width + n) - (width - n)
for b in (0, 1):
    verify(sp.expand(h_exponent + (-1) ** b * h_exponent) == (4*n if b == 0 else 0), "sector exponent")

# The irrationality proof in the note uses the conjugate of 2cos(2 theta).
p_exact = (sp.sqrt(5) - 1) / 2
two_cos = sp.expand(2 * (p_exact - p_exact**2))
verify(sp.simplify(two_cos - (2*sp.sqrt(5)-4)) == 0, "Golden conjugate")
verify(-2*sp.sqrt(5)-4 < -2, "root-of-unity exclusion")

mp.mp.dps = 70
p = (mp.sqrt(5) - 1) / 2
theta = mp.asin(p)
q = p**2 + p**3 * 4 * mp.sin(512 * theta)**2 * p**7
A, B = mp.sqrt(p * (1 - q)), mp.sqrt(p**3 * q)
upper = (A+B)**2
upper_prime = (A+B)*(-A/(1-q) + B/q)
code_prime = 1 + mp.log(q/(1-q))/mp.log(1/p)
verify(mp.mpf(".41246") < q < mp.mpf(".41248") and A > B and upper_prime < 0 and code_prime > mp.mpf(".26"), "original centre")
targets = [mp.mpf(0), upper/3, upper]
errors = {}
for width in (64, 256, 1024, 4096):
    values = [(A*mp.cos(4*n*theta) + B)**2 for n in range(width+1)]
    errors[width] = [float(min(abs(x-s) for x in values)) for s in targets]
verify(max(errors[4096]) < .001 and errors[4096][0] < 1.e-6, "target approximation")

# At a switch of minimizers the envelope has different one-sided derivatives.
t, s0, s1 = sp.symbols("t s0 s1", real=True)
price = (t-s0)**2*(s1-t)
verify(sp.diff(price,t).subs(t,s0) == 0, "interior derivative")
verify(sp.simplify(sp.diff(price,t).subs(t,s1) + (s1-s0)**2) == 0, "boundary derivative")
print(json.dumps({"status":"PASS", "q":float(q), "cold_squared_upper":float(upper),
                  "upper_derivative":float(upper_prime), "parsed_derivative":float(code_prime),
                  "native_wires":6, "paid_steps":"4N+34", "target_errors":errors,
                  "full_physical_price_identified":False}, indent=2))
