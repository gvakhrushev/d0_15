"""Verify the source pins, one-tag instrument, CQ decompositions and price bounds."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import subprocess

import sympy as sp


root = Path(__file__).resolve().parents[7]
archive = "4f99c2c46e646d21ae5b9b0491da17bd1b094da0"
book_dir = "99_PRESERVED_SOURCE/D0_MAIN_GOLDEN_PASS30/books"
sources = {
    "BOOK_I_ARCHITECTURE": ("87bf55debc4296b0574db1d0045156b350f2dd1e17fcc01d3e3ad5bb9a980fe9", 417, "EncLen"),
    "BOOK_II_MECHANISM": ("42224fdbfb6e474e2025d38da45d01bf1c9e17132c182e82d8875868df62c9b0", 777, "Info"),
    "BOOK_III_SPECTRUM": ("03f648854e4e295dc33c5cf8a77e87fcad8e6bb6d68322511df68461cb357ebe", 797, "BRIDGE"),
}
for book, (digest, line, fragment) in sources.items():
    path = f"{archive}:{book_dir}/{book}_GOLDEN_PASS30.txt"
    data = subprocess.check_output(["git", "show", path], cwd=root)
    assert sha256(data).hexdigest() == digest
    assert fragment in data.decode().splitlines()[line - 1]

# Reduce the native 2x2 matrices exactly in Q[sqrt(p)].
a = sp.Symbol("a")
relation = a**4 + a**2 - 1
p = a**2
s = p**6
c = 2*a*p


def reduce(value):
    return sp.rem(sp.expand(value), relation, a)


G = sp.Matrix([[a, -p], [p, a]])
Z = sp.diag(1, -1)
X = sp.Matrix([[0, 1], [1, 0]])
v = sp.Matrix([a, p])
inverse = Z*G*Z
for bit, expected in ((0, sp.Matrix([1, 0])), (1, sp.Matrix([c, p**3]))):
    assert all(reduce(x) == 0 for x in inverse*(X**bit)*v - expected)
assert reduce(1 - s - 4*p**3) == reduce(c*c + s - 1) == 0

# Exact probability-law calculation at an arbitrary interior success rate.
# The conclusions use arbitrary s symbolically; here every record on both
# supports is also checked with nontrivial old conditional spectra.
q = F(2, 5)
success = F(1, 17)
for m in range(1, 7):
    first, second, pair = ({}, {}), ({}, {}), ({}, {})
    for b, flags in product((0, 1), product((0, 1), repeat=m)):
        prob = success**sum(flags) * (1-success)**(m-sum(flags))
        record = tuple((1, 0) if not u else ((0, 0) if b == 0 else (1, 1))
                       for u in flags)
        left, right = zip(*record)
        for law, key in ((first[b], left), (second[b], right), (pair[b], record)):
            law[key] = law.get(key, F(0)) + prob
    assert len(first[0]) == len(second[1]) == 2**m
    assert first[1] == {(1,)*m: 1} and second[0] == {(0,)*m: 1}
    ambiguous = pair[0].keys() & pair[1].keys()
    assert ambiguous == {((1, 0),)*m}
    key = next(iter(ambiguous))
    assert pair[0][key] == pair[1][key] == (1-success)**m
    old0, old1 = ((1-q)*F(1, 3), (1-q)*F(2, 3)), (q*F(1, 4), q*F(3, 4))
    spectrum = [x*w for old, cond in ((old0, second[0]), (old1, second[1]))
                for x in old for w in cond.values()]
    assert sum(spectrum) == 1 and len(spectrum) == 2 + 2*(2**m)

# Enclose log(phi) by 2 atanh(p^3), bounding its positive Taylor tail.
lo, hi = F(6180, 10000), F(6181, 10000)
assert lo**2+lo < 1 < hi**2+hi
t0, t1 = lo**3, hi**3
low_log = 2*(t0 + t0**3/3 + t0**5/5)
high_log = 2*(t1+t1**3/3+t1**5/5+t1**7/(7*(1-t1*t1)))
assert F(48, 100) < low_log < high_log < F(482, 1000)
shi = F(57, 1000)
assert hi**6 < shi
lower_A = (1-shi)*(1+shi/2)
assert 6 + lower_A/high_log > F(801, 100)
assert 6 + 1/low_log < F(81, 10)

# Check the disjoint, prefix-free interval construction with rational split
# probabilities. The golden proof uses weights p and p^2 on the same tree.
probabilities = (F(1, 19), F(3, 19), F(8, 19), F(7, 19))
small, big = F(2, 5), F(3, 5)
start = F(0)
words = []
for mass in probabilities:
    midpoint = start + mass/2
    left, width = F(0), F(1)
    word = ""
    while width > mass/2:
        split = left + big*width
        if midpoint < split:
            width *= big
            word += "0"
        else:
            left = split
            width *= small
            word += "10"
    assert start <= left < left+width <= start+mass
    assert small*mass/2 < width <= mass/2
    words.append(word)
    start += mass
assert not any(i != j and x.startswith(y)
               for i, x in enumerate(words) for j, y in enumerate(words))
print("PASS: three source books, native one-tag columns, full CQ sectors, "
      "8.01 < threshold < 8.1, separated golden token code.")
